# Azure Glossary

A comprehensive A–Z reference of Azure services, sub-features, architectural concepts, and terminology. Written for Solution Architects who know AWS well but are new to Azure. Each entry explains what it is, why a customer cares, key tradeoffs, and the AWS equivalent where helpful. Sorted alphabetically.

---

## Services with Sub-Entries

| Service | Sub-entries |
|---|---|
| **Azure Active Directory (Entra ID)** | B2B, B2C, Conditional Access, Domain Services, External Identities, Managed Identities, PIM, SSPR |
| **Azure AI Foundry** | Model Catalog, Prompt Flow, Safety Evaluations |
| **Azure API Management** | Developer Portal, Policies, Self-Hosted Gateway |
| **Azure App Service** | Deployment Slots, Environment (ASE), Service Plans, WebJobs |
| **Azure Blob Storage** | Access Tiers, Data Lake Storage Gen2, Immutability Policies, Lifecycle Management, Object Replication, Soft Delete, Static Website |
| **Azure Container Apps** | Dapr Integration, KEDA Scaling, Revisions |
| **Azure Cosmos DB** | Analytical Store, Cassandra API, Change Feed, Gremlin API, MongoDB API, NoSQL API, PostgreSQL API, Table API |
| **Azure Data Factory** | Data Flows, Integration Runtime, Linked Services, Managed Virtual Network, Pipelines, Triggers |
| **Azure Database for MySQL / PostgreSQL** | Flexible Server, Single Server |
| **Azure Databricks** | Delta Live Tables, Feature Store, MLflow, Unity Catalog |
| **Azure Event Hubs** | Capture, Dedicated, Kafka Surface, Schema Registry |
| **Azure Kubernetes Service (AKS)** | Azure CNI, Fleet Manager, Managed Identity Integration, Node Pools, OIDC Issuer |
| **Azure Monitor** | Action Groups, Alerts, Application Insights, Log Analytics, Metrics, Workbooks |
| **Azure OpenAI Service** | Assistants API, Batch API, Embeddings, Fine-Tuning, GPT-4o, DALL-E |
| **Azure Policy** | Initiatives, Remediation Tasks |
| **Azure SQL** | Elastic Pool, Hyperscale, Ledger, Managed Instance, Serverless |
| **Azure Storage** | Azure Files, Azure Queues, Azure Tables, Blob Storage |
| **Azure Synapse Analytics** | Dedicated SQL Pool, Link for Cosmos DB, Pipelines, Serverless SQL Pool, Spark Pool, Studio |
| **Azure Virtual Network** | DDoS Protection, Network Security Groups, Peering, Private Endpoint, Service Endpoints, User-Defined Routes |
| **Microsoft Defender for Cloud** | Defender CSPM, Defender for Servers, Defender for SQL, Defender for Storage, Security Score |
| **Microsoft Fabric** | Data Activator, Eventstream, KQL Database, Lakehouse, OneLake, Pipelines, Real-Time Intelligence, Warehouse |
| **Microsoft Purview** | Data Catalog, Data Lineage, Data Map, Information Protection, Insider Risk Management |

---

## A

### Azure Active Directory (Entra ID)
Microsoft's cloud identity platform — the Azure equivalent of AWS IAM combined with a full enterprise identity provider. Nearly every Azure service and Microsoft 365 product relies on Entra ID for authentication and authorization. Customers moving to Azure will consolidate identity here; it supports SSO, MFA, conditional access, and federation with on-premises Active Directory. Microsoft rebranded it "Microsoft Entra ID" in 2023 but the old name is still widely used.

### Azure AD B2B (Business-to-Business)
Lets external users (partners, contractors) access your Azure resources using their own organizational credentials. Instead of creating guest accounts manually, B2B sends an invite link; the external user signs in with their home directory. The AWS analogy is cross-account IAM role federation. Recommend when a customer needs to collaborate with external organizations without managing their identities.

### Azure AD B2C (Business-to-Consumer)
A white-label identity service for customer-facing applications — handles sign-up, sign-in, password reset, and social login (Google, Facebook) for millions of end users. Separate from the corporate Entra ID tenant. The AWS equivalent is Amazon Cognito. Recommend for customers building consumer apps who don't want to build auth from scratch.

### Azure AD Conditional Access
Policy engine that evaluates sign-in risk and enforces controls — require MFA, block access from specific countries, require compliant devices — based on conditions like user role, IP location, app being accessed, and sign-in risk score. Think of it as AWS IAM condition keys but applied at the authentication layer, not the API layer. Essential for Zero Trust security posture.

### Azure AD Domain Services (AADDS)
A managed Active Directory domain — provides LDAP, Kerberos, NTLM, and Group Policy without deploying domain controllers on VMs. Useful when customers are lifting legacy apps that require AD but want to avoid managing DCs. Not a full replacement for on-premises AD; it's a one-way sync from Entra ID.

### Azure AD External Identities
The umbrella for B2B and B2C. The key customer conversation: "Do you need partners to access internal apps (B2B) or do you need a sign-in system for your own customers (B2C)?"

### Azure AD Managed Identities
Automatically managed service principals for Azure resources — VMs, Functions, App Service — that can authenticate to Azure services without storing credentials in code or config. Equivalent to AWS EC2 Instance Profiles / IAM Roles for Services. This is the recommended pattern for service-to-service auth on Azure; always recommend it over storing connection strings.

### Azure AD Privileged Identity Management (PIM)
Just-in-time (JIT) privileged access for Azure roles and Entra ID roles. Users request elevated access for a limited time window, and approvals + audit logs are enforced. The equivalent of AWS IAM temporary credentials via STS, but with an approval workflow UI. Recommend to any customer with compliance requirements (SOC 2, PCI).

### Azure AD Self-Service Password Reset (SSPR)
Allows end users to reset their own passwords without IT involvement, using registered MFA methods. Reduces helpdesk tickets. Relevant when customers are consolidating identity management.

### Azure AI Foundry
Microsoft's unified platform for building, evaluating, and deploying AI applications — previously called "Azure AI Studio." Think of it as a workbench for enterprise AI: you bring your own data, choose a model from the catalog, build a prompt flow, run safety evaluations, and deploy to an endpoint. The AWS equivalent is Amazon Bedrock + SageMaker Studio combined.

### Azure AI Foundry Model Catalog
A browsable library of models — OpenAI GPT-4o, Meta Llama, Mistral, Cohere, Phi — that can be deployed to managed endpoints or used via API. Some are hosted by Microsoft (pay-per-token), others run on your own compute (pay-per-hour). The distinction matters for data residency and cost conversations.

### Azure AI Foundry Prompt Flow
A visual IDE for building, testing, and deploying LLM-based pipelines — chain together LLM calls, code execution, and tool integrations into a flow. Supports both UI-based and YAML-based authoring. Competes with LangChain/LangGraph in the orchestration space but with a more managed, less code-heavy experience.

### Azure AI Foundry Safety Evaluations
Built-in tooling to measure LLM output quality and safety — groundedness, coherence, relevance, and harm categories (hate, self-harm). Run evaluations against a dataset before deploying a model to production. Increasingly required for enterprise AI governance.

### Azure AI Search
Managed search service built on Apache Lucene/Elasticsearch internals, with Microsoft-specific extensions for AI enrichment — OCR, entity extraction, key phrase extraction applied to documents at index time. The "killer feature" for RAG (Retrieval-Augmented Generation) architectures: it handles vector search, hybrid search (keyword + semantic), and integrates with Azure OpenAI. AWS equivalent is Amazon OpenSearch Service. Position this whenever a customer needs to make their documents "findable" by an AI chatbot.

### Azure AI Services (Cognitive Services)
A family of pre-built AI APIs — Vision, Speech, Language, Decision — accessible via REST calls without any ML expertise. Customers get capabilities like OCR, translation, sentiment analysis, and form recognition by calling an API endpoint. AWS equivalent is the various Amazon AI services (Rekognition, Transcribe, Comprehend). Good for customers who want AI capability without data science teams.

### Azure Analysis Services
A managed, cloud-hosted tabular analysis engine (based on SQL Server Analysis Services). Used for building semantic models — business metrics definitions, KPIs, hierarchies — that Power BI and Excel can query. Being superseded by Power BI Premium / Fabric for net-new deployments. Bring this up when customers have existing SSAS investments they want to migrate to the cloud.

### Azure API Management (APIM)
A full-lifecycle API gateway — publish, secure, transform, monitor, and monetize APIs. Sits in front of backend services (Azure Functions, App Service, external APIs) and handles auth, rate limiting, caching, request/response transformation, and developer portal. AWS equivalent is Amazon API Gateway + AWS Marketplace for developer portals. A single APIM instance can front hundreds of APIs; it's the right answer for customers building a platform with many internal or external API consumers.

### Azure API Management Developer Portal
A customizable, auto-generated website where external developers can discover APIs, read documentation, test endpoints interactively, and obtain API keys. Published from the APIM service; customers can white-label it. Reduces onboarding friction for API programs.

