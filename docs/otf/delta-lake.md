---
layout: default
title: Delta Lake
nav_order: 2
---

# Delta Lake: Complete Technical Reference

---

## 1. What Is It & Why It Exists

### The Problem It Solves

Traditional data lakes built on raw object storage (S3, ADLS, GCS) store files — nothing more. There is no transaction coordinator, no schema registry, and no mechanism to guarantee that a reader sees a consistent snapshot while a writer is mid-flight. This produces a class of failure modes that are painful in production:

- **Dirty reads**: a downstream job reads a partially written partition because the writer failed halfway.
- **Lost updates**: two concurrent writers overwrite each other's output with no conflict detection.
- **Schema drift**: a pipeline adds a new column; all downstream consumers break silently or loudly.
- **No rollback**: a bad `DELETE` or `OVERWRITE` is permanent — the only recovery is restoring from a separate backup.
- **Small file explosion**: streaming or micro-batch workloads write thousands of tiny files, degrading Parquet read performance by orders of magnitude.

Delta Lake, open-sourced by Databricks in 2019, adds a **transaction log** on top of Parquet files stored in object storage. That single addition is enough to provide full ACID semantics, schema enforcement, schema evolution, time travel, and efficient upserts — all without moving data out of your own storage bucket.

### How It Fits into the Modern Data Stack

```mermaid
flowchart TD
    A["Orchestration Layer\nAirflow / Prefect / Databricks Workflows"]
    B["Compute / Query Engines\nApache Spark · Trino · Athena · Flink · Databricks"]
    C["Delta Lake Layer\n_delta_log/ JSON + Parquet checkpoints + data Parquet"]
    D["Object Storage / Lakehouse Storage\nS3 · ADLS Gen2 · GCS · HDFS"]

    A --> B
    B -->|reads/writes via Delta protocol| C
    C --> D
```

Delta Lake sits between compute and raw storage. It does not move data to a proprietary store — the underlying files are plain Parquet, readable by any engine that understands the Delta protocol. The catalog layer (Unity Catalog, Hive Metastore, AWS Glue) records table locations; the Delta log itself is the source of truth for table state.

### When to Choose Delta Lake Over Iceberg or Hudi

| Signal | Choose Delta Lake |
|---|---|
| Primary compute is Databricks or Spark on AWS EMR/Azure HDInsight | Strong native integration, Unity Catalog is first-class |
| You need Liquid Clustering (auto-optimized physical layout without upfront partition decisions) | Delta-only feature |
| Team wants SQL-first workflow with `MERGE`, `UPDATE`, `DELETE` maturity | Delta's DML support has been production-hardened the longest |
| You need Delta Sharing (open protocol for sharing live data across orgs without copying) | Delta-only |
| CDC / streaming ingestion is secondary to large analytical batch workloads | Delta excels; Hudi is stronger when CDC upsert rate dominates |
| You want to avoid the catalog complexity of Iceberg's REST catalog ecosystem | Delta's log-based approach is simpler to operate |

---

## 2. Core Architecture

### Internal File Layout

```
s3://my-bucket/warehouse/sales/
├── _delta_log/
│   ├── 00000000000000000000.json      ← commit 0  (CREATE TABLE)
│   ├── 00000000000000000001.json      ← commit 1  (INSERT batch 1)
│   ├── 00000000000000000002.json      ← commit 2  (INSERT batch 2)
│   ├── 00000000000000000009.json      ← commit 9  (DELETE)
│   ├── 00000000000000000010.checkpoint.parquet   ← checkpoint at v10
│   └── _last_checkpoint                           ← pointer to latest checkpoint
├── part-00000-3b3f1234-snappy.parquet
├── part-00001-9a2c5678-snappy.parquet
└── year=2024/month=01/
    ├── part-00000-abc123-snappy.parquet
    └── part-00001-def456-snappy.parquet
```

**Key components:**

- **`_delta_log/`**: The transaction log directory. Every committed transaction appends a new JSON file (numbered sequentially). Each JSON file is a set of *actions*.
- **Commit JSON files**: Contain `add`, `remove`, `metaData`, `protocol`, `commitInfo`, and `txn` actions. An `add` action records a new Parquet file path plus column statistics. A `remove` action tombstones a file (marks it logically deleted without immediately deleting bytes).
- **Checkpoint files** (`.checkpoint.parquet`): Every 10 commits (configurable), Delta consolidates the entire log state into a single Parquet file. A reader starting from scratch reads the latest checkpoint + only the JSON commits after it, instead of replaying the entire history.
- **`_last_checkpoint`**: A tiny JSON file pointing to the most recent checkpoint version, allowing readers to skip log scanning.
- **Data files**: Plain Snappy-compressed Parquet. No Delta-specific encoding — any Parquet reader can open them directly (though without transactional guarantees).

### Layer Relationship (ASCII Diagram)

```mermaid
flowchart TD
    RW["Reader / Writer\nSpark · Trino · Flink"]
    TL["Transaction Log - _delta_log/\n*.json + *.checkpoint\nActions: metaData, add, remove, commitInfo"]
    NC["New Commit JSON\n000...N.json\natomic PUT via S3/ADLS"]
    DF["Data Files - Parquet\nwritten before commit\nstaged in object store"]
    LS["Logical Table Snapshot version N\nall add actions minus all remove actions\nat the resolved version"]

    RW -->|resolve table version| TL
    RW -->|write new commit| NC
    RW -->|write data files| DF
    NC --> TL
    TL -->|reconstruct snapshot| LS
    DF --> LS
```

### Snapshot / Versioning Model

Every successful commit produces a new **version** (monotonically increasing integer). A snapshot at version *N* is the complete set of Parquet files that are in `add` state after replaying all log entries from 0 through *N* (or from the latest checkpoint before *N*).

Readers always work against an immutable snapshot. A reader that opened version 5 continues to see version 5 even if version 6, 7, 8 are committed while it runs. This is **snapshot isolation**.

