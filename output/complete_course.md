# AWS Databricks Data Engineer Certification
### A Comprehensive Udemy Course Guide

**Generated:** 2026-03-24  
**Target Audience:** data engineers familiar with Apache Spark and AWS Glue who want to prepare for the Databricks Certified Data Engineer Associate exam on AWS  
**Total Sections:** 15

---

## AWS Databricks Data Engineer Certification Prep  

**Welcome!** Whether you’re a Spark‑savvy engineer who already builds ETL jobs in AWS Glue or a data‑pipeline builder eager to turn that experience into a vendor‑validated credential, this course will take you from “I’ve used Databricks” to “I can pass the **Databricks Certified Data Engineer Associate (AWS)** with confidence.  

### What you’ll master  

| Domain | Key skills you’ll acquire |
|--------|----------------------------|
| **Exam fundamentals** | Exam structure, domain weighting, the exact language of the test‑maker. |
| **AWS‑to‑Databricks integration** | VPC, IAM, S3 bucket policies, and RDS/Redshift networking so you can launch a production‑grade workspace in minutes. |
| **Spark on Databricks** | Runtime tuning, auto‑scoping, JIT compilation, and the Cluster Autoscaler for cost‑effective scaling. |
| **Delta Lake fundamentals** | Schema evolution, time‑travel, ACID guarantees, and the Delta Engine. |
| **Lakehouse design** | Unified, versioned data stores that combine warehouse reliability with lake scalability. |
| **Ingestion & streaming** | Auto Loader, Structured Streaming, change‑data‑capture patterns, and secure delta writes. |
| **ETL pipelines** | Databricks Jobs, Delta Live Tables, idempotent pipelines, and reusable notebooks. |
| **Governance** | Unity Catalog, row‑level security, data lineage, and audit‑ready metadata. |
| **Orchestration** | Native Workflows, Airflow integration, and dependency‑aware task graphs. |
| **Performance engineering** | Query plan analysis, partition pruning, caching, the Profiler, and cost‑aware tuning. |
| **Advanced optimisation** | Z‑order, data skipping, `OPTIMIZE`, and column‑pruning for sub‑second latency on TB‑scale tables. |
| **Testing, debugging & monitoring** | Unit & integration tests, Spark UI, Repos for CI/CD, alerts, and dashboards. |
| **Capstone project** | Build an end‑to‑end, exam‑style solution, then walk through a mock exam under real‑time constraints. |

### Prerequisites assumed  

- **Hands‑on Spark** – You can author DataFrames, Spark SQL, and basic RDD transformations.  
- **AWS fundamentals** – S3, IAM, VPC, and Glue Data Catalog.  
- **Linux/Docker basics** – A single terminal session and a Docker‑ready host.  

### How to use this material  

1. **Follow the linear roadmap** – Each chapter builds on the previous one, mirroring a real Lakehouse lifecycle.  
2. **Practice, then practice again** – Every section ends with a hands‑on lab and a set of “exam‑style” multiple‑choice questions. Finish the lab before you answer the questions.  
3. **Version‑control your notebooks** – All notebooks live in a Git‑backed repo. Clone, commit, and push as if you were working on a production team; this reinforces the CI/CD mindset the exam rewards.  
4. **Mock‑exam sprint** – The final chapter replicates the 90‑minute, 45‑question format. Time yourself, review the scoring feedback, and repeat until you hit a 90 %+ confidence score.  

### Brief exam overview  

The **Databricks Certified Data Engineer Associate (AWS)** is a 90‑minute, 45‑question, multiple‑choice test. It is divided into six domains:

| Domain | % of exam | Focus |
|--------|-----------|-------|
| **Fundamentals** | 15 % | Spark architecture, Databricks runtime, security basics |
| **Ingestion & Storage** | 25 % | S3 ↔️ Delta Lake, streaming, change data capture |
| **ETL & Data Pipelines** | 25 % | Jobs, Delta Live Tables, orchestrator‑aware pipelines |
| **Governance** | 15 % | Unity Catalog, row‑level security, data lineage |
| **Performance** | 15 % | Query optimisation, caching, cost‑aware tuning |
| **Operational Monitoring** | 5 % | Logging, alerting, debugging tools |

Questions blend scenario‑based MCQs with “select‑all‑that‑apply.” The scoring algorithm penalises blind guessing, so you need genuine confidence in each answer.  

Our course mirrors this layout: each domain has a dedicated lab, a bank of practice questions, and a timed mock that uses the exact question‑style and time limits you’ll face on exam day.  

---

By the end of this journey you will **design, build, and operate** a production‑grade Lakehouse on AWS, **debug** issues quickly, and **pass** the Databricks Certified Data Engineer Associate exam with confidence.  

**Ready? Let’s unlock the Lakehouse together.**  



---  

*Sections covered in this course:* Course Introduction → Exam Overview & Strategy → AWS Setup → Databricks Platform → Spark on Databricks → Delta Lake Core Concepts → Lakehouse Architecture → Data Ingestion with Auto Loader → Data Transformation & ETL Pipelines → Unity Catalog & Governance → Workflows & Orchestration → Performance Tuning → Advanced Delta Optimization → Testing, Debugging, & Monitoring → Capstone & Exam Readiness.  



---

---

## Table of Contents

