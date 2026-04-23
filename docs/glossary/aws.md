# AWS Glossary

A comprehensive A–Z reference of AWS services, sub-features, architectural concepts, and terminology. Written for Solution Architects who need to understand what each term means, why it matters, and how to talk about it in a customer conversation. Sorted alphabetically.

---

## Services with Sub-Entries

| Service | Sub-entries |
|---|---|
| **ACM** | Private CA |
| **Athena** | Federated Query, Apache Spark, Named Queries, Workgroups |
| **Aurora** | Auto Scaling, Backtrack, Global Database, ML, Parallel Query, Serverless v2 |
| **Bedrock** | Agents, Flows, Guardrails, Knowledge Bases, Model Evaluation, Model Fine-Tuning, Studio |
| **CloudFront** | Behaviors, Cache Policies, Field-Level Encryption, Functions, Lambda@Edge, Origin Shield |
| **CloudWatch** | Alarms, Application Insights, Container Insights, Contributor Insights, Dashboards, Evidently, Logs Insights, Metrics, RUM, Synthetics |
| **Cognito** | Advanced Security Features, Hosted UI, Identity Pools, User Pools |
| **Comprehend** | Custom Classification, Custom Entity Recognition, Medical |
| **Connect** | Contact Lens, Voice ID, Wisdom |
| **DocumentDB** | Elastic Clusters |
| **DynamoDB** | Auto Scaling, DAX, Global Tables, On-Demand Capacity, PartiQL, PITR, Streams, TTL, Transactions |
| **EC2** | Capacity Reservations, Dedicated Hosts, Dedicated Instances, Hibernate, Image Builder, IMDS, Nitro Enclaves, Spot Fleet |
| **ECS** | Anywhere, Service Connect, Services, Task Definitions |
| **EKS** | Add-ons, Anywhere, Auto Mode, Fargate Profiles, Managed Node Groups |
| **ElastiCache** | Global Datastore, Serverless, Redis Cluster Mode |
| **Elastic Beanstalk** | Extensions (.ebextensions) |
| **ELB** | ALB Listener Rules, ALB Target Groups, ALB WAF Integration |
| **EMR** | on EC2, on EKS, Serverless, Studio |
| **EventBridge** | Event Bus, Pipes, Rules, Schema Registry, Scheduler |
| **FSx** | Lustre S3 Integration, NetApp ONTAP FlexClone, Windows Shadow Copies |
| **Glue** | Crawlers, Data Catalog, DataBrew, ETL Jobs, for Ray |
| **GuardDuty** | EKS Protection, Lambda Protection, Malware Protection, RDS Protection, S3 Protection |
| **IAM** | Access Analyzer, Groups, Permissions Boundaries, Policies, Roles, Service-Linked Roles, Users |
| **Inspector** | CIS Scans |
| **IoT Core** | Device Shadow, Fleet Indexing, Jobs, Rules Engine |
| **IoT** | Device Defender, Greengrass, SiteWise, TwinMaker |
| **KMS** | Customer Managed Keys, Key Policies, Multi-Region Keys |
| **Kinesis** | Data Firehose, Data Streams, Enhanced Fan-Out, Video Streams, Managed Flink |
| **Lake Formation** | Blueprints, Data Sharing, Fine-Grained Permissions, LF-Tags |
| **Lambda** | Concurrency, Container Images, Destinations, Event Source Mappings, Extensions, Function URLs, Layers, Power Tuning, Provisioned Concurrency |
| **Lex** | Intents, Slot Types |
| **Managed Blockchain** | Hyperledger Fabric, Ethereum |
| **MSK** | Connect, Replicator, Schema Registry, Serverless |
| **Neptune** | Analytics, Serverless |
| **OpenSearch** | Cold Storage, Serverless, UltraWarm |
| **Organizations** | AI Services Opt-Out Policy, Backup Policies, SCPs, Tag Policies |
| **Personalize** | Campaigns, Event Tracker, Filters |
| **Pinpoint** | Journeys, Segments |
| **PrivateLink** | Endpoint Services |
| **QuickSight** | Embedded Analytics, ML Insights, Q (Natural Language), SPICE |
| **RDS** | Blue/Green Deployments, Custom, Enhanced Monitoring, Multi-AZ, Performance Insights, Proxy, Read Replicas |
| **Redshift** | Concurrency Scaling, Data API, Data Sharing, Federated Query, ML, RA3 Nodes, Serverless, Spectrum |
| **Rekognition** | Custom Labels, Video |
| **Route 53** | Health Checks, Hosted Zones, Resolver, Routing Policies, Traffic Flow |
| **S3** | Access Points, Batch Operations, CRR, Event Notifications, Intelligent-Tiering, Inventory, Lifecycle Policies, Multi-Region Access Points, Object Lambda, Object Lock, RTC, S3 Select, SRR, Storage Lens, Transfer Acceleration, Versioning |
| **SageMaker** | Autopilot, Canvas, Clarify, Data Wrangler, Debugger, Distributed Training, Experiments, Feature Store, Ground Truth, HyperPod, Inference, JumpStart, Model Monitor, Model Registry, Pipelines, Studio |
| **SES** | Configuration Sets, Dedicated IPs, Virtual Deliverability Manager |
| **Step Functions** | Activity Tasks, Express Workflows, Standard Workflows, SDK Integrations |
| **SSM (Systems Manager)** | AppConfig, Automation, Distributor, Inventory, OpsCenter, Parameter Store, Patch Manager, Run Command, Session Manager, State Manager |
| **Textract** | Analyze Lending, Queries |
| **Timestream** | Live Analytics |
| **Transcribe** | Call Analytics, Medical |
| **Transfer Family** | AS2, Custom Identity Provider |
| **Transit Gateway** | Network Manager, Multicast, Route Tables |
| **VPC** | DHCP Option Sets, Endpoint Policies, Flow Logs, Reachability Analyzer, Sharing, Traffic Mirroring |
| **VPN** | Client VPN, Site-to-Site VPN |
| **WAF** | Bot Control, Fraud Control (ATP + ACFP), Managed Rule Groups, Web ACLs |
| **X-Ray** | Groups, Sampling Rules, Service Map |

---

## A

### 1. ACM (AWS Certificate Manager)
A managed service that provisions, deploys, and renews SSL/TLS certificates. Eliminates manually tracking certificate expiration across load balancers, CloudFront, and API Gateway. Public certificates are free. Integrates directly with ALB, CloudFront, API Gateway, and Elastic Beanstalk — enabling HTTPS with no manual certificate installation.

### 2. ACM Private CA (Private Certificate Authority)
A managed private CA for issuing internal certificates — for internal services, mutual TLS (mTLS), IoT devices, or code signing. Unlike public ACM certificates (which are free and browser-trusted), private certificates carry a monthly CA fee (~$400/month/CA) plus per-certificate charges. Supports certificate hierarchies (root CA → subordinate CA).

### 3. Amazon AppFlow
A fully managed integration service for transferring data between AWS and SaaS applications — Salesforce, ServiceNow, Slack, Google Analytics, SAP, Zendesk — without writing custom code. Flows can run on schedule, on event, or on demand. Data can be transformed, filtered, and mapped during transfer. The low-code path for moving data between business applications and AWS analytics services (S3, Redshift, EventBridge).

### 4. Amazon AppStream 2.0
A managed application streaming service that delivers desktop applications to any device through a browser. The application runs on AWS, not the end-user device — nothing to install or update on the client. Used for software trials, remote workforces, and BYOD scenarios. Differs from WorkSpaces (full desktop streaming) by streaming individual applications.

### 5. Amazon Athena
A serverless, interactive query service for analyzing data in S3 using standard SQL. No infrastructure to manage; pay per data scanned (~$5/TB). Compatible with Glue Data Catalog for schema management.

### 6. Athena Federated Query
Extends Athena SQL across data sources beyond S3 — DynamoDB, RDS, CloudWatch Logs, OpenSearch, on-premises JDBC sources — using Lambda-based data source connectors. A single SQL query can join data across S3 and RDS without moving data.

### 7. Athena for Apache Spark
Runs interactive Apache Spark workloads inside Athena using managed Jupyter notebooks. No cluster to provision — Spark sessions start in seconds. Used for data exploration and ML feature engineering on data lake data.

### 8. Athena Named Queries
Saved SQL queries in Athena (stored in S3 or the Athena console) that can be re-run or shared across teams. Combined with Workgroups, they provide a governed query library.

### 9. Athena Workgroups
Logical groupings of Athena users and queries with separate settings for data scan limits, query result locations, encryption, and cost controls. Enables cost allocation and governance by team or project.

### 10. Amazon Augmented AI (A2I)
A service for building human review workflows for ML predictions. When a model's confidence falls below a threshold, A2I routes the prediction to a human reviewer. Pre-built task UIs exist for Textract (document review) and Rekognition (image moderation). Used in regulated industries where humans must validate automated decisions.

### 11. Amazon Aurora
A MySQL- and PostgreSQL-compatible managed relational database delivering up to 5x MySQL throughput. Separates compute from storage; storage replicates six ways across three AZs and grows automatically to 128 TB.

### 12. Aurora Auto Scaling
Automatically adds or removes Aurora Replicas based on CPU or connection count metrics. Scales read capacity without manual intervention or downtime.

### 13. Aurora Backtrack
Rewinds an Aurora MySQL cluster to a previous point in time — without restoring from a backup. Backtrack operates in seconds/minutes versus the hour-long restore process. Backtrack window up to 72 hours. Aurora PostgreSQL does not support Backtrack (use point-in-time restore instead).

### 14. Aurora Global Database
Spans an Aurora cluster across up to five AWS Regions with sub-second replication from primary to secondary Regions. Secondary Regions serve read traffic with local latency. In a disaster, a secondary Region can be promoted to primary in under a minute. Used for globally distributed applications and cross-Region DR.

### 15. Aurora ML
Integrates Aurora with SageMaker and Comprehend so that ML inference can be called from SQL. For example: `SELECT sentiment_analysis(review_text) FROM reviews` — Aurora calls a SageMaker endpoint in-query. Enables ML inference without extracting data from the database.

### 16. Aurora Parallel Query
Pushes query processing to the Aurora storage layer, allowing analytical queries to run in parallel across storage nodes without impacting OLTP workloads. Reduces query latency for large table scans on Aurora MySQL. An alternative to offloading analytical workloads to Redshift for mixed OLTP/analytics patterns.

### 17. Aurora Serverless v2
Scales Aurora compute capacity up and down in fine-grained increments (0.5 ACU steps) in response to actual workload demand — including scaling to near-zero when idle. Billed per ACU-second. Right for intermittent, unpredictable, or dev/test workloads where always-on provisioned capacity would be wasteful.

### 18. Amazon Bedrock
A fully managed service providing access to foundation models (FMs) from Anthropic, Meta, Mistral, Cohere, Stability AI, and Amazon through a single API. No infrastructure, no ML expertise required. The platform for building generative AI applications on AWS.

### 19. Bedrock Agents
Multi-step AI agents that plan and execute tasks by combining foundation model reasoning with tool use. Agents can call APIs, query knowledge bases, run Lambda functions, and interact with data sources to complete complex, multi-turn tasks autonomously. Configured through the Bedrock console with an instruction prompt, action groups (API schemas), and knowledge base connections.

### 20. Bedrock Flows
A visual builder for creating multi-step generative AI workflows — chaining prompts, conditions, knowledge base lookups, Lambda functions, and agent calls into a directed acyclic graph (DAG). Allows building complex AI orchestration logic without custom application code.

### 21. Bedrock Guardrails
Configurable safety and content filters applied to both input and output of FM interactions. Controls include: topic denial (block off-topic queries), content filtering (violence, hate speech, adult content), PII redaction, word filters, and grounding checks (detect hallucinations vs. retrieved context). Applied consistently across all models in Bedrock without model-specific tuning.

### 22. Bedrock Knowledge Bases
Managed Retrieval Augmented Generation (RAG) pipeline. Connects a data source (S3, Confluence, SharePoint, Salesforce, web crawler) to a vector store (OpenSearch Serverless, Pinecone, RDS pgvector, MongoDB Atlas, Aurora). Bedrock handles chunking, embedding, and indexing automatically. At query time, retrieves relevant chunks and injects them into the FM prompt — grounding responses in customer data.

### 23. Bedrock Model Evaluation
A framework for evaluating and comparing foundation models on customer-defined tasks. Supports automatic evaluation (using built-in metrics: ROUGE, BERTScore, toxicity, accuracy on MCQ) and human evaluation (routes outputs to a labeling workforce). Helps customers choose the right model for their use case based on quality and cost metrics.

