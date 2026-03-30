# 📚 Section 1 – Course Introduction  
**AWS Certified Data Engineer Associate (DEA‑C01)**  

> *“You don’t pass the exam by memorizing a checklist. You pass by **understanding the AWS data‑engineering fabric**, why each thread exists, and how you can stitch them together to survive real‑world traffic spikes, cost pressures, and compliance audits.”* – Your instructor, a former AWS Solutions Architect with 7 + years of production pipeline experience  

---

## Overview  

Data engineering on AWS is **the discipline of turning raw, high‑velocity digital events into trusted, query‑ready datasets** that power downstream analytics, machine‑learning, and operational intelligence.  

At a high‑level, AWS provides a **managed, loosely‑coupled stack** that lets you:

1. **Capture** events from every imaginable source (IoT devices, web apps, batch jobs) – *Kinesis, CloudWatch Logs, API Gateway, partner services*.  
2. **Transport** those events with durable ordering, replayability, and back‑pressure handling – *Kinesis Data Streams, MSR, MSK*.  
3. **Transform** in‑flight or at rest using serverless or managed compute – *Lambda, Glue Spark, EMR, Fargate*.  
4. **Persist** in the right format and granularity for cost‑effective query or ML consumption – *S3 (Parquet/ORC/JSON), DynamoDB, Redshift, Aurora Serverless, Timestream*.  
5. **Govern & Protect** the data with fine‑grained IAM, encryption, and audit trails – *Resource‑based policies, KMS, CloudTrail, Config*.  

These building blocks are **not a linear chain**; they are a **graph of capabilities** you stitch together based on latency, durability, cost, and compliance constraints. The DEA‑C01 exam expects you to **choose the correct graph node for a given business requirement**, not just recite the service names.

The **core problem** this ecosystem solves is **“data latency at scale”** – handling millions of events per second while guaranteeing exactly‑once processing, sub‑second freshness, and end‑to‑end security. The alternative (batch‑only, on‑prem ETL) simply can’t meet modern SLAs for fraud detection, ad‑tech attribution, or real‑time personalization.

---

## Core Concepts  

| Concept | Why It Matters | AWS‑Specific Gotchas |
|---------|----------------|----------------------|
| **Exactly‑once semantics** | Guarantees no duplicate downstream records – critical for financial events, inventory updates, etc. | Kinesis **`shard‑iterator-type`** can be `TRIM_HORIZON`, `LATEST`, or `AT_SEQUENCE_NUMBER`. Forgetting to set `NEW_SEQUENCE_NUMBER` after a successful `PutRecord` can cause **`IntegriityViolationException`**. |
| **Retention window** | Determines how long raw events stay readable; influences replay after a bug. | Default Kinesis retention is **24 h**; you must **explicitly set `RetentionPeriodHours`** (max 365 h). Under‑provisioned retention leads to “**Data lost due to retention expiration**” errors. |
| **Parallelism = shards** | Shard count drives throughput; scaling is a *horizontal* operation. | Kinesis **shard limit** is **5,000 records/second**, **1,000 records/second** per **partition key**. Exceeding triggers **`ProvisionedThroughputExceededException`** – you must **increase shard count** *before* hitting limits. |
| **Data lake zone** | The “single source of truth” where raw & curated layers coexist. | S3 **`ObjectLock`** default **`Compliance`** mode can **prevent deletion** of data, causing **storage cost creep** if you forget to enable **`default retention`**. |
| **Partitioning & bucket sizing** | Impacts query latency (Athena) and cost (S3 requests). | Athena’s **partition pruning** works only if **partition columns** are **`adddate`** or **`event_id`** and the **data format is columnar (Parquet/ORC)**. Using plain CSV on a high‑cardinality partition will **slow scans** and **blow up your bill**. |
| **Glue Crawlers** | Auto‑discover schema & partitions – a huge time‑saver. | Crawlers **default to a 10 GB data limit** per run; larger tables need **multiple crawlers** or **incremental crawls** (`CrawlerState`) else they will silently skip newer data. |
| **Redshift Spectrum** | Query S3 directly without loading. | Spectrum **requires external tables** to have **`AWS_REGION`** set in the `redshift` profile; missing this leads to **`AccessDeniedException`** from S3 despite correct IAM. |
| **Consistency model** | Knowing eventual vs. strong consistency prevents stale reads. | DynamoDB **global tables** provide **regional read/write consistency** only within a region; cross‑region reads are **eventually consistent**. In a multi‑region analytics pipeline, a read from the **replica** may return **stale data** for up to **15 minutes**. |

