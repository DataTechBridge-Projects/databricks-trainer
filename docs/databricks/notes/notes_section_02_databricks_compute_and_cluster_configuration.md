# Databricks Compute and Cluster Configuration — SA Quick Reference

## What It Is
Databricks compute is the scalable "engine" used to process and analyze data. It allows you to separate your permanent data storage from the temporary processing power needed to run queries and pipelines.

## Why Customers Care
- **Cost Control:** Eliminate "cloud sprawl" by automatically shutting down idle resources and using low-cost spot instances.
- **Operational Efficiency:** Shift your team from managing servers to orchestrating data workloads.
- **Performance Optimization:** Right-size your engine—using high-power clusters for heavy ETL and lightweight, instant-start warehouses for BI.

## Key Differentiators vs Alternatives
- **Decoupled Architecture:** Compute is transient and scales independently of your data, ensuring you never pay for idle storage capacity.
- **Automated Orchestration:** Native autoscaling and serverless options remove the manual burden of provisioning and managing VM instances.
- **Tiered Pricing Models:** Distinct cluster types (Job vs. All-Purpose) allow you to run production workloads at roughly 50% less cost than interactive ones.

## When to Recommend It
Recommend Databricks compute to organizations migrating from legacy Hadoop or AWS Glue who are struggling with "cloud sprawl" and unpredictable monthly bills. It is ideal for customers moving from manual infrastructure management to a modern, automated data estate where they need to support diverse personas—from Data Engineers running production pipelines to SQL Analysts running BI dashboards.

## Top 3 Objections & Responses
**"Won't managing different cluster types increase our operational overhead?"**
→ Actually, it reduces it; by using Serverless SQL and Job clusters, you automate the lifecycle management and scaling, letting your team focus on data, not servers.

**"Are Spot instances too risky for our production workloads?"**
→ Not if configured correctly; we recommend using Spot instances for Worker nodes to capture up to 90% savings, while keeping the Driver node on On-Demand to ensure job stability.

**"We are already using AWS Glue; why change our compute strategy?"**
→ Databricks offers superior cost-to-performance optimization through better autoscaling and specialized compute types like SQL Warehouses that are purpose-built for BI.

## 5 Things to Know Before the Call
1. **The Golden Rule:** Always use **Job Clusters** for production ETL; they are significantly cheaper than All-Purpose clusters.
2. **The Driver is Critical:** Never use Spot instances for the **Driver Node**—if the Driver fails, the entire job fails.
3. **Watch the "All-Purpose" Bill:** These are the most expensive clusters; leaving them running overnight is the #1 cause of budget overruns.
4. **Serverless is the Future:** SQL Warehouses (especially Serverless) provide near-instant startup, removing the "wait time" for analysts.
5. **Storage is Permanent, Compute is Not:** Data lives in S3; compute is transient and can be spun up or down as needed.

## Competitive Snapshot
| vs | Advantage |
|---|---|
| **Legacy Hadoop/On-Prem** | Eliminate hardware's fixed capacity; scale instantly to meet demand. |
| **AWS Glue** | Superior workload-specific compute (SQL Warehouses) and better cost transparency. |
| **Manual EC2 Management** | Automated scaling and "Serverless" options remove the need for server administration. |

---
*Source: Databricks Compute and Cluster Configuration course section*