### 24. Bedrock Model Fine-Tuning
Customizes a foundation model with customer-specific training data to improve performance on domain-specific tasks. Two approaches: **Fine-tuning** (supervised learning on labeled input-output pairs) and **Continued Pre-training** (unsupervised learning on domain text to inject proprietary knowledge). Fine-tuned models are stored privately in the customer's account. Not all Bedrock models support fine-tuning — check model cards.

### 25. Bedrock Studio
A web-based workspace for collaboratively building, testing, and sharing generative AI applications powered by Bedrock. Teams can prototype prompts, agents, and knowledge bases and share them within the organization for review and iteration.

### 26. Amazon Braket
AWS's managed quantum computing service. Provides access to quantum hardware from IonQ, Rigetti, D-Wave, and OQC, plus managed quantum circuit simulators. Braket Hybrid Jobs runs quantum-classical hybrid algorithms on EC2 or SageMaker. Relevant for customers exploring quantum advantage for optimization problems in finance, pharma, and logistics.

### 27. Amazon Chime SDK
Developer APIs and SDKs for embedding real-time audio, video, and messaging into custom applications. Customers building telehealth, contact center, or collaboration features use the SDK rather than the end-user Chime application.

### 28. Amazon CloudFront
A global CDN with 400+ PoPs caching static and dynamic content at edge locations. Integrates with S3, ALB, API Gateway, Lambda@Edge. Functions as a security perimeter via WAF, Shield Advanced, and ACM.

### 29. CloudFront Behaviors
Rules within a CloudFront distribution that match URL patterns and apply different cache policies, origin configurations, or functions. Example: `/api/*` routes to an ALB origin with no caching; `/*.jpg` routes to S3 with a 30-day cache TTL.

### 30. CloudFront Cache Policies
Control what CloudFront caches and for how long — TTL settings, and which request headers/cookies/query strings are included in the cache key. Managed cache policies (CachingOptimized, CachingDisabled) cover most use cases; custom policies give precise control.

### 31. CloudFront Field-Level Encryption
Adds an additional layer of security for sensitive data (e.g., credit card numbers) by encrypting specific form fields at the CloudFront edge using a customer-provided public key. Only applications that hold the corresponding private key can decrypt the fields — even AWS cannot read them in transit.

### 32. CloudFront Functions
Lightweight JavaScript functions that run at CloudFront edge locations for simple request/response manipulation — URL rewrites, header manipulation, A/B testing redirects. Sub-millisecond execution, millions of requests per second. Cheaper and faster than Lambda@Edge for simple transformations that don't need Node.js capabilities or access to external services.

### 33. CloudFront Lambda@Edge
Node.js or Python Lambda functions that run at CloudFront Regional Edge Caches (not all PoPs) for more complex edge logic — authentication, cookie manipulation, dynamic content personalization, A/B testing with backend logic. Runs at four event types: Viewer Request, Origin Request, Origin Response, Viewer Response.

### 34. CloudFront Origin Shield
An additional caching layer (a single Regional cache) between CloudFront edge PoPs and the origin. Reduces origin load by consolidating cache misses from all edge locations through a single point before hitting the origin. Reduces origin egress costs and origin request volume.

### 35. Amazon CloudWatch
The primary observability service for AWS. Collects metrics, logs, and traces. Enables alarms, dashboards, and automated actions.

### 36. CloudWatch Alarms
Monitor a single CloudWatch metric or math expression and trigger actions (SNS notification, Auto Scaling action, EC2 action) when the metric crosses a threshold. Three states: OK, ALARM, INSUFFICIENT_DATA. Composite Alarms combine multiple alarms using AND/OR logic to reduce alarm noise.

### 37. CloudWatch Application Insights
Automatically detects and configures monitoring for common application stacks (.NET, Java, SQL Server, SAP HANA) running on EC2. Surfaces anomalies as problems in the CloudWatch console with correlated logs, metrics, and traces — reducing mean time to resolution.

### 38. CloudWatch Container Insights
Collects, aggregates, and summarizes container metrics and logs from ECS, EKS, and Kubernetes. Provides cluster, node, pod, and container-level metrics. Powered by the CloudWatch Agent and Fluent Bit for log collection.

### 39. CloudWatch Contributor Insights
Analyzes log data in real time to identify the top contributors to a metric (e.g., which IP addresses generate the most 5XX errors, which DynamoDB keys are most frequently accessed). Creates rules using log fields; outputs ranked time series data. No custom code required.

### 40. CloudWatch Dashboards
Customizable, shareable monitoring dashboards displaying metrics, alarms, logs, and CloudWatch Synthetics canary results. Supports cross-account and cross-Region widgets. Automatic dashboards for most AWS services are available pre-built in the console.

### 41. CloudWatch Evidently
A feature flagging and A/B testing service. Allows gradually rolling out new features to a percentage of users and measuring the impact on business metrics before full rollout. Integrated with CloudWatch for metric collection and analysis.

### 42. CloudWatch Logs Insights
An interactive query language for analyzing CloudWatch Logs data. SQL-like syntax supports filtering, aggregation, sorting, and pattern extraction from log data. Useful for ad hoc log investigations and building operational dashboards from log-derived metrics.

### 43. CloudWatch Metrics
Time-series data points from AWS services and custom application code. Metrics have a namespace, name, and up to 30 dimensions. Standard resolution: 1-minute granularity; High Resolution: 1-second granularity. Metric Math allows creating new metrics by combining existing ones. CloudWatch Metric Streams delivers near-real-time metrics to Kinesis Data Firehose or third-party observability tools (Datadog, Dynatrace, New Relic).

### 44. CloudWatch RUM (Real User Monitoring)
Collects real-time telemetry from end-user browser sessions — page load performance, JavaScript errors, HTTP call failures — and correlates them with CloudWatch metrics and X-Ray traces. Provides a user-experience perspective to complement infrastructure-side observability.

### 45. CloudWatch Synthetics
Runs configurable canary scripts (Node.js or Python) on a schedule to monitor endpoints, APIs, and user flows. Canaries simulate user actions — loading a URL, submitting a form — and alert when behavior changes (broken links, latency spikes, wrong content). Independent of application code; detects issues even when no real user traffic exists.

### 46. Amazon CodeCatalyst
A unified software development service combining project management, source control (Git), CI/CD, and cloud dev environments. Blueprint-based project creation; integrates with GitHub. Aimed at development teams wanting a managed DevOps toolchain.

### 47. Amazon Cognito
An identity service for web and mobile applications.

### 48. Cognito Advanced Security Features
An add-on for User Pools that adds adaptive authentication (step-up MFA based on risk signals like unusual location or device), compromised credential detection, and a security dashboard showing sign-in anomalies. Requires an additional per-MAU charge.

### 49. Cognito Hosted UI
A pre-built, customizable sign-in and sign-up web UI provided by Cognito User Pools. Handles the complete authentication flow (sign in, sign up, MFA challenge, password reset) without building custom UI screens. Supports social identity provider federation (Google, Facebook, Apple) and SAML enterprise federation.

### 50. Cognito Identity Pools (Federated Identities)
Exchanges a Cognito User Pool token, social identity provider token, or SAML assertion for temporary AWS credentials (via STS). Enables mobile and web applications to call AWS services directly (S3, DynamoDB, Lambda) with per-user IAM role assumptions. Supports unauthenticated (guest) access with restricted permissions.

### 51. Cognito User Pools
A fully managed user directory for web and mobile applications. Handles user sign-up, sign-in, MFA (SMS, TOTP, email OTP), social federation (Google, Facebook, Apple), SAML/OIDC enterprise federation, and email/phone verification. Issues JWT tokens (id_token, access_token, refresh_token) on successful authentication. User attributes, groups, and Lambda triggers (pre-sign-up, post-confirmation, pre-token generation) allow customization.

### 52. Amazon Comprehend
An NLP service for extracting meaning from unstructured text — entity recognition, sentiment analysis, key phrase extraction, language detection, and PII detection/redaction.

### 53. Comprehend Custom Classification
Trains a custom text classification model using labeled examples. Classifies documents into user-defined categories (e.g., support ticket type, legal document category) without ML expertise. Inference available as real-time single-document or asynchronous batch.

### 54. Comprehend Custom Entity Recognition
Trains a custom NER (named entity recognition) model to identify domain-specific entities not covered by the standard model — product names, internal codes, medical device identifiers. Requires labeled training examples.

### 55. Comprehend Medical
A specialized version of Comprehend for extracting medical information from clinical text — diagnoses, medications, dosages, procedures, anatomical terms. Includes ICD-10-CM and RxNorm entity linking. HIPAA eligible. Used by healthcare and life sciences customers for clinical NLP without building custom models.

### 56. Amazon Connect
A cloud-based contact center providing voice, chat, and task channels — IVR, agent desktops, real-time and historical analytics, and workforce management. Pay per minute of use. Deploys in minutes with no telephony infrastructure.

### 57. Connect Contact Lens
An ML-powered analytics overlay for Connect. Provides real-time and post-call sentiment analysis, automatic call transcription, keyword/phrase spotting, agent performance scoring, and conversation summaries. Helps supervisors monitor agent quality and surface compliance issues without listening to every call.

### 58. Connect Voice ID
Real-time caller authentication using voice biometrics. Analyzes voice characteristics to verify a caller's identity against a stored voiceprint — replacing security questions and PIN entry. Reduces handle time and fraud risk. Integrates into contact flows without custom code.

### 59. Connect Wisdom
An ML-powered knowledge retrieval service for Connect agents. Surfaces relevant articles, procedures, and FAQs in real time during a call based on what the customer is saying — without the agent needing to search manually. Indexes content from Salesforce, ServiceNow, S3, and other sources.

### 60. Amazon Detective (see Amazon Detective — standalone entry)

### 61. Amazon DocumentDB
A fully managed document database compatible with the MongoDB API. Stores JSON-shaped data; separates compute from storage (same architecture as Aurora) with six-way replication across three AZs. Not a complete drop-in for all MongoDB features; removes the operational burden of managing MongoDB clusters.

### 62. DocumentDB Elastic Clusters
A DocumentDB deployment option that automatically scales storage and compute horizontally (sharded) — beyond the limits of a single DocumentDB cluster. Each shard is independently managed. Designed for workloads with extremely large document datasets that exceed single-cluster capacity.

### 63. Amazon DynamoDB
A fully managed NoSQL key-value and document database with single-digit millisecond performance at any scale.

### 64. DynamoDB Auto Scaling
Monitors DynamoDB table and GSI read/write capacity consumption and automatically adjusts provisioned capacity up or down using Application Auto Scaling and CloudWatch. Prevents throttled requests during traffic spikes without over-provisioning. Configured with a target utilization percentage and min/max capacity bounds.

### 65. DynamoDB Accelerator (DAX)
An in-memory cache for DynamoDB delivering microsecond read latency. Write-through; serves eventually consistent reads only. Best for read-heavy workloads with repetitive key access (leaderboards, session state, catalog lookups).

### 66. DynamoDB Global Tables
Multi-region, active-active replication. Writes in any Region are replicated to all other Regions with typically sub-second latency. Conflict resolution: last-writer-wins based on timestamp. Provides both global low-latency reads/writes and cross-Region disaster recovery in a single configuration.

### 67. DynamoDB On-Demand Capacity Mode
Pay-per-request pricing; DynamoDB instantly accommodates any throughput without capacity planning. Ideal for unpredictable or spiky workloads. More expensive per request than Provisioned mode — if traffic patterns are known, Provisioned + Auto Scaling is cheaper.

### 68. DynamoDB PartiQL
An SQL-compatible query language for DynamoDB. Allows SELECT, INSERT, UPDATE, DELETE using familiar SQL syntax — without learning DynamoDB's native expression syntax. Useful for ad hoc queries in the console and migrations from relational databases. Does not add SQL join or aggregation capabilities; each statement still maps to a DynamoDB operation.

### 69. DynamoDB Point-in-Time Recovery (PITR)
Continuous backup of DynamoDB tables enabling restoration to any second within a 35-day rolling window — without writing backup code or schedules. Protects against accidental writes or deletes. Restores create a new table; the original table is unaffected.

### 70. DynamoDB Streams
A time-ordered log of item-level changes (INSERT, MODIFY, REMOVE) to a DynamoDB table. Events are available for 24 hours and can trigger Lambda functions or be consumed by Kinesis Data Streams. Used for building event-driven pipelines, cross-region replication (before Global Tables), and change data capture.

### 71. DynamoDB Time to Live (TTL)
A mechanism for automatically deleting expired items from a table — no write cost or throughput consumption. Each item can have a TTL attribute (Unix epoch timestamp); DynamoDB deletes items within 48 hours of expiration. Used for session expiry, log retention, and time-boxed data without manual cleanup.

