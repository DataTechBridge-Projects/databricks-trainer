## Capstone and Exam Readiness {#section-15}

> **Goal of this section** –  By the end of the 45‑60 min walkthrough you will have (1) built a production‑grade end‑to‑end data‑engineering pipeline that mirrors the format of the Databricks Certified Data Engineer Associate exam, (2) internalised the “must‑know” concepts that the exam stresses, and (3) equipped yourself with a reusable cheat‑sheet of commands, patterns, and AWS‑specific knobs you can reference on test day.  

---

### Overview  

The **Capstone** in this course is deliberately built around the same three‑phase architecture that the exam evaluates:  

1. **Ingestion** – Reliable, idempotent capture of raw data from S3 (or Kinesis) using **Auto Loader** and **Structured Streaming**.  
2. **Transformation & Business Logic** – Declarative, testable transformations written in **Delta Lake**, leveraging **spark.sql()** and **DataFrame API**, and protected by **schema enforcement** and **time‑travel**.  
3. **Serve & Govern** – Secure, governed tables that are instantly queryable from Athena, Redshift Spectrum, or downstream Databricks notebooks, with full auditability via **CloudWatch** and **AWS Lake Formation** integration.  

Each phase maps directly to a *domain* in the exam blueprint (Data Ingestion, Data Storage, Data Governance, and Data Operations). The capstone forces you to make design decisions (e.g., trigger‑once vs. continuous, checkpointing strategy, IAM policy granularity) that you will be asked to justify on the exam.  

---

### Core Concepts  

| Concept | Why It Matters for the Associate Exam | Practical Tips |
|---------|----------------------------------------|----------------|
| **Delta Lake ACID transactions** | The exam expects you to know how to achieve *exactly‑once* semantics, avoid write skew, and use **time‑travel** for data recovery. | Use `OPTIMIZE` + `ZORDER`, enable `delta.logRetentionDuration`, and demonstrate a rollback: `spark.sql("RESTORE TABLE mydb.mytable TO VERSION AS OF 5")`. |
| **Auto Loader (cloudFiles)** | Auto Loader is the preferred way to ingest streaming data on AWS; it automatically handles file detection, schema evolution, and **checkpoint** management. | Read files with `df = spark.readStream.format("cloudFiles").option("cloudFiles.format", "json").load("s3://bucket/raw/")`. Turn on `maxFilesPerTrigger` for batch‑like behavior. |
| **Schema Evolution & Merge (Delta MERGE INTO)** | The exam tests ability to implement *slowly changing dimensions* and **upserts** efficiently. | Keep `spark.databricks.delta.retentionDuration` at default (30 days) for safe deletes, and always filter on the **primary key** before a merge to avoid duplicate writes. |
| **Spark Optimizer (Catalyst) & Adaptive Query Execution (AQE)** | You must identify when AQE can improve a job (e.g., skew joins) and how to enable/disable it. | Set `spark.sql.adaptive.enabled = true` and use `spark.sql.adaptive.skewJoin.enabled = true`. Show the `EXPLAIN` output that includes `AQE` stages. |
| **Structured Streaming Checkpoints** | Checkpoint location drives fault‑tolerance; the exam will ask where to place it (e.g., S3 vs. EBS) and how to clean it. | Use `df.writeStream.setCheckpointLocation("s3://my-checkpoints/")`. Keep the checkpoint **separate** from the source data, and enable `spark.databricks.delta.retentionDuration` to control checkpoint cleanup. |
| **Lake Formation & IAM Integration** | Governance is a hot‑topic. The exam expects you to know how to **grant** and **revoke** permissions at the *catalog* and *table* level. | Grant with `grant CREATE TABLE ON DATABASE mydb TO `iam_user`;`. Use `aws glue get-database` to verify the underlying S3 location. |
| **Data Quality Tests (Declarative Tests)** | The exam includes a question about *continuous validation* – use **Delta Table Constraints** or **Great Expectations** integrated via `spark_df.where("...").count() == 0`. | Add a constraint: `ALTER TABLE mydb.mytable ADD CONSTRAINT my_constraint CHECK (amount > 0)`. |
| **Cost‑Optimised Query Execution** | You’ll need to reason about **caching**, **photon** vs. **spark‑sql**, and **cluster pool** sizing. | Enable Photon: `spark.databricks.optimizer.photon.enabled = true`. Use `spark.databricks.clusterProfile=...` to pick the right pool (e.g., `i3.xlarge` for small batch jobs, `r5.2xlarge` for heavy aggregations). |

---

### Architecture / How It Works  

The following **Mermaid diagram** captures the data flow for the capstone pipeline, highlighting AWS‑specific touch‑points (S3, IAM, Glue, Lake Formation).  

