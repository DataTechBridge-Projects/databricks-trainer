# Data Ingestion

> **Section 4 of 15** – *AWS Certified Data Engineer Associate (DEA‑C01)*  
> **Audience:** Cloud engineers & developers who already know the core AWS services and want to ace the exam.

> **Teaching goal:** 45‑60 min of lecture + hands‑on.  The material is written as a technical book, with “why” and “when” embedded in every “what”.

---

## Overview  

Data ingestion is the *first mile* of any data‑centric architecture.  It is the set of processes that move raw events, logs, sensor readings, or transaction records from an origin—often an application, device, or upstream system—into a durable, query‑able store on AWS.  

* **Problem it solves:**  The classic “ETL bottleneck” and the “schema‑on‑write” explosion.  Instead of trying to ingest, clean, and transform everything up‑front, we push *immutable* blobs into a purpose‑built ingestion service and let downstream pipelines (Glue, Athena, Redshift) apply schema and enrichment lazily.  

* **Core role in the AWS data ecosystem:**  
  - **Streaming ingestion** – Kinesis Data Streams (KDS) and Kinesis Data Firehose provide durable, horizontally scalable ingest for high‑velocity data.  
  - **Batch ingestion** – S3 multipart uploads, AWS Snowball, and AWS DataSync are still part of “ingestion” because they get data *into* the lake.  
  - **Pattern:**  *Write‑once, read‑many* – once data lands in S3 (via Firehose or direct upload) it can be processed by Glue, Athena, EMR, Redshift Spectrum, etc.  No other service should be expected to “store” the raw data.  

* **When to pick KDS vs. Firehose:**  
  - Use **KDS** when you need *ordering* per shard, custom back‑pressure handling, or you want to fan‑out to multiple downstream consumers (e.g., Lambda, Flink, EMR).  
  - Use **Firehose** when you can tolerate “best‑effort” delivery to a sink (S3, Redshift, Elasticsearch) and you want built‑in buffering, data format conversion, and automatic scaling.  

Understanding these trade‑offs is a frequent exam focus because candidates often default to “use Firehose because it’s easier,” ignoring the ordering guarantees and consumer‑driven scaling that KDS provides.

---

## Core Concepts  

### 1. Shards, Sequences, and Partition Keys  

| Concept | What it is | Exam‑relevant nuance |
|---------|------------|----------------------|
| **Shard** | A single unit of throughput (up to 1 MB/s write, 2 MB/s read). You can have up to 500 shards per stream by default (soft limit). | You must **explicitly** set `ShardCount` when creating a stream; the service *does not* auto‑scale shards. Auto‑scaling is an optional feature (via Application Auto Scaling). |
| **Sequence Number** | Monotonically increasing identifier for each record within a shard. | Readers must track the `ShardIterator` and `SequenceNumber` to avoid missing or duplicate records. |
| **Partition Key** | Hash of the user‑supplied key that determines which shard a record lands in. | Choosing a high‑cardinality key (e.g., UUID) distributes evenly. Using a low‑cardinality key (e.g., “US”) can cause hot shards → throttling. |

### 2. Read/Write Consumers  

- **Producers** (EC2, Lambda, Kinesis Producer Library) can batch records (`PutRecord`, `PutRecords`).  
- **Consumers** (Lambda, Kinesis Consumer Library, Amazon EMR) obtain a **shard iterator** (`AT_SEQUENCE_NUMBER`, `LATEST`, `TRIM_HORIZON`) and poll for data.  

**Why it matters:**  The exam asks you to differentiate *push* vs *pull* models and to pick the right iterator (`AT_LATEST` for near‑real‑time, `TRIM_HORIZON` for replay).

### 3. Batching & Compression  

- **BatchPutRecords** can send up to 500 records (or 4 MB) per call.  
- **Kinesis Data Firehose** buffers records (default 5 min or 5 MB) before delivering.  

**Exam trap:**  Assuming Firehose delivers records instantly. In reality you must tune `BufferingHints` and understand that `CompressionFormat` (`UNCOMPRESSED`, `GZIP`, `Snappy`) impacts both cost and query latency.

### 4. Default Behaviours that Surprise  

| Behaviour | Default | Why it trips people |
|-----------|---------|---------------------|
| **Retention period** (KDS) | 24 hours (soft, configurable 1–7 days) | Engineers expect infinite retention; KDS will delete after the configured window, causing “missing data” errors if you don’t checkpoint. |
| **Stream encryption** (KDS) | Server‑side encryption with AWS‑managed KMS (SSE‑KMS) enabled automatically if you select a KMS key; otherwise none. | Many assume encryption is disabled by default—check your stream’s `EncryptionType`. |
| **Firehose delivery retries** | 3 retries, exponential backoff, then dead‑letter queue (S3) | Not idempotent by default—if you send duplicate IDs you may need to handle them downstream. |

### 5. Limits & Quotas (as of 2025‑11)  

