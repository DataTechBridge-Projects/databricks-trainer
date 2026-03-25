WORKER_SYSTEM = """\
You are a senior AWS data engineering instructor writing content for a Udemy course.
Your writing style is precise, opinionated, and deeply practical — like an AWS Solutions Architect \
who has built and debugged real production pipelines. You explain not just *what* but *why* and *when*.\
"""

WORKER_PROMPT = """\
Write the complete course content for this section:

Section Title: {section}
Section {section_index} of {total_sections}
Course: {course_topic}
Target Audience: {course_audience}

Your content MUST include ALL of the following components, clearly labeled with markdown headings:

## {section}

### Overview
[3-4 paragraphs of deep conceptual explanation — explain the service's purpose, what problem it solves, \
and how it fits into the AWS data engineering ecosystem. Write like a technical book.]

### Core Concepts
[Detailed explanation of all key concepts with sub-sections. Include limits, quotas, and default \
behaviours that differ from what engineers expect.]

### Architecture / How It Works
[At least one ASCII or mermaid diagram in a code block showing architecture, data flow, or \
component relationships. Example:
```
+------------------+     +-------------------+     +-----------------+
|  Kinesis Stream  | --> |  Kinesis Firehose  | --> |   S3 (Parquet)  |
+------------------+     +-------------------+     +-----------------+
                                  |
                          +-------+-------+
                          |  Lambda Transform |
                          +---------------+
```
]

### AWS Service Integrations
[How this service connects to other AWS services. Cover at minimum:
- Which services feed data INTO this service and how
- Which services this service sends data TO and how
- IAM trust relationships required between services
- Common multi-service pipeline patterns that appear in the exam]

### Security
[Cover ALL of the following that apply to this service:
- IAM roles and resource-based policies (what permissions are needed and why)
- Encryption at rest (KMS key types, SSE-S3 vs SSE-KMS vs SSE-C where relevant)
- Encryption in transit (TLS, VPC endpoints)
- VPC and network isolation (PrivateLink, VPC endpoints, security groups)
- Audit logging (CloudTrail events, service-specific logging)
- Compliance considerations (FIPS, data residency, cross-account access)]

### Performance Tuning
[Specific, actionable tuning guidance:
- Configuration knobs with recommended values and reasoning
- Scaling patterns (horizontal vs vertical, auto-scaling triggers)
- Common bottlenecks and how to identify them
- Data format and partitioning recommendations for this service
- Cost vs performance trade-offs]

### Important Metrics to Monitor
[List the most critical CloudWatch metrics for this service with:
- Metric name (exact CloudWatch namespace and metric name)
- What it measures
- Threshold to alarm on and why
- What action to take when the alarm fires
Include at least 5-8 metrics.]

### Hands-On: Key Operations
[Step-by-step code examples using AWS CLI, boto3 (Python), or SQL as appropriate. \
Each block must have a comment explaining what it does and why. Cover the 2-3 most \
exam-relevant operations for this service.]

### Common FAQs and Misconceptions
[8-10 Q&A pairs covering:
- Questions that trip up engineers coming from on-premise or other clouds
- Exam-style trick questions with the correct answer and explanation
- Gotchas around pricing, limits, or default behaviour
Format as: **Q: ...** followed by **A: ...**]

### Exam Focus Areas
[Bulleted list of exactly what the AWS Certified Data Engineer Associate exam tests on this topic, \
mapped to the relevant exam domain (Ingestion & Transformation / Store & Manage / Operate & Support \
/ Design & Create Data Models)]

### Quick Recap
- [Key takeaway 1]
- [Key takeaway 2]
- [Key takeaway 3]
- [Key takeaway 4]
- [Key takeaway 5]
- [Key takeaway 6]

### Blog & Reference Implementations
[5-7 resources with a one-line description each:
- AWS Big Data Blog posts (aws.amazon.com/blogs/big-data/)
- AWS re:Invent session recordings relevant to this topic
- AWS Workshop Studio labs
- Well-Architected guidance
- GitHub reference architectures from aws-samples]

Be exhaustive. A presenter should be able to speak for 45-60 minutes from this section alone.\
"""

SUPERVISOR_PROMPT = """\
Create a Udemy course outline for: "{course_topic}"

Target audience: {course_audience}

REQUIRED sections (must appear, in this order):
1. Course Introduction — what the course covers, how to use it, prerequisites
2. Exam Overview and Strategy — AWS DEA-C01 exam format, four domains and weightings, question types, passing score, time management
3. AWS Data Architecture Foundations — data lake vs data warehouse vs lakehouse, AWS Well-Architected for analytics, S3 as the foundation (storage classes, lifecycle, versioning, encryption)
4. Data Ingestion — batch ingestion with AWS Glue, DMS, and DataSync; real-time ingestion with Kinesis Data Streams and Kinesis Firehose; event-driven ingestion with EventBridge and SQS
5. AWS Glue Deep Dive — Glue Data Catalog, crawlers, ETL jobs (PySpark and visual), Glue Studio, job bookmarks, Glue DataBrew for no-code transformation
6. Amazon S3 and Data Lake Design — partitioning strategies, S3 Select, S3 Inventory, optimizing for Athena and EMR, data formats (Parquet, ORC, Avro, JSON)
7. Amazon Athena — serverless SQL on S3, workgroups, query optimization, partitioning, federated queries, Athena for Apache Spark
8. Amazon Redshift — cluster vs Serverless, distribution styles, sort keys, COPY command, Redshift Spectrum, data sharing, Materialized Views, query optimization
9. Streaming Data with Kinesis and MSK — Kinesis Data Streams shards and consumers, Kinesis Data Analytics (Flink), Amazon MSK (Managed Kafka), MSK Connect, comparing streaming options
10. NoSQL and Purpose-Built Databases — DynamoDB (design patterns, streams, global tables), Amazon OpenSearch Service, Amazon ElastiCache, choosing the right database for analytics workloads
11. AWS Lake Formation and Data Governance — setting up Lake Formation, fine-grained access control, column and row-level security, data lineage with AWS Glue, AWS DataZone
12. Data Orchestration and Pipelines — AWS Step Functions for ETL workflows, Amazon MWAA (Managed Airflow), EventBridge Scheduler, Lambda for lightweight transformation, pipeline design patterns
13. Performance, Cost Optimization, and Monitoring — right-sizing EMR and Redshift, cost controls with S3 Intelligent-Tiering, CloudWatch metrics and alarms for data pipelines, AWS Cost Explorer for analytics workloads
14. Security, Compliance, and Networking — VPC endpoints for S3 and Redshift, IAM roles and resource-based policies, KMS encryption at rest and in transit, CloudTrail audit logging, FIPS compliance
15. Capstone and Exam Readiness — end-to-end pipeline architecture review, service selection decision trees, 30 practice questions with explanations, exam day tips

Rules:
- Cover AWS-native services only — no Databricks, no on-premise tools
- Each section must map clearly to one or more of the four DEA-C01 exam domains
- Do NOT include ML, SageMaker, or Bedrock sections — this is a Data Engineer cert, not ML
- Keep section titles concise and action/topic oriented
- Return ONLY a valid JSON array of the 15 section title strings. No markdown fences, no explanation.\
"""
