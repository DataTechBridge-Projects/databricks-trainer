# Performance Tuning  

*Section 12 – 15 – 2025‑08‑30*  

> **Goal of this section** – Give you a complete mental model of how Spark on AWS Databricks works under the hood, how to read the performance signals, and which concrete actions you can take to squeeze latency, throughput, and cost out of your pipelines.  Use the material as a 45‑60 minute “talk‑track” and then dive into the hands‑on notebooks to try every technique on a real cluster.

---  

## Overview  

Performance in Apache Spark is the product of three interacting forces: **algorithmic efficiency**, **data layout**, and **cluster/cluster‑environment configuration**.  In a managed Databricks workspace on AWS you control the latter two but not the former—your Spark code decides which algorithms are applied.  The first step to mastery is to separate the “what” (the data transformation) from the “how” (the execution plan) and to ask, at every decision point, which of the three forces is most likely to be the bottleneck.

A typical pipeline that we’ll use as a running example looks like this:  

1. **Raw ingestion** – Data lands in an S3 bucket and is consumed by **Auto Loader** (continuous streaming).  
2. **Bronze Delta** – The data is written to a bronze Delta table partitioned by a high‑cardinality date column.  
3. **Silver / Gold enrichment** – Multiple joins with curated reference data (stored in S3 and Glue Catalog) produce a gold table used by downstream BI.  

Every transformation in this flow has a different set of knobs to turn.  For instance, streaming jobs are sensitive to **trigger intervals** and **checkpoint sizing**, while batch joins are dominated by **join strategy selection** and **partitioning**.  

Because the exam focuses on *identifying* and *fixing* performance problems, you’ll spend most of your time reading the Spark UI, the query plan (`explain`), and the Databricks monitoring dashboards.  The practical tasks you will be able to perform after this section are:

- **Read and interpret** Spark listeners, stage durations, and data skew warnings.  
- **Select the right file format, partitioning scheme, and Z‑ordering** for a given column.  
- **Tune Spark config** (e.g., `spark.sql.autoBroadcastJoinThreshold`, `spark.databricks.io.cache.enabled`).  
- **Design a cost‑aware AWS architecture** that aligns I/O, compute, and storage.  

---  

## Core Concepts  

Below we break down the most exam‑relevant concepts.  Treat each sub‑section as a “mental checklist” when you audit a job.

### 1. Spark Query Planning & the Catalyst Optimizer  

| Item | Description |
|------|-------------|
| **Logical vs. Physical Plan** | Logical plan is an API‑level abstraction (`DataFrame`).  Catalyst rewrites it, then the physical plan shows the chosen operators (`Project`, `Filter`, `HashJoin`). |
| **Cost‑Based Optimizer (CBO)** | Introduced in Spark 3.x.  CBO estimates row counts using statistics (`spark.sql.statistics.collectSampleStats`).  It decides broadcast vs. shuffle join, and whether to push predicates. |
| **Explain & Show** | `df.explain(extended=True)` prints the logical + physical plan.  `df.explain(true)` also adds the metrics (e.g., `Estimated Cost`).  These are the primary exam artifacts. |
| **Broadcast Join** | When the right side of a join is below `spark.sql.autoBroadcastJoinThreshold` (default 10 MiB) Spark will automatically broadcast it.  You can force it with `broadcast(df)`.  **Cost‑tradeoff:** reduces shuffle but increases executor memory. |
| **Shuffle Partitions** | `spark.sql.shuffle.partitions` defaults to the number of cores in the cluster (usually 200).  Too many leads to small partitions and overhead; too few can cause large stragglers. |

### 2. Data Layout & I/O Optimizations  

| Concept | Why it matters on AWS Databricks |
|---------|-----------------------------------|
| **Columnar formats (Parquet/Delta)** | Reads only needed columns, reduces S3 GET requests.  Use `snappy` compression (default) – 1‑2 MiB per file is optimal for S3 (smaller files increase request latency). |
| **Partitioning** | Data is pruned when the partition column is used in a filter.  Choose **high‑cardinality, filter‑friendly** columns (e.g., `event_date`).  Avoid over‑partitioning (e.g., >10 k partitions) – each partition maps to a Spark task. |
| **Z‑Ordering** | Within Delta, Z‑order clusters data by a set of columns (`OPTIMIZE ... ZORDER BY (col1, col2)`).  Reduces file scans for queries that filter on those columns. |
| **Data Skipping (Bloom filters, min/max)** | Enabled by default for Delta.  Bloom filters help skip non‑matching rows for `!=` predicates.  You can tune `spark.databricks.delta.statistics` to keep column stats fresh. |
| **Caching & Persistence** | Use `df.persist(StorageLevel.MEMORY_AND_DISK)` sparingly.  In a streaming job, checkpointing is the right mechanism; in a batch job, caching can hide repeated reads but incurs shuffle when evicted. |

