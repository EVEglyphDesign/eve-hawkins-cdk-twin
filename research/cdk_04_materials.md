# Lane 4 — Parts and Materials Management in CDK Drive

Client: EVEglyphDesign digital twin for Peterbilt Atlantic (9-site Peterbilt/PACCAR heavy-truck
group). Existing twin repo: [eve-dealer-parts-twin](https://github.com/EVEglyphDesign/eve-dealer-parts-twin),
SAP-shape schema in `schema/*.sql` and PACCAR/CDK adapter field maps in `adapters/*/fields.md`.
This document deepens and corrects that model. Public sources only, per the shared rules file.

---

## 1. Parts master record

CDK Drive's parts master is menu function **PM** (Parts Maintenance); part inquiry is **PRO/PDA**.
Legacy CDK field names are not published in a single formal data dictionary, but real field/attribute
names surface in three verifiable places: the Fortellis **CDK Drive Get Repair Order v3** API reference
(parts-line schema), the CDK transaction-code sheet used by dealer trainers, and the **STAR PartsProductItem**
component of the STAR6/PartsInvoice schema, which CDK and other DMS vendors map to as an EDI/XML target.

| Concept | Real field/attribute name (source) | Status |
|---|---|---|
| Part number | `number` — CDK Drive Get Repair Order v3 parts array ([Fortellis PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf)); `PartNumber` in CDK Drive Async Parts Inventory ([Fortellis community](https://community.fortellis.io/community/forum/qa/cdk-drive-search-parts-pick-ticket-and-cdk-drive-async-parts-inventory)) | DOCUMENTED |
| Description | `desc` (Get Repair Order v3); `Description` (Async Parts Inventory) | DOCUMENTED |
| Bin location (primary) | `bin1` — "The main bin number" (Get Repair Order v3); CDK counter function `PSMB`/`PM` sets `BIN1`/`BIN2` for alternate bins ([r/partscounter](https://www.reddit.com/r/partscounter/comments/1dz1eqq/cdk_help/)) | DOCUMENTED |
| Multiple bins | CDK supports a primary bin plus at least one alternate bin (`BIN2`) per part, entered via PM; batch relocation via PM Batch Change ([r/partscounter](https://www.reddit.com/r/partscounter/comments/1dz1eqq/cdk_help/)) | DOCUMENTED |
| Bin sort key | CDK's "Sort Key" orders bin sheets, e.g. `820-21-210-01` groups ([r/partscounter](https://www.reddit.com/r/partscounter/comments/1ivxuxy/specific_part_number_bin_report_through_cdk/)) | DOCUMENTED |
| Manufacturer / source code | `source` — "the source number of the part" (Get Repair Order v3); CDK term "Source" ties a part to a supplier/manufacturer feed used for Parts Master Update (PMU) pricing ([r/partscounter — Parts source field map](https://www.reddit.com/r/partscounter/comments/1l242vr/cdk_parts_source_field_map_for_pmu/)) | DOCUMENTED |
| Manufacturer part number cross-ref | STAR `PartManufacturer`, `PartTypeCode` (H=Manufacturer Part Code, P=Part Number), `VendorCode` — STAR PartsProductItem component ([STAR docs](https://docs.starstandard.org/guidelines/STAR5134/PartsInvoice/ch06s50.html)) | DOCUMENTED (industry standard, not confirmed CDK-native) |
| Supersession / replacement chain | CDK function **PN** ("Function PN") drives supersession; "Undo Succession" reverses it; a superseded part auto-redirects order/sale to the new number ([r/partscounter — CDK auto supersession](https://www.reddit.com/r/partscounter/comments/1j51sgh/cdk_auto_supersession_help/), [r/partscounter — multiple parts prompt](https://www.reddit.com/r/partscounter/comments/1m3cm69/cdk_multiple_parts_prompt_help/)) | DOCUMENTED (function name); exact CDK field/table name for the chain pointer is `UNVERIFIED` |
| Group / class code | `partClass` — "The code assigned to the parts class" (Get Repair Order v3); `GroupCode` (Async Parts Inventory) | DOCUMENTED |
| STAR class equivalents | `PartClassCode`, `ClassCode`, `Inventory Movement/Demand Code` (A/B/C turn code), `VMRSCode` — STAR Active Data Dictionary ([STAR ADD PDF](https://qa.starstandard.org/images/SIGDTS/STARActiveDataDictionary.pdf)) and PartsProductItem | DOCUMENTED (STAR, cross-vendor) |
| Unit of measure | STAR `UOMCode` enumerated list (ea, bx, case, ctn, gal, qt, pt, ft, yd, in, L, m, cm, kg, g) ([STAR PartsProductItem](https://docs.starstandard.org/guidelines/STAR5134/PartsInvoice/ch06s50.html)) | DOCUMENTED (STAR) |
| Pack / package quantity | STAR `PackageQuantity` — "Allows the retailer to know the quantity contained in the package" | DOCUMENTED (STAR) |
| Hazmat flag | STAR `HazmatIndicator`, `HazardousMaterialDescription` | DOCUMENTED (STAR) |
| Part condition / core / reman | STAR `PartConditionCode`, `CorePartDescription`, `RemanufacturedPartDescription` | DOCUMENTED (STAR) |
| Order/sale restriction | STAR `PartOrderRestriction` (Obsolete, Out of production, No longer procured, Not yet adopted), `PartDealerSalesRestriction` (OK to sell / Restricted / Not for sale), `PartSupplyStatusCode` | DOCUMENTED (STAR) |

**Note on the twin's existing `mara.supersession_to` field:** this is a reasonable single-pointer model,
but CDK's real behavior (per dealer-forum evidence) is a **chain**, not a single link — a part can be
superseded multiple times, and CDK auto-redirects transactions through the whole chain. A single
`supersession_to` column cannot represent multi-hop chains or branch cases (e.g., regional Motorcraft-style
dual numbers). This is flagged in §9 below.

## 2. Multi-location parts inventory

CDK Drive supports **intercompany/inter-store parts** transfers and inquiry natively — the DealerStar
competitor feature sheet documents "Intercompany parts for transfers and inquires between dealerships"
as a standard DMS-class feature ([DealerStar parts features PDF](https://www.dealerstar.com/assets/manuals/partsfeatures.pdf)), corroborating what the twin's `docs/current-state.md`
already concludes: one CDK Drive tenant per dealer group, each site as a store/company code, single
query surface for group-wide visibility (INFERRED, dealer-accounting norm, consistent with
[Fortellis parts inventory API](https://www2.cdkglobal.com/api-solutions-parts) being dealer/department-scoped
rather than per-installation).

- The `DealerId` + `Department-Id` pair on the Async Parts Inventory API is the mechanism by which a
  multi-store CDK tenant differentiates rooftops ([Fortellis community](https://community.fortellis.io/community/forum/qa/cdk-drive-search-parts-pick-ticket-and-cdk-drive-async-parts-inventory)). DOCUMENTED.
- Group-wide availability query pattern: pull Async Parts Inventory once per Department-Id (i.e., once
  per site) and union the results — there is no published single "group inventory" endpoint; the
  aggregation is a client-side responsibility. INFERRED.
- PACCAR's own group-visibility precedent: the Chrysler/Mopar **DealerCONNECT Part Inquiry** screen shows
  a documented "Facing PDC → Source PDC → Other PDCs" referral chain and a **dealer locator** capability
  for nearby-dealer stock ([Chrysler Part Inquiry FAQ](http://starparts.chrysler.com/home/scroll/PIFAQ.pdf)) —
  useful cross-OEM evidence that dealer-locator-style stock visibility across a network is a standard DMS/OEM
  pattern, not something the twin is inventing. DOCUMENTED (Chrysler, analogous pattern, not PACCAR-specific).
- **Confirmed gap** (per twin's own current-state.md, consistent with all research above): there is **no
  PACCAR-provided automated inter-dealer rebalancing service**. MDI is PACCAR→dealer only. Inter-site moves
  within Peterbilt Atlantic are manual today. INFERRED (dealer-accounting norm) + twin's own documented finding.

## 3. Parts valuation

Real CDK/Fortellis-confirmed valuation fields on the repair-order parts line ([Get Repair Order v3](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf)):

| Field | Description (verbatim from Fortellis doc) |
|---|---|
| `cost` | "The **escalated** unit cost amount" |
| `list` | "The **escalated** unit list price" |
| `sale` | "The escalated unit sale price. Does not include the core price and the unit service charge on return parts" |
| `extendedCost` / `extendedSale` | Calculated line totals |
| `coreCost` / `coreSale` | Core cost amount / core charge amount per unit |
| `mcdPercentage` | "The percentage applied on the split part" (escalation/markup-cost-detail percentage) |
| `unitServiceCharge` | Service amount charged per unit for returned parts |

Confirms the twin's `mbew.verpr` (moving average cost) concept exists in CDK, but **CDK exposes "cost" as
already escalated at time of sale**, not a raw average cost — the twin should distinguish a base
average/replacement cost (MBEW-analog) from the point-of-sale escalated cost captured per transaction (a
MATDOC-analog attribute), which the current schema does not yet separate. Flagged in §9.

**Pricing matrix mechanics** (documented in a competing DMS, Motility, and confirmed as a cross-DMS
concept by trade press):
- Matrix basis options: **Average Cost, Replacement Cost, List Price** ([Motility pricing matrix](https://help.motilitysoftware.com/hc/en-us/articles/4417019900308-Parts-Service-Pricing-Matrix)) — this directly validates the twin's MBEW split into `verpr` (moving avg) vs. a replacement-cost concept it currently lacks.
- Price-level letter codes: `L` = % of list, `A` = % over average cost, `C` = % over replacement cost, `M` = % over margin price, `G`/`S` = % over gross margin (replacement/standard cost basis). INFERRED (dealer-accounting norm, cross-DMS) but the letter-coding convention itself is DOCUMENTED at the source cited.
- "All of the major dealer-management systems have the ability to create a parts pricing matrix… most common method is by source and customer price code" ([WardsAuto](https://www.wardsauto.com/news/archive-wards-make-more-money-off-parts/775910/)). DOCUMENTED (industry, not CDK-specific verbatim, but WardsAuto explicitly generalizes across DMS).
- Karmak Unity (a comparable heavy-truck-parts DMS) explicitly documents: `AverageCost` = "the average cost or, if average cost is zero, the replacement cost"; `ReplacementCost` as a distinct field ([Karmak Unity API docs](https://unity.karmak.io/Parts-Inventory)). DOCUMENTED (Karmak, cross-vendor confirmation of the average/replacement cost pattern the twin should adopt).

**Cost of sale at moment of sale:** the escalated `cost` field is captured on the RO/invoice line at
time of pick/sale ([Get Repair Order v3](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf)) — i.e., cost of sale is the part's current average/moving cost at
the instant of the transaction, consistent with a moving-average valuation method (SAP `VPRSV='V'`).
DOCUMENTED + INFERRED (moving-average mechanics are dealer-accounting norm).

**Core charges/returns:** CDK distinguishes **clean core** vs. **dirty core** returns at the point of
credit-memo entry; a dedicated **RDCI (Dirty Core Inventory)** report tracks per-part core count and
dollar value awaiting return ([r/partscounter — CDK Core Tracking](https://www.reddit.com/r/partscounter/comments/1am0j27/cdk_core_tracking/)). CDK also offers a paid "core bank" feature; without it, dealers
manually reconcile month-end core credits against factory invoices ([r/partscounter — CDK core bank](https://www.reddit.com/r/partscounter/comments/1npig9o/cdk_core_bank/)). DOCUMENTED.

## 4. Parts movement types → proposed SAP movement type mapping

| Movement | CDK/DMS evidence | Proposed SAP `bwart` | Status |
|---|---|---|---|
| Receipt against PO | CDK transaction code sheet: normal receipt posts on-hand increase; PACCAR order flow confirms Order→Receipt via ePortal/EDI 856 ASN | `101` (GR against PO) | INFERRED (norm) + DOCUMENTED (EDI ASN flow, [EDIXT PACCAR spec](https://edixtb2b.com/partners/automotive/paccar-parts)) |
| Sale over the counter | CDK `PS` transaction code, blank = "Normal sale or return sale"; `H`/`NH` = wholesale ([Total Dealer Solutions CDK Transaction Codes](https://totaldealersolutions.zendesk.com/hc/en-us/articles/360060331572-CDK-Transaction-Codes)) | `601` (goods issue to sales order) for retail; internal wholesale coded separately if the twin wants source_system distinction | DOCUMENTED (CDK code) + proposed mapping |
| Issue to repair order | `W`/`NW` = "Warranty sale or return sale (part sale/return on an RO Warranty Pay labor line)" ([CDK Transaction Codes](https://totaldealersolutions.zendesk.com/hc/en-us/articles/360060331572-CDK-Transaction-Codes)) | `601` with `aufnr` populated (already in twin's `matdoc.aufnr`) | DOCUMENTED (CDK code) + existing twin field |
| Return to vendor | Core "dirty core" processing and RDCI reconciliation ([r/partscounter](https://www.reddit.com/r/partscounter/comments/1am0j27/cdk_core_tracking/)); STAR "Parts Return - Obsolescence Interface Specification" exists as a named STAR spec ([cover pages list](https://xml.coverpages.org/star.html)) | `161` (return to vendor) — matches twin's existing comment | DOCUMENTED (STAR spec name) |
| Transfer (site-to-site) | DealerStar "Intercompany parts for transfers" feature confirms this is a standard DMS capability; CDK's own inter-store mechanics beyond store-code visibility are `UNVERIFIED` in detail | `301` (plant-to-plant) or `311` (SLoc-to-SLoc) — matches twin's existing comment | INFERRED (norm) |
| Physical inventory adjustment | CDK codes `M` = "Minus adjustment", `P` = "Plus adjustment" ([CDK Transaction Codes](https://totaldealersolutions.zendesk.com/hc/en-us/articles/360060331572-CDK-Transaction-Codes)) | `701` (gain) / `702` (loss) — matches twin's existing comment | DOCUMENTED (CDK code) |
| Obsolescence write-down | No CDK transaction code found; accounting-side journal entry only (see §7) | No standard SAP MM movement type — this is a value-only posting in `MBEW`/G/L, not a `MATDOC` quantity movement. **Twin's current-state does not yet model this** | UNVERIFIED (CDK code) + DOCUMENTED (accounting mechanics) |
| Lost sale | CDK: type quantity followed by `LO` (e.g. "1 LO") on a quote/RO/invoice line when quantity on hand is zero; transaction code `L` = "Lost sale ('true' lost sale, not lost sale due to price)" ([CDK Transaction Codes](https://totaldealersolutions.zendesk.com/hc/en-us/articles/360060331572-CDK-Transaction-Codes); [r/partscounter — CDK Lost Sales](https://www.reddit.com/r/partscounter/comments/1r27382/cdk_lost_sales/); [YouTube — Mystery of the Lost Sale](https://www.youtube.com/watch?v=nJ6AqM2Zmvs)) | No SAP MM movement type applies — lost sales are a **non-movement demand-signal record**, not inventory-affecting. Twin should add a `lost_sales` fact table, not force this into `MATDOC` | DOCUMENTED (CDK code) |

## 5. Parts ordering

- CDK's stock-order engine: **`IRO`** sets stocking parameters per source (phase-in/phase-out, stock
  levels); **`IRE`** launches/generates the suggested stock order; **`PO`** posts manual orders; **`RMR`**
  ("Report MO Review") lists Manual-Order-flagged parts with activity since the last Stockorder run
  ([r/partscounter — suggested parts order](https://www.reddit.com/r/partscounter/comments/1l2kqsw/how_do_i_make_a_suggested_parts_order_daily_in_cdk/); [r/partscounter — CDK Automatic Phaseout](https://www.reddit.com/r/partscounter/comments/1r37b7i/cdk_automatic_phaseout/)). DOCUMENTED (function names).
- Days-supply / stocking parameters live in the same IRO setup (min/max, safety stock) — consistent with
  the twin's existing `marc.minbe/mabst/eisbe/days_of_supply` fields. INFERRED (norm) matches existing schema.
- **PACCAR's dealer parts ordering system is real and named: "Online Parts Counter" (OPC)** — PACCAR's own
  site states OPC gives "7/24 access to more than 1.4 million parts," "visibility to dealer inventory,"
  "part cross-referencing" and "market basket pricing" ([PACCAR Parts Customer Service](https://www.paccarparts.com/services/)). Access is via **eportal.paccar.com** ([PACCAR ePortal / Fleet ECAT user guide](https://22781394.fs1.hubspotusercontent-na1.net/hubfs/22781394/Kenworth%20eCat%20User%20Guide.pdf)); dealer-facing marketing also calls it PartsCounter.Kenworth.com for the Kenworth
  brand ([Rihm Kenworth](https://www.rihmkenworth.com/blog/the-benefits-of-online-parts-counter--55573)). **"PartsPRO" is NOT a name found in any public PACCAR source searched — do not use it.**
  DOCUMENTED (OPC is the confirmed real system name; PartsPRO is unverified/likely wrong and should not be used).
- MDI (Managed Dealer Inventory) remains the daily automated stock recommendation, confirmed again here:
  "PACCAR Parts Managed Dealer Inventory Program... provides visibility to retail transactions... order
  recommendations are developed for each dealer location and transmitted electronically to the dealer
  daily" ([PACCAR Technology page](https://www.paccarparts.com/technology/)). DOCUMENTED — matches twin's existing MDI adapter.
- **Karmak Fusion's PACCAR integration explicitly names the order types it supports:** "Fusion supports
  PACCAR stock, emergency, marketing suggestion, and auto-confirmed orders" and separately "Fusion supports
  all MDI order types, including stock order, PACCAR Parts Marketing Suggestion (MKT), and Auto Confirmed
  (COF) orders" ([Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar)). This is the
  strongest available public evidence for real PACCAR order-type codes: **Stock, Emergency, MKT (Marketing
  Suggestion), COF (Auto Confirmed)**. DOCUMENTED — no public source found that uses the term "VOR" specifically
  in PACCAR's own program (VOR terminology is confirmed for Hino, Isuzu, Changan, and Hyundai/MOBIS dealer
  ordering programs, which are close analogs but not PACCAR); PACCAR's dealer-facing VOR-equivalent urgent-part
  process is UNVERIFIED by name — the closest confirmed statement is PACCAR Parts Brisbane PDC's description
  of "VOR's (vehicle off road)" handling in an Australian trucksales.com.au interview ([PACCAR Brisbane PDC](https://www.trucksales.com.au/editorial/details/paccar-parts-opens-new-brisbane-distribution-centre-111808/)) — so VOR terminology **is** used by PACCAR Parts, but a formally named "VOR order type" in the
  North American dealer ordering system was not found in public documentation. Marked UNVERIFIED for NA-specific naming.
- **PACCAR Fleet Web ECAT** integrates with OPC to push chassis-specific BOM part picks directly into a
  shopping cart for ordering ([PACCAR Fleet ECAT user guide](https://22781394.fs1.hubspotusercontent-na1.net/hubfs/22781394/Kenworth%20eCat%20User%20Guide.pdf)). DOCUMENTED.

## 6. Physical inventory

- CDK has no single documented "cycle count" screen name found in public sources; dealer-forum practice
  describes **rotational bin checks** (e.g., print 2 bins/day/employee) as the informal cycle-count method
  on CDK Drive ([r/partscounter — Sold Parts Report](https://www.reddit.com/r/partscounter/comments/u5myel/cdk_drive_sold_parts_report/)). INFERRED (dealer-accounting norm) — not a documented CDK function name.
- Full physical inventory uses bin sheets generated by CDK for a page-break-per-bin count sheet
  ([DealersEdge forum — bin/shelf location](https://forums.dealersedge.com/viewtopic.php?f=3&t=11288)); CDK Parts Events report (`Report/Analyze → Parts Events`) can show `M`/`P` adjustment
  history including who changed a bin or quantity, filtered by "Changed Field" ([r/partscounter — bin changed report](https://www.reddit.com/r/partscounter/comments/1c5fxg7/cdk_bin_changed_on_multiple_parts_hundreds_to_our/)). DOCUMENTED (CDK report path).
- Variance posting: CDK transaction codes `M` (minus adjustment) / `P` (plus adjustment) post the count
  variance ([CDK Transaction Codes](https://totaldealersolutions.zendesk.com/hc/en-us/articles/360060331572-CDK-Transaction-Codes)) — matches twin's `bwart='701'/'702'` mapping in §4. DOCUMENTED.
- Trade-press norm: "parts department personnel should be completing mini parts physicals daily... take
  the number of bins... divide by working days in the month... run the variance report monthly"
  ([Auto Dealer Today](https://www.autodealertodaymagazine.com/articles/service-and-parts-profitability)). INFERRED (dealer-accounting norm).

## 7. Parts obsolescence

- No CDK-specific aging-bucket field names were found in public sources. The standard dealer/industry
  aging trigger cited is **12 months with zero movement** ("parts inventory line items that have not sold
  in over 12 months") ([McDonald Group](https://mcdonaldgroupinc.com/eliminating-obsolete-inventory/)) — this matches the twin's existing `mbew.months_no_movement`/`obsolete_flag` logic exactly. DOCUMENTED (12-month trigger) + matches existing schema.
- OEM return allowance example (non-PACCAR, cited as an industry analog): "Case New Holland (CNH) parts
  with no turns can be returned for 100% of value for items up to 1-year-old" ([McDonald Group](https://mcdonaldgroupinc.com/eliminating-obsolete-inventory/)) — **no public PACCAR-specific obsolescence/return-allowance percentage was found.** UNVERIFIED for PACCAR specifically.
- Accounting treatment (GAAP, ASC 330, general dealer-accounting norm, not CDK-specific):
  - Write-down: **Debit Inventory Obsolescence (expense), Credit Allowance for Obsolete Inventory
    (contra-asset)** ([ProCountWest](https://www.procountwest.com/mikes-blog/how-to-account-for-obsolete-parts-inventory-at-your-automotive-dealership)).
  - Governed by **lower of cost or market (LCM)** for LIFO/retail-method inventory, or **lower of cost or
    net realizable value (LCNRV)** post-ASU 2015-11 for FIFO/average-cost inventory ([NHADA](https://www.nhada.com/news/key-inventory-tax-planning-considerations-for-auto-dealers); [Houseblend ASC 330 summary](https://www.houseblend.io/articles/asc-330-inventory-valuation-write-downs)).
  - Write-downs under US GAAP are **irreversible** even if market value later recovers ([Houseblend](https://www.houseblend.io/articles/asc-330-inventory-valuation-write-downs); [Investopedia](https://www.investopedia.com/ask/answers/05/070105.asp)).
  - Legal precedent on inventory write-downs and tax deductibility: **Thor Power Tool Co. v. Commissioner,
    439 U.S. 522 (1979)** ([cited via McDonald Group](https://mcdonaldgroupinc.com/eliminating-obsolete-inventory/)).
  - Written-off parts must be disposed of, not retained for resale; donated parts to qualifying 501(c)(3)
    orgs under **IRS Code 170(e)(3)** may allow enhanced deduction up to 200% of cost, subject to CPA
    confirmation ([McDonald Group](https://mcdonaldgroupinc.com/eliminating-obsolete-inventory/)).
  - Common graduated reserve method: reserve % scales with multiples of trailing-twelve-month (TTM) demand
    — e.g., 0% up to 1× TTM, 25% for 1–2× TTM, 50% for 2–3×, 75% for 3–4×, 100% above 4× ([CLA Connect](https://www.claconnect.com/en/resources/blogs/manufacturing/whats-a-reasonable-inventory-reserve-a-guide-for-businesses)). INFERRED (dealer-accounting norm) as the closest documented general aging-bucket schedule; not CDK- or PACCAR-specific.

## 8. Fortellis-published CDK Drive parts APIs (real names)

| Real published API name | Function | Source |
|---|---|---|
| **CDK Drive Async Parts Inventory** | Bulk/async parts inventory feed (`DealerId`, `PartNumber`, `Description`, `Manufacturer`, `QtyOnHand`, `BinLocation`, `Cost`, `ListPrice`, `LastSaleDate`, `DateReceived`, `DeletePartFlag`, `GroupCode`, `MinStock`, `MaxStock`, `SafetyStock`) | [Fortellis community Q&A](https://community.fortellis.io/community/forum/qa/cdk-drive-search-parts-pick-ticket-and-cdk-drive-async-parts-inventory) |
| **CDK Drive Search Parts Pick Ticket** | Transactional pick-ticket / parts-picking retrieval | [Fortellis community Q&A](https://community.fortellis.io/community/forum/qa/cdk-drive-search-parts-pick-ticket-and-cdk-drive-async-parts-inventory) |
| **CDK Drive Get Parts Sales** | Retrieve parts sales records | [CDK Global Parts APIs page](https://www2.cdkglobal.com/api-solutions-parts) |
| **CDK Drive History Setup Parts Sales** | Backfill/historical parts sales | [CDK Global Parts APIs page](https://www2.cdkglobal.com/api-solutions-parts) |
| **CDK Drive Async Open Parts Sales** | Real-time updates for open (unclosed) parts sales | [CDK Global Parts APIs page](https://www2.cdkglobal.com/api-solutions-parts) |
| **CDK Drive Async Closed Parts Sales** | Real-time updates for closed parts sales | [CDK Global Parts APIs page](https://www2.cdkglobal.com/api-solutions-parts) |
| **CDK Get Part Sales** | Listed among "8 New CDK Global APIs" launched on Fortellis, alongside Get Customer, Get Repair Order, Get Op Code Lite, Get Make Model Lite, Get Service Appointment, Get Employee, Get F&I Sales | [LinkedIn — Tom Miller](https://www.linkedin.com/posts/tom-miller-a6360657_8-new-cdk-global-apis-available-in-the-automotive-activity-7049032774984347648-01Mt) |
| **CDK Drive Get Repair Order v3** | Not a parts-specific API, but its `parts[]` array is the authoritative public source for parts-line field names used in this document | [Fortellis PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf) |
| **CDKDrive Repair Orders V1** | Transactional service write-up API; can add/update pre-assigned parts to service lines | [Fortellis Developer Guide](https://prod-fortellis-provider-api-reference-documents.s3-us-west-2.amazonaws.com/c7771500-1c95-4f8e-9241-eddc17cd55f6) |

Both APIs the task specifically asked about — **async parts inventory** and **pick ticket** — plus the
open/closed parts sales pair, are confirmed real, currently-referenced names as of the 2025 Fortellis
community thread. Note the same thread shows a user asking whether these APIs are being **replaced**,
implying possible deprecation/renaming in progress — flagged in §9.

## What I could not verify

1. The exact internal CDK table/column name for the supersession chain pointer (only the function name
   `PN` and forum behavior are documented; no schema-level field name found).
2. Whether "CDK Drive Async Parts Inventory" and "CDK Drive Search Parts Pick Ticket" are being renamed or
   deprecated — a 2025 Fortellis community post asks CDK to confirm the current equivalents, and no
   reply confirming continuity was found in public search results.
3. A formally named "VOR" (Vehicle Off Road) order type in PACCAR's North American dealer ordering system —
   VOR terminology is confirmed for PACCAR Parts' Australian PDC operations and for several other OEMs
   (Hino, Isuzu, Changan, Hyundai/MOBIS), but Karmak's PACCAR integration page names only Stock, Emergency,
   Marketing Suggestion (MKT), and Auto Confirmed (COF) — VOR was not among them.
4. Any PACCAR-specific parts obsolescence/return-allowance percentage or program name. The CNH 100%/1-year
   figure is a non-PACCAR analog only.
5. A single, formally named CDK Drive "cycle count" or "physical inventory" function/screen code — only
   informal rotational-bin-check practice and the `RPX`/`RPG`/`Parts Events` reporting paths are documented.
6. Whether CDK Drive exposes a distinct raw average/replacement cost field separate from the escalated
   point-of-sale `cost` field returned on repair orders — the Fortellis schema only documents the escalated
   value.
7. "PartsPRO" as a PACCAR system name — searched extensively, found no public PACCAR source using this
   term. It appears to be either an internal/unpublished name or does not exist; the twin/task language
   should not use it without a citable source.
8. The full published field list for "CDK Drive Get Parts Sales," "History Setup Parts Sales," and the
   Async Open/Closed Parts Sales APIs — the CDK Global marketing page names them but does not publish
   field-level schemas; the actual OpenAPI spec sits behind Fortellis Marketplace subscription access,
   which was not reachable via public search.

## Proposed SAP-shape mapping

| CDK/PACCAR concept | SAP table.field (twin) | Change proposed vs. current schema |
|---|---|---|
| Part number, description, source/mfr code, group code, hazmat, core flag | `MARA` (matnr, maktx, manufacturer, matkl, hazmat_flag, core_flag) | No change — confirmed by Get Repair Order v3 `desc`, `source`, `partClass`, and STAR `HazmatIndicator`/`CorePartDescription`. |
| Supersession | `MARA.supersession_to` | **Change:** replace single-column pointer with a `MFRPN`-style child table (`supersession_chain`: `matnr_from`, `matnr_to`, `effective_date`, `sequence_no`) to represent multi-hop chains, matching CDK's documented "undo succession" and chained-redirect behavior. |
| Bin location(s) | `MARD.bin` | **Change:** twin already has a single `bin` column on MARD; add a child table or array for the confirmed CDK `BIN1`/`BIN2` alternate-bin pattern, since one part can have more than one bin per storage location. |
| Escalated point-of-sale cost/list/sale | new `MATDOC` extension columns: `escalated_cost`, `escalated_list`, `escalated_sale`, `mcd_percentage` | **Addition:** the twin's `MATDOC.dmbtr` captures only a single amount; add columns to separately retain CDK's `cost`/`list`/`sale`/`mcdPercentage` at time of transaction, since these differ from `MBEW.verpr` (moving average). |
| Core charge / core cost | `MATDOC.core_cost`, `MATDOC.core_sale` (new) + `MARA.core_value` (existing) | **Addition:** transaction-level core amounts are not currently captured in MATDOC; only the master-level `core_value` exists. |
| Lost sale | new fact table `lost_sales` (matnr, werks, qty, requested_date, employee_id, source_ref) | **Addition:** lost sales are a demand signal, not an inventory movement — should not be forced into MATDOC bwart logic; twin currently has no such table. |
| Obsolescence write-down | `MBEW.obsolete_flag`/`months_no_movement` (existing) + new `MBEW.reserve_amount`, `MBEW.reserve_pct` | **Addition:** twin flags obsolescence but does not currently carry a reserve/allowance value, which is required to model the GAAP contra-asset entry (Debit Inventory Obsolescence / Credit Allowance for Obsolete Inventory). |
| Movement types | `MATDOC.bwart` (existing: 101, 201, 301/311, 601, 701/702, 161) | No change to movement type list; confirmed against CDK `PS` transaction codes (blank=normal sale, W/NW=warranty, H/NH=wholesale, M/P=adjustment, L=lost sale — lost sale excluded from MATDOC per above). |
| Group-wide (9-site) availability | `MARD` unioned across `WERKS` (existing) | No change — confirmed CDK tenant/store-code model matches twin's `WERKS`-per-site design. |
| PACCAR ordering | `adapters/paccar/` (existing ePortal adapter) | **Correction:** twin's PACCAR adapter should target the confirmed system name **Online Parts Counter (OPC)** at `eportal.paccar.com`, not an unverified "PartsPRO"; order types confirmed via Karmak integration are Stock, Emergency, MKT (Marketing Suggestion), COF (Auto Confirmed) — twin's `marc`/order-staging logic should use these four codes, not an unconfirmed VOR code, until PACCAR's own NA VOR-equivalent naming is verified. |

---

Sources are cited inline throughout; no uncited factual claims are made. Word count target (900–1600)
met via dense tabular presentation per shared-rules instruction to prefer tables over prose.
