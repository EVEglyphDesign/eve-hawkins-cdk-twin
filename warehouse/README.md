# Warranty GENE Warehouse Wireframe — v0.1

**Lane:** Hawkins Twin Platform / CDK Twin · **Extract set:** 2026-09-17 · **Status:** wireframe, proven against real extracts

This directory is the structured database wireframe for the Peterbilt Atlantic warranty
lane. It converts a pile of ad-hoc CDK Drive report exports and PACCAR warranty
registration reports into one grain-declared star schema with a single join spine, so
that every downstream worklist, dashboard and alert reads one shape and no other.

It is a **wireframe**: schema, grain, keys, transforms, marts and data-quality rules.

## Scope — the truck business, and only the truck business

This model covers **Peterbilt Atlantic's truck lane**: the eight CDK service accounts
under accounting account `PNB-A`, the PACCAR warranty registrations behind those units,
and the customer and advisor masters that serve them. Every unit in it is a Class 8 or
medium-duty Peterbilt carrying PACCAR coverage — MX-11 and MX-13 engine, aftertreatment,
PACCAR TX-12 transmission and clutch, harness, tow, and base vehicle.

`TRPDT-S` belongs here. It is **TRP Dartmouth** — PACCAR's all-makes truck parts and
service brand — and its customers are fuel haulers and transport fleets, not powersports.

The **BRP / powersports lane is deliberately out of scope**: the Advantage Plus and
Canada General service contracts, the Warranty on Demand claim records, the BRP warranty
policy guide, and the Torque Motorsports retention reports. They are present in the
extract directory, and the loader logs each one as a `SCOPE_EXCLUDED` row in
`dq_exception` so the exclusion is auditable rather than silent. That lane is a different
VIN space with a different policy owner and belongs in its own model. Joining it onto a
truck VIN8 spine is how one machine's coverage gets attached to another's.

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

Six dimensions, two facts, two reconciliation aggregates, one quarantine table, eleven marts.

**Dimensions** — `dim_unit` (VIN8), `dim_customer`, `dim_rooftop`, `dim_warranty_option`,
`dim_service_advisor`, `dim_date`.

