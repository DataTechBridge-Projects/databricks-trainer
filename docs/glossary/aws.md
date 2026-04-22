# AWS Glossary

A comprehensive reference of AWS services, concepts, and terminology — sorted alphabetically. Written for Solution Architects who need to understand what each term means, why it matters, and how to talk about it in a customer conversation.

---

## A

### ACM (AWS Certificate Manager)
A managed service that provisions, deploys, and renews SSL/TLS certificates. Eliminates the operational burden of manually tracking certificate expiration dates and rotating them across load balancers, CloudFront distributions, and API Gateway endpoints. Free for certificates used with AWS services; customers pay only for private CA certificates.

### Amazon Athena
A serverless, interactive query service that lets you analyze data stored in Amazon S3 using standard SQL. There is no infrastructure to manage and no cluster to provision — you simply point Athena at an S3 location, define a schema in the AWS Glue Data Catalog, and start querying. You pay only for the data scanned per query (roughly $5/TB), which makes it extremely cost-effective for ad hoc analysis. Performance can be dramatically improved by using columnar formats (Parquet, ORC) and partitioning data by date or region — techniques that reduce the amount of data scanned per query.

### Amazon Aurora
A fully managed, MySQL- and PostgreSQL-compatible relational database engine built by AWS. It delivers up to five times the throughput of standard MySQL at one-tenth the cost of commercial databases like Oracle. Aurora separates compute and storage — the storage layer automatically grows in 10 GB increments up to 128 TB and replicates data six ways across three Availability Zones. Aurora Serverless v2 takes this further by automatically scaling compute capacity up or down in fine-grained increments, making it well-suited for applications with intermittent or unpredictable workloads.

### Amazon CloudFront
A global Content Delivery Network (CDN) with over 400 Points of Presence (PoPs) worldwide. It caches static and dynamic content at edge locations close to end users, dramatically reducing latency and offloading origin servers. Integrated natively with S3 (for static sites), ALB, and API Gateway. CloudFront also doubles as a security layer — it integrates with AWS WAF, Shield Advanced, and AWS Certificate Manager to protect applications at the edge before traffic ever reaches the origin.

### Amazon CloudWatch
The primary observability service for AWS. It collects metrics, logs, and traces from virtually every AWS service and lets you set alarms, build dashboards, and trigger automated actions based on thresholds. CloudWatch Logs Insights provides an interactive query language for log analysis. Container Insights, Lambda Insights, and Application Insights are purpose-built extensions for specific compute types. Think of it as the single pane of glass for operational health across an AWS environment.

### Amazon Comprehend
A Natural Language Processing (NLP) service that uses machine learning to extract meaning from unstructured text. It can identify entities (people, places, organizations), sentiment (positive/negative/neutral/mixed), key phrases, language, and PII (Personally Identifiable Information). No ML expertise required — you call an API with text and get structured results back. Common use cases include analyzing customer reviews, classifying support tickets, and redacting PII from documents.

### Amazon DynamoDB
A fully managed, serverless NoSQL key-value and document database. It delivers single-digit millisecond performance at any scale and is designed for workloads where read/write throughput must remain consistent even as data volume grows to hundreds of terabytes. DynamoDB uses a primary key (partition key alone, or partition key + sort key) to uniquely identify items. DynamoDB Streams captures item-level change events, enabling event-driven architectures. Global Tables provide multi-region, active-active replication for disaster recovery and low-latency global access.

### Amazon EC2 (Elastic Compute Cloud)
The foundational virtual server service in AWS. EC2 instances come in dozens of families optimized for different workloads — general purpose (M/T family), compute optimized (C family), memory optimized (R/X family), storage optimized (I/D family), and accelerated computing (P/G/Inf family for GPU/ML). EC2 is the "escape hatch" when managed services don't fit a workload, but it requires the customer to manage the OS, patching, and scaling. Pricing models include On-Demand, Reserved Instances (1 or 3 year), Spot (up to 90% discount for interruptible workloads), and Savings Plans.

### Amazon ECS (Elastic Container Service)
A fully managed container orchestration service for running Docker containers. ECS removes the need to manage a control plane — AWS handles scheduling, placement, and health checks. Containers can run on EC2 instances (you manage the fleet) or on AWS Fargate (serverless — no servers to manage at all). ECS integrates natively with IAM, ALB, CloudWatch, and ECR (Elastic Container Registry), making it the lowest-friction path to running containers on AWS.

### Amazon EKS (Elastic Kubernetes Service)
A managed Kubernetes service that runs the Kubernetes control plane across multiple Availability Zones. Customers bring their own worker nodes (EC2 or Fargate) but AWS handles etcd, the API server, and control plane upgrades. EKS is the right choice for organizations already invested in Kubernetes tooling and CNCF ecosystem (Helm, Argo, Flux). It comes with more operational overhead than ECS but provides full Kubernetes compatibility and portability. EKS Anywhere extends the same control plane to on-premises environments.

### Amazon EMR (Elastic MapReduce)
A managed big data platform for running open-source frameworks like Apache Spark, Hadoop, Hive, Presto, and Flink at scale. EMR handles cluster provisioning, configuration, and scaling while you focus on your data processing logic. EMR on EC2 gives you full control over cluster configuration; EMR Serverless removes cluster management entirely — you submit jobs and AWS handles all the infrastructure. A common architecture pairs EMR with S3 as the storage layer and AWS Glue Data Catalog as the metadata store.

