# Data Sharing and the Snowflake Marketplace — SA Quick Reference

## What It Is
A way to grant real-time access to live data across different organizations without ever moving or copying a single file. It replaces the old "copy-and-send" method with instant, secure access to a single source of truth.

## Why Customers Care
- **Eliminates Data Latency:** Partners see updates the second they happen, removing the "stale data" gap.
- **Massive Cost Savings:** Removes expensive data egress fees and the need for redundant storage.
- **Reduced Operational Risk:** Eliminates the need to build, manage, and secure complex ETL pipelines for every partner.

## Key Differentiators vs Alternatives
- **Zero-Copy Architecture:** Unlike traditional methods, no data is physically duplicated or re-ingested.
- **Live Metadata Access:** Consumers query the provider's live data via metadata pointers, ensuring instant synchronization.
- **Decoupled Economics:** The Provider manages the storage, while the Consumer pays only for the compute they use to run queries.

## When to Recommend It
Recommend this to customers managing partner ecosystems (e.g., supply chains, banking consortiums) or those struggling with "stale" vendor data. It is a "must-have" for mature cloud organizations looking to enrich their internal datasets with external signals—like weather, finance, or demographics—without the overhead of building new ingestion pipelines.

## Top 3 Objections & Responses
**"How do I know my sensitive data and business logic stay private?"**
→ We use **Secure Views** to mask PII and hide the underlying SQL logic, ensuring consumers only see exactly what you authorize.

**"Won't sharing data with so many partners drive up my egress and storage costs?"**
→ Actually, it eliminates egress fees entirely because no data is physically moved across the network, and there is zero data duplication.

**"Is it a management nightmare to handle dozens of different partners?"**
→ Not if you use a **Private Data Exchange**, which allows you to automate and curate a single, controlled ecosystem for a specific group of organizations.

## 5 Things to Know Before the Call
1. The **Consumer** must have an active Virtual Warehouse running to query the shared data.
2. The **Provider** is responsible for the storage costs; the **Consumer** pays for the compute.
3. **Direct Sharing** is the manual, 1-to-1 approach for known partners.
4. **Marketplace** is a public, searchable hub for discovering third-party datasets.
5. **Secure Views** are the industry standard for protecting sensitive logic during a share.

## Competitive Snapshot
| vs | Advantage |
|---|---|
| Traditional ETL (S3/FTP/Pipelines) | Eliminates data latency and the manual "copy-and-send" workflow. |
| Manual Data Ingestion | Zero-copy architecture removes the need to ingest, store, and manage duplicate datasets. |

---
*Source: Data Sharing and the Snowflake Marketplace course section*