Versions are retained until `VACUUM` physically deletes the underlying Parquet files referenced only by old `remove` actions. The default retention period is 7 days (`delta.deletedFileRetentionDuration`). Log files themselves are retained separately via `delta.logRetentionDuration` (default 30 days).

### ACID Transactions: Optimistic Concurrency

Delta Lake implements **optimistic concurrency control (OCC)**:

1. **Read phase**: The writer reads the current version of the log to determine the table state it will modify.
2. **Write phase**: The writer writes new Parquet data files to object storage (not yet visible — no commit entry exists yet).
3. **Commit attempt**: The writer attempts an **atomic PUT** of the next sequential JSON log file (e.g., `000...0012.json`). Object stores like S3 provide atomic PUT-if-not-exists semantics via conditional writes or via DynamoDB-backed locking in the case of S3 without native conditional writes.
4. **Conflict detection**: If another writer already committed `000...0012.json`, the current writer detects the conflict and either retries (if the conflict is in a non-overlapping partition) or aborts with a `ConcurrentModificationException`.

**Conflict resolution logic:**

- `APPEND` vs `APPEND`: always compatible — both succeed.
- `APPEND` vs `DELETE/UPDATE` on different partitions: compatible.
- `DELETE/UPDATE` vs `DELETE/UPDATE` on overlapping files: conflict — second writer retries or fails.
- `MERGE` with overlapping target files: conflict — second writer retries.

On AWS S3, Delta uses a **DynamoDB lock table** to emulate atomic rename semantics prior to S3 Express conditional writes. On Azure ADLS Gen2, Delta uses native atomic rename. On GCS, a similar lease mechanism is used.

```python
# Configure S3 with DynamoDB locking (required for true ACID on S3 standard)
spark = SparkSession.builder \
    .config("spark.delta.logStore.class",
            "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore") \
    .config("spark.io.delta.storage.S3DynamoDBLogStore.ddb.tableName",
            "delta_log_lock") \
    .config("spark.io.delta.storage.S3DynamoDBLogStore.ddb.region",
            "us-east-1") \
    .getOrCreate()
```

> **Note**: S3 now supports conditional writes natively (2024). The `S3DynamoDBLogStore` is still recommended for high-concurrency workloads until the native conditional write log store is fully production-hardened across all Delta versions.

---

## 3. Key Concepts Deep Dive

### Schema Evolution

Delta Lake enforces schema by default. Writing a DataFrame with a column that does not exist in the table schema raises an `AnalysisException`. Schema evolution must be explicitly enabled.

**Adding a column:**

```python
from delta.tables import DeltaTable

# Option 1: mergeSchema on write
df_new = spark.createDataFrame([
    (1, "Alice", "Engineering"),   # added 'department' column
], ["id", "name", "department"])

df_new.write \
    .format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save("s3://my-bucket/warehouse/employees")
```

```sql
-- Option 2: ALTER TABLE
ALTER TABLE employees ADD COLUMNS (department STRING);

-- Verify
DESCRIBE TABLE employees;
```

**Renaming a column** (requires column mapping mode):

```python
# Enable column mapping — must be set before rename
spark.sql("""
    ALTER TABLE employees
    SET TBLPROPERTIES (
        'delta.columnMapping.mode' = 'name',
        'delta.minReaderVersion' = '2',
        'delta.minWriterVersion' = '5'
    )
""")

spark.sql("ALTER TABLE employees RENAME COLUMN department TO dept")
```

**Dropping a column:**

```sql
ALTER TABLE employees DROP COLUMN dept;
```

Column mapping mode stores a physical column name (UUID-based) separately from the logical name, so rename and drop operations are purely metadata changes — no data rewrite required.

### Time Travel & Rollback

Every version of the table is queryable as long as the underlying Parquet files have not been vacuumed.

```python
# Read as of a specific version
df_v3 = spark.read \
    .format("delta") \
    .option("versionAsOf", 3) \
    .load("s3://my-bucket/warehouse/sales")

# Read as of a timestamp
df_yesterday = spark.read \
    .format("delta") \
    .option("timestampAsOf", "2024-01-15 00:00:00") \
    .load("s3://my-bucket/warehouse/sales")
```

```sql
-- SQL time travel syntax
SELECT * FROM sales VERSION AS OF 3;
SELECT * FROM sales TIMESTAMP AS OF '2024-01-15 00:00:00';

-- Describe history to find the right version
DESCRIBE HISTORY sales;
```

**Rollback (RESTORE):**

```python
from delta.tables import DeltaTable

dt = DeltaTable.forPath(spark, "s3://my-bucket/warehouse/sales")

# Restore to version 5
dt.restoreToVersion(5)

# Restore to timestamp
dt.restoreToTimestamp("2024-01-15 00:00:00")
```

```sql
RESTORE TABLE sales TO VERSION AS OF 5;
RESTORE TABLE sales TO TIMESTAMP AS OF '2024-01-15 00:00:00';
```

`RESTORE` creates a new commit that re-adds the files from the target version and removes the files added after it. The history between the current version and the restored version is preserved — you can always `RESTORE` forward again.

### MERGE / UPSERT Semantics

`MERGE` is the cornerstone of CDC pipelines on Delta Lake. It matches source rows to target rows on a join condition and applies different actions for matched vs. unmatched rows.

```python
from delta.tables import DeltaTable

target = DeltaTable.forName(spark, "customers")
source = spark.table("customers_staging")  # incoming CDC batch

target.alias("t").merge(
    source.alias("s"),
    "t.customer_id = s.customer_id"
).whenMatchedUpdate(
    condition="s.updated_at > t.updated_at",
    set={
        "name":       "s.name",
        "email":      "s.email",
        "updated_at": "s.updated_at"
    }
).whenNotMatchedInsert(
    values={
        "customer_id": "s.customer_id",
        "name":        "s.name",
        "email":       "s.email",
        "updated_at":  "s.updated_at"
    }
).whenMatchedDelete(
    condition="s.op = 'D'"
).execute()
```

