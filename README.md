# eve-hawkins-cdk-twin

**Sovereign digital twin of the CDK Drive DMS for Peterbilt Atlantic.**

Anchor deployment: Peterbilt Atlantic (9 locations, Hanwell HQ hub), Atlantic Canada.
Reusable pattern: any PACCAR / CDK Drive-backed heavy-truck dealer group.

**Status: wireframe.** This repository is the skeleton laid down before content lands. Every
module and adapter below carries an explicit status marker showing which research lane feeds
it. Nothing here should be read as a finished spec until that marker is cleared.

---

## Why this exists

CDK Drive is the dealer-side system of record for sales, F&I, service/fixed-ops, parts,
accounting, and payroll at a majority of North American dealer groups, including Peterbilt
Atlantic. It is a **single vendor-hosted DMS** — when it goes down (as in the June 2024
BlackSuit ransomware outage, which took ~15,000 dealers offline for roughly two weeks), the
dealer group has no independent copy of its own operational history. This twin exists so that
Peterbilt Atlantic — and, by the same reusable pattern, any other PACCAR/CDK dealer group —
owns a durable, queryable, SAP-shape copy of its own DMS data that outlives any single vendor
relationship.

This repository is the **CDK Drive rail**. It is a sibling to
[`eve-dealer-parts-twin`](https://github.com/EVEglyphDesign/eve-dealer-parts-twin), which
covers the PACCAR parts-inventory rail specifically, and to
[`eve-hawkins-telus-twin`](https://github.com/EVEglyphDesign/eve-hawkins-telus-twin), which
covers the TELUS call-history rail. Each twin follows the same design law: SAP-shape schema,
one adapter per external system, and an honest current-state accounting of what is built
versus what is aspirational.

---

## The six modules

CDK Drive's functional surface is organized here into six modules, each mapped onto its SAP
control-object analogue. See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the layered model that
ties them together.

| # | Module | What it covers | Status |
|---|---|---|---|
| 01 | [`modules/01-organization.md`](modules/01-organization.md) | Dealer/company/department/store hierarchy — CMF, Company Number, Department-Id, the 9-site topology | wireframe / to be filled from lane 1 |
| 02 | [`modules/02-ledger.md`](modules/02-ledger.md) | Chart of accounts, accounting schedules, journals, month-end close | wireframe / to be filled from lane 2 |
| 03 | [`modules/03-cost-objects.md`](modules/03-cost-objects.md) | Departments as cost/profit centres, the repair order as cost collector, technician time, absorption | wireframe / to be filled from lane 3 |
| 04 | [`modules/04-materials.md`](modules/04-materials.md) | Parts master, valuation, movements, ordering | wireframe / to be filled from lane 4 |
| 05 | [`modules/05-master-data.md`](modules/05-master-data.md) | Customer, vehicle, employee, vendor masters | wireframe / to be filled from lane 5 |
| 06 | [`modules/06-document-flow.md`](modules/06-document-flow.md) | Deal, repair order, counter ticket, warranty claim, AR/AP, payroll — the transactional document chains | wireframe / to be filled from lane 6 |

---

## Design principles

Carried over from `eve-dealer-parts-twin` and applied identically here:

- **SAP-shape schema.** Column and table names mirror the closest SAP MM/FI/CO/SD analogue.
  Never an invented CDK field name — every field mapping in this repository traces to a
  published CDK, Fortellis, or cross-DMS source, or is marked as an open question.
- **One adapter per external system, not per site.** CDK Drive (via Fortellis) is one adapter.
  PACCAR is one adapter. Each of the 9 sites is a plant/store row inside that one adapter, not
  a separate integration.
- **Honest current-state accounting.** [`docs/current-state.md`](docs/current-state.md) says
  plainly what is built, what is stubbed, and what is not yet started.
- **No invented endpoints.** If a Fortellis API name, header, or field cannot be traced to a
  public source, it is filed in [`docs/open-questions.md`](docs/open-questions.md) instead of
  guessed at.

---

## Repo layout

```
modules/         Six functional module write-ups (org, ledger, cost objects, materials,
                 master data, document flow) mapping CDK Drive onto SAP-shape objects
schema/          SAP-aligned table definitions for the canonical core
adapters/
  cdk-fortellis/  CDK Drive via the Fortellis REST platform — auth, async start/poll/pull
  paccar/         PACCAR ePortal / eCat / Web Fleet — the OEM-side rail
  export-fallback/ Flat-file / report-export path when neither API surface is available
docs/            Architecture notes, current-state audit, open-questions register,
                 and the public GitHub Pages landing page
```

---

## Related repos

- [eve-dealer-parts-twin](https://github.com/EVEglyphDesign/eve-dealer-parts-twin) — dealer
  parts-inventory digital twin, SAP-shape schema, PACCAR/CDK adapters, 9-location topology
- [eve-hawkins-telus-twin](https://github.com/EVEglyphDesign/eve-hawkins-telus-twin) — call
  history truth surface for Peterbilt Atlantic, Hawkins Twin lane

---

## Current-state analysis

See [`docs/current-state.md`](docs/current-state.md) for the honest audit of what is built
versus what is not, and [`docs/open-questions.md`](docs/open-questions.md) for the numbered
register of everything still unverified against a live CDK Drive tenant.

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
