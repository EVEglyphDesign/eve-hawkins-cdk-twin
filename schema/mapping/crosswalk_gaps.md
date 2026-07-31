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
`gen_crosswalk.py` after Lane I lands new table YAMLs — this document names the *cause*
of each gap, not a row count, so it stays true as the canon grows. The counts below were
current as of the last regeneration noted at the bottom of this file.

Two different parties close these gaps:

- **Us (this repo, or a PR against `eve-datasphere-sovereign`)** — writing a missing
  SAP table YAML in the Datasphere canon. Lane I owns this concurrently for AUFK and
  others; once a `tables/<TABLE>.yaml` lands, re-running `gen_crosswalk.py` flips the
  affected rows from `TABLE_INVENTORIED_NOT_DEFINED`/`TABLE_MISSING` to `RESOLVED` or
  `FIELD_MISSING` with no further work here.
- **The CDK admin login (tomorrow, per Luke)** — a fact about CDK's own field shape or
  the dealer's actual usage that cannot be derived from any document already in hand.
  No table YAML fixes this category; it needs the live system.

---

## Rank 1 — blocks the ledger tie-out outright (ledger-critical, per `validate_crosswalk.py`)

These are the fields `validate_crosswalk.py` treats as fatal: the repair order key, the
GL journal amount/account/date, and the schedule control key / open amount. As of the
last run, **4 of 8 checked ledger-critical references fail.**

| CDK field | sap_field | Status | What closes it | Who |
|---|---|---|---|---|
| `repair-order.data[].roNumber` (PK) | `AUFK-AUFNR` | `TABLE_INVENTORIED_NOT_DEFINED` | Write `schema/sap-modules/co/tables/AUFK.yaml` (or pm/pp — AUFK is inventoried in all three) with at least `AUFNR`, `AUART`, `KOKRS`, `KOSTL` defined | **Us / Lane I** — this is the canonical known gap named in `ALIGNMENT_BRIEF.md` |
| `accounting-schedule.controlKeyType` (key) | *(none)* | no `sap_field` at all | CDK's `fields.json` does not yet assert which SAP field the schedule control key type maps to (candidate: the assignment/reference field family — `BSEG-ZUONR`/`XBLNR`/`AUFNR`, per the brief). Needs a `sap_field` value added to `fields.json` first (Lane F's file, not ours to edit), then this crosswalk will pick it up automatically. | **CDK admin login** — confirm which of ZUONR/XBLNR/AUFNR the dealer's control key actually behaves like, or Lane F if the mapping is already knowable from documentation |
| `accounting-schedule.controlKeyValue` (key) | *(none)* | no `sap_field` at all | Same as above — needs a `sap_field` value in `fields.json` before this crosswalk has anything to resolve | **CDK admin login** / Lane F |
| `accounting-schedule.openItemAmount` (business) | `BSEG amount (analogue)` | `NO_SAP_ANALOGUE` (prose, not `TABLE-FIELD`) | The intent is clear (`BSEG` line amount) but the field name was never specified. Tighten to `BSEG-DMBTR` or `BSEG-WRBTR` in `fields.json`, matching whichever currency field the open-item subledger actually reports | **Lane F** (fields.json owner) to tighten the annotation; the target table `BSEG` is already `RESOLVED`-capable in the canon (`fi/tables/BSEG.yaml` exists) |

The other 4 of 8 ledger-critical checks pass today: `gl-journal-posting.debitAmount`,
`.creditAmount`, `.glAccountNumber`, and `.postingDate` (via `BKPF-BUDAT`, distinct from
the `accounting-schedule.postingDate` gap below) all resolve to `RESOLVED` against `BSEG`/`BKPF`.

**Impact:** the repair-order key gap is the single highest-leverage fix available to us —
one YAML file (or Lane I landing it) flips 4 crosswalk rows (`repair-order.roNumber` ×2
entities' worth, `ro-labour-line.roNumber`, `ro-part-line.roNumber`, plus
`repair-order.payType`) from unresolved to resolved and clears the top ledger-critical
failure. The two schedule control-key rows cannot be closed from this repo alone — they
need a `sap_field` value that does not exist yet in `fields.json`.

---

## Rank 2 — `TABLE_INVENTORIED_NOT_DEFINED`: named in the canon, not yet field-defined

11 rows. The table is acknowledged to exist in the SAP landscape (`TABLES.yaml` lists it)
but nobody has written the field-level `tables/<TABLE>.yaml` yet. This is pure canon debt,
entirely closable from the Datasphere repo, and exactly the category Lane I is working
concurrently.

