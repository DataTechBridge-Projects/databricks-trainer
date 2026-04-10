# Building Declarable Pipelines with Delta Live Tables (DLT) — SA Quick Reference

## What It Is
DLT is a managed framework that lets engineers define *what* data should look like rather than writing complex code for *how* to move it. It automates the "plumbing"—like infrastructure, task scheduling, and error handling—so teams can focus on delivering business logic.

## Why Customers Care
- **Reduced Operational Overhead:** Eliminates manual work for managing clusters, checkpoints, and complex task dependencies.
- **Built-in Data Quality:** Automatically catches, drops, or flags bad data using "Expectations" to prevent downstream reporting errors.
- **Faster Time-to-Market:** Accelerates the development of Medallion architectures (Bronze/Silver/Gold) by automating the orchestration layer.

## Key Differentiators vs Alternatives
- **Declarative vs. Imperative:** Unlike Spark or Glue, you define the end state, and DLT manages the underlying DAG, retries, and state.
- **Integrated Data Quality:** Unlike standard ETL, quality constraints are baked directly into the pipeline code, not added as an afterthought.
- **Lower TCO:** Reduces "Data Engineering Debt" by automating the maintenance of complex, multi-step pipelines.

## When to Recommend It
Recommend DLT to organizations moving from "ad-hoc" data processing to a structured Medallion architecture. It is ideal for customers experiencing high operational costs from maintaining complex Airflow/Step Functions DAGs or those struggling with "brittle" pipelines that break frequently due to schema changes or bad data.

## Top 3 Objections & Responses
**"Won't this increase our costs by managing the infrastructure for us?"**
→ While there is a management premium, the TCO is lower because you are trading expensive engineering hours spent on "plumbing" for automated, efficient compute.

**"We already have Airflow/Step Functions for orchestration; why do we need DLT?"**
→ DLT replaces the need to orchestrate individual Spark tasks; it manages the dependencies and lineage within the pipeline itself, reducing the complexity of your external orchestrator.

**"If we use 'Fail Update' for quality, won't our pipelines be constantly breaking?"**
→ The key is a strategic use of Expectations: use `DROP ROW` for minor drift to maintain availability, and reserve `FAIL UPDATE` only for critical business logic errors that would invalidate downstream reports.

## 5 Things to Know Before the Call
1. **The Medallion Native:** DLT is purpose-built to automate the Bronze $\to$ Silver $\to$ Gold flow.
2. **Streaming vs. Live:** Use *Streaming Live Tables* for low-latency, incremental updates; use *Live Tables* (materialized views) for complex aggregations.
3. **Expectations are the "Secret Sauce":** They allow for automated data cleansing (dropping rows) or quarantining without manual intervention.
4. **Auto Loader Integration:** DLT works best with Auto Loader for efficient, scalable file ingestion from S3/Cloud Storage.
5. **Avoid "Fail Update" Overuse:** Over-using strict constraints can lead to pipeline downtime; strategy is key to maintaining data freshness.

## Competitive Snapshot
| vs | Advantage |
|---|---|
| **Standard Spark / Notebooks** | Automates orchestration, lineage, and infrastructure management. |
| **AWS Glue / Manual ETL** | Shifts from "writing plumbing" to "architecting data flows." |
| **Airflow / Step Functions** | Replaces manual task-dependency management with a single, unified DAG. |

---
*Source: Building Declarable Pipelines with Delta Live Tables (DLT) course section*