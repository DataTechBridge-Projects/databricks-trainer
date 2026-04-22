# Capital Markets & Trade Data

## Overview

Capital markets is where securities — stocks, bonds, derivatives, commodities — are bought and sold. It is the segment of BFSI most associated with high-speed data, quant models, and large technology investments. It is also the segment where data latency has the most direct financial consequence: being a millisecond late on a trade can mean missing a price, and being wrong on a risk calculation can mean understating exposure by millions.

As a Data SA, capital markets conversations are usually about one of three things: getting market data in fast and reliably, calculating risk and P&L accurately across a large portfolio, or satisfying a regulator who wants a complete audit trail of every trade.

## Key Market Segments

### Equities
Shares in publicly listed companies. Traded on exchanges (NYSE, LSE, Euronext) and over-the-counter (OTC). Generates tick data (every price update) at extremely high frequency during market hours.

### Fixed Income
Bonds — debt instruments issued by governments (gilts, treasuries) and corporations. More complex than equities because bonds have a maturity date, a coupon schedule, and a credit rating that changes over time. Largely OTC market, so pricing is less transparent than equities.

### Derivatives
Contracts whose value is derived from an underlying asset (equity, rate, FX, commodity). Include options, futures, swaps, and forwards. Derivatives can be exchange-traded (standard contracts) or OTC (bespoke). OTC derivatives generate complex data requirements because the terms of each contract are unique.

### Foreign Exchange (FX)
The largest market in the world by volume (~$7.5 trillion/day). Spot, forward, and swap transactions. Banks act as market makers, quoting bid/offer prices continuously.

### Commodities
Oil, gas, metals, agricultural products. Traded on exchanges (CME, ICE) and OTC. Banks with commodities desks need market data feeds from commodity exchanges alongside their financial data.

## The Trade Lifecycle

Every trade goes through a sequence of stages from agreement to final settlement. Data is produced and consumed at each stage:

```
Pre-Trade → Execution → Post-Trade → Settlement → Accounting
    ↓            ↓            ↓            ↓            ↓
Market data   Trade blotter  Confirmation  CSD/CCP     GL entry
Risk limits   Order book     Matching      Netting     P&L calc
Analytics     FIX messages   Affirmation   Fails mgmt  Regulatory
```

**Key stages explained:**
- **Execution:** Trade is agreed (price, quantity, counterparty). Captured in the trade blotter. FIX protocol is the standard messaging format for electronic trading.
- **Confirmation/Matching:** Both sides confirm they agree on the trade terms. Mismatches (breaks) must be resolved quickly.
- **Clearing:** For exchange-traded products, a Central Counterparty (CCP) like LCH or CME Clearing steps between buyer and seller, taking on counterparty credit risk. Requires margin to be posted.
- **Settlement:** Securities and cash are exchanged, typically T+1 or T+2 days after trade. Happens through a Central Securities Depository (CSD) like Euroclear or DTCC.

## Market Data

Market data is the lifeblood of capital markets. It comes in multiple tiers:

| Type | Description | Latency | Volume |
|------|-------------|---------|--------|
| **Tick data** | Every price update for a security | Microseconds | Extremely high |
| **Level 1** | Best bid/offer and last trade price | Milliseconds | High |
| **Level 2 / Order book** | Full depth of the order book | Milliseconds | Very high |
| **Reference data** | Static attributes of securities (ISIN, CUSIP, rating, sector) | Daily | Low volume, high importance |
| **Corporate actions** | Dividends, stock splits, rights issues | Event-driven | Low but critical |

**Data SA note:** Reference data is often the most painful problem. A security might have a different identifier on every system (ISIN, CUSIP, SEDOL, Bloomberg ticker, Reuters RIC). Maintaining a consistent security master across all downstream systems is a major data management challenge.

## Risk & P&L Data

The most critical daily output for a trading desk is its P&L (Profit and Loss) — how much money did we make or lose today? And its risk reports — how much could we lose if the market moves against us?

**Key risk measures:**
- **VaR (Value at Risk):** The maximum loss expected with X% confidence over Y days. Regulatory capital is partly based on VaR.
- **Greeks (Delta, Gamma, Vega, Theta):** Sensitivities of a derivatives position to changes in market variables. Computed per position, aggregated across portfolios.
- **Counterparty Credit Exposure:** If a counterparty defaults on an OTC derivative, what is the bank's expected loss?
- **Stress Testing / Scenario Analysis:** What happens to the portfolio if the market crashes 20%? Required by regulators (CCAR in the US, ICAAP in the EU).

P&L and risk calculations require joining trade data, market data, and reference data — often across multiple asset classes and booking systems. This is a complex data integration problem.

## Regulatory Reporting in Capital Markets

Capital markets is one of the most heavily regulated data environments:

| Regulation | Jurisdiction | Data Requirement |
|-----------|-------------|-----------------|
| **MiFID II / MiFIR** | EU | Trade reporting to regulators within 15 minutes of execution; transaction reporting T+1 |
| **EMIR** | EU | OTC derivative reporting to trade repositories |
| **Dodd-Frank / CFTC** | USA | Swap data reporting |
| **FRTB** | Global | Fundamental Review of the Trading Book — new internal models for market risk capital; very data-intensive |
| **Basel III / IV** | Global | Capital adequacy — requires granular trade and exposure data |

**SA conversation:** Many banks have reporting pipelines that are fragile, manual, or late. The business case for a modern data platform is often built on regulatory compliance risk reduction.

## Common Customer Problems You Will Hear

**"Our end-of-day P&L takes 6 hours to compute and trading can't see their numbers until midnight"**
This is a data pipeline performance and architecture problem. Usually caused by sequential processing on a legacy system. The conversation is about parallelization, columnar storage, and in-memory computation.

**"We have 12 different systems that each have a different version of the trade"**
Trade data fragmentation across front-office, middle-office, and back-office systems. A golden source trade data store (often called a "trade data hub") is the solution.

**"We're failing our MiFID II transaction reporting SLA"**
The reporting pipeline is too slow or breaks when volume spikes. Reliability, observability, and latency improvements on the reporting pipeline.

**"Our risk team can't see our exposure across equity and fixed income positions"**
Cross-asset risk aggregation requires a unified position data model, consistent security master, and a single analytics layer.

**"We need to ingest real-time market data for our analytics platform"**
High-volume tick data ingestion — streaming pipeline, time-series storage, and query optimization for market data workloads.
