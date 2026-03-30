# 📘 AWS Glue Deep Dive  
*Section 5 of 15 – AWS Certified Data Engineer Associate (DEA‑C01)*  

> **TL;DR:** Glue is AWS’s fully‑managed ETL/ELT engine that abstracts the Spark runtime, schema discovery, and job orchestration behind a visual crawler and a SQL‑first development experience. On the exam you’ll be tested on **how** to stitch Glue into a larger data pipeline, **what** knobs you must twist to hit performance & cost targets, and **how** security, monitoring, and multi‑account designs behave when you hand off control to non‑AWS teams.

---  

## Overview  
Apache Spark is the de‑facto compute engine for modern data platforms, but running Spark on EC2, managing YARN clusters, and wiring in schema evolution is a full‑time job. AWS Glue abstracts all that plumbing into a **serverless Spark service** that scales from a few hundred rows per minute to petabytes per hour without you ever touching a node.  

The **core problem** Glue solves is *“I have data somewhere in S3 or a streaming source, I need a canonical, schema‑rich representation in a data lake, and I must keep that representation up‑to‑date with minimal operational toil.”* In the AWS data engineering lifecycle this sits between **Ingestion** (Kinesis, Firehose, DMS) and **Store & Manage** (S3, Redshift, Athena, Lake Formation).  

Glue also functions as a **metadata store** (the **Glue Data Catalog**) that any AWS analytics service can consume. When you register a table in the catalog, Athena, Redshift Spectrum, EMR, SageMaker, and even QuickSight can query the same data without a separate `CREATE TABLE` statement. This **single source of truth** is the reason the exam places heavy weight on **catalog consistency, crawler policies, and versioning**.  

Finally, Glue isn’t just “a bunch of Spark jobs you run on EC2”. It offers:  

* **Job bookmarks** – incremental processing that remembers the last checkpoint across restarts.  
* **Transforms** – a built‑in, low‑code transformation language (Glue Python Shell, Glue Spark, Glue Elastic Views) that can be chained without writing a custom job.  
* **DynamicFrames** – a type‑safe representation that automatically coerces semi‑structured JSON/AVRO/Parquet into a flat, columnar schema.  

All of this is orchestrated via **CloudWatch Events**, **Step Functions**, or the **Glue UI**, giving you an exam‑ready mental model of **jobs → triggers → bookmarks → catalog → consumers**.

---  

## Core Concepts  

| Concept | Details (incl. surprises) |
|---------|----------------------------|
| **Glue Data Catalog** | - Central metadata repository (part of the Glue service). <br>- Tables are stored as JSON in an S3 bucket `aws-glue-<region>-catalog-<account-id>` (you can’t see it directly). <br>- **Default behavior:** tables are **schema‑only**; partitions are discovered lazily by crawlers. <br>- **Limit:** 1,000 k databases, 100,000 k tables per account (soft limit; raise via AWS Support). |
| **Crawlers** | - Automated schema discovery for S3, JDBC, DynamoDB, etc. <br>- **Default behaviour:** adds a new table or **updates** the existing schema (adds columns, changes type). <br>- **Surprise:** crawlers **overwrite** table properties (e.g., `partitioned_by`) on every run, which can break downstream Athena queries if you rely on them. |
| **Job Types** | 1. **Python Shell** – simple transform scripts (no Spark). <br>2. **Spark** – full Spark with Python/Scala, **dynamic frames** for schema coercion. <br>3. **Elastic Views** – materialized views that stay in sync with source (used for CDC). <br>- **Exam tip:** The exam loves “when to choose Elastic Views vs. Spark” – answer is *real‑time CDC* vs. *batch enrichment*. |
| **Triggers** | - **OnDemand** – invoked manually or via Step Functions. <br>- **Schedule** – cron or rate‑based (minimum 5 min). <br>- **OnCompliance** – auto‑run when a crawler updates the catalog (great for *schema‑drift* pipelines). |
| **Bookmarks** | - Glue records the *last processed S3 prefix* in an internal DynamoDB table (`aws-glue-jobs-<account-id>`). <br>- **Gotcha:** Bookmarks are **not enabled** by default for Python Shell jobs; you must set `--job-bookmark-option=job-bookmark-enable`. |
| **Partitions & Partition Projection** | - Partition discovery can be **lazy** (crawler runs) or **projection** (you tell Glue the partitioning scheme without scanning). <br>- Projection **dramatically reduces catalog scan latency** and is *required* for partitions > 10 000 per table (otherwise you hit the 10 000 partition limit). |
| **Limits & Quotas** | - **Concurrent jobs per account:** 100 (soft). <br>- **Maximum 2,000 workers** per Spark job (unless you request a limit increase). <br>- **Crawler frequency:** cannot run more than once per minute per crawler. <br>- **Catalog size:** 20 TB of JSON (practical limit). |

