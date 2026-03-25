# Exam Overview and Strategy  
**Section 2 of 15 – AWS Databricks Data Engineer Certification**  

> **Goal of this section:** Give you a panoramic view of the Databricks Certified Data Engineer – Associate (AWS) exam, tie together the core technical concepts with the AWS ecosystem, and arm you with concrete “do‑it‑yourself” snippets you can run today. By the end of the 45‑60 min walkthrough you should be able to answer *why* each topic matters, *what* the exam is looking for, and *how* to demonstrate the skill in a live notebook.

---  

## Overview  

The Databricks Data Engineer Associate (AWS) exam validates that you can **design, build, and operate** data pipelines that ingest, transform, store, and surface data using **Databricks Runtime for Apache Spark** on **AWS**. The exam is intentionally cross‑cloud (it also lists GCP/Azure objectives) but the *associate* level on AWS expects you to be fluent in the *AWS‑specific integration points* that you’ll encounter daily: S3, IAM, Glue, EMR, and Lake Formation.  

The exam is **60 minutes**, **45–55 questions** (multiple‑choice, multiple‑select, and **scenario‑based** items). The passing score is **70 %**. The exam is divided into four **domains** (each 20‑25 % of the total):  

| Domain | What you’ll do | Typical question style |
|--------|----------------|------------------------|
| **Data Ingestion & Processing** | Use Structured Streaming, Auto Loader, and Spark‑SQL to pull data from S3, change schemas, and apply business logic. | “Which loader option best handles nested JSON with schema evolution?” |
| **Data Storage & Optimization** | Choose the right file format, partition strategy, and Delta Lake features (e.g., Z‑order, vacuum, compaction). | “How would you improve query latency for a 2‑TB fact table that is frequently filtered on `event_date`?” |
| **Data Governance & Security** | Apply IAM roles, S3 bucket policies, Lake Formation permissions, and manage data lifecycle. | “Which IAM policy combination permits a notebook to read from `s3://my-bucket/raw/` but not write?” |
| **Monitoring, Debugging & Cost‑Efficiency** | Set up job clusters, use Spark UI / CloudWatch, read logs, and interpret Spark UI metrics. | “You see a Spark UI stage with 30 % of tasks timed‑out. Which cluster configuration is most likely the root cause?” |

> **Strategic take‑away:** The exam never asks you to write production‑grade Terraform scripts or to recall the exact default values of every Spark conf key. It **tests reasoning** – *“Given X, why would you choose Y?”* – and expects you to map the answer to an AWS service you already know.  

---

## Core Concepts  

Below is a concise, but **exhaustive**, map of the concepts the exam focuses on. Treat each bullet as a *mini‑lecture*; you should be able to explain it in < 2 minutes.

### 1. Spark Core & APIs  

* **DataFrames & Datasets** – The *immutable* logical plan, Catalyst optimizer, Tungsten execution.  
* **Structured Streaming** – Micro‑batch vs. continuous mode; watermarking; exactly‑once guarantees.  
* **Spark SQL & Catalyst** – Use `spark.sql` for ad‑hoc analytics; understand *predicate push‑down* and *join reordering*.  

### 2. Delta Lake  

| Feature | Why it matters for the exam |
|---------|-----------------------------|
| **Transactional guarantees** | Guarantees atomic commits when writing streaming data. |
| **Schema enforcement & evolution** | Avoids “illegal data” errors in production pipelines. |
| **Z‑ordering & data skipping** | Directly influences query latency and cost. |
| **VACUUM & COMPACTION** | Controls storage bloat; required to answer “when should you run VACUUM?”. |
| **Change Data Feed (CDF)** | Enables incremental downstream pipelines – a frequent scenario in exam questions. |

### 3. Auto Loader (Cloud‑Optimized Ingestion)  

* **Event‑by‑event processing** – Detects new objects in S3 and triggers a micro‑batch.  
* **Trigger options** – `once`, `availableNow`, `continuous`.  
* **Schema inference strategies** – `inferSchema`, `mergeSchema`, `ignoreChanges`.  
* **Checkpointing** – Guarantees exactly‑once by storing progress in a separate S3 prefix.  

### 4. Partitioning & Bucketing  

* **Static partitioning** – Deterministic split on columns (`event_date`, `country`).  
* **Dynamic partition pruning** – Leveraged automatically by Spark 3.2+ when you filter on partition columns.  
* **Bucketed tables** – When combined with Z‑order, can reduce file scan for high‑cardinality columns.  

### 5. Cluster & Resource Management  