### 72. DynamoDB Transactions
Enables ACID transactions across multiple items and tables in a single all-or-nothing operation (TransactWriteItems and TransactGetItems). Up to 100 items per transaction. Useful for financial ledgers, order management, and any workflow requiring atomic multi-item consistency guarantees.

---

## E

### 73. Amazon EC2 (Elastic Compute Cloud)
The foundational virtual server service in AWS. Instance families: general purpose (M/T), compute optimized (C), memory optimized (R/X/u), storage optimized (I/D/H), and accelerated computing (P/G/Trn/Inf).

### 74. EC2 Capacity Reservations
Reserves EC2 capacity in a specific AZ for a specific instance type — without any billing commitment. Guaranteed capacity is available whenever needed. Billed at On-Demand rates whether or not instances are running. Used to guarantee capacity for critical workloads in AZs that might run out of On-Demand capacity during peak events.

### 75. EC2 Dedicated Hosts
Physical EC2 servers dedicated exclusively to a single customer. Provides visibility into the physical host (socket and core count) required for BYOL (Bring Your Own License) software licensing (Windows Server, SQL Server, Oracle). Can be On-Demand or Reserved. Full control over instance placement on the host.

### 76. EC2 Dedicated Instances
EC2 instances running on hardware dedicated to a single customer — but without visibility into the physical host or control over instance placement. Less expensive than Dedicated Hosts; used when hardware isolation is required by compliance but BYOL socket-based licensing is not needed.

### 77. EC2 Hibernate
Saves the contents of EC2 instance RAM to the EBS root volume, then stops the instance. On restart, the instance resumes from exactly where it left off — applications continue running without reboot or re-initialization. Root volume must be encrypted. Supported on select instance families and sizes. Useful for long-running processes that need to pause and resume quickly.

### 78. EC2 Image Builder
Automates creation, testing, and distribution of custom AMIs and container images via pipelines. Eliminates the manual process of launching an instance, installing software, and creating an AMI. Integrates with SSM for component reuse and Organizations for cross-account image sharing.

### 79. EC2 Instance Metadata Service (IMDS)
A local HTTP endpoint (`169.254.169.254`) accessible from within an EC2 instance that returns instance metadata — instance ID, Region, AZ, IAM role credentials, public IP, user data. IMDSv2 (Session-Oriented) is the secure version — requires a PUT request to get a session token before accessing metadata, protecting against SSRF attacks. IMDSv1 (less secure, token-optional) should be disabled on new instances.

### 80. EC2 Nitro Enclaves
Isolated compute environments within an EC2 instance for processing highly sensitive data — cryptographic keys, PII, healthcare data — in a hardened enclave with no persistent storage, no interactive access, and no network access (except a local vsock to the parent instance). The parent instance controls what data enters the enclave. Used for payment processing, key management, and compliance-mandated data isolation.

### 81. EC2 Spot Instances
Use spare AWS capacity at up to 90% discount. AWS can reclaim with a 2-minute warning. Right for fault-tolerant, stateless, checkpointed workloads: batch, ML training, CI/CD, big data.

### 82. EC2 Spot Fleet
A collection of Spot and optionally On-Demand instances fulfilling a target capacity or price. Spot Fleet diversifies across instance types and AZs — maximizing availability and minimizing interruption. Allocation strategies: `lowestPrice`, `diversified`, `capacityOptimized` (recommended — reduces interruptions by selecting pools with the most available capacity).

### 83. Amazon ECS (Elastic Container Service)
A fully managed container orchestration service. AWS handles scheduling, placement, and health checks. Containers run on EC2 or Fargate.

### 84. ECS Anywhere
Extends ECS scheduling to on-premises servers and VMs managed via SSM Agent. On-premises servers register as ECS external instances; ECS schedules tasks on them using the same API and console as cloud ECS. Enables a hybrid container deployment model without adopting Kubernetes.

### 85. ECS Service Connect
A managed service mesh capability within ECS that handles service discovery, load balancing, and observability for inter-service communication — without requiring App Mesh, Envoy configuration, or custom DNS. Services register under a namespace and connect to each other by short service names. Traffic metrics appear automatically in CloudWatch.

### 86. ECS Services
Long-running ECS configurations that maintain a desired count of task replicas, integrate with load balancers (ALB/NLB), handle rolling updates, and support Auto Scaling. Services ensure container availability and replace failed tasks automatically.

### 87. ECS Task Definitions
JSON blueprints defining how a container should run — Docker image, CPU/memory allocation, port mappings, environment variables, secrets (from Secrets Manager or SSM Parameter Store), log configuration, and volume mounts. Versioned; new deployments reference a specific revision.

### 88. Amazon EKS (Elastic Kubernetes Service)
A managed Kubernetes service. AWS runs the control plane across multiple AZs; customers provide worker nodes (EC2 or Fargate).

### 89. EKS Add-ons
Managed operational software for EKS clusters — kube-proxy, CoreDNS, VPC CNI, EBS CSI driver, EFS CSI driver. AWS manages add-on versioning, testing, and patching. Add-ons can be installed, updated, and removed via the EKS console, CLI, or API without manual Helm operations.

### 90. EKS Anywhere
Runs EKS on customer-managed infrastructure — VMware vSphere, bare metal, Nutanix, Apache CloudStack. Uses the same EKS Distro Kubernetes distribution as cloud EKS. AWS manages Kubernetes upgrades and configuration; infrastructure management remains with the customer. Enables consistent Kubernetes operations across cloud and on-premises.

### 91. EKS Auto Mode
A fully managed EKS configuration (launched 2024) where AWS automatically provisions, scales, and terminates EC2 worker nodes based on pod scheduling requirements. Customers define compute classes and resource limits; EKS Auto Mode selects optimal instance types and manages the lifecycle. Blurs the distinction between ECS Fargate and EKS managed nodes.

### 92. EKS Fargate Profiles
Configuration that determines which Kubernetes pods run on Fargate (serverless, no EC2 nodes). Fargate Profiles match pods based on namespace and label selectors. Each Fargate pod gets dedicated compute — no noisy neighbor risk. Fargate for EKS is typically more expensive per compute unit than EC2 nodes but eliminates node fleet management.

### 93. EKS Managed Node Groups
Automate the provisioning and lifecycle of EC2 worker nodes for EKS clusters. AWS provisions nodes using an Auto Scaling Group, handles node upgrades (drain → terminate → replace) with zero-downtime procedures, and applies security patches. Customer controls instance type, size, AMI, and scaling bounds.

### 94. Amazon ElastiCache
A fully managed in-memory caching service supporting Redis and Memcached. Sub-millisecond read latency.

### 95. ElastiCache Global Datastore
Replicates a Redis ElastiCache cluster across multiple AWS Regions with typically sub-second latency. Secondary Regions serve read traffic; primary Region handles writes. Supports cross-Region failover for globally distributed applications. Similar to Aurora Global Database but for Redis cache.

### 96. ElastiCache Serverless
A serverless Redis and Memcached offering that automatically scales cache capacity based on application demand — no cluster sizing or shard management. Billed per ECU (ElastiCache Compute Units) consumed. Eliminates the need to predict peak cache capacity.

### 97. ElastiCache for Redis Cluster Mode
Distributes data across multiple shards (partitions), each a primary + replica pair. Enables horizontal scaling beyond the memory limits of a single node. Supports up to 500 nodes per cluster. Data is distributed using consistent hashing on the key space. Write operations go to the primary in each shard; reads can go to replicas.

### 98. Elastic Beanstalk
A PaaS for deploying web applications without managing infrastructure. Upload code; Beanstalk handles provisioning, load balancing, auto scaling, and monitoring.

### 99. Elastic Beanstalk Extensions (.ebextensions)
Configuration files (YAML/JSON in a `.ebextensions/` folder in the application bundle) that customize the Elastic Beanstalk environment — installing packages, running commands, setting environment properties, modifying load balancer listeners. Provide escape-hatch customization without leaving the Beanstalk model.

### 100. Elastic Load Balancing (ELB)
Distributes incoming traffic across multiple targets. Three types: ALB (Layer 7), NLB (Layer 4), GWLB (Layer 3/4 for network appliances).

### 101. ALB Listener Rules
Conditions and actions on an ALB listener. Conditions match on path, hostname, HTTP header, query string, source IP, or HTTP method. Actions forward to a target group, redirect, return a fixed response, authenticate with Cognito, or authenticate with OIDC. Enables a single ALB to route to multiple microservices based on URL path or hostname.

### 102. ALB Target Groups
A logical grouping of targets (EC2 instances, ECS tasks, Lambda functions, IP addresses) that receive traffic from an ALB listener rule. Target groups have their own health check configuration. A target can be in multiple target groups. Weighted target groups allow gradual traffic shifting between versions.

### 103. ALB WAF Integration
Attaches a WAF Web ACL to an ALB to inspect and filter HTTP traffic before it reaches application targets. The ALB forwards each request to WAF for rule evaluation; WAF returns Allow or Block. Requires WAF to be deployed in the same Region as the ALB (unlike CloudFront WAF, which is global).

### 104. Amazon EMR (Elastic MapReduce)
A managed big data platform for Apache Spark, Hadoop, Hive, Presto, Flink, Hudi, and Iceberg.

### 105. EMR on EC2
Traditional EMR deployment on an EC2-based cluster — a master node (primary), core nodes (compute + HDFS storage), and optional task nodes (compute only, good for Spot). Customer controls instance types, cluster sizing, and configuration. Auto Scaling adjusts task node count based on metrics.

### 106. EMR on EKS
Runs Apache Spark jobs on an existing Amazon EKS cluster using EMR's optimized Spark runtime. Shares the Kubernetes node pool with other workloads, improving utilization. Integrates EMR's job management, monitoring, and optimized Spark runtime with Kubernetes workload orchestration.

### 107. EMR Serverless
Submit Spark or Hive jobs without provisioning or managing a cluster. EMR Serverless provisions resources on demand, runs the job, and releases resources when complete. Pre-initialized capacity can be configured to reduce cold-start latency. Right for intermittent batch jobs where always-on cluster cost is unjustifiable.

### 108. EMR Studio
A managed web-based IDE for data engineers and data scientists. Provides Jupyter notebooks connected to EMR clusters or EMR Serverless. Supports Git integration, collaboration, and debugging. Replaces the older EMR Notebooks interface.

### 109. Amazon EventBridge
A serverless event bus for connecting AWS services, SaaS apps, and custom applications using events.

### 110. EventBridge Event Bus
A pipeline that receives events and delivers them to targets based on matching rules. Three types: **Default** (receives events from AWS services), **Custom** (receives events from custom applications), **Partner** (receives events from SaaS partners — Zendesk, Shopify, Datadog). Each account and Region has its own default event bus.

### 111. EventBridge Pipes
Connects a source (SQS, Kinesis, DynamoDB Streams, Kafka, MQ) to a target (Lambda, Step Functions, API Gateway, EventBridge bus) with optional filtering, enrichment (Lambda or API Gateway call), and transformation — in a single, managed resource. Reduces boilerplate code for event-driven integration patterns.

### 112. EventBridge Rules
Pattern-matching rules on an event bus that route matching events to one or more targets. Rules match on any combination of event fields using prefix matching, wildcard matching, or exact value matching. A single rule can have up to 5 targets.

### 113. EventBridge Schema Registry
Automatically discovers and stores event schemas from events flowing through EventBridge buses. Schemas are available as code bindings (Java, Python, TypeScript) so that developers can work with strongly typed event objects rather than raw JSON. Makes it easier to build and document event-driven integrations.

### 114. EventBridge Scheduler
A managed scheduler that invokes targets (Lambda, Step Functions, SQS, any EventBridge API destination) on a cron or rate schedule — or at a specific one-time date/time. More scalable and precise than CloudWatch Events for scheduling at scale (millions of schedules). Supports flexible time windows (run the job within a 15-minute window around the scheduled time to spread load).

---

## F

### 115. AWS Fargate
Serverless compute for containers (ECS and EKS). Define CPU and memory; AWS provisions and patches the underlying compute.

### 116. Fargate Spot
Up to 70% discount on Fargate tasks for interruptible workloads. AWS can reclaim capacity with a 2-minute warning. Suitable for batch jobs, CI/CD, and other fault-tolerant container workloads that can tolerate interruption.

### 117. AWS Fault Injection Simulator (FIS)
A managed chaos engineering service. Pre-built experiment templates simulate AZ failures, EC2 terminations, CPU/memory stress, network latency injection, RDS failovers. Integrated stop conditions (CloudWatch alarms) automatically halt experiments if thresholds are breached.

