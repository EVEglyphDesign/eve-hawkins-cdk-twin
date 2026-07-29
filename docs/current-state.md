# Current-state analysis — Peterbilt Atlantic CDK Drive twin

**Status: wireframe / to be filled from lanes 1, 7, 8.** This is an honest audit of what
exists today versus what this repo has actually built so far (almost nothing — the modules
and schema proposal are research-grounded drafts, not working code).

**Scope:** what Peterbilt Atlantic's 9 sites actually run today across the DMS and OEM rails,
why a single point of failure exists, and why a group-owned twin is the reusable win — the
same framing already established for the materials domain in
[`eve-dealer-parts-twin/docs/current-state.md`](https://github.com/EVEglyphDesign/eve-dealer-parts-twin/blob/main/docs/current-state.md),
extended here to the full DMS (ledger, cost objects, master data, document flow).

---

## 1. The two rails every site runs

### Rail A — PACCAR (OEM backbone)

- **Backend:** a materially SAP-shaped enterprise stack — confirmed pieces are **SAP
  S/4HANA** (core ERP, run on IBM Power/HANA), **SAP Transportation Management**, **SAP GTS**
  (trade compliance), **SAP IBP** (demand planning), **SAP BusinessObjects Financial
  Consolidation** (close/consolidation, live since 2017), and **SAP Concur** (travel &
  expense) — assembled from several separate PACCAR job postings, case studies, and vendor
  materials rather than one blanket "PACCAR runs 100% SAP" statement.
  ([IBM/Mainline case study](https://mainline.com/wp-content/uploads/PDFs/CS_PACCAR-Power.pdf),
  [SAP Innovation Awards 2021 pitch deck](https://www.sap.com/bin/sapdxc/proxy.inmsl.attachment.11352.pitch-deck.pdf))
- **Dealer-facing systems (real names only):** **Online Parts Counter (OPC)** for parts
  ordering, **Managed Dealer Inventory (MDI)** for daily stock recommendations, **PRWS**
  (PACCAR Registration and Warranty System) for warranty claims, **PACCAR Solutions/PSSM**
  and **TruckTech+/SmartLINQ** (both built on **Decisiv**) for service case management and
  telematics. None of these publish a public REST API for dealers — access is portal/SSO or
  mediated entirely through a DMS vendor's own integration (documented for Karmak Fusion).
  ([Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar))
- **Financial reporting to PACCAR:** Karmak's integration page states "financial statements
  are automatically downloaded to PACCAR" as standard DMS-to-OEM behavior; the equivalent for
  CDK Drive is `UNVERIFIED` but structurally analogous. PACCAR-brand dealers most plausibly
  report in the industry-standard **NADA financial-statement format**
  ([NADA — What's Important on the Financial Statement](https://www.nada.org/nada/education-consulting/tailored-training/whats-important-financial-statement)),
  though PACCAR's own chart-of-accounts numbering and submission deadline are not publicly
  documented — a genuine, acknowledged gap, not a research failure.

**Key point:** Peterbilt Atlantic's nine sites do not each run their own instance of
anything on the PACCAR side. They share PACCAR's centralized systems and receive site-scoped
feeds (MDI recommendations, per-site OPC access).

### Rail B — CDK Drive (Dealer DMS)

- **Backend:** CDK Global, LLC, now privately held by **Brookfield Business Partners**
  (acquired 2022, $8.3B enterprise value); no shares trade publicly, so post-acquisition
  financials are not disclosed.
  ([Bloomberg](https://www.bloomberg.com/news/articles/2022-04-07/brookfield-partners-agrees-to-buy-cdk-global-for-8-3-billion))
- **Modern integration surface:** **CDK Fortellis**, a REST API marketplace. Real API names
  are documented per module — `CDK Drive Get Repair Order v3`, `CDK Drive Get Customer v3`,
  `CDK Drive Async Parts Inventory`, `CDK Drive Payment Settling API`, and others cataloged in
  [`../adapters/cdk-fortellis/README.md`](../adapters/cdk-fortellis/README.md).
- **Deployment model:** typically **one CDK Drive tenant per dealer group**, with each
  rooftop configured as a store/department inside it — confirmed by the Fortellis
  `Department-Id` header requirement documented in
  [`../modules/01-organization.md`](../modules/01-organization.md).
- **Heavy Truck caveat:** CDK's Heavy Truck DMS product line markets "80+ Heavy Truck
  OEM-specific integrations" but its underlying vehicle/chassis schema is not separately
  published — `UNVERIFIED` whether Peterbilt Atlantic's tenant fully matches the light-vehicle
  Drive field names this research draws on for most modules, versus a heavy-truck-specific
  variant.
- **Important open question, not yet resolved by any lane's research:** the heavy-duty DMS
  competitive landscape includes Karmak Fusion and Procede Excede as dominant vendors with
  *documented* PACCAR/Peterbilt integrations, while CDK Drive Heavy Truck's PACCAR-specific
  integration depth is comparatively thin in public sources. Before further build-out, confirm
  directly with Peterbilt Atlantic which DMS the 9 sites actually run — the task brief
  specifies CDK Drive, but this should be reconciled against the vendor landscape finding, not
  assumed.

---

## 2. Single-instance or per-site? — the answer

| Layer | Deployment shape | What Peterbilt Atlantic sees per site |
|---|---|---|
| PACCAR SAP-shape backbone | Centralized at PACCAR | One login/feed per site per system (OPC, MDI) |
| PRWS (warranty) | Centralized, reachable via Fortellis | Claims filed per-RO, regardless of site |
| CDK Drive | One dealer-group tenant (typical pattern) | Each site = store/department code inside the tenant |
| CDK Fortellis APIs | Single API surface for the tenant | Filter by `Department-Id` for per-site data |

**Neither rail is installed per-site.** This is the same structural finding the parts twin
already established for materials — one adapter per rail should cover all 9 sites for every
domain in this repo, not just parts.

---

## 3. Why a single point of failure exists today

CDK Drive was taken offline for approximately **19 days in June–July 2024** by the BlackSuit
ransomware group, affecting an estimated **15,000 North American dealerships**; CDK reportedly
paid roughly **$25 million** in ransom (387 BTC), and dealer losses were separately estimated
at $605M–$1B in lost sales/operations across the industry.
([CNN](https://www.cnn.com/2024/07/11/business/cdk-hack-ransom-tweny-five-million-dollars),
[ISPartners](https://www.ispartnersllc.com/blog/car-dealership-cyberattack/))

This is the direct architectural argument for this twin: every module and adapter in this
repo assumes CDK Drive can go dark for weeks at a time, and designs the export-fallback path
([`../adapters/export-fallback/README.md`](../adapters/export-fallback/README.md)) as a
first-class citizen rather than an edge case.

## 4. The economics argument for owning rather than renting

CDK's own **Partner Program Pricing Guide** shows the vendor monetizes even read-access to a
dealer's own transactional data as a distinct, metered product — a base extract fee plus a
per-data-type charge, on top of core module subscription fees.
([CDK Partner Program Price Guide PDF](https://www.cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf))
Under IAS 38 / ASPE Section 3064, a hosted DMS subscription typically fails the "control" test
required to capitalize it as an intangible asset — it is a recurring rental expense, not a
balance-sheet asset, and disappears entirely on contract exit
([PwC — Cloud computing accounting considerations](https://www.pwc.co.za/en/assets/pdf/cloud-computing.pdf)).
A dealer-controlled twin, by contrast, is structured to satisfy the control criterion and
could be capitalized as an intangible asset if development costs meet the six IAS 38
recognition tests. This is the accounting-standards basis for treating this repo as a capital
asset the dealer group owns, not a subscription line-item.

## 5. What the twin adds

1. **SAP-shape schema across the whole DMS**, not just parts — ledger, cost objects,
   materials, master data, document flow — so a PACCAR SAP payload maps 1:1 wherever the
   two systems touch, and the schema outlives any DMS vendor change.
2. **A canonical warranty/service/AR document trail** independent of CDK's own retention and
   uptime, addressing the ransomware-outage single-point-of-failure risk directly.
3. **A CASL-compliant consent log** (Module 05 §6) that CDK's own customer schema does not
   provide, closing a real Canadian-compliance gap rather than a hypothetical one.

## 6. Why this is reusable across a multi-group PACCAR dealer network

Every PACCAR-network dealer group faces the same three structural facts documented in this
research: a centralized OEM-side SAP-shape backbone, a centralized (or near-centralized) DMS
tenant, and no OEM-provided inter-dealer or inter-system rebalancing/reconciliation layer.
**One CDK adapter, one PACCAR adapter, one export-fallback adapter, one SAP-shape schema —
deployed per dealer group, reused across every group.**

## 7. What we do NOT do

- **Not** replace CDK Drive as the operational system of record. The twin reads; CDK stays
  the counter/service/finance staff's daily tool until and unless Peterbilt Atlantic decides
  otherwise.
- **Not** replace PRWS, OPC, MDI, or any PACCAR system. The twin ingests the RO-relevant slice
  that reaches CDK; it does not attempt to mirror PACCAR's telematics or warranty-adjudication
  internals, per the sovereign-data posture in
  [`../adapters/paccar/README.md`](../adapters/paccar/README.md).
- **Not** implement SAP. This repo uses SAP's **data shape**, not SAP itself, matching the
  parts twin's own stated design principle.
- **Not** claim any schema, field name, or endpoint in this repo is confirmed against a live
  Peterbilt Atlantic CDK Drive tenant. Every mapping here is a proposal pending reconciliation
  — see [`open-questions.md`](open-questions.md).

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
