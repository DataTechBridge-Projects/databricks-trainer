# Migration Strategies: Transitioning from AWS Glue to Databricks — SA Quick Reference

## What It Is
A strategic shift from using AWS Glue as a standalone ETL engine to using Databricks as a unified Lakehouse platform. You aren't moving your data out of S3; you are upgrading the "brain" that manages, governs, and processes that data.

## Why Customers Care
- **Increased Engineering Velocity:** Move from manual, fragmented ETL jobs to automated, declarative pipelines like Delta Live Tables.
- **Unified Governance:** Replace the fragmented Glue Data Catalog with Unity Catalog for centralized access control and lineage across SQL and ML.
- **Reduced Metadata Latency:** Eliminate slow, expensive Glue Crawlers in favor of Auto Loader’s real-time, file-notification-based ingestion.

## Key Differentiators vs Alternatives
- **Beyond Simple ETL:** Unlike Glue, which is a "black box" compute engine, Databricks provides a collaborative workspace where Data Engineers and Data Scientists work on the same compute.
- **Elimination of "The Glue Wall":** Databricks solves the debugging and dependency management friction that occurs when Glue clusters become too complex to manage.
- **Operational Efficiency:** Replaces manual schema inference (Crawlers) with cloud-native, automated ingestion (Auto Loader) that scales without manual intervention.

## When to Recommend It
Target customers experiencing "The Glue Wall"—enterprises where data complexity has outpaced their ability to manage Glue Crawlers and fragmented catalogs. Look for signals like high engineering friction, a need to move from batch to real-time streaming, or teams struggling to govern data for both BI and Machine Learning.

## Top 3 Objections & Responses
**"We don't want to move our data; it's too much volume/risk."**
→ You aren't moving the data. Your S3 bucket remains your single source of truth; we are simply upgrading the compute logic and governance layer sitting on top of it.

**"Moving our PySpark scripts will be a massive, expensive engineering effort."**
→ We recommend a phased approach. Start with "Re-platforming" to modernize orchestration, and only "Refactor" your most mission-critical pipelines to maximize ROI.

**"Why change if our Glue jobs are working fine right now?"**
→ Glue is great for simple batching, but it creates technical debt as you scale. Moving to Databricks allows you to transition from reactive maintenance to proactive innovation with Auto Loader and Delta Live Tables.

## 5 Things to Know Before the Call
1. **Data stays put:** The migration is about moving *logic and governance*, not moving S3 objects.
2. **The `glueContext` Trap:** A pure "Lift-and-Shift" will fail if scripts rely on AWS-specific libraries; they must be stripped of Glue wrappers.
3. **Crawlers are an anti-pattern:** Don't try to replicate Glue Crawlers in Databricks; pitch Auto Loader instead.
4. **Metadata is the priority:** A successful migration means moving table definitions from the Glue Catalog to Unity Catalog.
5. **Focus on Velocity, not just Cost:** The primary driver for migration is usually higher engineering speed, not just lower compute spend.

## Competitive Snapshot
| vs | Advantage |
|---|---|
| **AWS Glue** | Provides a unified collaborative environment (SQL + ML) instead of just isolated ETL tasks. |
| **Legacy On-Prem ETL** | Enables cloud-native, serverless scaling and automated schema discovery without manual management. |

---
*Source: Migration Strategies: Transitioning from AWS Glue to Databricks course section*