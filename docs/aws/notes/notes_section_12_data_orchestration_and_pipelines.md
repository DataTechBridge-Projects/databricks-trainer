# Data Orchestration and Pipelines — SA Quick Reference

## What It Is
Data orchestration is the "brain" that manages complex, multi-step workflows across disconnected services. It ensures that when one task finishes—like an ETL job—the next step—like a dashboard refresh—starts automatically and reliably.

## Why Customers Care
- **Eliminates Manual Intervention:** Replaces disconnected, fragile scripts with automated, self-healing workflows.
- **Ensures Data Reliability:** Automatically handles retries and error logic so downstream users don't consume broken data.
- **Provides End-to-End Visibility:** Creates a single, auditable trace of every step in the data lifecycle for compliance and debugging.

## Key Differentiators vs Alternatives
- **Native AWS Integration:** Seamlessly triggers and manages Glue, Lambda, EMR, and Athena without managing infrastructure.
- **Choice of Workflow Type:** Scale from high-volume, low-cost "Express" workflows to mission-critical, "Standard" long-running processes.
- **Serverless Operational Model:** No servers to patch or scale; AWS manages the availability and execution of the state machine.

## When to Recommend It
Recommend this when a customer moves from "single-script" processing to a distributed data architecture. Look for signals like manual data refreshes, "silent" pipeline failures, or complex dependencies where the output of one service (e.g., Glue) must trigger another (e.g., Athena or SNS).

## Top 3 Objections & Responses
**"We already use Airflow/MWAA, why switch to Step Functions?"**
→ Use MWAA for complex, code-heavy data science pipelines, but use Step Functions for high-scale, low-latency, or event-driven AWS service orchestration to reduce operational overhead.

**"Won't this be expensive if we have high-frequency tasks?"**
→ For high-frequency, short-duration tasks (under 5 mins), use **Express Workflows**; they are designed specifically for high-volume, low-cost execution.

**"How do we handle massive datasets in the pipeline?"**
→ We use the **"Claim Check" pattern**: we never pass the raw data through the orchestrator; we pass an S3 URI (a pointer), keeping the payload small and the pipeline performant.

## 5 Things to Know Before the Call
1. **Payload Limit:** Step Functions have a 256 KB limit; never pass large datasets directly in the JSON payload.
2. **Stateful vs. Stateless:** Services like Glue are stateless; Step Functions provide the "state" (memory) of the entire process.
3. **Standard vs. Express:** "Standard" is for auditability and long-running jobs; "Express" is for high-speed, high-volume triggers.
4. **The "Map" State:** This is the secret to scale—it allows you to loop through S3 files and run tasks in parallel.
5. **Security is Granular:** Always advocate for a "Least Privilege" IAM role specific to that single pipeline, not a broad admin role.

## Competitive Snapshot
| vs | AWS Advantage |
|---|---|
| **On-Prem/Legacy Schedulers** | Eliminates "server management" and scales instantly with cloud-native triggers. |
| **Manual Cron Jobs/Scripts** | Replaces "silent failures" with automated retries, error handling, and SNS alerts. |
| **Generic Managed Airflow** | Provides deeper, native "one-click" integration with the broader AWS ecosystem. |

---
*Source: Data Orchestration and Pipelines course section*