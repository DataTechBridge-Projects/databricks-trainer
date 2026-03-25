# Unity Catalog & Governance  

*Section 10 of 15 – AWS Databricks Data Engineer Certification*  

> **Goal of this section** – Give you a complete mental model of Unity Catalog (UC) and the governance primitives that sit on top of it, show how they map to AWS services, and walk you through the exact operations you’ll be asked to perform on the exam. By the end you should be able to design a secure, multi‑tenant data platform, explain the data‑access flow, and write the few lines of code that a data engineer would use in production.

---  

## Overview  

Unity Catalog (UC) is Databricks’ unified, cross‑workspace data catalog that replaces the older Hive metastore. It provides **centralized metadata, fine‑grained access control, data masking, row‑level security (RLS), and lineage** for all data assets—tables, views, functions, and ML models—regardless of whether those assets live in Delta Lake on S3, external Glue tables, or Azure/Google clouds.  

In the AWS context, UC is tightly coupled with **S3** for storage, **IAM** for identity, **AWS Glue** for crawlers and schema inference, and **Lake Formation** for additional fine‑grained column‑level permissions (when enabled). The UC metastore stores its own JSON‑backed catalog in S3, replicated across regions, and is itself version‑controlled via **Databricks Repos** or external Git.  

A governance layer built on top of UC consists of three pillars:  

1. **Catalog‑Schema‑Table hierarchy** – You create *catalogs* (top‑level containers), *schemas* (namespaces), and *tables* (the actual data). This hierarchy mirrors AWS’s Organizational Units → Accounts → Resources but is expressed in SQL/Databricks UI.  
2. **Privilege model** – UC implements **SQL‑standard GRANT/REVOKE** for *SELECT, INSERT, UPDATE, DELETE, ALTER, USAGE, etc.* at catalog, schema, and table levels, plus **data‑masking policies** and **row‑level security policies** that can reference UDFs or AWS Secrets Manager.  
3. **Auditing & lineage** – Every access attempt is emitted to **CloudTrail** (via the Databricks service‑linked role) and to **Databricks Unity Catalog audit logs**. UC also captures table and query lineage that can be visualized in the UI or exported to AWS Athena for further analysis.  

Together, these capabilities let a data engineer enforce **multi‑tenant isolation**, **data classification**, and **compliance (GDPR, HIPAA)** while still giving data scientists a seamless Spark API to read/write data using the familiar `spark.read.table("catalog.schema.table")` pattern.

---

## Core Concepts  

Below are the building blocks you need to master. Each concept includes practical notes that map directly to exam‑style questions.

### 1️⃣ Catalogs, Schemas, and Tables  

| Level | Purpose | Typical AWS Mapping |
|-------|---------|---------------------|
| **Catalog** | Logical container for a business domain or regulatory scope (e.g., `finance`, `marketing`). Holds schemas and tables. | Equivalent to an AWS Organizational Unit (OU) or an AWS account. |
| **Schema** | Namespace within a catalog (e.g., `raw`, `curated`, `analytics`). Can hold versioned tables. | Similar to a Glue Database or a Lake Formation data lake zone. |
| **Table / View** | Physical Delta table (`USING DELTA`) or external view (e.g., a Hive table, a Glue table). | Stored as Delta Lake files in a specific S3 prefix, e.g., `s3://my-bucket/curated/events/`. |

*Key Exam Fact:* The exam often asks you to **choose the minimal set of UC objects** that can satisfy a given security requirement (e.g., “grant read‑only to a subset of columns”). Knowing that you must create a **catalog** *only* if you need to isolate data across business units, and **schemas** for domain‑level segregation, will save you time.

### 2️⃣ Privileges and Permission Types  

| Privilege | Scope | Example Use |
|-----------|-------|-------------|
| `USAGE` | Catalog → Allows navigating down to schemas. | `GRANT USAGE ON CATALOG finance TO data_engineer;` |
| `SELECT` | Table / View → Reads data. | `GRANT SELECT ON TABLE finance.events TO analyst;` |
| `INSERT` / `DELETE` | Table → Write operations. | `GRANT INSERT, DELETE ON TABLE finance.events TO ingestion_pipeline;` |
| `ALTER` | Table → Change schema (add columns, rename). | `GRANT ALTER ON TABLE finance.events TO admin;` |
| `CREATE` | Catalog / Schema → Ability to create sub‑objects. | `GRANT CREATE ON CATALOG finance TO data_engineer;` |

*Data Masking*: A **masking policy** can be attached to a column (e.g., SSN). The policy evaluates at query time and replaces sensitive values with a placeholder (`xxxx-xx-`).  

*Row‑Level Security*: Defined via a **RLS policy** that references a Spark UDF or a SQL function returning a boolean. Example: `SELECT * FROM finance.events WHERE region = current_user_region();`

### 3️⃣ Integration with AWS Glue & Lake Formation  

* **Glue Crawlers → UC**: When you run a Glue crawler against an S3 prefix that is *already* registered as a UC location, the crawler will *not* overwrite the metastore; it will instead **log warnings** and you can manually sync the metadata.  

