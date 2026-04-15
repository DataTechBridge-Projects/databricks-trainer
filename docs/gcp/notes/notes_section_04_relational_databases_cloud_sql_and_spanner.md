# Relational Databases: Cloud SQL and Spanner — SA Quick Reference

## What It Is
Google’s managed database services that automate the "heavy lifting" of maintenance like patching, backups, and replication. Use Cloud SQL for familiar, regional workloads and Cloud Spanner for massive, global applications that require unlimited scale.

## Why Customers Care
- **Reduced Operational Overhead:** Eliminate manual database administration to focus engineering talent on product innovation.
- **Uninterrupted Business Continuity:** High Availability (HA) configurations protect against zonal failures and data loss.
- **Global Scalability:** Prevent the "vertical scaling wall" by growing your database capacity alongside your user base.

## Key Differentiators vs Alternatives
- **TrueTime Technology:** Spanner uses atomic clocks and GPS to provide global, external consistency that traditional distributed databases cannot match.
- **Seamless Migration Path:** Cloud SQL provides a low-risk "lift-and-shift" destination for existing MySQL, PostgreSQL, and SQL Server workloads.
- **Horizontal vs. Vertical Scaling:** Unlike traditional RDBMS that require larger machines (and downtime) to scale, Spanner scales by simply adding nodes.

## When to Recommend It
Recommend **Cloud SQL** for organizations migrating on-prem workloads or running standard web apps (CMS, ERP) where regional presence is sufficient. Recommend **Cloud Spanner** for mature, high-growth enterprises managing mission-critical, global-scale applications—such as financial transactions or global e-commerce—that demand massive throughput and absolute data integrity across multiple continents.

## Top 3 Objections & Responses
**"Cloud Spanner seems too complex and expensive for our needs."**
→ Spanner is an investment in scalability; it prevents the massive technical debt and costly re-architecting required when traditional databases hit their physical limits.

**"We are already comfortable with our current MySQL/PostgreSQL setup."**
→ Cloud SQL is designed specifically for that; it’s the same engine you know, but with the "undifferentiated heavy lifting" of management handled by Google.

**"How do we know the data is consistent if users are in different countries?"**
→ Spanner uses Google’s proprietary TrueTime API to ensure synchronous, strong consistency globally, ensuring a transaction is visible everywhere the moment it's committed.

## 5 Things to Know Before the Call
1. **Scaling Mechanics:** Cloud SQL scales vertically (bigger machines), while Spanner scales horizontally (more nodes).
2. **The "Lag" Risk:** Cloud SQL read replicas are asynchronous, meaning there is a slight possibility of reading stale data.
3. **The "Downtime" Risk:** Scaling Cloud SQL vertically often involves a brief period of downtime or a failover event.
4. **Schema Design:** Spanner requires more intentional schema design (like interleaving) compared to traditional databases.
5. **The "NewSQL" Label:** Spanner is the industry leader in "NewSQL"—combining the ACID guarantees of relational DBs with the scale of NoSQL.

## Competitive Snapshot
| vs | Advantage |
|---|---|
| On-Prem RDBMS | Eliminate manual patching, backups, and hardware management. |
| Traditional Distributed DBs | Spanner provides true global, strong consistency via TrueTime. |
| Standard Vertical RDBMS | Spanner offers virtually unlimited horizontal throughput without downtime. |

---
*Source: Relational Databases: Cloud SQL and Spanner course section*