---

## Architecture / How It Works  

Below is a **canonical end‑to‑end streaming pipeline** that covers the four exam domains (Ingestion, Transformation, Store/Manage, Operate/Support).  

```mermaid
graph LR
    subgraph Source Layer
        A[Application / IoT Devices] -->|HTTPS| B[Amazon API GW]
        C[IoT Core] -->|MQTT| D[Amazon Kinesis Data Streams]
    end
    subgraph Ingestion
        D -->|shard| E[Kinesis Data Firehose]
    end
    subgraph Transformation
        E -->|buffer| F[Lambda (JSON → Parquet)]
        F --> G[Amazon S3 (raw/processed)]
    end
    subgraph Batch/ELT
        H[Glue Spark Jobs] -->|JDBC| I[Amazon Redshift]
        I -->|COPY| J[Amazon Redshift Spectrum (external tables)]
    end
    subgraph Analytics
        J -->|SQL| K[Amazon Athena]
        K -->|Results| L[QuickSight / ML Model]
    end
    subgraph Governance
        S3 -->|KMS| M[KMS Keys (SSE‑KMS)]
        N[CloudTrail] -->|Logs| O[CloudWatch Logs]
        O -->|Metric filters| P[CloudWatch Alarms]
    end
    style Source Layer fill:#f9f,stroke:#333,stroke-width:2px
    style Transformation fill:#bbf,stroke:#333,stroke-width:2px
    style Governance fill:#efe,stroke:#333,stroke-width:2px
```

**Key take‑aways from the diagram**

* **Event flow is **asynchronous** – each component decouples via Kinesis shards.**  
* **Lambda is the only compute that **touches data while it’s still in transit** (good for enrichment).**  
* **Glue jobs are **batch‑oriented** – they **re‑process** raw data, not a replacement for streaming.**  
* **Redshift Spectrum provides **the “store‑and‑query” hybrid** that lets you avoid `COPY` for ad‑hoc analytics.**  

---

## AWS Service Integrations  

| Direction | Services Feeding **IN** | Integration Mechanism | Typical Use‑Case | Security / Trust |
|-----------|--------------------------|-----------------------|------------------|-------------------|
| **Into Kinesis** | • API Gateway (REST, WebSocket) <br> • IoT Core (MQTT, HTTP) <br> • CloudWatch Logs (via subscription) <br> • MSK (Kafka) <br> • Direct `PutRecord` from SDKs | *Stream as a service* – producers write to the shard `PutRecord` API. | Real‑time clickstreams, telemetry, security logs. | IAM role `kinesis:PutRecord` on stream resource; **resource‑based policies** allow specific accounts to put records. |
| **Into Firehose** | • Kinesis Data Streams <br> • S3 ObjectCreated events <br> • DynamoDB Streams | Direct delivery, **no consumer logic**. | Bulk ingest of logs, click events → S3 (partitioned). | Firehose delivery stream uses **IAM service role**; can assume **`AWSLambdaRole`** or **`S3Role`** for data delivery. |
| **From Firehose** | • Amazon S3 (prefix‑based) <br> • Amazon Redshift (via `COPY`) <br> • Elasticsearch (via Lambda) | S3 event notifications, `COPY` command, Lambda trigger. | Analytics pipelines: S3 → Athena → QuickSight. | Firehose uses **S3 bucket policy** (`arn:aws:iam::account:s3:::my-bucket/*`) and **KMS key policy** for `s3:PutObject`. |
| **Glue Crawlers** | • S3 data lake (raw) <br> • DynamoDB tables (metadata) | Crawlers scan data and write **Glue Data Catalog** entries. | Auto‑discover schema for Athena/Redshift Spectrum. | Glue uses an **execution role** (`GlueServiceRole`) with `glue:*` on the catalog and `s3:GetObject` on data. |
| **Glue Jobs → Redshift** | • S3 (Parquet) <br> • JDBC to Redshift | Spark job writes via **JDBC** with bulk load. | Denormalized fact tables for BI. | Job role needs `redshift:CopyFromS3`, `redshift-data:ExecuteStatement`. |
| **Lambda → DynamoDB** | • Event source mapping from Kinesis <br> • API Gateway | Lambda polls Kinesis, writes to DynamoDB. | Real‑time user profile store. | Lambda execution role must have `dynamodb:PutItem` on table. |
| **Redshift ↔ S3** | • `COPY` from S3 <br> • Spectrum external tables | Use **IAM role** for S3 access, **KMS** for decryption. | Data lake to data warehouse. | Must enable **`redshift:AssumeRole`** in S3 bucket policy and **`kms:Decrypt`** for the key. |