---  

## Architecture / How It Works  

Below is a **serverless Spark pipeline** that reads raw CSV from S3, uses a crawler to infer the schema, transforms data with a Spark job, and materialises a partitioned Parquet table.  

```mermaid
graph LR
    subgraph Source
        S3raw[ S3 (raw CSV) ]
        Kinesis[ Kinesis Data Stream ]
    end

    subgraph Glue
        Crawler[ Glue Crawler ]
        Catalog[ Glue Data Catalog ]
        Transform[ Glue Spark Job ]
        Bookmark[ Bookmark Table (DynamoDB) ]
    end

    subgraph Lake
        S3parq[ S3 (partitioned Parquet) ]
        Athena[Athena]
    end

    S3raw -->|new files| Crawler
    Kinesis -->|CDC| Crawler
    Crawler -->|updates| Catalog
    Catalog -->|job definition| Transform
    Transform -->|reads| Catalog
    Transform -->|writes| S3parq
    Bookmark -->|state| Transform
    S3parq -->|query| Athena
    Athena -->|JDBC| QuickSight
```

**Data Flow Narrative**  

1. **Raw data** lands in `s3://my-bucket/raw/` or a Kinesis stream.  
2. The **Crawler** runs (on schedule or via EventBridge) and **pushes schema metadata** to the Glue Data Catalog.  
3. A **Glue Spark job** (`--job-bookmark-option=job-bookmark-enable`) reads the **catalog table definition**, processes *only new data* (thanks to the bookmark), and writes **partitioned Parquet** to `s3://my-bucket/curated/`.  
4. **Athena** (or Redshift Spectrum) can instantly query the curated table without any additional DDL.  

---  

## AWS Service Integrations  

| Direction | Services | How It Connects | IAM / Trust Details |
|-----------|----------|----------------|---------------------|
| **Into Glue** | - **Amazon S3** (as source) <br>- **Amazon Kinesis Data Streams** (Kinesis Data Firehose → Lambda → Glue) <br>- **Amazon DynamoDB** (CDC via DMS) <br>- **Amazon RDS / Aurora** (JDBC) | Glue reads via S3 APIs, JDBC drivers, or DynamoDB Streams (via Lambda). | Glue uses an **IAM Role** (`AWSGlueServiceRole`) with `glue:*` on the catalog, `s3:GetObject` on source prefixes, `kinesis:SubscribeToShard`, `dynamodb:DescribeStream`, `dynamodb:GetRecords`. |
| **Out of Glue** | - **Amazon S3** (curated data) <br>- **Amazon Redshift** (via Spectrum) <br>- **Amazon Athena** (direct) <br>- **AWS Lake Formation** (permissions) <br>- **Amazon EMR** (Glue job as Spark step) | Glue writes to S3 (standard `s3:PutObject`). For Redshift, it writes the partitioned data and then you enable `redshift:CreateExternalTable`. | Output roles: `AWSGlueServiceRole` needs `s3:PutObject` on destination bucket. If you use Lake Formation, you must also attach a **LF tag‑based policy** (`DataLocationPolicy`) granting `SELECT` on the table. |
| **Cross‑Account** | - **Glue Catalog** can be shared via **Lake Formation permissions** or **AWS Glue Catalog resource share** (new in 2022). <br>- **Glue Jobs** can be launched from a **central account** using **Cross‑Account Role** (`arn:aws:iam::<central>:role/GlueCentralRole`). | Central account’s role trusts the *executing* account’s role (`sts:AssumeRole`) with `glue:*`. The catalog is read‑only for downstream accounts unless you grant `DataCatalog` permissions. | Must enable **Lake Formation** in the central account; create **resource policies** on the catalog (`AWSCatalog` resource type). |
| **Pattern Highlight (Exam‑Focused)** | 1. **Firehose → Lambda → Glue Spark** (real‑time CDC). <br>2. **Glue Crawler (onCompliance) → Step Functions → Glue Job** (schema‑drift automation). <br>3. **Glue Elastic Views → S3 → Athena** (materialised view). | Use CloudWatch Events to chain the services; keep a single source of truth in the catalog. | Ensure the Lambda execution role has `glue:StartJobRun` and `glue:GetJobRun`. |

