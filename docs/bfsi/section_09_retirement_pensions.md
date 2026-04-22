# Retirement Products & Pension Data

## Overview

Retirement is one of the most data-intensive and long-horizon financial businesses that exists. A pension fund may hold records for a participant who joined at age 22 and live to claim a benefit at 85 — a 63-year data relationship. Every contribution, every salary change, every life event (marriage, divorce, death), and every investment return must be recorded accurately because the benefit calculation at retirement depends on the complete history.

For Data SAs, pension and retirement is uniquely challenging because the data does not just need to be accurate *today* — it must be reproducible at any point in the past. "What was this member's projected benefit on 1st January 2010?" must be answerable decades later, typically for regulatory, legal, or audit purposes.

## The Two Major Retirement Models

### Defined Benefit (DB) — "Final Salary" or "Career Average"
The employer promises a specific benefit at retirement — typically a formula based on salary and years of service. The employer bears the investment risk: if the fund underperforms, the employer must make up the shortfall.

**Example benefit formula:** 1/60th of final salary × years of service
- 30 years of service, £60,000 final salary = £30,000 per year pension

DB schemes are largely closed to new entrants in the private sector (the liability is too uncertain), but many legacy schemes remain open to existing members and have very large asset pools. Public sector schemes (government, teachers, NHS) are still predominantly DB.

**Data characteristics:** Long member history, actuarial valuation required (typically every 3 years), complex benefit calculations at retirement, survivor benefits (spouses, dependants), transfer value calculations.

### Defined Contribution (DC) — "Money Purchase"
The employer and/or employee contribute a defined amount into an individual account. The account is invested in market funds. Whatever the pot is worth at retirement is what the member gets — the member bears the investment risk.

**Examples:** 401(k) in the USA, workplace pensions in the UK (NEST, employer schemes), superannuation in Australia.

**Data characteristics:** Per-member account balance, contribution records, investment election, fund performance, charges, and ultimately a decumulation event (annuity purchase, drawdown, or lump sum).

### Hybrid Schemes
Some schemes combine DB and DC elements. Cash Balance plans are a common example — the employer promises a pot size (like DC) but the pot is based on a formula (like DB). The employer bears investment risk up to the promised pot level.

## Key Retirement Data Domains

### Member Data
The foundation of any pension administration system. Each member record contains:
- Personal details (name, date of birth, NI/SSN, address, marital status)
- Employment history (employer, start date, service breaks, end date)
- Salary history (for DB benefit calculation)
- Nomination of beneficiaries (who receives a death benefit)
- Contact and bank details (for payment)
- Communication preferences and engagement history

**Data quality challenge:** Member data accumulated over decades is often dirty. Address records go stale, names change on marriage/divorce, beneficiary nominations become outdated. Data cleansing campaigns are a recurring exercise for large pension administrators.

### Contribution Data
For DC schemes, every contribution must be tracked:
- Contribution date, amount, source (employee vs. employer vs. additional voluntary)
- Investment allocation at time of contribution
- Payroll source data — contributions originate from payroll files

**Reconciliation:** Contributions must reconcile between the payroll system (what was deducted from pay) and the pension administrator's record (what was received and invested). Breaks occur regularly and must be investigated and corrected.

### Investment & Valuation Data

**For DB schemes:**
- The scheme holds a large, diversified investment portfolio managed by external asset managers
- Asset valuations feed into the actuarial valuation — determining whether the scheme is in surplus or deficit
- The Liability Driven Investment (LDI) strategy that many DB schemes use requires matching asset duration to liability duration — complex data joins between asset positions and member benefit projections

**For DC schemes:**
- Each member has a "pot" invested across a range of fund options
- Daily unit prices are applied to member holdings to calculate account balances
- Lifestyle/target-date fund switching means contributions are automatically moved to lower-risk assets as the member approaches retirement

### Benefit Calculation Data

**DB benefit calculation at retirement** is surprisingly complex:

- Basic pension = accrual rate × pensionable service × pensionable salary (with adjustments for revaluation during deferment)
- Early retirement reduction (if taken before Normal Retirement Age)
- Late retirement enhancement (if taken after NRA)
- Commutation (trading pension for a tax-free cash lump sum)
- Guaranteed Minimum Pension (GMP) for contracted-out schemes (UK) — historical government override that complicates benefit calculations enormously