### Common Multi‑Service Patterns (Exam‑Friendly)

1. **“Raw‑to‑Curated” lake** – Kinesis → Firehose → S3 (raw) → Glue Crawler → Glue ETL → S3 (curated) → Athena/Redshift Spectrum.  
2. **“Event‑driven microservice”** – API Gateway → Lambda (validation) → Kinesis → Lambda (enrichment) → DynamoDB (profile) + Firehose → S3 (archival).  
3. **“Streaming analytics”** – IoT Core → Kinesis → Kinesis Data Analytics (SQL) → S3 (Parquet) → Redshift Spectrum → QuickSight.  

Each pattern hinges on **IAM trust relationships** (`AWS::IAM::Role` → `Principal: Service:...`) and **resource‑based policies** (e.g., `kinesis:PutRecord` on a specific stream ARN).  

---

## Security  

### IAM Roles & Resource‑Based Policies  

| Component | Required Permissions (minimum) | Reason |
|-----------|--------------------------------|--------|
| **Kinesis Producer (App/Device)** | `kinesis:PutRecord`, `kinesis:PutRecords` on `arn:aws:kinesis:region:account:stream/stream-name` | Direct write to stream; without this you get `AccessDenied`. |
| **Kinesis Consumer (Lambda/Firehose)** | `kinesis:GetRecords`, `kinesis:GetShardIterator`, `kinesis:DescribeStream` | Consumer must be able to read shards; often attached to a **service‑linked role** for Lambda. |
| **Lambda Function (Transformation)** | `lambda:InvokeFunction` on other Lambdas (if chained) <br> `s3:PutObject` on destination bucket <br> `kms:Encrypt` on KMS key | Writes transformed data to S3 and logs via CloudWatch. |
| **Glue Crawler** | `glue:GetDatabase`, `glue:GetTable`, `s3:GetObject`, `glue:StartCrawler` | Reads raw data, writes to Glue Catalog. |
| **Redshift Spectrum** | `redshift-data:ExecuteStatement`, `redshift-data:BatchExecuteStatement` on `arn:aws:rds:region:account:cluster:cluster-name` <br> `s3:GetObject`, `s3:ListBucket` on data lake bucket | Allows Spectrum to query S3 data. |
| **S3 Bucket (Data Lake)** | **Bucket Policy**: `{"Principal":"*", "Action":"s3:GetObject", "Condition":{"StringEquals":{"aws:PrincipalArn":"arn:aws:iam::123456789012:role/DataLakeRole"}}}` | Enforces **principle of least privilege** and **auditability**. |

### Encryption  

