# Spark on Databricks  *(Section 5 of 15 – AWS Databricks Data Engineer Certification)*  

> **Goal of this section** – To give you a mental model of *how Spark runs on Databricks in AWS*, the essential components you must master for the **Databricks Certified Data Engineer Associate** exam, and a set of hands‑on exercises you can run in a few minutes.  

---  

## Overview  

Apache Spark is a unified analytics engine for large‑scale data processing. In the context of AWS, Databricks is the *managed, collaborative, and secure* platform that runs Spark on top of the native AWS services (S3, IAM, Glue, Lake Formation, CloudWatch, etc.).  

1. **Databricks as a “Spark‑as‑a‑service”** – When you launch a Databricks cluster, the control plane (the *Databricks service* hosted in the Databricks-managed AWS account) provisions an **EC2 instance pool** that assumes an **IAM role** (the *instance profile*). Each worker node receives that role, which grants it fine‑grained permissions to read/write S3, query the Glue Data Catalog, and invoke other AWS services.  

2. **Collaboration & notebooks** – Notebooks are not just REPLs; they are *first‑class data assets* that can be versioned, scheduled, and executed as jobs. They support mixed‑language (`%python`, `%sql`, `%scala`, `%r`) and automatically register *temporary views* that can be consumed across cells.  

3. **Delta Lake as the default storage layer** – Databricks encourages the use of Delta Lake (an open‑source storage format built on Apache Parquet that adds ACID transactions, time‑travel, and schema enforcement). All writes from notebooks, jobs, or streaming pipelines should be to Delta tables that live in **S3** and are governed by **Unity Catalog** (Databricks’ unified data‑governance layer).  

4. **Serverless vs. provisioned clusters** – In AWS you can run **standard clusters** (you manage the EC2 instance types) or **serverless SQL/Compute** (Databricks fully manages the infrastructure, you only specify the number of DBUs and the runtime version). For the associate exam you must know the trade‑offs: cost, startup latency, and security implications (instance‑profile vs. service‑principal).  

5. **Streaming & Auto Loader** – Databricks’ *Auto Loader* (cloud‑native file ingestion) automatically detects new files in an S3 prefix, handles schema evolution, and writes them into a Delta table in *append* or *merge* mode. It abstracts away the complexity of checkpoint directories and back‑pressure handling.  

By the end of this section you should be able to:  

- Explain where Spark’s **driver** and **executors** live on a Databricks cluster and how they interact with S3, Glue, and Unity Catalog.  
- Differentiate between **interactive notebooks**, **jobs**, and **serverless compute**.  
- Show how to *securely* load data from an S3 bucket using an IAM role and *write* it to a Delta Lake table protected by Unity Catalog.  
- Anticipate the *exam‑focused* questions that test your ability to design, monitor, and troubleshoot Spark workloads on Databricks.  



---  

## Core Concepts  

Below is a concise, exam‑ready taxonomy of the Spark concepts you’ll need to master on Databricks. Each sub‑section contains enough depth for a 5‑minute mini‑lecture.

### 1. Cluster Architecture  

| Component | Databricks representation | AWS equivalent | Typical size for an associate exam |
|-----------|---------------------------|----------------|-------------------------------------|
| **Control Plane** | Managed service in the Databricks AWS account | – (no direct access) | Understand that you never manage the control plane. |
| **Driver Node** | Runs the Spark driver, UI, and notebook cells | EC2 instance (single‑core) | 1 driver per job; use `spark.databricks.delta.retentionDurationCheck.enabled` false for test. |
| **Worker Nodes (Executors)** | Pools of EC2 instances (autoscaling groups) | EC2 Spot/On‑Demand | 2–4 executors per task; choose `i3.xlarge` for 4 vCPU/16 GiB. |
| **Cluster‑Init Scripts** | `init.sh` runs on each node before Spark starts | User‑data for EC2 | Use to install custom libs (e.g., `pip install pyspark==3.5.0`). |
| **Spark UI** | Embedded in notebooks & job pages (via HTTPS) | – | Can be accessed via `https://<databricks-instance>/`. |
| **Security** | Instance profile → IAM Role (e.g., `Databricks-ExecutionRole`) | S3 bucket policies, KMS CMK, Lake Formation | Must allow `s3:GetObject`, `s3:PutObject`, `glue:*`. |

**Key Points**  

- **Autoscaling**: Databricks uses *elastic scaling* – it can spin up new workers in < 30 seconds. For exam scenarios, be able to read a table that shows “target size = 2 workers, min = 1, max = 5”.  
- **Task Scheduling**: Spark on Databricks runs *dynamic allocation*; tasks are scheduled on workers based on stage DAGs.  

