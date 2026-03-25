## Data Transformation and ETL Pipelines  

> **Section 9 of 15 – AWS Databricks Data Engineer Certification**  
> **Target audience:** Data engineers who already know Apache Spark and AWS Glue and want to ace the **Databricks Certified Data Engineer Associate (AWS)** exam.  

---  

### Overview  

Data transformation is the heart of every analytics platform. In a modern cloud lakehouse you rarely move data from a source to a target in a single step; you typically **ingest**, **clean**, **enrich**, **aggregate**, and **publish** data through a series of reusable, version‑controlled pipelines.  

* In **Spark**, transformations are expressed as lazy, immutable DataFrame operations (`select`, `withColumn`, `join`, `groupBy`, …). When you trigger an action (`write`, `collect`, `show`), Spark materialises the logical plan into a physical DAG of tasks.  
* **Databricks** augments Spark with a set of production‑ready features that make ETL pipelines resilient, observable, and cloud‑native: **Auto Loader** (continuous, schema‑evolution aware), **Structured Streaming** integration, **Delta Lake** transactional guarantees, **Job Clusters** vs. **All‑Purpose Clusters**, and **Workspace‑level job dependencies**.  
* On **AWS**, these capabilities sit on top of the storage and security primitives you already use: **S3** as the data lake, **IAM** for fine‑grained permissions, **AWS Glue** for catalog and schema discovery, **EMR** (or Serverless Spark) for compute, **Lake Formation** for fine‑grained data‑access policies, and **CloudWatch** for metrics & alerts.  

The exam expects you to understand **how to design a maintainable ETL pipeline**, not just how to write a single Spark job. You’ll be asked to:

1. Choose the right **trigger mode** (batch vs. continuous) for a given ingestion pattern.  
2. Apply **schema evolution** safely with Delta Lake.  
3. Use **Auto Loader** to avoid data‑loss when files arrive asynchronously in S3.  
4. Implement **idempotent processing** (exact‑once semantics) using **checkpointing** and **Delta’s merge**.  
5. Integrate with **AWS Glue Data Catalog** to keep a single source of truth for table metadata.  

By the end of this section you will be able to sketch a full‑end‑to‑end ETL architecture on a whiteboard, explain why each component is placed where it is, and write the minimal Spark code that a production team would put under version control.  

---  

### Core Concepts  

Below are the building blocks you must master. Each sub‑section can be a separate lecture (≈5‑7 min) or a deep‑dive in a lab.  

| Concept | Why it matters for the exam | Typical gotchas |
|---------|----------------------------|-----------------|
| **Delta Lake table format** | Guarantees ACID, schema enforcement, and upserts. | Using the `append` mode on a non‑Delta target leads to race conditions. |
| **Auto Loader (cloudFiles)** | Incrementally discovers new files, avoids schema drift, and automatically handles file‑arrival latency. | Forgetting to set `readAutoFiles` or using `recursive` incorrectly can cause duplicate ingestion. |
| **Structured Streaming** | Allows you to treat continuous ingestion as a streaming query with exactly‑once guarantees. | Not setting `outputMode` (`append` vs `complete`) leads to downstream validation errors. |
| **Checkpointing** | Provides a reliable offset store for streaming and a replay‑safe restart for batch jobs. | Storing checkpoints in the same bucket as the raw data can cause permission errors. |
| **MERGE (Delta upserts)** | The idiomatic way to implement “process‑and‑update” pipelines. | Mismatched partitioning keys can create many small files after a merge. |
| **Job orchestration & dependencies** | Databricks Jobs can trigger other jobs, pass parameters, and retry on failure. | Using the same **Job Cluster** for unrelated jobs can cause Spark UI clutter and resource contention. |
| **Glue Catalog integration** | Enables schema‑on‑read across services (Athena, Redshift Spectrum, EMR). | Not granting `SELECT` on the Glue catalog to the EMR role leads to “Table not found” errors. |
| **IAM & Lake Formation policies** | Control who can read/write at the object level. | Over‑permissive bucket policies can expose raw data to downstream consumers. |
| **Observability (CloudWatch, Spark UI, DBX)** | Detect failures early and meet SLA. | Ignoring streaming back‑pressure metrics can hide bottlenecks. |

#### 1. Delta Lake Fundamentals  

* **Table storage** – A Delta table is a directory (`/path/to/table/_delta_log/`) that holds JSON log files describing every commit.  
* **Schema enforcement** – `ALTER TABLE … SET TBLPROPERTIES (delta.autoOptimize.optimizeWrite = true)` forces Spark to write Optimized Writes.  
* **Time travel** – You can query a previous version with `VERSION AS OF` or `TIMESTAMP AS OF`.  

#### 2. Auto Loader  

```python
df = (
    spark.readStream
         .format("cloudFiles")
         .option("cloudFiles.format", "parquet")
         .option("cloudFiles.schemaLocation", "/mnt/checkpoints/s3_raw/schema")
         .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
         .load("s3://my-lake/raw/events/")
)
```

