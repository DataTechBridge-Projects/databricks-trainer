# Retail Banking Products & Data Flows

## Overview

Retail banking is the most recognizable segment of the financial industry — it is the bank branch on the high street, the mobile app, the credit card statement. For a Data SA, retail banking is also the segment with the highest transaction volume, the richest behavioral data, and the most mature regulatory requirements around customer data.

Understanding retail banking products matters because each product generates a distinct data shape and sits at a different stage of the customer lifecycle. When a bank says "we want a 360-degree customer view," they mean they want all of these product data streams joined together on a single customer identity.

## Core Retail Banking Products

### Current / Checking Accounts
The primary transaction account. Every debit card purchase, direct debit, standing order, and bank transfer flows through here. This is the highest-frequency data source in retail banking — a mid-size bank processes millions of transactions per day.

**Data characteristics:** High volume, append-only transaction ledger, real-time fraud scoring required, regulatory retention typically 7 years.

### Savings & Deposit Accounts
Interest-bearing accounts where customers hold idle cash. Lower transaction frequency than current accounts but critical for liability management (banks use deposit data to model how much cash they need on hand).

**Data characteristics:** Lower volume, interest accrual calculations run nightly batch, customer lifetime value modeling depends heavily on deposit balances.

### Mortgages & Home Loans
Long-tenure secured loans (15–30 years) collateralized by property. Origination generates a large documentation data payload (income verification, credit check, property valuation). Post-origination, the data is relatively quiet — monthly repayments, occasional restructuring events.

**Data characteristics:** Document-heavy at origination (unstructured + structured), long retention requirement, credit risk models need property value feeds and macroeconomic data as inputs.

### Personal Loans & Auto Loans
Unsecured or asset-backed consumer lending. Shorter tenure than mortgages (1–7 years). Higher interest rates, higher default risk. Origination is heavily automated via credit scoring pipelines.

**Data characteristics:** Credit bureau data ingestion at origination, behavioral scoring during the loan lifecycle (early arrears signals), collections workflow data at end of life.

### Credit Cards
Revolving credit product. Generates the richest behavioral data in retail banking — every merchant, every purchase category, every repayment behavior is recorded. The basis for most retail banking fraud models and customer segmentation.

**Data characteristics:** High cardinality transaction data (merchant codes, geolocation, device), near-real-time fraud scoring (milliseconds), spend analytics, authorization vs. settlement reconciliation.

## The Retail Banking Data Lifecycle

```
Customer Onboarding → Product Application → Account Opening → Transacting → Servicing → Retention/Churn
       ↓                      ↓                   ↓               ↓              ↓              ↓
   KYC/AML data          Credit decision       Core banking     Ledger data    Call center    ML churn
   Identity docs          Bureau data          system record    Card txns      CRM events     scoring
```

## Key Data Domains in Retail Banking

| Domain | What it contains | Why it matters to SAs |
|--------|-----------------|----------------------|
| **Customer Master** | Name, address, identity documents, relationship history | The glue between all product data — entity resolution is hard when customers exist across 5+ systems |
| **Transaction Ledger** | Every debit/credit event with timestamp, amount, counterparty | Source of truth for balance calculations, fraud, and regulatory reporting |
| **Product Register** | All open accounts/loans/cards with their terms | Needed for customer 360, regulatory reporting (CCAR, stress testing) |
| **Credit Bureau Data** | External credit scores and tradelines ingested at origination | Third-party data — refresh cadence and licensing matter for data architecture |
| **Behavioral / Interaction Data** | Mobile app events, branch visits, call center logs | Powers personalization and churn models — typically lives in a separate digital data layer |

## Common Customer Problems You Will Hear

**"We can't join our mortgage data with our current account data"**
Classic multi-system problem. Core banking system for deposits, a loan origination system for mortgages, a card processing platform for credit cards — each with its own customer ID. The data platform needs a master data management or entity resolution layer.

**"Our fraud model is reacting too slowly"**
Batch fraud scoring (run overnight) catches fraud after the fact. The ask is to move to real-time feature computation on the transaction stream. This is a streaming pipeline + ML feature store conversation.

**"We need to report all transactions over €10,000 to the regulator by 9am"**
AML transaction monitoring. The data pipeline needs to be reliable, fast, and have clear lineage so the compliance team can explain exactly where each number came from.

**"We want to show customers their spending insights in the app"**
Merchant category enrichment + near-real-time aggregation. Requires transaction data to be available to the API layer within seconds of the transaction being posted.

## What "Real-Time" Actually Means Here

Retail banking has several distinct latency tiers — make sure you clarify with the customer which one they mean:

| Tier | Latency | Use case |
|------|---------|----------|
| **Authorization-time** | < 200ms | Fraud scoring on card swipe |
| **Near-real-time** | Seconds to minutes | Spending notifications, balance updates |
| **Intraday batch** | Every 1–4 hours | Risk dashboards, treasury position |
| **End-of-day batch** | Overnight | Regulatory reporting, interest accrual, GL reconciliation |
