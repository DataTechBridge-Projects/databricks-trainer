# Corporate & SME Banking

## Overview

Corporate and SME banking serves businesses rather than individuals. The products are structurally similar to retail — loans, accounts, payments — but the scale per customer is orders of magnitude larger, the relationships are more complex, and the data is richer with counterparty and contractual detail.

A mid-market corporate customer might have a revolving credit facility, multiple foreign currency accounts, trade finance instruments, interest rate swaps, and a cash pooling arrangement — all generating data that needs to be consolidated into a single relationship view so the bank can manage its exposure and the relationship manager can have an informed conversation.

For Data SAs, corporate banking is interesting because the data volumes are lower but the data *complexity* is higher. Getting the data model right matters more than getting the pipeline throughput right.

## Core Corporate Banking Products

### Commercial Loans & Credit Facilities
Term loans and revolving credit facilities (RCFs) to businesses. An RCF works like a corporate credit card — the customer can draw down and repay within an agreed limit. Banks track utilization daily to manage their capital requirements.

**Data characteristics:** Covenant tracking (financial ratios the borrower must maintain), drawdown and repayment events, collateral register, credit rating changes.

### Cash Management & Transaction Banking
The operational banking services that keep a business running day-to-day: business current accounts, payroll processing, supplier payments, and collections. This is the "sticky" product — once a corporate's ERP system is integrated with the bank's payment rails, switching is painful.

**Data characteristics:** High-value, lower-frequency transactions compared to retail. SWIFT message data (MT/MX formats), virtual account structures, intraday liquidity reporting.

### Trade Finance
Products that facilitate international trade: Letters of Credit (LC), Documentary Collections, Bank Guarantees, and Supply Chain Finance. Each instrument involves multiple parties (importer bank, exporter bank, shipping company) and has a document-heavy lifecycle.

**Data characteristics:** Unstructured document data (bills of lading, invoices), multi-party workflows, sanctions screening at every step, long settlement cycles (30–120 days).

### Foreign Exchange (FX) & Treasury
Banks offer FX conversion and hedging products (spot, forward, options) to help corporates manage currency risk. Treasury products extend to interest rate swaps and commodity hedging.

**Data characteristics:** Market data dependency (real-time FX rates), trade blotter, mark-to-market valuations, counterparty exposure netting.

### Supply Chain Finance (SCF)
The bank sits between a large buyer and its suppliers, paying suppliers early (at a discount) and collecting from the buyer on the original invoice due date. Also called "reverse factoring."

**Data characteristics:** Invoice data ingestion from buyer ERP systems, dynamic discounting calculations, supplier onboarding data.

## Key Data Challenges in Corporate Banking

### Counterparty Hierarchy
A corporate customer is rarely a single legal entity — it is a group of subsidiaries, holding companies, and special purpose vehicles. The bank needs to understand the *legal entity hierarchy* to correctly aggregate exposure across the group.

This is a graph data problem. Banks use Legal Entity Identifier (LEI) data from GLEIF as a reference dataset to map corporate structures.

### Covenant Monitoring
A loan agreement typically requires the borrower to maintain certain financial ratios (e.g., Debt/EBITDA < 4x). The bank needs to ingest the borrower's financial statements periodically and compute whether covenants are being met. Breach triggers an early warning process.

**SA conversation:** This is often a manual Excel-based process the bank wants to automate — a clear data pipeline + rules engine opportunity.

### Intraday Liquidity
Regulators (BCBS 248) require large banks to monitor and report their intraday liquidity position in near-real-time. The bank needs to aggregate all expected inflows and outflows across all nostro accounts throughout the day.

This is a genuine streaming + real-time aggregation problem. Banks that are still doing this in batch are out of compliance.

### KYC for Corporates (KYB)
Know Your Business (KYB) is more complex than retail KYC. The bank must verify the beneficial owners (any individual with >25% ownership), directors, and the legitimacy of the business. For a multinational with a complex holding structure, this is a multi-week data gathering exercise.

**Data platform angle:** Entity resolution, document management, and workflow orchestration — a good opportunity for graph databases and document AI.

## Data Sources Unique to Corporate Banking

| Source | What it contains |
|--------|-----------------|
| **SWIFT Network** | Interbank payment messages (MT103, MT202, ISO 20022 MX format) |
| **GLEIF / LEI Registry** | Legal entity hierarchy and ownership data |
| **ERP Integration** | SAP/Oracle financial data from corporate customers (for SCF and covenant monitoring) |
| **Credit Rating Agencies** | Moody's, S&P, Fitch ratings and watch-list changes |
| **Trade Registries** | Company filings, director data, UBO (Ultimate Beneficial Owner) data |

## Common Customer Problems You Will Hear

**"Our relationship managers don't have a single view of the client"**
Data is spread across a loan origination system, a treasury system, a trade finance platform, and the CRM. A data platform with a consolidated client data model and semantic layer solves this.

**"We're failing our intraday liquidity reporting"**
A batch-based data architecture cannot support intraday liquidity monitoring. The conversation is about streaming ingestion from payment systems and real-time aggregation.

**"Our covenant monitoring is manual and we miss breaches"**
An opportunity for a data pipeline that ingests borrower financials (structured or unstructured) and runs covenant calculations automatically, with alerting.
