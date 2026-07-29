# Schema — SAP-shape CDK twin

**Status: load-ready.** Real `.sql` DDL now exists for all 21 entities, in both Postgres
and Snowflake dialects, generated straight from the field-level metadata dictionary — see
[**Load-ready generation — how this works**](#load-ready-generation--how-this-works) below
for the full story. The proposal-table narrative immediately below is kept for the module
research trail; the generated DDL in `schema/ddl/` is now the actual load-ready artefact.

Column names mirror SAP so a PACCAR-side or third-party payload maps 1:1, and the group's
data model outlives any single DMS vendor — same design principle as
[`eve-dealer-parts-twin/schema/`](https://github.com/EVEglyphDesign/eve-dealer-parts-twin/tree/main/schema),
which this schema extends rather than duplicates for the materials domain.

Reference: [SAP Material Master documentation](https://help.sap.com/docs/SUPPORT_CONTENT/ldm/3363506132.html).

## Tables inherited from the parts twin (materials domain — not redefined here)

These already exist as real DDL in `eve-dealer-parts-twin/schema/` and are reused, not
rebuilt, by this repo: `mara.sql`, `marc.sql`, `mard.sql`, `mbew.sql`, `matdoc.sql`,
`mvke.sql`, `marm.sql`, `mfrpn.sql`. Module 04 (`../modules/04-materials.md`) proposes
extensions to several of these (supersession chain, escalated point-of-sale cost columns,
core-charge columns, a new `lost_sales` fact table) — those extensions belong in this repo's
own migration files once written, not in the parts twin.

## Proposed new tables for this twin

| File | SAP analog | Role | Sourced from |
|---|---|---|---|
| `orgunit.sql` | `T001W` (plant) / `TVKO` (sales org) | Site/rooftop master — one row per Peterbilt Atlantic location | Module 01 |
| `ska1.sql` / `skb1.sql` | SKA1/SKB1 | Chart-of-accounts and company-code account master | Module 02 |
| `bseg.sql` | BSEG | Ledger line items (journal postings) | Module 02 |
| `fsv.sql` | FSV (financial statement version) | Reporting hierarchy for the NADA-format composite | Module 02, Module 06 §8 (via lane 8) |
| `costcenter.sql` | KS01/CSKS (cost center master) | Department-as-profit-center master | Module 03 |
| `internalorder.sql` | AUFK (internal order master) | Repair-order-as-internal-order analogue | Module 03 |
| `lost_sales.sql` | *(no SAP analog — new fact table)* | Demand-signal record for stock-outs flagged at POS | Module 04 §8 |
| `kna1.sql` / `knb1.sql` | KNA1/KNB1 | Customer master (general + company-code data) | Module 05 §1 |
| `zveh_service.sql` | *(custom — no SAP analog)* | Service-department vehicle record, keyed by VIN | Module 05 §2 |
| `zveh_stock.sql` | *(custom — no SAP analog)* | New/used truck inventory record | Module 05 §2 |
| `zveh_build.sql` | *(custom — no SAP analog)* | Factory build/chassis record fed from PACCAR's B2B infrastructure | Module 05 §2, Module 06 §7 (via lane 8) |
| `lfa1.sql` / `lfb1.sql` | LFA1/LFB1 | Vendor master (general + company-code data) | Module 05 §4 |
| `consent_log.sql` | *(no SAP analog — new fact table)* | CASL consent evidence log | Module 05 §6 |
| `zwarr_claim.sql` | *(custom — no SAP analog)* | PACCAR PRWS warranty claim record | Module 06 §4 (via lane 8) |
| `zpromise_pay.sql` | *(custom — no SAP analog)* | AR promise-to-pay tracking (`PromiseID`) | Module 06 §5 |
| `zweowe.sql` | *(custom — no SAP analog)* | Deal-desk We-Owe open-item tracking | Module 06 §1 |

## Design notes

- **Primary key discipline:** follows the parts twin's convention — a client-level master
  keyed by its natural business key (`MATNR` for parts, proposed `KUNNR` for customers,
  `LIFNR` for vendors, VIN for vehicles), with child tables inheriting that key plus their own
  scope key (site, company code, department).
- **Column-store target:** same target stack as the parts twin — ANSI SQL tested on DuckDB,
  portable to ClickHouse/Iceberg.
- **Custom (`Z`-prefixed) objects are a deliberate signal, not a shortcut.** Every `Z`-table
  above exists because no native SAP MM/SD/FI table was found in the module research that
  models the CDK or PACCAR concept at the fidelity required (e.g., a warranty claim is not a
  standard SAP object; a "promise to pay" is not a standard dunning object). Where research
  later locates a better-fitting native SAP object, the `Z`-table should be retired in favor
  of it — do not treat the `Z`-prefix as permanent.
- **No DDL has been written yet.** This file intentionally stops at the proposal-table level.
  Writing real `CREATE TABLE` statements before the field-level research in each module is
  reconciled against a live tenant risks baking in invented column names — see the repo-wide
  rule against inventing CDK fields or endpoints in `../README.md`.

---

## CDK-to-SAP object mapping (operator vocabulary), and JSON Schema files

**Added by the Lane B extract harness** (`extract/**`, `adapters/cdk-fortellis/**`,
`adapters/export-fallback/**`) to give the extract scripts in `extract/bin/` a concrete
normalisation target ahead of live-tenant DDL. This section maps the 21 entities in
[`docs/model/model.json`](../docs/model/model.json) to their SAP analogue in the operator's
own vocabulary — Luke Weatherbie thinks in dealer/DMS terms, not SAP terms, so this table
reads dealer-object -> SAP-object -> what that actually means for a controller:

- **Repair order ≈ internal order with a settlement rule.** A CDK repair order (RO) behaves
  like an SAP internal order (AUFK/COEP): it collects labor and parts cost, then settles to
  one of three payer schedules (customer / warranty / internal) exactly the way an internal
  order settles to a cost object.
- **Accounting schedule ≈ reconciliation account subledger.** A CDK accounting schedule is a
  list of open items (by RO, stock number, or VIN) sitting behind one GL control account —
  the same role SAP's reconciliation-account open-item list plays behind a control account.
- **Department ≈ cost centre.** CDK's department suffix on a GL account is the same
  dimension as an SAP cost centre (CSKS/CEPC) — it is how "which part of the store" gets
  reported without a separate GL account per department.
- **Parts master ≈ MM material master.** CDK's parts master/inventory record maps to the
  combination of SAP's MARA (material), MARC (plant data), and MBEW (valuation) — one CDK
  part number carries what SAP splits across three tables.

| CDK entity (`docs/model/model.json` id) | Name | SAP analogue | API reach | Field confidence mix |
|---|---|---|---|---|
| `dealer-rooftop-partition` | Dealer / Rooftop Partition | Company Code (T001) / Plant (WERKS) plus a module-scoping flag | partial | documented: 7 |
| `customer-master` | Customer Master | KNA1 (general customer master), per-store scoping like KNVV | full | documented: 10 |
| `vehicle-master` | Vehicle / Unit Master | Equipment master (EQUI), serialized — VIN as equipment number | partial | documented: 8, unverified: 1 |
| `employee-master` | Employee / Technician Identifiers | HR-adjacent Z-fields on transaction tables (no clean HR analogue) | partial | documented: 8 |
| `vendor-master` | Vendor / Supplier Master | LFA1 (vendor master, general data) | none | documented: 3, inferred: 2, unverified: 1 |
| `gl-account-master` | GL Account Master | SKA1/SKB1 (chart of accounts + company-code GL segment) | none | documented: 7 |
| `accounting-schedule` | Accounting Schedule | Reconciliation-account subledger / open-item list | none | documented: 3, inferred: 3 |
| `gl-journal-posting` | GL Journal / Posting | BKPF/BSEG (accounting document header + line items) | partial | documented: 5, inferred: 1 |
| `repair-order` | Repair Order | Internal order (AUFK/COEP) with a payer settlement rule | full | documented: 10 |
| `ro-labour-line` | RO Labour Line | Confirmation/activity allocation line (COEP) | full | documented: 7 |
| `ro-part-line` | RO Part Line | Goods movement / material consumption line (MSEG) | full | documented: 7 |
| `parts-master-inventory` | Parts Master / Inventory | MARA/MARC/MBEW combined | partial | documented: 9 |
| `parts-order-supersession` | Parts Order + Supersession | Purchase order (EKKO/EKPO) + material supersession chain | partial | documented: 7 |
| `parts-pick-ticket` | Parts Pick Ticket | Reservation / goods issue slip (MB1A-style) | partial | documented: 2, inferred: 4 |
| `counter-parts-sale` | Counter / Parts Sale | Sales order + billing document (VBAK/VBRK), cash/wholesale | partial | documented: 5, inferred: 1 |
| `deal-jacket-vehicle-sale` | Deal Jacket / Vehicle Sale | Sales order + billing document (VBAK/VBRK) + F&I lines | partial | documented: 6, inferred: 2 |
| `technician-time-punch` | Technician Time Punch | Time confirmation (CATS-style) feeding activity allocation | partial | documented: 5, inferred: 1 |
| `work-in-process` | Work-in-Process (WIP) | WIP account tied to internal order settlement | partial | documented: 4, inferred: 3 |
| `warranty-claim` | Warranty Claim | Debit memo / claims-management document vs. factory receivable | none | documented: 6 |
| `purchase-receipt-document` | Purchase / Receipt Document | Purchase order + goods receipt (EKKO/EKBE), 3-way match | none | documented: 5, inferred: 1 |
| `cost-centre-department` | Cost Centre / Department | Cost centre / profit centre (CSKS/CEPC) | none | documented: 7 |

"API reach" and the confidence mix are copied verbatim from
[`docs/model/model.json`](../docs/model/model.json) — do not re-derive or round these up.
Where an entity shows `none`, that is a finding (no Fortellis path exists), not a gap to
pad; see [`../adapters/export-fallback/README.md`](../adapters/export-fallback/README.md)
for how that data actually reaches the twin.

### `schema/jsonschema/*.schema.json`

One [JSON Schema](https://json-schema.org/) file per entity — the canonical target shape
the `extract/bin/*.py` scripts normalise rows into before anything is loaded into the SQL
tables proposed above. Each property carries:

- `x-cdk-field-name` — the literal CDK/Fortellis field name, never renamed silently
- `x-confidence` — `documented` / `inferred` / `unverified`, copied from
  [`docs/model/model.json`](../docs/model/model.json) at the field level (never uniform
  across an entity — see the mix column above)
- `x-source-title` / `x-source-url` — the original Fortellis doc or research source, where one exists

These are intentionally permissive (`additionalProperties: true`, nullable types) because
real tenant payloads are UNVERIFIED beyond the documented shape — see
[`../extract/README.md`](../extract/README.md) for how the extract scripts treat unknown
fields (never invented, always passed through and flagged).

---

## Load-ready generation — how this works

**Added by Lane F.** This is the piece that makes tomorrow's CDK admin login a *fill*,
not a *discovery*: the target tables already exist, in two dialects, before a single row
lands. Lane F owns exactly four paths — `schema/ddl/**`, `schema/bin/**`,
`schema/mapping/**`, and this README — and touches nothing under `docs/` or `extract/bin/`.

### What generates what

| Script | Reads | Writes |
|---|---|---|
| [`schema/bin/gen_ddl.py`](bin/gen_ddl.py) | `docs/model/fields.json` (contract `EgD-CDK-FIELDS-v2`, built by Lane D) | `schema/ddl/postgres/<entity_id>.sql` × 21, `schema/ddl/postgres/000_all.sql` rollup, `schema/ddl/snowflake/<entity_id>.sql` × 21 |
| [`schema/bin/gen_mapping.py`](bin/gen_mapping.py) | `docs/model/fields.json` | `schema/mapping/cdk_to_sap_field_map.csv` (one row per field), `schema/mapping/README.md` |
| [`schema/bin/validate_load_ready.py`](bin/validate_load_ready.py) | `docs/model/fields.json`, the generated `schema/ddl/**`, and [`extract/config/targets.yaml`](../extract/config/targets.yaml) | a pass/fail preflight report on stdout, exit code 0/1 |
| [`schema/bin/fixture_fields.py`](bin/fixture_fields.py) | nothing (self-contained) | a fixture matching the `EgD-CDK-FIELDS-v2` shape, used to build and test the three scripts above before Lane D's real file existed |

All four scripts are stdlib-only Python 3, have a clean `--help`, and are idempotent —
re-running any of them regenerates the same output from the same input, never appends or
drifts.

### Current status of this run

**`docs/model/fields.json` had not yet been published by Lane D at the time this was
built.** Per the Lane F brief, the generators were built and proven against
[`schema/bin/fixture_fields.py`](bin/fixture_fields.py) — a fixture that matches the exact
`EgD-CDK-FIELDS-v2` contract shape (same field attributes, same 21 fixed entity ids) but is
deliberately thin (4-5 representative fields per entity: a primary key, a currency field, a
date, an enum status code, and one cross-entity foreign key) so that every code path in the
generators is exercised: every datatype/unit mapping, NOT-NULL-only-when-DOCUMENTED, FK
resolution, system columns, and column comments.

Running the fixture through the pipeline today produced:

- **21 Postgres tables**, **21 Snowflake tables**, **169 total columns** (85 fixture fields
  + 4 system columns × 21 tables).
- **85 mapped rows** in `cdk_to_sap_field_map.csv` (confidence mix: 43 DOCUMENTED / 21
  INFERRED / 21 UNVERIFIED — an artefact of the fixture's fixed pattern, not a real
  confidence distribution).
- `validate_load_ready.py` **PASS**: every entity has DDL in both dialects, every
  `load_column` is unique and legal in both dialects, the one fixture FK
  (`ro-labour-line.repair_order_number` → `repair-order.repair_order_number`) resolves, and
  every entry in `extract/config/targets.yaml` maps to an existing table.

**This is a load-bearing test, not the deliverable.** The moment
[`docs/model/fields.json`](../docs/model/fields.json) is published, re-run:

```bash
python3 schema/bin/gen_ddl.py     --fields docs/model/fields.json --out-dir schema/ddl
python3 schema/bin/gen_mapping.py --fields docs/model/fields.json --out-dir schema/mapping
python3 schema/bin/validate_load_ready.py --fields docs/model/fields.json \
    --ddl-dir schema/ddl --targets extract/config/targets.yaml
```

This overwrites the fixture-derived `schema/ddl/**` and `schema/mapping/**` output with the
real field-level dictionary's output — same file paths, same shape, real numbers.

### How the extract lands in these tables

1. **Metadata phase first** ([`extract/config/targets.yaml`](../extract/config/targets.yaml),
   `phase: metadata`) fills the reference tables in
   [`schema/ddl/enums/000_enum_tables.sql`](ddl/enums/000_enum_tables.sql) and the
   metadata-group entity tables (`cdk_dealer_rooftop_partition`, `cdk_gl_account_master`,
   `cdk_accounting_schedule`, `cdk_cost_centre_department`, `cdk_employee_master`) — GL chart
   of accounts, schedule control keys, department suffixes, and code lists, before a single
   transaction row is pulled, per the brief's "metadata before transactions, always" rule.
2. **Masters and transactions phases** fill the remaining entity tables in the same load
   order as `extract/config/targets.yaml`: masters (customer, vehicle, vendor, parts) then
   transactions (repair order and its labour/part/punch children, counter sales, deal
   jackets) then ledger (GL journal postings, WIP, purchase/receipt documents).
3. Every row an extract script in `extract/bin/*.py` produces carries the four system
   columns generated onto every table here — `_rooftop_id`, `_extracted_at`,
   `_source_route` (`fortellis` \| `export` \| `screen`, matching `targets.yaml`'s `source`
   field), and `_batch_id` — so a load can be traced back to exactly which extract run and
   which of the three adapters (`adapters/cdk-fortellis`, `adapters/export-fallback`,
   screen-captured) produced it.
4. **Foreign keys are enforced only where `fk_target` resolves** (e.g. RO labour/part lines
   → repair order). Code-list columns (pay type, RO status, etc.) are deliberately **not**
   given hard FKs into `schema/ddl/enums/` — those lists are still partly UNVERIFIED, and a
   hard FK would reject a legitimate but not-yet-catalogued code on day one. Validate
   against the enum tables in the extract/load pipeline instead of the database constraint
   layer until the code lists are confirmed on tenant login.
5. **`NOT NULL` is only ever a live constraint when the source field is both `nullable:
   false` and `confidence: DOCUMENTED`.** Everywhere else the constraint is commented out
   in the generated DDL with the reason inline — never enforce a hard rule on an inference,
   because an UNVERIFIED field that turns out nullable in the real tenant would otherwise
   break the very first load.

### Enum / code-list reference tables

[`schema/ddl/enums/000_enum_tables.sql`](ddl/enums/000_enum_tables.sql) is hand-authored
(not generated from `fields.json`, which carries enum values inline per-field rather than as
a standalone catalogue) and covers the seven code lists named in the brief: pay type, RO
status, labour-op type, parts source, parts price class, GL account type, document type, and
schedule control key. Every seed row carries its own `confidence` column, and every table
ends in an `UNVERIFIED_STUB` row — a concrete place for tomorrow's tenant-login discovery to
insert newly-confirmed codes instead of starting from a blank table.

### Running the validator

```bash
python3 schema/bin/validate_load_ready.py --fields docs/model/fields.json \
    --ddl-dir schema/ddl --targets extract/config/targets.yaml
```

Checks performed: (1) every entity in `fields.json` has generated DDL in both dialects; (2)
every `load_column` is unique within its entity and a legal, unquoted, lowercase SQL
identifier with no reserved-word collision, checked against both dialects; (3) every
`fk_target` resolves to a real entity and a real column on it; (4) every extract target in
`extract/config/targets.yaml` maps to a table that exists in the generated DDL. Exits 0 on
pass, 1 on any failure, and prints the full list of what failed.

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