### 2. Databricks Runtime (DBR)  

- DBR is a **custom Spark distribution** that ships with:  
  - Optimized **Apache Spark** binaries (YARN is not used; instead, Databricks uses its own *cluster manager*).  
  - **Photon** (vectorized query engine) – optional but recommended for SQL workloads.  
  - **Koalas** (pandas‑like API for Spark DataFrames) – pre‑installed for rapid prototyping.  

| Feature | Recommended DBR version for 2025 exams | Reason |
|---------|-------------------------------------------|--------|
| **Spark 3.5** | `12.2.x` (or later) | Includes `spark.sql.adaptive.enabled=true`. |
| **Delta Lake 2.4** | Pre‑installed in DBR 12.x | Guarantees compatibility with `MERGE` semantics. |
| **Photon** | `photon.enabled=true` | Improves SQL latency by up to 3×. |
| **Cluster Libraries** | Use *wheel* or *pypi* – avoid `conda` for exam speed. |

### 3. Delta Lake Fundamentals  

| Concept | Databricks API | Typical Syntax |
|---------|----------------|----------------|
| **Write** | `DataFrame.write.format("delta").mode("overwrite")` | `df.write.format("delta").mode("overwrite").saveAsTable("silver.sales")` |
| **Read** | `DeltaTable.forName(spark, "gold.sales")` | `spark.table("silver.sales")` |
| **ACID** | Atomic commit via the transaction log (`_delta_log/`) | Enforced automatically – no extra config needed. |
| **Time‑Travel** | `SELECT * FROM gold.sales VERSION AS OF 3` | Requires `spark.databricks.delta.retentionDurationCheck.enabled=false` for older versions. |
| **Schema Evolution** | `spark.databricks.delta.schema.autoMerge.enabled=true` | Useful when adding columns from streaming source. |

### 4. Auto Loader & Structured Streaming  

- **Auto Loader** is a *high‑throughput ingestion* method for S3, ADLS, and GCS. It works by using a **checkpoint directory** that tracks the *event log* on S3 (via S3 *list‑objects* operations).  

**Supported formats**: CSV, JSON, Parquet, Avro, ORC, XML.  

**Load patterns**  

| Mode | Description | Example |
|------|-------------|---------|
| `cloudFiles("s3://bucket/raw", "json")` | Incrementally read new files | `df = spark.readStream.format("cloudFiles").option("cloudFiles.format", "json").load("s3://raw-data/events/")` |
| `trigger(availableNow=True)` | One‑off batch mode – used for back‑fills | `df.writeStream.trigger(once).start()` |
| `mergeSchema` (auto) | Handles schema drift | `df = spark.readStream.format("cloudFiles").option("mergeSchema", "true")` |

### 5. Unity Catalog (Fine‑Grained Governance)  

- **Catalogs → Schemas → Tables** – A three‑level hierarchy.  
- **Grant Model** – Permissions are *inherited*; e.g., `GRANT SELECT ON SCHEMA marketing TO `data_engineer_jane``.  

**Exam focus**: you’ll be asked to *identify the correct grant statement* for a given scenario (e.g., “Allow `analyst` to read tables in `silver` but not write”).  

### 6. Serverless SQL vs. Dedicated Compute  

| Metric | Serverless SQL | Dedicated (Standard) Cluster |
|--------|----------------|------------------------------|
| **Startup latency** | < 5 seconds (warm) | 1–2 minutes (cold start) |
| **Cost model** | DBU (Data Processing Units) billed per second | EC2 + DBU + storage |
| **Security** | Uses *service principal* (no instance profile) – easier for Lake Formation | Relies on instance profile – more granular IAM policy needed |
| **When to use** | Ad‑hoc queries, BI dashboards | Heavy ETL jobs, ML training, custom libraries |

> **Exam tip** – The exam often gives you a scenario with a *high‑concurrency, low‑latency* requirement and asks you whether to enable *Serverless* or *Cluster*; remember: **Serverless is limited to 10 k concurrent queries, no custom libs, and you can’t attach a notebook directly**.  



---  

## Architecture / How It Works  

Below is a **serverless‑style architecture** that illustrates a typical end‑to‑end Spark on Databricks pipeline in AWS. The diagram uses **Mermaid** (supported in Databricks notebooks) and an ASCII fallback.

