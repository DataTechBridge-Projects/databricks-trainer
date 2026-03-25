## Lakehouse Architecture  

*Section 7 of 15 – AWS Databricks Data Engineer Certification*  

---  

### Overview  

The Lakehouse paradigm fuses the best of two worlds: the open‑format, file‑system scalability of a data lake and the transactional guarantees, schema enforcement, and performance optimizations of a data warehouse. In the AWS Databricks implementation, the **Lakehouse** lives on top of **Delta Lake**, which is a storage layer that adds ACID transactions, versioning, and schema enforcement on top of object storage (e.g., Amazon S3).  

When you write data to Delta, you are not merely dumping parquet files into S3; you are updating a **transaction log** (`_delta_log`) that records every commit as an atomic JSON file. This log enables **time‑travel**, **concurrent reads/writes**, and **exactly‑once** semantics without a separate catalog. Databricks uses the same Spark engine for both batch and streaming workloads, letting you query the same tables interactively, via notebooks, jobs, or external tools—all with a single SQL endpoint or API surface.  

The architecture is intentionally **cloud‑native**: it leverages **S3’s durability and elasticity**, **IAM** for fine‑grained access, **AWS Glue Catalog** for metadata, and **Lake Formation** for column‑level security when needed. At the same time, Delta’s design is storage‑agnostic, meaning you could move the same data to Azure Data Lake Storage or Google Cloud Storage without changing your PySpark code. This portability is a key exam objective—you must understand which decisions are **Databricks‑specific** versus **AWS‑specific**.  

Finally, because the exam stresses **practical implementation**, you’ll see questions that ask you to choose the right storage format, configure a **`VACUUM`** retention period, decide between **Auto Loader** vs. ** Structured Streaming** for ingest, and tune **optimizations** such as `OPTIMIZE` and **Z‑order**. This section walks you through each of those pieces in depth.  

---  

### Core Concepts  

Below we break down the foundational pillars of the Lakehouse on AWS.  

#### 1. Delta Lake Table Formats  

| Feature | What it does | Why it matters for the exam |
|---------|--------------|----------------------------|
| **Transactional Log (`_delta_log`)** | Immutable JSON commit files, each representing a set of file additions/removptions. | Enables **exactly‑once** writes and **time‑travel** (`SELECT * FROM table VERSION AS OF 3`). |
| **Schema Enforcement** | The schema stored in the log is validated on every write. | Prevents “silent schema drift” that can corrupt warehouse‑level reporting. |
| **Schema Evolution** | `ALTER TABLE ... SET TBLPROPERTIES (delta.columnMapping.mode='name')` + `MERGE`/`UPDATE` for structural changes. | Critical for evolving models (e.g., adding a new event‑date column) while preserving downstream downstream pipelines. |
| **Compaction & Optimizations** | `OPTIMIZE table ZORDER BY (date)` & `VACUUM`. | Reduces file‑count, improves pruning, and controls storage cost. |
| **Data Skipping** | Built‑in statistics (min/max, null counts) stored per file. | Drives predicate push‑down for selective scans (e.g., `WHERE event_date = '2024-10-01'`). |

#### 2. Ingestion Pathways  

| Path | Typical Use‑Case | Recommended Settings |
|------|------------------|-----------------------|
| **Auto Loader (File System)** | Low‑latency ingestion from S3, Kinesis, or ADLS. | `readStream.format("cloudFiles").option("cloudFiles.format","json")` |
| **Structured Streaming with `trigger(processingTime='30 seconds')`** | Real‑time analytics where ordering guarantees are essential. | Use **checkpointing** on a dedicated S3 prefix, enable **exactly‑once** (`outputMode("append")`). |
| **Batch `spark.read.format("json").load(s3_path)`** | One‑off loads for large historical data. | Use **repartition** on a key (e.g., `event_date`) before writing to Delta. |

#### 3. Compute & Execution  

- **Databricks SQL & Spark Pools** abstract the cluster lifecycle; you pay per DBU (Databricks Unit) and per VM type.  
- **Cluster Autoscaling** automatically adds/removes workers based on workload.  
- **Job Clusters vs. All‑Purpose Clusters** – exam may ask you when to use a **job cluster** (ephemeral, per‑job) versus an **all‑purpose** cluster (persistent, for notebooks).  

#### 4. Governance & Security  

| AWS Service | Lakehouse Role |
|-------------|----------------|
| **IAM / S3 bucket policies** | Control who can read/write raw S3 prefixes (`s3://my-raw/`). |
| **AWS Glue Data Catalog** | Serves as the external Hive metastore; Delta tables are **registered** as Hive tables for compatibility. |
| **Lake Formation** | Centralized column‑level security, fine‑grained permissions, and data‑masking policies. |
| **AWS KMS** | Envelope encryption for S3 objects; Databricks respects the KMS key used at bucket level. |
| **CloudWatch Logs & Metrics** | Provide per‑cluster DBU consumption, shuffle write metrics, and streaming lag. |

---  

### Architecture / How It Works  

The diagram below shows a typical end‑to‑end Lakehouse pipeline on AWS.  