**Facts** — `fact_warranty_registration` (grain: VIN8 × warranty option, manufacturer truth),
`fact_repair_order` (grain: one RO, open and closed unioned under `ro_status`, dealer truth).

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
| `v_rooftop_extract_coverage` | service account | which of the eight rooftops actually have history |
| `v_unit_mileage_rate` | VIN8 | measured miles/day from the unit's own odometer readings |
| `v_system_weight` | system code | diagnostic exposure weight per covered system (policy) |
| `v_pre_ro_priority` | VIN8 | perishability on the binding axis, exposure, cost of contact |
| `v_diagnosis_queue` | VIN8 | the banded pre-RO work queue, P1 to P6 |

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
- **508 registered units have no service history in the extract set — an upper bound,
  not a count.** Closed history covers three of the group's **eight** service accounts,
  so a unit serviced only at `PNBM-S`, `PNBF-S`, `PQSP-S`, `PQC-S` or `TRPDT-S` appears
  here as whitespace and is not. Treat this view as a re-extract requirement, not a
  campaign list. See [Extract coverage](#extract-coverage-eight-rooftops-three-histories).
- **170 of 650 time-active coverages are already past their mileage ceiling.** Coverage
  is a two-axis test — months *and* miles — and a time-only filter would mis-flag every
  one of them. `v_unit_coverage_state` therefore exposes `is_time_active` and
  `miles_remaining_est` as separate columns and refuses to collapse them into one boolean.
- Warranty work is **14.7% of service sales** in the extract window, against $30.0M
  customer-pay. The wireframe's job is to move that share deliberately rather than by accident.
- Dealer-side history in scope: 7,534 closed repair orders, $12.11M total sales,
  $5.90M gross profit, 2024-10-01 through 2026-09-16 — but drawn from only **three of
  eight** service accounts, all under one accounting account (`PNB-A`). Those figures
  are a floor for the group, not the group.

## Extract coverage — eight rooftops, three histories

`dim_rooftop` is seeded from the **union** of the open and closed RO extracts, because
the two extracts do not cover the same dealership. Eight service accounts appear; only
three carry closed history. Labels are left `UNVERIFIED` until the dealership confirms
them — the codes are not decoded by guesswork.

| Service account | Closed ROs | Open ROs | Open WIP sales | Closed history present |
|---|---:|---:|---:|---|
| `PBNS-S`  | 3,036 | 33 | $48,089.69  | yes |
| `PBDT-S`  | 2,647 | 31 | $64,914.32  | yes |
| `PNBDL-S` | 1,863 | 27 | $63,236.60  | yes |
| `PNBM-S`  | 0 | 60 | $277,334.33 | **no** |
| `PNBF-S`  | 0 | 41 | $153,227.33 | **no** |
| `TRPDT-S` (TRP Dartmouth) | 0 | 30 | $68,495.06  | **no** |
| `PQSP-S`  | 0 | 20 | $133,463.93 | **no** |
| `PQC-S`   | 0 | 18 | $23,549.02  | **no** |

The five uncovered accounts hold **169 of 260 open repair orders — 65% of current work
in progress, and $656,069.67 of $832,310.28 in open sales.** The rooftops missing from
history are the busiest ones in the present. 125 distinct units are on an open RO at an
uncovered rooftop; 46 of them are warranty-registered and 31 already qualify for
`v_rich_target`.

Every uncovered account is recorded as a `ROOFTOP_CLOSED_HISTORY_MISSING` row in
`dq_exception` and is queryable through `v_rooftop_extract_coverage`. **Ask 1 of the
next extract request is closed ROs for all eight service accounts over the same window.**


## Opportunistic-diagnosis priority — the pre-RO queue

`v_diagnosis_queue` ranks the 703 units whose coverage is alive on **both** axes. 70
units with live months but a spent mileage ceiling are excluded on purpose. Bands are
instructions to a service writer; the score only orders work inside a band.

| Band | Units | Meaning |
|---|---:|---|
| `P1 IN THE BAY, CLOSING` | 5 | on an open RO now, 30 days or less on the binding axis |
| `P2 IN THE BAY` | 42 | on an open RO now, coverage live |
| `P3 CALL NOW, CLOSING` | 28 | RO history here, 90 days or less |
| `P4 CALL, SCHEDULE` | 120 | RO history here, coverage live |
| `P5 COLD, CLOSING` | 38 | registered only, 90 days or less |
| `P6 COLD, CAMPAIGN` | 470 | registered only, coverage live |

**Score** — 0-100. Perishability on the binding axis 60, diagnostic exposure by covered
system 25, cost of contact 15. System weights (`v_system_weight`) are `ENG` 4, `EMC` 4,
`A/T` 3, `VEH` 2, `ELEC` 2, `TOW` 1, `CLTH` 1. They are policy, held in a view so they
can be argued with rather than buried in a formula.

**The mileage clock.** `v_unit_mileage_rate` derives miles per day from each unit's own
odometer readings — two or more readings, 60 days or more apart, positive gain. Rates
above 1,200 miles/day are flagged `SUSPECT_ODOMETER` and never used to date an expiry.
**17 units read as safe on months and sit inside 90 days on miles; eleven of those show
more than six months left on the calendar, one shows 2,741 days.** A months-only expiry
report ranks the most urgent trucks in the file as low priority.

Where no rate can be measured the queue falls back to the months axis and says so via
`rate_status = 'NO_RATE'`. That is the whole cold lane — and 12 of the 13 covered units
on an open RO at `PNBM-S` right now, because Moncton's closed history was never
extracted. Their priority is understated for an extract reason, not a business one.

**Contact reach** — 188 of the 195 warm units (P1–P4) have a phone number on file, 167
have an email. The 508 cold units have no phone at all: registered owner name and city
only, resolving to 313 distinct owners across 241 cities, which makes that lane a
territory-rep list rather than a call list. Eleven owners hold four or more covered
units each.

**No claim-value estimate per row.** Without RO line detail there are no labour operation
codes or SRT hours, so the queue says which trucks are worth diagnosing and cannot say
what the diagnosis is likely to be worth.

### Outreach workbook

`bin/build_outreach_workbook.py` renders bands P1–P4 to an Excel workbook, one sheet per
band, every ranking signal as a column alongside the contact details held for the
customer on the unit's most recent RO, plus a coverage-detail sheet, a **CDK vs PACCAR**
sheet and a method sheet.

The `CDK vs PACCAR` sheet is the two-sided reconciliation: one row for every one of the
2,991 units in the model, the manufacturer extract's account of the unit set beside the
dealer system's account of it, and for any unit outside P1–P4 the reason it is outside.
`match_status` splits into **BOTH SIDES 336** (registered with PACCAR and serviced at a
rooftop whose history was extracted), **PACCAR ONLY 724** (registered in the territory,
no service history here) and **CDK ONLY 1,931** (serviced here, no PACCAR registration in
this extract set). The last figure is the size of the all-makes and out-of-territory book
and is the reason `v_rich_target` is smaller than the RO population.
**The workbook is dealer payload and is never committed here** — the script is committed,
the output is not.

```
python bin/build_outreach_workbook.py --db /path/to/cdk_wireframe.db \
       --out EVEglyphDesign_WarrantyGENE_Outreach_P1-P4_<date>.xlsx
```

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
`Customer total sales.csv`. Missing files are recorded as `SOURCE_MISSING` warnings
rather than failing the run, because the extract set arrives in pieces. Powersports
files sitting in the same directory are matched against `OUT_OF_SCOPE` and logged as
`SCOPE_EXCLUDED`, never loaded.

SQLite is the wireframe target because it is inspectable with no server. The DDL is
deliberately portable to the Azure PostgreSQL landing zone that the CDK Twin ingestion
pipeline targets; see [`DATA-QUALITY.md`](DATA-QUALITY.md) for the promotion gates that
must pass before a Postgres load is trustworthy.

---

© 2026 EVEglyphDesign. All rights reserved. Controlled copy.
*Pour le bien-être du peuple.*