```mermaid
graph TD
    subgraph AWS_Ecosystem
        S3_Raw[S3 Bucket<br/>(Raw Landing Zone)]
        S3_Staging[S3 Bucket<br/>(Staging / Bronze)]
        S3_Refined[S3 Bucket<br/>(Silver / Gold)]
        Glue_Catalog[Glue Data Catalog<br/>(Metastore)]
        Lake_Formation[Lake Formation<br/>Permissions]
    end

    subgraph Databricks_Environment
        Cluster[Databricks Cluster<br/>(Standard / Serverless)]
        Notebook[Notebook / Job]
        Stream[Auto Loader (Streaming Query)]
        DeltaTable[Delta Table<br/>(Silver/Gold)]
    end

    %% Data Flow
    S3_Raw -->|S3 Event| Stream
    Stream -->|Auto Loader| DeltaTable
    DeltaTable -->|Spark SQL| Notebook
    Notebook -->|Write| S3_Staging
    Notebook -->|Write| S3_Refined
    Glue_Catalog -.->|Metadata| DeltaTable
    DeltaTable -->|Grant| Lake_Formation

    %% Interaction
    Notebook -->|Query| Cluster
    Cluster -->|Execute Spark| S3_Refined
```

**ASCII fallback** (copy‑paste into a plain‑text slide)

```
+----------------------+      +-----------------------+      +----------------------+
|  Raw S3 Bucket (Bronze)  | --> |  Auto Loader (Stream) | --> |  Delta Lake (Silver) |
+----------------------+      +-----------------------+      +----------------------+
                                         |                               |
                                         v                               v
                                 +----------------------+      +-------------------+
                                 |  Databricks Cluster |      |  Unity Catalog   |
                                 +----------------------+      +-------------------+
                                           |                              |
                                           v                              v
                                 +----------------------+      +-------------------+
                                 |  Notebook / Job      |      |  S3 (Gold)        |
                                 +----------------------+      +-------------------+

All I/O between Spark executors and S3 is performed via the
IAM role attached to the cluster (Databricks‑ExecutionRole).
```

**How the pieces interact (exam‑ready narrative):**  

1. **Landing** – A data‑producer (e.g., AWS IoT) writes JSON files to `s3://bronze/events/`.  
2. **Auto Loader** – A notebook in `bronze_to_silver` launches a streaming query:  

   ```python
   bronze_df = spark.readStream.format("cloudFiles") \
       .option("cloudFiles.format", "json") \
       .option("cloudFiles.schemaLocation", "/dbfs/tmp/schema") \
       .load("s3://bronze/events/")
   silver_df = bronze_df.selectExpr("CAST(id AS STRING)",
                                   "CAST(event_ts AS TIMESTAMP)",
                                   "CAST(payload AS STRING)")
   (silver_df.writeStream
        .format("delta")
        .option("checkpointLocation", "s3://lake/checkpoints/bronze_to_silver")
        .outputMode("append")
        .start("s3://silver/events/"))
   ```

3. **Delta Table Registration** – Using the notebook UI, the writer executes:  

   ```sql
   CREATE TABLE IF NOT EXISTS silver.events
   USING DELTA
   LOCATION 's3://silver/events/'
   ```

   This registers the Delta table in the **Unity Catalog** (`silver.events`).  

4. **Fine‑Grained Access** – An admin grants `SELECT` to the `analyst` role:  

   ```sql
   GRANT SELECT ON TABLE silver.events TO `analyst`;
   ```

5. **Consumption** – A downstream BI tool (e.g., Amazon QuickSight) connects via the *Databricks SQL* endpoint and runs:  

   ```sql
   SELECT event_type, COUNT(*) AS cnt
   FROM silver.events
   WHERE event_ts >= current_date - 1
   GROUP BY event_type;
   ```

Every step is **idempotent** and **transactionally safe** because the write path uses Delta Lake’s transaction log. The driver tracks the latest *committed* batch and the executors process only new files, guaranteeing exactly‑once semantics.  



---  

## Hands-On: Key Operations  

Below is a **step‑by‑step notebook** that covers the most common exam tasks. Each block includes a short comment that you can read aloud while coding. Feel free to copy the cells into your own Databricks workspace.

> **Prerequisite** – The cluster you attach to this notebook must have the **Databricks‑ExecutionRole** with the following policy (simplified for the exam):  

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": [
        "arn:aws:s3:::analytics-bronze/*",
        "arn:aws:s3:::analytics-silver/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "glue:*"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:PutMetricData"
      ],
      "Resource": "*"
    }
  ]
}
```

---

### 1️⃣ Create a Managed Table from a CSV Landing Zone  

```python
# 1️⃣ Define input & output locations
bronze_path = "s3://analytics-bronze/customers/"
silver_path = "s3://analytics-silver/customers/"

# 2️⃣ Read the CSV (use schema inference for demo)
customers = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(bronze_path)

# 3️⃣ Show a few rows (helps you