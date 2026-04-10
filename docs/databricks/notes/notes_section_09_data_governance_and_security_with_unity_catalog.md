# Data Governance and Security with Unity Catalog — SA Quick Reference

## What It Is
Unity Catalog is a centralized governance layer for your entire Databricks Lakehouse. It provides a single, unified point to manage access, auditing, and data lineage across all your workspaces and cloud accounts.

## Why Customers Care
- **Eliminates Security Silos:** Define a permission once at the account level and enforce it globally, regardless of which workspace a user logs into.
- **Reduces "Audit Tax":** Automated data lineage and audit logs drastically cut the engineering hours spent proving compliance to regulators.

- **Enables Fine-Grained Security:** Protect sensitive information without duplicating data by using row-level filtering and column-level masking.

## Key Differentiators vs Alternatives
- **Unified Identity Federation:** Unlike legacy models that require managing users per workspace, UC manages identities at the Account level for true global consistency.
- **End-to-End Lineage:** Provides automated, out-of-the-box visibility into data transformations, which is often a manual, fragmented process in traditional environments.
- **Centralized Three-Tier Namespace:** Simplifies complex data landscapes using a structured `catalog.schema.table` hierarchy that makes discovery intuitive.

## When to Recommend It
Recommend Unity Catalog to enterprise customers moving from "fragmented" to "governed" cloud maturity. It is essential for any organization running multiple Databricks workspaces, handling sensitive PII/PHI, or facing heavy regulatory audit requirements. If the customer is currently struggling with manual permission reconciliations or "security silos" between Dev and Prod environments, UC is the direct solution.

## Top 3 Objections & Responses
**"We already have AWS IAM roles and S3 bucket policies to manage security."**
→ IAM is great for infrastructure, but UC manages the *data* layer; UC allows you to use SQL-based fine-grained access (like masking SSNs) that IAM simply cannot do.

**"Won't moving to Unity Catalog create more management overhead?"**
→ It actually reduces overhead by replacing manual, per-workspace ACLs and Hive Metastore reconciliations with a single, centralized "source of truth" at the Account level.

**"We need to share data with teams that don't use Databricks."**
→ You can still use External Tables for this; UC allows you to maintain governance while ensuring your "Gold" layer remains accessible to tools like Amazon Athena or Snowflake.

## 5 Things to Know Before the Call
1. **The "Drop" Danger:** Deleting a *Managed Table* deletes both the metadata and the physical S3 files; it is permanent.
2. **Namespace Shift:** Moving to UC means moving from a 2-tier (`schema.table`) to a 3-tier (`catalog.schema.table`) structure.
 **Identity is Global:** Users and groups are managed at the Account level, not within individual workspaces.
4. **Managed vs. External:** Use *Managed* for internal Lakehouse pipelines to simplify lifecycle; use *External* for data sharing with the broader ecosystem.
5. **PII Protection:** UC is the primary vehicle for implementing masking functions to hide sensitive columns without creating separate "scrubbed" copies of data.

## Competitive Snapshot
| vs | Advantage |
|---|---|
| Legacy Hive Metastore | Eliminates fragmented security silos and manual permission reconciliation. |
| Manual S3/IAM Management | Provides fine-grained, SQL-based control (row/column level) that IAM lacks. |
| Traditional Data Silos | Centralizes lineage and auditing across all workspaces in a single view. |

---
*Source: Data Governance and Security with Unity Catalog course section*