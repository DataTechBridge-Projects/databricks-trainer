## Course Introduction  

Welcome to the **AWS Databricks Data Engineer Certification** Udemy course.  
This section serves as a full‑fledged, “first‑lecture” style primer that a presenter can use to drive a 45‑ to 60‑minute live‑coding / storytelling session.  
You will learn not only *what* the exam expects you to know, but also *why* each concept matters in the broader AWS‑centric Lakehouse ecosystem.  
The material is deliberately dense and precise—think of a technical book chapter that you can skim for a quick refresher or read line‑by‑line while you deliver the lecture.  

---

### Overview  

* **Why Databricks on AWS?**  The Databricks Lakehouse blends the scalability of Apache Spark on Amazon EMR with the low‑latency, ACID‑guaranteed storage of Delta Lake.  On AWS you get a fully managed workspace that can be provisioned in a VPC, access any S3 bucket, and leverage native IAM for fine‑grained security—all without managing clusters.  The exam, therefore, tests whether a data engineer can *design* data pipelines that are both cloud‑native and performance‑aware.  

* **Lakehouse vs. Classic Architecture**  Classic “data‑warehouse‑plus‑Spark” stacks often involve ETL jobs that copy data from S3 → Redshift → BI, leading to eventual consistency and costly data movement.  The Lakehouse collapses those steps into a single write‑once, read‑many data format (Delta) that lives directly on S3 and can be served via Spark SQL, Python, or SQL tools.  The exam’s emphasis on *single source of truth* and *unified batch/streaming* stems from this shift.  

* **Exam Context**  The Databricks Certified Data Engineer Associate exam (AWS) is 90 minutes, 45 multiple‑choice questions, and is weighted across six domains.  The *Core Concepts* you will master here map directly to **Domain 1 – Architectural Design** and **Domain 2 – Engineering a Data Lakehouse Solution**.  The other exam domains (e.g., Monitoring, Governance) will be addressed later in the course.  

* **Target Learner Persona**  You already know Apache Spark concepts such as RDD transformations, DataFrames, and the Spark SQL optimizer, and you have hands‑on experience with AWS Glue crawlers, jobs, and IAM policies.  The missing piece for the exam is *how* those skills translate into the Lakehouse context, how to orchestrate jobs on Databricks, and which AWS services you must bind to in a secure, cost‑effective fashion.  

In the next subsection you’ll see the building blocks of that design, laid out in a systematic, exam‑aligned way.

---

### Core Concepts  

Below each concept is broken into sub‑sections that you can expand or shrink on‑the‑fly during a live presentation.  The order follows the natural learning progression: start with the overall model, then drill into the storage format, then into data ingestion, processing, and finally security/performance.  

#### 1. Databricks Lakehouse Architecture  

| Sub‑concept | Description |
|-------------|-------------|
| **Workspace** | A logical container for notebooks, jobs, and libraries.  In the exam you must know the difference between **Shared** and **Repos** workspaces, and how they map to AWS VPC & IAM. |
| **Cluster Types** | Standard, Job, and Service clusters.  Know the impact of **auto‑termination**, **node types**, and **cluster reuse** on cost and performance. |
| **Delta Lake** | A transaction log (Parquet + transaction files) that provides ACID transactions, schema enforcement, and time travel.  The exam often asks you to pick the correct **`OPTIMIZE`** or **`ZORDER`** strategy. |
| **Auto Loader** | The preferred way to ingest files from S3 in a streaming fashion.  Supports **event‑based**, **file‑system event**, and **cloudFiles** APIs.  Critical for “zero‑downtime” pipelines. |

#### 2. Delta Lake Fundamentals  

* **Write Paths** – `write.format("delta")`, `mode("overwrite")`, `mode("append")`, and the concept of **`MERGE`** for upserts.  
* **Data Versioning** – Every commit adds a new entry in `transaction/_delta_log/`.  Use **`SELECT * FROM table VERSION AS OF 10`** to retrieve historic snapshots.  
* **Compaction & Clustering** – `OPTIMIZE delta.` and `CONVERT TO DELTA` are key for exam questions that ask for **“improve query latency for a columnar scan.”**  

#### 3. Structured Streaming Integration  

* **Exactly‑Once Semantics** – Built on Delta Lake’s transaction log; the exam frequently asks which configuration (`spark.databricks.streaming.kafka.enableAutoCommit`) guarantees exactly‑once.  
* **Trigger Types** – `availableNow`, `continuous`, `once`, `processingTime`.  Knowing when to use each is the difference between “watermark‑driven” vs. “fixed‑batch” pipelines.  

#### 4. Job Orchestration & Parameterization  