### 118. AWS Firewall Manager
Centrally configures WAF rules, Shield Advanced, VPC security groups, Network Firewall policies, and Route 53 Resolver DNS Firewall rules across an AWS Organization. Automatically applies policies to new accounts and resources as they are created.

### 119. Amazon Forecast (see Amazon Forecast — already detailed)

### 120. Amazon FSx
Managed file system services for Windows File Server, Lustre, NetApp ONTAP, and OpenZFS. (See FSx sub-entries below.)

### 121. FSx for Lustre — S3 Integration
Links an FSx for Lustre file system to an S3 bucket. Files are lazily loaded from S3 on first access (no need to pre-stage all data). After processing, results can be exported back to S3. This pattern connects the high-throughput Lustre file system to the durable, cheap S3 storage layer for HPC and ML training workflows.

### 122. FSx for NetApp ONTAP — FlexClone
Creates instant, space-efficient clones of volumes or files — only changed blocks consume additional storage. Used for dev/test environments (clone production data without duplication cost), CI/CD pipeline data seeding, and database cloning. Unique to ONTAP; not available in other FSx variants.

### 123. FSx for Windows File Server — Shadow Copies
Volume Shadow Copy Service (VSS) integration for FSx for Windows. Creates point-in-time snapshots of the file system that users can access directly from Windows Explorer ("Previous Versions") to recover accidentally deleted or modified files — without involving IT or restoring from backup.

---

## G

### 124. Amazon GuardDuty
Intelligent threat detection analyzing CloudTrail events, VPC Flow Logs, DNS logs, S3 data plane events, and EKS audit logs.

### 125. GuardDuty EKS Protection
Analyzes EKS audit logs and runtime activity to detect threats within Kubernetes clusters — unauthorized API server calls, suspicious container launches, privilege escalation, crypto mining. Runtime monitoring uses a GuardDuty security agent (DaemonSet) to observe process, network, and file system activity on EKS nodes.

### 126. GuardDuty Lambda Protection
Monitors network activity logs for Lambda functions, detecting functions communicating with known malicious IPs or domains, or exhibiting anomalous network behavior (e.g., a data processing Lambda suddenly making outbound connections to a C2 server).

### 127. GuardDuty Malware Protection
Scans EBS volumes attached to EC2 instances and container workloads flagged by GuardDuty findings for malware, trojans, worms, and crypto miners — without requiring an antivirus agent. Triggered automatically by relevant GuardDuty findings.

### 128. GuardDuty RDS Protection
Analyzes Aurora and RDS login activity to detect anomalous database access — unusual login locations, brute force attempts, privilege escalation, suspicious queries from compromised credentials.

### 129. GuardDuty S3 Protection
Analyzes S3 data plane API events (GetObject, PutObject, DeleteObject) to detect threats — exfiltration of large volumes of data, unusual API call patterns from compromised identities, access from Tor exit nodes.

### 130. AWS Glue
A serverless data integration service with ETL, Data Catalog, Crawlers, and DataBrew.

### 131. Glue Crawlers
Automatically scan data stores (S3, RDS, DynamoDB, JDBC, Delta Lake, Iceberg) on a schedule to infer schemas and populate the Glue Data Catalog. Support incremental crawling (only scan new/changed data). The starting point for cataloging a data lake without writing schema DDL manually.

### 132. Glue Data Catalog
A centralized, managed metadata repository — databases, tables, and schema definitions — used by Athena, Redshift Spectrum, EMR, and Lake Formation. Compatible with the Apache Hive Metastore API. Tables in the Catalog describe where data lives in S3 (or other sources), the format (CSV, Parquet, ORC, JSON), and the schema. A single Catalog is shared across all services in an account and Region.

### 133. Glue DataBrew
A visual data preparation tool with 250+ built-in transformations — no code required. Data profiling, anomaly detection, format normalization. Publishes transformation recipes that run as Glue jobs. Bridges the gap between business analysts and data engineers.

### 134. Glue ETL Jobs
Apache Spark-based batch data transformation jobs. Written in Python or Scala using the Glue DynamicFrame API (or standard Spark DataFrames). Run on managed Spark clusters that scale automatically. Glue Studio provides a drag-and-drop visual interface for building ETL jobs without writing code. Glue Streaming jobs process data continuously from Kinesis or Kafka.

### 135. Glue for Ray
Runs distributed Python workloads using the Ray framework on Glue serverless infrastructure. Enables data scientists to scale Python-native workloads (Pandas, NumPy, scikit-learn) across multiple nodes without switching to Spark.

---

## H

### 136. High Availability (HA)
Designing systems to remain operational through component failures. On AWS: distribute across multiple AZs, use managed services with built-in redundancy (RDS Multi-AZ, Aurora, ALB), and automate failure recovery (Auto Scaling, Route 53 health checks).

---

## I

### 137. AWS IAM (Identity and Access Management)
The access control foundation of AWS — who can do what on which resources.

### 138. IAM Access Analyzer
Analyzes resource-based policies (S3 buckets, IAM roles, KMS keys, Lambda functions, SQS queues, Secrets Manager secrets, EFS file systems) to identify resources accessible from outside the account or AWS Organization. Generates findings for any external access — intended or unintended. Also validates IAM policies for syntax errors and policy checks, and generates least-privilege policies from CloudTrail activity (Policy Generation).

### 139. IAM Groups
Collections of IAM users that inherit the policies attached to the group. Groups simplify permission management at scale — attach a policy to the group instead of each user individually. A user can belong to multiple groups; permissions are the union of all group policies. Note: groups cannot be nested (no group-within-a-group).

### 140. IAM Identity Center (see SSO / IAM Identity Center)

### 141. IAM Permissions Boundaries
An advanced IAM feature setting the maximum permissions a role or user can have — even if their identity policies grant more. A permissions boundary does not grant permissions; it restricts what can be granted. Used to delegate IAM role creation to developers (they can create roles, but only within the boundary you define). Common in landing zone designs to prevent privilege escalation.

### 142. IAM Policies
JSON documents that grant or deny permissions. Types: **AWS Managed** (maintained by AWS for common use cases), **Customer Managed** (created and managed by the customer), **Inline** (embedded directly in a user/role/group — not reusable), **Resource-Based** (attached to a resource, e.g., S3 bucket policy, KMS key policy — grant cross-account access). Evaluation order: explicit Deny > SCP > resource-based policy > identity-based policy > permissions boundary.

### 143. IAM Roles
An IAM identity with permissions policies but no long-term credentials. Roles issue temporary credentials via STS (AWS Security Token Service). Used for: EC2 instance profiles (grant EC2 apps AWS permissions), Lambda execution roles, cross-account access, federated identity (SAML/OIDC), and service-to-service permissions. Preferred over IAM Users for all non-human access.

### 144. IAM Service-Linked Roles
Pre-defined IAM roles created and managed by specific AWS services — the service defines the trust policy and permissions. Customers cannot edit the permission policy (only the trust relationship in some cases). Automatically created when enabling a service feature. Examples: the AWSServiceRoleForAutoScaling role used by Auto Scaling, the AWSServiceRoleForElasticLoadBalancing role used by ELB.

### 145. IAM Users
Long-term IAM identities for individual people or applications. Have permanent credentials (password for console access; access key ID + secret access key for programmatic access). Best practice: use IAM Roles instead of IAM Users wherever possible; if IAM Users are needed, enforce MFA and rotate access keys. IAM Identity Center (SSO) with federated login is strongly preferred over creating individual IAM Users for humans.

### 146. Amazon Inspector
Automated vulnerability management for EC2, ECR container images, and Lambda functions — scanning for CVEs and network exposure.

### 147. Inspector CIS Scans
Runs Center for Internet Security (CIS) benchmark assessments against EC2 instances to check OS-level configuration hardening — password policies, filesystem permissions, network settings. Reports compliance gaps against the CIS benchmark level (Level 1 or Level 2). Available as scheduled or on-demand scans.

### 148. Amazon IoT Core
A managed service for connecting IoT devices to AWS using MQTT, HTTP, or WebSocket.

### 149. IoT Core Device Shadow
A JSON document that stores the last-known state of an IoT device (reported state) and desired future state. Applications interact with the shadow even when the device is offline — the device syncs its state when connectivity is restored. Each device can have multiple named shadows. Essential for building responsive IoT UIs that don't depend on live device connectivity.

### 150. IoT Core Fleet Indexing
Indexes device registry data and device shadow attributes, enabling SQL-like queries across thousands or millions of devices — "find all devices with firmware < 2.0 in California." Supports aggregation queries for fleet analytics dashboards.

### 151. IoT Core Jobs
Manages remote operations across a fleet of IoT devices — firmware updates, configuration changes, commands. Jobs target a device group, deliver the job document, track execution status per device, and support rollout scheduling (gradual deployment with configurable rollout rates and abort criteria).

### 152. IoT Core Rules Engine
Evaluates inbound device messages using SQL-like queries and routes matching messages to AWS services — Lambda, DynamoDB, S3, Kinesis, SQS, SNS, IoT Analytics, and others. A single rule can fan out to multiple targets. Enables serverless device data processing without a custom message broker.

### 153. AWS IoT Device Defender
A security service for auditing IoT device configurations and detecting anomalous device behavior. **Audit** checks device configurations against security best practices (e.g., devices sharing certificates, overly permissive policies). **Detect** uses ML to establish a baseline of normal device behavior (message rates, connection frequency, port usage) and alerts when a device deviates — indicating a compromised or malfunctioning device.

### 154. AWS IoT Greengrass
Extends AWS to edge devices for local compute (Lambda, Docker), ML inference (SageMaker models), and data stream management — even without internet connectivity. Syncs state with IoT Core when connectivity is restored.

### 155. AWS IoT SiteWise
A managed service for collecting, organizing, and analyzing data from industrial equipment — PLCs, SCADA systems, historians. SiteWise Edge runs locally on industrial gateways; data is streamed to AWS for analysis, visualization (SiteWise Monitor), and ML. Structures industrial data into an asset model hierarchy (site → factory → line → machine → sensor) for consistent representation.

### 156. AWS IoT TwinMaker
Creates digital twins of physical systems — factories, buildings, industrial equipment — by connecting real-time sensor data (from IoT SiteWise, Kinesis, SQL databases) to 3D models (imported from CAD/BIM tools or Grafana). Enables operators to visualize the state of a physical system in a 3D environment and drill into components when anomalies are detected. Built on a graph-based knowledge representation.

---

## K

### 157. Amazon Kinesis
A family of real-time data streaming services.

### 158. Amazon Data Firehose (formerly Kinesis Data Firehose)
A fully managed delivery service for streaming data. Receives records from Kinesis Data Streams, MSK, direct PUT, or other sources and delivers batched, compressed, and optionally transformed data to S3, Redshift, OpenSearch, Splunk, or any HTTP endpoint. Format conversion transforms JSON to Parquet/ORC for cost-effective S3 storage. Lambda data transformation runs custom code on each record in flight. Zero infrastructure management — the simplest path from streaming data to a data store.

### 159. Kinesis Data Streams
A low-latency, durable stream for ingesting data at scale. Data is split across shards (each shard: 1 MB/s write, 2 MB/s read). Consumers can be Lambda (event-source mapping), Kinesis Client Library (KCL) applications, or Enhanced Fan-Out (dedicated 2 MB/s per consumer per shard). Retention: 1–365 days. On-Demand mode eliminates shard count management.

### 160. Kinesis Enhanced Fan-Out
Delivers stream data to multiple consumers simultaneously over dedicated HTTP/2 connections — each consumer gets 2 MB/s per shard, regardless of other consumers. Standard mode shares 2 MB/s across all consumers. Enhanced Fan-Out is required when multiple consumers need low-latency (< 70ms) delivery from the same stream.

### 161. Kinesis Video Streams
Ingests, processes, and stores video streams from cameras, drones, and industrial sensors. Integrates with Amazon Rekognition Video for real-time face search and object detection, and with SageMaker for custom ML inference on video. Supports WebRTC for two-way, real-time video communication.

### 162. Amazon Managed Service for Apache Flink
Runs Apache Flink applications for stateful stream processing — windowed aggregations, pattern detection, stream joins. Supports Java, Python, SQL, and Scala. Auto-scales parallelism. Integrates with Kinesis Data Streams, MSK, S3, and DynamoDB.

### 163. AWS KMS (Key Management Service)
Manages encryption keys used across AWS services.

### 164. KMS Customer Managed Keys (CMK)
Encryption keys created and managed by the customer. The customer defines key policies (who can use and manage the key), enables automatic annual rotation, controls key deletion (7–30 day waiting period), and can disable/re-enable keys. ~$1/key/month + API call charges. Required when audit requirements demand customer control over key lifecycle.