**GMP is a known pain point:** Millions of UK scheme members accrued GMP rights between 1978 and 1997 — a government override of the scheme benefit. These rights are complex, historically poorly recorded, and require a reconciliation process called "GMP reconciliation" against HMRC records. Many schemes are still working through this.

### Regulatory Reporting Data

| Report / Submission | Who requires it | Frequency | Data complexity |
|--------------------|----------------|-----------|-----------------|
| **Actuarial valuation** | Scheme trustees (DB) | Every 3 years | Full member data + investment data + actuarial assumptions |
| **Annual benefit statements** | Members | Annual | Per-member projected benefit calculation |
| **PPF (Pension Protection Fund) levy data** | UK PPF | Annual | Scheme funding level and investment risk assessment |
| **Pensions Dashboard** | UK FCA/TPR (from 2024-26) | Real-time API | Member benefit entitlements must be queryable on-demand |
| **HMRC pension savings statements** | HMRC | Annual | Members who exceed the Annual Allowance for tax-relieved contributions |
| **Auto-enrolment declarations** | UK TPR | At enrollment | Employer confirms eligible workers have been enrolled |
| **Form 5500** | US DOL | Annual | DC scheme financial and participation data (USA) |

## The Pensions Dashboard (UK) — A Live Data Architecture Challenge

The UK government is mandating that all pension schemes connect to a central "Pensions Dashboard" by 2026–2027. Members will be able to log in and see all their pension entitlements from every scheme they have ever been in — a "find all my pensions" service.

**What this requires from schemes:**
- A real-time API that can respond to a member identity query with their current entitlement data within seconds
- Member data must be cleansed and matched against a national identity system
- For DB schemes, projected benefit at retirement must be calculated on-demand — not just at annual statement time

This is a live data engineering project at hundreds of pension schemes right now. It requires modernizing legacy batch-based member administration systems to support real-time queries.

## Decumulation: The Other End of the Pipeline

Accumulation (saving up) gets most of the attention, but decumulation (drawing down in retirement) has its own data complexity.

**Annuities:** The member uses their DC pot to buy a guaranteed income for life from an insurance company. The annuity purchase generates a data event: the pot is transferred, an annuity contract is created, and payments begin. The insurer now holds the longevity risk and needs actuarial data to model it.

**Drawdown (Flexi-access drawdown):** The member leaves the pot invested and draws an income directly from it. The pot remains in the pension scheme/platform — generating ongoing valuation, investment, and payment data. In the UK, drawdown became very common after the "pension freedoms" reforms of 2015.

**Defined Benefit in payment:** The scheme pays a monthly pension to the member for the rest of their life (and potentially a survivor's pension to a spouse). The scheme must maintain a payroll for retired members — sometimes tens of thousands of pensioners — and apply annual increases (typically linked to RPI or CPI inflation).

## Common Customer Problems You Will Hear

**"We can't produce our annual benefit statements on time"**
The benefit calculation requires data from multiple legacy systems (payroll history, scheme rules, fund valuations) that are poorly integrated. A data platform that consolidates member and benefit data into a single governed store makes statement generation reliable and auditable.

**"Our GMP reconciliation has been running for 5 years and we're still not done"**
GMP data quality issues are endemic. The cleansing, matching, and correction process requires data engineering at scale — matching member records to HMRC data, identifying discrepancies, and applying corrections in a controlled, auditable way.

**"We need to connect to the Pensions Dashboard and we have no real-time capability"**
The scheme currently calculates benefits in a nightly batch run. Connecting to the dashboard requires on-demand calculation. This is a data modernization project — moving from batch to on-demand benefit calculation.

**"We're consolidating three DB schemes following a company merger"**
Three different scheme rules, three different member administration systems, potentially three different actuarial assumptions. Data migration, member matching, and benefit harmonization are all data engineering problems.

**"Our trustees can't see the scheme's funding position in real time"**
The actuarial valuation is a point-in-time exercise done every 3 years, with interim estimates done less frequently. Real-time or daily funding level estimates require integrating investment data (daily valuations) with liability estimates (actuarial model outputs) into a dashboard. This is a very common modernization conversation with larger DB schemes.