### Azure API Management Policies
XML-based transformation rules applied to API requests and responses — rewrite URLs, add headers, enforce JWT validation, throttle by key, cache responses. Policies execute inbound (before backend), backend (modifying the backend request), outbound (after backend), and on-error. The "configuration over code" way to add cross-cutting concerns to APIs.

### Azure API Management Self-Hosted Gateway
A containerized APIM gateway that runs on-premises or in other clouds, but is managed centrally from the Azure APIM control plane. Enables hybrid API management — on-premises APIs get the same policies, monitoring, and developer portal as cloud APIs. Key differentiator for customers with strict data residency requirements.

### Azure App Configuration
A managed service for centralized application settings and feature flags — keeps configuration out of code and app bundles. Integrates with Key Vault for secrets references. Feature flags enable progressive deployment (canary, ring-based rollouts). AWS equivalent is AWS AppConfig (part of Systems Manager). Recommend when customers are building microservices and want to avoid redeployment for config changes.

### Azure App Service
Microsoft's PaaS for hosting web applications, REST APIs, and mobile backends. Supports .NET, Java, Node.js, Python, PHP, Ruby. AWS equivalent is Elastic Beanstalk or App Runner. Key pitch: developers deploy code or containers without managing servers; the platform handles OS patching, load balancing, and auto-scaling.

### Azure App Service Deployment Slots
Staging environments within the same App Service plan that allow zero-downtime deployments via slot swap. A swap atomically routes production traffic to the staged version; the previous production version becomes the new staging slot (instant rollback). AWS equivalent is Elastic Beanstalk environment swap or CodeDeploy blue/green.

### Azure App Service Environment (ASE)
A fully isolated, dedicated deployment of App Service inside a customer's VNet — all compute is single-tenant. Used for compliance requirements that mandate network isolation or dedicated compute. Significantly more expensive than multi-tenant App Service; position it only for regulated workloads (finance, healthcare).

### Azure App Service Plans
The compute tier that backs App Service, Azure Functions (non-Consumption), and Logic Apps. Defines VM size, OS, region, and scaling limits. Shared across multiple apps — a customer can run 10 web apps on a single plan. AWS analogy: the underlying EC2 instance type for Elastic Beanstalk, but abstracted.

### Azure App Service WebJobs
Background tasks that run in the context of an App Service web app — think cron jobs or queue processors. Being superseded by Azure Functions for new workloads, but WebJobs still appear in legacy .NET shops. Continuous WebJobs run always; triggered WebJobs run on demand or on schedule.

### Azure Application Gateway
A Layer 7 (HTTP/HTTPS) load balancer with WAF capability, SSL termination, URL-based routing, and cookie-based session affinity. Regional service (unlike Azure Front Door which is global). AWS equivalent is Application Load Balancer (ALB) + AWS WAF. Choose Application Gateway when customers need WAF at the regional level or complex URL routing within a single region.

### Azure Arc
Microsoft's hybrid/multicloud control plane — extends Azure management (policy, monitoring, Defender, role-based access) to resources running anywhere: on-premises servers, other clouds (AWS, GCP), and edge locations. Arc-enabled servers appear as Azure resources even though they run elsewhere. This is Microsoft's answer to the "manage everything from one place" requirement. Key differentiator in hybrid customer conversations.

### Azure Arc-Enabled Data Services
Runs Azure SQL Managed Instance or PostgreSQL on any Kubernetes cluster (on-premises, edge, other clouds) while maintaining the same management APIs, patching, and billing as Azure SQL. Customers get cloud-like database capabilities with data residency control. Strong play for regulated industries that can't put data in the public cloud but want managed database services.

### Azure Arc-Enabled Kubernetes
Attaches any CNCF-conformant Kubernetes cluster to Azure — on-premises, EKS, GKE — and manages it through Azure: GitOps deployments, Azure Policy, Defender for Containers, and monitoring via Azure Monitor. The cluster stays where it is; Azure becomes the control plane. Relevant for customers with Kubernetes sprawl across environments.

### Azure Automation
Managed service for process automation using PowerShell or Python runbooks — scheduled tasks, config management (DSC), update management, and inventory collection for Azure and on-premises VMs. AWS equivalent is AWS Systems Manager Automation + Patch Manager. Relevant for customers automating VM lifecycle and patching at scale.

### Azure Bastion
A managed, browser-based SSH/RDP service that lets admins connect to VMs without exposing public IPs or managing jump hosts. Runs directly in the Azure portal; traffic goes over TLS on port 443 (firewall-friendly). AWS equivalent is AWS Systems Manager Session Manager. Recommend universally for secure VM access — eliminates the "open RDP to the world" anti-pattern.

### Azure Blob Storage
Microsoft's object storage service — the Azure equivalent of Amazon S3. Stores unstructured data: documents, images, videos, backups, logs. Three account types matter: Standard (HDDs, lower cost), Premium (SSDs, low-latency), and the Data Lake Storage Gen2 overlay (hierarchical namespace for analytics). Foundational for nearly every Azure architecture.

### Azure Blob Storage Access Tiers
Cost optimization layers for blob data: **Hot** (frequent access, highest storage cost, lowest retrieval cost), **Cool** (infrequent access, lower storage cost, higher retrieval cost, minimum 30-day retention), **Cold** (rarely accessed, even lower storage, minimum 90 days), **Archive** (offline storage, hours to rehydrate, lowest cost). AWS equivalent is S3 Standard / S3-IA / S3 Glacier. Lifecycle policies automate tier transitions.

### Azure Blob Storage Data Lake Storage Gen2 (ADLS Gen2)
A hierarchical namespace overlay on Blob Storage that enables folder-level operations (rename, delete directory atomically) and POSIX-like ACLs. Makes Blob Storage behave like HDFS — required for Azure Databricks, Synapse Analytics, and HDInsight to perform efficiently. Not a separate service; it's a feature flag enabled at storage account creation. AWS equivalent is S3 with a flat namespace (no true equivalent — GCS and ADLS Gen2 have real directories; S3 simulates them).

### Azure Blob Storage Immutability Policies
Write-Once-Read-Many (WORM) locks on blob containers — data cannot be modified or deleted for the policy duration. Two modes: **Time-based retention** (locked for N days) and **Legal hold** (locked until explicitly released). Required for SEC 17a-4, FINRA, and HIPAA compliance. AWS equivalent is S3 Object Lock.

### Azure Blob Storage Lifecycle Management
Rules that automatically move blobs between access tiers or delete them based on age or last-modified date. Reduces storage costs without manual intervention. AWS equivalent is S3 Lifecycle Policies.

### Azure Blob Storage Object Replication
Asynchronously copies blobs between two storage accounts — same or different regions, same or different subscriptions. Used for geo-redundancy, compliance (keeping data in specific regions), and disaster recovery. AWS equivalent is S3 Cross-Region Replication.

### Azure Blob Storage Soft Delete
A recycle-bin feature for blobs — deleted data is retained for a configurable period (1–365 days) before permanent deletion. Protects against accidental deletes and ransomware. Can be applied at container level and blob level independently. AWS equivalent is S3 Versioning + S3 MFA Delete.

### Azure Blob Storage Static Website
Serve HTML, CSS, and JS files directly from a Blob Storage container over HTTP/HTTPS — no web server needed. Combined with Azure CDN or Front Door for HTTPS and global distribution. AWS equivalent is S3 static website hosting + CloudFront.

### Azure Cache for Redis
Managed Redis service — in-memory caching layer for session storage, leaderboards, pub/sub, and reducing database load. AWS equivalent is ElastiCache for Redis. Two tiers: Basic/Standard (single/replicated), and Enterprise (full Redis Enterprise with modules like RediSearch, RedisJSON). Choose Enterprise for customers needing active-active geo-replication or Redis modules.

### Azure CDN
Content Delivery Network for accelerating static content delivery globally — caches assets at edge PoPs close to users. Three profiles available: **Azure CDN Standard from Microsoft** (basic, integrated with Azure), **Azure CDN from Akamai**, and **Azure CDN from Verizon** (more advanced rules). Being consolidated into Azure Front Door for new deployments. AWS equivalent is CloudFront.

### Azure Cognitive Search
See **Azure AI Search** — the service was renamed in 2023.

### Azure Container Apps
A serverless container hosting service built on top of Kubernetes (AKS) and Dapr — customers deploy containers without managing Kubernetes clusters. Automatically scales to zero and handles HTTP ingestion and event-driven scaling via KEDA. The sweet spot between App Service (too opinionated) and AKS (too much cluster management). AWS equivalent is AWS App Runner or ECS Fargate.

### Azure Container Apps Dapr Integration
Dapr (Distributed Application Runtime) is built into Container Apps as a sidecar — provides service discovery, state management, pub/sub, and secrets without modifying application code. Customers get microservices plumbing for free. No AWS equivalent out of the box.

### Azure Container Apps KEDA Scaling
Container Apps uses KEDA (Kubernetes Event-Driven Autoscaling) under the hood — scale containers based on queue depth, Event Hub lag, HTTP requests, or custom metrics. Enables scaling to zero when idle. AWS equivalent is KEDA on EKS (self-managed) or ECS auto-scaling.