* **Lake Formation**: If you enable *Lake Formation permissions* on a UC location, any table registered in UC inherits the **column‑level LF permissions**. The benefit is you can use LF’s *grant* API to define column permissions for external tables, and UC will enforce those when the table is accessed through Spark.  

* **IAM → Databricks Service‑Linked Role**: UC uses a service‑linked role (`databricks-unity-catalog`) that must have `s3:ListBucket`, `s3:GetObject`, and `glue:*` permissions on the S3 locations that store the catalog metadata. The exam may ask you to **list the minimal IAM policies** required for a UC metastore in a given VPC.

### 4️⃣ Auditing, Lineage, and Data Quality  

* **Audit Logs** – Sent to CloudTrail (event name `databricks.unityCatalog.*`). You can route them to a dedicated S3 bucket for long‑term retention and then run Athena queries to surface who accessed what.  

* **Lineage** – UC captures both **upstream** (source tables → downstream views) and **downstream** (queries that read a table). The lineage UI can be queried via `SELECT * FROM system.lineage WHERE table = 'finance.events';`.  

* **Data Quality Checks** – UC does **not** enforce schema evolution; you still need Delta’s `MERGE` and `CHECK CONSTRAINTS`. However, you can attach a **constraint** (`CREATE CONSTRAINT my_event_not_null ON finance.events (event_id) IS NOT NULL`) that will be enforced during writes.

---  

## Architecture / How It Works  

Below is a logical flow that illustrates where Unity Catalog lives relative to the rest of the AWS data platform.  

```mermaid
flowchart TD
    subgraph AWS[ AWS Account ]
        S3[ S3 Buckets<br/>raw/ & curated/ ]
        GLUE[ AWS Glue<br/>Crawler & Table Registry ]
        LF[ Lake Formation<br/>Data Permissions ]
        CT[ CloudTrail<br/>Audit Logs ]
    end

    subgraph Databricks[ Databricks Workspace ]
        UC[ Unity Catalog<br/>Metastore (S3 backed) ]
        CL[ Cluster (Spark) ]
        UI[ UI / Jobs / Repos ]
    end

    S3 -->|raw files| GLUE
    GLUE -->|crawls| UC
    LF -->|column/row LF grants| UC
    UC -->|metadata store| S3
    CL -->|spark.sql| UC
    CL -->|read/write Delta| S3
    UI -->|catalog operations| UC
    UC -->|audit events| CT

    classDef aws fill:#FFEECC,stroke:#333,stroke-width:1px;
    classDef dc fill:#CCE5FF,stroke:#333,stroke-width:1px;
    class S3,GLUE,LF,CT aws;
    class UC,CL,UI dc;
```

**Explanation of the diagram**

1. **Raw data lands in S3** → a Glue crawler discovers the schema. The crawler writes its metadata to UC (instead of the Glue Data Catalog).  
2. **Lake Formation policies** are attached to the UC location (e.g., `s3://my-bucket/curated/`). When a user runs a query, Databricks checks both the **UC privilege** and any **Lake Formation column masks**.  
3. **Clusters** talk to UC via the **HiveThriftCatalog** (the SQL layer). All read/write commands are translated into **Delta Lake** transactions that land in the S3 bucket.  
4. Every permission check and query is streamed to **CloudTrail** where the **Databricks service‑linked role** posts audit events. This creates an immutable trail for compliance.  

---  

## Hands‑On: Key Operations  

Below are the exact code snippets you would type in a Databricks notebook or a job to **create a catalog, grant permissions, and enforce masking/RLS**. Each block is accompanied by a brief “what’s happening” note.

> **Tip for the exam** – Most questions present a *scenario* and ask you to pick the *fewest* statements that accomplish the goal. Memorize the pattern: **`CREATE CATALOG …` → `CREATE SCHEMA …` → `CREATE TABLE …` → `GRANT SELECT …`** plus **masking / RLS** if required.

### 1️⃣ Create a Catalog, Schema, and External Table  

```python
# 1️⃣ Catalog
spark.sql("""
CREATE CATALOG IF NOT EXISTS finance
COMMENT 'Business unit for financial transactions';
""")

# 2️⃣ Schema inside the catalog
spark.sql("""
CREATE SCHEMA IF NOT EXISTS finance.raw
COMMENT 'Raw ingest tables (Parquet)';
""")

# 3️⃣ External table that points to a Glue‑registered location
spark.sql("""
CREATE DATABASE IF NOT EXISTS glue_db
""")  # This is just to reference a Glue table

spark.sql("""
CREATE TABLE IF NOT EXISTS finance.raw.events
USING PARQUET
LOCATION 's3://my-data-lake/raw/events/'
COMMENT 'Raw events as they land in S3';
""")

# Verify
spark.sql("DESCRIBE DETAIL finance.raw.events").show(truncate=False)
```

> **Why it matters** – The `LOCATION` is *catalog‑aware*. Even though the files live in S3, the table definition lives in UC, giving you immediate access‑control options.

### 2️⃣ Grant Privileges  