- **Kinesis Data Streams**  
  - `ShardCount` soft limit: 500 (request increase to 5 000).  
  - `PutRecord` rate: 1,000 records/second per shard (burst up to 5,000).  
  - `GetRecords` payload: max 10 MB per 5 seconds per shard.  

- **Kinesis Data Firehose**  
  - Max record size: 1 MiB (compressed) per record.  
  - Delivery stream can deliver to S3, Redshift, Elasticsearch; each target has its own write limits (e.g., Redshift `COPY` max 2 GB per file).  

**Tip for the exam:**  When a question mentions “high write throughput > 1 GB/s per shard”, the answer is almost always “scale out the number of shards or use a different ingestion service (e.g., Amazon MSK, or SQS + Lambda)”.

---

## Architecture / How It Works  

Below is the canonical real‑time ingestion pipeline used in the exam (and in production at many companies).  It shows **Kinesis Data Streams → Lambda (transform) → S3 (Parquet) → Glue Catalog**.  

```mermaid
flowchart TD
    A[Producers (EC2 / IoT / SDKs)] -->|PutRecord / PutRecords| B[Kinesis Data Stream]
    B -->|Shard Iterator| C[Lambda (Transform & Enrich)]
    C -->|BatchPutRecords / Firehose| D[Kinesis Data Firehose]
    D -->|Deliver to S3 (Parquet + Glue Metadata)| E[Amazon S3 (Raw Zone)]
    E -->|AWS Glue Crawler| F[Glue Data Catalog (Catalog Zone)]
    F -->|Athena / Redshift Spectrum| G[Query Engine]
    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#bbf,stroke:#333,stroke-width:2px
    style D fill:#bfb,stroke:#333,stroke-width:2px
    style E fill:#ffb,stroke:#333,stroke-width:2px
```

**Explanation of the flow:**  

1. **Producers** push raw events directly to the KDS via the **Kinesis Producer Library (KPL)** or the low‑level `PutRecord` API. The `PartitionKey` dictates shard placement.  
2. **Shards** temporarily hold the data. KDS guarantees **ordered, immutable** storage for the retention window.  
3. **Lambda** (triggered by a **Kinesis Event Source Mapping**) consumes the stream, applies schema‑on‑read transformations (e.g., flatten JSON), and writes enriched records to **Firehose** using the **`FirehoseDeliveryStream`** API.  
4. **Firehose** buffers, optionally compresses (Snappy), converts to columnar format (Parquet/ORC), and writes to **S3** with a *date‑partitioned* prefix.  
5. **S3** becomes the *source of truth* for the data lake. A nightly **Glue Crawler** updates the catalog, enabling **Athena** or **Redshift Spectrum** to query the data instantly.  

*Key takeaway:*  This pattern separates *raw* ingestion (KDS) from *mass‑load* ingestion (Firehose) and gives you three points of independent scaling.

---

## AWS Service Integrations  

| Integration | Direction | Mechanism | Exam‑relevant nuance |
|-------------|-----------|-----------|----------------------|
| **Producers → KDS** | In | SDKs (`AWS SDK for Java/Python/Go`), KPL, `PutRecord`/`PutRecords` | Must use `DataPublisher` pattern for back‑pressure. |
| **KDS → Lambda** | In/Out | Event Source Mapping (consumer) | Lambda can be *concurrent* (default 5). To achieve > 1000 records/sec you need **parallelization factor** = `desiredThroughput / (batchSize * lambdaConcurrency)`. |
| **KDS → Firehose** | In/Out | Direct `PutRecord` to stream, then Firehose as consumer; or use **Firehose delivery stream** as a *destination* with *extended retention* (via `ExtendedRetryOptions`). | Firehose can *auto‑retry* on failure; you must configure *RetryOptions* and *DeadLetterConfiguration* to an S3 bucket. |
| **Firehose → S3** | Out | Buffering → Optional **Glue Data Catalog** integration (auto‑update) | S3 prefixes can be **partitioned by `year=`, `month=`, `day=`** using *record conversion* options. |
| **Firehose → Redshift / Elasticsearch** | Out | Use **`ExtendedS3DestinationConfiguration`** for extra metadata, or **`DataStructure`** for `JSON` vs `PARQUET`. | For Redshift, Firehose uses **`INSERT`** via the Redshift `COPY` command; you must supply `Role` ARN with `redshift.amazonaws.com` trust. |
| **Glue Crawler → Catalog** | In | Periodic inspection of S3 prefixes | Must have **`AmazonS3ReadOnlyAccess`** on the bucket and **`AWSGlueServiceRole`** with `glue:BatchCreatePartition` etc. |
| **CloudWatch Alarms → SNS** | Out | CloudWatch → SNS → Lambda/Email | Use **`insights`** on KDS for real‑time shard health; alarms should trigger on `ReadProvisionedThroughputExceeded` **and** `WriteProvisionedThroughputExceeded`. |

### Multi‑service pipeline patterns that appear on the exam  