### Azure Container Apps Revisions
Immutable snapshots of a Container App configuration — each deployment creates a new revision. Supports traffic splitting between revisions (e.g., 90% to v1, 10% to v2) for canary deployments. AWS equivalent is ECS task definition revisions + weighted target groups.

### Azure Container Instances (ACI)
Run individual containers on demand without any cluster management — pay per second of CPU and memory. The fastest way to run a container in Azure for short-duration tasks, batch jobs, or dev/test. Not designed for long-running production services (use Container Apps or AKS). AWS equivalent is AWS Fargate standalone tasks.

### Azure Container Registry (ACR)
Private registry for Docker and OCI container images. Integrates natively with AKS, Container Apps, App Service, and Azure Pipelines. Geo-replication pushes images to multiple regions for fast pull performance globally. AWS equivalent is Amazon ECR.

### Azure Cosmos DB
Microsoft's flagship globally distributed, multi-model NoSQL database. The "no single point of failure across any region" pitch: customers choose consistency level (Strong to Eventual) and get millisecond reads/writes globally. AWS equivalent is DynamoDB (document/key-value) + Cassandra (wide-column) — Cosmos DB supports multiple APIs. Key differentiator: you can switch consistency level per request, and the global active-active replication is built in rather than bolted on.

### Azure Cosmos DB Analytical Store
A columnar, append-only copy of operational Cosmos DB data that enables analytical queries without impacting transactional performance — called the HTAP (Hybrid Transactional/Analytical Processing) pattern. Synapse Link connects the analytical store directly to Synapse Analytics for SQL or Spark queries. No ETL pipeline needed. AWS equivalent would be DynamoDB Streams → S3 → Athena, but much more complex.

### Azure Cosmos DB Cassandra API
Exposes a Cassandra-compatible endpoint so existing Cassandra applications can migrate to Cosmos DB without code changes. Customers get Cosmos DB's global distribution and SLAs on top of their Cassandra schema. Tradeoff: not 100% Cassandra-compatible; some CQL features aren't supported.

### Azure Cosmos DB Change Feed
A persistent, ordered log of every document change (insert and update — not deletes by default) in a Cosmos DB container. Downstream consumers (Functions, Databricks, Stream Analytics) can react to changes in near-real-time. The foundational pattern for event-driven architectures on Cosmos DB. AWS equivalent is DynamoDB Streams.

### Azure Cosmos DB Gremlin API
A graph database API compatible with Apache TinkerPop Gremlin query language. Use for social networks, recommendation engines, and fraud detection where relationships between entities matter. AWS equivalent is Amazon Neptune (Gremlin).

### Azure Cosmos DB MongoDB API
Exposes a MongoDB-compatible wire protocol — existing MongoDB applications can point at Cosmos DB with minimal code changes. Most popular Cosmos DB API for new customers migrating from MongoDB Atlas. Tradeoff: not 100% MongoDB compatible; some operators and aggregation pipeline stages differ.

### Azure Cosmos DB NoSQL API
The native Cosmos DB API — uses JSON documents, a SQL-like query language (with quirks), and JavaScript stored procedures. Best performance and deepest feature integration with other Azure services. The default choice for net-new development on Cosmos DB.

### Azure Cosmos DB PostgreSQL API
A distributed PostgreSQL service powered by the Citus extension — shards tables across multiple nodes for horizontal scale-out. Not the same as single-node Azure Database for PostgreSQL. Best for customers who need relational semantics with massive write throughput. AWS equivalent is Amazon Aurora Distributed (or Aurora with Babelfish for migration scenarios).

### Azure Cosmos DB Table API
Key-value store with a table/row model compatible with Azure Table Storage. Migration path for customers on legacy Azure Table Storage who want global distribution and SLAs. New customers should evaluate whether Cosmos DB NoSQL API is a better fit.

### Azure Cost Management + Billing
Microsoft's native cost visibility and optimization tool. View spending by subscription, resource group, tag, or service. Set budgets with alerting thresholds, download invoices, and analyze trends. AWS equivalent is AWS Cost Explorer + AWS Budgets. Recommend early in every engagement — customers consistently underestimate Azure's billing complexity across subscriptions.

### Azure Data Factory (ADF)
Azure's managed ETL/ELT orchestration service — visually design pipelines to move and transform data between 90+ sources (on-premises databases, SaaS apps, file systems) and Azure destinations. AWS equivalent is AWS Glue + Step Functions. ADF is the primary data integration service for Azure; almost every data platform conversation on Azure involves it.

### Azure Data Factory Data Flows
Visually designed, code-free data transformation logic within ADF pipelines — backed by Spark but abstracted into a drag-and-drop UI with 80+ transformation types. AWS equivalent is AWS Glue Studio visual job editor. Good for data engineers who know SQL logic but not Spark/PySpark.

### Azure Data Factory Integration Runtime (IR)
The compute engine that executes ADF activities. Three types: **Azure IR** (managed, runs in Azure), **Self-Hosted IR** (runs on-premises or in a private network for reaching on-prem sources), **Azure-SSIS IR** (managed SSIS runtime for lifting existing SSIS packages). The Self-Hosted IR is a key conversation point for hybrid data integration scenarios.

### Azure Data Factory Linked Services
Named connections to data sources and destinations — store the connection string, credentials, and configuration for each endpoint that pipelines access. Credentials can be backed by Azure Key Vault. The concept is equivalent to SSIS connection managers or Glue connections.

### Azure Data Factory Managed Virtual Network
Isolates the Azure IR inside a managed VNet, enabling private connectivity to data sources via Private Endpoints — without the customer managing any networking. Addresses the "how do I reach on-premises data securely from ADF" question without a Self-Hosted IR. More expensive but simpler operationally.

### Azure Data Factory Pipelines
Logical groupings of activities — copy, transform, call a stored proc, invoke a Function, run a notebook — sequenced with branching, loops, and conditional logic. The top-level unit of orchestration in ADF. Parameterized pipelines enable reuse across environments.

### Azure Data Factory Triggers
Mechanisms that start pipeline runs: **Schedule** (cron-like), **Tumbling Window** (for backfill scenarios — processes consecutive, non-overlapping time intervals), **Event-based** (file arrives in Blob Storage), **Custom Events** (Event Grid). Understanding tumbling window vs. schedule is a common interview/exam topic.

### Azure Data Lake Storage Gen2 (ADLS Gen2)
See **Azure Blob Storage Data Lake Storage Gen2** — it is implemented as a feature of Blob Storage, not a standalone service.

### Azure Database for MySQL
Managed MySQL (v5.7 and 8.0) with automated backups, patching, HA, and read replicas. AWS equivalent is Amazon RDS for MySQL / Aurora MySQL. Good migration target for customers running self-managed MySQL.

### Azure Database for MySQL Flexible Server
The current, recommended deployment model — gives customers control over maintenance windows, zone-redundant HA, and stop/start capability (reduces cost during dev/test hours). Replaces the deprecated "Single Server" model.

### Azure Database for MySQL Single Server
Deprecated model — limited configuration options. Customers on Single Server should be migrated to Flexible Server. Relevant to recognize in legacy environments.

### Azure Database for PostgreSQL
Managed PostgreSQL with automated backups, HA, and read replicas. AWS equivalent is Amazon RDS for PostgreSQL / Aurora PostgreSQL. Strong for customers with existing PostgreSQL workloads; supports pgvector for AI embeddings use cases.

### Azure Database for PostgreSQL Flexible Server
The current recommended model — similar to MySQL Flexible Server. Adds zone-redundant HA, maintenance window control, stop/start, and connection pooling via PgBouncer built in.

### Azure Database for PostgreSQL Single Server
Deprecated — migrate customers to Flexible Server.

### Azure Databricks
A managed Apache Spark and data intelligence platform, jointly developed by Microsoft and Databricks. Tightly integrated with Azure: ADLS Gen2, Synapse, ADF, and Entra ID. Same Databricks product as AWS/GCP variants but with Azure-native networking (VNet injection) and billing through Azure Marketplace. The premium data engineering and ML platform on Azure.

### Azure Databricks Delta Live Tables
A declarative pipeline framework within Databricks for building reliable, maintainable data pipelines on Delta Lake — define transformations as SQL or Python, DLT handles orchestration, error handling, and data quality checks. The "guardrails on" approach to pipeline development.

### Azure Databricks Feature Store
A centralized repository for ML features — store, discover, and serve features for training and inference, ensuring consistency between training and serving environments. Integrated with MLflow for experiment tracking.

### Azure Databricks MLflow
Open-source ML lifecycle platform integrated into Databricks — tracks experiments, packages models, manages the model registry, and serves models. Standard tooling for MLOps on Azure Databricks.

### Azure Databricks Unity Catalog
Unified governance for all data assets (tables, files, ML models) across Databricks workspaces — fine-grained access control, lineage, and auditing. The cross-workspace governance layer. See also Microsoft Purview for broader Azure governance.

