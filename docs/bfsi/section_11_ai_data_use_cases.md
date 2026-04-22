# AI & Data Use Cases in BFSI

## Overview

BFSI was using machine learning long before "AI" became a boardroom priority. Credit scoring, fraud detection, and algorithmic trading have been data-driven for decades. What has changed is the breadth of application, the quality of the underlying data infrastructure required to support it, and the regulator's growing interest in model governance.

For Data SAs, AI and ML conversations in BFSI are almost always preceded by a data infrastructure conversation. The limiting factor is rarely the algorithm — it is whether the bank has clean, integrated, governed data that the model can be trained on and served from. Selling the data platform *is* selling the AI capability.

## The Data SA's Frame for AI in BFSI

Before jumping into use cases, understand the three things every BFSI AI conversation requires you to address:

1. **Data availability:** Is the data that feeds this model available, clean, and accessible? (Usually not, and that's your opportunity)
2. **Model governance:** Can the bank explain why the model made a decision? Regulators require explainability, especially for decisions that affect customers (credit decisions, fraud flags)
3. **Model risk management (MRM):** Banks are required to validate, monitor, and document every model that is used in a business process. This is not optional — it is regulatory requirement (SR 11-7 in the US, SS1/23 in the UK)

## Use Case Map by BFSI Segment

### Retail Banking

| Use Case | What it does | Data requirements | Maturity |
|----------|-------------|-------------------|----------|
| **Fraud detection** | Flags suspicious card/payment transactions in real time | Transaction history, device fingerprint, geolocation, merchant data, peer behavior | Very mature — most banks have this |
| **Credit scoring** | Predicts probability of default at origination | Application data, bureau data, behavioral history | Mature — ongoing refinement |
| **Next best offer / Personalization** | Recommends relevant products to customers | Transaction data, product holdings, demographic data, digital behavior | Growing — many banks are early stage |
| **Churn prediction** | Identifies customers at risk of leaving | Balance trends, product engagement, complaint history, channel usage | Moderate maturity |
| **AML transaction monitoring** | Detects money laundering patterns | Full transaction history, entity relationships, network data | Increasingly ML-augmented |
| **Customer service chatbots** | Handles routine inquiries via NLP | CRM data, product data, policy documents | Rapidly growing with LLMs |

### Capital Markets

| Use Case | What it does | Data requirements | Maturity |
|----------|-------------|-------------------|----------|
| **Algorithmic trading** | Executes trades based on market signals | Tick data, order book data, alternative data | Very mature at top-tier banks |
| **Trade surveillance** | Detects market manipulation (spoofing, layering) | Full order and trade history, chat records | Active regulatory requirement |
| **Credit rating models** | Internal counterparty rating | Financial statements, market data, behavioral signals | Mature |
| **P&L explanation** | Attributes daily P&L to market moves | Position data, risk sensitivities, market data | Improving with better data integration |
| **Sentiment analysis** | Extracts market signals from news/filings | News feeds, earnings transcripts, regulatory filings | Growing |

### Insurance

| Use Case | What it does | Data requirements | Maturity |
|----------|-------------|-------------------|----------|
| **Claims fraud detection** | Identifies fraudulent claims | Claims data, claimant history, network data, third-party data | Growing |
| **Pricing models (GLM/GBM)** | Risk-based premium calculation | Historical loss data, applicant data, third-party enrichment | Very mature |
| **Telematics-based pricing** | Uses driving behavior to price motor insurance | IoT/telematics data streams, GPS, accelerometer data | Mature in progressive insurers |
| **Underwriting automation** | Straight-through processing for standard risks | Application data, external data APIs | Growing |
| **Cat model integration** | Incorporates third-party catastrophe model outputs | Exposure data, cat model APIs (AIR, RMS) | Mature at large insurers |
| **Document AI (claims)** | Extracts data from claim documents | Scanned documents, repair estimates, medical records | Rapidly growing with modern LLMs |

### Wealth & Pensions

| Use Case | What it does | Data requirements | Maturity |
|----------|-------------|-------------------|----------|
| **Robo-advisory** | Automated portfolio construction and rebalancing | Client profile, market data, fund data | Mature |
| **Suitability checking** | Validates that investment recommendations match client profile | Client mandate, transaction history, market conditions | Growing |
| **Retirement projections** | Forecasts retirement income under different scenarios | Member data, contribution history, investment performance, mortality tables | Growing |
| **Vulnerability detection** | Identifies financially vulnerable customers | Behavioral signals, transaction patterns, engagement data | Emerging — regulatory interest growing |

## The Feature Store: The Critical Data Infrastructure for ML in BFSI

The most important data infrastructure concept for BFSI ML is the **feature store** — a centralized repository of precomputed ML features that can be served both for model training (batch) and real-time inference.

**Why BFSI needs feature stores:**
- The same features (e.g., "average transaction value in the last 30 days") are used across fraud, AML, and churn models — they should be computed once and reused
- Real-time inference (fraud scoring at authorization) requires features to be available with sub-100ms latency — they cannot be computed on the fly
- Regulatory explainability requires knowing exactly what feature values were used when the model made a decision — the feature store provides this audit trail
- Preventing training/serving skew — the feature computation must produce identical results in training and production, or model behavior degrades

**Feature store architecture pattern:**
```
Source data (transactions, customer, market) 
    → Feature computation pipeline (batch + streaming)
    → Feature store (offline store for training + online store for serving)
    → Model training                    → Model inference (real-time)
```

Vendors: Databricks Feature Store, AWS SageMaker Feature Store, Feast (open source), Tecton.

## Model Risk Management (MRM) — The Regulatory Layer

Every predictive model used in a business process at a bank must go through a formal model validation process. This is regulatory requirement (SR 11-7 in the US, PRA SS1/23 in the UK).

**MRM lifecycle:**
1. **Model development:** Data scientist builds and documents the model
2. **Model validation:** An independent team challenges the model's methodology, data, and performance
3. **Model approval:** Risk committee approves the model for production use
4. **Production monitoring:** Ongoing monitoring of model performance (PSI, KS statistic, accuracy metrics) — model is flagged for review if it drifts
5. **Annual review:** Formal re-validation at least annually

**Data platform implications:**
- Model metadata (version, training data, feature definitions, validation results) must be stored and queryable — an MLflow or similar experiment tracking tool integrated with the data platform
- Model monitoring requires a pipeline that continuously compares predictions with outcomes — for credit models, you need to wait months or years to observe default outcomes
- The data used to train a model must be traceable and reproducible — you need to be able to recreate the training dataset from the data platform as of the date it was used

## The Generative AI Wave in BFSI

LLMs (Large Language Models) are now being deployed across BFSI use cases. The most traction is in:

- **Customer service:** Conversational AI for call center deflection and digital banking assistants
- **Document processing:** Extracting structured data from loan applications, KYC documents, insurance claims, and regulatory filings
- **Code generation:** Helping developers write and explain code (compliance with internal review processes required)
- **Regulatory intelligence:** Summarizing regulatory changes and mapping them to internal policies
- **Audit and compliance review:** Reviewing large volumes of documents for compliance gaps

**The critical data concern for GenAI in BFSI:** Data privacy and confidentiality. Banks cannot send customer PII or confidential financial data to external LLM APIs. The architecture must involve either (a) private deployment of the model, (b) strict data anonymization before sending to an external API, or (c) a retrieval-augmented generation (RAG) pattern where the LLM only receives pre-filtered content.

## Common Customer Problems You Will Hear

**"We want to build an AI fraud model but our transaction data is in 6 different systems"**
The AI project is blocked by data engineering. A unified transaction data platform with a feature store is the prerequisite — the model is the second step, not the first.

**"Our model risk management team is overwhelmed — they can't validate models fast enough"**
The bank is generating more models than its MRM process can handle. A model registry with automated monitoring metrics reduces the manual validation burden and speeds up the cycle.

**"We deployed a credit model and the regulator is asking us to explain a decision"**
Explainability gap. The model (likely a black-box ensemble) cannot produce a human-readable explanation. Transitioning to an interpretable model or adding a SHAP-based explanation layer, with the feature values stored in the feature store, satisfies this.

**"We want to use GenAI for document processing in our KYC team"**
Document AI on sensitive KYC documents. The architecture question is whether the model is deployed privately or via a managed API with data residency and privacy guarantees. This is as much a data governance conversation as a technology one.
