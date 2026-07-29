# Schema — SAP-shape CDK twin

**Status: wireframe / to be filled from lanes 2, 3, 4, 5, 6.** No `.sql` DDL files exist yet
in this directory. This README lays out the proposed table set as derived from the module
research; each row's SAP analog and role is a **proposal**, not a confirmed CDK-to-SAP
mapping. Column-level DDL should not be written until the mappings in Modules 01–06 are
reconciled against a live CDK Drive tenant (see `docs/open-questions.md`).

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

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
