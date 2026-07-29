# Module 04 — Materials

**Status: drafted from lane 4 research (`cdk_04_materials.md`). This module extends the
SAP-shape parts schema already defined in
[`eve-dealer-parts-twin/schema/`](https://github.com/EVEglyphDesign/eve-dealer-parts-twin/tree/main/schema);
it does not duplicate it. Several field-level names remain unverified — see
`docs/open-questions.md`.**

Covers: parts master, valuation, movements, ordering.

---

## 1. Parts master record

CDK Drive's parts master is menu function **PM** (Parts Maintenance); part inquiry is
**PRO/PDA**. Real field/attribute names surface in the Fortellis **CDK Drive Get Repair
Order v3** parts-line schema, the CDK transaction-code sheet used by dealer trainers, and the
STAR `PartsProductItem` component that CDK and other DMS vendors map to as an EDI/XML target.

| Concept | Real field/attribute name (source) | Status |
|---|---|---|
| Part number | `number` (Get Repair Order v3 parts array); `PartNumber` (Async Parts Inventory) | DOCUMENTED |
| Description | `desc` (Get Repair Order v3); `Description` (Async Parts Inventory) | DOCUMENTED |
| Bin location (primary) | `bin1` — "the main bin number" (Get Repair Order v3) | DOCUMENTED |
| Multiple bins | Primary bin plus at least one alternate bin (`BIN2`) per part, entered via PM | DOCUMENTED |
| Manufacturer / source code | `source` — "the source number of the part" (Get Repair Order v3) | DOCUMENTED |
| Supersession / replacement chain | Function **PN** drives supersession; "Undo Succession" reverses it | DOCUMENTED (function name); exact schema field for the chain pointer is `UNVERIFIED` |
| Group / class code | `partClass` (Get Repair Order v3); `GroupCode` (Async Parts Inventory) | DOCUMENTED |
| Unit of measure | STAR `UOMCode` enumerated list | DOCUMENTED (STAR, cross-vendor) |

Sources: [CDK Drive Get Repair Order v3](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf),
[Fortellis community Q&A — Async Parts Inventory](https://community.fortellis.io/community/forum/qa/cdk-drive-search-parts-pick-ticket-and-cdk-drive-async-parts-inventory),
[STAR PartsProductItem](https://docs.starstandard.org/guidelines/STAR5134/PartsInvoice/ch06s50.html).

**Note on the parts-twin's existing `mara.supersession_to` field:** CDK's real behavior is a
**chain**, not a single link — a part can be superseded multiple times, and CDK auto-redirects
transactions through the whole chain. A single `supersession_to` column cannot represent
multi-hop chains. Flagged as a proposed change below.

## 2. Multi-location parts inventory

CDK Drive supports intercompany/inter-store parts transfers and inquiry natively — a
comparable DMS vendor documents "Intercompany parts for transfers and inquires between
dealerships" as a standard DMS-class feature
([DealerStar parts features PDF](https://www.dealerstar.com/assets/manuals/partsfeatures.pdf)),
consistent with the one-CDK-tenant-per-group model already established in
[`eve-dealer-parts-twin/docs/current-state.md`](https://github.com/EVEglyphDesign/eve-dealer-parts-twin/blob/main/docs/current-state.md).

The `DealerId` + `Department-Id` pair on the Async Parts Inventory API is the mechanism by
which a multi-store CDK tenant differentiates rooftops
([Fortellis community](https://community.fortellis.io/community/forum/qa/cdk-drive-search-parts-pick-ticket-and-cdk-drive-async-parts-inventory)).
There is no published single "group inventory" endpoint — group-wide availability is a
client-side union of per-Department-Id pulls. `INFERRED`.

**Confirmed gap** (consistent with the parts-twin's own current-state finding): there is no
PACCAR-provided automated inter-dealer rebalancing service. Inter-site moves within Peterbilt
Atlantic are manual today.

## 3. Parts valuation

Real CDK/Fortellis-confirmed valuation fields on the repair-order parts line
([Get Repair Order v3](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf)):

| Field | Description (verbatim from Fortellis doc) |
|---|---|
| `cost` | "The escalated unit cost amount" |
| `list` | "The escalated unit list price" |
| `sale` | "The escalated unit sale price. Does not include the core price and the unit service charge on return parts" |
| `extendedCost` / `extendedSale` | Calculated line totals |
| `coreCost` / `coreSale` | Core cost amount / core charge amount per unit |
| `mcdPercentage` | "The percentage applied on the split part" |
| `unitServiceCharge` | Service amount charged per unit for returned parts |

**CDK exposes `cost` as already escalated at time of sale**, not a raw average cost — the
parts-twin schema should distinguish a base average/replacement cost (`MBEW`-analog) from the
point-of-sale escalated cost captured per transaction (a `MATDOC`-analog attribute), which the
current schema does not yet separate.

**Pricing matrix mechanics** (documented in a comparable heavy-truck-parts DMS, Karmak
Unity): `AverageCost` = "the average cost or, if average cost is zero, the replacement cost";
`ReplacementCost` as a distinct field
([Karmak Unity API docs](https://unity.karmak.io/Parts-Inventory)) — cross-vendor
confirmation of the average/replacement cost split the twin should adopt.

**Core charges/returns:** CDK distinguishes clean core vs. dirty core returns at credit-memo
entry; a dedicated **RDCI (Dirty Core Inventory)** report tracks per-part core count and
dollar value awaiting return
([r/partscounter — CDK Core Tracking](https://www.reddit.com/r/partscounter/comments/1am0j27/cdk_core_tracking/)).

## 4. Parts movement types → proposed SAP movement type mapping

| Movement | CDK/DMS evidence | Proposed SAP `bwart` |
|---|---|---|
| Receipt against PO | CDK transaction code sheet; PACCAR EDI 856 ASN flow | `101` (GR against PO) |
| Sale over the counter | CDK `PS` transaction code, blank = normal sale/return; `H`/`NH` = wholesale | `601` (goods issue to sales order) |
| Issue to repair order | `W`/`NW` = warranty sale/return on an RO Warranty Pay labor line | `601` with `aufnr` populated |
| Return to vendor | Dirty-core processing, RDCI reconciliation; STAR "Parts Return - Obsolescence Interface Specification" | `161` (return to vendor) |
| Transfer (site-to-site) | DealerStar "Intercompany parts for transfers" — standard DMS capability; CDK's own inter-store mechanics beyond store-code visibility `UNVERIFIED` | `301`/`311` |
| Physical inventory adjustment | CDK codes `M` = minus adjustment, `P` = plus adjustment | `701` (gain) / `702` (loss) |
| Obsolescence write-down | No CDK transaction code found; accounting-side journal entry only | No MM movement type — value-only posting in `MBEW`/G/L |
| Lost sale | CDK: quantity + `LO` on a quote/RO/invoice line when qty on hand is zero; code `L` = "true" lost sale | No SAP MM movement type — non-movement demand-signal record |

(Sources: [CDK Transaction Codes, Total Dealer Solutions](https://totaldealersolutions.zendesk.com/hc/en-us/articles/360060331572-CDK-Transaction-Codes),
[EDIXT PACCAR Parts partner spec](https://edixtb2b.com/partners/automotive/paccar-parts).)

## 5. Parts ordering

CDK's stock-order engine: **`IRO`** sets stocking parameters per source; **`IRE`** launches
the suggested stock order; **`PO`** posts manual orders; **`RMR`** lists Manual-Order-flagged
parts with activity since the last Stockorder run
([r/partscounter — suggested parts order](https://www.reddit.com/r/partscounter/comments/1l2kqsw/how_do_i_make_a_suggested_parts_order_daily_in_cdk/)).

PACCAR's dealer parts ordering system is real and named **Online Parts Counter (OPC)** —
"7/24 access to more than 1.4 million parts," "visibility to dealer inventory," "part
cross-referencing" ([PACCAR Parts Customer Service](https://www.paccarparts.com/services/)),
accessed via `eportal.paccar.com`. **"PartsPRO" is not a name found in any public PACCAR
source and must not be used.**

Karmak Fusion's PACCAR integration names real PACCAR order types: **Stock, Emergency, MKT
(Marketing Suggestion), COF (Auto Confirmed)**
([Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar)). A formally
named "VOR" order type in PACCAR's North American dealer ordering system is `UNVERIFIED` —
VOR terminology is confirmed for PACCAR's Australian PDC operations, not the NA program.

MDI (Managed Dealer Inventory) remains the daily automated stock recommendation
([PACCAR Technology page](https://www.paccarparts.com/technology/)).

## 6. Physical inventory and obsolescence

No single documented CDK "cycle count" screen name was found; dealer-forum practice describes
rotational bin checks as the informal method
([r/partscounter](https://www.reddit.com/r/partscounter/comments/u5myel/cdk_drive_sold_parts_report/)).
Variance posting uses transaction codes `M`/`P` per §4.

The standard industry aging trigger is 12 months with zero movement
([McDonald Group](https://mcdonaldgroupinc.com/eliminating-obsolete-inventory/)), matching the
parts-twin's existing `mbew.months_no_movement`/`obsolete_flag` logic. Accounting treatment
under GAAP ASC 330: debit Inventory Obsolescence (expense), credit Allowance for Obsolete
Inventory (contra-asset), governed by lower-of-cost-or-market/net-realizable-value rules
([Houseblend ASC 330 summary](https://www.houseblend.io/articles/asc-330-inventory-valuation-write-downs)).
No PACCAR-specific obsolescence/return-allowance percentage was found — `UNVERIFIED`.

## 7. Publicly documented Fortellis parts APIs (real names)

| API | Function | Source |
|---|---|---|
| CDK Drive Async Parts Inventory | Bulk/async parts inventory feed | [Fortellis community Q&A](https://community.fortellis.io/community/forum/qa/cdk-drive-search-parts-pick-ticket-and-cdk-drive-async-parts-inventory) |
| CDK Drive Search Parts Pick Ticket | Transactional pick-ticket retrieval | [Fortellis community Q&A](https://community.fortellis.io/community/forum/qa/cdk-drive-search-parts-pick-ticket-and-cdk-drive-async-parts-inventory) |
| CDK Drive Get Parts Sales / History Setup Parts Sales | Retrieve / backfill parts sales records | [CDK Global Parts APIs page](https://www2.cdkglobal.com/api-solutions-parts) |
| CDK Drive Async Open/Closed Parts Sales | Real-time updates for open/closed parts sales | [CDK Global Parts APIs page](https://www2.cdkglobal.com/api-solutions-parts) |
| CDK Drive Get Repair Order v3 | Authoritative source for parts-line field names (`parts[]` array) | [Fortellis PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf) |

A 2025 Fortellis community thread shows a user asking whether the Async Parts Inventory /
Pick Ticket APIs are being replaced — no confirming reply found. Flagged as an open question.

## 8. Proposed changes to the existing parts-twin schema

| CDK/PACCAR concept | Change proposed |
|---|---|
| Supersession | Replace single-column `MARA.supersession_to` with a child table (`matnr_from`, `matnr_to`, `effective_date`, `sequence_no`) to represent multi-hop chains |
| Bin location(s) | Add a child table for the confirmed `BIN1`/`BIN2` alternate-bin pattern |
| Escalated point-of-sale cost | Add `MATDOC` extension columns (`escalated_cost`, `escalated_list`, `escalated_sale`, `mcd_percentage`) distinct from `MBEW.verpr` |
| Core charge / core cost | Add `MATDOC.core_cost`, `MATDOC.core_sale` — transaction-level core amounts not currently captured |
| Lost sale | New fact table `lost_sales` (matnr, werks, qty, requested_date, employee_id, source_ref) — a demand signal, not an inventory movement |
| Obsolescence reserve | Add `MBEW.reserve_amount`, `MBEW.reserve_pct` alongside the existing obsolete flag |
| PACCAR adapter naming | Target confirmed system name **Online Parts Counter (OPC)**, not an unverified "PartsPRO"; order-staging logic should use Stock/Emergency/MKT/COF, not an unconfirmed VOR code |

These are proposals pending reconciliation against a live CDK Drive tenant — see
[`docs/open-questions.md`](../docs/open-questions.md).

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
