# Module 05 — Master Data

**Status: drafted from lane 5 research (`cdk_05_masters.md`). This module covers customer,
vehicle, employee, vendor, and GL master data outside the parts master (Module 04). Several
schemas here are surface-only — no public CDK employee/vendor master schema was found. See
`docs/open-questions.md`.**

---

## 1. Customer master

The authoritative public field list comes from **CDK Drive Get Customer v3**, a Fortellis API.
Confirmed fields:

| Field | Description | Source |
|---|---|---|
| `customerId` | Unique customer identifier | [CDK Drive Get Customer v3 (Fortellis)](https://developer.fortellis.io/) |
| `customerName` | Individual or business name | Fortellis Get Customer v3 |
| `contactMethods` | Array of phone/email/address contact records | Fortellis Get Customer v3 |
| `overDues` | Overdue balance / AR aging indicator on the customer record | Fortellis Get Customer v3 |
| `partsFlag` | Flag distinguishing a parts-only account relationship | Fortellis Get Customer v3 |
| `isDeleteDataFlag` | Soft-delete / data-removal indicator (CASL/consent relevant, see §5) | Fortellis Get Customer v3 |
| `optOutFlag` | Marketing/communication opt-out flag | Fortellis Get Customer v3 |

**Business vs. individual customer:** CDK models a customer as **mutually exclusive**
business-or-individual — a record cannot be both simultaneously. Fleet accounts (the dominant
customer type for a heavy-truck dealer group like Peterbilt Atlantic) are business-type
customer records. `DOCUMENTED` (field-level structure); exact fleet-hierarchy modeling
(parent account → multiple VINs/drivers) beyond the flat business-customer record is
`UNVERIFIED`.

Proposed SAP mapping:

| CDK concept | Proposed SAP object |
|---|---|
| Customer master (business/individual) | `KNA1` (general data) / `KNB1` (company code data) |
| Contact methods array | `KNVK` (customer contact partner) or a child address table keyed to `KNA1` |
| Overdue/AR aging flag | Derived from `BSID`/`BSAD` (open/cleared AR items), not a stored master field |
| Opt-out / delete-data flags | Custom compliance extension to `KNA1` — no native SAP consent-timestamp field; see §5 |

## 2. Vehicle master

Two distinct, separately documented CDK surfaces:

1. **CDK Drive Service Vehicles API** (Fortellis) — a vehicle record scoped to the *service*
   department's view (VIN, make/model/year, mileage/last-service data used to build repair
   orders). `DOCUMENTED` as a distinct API surface from parts/inventory.
2. **Vehicle inventory record** (new/used truck in stock) — a separate CDK object tracking
   stock number, acquisition, and sale status; not the same schema as the Service Vehicles
   record. `DOCUMENTED` as structurally distinct; exact field list for the inventory-side
   vehicle record was not retrieved in lane 5 — `UNVERIFIED`.

**Heavy Truck DMS caveat:** CDK's Heavy Truck product line is a **separate CDK product** from
the light-vehicle Drive DMS lane 5 primarily documented against. Its vehicle/chassis schema is
not separately published. This matters directly for Peterbilt Atlantic: the VIN/chassis-number
and build-record concepts documented in lane 8 (`cdk_08_paccar_oem.md`) — 17-character VIN,
8-character chassis number, factory build record pulled from "PACCAR's B2B infrastructure" —
sit on the PACCAR side of the seam, not inside a published CDK Heavy Truck vehicle-master
schema. `UNVERIFIED` for the CDK-side field names; see Module 06 §5 and `adapters/paccar/README.md`.

Proposed SAP mapping:

| CDK concept | Proposed SAP object |
|---|---|
| Service Vehicles record (VIN, mileage, service history pointer) | Custom object `ZVEH_SERVICE`, keyed by VIN, referencing the service-order object (Module 06) |
| Vehicle inventory (new/used stock) | Custom object `ZVEH_STOCK` (stock number, acquisition date/cost, sale status) — no native SAP MM equivalent for a serialized truck-as-inventory-item at this fidelity without Serial Number Management (`EQUI`/`IEQ`), and even that is `UNVERIFIED` as unused |
| Factory build/chassis record | `ZVEH_BUILD` (per lane 8's proposed mapping) — 17-char VIN, 8-char chassis number, sourced from PACCAR's B2B feed, not CDK |

## 3. Employee master

**No public CDK employee-master schema was found.** Employee identity surfaces only
indirectly, through fields *on other objects*:

| Where employee identity appears | Field | Source |
|---|---|---|
| Repair order | `serviceAdvisor` | CDK Drive Get Repair Order v3 (referenced in Module 03/04 research) |
| Repair order | `cashier` | CDK Drive Get Repair Order v3 |
| Repair order | `technicianIds[]` | CDK Drive Get Repair Order v3 |

There is no confirmed "Get Employee" or "Employee Master" Fortellis API in the lane 5
research. Payroll-side employee records are handled by third-party systems (ADP, Netchex,
Workzoom) integrated via file export — see Module 06 §6 and `adapters/export-fallback/README.md`.
`UNVERIFIED`: whether CDK Drive exposes any employee-master API at all; treat as a confirmed
gap pending direct tenant access.

Proposed SAP mapping:

| CDK concept | Proposed SAP object |
|---|---|
| Employee IDs surfaced on RO/parts/GL records | `PERNR` (Personnel Number) reference field appended to relevant fact tables — but the twin has **no CDK-side master record to populate `PA0001`/`PA0002` from**; employee master must be sourced from payroll export files, not CDK |

## 4. Vendor / AP master

**No public CDK vendor-master API was found** in lane 5 research. AP/vendor data is
referenced only in the context of the Foundations Suite AP workflow (Module 06 §6) and the
GL Inquiry Workflow — neither of which lane 5 or lane 6 confirmed exposes a distinct vendor
master schema via Fortellis. `UNVERIFIED`.

Proposed SAP mapping (aspirational — no confirmed CDK source field list exists yet):

| CDK concept | Proposed SAP object |
|---|---|
| Vendor identity (name, remit-to address, terms) | `LFA1` (vendor general data) / `LFB1` (company code data) |
| Purchase pricing/terms per vendor (e.g., PACCAR Parts) | `EINA`/`EINE` (purchasing info record) |

## 5. GL / account master

Lane 5 confirms only a **marketing-level** signal: MindBridge (an AP/audit analytics vendor)
references a **"company number"** as a dimension on CDK-sourced GL data, consistent with the
Module 01 organization hierarchy (Company Number sitting between Client# and Department-Id).
No public CDK chart-of-accounts master API (distinct from the accounting-schedule mechanism
documented in Module 02) was found in lane 5. `UNVERIFIED` beyond what Module 02 already
established from lane 2.

## 6. CASL / consent compliance gap (Canadian relevance)

Lane 5's most concrete finding for a Canadian-headquartered dealer group: CDK's customer
record exposes only a binary **`optOutFlag`** and **`isDeleteDataFlag`** — it does **not**
capture the **consent timestamp, consent source, or consent scope** required for compliant
recordkeeping under Canada's **Anti-Spam Legislation (CASL)**. A block/opt-out flag alone is
insufficient evidence of when/how/why a customer opted in or out. `DOCUMENTED` as a structural
gap in the CDK customer schema itself, directly relevant to Peterbilt Atlantic's Atlantic
Canada operations.

**Proposed twin remediation:** a custom `consent_log` child table (customer_id, consent_type,
timestamp, source_channel, evidence_reference) that the twin populates going forward,
independent of what CDK's own flags capture. This does not retroactively fix historical gaps
in CDK's own data — it only prevents new gaps once the twin is the system of record for
consent evidence.

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