```sql
-- Equivalent SQL MERGE
MERGE INTO customers AS t
USING customers_staging AS s
ON t.customer_id = s.customer_id
WHEN MATCHED AND s.updated_at > t.updated_at THEN
  UPDATE SET t.name = s.name, t.email = s.email, t.updated_at = s.updated_at
WHEN MATCHED AND s.op = 'D' THEN
  DELETE
WHEN NOT MATCHED THEN
  INSERT (customer_id, name, email, updated_at)
  VALUES (s.customer_id, s.name, s.email, s.updated_at);
```

**Performance note**: `MERGE` rewrites every Parquet file that contains at least one matched row. On large tables, narrow the target scan using partition predicates or Liquid Clustering to minimize the number of files touched.

### Compaction / Small File Problem

Streaming or frequent micro-batch writes produce many small Parquet files. Reading 10,000 × 1 MB files is dramatically slower than reading 100 × 100 MB files due to S3 request overhead and Parquet footer parsing cost.

**`OPTIMIZE`** compacts small files into larger ones (target size ~1 GB by default):

```sql
-- Compact all files
OPTIMIZE sales;

-- Compact only a specific partition
OPTIMIZE sales WHERE event_date = '2024-01-15';
```

```python
from delta.tables import DeltaTable

dt = DeltaTable.forName(spark, "sales")
dt.optimize().executeCompaction()

# With Z-ordering (co-locate related data for query pruning)
dt.optimize().executeZOrderBy("customer_id", "event_date")
```

**Auto Optimize** (Databricks-specific, also available via table properties):

```sql
ALTER TABLE sales SET TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',   -- bin-pack small writes at write time
    'delta.autoOptimize.autoCompact'   = 'true'    -- run compaction after each write
);
```

**`VACUUM`** removes Parquet files no longer referenced by any live version:

```sql
-- Default: remove files older than 7 days
VACUUM sales;

-- Override retention (dangerous — breaks time travel)
VACUUM sales RETAIN 24 HOURS;
```

### Liquid Clustering (Delta-Specific)

Traditional Hive-style partitioning requires you to choose partition columns upfront. Wrong choices are expensive to fix (full table rewrite). Partition columns with high cardinality (e.g., `user_id`) produce millions of tiny directories. Date-partitioned tables are efficient only for date-range queries; cross-partition queries (e.g., filter by `product_id`) still scan everything.

**Liquid Clustering** replaces explicit partitioning with a flexible, re-clusterable physical layout. Data is co-located on clustering keys using a space-filling curve, but the layout can be changed at any time with a simple `ALTER TABLE` — no data migration required.

```sql
-- Create table with Liquid Clustering (no PARTITIONED BY clause)
CREATE TABLE sales (
    sale_id     BIGINT,
    customer_id BIGINT,
    product_id  BIGINT,
    event_date  DATE,
    amount      DECIMAL(18,2)
) USING DELTA
CLUSTER BY (customer_id, event_date);
```

```python
# PySpark DDL with Liquid Clustering
DeltaTable.create(spark) \
    .tableName("sales") \
    .addColumn("sale_id",     "BIGINT") \
    .addColumn("customer_id", "BIGINT") \
    .addColumn("product_id",  "BIGINT") \
    .addColumn("event_date",  "DATE") \
    .addColumn("amount",      "DECIMAL(18,2)") \
    .clusterBy("customer_id", "event_date") \
    .execute()
```

```sql
-- Change clustering keys later — no rewrite needed immediately
ALTER TABLE sales CLUSTER BY (product_id, event_date);

-- Incrementally apply the new clustering layout
OPTIMIZE sales;
```

**When to use Liquid Clustering over partitioning:**
- Cardinality of filter columns > 10,000 distinct values.
- Multiple columns are used in filters interchangeably.
- Query patterns are not yet stable / likely to evolve.
- Table is small-to-medium (< 1 TB) — partitioning adds overhead at small scale.

---

## 4. Implementation Guide

### Creating a Table

```python
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField, LongType, StringType, DateType, DecimalType
)
from delta.tables import DeltaTable

spark = SparkSession.builder \
    .appName("DeltaLakeDemo") \
    .config("spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

schema = StructType([
    StructField("order_id",    LongType(),         nullable=False),
    StructField("customer_id", LongType(),         nullable=False),
    StructField("product_id",  LongType(),         nullable=False),
    StructField("order_date",  DateType(),         nullable=False),
    StructField("status",      StringType(),       nullable=True),
    StructField("amount",      DecimalType(18, 2), nullable=True),
])

# Create managed table in the metastore
DeltaTable.create(spark) \
    .tableName("orders") \
    .addColumns(schema) \
    .clusterBy("customer_id", "order_date") \
    .property("delta.autoOptimize.optimizeWrite", "true") \
    .property("delta.dataSkippingNumIndexedCols", "4") \
    .execute()
```

```sql
-- Equivalent SQL DDL
CREATE TABLE IF NOT EXISTS orders (
    order_id    BIGINT      NOT NULL,
    customer_id BIGINT      NOT NULL,
    product_id  BIGINT      NOT NULL,
    order_date  DATE        NOT NULL,
    status      STRING,
    amount      DECIMAL(18,2)
)
USING DELTA
CLUSTER BY (customer_id, order_date)
TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.dataSkippingNumIndexedCols' = '4'
);

-- External table pointing to existing S3 path
CREATE TABLE IF NOT EXISTS orders_ext
USING DELTA
LOCATION 's3://my-bucket/warehouse/orders'
-- (schema inferred from existing Delta log if table already exists)
;
```

### Writing Data: Batch

```python
from pyspark.sql import Row
from datetime import date
from decimal import Decimal

data = [
    Row(order_id=1, customer_id=101, product_id=500,
        order_date=date(2024, 1, 10), status="COMPLETED", amount=Decimal("99.99")),
    Row(order_id=2, customer_id=102, product_id=501,
        order_date=date(2024, 1, 11), status="PENDING",   amount=Decimal("149.00")),
]

df = spark.createDataFrame(data, schema=schema)

# Append
df.write.format("delta").mode("append").saveAsTable("orders")

# Overwrite entire table
df.write.format("delta").mode("overwrite").saveAsTable("orders")

# Overwrite a specific partition (Dynamic Partition Overwrite)
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
df_jan = df.filter("order_date >= '2024-01-01' AND order_date < '2024-02-01'")
df_jan.write.format("delta").mode("overwrite").saveAsTable("orders")
```