### 165. KMS Key Policies
The primary access control mechanism for KMS keys — unlike most AWS resources (where IAM is the primary control), KMS keys require both a key policy and an IAM policy to grant access. The key policy defines which IAM principals in the account (or cross-account) are allowed to use and manage the key. Without an explicit allow in the key policy, even the account root user cannot use the key.

### 166. KMS Multi-Region Keys
Key pairs where the same key material is replicated to multiple AWS Regions. Allows encrypting data in one Region and decrypting it in another without re-encrypting. Useful for cross-Region data replication scenarios (DynamoDB Global Tables, S3 Cross-Region Replication) where data must remain encrypted end-to-end.

---

## L

### 167. AWS Lambda
Serverless compute running code in response to events. Stateless, event-driven, zero infrastructure. Scales from zero to thousands of concurrent executions.

### 168. Lambda Concurrency
The number of Lambda function instances processing requests simultaneously. **Unreserved Concurrency**: drawn from the account-level pool (default 1,000 per Region). **Reserved Concurrency**: guarantees a function a fixed number of concurrent executions — prevents other functions from consuming the pool, and also caps the function's maximum concurrency. **Provisioned Concurrency**: pre-initializes execution environments to eliminate cold starts — billed even when idle.

### 169. Lambda Container Images
Packages a Lambda function as a Docker container image (up to 10 GB) instead of a ZIP deployment package. Allows using standard Docker tooling, CI/CD pipelines, and any runtime — not just the officially supported ones. Images are stored in ECR and deployed to Lambda. Cold starts may be slightly higher than ZIP deployments for large images.

### 170. Lambda Destinations
Configures where Lambda sends asynchronous invocation results — both on success and on failure — to SQS, SNS, Lambda, or EventBridge. An alternative to DLQs that carries the full event context plus execution metadata. On-success destinations enable chaining async workflows; on-failure destinations capture failures with context for debugging.

### 171. Lambda Event Source Mappings
A Lambda resource that reads from a source (Kinesis Data Streams, DynamoDB Streams, SQS, MSK, MQ, Kafka) and invokes the function with batches of records. Lambda manages polling, batch sizing, parallelism, error handling (retry or send to DLQ), and windowing (for streams, wait until a batch is complete or a time window expires).

### 172. Lambda Extensions
Sidecar processes that run alongside a Lambda function to integrate monitoring, security, and governance tools — without modifying function code. Extensions can be internal (share the same process) or external (run as a separate process in the execution environment). Examples: Datadog, New Relic, HashiCorp Vault agents running as Lambda extensions.

### 173. Lambda Function URLs
Built-in HTTPS endpoints for Lambda functions — no API Gateway required. Accessible via a unique URL; supports IAM authentication or no auth. Supports streaming responses. Right for simple HTTP use cases where API Gateway features (usage plans, request validation, custom domain, stage management) are not needed.

### 174. Lambda Layers
ZIP archives containing libraries, runtimes, or data shared across multiple Lambda functions. Layers are versioned and can be shared across accounts. Reduces function package size and enables a consistent dependency layer across a team's functions. Up to 5 layers per function; total unzipped size (function + layers) must not exceed 250 MB.

### 175. Lambda Power Tuning
An open-source AWS Step Functions state machine that automatically runs a Lambda function at multiple memory configurations and finds the optimal memory setting for the desired balance of performance and cost. Run via the AWS Serverless Application Repository. Not a native AWS service, but the standard tool for Lambda cost/performance optimization.

### 176. Lambda Provisioned Concurrency
Pre-initializes Lambda execution environments so that functions respond immediately without a cold start — crucial for latency-sensitive workloads (APIs, user-facing applications). Billed per provisioned concurrency-hour. Can be combined with Application Auto Scaling to add/remove provisioned concurrency on a schedule or based on utilization.

### 177. Amazon Lake Formation
A service for building, securing, and managing data lakes on S3. Adds fine-grained permissions (column-level, row-level) on top of S3 and the Glue Data Catalog.

### 178. Lake Formation Blueprints
Pre-built workflows for ingesting data from common sources (RDS, S3, DynamoDB, CloudTrail logs) into the data lake. Blueprints automate the Glue ETL job and Glue Crawler creation, scheduling, and monitoring. Reduce the time to onboard a new data source from days to minutes.

### 179. Lake Formation Data Sharing
Enables sharing of Glue Data Catalog databases and tables across AWS accounts without copying data. A data producer grants Lake Formation permissions on specific databases/tables to a data consumer account. The consumer accesses data directly in the producer's S3 bucket via the granted permissions. Used for cross-account analytics and building data marketplaces within an organization.

### 180. Lake Formation Fine-Grained Permissions
Row-level and column-level security on top of Glue Data Catalog tables. Column-level security restricts which columns a principal can query (e.g., hide SSN from analysts). Row-level security uses Lake Formation Filters to restrict which rows are visible (e.g., analysts can only see data for their Region). Applied consistently across all services that use the Glue Data Catalog (Athena, Redshift Spectrum, EMR, Glue ETL).

### 181. Lake Formation LF-Tags
A tag-based access control model for Lake Formation. Administrators define tag keys and allowed values (e.g., `Sensitivity = [Public, Confidential, Restricted]`); resources (databases, tables, columns) are tagged with these values; principals are granted access to data with specific tag values via LF-Tag policies. Scales better than resource-by-resource permission grants in large data lakes with hundreds of tables.

### 182. Amazon Lex
A service for building voice and text chatbots using ASR and NLU technology.

### 183. Lex Intents
The core building block of a Lex bot — represents an action the user wants to perform. Each intent has: training utterances (example phrases a user might say), slots (parameters the bot needs to fulfill the intent), and a fulfillment step (Lambda function or dialog code hook). Example: "BookHotel" intent with slots for `City`, `CheckInDate`, `CheckOutDate`, `RoomType`.

### 184. Lex Slot Types
Defines the type and valid values for a slot in an intent. Built-in slot types cover common data types (dates, times, numbers, cities, airport codes, credit card numbers). Custom slot types define domain-specific values (product names, account types, service codes) with optional synonyms.

### 185. Amazon Lightsail
A simplified VPS platform with predictable monthly pricing bundling compute, storage, and networking. For developers, small businesses, and non-AWS specialists. Connects to broader AWS via VPC peering.

---

## M

### 186. Amazon Macie (see Macie — already detailed)

### 187. Amazon Managed Blockchain
Managed Hyperledger Fabric and Ethereum networks for multi-party distributed ledger use cases.

### 188. Managed Blockchain — Hyperledger Fabric
A permissioned blockchain where participants are known and must be invited. AWS manages the ordering service, peer nodes, and certificate authorities. Each member runs their own peer nodes; AWS manages the underlying infrastructure. Used for supply chain traceability, cross-institution financial settlement, and healthcare data sharing among known parties.

### 189. Managed Blockchain — Ethereum
Access to the public Ethereum network via fully managed Ethereum nodes. Customers interact with the Ethereum blockchain (read state, submit transactions) through these nodes without operating their own node infrastructure. Used for decentralized application (dApp) development, NFT platforms, and DeFi integrations.

### 190. Amazon MemoryDB for Redis
A Redis-compatible, durable, in-memory primary database (not just a cache). Multi-AZ transactional log ensures zero data loss. Microsecond reads, single-digit millisecond writes.

### 191. Amazon MSK (Managed Streaming for Apache Kafka)
Fully managed Apache Kafka — brokers, ZooKeeper, patching.

### 192. MSK Connect
Runs Apache Kafka Connect connectors (source and sink) as a fully managed service. Source connectors ingest data from external systems (databases, SaaS) into MSK topics; sink connectors deliver data from MSK topics to external systems (S3, OpenSearch, Redshift). No Kafka Connect infrastructure to manage.

### 193. MSK Replicator
Automatically replicates MSK topics across two MSK clusters in different Regions — for disaster recovery, cross-Region analytics, and active-active multi-Region architectures. Preserves consumer group offsets so consumers in the secondary Region can resume exactly where they left off.

### 194. MSK Schema Registry (Glue Schema Registry)
A central repository for Kafka message schemas (Avro, JSON Schema, Protobuf). Producers register schemas; consumers retrieve them to deserialize messages. Enforces schema compatibility rules (backward, forward, full) to prevent breaking changes from reaching consumers. Integrated with MSK and Glue via the AWS Glue Schema Registry.

### 195. MSK Serverless
Eliminates Kafka broker provisioning — MSK Serverless automatically scales capacity based on throughput. No shard/partition capacity planning. Priced per partition-hour and data throughput. Right for variable Kafka workloads where cluster sizing is difficult.

### 196. Multi-AZ
Deploying resources across multiple Availability Zones for high availability. For RDS/Aurora: synchronous standby replica with automatic failover. For EC2: instances distributed in an Auto Scaling Group behind an ELB.

---

## N

### 197. NAT Gateway
A managed, AZ-specific service enabling outbound-only internet access from private subnets. Deploy one per AZ for high availability. Charges per hour + data processed. NAT Instance (EC2-based) is an older, self-managed alternative — avoid for new deployments.

### 198. Amazon Neptune
A fully managed graph database supporting Property Graph (Gremlin, openCypher) and RDF (SPARQL).

### 199. Neptune Analytics
Adds vector search and graph analytics capabilities — PageRank, community detection, shortest path, centrality — to existing Neptune databases. Enables ML-informed graph queries: find the most influential fraud cluster, recommend items based on graph distance. Runs analytics as managed queries alongside OLTP workloads.

### 200. Neptune Serverless
Automatically scales Neptune compute capacity up and down based on workload demand, including scaling to near-zero during idle periods. Eliminates the need to choose and manage instance sizes for graph workloads. Billed per Neptune Capacity Unit (NCU)-second.

### 201. AWS Network Firewall
A managed stateful network firewall and IDS/IPS for VPCs. Uses Suricata-compatible rules for deep packet inspection, domain-based filtering, and protocol anomaly detection. Deployed in a dedicated firewall subnet; Traffic must be routed through it via route table manipulation.

### 202. Network Firewall Managed Rule Groups
Pre-built Suricata rule sets maintained by AWS and third-party vendors (CrowdStrike, Proofpoint, etc.) covering known malware domains, command-and-control infrastructure, and exploit signatures. Customers subscribe to managed rule groups without writing or maintaining their own rules.

---

## O

### 203. Amazon OpenSearch Service
Managed OpenSearch (forked from Elasticsearch) for log analytics, full-text search, and operational dashboards.

### 204. OpenSearch Cold Storage
Moves older, infrequently queried indices to S3-backed cold storage at significantly lower cost than warm storage. Data is accessible but requires a brief attach step before querying. Part of the OpenSearch UltraWarm and Cold tiered storage model.

### 205. OpenSearch Serverless
Runs OpenSearch without provisioning or managing clusters. Capacity scales automatically based on indexing and search demand. Separates indexing and search into independent scaling dimensions. Priced per OCU (OpenSearch Compute Unit) consumed. Right for variable or unpredictable search/analytics workloads.

### 206. OpenSearch UltraWarm
Adds a warm storage tier backed by S3 with dedicated warm nodes that serve queries. Index data moves automatically from hot (primary) to warm storage based on age. Warm storage costs significantly less than hot primary storage for infrequently queried log data while remaining fully queryable without re-attaching.

### 207. AWS Organizations
Centrally manages multiple AWS accounts with OUs, SCPs, and consolidated billing.

### 208. Organizations AI Services Opt-Out Policy
An Organization policy that opts out all accounts in the Organization (or specific OUs) from having their data used to train AWS AI services. Applies to Comprehend, Lex, Polly, Rekognition, Textract, Transcribe, and others. Relevant for customers with strict data privacy requirements who want to prevent any customer data from leaving their control for model training.

### 209. Organizations Backup Policies
Organization-wide policies that mandate AWS Backup plans across all member accounts. Define backup frequency, retention, vault configuration, and resource selection. Ensures that every account complies with the organization's data protection requirements without relying on individual account administrators.

### 210. Organizations Service Control Policies (SCPs)
Maximum permission guardrails for accounts or OUs. Do not grant permissions — only restrict. An explicit Deny in an SCP overrides any IAM policy in the account. Common SCPs: restrict to approved Regions, prevent disabling GuardDuty/CloudTrail, block IAM user creation, restrict instance types, prevent root account usage.

### 211. Organizations Tag Policies
Enforce consistent resource tagging across the Organization. Define allowed tag keys and allowed values for each key. Tag policies prevent misconfigured tags (typos, non-standard values) that break cost allocation reports. Non-compliant resources are reported in the Tag Policy compliance report.

---

## P

### 212. Amazon Personalize
A fully managed ML service for real-time personalization and recommendations. Upload interaction data; Personalize trains a recommendation model automatically.