### Amazon EventBridge
A serverless event bus that connects AWS services, SaaS applications, and custom applications using events. It receives events (JSON payloads describing something that happened), matches them against rules, and routes them to targets like Lambda, SQS, Step Functions, or Kinesis. EventBridge Scheduler adds the ability to invoke targets on a cron or rate schedule. The Schema Registry auto-discovers and stores event schemas, making it easier to build loosely coupled, event-driven architectures.

### Amazon Glacier / S3 Glacier
AWS's lowest-cost archival storage tier. Data stored in S3 Glacier Instant Retrieval is accessible in milliseconds; S3 Glacier Flexible Retrieval takes minutes to hours; S3 Glacier Deep Archive (the cheapest tier at ~$1/TB/month) takes up to 12 hours for retrieval. All tiers provide 11 nines of durability. Glacier is the right answer for compliance-driven retention (audit logs, financial records, medical imaging) where data is rarely or never accessed after initial storage.

### Amazon GuardDuty
An intelligent threat detection service that continuously analyzes AWS CloudTrail events, VPC Flow Logs, and DNS logs to identify malicious activity or unauthorized behavior. Machine learning models identify anomalies like unusual API calls, compromised credentials, or communication with known malicious IP addresses. No agents to deploy — GuardDuty is enabled with a single click and starts producing findings immediately. Findings are surfaced in the GuardDuty console and can be routed to Security Hub or EventBridge for automated remediation.

### Amazon Inspector
An automated vulnerability management service that continuously scans EC2 instances, container images in ECR, and Lambda functions for known software vulnerabilities (CVEs) and unintended network exposure. Inspector integrates with AWS Systems Manager Agent and requires no separate agent installation on modern AMIs. Risk scores are normalized using the industry-standard CVSS framework. Inspector replaces the older "Amazon Inspector Classic" and is now fully automated rather than assessment-based.

### Amazon Kinesis
A family of services for ingesting and processing real-time streaming data at scale:
- **Kinesis Data Streams** — low-latency ingestion of streaming data into shards; consumers process data in near-real-time
- **Kinesis Data Firehose** (now Amazon Data Firehose) — fully managed delivery of streaming data to destinations like S3, Redshift, OpenSearch, or Splunk; handles batching, compression, and encryption automatically
- **Kinesis Data Analytics** (now Amazon Managed Service for Apache Flink) — run Apache Flink applications to process and analyze streaming data using SQL or Java/Python

Kinesis is the AWS-native answer to Apache Kafka for teams that want a fully managed streaming platform without cluster operations.

### Amazon Lake Formation
A service that makes it faster and simpler to build, secure, and manage a data lake on S3. Lake Formation sits on top of S3 and the Glue Data Catalog and adds a fine-grained permissions layer — column-level and row-level security — that S3 bucket policies alone cannot provide. It also accelerates the initial data lake setup by automating blueprints for ingesting data from common sources (RDS, S3, DynamoDB). Lake Formation is the governance layer; Glue and Athena are the processing and querying layers that operate within the boundaries it defines.

### Amazon Macie
A data security service that uses machine learning to automatically discover, classify, and protect sensitive data stored in S3. Macie can identify PII (names, credit card numbers, SSNs, passport numbers), financial data, and other sensitive content. It produces findings that appear in the Macie console and can be routed to Security Hub or EventBridge. Particularly relevant for customers in regulated industries (healthcare, finance, retail) who need to demonstrate they know where sensitive data lives.

### Amazon MSK (Managed Streaming for Apache Kafka)
A fully managed Apache Kafka service. AWS provisions and manages the Kafka brokers and ZooKeeper nodes, handles patching and replacement of failed brokers, and integrates with IAM, VPC, and CloudWatch. MSK Serverless removes broker provisioning entirely — capacity scales automatically. The key SA distinction from Kinesis: MSK gives you full Kafka API compatibility, which matters when customers have existing Kafka workloads or are committed to the Kafka ecosystem (connectors, Kafka Streams, ksqlDB).

### Amazon OpenSearch Service
A managed search and analytics service based on the open-source OpenSearch (forked from Elasticsearch) project. Used for log analytics (as part of the SIEM or observability stack), full-text search (product catalogs, document search), and operational dashboards. OpenSearch Service manages cluster provisioning, patching, and cross-zone replication. It integrates with Kinesis Data Firehose for streaming log ingestion and Cognito for dashboard authentication. Customers migrating from self-managed Elasticsearch can move to OpenSearch Service with minimal API changes.

### Amazon RDS (Relational Database Service)
A managed service for running relational databases — MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, and Amazon Aurora — without managing the underlying OS or database engine installation. AWS handles automated backups (up to 35-day retention), Multi-AZ failover (typically under 60 seconds), read replicas for horizontal read scaling, and patch management. RDS is the right answer when customers need a familiar relational database model with reduced operational overhead. For new workloads, Aurora is generally the preferred choice for MySQL/PostgreSQL workloads due to its performance and storage architecture.

### Amazon Redshift
A fully managed, petabyte-scale cloud data warehouse. Redshift uses a columnar storage format and massively parallel processing (MPP) to execute complex analytical queries across terabytes of data in seconds. Redshift Spectrum extends queries directly to data stored in S3 without loading it into the warehouse. Redshift Serverless automatically scales compute based on workload demand. The RA3 node type introduced compute/storage separation — compute scales independently while data is stored durably in Redshift Managed Storage backed by S3.

### Amazon Route 53
AWS's scalable DNS (Domain Name System) and domain registration service. Route 53 translates human-readable domain names into IP addresses and supports advanced routing policies: Simple, Weighted (traffic splitting), Latency-based, Failover (active-passive), Geolocation, Geoproximity, and Multivalue. Health checks allow Route 53 to automatically remove unhealthy endpoints from DNS responses. Route 53 Resolver extends DNS resolution between VPCs and on-premises networks via Direct Connect or VPN.