1. **KDS → Kinesis Analytics (SQL) → S3** – For real‑time aggregation, you’ll be asked to choose the correct **`Kinesis Analytics`** (SQL) version and to understand that it can only read *up to 1 MB/s per stream* (so you may need multiple streams).  
2. **Firehose → S3 → Athena → QuickSight** – A classic *batch* ingestion path; the exam may ask about **`External Table`** definitions in Athena and the need for **`Table properties`** to enable *partition projection*.  
3. **KDS → Lambda → Step Functions → S3** – For complex fan‑out and stateful transformations (e.g., deduplication across shards). Step Functions can orchestrate Lambda retries, and you can store the **state machine ARN** in the stream’s **`Enhanced Monitoring`**.  

---

## Security  

### IAM Roles & Resource Policies  

| Permission | Needed By | Why |
|------------|-----------|-----|
| `kinesis:PutRecord` / `kinesis:PutRecords` | Producers (EC2, Lambda, EC2 Instance Role) | Write raw data to the stream. |
| `kinesis:GetShardIterator` + `kinesis:DescribeStream` | Consumers (Lambda, KCL) | Retrieve shard metadata and iterators. |
| `kinesis:SubscribeToShard` (KCL) | KCL processes | Pull records in the *pull* model. |
| `firehose:PutRecord` | Producers that send directly to a delivery stream (rare). | |
| `firehose:DeliverData` (target) | Firehose to S3 / Redshift | Destination service calls. |
| `kms:Decrypt` / `kms:Encrypt` | Streams with SSE‑KMS | Must have `kms:GenerateDataKey*` for the CMK. |
| `logs:CreateLogGroup` / `logs:CreateLogStream` | Lambda functions consuming KDS | For structured logging of errors. |

**Trust Relationships:**  

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "kinesis.amazonaws.com" },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": { "Service": "lambda.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

- **Kinesis** (stream) uses a *resource‑based policy* (`kinesis:PutRecord`) to allow the *producer role* to write.  
- **Lambda** needs a separate *execution role* (least privilege) with `kinesis:GetRecords`, `kinesis:DescribeStreamSummary`, and `firehose:PutRecord`.  

### Encryption  

| Layer | Options | When to use |
|-------|---------|-------------|
| **At Rest (S3)** | SSE‑S3 (AES‑256), SSE‑KMS (AWS‑managed or Customer‑managed), SSE‑C (customer-provided keys) | - **SSE‑KMS** for compliance (FIPS) because you can enforce IAM key policy and audit via CloudTrail. |
| **At Rest (KDS / Firehose)** | SSE‑KMS (default for KDS if you enable encryption) | Use customer‑managed CMK for audit. |
| **In Transit** | TLS 1.2 enforced on all SDK endpoints. For VPC‑bound workloads you can enable **VPC Endpoint for Kinesis Data Streams** (`com.amazonaws.<region>.kinesis`) which terminates TLS inside the VPC. | Avoid data exfiltration; enables *PrivateLink* to keep traffic off the public internet. |
| **Lambda → Firehose** | Uses the SDK over HTTPS (TLS). Ensure the **`aws:SourceVpce`** condition key is used if you require traffic to be **PrivateLink‑only**. | Good for PCI‑DSS workloads. |

### VPC & Network Isolation  

- **Kinesis Data Streams** does **not** support in‑VPC endpoints directly (as of 2025) – traffic always goes over the public internet, but you can protect it with **VPC endpoints for the Kinesis API** and **Security Group** on the associated ENIs.  
- **Kinesis Data Firehose** *does* support **VPC Delivery** (target can be an S3 bucket in a VPC via **VPC Endpoint for S3**).  When you enable **`DeliveryStreamEncryptionConfig`** with a **`VpcConfig`**, Firehose creates ENIs in your subnets and **does not expose traffic to the internet**.  

**Gotcha:**  If you enable VPC for Firehose *and* also enable **`Redshift`** as a destination, Redshift must be in the same VPC and have an **`S3`** IAM role trust that allows the Firehose ENI to write.  

### Audit Logging  

| Service | CloudTrail event | What to watch |
|---------|------------------|----------------|
| **Kinesis Data Streams** | `PutRecord`, `PutRecords`, `GetRecords`, `DescribeStream` | Spike in `PutRecords` → possible data injection attack; `GetRecords` > 100 k/sec may indicate a DoS. |
| **Kinesis Data Firehose** | `DeliveryStreamCreated`, `DeliveryStreamRecordConversionConfiguration` | Changes to `ExtendedS3DestinationConfiguration` (e.g., new prefix) may indicate a malicious config change. |
| **Lambda (Kinesis consumer)** | `LambdaInvoke` with `SourceArn` = stream ARN | Unexpected invocations could be a rogue function. |
| **S3 (target bucket)** | `PutObject`, `PutObjectTagging`, `DeleteObject` | Look for objects written outside of the expected time window (e.g., nightly batch). |