| Concept | AWS‑specific knobs |
|---------|--------------------|
| **Cluster types** – All‑purpose vs. Job clusters | Job clusters are **ephemeral**, automatically terminated on job success/failure. |
| **Instance pools** – Re‑use pre‑warmed EC2 instances | Reduces startup latency and cost (especially for short‑lived jobs). |
| **Autoscaling policies** – `maxWorkers`, `minWorkers`, `autoscale` | Must stay within the VPC’s subnet and IAM instance profile limits. |
| **Spot vs. On‑Demand** – Cost‑efficiency | Spot is allowed for `pool` but you must handle possible pre‑emptions. |
| **Spark configuration overrides** – `spark.databricks.delta.retentionDurationCheck.enabled` | Disable to avoid unnecessary retention checks in a CI pipeline. |

### 6. Governance – Lake Formation & Glue Catalog  

* **Glue Data Catalog** – Shared metastore; `Table` objects map to Delta tables.  
* **Lake Formation permissions** – `GRANT SELECT`, `DENY INSERT` on databases/tables.  
* **Column‑level security** – Often asked: “Which security method allows you to hide `ssn` column from a downstream analyst?” – answer: Lake Formation column‑masking.  

### 7. Monitoring & Cost  

* **Spark UI metrics** – `stages`, `tasks`, `executor metrics`, `stage duration`.  
* **Databricks job run IDs** – Used for CloudWatch Logs subscription filters.  
* **Cost‑per‑task** – Understanding that a single large job can be cheaper than many small jobs (due to startup overhead).  

---

## Architecture / How It Works  

Below is a **single‑pane data pipeline** that you will see on many exam questions. The diagram captures the **end‑to‑end flow** from raw data landing in S3 to an optimized Delta Lake table ready for analytics.  

```mermaid
graph LR
    subgraph S3 Raw Layer
        S3_RAW[ s3://my-bucket/raw/ ]:::s3
    end

    subgraph AutoLoader
        AL[ Auto Loader (Structured Streaming) ]:::loader
    end

    subgraph DeltaLake
        DL[ Delta Lake (s3://my-bucket/curated/) ]:::delta
    end

    subgraph Serving
        BI[ Databricks SQL Dashboard / BI Tool ]:::serving
    end

    classDef s3 fill:#F7D060,stroke:#333,stroke-width:2px;
    classDef loader fill:#6BBF59,stroke:#333,stroke-width:2px;
    classDef delta fill:#5A9BD4,stroke:#333,stroke-width:2px;
    classDef serving fill:#F2911F,stroke:#333,stroke-width:2px;

    S3_RAW -->|s3:ObjectCreated:*| AL
    AL -->|writes with checkpoint| DL
    DL -->|registered in Glue Catalog| BI
```

**Explanation (talk through each arrow):**  

1. **Raw S3 bucket** receives CSV/JSON/Avro files from upstream producers.  
2. **Auto Loader** is configured with the `cloudFiles` reader format; it continuously polls S3 (or uses S3 Event Notifications) and materializes **new files** into a **micro‑batch** DataFrame.  
3. The **Delta Lake** table is the *single source of truth* – it receives writes with **schema evolution** enabled and **optimize‑+‑ZORDER** scheduled later (via a separate job).  
4. **Glue Data Catalog** is automatically synced when you use `df.write.format("delta").saveAsTable("curated.events")`.  
5. Downstream **BI tools** (e.g., Tableau, PowerBI) connect via **Databricks SQL endpoint** and query the curated table with **predicate push‑down** and **file skipping**.  

*Key take‑away for the exam:* **Every stage has a “canonical AWS service”** (S3, Glue, Lake Formation, CloudWatch). The exam will ask you to **identify the bottleneck** (e.g., “Why are we scanning 1 TB of CSV files when a Delta table would have scanned only 50 GB?”).  

---

## Hands-On: Key Operations  

> **Goal:** Provide a **copy‑pasteable notebook** that you can run in a Databricks workspace on AWS. Each cell is annotated with *why* it matters for the exam.  

### 1️⃣ Auto Loader – Incremental CSV Ingestion  

