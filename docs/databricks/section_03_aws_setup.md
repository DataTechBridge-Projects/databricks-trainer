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