Enable **AWS Config** with the rule `kinesis-streams-encrypted` and `firehose-delivery-stream-logging-enabled` to get continuous compliance checks.

### Compliance & Residency  

- **FIPS 140‑2 endpoints** – Use `*.amazonaws.com` for standard AWS, or `*.aws-gov.com` for GovCloud. Ensure your SDK/CLI uses the **`aws-region.amazonaws.com`** endpoint; mixing endpoints leads to *unencrypted* traffic to non‑FIPS endpoints.  
- **Data residency** – S3 bucket location (`us-east-1` vs `eu-west-1`) determines where Firehose lands data. You cannot change the region after the bucket is created; you must create a *new* delivery stream pointing to a bucket in the desired region.  
- **Cross‑account access** – Use **`ResourceBasedPolicy`** on the Kinesis stream to allow a role from another account to `PutRecord`. The policy must include `Principal: {"AWS": "arn:aws:iam::<account-id>:root"}` and `Action: "kinesis:PutRecord"`; otherwise you’ll see `AccessDenied` errors that are impossible to debug without looking at the resource policy.  

---

## Performance Tuning  

### 1. Stream Configuration Knobs  

| Parameter | Recommended Value | Rationale |
|-----------|-------------------|-----------|
| **`ShardCount`** (initial) | **`ceil(PeakWriteRate / 1 MB/s) + 1`** | Gives headroom for burst and for the default 5‑minute scale‑out cooldown. |
| **`RetentionPeriodHours`** | **24‑48** (default 24) | Longer retention enables replay but raises storage cost. For replay‑heavy analytics, bump to 72 h. |
| **`EnhancedMonitoring`** | `Enable` (for `ReadProvisionedThroughputExceeded` & `WriteProvisionedThroughputExceeded`) | Allows CloudWatch to emit **`EnhancedMetric`** granularity (1‑second) for rapid auto‑scaling. |
| **`StreamModeDetails`** (`PROVISIONED` vs `ON_DEMAND`) | **`ON_DEMAND`** for unpredictable spikes, **`PROVISIONED`** with **Auto Scaling** for predictable, high‑throughput workloads. | Exam often tests *difference* – `ON_DEMAND` automatically adds shards; `PROVISIONED` needs explicit scaling. |

### 2. Auto Scaling  

```bash
aws application-autoscaling put-scaling-policy \
  --service-namespace kinesis \
  --resource-id stream/<stream-name>/shardId/<shard-id> \
  --scalable-dimension kinesis:stream:WriteCapacityUnits \
  --policy-name target-tracking-write-throughput \
  --target-tracking-scaling-policy-configuration file://policy.json
```

**policy.json (example):**

```json
{
  "TargetValue": 80.0,
  "PredefinedMetricSpecification": {
    "PredefinedMetricType": "KinesisStreamWriteProvisionedThroughput"
  },
  "ScaleOutCooldown": 60,
  "ScaleInCooldown": 300
}
```

- **Why 80 %?**: AWS recommends not hitting 100 % to avoid throttling on the *first* scale‑out cycle.  

### 3. Scaling Patterns  

| Pattern | When to use | How to implement |
|---------|-------------|------------------|
| **Horizontal (shard) scaling** | Sustained > 1 MB/s write per shard. | Use **Application Auto Scaling** for `ON_DEMAND` streams (scale‑out automatically) or manually `UpdateShardCount` for `PROVISIONED`. |
| **Vertical (producer)** | You have a single Lambda writing to KDS and hitting the 1 MB/s shard limit. | Increase **`BatchSize`** in the Kinesis Producer Library; ensure the `Data` payload is not larger than 1 MiB per record. |
| **Parallel Consumer (Lambda)** | You need > 10 k records/sec read throughput. | Set `MaximumConcurrency` in the Lambda event source mapping (default 5) and increase `BatchSize` to 100. |
| **Buffering in Firehose** | To reduce S3 PUT cost and improve write performance. | Adjust `BufferingHints` (`SizeInMBs: 5`, `IntervalInSeconds: 300`) and enable `CompressionFormat: GZIP`. |

### 4. Bottlenecks & Detection  

- **Throttling:** `ThrottledRequests` (KDS metrics) > 0 → increase shards or move to `ON_DEMAND`.  
- **Iterator Age:** `GetRecords.IteratorAgeMilliseconds` > 30 000 ms indicates lag; either consumer is too slow or shard throttling occurs.  
- **Hot Partition:** Monitor `PutRecord.Successes` per `PartitionKey`; a single key dominating shard throughput (> 80 % of shard’s 1 MB/s) → split key or add a **salt**.  

**Identification tip:**  Use **`Kinesis Data Analytics`** to query `SHARD_ID` and `PUT_RECORDS` metrics; a heatmap in CloudWatch dashboards will highlight hot shards.

### 5. Data Formats & Partitioning  

- **Firehose** supports `JSON`, `CSV`, `Parquet`, `ORC`.  
  - **Parquet** + **Snappy** reduces storage by ~70 % and enables predicate pushdown in Athena.  
  - **Columnar format** is mandatory for *time‑series* where you’ll query by date.  