| SAP table | Module(s) inventoried in | CDK fields blocked | What closes it | Who |
|---|---|---|---|---|
| `AUFK` | CO, PM, PP | `repair-order.roNumber`, `repair-order.payType`, `ro-labour-line.roNumber`, `ro-part-line.roNumber` (4 rows) | Write `tables/AUFK.yaml` with `AUFNR` (order number, key), `AUART` (order type), `KOKRS`, `KOSTL` at minimum | **Lane I** (in progress per brief) |
| `MAKT` | MM | `ro-part-line...parts[].desc`, `parts-master-inventory.Description` (2 rows) | Write `tables/MAKT.yaml` with `MATNR` (key), `SPRAS` (key), `MAKTX` | Us / Lane I |
| `MARD` | MM | `ro-part-line...parts[].bin1`, `parts-master-inventory.QtyOnHand`, `parts-master-inventory.BinLocation` (3 rows) | Write `tables/MARD.yaml` with `MATNR`+`WERKS`+`LGORT` (keys), `LABST`, `LGPBE` | Us / Lane I |
| `SKAT` | FI | `gl-account-master.accountName` (1 row) | Write `tables/SKAT.yaml` with `SPRAS`+`KTOPL`+`SAKNR` (keys), `TXT50` | Us / Lane I |
| `ADR6` | CROSS | `customer-master...emailAddresses[].address` (1 row) | Write `tables/ADR6.yaml` with `ADDRNUMBER` (key), `SMTP_ADDR` | Us / Lane I |

**Impact:** closing `AUFK` alone clears 4 rows including the top ledger-critical gap
(Rank 1). The remaining four tables (`MAKT`, `MARD`, `SKAT`, `ADR6`) are master-data
enrichment fields (part descriptions, bin locations, GL account long text, email) — real
gaps, but none is ledger-critical on its own.

---

## Rank 3 — `TABLE_MISSING`: not named anywhere in the SAP canon

5 rows, across 2 tables. These tables have no inventory entry at all in any
`schema/sap-modules/*/TABLES.yaml` — a bigger lift than Rank 2 because even the module
placement has not been decided.

| SAP table | CDK fields blocked | What it would take | Who |
|---|---|---|---|
| `KNC1` | `customer-master.data[].balances` (1 row, via `KNC1-SLD03 (analogue)`) | Add `KNC1` (Customer Master — Transaction Figures) to `fi/TABLES.yaml`, then define it. Field name in `fields.json` is already annotated `(analogue)` — the dealer concept (aging balance) does not map cleanly to a single SAP field even once KNC1 exists | Us (add inventory + define), but the mapping itself needs Lane F to confirm which SLD0x bucket, if any, is the right analogue |
| `KNKK` | `customer-master.data[].creditLimit` (1 row) | Add `KNKK` (Customer Master Credit Management) to `fi/TABLES.yaml` and define `KLIMK` at minimum | Us / Lane I |
| `CATSDB` | `technician-time-punch.technicianId`, `.workDate`, `.duration` (3 rows) | Add `CATSDB` (Time Sheet — cross-application) to a module (likely `cross` or `hr`) and define `PERNR`, `WORKDATE`, `STDAZ` | Us / Lane I |

**Impact:** none of these is ledger-critical. `technician-time-punch` has NO API reach
per `FIELD_CONTRACT.md`'s known-reach table, so this data arrives by file/screen export
regardless of whether `CATSDB` is ever defined — closing the table gap improves the
crosswalk's honesty but does not unblock an extract that cannot run yet either way.

---

## Rank 4 — `FIELD_MISSING`: table defined, field absent