### 3. Execution Tuning – Core Settings  

| Setting | Typical Range | Effect |
|---------|----------------|--------|
| `spark.databricks.io.cache.enabled` | `true` / `false` | Enables in‑node parquet cache.  Improves repeated reads of same table but adds heap pressure. |
| `spark.sql.shuffle.partitions` | 1‑2 × total cores (often 200‑500) | Controls number of reducers for joins, aggregations, and writes. |
| `spark.sql.adaptive.enabled` | `true` (recommended) | Allows dynamic reduction of shuffle partitions at runtime. |
| `spark.sql.broadcastTimeout` | `300` seconds (default) | Increase when joining large tables that must be broadcast. |
| `spark.databricks.optimizer.dynamicPartitionPruning` | `true` | Enables runtime pruning of partitions for joins. |

### 4. Data Skew – The Silent Killer  

- **Symptom:** One task takes > 90 % of stage time; others are near‑idle.  
- **Root cause:** A join key with a heavy‑tailed distribution (e.g., `user_id` where a few users have billions of rows).  
- **Detection:** `df.groupBy("col").count().orderBy(desc("count"))` or Spark UI “Tasks” view.  
- **Fixes:**  
  1. **Salting** – Add a random bucket column to the heavy side before the join.  
  2. **Skew‑join hint** – `df1.join(df2.hint("skew")`, ...) – tells Spark to use a different join strategy.  
  3. **Broadcast with larger threshold** – if the skewed side is still small after salting.  

### 5. Streaming‑Specific Tuning  

| Area | Key knob | Recommended value |
|------|----------|-------------------|
| **Trigger** | `trigger(processingTime='30 seconds')` | Align with S3 list frequency; avoid sub‑second triggers that cause many empty micro‑batches. |
| **Checkpoint directory** | Write to highly durable S3 bucket with `fs.s3a.fast.upload=true` | Prevents data loss and reduces retries. |
| **Auto Loader checkpointing** | Use `cloudFiles`, `maxFilesPerTrigger=10000`, `mergeSchema=false` | Controls file discovery latency and schema drift handling. |
| **State store** | `spark.sql.streaming.stateStore.maintainer.batchSizeRows=50000` | Larger batches reduce the number of state writes. |

---  

## Architecture / How It Works  

The diagram below shows a typical end‑to‑end pipeline on AWS Databricks and highlights where each performance knob lives.  

```mermaid
flowchart LR
    subgraph AWS[ AWS Infra ]
        S3Raw[ S3 Raw Bucket ]:::s3
        S3Staging[ S3 Staging Bucket ]:::s3
        GlueCatalog[ AWS Glue Catalog ]:::glue
    end

    subgraph Databricks[ Databricks Workspace ]
        AutoL[ Auto Loader (Streaming) ]:::db
        Bronze[ Bronze Delta (bronze_db)]:::delta
        Silver[ Silver Delta (enriched)]:::delta
        Gold[ Gold Delta (BI)]:::delta
        Cache[ In‑Node Cache (Databricks.io.cache)]:::cache
    end

    S3Raw -->|PUT| AutoL
    AutoL -->|write| Bronze
    Bronze -->|read| GlueCatalog
    GlueCatalog -->|lookup| Silver
    Silver -->|write| Gold
    Gold -->|read| downstream[ BI / Looker ]:::downstream

    classDef s3 fill:#f8f9fa,stroke:#bbb,stroke-width:1px;
    classDef glue fill:#e2f0d9,stroke:#5a9;    
    classDef db fill:#dfe7f6,stroke:#2a6;    
    classDef delta fill:#fff3cd,stroke:#e69;    
    classDef cache fill:#fff,stroke:#999,stroke-dasharray: 5 5;    
    classDef downstream fill:#f2dede,stroke:#c33;
```

**How the knobs map to the diagram**  

| Region | Performance knobs you can apply |
|--------|---------------------------------|
| **S3 Raw** | – **multipart upload / S3 Transfer Acceleration** (`fs.s3a.fast.upload=true`). <br> – **Consistent view** (`s3.enableRequestSigning=true`) to avoid list‑after‑write latency. |
| **Auto Loader** | – `cloudFiles` options for **file discovery parallelism** (`maxFilesPerTrigger`). <br> – **Auto Loader checkpointing** (writes to `s3Staging`). |
| **Bronze Delta** | – **Partitioning on ingestion date** (`partitionBy("date")`). <br> – **Z‑ordering on `customer_id`** for later lookups. |
| **Silver** | – **Broadcast small reference tables** (`hint("broadcast")`). <br> – **Adaptive query execution** for join re‑partitioning. |
| **Gold** | – **Optimized storage format** (`parquet` + `snappy`). <br> – **Cache hot tables** (`cache.table("gold_popular")`). |
| **Downstream** | – **Cache size awareness** – keep hot subset in **Databricks io cache** to reduce downstream S3 GETs. |

