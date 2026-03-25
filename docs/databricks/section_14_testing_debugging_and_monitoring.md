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