### Amazon S3 (Simple Storage Service)
The object storage backbone of AWS. S3 stores data as objects (files + metadata) in flat namespaces called buckets. It provides 11 nines of durability (99.999999999%) by replicating data across at least three Availability Zones. S3 is the de facto landing zone for data lakes, backup targets, static website hosting, and artifact storage. Storage classes (Standard, Intelligent-Tiering, Standard-IA, Glacier) allow customers to optimize cost based on access frequency. S3 Lifecycle Policies automate transitions between storage classes. S3 Versioning protects against accidental deletion and overwrites.

### Amazon S3 Intelligent-Tiering
A storage class that automatically moves objects between access tiers (Frequent Access, Infrequent Access, Archive Instant Access) based on actual usage patterns — at no retrieval cost. It eliminates the need to manually predict access patterns, making it the right default choice for data lakes where usage is unpredictable. A small monthly monitoring fee applies per object, so it's not cost-effective for very small objects (< 128 KB).

### Amazon SageMaker
The end-to-end ML platform on AWS. SageMaker covers the entire ML lifecycle: data labeling (Ground Truth), feature engineering (Feature Store), model training (managed training jobs with distributed training support), experiment tracking, model hosting (real-time endpoints, batch transform, serverless inference), and MLOps (Pipelines, Model Registry, Model Monitor). SageMaker Studio is the integrated IDE. Customers who want to build custom ML models without managing any ML infrastructure use SageMaker; customers who want pre-built ML capabilities use AWS AI Services (Rekognition, Comprehend, Forecast, etc.).

### Amazon SNS (Simple Notification Service)
A fully managed pub/sub messaging service for fan-out architectures. A message published to an SNS topic is delivered to all subscribed endpoints — which can include SQS queues, Lambda functions, HTTP/HTTPS endpoints, email addresses, and SMS recipients. SNS is the "broadcast" layer in event-driven architectures; SQS is the "buffer" layer. Together (SNS → SQS), they decouple producers from consumers while ensuring no messages are lost.

### Amazon SQS (Simple Queue Service)
A fully managed message queuing service that decouples application components. Producers send messages to a queue; consumers poll the queue and process messages independently. SQS Standard queues offer at-least-once delivery and best-effort ordering (nearly unlimited throughput); FIFO queues guarantee exactly-once processing and strict ordering (up to 3,000 messages/second with batching). The visibility timeout prevents duplicate processing — when a consumer picks up a message, it becomes temporarily invisible to other consumers until the consumer deletes it or the timeout expires.

### Amazon VPC (Virtual Private Cloud)
The networking foundation of every AWS deployment. A VPC is a logically isolated section of the AWS cloud where you launch resources in a virtual network you define. You control IP address ranges (CIDR blocks), subnets (public vs. private), route tables, internet gateways, NAT gateways, and network ACLs. Security Groups act as stateful firewalls at the instance level. VPC Peering and AWS Transit Gateway extend connectivity between VPCs and to on-premises networks. Understanding VPC design — subnet sizing, AZ distribution, egress architecture — is foundational for any solution architecture conversation.

### AMI (Amazon Machine Image)
A pre-configured template for launching EC2 instances. An AMI includes the root volume (OS + installed software), launch permissions, and a block device mapping. AWS provides hundreds of public AMIs (Amazon Linux 2023, Ubuntu, Windows Server); customers can create custom AMIs that bake in application dependencies to reduce instance startup time. AWS Marketplace offers third-party AMIs with commercial software pre-licensed.

### API Gateway (Amazon API Gateway)
A fully managed service for creating, deploying, and managing REST, HTTP, and WebSocket APIs at any scale. It handles authentication (IAM, Cognito, Lambda authorizers), throttling, caching, request/response transformation, and monitoring. API Gateway is the front door for serverless backends (Lambda) and acts as a proxy to other AWS services or HTTP endpoints. HTTP APIs are cheaper and lower-latency than REST APIs for most use cases; REST APIs add more features (usage plans, request validation, API keys).

### ARN (Amazon Resource Name)
A globally unique identifier for every AWS resource. The format is `arn:partition:service:region:account-id:resource`. ARNs are used in IAM policies to specify exactly which resources a principal can or cannot access. Being able to read an ARN (e.g., `arn:aws:s3:::my-bucket` vs. `arn:aws:s3:::my-bucket/*`) is essential for writing precise IAM policies.

### Auto Scaling
The mechanism for automatically adjusting the number of EC2 instances, ECS tasks, DynamoDB capacity units, or other scalable resources based on demand. EC2 Auto Scaling Groups (ASGs) use scaling policies — Target Tracking (e.g., keep CPU at 50%), Step Scaling, or Scheduled Scaling — to add or remove instances. Predictive Scaling uses ML to forecast demand and pre-scale before a load spike hits. Auto Scaling is the primary tool for both cost optimization (scale in during off-hours) and high availability (maintain minimum capacity across AZs).

### Availability Zone (AZ)
One or more discrete data centers within an AWS Region, each with independent power, cooling, and networking. AZs within a Region are connected by high-bandwidth, low-latency fiber. Distributing resources across multiple AZs (Multi-AZ architecture) is the baseline requirement for high-availability designs — a failure in one AZ does not impact resources in others. Most managed AWS services (RDS Multi-AZ, Aurora, ALB) handle AZ redundancy automatically.

### AWS Backup
A centralized, policy-driven backup service that automates data protection across AWS services — EC2, EBS, RDS, Aurora, DynamoDB, EFS, FSx, S3, and VMware workloads. Backup plans define schedules and retention periods; backup vaults store the recovery points. AWS Backup Vault Lock (WORM — Write Once Read Many) prevents backup deletion, satisfying compliance requirements in regulated industries.

