# Data Architect Glossary

> Exhaustive reference of terms, acronyms, and concepts across all Data Architecture domains.

---

## 1. Storage & Architecture Patterns

| Term | Full Form / Description |
|------|------------------------|
| EDW | Enterprise Data Warehouse — centralized repository for integrated, historical data from across the organization, optimized for reporting and analytics |
| ODS | Operational Data Store — near-real-time integration layer that consolidates data from source systems for operational reporting; not a replacement for EDW |
| Data Lake | Storage repository holding vast amounts of raw data in its native format (structured, semi-structured, unstructured) until needed; schema-on-read |
| Data Lakehouse | Architecture combining the low-cost storage of a data lake with the structure and ACID transactions of a data warehouse (e.g., Delta Lake, Apache Iceberg) |
| Data Warehouse | Subject-oriented, integrated, time-variant, non-volatile collection of data in support of management decisions (Inmon's definition) |
| Data Mart | A subset of a data warehouse focused on a single subject area or business unit (e.g., Sales Mart, Finance Mart) |
| Data Hub | Central integration point for data exchange between systems; often includes a metadata registry and routing logic |
| Data Mesh | Decentralized sociotechnical architecture where domain teams own and serve their data as products, with federated governance |
| Data Fabric | Architecture that provides consistent, automated data management across hybrid and multi-cloud environments using metadata and AI |
| Lambda Architecture | Hybrid batch + speed processing architecture; combines a batch layer (high latency, accurate) with a speed layer (low latency, approximate) |
| Kappa Architecture | Simplified streaming-only architecture that eliminates the batch layer; all data processed as streams |
| Medallion Architecture | Layered data organization: Bronze (raw), Silver (cleaned/conformed), Gold (business-level aggregates); popularized by Databricks |
| Bronze Layer | Raw ingestion layer in medallion architecture; data lands as-is from source systems |
| Silver Layer | Cleaned, deduplicated, and conformed data layer; applies data quality rules and joins |
| Gold Layer | Business-level aggregates and curated datasets ready for BI consumption |
| HTAP | Hybrid Transactional/Analytical Processing — systems that support both OLTP and OLAP workloads simultaneously |
| OLTP | Online Transactional Processing — systems optimized for high-volume, low-latency read/write operations (e.g., order entry systems) |
| OLAP | Online Analytical Processing — systems optimized for complex queries across large datasets for decision support |
| MPP | Massively Parallel Processing — distributes query execution across many nodes simultaneously; used in Redshift, Snowflake, BigQuery |
| SMP | Symmetric Multiprocessing — multiple processors sharing a single memory space; limits scalability compared to MPP |
| Shared-Nothing Architecture | Each node in a cluster has its own CPU, memory, and disk; no resource contention; basis for most MPP systems |
| Shared-Disk Architecture | Nodes share storage but have independent CPUs/memory; common in cloud-native warehouses like Snowflake |
| Data Vault | Modeling methodology for enterprise data warehouses; highly scalable, auditable, and adaptable (see Data Modeling section) |
| Operational Analytics | Running analytics directly on operational/transactional data with minimal latency |
| Logical Data Warehouse | Virtual data warehouse layer that federates queries across multiple physical data stores without moving data |
| Virtual Data Warehouse | Query federation layer that presents a unified schema across disparate sources |
| Data Virtualization | Technology that provides real-time, unified data access across disparate systems without physical data movement |
| CDP | Customer Data Platform — system that creates a unified, persistent customer database accessible to other systems |
| MDM | Master Data Management — discipline for defining and managing critical data assets (customers, products, locations) to ensure single authoritative version |
| Reference Data | Data that defines valid values for other data fields (e.g., country codes, currency codes, status values) |
| Landing Zone | Initial staging area where raw data is deposited before processing; often synonymous with Bronze layer |
| Staging Area | Temporary storage area used during ETL for intermediate transformations before loading to target |
| Cold Storage | Low-cost, high-latency storage tier for infrequently accessed archival data |
| Hot Storage | High-cost, low-latency storage tier for frequently accessed, active data |
| Warm Storage | Middle-tier storage with moderate cost and access latency |
| Polyglot Persistence | Using multiple database technologies (relational, document, graph, key-value) best suited to each workload within one system |
| Event Store | Append-only log of all state-changing events in a system; basis for event sourcing pattern |
| Time-Series Database | Optimized for storing and querying timestamped data points (e.g., InfluxDB, TimescaleDB) |
| Graph Database | Stores data as nodes and edges to represent and traverse relationships (e.g., Neo4j, Amazon Neptune) |
| Document Store | Stores data as JSON/BSON documents with flexible schema (e.g., MongoDB, Couchbase) |
| Key-Value Store | Simplest NoSQL model; stores data as key-value pairs (e.g., Redis, DynamoDB) |
| Wide-Column Store | Stores data in rows with dynamic columns; suited for time-series and sparse data (e.g., Cassandra, HBase) |
| NewSQL | Databases providing ACID guarantees of traditional RDBMS with horizontal scalability of NoSQL (e.g., CockroachDB, Spanner) |
| In-Memory Database | Stores data primarily in RAM for ultra-low latency (e.g., Redis, SAP HANA, MemSQL) |
| Data Swamp | A poorly governed data lake where data quality, lineage, and discoverability have broken down |
| Unified Namespace | Single logical namespace that abstracts all data sources for query purposes |
| Reverse ETL | Process of syncing data from a data warehouse back into operational systems (CRM, marketing tools) |
| Zero-Copy Cloning | Creating a metadata-only copy of a dataset without duplicating physical storage (Snowflake feature) |
| Data Sharing | Capability to share live data across accounts or organizations without copying (Snowflake, Databricks Delta Sharing) |
| External Table | Table definition pointing to data stored outside the database (e.g., files in S3) |
| Federated Query | Querying data across multiple heterogeneous systems from a single SQL interface |

---

## 2. Data Modeling

| Term | Full Form / Description |
|------|------------------------|
| Kimball | Ralph Kimball's dimensional modeling methodology; centers on fact and dimension tables optimized for business user queries |
| Inmon | Bill Inmon's enterprise data warehouse approach; normalized 3NF central warehouse with subject-area data marts fed from it |
| Data Vault 2.0 | DV2.0 — Dan Linstedt's hybrid modeling approach with Hubs (business keys), Links (relationships), and Satellites (context); agile and auditable |
| Anchor Modeling | Ultra-normalized modeling approach using anchors, attributes, ties, and knots; handles change well but complex to query |
| Activity Schema | Modern analytics modeling pattern organizing all data around a single entity timeline |
| Dimensional Model | Fact-and-dimension schema design for analytical databases; optimized for query performance and business usability |
| Fact Table | Central table in a dimensional model storing numeric measures and foreign keys to dimensions (e.g., Sales Fact) |
| Dimension Table | Descriptive attributes table providing context for facts (e.g., Date, Customer, Product dimensions) |
| Star Schema | Dimensional model with a central fact table surrounded by denormalized dimension tables; simple and fast to query |
| Snowflake Schema | Normalized variant of star schema where dimension tables are further normalized into sub-dimensions |
| Galaxy Schema | Multiple fact tables sharing dimension tables; also called Fact Constellation |
| Bridge Table | Resolves many-to-many relationships between fact and dimension tables |
| Degenerate Dimension | Dimension attribute stored directly in the fact table rather than a separate dimension table (e.g., invoice number) |
| Junk Dimension | Combines low-cardinality miscellaneous flags/indicators into a single dimension to reduce fact table width |
| Role-Playing Dimension | Single dimension table used multiple times in a fact table for different purposes (e.g., Date as Order Date, Ship Date) |
| Outrigger | Secondary dimension table attached to a primary dimension table (not directly to fact); used sparingly |
| Conformed Dimension | Dimension shared across multiple fact tables or data marts with consistent meaning and values |
| Conformed Fact | Fact measure with consistent definition and granularity across data marts |
| Grain | The level of detail represented by a single row in a fact table; must be declared before design begins |
| Factless Fact Table | Fact table with no numeric measures; captures events or coverage relationships (e.g., student enrollment) |
| Accumulating Snapshot | Fact table pattern tracking the lifecycle of a process with multiple date stamps updated as milestones are reached |
| Periodic Snapshot | Fact table capturing state at regular intervals (daily, weekly, monthly) |
| Transaction Fact Table | Records individual business events or transactions at the lowest grain |
| SCD | Slowly Changing Dimension — technique for managing changes to dimension attributes over time |
| SCD Type 0 | Dimension attributes never change; historical value is retained forever |
| SCD Type 1 | Overwrite old value; no history kept; current state only |
| SCD Type 2 | Add a new row for each change; full history preserved with effective dates and current flag |
| SCD Type 3 | Add a new column for the previous value; limited history (typically tracks only one prior value) |
| SCD Type 4 | Separate history table; current values in main table, all history in mini-dimension |
| SCD Type 6 | Hybrid combining Types 1, 2, and 3; adds current value column to Type 2 rows |
| Hub | Data Vault component storing a unique list of business keys with metadata (load date, source) |
| Link | Data Vault component capturing relationships between two or more Hubs |
| Satellite | Data Vault component storing descriptive context and history for a Hub or Link |
| PIT Table | Point-in-Time table in Data Vault — pre-joins satellites at specific snapshots for query performance |
| Bridge Table (DV) | Data Vault construct that pre-joins a chain of links and hubs for performance |
| Business Vault | Data Vault layer containing business rules and calculations applied to Raw Vault data |
| Raw Vault | Data Vault layer containing data as-received from sources, no business rules applied |
| 3NF | Third Normal Form — relational database design where all attributes depend only on the primary key; eliminates redundancy |
| 1NF | First Normal Form — all column values are atomic (indivisible), no repeating groups |
| 2NF | Second Normal Form — 1NF plus all non-key attributes fully depend on the entire composite primary key |
| BCNF | Boyce-Codd Normal Form — stronger version of 3NF; every determinant is a candidate key |
| Denormalization | Intentionally adding redundancy to a normalized schema to improve read query performance |
| ERD | Entity-Relationship Diagram — visual representation of entities and their relationships in a data model |
| Conceptual Model | High-level model showing key entities and relationships; no technical detail; used for stakeholder communication |
| Logical Model | Detailed data model with entities, attributes, and relationships; technology-agnostic |
| Physical Model | Implementation-specific model with tables, columns, data types, indexes, and constraints |
| Surrogate Key | System-generated artificial primary key (integer or UUID) assigned to dimension rows |
| Natural Key | Business-assigned identifier that has meaning outside the database (e.g., customer ID, SSN) |
| Composite Key | Primary key made up of two or more columns |
| Foreign Key | Column(s) referencing the primary key of another table to enforce referential integrity |
| Business Key | Identifier used in the business domain to uniquely identify an entity; basis for Data Vault Hubs |
| Cardinality | The number of unique values in a column; also describes relationship types (1:1, 1:M, M:N) |
| Granularity | Level of detail in a dataset; fine grain = more rows, each representing a smaller unit of measurement |
| Normalization | Process of organizing data to reduce redundancy and improve data integrity |
| Data Type | Classification of a column's values (INTEGER, VARCHAR, DATE, BOOLEAN, etc.) |
| Null Handling | How missing/unknown values are represented and treated in queries and aggregations |
| Temporal Table | Table that automatically tracks row history with valid-time or transaction-time columns; ISO SQL:2011 standard |
| Bi-Temporal Modeling | Tracking both valid time (when something was true in reality) and transaction time (when it was recorded) |
| Polymorphic Association | Single table stores relationships to multiple entity types; common anti-pattern in relational modeling |
| Anti-Pattern | A modeling or design choice that seems reasonable but causes problems (e.g., EAV for structured data) |
| EAV | Entity-Attribute-Value — stores data as rows of key-value pairs; flexible but hard to query and validate |
| Wide Table | Denormalized table with many columns; common in analytics/columnar stores for query performance |
| Schema Evolution | The ability to change a data schema (add/remove columns) without breaking existing consumers |
| Semantic Key | A meaningful business key embedded in a surrogate; combines audibility and performance |
| Hash Key | MD5 or SHA-1 hash of business key fields used as surrogate in Data Vault for deterministic, parallel loading |

---

## 3. Integration & Processing

| Term | Full Form / Description |
|------|------------------------|
| ETL | Extract, Transform, Load — data integration pattern where transformation occurs before loading into target |
| ELT | Extract, Load, Transform — data is loaded raw into target system and transformed there using its compute power |
| CDC | Change Data Capture — technique for identifying and capturing data changes in source systems (insert, update, delete) |
| Log-Based CDC | CDC using database transaction logs (WAL, binlog) to capture changes without impacting source performance |
| Query-Based CDC | CDC using timestamps or watermarks in SQL queries to detect changed rows; higher source impact |
| Trigger-Based CDC | CDC using database triggers to capture changes; high overhead, generally avoided |
| Batch Processing | Processing data in discrete, scheduled chunks; high latency, high throughput |
| Micro-Batch | Near-real-time processing of small batches at short intervals (e.g., Spark Structured Streaming) |
| Stream Processing | Continuous processing of data as it arrives with very low latency (e.g., Apache Flink, Kafka Streams) |
| Real-Time Processing | Data processing with sub-second latency; used for alerts, fraud detection, live dashboards |
| Near-Real-Time | Processing with latency of seconds to minutes; acceptable for many operational analytics use cases |
| Data Pipeline | Series of processing steps that move and transform data from source to destination |
| Ingestion | Process of bringing data into a storage system from external sources |
| Message Queue | Asynchronous communication buffer between systems (e.g., RabbitMQ, Amazon SQS) |
| Event Streaming | Durable, ordered log of events accessible for replay by multiple consumers (e.g., Apache Kafka) |
| Kafka | Apache Kafka — distributed event streaming platform; uses topics, partitions, producers, and consumers |
| Pub/Sub | Publish-Subscribe messaging pattern where producers publish to topics and consumers subscribe independently |
| Topic | Named channel in a messaging system where events are published and consumed |
| Partition | Subdivision of a Kafka topic for parallelism and ordering guarantees |
| Consumer Group | Set of consumers that collectively read all partitions of a topic; enables parallel consumption |
| Exactly-Once Semantics | Processing guarantee that each message is processed exactly once, even in failure scenarios |
| At-Least-Once | Processing guarantee that a message will be processed at minimum once; duplicates possible |
| At-Most-Once | Processing guarantee that a message is processed no more than once; data loss possible |
| Idempotency | Property of an operation that can be applied multiple times without changing the result beyond the first application |
| Backpressure | Mechanism for a downstream system to signal an upstream system to slow data production |
| Watermark | In stream processing, a threshold indicating how late events can arrive and still be included in a window |
| Event Time | The time when an event actually occurred in the real world |
| Processing Time | The time when an event is processed by the stream processor |
| Tumbling Window | Fixed-size, non-overlapping time window for stream aggregations |
| Sliding Window | Overlapping time windows that advance by a step smaller than the window size |
| Session Window | Dynamic window that groups events within a period of activity, closing after a gap of inactivity |
| Late Arriving Data | Events that arrive after the expected processing window; requires special handling strategies |
| Upsert | Operation that inserts a new record or updates an existing one based on a key match (UPDATE + INSERT) |
| Merge | SQL/DML operation combining INSERT, UPDATE, and DELETE in a single statement based on match conditions |
| Full Refresh | Loading strategy that truncates and reloads an entire table; simple but expensive for large datasets |
| Incremental Load | Loading only new or changed records since the last extraction; requires reliable watermarking |
| Delta Load | Synonym for incremental load; loading only the "delta" (changes) since the last run |
| Data Replication | Copying data from one system to another to ensure availability, redundancy, or geographic distribution |
| Webhook | HTTP callback that pushes data to a URL when an event occurs; event-driven integration pattern |
| API Integration | Connecting systems via REST, SOAP, or GraphQL APIs to exchange data |
| REST | Representational State Transfer — stateless HTTP-based API design style; uses GET, POST, PUT, DELETE |
| GraphQL | Query language for APIs that allows clients to request exactly the data they need |
| gRPC | Google Remote Procedure Call — high-performance RPC framework using Protocol Buffers |
| Protocol Buffers | Protobuf — Google's binary serialization format; more efficient than JSON/XML |
| Avro | Apache Avro — compact binary data serialization format with schema evolution support; common in Kafka |
| Parquet | Apache Parquet — columnar binary storage format; efficient for analytical queries; default in many lake formats |
| ORC | Optimized Row Columnar — columnar format developed for Hive; includes built-in indexes and statistics |
| JSON | JavaScript Object Notation — lightweight, human-readable data interchange format |
| CSV | Comma-Separated Values — plain-text tabular format; ubiquitous but lacks schema enforcement |
| XML | Extensible Markup Language — hierarchical text-based format; verbose but self-describing |
| Schema Registry | Service that stores and validates Avro/Protobuf/JSON schemas for event streams (e.g., Confluent Schema Registry) |
| DAG | Directed Acyclic Graph — representation of pipeline dependencies; used by Airflow, dbt, and other orchestrators |
| Orchestration | Coordinating and scheduling the execution of pipeline tasks and dependencies |
| Airflow | Apache Airflow — open-source workflow orchestration platform using Python DAGs |
| Prefect | Modern Python-native orchestration platform with dynamic workflows |
| Dagster | Data-aware orchestration platform with built-in asset tracking and lineage |
| dbt | Data Build Tool — SQL-based transformation framework for the ELT pattern; version-controls SQL models |
| Fivetran | Managed connector service for automated data ingestion from SaaS and database sources |
| Airbyte | Open-source data integration platform with a large connector catalog |
| Singer | Open-source data integration specification using taps (sources) and targets (destinations) |
| Debezium | Open-source CDC platform that captures database changes via transaction logs |
| Flink | Apache Flink — distributed stream processing framework with exactly-once guarantees |
| Spark | Apache Spark — unified analytics engine for large-scale batch and streaming data processing |
| Spark Streaming | Micro-batch streaming layer on Apache Spark |
| Structured Streaming | Spark's continuous streaming API built on top of Spark SQL |
| Beam | Apache Beam — unified programming model for batch and streaming pipelines; runs on multiple runners |
| Dataflow | Google Cloud Dataflow — managed Apache Beam service |
| Kinesis | Amazon Kinesis — managed real-time data streaming service |
| Event Hub | Azure Event Hubs — fully managed event ingestion service; Kafka-compatible |
| Pub/Sub (GCP) | Google Cloud Pub/Sub — managed messaging and ingestion service |
| SQS | Amazon Simple Queue Service — managed message queuing service |
| SNS | Amazon Simple Notification Service — managed pub/sub messaging for fan-out patterns |
| Data Contracts | Formal agreement between data producers and consumers defining schema, quality, and SLA expectations |
| Schema-on-Read | Schema is applied when data is read, not when it is written; enables flexible ingestion |
| Schema-on-Write | Schema is enforced when data is written; ensures data quality at the point of ingestion |
| Data Serialization | Converting data structures to a format suitable for storage or transmission |
| Compression | Reducing data size using algorithms (GZIP, Snappy, LZ4, ZSTD); critical for storage cost and I/O performance |
| Partitioning | Dividing data into logical segments (by date, region, etc.) to improve query performance and data management |
| Bucketing | Sub-partitioning data into fixed buckets by hash of a column; improves join and aggregation performance |
| Z-Ordering | Multi-dimensional clustering technique (Delta Lake) that co-locates related data to reduce query I/O |
| Clustering | Physically organizing data on disk by one or more columns to improve range query performance |
| Pushdown Predicate | Filtering applied at the storage layer before data is sent to the compute layer; reduces data scan |
| Data Skew | Uneven distribution of data across partitions causing some tasks to run much longer than others |
| Shuffle | Redistribution of data across partitions during operations like joins and aggregations in distributed systems |
| Broadcast Join | Join optimization where a small table is replicated to all nodes to avoid shuffling a large table |

---

## 4. Metadata & Data Governance

| Term | Full Form / Description |
|------|------------------------|
| DAMA | Data Management Association — professional organization that publishes the DMBOK framework |
| DMBOK | Data Management Body of Knowledge — DAMA's comprehensive framework for data management disciplines |
| Data Governance | Framework of policies, processes, standards, and roles that ensure data is managed as a strategic asset |
| Data Steward | Person responsible for the quality and fitness of a specific data domain or dataset |
| Data Owner | Business executive accountable for the quality, security, and appropriate use of a data asset |
| Data Custodian | IT role responsible for technical management and storage of data assets |
| Data Catalog | Metadata repository providing searchable inventory of data assets with descriptions, lineage, and quality info |
| Business Glossary | Curated dictionary of business terms with agreed definitions; foundation for data governance |
| Data Dictionary | Technical documentation of datasets, tables, and columns including types, constraints, and descriptions |
| Data Lineage | End-to-end tracking of data origin, movement, transformations, and consumption |
| Impact Analysis | Using lineage to assess downstream effects of a proposed schema or pipeline change |
| Active Metadata | Metadata that drives automated decisions and actions (e.g., triggering quality checks, routing data) |
| Passive Metadata | Metadata used for documentation and discovery but not for automation |
| Technical Metadata | Information about data structure, format, storage, and access (table schemas, file sizes, partitions) |
| Business Metadata | Context describing business meaning, ownership, and usage policies |
| Operational Metadata | Information about data pipelines, job runs, data volumes, and processing history |
| Data Profiling | Statistical analysis of data to understand its content, structure, quality, and relationships |
| Data Classification | Categorizing data by sensitivity level (Public, Internal, Confidential, Restricted) |
| PII | Personally Identifiable Information — any data that can identify a specific individual (name, SSN, email) |
| PHI | Protected Health Information — health data protected under HIPAA regulations |
| PCI DSS | Payment Card Industry Data Security Standard — security standard for handling cardholder data |
| GDPR | General Data Protection Regulation — EU regulation governing personal data collection and processing |
| CCPA | California Consumer Privacy Act — California law giving consumers rights over personal data |
| HIPAA | Health Insurance Portability and Accountability Act — US law protecting medical information |
| Data Residency | Requirement that data be stored and processed within specific geographic boundaries |
| Data Sovereignty | Legal concept that data is subject to the laws of the country where it is collected or stored |
| Right to be Forgotten | GDPR right allowing individuals to request deletion of their personal data |
| Data Minimization | Principle of collecting only the minimum data necessary for a stated purpose |
| Purpose Limitation | Principle that data collected for one purpose should not be used for a different purpose |
| Consent Management | Systems and processes for capturing, storing, and enforcing user consent for data processing |
| Data Retention Policy | Rules governing how long data is kept before archival or deletion |
| Data Lifecycle Management | DLM — governing data from creation through archival and deletion |
| Data Access Control | Policies and mechanisms controlling who can read, write, or modify specific data assets |
| RBAC | Role-Based Access Control — granting data access based on user roles rather than individual identities |
| ABAC | Attribute-Based Access Control — access decisions based on attributes of users, resources, and environment |
| Column-Level Security | Restricting access to specific columns in a table based on user role or attribute |
| Row-Level Security | RLS — filtering rows returned to a user based on their identity or role |
| Dynamic Data Masking | Masking sensitive data in query results without changing the stored data |
| Tokenization | Replacing sensitive data values with non-sensitive tokens; original value stored in a secure vault |
| Encryption at Rest | Encrypting data while stored on disk; protects against physical media theft |
| Encryption in Transit | Encrypting data as it moves over networks (TLS/SSL); protects against interception |
| Key Management | Managing cryptographic keys for encryption; critical for key rotation and access control |
| Audit Trail | Immutable log of all data access and modification events for compliance and forensic purposes |
| Data Trust Score | Metric quantifying the reliability and quality of a dataset based on multiple quality dimensions |
| Data Policy | Formal rules governing data collection, use, storage, sharing, and disposal |
| Data Standard | Agreed specifications for data formats, definitions, coding, and quality rules |
| Interoperability | Ability of different systems to exchange and use data without special integration effort |
| Data Portability | Ability to transfer data from one system to another in a usable format |
| Metadata Management | Discipline for collecting, storing, maintaining, and using metadata to improve data usability |
| Apache Atlas | Open-source metadata management and governance platform for Hadoop ecosystems |
| Collibra | Enterprise data governance and catalog platform |
| Alation | AI-based data catalog and governance platform |
| Atlan | Modern collaborative data catalog with active metadata capabilities |
| DataHub | LinkedIn's open-source metadata platform for data discovery and lineage |
| OpenMetadata | Open-source metadata platform and data catalog |
| Unity Catalog | Databricks' unified governance layer for data and AI assets |
| Informatica IDMC | Informatica Intelligent Data Management Cloud — enterprise data management platform |
| Waterline Data | AI-driven data discovery and cataloging tool (acquired by Infogix) |
| Data Contract | Formal schema and quality agreement between data producers and consumers |
| Schema Registry | Central repository for managing and versioning event schemas (Confluent, AWS Glue) |
| Data Mesh Governance | Federated computational governance in Data Mesh; policies enforced via automated platforms, not central teams |
| FAIR Principles | Findable, Accessible, Interoperable, Reusable — principles for scientific data management |

---

## 5. Semantic Layer & Ontology

| Term | Full Form / Description |
|------|------------------------|
| Semantic Layer | Abstraction that translates business terms into technical data queries; sits between data and BI tools |
| Metric Layer | Centralized definition of business metrics (revenue, churn) ensuring consistent calculation everywhere |
| Headless BI | Metric definitions and business logic decoupled from any specific BI tool; accessible via API |
| Metrics Store | Repository of defined, versioned, and governed business metrics (e.g., dbt Metrics, Cube.js) |
| Ontology | Formal representation of knowledge including concepts, categories, and relationships in a domain |
| Knowledge Graph | Graph structure that represents real-world entities and semantic relationships between them |
| RDF | Resource Description Framework — W3C standard for representing information as subject-predicate-object triples |
| RDFS | RDF Schema — vocabulary extension for RDF providing class and property hierarchies |
| OWL | Web Ontology Language — W3C standard for creating rich ontologies on top of RDF |
| SPARQL | SPARQL Protocol and RDF Query Language — query language for RDF data stores |
| Triple | Atomic unit of RDF data: subject (entity) + predicate (relationship) + object (entity or value) |
| Named Graph | RDF graph with an associated URI; allows managing and querying subsets of a triple store |
| Linked Data | Practice of using RDF and HTTP URIs to publish and connect structured data on the web |
| SKOS | Simple Knowledge Organization System — W3C standard for expressing controlled vocabularies |
| Taxonomy | Hierarchical classification system for organizing concepts into parent-child relationships |
| Thesaurus | Vocabulary of preferred terms with synonyms, broader/narrower terms, and related terms |
| Controlled Vocabulary | Standardized set of terms used for consistent tagging and classification |
| URI | Uniform Resource Identifier — globally unique identifier for resources in linked data and the web |
| Property Graph | Graph model where nodes and edges can have properties; used by Neo4j, TigerGraph |
| Cypher | Declarative query language for property graphs; used by Neo4j |
| Gremlin | Graph traversal language for property graphs; part of Apache TinkerPop |
| Triple Store | Database optimized for storing and querying RDF triples (e.g., Stardog, GraphDB, Amazon Neptune) |
| Inference / Reasoning | Deriving new facts from existing knowledge using ontology rules (e.g., OWL reasoning) |
| Semantic Search | Search that understands the meaning and context of queries rather than just keyword matching |
| Entity Resolution | Process of identifying when records from different sources refer to the same real-world entity |
| Entity Extraction | NLP technique for identifying named entities (people, places, organizations) in unstructured text |
| Knowledge Representation | Formal encoding of domain knowledge for automated reasoning |
| dbt Semantic Layer | dbt's implementation of a metric layer allowing consistent metric definitions across BI tools |
| LookML | Looker's proprietary data modeling language for defining metrics, dimensions, and explores |
| AtScale | Semantic layer and universal data model platform |
| Cube.js | Open-source analytical API platform with a metric/semantic layer |
| Superset Semantic Layer | Apache Superset's virtual dataset layer for metric definitions |
| Open Metadata Standards | Efforts like OpenLineage, OpenMetadata, and dbt Contracts to standardize metadata exchange |
| Conceptual Schema | Technology-agnostic representation of business concepts and their relationships |
| Domain Model | Model representing concepts, relationships, and rules within a specific business domain |
| Fact vs. Dimension (semantic) | Semantic layer concepts mapping to numerical metrics (facts) vs. descriptive attributes (dimensions) |

---

## 6. BI & Analytics

| Term | Full Form / Description |
|------|------------------------|
| OLAP | Online Analytical Processing — multi-dimensional analysis of business data for decision support |
| ROLAP | Relational OLAP — OLAP implemented on relational databases using SQL; no pre-aggregated cubes |
| MOLAP | Multidimensional OLAP — data stored in pre-aggregated multidimensional arrays; fast queries, less flexible |
| HOLAP | Hybrid OLAP — combines ROLAP and MOLAP; aggregates in multidimensional store, details in relational |
| Cube | Multi-dimensional data structure with pre-calculated aggregates along dimensions and hierarchies |
| MDX | MultiDimensional Expressions — query language for OLAP cubes (Microsoft Analysis Services, Essbase) |
| DAX | Data Analysis Expressions — formula language used in Power BI, Power Pivot, and SSAS Tabular models |
| Power Query / M | Microsoft's data transformation language and engine embedded in Power BI and Excel |
| Measure | Numeric value calculated in a BI context (sum, average, count); can be implicit or explicit |
| Dimension (BI) | Categorical attribute used to slice and filter measures (Time, Geography, Product) |
| Hierarchy | Ordered levels within a dimension enabling drill-down (Year > Quarter > Month > Day) |
| KPI | Key Performance Indicator — quantifiable metric reflecting critical business objectives |
| OKR | Objectives and Key Results — goal-setting framework pairing aspirational goals with measurable outcomes |
| Drill-Down | Navigating from a summary level to more detailed data (e.g., Year → Quarter → Month) |
| Drill-Up / Roll-Up | Aggregating detail data to a higher summary level |
| Drill-Through | Accessing underlying transaction-level detail records from a summarized BI view |
| Slice | Filtering a cube on one dimension to a specific value |
| Dice | Filtering a cube on multiple dimensions simultaneously |
| Pivot | Rotating a data table to exchange rows and columns for different analytical perspectives |
| Cross-Tab | Cross-tabulation — matrix display with row and column totals; pivot table equivalent |
| Scorecard | Dashboard presenting KPIs against targets, typically using RAG (Red/Amber/Green) status indicators |
| Dashboard | Visual display of key metrics and data visualizations for at-a-glance monitoring |
| Report | Structured presentation of data with filtering and formatting; less interactive than a dashboard |
| Ad Hoc Query | Unscheduled, user-defined query created on-demand to answer a specific business question |
| LOD | Level of Detail — Tableau expression type (FIXED, INCLUDE, EXCLUDE) for controlling aggregation scope |
| Table Calculation | Tableau calculations performed on the result set after aggregation, not on underlying data |
| Calculated Field | User-defined computed column or measure within a BI tool |
| Aggregation | Summarizing multiple rows into a single value (SUM, COUNT, AVG, MIN, MAX) |
| Running Total | Cumulative sum of a measure over an ordered dimension (e.g., year-to-date revenue) |
| YTD | Year-to-Date — cumulative value from the start of the fiscal/calendar year to current date |
| MTD | Month-to-Date — cumulative value from the start of the current month |
| QTD | Quarter-to-Date — cumulative value from the start of the current quarter |
| Period-over-Period | Comparing a metric in one period to the same metric in a prior period (YoY, MoM, WoW) |
| Time Intelligence | BI functions for date-based calculations (SAMEPERIODLASTYEAR, DATEADD in DAX) |
| Parameterized Report | Report with user-defined input parameters that filter or modify the output |
| Paginated Report | Fixed-layout, print-optimized report; suitable for invoices, statements, pixel-perfect output |
| Self-Service BI | BI tools enabling business users to create their own reports and analyses without IT assistance |
| Augmented Analytics | AI/ML-powered analytics that automates insight discovery, data preparation, and explanation |
| Natural Language Query | NLQ — querying data using plain language questions; enabled by NLP in BI tools |
| Embedded Analytics | BI capabilities integrated directly into business applications rather than standalone tools |
| Pixel-Perfect Reporting | Reports with precise layout control for printing; contrasted with interactive dashboards |
| Semantic Model | In Power BI, the dataset layer that defines measures, hierarchies, relationships, and row-level security |
| Tabular Model | Microsoft SSAS model type storing data in-memory in columnar format for fast DAX queries |
| Multidimensional Model | Microsoft SSAS model using MDX cubes with pre-aggregated measures |
| Composite Model | Power BI model combining DirectQuery and import sources in the same dataset |
| DirectQuery | Power BI/Tableau mode sending live queries to the source system; no local data import |
| Import Mode | Power BI mode that loads data into an in-memory columnar engine (VertiPaq) |
| VertiPaq | In-memory columnar storage engine powering Power BI's import mode |
| Tableau | Popular BI and data visualization platform known for drag-and-drop exploration |
| Looker | Google's data platform for BI with LookML semantic modeling |
| Power BI | Microsoft's BI suite including Desktop, Service, and Mobile components |
| MicroStrategy | Enterprise BI platform known for large-scale deployments and HyperIntelligence |
| Qlik | BI platform with associative data model engine (QlikView, Qlik Sense) |
| Superset | Apache Superset — open-source BI and data visualization platform |
| Metabase | Open-source BI tool designed for simplicity and self-service |
| Redash | Open-source data visualization and querying tool |
| Grafana | Open-source observability and visualization platform; strong for time-series and operational metrics |
| A/B Testing | Controlled experiment comparing two variants (A and B) to determine which performs better |
| Cohort Analysis | Analyzing behavior of groups of users who share a common characteristic at a point in time |
| Funnel Analysis | Tracking sequential steps users take toward a conversion goal |
| Retention Analysis | Measuring how many users return over time after initial engagement |
| Attribution Modeling | Assigning credit for a conversion to different marketing touchpoints |
| Segmentation | Dividing users or data into groups based on shared attributes for targeted analysis |

---

## 7. Cloud & Infrastructure

| Term | Full Form / Description |
|------|------------------------|
| MPP | Massively Parallel Processing — distributes query work across many nodes; core architecture of cloud warehouses |
| Columnar Storage | Data stored by column rather than row; dramatically improves analytical query performance and compression |
| Row-Based Storage | Traditional RDBMS storage; efficient for OLTP (full row access) but poor for analytical (column scans) |
| Compression Ratio | Measure of how much data is reduced by compression; columnar formats achieve much higher ratios than row-based |
| Data Skipping | Using metadata (min/max statistics, bloom filters) to skip irrelevant data files during query execution |
| Bloom Filter | Probabilistic data structure used to test whether an element is in a set; used in Parquet and Iceberg |
| Zone Maps | Column-level min/max statistics stored in file metadata for data skipping optimization |
| Open Table Format | Specification defining how data lake files are organized and queried with ACID support |
| Delta Lake | Linux Foundation open table format providing ACID transactions and schema enforcement on data lakes |
| Apache Iceberg | Open table format for huge analytic datasets with schema evolution and time travel |
| Apache Hudi | Hadoop Upserts Deletes and Incrementals — open table format with CDC and incremental processing |
| ACID | Atomicity, Consistency, Isolation, Durability — properties guaranteeing reliable database transactions |
| Atomicity | Transaction property: all operations succeed or none do; no partial updates |
| Consistency | Transaction property: database moves from one valid state to another |
| Isolation | Transaction property: concurrent transactions don't interfere with each other |
| Durability | Transaction property: committed transactions survive system failures |
| MVCC | Multi-Version Concurrency Control — allows concurrent reads and writes by maintaining multiple data versions |
| Time Travel | Ability to query data as it existed at a past point in time; supported by Delta Lake, Iceberg, Snowflake |
| Data Versioning | Tracking changes to datasets over time, enabling rollback and historical queries |
| Snapshot Isolation | Transaction isolation level where reads see a consistent snapshot of data at the transaction start time |
| Write-Ahead Log | WAL — transaction log written before data changes; enables crash recovery and CDC |
| Optimistic Concurrency | Allows multiple transactions to proceed without locking; checks for conflicts at commit time |
| Pessimistic Concurrency | Locks data resources during a transaction to prevent conflicts; reduces throughput |
| Manifest File | Metadata file in Iceberg/Delta that tracks which data files are part of a table snapshot |
| Transaction Log | Ordered record of all changes to a Delta Lake table; basis for ACID properties and time travel |
| Compaction | Process of merging many small files into fewer larger files to improve read performance |
| Small File Problem | Performance issue where too many small files cause excessive metadata overhead and slow queries |
| Auto-Optimize | Databricks feature that automatically compacts small files |
| Liquid Clustering | Databricks' dynamic, incremental replacement for static partition-based clustering |
| Copy-on-Write | Table format update strategy: rewrites entire data files on every update; better for read-heavy workloads |
| Merge-on-Read | Table format update strategy: writes delta files on update; merges at read time; better for write-heavy workloads |
| Serverless | Computing model where infrastructure management is abstracted away; auto-scales and billed per use |
| Elastic Scaling | Automatically adding or removing compute resources based on workload demand |
| Separation of Storage and Compute | Architecture where data storage and query compute scale independently; foundational to Snowflake, BigQuery |
| Virtual Warehouse | Snowflake's independent compute cluster that can be sized and scaled independently |
| Slot | BigQuery's unit of computational capacity; reserved or on-demand pricing |
| Redshift | Amazon Redshift — managed MPP data warehouse on AWS |
| BigQuery | Google BigQuery — serverless, multi-cloud data warehouse |
| Snowflake | Cloud data platform with separated storage and compute; supports multi-cloud deployment |
| Synapse Analytics | Azure Synapse Analytics — integrated analytics service combining data warehousing and big data |
| Databricks | Unified analytics platform built on Apache Spark; pioneered the Lakehouse concept |
| S3 | Amazon Simple Storage Service — object storage; de facto standard for data lake storage |
| ADLS | Azure Data Lake Storage — Microsoft's scalable object storage for analytics workloads |
| GCS | Google Cloud Storage — Google's object storage service |
| Object Storage | Storage model using objects with metadata and unique IDs; highly scalable, no hierarchy |
| Block Storage | Raw storage volumes (EBS, Azure Disks); low latency, used for databases |
| File Storage | Hierarchical filesystem-based storage (EFS, Azure Files, NFS) |
| Data Transfer Cost | Cloud charges for moving data between regions, availability zones, or out of cloud |
| Egress Cost | Charges for data transferred out of a cloud provider's network |
| Reserved Capacity | Pre-purchasing cloud compute/storage at discounted rates vs. on-demand pricing |
| Spot/Preemptible Instance | Unused cloud capacity sold at steep discount; can be interrupted; used for fault-tolerant batch jobs |
| VPC | Virtual Private Cloud — isolated network environment within a cloud provider |
| Private Link | Direct private network connection between services without traversing the public internet |
| IAM | Identity and Access Management — cloud service for managing authentication and authorization |
| Service Account | Non-human identity used by applications and services for authentication to cloud APIs |
| Encryption Key Management | KMS — managed service for creating and controlling encryption keys (AWS KMS, Azure Key Vault, GCP KMS) |
| Data Plane | The infrastructure layer that processes and stores actual data |
| Control Plane | The infrastructure layer managing metadata, configuration, and orchestration |
| Multi-Cloud | Strategy of using services from multiple cloud providers to avoid lock-in or optimize cost/capability |
| Hybrid Cloud | Combining on-premises infrastructure with public cloud services |
| Data Gravity | Tendency for data to attract applications and services; moving large datasets is expensive |
| Vendor Lock-In | Dependency on a single vendor's proprietary technology that makes migration costly |
| Open Standards | Non-proprietary specifications enabling interoperability (Parquet, Iceberg, OpenTelemetry) |
| Cost Allocation Tags | Cloud resource tags used for billing attribution by team, project, or environment |
| FinOps | Financial Operations — practice of managing cloud costs and optimizing cloud financial management |
| Infrastructure as Code | IaC — managing infrastructure through version-controlled configuration files (Terraform, Pulumi) |
| Terraform | HashiCorp's open-source IaC tool for provisioning cloud infrastructure |
| Docker | Container platform enabling consistent application packaging and deployment |
| Kubernetes | K8s — container orchestration system for automating deployment, scaling, and management |
| Helm | Package manager for Kubernetes applications |
| CI/CD | Continuous Integration/Continuous Delivery — automated build, test, and deployment pipelines |

---

## 8. Data Quality & Observability

| Term | Full Form / Description |
|------|------------------------|
| Data Quality | Degree to which data is fit for its intended use; measured across multiple dimensions |
| DQ Dimensions | Standard aspects of data quality: completeness, accuracy, consistency, timeliness, validity, uniqueness |
| Completeness | DQ dimension: percentage of required fields that contain values; no unexpected nulls |
| Accuracy | DQ dimension: data correctly reflects the real-world entity or event it describes |
| Consistency | DQ dimension: data values are consistent across systems and over time |
| Timeliness | DQ dimension: data is available when needed and reflects current reality |
| Validity | DQ dimension: data conforms to defined formats, ranges, and rules |
| Uniqueness | DQ dimension: no unintended duplicate records exist |
| Integrity | DQ dimension: referential and relational integrity is maintained across datasets |
| Conformity | DQ dimension: data adheres to specified data standards and formats |
| Data Anomaly | Unexpected deviation from normal data patterns; may indicate quality issues or real events |
| Anomaly Detection | Automated identification of unusual patterns in data (statistical, ML-based approaches) |
| Data Drift | Gradual change in data distribution over time that degrades model or report accuracy |
| Schema Drift | Unexpected changes to a data source's schema that break downstream pipelines |
| Data Observability | End-to-end visibility into data health including freshness, volume, schema, distribution, and lineage |
| Data Reliability | Consistent availability of high-quality, trustworthy data to consumers |
| Freshness | How recently data was updated; critical SLA for operational and real-time analytics |
| Volume Anomaly | Unexpected spike or drop in row counts, signaling ingestion or source issues |
| Distribution Shift | Change in statistical distribution of column values over time |
| Null Rate | Percentage of null values in a column; tracked as a quality and freshness indicator |
| Duplicate Rate | Percentage of duplicate records in a dataset |
| Data SLA | Service Level Agreement for data products defining freshness, completeness, and availability targets |
| Data Contract | Formal specification defining schema, semantics, and quality expectations between producer and consumer |
| Great Expectations | Open-source Python library for defining, documenting, and validating data quality expectations |
| dbt Tests | dbt's built-in and extensible data testing framework (not_null, unique, accepted_values, relationships) |
| Soda | Data quality platform for defining and running data checks across SQL and file sources |
| Monte Carlo | Data observability platform using ML to detect and alert on data quality issues |
| Bigeye | Data observability and monitoring platform with automated anomaly detection |
| Acceldata | Data observability and pipeline intelligence platform |
| MoD | Metrics on Data — tracking operational metrics (row count, null %, freshness) on datasets over time |
| Data Testing | Automated validation of data against defined expectations or business rules |
| Unit Test (data) | Testing individual transformation logic with known inputs and expected outputs |
| Integration Test (data) | End-to-end test validating that the complete pipeline produces correct results |
| Data Reconciliation | Comparing data between source and target systems to verify completeness and accuracy of transfers |
| Checksum | Hash value computed over data to verify integrity during transfer or storage |
| Row Count Validation | Comparing record counts between source and target as a basic completeness check |
| Referential Integrity | Constraint ensuring foreign key values exist in the referenced primary key table |
| Business Rule Validation | Testing data against domain-specific rules (e.g., order amount must be positive) |
| Statistical Process Control | SPC — applying statistical methods to monitor and control data quality over time |
| Control Chart | Visualization plotting quality metrics over time with upper/lower control limits |
| Data Profiling | Automated analysis of data to understand structure, completeness, distribution, and relationships |
| Column Statistics | Min, max, mean, median, standard deviation, null count computed per column |
| Cardinality Check | Validating the number of distinct values in a column against expectations |
| Pattern Matching | Validating that values conform to expected formats using regex (e.g., email, phone) |
| Range Check | Validating that numeric or date values fall within expected bounds |
| Cross-Field Validation | Validating relationships between multiple columns (e.g., end_date >= start_date) |
| Golden Record | The authoritative, trusted version of a master data entity after deduplication |
| Data Deduplication | Process of identifying and removing duplicate records from a dataset |
| Fuzzy Matching | Identifying similar (not exact) records using string distance algorithms |
| Record Linkage | Linking records across systems that refer to the same entity without a common identifier |
| Probabilistic Matching | Matching records using statistical likelihood scores across multiple attributes |
| Data Quality Score | Composite metric summarizing overall quality of a dataset across multiple dimensions |
| Data Health Dashboard | Centralized view of data quality metrics and SLA compliance across data assets |
| Alerting | Automated notifications when data quality metrics breach defined thresholds |
| Root Cause Analysis | Systematic process for identifying the underlying cause of a data quality issue |
| Incident Management | Process for tracking, escalating, and resolving data quality incidents |
| Data Debugging | Tracing data issues through pipelines using lineage and observability tools |

---

## 9. Emerging Concepts

| Term | Full Form / Description |
|------|------------------------|
| Data Mesh | Decentralized data architecture treating data as a product, owned by domain teams, with federated governance |
| Data Product | A self-contained, discoverable, addressable, trustworthy, and interoperable data asset served by a domain team |
| Domain Ownership | Data Mesh principle: teams closest to the data own its quality, availability, and access |
| Data as a Product | Data Mesh principle: applying product thinking (SLAs, discoverability, documentation) to data assets |
| Self-Serve Data Platform | Data Mesh principle: infrastructure platform enabling domain teams to build and serve data products independently |
| Federated Computational Governance | Data Mesh principle: global policies enforced through automated platforms rather than central data teams |
| DataOps | Agile methodology applying DevOps principles to data engineering; emphasizes automation, collaboration, and quality |
| MLOps | Machine Learning Operations — practices for deploying, monitoring, and maintaining ML models in production |
| LLMOps | Practices for deploying and managing Large Language Model applications in production |
| ModelOps | Operationalizing all types of AI/ML models including statistical, ML, and deep learning models |
| Feature Store | Centralized repository for storing, sharing, and serving ML features for training and inference |
| Feature Engineering | Transforming raw data into features (input variables) that improve ML model performance |
| Feature Serving | Providing low-latency access to ML features for real-time model inference |
| Online Store | Feature store layer for low-latency feature retrieval for real-time inference (e.g., Redis) |
| Offline Store | Feature store layer for high-throughput feature retrieval for batch training (e.g., S3, BigQuery) |
| Training-Serving Skew | Discrepancy between features used in model training vs. what's served in production; major ML risk |
| Model Registry | Versioned repository for storing, tracking, and managing ML model artifacts |
| Experiment Tracking | Recording hyperparameters, metrics, and artifacts from ML training runs (MLflow, W&B) |
| MLflow | Open-source platform for managing the end-to-end ML lifecycle |
| Kubeflow | Kubernetes-native platform for deploying and managing ML workflows |
| Vector Database | Database optimized for storing and querying high-dimensional embedding vectors (Pinecone, Weaviate, Qdrant) |
| Embedding | Dense numerical vector representation of data (text, images, audio) capturing semantic meaning |
| RAG | Retrieval-Augmented Generation — LLM pattern that retrieves relevant context from a knowledge base before generating responses |
| Semantic Search | Finding results based on meaning/intent rather than exact keyword matching; uses vector similarity |
| ANN | Approximate Nearest Neighbor — algorithms for finding similar vectors efficiently (HNSW, IVF) |
| HNSW | Hierarchical Navigable Small World — graph-based algorithm for fast ANN search in vector databases |
| Cosine Similarity | Metric measuring the angle between two vectors; common similarity measure for embeddings |
| Fine-Tuning | Adapting a pre-trained LLM to a specific task by training on domain-specific data |
| Prompt Engineering | Designing effective prompts to get desired outputs from LLMs without changing model weights |
| LLM | Large Language Model — deep learning model trained on massive text datasets for NLP tasks (GPT-4, Claude) |
| Foundation Model | Large pre-trained model serving as a base that can be fine-tuned for specific tasks |
| Data Lakehouse | Architecture merging data lake flexibility with warehouse structure and ACID transactions |
| Open Lakehouse | Lakehouse built on open standards (Iceberg, Delta, Parquet) without vendor lock-in |
| Streaming Lakehouse | Real-time streaming ingestion and processing directly on lakehouse table formats |
| Data Fabric | AI-driven architecture providing automated, intelligent data management across heterogeneous environments |
| Knowledge Fabric | Evolution of data fabric incorporating semantic knowledge graphs and ontologies |
| Semantic Data Fabric | Data fabric with rich semantic metadata enabling context-aware data discovery and access |
| Active Metadata | Metadata that drives automated actions such as data quality checks, routing, or lineage tagging |
| Augmented Data Management | Using AI/ML to automate metadata management, data quality, and governance tasks |
| Generative AI for Data | Using LLMs for automated SQL generation, data documentation, anomaly explanation, and data exploration |
| Text-to-SQL | LLM capability to convert natural language questions into executable SQL queries |
| Data Contract (modern) | Machine-readable schema + quality + SLA agreement between producers and consumers; versioned and enforced |
| Open Data Contract Standard | ODCS — open specification for data contracts enabling interoperability between governance tools |
| Soda Core | Open-source data quality CLI tool supporting data contracts and checks |
| Streaming SQL | Writing streaming data pipelines using familiar SQL syntax (Flink SQL, ksqlDB, Apache Calcite) |
| ksqlDB | SQL streaming engine built on top of Apache Kafka |
| Materialize | Streaming database maintaining incrementally-updated materialized views from streaming sources |
| RisingWave | Cloud-native streaming database with PostgreSQL-compatible SQL |
| Reverse ETL | Syncing processed data warehouse data back into operational tools (CRM, marketing automation) |
| Operational Analytics | Analytics performed on operational data with low latency; bridges BI and operational systems |
| Unified Data Platform | Single platform combining data engineering, warehousing, analytics, and ML (Databricks, Snowflake) |
| Iceberg REST Catalog | Open REST API specification for interacting with Iceberg catalogs; enables multi-engine access |
| Apache Polaris | Open-source Iceberg catalog supporting the Iceberg REST Catalog spec |
| Apache Gravitino | Open-source unified metadata lake for managing metadata across heterogeneous data sources |
| Nessie | Open-source catalog with Git-like version control for Iceberg and Delta tables |
| Table Format Wars | Industry competition between Delta Lake, Apache Iceberg, and Apache Hudi for open table format dominance |
| UniForm | Databricks feature allowing Delta Lake tables to be read as Iceberg or Hudi tables |
| DeltaSharing | Open protocol for securely sharing live data across organizations without copying |
| Apache Arrow | In-memory columnar data format enabling zero-copy reads across different runtimes |
| Apache Arrow Flight | RPC framework for high-speed data transfer using Arrow format |
| ADBC | Arrow Database Connectivity — Arrow-native replacement for JDBC/ODBC for analytical workloads |
| Ibis | Python dataframe library with multiple backends (DuckDB, BigQuery, Spark) using the same API |
| DuckDB | Embeddable in-process OLAP database; fast analytics on local files without a server |
| MotherDuck | Serverless cloud DuckDB with collaboration features |
| Data Clean Room | Secure environment where multiple parties can analyze combined data without exposing raw data |
| Privacy-Enhancing Technologies | PETs — techniques (differential privacy, homomorphic encryption, secure MPC) for analyzing sensitive data safely |
| Differential Privacy | Mathematical framework adding calibrated noise to query results to protect individual privacy |
| Federated Learning | ML training across distributed data without centralizing the data; preserves privacy |
| Synthetic Data | Artificially generated data statistically similar to real data; used for testing and privacy compliance |
| Data Tokenomics | Emerging concept of data as an economic asset with pricing, ownership, and exchange mechanisms |
| DataOps Manifesto | Published principles for applying DevOps practices to data management |
| Continuous Integration (Data) | Automatically testing data pipeline code changes and data quality before merging to production |
| Continuous Delivery (Data) | Automatically deploying validated data pipeline changes to production environments |
| Infrastructure as Code (Data) | Managing data infrastructure, pipelines, and schemas through version-controlled code |
| Data Version Control | DVC — open-source tool for versioning datasets and ML models alongside code |
| dbt Cloud | Managed cloud service for running dbt transformations with scheduling and CI/CD |
| Git-based Workflows | Managing data pipeline code with Git for version control, branching, and code review |
| Blue-Green Deployment (Data) | Maintaining two identical environments to enable zero-downtime pipeline deployments |
| Canary Deployment (Data) | Gradually rolling out pipeline changes to a subset of users/data before full rollout |
| Schema Migration | Versioned, automated process for evolving database schemas in a controlled way |
| Data Incident | Event where data quality, availability, or security degrades below acceptable thresholds |
| SRE for Data | Applying Site Reliability Engineering principles to data systems for improved reliability |
| Data Engineering | Discipline focused on designing, building, and maintaining data infrastructure and pipelines |
| Analytics Engineering | Discipline at the intersection of data engineering and analysis; owns the transformation layer (dbt) |
| Data Platform Engineering | Building self-serve internal data infrastructure and tooling for data teams |
| Data as Code | Treating data assets (schemas, pipelines, quality rules) with software engineering rigor |
