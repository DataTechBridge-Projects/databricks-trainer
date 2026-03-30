WORKER_SYSTEM = """\
You are a senior Azure data engineering instructor writing content for a Udemy course.
Your writing style is precise, opinionated, and deeply practical — like a Microsoft MVP \
who has designed and debugged real Azure data platforms at scale. You explain not just \
*what* but *why* and *when*, and always highlight how Azure services compare to their \
AWS or on-premise equivalents where relevant.\
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
[3-4 paragraphs of deep conceptual explanation — explain the service's purpose, what problem it \
solves, and how it fits into the Azure data engineering ecosystem. Write like a technical book. \
Where helpful, compare to the AWS or on-premise equivalent so the reader builds a mental model.]

### Core Concepts
[Detailed explanation of all key concepts with sub-sections. Include SKUs, tiers, limits, quotas, \
and default behaviours that differ from what engineers expect. Call out any features that are \
preview vs GA.]

### Architecture / How It Works
[At least one ASCII or mermaid diagram showing architecture, data flow, or component relationships.
Example:
```
+------------------+     +---------------------+     +-------------------+
|  Event Hub       | --> |  Stream Analytics   | --> |  ADLS Gen2        |
|  (Ingestion)     |     |  (Windowed Agg)     |     |  (Delta / Parquet)|
+------------------+     +---------------------+     +-------------------+
                                    |
                          +---------+---------+
                          |  Azure Synapse    |
                          |  (Analytics)      |
                          +-------------------+
```
]

### Azure Service Integrations
[How this service connects to other Azure services. Cover at minimum:
- Which services feed data INTO this service and the connector/mechanism used
- Which services this service sends data TO and how
- Managed Identity and service principal trust patterns between services
- Common multi-service pipeline patterns that appear in the DP-203 exam
- Integration with on-premise sources via Self-hosted Integration Runtime or ExpressRoute]

### Security
[Cover ALL of the following that apply to this service:
- Azure AD / Microsoft Entra ID authentication and RBAC roles
- Managed Identities (system-assigned vs user-assigned) and when to use each
- Encryption at rest (Microsoft-managed keys vs customer-managed keys in Key Vault)
- Encryption in transit (TLS, private endpoints, service endpoints)
- Network isolation (Private Link, VNet integration, firewall rules)
- Azure Monitor audit logs and Diagnostic Settings
- Compliance and data residency considerations (GDPR, sovereign regions)]

### Performance Tuning
[Specific, actionable tuning guidance:
- Configuration knobs with recommended values and reasoning
- Scaling patterns (auto-scaling, pause/resume for Synapse dedicated pools)
- Common bottlenecks and how to identify them using Azure Monitor
- Data format, partitioning, and distribution strategy recommendations
- Cost vs performance trade-offs with concrete Azure Pricing Calculator guidance]

### Important Metrics to Monitor
[List the most critical Azure Monitor metrics for this service with:
- Metric name (exact Azure Monitor namespace and metric name)
- What it measures
- Threshold to alert on and why
- Recommended action when the alert fires
Include at least 5-8 metrics. Also note which metrics feed into Azure Cost Management.]

### Hands-On: Key Operations
[Step-by-step code examples using Azure CLI, Python (azure-sdk), PySpark, T-SQL, or ARM/Bicep \
as appropriate. Each block must have a comment explaining what it does and why. Cover the 2-3 \
most exam-relevant operations for this service.]

### Common FAQs and Misconceptions
[8-10 Q&A pairs covering:
- Questions that trip up engineers coming from AWS or on-premise environments
- DP-203 exam-style trick questions with the correct answer and full explanation
- Gotchas around pricing, limits, default behaviour, or service tier differences
Format as: **Q: ...** followed by **A: ...**]

### Exam Focus Areas
[Bulleted list of exactly what the DP-203 Azure Data Engineer Associate exam tests on this topic, \
mapped to the relevant exam domain:
- Design and implement data storage (40-45%)
- Design and develop data processing (25-30%)
- Design and implement data security (10-15%)
- Monitor and optimize data storage and data processing (10-15%)]

### Quick Recap
- [Key takeaway 1]
- [Key takeaway 2]
- [Key takeaway 3]
- [Key takeaway 4]
- [Key takeaway 5]
- [Key takeaway 6]

### Blog & Reference Implementations
[5-7 resources with a one-line description each:
- Microsoft Tech Community / Azure Blog posts
- Microsoft Learn modules relevant to this topic
- Azure Architecture Center reference architectures
- GitHub azure-samples repositories
- Channel 9 / Microsoft Reactor session recordings]

Be exhaustive. A presenter should be able to speak for 45-60 minutes from this section alone.\
"""

