# Risk, Compliance & Regulatory Reporting

## Overview

Risk and compliance is not a department at a bank — it is woven into every product, every transaction, and every data pipeline. Regulators worldwide have made it clear that the quality of a bank's data is as important as the quality of its capital. BCBS 239, the Basel Committee's principles for risk data aggregation, exists specifically because regulators discovered during the 2008 financial crisis that major banks could not accurately report their own risk exposures.

For Data SAs, risk and compliance is both a constraint and an opportunity. It is a constraint because every data platform you build in BFSI must satisfy lineage, auditability, retention, and accuracy requirements. It is an opportunity because compliance failures are existential events for a bank — the business case for better data infrastructure is already made.

## The Three Lines of Defence

Banks organize risk management around a "three lines of defence" model. Understanding this helps you know who your stakeholder is:

| Line | Who they are | Their data need |
|------|-------------|-----------------|
| **1st Line** | Business (traders, relationship managers, branch staff) | Risk dashboards, real-time position data, limit alerts |
| **2nd Line** | Risk & Compliance functions | Independent risk measurement, regulatory reporting, policy monitoring |
| **3rd Line** | Internal Audit | Audit trails, data lineage, access logs, historical data replay |

## Credit Risk

Credit risk is the risk that a borrower fails to repay a loan. It is the largest source of losses for most banks.

**Key data inputs:**
- Internal credit scoring models (behavioral, application, bureau data)
- Credit bureau feeds (Equifax, Experian, TransUnion) — updated at origination and periodically
- Collateral valuations (property prices for mortgage portfolios, asset values for secured lending)
- Macroeconomic data (unemployment rates, interest rates — inputs to stress testing models)
- Early arrears signals (missed payments, overlimit events, contact center flags)

**Key outputs:**
- PD (Probability of Default), LGD (Loss Given Default), EAD (Exposure at Default) — the three components of expected credit loss
- IFRS 9 staging: every loan must be classified as Stage 1 (performing), Stage 2 (significant increase in credit risk), or Stage 3 (defaulted) for accounting purposes
- ECL (Expected Credit Loss) reserve calculations — directly impacts the bank's income statement

**Data SA angle:** IFRS 9 ECL calculations require joining loan data, credit model outputs, macroeconomic scenarios, and historical loss data. Banks running this in Excel or legacy SAS environments are prime candidates for modernization.

## Market Risk

Market risk is the risk of loss from changes in market prices — interest rates, FX rates, equity prices, commodity prices.

**Key measures and their data requirements:**
- **VaR (Value at Risk):** Requires full position inventory + historical market data (typically 1–2 years of daily returns)
- **Stressed VaR / Expected Shortfall:** Requires a specific historical stress period (e.g., 2008 crisis data) applied to current positions
- **FRTB (Fundamental Review of the Trading Book):** New Basel standard requiring much more granular risk factor data and model approval processes — a significant data engineering challenge
- **Interest Rate Risk in the Banking Book (IRRBB):** Requires modeling how net interest income changes as rates move — needs full loan and deposit book data with behavioral assumptions

## Operational Risk

The risk of loss from failed processes, people, systems, or external events. Less amenable to quantitative modeling than credit or market risk, but regulators require banks to collect operational loss event data.

**Data requirement:** Loss event database — date, business line, event type, amount, root cause. Banks must submit this data to regulators and use it to calibrate capital models.

## AML (Anti-Money Laundering)

AML is the process of detecting customers who are using the bank to launder criminal proceeds. It generates some of the largest and most complex data workloads in retail banking.

**Key components:**
- **Transaction Monitoring:** Rules and ML models that flag unusual transaction patterns (structuring, rapid cash movement, mule accounts). Runs on the full transaction history — often the most data-intensive workload in a retail bank.
- **Sanctions Screening:** Every payment must be checked against sanctions lists (OFAC, EU, UN) in real time. Requires a low-latency lookup against a constantly updated reference dataset.
- **Customer Risk Rating:** Each customer is assigned an AML risk rating (Low/Medium/High) based on their profile, jurisdiction, and transaction behavior. High-risk customers require Enhanced Due Diligence (EDD).
- **SAR Filing:** Suspicious Activity Reports filed with regulators (FinCEN in the US, NCA in the UK) when money laundering is suspected. The data trail supporting a SAR must be complete and auditable.

**Data SA angle:** Legacy transaction monitoring runs overnight on the previous day's transactions. Modern banks want to detect suspicious patterns in near-real time. This is a streaming pipeline + graph analytics problem (following money across multiple hops through the banking system).

## KYC / KYB (Know Your Customer / Know Your Business)

KYC is the process of verifying a customer's identity before opening an account and monitoring them on an ongoing basis. KYB is the equivalent for corporate customers.

**Data flows:**
- Identity document capture and verification (ID, passport, proof of address)
- PEP (Politically Exposed Person) and adverse media screening — third-party data feeds
- UBO (Ultimate Beneficial Owner) data for corporate customers — often from external registry providers
- Ongoing monitoring — customer risk ratings are refreshed periodically and when triggered by events

**SA conversation:** KYC data is highly unstructured (scanned documents, news articles) and spread across multiple vendors and systems. A document AI + entity resolution pipeline is a strong solution here.

## BCBS 239: The Data Architect's Regulatory Framework

BCBS 239 (Basel Committee on Banking Supervision, Principles for Effective Risk Data Aggregation and Risk Reporting) is the regulation that most directly shapes enterprise data architecture decisions at large banks.

Its 14 principles boil down to four things:
1. **Governance** — A bank must know where its risk data comes from and who owns it
2. **Data architecture and IT infrastructure** — Risk data must be integrated and cannot live in disconnected silos
3. **Accuracy and integrity** — Risk data must be accurate, complete, and reconciled to the source systems
4. **Timeliness** — Risk reports must be producible within agreed timeframes (including under stress conditions)

**Direct implication for SAs:** Banks that are BCBS 239 compliant need data lineage tools, data quality monitoring, a data catalogue, and a clearly defined golden source for each risk metric. This is a modern data platform sale.

## Common Customer Problems You Will Hear

**"We can't produce our CCAR/stress test results on time"**
Stress testing requires aggregating data from dozens of systems under time pressure. The data pipeline is too fragile and too slow. The conversation is about data consolidation, pipeline reliability, and compute scalability.

**"Our AML transaction monitoring is producing too many false positives"**
Legacy rule-based systems flag too much and the investigations team is overwhelmed. ML-based behavioral analytics can reduce false positives significantly — this is a data + ML platform conversation.

**"We have no data lineage and our regulator is asking for it"**
Classic data governance gap. The bank cannot explain where a number in a regulatory report came from. A data catalogue with automated lineage is the solution.

**"Our IFRS 9 ECL process is manual and takes 3 weeks to run"**
A combination of poor data integration (the loan book lives in 5 systems) and inefficient computation (running in SAS on a single server). A cloud data platform with integrated ML can run this in hours.