### AWS Batch
A fully managed service for running batch computing jobs at any scale. You define a job (a Docker container + command), submit it to a managed queue, and AWS Batch provisions the right compute environment (EC2 On-Demand or Spot, or Fargate), schedules the jobs, and terminates compute when the queue is empty. It's the right answer for scheduled or event-triggered workloads that are too large for Lambda (>15 min) and don't need always-on compute.

### AWS CDK (Cloud Development Kit)
An open-source framework for defining cloud infrastructure using familiar programming languages — TypeScript, Python, Java, C#, and Go. CDK constructs represent AWS resources at three levels of abstraction: L1 (raw CloudFormation), L2 (higher-level, opinionated defaults), and L3 (patterns that combine multiple services). CDK synthesizes down to CloudFormation templates, so everything is still managed through CloudFormation's change sets and rollback mechanisms. Customers who prefer coding over YAML/JSON templating strongly favor CDK.

### AWS CloudFormation
The native Infrastructure-as-Code (IaC) service for AWS. Templates (written in JSON or YAML) declare the desired state of AWS resources; CloudFormation provisions and updates those resources in the correct order, handling dependencies automatically. Change sets allow teams to preview what will change before applying an update. Stack drift detection identifies manual changes made outside CloudFormation. For multi-account and multi-region deployments, CloudFormation StackSets automate deployment across an entire AWS Organization.

### AWS CloudTrail
The audit log for your AWS account. Every API call made to AWS — through the console, CLI, SDK, or another service — is recorded as an event in CloudTrail. Events include who made the call (IAM principal), what was called (API name), when it happened (timestamp), and from where (source IP). CloudTrail is the first place to look during a security investigation. Trails can be configured to deliver logs to S3 for long-term retention and to CloudWatch Logs for real-time alerting.

### AWS Config
A service that continuously records the configuration state of AWS resources and evaluates that state against rules (managed rules or custom Lambda-backed rules). Config answers two questions: "What did this resource look like at a point in time?" (configuration history) and "Does this resource comply with our policies?" (compliance evaluation). Config is the foundation for automated compliance reporting in regulated environments. Conformance Packs bundle multiple Config rules into a single deployable package aligned to frameworks like CIS Benchmarks or PCI DSS.

### AWS Control Tower
A service for setting up and governing a multi-account AWS environment (a "Landing Zone") following AWS best practices. Control Tower provisions a well-architected account structure (management account, log archive account, audit account), applies Service Control Policies (SCPs) via AWS Organizations, and enables guardrails (preventive and detective controls) across all enrolled accounts. It's the starting point for enterprise customers who are building their AWS environment from scratch and need governance at scale.

### AWS Direct Connect
A dedicated, private network connection between a customer's on-premises data center and AWS. Unlike VPN over the public internet, Direct Connect provides consistent bandwidth (1 Gbps to 100 Gbps), lower latency, and predictable performance. It bypasses the public internet entirely, which is required by some compliance frameworks. Direct Connect Gateway allows a single connection to reach VPCs across multiple AWS Regions. The typical setup pairs Direct Connect for production traffic with a VPN as a backup path.

### AWS Fargate
A serverless compute engine for containers that works with both ECS and EKS. With Fargate, you define CPU and memory requirements for a container task — AWS provisions, patches, and scales the underlying compute without you ever seeing a server. It eliminates the need to manage EC2 instance fleets for container workloads. Fargate is typically more expensive per compute unit than EC2 but significantly reduces operational overhead, making it the right default for teams that don't want to manage container host fleets.

### AWS Glue
A serverless data integration service with three main capabilities: (1) **Glue ETL** — runs Apache Spark jobs to transform data between sources and targets; (2) **Glue Data Catalog** — a centralized metadata repository (database and table definitions) used by Athena, Redshift Spectrum, and EMR; (3) **Glue Crawlers** — automatically scan data stores (S3, RDS, DynamoDB) and infer schemas to populate the Data Catalog. Glue Studio provides a visual drag-and-drop interface for building ETL pipelines. It's the glue (literally) that holds together the modern AWS data lake stack.

### AWS IAM (Identity and Access Management)
The access control foundation of AWS. IAM defines who (principals — users, roles, groups, services) can do what (actions) on which resources (ARNs) under what conditions. IAM Policies are JSON documents that grant or deny permissions. IAM Roles are preferable to IAM Users for granting access to EC2 instances, Lambda functions, and cross-account scenarios because they issue temporary credentials. The principle of least privilege — granting only the permissions required — is the core IAM security principle. IAM Access Analyzer identifies over-permissive policies and external access.

### AWS Lambda
The serverless compute service that runs code in response to events without provisioning or managing servers. Lambda functions are stateless, event-driven, and scale from zero to thousands of concurrent executions automatically. Supported runtimes include Python, Node.js, Java, Go, Ruby, .NET, and custom runtimes via Lambda Layers. Functions execute for up to 15 minutes. Lambda integrates with virtually every AWS service as both a trigger source (S3 events, DynamoDB Streams, API Gateway, EventBridge) and a target. Lambda@Edge and CloudFront Functions extend execution to the CDN edge.

### AWS Organizations
A service for centrally managing and governing multiple AWS accounts. Organizations allows account grouping into Organizational Units (OUs), applying Service Control Policies (SCPs) to enforce permission boundaries across accounts, and enabling consolidated billing. AWS Organizations is the prerequisite for Control Tower, Security Hub, GuardDuty, Config, and most multi-account governance services. A common account structure separates workloads by environment (dev/staging/prod) or by business unit.