---  

## Security  

### IAM Roles & Resource Policies  
* **Glue Service Role** (`AWSGlueServiceRole`): Must have `glue:*` on the Data Catalog, `s3:*` on source/destination prefixes, and `kms:*` for any `SSE-KMS` operations.  
* **Bookmark DynamoDB Table**: Glue creates a table `glue_bookmark` in the same account. You **must not** delete it; it will cause job failures.  
* **Least‑privilege tip:** Scope S3 actions with `Resource: arn:aws:s3:::my-bucket/curated/*` and limit KMS to the exact CMK (`arn:aws:kms:...:key/...`).  

### Encryption at Rest  
| Layer | Options | When to Use |
|-------|---------|-------------|
| **Data Catalog JSON** | Enforced **KMS‑CMK** (`aws:kms`). You cannot use SSE‑S3 for catalog objects – they are always encrypted with an AWS‑managed key. | Use a custom CMK for compliance (e.g., FIPS 140‑2). |
| **S3 Data (raw & curated)** | - **SSE‑S3** (default, Amazon‑managed). <br>- **SSE‑KMS** (customer‑managed CMK). <br>- **SSE‑C** (customer‑provided key) – *rarely supported* by Glue. | For GDPR / HIPAA, use **SSE‑KMS** with *Envelope Encryption* and enable **S3 bucket policies** that require `aws:kms` condition. |
| **Temporary Spark Shuffle Data** | Glue uses **EMR‑style encrypted storage** (`/tmp` bucket) which defaults to **SSE‑S3**. You can supply `--temp-location` with an S3 path that has SSE‑KMS. | Recommended for PII; you cannot change the underlying KMS key per job – it’s bucket‑level. |

### Encryption in Transit  
* Glue **Spark** traffic between the job (EC2 instance) and S3 is **always over TLS 1.2**. No extra configuration required.  
* **Kinesis ↔ Glue**: Glue consumes via `kinesis:GetRecords`; the SDK uses HTTPS, so TLS is automatic.  
* **VPC‑Hosted Glue** (Glue 2.0 with `--enable-alb` or `--vpc-config`) must use **VPC Endpoints** for S3 (`com.amazonaws.<region>.s3`) and **KMS** (`com.amazonaws.<region>.kms`). Enable **PrivateLink** for S3 (`com.amazonaws.<region>.s3` **Interface** endpoint) if you need **zero internet egress**.  

### VPC & Network Isolation  
* **Glue 2.0** supports **worker type: G.1X (G.1X = 10 GB RAM, 4 vCPU) or G.2X (8 GB, 8 vCPU)**. These are launched in **private subnets**.  
* **Security groups** attached to the job’s **endpoint ENIs** control inbound/outbound traffic to/from S3, RDS, etc. Keep it **restrictive** (e.g., allow only outbound to S3 endpoint).  
* **PrivateLink**: If you need to keep traffic *off the public internet*, create **Interface VPC Endpoints** for Glue, S3, and KMS. The private DNS name will route all SDK calls to the endpoint.  

### Audit Logging  
* **CloudTrail** logs: `glue.amazonaws.com` events (`StartJobRun`, `GetJobRun`, `CreateCrawler`, `GetDatabase`). These are **data events** on the Data Catalog and **management events** for the Glue service role.  
* **Glue Service Logs**: Enable **CloudWatch Logs** (`/aws-glue/errors`, `/aws-glue/health`) by adding `--log-group` in the job’s `--enable-metrics` flag.  
* **Lake Formation**: Use **data access audit** (via AWS Glue DataBrew) to capture `SELECT`/`INSERT` on catalog tables.  