1. [Course Introduction](#course-introduction)
2. [Exam Overview and Strategy](#exam-overview-and-strategy)
3. [AWS Setup](#aws-setup)
4. [Databricks Platform](#databricks-platform)
5. [Spark on Databricks](#spark-on-databricks)
6. [Delta Lake Core Concepts](#delta-lake-core-concepts)
7. [Lakehouse Architecture](#lakehouse-architecture)
8. [Data Ingestion with Auto Loader](#data-ingestion-with-auto-loader)
9. [Data Transformation and ETL Pipelines](#data-transformation-and-etl-pipelines)
10. [Unity Catalog & Governance](#unity-catalog-governance)
11. [Workflows and Orchestration](#workflows-and-orchestration)
12. [Performance Tuning](#performance-tuning)
13. [Advanced Delta Optimization](#advanced-delta-optimization)
14. [Testing, Debugging, and Monitoring](#testing-debugging-and-monitoring)
15. [Capstone and Exam Readiness](#capstone-and-exam-readiness)

---

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

---

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

---

# **AWS Setup**  
*Section 3 of 15 – AWS Databricks Data Engineer Certification*  

---

## Overview  

The **AWS Setup** section is the foundation for everything you will do with Databricks on Amazon Web Services. While you may already know Apache Spark and AWS Glue, the Databricks‑on‑AWS experience is a tightly‑integrated, cloud‑native platform that blurs the line between “data engineering” and “data platform”. In this chapter we de‑construct the **resource model**, **networking**, **security**, and **runtime lifecycle** that make a Databricks workspace on AWS feel like an extension of your existing AWS data estate rather than a foreign black box.  

You will explore why **S3 is the single source of truth for raw data**, how **IAM roles** act as the security perimeter for notebooks, clusters, and jobs, and why **Unity Catalog** (or the older **metastore**) is the glue that binds Lake Formation permissions, Glue crawlers, and EMR clusters together. Concepts such as **Auto Loader**, **Delta Live Tables (DLT)**, **cluster autoscaling**, **job orchestration**, and **observability** are examined in the context of the AWS services you already manage—particularly **S3, IAM, Glue, EMR, Lake Formation, CloudWatch**, and **EventBridge**.  

By the end of this section you should be able to:  

1. **Articulate** how a Databricks workspace on AWS maps to an AWS account, VPC, and IAM configuration.  
2. **Design** a minimal yet production‑grade architecture that separates raw, curated, and analytic data layers while leveraging Delta Lake for ACID guarantees.  
3. **Explain** the role of each core concept (catalogs, schemas, tables, clusters, jobs, etc.) and how they map to AWS primitives.  
4. **Execute** a set of hands‑on notebooks that create a full data pipeline from S3 → Auto Loader → Delta Lake → DLT → downstream analytics.  

The material is intentionally **dense**; a presenter can comfortably cover the entire section in a 45‑minute deep‑dive, interleaving theory, visual models, and live coding demos.

---

## Core Concepts  

Below are the core concepts you must master for the AWS Data Engineer Associate exam. Each concept is broken into sub‑sections that mirror the way Databricks surfaces the feature, the underlying AWS services it uses, and the exam‑level objectives.

### 1. Databricks Workspace (AWS Edition)  

| Sub‑concept | Description | AWS Correlation |
|-------------|-------------|-----------------|
| **Account‑level workspace** | A single tenant within an AWS account (or multi‑account via SCIM). | Uses a **single IAM role** (`databricksAccountRole`) that the Databricks service assumes via **AWS STS**. |
| **VPC networking** | Workspace runs in your VPC, using **private subnets** for cluster nodes. | Security groups control inbound/outbound traffic to **ECS‑like EMR‑style instances**. |
| **Instance pools** | Pre‑provisioned groups of EC2 instances used for fast cluster launch. | Directly ties to **EC2 Spot / On‑Demand** capacity and **Auto Scaling Groups**. |

*Exam tip:* Expect questions that ask which **AWS resource** a given workspace setting influences (e.g., “Which IAM role is used when a job writes to a catalog‑managed table?” → answer: **`databricksJobRole`**).

---

### 2. Storage: S3 as the Primary Data Lake  

* **Raw bucket (`s3://my-company-raw/`)** – immutable files, no schema enforcement.  
* **Bronze, Silver, Gold buckets (`s3://my-company/bronze/…`)** – Delta tables that form the **Lakehouse** layers.  

**Key integration points:**  

- **S3 Event Notifications → Auto Loader** (for incremental ingestion).  
- **Lake Formation** can enforce **S3 bucket‑level policies** that restrict Databricks access to only the bucket prefixes it owns.  

*Exam focus:* Understanding **permissions** (`s3:GetObject`, `s3:PutObject`) that the **Databricks instance profile** must have and how they are scoped via **IAM policies** attached to the instance role.

---

### 3. Catalog, Schemas, Tables (Unity Catalog)  

- **Catalog** = logical namespace (often an AWS account or a business unit).  
- **Schema** = logical container (e.g., `bronze`, `silver`, `gold`).  
- **Table** = Delta Lake object managed by the **metastore**.  

**Why Unity Catalog matters:**  

- Provides **column‑level and row‑level ACLs** that can be **propagated from Lake Formation**.  
- Enables **single source of truth for data lineage** across Glue crawlers, EMR, and Databricks.  

*Exam tip:* A typical question will ask “Which feature allows a data engineer to grant `SELECT` on column `customer_id` to a downstream analyst without exposing the full table?” → answer: **Unity Catalog row‑level security**.

---

### 4. Auto Loader  

Databricks’ **incremental ingestion** service that automatically detects new files in S3 and materializes them as **micro‑batches**.  

- **Sources:** *File event, path‑glob, schema evolution.*  
- **Triggers:** *Continuous* (low latency) or *Batch* (periodic).  

**Under the hood:** Auto Loader uses **S3 event notifications** and a **state store in DynamoDB** (or Delta Lake) to track progress.  

*Exam focus:* Knowing which **auto‑loader option** (`cloudFiles`, `readStream`) will you use for a **high‑throughput, exactly‑once ingestion** scenario (answer: **`cloudFiles` with `readStream` and `trigger` = "continuous"**).

---

### 5. Delta Live Tables (DLT)  

DLT provides a **declarative pipeline** that translates Python/SQL into a **managed, versioned pipeline**.  

- **Source tables** can be Auto Loader bronze tables.  
- **Target tables** are stored in **Gold bucket** with **schema enforcement** and **optimised writes** (`OPTIMIZE`).  

**Resource mapping:** DLT runs on **Databricks‑managed clusters** that consume **EC2 Spot** instances, with **job‑level IAM roles** for S3 access.

*Exam tip:* Expect scenario‑based questions about **pipeline orchestration** – “Which feature would you use to chain a bronze‑to‑silver transformation with data quality checks?” → answer: **Delta Live Tables**.

---

### 6. Cluster Autoscaling & Instance Pools  

- **Auto Scaling** reacts to workload metrics (executors’ CPU, pending tasks).  
- **Instance Pools** keep a warm cache of **pre‑booted workers** (Spot or On‑Demand).  

This is directly related to **AWS Auto Scaling Groups (ASG)** and **Spot Fleet**, which the exam sometimes tests.  

*Key nuance:* A **job that requires 100 % SLA** will often be forced to run on **On‑Demand instance pools** to avoid Spot interruptions.

---

### 7. Observability (CloudWatch, Databricks UI, and SQL Analytics)  

- **CloudWatch Logs** capture driver and executor logs when you enable **log delivery**.  
- **Databricks Spark UI** surfaces task stages; you can enable **Spark History Server** to pull metrics from **S3**.  

Understanding **log aggregation** and **cost attribution** (e.g., “Which CloudWatch metric indicates a cluster is under‑provisioned?”) is a frequent exam focus.

---

## Architecture / How It Works  

Below is a **high‑level data flow** that ties together the concepts above. The diagram uses Mermaid syntax (rendered by most markdown viewers) to show **data ingestion**, **transformation**, and **exposure** across the Lakehouse.

```mermaid
flowchart LR
    subgraph S3[S3 Buckets (AWS)]
        raw["Raw (bronze) bucket\ns3://my-company/raw/"]:::raw
        curated["Curated (silver) bucket\ns3://my-company/silver/"]:::curated
        analytics["Analytics (gold) bucket\ns3://my-company/gold/"]:::analytics
    end

    subgraph Databricks[Databricks Workspace]
        direction TB
        wc[Workspace\n(IAM role: databricksAccountRole)]:::workspace
        alb[Auto Loader\nreadStream\nsource=raw]:::loader
        dlt[Delta Live Tables\nbronze→silver→gold]:::dlt
        notebooks[Notebooks / SQL\ndashboards]:::nb
    end

    subgraph Metastore[Unity Catalog Metastore]
        catalog[Catalog "company"]:::catalog
    end

    %% Data flow
    raw -->|S3 Event| alb
    alb -->|writes to Delta tables| dlt
    dlt -->|materializes bronze, silver, gold| curated
    curated -->|query from notebooks| notebooks
    notebooks -->|SQL analytics, BI tools| analytics

    %% Permissions
    classDef raw fill:#f9f,stroke:#333,stroke-width:1px;
    classDef curated fill:#bbf,stroke:#333,stroke-width:1px;
    classDef analytics fill:#cfc,stroke:#333,stroke-width:1px;
    classDef workspace fill:#ddd,stroke:#333,stroke-width:1px;
    classDef loader fill:#ff9,stroke:#333,stroke-width:1px;
    classDef dlt fill:#9ff,stroke:#333,stroke-width:1px;
    classDef nb fill:#eee,stroke:#333,stroke-width:1px;
    classDef catalog fill:#faf,stroke:#333,stroke-width:1px;

    %% IAM & Lake Formation
    class wc,alb,dlt,notebooks,catalog IAM[IAM Roles & Lake Formation Permissions];
```

**Explanation of the flow:**  

1. **Ingestion** – S3 event notifications (e.g., `ObjectCreated:*`) trigger **Auto Loader** (`cloudFiles`) which reads the new files from the **Raw bucket**.  
2. **Bronze materialization** – Auto Loader writes **append‑only Delta tables** into the **Bronze bucket**.  
3. **Silver transformation** – A **Delta Live Table pipeline** consumes the bronze tables, performs schema enforcement, deduplication, and writes **versioned** tables into the **Silver bucket**.  
4. **Gold analytics** – Notebooks or scheduled **SQL queries** (Databricks SQL) read the **Silver** tables, produce aggregate views, and optionally write derived tables back to the **Gold bucket**.  

All of these steps are secured by **IAM roles (`databricksAccountRole`, `databricksJobRole`)** and **Lake Formation ACLs** that restrict who can read/write at the **catalog → schema → table** level.

---

## Hands-On: Key Operations  

Below is a **step‑by‑step notebook** that you can run in a Databricks workspace (choose **Python** or **SQL** cells). Each code block includes **inline comments** that map to the architecture diagram.

> **Tip for the exam:** Be able to explain **why** you use `spark.conf` settings, `dbutils.fs.mount`, or `readStream` options; the exam will probe deeper than just syntax.

### 1️⃣ Mount S3 and Set Up the IAM Role  

```python
# ---------------------------------------------------------
# 1.1 – Define the IAM role that Databricks will assume.
# ---------------------------------------------------------
# In the UI: Workspace Settings → IAM Roles → Add
# Role ARN: arn:aws:iam::123456789012:role/databricksAccountRole
# Attach policies: AmazonS3FullAccess (or tighter bucket‑level policy)
# ---------------------------------------------------------

dbutils.widgets.text("s3_account_id", "123456789012")
dbutils.widgets.text("s3_raw_path", "s3://my-company-raw/")
```

> **Why it matters:** The IAM role must have `s3:GetObject` on `my-company-raw/*` and `s3:PutObject` on the Bronze bucket. Without proper policy, Auto Loader will silently fail.

### 2️⃣ Configure Auto Loader (Bronze Ingestion)  

```python
from pyspark.sql.functions import *

# ---------------------------------------------------------
# 2.1 – Read raw JSON files from S3 using Auto Loader
# ---------------------------------------------------------
raw_path = f"s3://{dbutils.widgets.get('s3_account_id')}/my-company-raw/"

df_bronze = (
    spark.readStream
    .format("cloudFiles")                # Auto Loader
    .option("cloudFiles.format", "json") # Format can be JSON, CSV, Parquet, etc.
    .option("cloudFiles.schemaLocation", "/mnt/meta/bronze_schema/")
    .option("cloudFiles.inferColumnTypes", "true")
    .load(raw_path)
)

# ---------------------------------------------------------
# 2.2 – Write as a Delta table partitioned by `event_date`
# ---------------------------------------------------------
(
    df_bronze
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/mnt/checkpoints/bronze/")
    .partitionBy("event_date")
    .trigger(availableNow=True)  # One‑time run; for production use .trigger(processingTime='5 minutes')
    .start("/mnt/delta/bronze/events")
)
```

> **Exam nuance:** `outputMode("append")` is mandatory for incremental ingestion. `event_date` must be a column you can derive (e.g., `to_date(col("timestamp"))`).  

### 3️⃣ Define a Delta Live Table (Silver)  

```python
# ---------------------------------------------------------
# 3.1 – Create a DLT pipeline (Silver layer)
# ---------------------------------------------------------
# Place this in a notebook that has the "Delta Live Table" runtime.
# ---------------------------------------------------------

@dlt.table(
    comment="Silver events after deduplication and timezone conversion.",
    table_properties={"qualityLevel": "gold"}  # optional: marks as Gold in Unity Catalog
)
def silver_events():
    # Read the bronze delta table created by Auto Loader
    bronze = spark.read.format("delta").load("/mnt/delta/bronze/events")
    
    # Apply transformations
    from pyspark.sql.functions import col, from_unixtime, to_utc_timestamp, expr

    # Example: convert epoch ms to timestamp, drop malformed rows
    cleaned = (
        bronze
        .withColumn("event_ts", from_unixtime(col("event_ts"), "MM/dd/yyyy HH:mm:ss"))
        .withColumn("event_ts_utc", to_utc_timestamp(col("event_ts"), "America/New_York"))
        .filter(col("event_ts_utc").isNotNull())
        .dropDuplicates(["event_id"])
    )
    return cleaned

# ---------------------------------------------------------
# 3.2 – Persist to the Silver bucket (partitioned by event_date)
# ---------------------------------------------------------
@dlt.table
def gold_events():
    # This will be a downstream view, not materialised on S3
    # Return a view that downstream SQL can use
    return spark.read.format("delta").load("/mnt/delta/silver/events")
```

> **Why DLT?** It gives you **data quality checks** (e.g., `expectOrDrop`) and **automatic schema evolution**. In the exam, you may be asked to compare **SQL `INSERT OVERWRITE`** vs **Delta Live Tables** for **quality enforcement**.

### 4️⃣ Run an Analytic Query (Gold)  

```sql
-- 4.1 – Create a Databricks SQL dashboard that reads the silver layer
CREATE OR REPLACE VIEW analytics.monthly_revenue AS
SELECT
  DATE_TRUNC('month', event_ts_utc) AS month,
  SUM(CAST(amount AS DOUBLE)) AS total_revenue
FROM
  company_silver.events  -- this is the catalog.table registered by DLT
GROUP BY month
ORDER BY month DESC;
```

> **Exam tip:** You’ll be asked to identify which **catalog** a given table lives in (`company_silver.events`). Remember that **catalog = workspace**, **schema = bronze/silver/gold**, **table = events**.

### 5️⃣ Observe & Debug with CloudWatch  

```python
# ---------------------------------------------------------
# 5.1 – Enable CloudWatch logging for a running job
# ---------------------------------------------------------
import json
import boto3

---

# **Section 4 – Databricks Platform**  
*Course: AWS Databricks Data Engineer Certification*  
*Target audience: Data engineers who already know Apache Spark and AWS Glue and want to pass the Databricks Certified Data Engineer – Associate exam.*

---

## **Databricks Platform**

### **Overview**

Databricks is a unified analytics platform that brings together the best of Apache Spark, a collaborative notebook environment, and a fully managed cloud service. It abstracts the operational complexity of Spark clusters while exposing a rich set of services for data ingestion, transformation, feature engineering, model training, and serving—all at petabyte scale.  

The platform is built around three pillars:

1. **Unified Workspace** – A multi‑language (Python, SQL, Scala, R) notebook environment that supports version control, job scheduling, and CI/CD pipelines.  
2. **Lakehouse Architecture** – A hybrid model that merges the flexibility of a data lake (open file formats, schema‑on‑read) with the reliability of a data warehouse (ACID transactions, schema‑on‑write, and fast analytics on Delta Lake).  
3. **Managed Runtime** – Databricks‑maintained Spark clusters that are optimized for the underlying cloud (AWS, Azure, GCP). The runtime provides auto‑scaling, cluster‑wide libraries, and security‑enhanced networking without the need for manual EMR or Glue configuration.

For the exam you must understand **how these pillars map to AWS services** and **what operational choices you have when you provision a Databricks workspace** (e.g., VPC, IAM roles, storage back‑ends, and monitoring).

---

### **Core Concepts**

Below each concept is broken out with sub‑sections you can use as talking points for a 45‑minute presentation.

#### 1. **Databricks Workspace**
* **Workspace hierarchy** – Servers → Clusters → Jobs → Notebooks → Repos.  
* **Workspace UI vs. API** – All actions (create clusters, submit jobs, manage secrets) are reachable via REST and Terraform.  
* **Multi‑tenancy** – Separate “workspaces” per environment (dev, test, prod) and per business unit; each workspace can have its own `workspace`‑level IAM policies.

#### 2. **Clusters**
* **Instance pools** – Pre‑warmed groups of EC2 instances that enable rapid scale‑out and consistent configuration.  
* **Autoscaling policies** – Minimum/maximum workers, idle timeout, and Spark‑dynamic allocation integration.  
* **Cluster modes** –  
  * *Standard* – Single driver, multiple workers (default).  
  * *High‑concurrency* – Optimized for notebooks and Jobs with many short‑lived tasks (e.g., 100+ concurrent queries).  

#### 3. **Delta Lake**
* **ACID transactions** – Guarantees atomic writes with versioned data.  
* **Time‑travel** – `VERSION AS OF` and `TIMESTAMP AS OF` for reproducible analytics.  
* **Optimized reads** – Data skipping (statistics), Z‑order clustering, and file compaction.

#### 4. **Auto Loader (Cloud Files)**
* **Incremental ingestion** – Detects new files in S3, ADLS, or GCS and automatically triggers schema inference, new‑file discovery, and streaming writes into Delta tables.  
* **Trigger options** – *Push* (file event) vs. *Polling* (interval) vs. *Event‑driven* (SQS, SNS).  

#### 5. **Serverless SQL & Data Engineering**
* **SQL warehouses** – Serverless, on‑demand query compute that can query Delta tables directly from the UI or via `spark.sql()`.  
* **Job orchestration** – Jobs can be scheduled with CRON expressions, have max retries, and use “max concurrent runs” to control resource contention.

#### 6. **Security & Governance**
* **Unity Catalog** – Centralized data governance that enforces table‑level, column‑level, and row‑level access across all workspaces.  
* **Encryption** – Data at rest (SSE‑KMS on S3) and in transit (TLS).  
* **Networking** – PrivateLink, VPC endpoints, and “Enable IP Access List” for workspace connectivity.

---

### **Architecture / How It Works**

The diagram below shows a typical end‑to‑end data pipeline that uses Databricks on AWS, S3 as the raw storage layer, and Delta Lake for the curated lake. The flow also demonstrates where you can plug in AWS services (Glue, IAM, CloudWatch).

```mermaid
flowchart TB
    subgraph AWS
        S3_Raw["Raw S3 Bucket (s3://company-raw/)"] 
        S3_Cur["Curated Delta Lake (s3://company-curated/)"] 
        IAM[IAM Role for Databricks\narn:aws:iam::123456789012:role/DatabricksClusterRole] 
        Glue[Glue Catalog & Crawlers] 
        CW[CloudWatch Logs & Metrics] 
    end

    subgraph Databricks
        Workspace["Databricks Workspace\n(PrivateLink VPC Endpoint)"] 
        AutoLoad["Auto Loader (Streaming)"] 
        SparkCluster["Databricks Cluster\n(Autoscaling, Instance Pool)"] 
        Unity["Unity Catalog\nData Governance"] 
        Jobs["Jobs & Scheduler"] 
        SQL["SQL Warehouse (Serverless)"] 
    end

    %% Data Flow
    S3_Raw -->|Event (S3 Put)| AutoLoad -->|Writes| Delta["Delta Lake Table\n(s3://company-curated/)"] --> Unity
    SparkCluster -->|Read/Write| Delta
    Jobs -->|Runs scheduled queries| Delta
    Unity -->|Reads metadata| Glue
    Jobs -->|SQL Analysts use| SQL
    Workspace -->|Interactive notebooks| SparkCluster

    %% Monitoring
    Jobs -->|metrics| CW
    SparkCluster -->|logs| CW
    AutoLoad -->|metrics| CW

    style AWS fill:#f8f9fa,stroke:#333,stroke-width:1px
    style Databricks fill:#e2f0ff,stroke:#333,stroke-width:1px
```

**Key take‑aways from the diagram**

* All data lands in **raw S3**; Databricks’ Auto Loader watches that bucket and streams changes into a **Delta Lake** zone.  
* The **Unity Catalog** sits on top of the curated zone, providing a single source of truth for table permissions and schema evolution.  
* Spark clusters are **managed by Databricks** (runtime, libraries, autoscaling) but still assume an **IAM role** that can read/write the S3 buckets and publish CloudWatch logs.  
* **Glue** is the source of the external Hive metastore; Databricks reads it to resolve schema when you first create a Delta table.  

---

### **Hands-On: Key Operations**

Below are concrete code snippets you can run in a Databricks notebook. Each block includes a short description, a purpose, and the expected outcome.

#### **1️⃣ Creating a Managed Delta Table with Auto Loader**

```python
# ---------------------------------------------------------
# 1️⃣ Define the source (raw S3) and target (curated Delta)
# ---------------------------------------------------------
raw_path = "s3://company-raw/events/"
curated_path = "s3://company-curated/events/"

# ---------------------------------------------------------
# 2️⃣ Auto Loader – streaming read with schema inference
# ---------------------------------------------------------
df_raw = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "/dbfs/tmp/schema_cache/events")
    .option("cloudFiles.schemaInference", "true")
    .load(raw_path)
)

# ---------------------------------------------------------
# 3️⃣ Write into Delta with checkpointing
# ---------------------------------------------------------
(
    df_raw
    .writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/dbfs/checkpoints/events_loading")
    .trigger(availableNow=True)   # For demo; use .trigger(ProcessingTime('5 minutes')) in prod
    .start(curated_path)
    .awaitTermination()
)
```

**Explanation**

* `cloudFiles.schemaLocation` stores the inferred schema so future files don’t re‑infer it, saving time.  
* `outputMode("append")` is safe for immutable event streams.  
* `checkpointLocation` guarantees exactly‑once semantics even if the job restarts.

---

#### **2️⃣ Optimizing a Delta Table (Z‑Ordering & OPTIMIZE)**

```sql
-- In the same notebook, switch to SQL for concise commands
USE CATALOG company_db;
USE SCHEMA raw;

-- Compaction & file size tuning
OPTIMIZE events
  WHERE event_date = '2024-11-01'   -- partition pruning
  ZORDER BY (user_id, event_type);  -- improve point‑lookup performance

-- Refresh table statistics for the optimizer
ANALYZE TABLE company_db.raw.events COMPUTE STATISTICS;
```

**Why it matters for the exam** – You’ll be asked how to make large Delta tables faster and how `OPTIMIZE` interacts with **cluster‑wide file compaction** and **statistics collection** for the query planner.

---

#### **3️⃣ Deploying a Job Using Databricks Jobs API (Python SDK)**

```python
import json, requests
from pathlib import Path

# ---------------------------------------------------------
# 1️⃣ Auth – use a personal access token (PAT) stored in a secret scope
# ---------------------------------------------------------
token = dbutils.secrets.get(scope="secret-scope", key="databricks-pat")
auth_header = {"Authorization": f"Bearer {token}"}
workspace_url = "https://adb-1234567890123456.19.azuredatabricks.net"

# ---------------------------------------------------------
# 2️⃣ Define the job (runs notebook that runs the above Auto Loader)
# ---------------------------------------------------------
job_payload = {
    "name": "Event Loader - Prod",
    "new_cluster": {
        "spark_version": "13.3.x-scala2.12",
        "node_type_id": "i3.xlarge",
        "num_workers": 2,
        "autoscale": {"min_workers": 2, "max_workers": 10},
        "aws_attributes": {"security_groups": ["sg-0123abcd"], "first_instance_profile": "my-instance-profile"}
    },
    "notebook_task": {
        "notebook_path": "/Shared/Load/auto_loader_events"
    },
    "max_concurrent_runs": 1,
    "schedule": {"quartz_cron_expression": "0 */6 * * ? *"}   # every 6 hours
}

# ---------------------------------------------------------
# 3️⃣ POST to Jobs endpoint
# ---------------------------------------------------------
response = requests.post(
    f"{workspace_url}/api/2.0/jobs/create",
    headers=auth_header,
    json=job_payload
)
job_id = response.json()["job_id"]
print(f"Job submitted, ID: {job_id}")
```

**Notes for the presenter**

* Show how the **cluster configuration** (autoscale, security groups, IAM role) is defined directly in the job payload – a typical exam scenario.  
* Emphasize that the **PAT** must be stored in a **Databricks secret scope** or via an **AWS Secrets Manager** integration to keep it out of code.

---

#### **4️⃣ Querying a Delta Table with Serverless SQL**

```sql
-- Create a catalog and schema if they don't exist
CREATE CATALOG IF NOT EXISTS company_db;
CREATE SCHEMA IF NOT EXISTS company_db.analytics;

-- Register the curated Delta location as a table
CREATE TABLE IF NOT EXISTS company_db.analytics.events
USING DELTA
LOCATION 's3://company-curated/events/';

-- Example analytical query using window functions
SELECT
    event_date,
    COUNT(*) AS total_events,
    APPROX_PERCENTILE(user_id, 0.5) AS median_user_id
FROM company_db.analytics.events
WHERE event_date BETWEEN DATE_SUB(current_date(), 30) AND current_date()
GROUP BY event_date
ORDER BY event_date;
```

*Running this query against the **SQL warehouse** automatically creates a separate compute cluster that scales on demand, isolates workloads, and can be paused when idle.*

---

### **AWS‑Specific Considerations**

| **AWS Service** | **Why it matters in Databricks** | **Key Configuration Tips** |
|-----------------|----------------------------------|-----------------------------|
| **S3** | Primary storage for raw, curated, and checkpoint data. | • Enable **S3 Server‑Side Encryption (SSE‑KMS)** with a CMK you own. <br>• Use **S3 bucket policies** that restrict access to the Databricks IAM role only. <br>• Turn on **Versioning** for raw buckets to enable rollback. |
| **IAM** | Databricks clusters assume an IAM role to read/write S3, read the Glue catalog, and push CloudWatch metrics. | • **Instance profile** must have `AmazonS3FullAccess` (or least‑privilege S3 actions), `AWSGlueConsoleFullAccess`, and `CloudWatchFullAccess`. <br>• Use **IAM Role for Service Accounts (IRSA)** for fine‑grained access from notebooks to AWS APIs (e.g., boto3 calls). |
| **Glue** | Central metastore for schema. Databricks reads tables via **Unity Catalog** but can be configured to sync with the Glue Data Catalog. | • Enable **Glue Data Catalog integration** in the workspace (Admin Console → Metastore settings). <br>• Run Glue **Crawlers** after large data loads to refresh table metadata. |
| **EMR** | Not a replacement for Databricks, but sometimes you run Spark jobs on EMR for cost‑optimized batch workloads. | • If you need to spin up an EMR cluster from a Databricks notebook, use the **AWS SDK** (`boto3`) with `cluster_id` returned from the EMR `run_job_flow` API. |
| **Lake Formation** | Provides fine‑grained table‑level permissions that complement Unity Catalog. | • When a table is created in a Databricks location that is also registered in Lake Formation, **grant SELECT** to a LF principal, then **enable LF integration** on the Databricks workspace. |
| **CloudWatch** | Default destination for Spark metrics, logs, and job run events. | • Enable **Log Delivery** from the workspace → *Cluster* → *Logging* to a dedicated S3 bucket. <br>• Create **CloudWatch Alarms** on `cluster_start_failure` and `executor_core_utilization` metrics to catch runaway scaling. |
| **VPC / PrivateLink** | Guarantees that data traffic never traverses the public internet. | • Deploy the workspace inside a **VPC** and enable **PrivateLink** for the Databricks service. <br>• Use **S3 VPC Endpoints (Gateway)** for S3 access without NAT gateways. |
| **KMS** | Encryption at rest for both S3 and Delta Lake tables. | • Use a **Customer‑Managed CMK** for S3 bucket encryption and for the Delta Lake transaction log if you require additional control. |

> **Exam tip:** Questions often ask you to identify the *minimum* IAM permissions required for a cluster to read from a specific S3 bucket and write to another bucket, or to decide whether a job should run on a **standard** vs **high‑concurrency** cluster based on latency requirements.

---

### **Exam Focus Areas**

- **Cluster provisioning & autoscaling** – understand standard vs high‑concurrency, instance pools, and how to set max/min workers.  
- **Delta Lake fundamentals** – ACID, time‑travel, OPTIMIZE, Z‑ordering, and how to manage schema evolution (`ALTER TABLE … SET TBLPROPERTIES delta.sharing.isDelta = true`).  
- **Auto Loader configurations** – new‑file discovery, triggering strategies, and handling schema changes.  
- **Unity Catalog vs. Glue Catalog** – permissions, table registration, and cross‑workspace data sharing.  
- **Job scheduling & API usage** – creating jobs via UI, REST API, and Terraform; setting max concurrent runs; using `max_retries`.  
- **SQL Warehouses** – when to use serverless SQL vs. notebook jobs; cost‑based scaling; query result caching.  
- **Security & networking** – VPC, PrivateLink, S3 bucket policies, and IAM role scoping.  
- **Monitoring & troubleshooting** – CloudWatch metrics for cluster health, Spark UI, and job run logs.  

---

### **Quick Recap**

- **▶️ The Databricks workspace is the single source of truth for notebooks, jobs, and clusters, but it lives inside your AWS account.**  
- **▶️ Delta Lake + Auto Loader give you lakehouse‑grade reliability and automatic incremental ingestion – the two features the exam loves to test.**  
- **▶️ Cluster configuration (standard vs. high‑concurrency) dictates cost and performance; know the knobs you can turn.**  
- **▶️ AWS services (S3, IAM, Glue, Lake Formation, CloudWatch) are tightly coupled; any architecture question will involve at least two of them.**  
- **▶️ Master the “Job API payload” – it is the bridge between code, security, and resource allocation.**  

---

### **Code References**

| Resource | Link

---

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

---

# Delta Lake Core Concepts  

*(Section 6 of 15 – AWS Databricks Data Engineer Certification)*  

> **Goal of this section** – By the end of the 45‑60 min walkthrough a data engineer should be able to *explain* every Delta Lake feature that appears on the Databricks Associate exam, *perform* the most common Delta operations in a notebook, and *map* those operations to the AWS services they use in production (S3, IAM, Glue, EMR, Lake Formation, CloudWatch, etc.).  

---  

## Overview  

Delta Lake is an open‑source storage layer that brings **transactional guarantees, schema enforcement, and high‑performance reads** to Apache Spark workloads on AWS.  In contrast to raw data in S3 (which is immutable and offers eventual consistency only), Delta Lake stores **data as Parquet files** that are *versioned* and *validated* by the Delta transaction log (`_delta_log`).  The log is a set of JSON checkpoint files that record every commit (add, remove, or update) as an atomic operation.  Because the commit protocol is implemented in Spark, the same API works for batch and streaming jobs, and because the files are stored in S3 the solution scales horizontally, is fault‑tolerant, and can be integrated with the rest of the AWS ecosystem.  

Key concepts introduced here:  

* **ACID transactions** – a write to a Delta table is either fully visible or invisible, never partially visible.  
* **Schema evolution & enforcement** – you can add/rename columns without breaking downstream jobs.  
* **Time travel** – you can query any previous version of a table (e.g., `SELECT * FROM my_table VERSION AS OF 3`).  
* **Optimized reads** – file compaction, Z‑ordering, and data skipping (statistics) dramatically reduce I/O for analytical queries.  

On AWS, Delta Lake is typically the **glue** between raw ingestion (e.g., S3 buckets with raw logs) and the curated, analytics‑ready data that data scientists and downstream jobs consume.  The next sections drill down into the components that make this possible.  



---  

## Core Concepts  

Below each concept is broken into bite‑size sub‑sections that map directly to exam objectives.  

### 1. Delta Lake Tables  

| Concept | Description |
|---------|-------------|
| **Managed vs. External** | Managed tables store the table location inside the database (`spark.sql("CREATE TABLE db.t"));`) and the system creates a hidden `_delta_log` folder. External tables only point to an existing directory; the location is managed outside Spark (e.g., an S3 bucket). |
| **Table format** | Data lives in a folder containing **Parquet files** + a **_delta_log** folder.  The log contains JSON files (`00000000000000000000.json`, `00000000000000000001.json`, …) that capture every transaction. |
| **Table properties** | `delta.logRetentionDuration`, `delta.dataSkippingStats.enabled`, `delta.autoOptimize.optimizeWrite` are set via `ALTER TABLE … SET TBLPROPERTIES`.  These control compaction, caching, and auto‑optimizations. |

### 2. ACID Transactions  

* **Atomicity** – A Spark job writes a batch of new Parquet files, then atomically writes a JSON commit file to `_delta_log`.  If the job crashes before the commit, the transaction never appears.  
* **Consistency** – Reads that use the latest **valid snapshot** will see either the old state *or* the new state, never an intermediate one.  
* **Isolation** – Each transaction gets a **transaction ID** (e.g., `txId = 5`).  Reads at version 4 will not see version 5 until the transaction is committed.  
* **Durability** – Once the commit file is persisted in S3, it is stored on at least three S3 replicas.  The commit cannot be rolled back.  

### 3. Schema Enforcement & Evolution  

```python
# Enable schema enforcement (default in Databricks)
spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")

# Add a nullable column without breaking existing jobs
df.write.format("delta") \
    .option("mergeSchema", "true") \
    .mode("append") \
    .saveAsTable("sales")

# Disallow column renames unless you explicitly enable them
spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "false")
```

* **Enforced** – If an incoming DataFrame has a column missing or a type mismatch, the write fails.  
* **Evolution** – `mergeSchema` on write (or `ALTER TABLE … ALTER COLUMN …`) can add columns, rename, or drop columns.  

### 4. Time Travel & Data Retention  

```sql
-- View table as it existed 12 hours ago
SELECT * FROM sales VERSION AS OF TIMESTAMP '2025-11-20 13:45:00';

-- List all available versions
DESCRIBE HISTORY sales;

-- Revert to a previous version (creates a new branch)
RESTORE TABLE sales TO VERSION AS OF 41;
```

* **Retention** – Controlled by `delta.logRetentionDuration` (default 30 days).  If you need longer history for audits, increase it, but remember the cost of storing extra log files in S3.  

### 5. Optimized Reads – File Compaction & Z‑Ordering  

* **Data Skipping** – Delta automatically writes statistics (min/max, null count, distinct values) for each Parquet file. Spark uses these to prune files during query planning.  
* **Optimize (Compaction)** – Combines small files into larger files (default 256 MiB) and rewrites the history.  
* **Z‑Order** – Physically reorders data inside files based on one or more columns, drastically reducing the amount of data scanned for queries that filter on those columns.  

```python
# Optimize and Z‑order a table
spark.sql("OPTIMIZE sales WHERE is_current = true")
    .option("zorderBy", "customer_id,order_date") \
    .execute()
```

---  

## Architecture / How It Works  

Below is a **logical data flow** for an end‑to‑end ingestion pipeline on AWS.  The diagram uses **Mermaid syntax** for easy rendering in most documentation tools.  

```mermaid
flowchart TB
    subgraph ingestion[Raw Ingestion]
        A[S3 Raw Landing Zone<br/>(bucket: raw-logs)] -->|EventBridge| B[Auto Loader (Streaming)]
        C[Glue Crawler] -->|Update Glue Catalog| D[Delta Catalog (Glue Integration)]
    end

    subgraph processing[Databricks Clusters]
        B -->|micro‑batch| E[Delta Write (bronze)]
        E -->|SQL / PySpark| F[Delta Optimize / Z‑Order (silver)]
        F -->|SQL| G[BI Dashboard (QuickSight / Tableau)]
    end

    subgraph serving[Production Layer]
        D -->|Enable Delta Lake| G
        G -->|Query| H[Databricks SQL Warehouse]
    end

    subgraph observability[Ops & Governance]
        I[S3 Access Logs] -->|CloudWatch| J[CloudWatch Logs & Metrics]
        K[Delta Lake REST API] -->|Audit| J
        L[IAM Role] -.->|Secure access| A & B & E & F
    end
```

### Narrative Walk‑through  

1. **Raw data** lands in an S3 bucket (`raw-logs`).  An S3 event triggers **AWS EventBridge** which starts a **Databricks Auto Loader** job (continuous streaming).  
2. Auto Loader writes directly into a **bronze Delta table** (`bronze.sales`).  Because Auto Loader writes with *mergeSchema* enabled, any new nested fields appear automatically.  
3. A **Databricks notebook** runs nightly to **optimize and Z‑order** the bronze table, producing a **silver Delta table** (`silver.sales_curated`).  
4. The **Delta Catalog** registers the tables with the Glue Data Catalog, allowing **Lake Formation** permissions and cross‑service (Athena, Redshift Spectrum) access.  
5. Analysts query the curated table through **Databricks SQL Warehouse** or external tools (QuickSight, Tableau) – all benefit from **statistics‑driven pruning** and **compact file sizes**.  

---  

## Hands-On: Key Operations  

The following notebook‑style snippets are ready to copy/paste into a Databricks cluster (Python/Scala/SQL mixed).  Each block includes a short rationale.  

### 1️⃣ Create a Managed Bronze Table  

```python
# ------------------------------------------------------------------
# 1. Read raw JSON from S3 using Auto Loader (micro‑batch streaming)
# ------------------------------------------------------------------
raw_df = (spark.readStream.format("cloudFiles")
          .option("cloudFiles.format", "json")
          .option("cloudFiles.schemaLocation", "/tmp/schema/sales")
          .option("cloudFiles.schemaEvolutionMode", "addColumns")
          .load("s3://raw-logs/sales/*.json"))

# Write to a bronze Delta table (append only)
(write_q = raw_df.writeStream.format("delta")
                         .option("checkpointLocation", "/tmp/checkpoints/sales")
                         .outputMode("append")
                         .trigger(processingTime="30 seconds")
                         .start("/mnt/delta/bronze/sales"))

# In another notebook, run the following to make it a table:
spark.sql("DROP TABLE IF EXISTS bronze.sales")
spark.sql("""
    CREATE TABLE IF NOT EXISTS bronze.sales
    USING DELTA
    LOCATION '/mnt/delta/bronze/sales'
""")
```

*Why?*  Auto Loader handles schema evolution and back‑pressure. The checkpoint location guarantees exactly‑once semantics.  

---

### 2️⃣ Enforce Schema & Add a Column (Schema Evolution)  

```sql
-- First, enforce schema on the table
ALTER TABLE bronze.sales SET TBLPROPERTIES (delta.autoMerge.schema.enabled = true);

-- Append new data that contains a new column `promo_code`
sales_new_df = spark.read.format("json").load("s3://raw-logs/sales_2025-11-30.json")
sales_new_df.write.format("delta").mode("append").saveAsTable("bronze.sales")
```

*Why?*  Without `delta.autoMerge.schema.enabled`, the write would fail because the schema of the new JSON includes `promo_code`.  

---

### 3️⃣ Optimize & Z‑Order the Silver Table  

```python
# Optimize (file compaction) – runs nightly via a Databricks job
spark.sql("OPTIMIZE bronze.sales WHERE is_current = true")
    .option("maxFileSize", "256MB")
    .execute()

# Z‑order on the columns most used in filters
spark.sql("""
    OPTIMIZE bronze.sales
    WHERE is_current = true
    ZORDER BY (customer_id, order_timestamp)
""")
```

*Why?*  Optimizing reduces the number of Parquet files from thousands of 10‑MiB blobs to ~10–20 256‑MiB files, cutting I/O and improving cache locality.  

---

### 4️⃣ Time‑Travel Query  

```sql
-- Show sales for a specific day *before* the schema changed
SELECT * FROM bronze.sales VERSION AS OF TIMESTAMP '2025-11-28 00:00:00'
WHERE order_timestamp::date = '2025-11-25'
```

*Why?*  Demonstrates the *reproducibility* of analytical results—critical for audit trails.  

---

### 5️⃣ Vacuum & Retention Management  

```python
# Delete old files after 7 days (Delta default is 30 days)
spark.sql("VACUUM bronze.sales RETAIN 168 HOURS")   # 168 hours = 7 days
```

*Why?*  Removing obsolete files frees S3 storage and reduces the size of the transaction log.  

---  

## AWS‑Specific Considerations  

| AWS Service | How it interacts with Delta Lake | Recommended Settings / Tips |
|-------------|----------------------------------|------------------------------|
| **S3** | Stores all Parquet files and `_delta_log`. | Use **S3 Object Lock** (Governance mode) on `_delta_log` to prevent accidental deletion; enable **S3 Batch Operations** for lifecycle policies (e.g., transition older versions to Glacier). |
| **IAM** | The Databricks instance profile must have `s3:GetObject`, `s3:PutObject`, `s3:ListBucket` on the Delta lake bucket, plus `glue:*` for catalog access. | Attach a **policy with condition `aws:PrincipalTag/DeltaAccess`** to enforce bucket‑level scoping. Rotate keys via **IAM Access Analyzer** for compliance. |
| **AWS Glue (Crawler + Data Catalog)** | Glue crawlers discover Delta tables; the Delta Lake **catalog** (Unity Catalog) can be used as a single source of truth. | Register Delta tables under **Unity Catalog**; enable **Lake Formation** permissions to let Athena/Redshift Spectrum query them without copying data. |
| **AWS Glue ETL** | Can read/write Delta tables using the **Spark‑SQL dialect** of Glue. | Use **`glueversion: "4.0"`** and the **`delta`** connector (`spark.conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")`). |
| **Amazon EMR (with Databricks on‑AWS)** | EMR can host a Databricks‑compatible Spark cluster that runs Delta jobs, but for the exam focus we assume **Databricks on AWS** as a managed service. | EMRFS consistent view is **not required** when using Delta because the transaction log is stored in S3. However, ensure **EMRFS S3Guard** is disabled to avoid caching stale file listings. |
| **Lake Formation** | Centralizes fine‑grained access; can grant `SELECT` on a Delta table to a data scientist group. | Use **`grant SELECT ON TABLE delta.sales TO `data_analyst`** with a `columnMask` if you need column‑level security. |
| **CloudWatch** | Auto Loader streams metrics (`files_per_trigger`, `trigger_error_count`).  Delta write events can be logged via **`spark.databricks.delta.logStore.file.system.enabled`**. | Create a **CloudWatch dashboard** with metrics: `DeltaCommitTime`, `DeltaTransactionLogSize`, `S3PutObjectBytes`. Set alarms when transaction log growth > 2 GB/day (possible write‑skew). |
| **AWS Transfer Family (optional)** | For on‑prem data ingestion, you may receive files via SFTP. Store them temporarily in S3, then let Auto Loader ingest. | Use **S3 EventBridge** on the destination bucket to start Auto Loader only when new files are > 50 MiB (avoid tiny files). |

**Security Best‑Practice** – Store the **Delta log in a separate S3 bucket** (or a dedicated prefix with a separate KMS key) and enforce **cross‑account read‑only** access for analytics accounts. This isolates data‑processing responsibilities and aligns with AWS **Shared Responsibility Model**.  

---  

## Exam Focus Areas  

*The Databricks Certified Data Engineer Associate exam tests your ability to recall concepts **and** perform operations in a live notebook.*  Below are the most frequently asked topics for this section.  

- **Delta Architecture** – Explain why the transaction log (`_delta_log`) provides ACID semantics.  
- **Table Types** – Be able to distinguish *managed* vs *external* Delta tables, and know how to set the `location` property.  
- **Schema Enforcement** – State the default behavior (`spark.databricks.delta.schema.autoMerge.enabled = false`).  Show how to enable it safely.  
- **Time Travel** – Write a SQL query that reads a specific version or timestamp.  
- **Optimize & Z‑Ordering** – Identify the correct command (`OPTIMIZE`) and required options (`maxFileSize`, `zorderBy`).  
- **Data Skipping** – Explain how statistics are generated and used.  
- **Vacuum & Retention** – When can you safely run `VACUUM`?  (Answer: after a successful `OPTIMIZE` and when you are sure no job is still reading older versions.)  
- **AWS Integration** – Which IAM permissions are required for a Delta write to S3?  (Answer: `s3:PutObject`, `s3:PutObjectAcl`, `s3:GetObject`, `s3:DeleteObject

---

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

---

## Data Ingestion with Auto Loader
### Section 8 of 15 – AWS Databricks Data Engineer Certification  

> **Prerequisites** – Before diving into this section you should be comfortable with:  
> - Spark Structured Streaming (read/write, watermarking, stateful ops).  
> - AWS Glue jobs, S3 event notifications, and IAM policies.  
> - The basic concepts of Delta Lake (ACID, schema enforcement, Z‑ordering).  

> **Goal of the Section** – To equip you with a deep, exam‑ready understanding of Auto Loader, its architecture, operational patterns, and AWS‑specific integration so you can **explain, configure, and troubleshoot** data ingestion pipelines for the Databricks Certified Data Engineer Associate exam.

---  

## Overview  
*(3‑4 paragraphs written like a technical book chapter)*  

Auto Loader is Databricks’ **managed incremental data ingestion engine** that monitors external storage locations (S3, ADLS, Azure Blob) and automatically discovers new files, schema changes, and file formats without the need for complex custom logic. Unlike a traditional `spark.readStream` + `trigger(processingTime)` pattern, Auto Loader continuously polls source directories, leverages **checkpointing** and **metadata inference**, and guarantees **exactly‑once** ingestion when paired with Delta Lake.  

Its design is motivated by the “**unknown‑file‑set problem**”: in a data lake you rarely know the exact schema of incoming files ahead of time, nor can you pre‑register each partition. Auto Loader solves this by (1) **continuously scanning** the source for new files, (2) **inferring** the schema (or using a supplied schema), (3) **building a streaming micro‑batch** for each poll interval, and (4) **applying schema evolution** in a deterministic way. The **checkpoint** directory stores the **watermark** (last processed file) and the **batch offsets**, enabling the engine to resume after failures without re‑processing data.  

In an AWS‑centric environment Auto Loader plugs directly into S3 event notifications or **Glue crawlers** for schema discovery, and it can be combined with **Lake Formation permissions** to enforce fine‑grained security. It also integrates with **EMR Serverless** for cost‑effective processing, and with **CloudWatch** for observability (metrics, logs, and dead‑letter queues). The exam expects you to understand **how Auto Loader differs from manual Structured Streaming, what guarantees it provides, and which configuration knobs you should tune for reliability and cost**.  

---  

## Core Concepts  

Below are the building blocks you must master. Each sub‑section can be expanded in a live notebook.

| Concept | Why It Matters | Typical Parameters |
|---------|----------------|--------------------|
| **Source URI** | Absolute path (e.g., `s3://my-bucket/raw/`) that Auto Loader will watch. Supports wildcards and partitions. | `sourcePath`, `recursive` |
| **File Discovery & Polling** | Auto Loader polls S3 using list‑operations; the interval can be **event‑driven** (S3 event notifications + SQS) or **time‑driven** (`maxFilesPerTrigger`). | `fileDiscoveryMode`, `maxFilesPerTrigger` |
| **File Format Inference** | Works for **JSON**, **CSV**, **Parquet**, **AVRO**, **ORC**. Schema inference can be **explicit** (`schemaLocation`) or **implicit** (`inferSchema`). | `cloudFiles.format`, `cloudFiles.schemaLocation` |
| **Micro‑batch Management** | Each poll results in a micro‑batch that is executed as a regular Spark Structured Streaming job. Auto Loader handles **idempotent offsets** and **watermarking** automatically. | `trigger` (continuous vs. default), `processingTime` |
| **Schema Evolution & Merge** | When new columns appear, Auto Loader can **merge** into Delta tables using `mergeSchema` or `overwriteSchema`. Guarantees **backward compatibility** for downstream pipelines. | `mergeSchema`, `overwriteSchema` |
| **Checkpointing & Offsets** | Stores the **last processed file list** in the checkpoint directory. The checkpoint is *not* a Spark checkpoint; it is a tiny JSON set of file paths + timestamps. | `checkpointLocation` |
| **Safety Guarantees** | - **Exactly‑once** when writing to Delta Lake. <br>- **At‑least‑once** to external stores (e.g., Kafka). | `badRecordsPath`, `deadLetterQueue` |
| **Failure Recovery** | On failure, the job restarts from the checkpoint; if a file was partially processed, Auto Loader re‑processes the entire file (idempotent write). | `restartFromCheckpoint` |

### 8.1 File Discovery Modes  

1. **Continuous** – Auto Loader continuously watches for new files (uses S3 events + a **manifest** file). Ideal for low‑latency pipelines.  
2. **Batch** – Polls every `triggerInterval` (default 1 minute) and processes all files discovered since the last checkpoint. Simpler, more deterministic for exam scenarios.  

### 8.2 Schema Evolution Strategies  

- **Append‑Only**: `df.writeStream.format("delta").option("mergeSchema", "true")`. Use when new columns are *optional*.  
- **Overwrite**: `option("overwriteSchema", "true")` – useful for **re‑processing** data with a new schema (e.g., after a schema change event).  

### 8.3 Bad Record Handling  

```python
df = spark.readStream.format("cloudFiles") \
    .option("cloudFiles.format", "json") \
    .option("cloudFiles.schemaLocation", "/mnt/checkpoints/schemas") \
    .option("cloudFiles.includeFirstRow", "true") \
    .load("s3://data-raw/")
```

- `df.writeStream.format("delta").option("badRecordsPath", "/mnt/bad_records")` – captures malformed rows to a Delta table for later inspection.  

---  

## Architecture / How It Works  

Below is a **mermaid** diagram that shows the data flow from an S3 bucket to a Delta Lake table using Auto Loader.  

```mermaid
flowchart LR
    subgraph AWS
        S3[S3 Bucket<br/>raw/]
        SQS[S3 Event → SQS Queue]
        IAM[IAM Role<br/>Databricks‑Loader]
    end

    subgraph Databricks
        DL[Auto Loader<br/>(cloudFiles)] 
        CP[Checkpoint Dir<br/>(/mnt/checkpoints)]
        BD[Delta Lake<br/>bronze_table]
        LFA[Lake Formation<br/>Catalog & Permissions]
    end

    S3 -->|new file| SQS
    SQS -->|trigger| DL
    DL -->|read incremental| CP
    CP -->|store offsets| DL
    DL -->|write micro‑batch| BD
    BD -->|cataloged| LFA

    style S3 fill:#f9f,stroke:#333,stroke-width:2px
    style DL fill:#bbf,stroke:#333,stroke-width:2px
```

**Explanation of the diagram**  

1. **S3 Bucket** – producers land raw files (e.g., `raw/year=2025/...`).  
2. **S3 Event + SQS** – optional event notification pushes a message to an SQS queue; Auto Loader polls the queue for a *push* model (otherwise it uses the default *pull* model).  
3. **Auto Loader** – receives the trigger, reads the incremental file list, builds a micro‑batch, and writes to the **Delta Lake bronze** table.  
4. **Checkpoint Directory** – stores the high‑water mark (last file list) and the offset state; it lives on a highly available storage location (`/mnt/checkpoints`).  
5. **Delta Lake Bronze** – the landing zone where data is **append‑only**, `mergeSchema` enabled, ready for downstream *silver* and *gold* transformations.  
6. **Lake Formation** – enforces column‑level access and registers the Delta table as a catalog entity.  

---  

## Hands‑On: Key Operations  

The following notebook‑style snippets illustrate the most exam‑relevant tasks. Each block is annotated with a **purpose note** to help you explain the *why* while presenting.

```python
# --------------------------------------------------------------
# 1️⃣  Define the source and checkpoint locations
# --------------------------------------------------------------
source_path = "s3://my-company-raw/events/"
checkpoint_path = "s3://my-company-checkpoints/events/"

# --------------------------------------------------------------
# 2️⃣  Read the streaming source with Auto Loader
# --------------------------------------------------------------
df = (
    spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")               # format can be parquet, csv, etc.
        .option("cloudFiles.inferColumnTypes", "true")    # auto‑cast strings to ints, timestamps
        .option("cloudFiles.schemaLocation", "/mnt/checkpoints/schemas/events/")
        .option("cloudFiles.maxFilesPerTrigger", 500)     # throttles batch size (helps control cost)
        .option("cloudFiles.enableWatermark", "true")     # required for time‑based joins
        .load(source_path)
)

# --------------------------------------------------------------
# 3️⃣  Write to Delta Lake (Bronze) with exactly‑once semantics
# --------------------------------------------------------------
query = (
    df.writeStream
        .format("delta")
        .outputMode("append")                # only append; merge will be done later if needed
        .option("checkpointLocation", checkpoint_path)
        .option("mergeSchema", "true")       # automatically add new columns
        .trigger(processingTime="30 seconds")  # default micro‑batch interval
        .start("s3://my-company-delta/bronze/events/")
)

# --------------------------------------------------------------
# 4️⃣  Capture bad records – exam tip: you must set this before a failure
# --------------------------------------------------------------
df_bad = (
    df.reformat("json")  # ensure the DataFrame is a streaming DataFrame with a defined schema
)

df_bad.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/mnt/checkpoints/bad_records/") \
    .option("badRecordsPath", "s3://my-company-bad/records/") \
    .start()
```

### Block‑by‑Block Explanation  

| Block | What It Demonstrates | Exam Relevance |
|-------|----------------------|----------------|
| **1️⃣** | Setting the **source** and **checkpoint** as S3 URIs (the same storage accounts can be reused across jobs). | Auto Loader **must** have a checkpoint on durable storage for exactly‑once guarantees. |
| **2️⃣** | Using `format("cloudFiles")` – the *only* Spark connector that implements Auto Loader. `inferColumnTypes` and `schemaLocation` illustrate schema handling. | Shows you can **avoid manual schema injection**; the exam will ask about **`cloudFiles.schemaLocation`** vs. **`inferColumnTypes`**. |
| **3️⃣** | Writing to Delta Lake with `mergeSchema` and a **30‑second trigger**. `outputMode("append")` is required for Auto Loader. | Guarantees **exactly‑once** when the sink is Delta. Also highlights **watermarking** (implicit when `enableWatermark` is true). |
| **4️⃣** | Demonstrates **bad‑record handling** using `badRecordsPath` and `badRecordsFileSink`. | Frequently tested: *What happens to malformed JSON?* Capture and later analyze. |

> **Tip for the exam** – If a question asks *how to guarantee that a schema change will not break the pipeline*, the correct answer is to set `mergeSchema` to **true** *or* explicitly `overwriteSchema` when you know you need a full schema replacement.  

---  

## AWS‑Specific Considerations  

| AWS Component | Integration Point | Recommended Settings / Gotchas |
|---------------|-------------------|--------------------------------|
| **S3 Bucket** | Source for raw files; destination for `badRecordsPath`. | Enable **S3 Event Notifications** for the prefix you monitor. Use **Object Lambda** (optional) to transform CSV headers to a uniform schema before Auto Loader sees them. |
| **IAM Role** | Databricks runtime role must have `s3:ListBucket`, `s3:GetObject`, `s3:PutObject` on the raw and checkpoint locations. | Grant `s3:GetObjectVersion` if you need to read versioned objects. Use **Managed Instance Profile** for EMR Serverless or **Databricks Instance Profile** with a policy that follows the **least‑privilege** principle. |
| **AWS Glue Catalog** | Auto Loader can automatically **populate** the catalog if you set `catalogTable` option (requires Hive Metastore). | Run a **Glue Crawler** on the raw bucket *once* to generate an initial schema; then `cloudFiles.schemaLocation` can reference that schema. |
| **Lake Formation** | Register the Delta Lake bronze tables. Permissions are checked at read/write time. | After creating a bronze table, execute `lakeFS` or `glue` `grant` statements to give downstream teams `SELECT` on the table and `INSERT` on the bronze location. |
| **EMR Serverless** | Auto Loader runs as part of a **Spark‑SQL job** on EMR Serverless – you only pay for the micro‑batch runtime. | Set **`spark.databricks.delta.retentionDurationCheck.enabled` = false** if you want aggressive data cleanup (useful for cost control in exam scenarios). |
| **CloudWatch** | Auto Loader emits **metrics** (`databricks.autoloader.*`) and **log events** to `/databricks/logs/autoloader`. | Create a **CloudWatch alarm** on `NumberOfFilesProcessed` that triggers an SNS notification if the rate spikes (possible data duplication). |
| **AWS Step Functions (optional)** | Orchestrates a **multi‑step pipeline**: Auto Loader → Bronze → Silver → Gold. | Use the `aws-sdk` task to call `databricks:CancelRestJob` for graceful shutdown during maintenance. |

> **Key Takeaway:** Auto Loader is **agnostic** to the underlying cloud, but on AWS you must be aware of **event notification latency**, **IAM policy granularity**, and **cost implications of checkpoint storage**. The exam will often ask *which combination of S3 notifications and Auto Loader settings gives sub‑minute latency* – the answer is “**S3 event → SQS → Auto Loader (continuous mode)**”.  

---  

## Exam Focus Areas  

- **Identify the correct format** to read a streaming source with Auto Loader (`cloudFiles`).  
- **Explain the role of `cloudFiles.schemaLocation`** and why it must be stored in a reliable location.  
- **Compare and contrast**: `mergeSchema` (default safe) vs. `overwriteSchema` (use with caution).  
- **Select the right trigger** for a given latency requirement:  
  - *Continuous* → < 5 s latency (requires S3 event + SQS).  
  - *Micro‑batch* (`trigger(processingTime)`) → predictable cost, easier to reason about.  
- **Configure exactly‑once** semantics: checkpoint location, write mode, and Delta Lake `mergeSchema`.  
- **Troubleshoot common failure modes**:  
  - Missing IAM permissions → `AccessDenied` errors.  
  - Stale checkpoint → duplicate processing.  
  - `FileAlreadyExistsException` – caused by writing to the same delta location with two concurrent jobs.  
- **Cost‑optimization**: Use `maxFilesPerTrigger` to cap the number of files processed per micro‑batch; choose **EMR Serverless** for autoscaling without EC2 management.  

---  

## Quick Recap  

- ✅ **Auto Loader = managed, schema‑agnostic, exactly‑once streaming ingest** – no custom code needed.  
- ✅ **Checkpointing is mandatory** and must be on a durable store (S3, ADLS).  
- ✅ **`cloudFiles` options** (`format`, `inferColumnTypes`, `schemaLocation`, `maxFilesPerTrigger`) control latency, cost, and schema handling.  
- ✅ **Exactly‑once guarantees** require Delta Lake + checkpoint; other sinks (Kafka, Kinesis) give at‑least‑once.  
- ✅ **AWS integration**: S3 event notifications, IAM role scopes, Glue catalog, Lake Formation, and CloudWatch metrics are all part of a production‑grade pipeline.  

---  

## Code References  

| Resource | Link | Why It Helps |
|----------|------|--------------|
| **Databricks Auto Loader Documentation** | https://docs.databricks.com/ingestion/auto-loader/index.html | Full reference for every option, example notebooks, and troubleshooting guide. |
| **Spark Structured Streaming – Continuous Processing** | https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#continuous-processing | Useful to differentiate Auto Loader’s continuous mode vs. micro‑batch. |
| **Delta Lake Optimized Writes** | https://docs.delta.io/latest/delta-update.html | Shows how `mergeSchema` works under the hood. |
| **AWS Glue & Delta Lake Integration Guide** | https://docs.aws.amazon.com/emr/latest/EMR-ReleaseGuide/emr-delta-lake.html | Provides the IAM policy snippets for Delta on E

---

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

---

# Unity Catalog & Governance  

*Section 10 of 15 – AWS Databricks Data Engineer Certification*  

> **Goal of this section** – Give you a complete mental model of Unity Catalog (UC) and the governance primitives that sit on top of it, show how they map to AWS services, and walk you through the exact operations you’ll be asked to perform on the exam. By the end you should be able to design a secure, multi‑tenant data platform, explain the data‑access flow, and write the few lines of code that a data engineer would use in production.

---  

## Overview  

Unity Catalog (UC) is Databricks’ unified, cross‑workspace data catalog that replaces the older Hive metastore. It provides **centralized metadata, fine‑grained access control, data masking, row‑level security (RLS), and lineage** for all data assets—tables, views, functions, and ML models—regardless of whether those assets live in Delta Lake on S3, external Glue tables, or Azure/Google clouds.  

In the AWS context, UC is tightly coupled with **S3** for storage, **IAM** for identity, **AWS Glue** for crawlers and schema inference, and **Lake Formation** for additional fine‑grained column‑level permissions (when enabled). The UC metastore stores its own JSON‑backed catalog in S3, replicated across regions, and is itself version‑controlled via **Databricks Repos** or external Git.  

A governance layer built on top of UC consists of three pillars:  

1. **Catalog‑Schema‑Table hierarchy** – You create *catalogs* (top‑level containers), *schemas* (namespaces), and *tables* (the actual data). This hierarchy mirrors AWS’s Organizational Units → Accounts → Resources but is expressed in SQL/Databricks UI.  
2. **Privilege model** – UC implements **SQL‑standard GRANT/REVOKE** for *SELECT, INSERT, UPDATE, DELETE, ALTER, USAGE, etc.* at catalog, schema, and table levels, plus **data‑masking policies** and **row‑level security policies** that can reference UDFs or AWS Secrets Manager.  
3. **Auditing & lineage** – Every access attempt is emitted to **CloudTrail** (via the Databricks service‑linked role) and to **Databricks Unity Catalog audit logs**. UC also captures table and query lineage that can be visualized in the UI or exported to AWS Athena for further analysis.  

Together, these capabilities let a data engineer enforce **multi‑tenant isolation**, **data classification**, and **compliance (GDPR, HIPAA)** while still giving data scientists a seamless Spark API to read/write data using the familiar `spark.read.table("catalog.schema.table")` pattern.

---

## Core Concepts  

Below are the building blocks you need to master. Each concept includes practical notes that map directly to exam‑style questions.

### 1️⃣ Catalogs, Schemas, and Tables  

| Level | Purpose | Typical AWS Mapping |
|-------|---------|---------------------|
| **Catalog** | Logical container for a business domain or regulatory scope (e.g., `finance`, `marketing`). Holds schemas and tables. | Equivalent to an AWS Organizational Unit (OU) or an AWS account. |
| **Schema** | Namespace within a catalog (e.g., `raw`, `curated`, `analytics`). Can hold versioned tables. | Similar to a Glue Database or a Lake Formation data lake zone. |
| **Table / View** | Physical Delta table (`USING DELTA`) or external view (e.g., a Hive table, a Glue table). | Stored as Delta Lake files in a specific S3 prefix, e.g., `s3://my-bucket/curated/events/`. |

*Key Exam Fact:* The exam often asks you to **choose the minimal set of UC objects** that can satisfy a given security requirement (e.g., “grant read‑only to a subset of columns”). Knowing that you must create a **catalog** *only* if you need to isolate data across business units, and **schemas** for domain‑level segregation, will save you time.

### 2️⃣ Privileges and Permission Types  

| Privilege | Scope | Example Use |
|-----------|-------|-------------|
| `USAGE` | Catalog → Allows navigating down to schemas. | `GRANT USAGE ON CATALOG finance TO data_engineer;` |
| `SELECT` | Table / View → Reads data. | `GRANT SELECT ON TABLE finance.events TO analyst;` |
| `INSERT` / `DELETE` | Table → Write operations. | `GRANT INSERT, DELETE ON TABLE finance.events TO ingestion_pipeline;` |
| `ALTER` | Table → Change schema (add columns, rename). | `GRANT ALTER ON TABLE finance.events TO admin;` |
| `CREATE` | Catalog / Schema → Ability to create sub‑objects. | `GRANT CREATE ON CATALOG finance TO data_engineer;` |

*Data Masking*: A **masking policy** can be attached to a column (e.g., SSN). The policy evaluates at query time and replaces sensitive values with a placeholder (`xxxx-xx-`).  

*Row‑Level Security*: Defined via a **RLS policy** that references a Spark UDF or a SQL function returning a boolean. Example: `SELECT * FROM finance.events WHERE region = current_user_region();`

### 3️⃣ Integration with AWS Glue & Lake Formation  

* **Glue Crawlers → UC**: When you run a Glue crawler against an S3 prefix that is *already* registered as a UC location, the crawler will *not* overwrite the metastore; it will instead **log warnings** and you can manually sync the metadata.  

* **Lake Formation**: If you enable *Lake Formation permissions* on a UC location, any table registered in UC inherits the **column‑level LF permissions**. The benefit is you can use LF’s *grant* API to define column permissions for external tables, and UC will enforce those when the table is accessed through Spark.  

* **IAM → Databricks Service‑Linked Role**: UC uses a service‑linked role (`databricks-unity-catalog`) that must have `s3:ListBucket`, `s3:GetObject`, and `glue:*` permissions on the S3 locations that store the catalog metadata. The exam may ask you to **list the minimal IAM policies** required for a UC metastore in a given VPC.

### 4️⃣ Auditing, Lineage, and Data Quality  

* **Audit Logs** – Sent to CloudTrail (event name `databricks.unityCatalog.*`). You can route them to a dedicated S3 bucket for long‑term retention and then run Athena queries to surface who accessed what.  

* **Lineage** – UC captures both **upstream** (source tables → downstream views) and **downstream** (queries that read a table). The lineage UI can be queried via `SELECT * FROM system.lineage WHERE table = 'finance.events';`.  

* **Data Quality Checks** – UC does **not** enforce schema evolution; you still need Delta’s `MERGE` and `CHECK CONSTRAINTS`. However, you can attach a **constraint** (`CREATE CONSTRAINT my_event_not_null ON finance.events (event_id) IS NOT NULL`) that will be enforced during writes.

---  

## Architecture / How It Works  

Below is a logical flow that illustrates where Unity Catalog lives relative to the rest of the AWS data platform.  

```mermaid
flowchart TD
    subgraph AWS[ AWS Account ]
        S3[ S3 Buckets<br/>raw/ & curated/ ]
        GLUE[ AWS Glue<br/>Crawler & Table Registry ]
        LF[ Lake Formation<br/>Data Permissions ]
        CT[ CloudTrail<br/>Audit Logs ]
    end

    subgraph Databricks[ Databricks Workspace ]
        UC[ Unity Catalog<br/>Metastore (S3 backed) ]
        CL[ Cluster (Spark) ]
        UI[ UI / Jobs / Repos ]
    end

    S3 -->|raw files| GLUE
    GLUE -->|crawls| UC
    LF -->|column/row LF grants| UC
    UC -->|metadata store| S3
    CL -->|spark.sql| UC
    CL -->|read/write Delta| S3
    UI -->|catalog operations| UC
    UC -->|audit events| CT

    classDef aws fill:#FFEECC,stroke:#333,stroke-width:1px;
    classDef dc fill:#CCE5FF,stroke:#333,stroke-width:1px;
    class S3,GLUE,LF,CT aws;
    class UC,CL,UI dc;
```

**Explanation of the diagram**

1. **Raw data lands in S3** → a Glue crawler discovers the schema. The crawler writes its metadata to UC (instead of the Glue Data Catalog).  
2. **Lake Formation policies** are attached to the UC location (e.g., `s3://my-bucket/curated/`). When a user runs a query, Databricks checks both the **UC privilege** and any **Lake Formation column masks**.  
3. **Clusters** talk to UC via the **HiveThriftCatalog** (the SQL layer). All read/write commands are translated into **Delta Lake** transactions that land in the S3 bucket.  
4. Every permission check and query is streamed to **CloudTrail** where the **Databricks service‑linked role** posts audit events. This creates an immutable trail for compliance.  

---  

## Hands‑On: Key Operations  

Below are the exact code snippets you would type in a Databricks notebook or a job to **create a catalog, grant permissions, and enforce masking/RLS**. Each block is accompanied by a brief “what’s happening” note.

> **Tip for the exam** – Most questions present a *scenario* and ask you to pick the *fewest* statements that accomplish the goal. Memorize the pattern: **`CREATE CATALOG …` → `CREATE SCHEMA …` → `CREATE TABLE …` → `GRANT SELECT …`** plus **masking / RLS** if required.

### 1️⃣ Create a Catalog, Schema, and External Table  

```python
# 1️⃣ Catalog
spark.sql("""
CREATE CATALOG IF NOT EXISTS finance
COMMENT 'Business unit for financial transactions';
""")

# 2️⃣ Schema inside the catalog
spark.sql("""
CREATE SCHEMA IF NOT EXISTS finance.raw
COMMENT 'Raw ingest tables (Parquet)';
""")

# 3️⃣ External table that points to a Glue‑registered location
spark.sql("""
CREATE DATABASE IF NOT EXISTS glue_db
""")  # This is just to reference a Glue table

spark.sql("""
CREATE TABLE IF NOT EXISTS finance.raw.events
USING PARQUET
LOCATION 's3://my-data-lake/raw/events/'
COMMENT 'Raw events as they land in S3';
""")

# Verify
spark.sql("DESCRIBE DETAIL finance.raw.events").show(truncate=False)
```

> **Why it matters** – The `LOCATION` is *catalog‑aware*. Even though the files live in S3, the table definition lives in UC, giving you immediate access‑control options.

### 2️⃣ Grant Privileges  

```sql
-- Grant read‑only to the analyst role
GRANT SELECT ON CATALOG finance TO `analyst_role`;

-- Allow the ingestion pipeline to write to the raw layer
GRANT INSERT, DELETE ON TABLE finance.raw.events TO `pipeline_role`;

-- Enable USAGE on the schema for the analyst
GRANT USAGE ON SCHEMA finance.raw TO `analyst_role`;
```

> **Exam note:** When a role needs *both* read and write on a table, you must also `GRANT USAGE` on the parent catalog and schema, otherwise the `SELECT` will be denied silently.

### 3️⃣ Attach a Data‑Masking Policy (SSN example)  

```sql
-- 1️⃣ Create a masking policy
CREATE MASKING POLICY IF NOT EXISTS finance.mask_ssn
  USING 'SELECT CASE WHEN is_current_user(''admin'') THEN ssn
           ELSE CONCAT(''xxx-xx-'', right(ssn,4))
       END' 
  COMMENT 'Masks SSN for non‑admin users';

-- 2️⃣ Apply it to the column
ALTER TABLE finance.raw.events
ALTER COLUMN ssn SET MASKING POLICY finance.mask_ssn;
```

Now a user without the `admin` role sees `xxx-xx-1234` instead of the real SSN.

### 4️⃣ Row‑Level Security (RLS) – Regional Isolation  

```sql
-- 1️⃣ UDF that returns the current user's allowed region
CREATE OR REPLACE TEMPORARY FUNCTION current_user_region() RETURNS STRING
  USING `com.mycompany.udfs.CurrentUserRegion`;

-- 2️⃣ RLS policy (referencing the UDF)
CREATE ROW FILTER ON finance.curated.events
  USING (current_user_region() = region);

-- 3️⃣ Grant to a role that already has SELECT
GRANT SELECT ON finance.curated.events TO `data_scientist`;
```

The RLS filter guarantees each user can only see rows whose `region` column matches the region resolved by the UDF (often derived from the user’s IAM principal via `CURRENT_USER()`).

### 5️⃣ Auditing a Query (via SQL)  

```sql
-- Run a query and then view the audit log via the Unity Catalog audit view
%sql
SELECT region, count(*) as events
FROM finance.curated.events
WHERE event_date = current_date()
GROUP BY region;

-- In a separate notebook (or via Athena) read the audit log:
spark.sql("""
SELECT *
FROM system.access_history
WHERE query_text like '%events%'
ORDER BY event_time DESC
LIMIT 10;
""")
```

---  

## AWS‑Specific Considerations  

| AWS Service | How it Touches Unity Catalog | Practical Tips for the Exam |
|-------------|-----------------------------|------------------------------|
| **S3** | UC stores its metastore JSON in a dedicated bucket (`s3://<account-id>-uc-meta/`). All Delta tables also read/write from S3. | Ensure the **Databricks service‑linked role** (`databricks-unity-catalog`) has `s3:GetObject` on the *catalog bucket* and *all data buckets* used by your tables. The role **cannot** have `s3:*` on the entire account – the exam may ask for the *least‑privilege* policy. |
| **IAM** | IAM users/groups are mapped to UC **roles** via the `GRANT` statements (e.g., `GRANT SELECT ON ... TO `john.doe``). The Databricks UI translates the `john.doe` string to a **Databricks identity** that ultimately resolves to an **IAM principal** via the service‑linked role. | Remember: **Cross‑account** UC works by setting up a *trust relationship* between the Databricks workspace in Account A and the S3 bucket in Account B. You need to attach the `databricks-unity-catalog` role to both accounts. |
| **AWS Glue** | Glue crawlers can **populate** UC if you run `CREATE EXTERNAL TABLE` that points to a Glue Data Catalog location. However, UC metadata is the **single source of truth**; any changes made in Glue (e.g., adding a new column) must be **propagated** manually via `ALTER TABLE`. | For the exam, you may be asked: “A new column is added to a Glue table. What steps are required for the table to be queryable through UC?” – Answer: **`REFRESH TABLE <catalog.schema.table>`** and optionally **`ALTER TABLE ... ADD COLUMNS …`** in UC. |
| **Lake Formation** | When you **grant LF permissions** to a UC location, those permissions are *enforced* on top of UC’s own privileges. LF column‑level grants are stored in the **Data Catalog** of Lake Formation, not UC. | The exam may present a scenario where a user can read a table but cannot see a specific column. You’ll need to state: **Grant LF column‑level SELECT** *and* verify that the user has the **table SELECT** in UC. |
| **EMR** | EMR clusters can mount a UC catalog via the **Spark `spark.databricks.unityCatalog.jdbc.enabled`** config. EMR also supports **IAM roles for EC2** that grant access to the UC metastore bucket. | If you’re building a **Hybrid** solution (Databricks on a VPC, EMR for batch), you’ll need **VPC endpoints** for `s3` and `sts` so the EMR cluster can fetch the UC metadata without leaving the network. |
| **CloudWatch / CloudTrail** | UC logs each `GRANT`/`REVOKE` and every `SELECT` attempt to CloudTrail.

---

## Workflows and Orchestration  

*The *Workflows and Orchestration* section is the “glue” that binds together the raw data ingestion, transformation, and analytics pipelines you will build on Databricks on AWS.  In this part of the course you will learn how to model complex data‑processing logic as *workflows*—a first‑class, declarative object in Databricks—that can be scheduled, versioned, and monitored with the same security and cost‑control guarantees you already know from AWS Glue.  You will leave this section able to design, implement, and troubleshoot end‑to‑end pipelines that meet the requirements of the **Databricks Certified Data Engineer Associate** exam.*  

---  

### Overview  

Data pipelines on a lakehouse are rarely linear.  In practice you will encounter:  

1. **Branching** – separate paths for raw‑to‑bronze, bronze‑to‑silver, and silver‑to‑gold transformations.  
2. **Parallelism** – multiple independent tasks (e.g., partitioning, back‑fills, ML model training) that must run concurrently.  
3. **Conditional execution** – run a downstream task only if a upstream task succeeded or only for certain date ranges.  
4. **Dynamic parameters** – pass the run date, a configuration file, or a version tag from an upstream system.  

Databricks **Workflows** (formerly “Jobs with tasks”) provide a native, UI‑driven, and API‑driven way to express exactly these patterns. A workflow is a directed acyclic graph (DAG) of *tasks*; each task can be a notebook, a Python script, an SQL query, or a Delta Live Tables (DLT) pipeline. The workflow engine takes care of:  

* **Task orchestration** – executing tasks in the correct order, respecting dependencies and retry policies.  
* **Cluster management** – provisioning a *job cluster* (or using an existing all‑purpose cluster) only for the duration of the task.  
* **Security** – attaching an IAM role to the job, using DBFS secrets, and enforcing Lake Formation table ACLs.  
* **Observability** – streaming task‑level logs to CloudWatch, exposing metrics to Databricks UI, and providing built‑in alerts for failure.  

From the exam perspective you must know *what* a workflow is, *how* it differs from a classic “job” (single notebook or JAR), and *when* you would choose a workflow over a DLT pipeline.  The diagram below shows a typical end‑to‑end pipeline that you could model as a workflow on Databricks.  

---  

### Core Concepts  

#### 1. Workflow Definition (`workflow.json`)  

* A JSON representation that lists tasks, dependencies, and schedules.  
* Supports version control via the Databricks REST API (`POST /api/2.1/jobs/workflows`).  

```json
{
  "name": "etl_sales_pipeline",
  "tasks": [
    {
      "task_key": "extract",
      "type": "NOTEBOOK",
      "notebook_path": "/Shared/ingest/sales_raw",
      "depends_on": []
    },
    {
      "task_key": "transform",
      "type": "SQL",
      "sql_file_path": "/Shared/transform/sales_transform.sql",
      "depends_on": ["extract"]
    },
    {
      "task_key": "load",
      "type": "NOTEBOOK",
      "notebook_path": "/Shared/load/sales_gold",
      "depends_on": ["transform"]
    }
  ],
  "schedule": { "quartz_cron_expression": "0 0 * * ? *" }
}
```

#### 2. Task Types  

| Type | Typical Use | Execution Context |
|------|-------------|-------------------|
| **NOTEBOOK** | Complex PySpark logic, incremental loads | Notebook server (Python, Scala, SQL) |
| **PYTHON** | Stand‑alone scripts, utility functions | Small job cluster (default `spark.databricks.cluster.profile = task`) |
| **SQL** | Declarative queries, view materializations | Uses existing clusters; supports SQL Warehouses |
| **DATAPROC** | External systems (S3, Glue, EMR) via `dbutils.fs` | Runs in the same cluster as the workflow job |
| **DYNAMIC** | Parameter‑driven branches (e.g., for each country) | Uses *parameterization* to create multiple tasks at runtime |

#### 3. Dependencies & Conditional Execution  

* `depends_on` – explicit upstream task list.  
* `on_success`, `on_failure` – optional listeners that can trigger another task or a *notebook* for alerting.  

```python
# Example of a conditional listener using the Jobs API
dbutils.jobs.submitTask(
    job_id = workflow_id,
    task_key = "notify",
    notebook_params = {"alert": "email", "topic": "sales_failed"},
    trigger_type = "ON_FAILURE"
)
```

#### 4. Parameterization  

Workflows can accept **parameter values** that are resolved at run time. This is essential for back‑fills, environment‑specific configs, or date‑based logic.  

```json
{
  "tasks": [
    {
      "task_key": "incremental_load",
      "type": "NOTEBOOK",
      "notebook_path": "/Shared/load/incremental",
      "depends_on": [],
      "parameters": {
        "source_path": "/mnt/raw/sales/{{run_date}}/",
        "target_table": "bronze.sales"
      }
    }
  ],
  "run_id": 12345,
  "run_date": "2024-10-15"
}
```

*When the workflow is invoked with `{{run_date}}` resolved to `2024-10-15`, the notebook sees the exact S3 path for that day.*  

#### 5. Monitoring & Alerting  

* **Databricks UI** – DAG view, task statuses, and per‑task logs.  
* **CloudWatch Logs** – Each job cluster writes a `AWSLogs/<account-id>/databricks/jobs/<workflow-name>` log stream.  
* **Event‑Bridge Integration** – Emit a `DatabricksJobSucceeded` or `DatabricksJobFailed` event to trigger SNS or Step Functions.  

---  

### Architecture / How It Works  

Below is a **high‑level architecture** of a typical ETL workflow that moves data from an S3 landing zone to a Delta Lake gold table.  The diagram uses Mermaid syntax (supported in the Databricks notebook UI and Markdown viewers).  

```mermaid
graph TD
    A[Raw S3 Bucket] -->|S3 Event| B[Auto Loader (Delta Live Table)]
    B -->|Writes to /bronze| C[Bronze Delta Table (S3)]
    C -->|Spark SQL / Notebook| D[Transform Task (WorkFlow Task #1)]
    D -->|Writes to /silver| E[Silver Delta Table (S3)]
    E -->|DBT or Notebook| F[Gold Delta Table (Lake Formation)
    F -->|BI Tools| G[Analytics Dashboard]
    D -->|Optional| H[Alert Notebook (on_failure)]
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style G fill:#9f9,stroke:#333,stroke-width:2px
```  

**Explanation of the flow:**  

1. **Auto Loader** runs continuously on the *raw* S3 bucket and produces incremental Delta files in the bronze zone.  
2. A **Workflows task** (`bronze_to_silver`) reads the bronze Delta table, performs a transformation using Spark SQL, and writes to a silver Delta table.  
3. Another **Workflows task** (`silver_to_gold`) joins the silver table with reference data (stored in an EMR Hive metastore) and materializes the gold table under Lake Formation governance.  
4. Success logs flow to **CloudWatch**, while failure triggers a separate notebook that sends a Slack message.  

---  

### Hands-On: Key Operations  

Below is a **step‑by‑step notebook** that you can copy into a Databricks workspace and run end‑to‑end.  The example creates a simple workflow that extracts a CSV from S3, transforms it with PySpark, and loads the result into a Delta table.  

> **Prerequisites** – You must have:  
> * An S3 bucket `s3://my-data-lake/raw/` accessible from a DBFS mount.  
> * An IAM role `arn:aws:iam::<acct-id>:role/databricks-workflow-role` attached to the cluster with `s3:*`, `logs:*`, and `glue:*` permissions.  
> * A cluster with the `spark.databricks.cluster.profile` set to `task` for job clusters.  

#### Step 1 – Mount the S3 bucket (once per workspace)  

```python
# DBFS mount point: /mnt/raw-data
configs = {"fs.s3a.aws.credentials.provider": "com.amazonaws.auth.InstanceProfileCredentialsProvider"}
spark.conf.set("fs.s3a.mount.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
dbutils.fs.mount(
  source = "s3://my-data-lake",
  mount_point = "/mnt/raw-data",
  extra_configs = configs
)
```

#### Step 2 – Define the three tasks as notebooks  

| Task | Path (relative to workspace) | Language |
|------|-------------------------------|----------|
| `extract` | `/Shared/etl/extract_sales` | Python |
| `transform` | `/Shared/etl/transform_sales` | SQL |
| `load` | `/Shared/etl/load_sales` | Python |

> *Tip for the exam:* The **task key** in the workflow JSON must match the *actual* path used here (e.g., `extract` → `/Shared/etl/extract_sales`).  

#### Step 3 – Create the workflow via the REST API  

```bash
# Save the workflow definition locally (workflow_def.json)
cat > workflow_def.json <<'EOF'
{
  "name": "sales_etl_workflow",
  "tasks": [
    {
      "task_key": "extract",
      "type": "NOTEBOOK",
      "notebook_path": "/Shared/etl/extract_sales",
      "depends_on": []
    },
    {
      "task_key": "transform",
      "type": "SQL",
      "sql_file_path": "/Shared/etl/transform_sales.sql",
      "depends_on": ["extract"]
    },
    {
      "task_key": "load",
      "type": "NOTEBOOK",
      "notebook_path": "/Shared/etl/load_sales",
      "depends_on": ["transform"]
    }
  ],
  "schedule": { "quartz_cron_expression": "0 30 2 * * ? *" },
  "aws_iam_role": "arn:aws:iam::123456789012:role/databricks-workflow-role"
}
EOF
```

```python
import requests, json, os, base64

# Parameters
HOST = "https://<databricks-instance>.cloud.databricks.com"
TOKEN = dbutils.secrets.get(scope="databricks", key="personal-token")
WORKFLOW_NAME = "sales_etl_workflow"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# POST the workflow
resp = requests.post(
    f"{HOST}/api/2.1/jobs/workflows/create",
    headers=HEADERS,
    data=json.dumps({"definition": json.load(open("workflow_def.json"))})
)

print("Workflow creation response:", resp.json())
```

#### Step 4 – Trigger a run (manually for demo)  

```python
payload = {"run_name": "sales_etl_run_20241015"}
resp = requests.post(
    f"{HOST}/api/2.1/jobs/workflows/runs/submit",
    headers=HEADERS,
    json={"name": "sales_etl_workflow", "run_name": "sales_etl_run_20241015"}
)
run_id = resp.json()["run_id"]
print("Submitted run ID:", run_id)
```

#### Step 5 – Inspect the run  

```python
import time
run = requests.get(
    f"{HOST}/api/2.1/jobs/workflows/runs/get?run_id={run_id}",
    headers=HEADERS
).json()

while run["state"]["life_cycle_state"] not in ("TERMINATED", "SKIPPED", "INTERNAL_ERROR"):
    time.sleep(5)
    run = requests.get(
        f"{HOST}/api/2.1/jobs/workflows/runs/get?run_id={run_id}",
        headers=HEADERS
    ).json()

print("Final state:", run["state"]["life_cycle_state"])
print("Task statuses:")
for t in run["tasks_status"]:
    print(f"  {t['task_key']}: {t['result_state']}")
```

**What you should see**  

| Task | Result State | Typical Logs |
|------|--------------|--------------|
| `extract` | `SUCCESS` | Writes to `/mnt/raw-data/processed/sales/` |
| `transform` | `SUCCESS` | Executes `SELECT * FROM bronze.sales` and creates `silver.sales` |
| `load` | `SUCCESS` | Writes to Delta gold table `gold.sales` |

You can view **individual task logs** from the *Run* UI, and the **overall workflow run** appears in CloudWatch under `/aws/databricks/jobs/sales_etl_workflow`.  

---  

### AWS‑Specific Considerations  

| AWS Component | How it Interacts with Workflows | Gotchas / Best Practices |
|---------------|----------------------------------|---------------------------|
| **S3** | Source and sink for raw/transformed data. Use *S3A* with *Instance Profile* credentials for seamless access from job clusters. | - Enable **S3 Transfer Acceleration** for large parallel writes. <br> - Set **Lifecycle policies** on bronze/silver buckets to transition older data to Glacier. |
| **IAM Role** (`databricks-workflow-role`) | Attached to each *job cluster* at task runtime. Grants `s3:*`, `glue:*`, `logs:*`, `cloudwatch:*`. | - Use **least‑privilege**: restrict `s3:*` to the specific bucket prefixes used by the workflow. <br> - Rotate the role via **AWS IAM Ops** or **Service Catalog** for compliance. |
| **Glue Data Catalog** | Source tables for SQL tasks, and target tables for Delta (via `spark.sql("REFRESH TABLE")`). | - Enable **Lake Formation** permissions on the catalog so the workflow role can `SELECT` and `INSERT`. <br> - Ensure **Table versioning** (`spark.databricks.delta.retentionDurationCheck.enabled = false`) if you need to back‑fill. |
| **EMR (for Delta Live Tables)** | Some DLT pipelines still require an *EMR* under‑the‑hood. The workflow can *trigger* a DLT pipeline that runs on EMR. | - Pin EMR version (`emr-6.12.0`) to guarantee the same Spark version as your workspace. |
| **Lake Formation** | Provides fine‑grained table ACLs. The workflow’s IAM role must have a *Lake Formation* principal mapping. | - After adding a new table to the gold zone, **grant** `SELECT` to the workflow role *before* the load task runs. |
| **CloudWatch** | Captures stdout/stderr, task metrics, and job run lifecycle events. | - Create a **Metric Filter** on `*failed*` log patterns to push to an SNS topic for on‑call alerts. |
| **Step Functions (optional)** | You can embed a Databricks Workflows task as a *Callback* state to orchestrate long‑running ML experiments. | - Keep the state machine **idempotent**; store intermediate results in S3 for replay. |

#### IAM Example Policy Snippet (for `databricks-workflow-role`)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3ReadWrite",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3

---

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

---

## Advanced Delta Optimization  

*(Section 13 of 15 – AWS Databricks Data Engineer Certification)*  

---

### Overview  

Delta Lake is the backbone of reliable, performant data lakehouses on AWS. While its **ACID transactions**, **schema enforcement**, and **time travel** capabilities make it safe for batch and streaming workloads, raw Parquet files stored in S3 can quickly become a performance bottleneck when millions of files are being written, queried, or compacted.  

*Advanced Delta Optimization* dives into the **why** and **how** of the optimization primitives that transform a chaotic lake into a query‑efficient one. You will learn to balance **file consolidation**, **data skipping**, and **concurrency control** while keeping in mind the economics of AWS S3 storage and the integration points with **AWS Glue**, **EMR**, and **Lake Formation**.  

* By the end of this section you should understand:  

  1. **Core optimization operations** (`OPTIMIZE`, `ZORDER BY`, `VACUUM`, `OPTIMIZE WRITE`) and when each is the right tool.  
  2. **Transaction log mechanics** (checkpointing, commit protocol, and conflict resolution).  
  3. **How to tune Delta Lake settings** for the AWS environment (e.g., `spark.databricks.delta.optimizeWrite.enabled` and `spark.databricks.delta.autoCompact.enabled`).  
  4. **Operational monitoring** with CloudWatch and Glue job metrics.  

*You will be able to explain, demonstrate, and troubleshoot these concepts both in a live notebook and on the Databricks Data Engineer Associate exam.*  

---

### Core Concepts  

| Concept | Why It Matters | Key Settings & API | Typical Use‑Case |
|---------|----------------|--------------------|-----------------|
| **`OPTIMIZE`** (Z‑order aware) | Merges small files, compacts data files, and rewrites the transaction log for faster reads. | `OPTIMIZE table_path [ZORDER BY (col1, col2)]` <br> `spark.databricks.delta.optimizeWrite.enabled = true` | Periodic nightly compaction of a large fact table. |
| **Z‑Ordering** | Orders data within files by the most‑filtered columns, enabling **data skipping** at the file level. | `OPTIMIZE ... ZORDER BY (date, customer_id)` <br> `spark.databricks.delta.zOrderingKeyCount = 2` | Queries filtering on `event_date` and `region_id`. |
| **Auto Compaction** | Continuously merges partially‑filled files that arise from high‑velocity streaming writes. | `spark.databricks.delta.autoCompact.enabled = true` <br> `spark.databricks.delta.autoCompact.maxFileSize = 128MB` | Low‑latency dashboards that ingest change‑data‑capture (CDC) streams. |
| **VACUUM** | Removes stale files after a retention window, preventing storage bloat while preserving time‑travel. | `VACUUM table_path RETAIN 168 HOURS` <br> `spark.databricks.delta.retentionDurationCheck.enabled = false` (optional, exam‑relevant) | Deleting old versioned files in a production table. |
| **Commit Protocol & Conflict Resolution** | Guarantees ACID semantics; understanding it prevents “lost updates” when multiple writers target the same table. | `DeltaTable.forPath(spark, path).generate` <br> `spark.databricks.delta.signal.maxActiveTriggeringTasks` (for streaming) | Coordinating incremental loads from multiple EMR clusters. |
| **Data Skipping (Bloom filters, column stats)** | Allows the query engine to prune files early, dramatically reducing I/O. | `spark.databricks.delta.columnStats.enabled = true` <br> `spark.databricks.delta.bloomFilterColumns` | Selecting a single column from a table with millions of partitions. |
| **`OPTIMIZE WRITE` (continuous compaction)** | Writes in a streaming setting that auto‑optimizes micro‑batches without explicit `OPTIMIZE`. | `spark.databricks.delta.optimizeWrite.enabled = true` <br> `spark.databricks.delta.retentionDurationCheck.enabled = true` | Real‑time ingest pipelines that require sub‑minute query latency. |

#### Deep Dives  

1. **File Consolidation vs. Z‑Ordering**  
   - *File consolidation* is about reducing the number of objects in S3. Small files (<128 KB) cause high request costs and metadata bloat.  
   - *Z‑ordering* works on the *granularity of files*; it does not change file count but improves pruning. A well‑optimized table may still have 500 K files if Z‑ordering is not applied to the most selective columns.  

2. **Auto Compaction vs. Manual `OPTIMIZE`**  
   - Auto compaction runs *continuously* and is ideal for streaming pipelines with *micro‑batch* size ≤ 100 MB.  
   - Manual `OPTIMIZE` is recommended for *batch jobs* or when you need deterministic control (e.g., run after a full nightly load).  

3. **Retention, Vacuum, and Time‑Travel**  
   - The default retention period in Delta on AWS is **7 days** (configurable). If you need to keep older versions for compliance, you may temporarily disable the retention check (`spark.databricks.delta.retentionDurationCheck.enabled = false`)—a **exam trap** to watch.  

4. **Spark Configuration Levers**  
   - `spark.databricks.delta.retentionDurationCheck.enabled` – toggles the 7‑day check during `VACUUM`.  
   - `spark.databricks.delta.maxFileSize` – controls the target size of newly written Parquet files; default 1 GB, often lowered to 256 MB for faster reads.  

---

### Architecture / How It Works  

Below is a simplified **data‑flow diagram** that shows where Delta optimization primitives sit in a typical AWS Lakehouse pipeline.  

```mermaid
flowchart LR
    subgraph Raw Ingestion
        S3[Raw S3 Bucket] -->|Kinesis / Firehose| AL[Auto Loader (Delta)] 
    end

    subgraph Delta Lake
        AL -->|writes| DELTATABLE[Delta Table (S3)]
        DELTATABLE -->|OPTIMIZE| OPT[Compaction Service]
        DELTATABLE -->|ZORDER| ZORDER[Z‑order Writer]
        ZORDER -->|writes| ZORDERED[Delta Table (Optimized)]
        ZORDERED -->|queries| Q[Databricks SQL / Notebook]
    end

    subgraph AWS Services
        IAM[IAM Role] -->|access| S3
        EMR[EMR Cluster] -->|Spark jobs| Q
        Glue[Glue Catalog] <--> DELTATABLE
    end

    style S3 fill:#f9f,stroke:#333,stroke-width:1px
    style DELTATABLE fill:#bbf,stroke:#333,stroke-width:1px
    style ZORDERED fill:#bfb,stroke:#333,stroke-width:1px
```

**Explanation of the diagram**

1. **Raw data lands in S3** and is captured by **Auto Loader** (streaming) or a **batch copy** (EMR).  
2. Auto Loader writes *raw Parquet* files to the **Delta table path**.  
3. **Auto‑Optimize** (`spark.databricks.delta.optimizeWrite.enabled`) can trigger a *continuous merge* while the write stream runs, producing *small files* that are later *auto‑compacted*.  
4. Periodic **manual `OPTIMIZE`** tasks, possibly orchestrated by **AWS Step Functions**, invoke **Z‑ordering** to reorder data files based on hot filters.  
5. The final **optimized table** feeds downstream analytics via Databricks SQL, JDBC, or external BI tools.  
6. **Glue Catalog** is updated automatically via Delta’s **transaction log**, while **IAM** provides fine‑grained S3 access control.  

---

### Hands-On: Key Operations  

> **Prerequisites** – A Databricks workspace on AWS with a **Delta table** already created (`my_db.fact_sales`) and an **IAM role** with `s3:ListBucket`, `s3:GetObject`, `s3:PutObject` for the bucket `s3://my-data-lake`.  

#### 1️⃣ Write a streaming micro‑batch and enable auto‑optimize  

```python
# Configure Spark for Delta Optimize Write
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.maxFileSize", "256MB")  # smaller files -> more frequent compactions

# Load CDC events from Kinesis → Delta (using Auto Loader)
(df_stream = spark.readStream.format("cloudinary")
                               .option("cloudinary.format.cloud", "kinesis")
                               .option("cloudinary.kinesis.stream", "sales-cdc")
                               .load()
                               .selectExpr("*", "to_timestamp(event_timestamp) as event_ts"))

# Write to Delta table with partitioning by event_date (derived column)
(write_q = df_stream.writeStream.format("delta")
                               .option("checkpointLocation", "s3://my-data-lake/checkpoints/sales_cdc")
                               .outputMode("append")
                               .partitionBy("event_date")  # Z‑order will be applied later
                               .table("my_db.fact_sales_tmp"))
```

*Explanation* – Auto Loader writes *immutable* micro‑batches. With `optimizeWrite` enabled, each micro‑batch is **auto‑compacted** as soon as the file size crosses 256 MB, preventing the “small‑file” problem.

#### 2️⃣ Perform a batch `OPTIMIZE` with Z‑ordering  

```sql
-- Run this in a Databricks notebook cell (SQL)
OPTIMIZE my_db.fact_sales
  ZORDER BY (event_date, product_id);
```

*Result* – Delta will merge all Parquet files under `my_db.fact_sales` into larger files (default `maxFileSize` of 1 GB) and internally reorder the data to place `event_date` and `product_id` close to the file header, enabling **column‑level skipping**.

#### 3️⃣ Verify file statistics & data skipping  

```python
# Verify that file stats are collected and that pruning will work
spark.sql("DESCRIBE DETAIL my_db.fact_sales").show()
```

*Typical output*  

| file_count | data_skipped | min(event_date) | max(event_date) |
|------------|--------------|-----------------|-----------------|
| 15,247     | 12.8 GB      | 2022-01-01      | 2024-12-01      |

The `min` / `max` columns are stored in the Delta **statistics** and are consulted by the query optimizer.

#### 4️⃣ Manual `VACUUM` after a data retention window  

```python
# Delete all versions older than 14 days (336 hours)
spark.sql("VACUUM my_db.fact_sales RETAIN 336 HOURS")
```

*Caution* – If you are testing on a production table, ensure you have **no active streaming write** (use `spark.databricks.delta.retentionDurationCheck.enabled = false` only for troubleshooting, not in production code).

#### 5️⃣ Enable Bloom filters for a heavily filtered column  

```python
# Add a Bloom filter on transaction_id (high cardinality, low cardinality per file)
spark.sql("""
  ALTER TABLE my_db.fact_sales
  SET TBLPROPERTIES (
    delta.columnMapping.mode = 'name',
    delta.bloomFilterColumns = 'transaction_id'
  )
""")
```

Now any query that filters on `transaction_id` can prune **up to 95 %** of files based on the Bloom filter.

---

### AWS‑Specific Considerations  

| AWS Service | Interaction with Delta Optimization | Practical Tips for the Exam |
|-------------|--------------------------------------|------------------------------|
| **S3 (Standard / Intelligent‑Tiering)** | All Delta files reside here; file size directly influences **GET/PUT request costs**. | *Target 256–512 MB Parquet files* for most analytics; *enable S3 Intelligent‑Tiering* to offload infrequently accessed files. |
| **IAM Roles & Policies** | Auto Loader, EMR, and Glue need `s3:*` on the lake bucket **plus** `glue:*` for catalog updates. | *Least‑privilege*: `s3:PutObject` only on `s3://my-data-lake/*`, `s3:GetObjectVersion` for time‑travel checks. |
| **AWS Glue Data Catalog** | Delta tables automatically register in the catalog via `spark.sql("CREATE TABLE ...")` using the catalog. | *Keep the catalog in sync*: set `spark.databricks.delta.inferPartitionColumns.enabled = true`. |
| **AWS Lake Formation** | Can enforce **LF-Tag‑Based access** on a Delta table, limiting which IAM principals see which partitions. | *Exam tip*: know how to enable a **Lake Formation tag** on a Delta table and reference it in a query with `WHERE collection = 'finance'`. |
| **EMR on EKS / Managed Spark** | Delta optimizations must be configured via **cluster spark-defaults.conf** (e.g., `spark.databricks.delta.optimizeWrite.enabled`). | *Remember to set the config at cluster launch; otherwise `OPTIMIZE` will be a no‑op*. |
| **CloudWatch / Databricks Metrics** | Metrics like `DeltaTableOptimizer` and `DeltaCompactionJob` are exposed through the **Databricks Metrics** integration. | *Watch for “Failed to compact files” errors in CloudWatch logs – often due to insufficient S3 permissions.* |
| **AWS Step Functions (or Glue Scheduler)** | Orchestrate nightly `OPTIMIZE` jobs that run after the EMR batch load finishes. | *Exam scenario*: “You have a daily load at 02:00 AM. Which scheduled API should you use to ensure the table is optimized before the 08:00 AM dashboard runs?” – Answer: **Step Functions** with a *wait state* after the Glue job completes. |

**AWS‑only gotchas**  

1. **S3 Request Rate Limits** – A burst of many small files can trigger **5,500 PUT/LIST requests per second** per prefix. If you observe “TooManyRequests” errors in the notebook, you need to enable **auto‑compact** or increase the `maxFileSize`.  
2. **Glue Table Partition Projection** – Delta can infer partition columns on the fly, but for fast pruning you should **register the partitions in Glue** using `MSCK REPAIR` or `ALTER TABLE ADD PARTITION`.  
3. **Lake Formation “Enforced Tables”** – If a table is *enforced* in Lake Formation, `VACUUM` will fail unless the IAM role also has `lakeformation:UpdateTable`.  

---

### Exam Focus Areas  

- **Conceptual:**  
  - Difference between *auto‑optimize* (continuous) and *batch `OPTIMIZE`* (deterministic).  
  - How *Z‑ordering* creates *data skipping* and why it matters for columnar queries.  
  - The role of **transaction log checkpoints** in conflict resolution and why you *must* run `VACUUM` before deleting older files.  

- **Practical (hands‑on):**  
  - Write a `spark.sql("OPTIMIZE … ZORDER BY (…)")` statement and explain the underlying file rewrite steps.  
  - Configure the following Spark settings to enable **auto‑compact** for a streaming job (show the three `conf.set` lines).  
  -

---

## Testing, Debugging, and Monitoring  

*Section 14 of 15 – AWS Databricks Data Engineer Certification*  

---  

### Overview  

Testing, debugging, and monitoring are the three pillars that turn a **working Spark job** into a **reliable production pipeline**. In the context of Databricks on AWS, these pillars are tightly coupled with the collaborative notebook environment, the unified data platform (Delta Lake, Auto Loader, Unity Catalog), and the underlying AWS services (S3, IAM, Glue, CloudWatch, etc.).  

* **Testing** is not an after‑thought; it is a **shift‑left** practice baked into notebooks via unit‑style tests for transforms, schema validation, and data quality checks that run on every commit.  
* **Debugging** in a distributed environment goes beyond “print statements.” It requires understanding the **execution plan**, the **spark UI**, the **executor logs**, and the **event logs** that tie Spark tasks to underlying AWS resources.  
* **Monitoring** is the continuous loop that feeds telemetry back into the system. It includes **metrics (CPU, memory, I/O), logs (driver and executor), traces (S3 request IDs, Glue catalog changes), and alerts** that let you spot performance regressions, data drift, or security incidents before they impact downstream consumers.  

For the **Databricks Certified Data Engineer Associate** exam, you’ll be expected to design, implement, and troubleshoot a complete end‑to‑end workflow that includes a Delta table loaded by Auto Loader, a downstream enrichment job, and a set of data‑quality assertions. The exam also tests whether you can **instrument the pipeline** using Databricks REST APIs, Jobs UI, and CloudWatch, and **configure IAM/SCIM permissions** so that only the right users can read or write data.

---

### Core Concepts  

| Concept | Why it matters | Typical Tools / APIs | How it maps to AWS |
|---------|----------------|----------------------|--------------------|
| **Unit Testing (UT) of transforms** | Catches logical errors before data is written to lake. | `unittest`, `pytest`, `spark-testing-base`, `DeltaTable.assert()` | Run UT in a CI pipeline (CodeBuild) that spins up a **temporary EMR cluster** or **Databricks “dbfs:/tmp”** workspace. |
| **Integration / End‑to‑End (E2E) testing** | Validates the whole data flow, schema evolution, and streaming semantics. | `pytest` + Spark Structured Streaming `awaitTermination`, `Databricks Jobs API` | Use **S3 versioned buckets** as source & sink; verify that S3 event notifications trigger the correct jobs. |
| **Debugging (local & remote)** | Identifies why a job fails, stalls, or produces bad results. | `spark.debug()`, `sparkContext.setLogLevel("DEBUG")`, **Databricks Debugger**, **Spark UI**, **S3 Access Logs** | Leverage **CloudWatch Logs Insights** on `spark.driver` and `spark.executor` logs; trace a failing S3 request using **AWS X‑Ray** if you have instrumentation. |
| **Job Scheduling & Parameterization** | Enables reproducible runs and safe rollouts. | **Databricks Jobs**, **Job Clusters**, **Job Parameters**, **Jobs UI**, `dbutils.jobs.runNow` | Schedule a job that **writes a checkpoint** to a versioned S3 prefix; enable **Job Run That Triggers Another Job** (DBX) for multi‑step pipelines. |
| **Observability (Metrics, Logs, Traces)** | Provides the data needed for SLA reporting & root‑cause analysis. | **Databricks Metrics**, **EventBridge**, **CloudWatch**, **Grafana**, **OpenTelemetry** | Export `spark.executor.metrics` to CloudWatch; set up **CloudWatch Alarms** on `JobRunTime` and `DataSkew` metrics. |
| **Data Quality & Governance** | Guarantees that downstream consumers receive trustworthy data. | **Delta Expectation**, **Data Quality Checks (DQ) UI**, **Unity Catalog policies**, **Lake Formation** | Enforce **column-level ACLs** in Unity Catalog; use **Lake Formation tag‑based policies** for PII masking. |

#### Sub‑sections  

1. **Unit‑Test Framework for Notebooks** – how to import notebooks as modules, use `spark-testing-base`, and assert schema evolution.  
2. **Spark Structured Streaming Checkpoints** – why you need deterministic checkpoints, idempotent offsets, and handling of **late data** with `watermark`.  
3. **Debugging with the Databricks Debugger** – step‑through debugging of a streaming job, live variable inspection, and attaching to an **EMR‑based job cluster**.  
4. **Monitoring with the Built‑in Metrics Dashboard** – customizing the **Jobs > Metrics** view, creating **Dashboard panels** for executor memory, input rate, and **spark.scheduler.taskMetrics**.  
5. **Alerting & Incident Response** – CloudWatch Alarms, SNS topics, and the **Databricks Incident Command System (DICS) playbook**.  

---

### Architecture / How It Works  

Below is a **high‑level data‑pipeline architecture** that integrates the three observability pillars. The diagram is expressed in Mermaid syntax so it can be rendered directly in the Udemy viewer.

```mermaid
graph TD
    subgraph Source (AWS)
        A[Raw S3 Bucket (raw/) ] -->|S3 Event| B[Auto Loader (Databricks Streaming)]
    end
    subgraph Processing (Databricks)
        B --> C[Delta Lake Table (gold/)]
        C --> D[SQL Enrichment Job (Job Cluster)]
        D --> E[Analytics Dashboard (QuickSight)]
    end
    subgraph Observability
        B --> F[Databricks REST / Job API]
        C --> G[Delta Expectation (Data Quality)]
        D --> H[Spark UI + Structured Streaming UI]
        H --> I[CloudWatch Logs (Executor/Driver)]
        C --> J[Metrics Export (Prometheus + Grafana)]
        F --> K[EventBridge → SNS → PagerDuty]
    end
    style Source fill:#f9f9f9,stroke:#333,stroke-width:1px
    style Processing fill:#e6f7ff,stroke:#0077b6,stroke-width:2px
    style Observability fill:#fff3e0,stroke:#ff9800,stroke-width:2px
```

**Explanation of the flow**

* **Raw S3 bucket** receives files in *real time* (e.g., IoT sensor payloads). An **S3 PUT** triggers a **S3 Event** that Auto Loader consumes *asynchronously* (triggered by the **EventBridge** rule that creates a **job run**).  
* **Auto Loader** writes to a **Delta table** using the *bronze* layer, with **schema inference** and **checkpointing** to a dedicated S3 prefix.  
* A downstream **SQL enrichment job** runs on a **Job Cluster** that reads the bronze layer, performs look‑ups from a **Glue Data Catalog**, and writes the *gold* table.  
* Throughout the pipeline, **metrics**, **logs**, and **trace IDs** are emitted to **CloudWatch**. A **CloudWatch Alarm** on the *latency* metric (`spark.sql.streaming.lastProgress` > 5 min) fires an SNS notification, which can invoke a **re‑run** via the **Databricks Jobs API**.  

---

### Hands-On: Key Operations  

Below are **self‑contained code snippets** you can copy into a Databricks notebook. Each block is annotated to explain the purpose and the observability hook.

#### 1. Unit‑test a Transform (PyTest + Spark‑Testing‑Base)

```python
# file: test_transforms.py
import unittest
from pyspark.sql import SparkSession
from delta.tables import DeltaTable
from pyspark.sql.functions import col, when, lit

# -------------------------------------------------
# Spark session with a deterministic metastore
# -------------------------------------------------
@pytest.fixture(scope="module")
def spark():
    spark = (
        SparkSession.builder
        .appName("unit-test")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "2")
        .config("spark.databricks.delta.retentionDurationCheck.enabled", "false")
        .getOrCreate()
    )
    yield spark
    spark.stop()

class TestCustomerTransform(unittest.TestCase):
    def setUp(self, spark):
        data = [
            (1, "US", 25, "2024-10-01"),
            (2, "CA", 40, None),
            (3, "US", -5, "2024-09-30")
        ]
        self.df = spark.createDataFrame(data, ["id", "country", "age", "date"])

    def test_age_validation(self, spark):
        # Transform: keep rows where age >= 0 and date is not null
        transformed = (
            self.df.filter(col("age") >= 0)
            .filter(col("date").isNotNull())
            .withColumn("age_group", when(col("age") < 18, "minor").otherwise("adult"))
        )
        # Convert to Delta for schema assertions
        transformed.write.format("delta").mode("overwrite").save("/tmp/delta_test")
        # Load back and assert expectations
        delta_tbl = DeltaTable.forPath(spark, "/tmp/delta_test")
        self.assertEqual(delta_tbl.history(limit=1)[0].operation, "MERGE")
        self.assertTrue(delta_tbl.toDF().filter(col("id") == 3).count() == 0)  # -5 removed
```

*Run:* `pytest -vv test_transforms.py`  

**Key takeaways** –  
- Uses **`local[*]`** for fast feedback.  
- Stores the result in a **Delta table** under `/tmp/delta_test`; this path can be mounted to S3 in a real CI job for integration testing.  

---

#### 2. Auto Loader with Event‑Driven Ingestion

```python
# Notebook cell – configure Auto Loader
raw_path = "s3://my-bucket/raw/"
bronze_path = "s3://my-bucket/bronze/customers/"

# Define schema for deterministic reads
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
customer_schema = StructType([
    StructField("id", IntegerType(), False),
    StructField("country", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("date", TimestampType(), True)
])

# Start the continuous streaming read
df_raw = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", "s3://my-bucket/schema/")
    .schema(customer_schema)
    .load(raw_path)
)

# Write to Delta with checkpointing
(
    df_raw
    .writeStream.format("delta")
    .outputMode("append")
    .option("checkpointLocation", "s3://my-bucket/checkpoints/customers/")
    .trigger(availableNow=1)   # batch mode for demo
    .start(bronze_path)
    .awaitTermination(30)      # run for 30 sec (demo)
)
```

*Observability hooks* –  
- `spark.conf.set("spark.databricks.eventLog.enabled", "true")` writes a **JSON event log** to `s3://my-bucket/eventlogs/`.  
- Enable **`spark.databricks.metrics.enabled`** to push executor metrics to **Prometheus** (via the built‑in endpoint).  

---

#### 3. Data‑Quality Assertion on the Gold Table

```python
# Load the gold table and run expectations
gold_path = "s3://my-bucket/gold/customers/"
gold_df = spark.read.format("delta").load(gold_path)

# Expectation: age must be > 0 and country must be in ["US","CA"]
expectations = gold_df.expectations().addNonNull("country") \
                               .addMonotonic("date") \
                               .addNumericColumn("age", ">= 0")
gold_df.expectAll(expectations)

# If any expectation fails, a SparkException is raised.
# In a job you can catch it and send a Slack alert via a webhook.
```

**Why it matters:**  
- The `expect*` API writes results to the **Spark event log** and can be captured by **Databricks Repos** for automated testing.  

---

#### 4. Debugging a Stalled Streaming Job  

```python
# Assume a streaming job has stopped making progress (> 10 min)
# 1. Open the Structured Streaming UI: https://<databricks-instance>/rmui/jobs/<job-id>/ui?type=streaming
# 2. In a separate notebook, retrieve the Spark UI for the driver:
spark.sparkContext.setLogLevel("DEBUG")
driver_logs = spark._jvm.org.apache.spark.deploy.SparkDriverUtils.getLogFile()
print(driver_logs)   # For illustration only; actual logs in CloudWatch.

# 3. Use the built‑in debugger (if enabled):
dbutils.debugsessions.start()
```

*What to look for:*  
- **`longRunningTask`** metric in CloudWatch (high `Task Duration`).  
- **Executor GC time** (`gcTime` metric).  
- **S3 request latency** (`s3.request.time`) via CloudWatch Logs Insights on the bucket’s access logs.  

---

### AWS‑Specific Considerations  

| AWS Service | Role in the pipeline | Best‑Practice Tips |
|-------------|----------------------|--------------------|
| **Amazon S3** | Source (raw), sink (bronze/gold), checkpoint location, schema location | - Use **S3 requester‑pays** only for external data.<br>- Enable **S3 Object Lock** on checkpoint folders to prevent accidental deletes.<br>- Version bucket + **Lifecycle policies** to prune old raw files. |
| **IAM** | Grants to Databricks Workspace, Auto Loader, EMR clusters | - Adopt **principle of least privilege** for the `databricks-workspace-role`.<br>- Use **IAM Conditions** on S3 (`s3:ExistingObjectTag`) to enforce tag‑based data access. |
| **AWS Glue (Data Catalog)** | Central metadata for tables, used by Auto Loader and Delta | - Register **Bronze/Gold** tables as **external tables** referencing the Delta locations.<br>- Keep **catalog table schemas** in sync with Delta via **`spark.sql("REFRESH TABLE ...")`**. |
| **AWS Lake Formation** | Fine‑grained column‑level permissions, data ingestion wizard | - Grant **`SELECT` on gold table** to a **Lake Formation data lake group**.<br>- Use **LF tag‑based access** to mask `age` for PII. |
| **Amazon EMR** (optional for custom job clusters) | Provides `spark` on EMR with YARN, can be used for **large‑scale batch** jobs. | - Prefer **Databricks Job Clusters** for most use‑cases; only use EMR when you need **EMRFS auth** or **custom bootstrap scripts**. |
| **Amazon CloudWatch** | Central metrics, logs, alarms, dashboards | - Turn on **Databricks CloudWatch Metrics** (`spark.metric.group` = `databricks`).<br>- Create **Log Groups** for each job (`/aws/databricks/jobs/<job-id>/driver`).<br>- Set alarms on **`spark.sql.shuffle.skew`** or **`DataSkew`**. |
| **Amazon EventBridge** | Triggers jobs based on S3 events, integrates with Databricks Jobs API. | - Event pattern: `source: ["aws.s3"]`, `detail-type: ["Object Created"]`, `bucket: ["my-bucket"]`. |
| **AWS CloudTrail** | Auditing of IAM actions on Databricks clusters, S3 access. | - Enable **Trail** for all regions; forward logs to a **central S3 bucket** for forensic analysis. |

#### Integration Checklist  

1. **Workspace IAM Role** – Has `s3:*` on the bucket, `glue:*` on the catalog, `cloudwatch:PutMetricData`, and `datasync:*` (if you copy data).  
2. **SCIM Provisioning** – Ensure **AD groups** map to Unity Catalog **privilege sets** (e.g., `CAN_READ` on bronze, `CAN_WRITE` on gold).  
3. **Encryption** – Enforce **SSE‑S3** on raw bucket, **SSE‑KMS** on gold/gold data. Enable **`spark.databricks.security.secretProvider`** to fetch KMS keys.  
4. **Network** – Use **PrivateLink** or **VPC endpoints** for S3 and Glue so the cluster never traverses the public internet.  

---

### Exam Focus Areas  

*You do not need to memorize every line of code, but you must be able to reason about these concepts under exam conditions.*

- **Describe** the steps required to **enable data‑quality expectations** on a Delta table and **interpret the outcome**.  
- **Identify** which **Spark UI metrics** (e.g., *Task Deserialization Time*, *Shuffle Read/Write*, *Executor GC Time*) are critical for diagnosing a *slow streaming job* and **map them to CloudWatch metrics

---

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