### Azure DDoS Protection
Protection against volumetric and protocol-based DDoS attacks on Azure resources. Two tiers: **Basic** (free, always-on for Azure infrastructure) and **Standard/Network** (per-VNet, per-month fee, telemetry, adaptive tuning, cost guarantee for scale-out during attacks). AWS equivalent is AWS Shield Standard (free) and Shield Advanced (paid). Recommend Standard for public-facing applications with SLA requirements.

### Azure DevOps
Microsoft's complete DevOps platform — Repos (Git), Pipelines (CI/CD), Boards (work tracking), Artifacts (package registry), and Test Plans. AWS equivalent split across CodeCommit + CodePipeline + CodeBuild + CodeArtifact + Jira. Strong in enterprises already using Microsoft tooling; many customers use Azure DevOps alongside GitHub Actions.

### Azure DNS
Managed DNS hosting for domain names — answer DNS queries using Microsoft's global Anycast network. Supports public zones (internet-facing) and private zones (resolution within VNets). AWS equivalent is Route 53 (hosted zones). Note: Azure DNS cannot purchase domain names — use App Service Domains or a registrar.

### Azure Event Grid
A fully managed event routing service that enables event-driven architectures — publish events from Azure services (Blob Storage, Resource Manager, IoT Hub) and route to subscribers (Functions, Logic Apps, Event Hubs, custom webhooks). Uses a push model with at-least-once delivery. AWS equivalent is Amazon EventBridge. The "glue" connecting Azure services in reactive architectures.

### Azure Event Hubs
A managed, high-throughput event streaming service — handles millions of events per second, retains data for 1–90 days, and is compatible with the Apache Kafka protocol. AWS equivalent is Amazon Kinesis Data Streams + MSK. The standard ingestion point for telemetry, logs, and clickstream data on Azure.

### Azure Event Hubs Capture
Automatically archives Event Hub data to Blob Storage or ADLS Gen2 in Avro format — no consumer code needed. Enables replay and batch processing of streaming data. AWS equivalent is Kinesis Data Firehose delivering to S3.

### Azure Event Hubs Dedicated
Single-tenant Event Hubs deployment — guaranteed capacity, no noisy neighbors, private networking. For customers with extreme throughput requirements or compliance mandates. Significantly more expensive than standard tiers.

### Azure Event Hubs Kafka Surface
Event Hubs exposes a Kafka-compatible endpoint — existing Kafka producers and consumers can connect to Event Hubs by changing the broker endpoint, without code changes. The migration path from self-managed Kafka to a managed Azure service.

### Azure Event Hubs Schema Registry
Centralized schema store for event data — enforce Avro or JSON schemas on producers and consumers, preventing schema drift from breaking downstream systems. AWS equivalent is MSK Schema Registry.

### Azure ExpressRoute
A private, dedicated network connection between on-premises infrastructure and Azure — bypasses the public internet, offers predictable latency and bandwidth, and can be encrypted with MACsec. AWS equivalent is AWS Direct Connect. Bandwidth 50 Mbps to 100 Gbps. Essential for hybrid customers with data gravity on-premises or strict latency/compliance requirements.

### Azure Firewall
Managed, stateful network firewall — filters traffic at Layer 3/4 (IP and port) and Layer 7 (FQDNs and URLs). Central in Hub-and-Spoke network architectures. Two tiers: **Standard** (FQDN filtering, threat intelligence) and **Premium** (TLS inspection, IDPS). AWS equivalent is AWS Network Firewall. Position whenever customers ask "how do I control outbound internet traffic from VMs?"

### Azure Front Door
Microsoft's global Layer 7 load balancer and CDN — routes traffic to the closest healthy origin, provides WAF, SSL offload, URL rewriting, and caching at edge PoPs worldwide. AWS equivalent is AWS CloudFront + Global Accelerator combined. Recommended over regional Application Gateway for globally distributed applications.

### Azure Functions
Serverless compute — runs event-triggered code without managing servers. Supports C#, JavaScript, Python, Java, PowerShell. AWS equivalent is AWS Lambda. Triggers include HTTP, Timer, Blob Storage, Event Hubs, Cosmos DB Change Feed, Service Bus. Scale to zero means zero cost when idle (on Consumption plan).

### Azure Functions Durable Functions
An extension to Azure Functions for orchestrating stateful workflows — chains function calls, handles fan-out/fan-in, supports long-running activities and human approval patterns without managing state. AWS equivalent is AWS Step Functions. Use when customers outgrow simple event-triggered functions and need workflow logic.

### Azure HDInsight
Managed open-source analytics clusters — Hadoop, Spark, Kafka, HBase, Hive, Storm. AWS equivalent is Amazon EMR. Being superseded by Azure Databricks for Spark and Fabric for analytics. Still relevant for customers with existing Hadoop investments or needing HBase/Storm.

### Azure IoT Hub
Managed IoT message broker — bidirectional communication between Azure cloud and millions of IoT devices. Handles device registration, authentication (X.509 certificates or SAS tokens), telemetry ingestion, and device twin (shadow) state. AWS equivalent is AWS IoT Core. Foundation for most Azure IoT architectures.

### Azure Key Vault
Managed secrets, keys, and certificates store — applications retrieve credentials at runtime without embedding them in code. Integrates with Managed Identities so apps authenticate to Key Vault without any stored credentials. AWS equivalent is AWS Secrets Manager + AWS KMS combined. Standard recommendation for any customer storing database passwords, API keys, or TLS certificates.

### Azure Kubernetes Service (AKS)
Microsoft's managed Kubernetes service — control plane is free, customers pay for agent node VMs. Deep integration with Azure networking, ACR, Entra ID, and Azure Monitor. AWS equivalent is EKS. Strong for customers with existing Kubernetes expertise who want to avoid control plane management.

### Azure Kubernetes Service Azure CNI
A networking plugin for AKS that assigns pods real VNet IP addresses — pods are directly routable from on-premises and other VNets without NAT. Contrast with Kubenet (simpler but pods get overlay IPs not routable outside the cluster). Required for customers with strict network compliance or integration with on-premises routing.

### Azure Kubernetes Service Fleet Manager
Multi-cluster Kubernetes management across multiple AKS clusters — deploy workloads, enforce policies, and do staged rollouts across a fleet. Relevant for customers running 10+ AKS clusters across regions or environments.

### Azure Kubernetes Service Managed Identity Integration
AKS pods can assume Entra ID Managed Identities (via Workload Identity) to access Azure resources (Key Vault, Storage, SQL) without storing credentials. Replacement for the older Pod Identity (AAD Pod Identity) pattern.

### Azure Kubernetes Service Node Pools
Groups of VMs within an AKS cluster with the same configuration (VM size, OS). System node pools run Kubernetes system pods; user node pools run workloads. Allows mixing GPU nodes, spot nodes, and standard nodes in one cluster. Spot node pools reduce compute costs by up to 90% for interruption-tolerant workloads.

### Azure Kubernetes Service OIDC Issuer
Enables AKS to issue OIDC tokens for pods — used by Workload Identity (Managed Identity integration) and external identity federation. Required for the recommended, secretless approach to pod-to-Azure-service auth.

### Azure Load Balancer
Layer 4 (TCP/UDP) load balancer — distributes traffic across VMs or VMSS within a region. Two tiers: **Basic** (free, limited features) and **Standard** (SLA, availability zones, outbound rules). AWS equivalent is Network Load Balancer (NLB). Choose Load Balancer for non-HTTP workloads (databases, gaming servers); use Application Gateway or Front Door for HTTP.

### Azure Log Analytics Workspace
The central data store for Azure Monitor logs — VMs, containers, network flows, security events, and custom app logs all feed here. Queries use KQL (Kusto Query Language). AWS equivalent is Amazon CloudWatch Logs + Log Insights, or OpenSearch. One workspace per environment is common; some customers use one per region for data residency.

### Azure Logic Apps
Low-code workflow automation with 500+ pre-built connectors — SAP, Salesforce, ServiceNow, Office 365, Dynamics. Run on Consumption (serverless) or Standard (dedicated, VNET-integrated) plans. AWS equivalent is AWS Step Functions + EventBridge Pipes (but Logic Apps has far more SaaS connectors out of the box). Position for business process automation and integration with enterprise SaaS.

### Azure Machine Learning
Microsoft's MLOps platform — manage datasets, train models at scale (distributed training, AutoML), track experiments, build pipelines, manage the model registry, and deploy to online/batch endpoints. AWS equivalent is Amazon SageMaker. More open than Azure OpenAI (bring your own OSS models); less turnkey than Azure AI Foundry for pure LLM scenarios.

### Azure Managed Disks
Block storage for Azure VMs — abstracts the underlying storage account, handles replication, and provides SLA-backed IOPS and throughput. Four disk types: **Standard HDD** (dev/test), **Standard SSD** (web servers), **Premium SSD** (production databases), **Ultra Disk** (extreme IOPS — database logs, HPC). AWS equivalent is Amazon EBS with gp2/gp3/io1/io2 tiers.

