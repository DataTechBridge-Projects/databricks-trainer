# Compliance, Security & Regulatory Considerations for BFSI Data Solutions

## Overview

Building a data platform for a retailer and building one for a bank are fundamentally different exercises. The technical components — storage, compute, pipelines, dashboards — are largely the same. What is different is the *constraints* that govern every design decision: who can see what data, where data can physically reside, how long it must be kept, what happens if it is breached, and whether a regulator can audit every step of the pipeline.

This section covers what a Data SA must know *before* proposing an architecture to a BFSI customer. Getting these wrong does not result in a failed project — it results in regulatory fines, license revocation, or reputational damage that can end careers and close businesses.

Think of this section as the checklist you run through before committing to any design.

---

## 1. Data Residency & Sovereignty

**The rule:** Financial data — especially customer PII and transaction data — may not leave a defined geographic boundary without explicit regulatory approval.

**Why it matters:** Banks are licensed entities operating under national regulators. The UK FCA, the EU ECB, the US OCC, the RBI in India — each has jurisdiction over the institutions it licenses, and each has views on where data about their citizens or within their borders can be processed and stored.

**Key regulations:**
- **EU GDPR Article 46 / Chapter V:** Data transfers outside the EU require adequacy decisions, Standard Contractual Clauses (SCCs), or Binding Corporate Rules. The Schrems II ruling invalidated the EU-US Privacy Shield — cross-Atlantic data transfers require careful legal structuring.
- **India DPDP Act (2023):** India's Digital Personal Data Protection Act — still being implemented but will restrict cross-border transfer of Indian citizens' personal data.
- **China PIPL:** Personal Information Protection Law — very restrictive on data leaving China. Financial data is classified as "important data" with additional restrictions.
- **DORA (EU, from Jan 2025):** The Digital Operational Resilience Act requires that critical data and ICT systems remain accessible and resilient. Third-party (cloud) providers used by EU financial institutions must meet contractual requirements about data location and access.

**What to consider when designing:**
- Which cloud regions are in scope? A bank with EU customers cannot default to `us-east-1`.
- Does the architecture involve any cross-region replication? If so, what is the legal basis?
- If using a multi-cloud or SaaS vendor, where does data-at-rest live? Where is it processed?
- Encryption key management — does the bank control the keys (BYOK/HYOK), or does the cloud provider? Regulators increasingly expect banks to control their own encryption keys.

---

## 2. Data Classification & Access Control

**The rule:** Not everyone in the organization should be able to see all data. Financial data is among the most sensitive in the world — it is a direct target for fraud, identity theft, and insider abuse.

### Data Classification Tiers

Most BFSI organizations use a classification scheme similar to:

| Class | Examples | Typical controls |
|-------|---------|-----------------|
| **Public** | Published interest rates, product brochures | No restriction |
| **Internal** | Aggregated performance reports, internal procedures | Employee access only |
| **Confidential** | Customer PII, account numbers, salary data | Role-based access, audit logging |
| **Restricted / Secret** | Encryption keys, authentication credentials, trade secrets | Privileged access management, break-glass procedures |
| **Regulated** | Data subject to specific legal regimes (PCI-DSS card data, HIPAA health data) | Specific technical controls mandated by regulation |

**As a Data SA, you must ask:** What classification does this data carry, and does the proposed architecture enforce the right controls at each layer?

### PCI-DSS (Payment Card Industry Data Security Standard)
If the solution handles card data — Primary Account Numbers (PAN), cardholder names, CVV codes, expiry dates — PCI-DSS applies. It is not optional.

**Key PCI-DSS controls relevant to data architecture:**
- **Cardholder data must be encrypted at rest and in transit** — AES-256 minimum for at-rest data
- **PANs must be masked when displayed** — only the last 4 digits should ever be visible to most users
- **CVV must never be stored post-authorization** — not in logs, not in databases, not in files
- **Network segmentation:** Systems that store, process, or transmit cardholder data must be in a clearly defined, isolated network zone (the "cardholder data environment" or CDE)
- **Audit logging:** All access to cardholder data must be logged with timestamps and user identity
- **Quarterly vulnerability scanning and annual penetration testing** of CDE systems

**PCI-DSS scope is the most common mistake in BFSI data architecture.** Anything that touches cardholder data — even if only in transit — is in scope. Developers who log raw card numbers "just for debugging" have caused multi-million pound compliance failures.

### Tokenization and Masking
The standard design pattern for reducing PCI-DSS scope is **tokenization**: replace the card number with a non-sensitive token at the earliest point of entry, and never store the real PAN in the data platform. The token vault (which holds the PAN-to-token mapping) is the only system in PCI scope.

Similarly, **data masking** (irreversibly replacing PII with realistic-looking synthetic values) is used in non-production environments. Developers and data scientists should never have access to production PII — they should work on masked datasets.

---

## 3. Identity, Authentication & Privileged Access

**The rule:** Every human and every system that accesses financial data must be authenticated, authorized to the minimum necessary privilege, and have their access logged.