| Layer | Options | When to Use |
|-------|---------|-------------|
| **At Rest (S3)** | `SSE‑S3` (AES‑256, AWS‑managed) <br> `SSE‑KMS` (customer‑managed CMK) <br> `SSE‑C` (customer‑provided keys) | **`SSE‑KMS`** is mandatory for **PCI‑DSS** workloads because you can **audit key usage** via CloudTrail. Use **`SSE‑S3`** only for non‑regulated, low‑cost logs. |
| **At Rest (Kinesis)** | **Server‑Side Encryption (SSE)** – default `AES‑256` (AWS‑managed) | Enable **Kinesis Server‑Side Encryption (SSE‑KMS)** for **compliance**. You must specify `EncryptionType: KMS` and `KMSKeyId` in the `PutRecord` request. |
| **In‑Transit** | TLS 1.2 via AWS SDKs (HTTPS) <br> **VPC Endpoints** (Gateway for S3, Interface for Kinesis, DynamoDB) | TLS is **automatic** for all AWS SDKs, but **VPC Endpoints** prevent traffic from traversing the public internet (recommended for highly regulated environments). |
| **KMS** | **AWS‑managed CMK** (`aws/kms`) <br> **Customer‑managed CMK** (`customers/key-id`) | Customer‑managed gives **full key rotation, policy control, and audit**. Use it for **data residency** (e.g., FIPS 140‑2 in GovCloud). |
| **VPC** | **PrivateLink** for Kinesis Data Analytics, **Interface Endpoints** for Glue and Redshift | Enables **zero‑exposure to the public internet** – you can lock down security groups to only allow traffic from specific ENIs. |

### Audit Logging  

| Service | CloudTrail Event Category | Typical Event |
|---------|---------------------------|---------------|
| **Kinesis** | `DataPlane` – `PutRecord`, `PutRecords`, `GetRecords` | Shows who wrote/read each shard; useful for **integrity audits**. |
| **Firehose** | `DeliveryStream` – `PutRecord` (via Firehose) | Audits inbound streaming data before it lands in S3. |
| **Lambda** | `Lambda` – `InvokeFunction` | Tracks transformation functions that touch data. |
| **Glue** | `Glue` – `GetDatabase`, `GetTable`, `StartCrawler` | Detects schema changes that could break downstream jobs. |
| **S3** | `ObjectCreated`, `ObjectDeleted`, `PutObject` | Detects unauthorized deletion of raw logs. |
| **Redshift** | `Redshift` – `CopyFromS3`, `ExecuteStatement` | Tracks bulk loads and analytics queries. |

**Action**: Set **CloudTrail multi‑region trail** with **S3 bucket** and **CloudWatch Logs** integration. Then create **CloudWatch metric filters** for `eventName` = `PutRecords` on Kinesis; alarm when **> 10,000** writes per minute (possible DDoS).  

### Compliance Considerations  

| Requirement | How to Meet It on AWS |
|-------------|------------------------|
| **FIPS 140‑2** | Use **AWS GovCloud** or **AWS Cloud Regions** that enforce FIPS endpoints; ensure **KMS keys** are set to **FIPS‑compatible**. |
| **Data Residency (EU‑only)** | Create **S3 bucket in `eu-west-1`** and **Kinesis stream in same region**; enable **ObjectLock** with `Compliance` mode to enforce retention. |
| **Cross‑Account Access** | Use **IAM Role with `sts:AssumeRole`** and **resource‑based policies** on Kinesis/Firehose that allow `aws:PrincipalArn` of the producer account. |
| **CMK Rotation** | Enable **automatic key rotation** (once per year) on **customer‑managed CMK**; verify via CloudTrail `EnableKeyRotation`. |
| **Auditability of Data Deletion** | Use **S3 Object Lock** with `retention-period` and **legal hold**; CloudTrail will log `DeleteObject` failures. |

---

## Performance Tuning  

### 1. **Kinesis Shard Scaling**  

| Setting | Recommended Value | Rationale |
|---------|-------------------|-----------|
| **Shard count** | **Start at 2–3× the expected peak throughput** (e.g., 100 shards for 10,000 records/sec * 2). | Guarantees **`PUT_RECORDS` success** and provides headroom for downstream `GetRecords` concurrency. |
| **Increasing shard capacity** | Use **`UpdateShardCount`** API with a **5‑minute warm‑up** before a traffic spike. | Reduces the risk of **“`ProvisionedThroughputExceeded`”** errors. |
| **Parallel consumers** | **At least 1 consumer per shard**; each consumer should batch `GetRecords` with **`MAX_BATCH_SIZE=10,000`**. | Maximizes **`GetRecords`** throughput; too few consumers = under‑utilized shards. |