### Azure Migrate
Hub for discovering, assessing, and migrating on-premises workloads to Azure — VMware/Hyper-V VMs, physical servers, databases, web apps, and VDI. Assessment reports estimate Azure sizing and costs. Migration tools handle replication and cutover. AWS equivalent is AWS Application Migration Service (MGN) + Migration Evaluator. Starting point for every lift-and-shift conversation.

### Azure Monitor
Azure's unified observability platform — collects metrics and logs from Azure resources, VMs, containers, and applications. AWS equivalent is Amazon CloudWatch. Components: Log Analytics (logs), Metrics (time series), Application Insights (APM), Alerts, Workbooks (dashboards), and Action Groups (notifications/automation).

### Azure Monitor Action Groups
Named sets of notification and remediation actions triggered by alerts — email, SMS, push notification, ITSM ticket (ServiceNow), Azure Function call, Logic App. Reusable across multiple alert rules. AWS equivalent is SNS topic + Lambda for custom actions.

### Azure Monitor Alerts
Rules that trigger when a metric or log condition is met — e.g., CPU > 90% for 5 minutes, or a specific error appears in logs. Stateful (fire once, resolve once) by default. AWS equivalent is CloudWatch Alarms.

### Azure Monitor Application Insights
APM (Application Performance Monitoring) service — SDKs instrument apps to send traces, exceptions, custom events, and dependency calls. Provides distributed tracing, failure analysis, performance profiling, and usage analytics. AWS equivalent is AWS X-Ray + CloudWatch Application Insights. Recommend for any customer running web applications.

### Azure Monitor Log Analytics
See **Azure Log Analytics Workspace**.

### Azure Monitor Metrics
Time-series numerical data from Azure resources — CPU, memory, request count, latency. Near-real-time (1-minute granularity), retained for 93 days. Free for most Azure resources. Basis for autoscaling and alerting. AWS equivalent is CloudWatch Metrics.

### Azure Monitor Workbooks
Interactive dashboards and reports built from Metrics, Log Analytics queries, and Azure Resource Graph — combine visualizations into a single view. Supports parameterization (environment, time range dropdowns). AWS equivalent is CloudWatch Dashboards (less powerful) or Grafana.

### Azure NetApp Files
Enterprise NFS/SMB file storage powered by NetApp ONTAP hardware — high performance (sub-millisecond latency), used for SAP HANA, HPC, Oracle, and Windows file server workloads that need shared file systems at scale. AWS equivalent is Amazon FSx for NetApp ONTAP. Position for customers migrating enterprise applications that require high-performance NAS.

### Azure OpenAI Service
Microsoft's managed access to OpenAI models (GPT-4o, GPT-4, o-series reasoning models, DALL-E, Whisper, Embeddings) — runs in Azure's infrastructure, complies with Azure's data privacy commitments (data is not used to train OpenAI models). The enterprise-safe way to use OpenAI models. AWS equivalent is Amazon Bedrock (with Anthropic, Cohere, etc.). Key pitch: data stays in the customer's Azure tenant/region; no data sharing with OpenAI.

### Azure OpenAI Service Assistants API
Stateful AI assistant API — manages conversation threads, file attachments, and tool calls (code interpreter, function calling, file search) server-side, removing the burden from the application to track conversation state. AWS equivalent is Amazon Bedrock Agents.

### Azure OpenAI Service Batch API
Asynchronous API for submitting large volumes of requests (millions of tokens) that complete within 24 hours at ~50% cost discount versus synchronous API. Ideal for document processing, classification, and evaluation tasks that don't need real-time responses.

### Azure OpenAI Service Embeddings
API for generating vector representations of text using Ada or newer embedding models — input text, output a high-dimensional float array usable for semantic similarity search, clustering, and RAG retrieval. Combined with Azure AI Search for vector search.

### Azure OpenAI Service Fine-Tuning
Customize a base model (GPT-4o mini, etc.) on customer-provided training data to improve performance on domain-specific tasks. Fine-tuned models are private to the customer's deployment. More costly per token than base models; use when prompt engineering alone is insufficient.

### Azure OpenAI Service GPT-4o
OpenAI's flagship multimodal model available on Azure — processes text, images, and audio natively. Lower latency and cost than GPT-4 Turbo; the default recommendation for most LLM workloads in 2026.

### Azure Policy
Azure's governance guardrails — define rules (deny, audit, deploy-if-not-exists) that enforce standards across subscriptions and resource groups. Example policies: "All storage accounts must use HTTPS," "All VMs must have the monitoring agent," "No public IP addresses." AWS equivalent is AWS Config Rules + Service Control Policies (SCPs). Managed at the Management Group level for enterprise scope.

### Azure Policy Initiatives
A collection of related policy definitions bundled together — e.g., the "CIS Microsoft Azure Foundations Benchmark" initiative contains 100+ individual policies. Assign one initiative to enforce a compliance framework across all subscriptions. AWS equivalent is AWS Config Conformance Packs.

### Azure Policy Remediation Tasks
Automatically fix non-compliant resources for certain policy effects (DeployIfNotExists, Modify). For example, automatically enable diagnostic settings on new storage accounts that don't have them. Requires a Managed Identity with appropriate permissions. AWS equivalent is AWS Config Remediation Actions.

### Azure Private DNS
Manages DNS resolution within VNets without exposing records to the internet. Private DNS zones are linked to VNets; VMs resolve internal hostnames. Auto-registration links a zone to a VNet and dynamically creates A records for VMs. Essential for private endpoint resolution — when a customer creates a Private Endpoint, a private DNS zone must be configured for the endpoint's hostname to resolve to the private IP.

### Azure Private Endpoint
A private network interface in a customer's VNet that maps to a specific Azure PaaS service (Storage, SQL, Key Vault, etc.). Traffic to that service goes over the Microsoft backbone, never the public internet. The "private only" network isolation pattern for PaaS services. AWS equivalent is AWS PrivateLink / VPC Interface Endpoints. Practically mandatory in regulated industries.

### Azure Private Link
The underlying Microsoft technology that enables Private Endpoints — allows customers to expose their own services privately to other VNets or tenants. Distinct from Private Endpoint (which is the consumer side). AWS equivalent is AWS PrivateLink Endpoint Services.

### Azure Purview
See **Microsoft Purview** — Microsoft rebranded the service in 2023 but the old name persists in customer conversations.

### Azure Queue Storage
Simple, managed message queue for asynchronous decoupling — messages up to 64KB, retained up to 7 days, no ordering guarantee. Part of Azure Storage accounts. AWS equivalent is Amazon SQS (Standard). For more advanced messaging (sessions, ordering, large messages, DLQ), use Azure Service Bus instead.