```mermaid
flowchart TD
    subgraph Ingest[Raw Ingestion]
        A[S3 Raw Bucket<br/>(e.g., s3://my-raw/)];
        B[Kinesis Firehose / S3 Event Notification];
        C[Auto Loader (cloudFiles)] -->|continuous| D[Delta Landing Zone<br/>s3://my-delta/landing/];
    end

    subgraph Processing[Processing & Enrichment]
        D -->|batch/stream| E[Delta Bronze Table<br/>my_db.bronze_events];
        E -->|UPSERT/MERGE| F[Delta Silver Table<br/>my_db.silver_events];
        F -->|Z‑order & OPTIMIZE| G[Delta Gold Table<br/>my_db.gold_events];
    end

    subgraph Consumption[Consumption Layer]
        H[Databricks SQL Endpoint] --> I[BI Tools (Tableau, PowerBI)];
        J[Spark Jobs] --> K[ML Training (Databricks MLflow)];
        G -->|External access| L[Glue Data Catalog & Athena];
    end

    style Ingest fill:#f9f9f9,stroke:#333,stroke-width:2px
    style Processing fill:#e8f5e9,stroke:#333,stroke-width:2px
    style Consumption fill:#e3f2fd,stroke:#333,stroke-width:2px
```

**Explanation**  

1. **Raw Ingestion** – Files land in an S3 bucket (`my-raw/`). An S3 event triggers **Auto Loader**, which automatically creates a **streaming DataFrame** that reads the new objects and writes them as **immutable parquet** into a **Delta Bronze** table.  

2. **Processing** – The Bronze table holds the *as‑is* data. Separate batch or streaming jobs read from Bronze, perform cleansing, join with reference data, and write to **Silver** (cleaned) and **Gold** (business‑ready) Delta tables. `OPTIMIZE` with `ZORDER` is typically run nightly on Gold for query acceleration.  

3. **Consumption** – Data scientists, analysts, and downstream applications query the Gold table via **SQL endpoints**, **Spark jobs**, or **Athena/Glue**. The same table is also exposed through the **Glue Catalog**, enabling cross‑service access without data duplication.  

---  

### Hands-On: Key Operations  

Below are the most exam‑relevant operations, each with a **self‑contained snippet** that you can paste into a Databricks notebook. Comments explain the “why”.  

#### 1. Create a Delta Table with a Schema  

```python
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DecimalType

spark = SparkSession.builder.getOrCreate()

# Define a reusable schema (helps enforce consistency across jobs)
event_schema = StructType([
    StructField("event_id", StringType(), False),
    StructField("event_timestamp", TimestampType(), False),
    StructField("user_id", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("amount", DecimalType(12, 4), True)
])

# Ingest raw JSON files via Auto Loader (streaming)
raw_stream = (spark.readStream
                .format("cloudFiles")
                .option("cloudFiles.format", "json")
                .option("cloudFiles.schemaLocation", "/tmp/schema/landing")
                .schema(event_schema)  # explicit schema prevents drift
                .load("s3://my-raw/landing/"))

# Write to Delta Bronze (append mode, exactly‑once)
(bronze_writer := raw_stream
 .write
 .format("delta")
 .option("checkpointLocation", "s3://my-raw/checkpoints/bronze_events")
 .mode("append")
 .saveAsTable("my_db.bronze_events"))
```

**Key points** – The `cloudFiles.schemaLocation` isolates schema metadata across runs; the table is **transactional**, so the downstream `MERGE` will be atomic.  

#### 2. Incremental Upsert from Bronze → Silver  

```python
from delta.tables import DeltaTable

# Load the current silver table (or create if absent)
silver_path = "my_db.silver_events"

# Assume we have a static reference dataset in a DataFrame `ref_df`
ref_df = spark.table("my_db.user_profile_ref")

# Define the MERGE condition – typical key is (user_id, event_timestamp)
source = spark.table("my_db.bronze_events")

# Build the UPSERT logic
delta_silver = DeltaTable.forName(spark, "my_db.silver_events")

(delta_silver.alias("t")
 .merge(
     source.alias("s"),
     "t.user_id = s.user_id AND t.event_timestamp = s.event_timestamp"
 )
 .whenMatchedUpdateAll()      # overwrite existing rows with newer data
 .whenNotMatchedInsertAll()   # insert new rows
 .execute()
)
```

*Why it matters* – The exam may ask you to **choose the right MERGE strategy** for slowly changing dimensions. This pattern ensures idempotency and avoids duplicate rows.  

#### 3. Optimize & Z‑order a Gold Table  

```python
# Run daily compaction on the Gold table
spark.sql("OPTIMIZE my_db.gold_events ZORDER BY (event_date, event_type)")
# Clean up old files – retain 7 days of history (default is 7, but we set explicitly)
spark.sql("VACUUM my_db.gold_events RETAIN 168 HOURS")  # 7 days
```

*Exam tip* – Remember that `VACUUM` with a retention less than the default can be used to **force deletion** when you’re sure no time‑travel queries will need older versions.  

#### 4. Query with Time Travel  