### AWS Secrets Manager
A service for storing, rotating, and retrieving secrets — database passwords, API keys, OAuth tokens — without hardcoding them in application code or configuration files. Secrets Manager supports automatic rotation for supported databases (RDS, Redshift, DocumentDB) using a Lambda function; the application always retrieves the current version of the secret without any code changes. Costs ~$0.40/secret/month plus API call charges. For non-rotating configuration values (not secrets), AWS Systems Manager Parameter Store is a free alternative.

### AWS Step Functions
A serverless orchestration service for building workflows as state machines. Each step in the workflow is a state — it can invoke a Lambda function, call an AWS service API (200+ service integrations via SDK integrations), wait for a human approval, run parallel branches, or retry failed steps with exponential backoff. Standard Workflows guarantee exactly-once execution for long-running processes; Express Workflows are optimized for high-volume, short-duration event processing. Step Functions replaces complex, error-prone orchestration logic in application code with a visual, auditable workflow.

### AWS Systems Manager (SSM)
A unified operations hub for managing EC2 instances and on-premises servers. Key capabilities: **Session Manager** (browser-based shell access without opening port 22 or managing SSH keys), **Parameter Store** (secure configuration and secrets storage), **Patch Manager** (automated OS patching across a fleet), **Run Command** (execute commands remotely without SSH), and **Inventory** (track software and configuration across instances). SSM Agent (pre-installed on Amazon Linux and recent Windows AMIs) is the only requirement.

### AWS Transit Gateway
A network transit hub that connects multiple VPCs and on-premises networks through a single gateway. Before Transit Gateway, connecting N VPCs required N*(N-1)/2 peering connections — a hub-and-spoke model with Transit Gateway at the center scales linearly. Transit Gateway also integrates with Direct Connect and VPN. Inter-Region Transit Gateway Peering extends the hub-and-spoke model globally. It's the right answer for customers with more than a handful of VPCs that need to communicate.

### AWS WAF (Web Application Firewall)
A web application firewall that protects web applications from common exploits — SQL injection, cross-site scripting (XSS), OWASP Top 10 vulnerabilities. WAF rules can match on IP addresses, HTTP headers, query strings, and body content. AWS Managed Rule Groups (maintained by AWS and third-party vendors) provide pre-built protection with minimal configuration. WAF deploys in front of CloudFront, ALB, API Gateway, and AppSync. Rate-based rules provide basic DDoS protection at Layer 7.

---

## B

### Billing Alarm
A CloudWatch alarm configured on the `EstimatedCharges` metric in the `AWS/Billing` namespace. Triggers an SNS notification when projected AWS charges exceed a specified threshold. A basic but essential control for any AWS environment — every account should have at least one billing alarm set. AWS Budgets provides more granular cost control with forecasting, service-level thresholds, and automated actions.

### Blue/Green Deployment
A deployment strategy where two identical environments ("blue" = current, "green" = new) run simultaneously. Traffic is switched from blue to green all at once (or gradually via weighted routing). If the new version has problems, rollback is instant — just switch traffic back to blue. Supported natively by Elastic Beanstalk, CodeDeploy, ECS, and Route 53 weighted routing policies. Eliminates downtime and reduces deployment risk.

---

## C

### CIDR (Classless Inter-Domain Routing)
The notation used to define IP address ranges in VPC subnet configuration. A CIDR block like `10.0.0.0/16` defines the network address (`10.0.0.0`) and the prefix length (`/16` = 16 bits fixed, leaving 16 bits for hosts = 65,536 addresses). Choosing VPC CIDR blocks that don't overlap with on-premises networks or other VPCs is critical for Direct Connect and VPC Peering connectivity. The `/16` to `/28` range is valid for VPC and subnet CIDR blocks.

### CloudWatch Logs
The log storage and analysis component of Amazon CloudWatch. Applications, OS, and AWS services send log events to Log Groups (logical containers) → Log Streams (sequences of events from a single source). Log Retention Policies automatically expire old logs. CloudWatch Logs Insights provides an interactive SQL-like query language for analyzing log data. Log subscriptions can stream logs in near-real-time to Lambda, Kinesis, or OpenSearch for processing or long-term storage.

### Compliance Frameworks (AWS)
AWS is certified against dozens of industry and government compliance frameworks including SOC 1/2/3, PCI DSS, HIPAA, ISO 27001/27017/27018, FedRAMP, GDPR, and NIST 800-53. AWS publishes audit reports in AWS Artifact. Crucially, compliance in AWS is a **shared responsibility** — AWS is responsible for the compliance of the infrastructure; customers are responsible for their own workloads and configurations running on that infrastructure. Customers can use AWS services (Config, Security Hub, Control Tower) to automate compliance checks.

### Cost Explorer
An AWS Cost Management tool that visualizes, understands, and manages AWS costs and usage over time. It provides pre-built reports (e.g., cost by service, by linked account) and lets you build custom charts with filters and groupings. The Savings Plans and Reserved Instance recommendations in Cost Explorer calculate potential savings based on historical usage. Cost Explorer data has a ~24-hour lag — it's for trend analysis, not real-time billing.

---

## D

### Data Lake
An architectural pattern where large volumes of raw data — structured, semi-structured, and unstructured — are stored in their native format in a centralized repository (typically S3) at low cost. Unlike a data warehouse, a data lake imposes no schema at ingest time (schema-on-read). The risk of a poorly governed data lake is a "data swamp" — data that cannot be trusted or found. AWS Lake Formation addresses governance; Glue handles transformation; Athena and Redshift Spectrum handle querying.

