# Module 01 — Organization

**Status: drafted from lane 1 research (`cdk_01_platform.md`). Not yet reconciled against a
live CDK Drive tenant — treat the hierarchy below as documented-but-unconfirmed at the
Peterbilt Atlantic instance level.**

Covers: dealer/company/department/store hierarchy — CMF, Company Number, Department-Id, and
how the 9 Peterbilt Atlantic sites are represented inside one CDK Drive tenant.

---

## 1. What CDK Drive is

CDK Drive is CDK Global's flagship dealer management system (DMS) — a single integrated
system of record for sales, F&I, service/fixed-ops, parts, accounting, and payroll across a
dealership ([CDK Drive product page](https://www.cdkglobal.com/dms/cdk-drive?x79rr9av=)).
CDK Global originated as ADP's Dealer Services division and spun off as an independent
company on October 1, 2014 ([Wikipedia](https://en.wikipedia.org/wiki/CDK_Global)).

**Drive Flex** is a separate, ground-up rewrite launched March 2018, targeted at 1–2 rooftop
dealers, AWS-hosted, usage-based pricing — not an upgrade path from Drive, and out of scope
for a 9-site group like Peterbilt Atlantic
([Auto Remarketing](https://www.autoremarketing.com/ar/technology/cdk-introduces-new-dms-pricing-model-dealers-operating-1-or-2-locations/)).

## 2. Internal hierarchy: Dealer ID → Company Number → Department ID → store

| Level | What it is | API surface | Status |
|---|---|---|---|
| **CMF / Client # (Dealer ID)** | Top-level CDK client identifier tied to a dealership's DealerSuite/eStore account | Not an API header itself — the anchor for Subscription-Id issuance | DOCUMENTED ([CDK Recruit landing page](https://www2.cdkglobal.com/l/146251/2016-04-29/4rg77?Business_Unit_Code=...), [DealerTrack 3PA authorization guide](https://us.dealertrack.com/wp-content/uploads/sites/2/2020/08/Dealertrack%20CDK%20Authorization%20Process.pdf)) |
| **Company ID / Company Number ("Co ID")** | Store-level accounting entity inside a Dealer/CMF | Legacy/EDI integration layer; not confirmed as its own REST header | DOCUMENTED at the legacy layer ([Mitchell RepairCenter CDK setup guide](https://www.mymitchell.com/tchs/helpfiles/RepairCenter/1033/Content/18181.htm)) |
| **Subscription-Id** | Fortellis-issued ID per app-user (dealer) relationship | `Subscription-Id` header — REQUIRED on every Fortellis CDK Drive call | DOCUMENTED ([CDK Drive Get Customer v3 spec](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf)) |
| **Department ID** | Identifies the specific DMS department/module targeted; each Department ID is bound to exactly one DMS type (Accounting, Finance, Inventory, Parts, Service) | `Department-Id` header — REQUIRED, response data filtered by it | DOCUMENTED ([CDK Drive Get Customer v3 spec](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf)) |
| **Store/branch** | Each physical rooftop in a group carries its own Department-Id set | Enumerated via Subscriptions API `apiDmsInfo`/`orgName` fields, not a dedicated header | DOCUMENTED ([Fortellis Community forum](https://community.fortellis.io/community/forum/install-app-subscriptions-and-support/cdk-fortellis-marketplace-subscriptions-and-support)) |

**Nesting, as documented across the above sources:** Dealer/CMF (contract & billing entity)
→ one or more Company Numbers/stores (legacy accounting layer) → per-store Fortellis
Subscription-Id → per-subscription set of Department-Ids, each scoped to one DMS type. A
given API call always carries **Subscription-Id** (which store/tenant) + **Department-Id**
(which module within that store) + `Authorization` + `Request-Id`.

`UNVERIFIED`: whether "Company Number" is formally exposed anywhere in the modern Fortellis
REST layer as its own field/header, or whether it is purely a legacy back-office/EDI-era
concept superseded by Subscription-Id + Department-Id. No Fortellis spec found that names a
`Company-Number` header — tracked as [open question](../docs/open-questions.md).

## 3. Multi-rooftop tenancy at a 9-site group

`INFERRED (dealer-accounting norm)`: for a 9-site group like Peterbilt Atlantic, the pattern
documented across CDK partner materials is one CMF/Client# or Dealer-level org per
legal/franchise entity, decomposed into per-store Company Numbers, each of which further
decomposes into Department IDs scoped to a single DMS subsystem. CDK's own materials never
publish an explicit "9 rooftops = 9 Company Numbers" rule; this is inferred from partner
setup docs (Mitchell, BettrData) that describe per-store department-ID sets and per-store CDK
Accounting Logons ([BettrData Fortellis CDK Drive API guide](https://docs.bettrdata.io/user-docs/how-to-guides/fortellis-cdk-drive-api)).

Fortellis community guidance confirms each physical store has its own set of Department-Ids,
and the subscription report lists "the store associated with each api under DMS attributes
column against each subscription-id"
([Fortellis Community — CDK Marketplace Subscriptions](https://community.fortellis.io/community/forum/install-app-subscriptions-and-support/cdk-fortellis-marketplace-subscriptions-and-support)).

**Key implication for this twin:** neither CDK Drive nor the PACCAR SAP backbone is installed
per-site. Both are centralized and site-scoped by identifier — which means one adapter per
rail (per `ARCHITECTURE.md`) covers all 9 Peterbilt Atlantic sites, consistent with the
"one adapter per external system, not per site" design principle already established in
[`eve-dealer-parts-twin`](https://github.com/EVEglyphDesign/eve-dealer-parts-twin).

## 4. Fortellis platform and the three/four-header contract

Fortellis is owned and operated by CDK Global; launched March 2018 as an API gateway,
Developer Network, and Marketplace for the automotive retail industry
([BusinessWire launch release](https://www.fi-magazine.com/323813/cdk-global-launches-fortellis-automotive-commerce-exchange-platform)).

Every CDK Drive API call carries the same three-header contract, confirmed identically across
multiple CDK Drive API specs, plus a CDK-specific fourth header:

| Header | Requirement | Function |
|---|---|---|
| `Authorization` | REQUIRED | `Bearer <token>` from Fortellis OAuth 2.0 Client Credentials flow |
| `Subscription-Id` | REQUIRED | Identifies the dealer/store-app subscription making the call |
| `Request-Id` | REQUIRED | Client-generated UUID correlation ID, echoed in the response |
| `Department-Id` | REQUIRED (CDK Drive specifically) | CDK's own DMS-partition mechanism layered on top of the platform contract |

Sources: [CDK Drive Get Customer v3 developer guide](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf),
[Fortellis Repair Orders v1 reference](https://community.fortellis.io/api-reference/vehicle-service/cdkdrive-repair-orders/cdkdrive-repair-orders-v1/get/%7BrepairOrderId%7D).

Full API catalogue and the CDK ransomware-outage architectural rationale are covered in
[`docs/current-state.md`](../docs/current-state.md).

## 5. Proposed SAP-shape mapping

| CDK Drive / Fortellis concept | Proposed SAP object in the twin | Rationale |
|---|---|---|
| Dealer ID / CMF (top-level client) | New root entity, analogous to a `T001W`-style plant/company-code master | Anchors the whole tenant; above plant level |
| Company Number (per-store legal/accounting entity) | `T001` (Company Code) per rooftop, or `WERKS` (Plant) if modeled at plant granularity | Matches "one store = one accounting entity" pattern from partner docs |
| Department ID (DMS-type-scoped) | Cross-module scoping flag alongside `MARC`/`MARD` records, tagged by functional module | Department-Id filters which module's data a call returns, not a single table |
| Subscription-Id (Fortellis app↔store binding) | Integration control table (no native SAP MM equivalent) | Tracks app, store (`WERKS`), and department for the twin's own API gateway |

This mapping is a proposal pending reconciliation against a live tenant — see
[`docs/open-questions.md`](../docs/open-questions.md).

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