```mermaid
flowchart TD
    subgraph Ingest[Ingestion Layer]
        A[S3 Bucket: raw/events/] -->|Event notifications| B[Auto Loader (spark.readStream.format('cloudFiles'))]
    end

    subgraph Processing[Transformation Layer]
        B --> C[Delta Lake Table: bronze.events]
        C -->|Streaming query| D[Structured Streaming Job (Spark Structured Streaming)]
        D --> E[Delta MERGE (upserts) → silver.events]
        E -->|Batch job| F[Spark SQL (Databricks SQL) for enrichment]
        F --> G[Delta Lake Table: gold.events]
    end

    subgraph Governance[Governance Layer]
        G -->|Table grants| H[AWS Glue Data Catalog (via Lake Formation)]
        H --> I[IAM Role: databricks-data-eng]
        H --> J[CloudWatch Logs + Alerts]
    end

    style Ingest fill:#f9f,stroke:#333,stroke-width:2px
    style Processing fill:#bbf,stroke:#333,stroke-width:2px
    style Governance fill:#cfc,stroke:#333,stroke-width:2px
```

**Explanation of the flow**  

1. **Raw S3 bucket** receives files from an external SaaS system (e.g., Stripe webhook). Event notifications trigger **Auto Loader** which continuously scans the bucket for new files.  
2. The streaming query writes **bronze** (raw) Delta tables with **append‑only** writes and a *checkpoint* on a separate S3 path (`s3://my‑project/checkpoints/events/`).  
3. A **batch job** (scheduled via `spark.databricks.job.runNow()` or AWS Step Functions) reads the bronze tables, performs **schema enforcement** (e.g., `cast(ts as timestamp)`), then writes the **silver** table via **MERGE** to upsert changes.  
4. The **gold** table is the final, query‑ready dataset. It is registered in **AWS Glue** (Lake Formation) and given **SELECT** permissions to downstream BI tools.  
5. **CloudWatch** dashboards monitor ingestion latency (`processing_time - event_time`) and error counts (`spark.streams.lastException`).  

---

### Hands-On: Key Operations  

Below are **self‑contained snippets** you can copy into a Databricks notebook. Each block is annotated with the *exam‑relevant* concept it demonstrates.

#### 1. Auto Loader – Continuous Ingestion

```python
# -------------------------------------------------
# 1️⃣ Auto Loader – Ingest new JSON events from S3
# -------------------------------------------------
raw_events_path = "s3://my-data-lake/events/raw/"

df_raw = (spark.readStream
          .format("cloudFiles")                     # <-- Auto Loader
          .option("cloudFiles.format", "json")
          .option("cloudFiles.schemaLocation", "s3://my-data-lake/_schemas/events_schema.json")
          .option("maxFilesPerTrigger", 1000)       # Small batches → near‑real‑time
          .load(raw_events_path))

# Attach a processing timestamp (exam‑focus: event time handling)
df_enriched = df_raw.withColumn("ingest_ts", current_timestamp())

# Write to a bronze Delta table (append only)
query = (df_enriched
         .writeStream
         .format("delta")
         .outputMode("append")
         .option("checkpointLocation", "s3://my-data-lake/checkpoints/events/bronze/")
         .table("my_data_events.bronze_events"))

query.awaitTermination()
```

*What to remember*: Auto Loader automatically **deduplicates** using a *metadata cache* in `schemaLocation`. The `maxFilesPerTrigger` option makes the streaming job behave like a *mini‑batch* – a pattern often asked about in the exam.

---

#### 2. Schema Evolution & Delta MERGE (Silver)

```python
# -------------------------------------------------
# 2️⃣ Silver layer – up‑sert (MERGE) incoming events
# -------------------------------------------------
silver_path = "s3://my-data-lake/events/silver/"
bronze_table = "my_data_events.bronze_events"
silver_table = "my_data_events.silver_events"

# Ensure bronze table exists as Delta
spark.sql(f"CREATE TABLE IF NOT EXISTS {bronze_table} USING DELTA LOCATION '{raw_path}'")

# Transform – cast types, enrich with a static lookup
df_silver = (spark.table(bronze_table)
             .withColumn("event_ts", col("event_ts").cast("timestamp"))
             .withColumn("is_fraud", when(col("amount") > 1000, True).otherwise(False)))

# Upsert to silver (primary key = (event_id))
(df_silver.write.format("delta")
   .mode("overwrite")   # Overwrite for simplicity in notebook; exam will use MERGE
   .saveAsTable(silver_table))

# Explicit MERGE (recommended for production)
df_silver = spark.table(silver_table).alias("tgt")
df_silver_upd = df_silver_upd.alias("src")

spark.sql(f"""
MERGE INTO {silver_table} AS tgt
USING (SELECT * FROM df_silver_upd) AS src
ON tgt.event_id = src.event_id
WHEN MATCHED AND src.is_latest = true THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
""")
```

*Exam tip*: When the question asks **how to implement SCD‑Type 1** on a streaming source, answer with a **Delta MERGE** that filters on a *watermark* or *is_latest* flag.

---

#### 3. Time‑Travel + Restore (Gold)

```python
# -------------------------------------------------
# 3️⃣ Gold layer – roll back a bad batch (time‑travel)
# -------------------------------------------------
gold_table = "my_data_events.gold_events"

df_gold = (spark.read.format("delta")
          .option("versionAsOf", 5)   # Pretend version 5 had a bug
          .loadAsTable(gold_table))

# Spot the bug: amount column has negative values
spark.sql("SELECT AVG(amount) FROM my_data_events.gold_events WHERE amount < 0").show()

# Restore to version 4 (good data)
spark.sql(f"RESTORE TABLE {gold_table} TO VERSION AS OF 4")
spark.sql("SELECT * FROM {gold_table} LIMIT 10").show()
```