### DDoS (Distributed Denial of Service)
An attack that attempts to overwhelm an application or network with traffic from many sources. AWS Shield Standard is automatically included for all AWS customers at no cost and protects against common Layer 3/4 DDoS attacks. AWS Shield Advanced adds 24/7 DDoS Response Team (DRT) support, cost protection for scaling charges during attacks, and advanced attack visibility. CloudFront, Route 53, and WAF add additional layers of protection at the edge.

### Dead Letter Queue (DLQ)
A queue (SQS) or topic (SNS) that receives messages that cannot be successfully processed after a configured number of attempts. DLQs prevent bad messages from blocking the queue and allow engineers to inspect, debug, and reprocess failed messages. Setting up DLQs for Lambda functions, SQS queues, and EventBridge targets is a reliability best practice — without them, processing failures are silent.

---

## E

### EBS (Elastic Block Store)
Block storage volumes for EC2 instances. Unlike instance store (ephemeral, lost when instance stops), EBS volumes persist independently of the instance lifecycle. Volume types are optimized for different workloads: gp3 (general purpose, baseline 3,000 IOPS), io2 Block Express (high-performance, up to 256,000 IOPS for databases), st1 (throughput-optimized HDD for sequential reads), sc1 (cold HDD for infrequently accessed data). EBS volumes live in a single AZ; EBS Snapshots (stored in S3) enable cross-AZ and cross-region backup.

### ECR (Elastic Container Registry)
A fully managed Docker container image registry. ECR integrates natively with ECS and EKS for image pulling and with CodePipeline/CodeBuild for CI/CD. ECR Image Scanning detects vulnerabilities in container images on push or on a schedule. ECR is private by default; Public ECR (gallery.ecr.aws) hosts publicly available images. Lifecycle Policies automatically expire old or untagged images to control storage costs.

### EFS (Elastic File System)
A fully managed, serverless NFS (Network File System) that can be mounted concurrently by multiple EC2 instances, ECS tasks, Lambda functions, and on-premises servers. EFS scales automatically with no capacity planning required and charges only for storage used. Performance modes: General Purpose (low latency) and Max I/O (higher aggregate throughput for parallel workloads). Storage classes: Standard and Infrequent Access (IA), with Lifecycle Management to move files automatically. EFS is the right answer when multiple compute resources need shared read/write access to the same file system.

### ElastiCache
A fully managed, in-memory caching service supporting Redis and Memcached. Used to reduce database load by caching frequently accessed data, with sub-millisecond read latency. Redis mode supports replication, clustering, Sorted Sets, Pub/Sub, and persistence; Memcached is simpler and better for pure caching. Common patterns: session storage, leaderboards, real-time analytics, database query caching. ElastiCache for Redis can serve as a message broker (Streams feature) or a rate limiter.

### Elastic Beanstalk
A Platform-as-a-Service (PaaS) for deploying and scaling web applications without managing infrastructure. You upload your application code (in Node.js, Python, Ruby, Java, Go, .NET, PHP, or Docker), and Elastic Beanstalk automatically handles provisioning, load balancing, auto scaling, and monitoring. You retain full access to the underlying EC2 instances and can customize the environment. Beanstalk is the right answer for developers who want fast deployment without deep AWS expertise — though most mature teams graduate to ECS, EKS, or direct IaC (CDK/CloudFormation) as their needs grow.

### Elastic Load Balancing (ELB)
A family of load balancers that distribute incoming traffic across multiple targets (EC2 instances, containers, Lambda, IP addresses):
- **Application Load Balancer (ALB)** — Layer 7 (HTTP/HTTPS), path-based and host-based routing, WebSocket support, WAF integration. Best for microservices and HTTP applications.
- **Network Load Balancer (NLB)** — Layer 4 (TCP/UDP/TLS), ultra-low latency, static IP addresses, handles millions of requests per second. Best for real-time applications, gaming, and financial services.
- **Gateway Load Balancer (GWLB)** — Layer 3/4, routes traffic through third-party virtual network appliances (firewalls, IDS/IPS). Best for network security inspection.

---

## F

### Fargate (see AWS Fargate)

### FSx
A family of managed file system services built on popular third-party file systems:
- **FSx for Windows File Server** — fully managed SMB file shares for Windows workloads (Active Directory integrated)
- **FSx for Lustre** — high-performance parallel file system for HPC, ML training, and video processing; can be linked to S3
- **FSx for NetApp ONTAP** — multi-protocol (NFS, SMB, iSCSI) with NetApp SnapMirror and tiering
- **FSx for OpenZFS** — ZFS-based, high-performance, low-latency storage with snapshots and clones

---

## G

### Global Accelerator (AWS Global Accelerator)
A networking service that routes user traffic through the AWS global backbone network to the nearest AWS edge location, reducing latency and improving availability for globally distributed applications. Unlike CloudFront (which caches content), Global Accelerator works at Layer 4 and proxies traffic — it's the right choice for non-HTTP protocols, dynamic content, and applications that need failover across Regions. It provides two static Anycast IP addresses that serve as a fixed entry point from anywhere in the world.

### Graviton (AWS Graviton)
AWS-designed ARM-based processors for EC2 instances and managed services (RDS, ElastiCache, Lambda, Fargate). Graviton3 (and Graviton4) instances typically deliver better price/performance than comparable x86 instances — often 20-40% better performance per dollar. Most Linux workloads are compatible with minimal changes. Graviton is a strong cost optimization and performance recommendation for EC2-heavy workloads.

---

## H

