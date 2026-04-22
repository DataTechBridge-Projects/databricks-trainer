# BFSI Industry Overview for Data Solution Architects

## Overview

Banking, Financial Services, and Insurance (BFSI) is one of the most data-intensive industries on the planet. Every transaction, trade, policy, claim, and customer interaction produces structured and unstructured data — and regulators demand that most of it be retained, auditable, and reportable for years. This is the industry where data platforms win or lose on trust, latency, compliance, and scale simultaneously.

As a Data Solution Architect, your job is not to become a banker. Your job is to understand *why* the data exists, *who* depends on it, and *what happens if it's wrong or late*. A 30-minute payment delay in retail banking is a customer complaint. In capital markets, a 30-millisecond delay in trade data is a P&L event.

This course covers the major segments of BFSI, the data that flows through each, and how a modern data platform (cloud data warehouse, lakehouse, streaming pipeline) maps onto real financial business problems.

## The Major Segments

### Retail Banking
Consumer-facing banking: checking accounts, savings, mortgages, personal loans, credit cards. Highest data volume by transaction count. Key data concerns: fraud detection, 360-degree customer view, regulatory reporting (AML, KYC), and personalization.

### Corporate & SME Banking
Banking services for businesses: trade finance, cash management, treasury, FX, working capital lending. Data is lower volume but higher value per record. Key concerns: counterparty risk, real-time cash position, covenant monitoring.

### Capital Markets
Trading of equities, fixed income, derivatives, and commodities. Extremely latency-sensitive. Generates massive tick data volumes. Key concerns: trade surveillance, P&L calculation, risk exposure, regulatory reporting (MiFID II, Dodd-Frank).

### Insurance (P&C and Life)
Property & Casualty covers cars, homes, commercial property. Life covers mortality, health, and long-term savings. Data concerns: underwriting (pricing risk), claims processing, fraud detection, and actuarial modeling.

### Wealth & Asset Management
Investment advisory and portfolio management for individuals and institutions. Data concerns: portfolio performance, fee calculation, regulatory suitability reporting, client onboarding (KYC).

### Retirement & Pensions
Defined benefit (DB) and defined contribution (DC) pension schemes. Long-horizon data — participant records may span 40+ years. Key concerns: actuarial valuation, benefit calculation, regulatory reporting, and member communication. Covered in detail in Section 09.

## Why BFSI Is Different for Data Architects

| Dimension | What it means for your data platform |
|-----------|--------------------------------------|
| **Regulation** | Data lineage, auditability, and retention are non-negotiable. GDPR, BCBS 239, MiFID II, Solvency II all impose specific data requirements |
| **Latency spectrum** | Same institution may need millisecond streaming (fraud) and overnight batch (regulatory reports) — both on the same data |
| **Data sensitivity** | PII, financial transaction data, and health data (for insurance) all co-exist — fine-grained access control is essential |
| **Legacy systems** | Most banks run 20-40 year old core banking systems. Your platform must ingest from mainframes and flat files, not just modern APIs |
| **M&A complexity** | Banks acquire other banks. Data consolidation across incompatible systems is a recurring workload |

## Key Regulatory Bodies & Frameworks to Know

| Framework | Region | Relevance to Data |
|-----------|--------|-------------------|
| **BCBS 239** | Global (Basel Committee) | Defines standards for risk data aggregation — directly drives data architecture decisions at large banks |
| **MiFID II** | EU | Requires trade reporting, best execution data, and transaction record-keeping for capital markets |
| **GDPR / CCPA** | EU / California | Right to erasure and data minimization — conflicts with long retention requirements, must be designed for |
| **AML / KYC** | Global | Anti-money laundering and Know Your Customer — requires transaction monitoring pipelines and entity resolution |
| **DORA** | EU (from 2025) | Digital Operational Resilience Act — imposes data recovery and incident reporting requirements on financial firms |
| **Solvency II** | EU | Insurance capital requirements — drives actuarial data models and reporting pipelines |

## How Data Platforms Map to BFSI Value

The conversation you will have with most BFSI customers is not "what is a data lakehouse." It is one of these:

- **"We can't produce our regulatory report on time"** → Data lineage, orchestration, and governed data products
- **"We have fraud losses we can't explain"** → Real-time streaming + ML feature store
- **"Our risk team can't see our exposure across all our books"** → Data consolidation, semantic layer, single source of truth
- **"We're migrating off our mainframe"** → CDC ingestion, schema mapping, parallel-run validation
- **"We acquired a bank and need to merge data"** → Data catalog, entity resolution, master data management

Knowing which segment your customer is in tells you which of these conversations you are about to have.
