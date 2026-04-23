# GCP Glossary

A comprehensive A–Z reference of Google Cloud Platform services, sub-features, architectural concepts, and terminology. Written for Solution Architects who know AWS well but are new to GCP — mapping GCP concepts to familiar AWS equivalents, explaining what each term means, why it matters, and how to talk about it in a customer conversation. Sorted alphabetically.

---

## Services with Sub-Entries

| Service | Sub-entries |
|---|---|
| **AlloyDB** | AlloyDB Omni, AlloyDB AI, Read Pools |
| **Anthos / GKE Enterprise** | Config Management, Fleet, Ingress for Anthos, Multi-Cloud, Policy Controller, Service Mesh |
| **Apigee** | API Analytics, API Products, Developer Portal, Hybrid, Monetization, Sense |
| **Artifact Registry** | Remote Repositories, Virtual Repositories |
| **BigQuery** | Authorized Views, BigQuery ML, BI Engine, Data Transfer Service, Editions, Omni, Reservations, Row-Level Security, Scheduled Queries, Slot Commitments, Storage API, Streaming Inserts, Workload Management |
| **Bigtable** | App Profiles, Autoscaling, Replication |
| **Cloud Armor** | Adaptive Protection, Bot Management, Edge Security Policies, Security Policies |
| **Cloud Billing** | Billing Budgets, Billing Export, Committed Use Discounts, Cost Table, Sustained Use Discounts |
| **Cloud Build** | Build Triggers, Private Pools, Workers |
| **Cloud CDN** | Cache Modes, Cache Keys, Signed URLs |
| **Cloud DNS** | Forwarding Zones, Managed Zones, Peering Zones, Private Zones, Response Policies |
| **Cloud Functions** | 1st Gen, 2nd Gen, Cloud Run Functions |
| **Cloud IAM** | Conditions, Custom Roles, Policy Bindings, Service Accounts, Workforce Identity Federation, Workload Identity Federation |
| **Cloud IDS** | Threat Detection |
| **Cloud Interconnect** | Dedicated Interconnect, Partner Interconnect |
| **Cloud Key Management Service (KMS)** | Autokey, Cloud HSM, EKM (External Key Manager), Key Rings |
| **Cloud Load Balancing** | Application Load Balancer (external), Application Load Balancer (internal), Network Load Balancer, Cross-Region Load Balancer, SSL Proxy, TCP Proxy |
| **Cloud Logging** | Log Analytics, Log Buckets, Log Exclusions, Log Router, Log Sinks, Log-Based Metrics |
| **Cloud Monitoring** | Alerting Policies, Dashboards, Managed Prometheus, SLOs, Uptime Checks |
| **Cloud NAT** | Manual NAT, Auto NAT |
| **Cloud Run** | Cloud Run Jobs, Cloud Run Functions, Cloud Run for Anthos, Sidecars |
| **Cloud Spanner** | Autoscaler, Change Streams, FGAC (Fine-Grained Access Control), Spanner Graph, Spanner Dual-Region, Spanner Multi-Region |
| **Cloud SQL** | Cloud SQL Auth Proxy, Cloud SQL for MySQL, Cloud SQL for PostgreSQL, Cloud SQL for SQL Server, Read Replicas |
| **Cloud Storage** | Autoclass, Notifications, Object Lifecycle Management, Object Versioning, Retention Policies, Signed URLs, Transfer Service, Uniform Bucket-Level Access |
| **Cloud VPN** | Classic VPN, HA VPN |
| **Composer (Cloud Composer)** | Composer 1, Composer 2, Composer 3 |
| **Compute Engine** | Committed Use Discounts, Custom Machine Types, Hyperdisk, Managed Instance Groups, Preemptible VMs, Reservations, Shielded VMs, Sole-Tenant Nodes, Spot VMs, Sustained Use Discounts |
| **Dataflow** | Dataflow Flex Templates, Dataflow Prime, Dataflow Shuffle |
| **Dataplex** | Auto Data Quality, Data Catalog (Dataplex), Lakes/Zones/Assets, Universal Metadata |
| **Dataproc** | Dataproc Metastore, Dataproc on GKE, Dataproc Serverless |
| **Firestore** | Datastore Mode, Native Mode |
| **GKE (Google Kubernetes Engine)** | Autopilot, Config Connector, GKE Standard, Node Auto-Provisioning, Node Pools, Workload Identity |
| **Looker** | Looker Studio, Looker (Enterprise BI), LookML, Looker Blocks |
| **Memorystore** | Memorystore for Redis, Memorystore for Redis Cluster, Memorystore for Valkey |
| **Network Connectivity Center** | Router Appliances, Spokes, VPN Spokes |
| **Pub/Sub** | Pub/Sub Lite, BigQuery Subscriptions, Cloud Storage Subscriptions, Push Subscriptions, Pull Subscriptions, Snapshots |
| **Secret Manager** | Regional Secrets, Secret Versions |
| **Security Command Center** | Attack Path Simulation, Event Threat Detection, Premium Tier, Security Health Analytics, Standard Tier, Virtual Machine Threat Detection |
| **Vertex AI** | Agent Builder, AutoML, Colab Enterprise, Custom Training, Datasets, Endpoints, Evaluation, Experiments, Feature Store, Gemini (Vertex), Grounding, Model Garden, Model Monitoring, Model Registry, Pipelines, Prediction, RAG Engine, Vector Search, Workbench |
| **VPC (Virtual Private Cloud)** | Firewall Policies, Firewall Rules, Flow Logs, Packet Mirroring, Private Google Access, Private Service Connect, Shared VPC, VPC Network Peering, VPC Service Controls |

---

## A

### 1. Access Transparency
A GCP feature that gives customers near-real-time logs whenever Google staff access customer content (e.g., for support). AWS equivalent: none direct (AWS Access Analyzer is different). Matters for regulated customers who need to verify that cloud vendor access is auditable.

### 2. AlloyDB
Google's fully managed, PostgreSQL-compatible database built on a disaggregated storage architecture. Designed for demanding OLTP and hybrid OLTP/analytics workloads. AWS equivalent: Aurora PostgreSQL. Key differentiator: columnar engine for analytics queries runs alongside OLTP without a separate cluster, and Google claims 4× faster than standard PostgreSQL for OLTP.

#### 2a. AlloyDB AI
An integrated capability that adds vector search, embeddings generation via Vertex AI, and direct model inference calls inside SQL queries. Lets customers build GenAI-powered features (semantic search, recommendations) without extracting data to a separate vector DB. Recommend when customers want to keep AI pipelines close to their operational data.

