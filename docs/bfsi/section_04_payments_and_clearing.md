# Payments & Clearing

## Overview

Payments is the plumbing of the financial system. Every time money moves — a card tap at a coffee shop, a payroll run, an international wire — it travels through a payments infrastructure made up of payment rails, clearing houses, and settlement systems. For a Data SA, payments is important because it generates some of the highest-volume, most latency-sensitive data in all of BFSI.

The payments landscape is also undergoing rapid change. The shift from batch overnight settlement to real-time payment (RTP) rails in most major markets means that data architectures built for end-of-day batch processing are being replaced with streaming-first designs.

## How Payments Work: The Core Concepts

### The Payment Journey
Every payment has three logical phases:

1. **Initiation** — The payer instructs their bank to send money (via card swipe, bank transfer, direct debit mandate)
2. **Clearing** — The payment message is exchanged between the paying bank and the receiving bank through a central clearing house or bilateral agreement
3. **Settlement** — The actual movement of funds between bank accounts at the central bank (or a correspondent bank) — this is where money actually changes hands

Clearing and settlement used to happen once per day. Real-time payment rails have collapsed this to seconds.

### Gross vs. Net Settlement
- **Gross settlement (RTGS):** Each payment settles individually and immediately. Used for high-value payments (central bank systems like Fedwire, CHAPS, TARGET2). Eliminates settlement risk but requires banks to hold more liquidity.
- **Net settlement:** Thousands of payments are accumulated and netted — only the net position between banks is settled at end of day. Used for card networks, ACH, BACS. More capital-efficient but introduces intraday settlement risk.

## Major Payment Rails

| Rail | Region | Type | Use case |
|------|--------|------|----------|
| **SWIFT** | Global | Messaging network | Cross-border bank transfers (not a settlement system — just the messaging layer) |
| **SEPA** (SCT, SCT Inst) | EU | Credit transfer | EUR payments within Europe; Inst = real-time |
| **Faster Payments / FPS** | UK | Real-time | Account-to-account payments, 24/7 |
| **ACH / Nacha** | USA | Batch net settlement | Payroll, direct debits |
| **FedNow** | USA | Real-time | Launched 2023 — US real-time payment rail |
| **UPI** | India | Real-time | Unified Payments Interface — world's largest RTP volume |
| **Visa / Mastercard** | Global | Card network | Authorization, clearing, and settlement for card payments |
| **CHAPS** | UK | RTGS gross | High-value same-day GBP settlements |

## Card Payments: The Data Flow

Card payments have their own ecosystem worth understanding separately because of their data richness and the number of parties involved.

```
Cardholder → Merchant → Acquirer → Card Network (Visa/MC) → Issuer → Cardholder's account
```

**Key data events:**
- **Authorization:** Real-time approval (< 200ms). Fraud model fires here. Authorization data includes merchant category code (MCC), amount, card BIN, terminal ID, geolocation.
- **Clearing:** Next-day batch. Full transaction detail is exchanged between acquirer and card network.
- **Settlement:** Funds move from the issuer's settlement account to the acquirer's account via the card network.
- **Reconciliation:** The merchant reconciles what was authorized vs. what was settled, and disputes any gaps (chargebacks).

**Data SA note:** Authorization data and settlement data are different records that must be reconciled. They travel on different timelines and often live in different systems. Reconciliation discrepancies are a real data quality problem.

## ISO 20022: The New Payment Data Standard

ISO 20022 is a global messaging standard that is replacing older formats (SWIFT MT, BACS, SEPA legacy) across virtually every major payment rail. The migration is largely complete or underway in most markets.

**Why it matters for data architects:**
- ISO 20022 messages carry significantly richer data than the formats they replace — full remittance information, LEI codes, purpose codes, and structured address fields
- This richer data enables better fraud detection, AML screening, and straight-through processing
- Banks migrating to ISO 20022 need to transform their data pipelines to parse and store the new message format while maintaining backwards compatibility with legacy systems

## Payment Data Characteristics

| Characteristic | Detail |
|---------------|--------|
| **Volume** | Top-tier banks process millions of transactions per day across all rails |
| **Latency requirement** | Fraud scoring at authorization: < 200ms. Real-time payment notification: seconds. |
| **Retention** | Typically 7–10 years for regulatory purposes |
| **Sensitivity** | Account numbers, sort codes, beneficiary details — all PII or financially sensitive |
| **Format variety** | SWIFT MT, ISO 20022 XML, fixed-width flat files, JSON APIs — all from different rails |

## Common Customer Problems You Will Hear

**"We need real-time fraud detection on payments"**
The bank is processing payments through a batch pipeline. The ask is to move authorization-time scoring to a streaming architecture with a sub-200ms response. This is a Kafka/Flink + ML feature store conversation.

**"We can't reconcile our card settlement data with our authorization data"**
Authorization and settlement records are on different systems, different formats, different timelines. A unified data platform with a payment reconciliation data model solves this.

**"We're migrating to ISO 20022 and need to transform our pipeline"**
Schema transformation at ingestion — the new richer fields need to be parsed, mapped to the internal data model, and made available to downstream consumers (fraud, AML, reporting) without disrupting existing flows.

**"We want to give customers real-time payment notifications"**
Payment events need to be available to the customer-facing API within seconds of posting. This is a streaming pipeline with a low-latency serving layer (e.g., a key-value store or stream-to-API pattern).

**"We process payments in 12 countries and can't see our total flow"**
Multi-region payment data consolidation. Different currencies, different rails, different formats — the data platform needs currency normalization, timezone handling, and a unified payment data model.
