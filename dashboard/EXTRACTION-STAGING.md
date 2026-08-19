# Dashboard extraction staging — the numbers we are targeting

**Peterbilt Atlantic · Hawkins Group · CDK/ATD/PACCAR dashboard**
**Version** v0.1 draft · **Date** 2026-08-19 · **Owner** EVEglyphDesign
**Companion** [`EXTERNAL-REFERENCES.md`](EXTERNAL-REFERENCES.md) · [`CDK-TO-ACDOCA-BY-ATD-PRIORITY.md`](CDK-TO-ACDOCA-BY-ATD-PRIORITY.md)

## What this is

Before the ledger extension is built, before a single Snowflake table is populated, the extraction has to know **which numbers it is trying to produce**. This file stages every number the operator dashboard displays as a *dealership* figure — with its definition, the ATD/PACCAR reference it will sit beside, and the smallest set of source primitives it depends on.

The staging is deliberately organised around **the 60 ATD Critical Operating Variables**. Not because the dashboard is a compliance report — but because every question a truck-dealer operator actually asks (What is my absorption? Am I making money on used trucks? Is my parts inventory earning its keep?) has already been reduced to a ratio by ATD, and reproducing those ratios is the smallest set that also answers everything downstream.

Once the 60 COVs land, the additional Peterbilt Standards of Excellence targets fall out for free from the same primitives.

---

## The primitive fact table

Everything the dashboard shows is a ratio, an annualisation, or a rate over these primitives. If the extraction produces this list correctly at group level and per-rooftop, everything else is arithmetic.

| Class | Primitive | CDK source | ACDOCA / SAP shape |
|---|---|---|---|
| **P&L** | Total dealership sales | Accounting schedule 1–99 revenue accounts | ACDOCA revenue postings |
| P&L | Total dealership gross profit | Sales − COGS by schedule | ACDOCA gross profit line |
| P&L | Total dealership expense | Departmental + unapplied expense accounts | ACDOCA operating-expense lines |
| P&L | Unapplied expense | Corporate/unapplied schedule | ACDOCA unapplied bucket, prorated at read time |
| P&L | Net profit after bonuses | Sales − expense − bonus | ACDOCA net line |
| P&L | Bonuses paid | Bonus accounts | ACDOCA compensation lines |
| **Balance** | Total assets | Asset schedule month-end | ACDOCB balance |
| Balance | LIFO reserve | LIFO account | ACDOCB balance |
| Balance | Net worth | Equity schedule month-end | ACDOCB balance |
| Balance | Total cash | Cash schedule month-end | ACDOCB balance |
| Balance | Customer deposits | Customer-deposit liability | ACDOCB balance |
| Balance | Parts, service, body-shop AR | Trade AR by dept | ACDOCB balance |
| Balance | AR aged >30 days | AR aging schedule | ACDOCB balance + aging attribute |
| Balance | Warranty receivables | Warranty AR | ACDOCB balance |
| **Inventory** | New-truck inventory value | New-truck asset account | ACDOCM valuation |
| Inventory | New-truck units in inventory | Vehicle master count | Material master count |
| Inventory | Used-truck inventory value | Used-truck asset account | ACDOCM valuation |
| Inventory | Used-truck units in inventory | Vehicle master count | Material master count |
| Inventory | Parts inventory value | Parts asset account | ACDOCM valuation |
| **Volumes** | New-truck units sold (period) | Deal file | Sales document count |
| Volumes | Used-truck units sold (period) | Deal file | Sales document count |
| Volumes | Repair orders opened / closed (period) | Service RO file | Service document count |
| Volumes | Counter tickets (period) | Parts counter file | Sales document count |
| **Headcount** | Total dealership employees | Payroll master | HR master |
| Headcount | New-truck sales employees | Payroll master | HR master |
| Headcount | Used-truck sales employees | Payroll master | HR master |
| Headcount | Service mechanical employees | Payroll master | HR master |
| Headcount | Parts employees | Payroll master | HR master |
| Headcount | Body-shop employees | Payroll master | HR master |
| **Dept revenue splits** | Customer / warranty / internal — parts | Parts sales by billing type | Sales doc attribute |
| Dept revenue splits | Customer / warranty / internal — service labor | Service labor by billing type | Sales doc attribute |
| Dept revenue splits | Counter retail / wholesale — parts | Parts sales by channel | Sales doc attribute |
| Dept revenue splits | Customer / warranty / internal — body shop | Body shop by billing type | Sales doc attribute |
| **F&I** | New F&I + net other income | F&I schedule | ACDOCA F&I line |
| F&I | Used F&I + net other income | F&I schedule | ACDOCA F&I line |