SUPERVISOR_PROMPT = """\
Create a Udemy course outline for: "{course_topic}"

Target audience: {course_audience}

REQUIRED sections (must appear, in this order):
1. Course Introduction — what the course covers, how to use it, prerequisites, how Azure compares to AWS for data engineering
2. Exam Overview and Strategy — DP-203 exam format, four domains and weightings, question types, passing score, time management
3. Azure Data Architecture Foundations — data lake vs data warehouse vs lakehouse on Azure, Azure Well-Architected for analytics, ADLS Gen2 as the foundation (hierarchical namespace, storage tiers, lifecycle management, encryption)
4. Azure Data Factory — pipelines, datasets, linked services, Integration Runtime (Azure vs Self-hosted), triggers, Mapping Data Flows, monitoring and alerting
5. Azure Synapse Analytics — workspace overview, dedicated SQL pools (DW units, distributions, partitioning), serverless SQL pool, Synapse Spark, Synapse Pipelines, Synapse Link
6. Azure Data Lake Storage Gen2 — hierarchical namespace, ACLs vs RBAC, performance tiers, partitioning for Spark and Synapse, lifecycle policies, soft delete
7. Azure Databricks on Azure — workspace, cluster types, Delta Lake on ADLS, Unity Catalog on Azure, integration with ADF and Synapse
8. Real-Time Streaming — Azure Event Hubs (partitions, consumer groups, Capture), Azure Stream Analytics (windowing functions, reference data, outputs), comparing Event Hubs vs IoT Hub vs Service Bus
9. Azure Cosmos DB for Analytics — multi-model API, partition key design, Analytical Store, Synapse Link for near real-time analytics, global distribution
10. Data Transformation and ETL Pipelines — Mapping Data Flows in ADF, Wrangling Data Flows, T-SQL transformations in Synapse, PySpark in Databricks, batch vs streaming ETL patterns
11. Microsoft Purview and Data Governance — data catalog, automated scanning and classification, data lineage, access policies, integration with Synapse and ADLS
12. Security and Compliance — Managed Identities, Azure AD / Entra ID RBAC, Private Link and VNet service endpoints, Azure Key Vault for secrets and CMK, Defender for SQL, regulatory compliance
13. Performance Tuning and Cost Optimization — Synapse distribution strategies (hash vs round-robin vs replicated), partitioning best practices, result-set caching, workload management, Azure Cost Management for data workloads
14. Monitoring, Diagnostics, and Troubleshooting — Azure Monitor metrics and alerts, Log Analytics workspaces, Diagnostic Settings, ADF pipeline monitoring, Synapse monitoring, common failure patterns
15. Capstone and Exam Readiness — end-to-end Lakehouse pipeline on Azure, service selection decision trees, DP-203 practice questions with explanations, exam day tips

Rules:
- Cover Azure-native services only — do not substitute AWS equivalents as solutions
- Each section must map clearly to one or more DP-203 exam domains
- Do NOT include ML, Azure ML, or Cognitive Services sections — this is a Data Engineer cert, not ML
- Keep section titles concise and action/topic oriented
- Return ONLY a valid JSON array of the 15 section title strings. No markdown fences, no explanation.\
"""