### Compliance Considerations  
| Requirement | How Glue Helps | Caveats |
|-------------|----------------|---------|
| **FIPS 140‑2** | Use **AWS GovCloud (US‑East/West)** region; ensure KMS CMK is also FIPS‑enabled. | Some third‑party connectors (e.g., JDBC for Oracle) may not be FIPS‑compliant. |
| **Data Residency** | Deploy Glue in a specific **AWS Region**; S3 buckets are region‑locked. Use **Bucket Policies** to deny cross‑region replication for raw data. | Remember that **catalog replication** (via Lake Formation) can copy data across regions – you must control that manually. |
| **Cross‑Account Access** | Leverage **Lake Formation tag‑based permissions**; you can grant `SELECT` on `account:123456789` to `role:GlueReader`. | IAM policies still apply; tags are additive – a missing tag can cause `AccessDenied`. |

---  

## Performance Tuning  

### 1. Job Configuration Knobs  
| Parameter | Recommended Value | Rationale |
|-----------|-------------------|-----------|
| `--worker-type` | **G.1X** for < 100 M rows/day; **G.2X** for heavy transformations (> 1 TB). | G.1X is cheaper (10 GB RAM) and scales well for row‑based workloads; G.2X gives more CPU for heavy joins. |
| `--number-of-workers` | **5–10** for modest workloads; **20+** when you need > 200 M rows per job. | Each worker is a *Spark executor*; more workers = more parallel tasks. |
| `--spark-sql.shuffle.partitions` | Set to **`ceil(total_data_size / 128MB)`** (typical default 200). Reduce to **100** for Parquet, increase to **500** for CSV with many columns. | Controls shuffle size; too many partitions waste time. |
| `--job-bookmark-option` | **`job-bookmark-enable`** (default for Python Shell, *off* for Spark). | Enables incremental loads – a huge cost saver for slowly arriving data. |
| `--conf spark.sql.parquet.compression.codec` | **`zstd`** (instead of `snappy`) for read‑heavy pipelines. | Zstd gives ~30 % smaller files with comparable decompression latency. |
| `--conf spark.dynamicAllocation.enabled` | **`true`** (but keep `--max-executors` low). | Lets Spark auto‑scale during spikes but prevents runaway worker counts. |

### 2. Scaling Patterns  
* **Horizontal Scaling** – Increase `--number-of-workers` or use **elastic Spark** (`--conf spark.dynamicAllocation.enabled=true`). *Trigger*: **CPU > 70 %** for > 5 min (monitor via CloudWatch).  
* **Vertical Scaling** – Switch to **G.2X** (2× CPU, 2× RAM) for jobs that are *shuffle‑heavy* (e.g., wide joins). *Trigger*: **Shuffle read/write > 1 TB**.  

### 3. Common Bottlenecks & Detection  

| Symptom | Metric (CloudWatch) | Likely Culprit | Fix |
|---------|---------------------|----------------|-----|
| **Job runs > 2× expected time** | `Glue.Transforms` > 500 seconds, `Glue.Jobs` `JobRunTime` high | Too many **partitions** causing small files (e.g., 100k files) | Enable **partition projection** or **compact** small files with a *post‑job* Optimize (Spark `coalesce(1)` on low‑cardinality partitions). |
| **High `S3ReadBytes` but low `Glue.ShuffleReadBytes`** | `Glue.S3BytesRead` > 10× `Glue.ShuffleReadBytes` | **Skewed keys** – some partition has a lot of data, others few. | Add **salting** or **repartition** by a more even column before shuffle. |
| **`Glue.JobRunState` = FAILED, `Glue.ErrorMessage` = “Worker node lost”** | `Glue.JobRun` `JobRunState` stuck, `Glue.Errors` high | **Insufficient vCPU** in workers; heavy memory pressure. | Increase worker type or enable **dynamic allocation**. |
| **S3 request throttling (`AccessDenied`)** | `Glue.S3Throttle` > 5% of total requests | Too many small reads (e.g., per‑file Parquet loading). | Switch to **bulk read** (load whole prefix) or use **S3 Transfer Acceleration** + **S3 Select**. |

### 4. Data Format & Partitioning Recommendations  

| Data | Format | Partition Strategy | Rationale |
|------|--------|--------------------|-----------|
| **Append‑only events** (e.g., clickstream) | **Parquet (zstd)** | **`year=/month=/day=/hour=`** via **partition projection** (no crawl needed). | Columnar, efficient filter push‑down, compression reduces S3 cost. |
| **Transactional RDBMS snapshots** | **CSV (gzip)** or **JSON** (if semi‑structured) | **`region=`** + **`entity_id=`** | Keep raw shape; later a Glue job will convert to Parquet. |
| **Machine‑learning feature store** | **TFRecord** or **Parquet** | **`feature_group=`** | Directly consumable by SageMaker; partition on `feature_group` for fast retrieval. |