### Writing Data: Streaming

```python
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, LongType

# Read from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:9092") \
    .option("subscribe", "orders_topic") \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON payload
order_schema = StructType([
    StructField("order_id",    LongType()),
    StructField("customer_id", LongType()),
    StructField("product_id",  LongType()),
    StructField("order_date",  StringType()),
    StructField("status",      StringType()),
    StructField("amount",      StringType()),
])

parsed_df = kafka_df.select(
    from_json(col("value").cast("string"), order_schema).alias("data")
).select("data.*")

# Write to Delta — exactly-once via idempotent commits
query = parsed_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "s3://my-bucket/checkpoints/orders") \
    .option("mergeSchema", "true") \
    .trigger(processingTime="30 seconds") \
    .toTable("orders")

query.awaitTermination()
```

### Reading with Time Travel

```python
# By version number
df_v2 = spark.read \
    .format("delta") \
    .option("versionAsOf", 2) \
    .table("orders")

# By timestamp
df_ts = spark.read \
    .format("delta") \
    .option("timestampAsOf", "2024-01-10 12:00:00") \
    .table("orders")

df_ts.show()

# Audit the history
spark.sql("DESCRIBE HISTORY orders").show(truncate=False)
```

```sql
SELECT * FROM orders VERSION AS OF 2;
SELECT * FROM orders TIMESTAMP AS OF '2024-01-10 12:00:00';

-- Show full commit history
DESCRIBE HISTORY orders;
```

### Running MERGE / UPSERT

```python
from delta.tables import DeltaTable

target = DeltaTable.forName(spark, "orders")

# Incoming updates from CDC source
updates = spark.createDataFrame([
    Row(order_id=1, customer_id=101, product_id=500,
        order_date=date(2024, 1, 10), status="SHIPPED", amount=Decimal("99.99")),
    Row(order_id=3, customer_id=103, product_id=502,
        order_date=date(2024, 1, 12), status="NEW",     amount=Decimal("200.00")),
], schema=schema)

target.alias("t").merge(
    updates.alias("s"),
    "t.order_id = s.order_id"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()
```

```sql
MERGE INTO orders AS t
USING orders_updates AS s
ON t.order_id = s.order_id
WHEN MATCHED THEN
    UPDATE SET *
WHEN NOT MATCHED THEN
    INSERT *;
```

### Schema Evolution in Practice

```python
# Step 1: add a new column to incoming data
df_with_new_col = spark.createDataFrame([
    Row(order_id=4, customer_id=104, product_id=503,
        order_date=date(2024, 1, 13), status="COMPLETED",
        amount=Decimal("75.50"), discount_pct=Decimal("10.00")),  # new column
])

# Step 2: write with mergeSchema enabled
df_with_new_col.write \
    .format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable("orders")

# Step 3: verify schema updated
spark.sql("DESCRIBE TABLE orders").show()

# Step 4: enable column mapping for rename/drop
spark.sql("""
    ALTER TABLE orders
    SET TBLPROPERTIES (
        'delta.columnMapping.mode' = 'name',
        'delta.minReaderVersion'   = '2',
        'delta.minWriterVersion'   = '5'
    )
""")

# Rename
spark.sql("ALTER TABLE orders RENAME COLUMN discount_pct TO discount_percentage")

# Drop (only safe after all readers have moved to new column name)
spark.sql("ALTER TABLE orders DROP COLUMN discount_percentage")
```

### Full Config Block

```python
spark = SparkSession.builder \
    .appName("DeltaLakeProduction") \
    \
    # ── Core Delta extensions ───────────────────────────────────────────────
    .config("spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension") \
    \
    # ── Replace the default catalog with Delta-aware catalog ────────────────
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    \
    # ── S3 atomic writes via DynamoDB locking ───────────────────────────────
    .config("spark.delta.logStore.class",
            "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore") \
    .config("spark.io.delta.storage.S3DynamoDBLogStore.ddb.tableName",
            "delta_log") \
    .config("spark.io.delta.storage.S3DynamoDBLogStore.ddb.region",
            "us-east-1") \
    \
    # ── Write tuning ────────────────────────────────────────────────────────
    # Target ~128 MB per output file (Spark default shuffle partitions × this)
    .config("spark.sql.files.maxRecordsPerFile", "0") \
    # Coalesce shuffle output to meet target file size
    .config("spark.databricks.delta.optimizeWrite.enabled", "true") \
    \
    # ── Read tuning ─────────────────────────────────────────────────────────
    # Cache Delta logs in memory for repeated reads
    .config("spark.databricks.delta.stalenessLimit", "3600000") \
    # Collect column statistics on write for data skipping
    .config("spark.databricks.delta.stats.collect", "true") \
    \
    # ── Schema enforcement ──────────────────────────────────────────────────
    # Reject writes with extra columns (default: true)
    .config("spark.databricks.delta.schema.autoMerge.enabled", "false") \
    \
    # ── Streaming reliability ───────────────────────────────────────────────
    # Limit files processed per micro-batch trigger
    .config("spark.databricks.delta.streaming.maxFilesPerTrigger", "1000") \
    \
    .getOrCreate()

# ── Table-level properties (set via ALTER TABLE or CREATE TABLE) ───────────
TABLE_PROPERTIES = {
    # Checkpoint every 10 commits (default) — reduce for high-frequency writes
    "delta.checkpointInterval":                "10",

    # Retain deleted file data for 7 days (must be >= spark.sql query timeout)
    "delta.deletedFileRetentionDuration":      "interval 7 days",

    # Retain log files for 30 days (governs time travel window)
    "delta.logRetentionDuration":              "interval 30 days",

    # Enable auto-compaction of small files after each write
    "delta.autoOptimize.autoCompact":          "true",

    # Enable bin-packing of shuffle output at write time
    "delta.autoOptimize.optimizeWrite":        "true",

    # Number of columns to collect min/max stats on (0 = all)
    "delta.dataSkippingNumIndexedCols":        "32",

    # Enable Bloom filter on high-cardinality columns
    "delta.bloomFilter.customer_id.enabled":   "true",
    "delta.bloomFilter.customer_id.fpp":       "0.01",
    "delta.bloomFilter.customer_id.numItems":  "10000000",

    # Column mapping for rename/drop support
    "delta.columnMapping.mode":                "name",
    "delta.minReaderVersion":                  "2",
    "delta.minWriterVersion":                  "5",
}
```