### Azure Red Hat OpenShift (ARO)
Managed OpenShift (Red Hat's Kubernetes distribution) jointly operated by Microsoft and Red Hat — the control plane and worker nodes run in the customer's Azure subscription but are managed by the two vendors. Position for customers with existing OpenShift investments or Red Hat licensing who want a managed experience. AWS equivalent is ROSA (Red Hat OpenShift on AWS).

### Azure Resource Manager (ARM)
Azure's control plane — all management operations (create, update, delete, RBAC) go through ARM. ARM Templates (JSON) and Bicep (DSL) are the infrastructure-as-code languages. AWS equivalent is CloudFormation + the AWS management API. Understanding that "everything in Azure goes through ARM" helps explain how Policy, RBAC, and tagging work consistently.

### Azure Role-Based Access Control (RBAC)
Azure's authorization system — assign built-in or custom roles to users, groups, and managed identities at the scope of Management Group, Subscription, Resource Group, or individual resource. Key built-in roles: Owner (full access), Contributor (full access minus RBAC management), Reader (read-only), and service-specific roles. AWS equivalent is IAM Policies attached to identities. Azure RBAC and IAM both use the principle of least privilege, but Azure's scope hierarchy is more explicit.

### Azure Service Bus
Enterprise messaging service — supports queues (point-to-point, at-least-once delivery) and topics/subscriptions (pub/sub with filtering). Features: sessions (ordered processing), dead-letter queues, message deferral, scheduled delivery, large messages (up to 100MB with premium). AWS equivalent is Amazon SQS (queues) + Amazon SNS (topics), but Service Bus provides both in one service with more messaging features. Position over Queue Storage when customers need ordering, filtering, or DLQ.

### Azure Service Endpoints
Route traffic from a VNet subnet to Azure PaaS services (Storage, SQL, Key Vault) over the Azure backbone rather than the public internet, without changing the destination IP. Simpler than Private Endpoints (no private IP provisioned) but less isolation — the PaaS service's public endpoint still exists. Being superseded by Private Endpoints for high-security scenarios.

### Azure SignalR Service
Managed WebSocket and real-time messaging service — abstracts WebSocket, Server-Sent Events, and Long Polling. App servers push real-time notifications (dashboards, collaborative editing, live feeds) to browser or mobile clients without managing WebSocket infrastructure. AWS equivalent is AWS API Gateway WebSocket API + connection management.

### Azure Spring Apps
Managed hosting for Java Spring Boot applications — deploys Spring apps with built-in service discovery, config server, and distributed tracing. Good for customers standardizing on Spring Framework. AWS equivalent is approximately Elastic Beanstalk for Java. Less relevant for non-Java shops.

### Azure SQL
Microsoft's flagship managed relational database family — SQL Server engine as a managed cloud service. The "no SQL Server DBA required" pitch. AWS equivalent is Amazon RDS for SQL Server or Aurora (PostgreSQL/MySQL). Azure SQL is the PaaS path; if customers need the full SQL Server agent, cross-database queries, or linked servers, they need SQL Managed Instance instead.

### Azure SQL Elastic Pool
A shared pool of compute and storage resources for multiple Azure SQL databases — databases scale up when needed and share idle capacity. Cost-efficient for SaaS customers managing hundreds of small databases with unpredictable, non-overlapping workloads. AWS equivalent: no direct equivalent (RDS is per-instance; Aurora Serverless v2 is the closest).

### Azure SQL Hyperscale
A highly scalable SQL database architecture — storage up to 100TB, rapid scaling, multiple replicas (read scale-out), and fast backups via storage snapshots rather than full copies. The right answer for customers whose databases grow beyond 4TB or need sub-minute backup. Still Azure SQL (not Synapse) — for OLTP, not analytics.

### Azure SQL Ledger
A verifiable, tamper-evident ledger feature built into Azure SQL — records of table changes are cryptographically hashed and linked, allowing customers to prove data hasn't been modified without a blockchain. Relevant for audit trail, financial record integrity, and supply chain scenarios.

### Azure SQL Managed Instance (MI)
Near-100% SQL Server compatibility in a fully managed service — supports SQL Server Agent, CLR, linked servers, cross-database queries, and database mail. The migration target for customers lifting SQL Server workloads from on-premises without code changes. Deploys inside a customer's VNet. More expensive than Azure SQL DB. AWS equivalent is Amazon RDS for SQL Server (but with more feature restrictions).

### Azure SQL Serverless
Auto-pause and auto-resume compute tier for Azure SQL Database — pauses when idle (saving cost), resumes automatically when a connection arrives (cold start ~30 seconds). Good for dev/test databases and intermittently used applications. Not available for production databases requiring zero cold start.

### Azure Static Web Apps
Managed hosting for static frontends (Angular, React, Vue) with integrated serverless API backends (Azure Functions) and CI/CD via GitHub Actions or Azure DevOps. Global distribution via CDN. Free tier available. AWS equivalent is AWS Amplify Hosting. Best for JAMstack or SPA applications.

### Azure Storage Account
The container resource for all Azure Storage services — Blob, Files, Queues, and Tables live inside a storage account. Key decisions at creation: **Performance** (Standard vs Premium), **Redundancy** (LRS, ZRS, GRS, GZRS), **Account Kind** (StorageV2 recommended). AWS equivalent is an S3 bucket (but one storage account hosts multiple services).

### Azure Storage Files
Managed cloud file shares using SMB 3.0 or NFS 4.1 — mountable by Windows, Linux, and macOS clients. Used to replace on-premises Windows file servers. Key tiers: **Transaction-optimized** (general workloads), **Hot/Cool** (infrequent access), **Premium** (SSD-backed, sub-millisecond latency). AWS equivalent is Amazon EFS (NFS) or FSx for Windows File Server (SMB).

### Azure Storage Queues
See **Azure Queue Storage**.

### Azure Storage Tables
Managed NoSQL key-value/wide-column store — accessible via OData REST API. Legacy service; for new workloads with more feature requirements, use Cosmos DB Table API (migration path) or Cosmos DB NoSQL API. AWS equivalent is DynamoDB (feature-poor comparison).

### Azure Synapse Analytics
Microsoft's unified analytics service — combines SQL data warehousing (Dedicated SQL Pool), serverless SQL querying over a data lake (Serverless SQL Pool), Apache Spark, ADF pipelines, and Power BI integration in one workspace (Studio). AWS equivalent is a combination of Redshift + Athena + EMR + Glue. The "one platform for all analytics workloads" pitch.

### Azure Synapse Analytics Dedicated SQL Pool
Azure's managed data warehouse — columnar, MPP (Massively Parallel Processing) SQL engine, formerly called Azure SQL Data Warehouse. Scale by adding DWUs (Data Warehouse Units). Pause when not in use to stop compute billing while keeping storage. AWS equivalent is Amazon Redshift. Right for structured, relational analytical workloads at scale.

### Azure Synapse Analytics Link for Cosmos DB
See **Azure Cosmos DB Analytical Store** — Synapse Link is the connector between Cosmos DB's analytical store and Synapse Spark/SQL.

### Azure Synapse Analytics Pipelines
ADF pipelines embedded inside Synapse Studio — same underlying technology as Azure Data Factory but accessible without leaving the analytics workspace. For customers who want integrated orchestration without a separate ADF instance.

### Azure Synapse Analytics Serverless SQL Pool
Query data in ADLS Gen2 using T-SQL — no infrastructure to provision, pay per TB scanned. The Azure equivalent of Amazon Athena. Great for ad-hoc exploration, data lake querying, and building logical views over raw files (CSV, Parquet, JSON, Delta).

### Azure Synapse Analytics Spark Pool
Managed Apache Spark clusters within Synapse — used for large-scale data transformation, ML, and streaming. Clusters auto-pause when idle. Similar to EMR or Databricks Spark, but less mature than Databricks for data engineering; most customers reaching for Spark on Azure choose Databricks over Synapse Spark.

### Azure Synapse Analytics Studio
The web-based unified IDE for Synapse — write SQL, run Spark notebooks, design pipelines, view linked services, and browse the data lake from one interface. Reduces context switching for data teams.

### Azure Virtual Desktop (AVD)
Managed Windows virtual desktops and remote apps in Azure — multi-session Windows 11 lets many users share one VM, reducing cost vs. VDI solutions. AWS equivalent is Amazon WorkSpaces. Key pitch for customers with remote workforces, regulated environments (HIPAA, financial), or BYOD policies.

### Azure Virtual Machine Scale Sets (VMSS)
Auto-scaling groups of identical VMs — scale in/out based on metrics or schedule. Two modes: **Uniform** (all VMs identical) and **Flexible** (mix VM types, better for Availability Zones). AWS equivalent is AWS Auto Scaling Groups. Backend for AKS node pools and Service Fabric.

### Azure Virtual Machines (VMs)
IaaS compute — wide range of VM sizes across general purpose (Dsv5), compute-optimized (Fsv2), memory-optimized (Esv5), storage-optimized (Lsv3), GPU (NCv3, NDv4), and HPC (HBv4) families. AWS equivalent is EC2 with instance families. Spot VMs offer up to 90% discount for interruptible workloads (equivalent to EC2 Spot).

### Azure Virtual Network (VNet)
Azure's private network — logically isolated from other customers' networks. VMs, containers, and PaaS services (via Private Endpoints) live inside VNets. VNets are regional; span across regions via Global VNet Peering. AWS equivalent is Amazon VPC. Key concepts: Subnets, Network Security Groups (NSGs), Route Tables, and Peering.

### Azure Virtual Network DDoS Protection
See **Azure DDoS Protection**.

### Azure Virtual Network Network Security Groups (NSGs)
Stateful firewall rules at the subnet or NIC level — allow/deny traffic by source/destination IP, port, and protocol. The first line of network defense within a VNet. AWS equivalent is Security Groups (NIC-level) and Network ACLs (subnet-level), but Azure NSGs cover both in one resource.

### Azure Virtual Network Peering
Connects two VNets using the Microsoft backbone — traffic stays off the internet, low latency, no gateway required. Can peer within the same region (VNet Peering) or across regions (Global VNet Peering). AWS equivalent is VPC Peering. For hub-and-spoke designs, combine with Azure Firewall or NVAs at the hub.

### Azure Virtual Network Service Endpoints
See **Azure Service Endpoints**.

### Azure Virtual Network User-Defined Routes (UDR)
Custom route table entries that override Azure's default routing — force traffic through a firewall (NVA or Azure Firewall) or route between subnets via specific next-hops. AWS equivalent is VPC Route Tables with custom routes. Required in hub-and-spoke architectures to force spoke VNet traffic through the hub firewall.

### Azure Virtual WAN (vWAN)
Microsoft-managed network hub service — connects VNets, ExpressRoute circuits, VPN sites, and Azure Firewall into a managed global transit network. Reduces the need to manually configure hub-and-spoke routing. AWS equivalent is AWS Transit Gateway + AWS Global Accelerator. Position for customers with many regions and branch offices who need simplified network management.

### Azure VPN Gateway
Managed VPN service for site-to-site (on-premises to Azure) and point-to-site (individual devices to Azure) VPN connectivity. Gateway SKUs determine bandwidth and tunnel count. AWS equivalent is AWS Site-to-Site VPN + AWS Client VPN. Use ExpressRoute for production workloads that need dedicated bandwidth; VPN Gateway for dev/test or backup connectivity.

---

## B

### Bicep
A domain-specific language (DSL) for deploying Azure resources — transpiles to ARM JSON templates but with cleaner syntax, modules, and type safety. The recommended IaC approach for Azure-native teams. AWS equivalent is AWS CloudFormation YAML (Bicep is analogous to CDK's simplification of CloudFormation). Terraform also works on Azure — recommend Bicep for Azure-only shops, Terraform for multicloud.

### Blue-Green Deployment (Azure)
Zero-downtime deployment pattern on Azure — two identical environments (blue = current production, green = new version); switch traffic via Azure Traffic Manager, Front Door, or App Service Deployment Slots. Azure doesn't have a managed "blue-green" service like CodeDeploy; customers implement it using the above primitives.

---

## C

### Cloud Adoption Framework (CAF)
Microsoft's structured guidance for cloud adoption — covers strategy, planning, readiness (Landing Zones), migration, governance, and management. AWS equivalent is the AWS Cloud Adoption Framework. Use CAF Landing Zones as the starting point for enterprise customer conversations about how to structure Azure subscriptions and governance.

### Cost Management (Azure)
See **Azure Cost Management + Billing**.

---

## D

### Data Lake
Architectural pattern (not a specific Azure service) for storing all data — raw, structured, semi-structured — in its native format at scale, then processing it on read rather than on write (schema-on-read). On Azure, ADLS Gen2 is the storage layer; ADF, Databricks, Synapse, and HDInsight are the processing layers. AWS equivalent is S3 + Glue + EMR/Athena.

### Defender for Cloud
See **Microsoft Defender for Cloud**.

### Delta Lake
Open-source ACID storage format (Parquet files + transaction log) developed by Databricks, used natively in Azure Databricks and Microsoft Fabric. Enables reliable batch and streaming pipelines, time travel (query historical data), schema enforcement, and MERGE (upsert) operations. The default table format recommendation on Azure's data platform.

---

## E

### Entra ID
See **Azure Active Directory (Entra ID)** — Microsoft's current official name for the service.

### Entra ID Workload Identity
Federation of Kubernetes service accounts with Entra ID Managed Identities — allows pods to authenticate to Azure services without secrets. Replaces the older AAD Pod Identity. Best practice for AKS-to-Azure service auth.

---

## F

### Fabric
See **Microsoft Fabric**.

---

## G

### Global VNet Peering
Cross-region VNet connectivity using the Microsoft backbone — connects Azure VNets in different regions without gateways. Bandwidth is charged per GB transferred. AWS equivalent is VPC Peering (cross-region). For large-scale multi-region networking, Azure Virtual WAN may be more manageable.

### Governance (Azure)
The combination of Azure Policy, Management Groups, RBAC, Blueprints (deprecated; use Templates + Policy), and Microsoft Purview. AWS equivalent is AWS Organizations + SCP + Config + Control Tower. Enterprise customers need governance defined before migrating workloads — position CAF Landing Zones early.

---

## H

### Hub-and-Spoke Network Topology
The recommended Azure network architecture for enterprises — a central "hub" VNet hosts shared services (Azure Firewall, VPN Gateway, ExpressRoute Gateway, DNS), and "spoke" VNets host workloads and peer to the hub. Traffic between spokes routes through the hub firewall for inspection. AWS equivalent is Transit Gateway hub-and-spoke. Position Azure Virtual WAN as the managed version of this pattern.

### Hyperscale (Azure SQL)
See **Azure SQL Hyperscale**.

---

## I

### Infrastructure as Code (IaC) on Azure
Three main options: **ARM Templates** (JSON, verbose, native), **Bicep** (DSL on top of ARM, recommended for Azure-native), **Terraform** (HCL, multicloud, large ecosystem). AWS equivalent: CloudFormation + CDK (native), Terraform (multicloud). For teams coming from AWS CDK, Bicep or Pulumi (supports TypeScript) will feel most familiar.

---

## K

### Key Vault
See **Azure Key Vault**.

### KQL (Kusto Query Language)
The query language used by Azure Monitor Log Analytics, Azure Data Explorer, and Microsoft Sentinel. Pipe-based syntax (similar to PowerShell or Splunk SPL, not SQL). Learning curve for AWS teams used to CloudWatch Logs Insights (which has a SQL-like dialect). KQL is powerful for time-series and log analysis; investing in KQL literacy pays off across multiple Azure services.

---

## L

### Landing Zone (Azure)
A pre-configured Azure environment — subscriptions, VNets, policies, RBAC, and monitoring — that follows CAF best practices. Deployed via the Azure Landing Zone Accelerator (Bicep templates). AWS equivalent is AWS Landing Zone / Control Tower. Position this for enterprise customers starting from scratch; avoids the "organic sprawl" problem.

### LRS / ZRS / GRS / GZRS
Azure Storage redundancy options: **LRS** (Locally Redundant Storage — 3 copies in one datacenter, cheapest), **ZRS** (Zone-Redundant Storage — 3 copies across Availability Zones), **GRS** (Geo-Redundant Storage — LRS + async copy to a paired region), **GZRS** (Geo-Zone-Redundant — ZRS + async geo-copy). AWS equivalent is S3's built-in regional replication + S3 CRR for geo-copies. Most production workloads should use ZRS or GRS minimum.

---

## M

### Management Groups
A hierarchy above subscriptions — organize subscriptions into groups, apply policy and RBAC at the Management Group level. Root Management Group → child groups → subscriptions. AWS equivalent is AWS Organizations + OUs. Required for enterprise-scale governance.

### Microsoft Defender for Cloud
Cloud security posture management (CSPM) and workload protection (CWPP) — gives a unified security score, identifies misconfigurations, and detects threats across Azure, on-premises, AWS, and GCP. AWS equivalent is AWS Security Hub + GuardDuty. Recommend to any customer with compliance requirements or multi-cloud environments.

### Microsoft Defender for Cloud Defender CSPM
The Cloud Security Posture Management tier — continuously assesses all Azure resources against security best practices, provides a Secure Score, shows attack paths, and gives contextual risk prioritization. Free tier gives basic recommendations; CSPM paid tier adds AI-powered attack path analysis.

### Microsoft Defender for Cloud Defender for Servers
Integrates threat protection for Windows and Linux VMs — EDR (Endpoint Detection and Response) via Microsoft Defender for Endpoint, file integrity monitoring, adaptive application controls. AWS equivalent is AWS GuardDuty + Amazon Inspector for EC2.

### Microsoft Defender for Cloud Defender for SQL
Detects SQL injection attempts, anomalous queries, and suspicious access patterns on Azure SQL, SQL MI, and SQL Server on VMs. AWS equivalent is Amazon GuardDuty RDS Protection + Macie (partial).

### Microsoft Defender for Cloud Defender for Storage
Scans blobs for malware, detects anomalous access patterns, and alerts on sensitive data exposure in Azure Storage accounts. AWS equivalent is Amazon GuardDuty S3 Protection + Macie.

### Microsoft Defender for Cloud Security Score
A numeric score (0–100%) representing the security posture of Azure subscriptions — each recommendation has a points value; remediating recommendations raises the score. Good executive-level KPI for security posture. AWS equivalent is AWS Security Hub Security Score.

### Microsoft Fabric
Microsoft's unified analytics platform — announced 2023, GA 2023. Think of it as a single SaaS analytics experience that combines data engineering, data warehousing, data science, real-time analytics, and BI (Power BI) in one product with one storage layer (OneLake) and one billing model (Fabric Capacity, like Synapse or Power BI Premium). AWS equivalent would be a hypothetical combination of S3 + Redshift + EMR + Kinesis + QuickSight, all on one platform.

### Microsoft Fabric Data Activator
Rule-based alerting and automation on streaming data — trigger Power Automate flows, Teams messages, or emails when data conditions are met (e.g., sales drop below threshold). No-code for business users. The "data-driven automation" feature within Fabric.

### Microsoft Fabric Eventstream
Real-time event streaming within Fabric — ingest events from Event Hubs, Kafka, IoT Hub, and custom sources; transform and route to Lakehouse, KQL Database, or other destinations. The Fabric-native streaming ingestion service.

### Microsoft Fabric KQL Database
Real-time analytics database (powered by Azure Data Explorer) within Fabric — optimized for time-series, log, and telemetry queries using KQL. Faster than SQL for high-volume append-only data. AWS equivalent is Amazon Timestream or OpenSearch.

### Microsoft Fabric Lakehouse
A unified storage and metadata layer within Fabric — ADLS Gen2 files (Delta format) exposed via both SQL (T-SQL endpoint) and Spark. The architectural centerpiece of Fabric; all Fabric items (notebooks, pipelines, SQL analytics) read/write to Lakehouses.

### Microsoft Fabric OneLake
Fabric's single, tenant-wide data lake — built on ADLS Gen2, logically one lake even if data is physically in multiple regions. All Fabric workspaces and items share OneLake; no data copying between tools. The "one copy of the data, many tools" value proposition. AWS equivalent would be a single S3 bucket accessible by all analytics services — which doesn't exist natively.

### Microsoft Fabric Pipelines
Data integration pipelines within Fabric — same technology as Azure Data Factory pipelines but embedded in the Fabric workspace. For customers already on Fabric, use Fabric Pipelines instead of a separate ADF instance.

### Microsoft Fabric Real-Time Intelligence
The umbrella for Fabric's streaming capabilities — Eventstream (ingestion), KQL Database (storage), and Data Activator (alerting). AWS equivalent is a combination of Kinesis + Timestream + EventBridge.

### Microsoft Fabric Warehouse
A SQL data warehouse within Fabric — T-SQL endpoint on Delta Lake storage. Similar to Synapse Dedicated SQL Pool but built on open formats (Delta) without a separate DWU-based billing. Recommended for customers starting fresh on Fabric; existing Synapse customers may stay on Dedicated SQL Pool during transition.

### Microsoft Purview
Microsoft's unified data governance platform — cataloging, classification, lineage, and policy enforcement across Azure, on-premises, and multicloud data estates. AWS equivalent is AWS Glue Data Catalog + Macie + Lake Formation combined. Key for customers with data governance requirements (GDPR, CCPA, HIPAA).

### Microsoft Purview Data Catalog
Searchable inventory of data assets — connects to Azure Storage, SQL, Synapse, Cosmos DB, on-premises SQL Server, and third-party sources. Data stewards annotate assets with business glossary terms. Helps customers answer "where is our customer data?"

### Microsoft Purview Data Lineage
Visual end-to-end data lineage — tracks how data flows from source to destination through ADF pipelines, Synapse, and Databricks. Helps compliance teams prove chain of custody for regulated data. AWS equivalent is partially covered by AWS Glue lineage tracking.

### Microsoft Purview Data Map
The underlying catalog index — scans data sources, extracts metadata and classification labels, and populates the catalog. Scans run on schedule. The "crawler" equivalent in AWS Glue.

### Microsoft Purview Information Protection
Classification, labeling, and protection for Microsoft 365 content (emails, documents) — extends to Azure Storage and third-party clouds. Sensitivity labels can encrypt files and control sharing. AWS equivalent is Macie (discovery-focused) + Lake Formation (access control), but Purview IP covers the labeling and encryption side more comprehensively.

### Microsoft Purview Insider Risk Management
Detects anomalous user behavior that could signal data leakage — e.g., unusual download volumes before a user's last day. Machine learning-based, integrates with Microsoft 365 signals. No direct AWS equivalent.

### Microsoft Sentinel
Cloud-native SIEM (Security Information and Event Management) and SOAR (Security Orchestration and Response) — ingests logs from Azure, Microsoft 365, on-premises, and multicloud; uses AI to detect threats; automates investigation and response via playbooks (Logic Apps). AWS equivalent is Amazon Security Lake + Amazon Detective + manual SOAR integration. One of Microsoft's strongest security products — position aggressively for enterprise customers with a SOC.

---

## N

### NSG Flow Logs
Network traffic logs captured at the NSG level — record allowed and denied flows with source/destination IP, port, and protocol. Stored in Blob Storage; analyzed via Network Watcher Traffic Analytics. AWS equivalent is VPC Flow Logs.

### Network Watcher
Azure's network diagnostics service — includes IP flow verify, next hop check, VPN diagnostics, packet capture, connection monitor, and traffic analytics. AWS equivalent is VPC Reachability Analyzer + CloudWatch network monitoring.

---

## O

### OneLake
See **Microsoft Fabric OneLake**.

---

## P

### Paired Regions
Azure's geo-redundancy model — most Azure regions are paired with a second region within the same geography (e.g., East US ↔ West US 2). GRS storage replicates to the pair; during Microsoft-initiated maintenance, only one region in a pair is updated at a time. AWS equivalent is AWS region pairs for GovCloud; standard AWS regions don't have formal pairs for services. Important for data residency conversations (pairs stay within the same country in most geographies).

### Power BI
Microsoft's business intelligence and data visualization platform. Connects to hundreds of data sources; builds dashboards and reports; embeds into applications. Two licensing models: **Per-user** (Power BI Pro/Premium Per User) and **Capacity** (Power BI Premium / Fabric Capacity). AWS equivalent is Amazon QuickSight. In Azure data platform conversations, Power BI is almost always the BI layer at the end of the pipeline.

### Premium SSD v2
Azure's highest-performance managed disk tier (below Ultra Disk) — independently configurable IOPS, throughput, and size without paying for a bundle. Good for production databases that need predictable performance. AWS equivalent is EBS gp3 (customizable IOPS) or io2.

### Private Endpoint
See **Azure Private Endpoint**.

---

## R

### RBAC (Azure)
See **Azure Role-Based Access Control (RBAC)**.

### Resource Group
A logical container for Azure resources — VMs, storage accounts, databases — that share the same lifecycle. Resources can only belong to one resource group; RBAC and Policy can be scoped to a resource group. Deletion of a resource group deletes all resources inside. AWS equivalent is a combination of tagging + CloudFormation stacks (there's no direct analog). Key design decision: organize by environment (prod vs. dev) or by application; most enterprises go by application + environment.

### Resource Locks
Prevent accidental deletion or modification of Azure resources — two types: **CanNotDelete** (read and modify allowed, delete blocked) and **ReadOnly** (no changes allowed). Applied at resource, resource group, or subscription level. Inherited by child resources. Useful for protecting shared infrastructure (Key Vault, networking) from accidental changes.

---

## S

### SLA (Azure)
Azure's service level agreements vary by service and tier. Many services offer 99.9%, 99.95%, or 99.99% uptime. Using Availability Zones typically raises SLAs. Key customer conversation: composite SLA (the SLA of a multi-service architecture is the product of component SLAs — a chain of 99.9% components degrades quickly).

### Sovereign Cloud (Azure)
Dedicated Azure environments for specific government and regulatory requirements: **Azure Government** (US federal), **Azure China** (operated by 21Vianet), **Azure Germany** (model discontinued; customers moved to standard regions). Important for public sector and highly regulated customers.

### Subscription
The billing and quota boundary in Azure — all resources are created inside a subscription; costs roll up per subscription. Enterprises have multiple subscriptions (one per environment, BU, or workload type). Analogous to an AWS Account. Management Groups organize subscriptions.

### Synapse Analytics
See **Azure Synapse Analytics**.

---

## T

### Tags (Azure)
Key-value metadata applied to Azure resources and resource groups — used for cost allocation, governance (Policy can audit/enforce tags), and operational filtering. Max 50 tags per resource. AWS equivalent is AWS resource tags. Recommend a consistent tagging strategy at project start — retrofitting tags is painful.

### Traffic Manager
Azure's DNS-based global load balancer — routes clients to the closest or healthiest endpoint across regions using routing methods: Performance, Priority, Weighted, Geographic, Subnet, MultiValue. AWS equivalent is Amazon Route 53 with routing policies (latency, failover, weighted). Not a data-path load balancer; it returns a DNS record pointing to the best endpoint — the client connects directly.

---

## U

### Ultra Disk
Azure's highest-performance managed disk — configurable from 100 IOPS to 160,000+ IOPS and sub-millisecond latency. For the most demanding database (Oracle, SAP HANA) and HPC workloads. Only available in select regions and VM sizes. AWS equivalent is EBS io2 Block Express.

---

## V

### VNet Integration (App Service)
Allows App Service apps to reach resources inside a VNet (databases, caches, internal APIs) — outbound traffic from the app routes through the VNet. Does not place the app in the VNet (inbound traffic still comes through the App Service load balancer). AWS equivalent is EC2-to-VPC routing for Elastic Beanstalk; Lambda VPC integration is more analogous.

### VNet Peering
See **Azure Virtual Network Peering**.

---

## W

### WAF (Web Application Firewall)
Azure's WAF is available in two placements: on **Azure Application Gateway** (regional, WAF v2) and on **Azure Front Door** (global, WAF policy). Both use OWASP Core Rule Set plus Microsoft-managed rules and custom rules. AWS equivalent is AWS WAF. Front Door WAF handles global attacks; Application Gateway WAF handles regional, VNet-internal traffic.

### Windows Virtual Desktop
See **Azure Virtual Desktop (AVD)** — renamed in 2022.

---

## Z

### Zero Trust (Azure)
Microsoft's security model — "never trust, always verify." On Azure, implemented through Conditional Access (verify identity), Private Endpoints (minimize network exposure), Managed Identities (no stored credentials), Defender for Cloud (continuous posture assessment), and Microsoft Sentinel (threat detection). AWS equivalent is the AWS Zero Trust architecture guidance using similar component combinations. Position whenever a customer asks about modern security posture or is moving away from perimeter-based ("castle and moat") security.

### Zone-Redundant Storage (ZRS)
Azure Storage redundancy that replicates data synchronously across three Availability Zones within a single region — survives an entire zone failure with no data loss or rehydration delay. AWS equivalent is S3's default intra-region redundancy (always spread across ≥3 AZs). ZRS is the minimum recommendation for production storage in regions with Availability Zones.
