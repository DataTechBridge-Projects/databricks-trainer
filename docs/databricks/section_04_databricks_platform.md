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