---

## 5. Integration with the Ecosystem

### Apache Spark — Config & Unity Catalog

```python
# Open-source Spark + Delta OSS (no Databricks)
spark = SparkSession.builder \
    .config("spark.jars.packages",
            "io.delta:delta-spark_2.12:3.2.0") \
    .config("spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()
```

**Unity Catalog integration (Databricks):**

Unity Catalog is a centralized, fine-grained governance layer built on top of Delta Lake. Tables, schemas, and catalogs are three-level namespaced (`catalog.schema.table`).

```sql
-- Create a catalog backed by an external S3 location
CREATE CATALOG prod_catalog
MANAGED LOCATION 's3://my-bucket/unity-catalog/prod';

-- Create schema within the catalog
CREATE SCHEMA prod_catalog.sales;

-- Create a table governed by Unity Catalog
CREATE TABLE prod_catalog.sales.orders (
    order_id    BIGINT NOT NULL,
    customer_id BIGINT NOT NULL,
    amount      DECIMAL(18,2)
)
USING DELTA
CLUSTER BY (customer_id);

-- Grant column-level access
GRANT SELECT ON prod_catalog.sales.orders (order_id, amount)
TO `analyst_group`;
```

**Delta Sharing** (cross-organization data sharing):

```python
# Provider side: share a Delta table without copying data
spark.sql("""
    CREATE SHARE orders_share;
    ADD TABLE prod_catalog.sales.orders TO SHARE orders_share;
    CREATE RECIPIENT partner_company;
    GRANT SELECT ON SHARE orders_share TO RECIPIENT partner_company;
""")

# Consumer side: read the shared table via open Delta Sharing protocol
from delta_sharing import SharingClient

client = SharingClient("s3://share-profile-bucket/config.share")
df = client.load_as_spark("partner_company.orders_share.orders")
df.show()
```

### AWS Glue / S3

```python
# EMR or Glue job — register Delta table in Glue Data Catalog
spark = SparkSession.builder \
    .config("spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.hadoop.hive.metastore.client.factory.class",
            "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory") \
    .enableHiveSupport() \
    .getOrCreate()

# Write Delta table and register in Glue
df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("path", "s3://my-bucket/warehouse/orders") \
    .saveAsTable("my_database.orders")

# Run Glue Crawler to discover Delta tables — set table type to CUSTOM
# In Glue Crawler config, set "Delta Lake" as the custom classifier
```

```yaml
# AWS Glue job config (glue_job.yaml)
GlueVersion: "4.0"
WorkerType: G.2X
NumberOfWorkers: 10
DefaultArguments:
  "--datalake-formats": "delta"
  "--conf": "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension
             --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog"
```

### Trino / Athena

```properties
# Trino Delta connector — catalog properties file
# /etc/trino/catalog/delta.properties
connector.name=delta_lake
hive.metastore.uri=thrift://metastore-host:9083
hive.s3.aws-access-key=AKIAIOSFODNN7EXAMPLE
hive.s3.aws-secret-key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
hive.s3.region=us-east-1
delta.max-split-size=128MB
delta.metadata.cache-ttl=10m
delta.metadata.live-files-cache-size=20MB
```

```sql
-- Trino: query a Delta table
SELECT customer_id, SUM(amount) AS total
FROM delta.sales.orders
WHERE order_date >= DATE '2024-01-01'
GROUP BY customer_id
ORDER BY total DESC
LIMIT 100;
```

**Athena** supports Delta Lake via the `symlink_format_manifest` approach or natively in Athena v3:

```sql
-- Generate manifests for Athena compatibility (if using manifest approach)
GENERATE symlink_format_manifest FOR TABLE delta.`s3://my-bucket/warehouse/orders`;

-- Athena v3: native Delta read (no manifest needed)
-- Just point a Glue table to the Delta path and set table type = DELTA
```

### Kafka / Flink (Streaming Writes)

```python
# Spark Structured Streaming from Kafka to Delta
from pyspark.sql.functions import from_json, col

stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:9092") \
    .option("subscribe", "orders") \
    .option("failOnDataLoss", "false") \
    .load()

parsed = stream_df.select(
    from_json(col("value").cast("string"), schema).alias("v")
).select("v.*")

# Foreground query with Delta sink
query = parsed.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "s3://my-bucket/checkpoints/orders_stream") \
    .trigger(processingTime="1 minute") \
    .toTable("orders")
```

```java
// Flink: write to Delta using the Flink/Delta connector
// (flink-connector-delta artifact)
import io.delta.flink.sink.DeltaSink;
import org.apache.flink.core.fs.Path;
import org.apache.flink.table.data.RowData;

DeltaSink<RowData> deltaSink = DeltaSink
    .forRowData(
        new Path("s3://my-bucket/warehouse/orders"),
        hadoopConf,
        rowType)
    .withMergeSchema(true)
    .build();

dataStream.sinkTo(deltaSink);
```

### dbt

```yaml
# profiles.yml — dbt-spark profile for Delta
my_delta_project:
  target: dev
  outputs:
    dev:
      type: spark
      method: thrift          # or databricks for Databricks SQL
      host: spark-thrift-host
      port: 10001
      schema: analytics
      threads: 4
