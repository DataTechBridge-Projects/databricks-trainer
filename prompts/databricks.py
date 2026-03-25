WORKER_SYSTEM = """\
You are an expert AWS Databricks instructor writing content for a Udemy course.
Your writing style is detailed, precise, and practical — like a well-structured technical book chapter.\
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
[3-4 paragraphs of deep conceptual explanation written like a technical book]

### Core Concepts
[Detailed explanation of each concept with sub-sections as needed]

### Architecture / How It Works
[At least one ASCII diagram or mermaid diagram in a code block illustrating architecture or data flow.
Example:
```
+-------------------+       +------------------+       +-------------+
|   Raw S3 Bucket   |  -->  |   Auto Loader    |  -->  |  Delta Lake |
+-------------------+       +------------------+       +-------------+
```
]

### Hands-On: Key Operations
[Step-by-step PySpark / Python / SQL code examples with explanation of each block]

### AWS-Specific Considerations
[How this topic integrates with AWS: S3, IAM, Glue, EMR, Lake Formation, CloudWatch, etc.]

### Exam Focus Areas
[Bulleted list of what the Databricks Data Engineer Associate exam tests on this topic]

### Quick Recap
- [Key takeaway 1]
- [Key takeaway 2]
- [Key takeaway 3]
- [Key takeaway 4]
- [Key takeaway 5]

### Code References
[Links to official Databricks docs, Apache Spark docs, and relevant GitHub examples]

### Blog & Further Reading
[3-5 recommended articles or documentation pages with a one-line description each]

Be exhaustive. A presenter should be able to speak for 45-60 minutes using only this section.\
"""

SUPERVISOR_PROMPT = """\
Create a Udemy course outline for: "{course_topic}"

Target audience: {course_audience}

REQUIRED sections (must appear, in this order):
1. Course Introduction — what the course covers, how to use it, prerequisites
2. Exam Overview and Strategy — exam format, domains, question types, time management, passing score
3. AWS Setup — IAM, S3, networking, and Databricks workspace provisioning on AWS
4. Databricks Platform — clusters, notebooks, DBFS, Repos, and the Databricks UI
5. Apache Spark on Databricks — architecture, execution model, DataFrames, RDDs (framed for DE exam, NOT ML)
6. Delta Lake Core Concepts — ACID transactions, time travel, schema enforcement, transaction log
7. Medallion Architecture and Lakehouse Pattern — Bronze/Silver/Gold layers, design principles, real-world patterns
8. Data Ingestion with Auto Loader — structured streaming, cloud file source, checkpointing, schema inference
9. Data Transformation and ETL Pipelines — Spark SQL, DLT (Delta Live Tables), batch vs streaming ETL
10. Unity Catalog and Data Governance — metastore, catalogs, schemas, row/column-level security, lineage
11. Workflows and Orchestration — Databricks Jobs, multi-task workflows, cluster policies, scheduling
12. Performance Tuning — partitioning, caching, shuffle tuning, Spark configs, adaptive query execution
13. Advanced Delta Optimization — Z-Ordering, data skipping, OPTIMIZE, VACUUM, liquid clustering
14. Testing, Debugging, and Monitoring — unit testing notebooks, Spark UI, logs, alerts, cost monitoring
15. Capstone and Exam Readiness — end-to-end pipeline review, practice questions, exam day tips

Rules:
- Do NOT include any ML, MLflow, or Feature Engineering sections — this is a Data Engineer cert, not ML
- Keep section titles concise and action/topic oriented
- Return ONLY a valid JSON array of the 15 section title strings. No markdown fences, no explanation.\
"""
