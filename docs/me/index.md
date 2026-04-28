# Data Solutions & Architecture

A personal reference library covering **modern data platform patterns, architectures, and solution design** for Solution Architects working across cloud and on-premises data ecosystems. Each page focuses on the concepts, trade-offs, and talking points that matter in customer conversations — not implementation cookbooks.

---

## Why This Exists

Data architecture is one of the most fragmented domains in enterprise IT. Customers are simultaneously managing legacy warehouses, cloud lakehouses, real-time streaming pipelines, and AI/ML workloads — often with overlapping tooling and unclear ownership.

This section helps SAs answer:

- What is the right architectural pattern for this customer's data problem?
- How do the major data platform components fit together — ingestion, storage, processing, serving?
- What are the key trade-offs between approaches (e.g. lakehouse vs. warehouse, batch vs. streaming)?
- How do I frame a data modernization story without overpromising?
- What does "good" look like at each layer of the data stack?

---

## Available References

| Topic | Description |
|-------|-------------|
| [Data Architecture Patterns](data-architecture-patterns.md) | Lakehouse, data warehouse, data mesh, data fabric — when to use each and how to position them |
| [Data Ingestion & Pipelines](data-ingestion-pipelines.md) | Batch, micro-batch, and streaming ingestion patterns — ETL vs. ELT, CDC, and pipeline tooling landscape |
| [Data Storage Layers](data-storage-layers.md) | Raw, curated, and serving zones; Delta Lake, Parquet, Iceberg; medallion architecture deep-dive |
| [Data Governance & Cataloging](data-governance-cataloging.md) | Unity Catalog, data lineage, access control, data quality, and metadata management patterns |
| [Real-Time & Streaming](real-time-streaming.md) | Kafka, Kinesis, Pub/Sub, Spark Streaming — architectures for low-latency data and event-driven systems |
| [Data Serving & Consumption](data-serving-consumption.md) | Semantic layers, SQL endpoints, data APIs, BI connectivity, and ML feature serving patterns |

---

> This is a living reference — pages will be expanded as new patterns and platforms become relevant. Each follows the same structure: what it is → why it matters → architecture → key trade-offs → SA talking points.