---  

## Hands-On: Key Operations  

Below is a **self‑contained notebook** you can copy into a Databricks cluster (Python 3.10, DBR 13.3).  Each block is annotated with the exact knob you are exercising and why it matters for the exam.

> **Prerequisite** – Run the following first to create a tiny bronze table:  

```sql
-- Bronze: raw clickstream data (10 M rows)
CREATE TABLE IF NOT EXISTS bronze.clicks (
  event_id   STRING,
  user_id    STRING,
  event_ts   TIMESTAMP,
  page       STRING,
  revenue    DOUBLE
)
USING DELTA
PARTITIONED BY (event_date)
LOCATION 's3://my-raw-bucket/clicks/';
```

---  

### 1️⃣ Inspect the physical plan  

```python
# Load a DataFrame
clicks = spark.read.format("delta").table("bronze.clicks")

# Simple filter that should be pushed down
filtered = clicks.filter(clicks.event_ts >= "2024-01-01")

# Show the extended plan
filtered.explain(extended=True)
```

**What to look for**  

- `Project` and `Filter` nodes are **pushed down** to the Delta source (see `PushedFilters`).  
- `FileScan` shows the **partition pruning** (`event_date` partition filter).  

**Exam tip:** The exam may ask you to spot a missing pruning predicate – that’s often a sign the column is **not** in the table’s partitioning scheme.

---  

### 2️⃣ Choose the right join strategy  

```python
# A small reference dataset (5 MB) and a large clicks table
references = spark.read.parquet("s3://reference/geo_lookup.parquet")
clicks_small = clicks.filter(clicks.event_date == "2024-02-01")  # ~5 M rows, ~300 MB

# Force broadcast join (exam expects you to use broadcast hint)
enriched = clicks_small.join(
    references.hint("broadcast"),
    on="country_code",
    how="left"
)

# Verify that Spark used a broadcast join
enriched.explain(extended=True)
```

**Why it matters**  

- The **right side** of the join is below the broadcast threshold.  
- The **hint** ensures the optimizer does not decide otherwise (e.g., due to a badly stale statistic).  

**Exam question:** “You see a shuffle stage when joining a 300 MiB table to a 10 GiB table. What should you change?” → *Add a broadcast hint or increase the broadcast threshold.*  

---  

### 3️⃣ Optimize data layout – Z‑ordering & OPTIMIZE  

```python
# Z‑order the bronze clicks table on user_id (high cardinality, frequent filter)
spark.sql("""
  OPTIMIZE bronze.clicks
  ZORDER BY (user_id)
""")

# Verify file statistics are fresh (helps CBO)
spark.sql("SET spark.databricks.delta.retentionDuration.check.enabled = false")
spark.sql("ANALYZE TABLE bronze.clicks COMPUTE STATISTICS FOR COLUMNS user_id")
```

**Result** – After `OPTIMIZE`, a query that filters by `user_id = 'U123'` will scan **~1 % of the files** instead of the whole dataset.  

---  

### 4️⃣ Tune shuffle partitions with Adaptive Query Execution (AQE)  

```python
# Enable AQE (usually already true in DBR)
spark.conf.set("spark.sql.adaptive.enabled", True)

# Run a join that will start with 500 partitions but AQE can shrink it
left = spark.range(0, 50_000_000, numSlices=500)   # large dataset
right = spark.range(0, 5_000_000, numSlices=50)

joined = left.join(right, "id")
joined.explain(extended=True)   # look for "AdaptiveExecution" and "ShufflePartitions"
```

**What to observe**  

- The **initial plan** shows 500 shuffle partitions.  
- At runtime, AQE can **reduce** this number (see `AdaptiveShufflePartitioning`).  

**Exam focus:** *Adaptive Query Execution is a must‑have for any production job – you should enable it unless you have a strong reason not to.*  

---  

### 5️⃣ Detect and fix data skew  

```python
# Identify skewed join key
skew_counts = (clicks.groupBy("user_id")
                 .agg(count("*").alias("cnt"))
                 .orderBy(desc("cnt"))
                 .limit(5)
                 .collect())

print("Top 5 user_id by volume:")
for r in skew_counts:
    print(r["user_id"], r["cnt"])
```

If the largest user ID accounts for **> 10 %** of rows, the next step is to **salt**:

```python
from pyspark.sql.functions import col, floor(rand()*10).alias("salt")

# Add 10‑bucket salt to the large side
large = clicks.withColumn("salt", floor(col("rand()") * 10).cast("int"))

# Explode the reference side to have the same salt key
ref = references.withColumn("salt", lit(0))

joined_salted = large.join(
    ref,
    (large.user_id == ref.user_id) & (large.salt == ref.salt),
    how="left"
)
```

**Result:** The heavy user is now distributed across 10 tasks instead of 1, eliminating the straggler.  

---  

### 6️