**Bottleneck detection**: CloudWatch metric `IncomingRecords` per shard plateauing near `5,000` while `OutgoingRecords` lags → **Consumer group lag** (`GetRecords.IteratorAgeMilliseconds`).  

### 2. **Lambda Transformations**  

| Parameter | Recommended Setting | Reason |
|-----------|---------------------|--------|
| **Memory** | **256 MiB** for simple JSON → Parquet (≈ 0.6 ms/record) | Lowest price while still offering **2 vCPU** to stay within **10 ms** per batch. |
| **Timeout** | **30 seconds** (max) | Avoids “cold start” penalties for high‑frequency batches; keep under **10 seconds** for 10‑record batches. |
| **Concurrency limit** | **Reserved concurrency = 5× expected parallel batches** (e.g., 50) | Guarantees **burst capacity** without throttling downstream S3. |
| **Environment variables** | `KMS_KEY_ID`, `OUTPUT_FORMAT=parquet` | Avoids **runtime lookups** that add latency. |

**Tip**: Use **`/tmp` for temporary buffers** *only* when < 128 MiB; larger buffers should be streamed directly to **S3** via **`boto3`** with multipart upload.

### 3. **S3 Storage & Query Costs**  

| Recommendation | Impact |
|----------------|--------|
| **Partition on `event_date` and `customer_id` (two‑level)** | Reduces Athena scan size **> 80 %** for date‑range queries. |
| **File size 128–256 MiB** (Parquet) | Balances **`GET` request cost** (≈ $0.0005 per 1000) with **scan efficiency** (avoid many small objects). |
| **Compress with ZSTD (level 3)** | **~30 % size reduction** vs. Snappy, **~20 % faster** scan because of less I/O. |
| **Enable S3 `Intelligent‑Tiering`** for raw logs older than 30 days | Moves infrequently accessed objects to **standard‑IA** automatically – **cost saving** without lifecycle policies. |
| **Set `s3:RequestPayment` = `false`** in bucket policy for external access | Prevents **unexpected cross‑account billing**. |

### 4. **Redshift Spectrum**  

* **`MAX\_PARALLEL\_SCAN`** – set to **`200`** for large clusters; **`0`** to let Redshift auto‑tune.  
* **`s3.parquet.compress`** – use **`zstd`** (if supported) for best trade‑off between size and CPU.  

### 5. **Cost vs. Performance Trade‑offs**  

| Scenario | Cheapest | Balanced | Highest Performance |
|----------|----------|----------|----------------------|
| **Kinesis data ingest** | 1‑shard stream with **`On‑Demand`** pricing | **5‑shard provisioned** (pre‑pay) + **`Enhanced Fan‑Out`** | 50+ shards + **`Enhanced Fan‑Out`** + **`Server‑Side Encryption (KMS)`** |
| **Transformation compute** | **Lambda (pay‑per‑invocation)** | **Lambda + Provisioned Concurrency** | **Fargate + Spot** with **`S3 Transfer Acceleration`** |
| **Data lake storage** | **S3 Standard** (no lifecycle) | **S3 Intelligent‑Tiering** | **S3 Glacier Deep Archive** (for > 365 day retention) |

---

## Important Metrics to Monitor  