3 rows. The table YAML exists and is well-formed, but the specific field the CDK side
wants was not included when the table was defined (these SAP tables have 80+ fields in
reality; the canon's YAML files carry a working subset).

| SAP table.field | CDK field | What closes it | Who |
|---|---|---|---|
| `KNA1-GBDAT` | `customer-master.data[].birthDate.day` | Add `GBDAT` (Date of Birth) to `fi/tables/KNA1.yaml` | Us / Lane I — trivial addition to an existing file |
| `SKB1-XMITKZ` | `gl-account-master.controlAccountFlag` | Add `XMITKZ`-equivalent (reconciliation account indicator) to `fi/tables/SKB1.yaml` — note real SAP calls this `MITKZ`/`XKRES`-family; confirm exact field name before adding | Us, but verify the real SAP field name first (this may be a `fields.json` annotation error, not a canon gap — see note below) |
| `BSEG-BUDAT` | `accounting-schedule.postingDate` | Add `BUDAT` to `fi/tables/BSEG.yaml` (note: `BKPF-BUDAT` is already defined and used successfully by `gl-journal-posting.postingDate` — `BUDAT` legitimately also lives on `BSEG` as a redundant/denormalized copy in real SAP, so this is a genuine add, not a duplicate) | Us / Lane I |

**Note on `SKB1-XMITKZ`:** real SAP's reconciliation-account indicator on SKB1 is
typically `XMITKZ` is not a standard SKB1 field name we can confirm from the leanx.eu-style
sources this canon cites elsewhere — this may be an annotation drawn from ERP convention
rather than a confirmed CDK/SAP source. Flag for Lane F to double check the intended field
name before Lane I spends effort adding a field that turns out to be misnamed.

**Impact:** all three are single-field additions to already-defined tables — the cheapest
gaps to close in this entire register, and none is ledger-critical.

---

## Rank 5 — `NO_SAP_ANALOGUE`: prose/bare-name annotations, not a resolvable reference

17 rows. These `sap_field` values in `fields.json` do not parse as strict `TABLE-FIELD`
(e.g. `"Client (Mandant) MANDT"`, `"PERNR (personnel number analogue)"`,
`"GM Account 247 (WIP-Labor)"`). Some of these *do* point at a real, resolvable SAP field
once tightened to `TABLE-FIELD` form; others are legitimately DMS-only concepts with no
crisp SAP handle. This crosswalk generator cannot guess which — that decision belongs to
whoever owns `fields.json` (Lane F), because tightening the annotation changes the
contract's own data, which is out of scope for this lane's owned paths.

| CDK field | Current `sap_field` text | Likely tightenable to | Genuinely no analogue? |
|---|---|---|---|
| `dealer-rooftop-partition.header.subscriptionId` | `Client (Mandant) MANDT` | `T000-MANDT` | No — tighten |
| `dealer-rooftop-partition.cmfClientNumber` | `Client (Mandant) MANDT` | `T000-MANDT` | No — tighten |
| `dealer-rooftop-partition.companyNumber` | `Company code BUKRS` | `T001-BUKRS` (not yet in canon — `T001` is not inventoried anywhere either, a secondary `TABLE_MISSING`) | No — tighten, but also needs `T001` added to canon |
| `dealer-rooftop-partition.header.departmentId` | `Cost center (analogue)` | `CSKS-KOSTL` (CSKS is `RESOLVED`-capable — already defined in `co/tables/CSKS.yaml`) | No — tighten |
| `dealer-rooftop-partition.dmsType` | `Module/component (analogue)` | — | Likely yes — CDK's own product-line concept |
| `dealer-rooftop-partition.rooftopName` | `General text — dealer master (analogue)` | — | Likely yes — dealer has no SAP business-partner master |
| `dealer-rooftop-partition.rooftopAddress` | `Address (analogue)` | `ADRC` (defined? no — `ADRC` is inventoried in `cross/TABLES.yaml` but not field-defined, another `TABLE_INVENTORIED_NOT_DEFINED` if tightened) | No — tighten, then also needs `ADRC.yaml` |
| `cost-centre-department.departmentCode` | `Cost center / profit center (KOSTL)` | `CSKS-KOSTL` | No — tighten |
| `cost-centre-department.departmentId` | `Cost center (KOSTL analogue)` | `CSKS-KOSTL` | No — tighten |
| `cost-centre-department.departmentName` | `Cost center description (KTEXT)` | `CSKT-KTEXT` (CSKT is `TABLE_MISSING` — not inventoried) | No — tighten, needs CSKT added |
| `cost-centre-department.scheduleIndex` | `Reconciliation account subledger type (analogue)` | — | Likely yes, or `SKB1-MITKZ`-family if tightened — needs Lane F judgement |
| `customer-master.data[].overDues.over30Due` | `Aging bucket 1 (analogue)` | `KNC1-SLD03`-family (KNC1 is `TABLE_MISSING`) | No — tighten, needs KNC1 added |
| `employee-master.data[].serviceAdvisor` | `PERNR (personnel number analogue)` | `PA0001-PERNR` (HR module is inventoried by infotype only, `PA0001` exists in `hr/TABLES.yaml` but not field-defined) | No — tighten, then `TABLE_INVENTORIED_NOT_DEFINED` |
| `gl-account-master.departmentSuffix` | `KOSTL (cost center, appended)` | `CSKS-KOSTL` | No — tighten |
| `accounting-schedule.openItemAmount` | `BSEG amount (analogue)` | `BSEG-DMBTR` or `BSEG-WRBTR` (BSEG is `RESOLVED`-capable) | No — tighten (see Rank 1, this is the ledger-critical duplicate of this same row) |
| `ro-part-line.transactionCode` | `BWART (movement type analogue)` | `MSEG-BWART` (MSEG is `RESOLVED`-capable — already used successfully by `purchase-receipt-document.movementTypeSapAnalogue`) | No — tighten |
| `work-in-process.wipLaborAmount` | `GM Account 247 (WIP-Labor)` | — | Yes — this is explicitly a GM-brand chart-of-accounts convention (account 247), not a generic SAP field; it names a specific GL account *value*, not a field. Correctly has no SAP field analogue; the analogue is `SKA1-SAKNR` = '247'-equivalent as a **value**, not a structural mapping |

**Impact:** of the 17, roughly 12 look tightenable to a real `TABLE-FIELD` reference by
Lane F (mostly landing on `CSKS`/`CSKT`/`BSEG`/`MSEG`/`PA0001`/`KNC1`/`T000`/`T001`/`ADRC`),
which would immediately improve resolution once the canon side is also filled in. The
`work-in-process.wipLaborAmount` case is the one row in this entire register that is a
correctly-labeled `NO_SAP_ANALOGUE` — a chart-of-accounts value, not a field mapping — and
should stay that way rather than being forced into a fake `TABLE-FIELD` shape.

---

## Coverage failures (whole entities with zero resolved SAP references)

`validate_crosswalk.py` additionally fails on any entity that carries `sap_field`
annotations but resolves **none** of them. As of the last run that is:

- `cost-centre-department` — all 4 references are Rank-5 prose, all tightenable to `CSKS`/`CSKT`
- `dealer-rooftop-partition` — all 7 references are Rank-5 prose, all tightenable to `T000`/`CSKS`/`ADRC`
- `employee-master` — its 1 reference (`PERNR`) is Rank-5, tightenable to `PA0001`
- `repair-order` — both references point at `AUFK`, the Rank-1/Rank-2 gap
- `technician-time-punch` — all 3 references point at `CATSDB`, a Rank-3 `TABLE_MISSING`
- `work-in-process` — its 1 reference is the correctly-unmappable GM-account value

Four of these six (`cost-centre-department`, `dealer-rooftop-partition`,
`employee-master`, `repair-order`) resolve to zero purely because of annotation format or
one missing table YAML — cheap fixes once Lane F tightens the annotations and Lane I (or
we) add `CSKS`/`CSKT`/`T000`/`ADRC`/`PA0001`/`AUFK` field definitions. `technician-time-punch`
is blocked on both a missing table and, per `FIELD_CONTRACT.md`, has no API reach anyway.
`work-in-process` is not actually a gap — it is one field, correctly marked
`NO_SAP_ANALOGUE`, and the coverage check flags it only because it is the entity's sole
`sap_field` reference; this is a known, accepted false-positive shape of the coverage
check for single-reference entities whose one reference is legitimately unmappable.

---

## What tomorrow's CDK admin login can and cannot fix

Nothing in this register is closable by the CDK admin login alone — every gap here is on
the **SAP canon side** (a missing or incomplete `tables/<TABLE>.yaml`) or the
**annotation side** (`fields.json`'s `sap_field` text needs tightening). The login matters
for a different reason: it will surface CDK fields that currently have no `sap_field` at
all (`accounting-schedule.controlKeyType`/`controlKeyValue`, and the six NONE-API-reach
objects per `FIELD_CONTRACT.md`), and only once Lane F adds a `sap_field` value for those
will this crosswalk have anything to resolve against. This register will not go stale
when that happens — new `sap_field` values simply produce new rows the next time
`gen_crosswalk.py` runs, following the same five-status resolution logic already in place.

---

*Last regenerated: see the `generated` timestamp in
[`docs/model/sap-crosswalk.json`](../../docs/model/sap-crosswalk.json). Re-run
`schema/bin/gen_crosswalk.py` after any change to either repo's canon and re-read the
`summary` block there for current counts — the ranked causes above do not change even as
counts do.*