### 213. Personalize Campaigns
A deployed recommendation solution that serves real-time recommendations via API. Each campaign is backed by a trained solution version. Campaigns have minimum TPS (provisioned throughput) and auto-scale above that minimum based on demand. Personalize returns ranked item lists with scores per user.

### 214. Personalize Event Tracker
Captures real-time user interaction events (clicks, views, purchases, ratings) from a website or application and sends them to Personalize. Events are used both to retrain models over time and to immediately influence recommendations in real time (without waiting for a full model retrain). Enables the "you just viewed X, here are similar items" real-time feedback loop.

### 215. Personalize Filters
SQL-like expressions applied to recommendation results to exclude or include items based on business rules — "don't recommend items the user has already purchased," "only recommend items in the user's subscription tier," "only show in-stock products." Applied at query time on top of the ML model output.

### 216. Amazon Pinpoint
A multi-channel customer engagement service for email, SMS, push notifications, and voice. Combines segmentation, journey orchestration, and analytics.

### 217. Pinpoint Journeys
Visual, multi-step message orchestration workflows. Define entry conditions (user attributes, events), branch logic (if user opened email → send push; else → send SMS), wait steps (24 hours after email, then check open), and end conditions. Used for onboarding flows, re-engagement campaigns, and lifecycle marketing.

### 218. Pinpoint Segments
Groups of users or endpoints (email addresses, device tokens, phone numbers) defined by user attributes, behavioral data, or imported lists. Dynamic segments automatically update based on real-time data; imported segments are static lists uploaded from CSV or S3. Campaigns and Journeys target segments.

### 219. AWS PrivateLink
Private connectivity from VPCs to AWS services and customer-hosted services without traversing the public internet. Creates Interface Endpoints (ENIs with private IPs).

### 220. PrivateLink Endpoint Services
Allows a customer to expose their own service (hosted behind an NLB) to other VPCs or accounts via PrivateLink. Consumers create Interface Endpoints to the service; traffic flows privately over AWS backbone without VPC peering, IGW, or public IPs. Used for SaaS providers offering private connectivity and for sharing internal services across accounts without VPC peering.

---

## Q

### 221. Amazon QuickSight
Cloud-native BI service with SPICE in-memory engine. Authors build dashboards; readers consume them.

### 222. QuickSight Embedded Analytics
Embeds QuickSight dashboards and visuals directly into customer-facing applications using a generated URL or SDK. Registered user embedding (per-session auth) for internal users; anonymous embedding (one-click access) for external customers. Enables building SaaS analytics features without building a custom BI layer.

### 223. QuickSight ML Insights
Automatically surface ML-driven insights within dashboards — anomaly detection (flags unexpected data points), forecasting (projects time-series data forward), and contribution analysis (explains which dimensions drive a metric change). Available to all QuickSight users without ML knowledge.

### 224. QuickSight Q (Natural Language Queries)
Business users type natural language questions ("What were total sales last quarter by region?") and QuickSight Q generates a visualization automatically using ML. Q Topics must be configured by an author (defining which datasets, fields, and synonyms Q can use). Lowers the barrier to self-service analytics.

### 225. QuickSight SPICE
Super-fast, Parallel, In-memory Calculation Engine. Caches dataset data in SPICE for fast interactive query performance — sub-second dashboard loading even on large datasets. SPICE capacity is allocated per user and per Region. Datasets can be scheduled to refresh SPICE on a cadence (hourly to daily). Direct Query mode bypasses SPICE for real-time data at the cost of query latency.

---

## R

### 226. Amazon RDS (Relational Database Service)
Managed relational databases — MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Aurora. AWS handles patching, backups, and Multi-AZ failover.

### 227. RDS Blue/Green Deployments
Creates a staging environment (green) that mirrors the production RDS cluster (blue) and keeps them synchronized using logical replication. Schema changes, engine upgrades, and parameter changes are applied to green and validated before a one-click switchover — with typically < 1 minute of downtime. Rollback reverts to blue in seconds. Available for RDS MySQL and Aurora MySQL.

### 228. RDS Custom
Provides access to the underlying OS and database engine for RDS Oracle and SQL Server — enabling customization that standard RDS doesn't allow: installing agents, patching on a custom schedule, modifying OS parameters. Sits between self-managed EC2 (full control) and standard RDS (zero access). Required for Oracle licensing models that mandate specific OS-level configurations.

### 229. RDS Enhanced Monitoring
Provides real-time OS-level metrics (CPU, memory, file system, disk I/O, swap) from the RDS host at up to 1-second granularity — versus the 1-minute minimum for standard CloudWatch RDS metrics. Delivered to CloudWatch Logs. Essential for diagnosing OS-level resource contention on RDS instances (e.g., high memory pressure from OS processes versus database processes).

### 230. RDS Multi-AZ
Maintains a synchronous standby replica of an RDS instance in a different AZ. Automatic failover in under 60 seconds if the primary fails. No data loss (synchronous replication). Failover is transparent to the application because the RDS endpoint DNS record is updated automatically. Not used for read scaling — use Read Replicas for that.

### 231. RDS Performance Insights
A database performance monitoring tool that makes it easy to detect and diagnose database load. Dashboard shows database load (in AAS — Average Active Sessions) broken down by wait type, SQL statement, host, and user. Identifies the exact query causing performance problems without requiring deep DBA expertise. Available for Aurora, MySQL, PostgreSQL, MariaDB, Oracle, and SQL Server on RDS.

### 232. RDS Proxy (see earlier entry)

### 233. RDS Read Replicas
Asynchronous read-only copies of an RDS or Aurora primary instance for horizontal read scaling. Applications direct read-heavy queries (reports, analytics, search) to replicas, offloading the primary. Up to 15 read replicas for Aurora, 5 for RDS MySQL/PostgreSQL. Read replicas can be promoted to standalone DB instances for migrations or regional failover.

### 234. Amazon Redshift
A petabyte-scale cloud data warehouse using columnar storage and MPP.

### 235. Redshift Concurrency Scaling
Automatically adds transient Redshift clusters to handle query bursts — providing consistent fast performance regardless of the number of concurrent queries. Customers get 1 hour of free concurrency scaling credits per 24 hours of main cluster usage. Beyond the free credits, concurrency scaling clusters are billed per second.

### 236. Redshift Data API
Allows running SQL queries against a Redshift cluster or Redshift Serverless asynchronously via API — without managing JDBC/ODBC connections. The API returns a query ID immediately; results are retrieved when ready. Enables serverless applications (Lambda functions, microservices) to interact with Redshift without persistent database connections.

### 237. Redshift Data Sharing
Enables live, read-only access to data in one Redshift cluster (producer) from another Redshift cluster or Redshift Serverless (consumer) — across accounts or within an account — without copying or moving data. Consumers always query the latest data in the producer's cluster. Eliminates ETL pipelines between data warehouses for cross-team data sharing.

### 238. Redshift Federated Query
Extends Redshift SQL to query data in RDS and Aurora (PostgreSQL and MySQL) directly, alongside Redshift tables and S3 data. Joins between operational databases and the data warehouse in a single query — without ETL. Performance depends on network bandwidth and the source database's ability to push down predicates.

### 239. Redshift ML
Trains, deploys, and runs ML models using SQL. `CREATE MODEL` triggers a SageMaker Autopilot training run on data in Redshift; the model is deployed as a Lambda function callable from Redshift SQL. Enables analysts to run ML inference directly in SQL without extracting data to SageMaker.

### 240. Redshift RA3 Nodes
RA3 instances separate compute from storage using Redshift Managed Storage (RMS) — high-performance SSD for hot data, backed by S3 for data that doesn't fit in SSD. Compute and storage scale independently. The standard node type for new Redshift clusters; enables resizing compute without migrating data.

### 241. Redshift Serverless
Runs Redshift analytics without provisioning clusters. Automatically scales compute capacity (RPU — Redshift Processing Units) based on workload demand. Billed per RPU-second plus storage. Ideal for intermittent analytics workloads and dev/test environments where paying for an idle cluster is wasteful.

### 242. Redshift Spectrum
Queries data directly in S3 (in Parquet, ORC, CSV, JSON, Avro, and more) using Redshift compute — without loading data into the warehouse. Uses a separate, serverless scaling layer so Spectrum queries don't consume Redshift cluster resources. Enables a single SQL query to join Redshift warehouse tables with data lake data in S3.

### 243. Amazon Rekognition
A computer vision service for analyzing images and video.

### 244. Rekognition Custom Labels
Trains a custom image classification or object detection model using customer-provided labeled images. Amazon AutoML handles model training — no ML expertise required. Inference is available as a hosted endpoint or batch job. Used for detecting domain-specific objects (product defects, custom logos, medical images) that Rekognition's general models don't cover.

### 245. Rekognition Video
Processes video files stored in S3 or live streams (via Kinesis Video Streams) for face search, object detection, activity recognition, text detection, and content moderation. Asynchronous API for stored video (submit job → poll or receive SNS notification); streaming analysis API for live video.

### 246. Amazon Route 53
AWS's DNS and domain registration service.

### 247. Route 53 Health Checks
Monitor endpoints (HTTP/HTTPS/TCP) or other CloudWatch alarms. Route 53 removes unhealthy endpoints from DNS responses (via failover or multivalue routing). Can monitor the health of a Region and trigger a DNS-level failover to a backup Region automatically. Three types: endpoint health checks, calculated health checks (combine multiple), and CloudWatch alarm health checks.

### 248. Route 53 Hosted Zones
A container for DNS records for a domain. **Public Hosted Zones** are accessible from the public internet. **Private Hosted Zones** are associated with VPCs and resolve only for resources within those VPCs — used for internal service discovery (e.g., `db.internal → 10.0.1.50`).

### 249. Route 53 Resolver
A managed DNS service for hybrid architectures. **Inbound Endpoints** allow on-premises DNS servers to resolve AWS private hosted zone names. **Outbound Endpoints** allow VPC resources to resolve on-premises domain names via on-premises DNS servers. DNS Firewall blocks queries to known malicious domains using managed or custom domain lists.

### 250. Route 53 Routing Policies
**Simple**: single value or multiple values (random selection by client). **Weighted**: percentage-based traffic splitting. **Latency**: routes to the Region with the lowest network latency for the user. **Failover**: active-passive with health check-based switching. **Geolocation**: routes based on the user's geographic location. **Geoproximity**: routes based on geographic distance, with configurable bias. **Multivalue Answer**: returns up to 8 healthy records (basic load balancing at DNS level).

### 251. Route 53 Traffic Flow
A visual editor for building complex routing configurations using multiple routing policies in a tree structure. Route traffic through multiple levels of rules — e.g., geoproximity within each Region, then latency within each location, then failover between AZs. Traffic Flow configurations (policies) can be versioned and reused across multiple record sets.

---

## S

### 252. Amazon S3 (Simple Storage Service)
Object storage with 11 nines of durability. The data lake backbone of AWS.

### 253. S3 Access Points
Named network endpoints attached to an S3 bucket, each with its own access policy and optional VPC restriction. Simplify managing access to shared datasets — instead of one complex bucket policy, each team, application, or use case has its own access point with targeted permissions. An S3 bucket can have thousands of access points.

### 254. S3 Batch Operations
Runs bulk S3 operations — copying, tagging, restoring from Glacier, ACL changes, Lambda invocations — across millions or billions of objects using a manifest (S3 Inventory report or CSV). A single Batch Operations job can process billions of objects in hours. Replaces manual scripting for large-scale S3 data management tasks.

### 255. S3 Cross-Region Replication (CRR)
Asynchronously copies objects from a source bucket to a destination bucket in a different AWS Region. Replicates new objects (not existing objects, unless using S3 Batch Operations for backfill). Used for disaster recovery, compliance (keep a copy in a specific country), and latency reduction (serve data from a closer Region). Versioning must be enabled on both buckets.

### 256. S3 Event Notifications
Triggers actions when objects are created, deleted, restored from Glacier, or have replication failures. Targets: SQS queues, SNS topics, Lambda functions, and EventBridge (for advanced filtering and fan-out). The foundation for object-driven event pipelines — e.g., "invoke Lambda when a new CSV file arrives in S3."

### 257. S3 Intelligent-Tiering
Automatically moves objects between access tiers based on usage patterns. Frequent Access (default) → Infrequent Access (30 days inactive) → Archive Instant Access (90 days inactive) → Archive Access (90–730 days, optional) → Deep Archive Access (180–730 days, optional). No retrieval fees; small per-object monitoring fee. The right default for unpredictable data lake access patterns.

