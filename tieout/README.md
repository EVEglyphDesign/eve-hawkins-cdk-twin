# Tie-out — method

**Status: plan drafted, not yet run.** This is the proof step the whole exercise stands or
falls on: rebuild Peterbilt Atlantic's June 2026 (default middle month of the three-month
extraction window) financials from data captured independently of CDK's own reports, and show
the rebuild reconciles to what CDK and PACCAR actually reported. See the clickable version of
this chain at [`docs/tieout/index.html`](../docs/tieout/index.html) (live:
[the Tie-Out Board](https://eveglyphdesign.github.io/eve-hawkins-cdk-twin/tieout/)), and the
data behind it in [`docs/tieout/tieout-plan.json`](../docs/tieout/tieout-plan.json).

Reads from `extract/out/2026-06/` (and, for a small number of checks, `extract/out/2026-05/`
and `extract/out/2026-07/` for items that clear across the month boundary). That extract output
belongs to the extract lane of this build — see [`docs/extract/`](../docs/extract/) — and does
not exist yet as of this writing. `tieout/bin/reconcile.py` is written to degrade gracefully
against that absence: see its own section below.

Why the middle month: June is the only month in a three-month window (May–July 2026 by
default) bracketed on both sides — May catches accounting-schedule items that opened before
the window and would otherwise look like phantom balances, July catches items that clear after
June closes and would otherwise look like unexplained drops. `DOCUMENTED (brief)`.

## Tolerance policy

Two-tier, modelled on the GM Dealer Standard Accounting Manual's own convention that a
reconciliation difference is a *named, bookable event* — "Adjustment for the difference
between the month-end schedule and the account balance" — not evidence the exercise failed
([GM Dealer Standard Accounting Manual](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf),
cited in [`modules/02-ledger.md`](../modules/02-ledger.md) §4).

| Tier | Rule | Action |
|---|---|---|
| Clean tie | Variance = \$0.00 and \(\lvert \text{variance} \rvert / \lvert \text{reported base} \rvert < 0.05\%\) | No entry required. Statement passes. |
| Tolerable variance | \(\lvert \text{variance} \rvert \le \$25.00\) per schedule/account, or \(\le 0.25\%\) of the reported base, whichever is greater | Logged in the break register as `INFO`, not a break. Typically timing — an in-transit posting, rounding on a flat-rate-hour conversion, or a document dated across midnight in a different timezone than the report engine. |
| Break | Exceeds the tolerable-variance threshold on any single schedule, GL account, or department line | Logged as `OPEN` with a required root-cause field. No statement below is considered tied out with an unresolved `OPEN` break. |

`INFERRED` — these thresholds are our proposal. Peterbilt Atlantic's own or PACCAR's tolerance
policy, if either publishes one, is `UNVERIFIED` and should override this on the day access lands.

## The five statements, in order of increasing difficulty

Each statement below is strictly harder to prove than the one before it: (a) only needs a row
count, (b) needs a schedule-to-GL sum, (c) needs a correct pay-type split across two record
types, (d) needs the whole chart of accounts to net to zero, and (e) needs a derived ratio to
match a KPI the dealer principal already watches — the softest number in the whole chain to pin
down, because two different, individually-reconciled inputs can still combine under different
allocation policies and disagree.

### (a) Transaction counts and dollars complete for the month

**Formula:** `count(rows in our extract, doc_date in [2026-06-01, 2026-06-30])` and
`sum(extended_amount)` per transaction class (repair order, RO labour line, RO part line,
counter parts sale, deal jacket, AP/purchase document, GL journal posting) — matched against
CDK's own row count/control total for the same class and month if captured at export time.

**Input files:** `extract/out/2026-06/repair_orders.jsonl`,
`extract/out/2026-06/ro_labour_lines.jsonl`, `extract/out/2026-06/ro_part_lines.jsonl`,
`extract/out/2026-06/counter_parts_sales.jsonl`, `extract/out/2026-06/deal_jackets.jsonl`,
`extract/out/2026-06/ap_documents.jsonl`, `extract/out/2026-06/gl_journal_postings.jsonl`.

**Expected variance sources:** pagination cut off early on a bulk/async pull (repair-order,
RO labour/parts, counter-parts-sale, and deal-jacket are the highest-confidence sources per
[`docs/model/model.json`](../docs/model/model.json) — `full` or `partial` API reach — so a gap
here is more likely an extraction bug than a real missing document); a document type excluded
from the export filter by mistake; a document dated in a different timezone than the report
engine, landing one day outside the window.

**Pass criterion:** row count and dollar sum match within the tolerable-variance tier above,
for every transaction class in scope. This is the floor every later statement inherits — do not
proceed to (b) until (a) is clean or every variance is logged.

### (b) Each accounting schedule's open items sum to its GL account balance at month-end

**Formula:** for each controlled schedule (warranty claims receivable, new-vehicle floor plan,
factory receivables, contracts in transit, service/parts WIP —
[`modules/02-ledger.md`](../modules/02-ledger.md) §2), `sum(open_item_amount where status =
'open' as of 2026-06-30, grouped by control_key)` must equal the GL control account's own
month-end balance for that account.

**Input files:** `extract/out/2026-06/accounting_schedules/*.jsonl` (one file per schedule
type, control key = RO#, stock#, VIN-last-8, or claim#), rolled up against
`extract/out/2026-06/gl_journal_postings.jsonl` filtered to the matching account number.

**Expected variance sources:** a manual journal entry posted directly to a reconciliation
account, bypassing the schedule (blocked natively in SAP via the `SKB1-MITKZ` reconciliation
flag; `UNVERIFIED` whether CDK Drive enforces the equivalent — see
[`modules/02-ledger.md`](../modules/02-ledger.md) §7); a schedule item that cleared on the
schedule report but whose GL reversal posted a day late; an aged warranty claim rejected by the
factory but not yet written off on our side.

**Pass criterion:** every schedule ties to its GL account within tolerance. `accounting-schedule`
and `gl-account-master` both have `none` for API reach in
[`docs/model/model.json`](../docs/model/model.json) — both sides of this check come from
screen-driven report export, not the API, so a break here is as likely to be an export-capture
gap as a real dealership variance.

### (c) Departmental gross profit rebuilt from RO labour/parts lines matches the reported department income statement

**Formula:** for each department (New Vehicle, Used Vehicle, Parts, Service, Body Shop,
Rental/Lease, F&I — [`modules/03-cost-objects.md`](../modules/03-cost-objects.md) §1), rebuild
gross profit as `sum(labour_sale_amount - labour_cost_amount) + sum(parts_sale_amount -
parts_cost_amount)` from RO labour and part lines, split by pay-type flag
(`hasCustPayFlag`/`hasIntPayFlag`/`hasWarrPayFlag`), plus counter parts sales for Parts. Compare
against the same department's gross-profit line on the reported June 2026 department income
statement.

**Input files:** `extract/out/2026-06/ro_labour_lines.jsonl`,
`extract/out/2026-06/ro_part_lines.jsonl`, `extract/out/2026-06/counter_parts_sales.jsonl` —
`ro-labour-line` and `ro-part-line` are the two `full`-API-reach entities in the whole model
([`docs/model/model.json`](../docs/model/model.json)), making this the statement with the
strongest source-data confidence despite being the third-hardest to prove.

**Expected variance sources:** a pay-type misclassification (a warranty line booked to
customer-pay gross); an internal recon or PDI job whose cost never rolled up to the receiving
vehicle stock number ([`modules/03-cost-objects.md`](../modules/03-cost-objects.md) §5–6); an
overhead allocation applied at the department-statement level that our RO-line rebuild
intentionally excludes (this statement checks gross profit, not net department income, on
purpose — overhead allocation is checked separately at (e)).

**Pass criterion:** each department's gross profit ties within the tolerable-variance tier,
evaluated per department, not in aggregate — a large positive break in Service offsetting a
large negative break in Parts is not a pass.

### (d) Trial balance debits equal credits and roll to the reported balance sheet

**Formula:** `sum(debit_amount) - sum(credit_amount)` across every posted GL line in
`gl_journal_postings.jsonl` for June 2026 must equal exactly zero (a double-entry identity, not
an estimate); each account's net balance must then roll up to its line on the reported June
2026 balance sheet.

**Input files:** `extract/out/2026-06/gl_journal_postings.jsonl`, aggregated across the full
chart of accounts — no schedule detail needed at this step.

**Expected variance sources:** debits ≠ credits internally means a capture gap or a
doubled/dropped posting in *our own extract* — a real general ledger cannot be out of balance,
so this failure mode points at the extraction, not the dealership. Debits = credits internally
but a break in the roll-up to the reported balance sheet line means a chart-of-accounts mapping
error between our SAP-shape schema (`SKA1`/`SKB1`/`BSEG` per
[`modules/02-ledger.md`](../modules/02-ledger.md) §7) and CDK's own account numbers.

**Pass criterion:** debits = credits exactly (zero tolerance — this is arithmetic, not
estimation); each balance sheet line ties within the tolerable-variance tier.

### (e) Absorption rate recomputed from our data matches the reported figure

**Formula:** NADA/ATD Slide Guide formula
([`modules/03-cost-objects.md`](../modules/03-cost-objects.md) §8): `Total Absorption =
(used-vehicle + service + parts + body shop gross profit, from statement (c)) ÷ total
dealership expense (from statement (d))`; `Fixed Absorption = fixed-ops (service + parts + body
shop) gross profit ÷ total dealer expense, adjusted`. This statement is purely derived — no new
extract file, since absorption rate is report-only and never stored as its own GL object.

**Input files:** none beyond the outputs of statements (c) and (d) — this is the one statement
in the chain that reads no raw extract file directly.

**Expected variance sources:** because absorption is a ratio of two figures each already
reconciled individually, the most likely variance source if (c) and (d) are both clean is a
different overhead-allocation method than ours — square footage or headcount prorate versus a
gross-profit-contribution-share prorate
([`modules/03-cost-objects.md`](../modules/03-cost-objects.md) §7) — which is a policy
difference to confirm with the dealer controller, not a data error.

**Pass criterion:** recomputed absorption percentage matches the reported figure within the
tolerable-variance tier, expressed in percentage points rather than dollars (absorption is a
ratio). This is deliberately the last and hardest statement — if it fails while (c) and (d) both
pass, the finding is a *policy* gap, and is exactly as valuable as a clean pass.

## What "tied out" means for this exercise

All five statements pass, or every variance is logged in the break register with a tier, a root
cause, and either a closed date or a named owner. A signed tie-out statement — one line, dated,
naming both the EVEglyphDesign lane owner and Luke Weatherbie as the dealer-side counterpart —
is the final artifact. See the `signoff` block in
[`docs/tieout/tieout-plan.json`](../docs/tieout/tieout-plan.json).

## Running it

```
python3 tieout/bin/reconcile.py --month 2026-06 --extract-dir extract/out --out-dir tieout/reports
```

See [`tieout/bin/reconcile.py`](bin/reconcile.py) for the implementation — it runs statements
(a)–(e) above in order, reads the same file paths named in each statement, and writes both a
markdown and a JSON report plus a populated break register. It runs cleanly with `--help` and
degrades gracefully (marks each statement `NOT RUN — input file missing` rather than crashing)
for any month or file that does not exist yet, since `extract/out/` had not been built by the
other lanes as of this writing.

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all
rights reserved. Stewardship of rights of use and assignment for large public and institutional
usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of
authorship and intent.