### High Availability (HA)
An architectural goal of designing systems to remain operational in the face of component failures. On AWS, HA typically means deploying resources across at least two Availability Zones, using managed services with built-in redundancy (ALB, RDS Multi-AZ, Aurora), and automating failure recovery (Auto Scaling, Route 53 health checks). HA is distinct from Disaster Recovery (DR): HA addresses in-Region failures (AZ outage); DR addresses Region-level failures.

---

## I

### IAM Role (see AWS IAM)

### IGW (Internet Gateway)
An AWS-managed gateway that enables communication between resources in a VPC and the public internet. An IGW is attached to a VPC and referenced in route tables for public subnets. EC2 instances in a public subnet need both a public IP/Elastic IP and a route to an IGW to communicate with the internet. Private subnets use a NAT Gateway for outbound-only internet access. The IGW itself is highly available and scales automatically.

### Instance Store
Ephemeral block storage physically attached to the EC2 host. Instance store volumes provide very high I/O throughput (suitable for temporary caches, buffers, and scratch data in HPC workloads) but are not persistent — data is lost when the instance stops or terminates. Not suitable for any data that must survive instance lifecycle events. Contrast with EBS, which persists independently of instance state.

---

## K

### KMS (AWS Key Management Service)
A managed service for creating and controlling encryption keys used to encrypt data across AWS services. KMS integrates with over 100 AWS services — S3, EBS, RDS, Redshift, Lambda, Secrets Manager, and more. Keys can be AWS-managed (free, created per service), customer-managed (more control, ~$1/month/key), or customer-provided (CMK — you provide key material). KMS enforces access via IAM policies and key policies and logs every key usage to CloudTrail. For compliance, KMS supports FIPS 140-2 validated HSMs.

---

## L

### Lambda (see AWS Lambda)

### Landing Zone
A pre-configured, multi-account AWS environment that follows best practices for security, governance, and architecture. A landing zone establishes the account structure (via AWS Organizations), network topology (hub-and-spoke VPC design), identity (SSO via IAM Identity Center), logging (centralized CloudTrail and Config logs), and guardrails (SCPs). AWS Control Tower automates landing zone setup. The landing zone is the foundation for enterprise AWS adoption — "building right from the start."

---

## M

### Multi-AZ
A deployment pattern where a resource or application is spread across multiple Availability Zones to achieve high availability. For managed services like RDS, Multi-AZ means AWS automatically maintains a synchronous standby replica in a different AZ and fails over to it (typically in under 60 seconds) if the primary has a hardware failure. For EC2 workloads, Multi-AZ is achieved by placing instances in an Auto Scaling Group that spans multiple AZs behind a load balancer.

### Multi-Region
An architecture where workloads are deployed across more than one AWS Region to achieve disaster recovery, reduce global latency, or meet data residency requirements. Multi-Region is significantly more complex than Multi-AZ and is warranted only for the highest availability requirements (99.99%+ SLA) or strict data sovereignty rules. Services like DynamoDB Global Tables, Aurora Global Database, S3 Cross-Region Replication, and Route 53 latency/failover routing support Multi-Region designs.

---

## N

### NAT Gateway
A managed AWS service that enables instances in private subnets to initiate outbound connections to the internet (e.g., downloading patches, calling external APIs) without allowing inbound connections from the internet. Unlike an Internet Gateway (which works bidirectionally), NAT is unidirectional — outbound only. NAT Gateways are AZ-specific; for high availability, deploy one per AZ. Charges apply for data processed (~$0.045/GB) in addition to an hourly charge.

---

## O

### On-Demand Instances
The baseline EC2 pricing model — pay per hour or per second for compute capacity, no upfront commitment. On-Demand is the right choice for short-lived, unpredictable workloads where you can't commit to a 1- or 3-year term. It's also the fallback when Reserved Instance or Savings Plan capacity is exhausted. Most customers use a mix of Savings Plans (for predictable base load) and On-Demand (for variable demand above the base).

---

## P

### Parameter Store (see AWS Systems Manager)

### Placement Groups
A logical grouping of EC2 instances that influences their physical placement within AWS infrastructure:
- **Cluster** — packs instances close together in a single AZ for ultra-low network latency and high throughput (HPC use case)
- **Spread** — places instances on distinct hardware to reduce correlated failures (maximum 7 instances per AZ per group)
- **Partition** — divides instances into logical partitions on separate hardware racks, used for large distributed systems (Hadoop, Cassandra, Kafka)

### PrivateLink (AWS PrivateLink)
A service that enables private connectivity between VPCs, AWS services, and on-premises networks without using the public internet. PrivateLink uses Elastic Network Interfaces (ENIs) with private IP addresses as entry points (Interface Endpoints) for AWS services. It's the alternative to VPC Gateway Endpoints (which only support S3 and DynamoDB) when you need private access to any of the 100+ AWS services that support PrivateLink. PrivateLink is also used to share custom services privately across VPCs without VPC Peering.

---

## R

### RDS Proxy
A fully managed database proxy for Amazon RDS and Aurora that sits between the application and the database, pooling and sharing connections. It dramatically reduces the overhead of establishing database connections, which is critical for Lambda functions (which can create thousands of short-lived connections, overwhelming a database). RDS Proxy also improves availability by failing over to a standby DB instance in under 30 seconds without dropping application connections.

### Reserved Instances (RIs)
An EC2 pricing discount (up to 72%) in exchange for a 1- or 3-year commitment to a specific instance family, Region, and OS. Standard RIs are the biggest discount but cannot be exchanged; Convertible RIs allow exchanging attributes (instance family, OS) and discount up to 54%. AWS Savings Plans are generally preferred over RIs for most use cases due to their flexibility across instance families and Lambda. RIs are still relevant for specific workloads (e.g., RDS Reserved Instances).