- **S3 Partitioning Scheme** (recommended):  

  ```
  s3://my-data-lake/raw/{service}/{year=YYYY}/{month=MM}/{day=DD}/{shardId}
  ```

- **Why:** Athena can auto‑detect partitions if you enable **`Table Properties` → `exTERNAL_TABLE_PROPERTIES`** with `skip.header.line.count=1` (if needed) and `skip.unknown.fields=true`.  

### 6. Cost vs Performance Trade‑offs  

| Decision | Cost Impact | Performance Impact |
|----------|-------------|---------------------|
| **`ON_DEMAND`** | $0.015 per million records written + $0.004 per shard‑hour (auto‑scaled) | Excellent for unpredictable spikes; auto‑scales instantly. |
| **`PROVISIONED` + Auto Scaling** | Predictable $ per shard hour; lower per‑record cost at scale (≥ 10 k rps) | Requires proactive sizing; can lead to over‑provisioning if not tuned. |
| **`Buffer Size 5 MB`** | Higher S3 PUT cost (larger objects) but fewer PUTs → lower API cost. | Improves write latency for Firehose (writes happen after buffer is full). |
| **`Parquet + Compression`** | Higher CPU usage (but negligible on Firehose) + lower storage. | Enables fast columnar scans in Athena (up to 10× faster). |

**Exam tip:**  If a question asks “Your pipeline must ingest 200 k records/sec with sub‑second latency and you have 10 GB per hour of data. Which ingestion service and config will keep cost under $200/month?” → answer: **Kinesis Data Streams in ON_DEMAND** (or provisioned with 200 shards) **plus Firehose to S3 with Parquet+Snappy** – both provide predictable costs and meet latency.

---

## Important Metrics to Monitor  

All metrics live under the namespace **`AWS/Kinesis`** (for KDS) and **`AWS/KinesisFirehose`** (for Firehose).  Below are the *must‑track* ones for the exam.

| Metric Name | Namespace | What It Measures | Threshold (Alarm) | Action on Alarm |
|-------------|-----------|------------------|-------------------|-----------------|
| **`PutRecord.Successes`** | `AWS/Kinesis` | Successful writes per stream (total). | `< 80%` of expected write rate for 5 min (e.g., < 800k/min when you target 1 M/min). | Investigate throttling; consider scaling shards or enabling auto‑scaling. |
| **`PutRecord.ThrottledRequests`** | `AWS/Kinesis` | Number of records rejected due to provisioned throughput. | `> 0` for 2 consecutive 1‑minute periods. | Immediately scale out (if `PROVISIONED`) or switch to `ON_DEMAND`. |
| **`GetRecords.IteratorAgeMilliseconds`** | `AWS/Kinesis` | Age of the oldest record that a consumer has not yet processed. | `> 30,000 ms` (30 s) for any shard. | Alert consumer (Lambda) may be under‑provisioned; increase concurrency or batch size. |
| **`ReadProvisionedThroughputExceeded`** | `AWS/Kinesis` | Read throttling events per stream. | `> 0` over 2‑minute window. | Scale out read capacity or switch to `ON_DEMAND`. |
| **`WriteProvisionedThroughputExceeded`** | `AWS/Kinesis` | Write throttling events per stream. | `> 0` over 2‑minute window. | Same as `PutRecord.ThrottledRequests`. |
| **`ShardIteratorAge`** | `AWS/Kinesis` (via custom metric `ShardIteratorAge` using CloudWatch metric math) | Time since the iterator was advanced for a given shard. | `> 1,000,000 ms` (15 min). | Investigate downstream pipeline; could be data loss. |
| **`DeliveryToS3.SuccessfulRequests`** (Firehose) | `AWS/KinesisFirehose` | Successful deliveries from Firehose to S3. | `< 95%` of total records delivered over 10 min. | Check S3 permissions or bucket health. |
| **`DeliveryToS3.FailedRecords`** (Firehose) | `AWS/KinesisFirehose` | Count of records that failed after retries (DLQ). | `> 0` for > 1 min. | Review DLQ bucket for error payload; adjust data format. |
| **`Firehose.RecordSizeMetric`** | `AWS/KinesisFirehose` | Average size of records delivered to S3 (MiB). | `> 4 MiB` (exceeds 1 MiB per record limit). | Reduce batch size in Lambda; consider compression. |

> **How to set up alarms (CLI snippet):**  

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "KDS-Write-Throttling" \
  --metric-name WriteProvisionedThroughputExceeded \
  --namespace AWS/Kinesis \
  --statistic Sum \
  --period 60 \
  --threshold 0 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --evaluation-periods 2 \
  --actions-enabled \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:kinesis-ops
