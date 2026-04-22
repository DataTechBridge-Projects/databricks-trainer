# Core Banking Systems & Data Architecture

## Overview

Core banking systems are the operational backbone of a bank — the system of record for accounts, transactions, and customer relationships. Understanding what they are, why they are so hard to replace, and how data flows out of them is essential for any Data SA working in BFSI.

Most data platform conversations in banking start with the question: "how do we get data out of the core banking system in a way that is reliable, timely, and doesn't break the bank's operations?" The answer to that question shapes the entire data architecture.

## What Is a Core Banking System?

A core banking system (CBS) is the central software that processes all financial transactions and maintains the ledger — the definitive record of every account balance and every transaction that moved money. All channels (branch, ATM, mobile app, internet banking) ultimately post transactions to the core banking system.

**Key functions of a core banking system:**
- Account management (opening, maintenance, closure)
- Transaction processing and posting
- Interest calculation and accrual
- Regulatory balance reporting (end-of-day positions)
- General ledger (GL) interface — feeding the bank's financial accounting system

### Major Core Banking Vendors

| Vendor | Product | Common in |
|--------|---------|-----------|
| **Temenos** | T24 / Transact | Tier 2 and 3 banks globally |
| **FIS** | Profile, Modern Banking Platform | US and global |
| **Finastra** | Fusion Equation, Kondor | Global |
| **Mambu** | Cloud-native SaaS | Fintechs, challenger banks, modernizing banks |
| **Thought Machine** | Vault Core | Cloud-native, newer entrants |
| **Finacle (Infosys)** | Finacle | Asia, Africa, India |
| **In-house systems** | Bespoke COBOL | Many large banks still run mainframe-era custom systems |

## Why Core Banking Is So Hard to Replace

The core banking system is the most mission-critical piece of software a bank runs. A 30-minute outage during business hours is front-page news and regulatory scrutiny. A failed migration can bring down the bank.

**The migration problem:**
- Decades of transaction history must be migrated accurately
- Thousands of downstream systems have integrations built against the existing CBS
- The CBS cannot be switched off — migrations must run in parallel, with a cutover during a very tight window
- Any data discrepancy between old and new systems is a regulatory and audit problem

This is why many banks have been "planning to replace the core banking system" for 20+ years and still haven't. The data risk alone is enormous.

**The practical implication for Data SAs:** Most customers are not replacing their core banking system — they are building a data layer *around* it. Your job is to extract data from the CBS reliably, not to replace it.

## How Data Flows Out of Core Banking

### End-of-Day Batch Extracts
The traditional approach. At end of business, the CBS produces flat files (fixed-width or CSV) containing the day's transactions and current account balances. These are loaded into a data warehouse overnight.

**Problems:** 24-hour latency, brittle file-based integrations, no history of intraday state, schema changes in the CBS break the extract.

### Database Replication
Directly replicating the CBS database to a read replica or staging environment. Some CBS vendors support this; others do not, or require significant licensing.

**Problems:** The CBS data model is often highly normalized and difficult to query. The schema is vendor-specific and may not be documented. Tightly coupled to the CBS vendor's internal data structure.

### Change Data Capture (CDC)
Capturing every change to the CBS database in real time as it happens, by reading the database transaction log. Tools like Debezium, Oracle GoldenGate, or AWS DMS enable this pattern.

**This is the gold standard for modern data ingestion from core banking.** CDC provides:
- Near-real-time data availability (seconds of latency)
- Complete change history (not just current state)
- Low impact on the CBS itself (reads the log, not the primary database)
- Exactly-once delivery semantics when implemented correctly

### API / Event Bus
Modern cloud-native core banking systems (Mambu, Thought Machine Vault) expose event streams and APIs natively. Every transaction is an event published to a message broker (Kafka) that downstream systems can consume.

**This is the ideal architecture** but only available for banks that have already modernized or deployed a new CBS. The majority of banks are still working with legacy systems.

## The Typical BFSI Data Architecture

Even without a core banking replacement, most banks evolve toward a similar data architecture:

```
Core Banking System (CBS)
        ↓ (CDC / batch extract)
    Staging / Landing Zone (raw data, immutable)
        ↓
    Integration Layer (cleanse, standardize, apply business rules)
        ↓
    Enterprise Data Warehouse / Data Lakehouse
        ↓                    ↓                    ↓
  Regulatory Reporting   Risk Analytics     Customer 360
  (overnight batch)      (intraday)         (real-time)
```

Around this core flow, there are dozens of other source systems feeding in:
- Loan origination systems (LOS)
- Card processing platforms (often third-party, e.g., FIS, Worldline)
- CRM systems (Salesforce, Microsoft Dynamics)
- Trading systems (Bloomberg, Murex, Calypso)
- Market data vendors (Refinitiv, Bloomberg)
- Insurance policy administration systems
- Regulatory reference data (LEI, ISIN, MCC codes)

## Data Management Concepts That Come Up in Every BFSI Conversation

### Golden Source / Single Source of Truth
Which system is authoritative for a given data element? If the CBS says the balance is £100 and the data warehouse says £102, which is right? Establishing golden sources and ensuring downstream systems match them is a fundamental data governance exercise.

### Data Lineage
The ability to trace a number in a report back to the source transaction that caused it. Required by BCBS 239, auditors, and regulators. Modern data platforms with built-in lineage (e.g., Apache Atlas, dbt with metadata, Databricks Unity Catalog) satisfy this requirement.

### Data Quality & Reconciliation
Financial data must balance. The sum of all account balances must equal the general ledger. The sum of all card transaction settlements must match the payment network's settlement file. Automated reconciliation jobs that detect and alert on breaks are a non-negotiable part of BFSI data pipelines.

### Data Retention & Archival
Regulatory requirements typically mandate:
- Transaction data: 7–10 years
- AML investigation records: 5–7 years
- Trade records (MiFID II): 7 years
- Pension member records: potentially lifetime + 6 years

Cost-effective tiered storage (hot/warm/cold) is important for very large historical datasets.

### Point-in-Time Query
The ability to answer "what was the state of X on date Y?" — essential for audits, disputes, regulatory inquiries, and backtesting. Requires temporal data modeling (SCD Type 2 or event sourcing patterns). Not all data warehouses support this well; it must be designed in.

## Common Customer Problems You Will Hear

**"Our core banking vendor is charging us a fortune for data access"**
Some CBS vendors charge separately for data extracts or API access. A CDC-based approach reading the database log directly can bypass this, but requires careful discussion with the vendor about licensing.

**"We can't reconcile our CBS data with our downstream data warehouse"**
Data is lost or transformed in the ETL layer without proper lineage tracking. Implementing CDC with immutable raw staging and clear transformation lineage solves this.

**"We want to migrate to a cloud-native core banking system"**
This is a major, multi-year programme. The data workstream includes: full historical data migration, parallel-run reconciliation, cutover data validation, and ensuring all downstream data consumers are re-pointed. This is a significant data engineering engagement.

**"We have 40 different systems and no one knows where the customer master data lives"**
Classic enterprise data management problem in banking. The answer is a master data management (MDM) initiative — establishing a golden source customer record and propagating it. A data catalog and data lineage tool help map what exists before you start.
