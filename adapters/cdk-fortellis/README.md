# CDK Drive (Fortellis) adapter

**Status: wireframe / to be filled from lanes 1, 4, 5, 6, plus the Lane B extract harness.**
Field-level mapping (`fields.md`) is not yet written. The runnable side of this adapter now
lives in [`../../extract/bin/`](../../extract/bin/) (`00_validate_access.py`,
`10_extract_metadata.py`, `20_extract_masters.py`, `30_extract_transactions.py`) and is
driven by [`../../extract/config/targets.yaml`](../../extract/config/targets.yaml) — see
[`../../extract/README.md`](../../extract/README.md) for the operator runbook. Every API
name below is confirmed via lane research; literal REST paths, pagination parameters, and
response envelope shapes used by the extract scripts are `UNVERIFIED` against a live tenant
until day one — each script's module docstring states its specific assumptions.

Pulls Peterbilt Atlantic's live DMS data — organization, ledger, cost objects, materials,
master data, and document flow — from CDK Drive via the **Fortellis** REST platform.

## What this adapter can and cannot reach — plainly

Per [`../../docs/model/model.json`](../../docs/model/model.json) (21 entities), copied
honestly, not rounded up:

- **FULL (documented, field-level schema confirmed):** customer master, repair order
  (header + labor + parts + sublet + technician punches, all nested in one call).
- **PARTIAL (endpoint or workflow documented, but schema/pagination gaps remain):**
  dealer/rooftop partition, vehicle/unit master, employee identifiers, GL journal
  posting, parts master/inventory (async bulk only), parts order/supersession, parts pick
  ticket, counter parts sale, deal jacket (FI Sales History bulk/delta — **read-only**,
  no write path for deal creation/update), technician time punch, work-in-process (mirrored
  off the RO status field, not a standalone object).
- **NONE — cannot be reached via this adapter, full stop:** vendor master, GL account
  master, accounting schedule, warranty claim, purchase/receipt document, cost
  centre/department master. These route through
  [`../export-fallback/`](../export-fallback/README.md) instead — see that adapter's
  README for the mechanism (DMS UI export, or hand capture on day one).

The practical consequence: **the ledger cannot be pulled by API at all.** Every GL-side
object needed for the tie-out (chart of accounts, accounting schedules, department master)
is a `NONE` above and must come from a file export or a screen capture, never from this
adapter.

## What it ingests

| Fortellis API | Twin target | Refresh cadence | Module |
|---|---|---|---|
| `CDK Drive Get Repair Order v3` | RO header/parts/labor fields feeding `internalorder.sql`, materials movement, warranty draft trigger | Per-transaction / on-demand | 03, 04, 06 |
| `getOpenRepairOrdersBulk` | Bulk pull of open ROs (Appointment/WIP state) | Scheduled poll | 06 |
| `CDK Drive Async Parts Inventory` | `mard`, `mara`, `mfrpn` (inherited from parts twin schema) | Real-time async push | 04 |
| `CDK Drive Search Parts Pick Ticket` | `matdoc` (issue movement) | Per-transaction | 04 |
| `CDK Drive Async Open/Closed Parts Sales` | `matdoc`, parts-sale document state | Real-time | 04, 06 |
| `CDK Drive Get Parts Sales` / `History Setup Parts Sales` | Backfill parts sales history | Batch backfill | 04 |
| `CDK Drive Get Customer v3` | `kna1`/`knb1`, `consent_log` trigger fields (`optOutFlag`, `isDeleteDataFlag`) | Scheduled poll | 05 |
| `CDK Drive Service Vehicles API` | `zveh_service` | Scheduled poll | 05 |
| `glwippost` / `glpost` (Fortellis GL posting APIs, per Module 02) | `bseg` | Per-posting-batch | 02 |
| `CDK Drive Payment Settling API` (PayNow / Invite-2-Pay / PromiseID) | `zpromise_pay`, AR settlement postings | Per-transaction | 06 |

**Not in scope for this adapter — no confirmed CDK employee or vendor master API exists**
(Module 05 §3–§4). Payroll and some AP flows route through `adapters/export-fallback/`
instead.

Refs:
- [CDK Global Parts APIs overview](https://www2.cdkglobal.com/api-solutions-parts)
- [CDK Global Heavy Truck OEM page](https://www2.cdkglobal.com/ht-oem)
- [Fortellis community Q&A — Async Parts Inventory / Pick Ticket](https://community.fortellis.io/community/forum/qa/cdk-drive-search-parts-pick-ticket-and-cdk-drive-async-parts-inventory)
- [CDK Drive Get Repair Order v3 (Fortellis PDF)](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf)

## Auth

OAuth 2.0 through Fortellis. Standard three-header contract (confirmed in Module 01, lane 1):

- `Authorization: Bearer <token>`
- `Subscription-Id: <subscription>` (per Fortellis marketplace subscription)
- `Request-Id: <uuid>` (correlation)

Additional required header for CDK Drive APIs:

- `Department-Id: <cdk-dept-id>` — CDK organizes data by **department** (Accounting /
  Finance / Inventory / Parts / Service). Each of the 9 Peterbilt Atlantic sites will have
  its own department ID(s) per functional area in the CDK tenant, per the hierarchy documented
  in [`../../modules/01-organization.md`](../../modules/01-organization.md).

See [Fortellis CDK Drive API — bettrdata docs](https://docs.bettrdata.io/user-docs/how-to-guides/fortellis-cdk-drive-api)
for the three-step async pattern (start → poll → pull), the same pattern used by the parts
twin's [`adapters/cdk/README.md`](https://github.com/EVEglyphDesign/eve-dealer-parts-twin/blob/main/adapters/cdk/README.md).

## Credentials

```
CDK_FORTELLIS_API_KEY=
CDK_FORTELLIS_API_SECRET=
CDK_FORTELLIS_SUBSCRIPTION_ID=
# One department ID per site per functional area — exact department taxonomy
# (Accounting/Finance/Inventory/Parts/Service department IDs per site) is
# UNVERIFIED until confirmed against the live Peterbilt Atlantic tenant.
CDK_DEPT_ID_PA01=
CDK_DEPT_ID_PA02=
CDK_DEPT_ID_PA03=
CDK_DEPT_ID_PA04=
CDK_DEPT_ID_PA05=
CDK_DEPT_ID_PA06=
CDK_DEPT_ID_PA07=
CDK_DEPT_ID_PA08=
CDK_DEPT_ID_PA09=
```

## Async flow

Every CDK Drive API follows: **start → poll status → pull result** (confirmed pattern, per
lane 1 and the parts twin's existing adapter).

```
POST /<resource>/bulk                                        → returns operationId
GET  /<resource>/long-operations/{operationId}/status         → poll until READY
GET  /<resource>/long-operations/{operationId}/result         → download dataset
```

`ingest.py` for this repo (not yet written) should reuse this loop across every bulk API
listed in "What it ingests" above, landing rows per the schema proposed in
[`../../schema/README.md`](../../schema/README.md).

## Known operational risk

CDK Drive was taken offline for roughly 19 days in June–July 2024 by the BlackSuit ransomware
group, affecting an estimated 15,000 North American dealerships
([CNN](https://www.cnn.com/2024/07/11/business/cdk-hack-ransom-tweny-five-million-dollars)).
This adapter is the single point of failure this repo's sovereign-twin architecture exists to
reduce — see [`../export-fallback/README.md`](../export-fallback/README.md) for the fallback
path when this adapter is unreachable, and
[`../../docs/current-state.md`](../../docs/current-state.md) for the architectural rationale.

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