### 258. S3 Inventory
Generates daily or weekly CSV or ORC reports listing all objects in a bucket along with their metadata — size, last-modified date, storage class, replication status, encryption status, object lock retention mode. Used as input to S3 Batch Operations, as an input to cost analysis, and for auditing object-level compliance attributes.

### 259. S3 Lifecycle Policies
Rules that automatically transition objects to cheaper storage classes or delete objects after a defined number of days. Example: move to Standard-IA after 30 days, Glacier after 90 days, delete after 365 days. Reduces storage costs without manual intervention. Applied at the bucket or prefix level.

### 260. S3 Multi-Region Access Points
A single global endpoint that routes S3 requests to the nearest available S3 bucket across multiple Regions. Built-in failover routing — if one Region is degraded, traffic automatically fails over to the next closest healthy bucket. Simplifies globally distributed application architecture that reads/writes S3 data.

### 261. S3 Object Lambda
Runs a Lambda function on data returned by S3 GetObject API calls. The function can redact PII, convert formats, filter rows, or add watermarks on the fly — without storing transformed copies. Applications call a standard S3 API; the Lambda transformation is transparent.

### 262. S3 Object Lock
Implements WORM (Write Once Read Many) storage using retention policies. **Compliance mode**: even the root account cannot delete or modify an object during the retention period. **Governance mode**: accounts with special IAM permissions can override. **Legal Hold**: indefinitely locks an object without a retention date. Required for SEC Rule 17a-4, HIPAA, FINRA, and similar regulations mandating immutable records.

### 263. S3 Replication Time Control (RTC)
A feature of S3 Cross-Region Replication that guarantees 99.99% of objects are replicated within 15 minutes. Provides CloudWatch metrics to monitor replication lag and compliance. Required when regulations mandate that replicated data be available within a specific SLA.

### 264. S3 Same-Region Replication (SRR)
Asynchronously copies objects from a source bucket to a destination bucket in the same AWS Region. Used for aggregating logs from multiple source buckets into one, creating separate production and test environments from the same data, and complying with data residency requirements that prohibit data from leaving the Region.

### 265. S3 Select
Retrieves a subset of data from a single S3 object using SQL expressions — filtering rows and projecting columns before data leaves S3. Reduces data transfer and speeds up retrieval for applications that need a fraction of a large CSV, JSON, or Parquet file.

### 266. S3 Storage Lens
An organization-wide visibility tool providing a single dashboard of S3 storage across all buckets, accounts, and Regions in an Organization. Metrics include total storage, object count, access patterns, data protection coverage, and cost efficiency recommendations. Identifies buckets with no versioning, no lifecycle policy, or no encryption. The starting point for S3 cost optimization and governance programs.

### 267. S3 Transfer Acceleration
Speeds up S3 uploads by routing traffic through CloudFront edge PoPs over the private AWS backbone. Most effective for large file uploads from geographically distant locations.

### 268. S3 Versioning
Preserves every version of every object in a bucket. Protects against accidental deletion (delete creates a delete marker; previous versions are retained) and overwrites. Required for S3 Cross-Region Replication, S3 Replication Time Control, and S3 Object Lock. Versioning adds storage cost — Lifecycle Policies with noncurrent version expiration manage this.

### 269. Amazon SageMaker
The end-to-end ML platform for building, training, and deploying ML models.

### 270. SageMaker Autopilot
Automatically trains and tunes ML models for tabular data (classification, regression). Customers provide a dataset and specify the target column; Autopilot explores algorithm options, generates feature engineering code (visible and editable), and produces a ranked leaderboard of candidate models. The no-code/low-code entry point to SageMaker for structured data problems.

### 271. SageMaker Canvas
A no-code ML interface for business analysts. Upload data, select the target column, build and evaluate a model, and generate predictions — without writing code. Under the hood, uses SageMaker Autopilot. Predictions can be exported to S3 or integrated with business applications. Includes natural language data preparation powered by Bedrock.

### 272. SageMaker Clarify
Detects bias in datasets and ML models, and generates model explanations (feature importance using SHAP values). Runs as a processing job during training and as a monitor on live inference endpoints. Produces human-readable bias reports and explainability reports. Required for responsible AI and regulated ML use cases (GDPR right to explanation, financial model fairness).

### 273. SageMaker Data Wrangler
A visual data preparation tool for ML feature engineering inside SageMaker Studio. 300+ built-in data transformations; integrates with S3, Athena, Redshift, Lake Formation, and SaaS data sources. Generates PySpark or Pandas code from visual transformations, which can be exported to a Glue job or SageMaker Pipeline. Bridges the gap between data analysts and ML engineers.

### 274. SageMaker Debugger
Captures tensors and metrics during model training in real time and detects training problems — vanishing gradients, overfitting, underutilization of GPU — without stopping the training job. Built-in rules cover common deep learning training issues; custom rules can be written in Python. Profiling mode generates a detailed system performance report (GPU utilization, I/O bottlenecks, framework overhead).

### 275. SageMaker Distributed Training
Libraries for training large ML models across multiple GPU instances. Two approaches: **Data Parallel** (copies the model to each GPU, splits training data — right for most models) and **Model Parallel** (splits the model across GPUs when the model is too large to fit on a single GPU — right for large language models and foundation model fine-tuning). Both are SageMaker-native libraries optimized for AWS GPU instances.

### 276. SageMaker Experiments
Tracks, compares, and manages ML experiments — training runs, hyperparameters, metrics, and artifacts. Each trial automatically records inputs, outputs, and metrics. The experiment dashboard allows comparing runs side-by-side to identify the best model configuration. Integrates with SageMaker Training Jobs, Pipelines, and notebooks.

### 277. SageMaker Feature Store
A managed repository for ML features. Features are computed once and stored in Feature Store — both in an online store (low-latency retrieval for real-time inference, backed by DynamoDB) and an offline store (historical feature retrieval for training, backed by S3). Ensures training and inference use the same feature definitions, preventing training-serving skew.

### 278. SageMaker Ground Truth
A managed data labeling service. Supports text, image, video, and 3D point cloud labeling tasks. Labeling workforces can be Amazon Mechanical Turk (public), private (internal team), or AWS-vetted vendors. Ground Truth Plus uses pre-trained models to auto-label high-confidence examples and routes only uncertain ones to humans, reducing labeling cost by up to 70%.

### 279. SageMaker HyperPod
A resilient compute infrastructure for training large foundation models and fine-tuning them at scale. HyperPod clusters span multiple instances with high-bandwidth networking (EFA — Elastic Fabric Adapter); the cluster management layer automatically detects and replaces failed nodes without interrupting long-running training jobs. Used for training models with billions of parameters where job failures are expensive.

### 280. SageMaker Inference
Hosts trained ML models and serves predictions. Four modes: **Real-time Endpoints** (persistent, low-latency REST endpoint), **Serverless Inference** (auto-scales to zero when idle, cold starts in seconds — for intermittent traffic), **Asynchronous Inference** (queued, large payload inference — up to 1 GB request, no timeout), **Batch Transform** (one-off or scheduled batch predictions on S3 data, no endpoint needed).

### 281. SageMaker JumpStart
A hub of pre-trained foundation models and ML solutions deployable with a few clicks. Foundation models include open-source models (Llama, Mistral, Falcon, Stable Diffusion) deployable on SageMaker endpoints. Solutions are end-to-end ML use case templates (fraud detection, predictive maintenance, churn prediction) with sample code and data. Lowers the barrier to experimenting with pre-trained models.

### 282. SageMaker Model Monitor
Continuously monitors deployed ML models for data quality drift, model quality drift (prediction accuracy), bias drift, and feature attribution drift. Compares live inference data against a baseline captured during training. Fires CloudWatch alarms when drift is detected. The operationalization layer that ensures a model in production remains accurate over time as input data distributions change.

### 283. SageMaker Model Registry
A centralized catalog for versioned, trained ML models. Models progress through stages (Staging → Production) via approval workflows. Each model version records the training job, metrics, container image, and artifact location. Integrates with SageMaker Pipelines for CI/CD — approved models automatically deploy to endpoints.

### 284. SageMaker Pipelines
A managed CI/CD service for ML workflows — automating data preparation, model training, evaluation, approval, and deployment as a reusable, parameterized pipeline. Each pipeline step is a SageMaker job or condition. Pipeline runs are tracked in SageMaker Experiments. The MLOps automation layer that enables reproducible ML workflows.

### 285. SageMaker Studio
The managed web-based IDE for ML — notebooks, experiments, training, models, pipelines, and monitoring in a unified interface. Each Studio user gets a personal JupyterServer backed by EFS. Studio also includes SageMaker Canvas, Data Wrangler, Feature Store, Model Registry, and Pipelines integration. The single entry point for all SageMaker workflows.

### 286. Amazon SES (Simple Email Service)
Cloud-based email sending for transactional and marketing email. SMTP relay or API; sub-cent per thousand emails.

### 287. SES Configuration Sets
Groups of rules applied when sending email. Actions include: publishing sending events (deliveries, bounces, complaints, opens, clicks) to CloudWatch, Kinesis Data Firehose, or SNS; enabling virtual deliverability manager recommendations; applying IP pool selection. Used for tracking deliverability metrics and routing email through specific dedicated IP pools.

### 288. SES Dedicated IP Addresses
Exclusive IP addresses for sending email — not shared with other AWS customers. Protects sender reputation: your sending behavior affects only your IPs. Two types: **Dedicated IPs** (fixed IPs, higher cost, managed manually or via Dedicated IP pools); **Managed Dedicated IPs** (AWS manages warming and pool assignment automatically).

### 289. SES Virtual Deliverability Manager
An ML-powered tool that analyzes sending behavior, identifies deliverability issues (high bounce rates, ISP blocks, missing authentication), and provides specific recommendations to improve inbox placement rates. Integrates with SES metrics and provides an account-level deliverability dashboard.

### 290. AWS Step Functions
A serverless workflow orchestration service using state machines.

### 291. Step Functions Activity Tasks
Long-running workflow steps where work is performed outside of AWS (on-premises systems, mobile devices, IoT sensors). The state machine waits for an external worker to poll for work, complete the task, and send a success/failure callback using a task token. Unlike Lambda (push-based), activities use a pull model.

### 292. Step Functions Express Workflows
Designed for high-volume, short-duration workloads. At-least-once execution semantics; up to 5 minutes duration; priced per state transition. Used for IoT data processing, streaming analytics, and high-rate event processing where cost per invocation matters more than exactly-once guarantees.

### 293. Step Functions Standard Workflows
Designed for long-running, durable workflows requiring exactly-once execution. State history is persisted for 90 days and visible in the console. Supports human approval steps (Wait for Callback), map states (parallel iteration over arrays), parallel branches, error handling with retry/catch, and timeouts up to 1 year.

### 294. Step Functions SDK Integrations
Direct integrations with 200+ AWS service APIs without requiring Lambda as a middleware. Supported services include: DynamoDB (GetItem, PutItem), S3 (GetObject, PutObject), SNS, SQS, Glue, Athena, EMR, ECS, Batch, SageMaker, Bedrock, and many more. Reduces the number of Lambda functions in a workflow, lowering latency and cost.

### 295. AWS Systems Manager (SSM)
A unified operations hub for EC2, on-premises servers, and edge devices.

### 296. SSM AppConfig
Deploys application configuration changes with gradual rollouts, schema validation, and automatic rollback if error metrics spike. Separates configuration changes from code deployments for feature flags, A/B test parameters, and operational toggles.

### 297. SSM Automation
Managed operational runbooks — multi-step automation documents (SSM Documents of type Automation) that perform tasks like patching an AMI, restarting an application stack, creating a backup, or responding to a security finding. Can be triggered by CloudWatch Events, scheduled, or invoked manually. Includes pre-built AWS-authored runbooks for common operations.

### 298. SSM Distributor
Packages and deploys software to EC2 instances and on-premises servers at scale — agents, security software, AWS tools. Distributor packages are versioned and can be installed on demand via Run Command or on a schedule via State Manager.

### 299. SSM Inventory
Collects metadata from managed instances — installed applications, OS configuration, Windows Registry, running services, network configuration. Queryable via the SSM console or via S3 + Athena for fleet-wide analysis. Used for software compliance, license management, and operational baseline documentation.

### 300. SSM OpsCenter
A central hub for viewing and resolving operational issues (OpsItems) surfaced from CloudWatch Alarms, EventBridge events, Config rules, GuardDuty findings, and other sources. Each OpsItem includes related CloudWatch metrics, run books, and resource information — reducing the time to diagnose and resolve incidents.

### 301. SSM Parameter Store
Centralized configuration and secret storage. Plain text (String), encrypted (SecureString using KMS), or structured (StringList). Hierarchical naming (e.g., `/app/prod/db-password`). Integrates with Lambda, ECS, EC2 Launch Templates, CloudFormation, and CodeBuild. Free for standard parameters; Advanced parameters support larger values and parameter policies (expiration notifications).