### Least Privilege Principle
No user or service account should have more access than the minimum required to do their job. In data platforms, this is violated constantly — data engineers often have read access to entire databases "for convenience" when they only need access to specific tables or schemas.

**Practical controls:**
- **Column-level security:** Mask or restrict sensitive columns (account number, date of birth, salary) even from users who can query the table
- **Row-level security:** A relationship manager should only see customers in their portfolio, not the entire customer base
- **Dynamic data masking:** Show masked values to most users; only privileged users see the real data — implemented at the query layer without storing duplicate data

### Privileged Access Management (PAM)
Database administrators, platform engineers, and anyone with elevated access (the ability to modify data, change access controls, or read restricted data) must use a PAM solution. This provides:
- **Credential vaulting:** No one knows the actual DBA password — the PAM system injects it at session time
- **Session recording:** Every privileged session is recorded and auditable
- **Approval workflows:** Emergency access requires a justification and approval

### Service Accounts & Secrets Management
Pipelines, ETL jobs, and APIs authenticate to databases and data stores using service accounts. These credentials must be:
- Stored in a secrets management system (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault) — never hardcoded in code or config files
- Rotated regularly (typically every 90 days or less)
- Scoped to the minimum necessary permissions for the pipeline's function

---

## 4. Encryption

**The rule:** All financial data must be encrypted in transit and at rest. This is both a regulatory expectation and a baseline security control.

| Layer | Standard | Notes |
|-------|---------|-------|
| **Data in transit** | TLS 1.2 minimum, TLS 1.3 preferred | All API calls, database connections, file transfers. Older protocols (SSL, TLS 1.0/1.1) must be disabled. |
| **Data at rest** | AES-256 | Cloud storage, databases, backups. Keys must be managed separately from the data. |
| **Key management** | HSM (Hardware Security Module) | Encryption keys for the most sensitive data should be stored in an HSM, not in software. Cloud HSM services (AWS CloudHSM, Azure Dedicated HSM) satisfy this. |
| **BYOK / HYOK** | Customer-managed keys | Many BFSI regulators expect the bank to hold its own encryption keys, not the cloud provider. BYOK (Bring Your Own Key) — cloud provider manages HSM but bank owns the key material. HYOK (Hold Your Own Key) — bank holds keys entirely outside the cloud provider. |
| **Database TDE** | Transparent Data Encryption | Standard encryption for database files at the storage layer — provided by most cloud databases by default. |
| **Field-level encryption** | Application-level | For the most sensitive fields (SSN, PAN, biometric data), encrypt at the application layer so that even database administrators cannot read the values. |

---

## 5. Audit Logging & Non-Repudiation

**The rule:** In financial services, if it wasn't logged, it didn't happen. Regulators, auditors, and courts rely on audit logs to reconstruct events.

**What must be logged:**
- Every read of sensitive data (who accessed what record, when, from where)
- Every write or change to data (what changed, from what value to what value, who made the change)
- Every authentication event (success and failure)
- Every privileged action (schema changes, access grants, data exports)
- Every pipeline execution (what data was processed, what transformations were applied, success/failure)

**Log requirements:**
- **Tamper-evident:** Logs must be stored in a system where they cannot be modified or deleted by the people whose actions they record — write-once storage (WORM) or a separate security information and event management (SIEM) system
- **Retention:** Audit logs are typically retained for 3–7 years depending on the regulation
- **Queryable:** Regulators will ask "show me all accesses to customer X's record in the last 6 months" — logs must be queryable, not just stored

---

## 6. Data Lineage, Auditability & BCBS 239

**The rule (BCBS 239, Principle 2):** A bank must be able to demonstrate that its risk data is complete, accurate, and traceable to source systems.

**What this means architecturally:**
- Every number in a regulatory report must be traceable back through every transformation to the raw source record that produced it
- If the pipeline transforms or aggregates data, that logic must be documented and version-controlled
- If data is corrected or restated, the original values and the correction must both be retained

**Tools that help:** dbt (transformation lineage), Apache Atlas (data catalog with lineage), Databricks Unity Catalog, Apache OpenLineage (open standard for lineage metadata), Collibra, Alation.

**The common failure mode:** Teams use Jupyter notebooks and ad-hoc SQL scripts for transformations. These are not version-controlled, not documented, and produce no lineage. A regulator asking "where did this number come from?" gets the answer "we'll need to ask the analyst who ran it, if they still work here."

---

## 7. Data Retention & the Right to Erasure Conflict

This is one of the most interesting architectural tensions in BFSI:

**Regulation A (e.g., AML law):** Retain all transaction data for 7 years.

**Regulation B (GDPR Article 17):** A customer has the right to request erasure of their personal data.

These two requirements conflict directly. The resolution is:
- Financial transaction data is typically exempt from the right to erasure when retention is required by law — the legal basis is a legal obligation, not consent
- Non-essential personal data (e.g., behavioral data from a marketing campaign) is not exempt and must be erasable
- The data architecture must be able to selectively erase certain data categories for a given individual while retaining their transaction records

