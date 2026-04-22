# Wealth & Asset Management

## Overview

Wealth management serves individuals and families who want to grow and protect their financial assets. Asset management serves institutional clients — pension funds, insurance companies, endowments — who pool capital and invest it professionally. Both segments are in the business of generating investment returns on behalf of clients, and both are deeply dependent on data to do it.

For Data SAs, wealth and asset management conversations tend to center on two themes: **performance and reporting** (did the portfolio make money, and can we prove it?) and **compliance and suitability** (are we managing money in a way that is appropriate for the client and defensible to a regulator?).

## Wealth Management: Key Concepts

### Client Segments
Wealth management is typically segmented by the size of the client's assets:

| Segment | Assets Under Management | Service model |
|---------|------------------------|---------------|
| **Mass Affluent** | $100K – $1M | Digital/hybrid, limited advisor interaction |
| **High Net Worth (HNW)** | $1M – $30M | Dedicated relationship manager, broader product range |
| **Ultra High Net Worth (UHNW)** | $30M+ | Full private banking service, family office structures, alternative investments |

### Advisory Models
- **Discretionary management:** The wealth manager makes investment decisions on the client's behalf within an agreed mandate. Requires demonstrating that decisions were consistent with the mandate — a data audit trail problem.
- **Advisory:** The advisor recommends, the client decides. Requires documenting advice given and whether the client followed it — suitability records.
- **Execution-only:** The client makes their own decisions. The platform just executes. Still requires KYC.
- **Robo-advisory:** Algorithm-driven portfolio construction and rebalancing, usually for the mass affluent segment. Generates large volumes of automated decision records that must be explainable.

### Key Products
- **Managed portfolios:** Discretionary model portfolios invested across equities, bonds, and alternatives
- **Structured products:** Bespoke investment products with defined payoff profiles (capital protection + upside participation)
- **Alternative investments:** Private equity, hedge funds, real estate, infrastructure — illiquid, complex to value and report
- **Custody:** Safekeeping of securities on behalf of the client — the custodian holds the assets and provides consolidated statements

## Asset Management: Key Concepts

### Fund Structures
- **UCITS (EU) / Mutual Funds (US):** Regulated, daily-liquidity funds for retail and institutional investors. Well-understood data model: NAV calculated daily, holdings disclosed periodically.
- **ETFs (Exchange-Traded Funds):** Listed funds that track an index. Create/redeem mechanism generates additional data flows between the ETF issuer and authorized participants.
- **Hedge Funds:** Less regulated, more complex strategies (long/short, macro, quant). Institutional investors only.
- **Private Equity / Infrastructure:** Closed-ended funds with a defined investment period and exit timeline. Very illiquid — assets are valued quarterly or less frequently.

### The Investment Management Process
```
Client mandate → Portfolio construction → Order generation → Execution → Settlement → Valuation → Reporting
       ↓                  ↓                     ↓               ↓            ↓             ↓            ↓
 IPS / guidelines    Model portfolio         OMS/EMS          Trade data   Custody data   NAV calc   Client report
 Risk parameters     Factor model            Compliance pre-  Allocation   Reconciliation  Performance Attribution
 Benchmark           Optimisation            trade check      Confirmations                GIPS calc  Regulatory
```

### Key Data Domains

**Portfolio data:** Holdings (security, quantity, cost basis), transactions, cash positions, corporate actions applied. The portfolio record must reconcile with the custodian's record daily.

**Market data:** Pricing for every security in every portfolio, every day. For liquid securities this is straightforward. For alternatives and OTC derivatives, pricing may require models or third-party valuations.

**Performance data:** Return calculations — time-weighted return (TWR) for manager performance, money-weighted return (MWR / IRR) for client experience. Attribution breaks down returns by asset allocation and security selection decisions.

**Benchmark data:** Index returns and compositions (e.g., MSCI World, Bloomberg Aggregate Bond Index) sourced from index providers — third-party data with licensing implications.

**Compliance data:** Investment guidelines and breaches. Pre-trade compliance checks stop orders that would violate guidelines. Post-trade monitoring catches breaches that slip through.

## Performance Measurement & GIPS

GIPS (Global Investment Performance Standards) is a global standard for calculating and presenting investment performance. Asset managers that claim GIPS compliance must follow strict rules for how returns are calculated, composites are constructed, and performance is presented.

**Why this matters for data:** GIPS compliance requires a complete, auditable history of every portfolio, every transaction, and every valuation. Data cannot be restated or corrected without documentation. The data platform must support point-in-time historical queries — you need to reproduce what the portfolio looked like on any given day in the past.

## Regulatory Landscape

| Regulation | Jurisdiction | What it means for data |
|-----------|-------------|------------------------|
| **MiFID II** | EU | Suitability documentation, best execution reporting, inducements disclosure |
| **PRIIPs KID** | EU | Standardized key information document for investment products — requires performance scenario calculations |
| **AIFMD** | EU | Alternative Investment Fund reporting — Annex IV regulatory reports to national regulators |
| **SEC Regulation Best Interest** | USA | Suitability documentation requirements for broker-dealers |
| **FATCA / CRS** | USA / Global | Tax information sharing — requires tracking client tax residency and reporting investment income |

## Common Customer Problems You Will Hear

**"Our performance reports take 3 days to produce and clients are complaining"**
Manual performance calculation process pulling data from multiple custodians and systems. A unified data platform with automated reconciliation and performance calculation dramatically reduces this.

**"We can't demonstrate suitability for our discretionary clients"**
The wealth manager is making decisions but not recording the rationale against the client's investment policy statement. A data platform that links every transaction to the portfolio mandate provides the audit trail.

**"Our custodian reconciliation breaks every day and we spend half the day fixing it"**
The portfolio management system and the custodian have different views of positions and cash. An automated reconciliation pipeline with exception management workflow is the solution.

**"We're launching a new ESG fund and need ESG data integrated into our investment process"**
ESG data (carbon emissions, board diversity, governance scores) comes from specialist data providers (MSCI ESG, Sustainalytics). Ingesting, normalizing, and integrating it with portfolio data for stock selection and reporting is a data engineering problem.

**"We acquired a fund manager and need to consolidate their data"**
Different portfolio management systems, different custodians, different data models. A data lake / data platform acts as the integration layer, with the PMS migration happening in a second phase.