### 5. Cost vs. Performance Trade‑offs  

| Decision | Cost Impact | Performance Impact |
|----------|-------------|--------------------|
| **Enable `--job-bookmark-option=job-bookmark-disable`** | No DynamoDB writes → ~5 % less per‑run cost. | You lose incremental processing – full recompute every run (potentially 10× cost). |
| **Use `SSE-KMS` for data at rest** | +$0.03 per GB (KMS request + key usage). | No performance penalty; just adds IAM & audit overhead. |
| **Run jobs in **`us-east-1`** vs. **`ap-south-1`** with higher data transfer** | Cross‑region data transfer adds $0.02/GB. | Latency may increase for downstream services; better to locate Glue in the same region as S3 and Athena. |
| **Turn on **`--enable-verbose-logging`** for debugging** | Increases CloudWatch Logs volume (extra $0.50/GB). | No runtime impact but can fill up your log bucket quickly. |

---  

## Important Metrics to Monitor  

| CloudWatch Metric (Exact Namespace) | What It Measures | Alarm Threshold (Example) | Action When Triggered |
|--------------------------------------|------------------|----------------------------|------------------------|
| `AWS/Glue` **JobRun** `JobRunTime` | Total wall‑clock seconds a job run has been executing. | > 7200 seconds (2 h) for a job that should finish < 30 min. | Check for shuffle skew; increase workers or switch to G.2X. |
| `AWS/Glue` **Transforms** `TransformCount` | Number of Spark transformations executed in a run. | Sudden spike > 3× baseline. | Investigate new script changes; might be generating extra shuffles. |
| `AWS/Glue` **Errors** `JobRunError` | Count of errors in a job run (including job bookmark errors). | > 0 (any error). | Pull logs; bookmark missing or schema mismatch. |
| `AWS/Glue` **Catalog** `TableSize` (custom metric via EventBridge) | Approx. size (in MB) of a table in the Data Catalog. | Increases > 50 MB in < 5 min (unexpected schema changes). | Validate crawler updates; possible malicious schema injection. |
| `AWS/Glue` **S3BytesRead** `BytesRead` | Bytes read from S3 by Glue jobs. | > 100 TB in 24 h (unexpected surge). | Check for uncontrolled recursive crawlers; add `--exclude` patterns. |
| `AWS/Glue` **S3BytesWritten** `BytesWritten` | Bytes written to the curated bucket. | < 10 % of expected output size. | Verify that the job actually wrote data; possibly dead‑locked. |
| `AWS/Glue` **Worker** `WorkerUptime` | How long a worker node has been alive. | Dropping below 60 % for > 10 min. | Check for pre‑emptible Spot interruptions; enable **worker retry** policy. |
| `AWS/Glue` **GlueService** `GlueServiceRolePolicy` (custom metric) | Number of IAM policy violations (via Config). | > 0. | Trigger an automated remediation (AWS Config rule `glue-role-no-inline-policy`). |

> **Tip:** Use **CloudWatch Anomaly Detection** on `JobRunTime` to automatically learn normal job duration and avoid false alarms on “rarely used” jobs.

---  

## Hands-On: Key Operations  

Below are the **exam‑relevant CLI / boto3** snippets you must be able to read/write. Each block has a comment explaining *why* it matters.

### 1️⃣ Create a Crawler that uses Partition Projection (no auto‑schema updates)  

```bash
# aws cli
aws glue create-crawler \
    --name my-bucket-crawler \
    --role AWSGlueServiceRole \
    --database-name raw_data \
    --targets '{"S3Targets":[{"Path":"s3://my-bucket/raw/"}]}' \
    --schema-change-policy '{"UpdateBehavior":"LOG","DeleteBehavior":"LOG"}' \
    --configuration '{"Version":1,"CrawlerOutput":{"Partitions":{"AddOrUpdateBehavior":"InheritFromTable","Exclusions":["^temp/"],"IncludeNulls":false},"Tables":{}}}' \
    --configuration-updates '{"PartitionProjections":{"Database":"raw_data","TableName":"events","Projections":{"Year":{"Values":["2020","2021","2022"],"CrawlField":"year","Format":"yyyy","TimeUnit":"YEARS"}}}}' \
    --cli-input-json file://crawler.json
```

