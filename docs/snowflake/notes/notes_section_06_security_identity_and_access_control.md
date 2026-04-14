# Security, Identity, and Access Control — SA Quick Reference

## What It Is
Snowflake uses a multi-layered "least privilege" model that separates identity (who you are) from authorization (what you can do). It ensures users only access the specific data required for their job, minimizing the blast radius of any potential breach.

## Why Customers Care
- **Regulatory Compliance:** Automated protection for PII/PHI to avoid massive GDPR or HIPAA fines.
- **Reduced Admin Overhead:** Eliminates "permission sprawl" by managing roles instead of thousands of individual users.
- **Risk Mitigation:** Limits the impact of compromised credentials through network-level and cell-level restrictions.

## Key Differentiators vs Alternatives
- **Decoupled Architecture:** Separates identity management (SSO) from data permissions, preventing administrative bloat.
- **Fine-Grained Governance:** Implements masking and row-level security within a single table, avoiding the need for fragmented, redundant data copies.
- **Automated Scalability:** A hierarchical RBAC model allows security policies to scale automatically as the organization grows.

## When to Recommend It
Target enterprises in highly regulated industries (Finance, Healthcare) or organizations managing multi-tenant workloads. It is essential for customers moving from fragmented, siloed data environments to a centralized, governed data platform where manual access management has become a bottleneck.

## Top 3 Objections & Responses
**"Managing permissions for thousands of users will be an administrative nightmare."**
→ Snowflake uses a hierarchical RBAC model where permissions are granted to roles, not users, allowing you to manage access via a single, scalable tree structure.

**"Even with roles, how do we prevent users from seeing sensitive columns like SSNs?"**
→ We use Dynamic Data Masking to redact sensitive information at query time, ensuring users see only the data their specific role is authorized to view.

**"We cannot have our data traversing the public internet due to security requirements."**
→ Snowflake supports AWS and Azure Private Link, ensuring your data traffic stays entirely within your private network, isolated from the public web.

## 5 Things to Know Before the Call
1. **Permissions flow upward:** In the role hierarchy, if Role A is granted to Role B, Role B inherits everything Role A can do.
2. **The `ACCOUNTADMIN` Golden Rule:** Never use this role for daily tasks; it should be reserved strictly for billing and account configuration.
3. **The `SYSADMIN` Workhorse:** This is the primary role used for creating all major objects like databases and warehouses.
4. **Network Policy Trap:** Be careful—applying a restrictive IP policy without including your own IP can immediately lock you out of the system.
5. **Multi-tenancy Hack:** Use Row Access Policies to serve different clients from the same table, rather than creating separate, expensive copies of data.

## Competitive Snapshot
| vs | Advantage |
|---|---|
| **Legacy Data Warehouses** | Replace manual, user-by-user permission management with scalable, automated RBAC. |
| **Traditional Cloud DWs** | Achieve cell-level security (masking/row-level) without the performance hit of complex, fragmented views. |

---
*Source: Security, Identity, and Access Control course section*