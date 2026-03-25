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