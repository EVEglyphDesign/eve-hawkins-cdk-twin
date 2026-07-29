# Architecture

**Status: wireframe / to be filled from lanes 1, 4, 6.** This document lays out the layered
model. Each layer names its real source systems and target shape; it does not yet contain
finished field mappings — those live in `modules/` and `schema/` as each lane's research
lands.

---

## The layers

The twin is organized as six layers, front to back: source systems the dealer group already
runs, an extract layer that pulls from them, a landing zone for raw pulls, a canonical
SAP-shape core, a set of semantic views over that core, and the surfaces that read from those
views.

```
┌─────────────────────────────────────────────────────────────────────┐
│  1. SOURCE SYSTEMS                                                  │
│     CDK Drive (via Fortellis REST) · PACCAR ePortal/eCat/Web Fleet  │
│     · CDK report-export / flat-file fallback path                  │
└───────────────────────────────┬───────────────────────────────────┘
                                 │  adapters/
┌───────────────────────────────▼───────────────────────────────────┐
│  2. EXTRACT                                                         │
│     One adapter per external system (not per site). Each adapter    │
│     handles its own auth, its own async start/poll/pull or          │
│     file-drop cadence, per adapters/*/README.md                    │
└───────────────────────────────┬───────────────────────────────────┘
                                 │
┌───────────────────────────────▼───────────────────────────────────┐
│  3. LANDING                                                         │
│     Raw pulled payloads staged as-received, before any field        │
│     mapping or SAP-shape transform is applied. Mirrors the async    │
│     long-operation pattern (Setup → Bulk → Delta) documented for    │
│     CDK Drive / Fortellis                                           │
└───────────────────────────────┬───────────────────────────────────┘
                                 │  schema/
┌───────────────────────────────▼───────────────────────────────────┐
│  4. CANONICAL SAP-SHAPE CORE                                        │
│     Column names mirror SAP MM/FI/CO/SD analogues (see              │
│     schema/README.md) so a PACCAR SAP payload maps 1:1 and the      │
│     dealer group's data model outlives any single DMS vendor        │
└───────────────────────────────┬───────────────────────────────────┘
                                 │
┌───────────────────────────────▼───────────────────────────────────┐
│  5. SEMANTIC VIEWS                                                  │
│     KPI and reporting views computed on top of the canonical core   │
│     — e.g. absorption rate, effective labor rate — never stored as  │
│     their own object, per the parts-twin's schema/kpi_views.sql     │
│     convention                                                      │
└───────────────────────────────┬───────────────────────────────────┘
                                 │
┌───────────────────────────────▼───────────────────────────────────┐
│  6. SURFACES                                                        │
│     Query/reporting surfaces reading only from layer 5 — never      │
│     directly from the landing zone or from a live source-system     │
│     call                                                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 1. Source systems

| System | Role | Access surface | Status |
|---|---|---|---|
| CDK Drive | Dealer-side system of record: sales, F&I, service/fixed-ops, parts, accounting, payroll | Fortellis REST APIs (OAuth 2.0, `Subscription-Id` + `Department-Id` + `Request-Id` header contract) | wireframe / to be filled from lane 1 — see [`adapters/cdk-fortellis/README.md`](adapters/cdk-fortellis/README.md) |
| PACCAR | OEM backbone: parts catalog, order history, warranty registration (PRWS), OPC e-commerce | PACCAR ePortal (SSO, no public REST API) / eCat / Web Fleet | wireframe — see [`adapters/paccar/README.md`](adapters/paccar/README.md) |
| Report-export fallback | Flat-file / scheduled-report path for any functional area not reachable by a documented API (e.g. AP three-way match, payroll flag hours, deal desk detail) | CDK Data Export/Import Tools, GL Inquiry Workflow, third-party payroll GL-push | wireframe — see [`adapters/export-fallback/README.md`](adapters/export-fallback/README.md) |

## 2. Extract

One adapter per external system, matching the convention already established in
[`eve-dealer-parts-twin/adapters/`](https://github.com/EVEglyphDesign/eve-dealer-parts-twin/tree/main/adapters).
Each of the 9 Peterbilt Atlantic sites is represented as a store/plant code inside the
relevant adapter, never as a separate adapter instance.

## 3. Landing

CDK Drive's own documented pattern for high-volume pulls is a three-step async operation:
start a job, poll `operationId` status, pull the result once `READY`
([Fortellis async pattern reference, via `eve-dealer-parts-twin`'s adapter README](https://github.com/EVEglyphDesign/eve-dealer-parts-twin/blob/main/adapters/cdk/README.md)).
The landing layer exists to hold that raw pulled result before any SAP-shape transform runs,
so a bad transform can be re-run against the same raw pull rather than re-querying CDK.

## 4. Canonical SAP-shape core

Table and column names mirror the closest SAP MM/FI/CO/SD analogue. The parts-inventory
shape (`MARA`/`MARC`/`MARD`/`MBEW`/`MATDOC`/`MVKE`/`MARM`/`MFRPN`) is already defined in
`eve-dealer-parts-twin/schema/` and is reused here rather than duplicated — see
[`schema/README.md`](schema/README.md) for the naming convention this repository adds on top
of it for the ledger, cost-object, master-data, and document-flow shapes.

## 5. Semantic views

KPIs such as absorption rate and effective labor rate are report-only computations over the
canonical core, not stored objects — following the same rule the parts-twin states explicitly
in its own `schema/kpi_views.sql`. This layer is where those views will live once the ledger
and cost-object shapes (modules 02 and 03) are finalized.

## 6. Surfaces

Not yet designed. Placeholder layer — no surface code exists in this repository yet.

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