* **Jobs API** – JSON payload for task definitions, `taskKey`, `maxRetries`, `retryDelay`.  The exam may present a YAML snippet and ask which field controls **`parallelism`**.  
* **Notebook‑to‑Job** – Use `%run` and `spark.conf.set` for parameter injection.  Know the difference between **`dbutils.widgets`** (Databricks‑only) and **`spark.read`** (pure Spark).  

#### 5. Security & Governance  

| Feature | AWS‑Specific Tie‑in | Exam Question Style |
|---------|--------------------|---------------------|
| **Cluster IAM Roles** | Each cluster can attach a *service‑linked* IAM role that allows access to S3, Glue, KMS, etc. | “Which IAM policy statement is required for a job that reads from `s3://my‑lakehouse/*`?” |
| **Table Access Controls (TAC)** | Uses Unity Catalog or Hive metastore; you must map **`GRANT SELECT`** to an AWS‑IAM user via **`aws_iam_role`** provider. | “What is the least‑privilege way to let a developer query `sales` table but not write?” |
| **Encryption** | Server‑side (SSE‑S3) vs. Customer‑managed (SSE‑KMS).  Delta Lake writes are encrypted automatically if the workspace’s **`kms`** is set. | “You need end‑to‑end encryption; which combination must you enable?” |

#### 6. Performance Tuning  

* **Caching / Persistence Levels** – `cache()`, `persist(StorageLevel.MEMORY_AND_DISK)` and the effect on driver memory.  
* **Spark Conf** – `spark.sql.shuffle.partitions`, `spark.databricks.io.cache.enabled`, and `spark.databricks.fileCache.enabled`.  These are typical exam “choose the best config” questions.  
* **Data Skipping** – `zorderBy` and `dataSkipping` on Delta; you’ll be asked to explain why clustering on a high‑cardinality partition column helps.  

---

### Architecture / How It Works  

Below is a simplified but exam‑relevant data‑flow that illustrates a typical end‑to‑end pipeline: raw CSV files land in S3, Auto Loader streams them into a bronze Delta table, an ELT job merges them into a silver fact table, and finally an analyst‑ready view is exposed via a Spark SQL query.  

```mermaid
flowchart TD
    subgraph S3 [Amazon S3]
        raw[Raw Landing Zone<br/>(s3://lakehouse/raw/)]
    end

    subgraph Databricks [Databricks Workspace]
        wl[Workspace: Bronze Notebook<br/>%run auto_loader]
        bronze[Delta Table: bronze_raw<br/>(s3://lakehouse/bronze/)]
        el[t ELT Notebook: Silver<br/>%sql/Delta merge]
        silver[Delta Table: silver_fact<br/>(s3://lakehouse/silver/)]
        query[SQL Analyst View<br/>%sql on silver_fact]
    end

    raw -->|CSV upload| wl
    wl -->|auto_load()| bronze
    bronze -->|MERGE| el
    el -->|writes| silver
    silver -->|SQL query| query

    style S3 fill:#E3F2FD,stroke:#607D8B,stroke-width:2px
    style Databricks fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px
```

**How it works, step‑by‑step:**  

1. **Landing** – Data producers drop CSV/JSON/Avro files into `s3://lakehouse/raw/`.  These are automatically detected by S3 event notifications (SNS → Lambda → IAM‑role).  
2. **Auto Loader** – The notebook `%run auto_loader` creates a streaming read (`spark.readStream.format("cloudFiles")`).  Files are *partitioned* by a `year=2024/month=09` folder structure, and each micro‑batch is appended to `bronze_raw`.  
3. **Bronze → Silver** – A batch job runs daily: it reads `bronze_raw`, applies a **`MERGE`** into `silver_fact` (the unified fact table).  The merge uses `watermark` to filter out stale data.  
4. **Analyst Consumption** – Business users run ad‑hoc SQL (`SELECT * FROM silver_fact WHERE event_date = CURRENT_DATE`) directly on the silver Delta table, leveraging **time travel** to see historical snapshots if needed.  

> **Exam tip:**  When the question asks “*Which component enables change‑data‑capture without custom code?*”, point to **Auto Loader + Delta Lake’s transaction log**.

---

### Hands-On: Key Operations  

The following code snippets are deliberately **self‑contained** and can be copy‑pasted into a Databricks notebook.  Each block is accompanied by a short comment that you can read aloud to illustrate the *why* behind the command.

#### 1. Mounting an S3 bucket with an IAM role  

```python
# 1️⃣ Attach an IAM role to the Databricks workspace (done in AWS console)
# 2️⃣ In the notebook, assume the role via an instance profile
dbutils.secrets.put(scope="project-scope", key="aws-iam-role", 
                    value="arn:aws:iam::123456789012:role/DatabricksLakehouseRole")

# Use dbutils.fs to list the bucket (demonstrates IAM propagation)
print(dbutils.fs.ls("s3://lakehouse-raw/"))
```

