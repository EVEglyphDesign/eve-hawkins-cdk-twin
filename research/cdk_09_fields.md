# cdk_09_fields.md — Lane D: Field-Level Metadata Dictionary

**Deliverable:** `docs/model/fields.json` — contract `EgD-CDK-FIELDS-v2`, 21 entities, 439 fields total.

This note documents method, sources, and the per-entity field-count / confidence-mix
table for the v2 field dictionary. It supersedes v1 (`docs/model/model.json`, 151
fields / 21 entities) with a materially deeper pass, concentrated on the four
FULL-reach objects and honest, complete-in-concept field sets for PARTIAL/NONE objects.

## Method (cheapest rung first)

1. Re-used all field-level detail already extracted from the repo's nine `research/cdk_0*.md`
   files and the prior research pass in this lane (no re-fetch of those files was needed —
   the dense field lists for parts-master-inventory, parts-order-supersession,
   parts-pick-ticket, counter-parts-sale, deal-jacket-vehicle-sale, technician-time-punch,
   work-in-process, warranty-claim, and purchase-receipt-document were carried over directly
   from that prior extraction).
2. Two targeted primary-source fetches were made this lane to reach FULL-object depth:
   - **Get Repair Order v3** full spec PDF (Fortellis) — the single richest source, supplying
     essentially all fields for `repair-order`, `ro-labour-line`, `ro-part-line`, and the
     RO-linked portion of `technician-time-punch`.
   - **Get Customer v3** full spec PDF (Fortellis) — supplying essentially all fields for
     `customer-master`.
3. For NONE-reach objects (`vendor-master`, `gl-account-master`, `accounting-schedule`,
   `warranty-claim`, `purchase-receipt-document`, and effectively `cost-centre-department`),
   field sets were built from dealer-accounting convention, the GM/Ford dealer standard
   accounting manual patterns already cited in earlier research files, and — where a
   real dealer-DMS integration partner corroborates a workflow — the
   [Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar). No
   `source_url` was fabricated for any field where none exists; those fields are marked
   `INFERRED` or `UNVERIFIED` with an explicit note.
4. Enum/code lists were prioritized: CDK parts transaction codes, PACCAR MDI order types,
   fee type codes (Lube/Miscellaneous/Sublet), FI Sales status codes (flagged UNVERIFIED —
   codes are confirmed to exist, but their meanings are not confirmed), WIP status, and
   deal lifecycle stages.

## Sources used (with URLs)

