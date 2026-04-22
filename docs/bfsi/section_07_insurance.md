# Insurance (P&C and Life)

## Overview

Insurance is fundamentally a data business. An insurer collects premiums today based on a statistical model of future losses. Get the model wrong — either because the data going in is bad or because rare events cluster unexpectedly — and the insurer pays out more than it collected. The entire business model depends on the quality and breadth of data used to price risk.

For Data SAs, insurance is interesting because it has three genuinely distinct data workloads: underwriting (pricing risk at origination), claims (processing losses when they occur), and actuarial (long-term financial modeling of the portfolio). Each workload has different latency, volume, and accuracy requirements.

## The Two Major Insurance Segments

### Property & Casualty (P&C) — Also called General Insurance
Covers losses to physical assets or third-party liability. Common products: motor insurance, home insurance, commercial property, liability, travel, cyber.

**Characteristics:** Shorter policy terms (usually annual), high claim frequency for motor/home, can have extreme tail risk (natural catastrophes), large external data dependency (weather, geospatial, telematics).

### Life & Health Insurance
Covers mortality (death benefit), disability, critical illness, and in some markets, health expenses. Also includes savings and investment-linked products (see Section 09 on Retirement for overlap).

**Characteristics:** Very long policy terms (decades for whole life), low claim frequency but high severity, heavy actuarial modeling, tightly regulated for solvency (Solvency II in the EU, RBC in the US).

## The Insurance Data Lifecycle

```
Distribution → Underwriting → Policy Issuance → In-force Management → Claims → Run-off
      ↓               ↓              ↓                    ↓              ↓          ↓
 Quote data      Risk data       Policy record        Renewal data    FNOL data   Reserve data
 Lead data       Pricing model   Premium schedule     Change events   Claim file  Regulatory
 Broker data     External data   Document store       Telematics      Settlement  Reinsurance
```

## Underwriting & Pricing

Underwriting is the process of evaluating risk and deciding what premium to charge. It is the most data-intensive phase of the insurance lifecycle and the one where competitive advantage is most directly tied to data quality.

**Key data inputs for pricing:**
- **Applicant data:** Age, location, claims history, no-claims discount, occupation
- **Vehicle data (motor):** Make, model, age, modifications, telematics data
- **Property data (home):** Construction type, age, rebuild value, flood zone, crime statistics
- **Third-party data:** Credit scores, weather history, geospatial risk scores, catastrophe model outputs
- **Internal loss data:** Historical claims by risk segment — the foundation of every pricing model

**Pricing models** range from simple actuarial rate tables to complex Generalized Linear Models (GLMs) and, increasingly, gradient boosting and neural networks. The model output is a technical price; underwriters may apply adjustments for large commercial risks.

**Data SA conversation:** Insurers want to incorporate more data sources (telematics, satellite imagery, IoT sensors) into pricing. This requires pipelines that can ingest diverse external data, join it to policy records, and feed it into model training and real-time scoring.

## Policy Administration

Once a policy is issued, the policy administration system (PAS) is the system of record. It tracks:
- Policy terms (coverage, exclusions, limits, deductibles)
- Premium schedule and payment status
- Endorsements (mid-term changes to coverage)
- Renewals

**Data challenge:** Most insurers run legacy PAS systems (some decades old). Migrating data out of these systems — or building a modern data layer on top of them — is a common modernization project.

## Claims

A claim is initiated when a policyholder reports a loss. Claims data is some of the most complex and valuable data in insurance.

**FNOL (First Notice of Loss):** The initial claim report. May come via phone, web portal, or increasingly via telematics/IoT (e.g., a connected car automatically reporting an accident). Starts the claims workflow.

**Claims data elements:**
- Incident details (date, location, circumstances, parties involved)
- Policy details (coverage at time of loss)
- Third-party data (police report, medical records, repair estimates, weather data at incident location)
- Reserve (the insurer's estimate of what the claim will ultimately cost)
- Payments (partial and final settlements)
- Subrogation (recovery from a third party who was at fault)

**Claims fraud** is a major data problem. In motor insurance, 10–20% of claims are estimated to involve some element of fraud. Fraud detection models look for patterns in claim characteristics, claimant history, repair shop networks, and social network connections between claimants.

## Actuarial Modeling

Actuaries use statistical models to estimate the future cost of claims already incurred or expected to be incurred on in-force policies. Their outputs directly determine how much capital the insurer must hold.

**Key actuarial data workloads:**
- **Reserve estimation (IBNR):** Incurred But Not Reported claims — the insurer must estimate the ultimate cost of claims that have occurred but haven't been reported yet. Requires historical claims development triangles.
- **Pricing validation:** Testing whether actual loss experience matches the pricing assumptions.
- **Capital modeling:** Simulating thousands of scenarios to determine the capital needed to survive extreme events (Solvency II ORSA, RBC).
- **Catastrophe (Cat) modeling:** Modeling the impact of hurricanes, earthquakes, or floods on the property portfolio — uses specialized third-party cat models (AIR, RMS) combined with the insurer's own exposure data.

**Data SA angle:** Actuarial workloads are traditionally run in SAS, R, or specialized actuarial tools on small data samples. Moving to a cloud data platform allows actuaries to run models on the full dataset, run more scenarios faster, and integrate with modern ML tools.

## Reinsurance

Reinsurers insure insurers — they take on a portion of the risk in exchange for a portion of the premium. Reinsurance arrangements generate their own data flows:
- **Bordereau data:** Detailed policy or claims data shared with the reinsurer periodically
- **Treaty statements:** Premium and claims summaries for portfolio reinsurance arrangements
- **Facultative placement data:** Individual risk submissions for large or complex risks

**Data challenge:** Bordereau data exchange is often still file-based (Excel, CSV via email or SFTP). Modernizing this is a clear data platform opportunity.

## Solvency II (EU) and RBC (US) — Key Regulatory Frameworks

| Framework | Jurisdiction | What it requires |
|-----------|-------------|-----------------|
| **Solvency II** | EU | Pillar 1: quantitative capital requirements. Pillar 2: governance and risk management. Pillar 3: regulatory reporting (QRT templates — very data-intensive quarterly submissions) |
| **Risk-Based Capital (RBC)** | USA | State-level capital requirements based on asset and liability risk |
| **IFRS 17** | Global | New insurance contract accounting standard — requires granular data on contract groups, coverage units, and risk adjustment calculations |

**IFRS 17** is particularly important for Data SAs right now. It came into force in 2023 and requires insurers to calculate profit in a fundamentally different way, needing granular data at the contract group level. Many insurers are still building or stabilizing their IFRS 17 data pipelines.

## Common Customer Problems You Will Hear

**"Our pricing team can't experiment with new data sources"**
Data science is bottlenecked on data engineering. A self-service data platform with pre-ingested third-party data (weather, geospatial, telematics) removes the friction.

**"Our claims reserves are calculated monthly in a spreadsheet"**
Manual actuarial process with poor auditability. Moving IBNR calculations to a governed, version-controlled data pipeline with a proper data model is the modernization play.

**"We're failing our Solvency II Pillar 3 reporting deadlines"**
The QRT (Quantitative Reporting Template) submissions require data from across the business assembled to tight deadlines. A reliable, orchestrated data pipeline with data quality checks is the solution.

**"Our fraud detection is based on rules and our fraud rate is rising"**
Rules-based fraud detection is easily gamed. ML models trained on claims characteristics and network data (connected claimants, repair shops, medical providers) significantly outperform rules. This is a data + ML platform conversation.