```sql
-- Grant read‑only to the analyst role
GRANT SELECT ON CATALOG finance TO `analyst_role`;

-- Allow the ingestion pipeline to write to the raw layer
GRANT INSERT, DELETE ON TABLE finance.raw.events TO `pipeline_role`;

-- Enable USAGE on the schema for the analyst
GRANT USAGE ON SCHEMA finance.raw TO `analyst_role`;
```

> **Exam note:** When a role needs *both* read and write on a table, you must also `GRANT USAGE` on the parent catalog and schema, otherwise the `SELECT` will be denied silently.

### 3️⃣ Attach a Data‑Masking Policy (SSN example)  

```sql
-- 1️⃣ Create a masking policy
CREATE MASKING POLICY IF NOT EXISTS finance.mask_ssn
  USING 'SELECT CASE WHEN is_current_user(''admin'') THEN ssn
           ELSE CONCAT(''xxx-xx-'', right(ssn,4))
       END' 
  COMMENT 'Masks SSN for non‑admin users';

-- 2️⃣ Apply it to the column
ALTER TABLE finance.raw.events
ALTER COLUMN ssn SET MASKING POLICY finance.mask_ssn;
```

Now a user without the `admin` role sees `xxx-xx-1234` instead of the real SSN.

### 4️⃣ Row‑Level Security (RLS) – Regional Isolation  

```sql
-- 1️⃣ UDF that returns the current user's allowed region
CREATE OR REPLACE TEMPORARY FUNCTION current_user_region() RETURNS STRING
  USING `com.mycompany.udfs.CurrentUserRegion`;

-- 2️⃣ RLS policy (referencing the UDF)
CREATE ROW FILTER ON finance.curated.events
  USING (current_user_region() = region);

-- 3️⃣ Grant to a role that already has SELECT
GRANT SELECT ON finance.curated.events TO `data_scientist`;
```

The RLS filter guarantees each user can only see rows whose `region` column matches the region resolved by the UDF (often derived from the user’s IAM principal via `CURRENT_USER()`).

### 5️⃣ Auditing a Query (via SQL)  

```sql
-- Run a query and then view the audit log via the Unity Catalog audit view
%sql
SELECT region, count(*) as events
FROM finance.curated.events
WHERE event_date = current_date()
GROUP BY region;

-- In a separate notebook (or via Athena) read the audit log:
spark.sql("""
SELECT *
FROM system.access_history
WHERE query_text like '%events%'
ORDER BY event_time DESC
LIMIT 10;
""")
```

---  

## AWS‑Specific Considerations  

| AWS Service | How it Touches Unity Catalog | Practical Tips for the Exam |
|-------------|-----------------------------|------------------------------|
| **S3** | UC stores its metastore JSON in a dedicated bucket (`s3://<account-id>-uc-meta/`). All Delta tables also read/write from S3. | Ensure the **Databricks service‑linked role** (`databricks-unity-catalog`) has `s3:GetObject` on the *catalog bucket* and *all data buckets* used by your tables. The role **cannot** have `s3:*` on the entire account – the exam may ask for the *least‑privilege* policy. |
| **IAM** | IAM users/groups are mapped to UC **roles** via the `GRANT` statements (e.g., `GRANT SELECT ON ... TO `john.doe``). The Databricks UI translates the `john.doe` string to a **Databricks identity** that ultimately resolves to an **IAM principal** via the service‑linked role. | Remember: **Cross‑account** UC works by setting up a *trust relationship* between the Databricks workspace in Account A and the S3 bucket in Account B. You need to attach the `databricks-unity-catalog` role to both accounts. |
| **AWS Glue** | Glue crawlers can **populate** UC if you run `CREATE EXTERNAL TABLE` that points to a Glue Data Catalog location. However, UC metadata is the **single source of truth**; any changes made in Glue (e.g., adding a new column) must be **propagated** manually via `ALTER TABLE`. | For the exam, you may be asked: “A new column is added to a Glue table. What steps are required for the table to be queryable through UC?” – Answer: **`REFRESH TABLE <catalog.schema.table>`** and optionally **`ALTER TABLE ... ADD COLUMNS …`** in UC. |
| **Lake Formation** | When you **grant LF permissions** to a UC location, those permissions are *enforced* on top of UC’s own privileges. LF column‑level grants are stored in the **Data Catalog** of Lake Formation, not UC. | The exam may present a scenario where a user can read a table but cannot see a specific column. You’ll need to state: **Grant LF column‑level SELECT** *and* verify that the user has the **table SELECT** in UC. |
| **EMR** | EMR clusters can mount a UC catalog via the **Spark `spark.databricks.unityCatalog.jdbc.enabled`** config. EMR also supports **IAM roles for EC2** that grant access to the UC metastore bucket. | If you’re building a **Hybrid** solution (Databricks on a VPC, EMR for batch), you’ll need **VPC endpoints** for `s3` and `sts` so the EMR cluster can fetch the UC metadata without leaving the network. |
| **CloudWatch / CloudTrail** | UC logs each `GRANT`/`REVOKE` and every `SELECT` attempt to CloudTrail.