| CloudWatch Metric (Namespace:Service) | Measures | Alarm Threshold (example) | Alarm Action |
|----------------------------------------|----------|---------------------------|--------------|
| **`IncomingRecords` (AWS/Kinesis)** | Number of records written to the stream per minute | `> 8,000` per shard (approaching `5,000` limit) | **Scale out** – `UpdateShardCount` + 20% shards; trigger SNS alert. |
| **`WriteProvisionedThroughputExceeded` (AWS/Kinesis)** | Count of write throttles | **`> 5` per 5‑minute period** | Auto‑scale shards; optionally enable **`OnDemand`** mode. |
| **`IteratorAgeMilliseconds` (AWS/KinesisConsumer)** | Lag between latest record and consumer iterator | **`> 5,000` ms** for > 5 consecutive periods | Scale up consumer count; add CloudWatch Event to trigger Lambda scaling. |
| **`Errors` (AWS/Lambda)** | Invocation errors per minute | **`> 10`** (especially `ServiceException` or `Throttles`) | Investigate code; add dead‑letter queue (DLQ) or increase memory. |
| **`TotalBytesRead` (AWS/S3)** | Bytes retrieved from S3 (for Athena) | **> 500 MiB** per query (unexpectedly high) | Optimize partitions, check for table scans; consider `EXPLAIN` query plan. |
| **`ScanBytes` (AWS/Glue)** | Bytes scanned by Glue jobs (cost driver) | **> 2 TB per job** | Review partition pruning; enable **`Crawler`** incremental mode. |
| **`CPUUtilization` (AWS/Redshift)** | CPU usage on each node | **> 80 %** for > 10 min | Add Spectrum concurrency or resize cluster. |
| **`NetworkOut` (AWS/ECS/EKS)** | Network traffic of streaming jobs (Fargate) | **> 10 Gbps** (approaching ENI limit) | Increase **`ENI`** size or split workload. |
| **`KMSKeyUnencrypted` (AWS/KMS)** | Count of keys without encryption enabled (policy) | **`> 0`** | Create remediation Lambda to enforce `EnforcedKmsEncryption` tag. |

**Why these metrics matter**: They map directly to **exam scenario pain points** (e.g., “your stream is being throttled – what metric do you check?” → `WriteProvisionedThroughputExceeded`).  

---

## Hands‑On: Key Operations  

Below are **real‑world CLI snippets** you should be able to run in a sandbox (or locally with `aws-vault`). Every block has an inline comment explaining the **“what”** and the **“why it’s on the exam”.**  

> **NOTE**: Replace `my‑account`, `us-east-1`, and `my‑stream` with your own values.

### 1️⃣ Create a Kinesis Data Stream with Exactly‑Once and Server‑Side Encryption  

```bash
# What: A provisioned 5‑shard Kinesis stream encrypted with a customer‑managed KMS key.
# Why: The exam loves “Exactly‑Once” + KMS details – you must know IAM permissions and key IDs.

aws kinesis create-stream \
  --stream-name my-prod-stream \
  --shard-count 5 \
  --encryption-type KMS \
  --kms-key-id alias/my-data-key \
  --region us-east-1 \
  --output json

# Verify
aws kinesis describe-stream \
  --stream-name my-prod-stream \
  --query "StreamDescription{Name:StreamName,ShardCount:ShardCount,EncryptionType:EncryptionTypeType}" \
  --output table
```

### 2️⃣ Put Records – Respect `SequenceNumber` for Exactly‑Once  

```python
# What: Use boto3 to put 3 records with explicit SequenceNumber.
# Why: Demonstrates understanding of the `NEW_SEQUENCE_NUMBER` lifecycle; a common exam trap is using `INSERT_AFTER`.

import boto3, time

kinesis = boto3.client('kinesis', region_name='us-east-1')
stream_name = 'my-prod-stream'

def put_with_seq(partition_key, data):
    # First put a placeholder to get a sequence number (or use put_records with explicit ids)
    resp = kinesis.put_record(
        StreamName=stream_name,
        Data=data,
        PartitionKey=partition_key,
        # Force a new sequence number regardless of previous writes
        SequenceNumber=aws.kinesis.client.meta.api_version)  # placeholder – not used
    # Correct approach: use `PutRecords` with `SequenceNumberForOrdering` or rely on auto.
    # Here we simply use put_record (boto handles the sequence number internally)
    return resp

# Example payloads
records = [
    {'Data': b'{"event":"click","user":"1234"}', 'PartitionKey': 'user-1234'},
    {'Data': b'{"event":"purchase","user":"1234"}', 'PartitionKey': 'user-1234'},
    {'Data': b'{"event":"view","user":"5678"}', 'PartitionKey': 'user-5678'}
]

for rec in records:
    put_with_seq(rec['PartitionKey'], rec['Data'])
    time.sleep(0.5)  # avoid hitting per‑second limit

print("✅ Records placed – check Stream's GetRecords for ordering.")
```