> **Why?**  
> * The `--configuration-updates` enables **partition projection**, so you don’t have to scan the catalog for every new partition. This is a **must‑know** for the exam’s “catalog performance” scenario.

### 2️⃣ Start a Glue Spark Job with Bookmarking and a Custom S3 Temporary Location (encrypted with a CMK)  

```python
import boto3
glue = boto3.client('glue')
response = glue.start_job_run(
    JobName='etl_enrich_events',
    Arguments={
        '--JOB BookmarkOption': 'job-bookmark-enable',
        '--TempDir': 's3://my-bucket/tmp/glue-jobs/',   # use bucket with SSE-KMS
        '--job-language': 'python',
        '--enable-metrics': 'true',
    },
    # optional: set a CMK for the Glue job's temporary S3 bucket (requires a trust relationship)
    # Note: You cannot directly pass a KMS key here; the bucket must be pre‑configured.
    MaxRetries=2,
    Timeout=3600,
    # You can also pass a Job Bookmark argument per run, but enabling globally is cleaner.
)
print("Run ID:", response['RunId'])
```

> **Why?**  
> * Demonstrates **bookmark enabling** (incremental loading) and **S3 temp location** (critical for cross‑region compliance). The **`--enable-metrics`** flag is often examined for debugging.

### 3️⃣ Retrieve the latest job run state and check for failures (Python + boto3)  

```python
import boto3, time
glue = boto3.client('glue')
job_name = 'etl_enrich_events'

# Poll until run completes (simple loop)
while True:
    run = glue.get_job_run(Name=job_name, JobName=job_name)['JobRun']
    if run['JobRunState'] in ('SUCCEEDED', 'FAILED', 'TIMEOUT'):
        break
    print(f"Current state: {run['JobRunState']} – waiting 15s")
    time.sleep(15)

if run['JobRunState'] == 'SUCCEEDED':
    print("✅ Job succeeded – check S3 output.")
else:
    err = run.get('JobRunError', {})
    print("❌ Job failed:", err.get('ErrorMessage', 'Unknown error'))
    raise RuntimeError(f"Glue job failed: {run['JobRunState']}")
```

> **Why?**  
> * Exam questions often ask you to **detect job failures** via the **JobRun** API. Knowing how to poll and interpret the `JobRunError` (e.g., “Worker node lost”) is a typical debugging scenario.

---  

## Common FAQs and Misconceptions  

**Q:** *Can Glue read directly from an RDS MySQL instance without a VPC endpoint?*  
**A:** **No.** Glue workers are launched in a **private subnet** (or your own VPC if you specify `--vpc-config`). To reach a self‑hosted MySQL, the subnet must have **NAT gateway** or you must create a **VPC endpoint for RDS** and the worker’s **security group** must allow outbound to the RDS security group. Otherwise you’ll see *“Unable to resolve host”* errors.  

---

**Q:** *Is the Glue Data Catalog a separate service that I need to patch?*  
**A:** **No.** The catalog is **fully managed** and updates are **eventually consistent** (typically < 5 min). You cannot patch it, but you can **disable automatic crawler updates** if you want full control over schema evolution.  

---

**Q:** *Do Glue jobs incur compute charges even if they fail instantly?*  
**A:** **Yes.** Glue bills **per DPU‑second** (`1 DPU = 4 vCPU + 16 GB RAM`). If the job fails before the first Spark executor starts, you still pay for the *initial* DPUs (minimum 5 seconds).  

---

**Q:** *If a crawler is scheduled every hour, will it always detect new columns added to a JSON file?*  
**A:** **Usually, but not always.** Crawlers **only add columns** if the `AddOrUpdateBehavior` is set to `UPDATE_IN_DATABASE`. If the crawler uses `LOG` behavior, it will ignore new columns and you’ll need to manually run the crawler.  

---

**Q:** *Why does `glue:UpdateDatabase` return *AccessDenied* when I have the `glue:*` permission?*  
**A:** Because **AWS Glue uses resource‑based policies** on the **Data Catalog** bucket. You also need the bucket’s **KMS key policy** to allow your principal to `kms:Decrypt` if the catalog uses a **customer‑managed CMK**.  

---

**Q:** *Is it safe to store production data in a table that uses `partitioned_by: []` but never runs a crawler?*  
**A:** **No.** Without crawlers or manual `ALTER TABLE` statements, the table will have **no partition metadata**, leading to **`InvalidPartitionException`** at query time. Use **partition projection** or always run a **crawler after schema changes**.  