* **`cloudFiles`** abstracts the S3 `listObjectsV2` call, tracks the last successful batch, and automatically retries transient errors.  
* **`schemaLocation`** persists the discovered schema so subsequent micro‑batches can evolve safely.  

#### 3. Incremental MERGE Example  

```python
source = spark.read.format("delta").load("s3://my-lake/staging/events/2024-10-01/")
target = spark.read.format("delta").load("s3://my-lake/curated/events/")

(
    source.alias("s")
    .merge(
        target.alias("t"),
        "s.event_id = t.event_id"
    )
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)
```

* Guarantees **idempotency** – re‑running the same micro‑batch does not create duplicate rows.  

#### 4. Job Cluster vs. All‑Purpose Cluster  

| Cluster type | Use‑case | Exam‑relevant detail |
|--------------|----------|-----------------------|
| **All‑Purpose** | Interactive notebooks, ad‑hoc analysis | Ideal for *development*; not recommended for production ETL because it can be paused and affect job SLAs. |
| **Job Cluster** (created per job, terminated on completion) | Production pipelines, scheduled jobs | Guarantees **resource isolation**, ensures cost predictability, and is required for **exactly‑once** guarantees when using checkpointing. |

---  

### Architecture / How It Works  

Below is a typical **real‑time ETL pipeline** that ingests raw CSV/JSON files from an external SaaS system into a Delta Lake curated zone.  

```mermaid
graph TD
    subgraph Ingest Layer
        A[External SaaS (JSON) -> S3 bucket: raw/events/] 
        B[Auto Loader (continuous) reads from raw/events/]
    end

    subgraph Processing Layer
        B --> C[Spark Structured Streaming job (Job Cluster)]
        C --> D[Delta Lake Staging (s3://lake/staging/events/)]
        D --> E[MERGE into curated table (s3://lake/curated/events/)]
    end

    subgraph Serving Layer
        E --> F[Databricks SQL endpoint / dbt models for analysts]
    end

    subgraph Ops & Governance
        G[CloudWatch Alarms] --> H[Databricks Job Cluster (retries)]
        I[Lake Formation tags] --> E
    end
```

**Explanation of the flow**  

1. **External SaaS** pushes new event files into `s3://my‑lake/raw/events/` every few minutes.  
2. **Auto Loader** continuously polls that prefix, detects new objects, and streams them into a **Spark Structured Streaming** query.  
3. The streaming query writes **batches** to a *staging* Delta table (`/staging/events/`).  
4. In a separate **batch** step (or using a trigger `once`), a **MERGE** operation upserts the staging data into the *curated* Delta table.  
5. The curated table is exposed via a **SQL warehouse** and consumed by downstream analysts; Lake Formation tags on the table enforce column‑level access.  
6. **CloudWatch** monitors the job’s `processing_time` and `num_records` metrics; an alarm triggers a retry on the Job Cluster.  

---  

### Hands‑On: Key Operations  

Below are **copy‑paste ready** snippets. Each block contains a short comment describing the purpose and any *gotchas* to watch for.  

#### 1️⃣ Set up the S3 bucket & IAM role (Terraform‑style)  

```hcl
resource "aws_s3_bucket" "lake_raw" {
  bucket = "my-company-raw-events"
  force_destroy = true
  tags = { Environment = "dev" }
}

resource "aws_iam_role" "databricks_etl" {
  name = "databricks-etl-role"
  assume_role_policy = data.aws_iam_policy_document.databricks_assume.json
}

resource "aws_iam_policy" "s3_access" {
  name = "LakeRawAccess"
  policy = data.aws_iam_policy_document.s3_access.json
}
```

*You need `s3:ListBucket`, `s3:GetObject`, `s3:PutObject` on `my-company-raw-events/*` and `s3:GetObjectVersion`, `s3:PutObjectVersion` on the checkpoint folder.*  

#### 2️⃣ Auto Loader + Structured Streaming (PySpark)  

```python
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, TimestampType

# 1. Define schema (adjust to SaaS payload)
event_schema = StructType() \
    .add("event_id", StringType()) \
    .add("event_type", StringType()) \
    .add("user_id", StringType()) \
    .add("event_ts", TimestampType())

# 2. Read with Auto Loader (continuous mode)
raw_stream = (
    spark.readStream
         .format("cloudFiles")
         .option("cloudFiles.format", "json")
         .option("cloudFiles.schemaLocation", "/mnt/checkpoints/events/schema")
         .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
         .option("maxFilesPerTrigger", 1000)   # prevents overwhelming downstream
         .load("s3://my-company-raw-events/events/")
         .select(from_json(col("value").cast("string"), event_schema).alias("data"))
         .select("data.*")
)

# 3. Write to Delta staging (append mode, deterministic)
query = (
    raw_stream
      .writeStream
      .format("delta")
      .outputMode("append")
      .option("checkpointLocation", "/mnt/checkpoints/events/checkpoint")
      .option("mergeSchema", "true")
      .trigger(availableNow=False)   # default is continuous
      .start("s3://my-company-lake/staging/events/")
)
```

**Key points**  