> **Explanation:** The `dbutils.secrets` call stores the IAM role ARN as a secret; the underlying EMR driver automatically assumes it, so you never hard‑code credentials.  This pattern satisfies the **least‑privilege** exam objective.  

#### 2. Reading a streaming dataset with Auto Loader  

```python
from pyspark.sql.functions import input_file_name

# Stream all CSV files arriving in the raw bucket
auto_load = (spark.readStream
                 .format("cloudFiles")
                 .option("cloudFiles.format", "csv")
                 .option("cloudFiles.schemaLocation", "/tmp/schema")
                 .load("s3://lakehouse/raw/")
                 .withColumn("source_path", input_file_name()))
# Trigger every 10 seconds (good for demo)
query = (auto_load.writeStream
                 .outputMode("append")
                 .format("delta")
                 .option("checkpointLocation", "/tmp/checkpoint")
                 .trigger(processingTime="10 seconds")
                 .start("s3://lakehouse/bronze/"))
```

> **Explanation:**  
* `cloudFiles.format = "csv"` tells Databricks to infer the schema lazily.  
* `checkpointLocation` ensures exactly‑once semantics by storing offsets in S3.  
* The `withColumn("source_path")` line is handy for downstream **metadata enrichment** (e.g., adding the originating prefix).  

#### 3. Merging incremental data (Bronze → Silver)  

```python
# Assume bronze_raw already exists
bronze_df = spark.read.format("delta").load("s3://lakehouse/bronze/")

# New incoming data (e.g., today's partition)
incremental_df = spark.read.format("delta").load("s3://lakehouse/bronze/2024/09=11/")

# Primary keys to use for upserts
merge_cond = "bronze.id = incremental.id"

spark.sql(f"""
    MERGE INTO s3://lakehouse/silver/fact  AS target
    USING increment_df  AS source
    ON {merge_cond}
    WHEN MATCHED THEN UPDATE SET *
    WHEN NOT MATCHED THEN INSERT *
""")
```

> **Explanation:** The `MERGE` statement is the recommended way to *upsert* rows into a Delta Lake table without duplicate primary keys.  It’s also *transactionally safe*: the entire merge runs as a single Spark task.  

#### 4. Setting a UMB (Unity Catalog) table for analyst access  

```sql
-- In a notebook using %sql, create a managed table
CREATE TABLE IF NOT EXISTS analytics.sales_fact
USING DELTA
LOCATION 's3://lakehouse/silver/fact/';

-- Grant SELECT to a role that maps to an AWS IAM group
GRANT SELECT ON TABLE analytics.sales_fact TO `analyst_group`;
```

> **Explanation:**  
* The `LOCATION` clause points to the underlying Delta folder; **Unity Catalog** then controls permissions, not the underlying S3 ACLs.  
* This is the **exam‑relevant** separation: *governance via UC, storage via S3*.  

#### 5. Enabling Adaptive Query Execution (AQE) for a streaming job  

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
# Reduce the number of shuffle partitions dynamically based on data size
spark.conf.set("spark.sql.shuffle.partitions", "200")
```

> **Explanation:** AQE can shrink or expand shuffle partitions at runtime, eliminating *skew* in streaming aggregations.  The exam often asks which configuration **reduces the risk of “Task serialization time too high”**.  

---

### AWS‑Specific Considerations  

| AWS Service | Lakehouse Interaction | Practical Tips for the Exam |
|-------------|-----------------------|-----------------------------|
| **Amazon S3** | Primary data lake storage.  Use *S3 Inventory* for periodic cataloging, *S3 Event Notifications* for Auto Loader triggers, and *S3 Object Lock* for immutable audit logs. | **Key point:** S3 *event‑driven* ingestion must reference the *same* IAM role that Databricks uses; mismatch → “AccessDeniedException”. |
| **AWS Glue Catalog** | Acts as the Hive metastore for Databricks.  You can register Delta tables as **Glue Tables** for cross‑workspace access.  Enable *Glue DataBrew* for data profiling in the bronze layer. | **Exam tip:** When a table appears in the *Glue Data Catalog* but not in *Unity Catalog*, you must **register it with UC** to get TAC. |
| **IAM & Service‑Linked Roles** | Databricks clusters require a **cluster‑profile** IAM role that allows S3 read/write, CloudWatch logs, and Glue calls.  Use *Instance Profiles* for EMR or *Instance Role* for Databricks Managed Workflows. | **Focus:** The *policy condition* `aws:SourceArn` must match the S3 bucket ARN for least‑privilege. |
| **AWS Lake Formation** | Optional: Use Lake Formation to