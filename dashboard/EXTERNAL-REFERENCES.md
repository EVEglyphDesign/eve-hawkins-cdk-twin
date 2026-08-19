# Dashboard external reference statistics — retrieval register

**Peterbilt Atlantic · Hawkins Group · CDK/ATD/PACCAR dashboard**
**Version** v0.1 draft · **Date** 2026-08-19 · **Owner** EVEglyphDesign
**Companion** [`EXTRACTION-STAGING.md`](EXTRACTION-STAGING.md) · [`CDK-TO-ACDOCA-BY-ATD-PRIORITY.md`](CDK-TO-ACDOCA-BY-ATD-PRIORITY.md)

## What this is

Every number on the operator dashboard is either **ours** (extracted from CDK, TELUS, mail — the twin) or **external** (a benchmark, industry rate, or manufacturer figure the dealership is being measured against). This file enumerates every external reference the dashboard needs, and — critically — where each one lives, so we can go back to the client with a single, priced ask list rather than one question at a time.

Three retrieval classes:

- **Held** — already in the repository or the client's own possession (usable today).
- **Client-ask** — held by the dealership but not yet handed to us (the sole action on the client side).
- **Third-party** — held by ATD, PACCAR, or a data provider; requires a subscription, portal login, or letter.

Nothing is estimated. Where a figure is not held, the dashboard shows the space and names what it is waiting for.

---

## A. ATD Performance Measurement 2026 — the industry benchmarks