> **Exam tip**: The **`SequenceNumber`** is **not** something you normally specify; the real exam asks “Which SDK call ensures `sequenceNumber` is generated for each record?” → `put_record` (auto) vs. `put_records` with **`SequenceNumberForOrdering`**.  

### 3️⃣ Configure Firehose to Deliver to S3 with Server‑Side Encryption (SSE‑KMS)  

```bash
aws firehose create-delivery-stream \
  --delivery-stream-name clickstream-to-s3 \
  --delivery-stream-type DirectPut \
  --s3-destination-update-number-of-open-files 5000 \
  --s3-destination-compression-format GZIP \
  --s3-destination-encryption-configuration \
    '{"RoleARN":"arn:aws:iam::123456789012:role/FirehoseDeliveryRole","ServerSideEncryptionConfiguration":{"EncryptionType":"KMS","KMSKeyArn":"arn:aws:kms:us-east-1:123456789012:key/abcd-1234-efgh-5678"},"BucketARN":"arn:aws:s3:::my-lake-raw"}',
  --kinesis-prefix "records/" \
  --region us-east-1
```

**Explanation**:  
* `DirectPut` = you push directly to Firehose (no Kinesis needed).  
* `ServerSideEncryptionConfiguration` forces **KMS** (exam often asks about **SSE‑KMS vs. SSE‑S3**).  
* `--compression-format` reduces storage costs – a performance‑cost trade‑off to know.

---

## Common FAQs and Misconceptions  

**Q: “When should I use `Enhanced Fan‑Out` on Kinesis versus standard polling?”**  
**A:** Use **Enhanced Fan‑Out** when you need **per‑shard 2 MB/s throughput** and **sub‑millisecond read latency** (e.g., real‑time fraud detection). Standard polling (`GetRecords`) is limited to **5 MB/s per shard** and **consumer lag can be seconds**. The exam will present a scenario with > 100 k rps and ask for the minimal changes – the answer is “enable Enhanced Fan‑Out and increase shard count”.

---

**Q: “Is `SSE‑S3` acceptable for PCI‑DSS data?”**  
**A:** **No.** PCI‑DSS requires **AWS‑managed encryption with customer‑controlled keys** for logging and transmission. `SSE‑S3` uses **AWS‑managed keys (SSE‑S3) or S3‑managed keys (SSE‑KMS without a custom CMK)** which does not meet the “customer‑controlled keys” requirement. The exam expects you to choose **`SSE‑KMS` with a customer‑managed CMK**.

---

**Q: “Can I write to a Kinesis stream from a Lambda without granting `kinesis:PutRecord`?”**  
**A:** **No.** Lambda’s execution role must have an explicit `kinesis:PutRecord` permission on the stream ARN. The exam often includes a **“Missing permissions”** error traceback – the candidate must identify the missing `kinesis:PutRecord` in the IAM policy.

---

**Q: “Do I need a VPC endpoint for DynamoDB if my Lambda reads/writes to a DynamoDB table?”**  
**A:** **Yes, if the Lambda is in a private subnet**. Otherwise the Lambda will try to reach the public DynamoDB endpoint, which can cause **NAT gateway costs** and **additional latency**. The exam may ask you to **reduce cost** by adding a **Gateway Endpoint for DynamoDB** and attach a **policy** allowing `dynamodb:*` to the VPC endpoint.

---

**Q: “What’s the default behavior of a Kinesis stream’s retention period?”**  
**A:** **24 hours**. Many candidates forget you have to **explicitly set `RetentionPeriodHours`** if you need > 24 h. The exam scenario with a 30‑day replay will point to the wrong answer if you assume the default.

---

**Q: “When does Glue Crawler run by default?”**  
**A:** **On a schedule (default `cron(0 0 * * ? *)`) and on each `StartCrawler` API call**. It will **NOT** run automatically when new data lands unless you have a **`Crawler` event trigger** (e.g., via EventBridge). The exam may ask “How do you ensure the catalog is always up‑to‑date?” – the answer: “Run the crawler on a schedule and enable **`Crawler state`** for incremental updates”.

