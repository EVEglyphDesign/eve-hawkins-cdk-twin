# Module 06 — Document Flow

**Status: drafted from lane 6 research (`cdk_06_transactions.md`), cross-referenced against
lane 8 (`cdk_08_paccar_oem.md`) for the PACCAR-specific warranty and heavy-truck lifecycle
steps. This module traces documents end-to-end: deal desk, service RO, parts counter,
warranty, AR/cashiering, AP/purchasing, and payroll. See `docs/open-questions.md` for
unresolved chargeback and reconciliation mechanics.**

---

## 1. Deal desk (vehicle sales) lifecycle

Documented states: **Pending → Finalized/Booked**, with a **We-Owe** object tracking
post-sale commitments owed to the customer (accessories, service items promised at time of
sale) that remain open after the deal books. `DOCUMENTED` state names; the full state machine
transition rules (e.g., what triggers Pending→Finalized beyond deal signature/funding) are
`UNVERIFIED` beyond the two named states plus We-Owe.

Proposed SAP mapping:

| CDK concept | Proposed SAP object |
|---|---|
| Deal (Pending/Finalized) | Sales order (`VBAK`/`VBAP`) with a custom status field for Pending/Booked, since native SD status profiles don't map 1:1 to deal-desk terminology |
| We-Owe | Custom open-item object (`ZWEOWE`) linked to the deal and to Module 06 §3 parts/labor fulfillment when the owed item is delivered |

## 2. Service repair order (RO) lifecycle

States: **Appointment → Open/WIP → Closed.** Confirmed Fortellis retrieval APIs include
`getOpenRepairOrdersBulk` (bulk pull of currently open ROs) alongside the Get Repair Order v3
detail API already used as the field-name source for parts lines (Module 04) and labor/RO
header fields (Module 03). `DOCUMENTED` state names and at least one bulk retrieval API name.

Proposed SAP mapping: RO as SAP-internal-order analogue is already established in Module 03
§2 — this module does not restate that mapping, only the document *flow* around it
(Appointment creation → WIP → invoice/close triggers the postings Module 02 §4 describes).

## 3. Parts counter document flow