**Source** — NADA Management Series *ATD Performance Measurement 2026*, publication code **TD08260519**, prepared by Sheila Foster, Manager, Financial Composite, National Automobile Dealers Association ([`atd.org`](https://www.atd.org) · [`nada.org`](https://www.nada.org)). PDF held in the client submission — `2026_ATDPerformance_TD08_260519-1.pdf`.

**Retrieval class** — **Held.** The 2026 publication is in the repository. Prior editions (2023, 2024, 2025 all appear as columns inside the 2026 guide) are covered by that single copy.

**What it gives us** — the 60 Critical Operating Variables (COVs), each with:

- The definition and division formula.
- **Total-Dealer Average** for 2023, 2024, 2025 (the 20-Group / Academy mean).
- **Best-of-Class Average** for the same three years (top-performing 20%).
- Six **Key COVs** and eleven **operating guides** (see below).

**Ingest plan** — the 60 COVs and their three-year benchmark grid are transcribed into `dashboard/atd-cov.json` on first use. Every dashboard tile that quotes an industry number reads from that file — one source, one place to correct.

### The eleven ATD operating guides (ceilings and floors)

| # | Guide | Target |
|---|---|---|
| 1 | Return on assets | 17–25% |
| 2 | Cash months' supply | 3 months |
| 3 | Parts & service receivables >30 days | 15% of avg-month customer parts & service sales |
| 4 | Warranty receivables | 100% of current-month parts & labor sales |
| 5 | Used-truck inventory turns | 6× / year |
| 6 | Service total labor gross % total labor sales | 73% (75% after unapplied time) |
| 7 | Parts sales per parts employee | $70,000 |
| 8 | Parts inventory turns | 6–8× / year |
| 9 | Parts inventory performance | 180% minimum |
| 10 | Fixed absorption | 115% |
| 11 | Total absorption | 130% |

These become the *green/amber/red* thresholds on every ATD-linked tile. They do not require a client ask.

### Watch-outs on the ATD numbers

- The guide explicitly warns against reading any COV in isolation ("one number by itself does not mean much"). The dashboard therefore never surfaces a single COV without at least the industry benchmark and the trailing 12-month direction beside it.
- "Departmental expense includes a percent of unapplied expense; the proration of the unapplied is based on the percentage of total expense each department incurs." Every department-level COV (20, 22, 29, 31, 38, 47, 51, 58) inherits this prorated-unapplied convention — the extraction layer must compute unapplied expense once at group level and apportion, or the numbers will not tie to the guide.

---

## B. Peterbilt Standards of Excellence — the manufacturer scorecard

**Source** — PACCAR / Peterbilt, 2026 Standards of Excellence Scorecards, distributed to Craig Allen (Peterbilt Atlantic, DLINK **P026**). Cover sheet + one scorecard per rooftop, scoring period **2025-10-01 to 2026-09-30**. Copies held in the client submission — `P026-Cover-Sheet.pdf`, `P026.pdf`, `P032.pdf`, `P040.pdf`, `P041.pdf`, `P046.pdf`, `P047.pdf`, `P048.pdf`.

**Retrieval class** — **Held for the current period.** The scorecards for future periods are pushed to the dealer by Peterbilt each quarter; retrieval is the client forwarding the file, not a query we can automate today.

**Structure — a rooftop's total score**

- **Operating Standards** — New Truck Heavy Duty, New Truck Medium Duty, Parts, Service, Training (100 points each, weighted 125/100/150/150/100 = 625 possible).
- **Facility Standards** — Facility Survey Score (300 points, weighted 450).
- **Financial Standards** — Financial Results (100 points, weighted 200) *computed at group level, not rooftop*.

Full-service rooftops carry 900 total points; parts/service-only carry 550.

### The seven rooftops in this batch

| DCODE | Location | Type | Points earned / possible | Score |
|---|---|---|---|---|
| P026 | Peterbilt Atlantic — Fredericton | Full service | 475 / 900 | 52.8% |
| P032 | Peterbilt Atlantic — Moncton | Full service | 584 / 900 | 64.9% |
| P040 | Peterbilt Atlantic — Kentville | Parts & service | 335 / 550 | 60.9% |
| P041 | Peterbilt Quebec East | Parts & service | 264 / 550 | 48.0% |
| P046 | Peterbilt Atlantic — Dartmouth | Full service | 348 / 900 | 38.7% |
| P047 | Peterbilt Atlantic — Deer Lake | Parts & service | 397 / 550 | 72.2% |
| P048 | Peterbilt Quebec East — Saint-Pascal | Full service | 301 / 900 | 33.4% |

**Open question — eight-vs-seven mismatch.** The Craig Allen intake noted **eight** published rooftops (matched by CDK invoice 10002236 carrying eight billed CMFs). Only seven scorecards are in this batch. **First ask to Craig — is the eighth rooftop a full-service or P&S-only location, and can we get its 2026 scorecard?** This must be resolved before the rooftop leaderboard tile is trusted.

### External reference figures inside the Peterbilt scorecard

Peterbilt already fuses in a set of third-party industry statistics we do **not** hold and must retrieve to reproduce or audit any question. These become their own retrieval column:

| Metric | Question source | Retrieval class | Notes |
|---|---|---|---|
| Heavy Duty Retail Market Share | RL Polk registrations in dealer AOR | **Third-party — S&P Global Mobility (formerly Polk)** | HD units *retailed by dealership* ÷ *total HD units registered per RL Polk in dealer AOR*. Requires the Polk registration feed for the dealer's Area of Responsibility. Peterbilt supplies the number; we cannot audit it without Polk. |
| Medium Duty Retail Market Share | RL Polk | Third-party — Polk | Same construction, MD basis. |
| Polk Market Share (HD & MD) | RL Polk | Third-party — Polk | Peterbilt AOR-registered units ÷ total AOR-registered units. |
| PFC Retail Market Share | Peterbilt Financial Corp / Kirby-Peterbilt | Third-party — PACCAR Financial | Dealer retail penetration threshold: 25% HD / 10% MD. |
| MX Engine Mix | Dealer invoicing from PACCAR | **Held on PACCAR side; retrievable from dealer.paccar.com** | HD units invoiced to dealer powered by MX ÷ total HD units invoiced. |
| TX-8 Mix | Dealer invoicing from PACCAR | PACCAR portal | MD basis. |
| TX-18 / Endurant XD Mix | Dealer invoicing from PACCAR | PACCAR portal | Vocational HD basis. |
| Conquest count | Peterbilt CRM — first Peterbilt sale to a customer in trailing 3 years | Peterbilt-side | Auditable against our CDK customer-first-sale date, once CDK is granted. |
| Red Oval certified count | Peterbilt Red Oval program | Peterbilt-side | Per full-service location. |
| Remote Diagnostics counts | PACCAR Solutions | Peterbilt-side | Sold, activated, expiring, renewed. |
| MDI (Materials Distribution Initiative) Tier | PACCAR Parts | Peterbilt-side | Elite Plus / Elite / Tier 1 / No Tier, averaged over four benefit periods. |
| RPM Scorecard component | PACCAR Parts | Peterbilt-side | Loyalty, active users, SalesDrive, training. |
| TRP Parts growth & TRP Store presence | PACCAR TRP | Peterbilt-side | Growth rate and location count. |
| Platinum Score | PACCAR Service | Peterbilt-side | Service quality index. |
| DFP (Dealer Financial Performance) grade | Peterbilt group-level | Peterbilt-side | A/B/C/≤D — group level, not rooftop. |
| ELEC-103/107/201/307 completion | PACCAR training system | **Held on PACCAR side; retrievable from PACCAR training portal** | Per-technician completion. |
| Master Technician % (MX-Certified) | PACCAR training | PACCAR training portal | Same. |
| Facility Survey Score | Peterbilt facility audit | Peterbilt-side | Delivered per rooftop, once per period. |

### Client-ask, Peterbilt lane

1. **Access — the PACCAR dealer portal for Craig Allen and one operator side by side** so we can inventory the source screens for MX Engine Mix, TX-8, TX-18, MDI Tier, RPM, TRP, and technician-training completion. Everything Peterbilt scores us on lives behind that login; nothing on our side of the twin can reproduce it without it.
2. **Delivery — Peterbilt's raw quarterly export** if one exists (some dealers receive an XLSX behind the PDF scorecard). If not, we ingest the PDF and record it as such.
3. **Missing rooftop** — the eighth scorecard, as noted above.

### Third-party ask, Peterbilt lane

1. **RL Polk / S&P Global Mobility registration data for the Peterbilt Atlantic AOR** — HD and MD, monthly. This is the single most expensive external reference on the dashboard and the only way to independently audit the market-share tiles. Client decision: subscribe to Polk directly, ask Peterbilt for the AOR feed (they license it), or leave the market-share tiles marked *Peterbilt-supplied, unaudited*.

---

## C. ATD 20-Group / Academy composite — the peer-group benchmark

**Source** — ATD 20 Group and ATD Academy composite reports. Tim Hawkins participates. Distinct from the *published* ATD Performance Measurement (B), which is the anonymised annual composite; the 20-Group reports Tim receives are the current-month peer composite for his specific group.

**Retrieval class** — **Client-ask.** The 20-Group composite is delivered to Tim directly; it is the number the wiki has previously called the "20-Group numbers" for Luke's variance worksheet.

**What it gives us** — a running peer-composite for the *current* fiscal period (not just 2025 as in the published guide), with the same COV shape. This is what fills the "peer" column beside the *industry* column on every tile.

**Ask — one exchange with Tim**: does he consent to the 20-Group current-period composite being loaded to the twin, and by what channel (monthly PDF, XLSX, or Foundant/Rollmaster export). If yes, we load; if not, the tile shows industry-only and the peer column is labelled *not shared*.

---

## D. Government / demographic reference — Statistics Canada + provincial

Kept lean, because most of the dashboard's benchmarking is intra-industry. Two figures are worth pulling only if the dashboard grows into a "market opportunity" view later:

| Figure | Source | Retrieval class | Trigger |
|---|---|---|---|
| Registered commercial trucks in NB / NS / NL / QC | [Statistics Canada Table 23-10-0067-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2310006701) | Third-party — free | Only when we build a market-share tile that does *not* depend on Polk. |
| Freight tonne-kilometres, Atlantic Canada | Statistics Canada Trucking Commodity Origin & Destination Survey | Third-party — free | Only for the "customer sector rotation" panel in the Customer Sphere. |

Neither is required for the v1 dashboard.

---

## E. Fuel, macro, and rate reference — deferred

The industry practice is to include a diesel price index, a Bank of Canada policy-rate line, and a used-truck price index alongside gross-per-unit tiles. We defer all three to v2:

- **Diesel** — Statistics Canada or Natural Resources Canada weekly retail prices (free).
- **Policy rate** — Bank of Canada published series (free).
- **Used-truck index** — ATD/NADA guide-book component (subscription).

Recorded here so v2 has a start point and v1 stays honest about what it does not show.

---

## Ask register — one page, ready to send

The three asks the dashboard genuinely needs before the industry-benchmark column stops being partial. Anything else on this page is either already held or is a v2 concern.

1. **Peterbilt dealer portal walkthrough** — Craig Allen + one operator, one call. Purpose: inventory the source screens behind MX / TX-8 / TX-18 / MDI / RPM / TRP / training / Platinum. Deliverable: a screen-by-screen list matched against the retrieval column above.
2. **The eighth rooftop's 2026 scorecard** — Craig confirms the missing DCODE and forwards its PDF.
3. **ATD 20-Group current-period composite** — Tim confirms whether it may enter the twin and by what channel.

The RL Polk / S&P Global Mobility question is worth surfacing at the same time but explicitly as a **v2 decision**, not a v1 blocker — the v1 dashboard can show market-share tiles as *Peterbilt-supplied, unaudited* and still be useful.

---

*Pour le bien-être du peuple.*
