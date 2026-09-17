# Warranty GENE Warehouse Wireframe — v0.1

**Lane:** Hawkins Twin Platform / CDK Twin · **Extract set:** 2026-09-17 · **Status:** wireframe, proven against real extracts

This directory is the structured database wireframe for the Peterbilt Atlantic warranty
lane. It converts a pile of ad-hoc CDK Drive report exports and PACCAR warranty
registration reports into one grain-declared star schema with a single join spine, so
that every downstream worklist, dashboard and alert reads one shape and no other.

It is a **wireframe**: schema, grain, keys, transforms, marts and data-quality rules.

## Custody

**No dealer rows are committed to this repository.** This repo holds the index, the
rules and the schema — never the payload. The loader reads a dealer-owned extract
directory and writes the database file outside the repository tree. The only published
artefact derived from the data is `profile/2026-09-17-extract-profile.json`, which
contains row counts and aggregates and no customer, VIN or contract row.

## The join spine — VIN8

The single most important finding in this extract set: **VIN8 joins the manufacturer
record to the dealer record.** CDK's `Vehicle ID` on the repair order carries the
8-character VIN suffix, and every PACCAR warranty-registration row is keyed on `VIN8`.

```
PACCAR warranty registration  ──VIN8──►  dim_unit  ◄──VIN8──  CDK repair order history
    (P026 P032 P046 P048)                                       (Closed ROs, Open ROs)
```

Measured yield on the 2026-09-17 set:

| | Units |
|---|---|
| Distinct units in `dim_unit` | 2,991 |
| Warranty-registered (PACCAR side) | 1,060 |
| Service-known (CDK RO side) | 2,267 |
| **Both sides — fully reconciled** | **336** |

The secondary key is the customer: CDK's legacy Pick `NAME-FILE` encodes the customer
number as `<store_prefix>*<customer_number>`, which resolves 818 of the 821 customers
appearing on repair orders back to the customer master. Registered-owner name is *not*
a usable join — only 65 of 534 manufacturer-side owner names match a CDK RO customer
name exactly, which is exactly why the model joins on VIN8 and treats names as attributes.

## Model

Six dimensions, three facts, two reconciliation aggregates, one quarantine table, six marts.

**Dimensions** — `dim_unit` (VIN8), `dim_customer`, `dim_rooftop`, `dim_warranty_option`,
`dim_service_advisor`, `dim_date`.

**Facts** — `fact_warranty_registration` (grain: VIN8 × warranty option, manufacturer truth),
`fact_repair_order` (grain: one RO, open and closed unioned under `ro_status`, dealer truth),
`fact_service_contract` (grain: one contract, BRP/Torque lane, VIN17-keyed with VIN8 derived).

**Aggregates** — `agg_customer_service_period`, `agg_customer_total_sales`. These are
tie-out instruments only. They are never a scoring input; a pre-aggregated total cannot
be attributed to a VIN and must not be allowed to look as if it can.

**Quarantine** — `dq_exception`. Nothing is silently dropped. Every unjoinable vehicle ID,
unparseable date and unknown customer lands as a row with a rule code and a severity.

Full ERD in [the entity-relationship diagram](ERD.md). DDL in
[`ddl/wireframe.sql`](ddl/wireframe.sql). Field-level lineage for all 40 mapped columns in
[`mapping/extract_to_model.csv`](mapping/extract_to_model.csv).

## Marts — the only shapes GENE may read

| View | Grain | Purpose |
|---|---|---|
| `v_unit_coverage_state` | VIN8 × option | coverage window state against a run date, both axes |
| `v_unit_service_profile` | VIN8 | RO count, last visit, max odometer, lifetime sales |
| `v_rich_target` | VIN8 | active coverage plus a reachability class |
| `v_whitespace_registered_never_serviced` | VIN8 | registered in territory, never in the bays |
| `v_coverage_expiring_180d` | VIN8 | expiry pressure inside two quarters |
| `v_serviced_unregistered` | VIN8 | serviced here, no manufacturer registration on file |

`v_rich_target` classes every unit with live coverage by how the dealership can actually
reach it:

| Reach class | Units | Expiring within 180 days |
|---|---|---|
| `ON_SITE_NOW` — on an open RO today | 60 | 14 |
| `KNOWN_CUSTOMER` — has RO history here | 205 | 35 |
| `REGISTERED_NEVER_SERVICED` — registered in territory, never serviced | 508 | 68 |

## What the wireframe already shows

- **773 units carry live manufacturer coverage**, holding 1,802 active coverages —
  1,236 engine, 273 aftertreatment, 257 vehicle, plus emissions, electrical, towing
  and cab-clothing lines.
- **60 units with active coverage are on an open repair order right now.** One is
  1 day from time expiry. This is the pre-RO decision window GENE exists to serve.
- **508 registered units have never been serviced at any of the three rooftops.**
  That is 48% of the manufacturer-registered population, addressable by city because
  the registration record carries the owner's city.
- **170 of 650 time-active coverages are already past their mileage ceiling.** Coverage
  is a two-axis test — months *and* miles — and a time-only filter would mis-flag every
  one of them. `v_unit_coverage_state` therefore exposes `is_time_active` and
  `miles_remaining_est` as separate columns and refuses to collapse them into one boolean.
- Warranty work is **14.7% of service sales** in the extract window, against $30.0M
  customer-pay. The wireframe's job is to move that share deliberately rather than by accident.
- Dealer-side history in scope: 7,534 closed repair orders, $12.11M total sales,
  $5.90M gross profit, 2024-10-01 through 2026-09-16, across three service accounts
  (`PBNS-S`, `PBDT-S`, `PNBDL-S`) under one accounting account (`PNB-A`).

## Boundary

GENE fires **before** the repair order exists. PACCAR's PRWS remains authoritative on
claim filing, and nothing in this model submits, adjudicates or authorises a claim.
`v_rich_target` produces a prompt for a service writer to decide — a review filter,
not a verdict.

## Running it

```bash
python bin/build_wireframe_db.py \
  --src /dealer-owned/path/to/extracts \
  --db  /dealer-owned/path/out/cdk_wireframe.db \
  --profile-out profile/$(date +%F)-extract-profile.json
```

The loader is idempotent, rebuilds from scratch each run, and prints an
aggregate-only profile. It expects `P026.csv`, `P032.csv`, `P046.csv`, `P048.csv`,
`Closed ROs.csv`, `Open ROs.csv`, `Customers.csv`, `service customer sales.csv`,
`Customer total sales.csv`, `Advantage plus customers.csv` and
`Canada General contracts.csv`. Missing files are recorded as `SOURCE_MISSING`
warnings rather than failing the run, because the extract set arrives in pieces.

SQLite is the wireframe target because it is inspectable with no server. The DDL is
deliberately portable to the Azure PostgreSQL landing zone that the CDK Twin ingestion
pipeline targets; see [`DATA-QUALITY.md`](DATA-QUALITY.md) for the promotion gates that
must pass before a Postgres load is trustworthy.

---

© 2026 EVEglyphDesign. All rights reserved. Controlled copy.
*Pour le bien-être du peuple.*