```sql
-- View the table as it existed 24 hours ago
SELECT *
FROM my_db.gold_events
VERSION AS OF (SELECT max(VERSION) FROM my_db.gold_events WHERE _change_type = 'update_preimage' AND event_date = DATE('2024-10-15'))
WHERE event_date = DATE('2024-10-15')
LIMIT 10;
```

Use this pattern when you need to **reproduce a historical report** – a common interview scenario.  

---  

### AWS-Specific Considerations  

| Topic | Best‑Practice Recommendation | Exam Relevance |
|-------|------------------------------|----------------|
| **S3 Storage Classes** | Store raw landing files in **Standard‑IA** or **Intelligent‑Tiering** (cost‑effective, high durability). Keep Delta tables on **S3 Standard** for frequent reads. Use **S3 Glacier Deep Archive** only for *historical* snapshots you rarely query. | Questions may ask you to select the correct bucket class for a given latency vs cost scenario. |
| **IAM Role per Cluster** | Assign a **cluster‑level IAM role** with `s3:ListBucket` + `s3:GetObject` for the raw bucket and `s3:PutObject` for the delta bucket. Use **instance profiles** to propagate temporary credentials to DBU. | You’ll be asked to choose the correct **instance profile** when enabling `dbfs:/cluster/role.json`. |
| **Glue Catalog vs. Unity Catalog** | On AWS, **Unity Catalog** is the preferred governance layer (supports Lake Formation policies, data masking, fine‑grained ACLs). Glue Catalog is still needed for external tables used by Athena. Use **`USE CATALOG`** at the workspace level. | Exam may differentiate a `CREATE TABLE ... USING DELTA` statement with `CATALOG` vs. `DATABASE`. |
| **Lake Formation Registration** | After creating a Delta table, register the **S3 path** with Lake Formation, then grant `SELECT` on the table to the `data_analysts` group. This also enables **column‑level masking** for PII fields (`email`, `ssn`). | Expect a scenario where a query fails because of missing Lake Formation permissions. |
| **EMR Integration (if using EMR as a compute engine)** | While Databricks runs on its own managed clusters, you may attach an **EMRFS cache** for Spark executors, which can improve read performance from large Delta tables stored in S3. | Rare but possible; you need to know that `spark.hadoop.fs.s3a.committer.name` should be set to `emrfs` when using this mode. |
| **Monitoring & Alerting** | Set **CloudWatch Alarms** on DBU usage (`databricks.dbus.usage`), S3 request latency, and Delta table file count. Use **Databricks Job Run** metrics to trigger **SNS** notifications for failed jobs. | A question could ask which metric you would monitor to detect “shuffle spill” spikes. |
| **Security (KMS + S3 encryption)** | Enable **SSE‑KMS** with a customer‑managed CMK for the Delta tables bucket. Databricks automatically uses the bucket’s default encryption; you can override per‑object encryption via the `fs.s3a.server.side.style` config. | The exam may test whether you know to **set `spark.databricks.delta.preview.enabled`** to `true` for certain features when using KMS‑encrypted buckets. |

---  

### Exam Focus Areas  

- **Identify the correct ingestion method** (Auto Loader vs. Structured Streaming vs. batch) for a given latency or exactly‑once requirement.  
- **Explain the role of the Delta transaction log** and how it enables ACID semantics on S3.  
- **Configure table properties** for **schema evolution**, **versioning**, and **time‑travel** (`delta.columnMapping.mode`).  
- **Select the right storage class** for raw landing vs. Delta tables and apply appropriate IAM permissions.  
- **Perform table maintenance**: `OPTIMIZE`, `VACUUM`, `ZORDER`, and **set appropriate retention** for GDPR/compliance.  
- **Differentiate Unity Catalog, Glue Catalog, and Hive Metastore** in the context of data sharing and governance.  
- **Interpret a given query** that uses `VERSION AS OF` or `AS OF TIMESTAMP` and reason about data consistency.  
- **Explain how you would implement column‑level security** for a PII field in a Delta table using Lake Formation and Unity Catalog.  

---  

### Quick Recap  

- ✅ **Delta Lake** provides ACID transactions, schema enforcement, and time‑travel on top of object storage.  
- ✅ **Auto Loader** is the recommended “set‑it‑and‑forget‑it” way to ingest continuously from S3.  
- ✅ **Upserts with MERGE** are the backbone of Bronze → Silver → Gold pipelines; always include a **stable key**.  
- ✅ **Compaction (`OPTIMIZE` + `ZORDER`) and vacuum** are essential to keep query latency low and storage cost under control.  
- ✅ **AWS services** (S3, IAM, Glue, Lake Formation, CloudWatch) are tightly woven into the Lakehouse: respect their limits and best‑practices.  

---  

### Code References  

| Resource | Link | Why it’s useful |
|----------|------|-----------------|
| Delta Lake Documentation (AWS) | <https://docs.databricks.com/delta/> | Official reference for table operations, `OPTIMIZE`, `VACUUM`, and time‑travel. |
| Auto Loader on AWS S3 | <https://docs.databricks.com