```

```sql
-- models/orders_summary.sql
{{ config(
    materialized='incremental',
    file_format='delta',
    incremental_strategy='merge',
    unique_key='order_id',
    merge_update_columns=['status', 'amount', 'updated_at'],
    on_schema_change='merge',
    tblproperties={
        'delta.autoOptimize.optimizeWrite': 'true',
        'delta.autoOptimize.autoCompact': 'true'
    }
) }}

SELECT
    order_id,
    customer_id,
    SUM(amount)       AS amount,
    MAX(status)       AS status,
    MAX(updated_at)   AS updated_at
FROM {{ ref('stg_orders') }}
{% if is_incremental() %}
WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}
GROUP BY order_id, customer_id
```

---

## 6. Performance Tuning

### File Sizing Recommendations

The target file size for Delta Lake Parquet files is **128 MB–1 GB** (uncompressed). With Snappy compression (~40% ratio), that typically means 50–400 MB on disk.

- **Too small (< 32 MB)**: excessive S3 LIST + GET requests per query; Parquet footer parsing overhead dominates.
- **Too large (> 1 GB)**: coarse-grained data skipping; a single predicate that matches 10% of rows still reads the whole file.
- **Optimal for most workloads**: 256–512 MB on disk (Snappy).

```sql
-- Set target file size for OPTIMIZE
ALTER TABLE orders SET TBLPROPERTIES (
    'delta.targetFileSize' = '268435456'  -- 256 MB in bytes
);
```

```python
# Control shuffle partition count to influence output file size
# Rule of thumb: total_data_size_bytes / target_file_size_bytes
spark.conf.set("spark.sql.shuffle.partitions", "200")

# Auto-size shuffle partitions (Spark 3.0+ AQE)
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "268435456")
```

### Partitioning Strategies

**When to partition:**
- Table size > 1 TB.
- There is a dominant filter column with low-to-medium cardinality (e.g., `region`, `year`, `date`).
- The partition column is nearly always present in `WHERE` clauses.

**When NOT to partition (use Liquid Clustering instead):**
- Filter column cardinality > 10,000 (e.g., `customer_id`, `product_id`).
- Multiple competing filter columns.
- Table is < 100 GB — partition overhead exceeds benefit.
- Query patterns are not yet stable.

```sql
-- Traditional date partition (acceptable for event tables > 1 TB)
CREATE TABLE events (
    event_id   BIGINT,
    user_id    BIGINT,
    event_type STRING,
    event_date DATE,
    payload    STRING
)
USING DELTA
PARTITIONED BY (event_date);

-- Better alternative for mixed query patterns: Liquid Clustering
CREATE TABLE events (
    event_id   BIGINT,
    user_id    BIGINT,
    event_type STRING,
    event_date DATE,
    payload    STRING
)
USING DELTA
CLUSTER BY (event_date, user_id);
```

### Compaction / OPTIMIZE Scheduling

```python
# Schedule OPTIMIZE after each large batch load
# Run as a separate job step after the data write job completes

from delta.tables import DeltaTable
from datetime import datetime, timedelta

dt = DeltaTable.forName(spark, "events")

# Z-order on the columns most commonly filtered
dt.optimize() \
  .where(f"event_date >= '{(datetime.today() - timedelta(days=3)).date()}'") \
  .executeZOrderBy("user_id", "event_type")
```

```sql
-- OPTIMIZE + Z-ORDER on last 3 days of data
OPTIMIZE events
WHERE event_date >= current_date() - INTERVAL 3 DAYS
ZORDER BY (user_id, event_type);

-- Vacuum with safe retention
VACUUM events RETAIN 168 HOURS;  -- 7 days
```

**Recommended OPTIMIZE schedule:**
- **Batch tables**: run `OPTIMIZE` once per day after the daily load.
- **Streaming tables**: enable `autoCompact` at the table level; run scheduled `OPTIMIZE + ZORDER` daily.
- **Never run OPTIMIZE mid-stream** — it competes with the streaming writer and can cause commit conflicts.

### Column Stats, Bloom Filters, Z-Ordering

**Column statistics** (min/max per file) are collected automatically on write for the first N columns (`delta.dataSkippingNumIndexedCols`). They enable **data file skipping** — files that cannot satisfy the predicate are excluded before a single byte is read.

```sql
-- Increase the number of columns with statistics (default: 32)
ALTER TABLE orders SET TBLPROPERTIES (
    'delta.dataSkippingNumIndexedCols' = '64'
);
```

**Bloom filters** are probabilistic membership structures that answer "is value X in this file?" in O(1). They are ideal for high-cardinality point lookups (UUID, user_id, email) where min/max stats provide no pruning value.

```sql
ALTER TABLE orders SET TBLPROPERTIES (
    'delta.bloomFilter.customer_id.enabled'  = 'true',
    'delta.bloomFilter.customer_id.fpp'      = '0.01',   -- 1% false positive rate
    'delta.bloomFilter.customer_id.numItems' = '5000000' -- expected distinct values
);
```

**Z-ordering** interleaves the sort order of multiple columns using a Z-curve (Morton code), co-locating rows that are similar on multiple dimensions into the same files. It improves skipping for multi-column predicates.

```sql
OPTIMIZE orders ZORDER BY (customer_id, product_id);
-- Now queries filtering on both customer_id AND product_id skip significantly more files
```

**Z-order vs Liquid Clustering:**
- Z-order requires re-running `OPTIMIZE ZORDER` after each significant data load.
- Liquid Clustering applies incrementally — `OPTIMIZE` with no explicit `ZORDER` respects the declared cluster keys.
- Liquid Clustering is preferred for new tables; Z-order is useful on legacy partitioned tables.

### Common Query Patterns and Tuning

```sql
-- Pattern 1: Point lookup on customer_id
-- → Enable Bloom filter on customer_id
-- → Cluster/Z-order by customer_id
SELECT * FROM orders WHERE customer_id = 12345;

-- Pattern 2: Date range scan
-- → Partition or cluster by order_date
-- → Column stats on order_date are sufficient; no Bloom filter needed
SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-01-31';