```

---

## Hands-On: Key Operations  

> **Goal:** Demonstrate the three most exam‑relevant operations for *Kinesis Data Streams*: (1) **Create a stream with auto‑scaling**, (2) **Write records from Python (boto3)**, (3) **Consume with a Lambda event source**.

### 1️⃣ Create a provisioned stream + auto‑scaling  

```bash
# 1️⃣ Create the stream (default retention 24h)
aws kinesis create-stream \
  --stream-name order-events \
  --shard-count 4 \
  --retention-period-hours 48 \
  --region us-east-1

# 2️⃣ Enable enhanced monitoring (required for auto‑scaling)
aws application-autoscaling register-scalable-target \
  --service-namespace kinesis \
  --resource-id stream/order-events \
  --scalable-dimension kinesis:stream:WriteCapacityUnits \
  --min-capacity 4 \
  --max-capacity 40

# 3️⃣ Create a target‑tracking scaling policy (80% target)
cat > policy.json <<'EOF'
{
  "TargetValue": 80.0,
  "PredefinedMetricSpecification": {
    "PredefinedMetricType": "KinesisStreamWriteProvisionedThroughput"
  },
  "ScaleOutCooldown": 60,
  "ScaleInCooldown": 300
}
EOF

aws application-autoscaling put-scaling-policy \
  --service-namespace kinesis \
  --resource-id stream/order-events \
  --scalable-dimension kinesis:stream:WriteCapacityUnits \
  --policy-name write-throughput-target-tracking \
  --scaling-policy-updatable scalable-property-target-tracking \
  --policy-config file://policy.json
```

**Why:**  The `CreateStream` call **does not** enable auto‑scaling; you must *register* the stream as a scalable target and then create a `TargetTrackingScalingPolicy`.  Forgetting step 2 is a classic exam trap.

### 2️⃣ PutRecords with boto3 (Python) – note batch limits  

```python
import boto3, json, uuid, time

kinesis = boto3.client('kinesis', region_name='us-east-1')
stream_name = 'order-events'

def generate_record(seq):
    """Simple order payload – JSON, partitioned by UUID prefix."""
    return {
        "order_id": str(uuid.uuid4()),
        "user_id": f"user-{seq % 1000}",
        "amount": round(100 + 1000 * (0.1 ** seq % 10), 2),
        "ts": int(time.time() * 1000)
    }

def put_batch(batch_num, start_seq):
    records = []
    for i in range(500):  # 500 records = ~5 MB payload (still < 4 MB)
        seq = start_seq + i
        payload = json.dumps(generate_record(seq)).encode('utf-8')
        shard_key = f"user-{seq % 200}"   # 200 distinct keys -> good distribution
        records.append({"Data": payload, "PartitionKey": shard_key})

    response = kinesis.put_records(Records=records, StreamName=stream_name)
    # Simple retry loop for demo
    while response['FailedRecordCount'] > 0:
        # In production you would check error messages and retry specific records
        print(f"Batch {batch_num} failed {response['FailedRecordCount']} records")
        response = kinesis.put_records(Records=records, StreamName=stream_name)
    print(f"✅ Batch {batch_num} sent ({len(records)} records)")

# Example: send 5 batches, 500 records each = 2,500 records total
for b in range(5):
    put_batch(batch_num=b+1, start_seq=b*500)
```

**Key points:**  

- **`PutRecords`** is the batch API (up to 500 records or 4 MiB).  
- Partition keys must be chosen wisely; the example uses a *salted* key to avoid hot shards.  
- The retry loop is a **must** for production because Kinesis can occasionally return `ProvisionedThroughputExceededException` for individual records.  

### 3️⃣ Lambda consumer (Kinesis Event Source Mapping)  

```python
import json, boto3, os

s3 = boto3.client('s3')
DEST_BUCKET = os.getenv('DEST_BUCKET', 'my-data-lake-raw')
DEST_PREFIX = 'kinesis/ingest/'

def lambda_handler(event, context):
    """
    Lambda triggered by Kinesis (via Event Source Mapping).  Each batch
    is flattened, partitioned by year/month/day, and written as a
    single Parquet file to S3 (leveraging AWS Glue Catalog for schema).
    """
    for rec in event['Records']:
        # 1️⃣ Decode and deserialize
        payload = json.loads(rec['kinesis']['data'].decode('utf-8'))

        # 2️⃣ Enrich – add a processing timestamp
        payload['processed_ts'] = int(time.time() * 1000)

        # 3️⃣ Serialize to Parquet (in‑memory for demo)
        import pyarrow as pa, pyarrow.parquet as pq
        table = pa.Table.from_pydict(payload)
        output = pq.write_table(table, f'/tmp/record.parquet')

        # 4️⃣ Upload to S3 with partitioning
        with open(output, 'rb') as f:
            s3_key = f"{DEST_PREFIX}{payload['ts'] // 1000 // 10000:04d}/{payload['ts'] // 1000 % 100:02d}/{payload['ts'] // 1000 % 1000:02d}/{payload['order_id']}.parquet"
            s3.upload_fileobj(f, DEST_BUCKET, s3_key)

    return {'statusCode': 200, 'body': 'OK'}
