# Stream and Batch Processing with Dataflow — SA Quick Reference

## What It Is
A fully managed, serverless service that processes both real-time streams and historical batch data using a single codebase. It uses the Apache Beam SDK to automate the heavy lifting of data transformations without requiring you to manage any servers.

## Why Customers Care
- **Eliminate Technical Debt:** Replace the "Lambda Architecture" (maintaining two separate codebases for batch and stream) with one unified pipeline.
- **Accelerated Time-to-Market:** Engineers focus on writing transformation logic instead of managing, scaling, or patching clusters.
- **Improved Data Consistency:** Using identical logic for both real-time and historical data ensures your "immediate" and "historical" numbers actually match.

## Key Differentiators vs Alternatives
- **Unified Programming Model:** Write code once in Apache Beam and apply it to both Pub/Sub (streaming) and Cloud Storage (batch).
- **True Serverless Scaling:** Automatically scales compute resources up and down based on data volume without manual intervention.
- **Architectural Offloading:** Uses "Streaming Engine" and "Shuffle Service" to move processing overhead off worker VMs, enabling much smoother autoscaling than traditional Spark.

## When to Recommend It
Recommend to enterprises migrating from legacy Hadoop/Spark clusters or those struggling with the operational complexity of maintaining separate streaming and batch teams. It is the go-to choice for complex, high-transformation workloads where data accuracy and engineering velocity are more important than the raw cost of compute.

## Top 3 Objections & Responses
**"It seems more expensive than just running SQL in BigQuery."**
→ BigQuery is perfect for simple aggregations, but Dataflow is for complex, custom logic and advanced windowing that SQL simply cannot perform.

**"We already have Spark/Dataproc expertise; why switch?"**
→ If you want to move from "managing infrastructure" to "delivering features," Dataflow provides the same capabilities without the operational burden of cluster management.

**"How do you handle data that arrives late or out of order?"**
→ Dataflow uses "watermarks" to track progress and "triggers" to intelligently decide when to update your results, ensuring late data is handled accurately rather than ignored.

## 5 Things to Know Before the Call
1. **Beam vs. Dataflow:** Beam is the language (SDK); Dataflow is the engine (Runner) that executes it.
2. **The "State Explosion" Risk:** Warning—setting overly frequent triggers in streaming can cause costs to spike by creating too much metadata.
3. **Windowing is Key:** Be ready to discuss how they want to slice time (Fixed, Sliding, or Session windows).
4. **The "Unified" Pitch:** The strongest value prop is replacing two separate engineering workflows with one.
5. **Integration Ecosystem:** Dataflow is the "glue" between sources like Pub/Sub and sinks like BigQuery or Bigtable.

## Competitive Snapshot
| vs | Advantage |
|---|---|
| **BigQuery SQL** | Wins on complex, custom transformations and advanced time-windowing. |
| **Dataproc (Spark/Hadoop)** | Wins on zero-ops serverless scaling and unified batch/stream logic. |
| **Legacy Lambda Architecture** | Wins by eliminating the need for two separate codebases and two engineering teams. |

---
*Source: Stream and Batch Processing with Dataflow course section*