* `maxFilesPerTrigger` caps batch size; use a value that fits your downstream merge latency.  
* `checkpointLocation` must be on *different* S3 bucket (or a different prefix) than the data you’re ingesting.  
* `availableNow=False` forces continuous mode; change to `once` for a batch‑style ETL.  

#### 3️⃣ MERGE into curated Delta table (batch, run as a separate job)  

```python
from delta.tables import DeltaTable

staging_path = "s3://my-company-lake/staging/events/"
curated_path = "s3://my-company-lake/curated/events/"

# Load both tables
staging_df = spark.read.format("delta").load(staging_path)
curated_df = spark.read.format("delta").load(curated_path)

# Resolve partitioning (e.g., partitionBy("event_date"))
target_delta = DeltaTable.forPath(spark, curated_path)

target_delta.alias("t") \
    .merge(
        source=staging_df.alias("s"),
        condition="s.event_id = t.event_id"
    ) \
    .whenMatchedUpdateAll() \
    .whenNotMatchedInsertAll() \
    .execute()
```

**Why this is idempotent** – Re‑running the job after a failure will process the *same* staging files, but the `MERGE` condition ensures rows already present are simply *updated*, not duplicated.  

#### 4️⃣ Register the curated table with AWS Glue Catalog  

```sql
CREATE DATABASE IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.events
USING DELTA
LOCATION 's3://my-company-lake/curated/events/'
TBLPROPERTIES (
  delta.autoOptimize.optimizeWrite = 'true',
  delta.enableChangeDataFeed = 'true'
);
```

*After this, you can query the table from Athena, Redshift Spectrum, or an EMR Spark job without copying data.*  

#### 5️⃣ Monitoring with CloudWatch  

In the Databricks job UI, under **Tasks → Monitoring**, enable **“Send task metrics to CloudWatch”** and configure a metric filter:

| CloudWatch Metric | Alarm Threshold | Intent |
|-------------------|-----------------|--------|
| `ProcessingTime` (seconds) | > 30 | Indicates slow file arrivals or cluster sizing. |
| `FailedTasks` (count) | > 0 | Triggers SNS notification for immediate investigation. |

---  

### AWS-Specific Considerations  

| AWS Service | Role in the ETL pipeline | Practical tip for the exam |
|-------------|--------------------------|-----------------------------|
| **Amazon S3** | Raw, staging, curated zones; source and destination for Delta tables. | Use **S3 **`S3Prefix`** in IAM policies to restrict a job to only its own prefixes (least‑privilege). |
| **AWS IAM** | Grants Spark executors permission to read/write S3, list Glue tables, and put CloudWatch logs. | Attach **`AWSGlueServiceRole`** + **`DatabricksS3FullAccess`** policies; never give `*` on the bucket. |
| **AWS Glue Data Catalog** | Central metadata store; Spark can read/write tables directly (`catalogName.tableName`). | Register every Delta table with Glue **once**; after that, use `spark.read.table("analytics.events")`. |
| **AWS Lake Formation** | Row‑ and column‑level security on top of the Glue catalog. | Grant `SELECT` on a column to a data‑science role; the underlying S3 policy remains open, but LF blocks unauthorized reads. |
| **EMR (Serverless Spark or EMR on EC2)** | Optional compute engine; can run the same Delta jobs if you cannot use Databricks. | When using EMR, you must set `--conf spark.databricks.delta.retentionDurationCheck.enabled=false` for **short‑lived tables**. |
| **CloudWatch** | Stores logs, metrics, and triggers alarms for job health. | Export **Spark UI metrics** (`spark.ui.enabled=true`) to CloudWatch Logs; then create a metric math expression for `failed_tasks / total_tasks`. |
| **Step Functions (optional)** | Orchestrates multi‑step pipelines (e.g., ingestion → validation → downstream enrich). | Use a **catch** block to move a failed ingestion to a *dead‑letter S3* bucket for later replay. |

**Common AWS pitfalls**  

* **S3 eventual consistency** (especially when using `listObjectsV2` in custom Auto Loader scripts). Rely on the built‑in Auto Loader, not hand‑rolled S3 listing.  
* **IAM role session duration** – Auto Loader may create many short‑lived S3 GET/PUT calls; set the role’s **max session duration** to at least 1 hour to avoid temporary credential expiration.  
* **Glue crawler race condition** – If you run a crawler on the curated bucket *while* a job is writing, the crawler can create a *conflicting schema* and cause job failures. Schedule crawlers at off‑peak times or set `--add-column-if-not-exists`.  

---  

### Exam Focus Areas  

- **Auto Loader options** – `cloudFiles.format`, `schemaLocation`, `mergeSchema`, `maxFilesPerTrigger`, and *continuous* vs *micro‑batch* triggers.  
- **Delta Lake upserts** – `MERGE` syntax, `whenMatchedUpdateAll`, `whenNotMatchedInsertAll`, and why you need `OPTIMIZE` after many small files.  
- **Checkpointing strategy** – Where to place it (different bucket/prefix), supported formats (Delta, plain Parquet), and impact on **exact‑once** semantics.