```

**Deploy steps (CLI):**  

```bash
# 1️⃣ Create S3 bucket if not exists
aws s3api create-bucket --bucket my-data-lake-raw --region us-east-1

# 2️⃣ Package Lambda (zip)
zip lambda_ingest.zip lambda_function.py

# 3️⃣ Create the function
aws lambda create-function \
  --function-name KinesisIngestProcessor \
  --runtime python3.11 \
  --handler lambda_function.lambda_handler \
  --role arn:aws:iam::123456789012:role/KinesisIngestRole \
  --zip-file fileb://lambda_ingest.zip \
  --timeout 30 \
  --memory-size 256

# 4️⃣ Attach Kinesis as event source (parallelization 2, batch size 100)
aws lambda create-event-source-mapping \
  --function-name KinesisIngestProcessor \
  --event-source-arn arn:aws:kinesis:us-east-1:123456789012:stream/order-events \
  --batch-size 100 \
  --maximum-batching-window-in-seconds 5 \
  --starting-position LATEST
```

**Why this pattern shows up in the exam:**  

- Demonstrates **Lambda ⇄ Kinesis** integration (requires proper IAM – see below).  
- Shows **partitioning** logic that ties directly to *S3 partition projection* and *Athena query performance*.  
- Includes **in‑memory Parquet conversion**, a technique the exam expects you to know for cost‑effective data lakeing.

#### IAM for the Lambda  

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kinesis:GetRecords",
        "kinesis:DescribeStream",
        "kinesis:GetShardIterator",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:kinesis:us-east-1:123456789012:stream/order-events"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectTagging",
        "s3:GetBucketLocation"
      ],
      "Resource": "arn:aws:s3:::my-data-lake-raw/*"
    }
  ]
}
```

- **`logs:*`** for debugging (always on).  
- **`s3:PutObject`** to the raw bucket (must have `kms:Decrypt` if bucket uses SSE‑KMS).  

---

## Common FAQs and Misconceptions  

**Q1 – “Can I use Kinesis Data Streams to ingest files directly (e.g., .CSV, .avro) without a producer app?”**  
**A:** No. KDS only accepts *binary* records via `PutRecord` APIs. For bulk file ingestion you should use **S3 multipart upload**, **AWS Snowball**, or **Firehose** which can *auto‑convert* file formats. Using KDS for large files will incur massive `PutRecord` call overhead and will quickly hit the 1 MB/record limit.  

---

**Q2 – “Why does my Lambda reading from Kinesis keep getting `IteratorAge` > 5 min even though I see data in the console?”**  
**A:** Most likely the **shard iterator is stale** because the consumer has not called `GetRecords` within the *`NewIterator`* timeout. Check that the Lambda’s **batch size** is > 0 and that **`MaximumBatchingWindowInSeconds`** is not too high (the default 300 s can cause lag). Also verify that the Lambda’s **execution role** has permission for `kinesis:GetRecords`; otherwise the Lambda silently fails and the iterator never advances.  

---

**Q3 – “Is the default Kinesis Data Stream encryption with AWS‑managed KMS a security risk?”**  
**A:** Not inherently. The default SSE‑KMS key (`aws/kinesis`) is owned by the **AWS account** and is **not accessible by other accounts** (resource‑based policy). However, it **cannot be disabled** without creating a **customer‑managed CMK** and updating the stream’s `EncryptionType` to `KMS`. For PCI‑DSS you must have a **customer‑managed CMK** with rotation enabled.  

---

**Q4 – “Do I need to configure VPC endpoints for Kinesis Data Streams to make it secure?”**  
**A:** *Optional*. KDS traffic goes over the public internet but is always TLS‑protected. If you have a strict **no‑internet** policy you can create a **VPC Interface Endpoint** for `kinesis` and then **disable public access** to the stream’s security group. Remember that Firehose *delivery* to S3 via VPC requires **both** a **VPC endpoint for S3** *and* **ENI in each subnet** (cost $0.01 per ENI‑hour).  

---

**Q5 – “What’s the difference between `ShardIterator` types `TRIM_HORIZON` and `AT_SEQUENCE_NUMBER`?”**  
**A:**  

- `TRIM_HORIZON` starts reading from the **oldest available record** (the farthest back retained data). Good for *reprocessing* a stream.  
- `AT_SEQUENCE_NUMBER` (e.g., `LATEST` or a specific sequence) reads from a *specific* point – the most common pattern for *real‑time* pipelines.  

The exam often asks you to choose `TRIM_HORIZON` for **data lake backfill** and `LATEST` for **real‑time alerting**.  

---

**Q6 – “Do I have to pay for the Kinesis **shard** even if I never write any records?”**  
**A:** Yes. A **provisioned** stream always incurs a **shard‑hour** charge. `ON_DEMAND` pricing is per‑record (no shard cost), but the **request rate** is higher per record (e.g., 5× the price). For *infrequent* batch ingestion (once per day), use a **batch upload** to S3 instead of KDS.  