CDK distinguishes **Open Parts Sales** from **Closed Parts Sales** as separate object states,
each with dedicated Fortellis retrieval APIs (`CDK Drive Async Open/Closed Parts Sales`,
named in Module 04 §7). `DOCUMENTED`. A parts sale can exist independently of a repair order
(over-the-counter retail/wholesale sale) or as a line item consumed by an open RO (Module 04
§1's `PS` transaction code, blank/`H`/`NH`/`W`/`NW` flags).

## 4. Warranty document flow

This is the module's most heavy-truck-specific section, per lane 8.

1. **Repair performed** — technician diagnoses (often via PACCAR's **DAVIE4** diagnostic tool,
   which sits outside CDK entirely) and records cause/correction on the RO.
   ([NHTSA technical bulletin](https://static.nhtsa.gov/odi/tsbs/2022/MC-10209715-0001.pdf))
2. **Claim draft created from the RO** — Fortellis-listed integration **PRWS** ("PACCAR
   Registration and Warranty System") is described by CDK itself as streamlining "the filing
   of PACCAR warranty claims by creating drafts in the PACCAR PRWS (warranty system) with
   information from the RO and tracking via a dynamic status screen."
   ([CDK Global Heavy Truck OEM page](https://www2.cdkglobal.com/ht-oem))
3. **Claim type selection in PRWS** — "Quick Claim" (pre-coded campaign/failure code) or "long
   claim" (manual Campaign #, Failure type, Standard Repair Time/SRT).
   ([NHTSA bulletin](https://static.nhtsa.gov/odi/tsbs/2022/MC-10209715-0001.pdf))
4. **Data required**: VIN, causal part number, Claim Category, Concern/Cause/Correction
   narrative, SRT code, claim story text.
   ([PACCAR/JW Speaker warranty portal instructions](https://paccar.jwspeaker.com/documents/JW%20Speaker%20Extended%20Warranty%20-%20Portal%20Instructions.pdf))
5. **Submission window** enforced per warranty policy bulletin (example cited: 14 days).
   ([NHTSA bulletin](https://static.nhtsa.gov/odi/tsbs/2022/MC-10209715-0001.pdf))
6. **Resubmission** — claims can be saved/resent without full re-entry (confirmed via the
   Procede/Excede PRWS v1.2 integration announcement, a comparable competing DMS's PRWS
   integration, not CDK's own — cited here as corroboration of PRWS's external behavior).
   ([LinkedIn — Procede/Excede PRWS v1.2](https://www.linkedin.com/posts/procede-software_procedesoftware-excededms-productupdate-activity-7402395748069548032-qWoj))

**The flow is one-directional from the twin's perspective: RO → PRWS draft.** There is no
public evidence of a return feed bringing claim-adjudication results (approved/denied/adjusted
amount) back into CDK Drive automatically — reconciliation of denied/adjusted claims against
the dealer's warranty receivable appears to be a manual dealer-side accounting step.
`UNVERIFIED` chargeback mechanics — flagged in `docs/open-questions.md`.

Proposed SAP mapping (per lane 8's proposal, reproduced here since it belongs to document
flow, not master data):

| CDK/PACCAR concept | Proposed SAP-shape object |
|---|---|
| Warranty claim (PRWS draft, status, SRT, campaign code) | Custom object `ZWARR_CLAIM` — VIN, Claim Category, Campaign Code, SRT, Concern/Cause/Correction, claim status, PRWS claim number. No native MM/SD table models an OEM warranty claim at this fidelity. |
| Warranty receivable / chargeback on denial | Posts against the warranty receivable G/L account already defined in Module 02 §4 — exact chargeback trigger is `UNVERIFIED` |

## 5. AR / cashiering

Confirmed Fortellis API: **CDK Drive Payment Settling API**, supporting **PayNow** and
**Invite-2-Pay** flows, with a **PromiseID** object tracking a customer's promise-to-pay
commitment ahead of actual settlement. `DOCUMENTED`.

Proposed SAP mapping:

| CDK concept | Proposed SAP object |
|---|---|
| Payment/settlement | `BSEG`/`BSID` line-item posting on settlement, referencing the RO/deal/parts-sale document |
| PromiseID | Custom object `ZPROMISE_PAY` (no native SAP "promise to pay" object at this granularity — closest analogue is a dunning/collections note, not a structured object) |

## 6. AP / purchasing

Documented via **Foundations Suite** and a **GL Inquiry Workflow**. Three-way match
(PO → receipt → invoice) as a *native* CDK capability is `UNVERIFIED` — lane 6 found
references to the Foundations Suite AP workflow and GL inquiry but no explicit confirmation
that three-way matching is automated inside CDK versus performed manually by AP staff using
the GL Inquiry Workflow as a lookup tool.

**Payroll has no CDK-native API.** Time/hours flow to CDK from the RO (technician flat-rate
time already established in Module 03 §3, via `technicianIds[]`), but actual payroll
processing is handled by third-party systems — ADP, Netchex, Workzoom — integrated primarily
through **file export**, not a live API. `DOCUMENTED` as a confirmed gap. This is the primary
justification for `adapters/export-fallback/README.md` existing as a first-class adapter
rather than a minor fallback note.

## 7. Heavy-truck-specific document flow additions

Beyond warranty (§4), lane 8 documents:

- **Online Parts Counter (OPC)** — PACCAR's real dealer parts-ordering platform
  (`eportal.paccar.com` / branded `PartsCounter.Kenworth.com`), integrating with DMS platforms
  including Karmak Fusion. No public REST API; structured B2B order upload/download exists.
  **"PartsPRO" is not a real PACCAR system name and must not be used anywhere in this repo.**
  ([Rihm Kenworth OPC description](https://www.rihmkenworth.com/blog/the-benefits-of-online-parts-counter--55573))
- **Electronic invoices and ASN** — PACCAR Parts sends electronic invoices (imported to DMS
  AP) and electronic packing slips (ASN) used to receive parts into dealer inventory via DMS
  integration (documented for Karmak Fusion; CDK Drive Heavy Truck's equivalent is
  `UNVERIFIED` but structurally analogous).
  ([Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar))
- **Decisiv-powered case management** — **PACCAR Solutions/PSSM**, **TruckTech+** (Kenworth),
  and **SmartLINQ** (Peterbilt) auto-create service cases from fault codes and push repair
  estimates into the dealer DMS; the case auto-closes when the RO is invoiced. **Peterbilt of
  Atlanta is itself named as a Decisiv-connected dealer** in Decisiv's own materials — direct
  evidence this integration pattern is live at Peterbilt-branded dealer locations, though not
  confirmed specifically for Peterbilt Atlantic (Atlantic Canada) as a named account.
  ([PACCAR Solutions login](https://paccar.decisiv.net/), [Decisiv help center](https://support.paccar.decisiv.net/hc/en-us))
- **PACCAR Parts Fleet Services / Service Gate** — payment-card and invoice/remittance
  platform for fleet/national accounts, structured invoice/remittance transmission via DMS
  integration. ([PACCAR Parts Fleet Services PDF](https://www.paccarpartsfleetservices.com/pdf/PACCAR.pdf))
- **Electronic Shipper** — referenced as a roadmap item in lane 6 research; treat as
  `UNVERIFIED`/forward-looking rather than a confirmed live document type.

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