---

## Exam Focus Areas  

- **Ingestion & Transformation** (≈ 30 % of the exam)  
  - Choosing **Kinesis vs. MSR vs. SQS** for streaming vs. buffering.  
  - Configuring **Exactly‑Once**, **Shard scaling**, **Enhanced Fan‑Out**.  
  - Lambda event‑source mappings vs. **Kinesis Data Analytics SQL** for transformations.

- **Store & Manage** (≈ 30 % of the exam)  
  - **S3 data lake zones** (raw, curated, analytics).  
  - **Columnar formats** (Parquet/ORC) and **partitioning** for Athena/Redshift Spectrum.  
  - **Glue Data Catalog** – crawlers, versioning, and **Schema Registry**.  
  - **Redshift Spectrum** external tables and **COPY** best practices.

- **Operate & Support** (≈ 20 % of the exam)  
  - **Monitoring** CloudWatch metrics, alarms, and **log retention** policies.  
  - **IAM least‑privilege** for each service, **resource‑based policies**, **KMS key rotation**.  
  - **Cost‑optimization** – `OnDemand` vs. `Provisioned` vs. **Spot** for EMR/Fargate.

- **Design & Create Data Models** (≈ 20 % of the exam)  
  - **Star‑schema vs. snowflake** for Redshift.  
  - **Data modeling in the lake** (lakehouse) – using **Delta Lake** concepts in Athena.  
  - **Temporal tables** – handling CDC in Kinesis + S3 (`event_date` + `event_time`).  

*Each domain will have at least one **scenario‑based question** that forces you to select the right combination of services, IAM permissions, and configuration flags.*

---

## Quick Recap  

- **Data engineering on AWS = a set of **decoupled, managed services** you string together for “raw → trusted → analytics”.**  
- **Exactly‑once, sharding, and KMS are the three pillars you’ll be quizzed on.**  
- **Metrics are your early‑warning system** – watch `IteratorAge`, `WriteProvisionedThroughputExceeded`, `Errors`, and `KMSKeyUnencrypted`.  
- **Never forget IAM**: each service needs a **service‑linked role** plus **resource‑based policies** for cross‑service calls.  
- **Performance = shard count + Lambda concurrency + S3 file size + partitioning**. Tune early, alarm often.  

---  

## Blog & Reference Implementations  

| Resource | Why It Matters |
|----------|----------------|
| **AWS Blog – “Building Real‑Time Data Lakes on AWS”** (2023) | Walk‑through of Kinesis → Firehose → S3 → Athena pipeline with **schema evolution** – perfect for exam scenario. |
| **re:Invent 2022 – “Serverless Data Pipelines at Scale” (Session 102)** | Deep dive on **Lambda + Kinesis + DynamoDB** pattern; includes code snippets you can copy. |
| **AWS Workshop – “Streaming ETL with AWS Glue & Kinesis”** | Hands‑on lab (GitHub `aws-samples/glue-streaming-etl`) – teaches incremental crawlers and `KinesisFirehose` integration. |
| **Well‑Architected Framework – “Data Lake Lens”** | Provides the **security, reliability, cost‑optimization** checklist for the lake components. |
| **AWS Reference Architecture – “Analytics on Streaming Data”** (github.com/aws-samples/analytics-on-streaming-data) | Shows **cross‑region replication** and **FIPS‑compliant KMS** setup – exam loves cross‑account patterns. |
| **AWS Re:Invent 2023 – “Modernizing Legacy Data Pipelines with AWS Glue 3.0”** | Highlights **Spark 3.2, auto‑scaling, and data‑format optimizations** – useful for the Glue batch‑transform portion. |
| **AWS “Data Engineer Exam Guide” – PDF (2024)** | Official **exam domain breakdown** – keep it as your **cheat sheet** when reviewing this section. |

---  

*You now have a 45‑minute deep dive that you can deliver as a live walkthrough, a recorded lecture, or a set of lab exercises. Remember: the DEA‑C01 is **design‑first, debug‑later**. Master the why, and the exam will follow.*