---

**Q7 – “Can I use the same Kinesis stream for both *real‑time* Lambda processing and *batch* Firehose delivery?”**  
**A:** Absolutely – this is the **dual‑consumer** pattern. The same shard can be read by **multiple consumers** simultaneously; however, each consumer **must maintain its own iterator**. A common mistake is to use the *same* Lambda function to both read and write back to the stream – this creates a *feedback loop* and can cause **exponential back‑off throttling**.  

---

**Q8 – “What’s the maximum size of a `PutRecord` payload and why does it matter?”**  
**A:** **1 MiB** (after base64‑decoding). The limit is per record *and* per shard – 5 000 records per second per shard, but each record is capped at 1 MiB. Exceeding this returns `InvalidArgumentException`. This forces you to **chunk large files** (e.g., split a 500 MB CSV into 500 KB records) *or* use **Firehose** which can ingest larger files via the *`ExtendedS3DestinationConfiguration`* that batches internally.  

---

## Exam Focus Areas  

| Exam Domain | Sub‑topic | What the exam will test on this section |
|-------------|-----------|------------------------------------------|
| **Ingestion & Transformation** | Design & implement a real‑time ingestion pipeline | Choose KDS vs Firehose, select shard count, configure partitioning, and map the pipeline to downstream services (Glue, Athena). |
| **Ingestion & Transformation** | Optimize costs and performance for streaming data | Calculate shard requirements from expected write throughput, apply auto‑scaling, and decide between `PROVISIONED` vs `ON_DEMAND`. |
| **Store & Manage** | Store ingested data in a columnar format | Identify Parquet vs JSON vs CSV for S3; justify partitioning scheme for Athena query performance. |
| **Operate & Support** | Monitor Kinesis health & troubleshoot throttling | Read CloudWatch metrics, interpret alarm thresholds, and execute scaling actions. |
| **Design & Create Data Models** | Model data for downstream analytics | Explain how ingestion order (KDS → Firehose → S3) supports a *lambda architecture* (speed layer + batch layer). |

---

## Quick Recap  

- **Real‑time vs batch ingestion:**  KDS gives *ordered, low‑latency* streams; Firehose gives *managed, buffered* delivery to S3/Redshift.  
- **Shards are the budget for throughput:**  *1 MB/s write* per shard; plan for *burst* and *auto‑scaling*; never forget to enable **enhanced monitoring**.  
- **IAM & encryption are inseparable from design:**  Use customer‑managed KMS keys, enforce VPC endpoints, and give least‑privilege roles.  
- **Metrics are your early‑warning system:**  Watch `WriteProvisionedThroughputExceeded`, `IteratorAge`, and `PutRecord.ThrottledRequests`.  
- **Hands‑on ops:**  Create a stream, write with `PutRecords`, and consume with Lambda – this trio is a *must‑know* for the exam.  
- **Integration patterns:**  Stream → Lambda (real‑time) **and** Stream → Firehose (batch).  Both must be idempotent.  
- **Cost:**  Provisioned shards cost $ per hour; ON_DEMAND costs $ per million records. Choose the model that matches the *predictability* of your traffic.  

---

## Blog & Reference Implementations  

| Resource | Why it matters for this section |
|----------|----------------------------------|
| **AWS Big Data Blog – “Real‑time Data Ingestion Patterns on Amazon Kinesis”** (2024‑03) | Walk‑through of the exact *KDS → Lambda → Firehose → S3* pattern with code. |
| **Re:Invent 2023 – “Building Scalable, Resilient Ingestion Pipelines with Kinesis”** (Session 3289) | Deep dive on shard sizing, auto‑scaling, and monitoring. |
| **AWS Workshop Studio – “Build a Serverless Real‑Time Analytics Pipeline”** | Hands‑on lab that wires a Kinesis stream to S3 and Athena; includes a ready‑to‑run CloudFormation template. |
| **AWS Well‑Architected – “Data Analytics Lens: Ingestion & Storage”** | Discusses cost‑performance trade‑offs of different ingestion services. |
| **aws-samples GitHub – “kinesis-data-stream-ingestion”** (Python boto3 examples) | Production‑grade pattern with error handling, DLQ, and IAM least‑privilege. |
| **AWS Documentation – “Kinesis Data Streams Developer Guide”** (Latest) | Always the go‑to reference for limits, API nuances, and service quotas. |
| **AWS Blog – “From Kinesis to S3: Optimizing for Parquet and Athena”** (2025‑02) | Shows why columnar formats, buffer hints, and partitioning matter for downstream cost. |

--- 

*End of Section 4 – Data Ingestion* 🎉  

You now have the **conceptual depth, operational playbook, and exam‑focused nuggets** to dominate any question on real‑time ingestion, and you can spin up the sample pipeline in under ten minutes. Good luck, and remember: **measure, monitor, and then scale**. 🚀