-- Pattern 3: Aggregation with GROUP BY customer_id
-- → Cluster by customer_id reduces shuffle size (data pre-sorted)
SELECT customer_id, COUNT(*), SUM(amount)
FROM orders
GROUP BY customer_id;

-- Pattern 4: MERGE on large tables
-- → Add partition predicate to MERGE to limit scan
MERGE INTO orders AS t
USING updates AS s
ON t.customer_id = s.customer_id AND t.order_date = s.order_date  -- narrows scan
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

---

## 7. Common Pitfalls & How to Avoid Them

**Pitfall:** Running `VACUUM` with a retention period shorter than 7 days without disabling the safety check.
**Symptom:** `IllegalArgumentException: requirement failed: Are you sure you would like to vacuum files with such a low retention period?`
**Fix:** Set `spark.databricks.delta.retentionDurationCheck.enabled = false` before running vacuum with a short retention, or keep retention >= 7 days. Never go below your longest running query duration.

---

**Pitfall:** Schema enforcement silently drops new columns from streaming writes.
**Symptom:** New columns from the Kafka source never appear in the Delta table; no exception is thrown.
**Fix:** Add `.option("mergeSchema", "true")` to the `writeStream` call, or set `spark.databricks.delta.schema.autoMerge.enabled = true` in the SparkSession config.

---

**Pitfall:** Concurrent `MERGE` jobs fighting over the same partition, causing repeated `ConcurrentModificationException` and exponential backoff.
**Symptom:** MERGE jobs take 10× longer than expected; Spark logs show repeated retry messages.
**Fix:** Partition the incoming CDC batches by the same key used in the MERGE condition, and process partitions serially or ensure each writer targets disjoint partitions. Alternatively, use Databricks' `delta.targetFileSize` tuning to reduce per-file contention surface.

---

**Pitfall:** `OPTIMIZE` running concurrently with a streaming writer causes the streaming job to fail with `FileNotFoundException`.
**Symptom:** Streaming query aborts with `FileNotFoundException` pointing to a Parquet file that was compacted away.
**Fix:** Enable `autoCompact` at the table level rather than running `OPTIMIZE` externally while the stream is active. If external `OPTIMIZE` is necessary, pause the stream or run it during a maintenance window.

---

**Pitfall:** Excessive small files on S3 due to streaming micro-batches writing with high parallelism.
**Symptom:** `DESCRIBE DETAIL table_name` shows `numFiles` in the tens of thousands; query scan times are 10-50× slower than expected for the data volume.
**Fix:** Enable `delta.autoOptimize.optimizeWrite = true` and `delta.autoOptimize.autoCompact = true`. Also reduce streaming parallelism: set `spark.sql.shuffle.partitions` to a value proportional to actual data volume per trigger.

---

**Pitfall:** Time travel queries failing after running `VACUUM` with default settings.
**Symptom:** `AnalysisException: No recreatable commits found at version X` or `FileNotFoundException` when querying old versions.
**Fix:** Extend `delta.logRetentionDuration` and `delta.deletedFileRetentionDuration` to match your SLA for time travel queries. Default 7-day data retention is often too short for audit use cases. Set to `interval 90 days` if compliance requires it.

---

**Pitfall:** DynamoDB lock table becoming a bottleneck for high-concurrency writes on S3.
**Symptom:** Write latency spikes to 10–30 seconds; DynamoDB `ConsumedWriteCapacityUnits` CloudWatch metric is maxed; Spark logs show `LockAcquisitionException`.
**Fix:** Increase DynamoDB provisioned write capacity (or switch to on-demand). Alternatively, co-partition your write workload to reduce contention — parallel writers on different table partitions should use different DynamoDB entries. Consider migrating to S3 conditional writes (Delta 3.x+) to eliminate the DynamoDB dependency.

---

**Pitfall:** Enabling column mapping on a table that downstream Trino or Athena jobs read, causing those jobs to fail.
**Symptom:** Trino throws `Column 'xyz' not found` after a rename, or reads null values for renamed columns.
**Fix:** Column mapping (`delta.columnMapping.mode = name`) requires reader version 2. Ensure all reader engines support Delta reader protocol version 2 before enabling. Coordinate column renames with downstream consumers; use a transition period where both the old and new column names coexist (add new column, backfill, deprecate old).

---

**Pitfall:** `RESTORE TABLE` does not shrink storage because `VACUUM` has not been run after the restore.
**Symptom:** After restoring to an old version, storage usage does not decrease; files added between the restore point and the current version are still present on disk.
**Fix:** After `RESTORE`, the files from the unwanted versions are tombstoned (in `remove` actions) but not deleted. Run `VACUUM` after the restore to physically remove them. Ensure retention period has passed or override it explicitly.

---

## 8. Comparison with the Other Two OTF Options

| Feature | Apache Iceberg | Delta Lake | Apache Hudi |
|---|---|---|---|
| **ACID support** | Full ACID (OCC via catalog) | Full ACID (OCC via log) | Full ACID (OCC + timeline) |
| **Streaming ingestion** | Good (Flink native) | Excellent (Spark Structured Streaming native) | Excellent (purpose-built for CDC) |
| **Schema evolution** | Add, rename, drop, reorder columns; partition evolution | Add, rename, drop (with column mapping); Liquid Clustering | Add, rename columns; schema-on-read flexibility |
| **Partitioning model** | Hidden partitioning + partition evolution (no rewrites) | Liquid Clustering (flexible) or Hive-style | Partition-based; multi-level partitioning supported |
| **Catalog dependency** | Requires catalog (Hive, REST, Glue, Nessie) | Self-describing via `_delta_log`; catalog optional | Self-describing via `.hoodie/`; catalog optional |
| **Cloud/managed service support** | Snowflake (read), BigQuery, Dremio, AWS (Athena native), GCP | Databricks (first-class), Azure Synapse, AWS EMR, Athena (v3) | Onehouse, AWS EMR, GCP Dataproc |
| **Primary use case** | Multi-engine lakehouse; strong catalog/governance requirements | Databricks-centric stack; SQL analytics; Delta Sharing | High-throughput CDC upserts; near-real-time analytics |
| **Time travel** | Via snapshot ID or timestamp | Via version number or timestamp | Via timeline (commits, deltacommits, clean) |
| **Upsert performance** | Good (copy-on-write by default) | Good (MERGE with file-level rewrites) | Excellent (MOR defers rewrites; optimized for CDC) |
| **Ecosystem maturity** | Broad; all major engines have native readers | Very mature; longest production history | Mature; strongest in AWS ecosystem |

