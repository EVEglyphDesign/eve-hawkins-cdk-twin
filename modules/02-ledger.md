# Module 02 — Ledger

**Status: drafted from lane 2 research (`cdk_02_ledger.md`). PACCAR-specific chart of
accounts and CDK Drive's own internal schedule/table names remain unverified — see
`docs/open-questions.md`.**

Covers: chart of accounts, accounting schedules, journals, month-end close.

---

## 1. Chart of accounts — OEM-mandated structure

Every major OEM requires franchised dealers to submit a monthly financial statement in a
factory-defined format, forcing the dealer's chart of accounts to map onto factory-standard
account numbers regardless of which DMS the dealer runs. This is formalized for GM as the
**GM Dealer Standard Accounting Manual** ([gm.acctmanual.com](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf))
and for Ford as the **Ford Online Accounting Manual**
([Ford dealerconnection](https://www.fmcdealerfbmi.dealerconnection.com/AccountingManual/en/coa-coacmplt-en-htm/)).
PACCAR's own SEC disclosures confirm PACCAR Financial Services runs dealer wholesale
financing (floor plan) and monitors dealers' financial position as part of that credit
relationship ([PACCAR 10-K, SEC](https://www.sec.gov/Archives/edgar/data/731288/000095017024017921/pcar-20231231.htm)).

`INFERRED (dealer-accounting norm)`: PACCAR/Peterbilt/Kenworth dealers are contractually
required to submit a Dealer Composite/factory-format financial statement analogous to GM's
and Ford's. **No public PACCAR-specific chart-of-accounts manual was located** — this is an
open item, tracked in [`docs/open-questions.md`](../docs/open-questions.md).

### Account numbering conventions (documented via the GM manual; structurally identical pattern used industry-wide)

| Convention | Rule | Example |
|---|---|---|
| Base account number | 3-digit number identifies the natural account | `231` = New Cars inventory |
| Department suffix | Expense (and many revenue) accounts append a 2-digit department code | `013-01` = Delivery Expense, New Vehicle Dept |
| Department code table | 01 New Vehicles, 02 Used Vehicles, 03 Lease & Rental, 04 F&I, 05 Mechanical/Service, 06 Body Shop, 07 Parts & Accessories, 09 General & Administrative | — |
| Sub-account letter suffix | Splits an account further for analysis/audit | `446A` Used Cars Retail–Certified vs `446B` Used Cars Retail–Other |
| Numeric ranges by statement section | 200s assets, 300s liabilities/equity, 400s sales, 600s cost of sales, 700s lease/rental cost detail, 800s/900s other income/expense and F&I | `220` AR-Customers; `400-418` New Cars Retail Sales |

(Source: [GM Dealer Standard Accounting Manual](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf).)

## 2. Accounting schedules — the DMS subledger mechanism

A **schedule** in dealership-DMS accounting is a subledger report of open-item detail behind
a single GL balance, distinct from the GL account itself, which only carries a summarized
period-end total: *"A schedule is simply a complicated report of accounting detail"*
([Digital Dealer, "Your DMS and Schedules"](https://digitaldealer.com/news/your-dms-and-schedules/65829/)).
A schedule is **"controlled"** by a designated key field — RO number, stock number, customer
ID, VIN-last-8, reference/document number — and every schedule-based GL account (floor plan
payable, factory receivables, warranty claims, contracts-in-transit, F&I chargebacks,
service/parts work-in-process) works this way, not just AR/AP as in a generic ERP
([Digital Dealer](https://digitaldealer.com/news/your-dms-and-schedules/65829/)).

| Schedule type | GL control account (GM numbering) | Control key | Behavior |
|---|---|---|---|
| Warranty claims receivable | 263 Warranty Claims | RO#/claim# | Aged schedule (30/60/90/120+), clears at zero balance |
| New vehicle floor plan | 231 New Cars (asset) vs 310 Notes Payable–New Vehicles (liability) | Stock#/VIN-last-8 | Viewed side-by-side vs inventory |
| Factory receivables (holdback, incentives) | 261 Factory Receivables | claim/program reference | Reconciled monthly to OEM statement |
| Contracts in transit | 205 Contracts in Transit | deal/contract # | Clears when funding received from lender |
| Service/parts WIP | 247 Work In Process–Labor | RO# | Clears when RO closes/invoices |

(Sourced to [GM Dealer Standard Accounting Manual](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf)
and [Digital Dealer](https://digitaldealer.com/news/your-dms-and-schedules/65829/).)

`INFERRED (dealer-accounting norm)`: CDK Drive's own internal schedule numbers (equivalent to
Ford's account 1140 or Autosoft's GLSKEDS export) were not located in any public CDK/Fortellis
document.

## 3. Journal entry mechanics

Named journal types documented across the reference DMS/accounting-manual sources: Standard
Entries Journal, Cash Receipts Journal, Cash Disbursements Journal, Purchase Journal, Payroll
Journal, New Vehicle Sales/Purchase Journal, Used Car Sales Journal, Internal Sales Journal,
Service Sales Journal, Warranty Sales Journal, Parts Sales Journal, Dealer Exchange Journal,
Statistical Data Journal, General Journal Entry
([GM Dealer Standard Accounting Manual](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf)).

**Publicly documented Fortellis GL posting APIs (real, published names):**

| API name | Endpoint | Status | Source |
|---|---|---|---|
| CDK Drive Post Accounts GL WIP | `https://api.fortellis.io/cdk/drive/glwippost/startWIP` | Confirmed correct resource URL by Fortellis support | [Fortellis Community: API Integration Response Errors](https://community.fortellis.io/community/forum/qa/api-integration-response-errors) |
| CDK Drive Post Accounting GL | `https://api.fortellis.io/cdk/drive/glpost/startWIP` | Exists but requires provisioning per subscriber | [Fortellis Community: API Integration Response Errors](https://community.fortellis.io/community/forum/qa/api-integration-response-errors) |
| Data Extract API Bundle | n/a (bundle) | Markets an extract/async bundle covering "core dealership operations, including accounting and general ledger data" | [CDK Global, Data Extract API Bundle](https://www.cdkglobal.com/data-extract-api-bundle) |

**Posting-period control / closed-period prevention:** `UNVERIFIED` at the CDK-specific
screen-name level. The general DMS/ERP pattern is that once a period is closed, subledger
modules are blocked from posting back into it
([ERP Software Blog, Dynamics GP Subledger Reconciliation](https://erpsoftwareblog.com/2018/07/dynamics-gp-subledger-reconciliation-best-practices/)).

## 4. Month-end close and factory statement submission

Each major balance-sheet schedule must be reconciled to its GL control account before close;
factory receivable balances must be reconciled specifically to the manufacturer's own
statement ([GM Dealer Standard Accounting Manual](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf)).
A real-world close-speed benchmark for a Peterbilt-branded rooftop, on a competing DMS, is
documented by Procede Software: Peterbilt of Atlanta closes the month in three standard
working days using Excede
([Procede Software customer story](https://www.procedesoftware.com/customer-stories/how-peterbilt-of-atlanta-streamlines-accounting-and-closes-the-month-in-just-three-standard-working-days/)) —
evidence of the close-speed expectation in the Peterbilt dealer network, though it does not
describe CDK Drive itself.

`INFERRED (dealer-accounting norm)` sequence: (1) close/cut off all subsidiary schedules for
the period; (2) reconcile every controlled schedule to its GL account balance; (3) reconcile
factory receivable/holdback/incentive accounts to the OEM's own dealer statement; (4) post
LIFO/inventory valuation adjustments; (5) run trial balance; (6) generate and transmit the
factory-formatted financial statement. No CDK-specific screen name for the submission step is
publicly documented.

## 5. Vehicle inventory accounting — floor plan, curtailment

Floor plan interest is **not** capitalized into vehicle inventory under GM's documented
treatment — it posts as a period expense against Interest Payable
([GM Interest Floorplan account](http://gm.acctmanual.com/Expenses/076_Interest_Floorplan.htm)).
Floor plan advances are typically repaid as inventory is sold, with a curtailment provision
requiring periodic principal reductions for stale inventory
([OCC Comptroller's Handbook, Floor Plan Lending](https://www.occ.treas.gov/publications-and-resources/publications/comptrollers-handbook/files/floor-plan-lending/pub-ch-floor-plan.pdf)).
PACCAR Financial Services operates dealer wholesale financing as a distinct segment
([PACCAR SEC 10-K filing](https://www.sec.gov/Archives/edgar/data/75362/000119312526057025/R32.htm)).

## 6. Warranty receivable accounting

Warranty claims create a GL receivable (GM `263 Warranty Claims`; Ford `1140 Warranty Claims
Receivable`) that is debited when a claim is filed and credited only when the factory pays or
rejects it, requiring aged schedule reporting by RO/claim number
([GM manual](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf);
[Digital Dealer](https://digitaldealer.com/news/your-dms-and-schedules/65829/)).

## 7. Proposed SAP-shape mapping

| CDK/dealer-accounting concept | Proposed SAP object/table | Rationale |
|---|---|---|
| GL account (3-digit + dept suffix) | `SKA1`/`SKB1` (GL account master) | Direct analog: natural account + cost-center-like department suffix |
| Department code (01–09) | Cost center or business area (`CSKS`/`TKA02`-style) | Departments are profit/cost segments, not separate legal entities |
| Schedule (controlled subledger) | `BSEG`/`BSID`/`BSAD` (open-item subledger line items) filtered by a control field | Schedules are SAP's open-item-managed subledger concept |
| GL control account for a schedule | Reconciliation account (`SKB1-MITKZ`) | SAP already enforces "no direct posting to a reconciliation account" |
| Journal type | Document type (`BKPF-BLART`) | Each named DMS journal is a document-type-scoped posting source |
| Posting period / closed-period lock | Posting period variant (`OB52`/`T001B`) | Same architectural control the SAP-side team already knows |
| Trial balance | `S001`/GL account balance display (`FAGLB03`/`FBL3N`) | Direct equivalent |
| Factory/OEM formatted statement | Custom drill-down report / FSV (`FSE2`) mapped from the same chart of accounts | FSV is SAP's native mechanism for multiple statement presentations off one COA |
| Floor plan payable / interest | Vendor/lender reconciliation account + periodic interest accrual document type | Standard AP-financing pattern; interest expensed, not capitalized |
| Warranty claims receivable | Customer (OEM) reconciliation account with open-item clearing by claim/RO reference (`BSID`) | Matches documented aged, RO-controlled receivable behavior |
| Fortellis `glpost`/`glwippost` APIs | Custom RFC/BAPI wrapper analogous to `BAPI_ACC_DOCUMENT_POST` | Both post a journal/document record into a live ledger from an external caller |

Pending items are tracked in [`docs/open-questions.md`](../docs/open-questions.md), including
the PACCAR-specific chart of accounts and CDK Drive's internal schedule table names.

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