Every primitive is either a **monthly balance** (M12 rolling for annualisation) or an **event count / value** (period-summed). Nothing else is needed to reproduce the 60 COVs.

---

## The 60 ATD Critical Operating Variables — as extraction targets

For each COV: the ratio, the primitives it depends on, and the industry references it sits beside on the dashboard. Best-of-class (2025) is used as the amber/green threshold; total-dealer 2025 as the neutral baseline; the operating guide (where one exists) as the ceiling/floor.

Columns:
- **#** — ATD number.
- **Ratio** — the division formula (from the ATD 2026 guide, page 2).
- **Primitives** — abbreviated from the table above.
- **TD25 / BoC25** — 2025 Total-Dealer / Best-of-Class averages (industry reference).
- **Guide** — ATD operating-guide target, where one is stated.

### Category 1 — Dealership-wide financial (COVs 1–13)

| # | Name | Ratio | Primitives | TD25 | BoC25 | Guide |
|---|---|---|---|---|---|---|
| 1 | Net Profit % Sales | Net profit after bonuses ÷ total sales | net_profit_after_bonuses, sales | 3.15% | 7.19% | — |
| 2 | Return on Assets | Annualised NPAB ÷ (assets + LIFO) | net_profit_after_bonuses ×12/M, assets, lifo | 4.74% | 8.54% | 17–25% |
| 3 | Return on Net Worth | Annualised NPAB ÷ (net worth + LIFO) | net_profit_after_bonuses ×12/M, net_worth, lifo | 19.22% | 25.72% | — |
| 4 | Percent Assets Owned | (net worth + LIFO) ÷ (assets + LIFO) | net_worth, lifo, assets | 24.67% | 33.20% | — |
| 5 | Sales / Employee | Total sales ÷ total employees | sales, employees | 81,592 | 65,775 | — |
| 6 | Gross / Employee | Gross ÷ total employees | gross_profit, employees | 14,475 | 14,027 | — |
| 7 | Expense / Employee | Expense ÷ total employees | expense, employees | 11,914 | 9,537 | — |
| 8 | Expense % Sales | Expense ÷ sales | expense, sales | 14.60% | 14.50% | — |
| 9 | Expense % Gross | Expense ÷ gross | expense, gross_profit | 82.31% | 67.99% | — |
| 10 | Cash Months' Supply | (cash − customer deposits) ÷ avg-month expense | cash, customer_deposits, expense/M | 3.11 | 5.44 | 3 months |
| 11 | P&S Receivables % Sales | P&S&BS AR ÷ (P+S+BS sales excl. warranty & internal) | ar_psbs, sales_customer_psbs | 82.92% | 55.67% | — |
| 12 | P&S Receivables % Past Due | P&S&BS AR >30d ÷ (P+S+BS sales excl. warranty & internal) | ar_psbs_30, sales_customer_psbs | 19.15% | 13.88% | 15% |
| 13 | Warranty Receivables % Sales | Warranty AR ÷ (parts + service + body-shop warranty sales) | ar_warranty, sales_warranty_psbs | 122.62% | 104.32% | 100% |

### Category 2 — New truck (COVs 14–22)

| # | Name | Ratio | TD25 | BoC25 |
|---|---|---|---|---|
| 14 | New Sales / Unit | New truck sales ÷ new units sold | 146,290 | 116,592 |
| 15 | New Gross / Unit | New truck gross ÷ new units sold | 9,623 | 7,230 |
| 16 | New Gross % Sales | New truck gross ÷ new truck sales | 6.58% | 6.20% |
| 17 | New F&I / Unit | New F&I & net other ÷ new units sold | 643 | 329 |
| 18 | New Inventory / Unit | New truck inventory ÷ units in inventory | 147,506 | 162,673 |
| 19 | New Inventory Turns | Annualised new COGS ÷ new inventory | 2.9 | 3.8 |
| 20 | Net Return on New Inventory | Annualised new-truck operating profit ÷ new inventory | 4.22% | 13.72% |
| 21 | New Sales / Emp | New sales ÷ new-truck employees | 675,298 | 1,056,325 |
| 22 | New Op Income / Emp | (new gross + new F&I) ÷ new-truck employees | 44,347 | 65,412 |

### Category 3 — Used truck (COVs 23–31)

