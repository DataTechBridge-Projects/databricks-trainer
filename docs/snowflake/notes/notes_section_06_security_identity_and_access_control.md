# Security, Identity, and Access Control — SA Quick Reference

## What It Is
A multi-layered defense system that ensures only the right people access the right data from approved locations. It replaces manual user permissions with an automated, scalable hierarchy of roles and fine-grained data controls.

## Why Customers Care
- **Reduced Compliance Risk:** Protects PII/PHI to prevent massive fines from GDPR, HIPAA, or CCPA violations.
- **Operational Efficiency:** Eliminates "permission sprawl" by managing roles instead of thousands of individual users.
- **Minimized Blast Radius:** Limits the impact of compromised credentials through network restrictions and cell-level masking.

## Key Differentiators vs Alternatives
- **Decoupled Identity & Authorization:** Separates "who you are" (SSO) from "what you can do" (RBAC) to prevent administrative bottlenecks.
- **Cell-Level Governance:** Enables "multi-tenancy" within a single table using Row Access Policies, rather than duplicating data for different users.
- **Automated Inheritance:** Uses a hierarchical structure where permissions flow upward, significantly reducing manual management overhead.

## When to Recommend It
Recommend for highly regulated industries (Finance, Healthcare) or rapidly scaling organizations. Look for signals like "manual permission management struggles," "difficulty passing audits," or "need to share sensitive data across different business units securely."

## Top 3 Objections & Responses
**"Managing a complex role hierarchy will be an administrative nightmare."**
→ It’s actually the opposite; by using an inherited hierarchy, you manage a few key roles rather than thousands of individual user permissions.

**"If we mask the data, our analysts won't be able to do their jobs."**
→ Dynamic Data Masking allows analysts to query live data seamlessly, only obscuring sensitive fields like SSNs while leaving the rest of the dataset functional.

**"We need total isolation; we can't have our data on the public internet."**
→ Snowflake supports Private Link (AWS/Azure), ensuring your data traffic stays entirely within your private network, never touching the public internet.

## 5 Things to Know Before the Call
1. **Permissions flow upward:** In the RBAC hierarchy, if Role A is granted to Role B, Role B inherits everything Role A can do.
2. **The "Super User" trap:** Never use `ACCOUNTADMIN` for daily tasks; it should be reserved strictly for billing and account-level configuration.
3. **The "Lockout" risk:** Applying a restrictive Network Policy without whitelisting your own IP can immediately lock you out of the Snowflake UI.
4. **Identity is external:** Snowflake relies on industry standards like SAML 2.0, allowing seamless integration with existing tools like Okta or Azure AD.
5. **Single-table multi-tenancy:** You can serve multiple clients or regions from one single table using Row Access Policies to filter visibility.

## Competitive Snapshot
| vs | Advantage |
|---|---|
| Legacy Data Warehouses | Eliminates "permission sprawl" through automated, hierarchical RBAC. |
| On-Premise Security | Delivers "Zero Trust" capabilities (Private Link/Masking) without manual hardware management. |

---
*Source: Security, Identity, and Access Control course section*