- [Get Repair Order v3 spec (Fortellis)](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf)
- [Get Customer v3 spec (Fortellis)](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf)
- [Fortellis Community — CDK Drive Async Parts Inventory / Search Parts Pick Ticket Q&A](https://community.fortellis.io/community/forum/qa/cdk-drive-search-parts-pick-ticket-and-cdk-drive-async-parts-inventory)
- [Total Dealer Solutions — CDK Transaction Codes](https://totaldealersolutions.zendesk.com/hc/en-us/articles/360060331572-CDK-Transaction-Codes)
- [Karmak — PACCAR Integration](https://www.karmak.com/integrations/paccar)
- [CDK Global — API Solutions for Parts](https://www2.cdkglobal.com/api-solutions-parts)
- NHTSA safety recall bulletins (PACCAR steel-axle campaign context) and PACCAR/JW Speaker
  dealer-portal warranty-claim submission instructions (used for `warranty-claim` field
  concepts; no single stable field-schema URL exists for a non-public claim system).
- BettrData CDK FI Sales integration reference (used for `deal-jacket-vehicle-sale` status
  code names only — meanings UNVERIFIED).

Where no fetchable URL exists for a field, `source_url` is omitted and the field is marked
`INFERRED` or `UNVERIFIED` per contract rules (`DOCUMENTED` requires a field-level
`source_url`).

## Per-entity field count and confidence mix

| # | entity_id | fields | DOCUMENTED | INFERRED | UNVERIFIED | API reach |
|---|-----------|-------:|-----------:|---------:|-----------:|-----------|
| 1 | dealer-rooftop-partition | 8 | 4 | 2 | 2 | partial |
| 2 | cost-centre-department | 7 | 3 | 3 | 1 | none |
| 3 | customer-master | 82 | 81 | 0 | 1 | full |
| 4 | vehicle-master | 25 | 24 | 0 | 1 | partial |
| 5 | employee-master | 19 | 14 | 2 | 3 | partial |
| 6 | vendor-master | 12 | 0 | 10 | 2 | none |
| 7 | gl-account-master | 9 | 6 | 2 | 1 | none |
| 8 | accounting-schedule | 10 | 7 | 2 | 1 | none |
| 9 | gl-journal-posting | 11 | 2 | 9 | 0 | partial |
| 10 | repair-order | 74 | 74 | 0 | 0 | full |
| 11 | ro-labour-line | 40 | 39 | 1 | 0 | full |
| 12 | ro-part-line | 33 | 31 | 2 | 0 | full |
| 13 | parts-master-inventory | 18 | 14 | 4 | 0 | partial |
| 14 | parts-order-supersession | 9 | 2 | 7 | 0 | partial |
| 15 | parts-pick-ticket | 9 | 1 | 8 | 0 | partial |
| 16 | counter-parts-sale | 9 | 3 | 0 | 6 | partial |
| 17 | deal-jacket-vehicle-sale | 11 | 0 | 4 | 7 | partial |
| 18 | technician-time-punch | 11 | 9 | 0 | 2 | partial |
| 19 | work-in-process | 9 | 4 | 5 | 0 | partial |
| 20 | warranty-claim | 18 | 0 | 15 | 3 | none |
| 21 | purchase-receipt-document | 15 | 0 | 9 | 6 | none |
| | **TOTAL** | **439** | **318** | **85** | **36** | |

v1 comparison: 151 fields / 21 entities → v2: **439 fields / 21 entities** (2.9x depth),
concentrated on the four FULL-reach objects (repair-order family: 74+40+33=147 fields
alone) while every PARTIAL/NONE object still received a complete, honestly-marked
field set rather than a stub.

## Key judgment calls

- **FI Sales status codes (`deal-jacket-vehicle-sale.dealStatus`)**: the codes
  `C, B, P, F, I, U` are confirmed by name via a third-party integration reference, but
  their plain-English meanings are not confirmed anywhere found. Marked `UNVERIFIED` with
  explicit "Likely: ... (unconfirmed)" labels rather than asserting a mapping as fact.
- **Parts supersession**: confirmed to be a multi-hop chain (CDK function `PN`, reversible
  via "Undo Succession"), not a single-pointer field — modeled as
  `supersessionChainPartNumber` (self-referencing FK) rather than a flat "supersededBy" field.
  Marked `INFERRED` since no field-level schema page was found.
- **Warranty claim schedule control-key concept**: captured as real fields on
  `warranty-claim` (`glAccountClaimReceivable`, `agingBucket`) mirroring the
  `accounting-schedule` entity's control-key/control-value/open-item/aging-bucket/GL
  account/posting-date pattern, per the task brief's explicit instruction.
- **PACCAR ordering platform naming**: confirmed as **Online Parts Counter (OPC)** at
  `eportal.paccar.com`; the earlier-considered name "PartsPRO" was confirmed not to exist
  and is explicitly *not* used anywhere in this dictionary.
- **`technician-time-punch`** ended up far better documented than its PARTIAL label would
  suggest, because the entire `technicianPunchTimes[]` array is embedded verbatim in the
  Get Repair Order v3 response (a FULL-reach API). Only non-RO/indirect time punches
  (training, cleanup, PTO) remain UNVERIFIED, since the fetched RO spec only covers
  RO-tied punches.
- **No `source_url` was ever fabricated.** Every field lacking a real fetchable page is
  `INFERRED` or `UNVERIFIED`, per contract rule that `DOCUMENTED` requires a field-level
  `source_url`.

## Validation performed

- JSON parses cleanly (`json.load` round-trip).
- All 21 `entity_id` values present, in the fixed order, no extras/omissions.
- `load_column` unique within every entity (enforced programmatically in the build script).
- Every field has a `confidence` mark in `{DOCUMENTED, INFERRED, UNVERIFIED}` (enforced
  programmatically).
- Every `DOCUMENTED` field carries a real `source_url` (enforced programmatically; several
  fields were downgraded from `DOCUMENTED` to `INFERRED` during the build specifically
  because no URL could be honestly attached).
- `field_count` on each entity matches `len(fields)`.

Build script: `/home/user/workspace/laneD_build/build_fields.py` (not part of the repo;
working artifact only).
