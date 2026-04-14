# Query Optimization and Performance Tuning — SA Quick Reference

## What It Is
It is the practice of ensuring queries touch only the necessary data to maximize speed and minimize waste. It focuses on maximizing "pruning" (skipping irrelevant data) and minimizing "spilling" (moving data to slow disk storage).

## Why Customers Care
- **Reduced Cloud Spend:** Eliminates wasted compute credits caused by inefficient, large-scale data scans.
- **Faster Time-to-Insight:** Prevents "slow dashboard" syndrome by reducing query latency for end-users.
- **Operational Scalability:** Ensures performance remains stable even as data volumes grow from Terabytes to Petabytes.

## Key Differentiators vs Alternatives
- **Metadata-Driven Pruning:** Unlike legacy systems that require manual indexing, Snowflake uses automatic micro-partition metadata to skip data.
- **Automated Heavy Lifting:** Features like the Query Acceleration Service handle sudden spikes without manual warehouse resizing.
- **Decoupled Scaling:** You can tune performance by adjusting compute (Warehouse) or structure (Clustering) without needing to re-architect the entire database.

## When to Recommend It
Target customers in the "optimization phase" of cloud maturity—those who have moved workloads to Snowflake but are seeing rising costs or dashboard latency. Look for signals like "Remote Spilling" in query profiles, high "Partitions Scanned" counts, or a CFO questioning the monthly credit consumption.

## Top 3 Objections & Responses
**"We'll just scale up to a larger Warehouse to fix the slowness."**
→ Scaling up adds horsepower, but it won't fix a "full table scan." If your query is scanning 100TB to find 10 rows, a larger warehouse just burns through your budget faster.

**"Can't we just enable Search Optimization (SOS) and Clustering on all our tables?"**
→ Those are surgical tools, not a blanket solution. They incur significant background compute and storage costs; we should only apply them to high-value, large-scale tables where the ROI is clear.

**"Our SQL developers are already writing optimized code; we don't need this."**
→ Great code is only half the battle. We need to look at the Snowflake Query Profile to see if the underlying data architecture—like micro-partitioning and pruning—is actually supporting that code.

## 5 Things to Know Before the Call
1. **Pruning is the North Star:** If "Partitions Scanned" is nearly equal to "Partitions Total," the customer is paying for a full table scan.
2. **Spilling is the "Performance Killer":** Local spilling is manageable; "Remote Spilling" to S3/Azure Blob is a massive latency and cost red flag.
3. **The Query Profile is your Truth:** Never guess; always use the Query Profile to diagnose exactly where the bottleneck lies.
4. **Avoid Over-Engineering:** Don't recommend Clustering or SOS for small tables; the maintenance cost will outweigh the performance gains.
5. **Optimization = CFO Win:** Every optimization effort should be framed as a way to reclaim wasted cloud spend.

## Competitive Snapshot
| vs | Advantage |
|---|---|
| Legacy/On-Prem | Eliminates the manual burden of managing indexes, vacuuming, and partitions. |
| Competitor (Standard Cloud DW) | Snowflake’s metadata-layer allows for more automated, hands-off data pruning. |

---
*Source: Query Optimization and Performance Tuning course section*