---

## 9. Quick Reference

### Cheat-Sheet Config Block

```sql
-- Full table properties reference with defaults and recommended values
ALTER TABLE my_table SET TBLPROPERTIES (

    -- Checkpoint frequency (default: 10 commits)
    -- Reduce to 5 for high-frequency streaming tables
    'delta.checkpointInterval'                  = '10',

    -- Retain deleted file data for time travel (default: interval 7 days)
    -- Increase for audit/compliance use cases
    'delta.deletedFileRetentionDuration'        = 'interval 7 days',

    -- Retain transaction log for time travel (default: interval 30 days)
    'delta.logRetentionDuration'                = 'interval 30 days',

    -- Auto-compact files after each write (default: false)
    -- Enable for streaming or frequent small-batch tables
    'delta.autoOptimize.autoCompact'            = 'true',

    -- Bin-pack write output to meet target file size (default: false)
    -- Enable to reduce small files from shuffle-heavy writes
    'delta.autoOptimize.optimizeWrite'          = 'true',

    -- Target file size for OPTIMIZE in bytes (default: 1073741824 = 1 GB)
    -- 256 MB recommended for most analytical tables
    'delta.targetFileSize'                      = '268435456',

    -- Number of columns to collect min/max stats on (default: 32, 0 = all)
    'delta.dataSkippingNumIndexedCols'          = '32',

    -- Bloom filter on high-cardinality lookup column
    'delta.bloomFilter.user_id.enabled'         = 'true',
    'delta.bloomFilter.user_id.fpp'             = '0.01',
    'delta.bloomFilter.user_id.numItems'        = '10000000',

    -- Column mapping mode: 'none' (default) or 'name' (enables rename/drop)
    'delta.columnMapping.mode'                  = 'name',
    'delta.minReaderVersion'                    = '2',
    'delta.minWriterVersion'                    = '5',

    -- Isolation level: Serializable (strictest) or WriteSerializable (default)
    'delta.isolationLevel'                      = 'WriteSerializable',

    -- Enable change data feed for downstream CDC consumers
    'delta.enableChangeDataFeed'                = 'false'
);
```

### Key SQL Commands Reference

```sql
-- ── DDL ────────────────────────────────────────────────────────────────────

-- Create managed table
CREATE TABLE db.my_table (id BIGINT, name STRING)
USING DELTA
CLUSTER BY (id)
TBLPROPERTIES ('delta.autoOptimize.optimizeWrite' = 'true');

-- Create external table
CREATE TABLE db.my_ext_table
USING DELTA
LOCATION 's3://bucket/path';

-- Add column
ALTER TABLE db.my_table ADD COLUMNS (new_col STRING);

-- Rename column (requires column mapping)
ALTER TABLE db.my_table RENAME COLUMN old_name TO new_name;

-- Drop column
ALTER TABLE db.my_table DROP COLUMN col_name;

-- Change table properties
ALTER TABLE db.my_table SET TBLPROPERTIES ('delta.targetFileSize' = '268435456');

-- Drop table (removes metastore entry; data on disk if external)
DROP TABLE db.my_table;


-- ── DML ────────────────────────────────────────────────────────────────────

-- Insert
INSERT INTO db.my_table VALUES (1, 'Alice'), (2, 'Bob');

-- Insert overwrite
INSERT OVERWRITE db.my_table SELECT * FROM staging;

-- Update
UPDATE db.my_table SET name = 'Updated' WHERE id = 1;

-- Delete
DELETE FROM db.my_table WHERE id = 2;

-- Merge / Upsert
MERGE INTO db.my_table AS t
USING staging AS s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;


-- ── TIME TRAVEL ────────────────────────────────────────────────────────────

SELECT * FROM db.my_table VERSION AS OF 5;
SELECT * FROM db.my_table TIMESTAMP AS OF '2024-01-01 00:00:00';

-- Restore to previous version
RESTORE TABLE db.my_table TO VERSION AS OF 5;
RESTORE TABLE db.my_table TO TIMESTAMP AS OF '2024-01-01 00:00:00';

-- View history
DESCRIBE HISTORY db.my_table;


-- ── MAINTENANCE ────────────────────────────────────────────────────────────

-- Compact files (optionally with Z-ordering)
OPTIMIZE db.my_table;
OPTIMIZE db.my_table WHERE event_date >= current_date() - INTERVAL 7 DAYS;
OPTIMIZE db.my_table ZORDER BY (user_id, event_date);

-- Remove files outside retention window
VACUUM db.my_table;
VACUUM db.my_table RETAIN 168 HOURS;

-- Inspect table details (file count, size, version)
DESCRIBE DETAIL db.my_table;

-- Show table schema + properties
DESCRIBE EXTENDED db.my_table;

-- Generate Athena-compatible symlink manifests
GENERATE symlink_format_manifest FOR TABLE delta.`s3://bucket/path`;
```

### Official Documentation Links

- [Official Docs](https://docs.delta.io/latest/index.html)
- [GitHub](https://github.com/delta-io/delta)
- [Delta Lake Protocol Specification](https://github.com/delta-io/delta/blob/master/PROTOCOL.md)
- [Delta Sharing Protocol](https://github.com/delta-io/delta-sharing)
- [Databricks Delta Lake Guide](https://docs.databricks.com/delta/index.html)
- [Unity Catalog Docs](https://docs.databricks.com/data-governance/unity-catalog/index.html)