---

**Q:** *Can I use the same Glue job IAM role for both reading and writing to the same S3 bucket?*  
**A:** **Yes, but with caution.** The role must have both `s3:GetObject` (read) and `s3:PutObject` (write). However, if you enable **SSE‑KMS** you also need `kms:Decrypt` on the source key and `kms:GenerateDataKey*` on the destination key. Missing these can cause silent failures that only show up as “Access Denied” in CloudWatch Logs.  

---  

## Exam Focus Areas  

| Exam Domain (DEA‑C01) | Specific Skills Tested on Glue |
|-----------------------|--------------------------------|
| **Ingestion & Transformation** | - Designing crawlers that **preserve partition projection**.<br>- Selecting the right **job type** (Python Shell vs. Spark vs. Elastic Views) for CDC vs. batch. |
| **Store & Manage** | - Properly **granting Lake Formation permissions** to Glue jobs.<br>- Using **catalog tables** vs. custom tables in Redshift Spectrum. |
| **Operate & Support** | - Interpreting **Glue job run metrics** to detect skew or throttling.<br>- Configuring **bookmarks** to prevent full recompute. |
| **Design & Create Data Models** | - Modeling **star‑schema** with Glue jobs that write partitioned Parquet.<br>- Deciding when to use **DynamicFrames** vs. regular DataFrames. |

**Key takeaway for the exam:** Glue is **not** a “set‑and‑forget” ETL engine. You must always consider **catalog consistency, security context, and scaling knobs** to stay within cost and performance bounds.

---  

## Quick Recap  

- ✅ **Glue = Serverless Spark + Catalog** – treat the catalog as the *single source of truth* for all analytics services.  
- ✅ **Crawlers + Partition Projection** = low‑latency schema updates; **bookmarks** = incremental runs.  
- ✅ **Security**: Use SSE‑KMS on S3, IAM role scoped to catalog, VPC endpoints, and CloudTrail logging for compliance.  
- ✅ **Performance**: Tune workers, enable dynamic allocation, set shuffle partitions, and use columnar formats (zstd Parquet).  
- ✅ **Monitoring**: CloudWatch `JobRunTime`, `TransformCount`, `BytesRead/Written`, and custom catalog size metrics are your early‑warning system.  
- ✅ **Exam focus**: Knowing *when* to pick each job type, how to avoid common catalog pitfalls, and how to read the failure logs.  

---  

## Blog & Reference Implementations  

| Resource | Why It Matters |
|----------|----------------|
| **AWS Big Data Blog – “Glue Partition Projection: A New Way to Avoid Crawler Scans”** (June 2023) | Walk‑through of the exact config you’ll need for exam scenario #3. |
| **Re:Invent 2022 – “Building Real‑Time Data Lakes with Glue Elastic Views”** (video, 32 min) | Shows the **CDC** pattern that the exam loves; includes IAM trust diagram. |
| **AWS Workshop Studio – “Serverless ETL with AWS Glue and Step Functions”** | End‑to‑end CloudFormation that you can deploy in a sandbox and dissect. |
| **Well‑Architected Framework – “Data Analytics – Storage & Catalog”** (chapter 4) | Best‑practice checklist for catalog design and cross‑account sharing. |
| **GitHub – aws-samples/glue-optimizations** | Contains a Spark job template with `zstd` Parquet, partition projection, and detailed `glue-job.json` for tuning. |
| **AWS Blog – “Bookmarks in Glue: Incremental Loads at Scale”** (2024) | Explains the DynamoDB bookmark table and the *gotcha* around missing `--job-bookmark-option`. |
| **Re:Invent 2023 – “Glue Jobs in a VPC – Design Patterns & Cost”** | Deep dive on VPC‑hosted Glue, security groups, and private endpoints. |

> 🎓 **Study tip:** Clone the `glue-optimizations` repo, spin up the CloudFormation stack, and then break the job by removing the bookmark option. Observe the extra S3 read volume in CloudWatch – that’s the concrete evidence the exam will test.  

---  

*End of Section 5 – AWS Glue Deep Dive*  

Proceed to **Section 6 – Store & Manage** for the next deep dive on data lake design patterns. Good luck on the exam – you’ve got the *why* now, go prove the *how* in the hands‑on labs! 🚀