### 302. SSM Patch Manager
Automates OS patching across a fleet of EC2 and on-premises instances. Patch baselines define approved patches and auto-approval rules (e.g., auto-approve security patches 7 days after release). Maintenance Windows schedule patching during defined periods. Patch compliance reports surface unpatched instances. Supports Windows, Amazon Linux, Ubuntu, RHEL, SUSE, Debian.

### 303. SSM Run Command
Executes commands (shell scripts, PowerShell, AWS CLI commands) remotely on one or more EC2 or on-premises instances without SSH or bastion hosts. Uses SSM Agent for secure communication. Results are streamed to the console, S3, or CloudWatch Logs. Rate controls prevent overwhelming a large fleet. Used for ad hoc operations, incident response, and bootstrapping.

### 304. SSM Session Manager
Browser-based, SSH-free shell access to EC2 instances and on-premises servers. No need to open port 22, manage SSH keys, or run a bastion host. All sessions are logged to S3 or CloudWatch Logs for audit. IAM-controlled access with optional MFA enforcement. Works via the AWS console, CLI (`aws ssm start-session`), or through standard SSH tunneling (SSH over SSM).

### 305. SSM State Manager
Enforces a desired configuration state on managed instances — ensures that specific software is installed, specific agents are running, or specific settings are configured. Associations define the SSM Document and schedule; State Manager runs the association and reports compliance. Prevents configuration drift from the defined baseline.

---

## T

### 306. Amazon Textract
ML service for extracting text and structured data (forms, tables, signatures) from scanned documents.

### 307. Textract Analyze Lending
Purpose-built document analysis for mortgage and loan workflows — US paystubs, W-2 forms, 1003 mortgage applications, bank statements. Returns normalized fields (gross income, employer name, loan amount) already mapped to lending data schemas. Reduces custom extraction code for financial services customers.

### 308. Textract Queries
Instead of extracting everything from a document, Queries lets you ask specific questions ("What is the patient name?", "What is the invoice total?") and Textract returns only those values. Reduces processing cost for documents where you only need a few fields, and improves accuracy by focusing extraction on specific content.

### 309. Amazon Timestream
Serverless time-series database for IoT and operational metrics. Separate memory and magnetic storage tiers.

### 310. Timestream Live Analytics
Runs real-time SQL queries on time-series data directly from the memory store — without moving data to the magnetic store. Sub-millisecond query latency for the most recent data. Used for operational dashboards and real-time anomaly detection on streaming IoT sensor data.

### 311. Amazon Transcribe
Automatic speech recognition (ASR) service converting audio to text.

### 312. Transcribe Call Analytics
Purpose-built for contact center audio analysis. Automatically transcribes calls, identifies speakers (agent vs. customer), detects sentiment per turn, flags interruptions and talk time ratios, detects customer issue categories, and summarizes call outcomes. Reduces the cost of post-call quality monitoring compared to human review.

### 313. Transcribe Medical
Specialized ASR for clinical conversations — clinic visits, surgical procedures, telemedicine. Trained on medical terminology; returns HIPAA-eligible transcriptions. Supports specialty vocabularies (cardiology, neurology, radiology, etc.).

### 314. AWS Transfer Family
Managed SFTP, FTPS, FTP, and AS2 file transfer service backed by S3 or EFS.

### 315. Transfer Family AS2
Adds AS2 (Applicability Statement 2) protocol support for B2B EDI file exchange — the protocol required by many retailers (Walmart, Target) and healthcare trading partners (X12 EDI). Handles message signing, encryption, MDN acknowledgements, and partner certificate management. Enables AWS-native EDI without on-premises AS2 servers.

### 316. Transfer Family Custom Identity Provider
Integrates Transfer Family with any identity source — Microsoft Active Directory, Okta, custom Lambda-based authentication — via API Gateway + Lambda. Allows validating SFTP credentials against an existing user directory without migrating users to Cognito or IAM. Used by customers with established SFTP partner authentication systems.

### 317. AWS Transit Gateway
A network hub connecting multiple VPCs and on-premises networks.

### 318. Transit Gateway Network Manager
Provides a global, centralized view of the AWS and hybrid network topology — VPCs, Transit Gateways, Direct Connect, and VPN connections across all Regions and accounts. Visualizes as a network map; monitors path health; provides routing analytics (which path does traffic take from A to B?). Generates CloudWatch Events for network topology changes.

### 319. Transit Gateway Multicast
Distributes a single data stream to multiple VPCs simultaneously — without individual unicast connections from source to each receiver. Used for video conferencing, financial market data feeds, and software distribution where the same data must reach many destinations with minimal bandwidth overhead.

### 320. Transit Gateway Route Tables
Separate route tables within a Transit Gateway that control which attachments (VPCs, VPN, Direct Connect) can communicate with each other. Used to implement network segmentation — e.g., production VPCs cannot route traffic to development VPCs, but both can route to shared services VPCs. Supports blackhole routes to drop traffic to specific destinations.

---

## V

### 321. Amazon VPC (Virtual Private Cloud)
The networking foundation of AWS. Define IP ranges, subnets, routing, and access controls.

### 322. VPC DHCP Option Sets
Configure which DNS servers, NTP servers, and domain names are assigned to VPC instances via DHCP. Customizing the DNS server allows VPC instances to use on-premises DNS servers (for hybrid DNS resolution) or a custom DNS server. Each VPC has one DHCP option set; AWS provides a default that uses AmazonProvidedDNS (Route 53 Resolver).

### 323. VPC Endpoint Policies
IAM resource-based policies attached to VPC Gateway and Interface Endpoints that control which principals and S3 buckets (for Gateway Endpoints) can be accessed through the endpoint. Endpoint policies add a layer of security beyond bucket policies and IAM policies — traffic through the endpoint can be restricted to specific buckets or actions, preventing data exfiltration to unauthorized S3 buckets.

### 324. VPC Flow Logs
Captures IP traffic metadata to/from VPC network interfaces. Published to CloudWatch Logs, S3, or Kinesis Data Firehose. Used for security analysis, network troubleshooting, and compliance. Custom log formats can include additional fields (traffic path, TCP flags, packet-level details).

### 325. VPC Peering
Private network connection between two VPCs via the AWS backbone. Non-transitive; CIDRs must not overlap. For many VPCs, Transit Gateway is preferred.

### 326. VPC Reachability Analyzer
A network diagnostics tool that analyzes the configuration of VPC networking components (security groups, NACLs, route tables, IGW, NAT GW, VPC Peering, TGW) to determine whether a network path exists between two endpoints — without sending actual traffic. Returns a hop-by-hop analysis showing where connectivity is blocked and why. Replaces manual route table and security group inspection.

### 327. VPC Sharing (Resource Access Manager)
Allows sharing VPC subnets with other AWS accounts in the same Organization using AWS Resource Access Manager (RAM). The subnet owner account controls the networking; participant accounts launch resources (EC2, RDS, Lambda) into the shared subnets. Centralizes network management in a single account while allowing multiple teams to use the same VPC — reducing VPC sprawl and Transit Gateway peering complexity.

### 328. VPC Traffic Mirroring
Copies network traffic from an EC2 instance's ENI to a monitoring appliance (an EC2 instance or NLB) for deep packet inspection, IDS/IPS analysis, or network forensics — without disrupting the original traffic. Filters control which traffic is mirrored (by port, protocol, CIDR). Used for security monitoring use cases that require full packet capture rather than just flow logs.

### 329. AWS VPN — Client VPN
A managed OpenVPN-based remote access VPN. End users install the AWS Client VPN or any OpenVPN-compatible client and connect to a Client VPN endpoint associated with a VPC. Scales automatically; authentication via Active Directory, SAML/SSO (Okta, Entra ID), or mutual certificate authentication. Split tunneling sends only VPC-destined traffic through the VPN; full tunneling sends all traffic through it.

### 330. AWS VPN — Site-to-Site VPN
An IPSec VPN connecting an on-premises Customer Gateway device to a Virtual Private Gateway or Transit Gateway. Two redundant tunnels per connection (active-active); up to 1.25 Gbps per tunnel. Used as the primary connectivity method for smaller customers and as a backup path for Direct Connect customers. Accelerated VPN option routes traffic over AWS Global Accelerator for improved performance.

---

## W

### 331. AWS WAF (Web Application Firewall)
Protects web applications from common exploits. Deploys in front of CloudFront, ALB, API Gateway, AppSync.

### 332. WAF Bot Control
A managed rule group (additional fee) that detects and controls bot traffic. Distinguishes legitimate bots (Google, LinkedIn scrapers) from malicious bots (credential stuffers, scrapers, DDoS bots). Common bots are allowed or blocked with pre-built rules; targeted inspection uses ML to detect sophisticated bots that mimic human behavior. Reduces fraudulent API usage and infrastructure load from bot traffic.

### 333. WAF Fraud Control — Account Creation Fraud Prevention
Detects automated account creation abuse (fake account farms, promotion abuse, credential stuffing during registration). Uses ML to score each account creation request and block high-risk submissions. Priced per protected endpoint.

### 334. WAF Fraud Control — Account Takeover Prevention (ATP)
Monitors login endpoints for credential stuffing and brute force attacks. Analyzes credential usage patterns, stolen credential databases, and request fingerprints. Automatically blocks high-volume login abuse while allowing legitimate users through. Requires the WAF SDK in the application to capture login success/failure signals.

### 335. WAF Managed Rule Groups
Pre-built rule sets maintained by AWS and third-party vendors. AWS-managed groups include: Core Rule Set (OWASP Top 10), Known Bad Inputs (common attack patterns), SQL Database, Linux/Windows OS, PHP, and WordPress. Third-party managed rules from CrowdStrike, F5, Imperva, and others cover more specialized threat intelligence. Customers pay a subscription fee per managed rule group.

### 336. WAF Web ACLs
The top-level WAF resource containing an ordered list of rules and rule groups. Each rule has a priority, conditions, and an action (Allow, Block, Count, CAPTCHA, Challenge). Rules are evaluated in priority order; the first matching rule's action applies. A Web ACL is associated with one or more resources (CloudFront distributions, ALBs, API Gateways). Default action (allow or block) applies when no rule matches.

### 337. AWS Well-Architected Framework
Best practices across six pillars: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, and Sustainability.

### 338. Well-Architected Lenses
Extensions to the Well-Architected Framework for specific industries or workload types. AWS provides lenses for: Serverless, SaaS, Data Analytics, IoT, Machine Learning, Financial Services, Healthcare, High Performance Computing, Media & Entertainment, and Hybrid Networking. Each lens adds domain-specific questions and best practices on top of the base framework pillars.

### 339. Well-Architected Tool
A console-based questionnaire tool guiding formal workload reviews against the Framework. Generates findings reports with High and Medium risks. Milestones track improvement over time. Supports custom lenses and can be shared across accounts for partner-led reviews.

### 340. AWS WorkSpaces
Cloud-hosted virtual desktops (VDI). WorkSpaces Personal: persistent individual desktops. WorkSpaces Pools: non-persistent pooled desktops for task workers. Pay per month (AlwaysOn) or per hour (AutoStop).

### 341. WorkSpaces Thin Client
A low-cost hardware device (the Amazon WorkSpaces Thin Client) for connecting to WorkSpaces, AppStream 2.0, and other virtual desktop services. Plug-and-play; no OS to manage. Reduces endpoint management cost compared to traditional PCs for call center agents, task workers, and kiosk use cases.

---

## X

### 342. AWS X-Ray
Distributed tracing service analyzing and debugging distributed applications — microservices, serverless, APIs.

### 343. X-Ray Groups
Filters traces by expression (e.g., `service("checkout-api") AND http.status = 5xx`) into named groups. Separate CloudWatch metrics and sampling rules apply per group. Used to focus observability on a specific service path or error condition without sorting through all traces.

### 344. X-Ray Sampling Rules
Controls the percentage of requests that are traced to manage cost and data volume. Default rule: 5% of all requests (plus 1 per second reservoir per host). Custom rules can match by host, service name, URL path, or HTTP method — trace 100% of `/checkout` requests while sampling 1% of `/health` checks. Sampling rules are managed centrally and pushed to SDK clients in real time.

### 345. X-Ray Service Map
A visual representation of the service graph — each connected node is a service (EC2 app, Lambda, DynamoDB, RDS, external HTTP); edges show call relationships with average latency and error rate. Allows a developer or operator to see at a glance where latency or errors originate in a distributed application without reading individual traces.

---

*Last updated: April 2026. Entries reflect services and features generally available at that date.*