| # | Name | Ratio | TD25 | BoC25 |
|---|---|---|---|---|
| 23 | Used Sales / Unit | Used sales ÷ used units sold | 52,323 | 51,875 |
| 24 | Used Gross / Unit | Used gross ÷ used units sold | 4,648 | 6,683 |
| 25 | Used Gross % Sales | Used gross ÷ used sales | 8.94% | 12.84% |
| 26 | Used F&I / Unit | Used F&I ÷ used units sold | 541 | 665 |
| 27 | Used Inventory / Unit | Used inventory ÷ units in inventory | 52,855 | 54,693 |
| 28 | Used Inventory Turns | Annualised used COGS ÷ used inventory | 2.8 | 3.0 (**Guide: 6×**) |
| 29 | Net Return on Used Inventory | Annualised used-truck operating profit ÷ used inventory | −11.67% | 18.13% |
| 30 | Used Sales / Emp | Used sales ÷ used-truck employees | 197,354 | 298,733 |
| 31 | Used Op Income / Emp | (used gross + used F&I) ÷ used-truck employees | 18,335 | 38,809 |

### Category 4 — Service mechanical (COVs 32–38)

| # | Name | Ratio | TD25 | BoC25 |
|---|---|---|---|---|
| 32 | Service Customer Labor % Total Labor | Service customer-labor sales ÷ total service labor sales | 68.32% | 68.59% |
| 33 | Service Customer Labor Gross % | Customer labor gross ÷ customer labor sales | 75.40% | 75.55% (**Guide: 73%/75%**) |
| 34 | Service Warranty Labor Gross % | Warranty labor gross ÷ warranty labor sales | 72.46% | 77.28% |
| 35 | Service Internal Labor Gross % | Internal labor gross ÷ internal labor sales | 68.84% | 71.64% |
| 36 | Service Sales / Emp | Total service sales ÷ service employees | 14,667 | 14,951 |
| 37 | Service Gross / Emp | Total service gross ÷ service employees | 10,348 | 10,830 |
| 38 | Service Absorption | Service gross ÷ total dealership expense | 37.24% | 47.25% |

### Category 5 — Parts (COVs 39–51)

| # | Name | Ratio | TD25 | BoC25 |
|---|---|---|---|---|
| 39 | Parts Gross % Sales | Parts gross ÷ parts sales | 27.27% | 27.96% |
| 40 | Parts Gross % Break-Even (Parts Expense ÷ Parts Sales) | Total parts expense ÷ total parts sales | 20.33% | 14.90% |
| 41 | Parts Customer RO Gross % | Customer-mech parts gross ÷ customer-mech parts sales | 28.30% | 29.99% |
| 42 | Parts Warranty RO Gross % | Warranty-mech parts gross ÷ warranty-mech parts sales | 21.66% | 21.10% |
| 43 | Parts Internal RO Gross % | Internal-mech parts gross ÷ internal-mech parts sales | 22.71% | 28.48% |
| 44 | Parts Counter Retail Gross % | Counter retail gross ÷ counter retail sales | 25.32% | 25.58% |
| 45 | Parts Wholesale Gross % | Wholesale gross ÷ wholesale sales | 24.54% | 21.58% |
| 46 | Parts Inventory Turns | Annualised parts COGS ÷ parts inventory | 5.0 | 5.2 (**Guide: 6–8×**) |
| 47 | Net Return on Parts Inventory | Parts operating profit ÷ parts inventory (prorated unapplied) | 46.95% | 92.90% |
| 48 | Parts Inventory Performance | Turns × gross % (COV 46 × COV 39) | 136.93% | 146.68% (**Guide: 180% min**) |
| 49 | Parts Sales / Emp | Parts sales ÷ parts employees | 63,275 | 73,904 (**Guide: $70,000**) |
| 50 | Parts Gross / Emp | Parts gross ÷ parts employees | 17,256 | 20,665 |
| 51 | Parts Absorption | Parts gross ÷ total dealership expense | 48.81% | 59.34% |

### Category 6 — Body shop (COVs 52–58)

| # | Name | Ratio | TD25 | BoC25 |
|---|---|---|---|---|
| 52 | Body Shop Customer Labor % Total Labor | BS customer-labor sales ÷ BS total labor sales | 72.92% | 80.96% |
| 53 | Body Shop Customer Labor Gross % | BS customer-labor gross ÷ BS customer-labor sales | 67.99% | 63.74% |
| 54 | Body Shop Warranty Labor Gross % | BS warranty-labor gross ÷ BS warranty-labor sales | 82.21% | 81.80% |
| 55 | Body Shop Internal Labor Gross % | BS internal-labor gross ÷ BS internal-labor sales | 80.67% | 75.85% |
| 56 | Body Shop Sales / Emp | BS sales ÷ BS employees | 14,538 | 14,381 |
| 57 | Body Shop Gross / Emp | BS gross ÷ BS employees | 9,280 | 8,610 |
| 58 | Body Shop Absorption | BS gross ÷ total dealership expense | 2.11% | 4.17% |

### Category 7 — Fixed & total absorption (COVs 59–60)