#### 2b. AlloyDB Omni
A downloadable, containerized version of AlloyDB that runs on any infrastructure — on-prem, other clouds, or a developer laptop. AWS equivalent: nothing direct (Aurora doesn't run outside AWS). Recommend when customers want AlloyDB compatibility in a hybrid or multi-cloud model.

#### 2c. AlloyDB Read Pools
Horizontally scalable read replicas within AlloyDB that share the same disaggregated storage as the primary, so there's no replication lag for data on disk. Scales read capacity independently of write capacity. Recommend for read-heavy OLTP workloads.

### 3. Anthos / GKE Enterprise
Google's hybrid and multi-cloud platform for managing Kubernetes clusters across GCP, on-prem (via Anthos on VMware or bare metal), AWS, and Azure. Now marketed as GKE Enterprise. AWS equivalent: EKS Anywhere + EKS Anywhere on VMware. The key pitch: single control plane and policy enforcement across all clusters.

#### 3a. Anthos Config Management (ACM)
A GitOps tool that syncs Kubernetes manifests from a Git repo to all registered clusters. AWS equivalent: Flux/ArgoCD (not a native AWS service). Ensures configuration consistency across clusters — important for customers with compliance requirements.

#### 3b. Fleet
The logical grouping of GKE clusters (and other Anthos-managed clusters) under a single management boundary. Think of it as the "org-level" umbrella. Enables uniform policy, config, and observability across a mixed fleet. Recommend when customers manage 10+ clusters.

#### 3c. Anthos Ingress for Anthos (Multi-cluster Ingress)
A globally distributed L7 load balancer that routes traffic across multiple GKE clusters in different regions using Cloud Load Balancing. AWS equivalent: Route 53 + ALB across regions, but with tighter Kubernetes integration. Simplifies active-active global deployments.

#### 3d. Anthos Multi-Cloud
Extends GKE Enterprise management plane to clusters running on AWS or Azure. Lets customers use the same GKE tooling, policy, and observability regardless of where Kubernetes runs. Useful for customers standardizing on Kubernetes operational tooling across clouds.

#### 3e. Anthos Policy Controller
Based on Open Policy Agent (OPA) Gatekeeper. Enforces custom admission policies on Kubernetes resources at deploy time. AWS equivalent: Kyverno (not native). Matters for customers who need to prevent misconfigured workloads from being deployed (e.g., no containers running as root).

#### 3f. Anthos Service Mesh (ASM)
A managed Istio-based service mesh for traffic management, mTLS between services, observability, and access policies. AWS equivalent: App Mesh (deprecated) or EKS with Istio. Recommend when customers need zero-trust networking between microservices or detailed service-level traffic visibility.

### 4. Apigee
Google Cloud's enterprise API management platform — design, secure, publish, analyze, and monetize APIs. AWS equivalent: API Gateway + some of the features require third-party tools. Apigee is significantly more feature-rich than AWS API Gateway for enterprise API programs.

#### 4a. Apigee API Analytics
Built-in dashboards showing API traffic, latency, error rates, and developer adoption. Helps customers understand which APIs are used, by whom, and where failures occur — useful for API product teams.

#### 4b. Apigee API Products
A packaging abstraction in Apigee that bundles one or more API proxies under a single product that developers subscribe to. Enables rate limiting, access control, and monetization per product rather than per API. Key differentiator vs. AWS: native support for API product catalogs.

#### 4c. Apigee Developer Portal
A customizable self-service portal where external developers discover, subscribe to, and test APIs. AWS API Gateway has a basic developer portal; Apigee's is more enterprise-grade with custom branding and full lifecycle management.

#### 4d. Apigee Hybrid
Runs the Apigee runtime (API proxies) on-prem or in another cloud while the management plane stays in GCP. AWS equivalent: nothing native. Matters for customers with data residency requirements or who need API gateways closer to on-prem backends.

#### 4e. Apigee Monetization
Native billing and revenue-sharing capabilities for APIs — charge per call, per tier, revenue share with partners. AWS API Gateway has no equivalent. Recommend when the customer is building an API-as-a-product business.

#### 4f. Apigee Sense
Threat detection for APIs — identifies bot traffic, brute-force attacks, and unusual usage patterns. Feeds into Cloud Armor for enforcement. Complements API security at the traffic-analysis layer.

### 5. App Engine
GCP's original PaaS — developers push code and Google handles infrastructure. Two environments: Standard (sandboxed, fast scaling to zero, language runtimes) and Flexible (Docker-based, more runtime flexibility). AWS equivalent: Elastic Beanstalk. For new projects, Cloud Run is generally preferred, but App Engine Standard remains popular for rapid prototyping and its deep GCP integration.

#### 5a. App Engine Standard
Runs in Google-managed sandboxes. Scales to zero instantly, bills per request (not per instance-hour). Supports Python, Java, Go, PHP, Node.js, Ruby. Ideal for bursty, variable workloads where cold starts are acceptable.

#### 5b. App Engine Flexible
Runs in Docker containers on Compute Engine VMs. Supports any language/runtime but does not scale to zero and has a minimum of one instance always running. For workloads that need custom runtimes or background threads but still want managed infrastructure.

### 6. Artifact Registry
Google's managed repository for container images, Maven packages, npm packages, Python packages, and other build artifacts. AWS equivalent: ECR + CodeArtifact combined. Replaces the older Container Registry.

#### 6a. Artifact Registry Remote Repositories
Proxy and cache artifacts from upstream public registries (Docker Hub, Maven Central, PyPI, npm). Prevents build failures due to public registry outages and reduces egress costs. AWS equivalent: CodeArtifact upstream proxying.

#### 6b. Artifact Registry Virtual Repositories
A single logical repository that aggregates multiple upstream repositories behind one endpoint, with a configurable priority order. Simplifies dependency management when teams use a mix of internal and proxied public artifacts.

---

## B

### 7. Bare Metal Solution
Google's managed offering to run specialized workloads (Oracle Database, SAP HANA) on dedicated physical hardware colocated in Google data centers, connected to GCP via high-speed networking. AWS equivalent: Dedicated Hosts, but with the workload still in AWS. Bare Metal Solution provides the physical isolation and licensing models Oracle/SAP customers require, with GCP connectivity for surrounding cloud services.

### 8. BigQuery
Google's serverless, petabyte-scale data warehouse and analytics platform. Often cited as GCP's biggest differentiator. AWS equivalent: Redshift, but with a fundamentally different pricing and architecture model — storage and compute are always separated, there's no cluster to manage, and you pay per query by default. The pitch: zero infrastructure, run SQL on petabytes, and combine with Gemini for AI-powered analytics.

#### 8a. BigQuery Authorized Views
A mechanism to share a subset of data from a dataset with another project or user without exposing the underlying tables. Enables row-level or column-level data sharing across teams or customers. AWS equivalent: Redshift datasharing + Lake Formation fine-grained permissions.

#### 8b. BigQuery BI Engine
An in-memory analysis service that accelerates BI tools (Looker Studio, Tableau, etc.) querying BigQuery by caching frequently accessed data. Reduces query latency from seconds to sub-second for dashboard workloads. AWS equivalent: Redshift Concurrency Scaling.

#### 8c. BigQuery Data Transfer Service
Managed connectors that automatically load data into BigQuery from SaaS sources (Google Ads, YouTube, Salesforce, etc.) on a schedule. AWS equivalent: Glue connectors + AppFlow. Reduces pipeline engineering effort for common marketing/sales data sources.

#### 8d. BigQuery Editions
The pricing model introduced in 2023 replacing flat-rate and on-demand tiers with three editions: **Standard** (on-demand + autoscaling slots), **Enterprise** (committed slots, PITR, BI Acceleration), and **Enterprise Plus** (highest SLA, geo-redundancy). Helps customers balance cost predictability vs. flexibility.

#### 8e. BigQuery ML (BQML)
Allows data analysts to create and train ML models using standard SQL inside BigQuery — no need to extract data to Vertex AI or Spark. AWS equivalent: Redshift ML (which calls SageMaker under the hood). Recommend when customers have strong SQL skills and want to add ML without learning Python/ML tooling.

#### 8f. BigQuery Omni
Runs BigQuery analytics on data stored in AWS S3 or Azure Blob Storage without moving it. Powered by Anthos. AWS equivalent: Redshift Spectrum or Athena (query S3 in place), but from a different cloud's analytics engine. Matters for multi-cloud customers who don't want to centralize all data in GCP.

#### 8g. BigQuery Reservations / Slot Commitments
Buy compute capacity (slots) upfront for 1-year or 3-year terms at discounted rates, then assign that capacity to projects or workloads. AWS equivalent: Redshift Reserved Nodes. Recommend for customers with predictable, high-volume analytics workloads.

#### 8h. BigQuery Row-Level Security
Row Access Policies filter which rows a user or group sees when querying a table. Enables multi-tenant analytics on a shared table without duplicating data. AWS equivalent: Lake Formation row-level filters.

#### 8i. BigQuery Scheduled Queries
Automate recurring SQL queries (e.g., nightly table refreshes, aggregations). Native to BigQuery, no external orchestration required for simple schedules. For complex pipelines, use Cloud Composer (Airflow).

#### 8j. BigQuery Storage API
A high-throughput API to read BigQuery table data directly into Spark, Pandas, or other compute frameworks — bypassing the query engine. Much faster than `EXPORT DATA` for bulk reads. AWS equivalent: S3 Select / Redshift UNLOAD for bulk extraction.

#### 8k. BigQuery Streaming Inserts
API to insert rows into BigQuery in near-real-time (seconds latency). Higher cost per row than batch loads, not transactional. For lower-latency scenarios, the BigQuery Storage Write API (with COMMITTED mode) is now preferred.

#### 8l. BigQuery Workload Management
The combination of Reservations, slot autoscaling, and job queues that lets admins prioritize, cap, and allocate BigQuery compute across teams. Critical for large enterprises where different departments share one BigQuery organization.

### 9. Bigtable
A fully managed, wide-column NoSQL database designed for low-latency reads/writes at massive scale — think billions of rows and thousands of columns. Powers Google Search, Gmail, and Maps internally. AWS equivalent: DynamoDB (key-value/document) or Cassandra on EC2. The key difference: Bigtable is optimized for time-series, IoT, and AdTech workloads with high read/write throughput, while DynamoDB excels at lower-scale, higher-flexibility use cases.

#### 9a. Bigtable App Profiles
Named routing configurations that determine which cluster handles reads/writes and what consistency model to use. Lets different applications (e.g., bulk data pipeline vs. user-facing app) share the same Bigtable instance with different performance/consistency tradeoffs.

#### 9b. Bigtable Autoscaling
Automatically adjusts the number of nodes in a cluster based on CPU utilization. Reduces cost during quiet periods and prevents throttling during traffic spikes. Node changes take 20+ minutes — not instant. Plan for gradual autoscaling, not burst spikes.

#### 9c. Bigtable Replication
Synchronizes data across multiple Bigtable clusters in different zones or regions. Enables high availability, disaster recovery, and geographically distributed reads. Replication is eventually consistent by default.

### 10. Cloud Armor
GCP's DDoS protection and Web Application Firewall (WAF) service, integrated with Cloud Load Balancing. AWS equivalent: Shield + WAF. Protects applications at the edge before traffic reaches backends.

#### 10a. Cloud Armor Adaptive Protection
ML-based anomaly detection that automatically generates suggested WAF rules when it detects potential DDoS attacks. Reduces manual response time during attacks. AWS equivalent: Shield Advanced automatic mitigation.

#### 10b. Cloud Armor Bot Management
Integrates with reCAPTCHA Enterprise to detect and manage bot traffic — allow, redirect, or block based on bot scores. AWS equivalent: WAF Bot Control.

#### 10c. Cloud Armor Edge Security Policies
WAF policies applied at Google's edge PoPs before traffic enters GCP's network. Provides protection for Cloud CDN-cached content even before it hits a load balancer. AWS equivalent: WAF rules on CloudFront.

#### 10d. Cloud Armor Security Policies
Rule sets (IP allowlists/denylists, geo-blocking, OWASP Top 10 WAF rules, rate limiting) attached to a backend service. The primary mechanism to protect web apps and APIs behind Cloud Load Balancing.

### 11. Cloud Billing
GCP's cost management layer — invoicing, cost allocation, budget enforcement, and discount management.

#### 11a. Cloud Billing Budgets
Set spending thresholds and trigger alerts or programmatic actions (e.g., disable billing via Pub/Sub) when costs approach or exceed a limit. AWS equivalent: AWS Budgets.

#### 11b. Cloud Billing Export
Export billing data to BigQuery for custom reporting, chargeback analysis, or cost anomaly detection. AWS equivalent: AWS Cost and Usage Report to S3. Recommend this immediately for any customer doing finance reporting.

#### 11c. Committed Use Discounts (CUDs)
Discounts of up to 57% for committing to use specific resources (vCPUs, memory, GPU) for 1 or 3 years. Two types: **Resource-based** (specific instance family) and **Spend-based** (commit to a dollar amount for Cloud SQL, Cloud Run, etc.). AWS equivalent: Reserved Instances / Savings Plans.

#### 11d. Sustained Use Discounts (SUDs)
Automatic discounts applied to Compute Engine VMs that run for more than 25% of a month — no commitment required. The longer an instance runs, the bigger the discount (up to 30%). AWS equivalent: nothing direct — SUDs are unique to GCP. Key SA talking point: GCP rewards consistent workloads automatically.

### 12. Cloud Build
GCP's managed CI/CD build service — runs containerized build steps defined in `cloudbuild.yaml`. AWS equivalent: CodeBuild.

#### 12a. Cloud Build Triggers
Automatically start builds on Git events (push, PR, tag) from Cloud Source Repositories, GitHub, GitLab, or Bitbucket. AWS equivalent: CodePipeline source stage + CodeBuild.

#### 12b. Cloud Build Private Pools
Dedicated build infrastructure running in the customer's VPC. Enables builds that access private resources (databases, internal APIs) without exposing them to the internet. AWS equivalent: CodeBuild in a VPC.

#### 12c. Cloud Build Workers
The compute that runs each build step. Default workers are ephemeral and managed by Google. Private Pool workers run in the customer's VPC on dedicated Compute Engine VMs.

### 13. Cloud CDN
Google's content delivery network, integrated with Cloud Load Balancing. Caches HTTP(S) responses at Google's globally distributed edge PoPs. AWS equivalent: CloudFront.

#### 13a. Cloud CDN Cache Modes
Controls what gets cached: **USE_ORIGIN_HEADERS** (respects origin cache headers), **CACHE_ALL_STATIC** (caches static assets regardless of headers), **FORCE_CACHE_ALL** (caches everything). Enables aggressive caching even for origins that don't set proper cache headers.

#### 13b. Cloud CDN Cache Keys
Customize what attributes (URL, headers, cookies, query params) define a unique cached object. Reduces cache fragmentation and increases cache hit rates. AWS equivalent: CloudFront cache policies.

#### 13c. Cloud CDN Signed URLs / Signed Cookies
Restrict CDN content access to requests with a valid cryptographic signature — used for paywalled content, time-limited downloads. AWS equivalent: CloudFront signed URLs.

### 14. Cloud Composer
Managed Apache Airflow service for workflow orchestration. AWS equivalent: MWAA (Managed Workflows for Apache Airflow).

#### 14a. Composer 1 / 2 / 3
Version generations of Cloud Composer. Composer 2 introduced autoscaling workers and better isolation. Composer 3 (latest) improves scalability and cost efficiency further. Always recommend the latest generation for new deployments.

### 15. Cloud Data Fusion
A visual, code-free ETL/ELT pipeline builder based on CDAP (open source). AWS equivalent: Glue Studio (visual ETL). Recommend for customers who need business analysts or data engineers without Spark coding skills to build data pipelines.

### 16. Cloud Deploy
A managed continuous delivery service for releasing applications to GKE, Cloud Run, and GKE Enterprise. Provides release approvals, rollback, canary deployments, and deployment history. AWS equivalent: CodeDeploy.

### 17. Cloud DNS
Google's managed, authoritative DNS service. AWS equivalent: Route 53.

#### 17a. Cloud DNS Forwarding Zones
Forward DNS queries for specific domains to on-prem or other DNS resolvers. Essential for hybrid setups where on-prem services need to resolve cloud DNS names and vice versa. AWS equivalent: Route 53 Resolver inbound/outbound endpoints.

#### 17b. Cloud DNS Managed Zones
The primary DNS container — a public or private zone that holds DNS records for a domain. AWS equivalent: Route 53 hosted zones.

#### 17c. Cloud DNS Peering Zones
Share DNS resolution from one VPC to another for private zones. Useful when a shared VPC needs to resolve names from a service producer's VPC. AWS equivalent: Route 53 private hosted zone sharing.

#### 17d. Cloud DNS Private Zones
DNS zones visible only within specified VPCs. Used for internal service discovery. AWS equivalent: Route 53 private hosted zones.

#### 17e. Cloud DNS Response Policies
Intercept and override DNS responses within a VPC — useful for split-horizon DNS or redirecting specific domains. No direct AWS equivalent.

### 18. Cloud Endpoints
A managed proxy (based on Extensible Service Proxy / ESP) for deploying, securing, and monitoring APIs running on App Engine, GKE, or Compute Engine. AWS equivalent: API Gateway (basic tier). For production enterprise APIs, Apigee is the preferred recommendation.

### 19. Cloud Functions
GCP's serverless, event-driven compute for small units of code. AWS equivalent: Lambda.

#### 19a. Cloud Functions 1st Gen
Original generation — single-instance concurrency, limited max instances, older runtime support. Still supported but not recommended for new deployments.

#### 19b. Cloud Functions 2nd Gen / Cloud Run Functions
Built on Cloud Run. Adds: up to 1000 concurrent requests per instance, longer timeout (up to 60 minutes), larger instances (up to 32 GB RAM), and traffic-splitting for gradual rollouts. The recommended generation for all new Cloud Functions deployments.

### 20. Cloud Healthcare API
Managed storage and processing of healthcare data in FHIR, HL7v2, and DICOM formats. AWS equivalent: HealthLake + HealthImaging. Matters for hospitals and health systems needing cloud-native interoperability.

### 21. Cloud IAM (Identity and Access Management)
GCP's access control system. AWS equivalent: IAM. Key GCP-specific terminology: **principals** (users, groups, service accounts, workload identities), **roles** (primitive, predefined, custom), **bindings** (role assigned to principal on a resource). Permissions flow from Organization → Folder → Project → Resource and are additive (no explicit deny by default, unlike AWS).

#### 21a. Cloud IAM Conditions
Attribute-based access control — grant a role only when conditions are met (time of day, resource tags, IP range). AWS equivalent: IAM Condition keys. Enables just-in-time access and time-limited elevated permissions.

#### 21b. Cloud IAM Custom Roles
Create roles with exactly the permissions needed — principle of least privilege. AWS equivalent: IAM custom policies. Note: GCP has thousands of fine-grained permissions; custom roles require careful assembly.

#### 21c. Cloud IAM Policy Bindings
The mechanism that attaches a role to a principal at a resource level. Each resource has an IAM policy (a list of bindings). AWS equivalent: resource-based policies. Understanding bindings is foundational to GCP security conversations.

#### 21d. Service Accounts
GCP's identity for compute resources and applications — not humans. AWS equivalent: IAM roles for EC2/Lambda. Key nuance: service accounts can themselves be granted roles, AND humans can impersonate service accounts (useful for temporary elevated access). A service account key is a JSON credential — avoid using service account keys in favor of workload identity federation.

#### 21e. Workforce Identity Federation
Allows external identity providers (Okta, Azure AD, ADFS) to authenticate human users to GCP without requiring a Google identity. AWS equivalent: IAM Identity Center with external IdP. Matters for enterprises that don't want to manage Google accounts separately.

#### 21f. Workload Identity Federation
Allows workloads running outside GCP (GitHub Actions, AWS Lambda, Azure Functions) to authenticate to GCP APIs without long-lived service account keys — using short-lived OIDC tokens instead. AWS equivalent: IAM roles with OIDC web identity federation. Security best practice for multi-cloud or CI/CD pipelines.

### 22. Cloud IDS (Intrusion Detection System)
A managed network-based intrusion detection service that uses Google Cloud's threat intelligence and Palo Alto Networks' signature database. Monitors network traffic for threats. AWS equivalent: GuardDuty (network threat detection portion). Cloud IDS requires Packet Mirroring to copy traffic to the inspection engine.

### 23. Cloud Interconnect
Dedicated physical network connections between on-prem infrastructure and GCP. AWS equivalent: Direct Connect.

#### 23a. Dedicated Interconnect
A direct, private 10 Gbps or 100 Gbps connection from the customer's network to Google's network at a colocation facility. Highest performance and lowest latency option. Requires physical presence at a supported colocation.

#### 23b. Partner Interconnect
Connect to GCP through a Google-approved network service provider when the customer can't reach a Google colocation directly. More accessible geographically, but introduces a third-party provider in the path.

### 24. Cloud Key Management Service (KMS)
Managed encryption key management — create, rotate, disable, and audit cryptographic keys. AWS equivalent: KMS.

#### 24a. Cloud KMS Autokey
Automatically creates and manages encryption keys for supported GCP services without requiring the customer to configure key rings manually. Reduces the operational burden of implementing CMEK across a project.

#### 24b. Cloud HSM
Hardware Security Module integration within Cloud KMS — keys are generated and stored in FIPS 140-2 Level 3 validated hardware. AWS equivalent: AWS CloudHSM or KMS with HSM-backed keys. For customers with the strictest key material requirements.

#### 24c. Cloud External Key Manager (EKM)
Allows customers to maintain encryption keys outside GCP (in a supported third-party key management system) and reference them for encrypting GCP data. Key material never leaves the external system. AWS equivalent: AWS KMS with custom key store (XKS). For highly regulated industries that require keys never reside in a cloud provider's infrastructure.

#### 24d. Key Rings
Logical grouping of keys within Cloud KMS — used for organization and IAM policy attachment. Keys inherit permissions from their key ring. AWS equivalent: KMS key policies per key (no grouping equivalent).

### 25. Cloud Load Balancing
GCP's global, fully managed load balancing service. Unlike AWS, all GCP load balancers are software-defined and globally distributed — no instance to provision. AWS equivalent: ELB family (ALB, NLB, GWLB, GLB).

#### 25a. Application Load Balancer (External)
L7 HTTP(S) load balancer that can operate in **Global** mode (anycast IP, traffic served from Google edge PoPs) or **Classic** mode. Supports URL-based routing, SSL termination, Cloud Armor integration. AWS equivalent: ALB + CloudFront for global.

#### 25b. Application Load Balancer (Internal)
L7 load balancer for traffic within a VPC or between VPCs via Shared VPC. Supports URL routing, gRPC, and proxy headers for internal microservices. AWS equivalent: Internal ALB.

#### 25c. Network Load Balancer
Pass-through L4 load balancer (external or internal) that preserves client IP and supports TCP/UDP/ESP. External NLB supports a global backend service. AWS equivalent: NLB.

#### 25d. Cross-Region Load Balancer
A global Application Load Balancer that automatically routes traffic to the nearest healthy backend across regions. Enables sub-100ms failover for global apps without DNS changes. AWS equivalent: Route 53 latency-based routing + ALB (less seamless).

#### 25e. SSL Proxy / TCP Proxy Load Balancers
L4 proxy-based load balancers for non-HTTP traffic. SSL Proxy terminates SSL. TCP Proxy routes based on TCP connection. AWS equivalent: NLB with TLS termination.

### 26. Cloud Logging
Centralized log management — collects logs from GCP services, applications (via agent), and Google Workspace. AWS equivalent: CloudWatch Logs.

#### 26a. Cloud Logging Log Buckets
Storage containers for logs, configurable with retention periods and region lock. Logs can be stored in the Default bucket (30-day retention) or custom buckets with longer retention. AWS equivalent: CloudWatch Log Groups with retention policies.

#### 26b. Cloud Logging Log Analytics
Run SQL queries against logs stored in Cloud Logging, powered by BigQuery. Enables complex analysis (e.g., correlate log events across services) without exporting to BigQuery first. AWS equivalent: CloudWatch Logs Insights.

#### 26c. Cloud Logging Log Exclusions
Filter out specific log entries before they're ingested to reduce costs. High-volume, low-value logs (e.g., health check hits) are common candidates. AWS equivalent: CloudWatch Logs subscription filters.

#### 26d. Cloud Logging Log Router
Routes log entries to one or more destinations (Cloud Logging buckets, Cloud Storage, Pub/Sub, BigQuery) based on filters. The routing happens before ingestion costs are incurred. AWS equivalent: CloudWatch Logs subscription + Kinesis Firehose.

#### 26e. Cloud Logging Log Sinks
Specific destination configurations within the Log Router — routes log entries matching a filter to Cloud Storage, BigQuery, Pub/Sub, or another Logging bucket. Key mechanism for log archival and SIEM integration.

#### 26f. Log-Based Metrics
Create Cloud Monitoring metrics from log entries matching a filter — count errors, track specific events. AWS equivalent: CloudWatch Metrics Filters.

### 27. Cloud Monitoring
GCP's metrics, alerting, and observability service. AWS equivalent: CloudWatch Metrics + Alarms.

#### 27a. Cloud Monitoring Alerting Policies
Define conditions that trigger notifications (email, PagerDuty, Pub/Sub, etc.) when metrics cross thresholds. AWS equivalent: CloudWatch Alarms.

#### 27b. Cloud Monitoring Dashboards
Build custom metric visualizations. AWS equivalent: CloudWatch Dashboards.

#### 27c. Managed Service for Prometheus (GMP)
Google-managed Prometheus — scrapes metrics from Kubernetes workloads and stores them in Google's globally replicated, horizontally scalable backend. No Prometheus server to operate. AWS equivalent: Amazon Managed Service for Prometheus. Key pitch: scales to billions of time series without ops overhead.

#### 27d. Cloud Monitoring SLOs
Native Service Level Objective tracking — define error budgets based on request success rates or latency percentiles, then monitor burn rate. AWS equivalent: CloudWatch SLO (limited); most AWS customers use DataDog or custom dashboards. A strong differentiator for SRE-focused customers.

#### 27e. Uptime Checks
Synthetic monitors that probe a URL or TCP endpoint from multiple global locations and alert on failures. AWS equivalent: CloudWatch Synthetics / Route 53 Health Checks.

### 28. Cloud NAT
A managed, software-defined Network Address Translation service that lets VMs without external IPs reach the internet. AWS equivalent: NAT Gateway.

#### 28a. Cloud NAT Auto NAT
Automatically allocates external IP addresses from a pool as needed. Simplest configuration.

#### 28b. Cloud NAT Manual NAT
Customer specifies which external IPs to use. Enables IP allowlisting with known egress IPs for external SaaS applications.

### 29. Cloud Run
GCP's fully managed serverless container platform — run any container without managing infrastructure. AWS equivalent: Fargate on ECS or Lambda Container Images. The key pitch: bring any Docker container, pay only for requests.

#### 29a. Cloud Run Jobs
Run containers to completion (batch or cron) rather than handling HTTP requests. AWS equivalent: Fargate Task scheduled via EventBridge, or Lambda with longer timeout. Ideal for data processing, ML batch inference, report generation.

#### 29b. Cloud Run Functions
The new brand name for Cloud Functions 2nd Gen — HTTP-triggered serverless functions, built on and deployed to Cloud Run infrastructure. Same platform, source-code-centric deployment experience.

#### 29c. Cloud Run for Anthos (Cloud Run on GKE)
Deploy Cloud Run workloads to existing GKE clusters (on-prem or cloud) rather than Google's managed infrastructure. Requires Anthos. Recommend when customers want serverless developer experience on their own Kubernetes clusters.

#### 29d. Cloud Run Sidecars
Attach additional containers to a Cloud Run service that run alongside the main container (e.g., Envoy proxy, logging agents). Enables service mesh integration and secrets management without modifying application code.

### 30. Cloud Scheduler
A fully managed cron job service — schedule HTTP/S calls to Cloud Run, Cloud Functions, Pub/Sub, or any HTTP endpoint. AWS equivalent: EventBridge Scheduler.

### 31. Cloud Spanner
Google's horizontally scalable, globally distributed, strongly consistent relational database — unique in offering ACID transactions at planetary scale with 99.999% SLA. AWS equivalent: Aurora Global Database gets close but does not offer the same write scalability across regions. The iconic pitch: "the only database that offers both relational consistency and horizontal write scaling."

#### 31a. Cloud Spanner Autoscaler
Automatically adjusts Spanner processing units (compute) based on CPU utilization. Reduces cost during off-peak hours. AWS equivalent: Aurora Serverless v2 autoscaling.

#### 31b. Cloud Spanner Change Streams
Capture and stream DML changes (INSERT/UPDATE/DELETE) from Spanner tables to downstream consumers via Dataflow. AWS equivalent: DynamoDB Streams or Aurora with DMS change capture.

#### 31c. Spanner Fine-Grained Access Control (FGAC)
Database roles and column-level access controls within Spanner. Enables masking or restricting specific columns from specific users/roles at the database level. AWS equivalent: Lake Formation column masking.

#### 31d. Spanner Graph
A native graph query capability within Spanner (using GQL — Graph Query Language). Query relationships and traverse graph structures directly in Spanner without a separate graph database. AWS equivalent: Neptune (separate service). A 2024 differentiator — no other scalable relational DB offers this natively.

#### 31e. Spanner Dual-Region Configuration
Deploys Spanner across two specific GCP regions with strong consistency. Balances write latency (lower than multi-region) with geographic redundancy. Suitable for customers with data residency requirements within a country.

#### 31f. Spanner Multi-Region Configuration
Deploys Spanner across 3+ regions globally (e.g., nam3 = US East/West + Council Bluffs) with strong consistency. Provides the highest availability (99.999% SLA) and geo-distributed read performance. Higher write latency than single-region (~50–100ms round trip to quorum).

### 32. Cloud SQL
Google's fully managed relational database service for MySQL, PostgreSQL, and SQL Server. AWS equivalent: RDS.

#### 32a. Cloud SQL Auth Proxy
A lightweight proxy binary that establishes encrypted, IAM-authenticated connections to Cloud SQL instances without opening firewall rules or requiring a public IP. AWS equivalent: RDS Proxy (different mechanism — RDS Proxy is connection pooling; Cloud SQL Auth Proxy is secure tunneling). Best practice for connecting applications to Cloud SQL.

#### 32b. Cloud SQL for MySQL
Managed MySQL — versions 5.7 and 8.0. Familiar for LAMP-stack migrations. AWS equivalent: RDS for MySQL.

#### 32c. Cloud SQL for PostgreSQL
Managed PostgreSQL — versions 14, 15, 16. For new workloads, consider AlloyDB if higher performance or vector capabilities are needed. AWS equivalent: RDS for PostgreSQL.

#### 32d. Cloud SQL for SQL Server
Managed SQL Server — Standard and Enterprise editions. AWS equivalent: RDS for SQL Server. Important: licensing is included in the hourly rate.

#### 32e. Cloud SQL Read Replicas
Scale read traffic horizontally. Can be in the same region or a different region (cross-region replica for DR). AWS equivalent: RDS Read Replicas.

### 33. Cloud Storage
GCP's object storage — durable, globally accessible, with multiple storage classes. AWS equivalent: S3.

#### 33a. Cloud Storage Autoclass
Automatically moves objects between storage classes (Standard → Nearline → Coldline → Archive) based on access patterns — no lifecycle rules to write. AWS equivalent: S3 Intelligent-Tiering. Recommend for workloads with unpredictable access patterns.

#### 33b. Cloud Storage Notifications
Sends Pub/Sub events when objects are created, deleted, or updated. Enables event-driven architectures triggered by data arrival. AWS equivalent: S3 Event Notifications → SNS/SQS.

#### 33c. Object Lifecycle Management
Rule-based policies to automatically delete or change the storage class of objects after a specified age or based on conditions. AWS equivalent: S3 Lifecycle Policies.

#### 33d. Object Versioning
Retain multiple versions of the same object. Enables recovery from accidental deletion. AWS equivalent: S3 Object Versioning.

#### 33e. Retention Policies
Lock a bucket so objects cannot be deleted before a minimum retention period — for compliance (SEC 17a-4, FINRA). AWS equivalent: S3 Object Lock.

#### 33f. Signed URLs
Time-limited URLs granting temporary access to private objects — for secure file downloads or uploads from external users. AWS equivalent: S3 Presigned URLs.

#### 33g. Cloud Storage Transfer Service
Managed data transfer service — move data from AWS S3, Azure Blob, HTTP sources, or on-prem to Cloud Storage. AWS equivalent: DataSync, Snow Family. Use for large-scale migrations.

#### 33h. Uniform Bucket-Level Access
Disables ACLs on objects and enforces all access through Cloud IAM only. Simplifies permission management and prevents misconfigured object-level ACLs. AWS equivalent: S3 Block Public Access + bucket policies only.

### 34. Cloud Tasks
A managed service for asynchronous task execution — enqueue tasks to be processed by HTTP workers (Cloud Run, App Engine, Compute Engine). AWS equivalent: SQS (but Cloud Tasks is push-based; SQS is pull-based). Use when you need guaranteed delivery and rate-controlled fan-out to HTTP workers.

### 35. Cloud VPN
Encrypted IPsec tunnels between on-prem networks and GCP VPCs. AWS equivalent: AWS Site-to-Site VPN.

#### 35a. Classic VPN
Single tunnel, no SLA guarantee on availability. Lower cost, suitable for non-critical or dev environments.

#### 35b. HA VPN
Two redundant tunnels with a 99.99% SLA when connected to a compatible on-prem VPN device. Recommended for production workloads. Requires a Cloud Router for dynamic routing (BGP).

### 36. Cloud Workstations
Fully managed, cloud-hosted development environments — browser or IDE-accessible, running on Compute Engine. AWS equivalent: WorkSpaces, Cloud9, or VS Code Dev Containers. Addresses security (code never leaves GCP) and onboarding speed (standardized dev envs).

### 37. Confidential Computing
Encrypts data **in use** (while being processed in memory) using hardware-based Trusted Execution Environments (TEEs) — AMD SEV or Intel TDX. AWS equivalent: AWS Nitro Enclaves. Matters for highly regulated workloads where even cloud provider staff should not be able to inspect running workloads.

#### 37a. Confidential VMs
Compute Engine VMs with AMD SEV (Secure Encrypted Virtualization) or Intel TDX encryption of VM memory. Drop-in for standard VMs — no code changes required. Performance overhead is minimal (under 10%).

#### 37b. Confidential GKE Nodes
GKE node pools where every node is a Confidential VM. Extends in-use encryption to containerized workloads.

#### 37c. Confidential Space
A TEE-based environment where multiple parties can collaborate on data analysis without any party seeing the raw data of others. Use case: joint fraud analysis between competing banks.

### 38. Config Connector
A Kubernetes add-on that lets teams manage GCP resources (Cloud SQL, Pub/Sub, BigQuery, etc.) as Kubernetes custom resources via YAML. AWS equivalent: AWS Controllers for Kubernetes (ACK). Enables GitOps-style infrastructure management alongside application code.

### 39. Contact Center AI (CCAI)
Google's suite of AI capabilities for contact centers — virtual agents (chatbots/IVR), agent assist (real-time suggestions for human agents), and insights (analytics on conversation data). AWS equivalent: Connect + Lex + Contact Lens. Differentiated by Google's Dialogflow NLU and CCAI Insights powered by Vertex AI.

---

## D

### 40. Database Migration Service (DMS)
A managed service to migrate databases to Cloud SQL, AlloyDB, or Spanner with minimal downtime using continuous replication. Supports migrations from MySQL, PostgreSQL, Oracle, and SQL Server. AWS equivalent: AWS DMS.

### 41. Dataflow
GCP's managed Apache Beam service for batch and streaming data processing pipelines. AWS equivalent: Kinesis Data Analytics for streaming, Glue for batch. The key differentiator: a single programming model (Apache Beam) that runs identically for batch and streaming.

#### 41a. Dataflow Flex Templates
Parameterized, containerized Dataflow pipeline templates that non-engineers can launch via UI or API without writing code. AWS equivalent: Glue Job Templates (more limited). Enables self-service pipelines for data teams.

#### 41b. Dataflow Prime
An autoscaling execution engine within Dataflow that automatically right-sizes worker machines and parallelism during a job run. Reduces cost and operational overhead for complex pipelines.

#### 41c. Dataflow Shuffle
A managed, storage-based shuffle service that externalizes the shuffle phase of batch pipelines off workers — reduces disk usage and speeds up large batch jobs significantly.

### 42. Dataform
A managed tool for data transformation in BigQuery — define SQL transformations as a DAG, manage dependencies, test data quality, and version control with Git. AWS equivalent: dbt Core on Redshift. Think of it as managed dbt inside GCP.

### 43. Dataplex
Google's intelligent data fabric for organizing, discovering, governing, and analyzing distributed data across GCP. Manages data in Cloud Storage, BigQuery, and other sources through a unified metadata and policy layer. AWS equivalent: Lake Formation + Glue Data Catalog + Macie.

#### 43a. Dataplex Auto Data Quality
Define and run data quality rules on BigQuery tables or Cloud Storage files, with scoring and alerting. Helps customers build trust in their data products.

#### 43b. Dataplex Data Catalog
The unified metadata repository within Dataplex — search, discover, and document data assets across GCP with business metadata, lineage, and tags. AWS equivalent: AWS Glue Data Catalog.

#### 43c. Dataplex Lakes, Zones, and Assets
The organizational hierarchy: a **Lake** is a logical data domain, **Zones** are sub-areas (raw vs. curated), and **Assets** are the actual data resources (Cloud Storage buckets, BigQuery datasets). Policies applied at the Lake level propagate down.

### 44. Dataproc
Managed Apache Spark and Hadoop service. AWS equivalent: EMR.

#### 44a. Dataproc Metastore
A fully managed Apache Hive metastore service — shared catalog for Dataproc, Dataflow, and BigQuery Omni. AWS equivalent: AWS Glue Data Catalog as a Hive metastore for EMR.

#### 44b. Dataproc on GKE
Run Dataproc Spark jobs as Kubernetes pods on an existing GKE cluster — share cluster infrastructure with other workloads and reduce cost. AWS equivalent: EMR on EKS.

#### 44c. Dataproc Serverless
Run Spark batch jobs without provisioning a cluster — Google provisions and autoscales infrastructure per job, billed per second. AWS equivalent: EMR Serverless. No cluster to manage; ideal for intermittent batch jobs.

### 45. Datastream
A serverless change data capture (CDC) and replication service — streams data changes from MySQL, PostgreSQL, Oracle, and SQL Server into BigQuery, Cloud Storage, or Cloud Spanner. AWS equivalent: DMS with CDC mode + Kinesis. Key pitch: near-real-time replication from operational databases into BigQuery for analytics.

---

## E

### 46. Eventarc
A managed eventing platform that routes events from GCP services, custom applications, and third-party sources to Cloud Run, Cloud Functions, or GKE targets. Uses CloudEvents standard. AWS equivalent: EventBridge. The glue that connects event producers and consumers without custom polling logic.

---

## F

### 47. Filestore
Managed NFS file storage for GCP — workloads that need a shared file system (HPC, CMS, media processing, lift-and-shift apps that require shared storage). AWS equivalent: EFS.

#### 47a. Filestore Basic
Standard NFS performance tiers (HDD-based) — cost-effective for low-IOPS file sharing.

#### 47b. Filestore Enterprise
High-performance, multi-zone NFS with 99.99% SLA and regional availability. For production workloads requiring high availability.

#### 47c. Filestore High Scale
Distributed, parallel NFS for HPC workloads requiring millions of IOPS. AWS equivalent: FSx for Lustre.

### 48. Firebase
Google's mobile and web application development platform — includes a real-time NoSQL database (Realtime Database), authentication, cloud messaging, hosting, and analytics. AWS equivalent: Amplify. Often introduced as a distinct product but runs entirely on GCP infrastructure and integrates with Firestore, Cloud Functions, and App Engine.

#### 48a. Firebase Authentication
Drop-in UI and SDKs for email/password, phone, and federated identity (Google, Apple, Facebook, SAML, OIDC) sign-in. AWS equivalent: Cognito User Pools.

#### 48b. Firebase Realtime Database
A JSON tree-based, real-time synced NoSQL database for mobile/web apps. Older product; Firestore is now preferred for new apps. Low latency sync across clients is the key capability.

#### 48c. Firebase Hosting
Global CDN-backed static hosting with SSL, custom domains, and preview channels. AWS equivalent: Amplify Hosting or S3 + CloudFront.

### 49. Firestore
GCP's serverless, document-oriented NoSQL database — successor to Datastore, designed for real-time web and mobile apps. AWS equivalent: DynamoDB (but with a richer document model and real-time listeners). Scales to millions of concurrent connections.

#### 49a. Firestore Datastore Mode
Backward-compatible with the original Cloud Datastore API. Suitable for server-side apps that previously used Datastore. No real-time listeners in this mode.

#### 49b. Firestore Native Mode
Full Firestore capabilities — real-time listeners, collections/documents hierarchy, rich queries, atomic operations. Recommended for new applications. Not compatible with Datastore API.

---

## G

### 50. Gemini (Google AI models)
Google's family of multimodal large language models — successor to PaLM 2. Available tiers: **Ultra** (most capable), **Pro** (balanced capability/cost), **Flash** (fast, cost-efficient), and **Nano** (on-device). Accessible via Vertex AI. AWS equivalent: Amazon Bedrock (foundation models). The 2026 key differentiator: Gemini's long context windows (up to 1M tokens) and native multimodality (text, code, image, audio, video).

### 51. Gemini for Google Cloud (formerly Duet AI)
An AI assistant embedded in the GCP console, Cloud Shell, and IDEs that helps with coding (code completion, explanation), infrastructure (writing Terraform, debugging deployments), and data (SQL generation in BigQuery). AWS equivalent: Amazon Q Developer. The pitch: AI assistance in every GCP workflow.

### 52. GKE (Google Kubernetes Engine)
Google's managed Kubernetes service — the engine that contributed the most to Kubernetes' creation and standardization. AWS equivalent: EKS. GKE is widely considered the most mature managed Kubernetes offering.

#### 52a. GKE Autopilot
A fully managed GKE mode where Google manages node provisioning, scaling, and security — customers only define pods, not nodes. Billed per pod resource requests (not per node). AWS equivalent: EKS with Fargate, but more integrated. Recommend for teams that want Kubernetes' portability without Kubernetes infrastructure operations.

#### 52b. GKE Standard
The traditional GKE mode where customers manage node pools — full control over machine types, OS, and configurations. AWS equivalent: EKS managed node groups.

#### 52c. GKE Config Connector
See Config Connector entry above.

#### 52d. GKE Node Auto-Provisioning
Automatically creates new node pools with the right machine type when a pod can't be scheduled — not just scaling existing pools. AWS equivalent: Karpenter (third-party) for EKS.

#### 52e. GKE Node Pools
Groups of nodes with identical configuration within a GKE cluster. Enables mixed workloads (e.g., GPU nodes for ML, high-memory nodes for databases, spot nodes for batch). AWS equivalent: EKS managed node groups.

#### 52f. GKE Workload Identity
Binds a Kubernetes service account to a GCP service account, allowing pods to call GCP APIs without storing credentials. AWS equivalent: IAM roles for service accounts (IRSA) on EKS. Security best practice for GKE workloads.

### 53. Google Cloud Marketplace
A catalog of third-party software and services deployable on GCP with consolidated billing. AWS equivalent: AWS Marketplace. Enables customers to purchase and deploy ISV solutions (databases, security tools, ML platforms) with GCP billing.

### 54. Google Distributed Cloud (GDC)
Extends GCP infrastructure to customer-owned hardware in their data center or edge locations. Delivers GCP APIs and managed services (GKE, BigQuery, Pub/Sub, etc.) entirely on-prem. AWS equivalent: Outposts. Addresses data sovereignty and air-gapped requirements. Two variants: **Edge** (smaller footprint) and **Hosted** (full rack, broader service coverage).

### 55. Google Workspace
Google's productivity and collaboration suite (Gmail, Docs, Meet, Drive, etc.) — distinct from GCP but shares identity (Google accounts) and integrates with GCP services. Not strictly a GCP service but frequently comes up in enterprise conversations about identity and data governance.

---

## H

### 56. Healthcare Data Engine
A managed solution that harmonizes and de-identifies health data for analytics and AI workloads. Combines Cloud Healthcare API, Dataflow, and BigQuery. AWS equivalent: AWS HealthLake.

---

## I

### 57. Identity-Aware Proxy (IAP)
A BeyondCorp-based service that gates access to GCP-hosted applications by verifying user identity and context (device, location) before allowing connections — without a VPN. AWS equivalent: Verified Access. The pitch: "VPN-less access to internal apps, controlled by identity."

### 58. Integration Connectors
Pre-built connectors for integrating GCP with enterprise SaaS applications (Salesforce, SAP, ServiceNow, etc.) via Application Integration. Part of GCP's Application Integration suite. AWS equivalent: AppFlow + EventBridge SaaS integrations.

---

## K

### 59. Knative
Open-source Kubernetes framework that Cloud Run is built on — provides serverless workload abstractions (Serving, Eventing) for Kubernetes. Customers won't typically use Knative directly; it's the underlying technology. AWS equivalent: no direct equivalent (Fargate doesn't expose the underlying abstraction layer).

---

## L

### 60. Looker
Google Cloud's enterprise analytics and BI platform. Two distinct products sharing a brand:

#### 60a. Looker (Enterprise BI)
A full-featured, code-first BI platform where data models are defined in LookML (a proprietary modeling language). Acquired by Google in 2020. Designed for embedded analytics and governed, self-service BI at enterprise scale. AWS equivalent: QuickSight (more limited governance model).

#### 60b. Looker Studio (formerly Data Studio)
A free, self-service drag-and-drop dashboarding tool connected to 800+ data sources. No LookML required. AWS equivalent: QuickSight (similar tier). Good for quick dashboards; not a substitute for enterprise-governed BI.

#### 60c. LookML
The data modeling language used in Looker Enterprise — defines metrics, dimensions, and relationships in code, enabling governed, reusable metric definitions. The key differentiator vs. other BI tools: business logic lives in LookML, not in each dashboard.

#### 60d. Looker Blocks
Pre-built LookML models for common data sources (Google Ads, BigQuery ML, Salesforce). Accelerates time-to-insight for common use cases.

---

## M

### 61. Managed Instance Groups (MIGs)
Compute Engine's auto-scaling group of identical VMs managed as a unit — rolling updates, health checks, autoscaling, multi-zone distribution. AWS equivalent: Auto Scaling Groups. Core building block for scalable stateless workloads on Compute Engine.

### 62. Media CDN
Google's edge delivery network optimized for large-scale video streaming and media delivery — built on the same infrastructure as YouTube. AWS equivalent: CloudFront for media. Differentiator: YouTube-scale edge caching specifically tuned for large object, high-bitrate streaming.

### 63. Memorystore
Fully managed in-memory cache. AWS equivalent: ElastiCache.

#### 63a. Memorystore for Redis
Managed Redis — basic and standard tiers, up to 300 GB per instance. Standard tier adds high availability with failover. AWS equivalent: ElastiCache for Redis.

#### 63b. Memorystore for Redis Cluster
Managed Redis Cluster mode — horizontal scaling across shards, supporting multi-TB datasets. AWS equivalent: ElastiCache for Redis with Cluster Mode Enabled.

#### 63c. Memorystore for Valkey
Managed Valkey (the open-source Redis fork after the license change in 2024). For customers who want an open-source-licensed, Redis-compatible cache. AWS equivalent: ElastiCache for Valkey.

### 64. Migration Center
A unified discovery and assessment platform for planning cloud migrations — inventory on-prem VMs, databases, and applications; model TCO and rightsizing recommendations. AWS equivalent: Migration Hub + Application Discovery Service.

### 65. Migrate to Virtual Machines
Google's VM migration service — lifts and shifts on-prem VMs to Compute Engine with minimal downtime using continuous replication. AWS equivalent: MGN (Application Migration Service).

---

## N

### 66. Network Connectivity Center (NCC)
A hub-and-spoke network topology management service — connect VPCs, on-prem networks (via Interconnect, VPN), and SD-WAN appliances through a central hub managed by Google. AWS equivalent: Transit Gateway. Simplifies complex multi-site, multi-VPC routing.

#### 66a. NCC Router Appliances
Third-party virtual network appliances (SD-WAN, firewalls) that can be registered with NCC and participate in BGP route exchange via Cloud Router. AWS equivalent: Transit Gateway Connect.

#### 66b. NCC Spokes
The connection endpoints that attach to an NCC hub — VPC spokes, VPN spokes, Interconnect spokes. Each spoke represents a network segment.

### 67. Network Intelligence Center
A suite of tools for visualizing, monitoring, and troubleshooting GCP network topology and performance. AWS equivalent: Network Manager + Reachability Analyzer.

#### 67a. Connectivity Tests
Simulate and validate network reachability between GCP resources — verify firewall rules, routing, and NAT without sending actual traffic. AWS equivalent: VPC Reachability Analyzer.

#### 67b. Network Topology
Interactive visualization of GCP network resources (VPCs, VMs, load balancers) and their relationships and traffic flows. AWS equivalent: Network Manager topology view.

#### 67c. Performance Dashboard
Latency heatmaps and packet loss metrics between GCP regions and zones. Helps diagnose inter-region performance issues.

---

## O

### 68. Organization
The top-level node in GCP's resource hierarchy — represents a company's entire GCP environment. Contains folders and projects. Policies (IAM, organization policies) applied at the Organization level cascade down. AWS equivalent: AWS Organization root. Required for enterprise governance.

### 69. Organization Policies
Centrally enforced constraints on what actions are allowed across all projects in an organization — e.g., restrict VM images to approved list, prevent creation of external IPs, enforce resource location to specific regions. AWS equivalent: SCPs (Service Control Policies) in AWS Organizations. Governance must-have for enterprise customers.

---

## P

### 70. Persistent Disk
Block storage for Compute Engine VMs. AWS equivalent: EBS. Types: **Standard** (HDD, lowest cost), **Balanced** (SSD, default), **SSD** (high-performance SSD), **Extreme** (highest IOPS SSD). Persistent Disks can be attached to multiple VMs in read-only mode simultaneously.

#### 70a. Hyperdisk
Next-generation block storage for Compute Engine — performance (IOPS and throughput) is provisioned independently of capacity. AWS equivalent: EBS io2 Block Express. Enables right-sized storage cost/performance.

#### 70b. Hyperdisk Throughput
Cost-effective Hyperdisk for throughput-intensive workloads (sequential reads/writes) — analytics, data warehousing. Lower IOPS, high throughput.

#### 70c. Hyperdisk Extreme
Highest-performance Hyperdisk for latency-sensitive OLTP databases. Maximum IOPS, lowest latency.

### 71. Projects
The primary unit of organization, billing, and access control in GCP — all resources belong to a project, and billing is tracked at the project level. AWS equivalent: AWS accounts (roughly). Key difference: multiple projects in a GCP Organization share a single billing account; AWS uses separate accounts per workload.

### 72. Pub/Sub
Google's fully managed, globally distributed message bus — decouples event producers from consumers at scale. AWS equivalent: SNS + SQS combined (Pub/Sub handles both fanout and queue-like consumption). The differentiator: globally replicated, at-least-once delivery, auto-scales to millions of messages/second.

#### 72a. Pub/Sub Lite
A lower-cost, zonal (or regional) Pub/Sub variant with provisioned throughput capacity. AWS equivalent: Kinesis Data Streams. Trades Pub/Sub's automatic global replication and scaling for lower cost — suitable for predictable, high-volume, cost-sensitive streaming.

#### 72b. Pub/Sub BigQuery Subscriptions
Write Pub/Sub messages directly to a BigQuery table without a Dataflow pipeline. Simplifies streaming ingestion for analytics use cases. AWS equivalent: Kinesis Firehose → Redshift (more complex setup).

#### 72c. Pub/Sub Cloud Storage Subscriptions
Write Pub/Sub messages to Cloud Storage as files on a schedule or size threshold. Useful for archival or batch processing of streaming data.

#### 72d. Pub/Sub Push Subscriptions
Pub/Sub delivers messages by making HTTP POST requests to a subscriber's endpoint (Cloud Run, App Engine, any HTTPS endpoint). The subscriber doesn't poll. AWS equivalent: SNS → SQS (SNS pushes, SQS receives).

#### 72e. Pub/Sub Pull Subscriptions
Subscribers explicitly poll Pub/Sub for messages. More control over consumption rate, suitable for worker pools. AWS equivalent: SQS consumers.

#### 72f. Pub/Sub Snapshots
Capture the state of a subscription at a point in time, enabling message replay (seek to snapshot). AWS equivalent: Kinesis extended data retention / SQS message retention (conceptually similar).

---

## R

### 73. Resource Manager
The GCP service for creating and managing the resource hierarchy (Organizations, Folders, Projects) and for applying labels and organization policies. AWS equivalent: AWS Organizations + Resource Groups.

### 74. Risk Manager
A risk assessment tool for GCP environments that evaluates the organization's security posture and provides a risk summary for cyber insurance purposes. No direct AWS equivalent.

---

## S

### 75. Secret Manager
A managed service for storing API keys, passwords, certificates, and other sensitive configuration data. AWS equivalent: Secrets Manager.

#### 75a. Regional Secrets
Store secret versions in a specific GCP region to meet data residency requirements. AWS equivalent: Secrets Manager with region-specific endpoints.

#### 75b. Secret Versions
Each time a secret value changes, a new version is created. Old versions can be kept, disabled, or destroyed. Enables rotation auditing and rollback. AWS equivalent: Secrets Manager secret versions.

### 76. Security Command Center (SCC)
GCP's centralized security management and risk visibility platform — finds misconfigurations, vulnerabilities, threats, and compliance violations across the GCP organization. AWS equivalent: Security Hub.

#### 76a. SCC Attack Path Simulation
Simulates how an attacker could exploit misconfigurations to reach high-value assets. Prioritizes findings by exploitability. AWS equivalent: Inspector attack path analysis (limited).

#### 76b. SCC Event Threat Detection
Detects threats in Cloud Logging and Google Workspace logs using Google's threat intelligence — malware, cryptomining, data exfiltration. AWS equivalent: GuardDuty.

#### 76c. SCC Premium Tier
Adds compliance posture management (PCI DSS, HIPAA, CIS benchmarks), Event Threat Detection, and attack path simulation on top of the standard tier. AWS equivalent: Security Hub with AWS Config rules + GuardDuty.

#### 76d. Security Health Analytics
Continuously scans GCP resource configurations for security misconfigurations (open firewall ports, public Cloud Storage buckets, disabled logging). The core of SCC's posture management. AWS equivalent: AWS Config rules + Security Hub FSBP checks.

#### 76e. SCC Standard Tier
Free tier — basic asset inventory, vulnerability findings for Container Registry, and limited misconfigurations. Recommend upgrading to Premium for any enterprise customer.

#### 76f. Virtual Machine Threat Detection (VMTD)
Detects threats running inside VMs (cryptomining, kernel rootkits) by scanning VM memory from the hypervisor level — without an agent. AWS equivalent: GuardDuty EC2 Runtime Monitoring (agent-based). Agentless is a key differentiator.

### 77. Shared VPC
A GCP networking pattern where a host project owns the VPC and shares subnets with service projects. Centralized network management; each team's project deploys resources into shared subnets. AWS equivalent: AWS Resource Access Manager (RAM) sharing VPC subnets across accounts. Best practice for large organizations to manage networking centrally.

### 78. Spanner — see Cloud Spanner

### 79. Storage Transfer Service — see Cloud Storage Transfer Service

---

## T

### 80. Transfer Appliance
A physical hardware device (up to 1 PB capacity) shipped to the customer to bulk-load data to Cloud Storage offline. AWS equivalent: Snowball Edge. For large migrations where network transfer would take months.

### 81. Terraform on Google Cloud
GCP is one of the most thoroughly supported providers in Terraform. Google publishes and maintains the `google` and `google-beta` Terraform providers, and provides the **Cloud Foundation Toolkit** — opinionated Terraform modules implementing GCP best practices. AWS equivalent: AWS CDK, CloudFormation. Recommend Terraform for multi-cloud customers; recommend Deployment Manager only for GCP-only shops (and even then, Terraform is preferred).

---

## V

### 82. Vertex AI
Google's unified ML and AI platform for building, deploying, and managing ML models and generative AI applications. AWS equivalent: SageMaker + Bedrock combined.

#### 82a. Vertex AI Agent Builder
A platform for building production-ready AI agents — conversational agents (Dialogflow CX-powered), search agents, and custom multi-turn reasoning agents backed by Gemini. AWS equivalent: Amazon Bedrock Agents. Rapid agent development with no ML expertise required.

#### 82b. Vertex AI AutoML
Automatically train models for structured data (tabular), text, images, and video with minimal ML expertise. AWS equivalent: SageMaker Autopilot, Rekognition Custom Labels (image). Recommend for customers with labeled datasets but no ML engineers.

#### 82c. Vertex AI Colab Enterprise
Managed Jupyter notebook environment (Google Colab) with GCP integration — data scientists access BigQuery, Cloud Storage, and Vertex AI resources with native auth. AWS equivalent: SageMaker Studio. No infrastructure to manage; scales notebook environments.

#### 82d. Vertex AI Custom Training
Train custom ML models using any framework (TensorFlow, PyTorch, JAX, scikit-learn) on managed, auto-scaling infrastructure — from a single GPU to thousands. AWS equivalent: SageMaker Training Jobs.

#### 82e. Vertex AI Datasets
Managed data assets that link training data (images, text, tabular, video) to Vertex AI models. Tracks data lineage — which data was used to train which model. AWS equivalent: SageMaker Ground Truth datasets.

#### 82f. Vertex AI Endpoints
Deploy trained models to scalable, managed REST API endpoints. Supports traffic splitting between model versions (blue/green, canary). AWS equivalent: SageMaker Endpoints.

#### 82g. Vertex AI Evaluation
Tools to assess model quality — both offline metrics (precision, recall, BLEU) and LLM-specific metrics (groundedness, coherence, safety). AWS equivalent: SageMaker Clarify + Model Monitor.

#### 82h. Vertex AI Experiments
Track and compare ML experiment runs — hyperparameters, metrics, artifacts. AWS equivalent: SageMaker Experiments.

#### 82i. Vertex AI Feature Store
A managed repository to store, share, and serve ML features online (low-latency serving) and offline (training). AWS equivalent: SageMaker Feature Store.

#### 82j. Gemini on Vertex AI
Access to Google's Gemini models (Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 2.0, etc.) via Vertex AI APIs with enterprise features: VPC Service Controls, customer-managed encryption keys, regional data residency, and usage audit logging. The enterprise-grade alternative to Google AI Studio (developer-focused).

#### 82k. Vertex AI Grounding
Connects Gemini responses to authoritative data sources — Google Search, customer's own data (via RAG Engine or Vertex AI Search). Reduces hallucinations by anchoring LLM output to current, verified information. AWS equivalent: Bedrock Knowledge Bases.

#### 82l. Vertex AI Model Garden
A curated catalog of foundation models (Google's own and third-party — Llama, Mistral, Anthropic Claude, etc.) ready to deploy or fine-tune on Vertex AI. AWS equivalent: Amazon Bedrock model catalog.

#### 82m. Vertex AI Model Monitoring
Detect data drift and skew between training data and production predictions. Alerts when model performance degrades. AWS equivalent: SageMaker Model Monitor.

#### 82n. Vertex AI Model Registry
A central repository to track all trained model versions, their metadata, and deployment status. AWS equivalent: SageMaker Model Registry.

#### 82o. Vertex AI Pipelines
Orchestrate ML workflows as repeatable, auditable DAGs (using Kubeflow Pipelines or TFX). AWS equivalent: SageMaker Pipelines.

#### 82p. Vertex AI RAG Engine
A managed Retrieval-Augmented Generation (RAG) infrastructure — chunk, embed, store, and retrieve documents to ground Gemini responses in customer data. AWS equivalent: Bedrock Knowledge Bases. Enables enterprise knowledge bases, document Q&A, and AI search.

#### 82q. Vertex AI Vector Search
A managed, high-performance approximate nearest neighbor (ANN) vector database — find semantically similar documents, images, or products. AWS equivalent: OpenSearch with k-NN or Aurora pgvector. Differentiator: built on Google's ScaNN technology, claimed to be the fastest ANN search at billion-vector scale.

#### 82r. Vertex AI Workbench
Managed JupyterLab environments for data scientists with deep GCP integration. Two modes: **Managed** (fully serverless) and **Instance** (user-managed VM). AWS equivalent: SageMaker Studio (Managed) and SageMaker Notebook Instances (Instance).

### 83. VPC (Virtual Private Cloud)
GCP's private networking layer for cloud resources. Key difference from AWS: GCP VPCs are **global by default** — a single VPC spans all regions, with subnets scoped to a region. AWS VPCs are region-scoped. This eliminates the need for VPC peering between regions within the same organization.

#### 83a. VPC Firewall Policies
Hierarchical firewall rules applied at Organization or Folder level — cascade down to all VPCs beneath. AWS equivalent: Security Groups + NACLs with AWS Firewall Manager.

#### 83b. VPC Firewall Rules
Per-VPC rules allowing or denying traffic based on IP ranges, tags, or service accounts. GCP uses **network tags** (string labels on VMs) to target firewall rules instead of Security Groups. AWS equivalent: Security Groups.

#### 83c. VPC Flow Logs
Capture metadata about network flows (source/destination IP, port, bytes) for network analysis, forensics, and billing reconciliation. AWS equivalent: VPC Flow Logs.

#### 83d. VPC Packet Mirroring
Clone and mirror traffic from specific VMs or subnets to a collector (IDS, packet capture tool). AWS equivalent: Traffic Mirroring. Used with Cloud IDS for network intrusion detection.

#### 83e. Private Google Access
Allows VMs without external IPs to reach Google APIs and services (BigQuery, Cloud Storage, etc.) through Google's internal network. AWS equivalent: VPC Endpoints with Gateway endpoints (for S3/DynamoDB).

#### 83f. Private Service Connect (PSC)
Enables consumers to access managed services (Google APIs, published services from other GCP tenants) via private internal IP addresses — no public internet traversal. AWS equivalent: PrivateLink. The preferred approach for private access to GCP APIs and ISV services.

#### 83g. Shared VPC — see Shared VPC entry above.

#### 83h. VPC Network Peering
Connect two GCP VPCs for private communication. Unlike AWS, GCP VPC peering is non-transitive — two peered networks cannot route through each other to a third. Use Network Connectivity Center for hub-and-spoke topologies. AWS equivalent: VPC Peering.

#### 83i. VPC Service Controls
A perimeter-based security control that restricts GCP API access to only those requests originating from within a defined perimeter (project, VPC, or IP range) — prevents data exfiltration to unauthorized destinations. AWS equivalent: Resource-based policies + VPC endpoints with endpoint policies. Critical for regulated data (PCI, HIPAA) in GCP.

---

## W

### 84. Workflows
A serverless orchestration service for chaining together GCP services, HTTP-based APIs, and long-running operations into durable workflows. AWS equivalent: Step Functions. Handles retries, error handling, and state across multi-step processes.

---

## Z

### 85. Zone
A single-failure-domain deployment area within a GCP region — roughly equivalent to an AWS Availability Zone. Zones have names like `us-central1-a`, `us-central1-b`. Best practice: deploy critical resources across at least two zones for high availability.

### 86. Zone and Region
GCP organizes infrastructure as:
- **Region**: A geographic area (e.g., `us-central1` in Iowa) containing 3+ zones. AWS equivalent: AWS Region.
- **Zone**: An isolated location within a region. AWS equivalent: Availability Zone.
- **Multi-region**: GCP's concept for services (Cloud Storage, Spanner, BigQuery) that span multiple regions automatically. AWS equivalent: Multi-Region with global replication.

---

*Last updated: 2026. Coverage reflects GCP services generally available as of early 2026.*