```python
# 1. Define the S3 source and checkpoint location
raw_path = "s3://my-bucket/raw/events/"
checkpoint_path = "s3://my-bucket/checkpoints/events/"

# 2. Stream the data – note the use of cloudFiles and the schema merge
df_stream = (
    spark.readStream
         .format("cloudFiles")
         .option("cloudFiles.format", "csv")
         .option("cloudFiles.schemaInference", "merge")   # schema evolution
         .option("cloudFiles.schemaEvolutionMode", "addNewColumns")  # tolerant
         .option("inferSchema", "true")
         .load(raw_path)
)

# 3. Basic transformation – add a processing column
from pyspark.sql.functions import col, from_json, schema_of_json, lit
import json

# Assume each CSV row has a JSON string in column `payload`
json_schema = schema_of_json(col("payload"))
df_enriched = df_stream.select(
    col("event_id"),
    from_json(col("payload").cast("string"), json_schema).alias("payload_json")
).select(
    "event_id",
    col("payload_json.*").alias("payload")  # flatten
).withColumn("ingest_ts", lit(current_timestamp()))

# 4. Write to Delta with checkpoint
(
    df_enriched
      .writeStream
      .format("delta")
      .outputMode("append")
      .option("checkpointLocation", checkpoint_path)
      .option("mergeSchema", "true")
      .trigger(availableNow=True)   # For demo; in prod use default micro‑batch
      .start("s3://my-bucket/curated/events/")
)
```

**Why this matters:**  

* `cloudFiles` abstracts the S3 `ListObjectsV2` call and handles **partial reads** – a frequent exam topic.  
* `schemaInference` + `mergeSchema` demonstrates **schema evolution** (the candidate must know when to use each).  
* The checkpoint location must be on **S3**, not DBFS, because the exam expects you to consider *persistence across driver failures*.  

### 2️⃣ Optimizing Writes – Z‑Ordering & Data Skipping  

```python
# Optimize a large fact table (approx. 200M rows)
delta_path = "s3://my-bucket/curated/events/"

spark.sql(f"""
    OPTIMIZE delta.`{delta_path}`
    WHERE ingest_ts >= date_sub(current_date(), 7)   -- keep recent 7 days
    ZORDER BY (event_timestamp)
""")
```

**Why this matters:**  

* The `OPTIMIZE … ZORDER BY` command is **high‑value** in the exam – you’ll see questions asking which **Delta feature** reduces file count for a given filter.  
* The `WHERE` clause limits the operation to recent data, avoiding a costly full‑table rewrite.  

### 3️⃣ Querying with Predicate Push‑Down (SQL)  

```sql
-- Query to understand why file skipping works
SELECT
    event_id,
    event_timestamp,
    payload['device_id'] as device_id,
    payload['event_type'] as event_type
FROM curated.events
WHERE event_timestamp >= TIMESTAMP '2024-09-01'
  AND device_id = 'camera_front'
;
```

*When you run the query, inspect the **Spark UI → SQL → File Source** tab. You’ll see that only 3 out of 12 data files are read – a concrete illustration of **data skipping**.*

### 4️⃣ Managing a Job Cluster via Databricks Jobs API (Python)  

```python
import json, requests, os
from urllib.parse import urljoin

DATABRICKS_TOKEN = dbutils.secrets.get(scope="databricks", key="token")
HOST = dbutils.secrets.get(scope="databricks", key="host")

def create_job(name, cluster_spec, notebook_path):
    url = f"{HOST}/api/2.1/jobs/create"
    payload = {
        "name": name,
        "new_cluster": cluster_spec,
        "notebooks": [{"path": notebook_path}],
        "max_retries": 1,
        "timeout_seconds": 3600
    }
    r = requests.post(url, headers={"Authorization": f"Bearer {DATABRICKS_TOKEN}"}, json=payload)
    return r.json()

cluster_spec = {
    "spark_version": "13.3.x-scala2.12",
    "node_type_id": "m5.xlarge",
    "num_workers": 2,
    "autoscale": {"min_workers": 2, "max_workers": 10},
    "aws_attributes": {"instance_profile": {"profile_name": "databricks-ec2-role"}},
    "aws_ganglia": {"enabled": True},
    "automatic_restart": {"cluster_restart": "TERMINATED_DUE_TO_LOSS_OF_HEARTBEAT"}
}
job_id = create_job("Optimize-Events", cluster_spec, "/Shared/Optimize_Events").get("job_id")
print("Created job id:", job_id)
```

**Why this matters:**  

* Many exam items present a **scenario** (“Your nightly ETL fails because the cluster is terminated when a node is pre‑empted”). The correct answer is *“use a job cluster with a Spot‑instance policy in an instance pool.”* The snippet shows how you would **programmatically provision** that job cluster – a skill the exam expects you to recognise.  

---

## AWS‑Specific Considerations  

| AWS Service | How it connects to Databricks (key exam points) | Common Pitfalls |
|-------------|---------------------------------------------------|-----------------|
| **S3** | *Source* (`s3://` paths), *checkpoint* store, *output* for Delta tables. Use **SSE‑S3** or **SSE‑KMS** for data at rest; ensure **IAM policy** on the Databricks instance profile allows `s3:GetObject` and `s3:PutObject` on the target prefixes. | Forgetting the **S3 Event Notification** to trigger Auto Loader → stale data; not enabling **S3 Block