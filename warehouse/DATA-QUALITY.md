# Data Quality — 2026-09-17 extract set

Nothing is silently dropped. Every rejection lands in `dq_exception` with a rule code
and a severity, and the counts below are reproducible by rerunning the loader.

| Rule | Severity | Count | Meaning |
|---|---|---|---|
| `VIN8_LENGTH` | WARN | 1,223 | RO rows whose `Vehicle ID` is not 8 or 17 characters, so they cannot reach the warranty registration |
| `DATE_PARSE` | WARN | 213 | PACCAR registration rows with a missing or unparseable in-service date — coverage end cannot be computed |
| `RO_DUPLICATE` | WARN | 12 | an RO number present in both the open and closed extract; the closed row wins |
| `CUST_UNKNOWN` | INFO | 3 | a customer on an RO absent from the customer master; a stub row is created |

## The five findings that constrain the model

**1. Vehicle ID is a VIN8, not a VIN.** 2,141 of 2,436 distinct CDK vehicle IDs are
8 characters, 245 are 6, and 4 are full 17-character VINs. The 6-character values
cannot be lengthened by inference and must not be fuzzy-matched to a VIN8 — a wrong
VIN match would attach one fleet's coverage to another fleet's truck. They are
quarantined, counted, and excluded from `v_rich_target`, which is why the mart
population is smaller than the RO population.

**2. The four PACCAR reports are disjoint partitions, not overlapping views.**
P026 (587 VINs), P032 (273), P046 (196) and P048 (4) share zero VIN8 between them,
and their city profiles differ — Fredericton and Dieppe in P026, Summerside and Cap Pelé
in P032, Kentville and Truro in P046, Quebec towns in P048. They union to exactly
1,060 units, which matches the count of `BASE/VEH` coverage rows exactly: one base
vehicle warranty per unit. Loading them as one union is therefore correct, and any
attempt to reconcile them against each other is wasted work.

**3. Coverage expiry has two axes and the mileage axis is already binding.** Of 650
time-active coverages where an odometer reading exists, 170 are already past their
mileage ceiling and 26 are within 25,000 of it. A time-only filter would present
170 dead coverages as live. `v_unit_coverage_state` exposes `is_time_active` and
`miles_remaining_est` separately and never collapses them.

**4. Owner name is not a join key.** Only 65 of 534 manufacturer-side registered-owner
names match a CDK RO customer name exactly. Registration owner is stored as an
attribute of the unit and is used for outreach copy, never for identity resolution.

**5. The aggregate extracts are not a population.** `Customer total sales.csv` is a
top-100 ranked report and `service customer sales.csv` covers 2,693 customers against
16,022 in the master. They are loaded into `agg_*` tables for tie-out and are barred
from scoring, because a customer-period total cannot be attributed to a VIN.

## Promotion gates — before any Azure PostgreSQL load is trusted

1. `dq_exception` carries zero `BLOCK` rows.
2. `SUM(total_sales)` over `ro_status='CLOSED'` ties to the closed-RO extract total
   ($12,105,138.15 on this set, 7,534 ROs).
3. `COUNT(*)` in `fact_warranty_registration` equals the summed source report rows
   less `VIN8_LENGTH/BLOCK` rejections (3,258 on this set).
4. Every `fact_repair_order.vin8` that is non-null is 8 characters.
5. `v_rich_target` contains no row whose nearest expiry is negative.
6. `dim_unit` row count equals the distinct union of registered and serviced VIN8
   (2,991 on this set).

## Known gaps in the extract set

- No RO **line detail** — the extracts are RO headers only. Labour operation codes,
  SRT hours, part numbers and the 3-C complaint text are absent, so margin estimate
  and 3-C compliance cannot yet be scored per job. This is the single highest-value
  addition to the next extract request.
- No claim-side data on the Peterbilt lane. PRWS claim history is not in this set,
  so booked-versus-eligible cannot be closed on the truck side yet.
- No SmartLINQ / PACCAR Solutions fault-code feed, so the event-driven rung is absent.
- Odometer arrives only via ROs, so units never serviced here have no mileage reading
  and their mileage axis is unknown — reported as `NULL`, never as zero.