| # | Name | Ratio | TD25 | BoC25 | Guide |
|---|---|---|---|---|---|
| 59 | Parts & Service Absorption | (parts + service + body-shop gross) ÷ total expense | 88.17% | 111.54% | **115%** |
| 60 | Total Dealership Absorption | (used gross + parts + service + BS gross) ÷ total expense | 91.11% | 117.09% | **130%** |

---

## Peterbilt Standards of Excellence — extraction crosswalk

Every Standards-of-Excellence line item is either a **PACCAR-supplied count** (retrieved per [`EXTERNAL-REFERENCES.md`](EXTERNAL-REFERENCES.md), Section B) or a figure we can independently derive from the same primitives above. Where we can derive, the twin's value goes beside PACCAR's on the audit view:

| SoE metric | Twin derivation |
|---|---|
| Parts Retail Growth | Δ counter retail sales YoY, from primitive `sales_counter_retail` |
| Fleet Sales Growth | Δ PACCAR-parts fleet-service sales YoY (requires PACCAR MDI category tagging on parts sales) |
| OPC Growth % | Δ online-parts-counter orders (requires OPC channel tag; may only exist in PACCAR portal) |
| TRP Growth | Δ TRP-branded parts purchases YoY (requires TRP part-number list from PACCAR) |
| Avg Days to Submit Warranty Claim | Mean (warranty-claim submit date − RO close date) |
| 1st-Time Warranty Approval Rate | Warranty claims approved on first pass ÷ total |
| Warranty Claim $ Approval | Approved $ ÷ requested $ |
| Financial Statement Timeliness | Month-end close date ≤ 15th of following month (from month-end close log) |
| Financial Statement Accuracy | Δ between submitted and audited/reviewed statement, per group-level financial |
| Statements-by-Location | Boolean — did we submit rooftop-level statements? |

The **Master Technician %**, **electrical-training %**, and **sales-training %** stay on the PACCAR-supplied side and are ingested as a monthly PDF/XLSX drop. There is no dealer-side substitute.

---

## Staging order

The extraction plan pulls in this order so that dashboard value lands sequentially rather than all at once. Each stage produces a tile block that can be reviewed on its own.

**Stage 1 — Dealership financial spine (COVs 1–13).**
Depends on: ACDOCA revenue, expense, unapplied; balance-sheet monthly snapshot; AR aging; warranty AR.
Value: the six Key COVs and the top-of-dashboard "Am I making money" tile block.

**Stage 2 — Absorption spine (COVs 38, 51, 58, 59, 60).**
Depends on: department gross by billing type; total dealership expense.
Value: absorption is Tim's headline number and the one PACCAR watches through Financial Standards.

**Stage 3 — Parts (COVs 39–51).**
Depends on: parts sales by billing type + channel; parts inventory value; parts employee count.
Value: the parts dashboard, which also gives the Peterbilt Parts scorecard nine of its ten fields.

**Stage 4 — Service (COVs 32–38).**
Depends on: service labor sales/gross by billing type; service employee count.
Value: the service dashboard and the Peterbilt Service scorecard.

**Stage 5 — New truck (COVs 14–22).**
Depends on: new-truck deal file; new-truck inventory; F&I schedule.
Value: sales-department dashboard; feeds Peterbilt HD/MD retail-market-share numerator.

**Stage 6 — Used truck (COVs 23–31).**
Depends on: used-truck deal file; used-truck inventory; F&I schedule.
Value: the highest-variance department; the "am I really making money on used?" tile.

**Stage 7 — Body shop (COVs 52–58).**
Depends on: body-shop sales by billing type; body-shop employee count.
Value: the smallest department by revenue but the one that most often fails absorption.

**Stage 8 — Peterbilt-supplied ingest (Standards of Excellence deltas).**
Depends on: PACCAR portal exports + quarterly PDF drop.
Value: the audit view that puts Peterbilt's number next to ours per metric.

Stages 1 and 2 are the minimum viable dashboard. Everything downstream is additive.

---

## Definition of done, per stage

A stage is done when:

1. Every primitive it depends on lands into the twin from the CDK export, with row counts logged and a checksum file committed.
2. The COVs it produces are reproduced against the ATD 2026 total-dealer average as a sanity check (the primitives sum up sensibly; nothing is off by an order of magnitude).
3. Each COV has a green/amber/red rule (best-of-class, total-dealer average, operating guide) recorded in `dashboard/thresholds.json`.
4. The tile is rendered on a page with **no estimated figures** — where a primitive is missing, the tile says what it is waiting for.

The Customer Sphere wireframe already enforces this rule ("a quoted figure stays a quote; the money panel is empty and says why"). This document extends it from customer-view to dashboard-view.

---

*Pour le bien-être du peuple.*