**Architectural implication:** Data lakes with immutable append-only storage (e.g., an S3 bucket with object lock) are incompatible with the right to erasure unless designed carefully. Patterns include:
- **Crypto-shredding:** Encrypt the individual's data with their own unique key. Erasure = destroy the key. The encrypted data remains but is unreadable.
- **Logical deletion with masking:** Mark records as deleted and apply masking at the query layer — the underlying bytes remain but are inaccessible
- **Separate cold storage:** Regulatory retention data in an immutable archive; personal data in a separate store that can be deleted

---

## 8. Third-Party & Cloud Provider Risk

**The rule (DORA, EBA Guidelines on Outsourcing):** Banks remain fully responsible for the security and resilience of their data even when a third-party cloud provider processes it. "It's the cloud provider's fault" is not an acceptable answer to a regulator.

**What banks are required to do:**
- **Due diligence** on every cloud or SaaS provider that processes material data — security assessments, penetration test results, SOC 2 reports
- **Contractual requirements** — the cloud contract must include data residency, access for regulators (the bank's regulator must be able to audit the cloud provider if needed), data portability, and exit provisions
- **Concentration risk:** UK PRA and EU ECB are concerned that too many banks using the same cloud provider creates systemic risk. Banks must document and manage this.
- **Exit planning:** The bank must be able to migrate off a cloud provider within a defined timeframe if required

**As a Data SA:** When you propose a cloud architecture to a BFSI customer, expect the information security and procurement teams to ask for the cloud provider's SOC 2 Type II report, their penetration test results, their data residency guarantees, and their contractual terms. Have these ready.

---

## 9. Resilience, Business Continuity & Data Recovery

**The rule:** Financial data pipelines are operational infrastructure. If the pipeline fails, the bank may not be able to produce its regulatory reports, price its products, or detect fraud.

**Key requirements:**
- **RPO (Recovery Point Objective):** How much data can the bank afford to lose in a disaster? For a payment processing pipeline, the answer is often zero — zero-RPO requires synchronous replication to a second region.
- **RTO (Recovery Time Objective):** How quickly must the pipeline be restored? Regulatory reporting pipelines often have same-day RTOs.
- **DORA (EU):** Requires financial institutions to define and test their ICT business continuity plans, including data backups and recovery procedures. From January 2025, cloud providers used by EU banks must also comply.
- **Backup validation:** Backups that have not been tested are not backups — they are hopes. Regulators expect evidence of regular restore testing.

**Design considerations:**
- Multi-region active-active or active-passive deployments for critical pipelines
- Immutable backups (cannot be deleted or overwritten by ransomware)
- Documented and tested runbooks for every failure mode
- Monitoring and alerting that detects pipeline failures before the business does

---

## 10. Insider Threat & Data Exfiltration

Banks are frequent targets of insider threats — employees who steal customer data to sell, or who exfiltrate proprietary trading strategies. Data architecture must make exfiltration detectable and difficult.

**Controls:**
- **Data Loss Prevention (DLP):** Policies that detect and block bulk data movements — e.g., an employee querying 100,000 customer records and exporting them to a personal device
- **Anomaly detection on data access:** Baseline normal access patterns and alert on deviations (e.g., a user who normally queries 100 records suddenly queries 50,000)
- **Egress controls:** Restrict which systems can move data outside the organization's perimeter — block direct uploads to external cloud storage from within the data platform
- **Separation of duties:** The person who builds the pipeline should not be able to approve their own access to production data; the DBA should not be able to approve schema changes without a second reviewer

---

## Summary: The Pre-Design Checklist for BFSI Data Solutions

Before committing to any architecture with a BFSI customer, get answers to these questions:

| # | Question | Why it matters |
|---|---------|---------------|
| 1 | What data classification levels will this platform hold? | Determines encryption, access control, and audit requirements |
| 2 | Which countries/regions will this data reside in? | Data residency and cross-border transfer rules |
| 3 | Does this platform touch card data (PAN)? | PCI-DSS scope and tokenization requirements |
| 4 | What are the regulatory retention requirements for each data type? | Affects storage design, lifecycle policies, and right to erasure handling |
| 5 | Who needs access to what data? Can we implement column/row-level security? | Least privilege and data masking requirements |
| 6 | What is the RPO and RTO for this pipeline? | Backup, replication, and business continuity design |
| 7 | Does the customer's regulator need to be able to audit this system? | Cloud provider contractual requirements, access for regulators |
| 8 | Will there be any personal data that must be erasable (GDPR Article 17)? | Crypto-shredding or logical deletion architecture |
| 9 | How will data lineage be captured for regulatory reporting? | Lineage tooling and transformation documentation |
| 10 | Who holds the encryption keys, and where are they stored? | BYOK/HYOK requirements, HSM usage |
| 11 | How will privileged access (DBAs, platform engineers) be controlled and monitored? | PAM solution, session recording |
| 12 | Has the customer done a third-party risk assessment on the proposed cloud provider? | Procurement and compliance sign-off timeline |