### Route Table
A set of rules (routes) that determines where network traffic from a subnet or gateway is directed. Every subnet in a VPC is associated with one route table. A route table entry has a destination (CIDR block or prefix list) and a target (local, IGW, NAT Gateway, VPC Peering connection, Transit Gateway, etc.). The most specific route wins. The local route (e.g., `10.0.0.0/16 → local`) is always present and cannot be deleted.

---

## S

### S3 Lifecycle Policy (see Amazon S3)

### S3 Transfer Acceleration
A feature that speeds up uploads to S3 by routing traffic through AWS CloudFront edge locations. Data is uploaded to the nearest edge location over the public internet and then transferred to the target S3 bucket over the private AWS backbone. Most effective for large file uploads from geographically distant locations. Charged per GB transferred in addition to standard S3 costs.

### Savings Plans
A flexible pricing model that offers significant discounts (up to 66%) on AWS compute usage in exchange for a consistent hourly spend commitment for 1 or 3 years. Compute Savings Plans apply across EC2, Lambda, and Fargate regardless of instance family, size, Region, OS, or tenancy. EC2 Instance Savings Plans offer a deeper discount (up to 72%) for a specific instance family in a specific Region. Savings Plans are generally preferred over Reserved Instances for most workloads due to their flexibility.

### Security Group
A stateful virtual firewall at the EC2 instance (or ENI) level. Inbound and outbound rules specify allowed protocols, ports, and source/destination IP ranges or security group IDs. Stateful means return traffic is automatically allowed — you only need to define inbound rules for inbound traffic, not both directions. Security Groups are the primary network security mechanism for EC2, RDS, Lambda (in VPC), and most other resource types. Default is to deny all inbound and allow all outbound.

### Service Control Policy (SCP)
An IAM policy type used in AWS Organizations to set maximum permission guardrails for accounts or OUs. SCPs do not grant permissions — they restrict what permissions can be granted. Even if an IAM policy allows an action, an SCP can deny it organization-wide. Common SCP patterns: preventing disabling of CloudTrail, restricting regions to approved regions, blocking the creation of IAM users, preventing changes to security tooling. SCPs are the "ceiling" of what any principal in the account can do.

### Shared Responsibility Model
AWS's framework for dividing security responsibilities between AWS and the customer. AWS is responsible for security **of** the cloud (physical infrastructure, hardware, hypervisor, managed service software). The customer is responsible for security **in** the cloud (OS patching on EC2, application code, IAM configuration, network ACLs, encryption choices, data classification). The division shifts based on the service type: for managed services like Lambda or S3, AWS takes on more responsibility; for EC2, the customer manages more.

### Spot Instances
EC2 instances that use spare AWS capacity at discounts of up to 90% versus On-Demand pricing. In exchange, AWS can reclaim Spot capacity with a 2-minute warning when demand increases. Ideal for fault-tolerant, stateless, or checkpointed workloads: batch processing, big data, CI/CD pipelines, ML training, and rendering. Spot Fleets and EC2 Fleet diversify across instance types and AZs to improve availability. Not appropriate for workloads that cannot tolerate interruption (databases, payment processing).

### SSO (AWS IAM Identity Center)
The recommended way to provide centralized SSO access to AWS accounts and business applications. IAM Identity Center (formerly AWS SSO) integrates with identity providers (Microsoft Entra ID/Azure AD, Okta, Google Workspace) via SAML 2.0 and SCIM for user provisioning. Users log in once to the AWS access portal and can assume Permission Sets across any account in the Organization. It eliminates the need to create and manage IAM users in individual accounts.

---

## T

### Transit Gateway (see AWS Transit Gateway)

### Trusted Advisor
A service that provides real-time guidance to help customers optimize their AWS infrastructure across five categories: **Cost Optimization** (underutilized resources, Reserved Instance recommendations), **Performance** (high-utilization instances, CloudFront optimizations), **Security** (open security groups, MFA on root, IAM key rotation), **Fault Tolerance** (Multi-AZ, S3 versioning, Route 53 health checks), and **Service Limits** (approaching service quotas). The number of checks available depends on the support plan — Basic/Developer plans get a limited set; Business and Enterprise plans get all checks via the API.

---

## V

### VPC Endpoint
A private connection between a VPC and an AWS service that doesn't require an internet gateway, NAT gateway, VPN, or Direct Connect connection. There are two types: **Gateway Endpoints** (for S3 and DynamoDB only, free) add an entry to the route table; **Interface Endpoints** (powered by PrivateLink, ~$0.01/hour/AZ + data charges) create ENIs with private IPs in the VPC. VPC Endpoints are essential for security-conscious architectures where S3 or other service traffic must not traverse the public internet.

### VPC Peering
A network connection between two VPCs that routes traffic privately using AWS backbone infrastructure. VPC Peering is non-transitive — if VPC A peers with VPC B and VPC B peers with VPC C, VPC A cannot communicate with VPC C through B. For more than a few VPCs, this limitation makes Transit Gateway the better choice. CIDR blocks between peered VPCs must not overlap.

---

## W

### Well-Architected Framework
AWS's documented set of best practices for building cloud workloads, organized into six pillars: **Operational Excellence**, **Security**, **Reliability**, **Performance Efficiency**, **Cost Optimization**, and **Sustainability**. Each pillar has design principles, best practice questions, and review guidance. The AWS Well-Architected Tool in the console guides customers through formal reviews of their workloads and produces a findings report. SAs use Well-Architected as a conversation framework to identify risks and improvement opportunities in customer architectures.

---

*Last updated: April 2026. Terms reflect services and features generally available at that date.*
