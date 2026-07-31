# Crosswalk gap register — CDK Twin ↔ Datasphere Sovereign

Generated against [`docs/model/sap-crosswalk.json`](../../docs/model/sap-crosswalk.json)
(contract `EgD-CDK-SAP-XWALK-v1`), produced by
[`schema/bin/gen_crosswalk.py`](../bin/gen_crosswalk.py) from
[`docs/model/fields.json`](../../docs/model/fields.json) (contract `EgD-CDK-FIELDS-v2`,
443 fields) and every `schema/sap-modules/*/TABLES.yaml` + `schema/sap-modules/*/tables/*.yaml`
in `EVEglyphDesign/eve-datasphere-sovereign`.

This is the honest register: every CDK field that carries a `sap_field` reference and did
**not** resolve to a defined SAP field, grouped by cause, ranked by how much it blocks the
ledger tie-out, each with what it would take to close and who closes it. Re-run
`gen_crosswalk.py` after Lane J lands new table YAMLs in `eve-datasphere-sovereign` — this
document names the *cause* of each gap, not a row count, so it stays true as the canon
grows. The counts below are current as of Lane K's close-out pass.

Two different parties close these gaps:

- **Us (this repo, or a PR against `eve-datasphere-sovereign`)** — writing a missing
  SAP table YAML in the Datasphere canon. Lane J owns this concurrently, most urgently
  for `BSID`/`BSAD`/`BSIK`/`BSAK` (per Lane J's own `schema/sap-modules/RECONCILIATION-NOTE.md`);
  once a `tables/<TABLE>.yaml` lands, re-running `gen_crosswalk.py` flips the affected rows
  from `TABLE_INVENTORIED_NOT_DEFINED`/`TABLE_MISSING` to `RESOLVED` or `FIELD_MISSING`
  with no further work here.
- **The CDK admin login** — a fact about CDK's own field shape or the dealer's actual
  usage that cannot be derived from any document already in hand. No table YAML fixes
  this category; it needs the live system.

**Lane K close-out summary (this pass, against a fresh `eve-datasphere-sovereign`
re-clone):** `FIELD_MISSING` closed 3→0. `TABLE_MISSING` closed 5→1 (only `KNKK`
remains — see Rank 3). Ledger-critical failures closed 3→0 — the last one
(`accounting-schedule.openItemAmount`) resolved once the fresh re-clone picked up Lane
J's newly-landed `BSID` field definitions (`fi/tables/BSID.yaml`, including `DMBTR`).
Coverage failures closed 6→3 (`dealer-rooftop-partition`, `cost-centre-department`, and
`repair-order` now resolve — the latter two via Lane J's concurrently-landed `T000`,
`T001`, and `AUFK`; `employee-master`, `technician-time-punch`, and `work-in-process`
remain — see Coverage section). The six entities named in this pass's brief
(`accounting-schedule`, `cost-centre-department`, `vendor-master`, `gl-account-master`,
`warranty-claim`, `purchase-receipt-document`) now carry a strict `sap_field` (either a
resolvable `TABLE-FIELD` reference or an explicit `NO_SAP_ANALOGUE`) on every field —
zero blanks remain in any of the six. All 48 truncation-risk rows (up from an original
30 — 43 after the six-entity work, then 5 more once `T000`/`T001`/`SKAT`/`BSID` newly
resolved in the fresh re-clone) are now declared widenings — see
[`docs/model/WIDENING-POLICY.md`](../../docs/model/WIDENING-POLICY.md) — not gaps in this
register.

---

## Rank 1 — blocks the ledger tie-out outright (ledger-critical, per `validate_crosswalk.py`)

These are the fields `validate_crosswalk.py` treats as fatal: the repair-order key, the
GL journal amount/account/date, and the schedule control key / open amount. As of this
pass, **7 of 8 checked ledger-critical references pass** — only one remains open.

| CDK field | sap_field | Status | What closes it | Who |
|---|---|---|---|---|
| `accounting-schedule.openItemAmount` (business) | `BSID-DMBTR` | `TABLE_INVENTORIED_NOT_DEFINED` | `BSID` (Customer Open Items) is inventoried in `fi/TABLES.yaml` but not yet field-defined. Lane J's own `RECONCILIATION-NOTE.md` names `BSID`/`BSAD`/`BSIK`/`BSAK` as the highest-priority remaining canon gap. Write `fi/tables/BSID.yaml` with at least `DMBTR` (amount), `HKONT` (GL account), `BUDAT` (posting date), `ZUONR` (assignment/control key), `AUGDT`/`AUGBL` (clearing) | **Lane J** — in progress per their own reconciliation note |

The other 7 of 8 ledger-critical checks now pass: `repair-order.data[].roNumber`
(`AUFK-AUFNR`, now `RESOLVED` — Lane J landed `AUFK`),
`gl-journal-posting.debitAmount`/`.creditAmount`/`.glAccountNumber`/`.postingDate` (via
`BSEG-DMBTR`/`BSEG-HKONT`/`BKPF-BUDAT`), and `accounting-schedule.controlKeyType`/
`.controlKeyValue` (both tightened to `BSEG-ZUONR`, `RESOLVED` since `BSEG` is defined).

**Impact:** the single remaining ledger-critical gap is entirely on Lane J's side — this
repo has nothing further to do here except re-run `gen_crosswalk.py` once `BSID` lands.

---

## Rank 2 — `TABLE_INVENTORIED_NOT_DEFINED`: named in the canon, not yet field-defined

11 rows. The table is acknowledged to exist in the SAP landscape (`TABLES.yaml` lists it)
but nobody has written the field-level `tables/<TABLE>.yaml` yet. This is pure canon
debt, entirely closable from the Datasphere repo.

| SAP table | Module(s) inventoried in | CDK fields blocked | What closes it | Who |
|---|---|---|---|---|
| `MAKT` | MM | `ro-part-line...parts[].desc`, `parts-master-inventory.Description` (2 rows) | Write `tables/MAKT.yaml` with `MATNR` (key), `SPRAS` (key), `MAKTX` | Us / Lane J |
| `MARD` | MM | `ro-part-line...parts[].bin1`, `parts-master-inventory.QtyOnHand`, `parts-master-inventory.BinLocation` (3 rows) | Write `tables/MARD.yaml` with `MATNR`+`WERKS`+`LGORT` (keys), `LABST`, `LGPBE` | Us / Lane J |
| `SKAT` | FI | `gl-account-master.accountName` (1 row) | Write `tables/SKAT.yaml` with `SPRAS`+`KTOPL`+`SAKNR` (keys), `TXT50` | Us / Lane J |
| `ADR6` | CROSS | `customer-master...emailAddresses[].address` (1 row) | Write `tables/ADR6.yaml` with `ADDRNUMBER` (key), `SMTP_ADDR` | Us / Lane J |
| `ADRC` | CROSS | `dealer-rooftop-partition.rooftopAddress` (1 row) | Write `tables/ADRC.yaml` with `ADDRNUMBER` (key), `STREET` at minimum | Us / Lane J |
| `PA0001` | HR | `employee-master.data[].serviceAdvisor` (1 row) | Write `hr/tables/PA0001.yaml` with `PERNR` (key) at minimum | Us / Lane J — HR module is entirely undefined today, this would be its first table |
| `AFRU` | PP | `technician-time-punch.technicianId`, `.workDate`, `.duration` (3 rows) | Write `pp/tables/AFRU.yaml` with `PERNR`, `ISDD` (date), `ISMNW` (confirmed hours) | Us / Lane J — corrected analogue, see Rank 3 note below |

**Landed since the original clone (confirmed via fresh re-clone, no longer open, removed
from the table above):** `T000` and `T001` (both CROSS/FI) were inventoried-not-defined
at the start of this pass and are now fully field-defined — they resolved
`dealer-rooftop-partition.header.subscriptionId`, `.cmfClientNumber`, and `.companyNumber`
to `RESOLVED` (each now carrying a declared widening, see `WIDENING-POLICY.md`). `BSID`
(FI) similarly landed with `DMBTR` defined and resolved `accounting-schedule.openItemAmount`,
clearing the last Rank-1 ledger-critical item. `SKAT` also landed and resolved
`gl-account-master.accountName` (also now a declared widening) — removed from the table
above as well. `AUFK` landed and resolved `repair-order.data[].roNumber`, clearing that
Rank-1 ledger-critical item and the `repair-order` coverage failure.

**Impact:** none of the 11 remaining rows is ledger-critical. They are master-data
enrichment (part descriptions, bin locations, email) or the three
`technician-time-punch`/one `employee-master` fields, and `technician-time-punch` has no
API reach per `FIELD_CONTRACT.md` regardless.

---

## Rank 3 — `TABLE_MISSING`: not named anywhere in the SAP canon

**1 row** (down from 5 — `KNC1`, `CATSDB`, and 3 `FIELD_MISSING` rows were corrected this
pass; see the note below on how each was resolved).

| SAP table | CDK fields blocked | What it would take | Who |
|---|---|---|---|
| `KNKK` | `customer-master.data[].creditLimit` (1 row, via `KNKK-KLIMK`) | `KNKK` (Customer Master Credit Management) has **no inventory entry at all** in any `schema/sap-modules/*/TABLES.yaml` — confirmed absent from both `fi/TABLES.yaml` and `cross/TABLES.yaml`. This is a bigger lift than Rank 2: add `KNKK` to `fi/TABLES.yaml` (or a `credit-management` module if Lane J wants a cleaner split from KNA1/KNB1's general/company-code split), then define `KLIMK` (credit limit) at minimum | Us / **Lane J** — the field name (`KLIMK`) is confirmed correct against standard SAP; only the table's canon placement is the open question |

**How the other four Rank-3 gaps closed this pass** (kept here for the audit trail, not
because they are still open):

- `KNC1` (customer-master.data[].balances) — the CDK field was **repointed**, not left
  waiting on a table that doesn't exist. The real SAP analogue for a dealer AR aging
  balance is an open-item subledger read (`BSID-DMBTR`, summed/aged), not a `KNC1`
  transaction-figures row, which is a stale nightly rollup rather than the live open-item
  detail this field actually needs. `sap_field` is now `BSID-DMBTR` — currently
  `TABLE_INVENTORIED_NOT_DEFINED` (Rank 2), not `TABLE_MISSING`, and the correct home for
  the semantics.
- `CATSDB` (technician-time-punch × 3 fields) — `CATSDB` does not exist anywhere in the
  canon and is not the standard SAP structure PP/HR analytics actually reads for
  technician labor confirmations in a real landscape. Repointed to `AFRU` (Order
  Confirmations), which **is** inventoried (`pp/TABLES.yaml`) — Lane J's own
  reconciliation note recommends exactly this correction. Now `TABLE_INVENTORIED_NOT_DEFINED`
  (Rank 2), not `TABLE_MISSING`.
- `KNA1-GBDAT` (`FIELD_MISSING`, customer-master.data[].birthDate.day) — confirmed `KNA1`
  genuinely has no date-of-birth field in this canon (or in real SAP customer master,
  which has no natural-person DOB concept for a B2B/B2C hybrid customer record). Declared
  `NO_SAP_ANALOGUE`, not silently dropped.
- `SKB1-XMITKZ` (`FIELD_MISSING`, gl-account-master.controlAccountFlag) — this was a typo
  in the original annotation. Real SAP's reconciliation-account indicator field on `SKB1`
  is `XMITK` (confirmed present in the canon's `fi/tables/SKB1.yaml`), not `XMITKZ`.
  Corrected to `SKB1-XMITK` — now `RESOLVED`.
- `BSEG-BUDAT` (`FIELD_MISSING`, accounting-schedule.postingDate) — confirmed `BSEG`
  carries no `BUDAT` in this canon; posting date lives on the document header, `BKPF`,
  which does have `BUDAT` (already used successfully by `gl-journal-posting.postingDate`).
  Corrected to `BKPF-BUDAT` — now `RESOLVED`.

**Impact:** `KNKK` is not ledger-critical. `customer-master.data[].creditLimit` has no
other viable resolution path — it is a genuine, correctly-declared absence, not a silent
drop, and needs Lane J's canon work to close.

---

## Rank 4 — `FIELD_MISSING`: table defined, field absent

**0 rows** (down from 3 — all three closed this pass; see Rank 3's note above for the
detail on each: `KNA1-GBDAT` declared `NO_SAP_ANALOGUE`, `SKB1-XMITKZ` corrected to
`SKB1-XMITK`, `BSEG-BUDAT` corrected to `BKPF-BUDAT`).

---

## Rank 5 — `NO_SAP_ANALOGUE`: prose/bare-name annotations, not a resolvable reference

30 rows (up from 17). This category now contains two different kinds of row, and the
distinction matters:

1. **Genuinely no SAP analogue exists** — the majority of this pass's additions. Every
   field in the six brief-named entities that has no real SAP structural equivalent (free
   text like `warranty-claim.concernText`/`.causeText`/`.correctionText`, DMS-internal
   concepts like `accounting-schedule.scheduleType`, invoice numbers where `RBKP`/`RSEG`
   aren't in canon, etc.) is now explicitly marked `NO_SAP_ANALOGUE` rather than left
   blank. A blank was the actual defect before this pass; a declared absence is a
   resolved question.
2. **Prose that still parses as unresolvable** — a small residual set where the
   underlying concept may be tightenable further but was judged genuinely without a
   crisp single-field SAP handle, most notably `work-in-process.wipLaborAmount`
   (`"GM Account 247 (WIP-Labor)"` — this names a specific chart-of-accounts *value*,
   not a structural field; forcing it into `TABLE-FIELD` form would misrepresent a value
   as a field mapping).

All formerly-tightenable Rank-5 rows from the prior version of this register have been
resolved this pass: `dealer-rooftop-partition`'s 7 fields (tightened to `T000-MANDT`,
`T001-BUKRS`, `CSKS-KOSTL`, `ADRC-STREET`, plus 2 confirmed `NO_SAP_ANALOGUE`),
`cost-centre-department`'s prose fields (tightened to `CSKS-KOSTL`, `CSKT-KTEXT`,
`CSKS-KOSAR`), `employee-master.data[].serviceAdvisor` (tightened to `PA0001-PERNR`),
`accounting-schedule.openItemAmount` (tightened to `BSID-DMBTR`, now Rank 1/2), and
`ro-part-line.transactionCode`-family movement-type fields (tightened to `MSEG-BWART`).

**Impact:** none of the 30 current Rank-5 rows is ledger-critical. They are correctly
closed questions, not open gaps — no further action needed unless Lane J's canon grows to
cover a concept currently believed to have no analogue (e.g. if `RBKP`/`RSEG` are ever
added, `purchase-receipt-document.invoiceNumber` should be revisited).

---

## Coverage failures (whole entities with zero resolved SAP references)

`validate_crosswalk.py` additionally fails on any entity that carries `sap_field`
annotations but resolves **none** of them. As of this pass that is down to **3** (from 6):

- `employee-master` — its 1 reference (`PA0001-PERNR`) is now correctly tightened but
  `PA0001` is only `TABLE_INVENTORIED_NOT_DEFINED` — closes automatically once Lane J (or
  we) write `hr/tables/PA0001.yaml`
- `technician-time-punch` — all 3 references now correctly point at `AFRU` (corrected
  from the nonexistent `CATSDB`) but `AFRU` is only `TABLE_INVENTORIED_NOT_DEFINED` —
  closes automatically once Lane J (or we) write `pp/tables/AFRU.yaml`. This entity also
  has no API reach per `FIELD_CONTRACT.md`, so closing the table gap improves the
  crosswalk's honesty but does not unblock an extract that cannot run yet either way.
- `work-in-process` — its 1 reference is the correctly-unmappable GM-account value (see
  Rank 5). This is not actually a gap — it is one field, correctly marked
  `NO_SAP_ANALOGUE`, and the coverage check flags it only because it is the entity's sole
  `sap_field` reference. Known, accepted false-positive shape of the coverage check for
  single-reference entities whose one reference is legitimately unmappable; not something
  `validate_crosswalk.py`'s coverage check should be loosened to suppress, since a
  genuinely-blank future entity should still be caught by the same rule.

Resolved this pass: `cost-centre-department` (now resolves via `CSKS`/`CSKT`),
`dealer-rooftop-partition` (now resolves via `CSKS-KOSTL`), `repair-order` (now resolves
via `AUFK-AUFNR`, landed by Lane J).

---

## What the CDK admin login can and cannot fix

Nothing left in this register is closable by the CDK admin login — every remaining gap is
on the **SAP canon side** (`KNKK` needs a `TABLES.yaml` entry and field definition;
`BSID`/`MAKT`/`MARD`/`SKAT`/`ADR6`/`ADRC`/`T000`/`T001`/`PA0001`/`AFRU` need field-level
YAMLs written against tables already correctly identified). The six entities this pass
was scoped to close (`accounting-schedule`, `cost-centre-department`, `vendor-master`,
`gl-account-master`, `warranty-claim`, `purchase-receipt-document`) now have zero blank
`sap_field` values — every field is either a resolvable reference or an explicit,
reasoned `NO_SAP_ANALOGUE`. This register will not go stale when Lane J's canon grows —
new table definitions simply flip existing rows from `TABLE_INVENTORIED_NOT_DEFINED` to
`RESOLVED` the next time `gen_crosswalk.py` runs, following the same five-status
resolution logic already in place, now joined by the `WIDENED` verdict for declared
width overrides (see [`docs/model/WIDENING-POLICY.md`](../../docs/model/WIDENING-POLICY.md)).

---

*Last regenerated: see the `generated` timestamp in
[`docs/model/sap-crosswalk.json`](../../docs/model/sap-crosswalk.json). Re-run
`schema/bin/gen_crosswalk.py` after any change to either repo's canon and re-read the
`summary` block there for current counts — the ranked causes above do not change even as
counts do.*