*Why it matters*: The exam will present a scenario where a batch job produces bad data. You must be able to **point‑in‑time** query and **restore** a table without manual copy‑pastes.

---

#### 4. Auditing with Lake Formation & IAM

```sql
-- Grant Lake Formation permissions (run as a Glue admin)
GRANT SELECT ON DATABASE my_data_events TO `arn:aws:iam::123456789012:user/databricks-data-eng`;
GRANT CREATE TABLE ON DATABASE my_data_events TO `awsdatabricksteam`;

-- Verify IAM policy (excerpt for the Databricks service principal)
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "glue:BatchCreateTable",
        "glue:GetTable",
        "glue:GetDatabase",
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "*"
    }
  ]
}
```

*Key takeaway*: The exam often asks *who* can **create a table** in a catalog that is governed by **Lake Formation** – you must reference both the **IAM principal** and the **Lake Formation grant** (they must align).

---

### AWS‑Specific Considerations  

| AWS Service | Role in the Capstone | Configuration Nuances |
|-------------|----------------------|-----------------------|
| **Amazon S3** | Raw, processed, checkpoint, and Athena output locations. | • Use **S3 bucket policies** that allow `s3:GetObject` for the Databricks VPC role **and** `s3:PutObject` for the `bronze/` and `silver/` prefixes only. <br>• Enable **S3 Object Versioning** on raw and silver to safeguard against accidental deletes. |
| **AWS Glue Data Catalog** (used by Delta Lake) | Central metadata store; integrated with **Lake Formation** for fine‑grained access. | • Register a **Database** with `catalog=awsdatabricks`. <br>• Use **Crawler** to automatically populate the `bronze_events` schema, then override the crawler's classifier to `json` with `allowMultipleLine`. |
| **AWS Lake Formation** | Fine‑grained table permissions. | • Grant `CREATE_TABLE` on the *catalog* to the Databricks IAM role. <br>• Use `GRANT SELECT` on the *gold* table to the analytics role (e.g., `quicksight.amazonaws.com`). |
| **IAM Roles** | Databricks workspace attaches an instance profile (`DatabricksInstanceProfile`). | • The role must have `AWSLambdaReadOnlyAccess` (if using Lambda for validation) and `CloudWatchFullAccess` for logging. <br>• Scope the role to **least privilege**: `s3:ListBucket` on `my-data-lake/`, `s3:GetObject` on `my-data-lake/checkpoints/`, `s3:PutObject` on `my-data-lake/processed/`. |
| **Amazon EMR** | (Optional) Deploy a **managed EMR Serverless** Spark pool for cost‑effective batch jobs. | • Use **EMRFS consistent view** to avoid eventual consistency issues when reading/writing checkpoints. |
| **AWS Step Functions** | Orchestrate the batch **Silver → Gold** transformation. | • Define a **Task State** that calls a Databricks Job API (`triggerNow`), then a **Choice** state that handles failures. |
| **Amazon CloudWatch** | Real‑time observability. | • Set a **Metric Filter** on the `spark` log group to capture `StreamingQueryListener` errors. <br>• Create an **Alarm** for > 5 min ingestion latency. |

**Gotchas**  

* **Checkpoint location** must be **globally unique** (cannot be under a bucket that has **eventual consistency** for `PUT`). Prefer a dedicated S3 bucket with **VPC Endpoint** to avoid public internet egress.  
* **Lake Formation registration** of the Glue catalog is a *separate* step from enabling the **Data Catalog** in the Databricks workspace; the exam may ask you to distinguish them.  
* **Instance profile** size affects **Spark UI** and **driver memory** – the exam often includes a scenario where a job fails due to OOM, and you must recommend moving the checkpoint to EFS (instead of S3) to improve I/O latency.  

---

### Exam Focus Areas  

- **Data Ingestion** – Recognise **Auto Loader** options (`cloudFiles`, `trigger`, `maxFilesPerTrigger`) and how to configure **checkpointing**.  
- **Delta Lake Transactions** – Ability to **read a specific version**, **restore a table**, and explain **vacuum** & **retention**.  
- **Structured Streaming** – Explain **exactly‑once** processing, watermarking, and **output modes** (`append`, `complete`).  
- **Schema Evolution & MERGE** – When to use `ALTER TABLE ... SET TBLPROPERTIES ('delta.enableChangeDataFeed' = true)` vs. a MERGE statement.  
- **Performance Tuning** – Diagnose a **skew join** with AQE, and recommend **photon** vs. **spark‑sql** for an aggregation.  
- **Governance** – Map **IAM actions** to **Lake Formation grants** for `CREATE TABLE`, `DESCRIBE`, and `SELECT`.  
- **AWS Integration** – Identify where a **S3 bucket policy** must grant **STS assume role** for Databricks, and how to enable **Glue Crawlers** without extra permissions