# Module 03 — Cost Objects

**Status: drafted from lane 3 research (`cdk_03_costobjects.md`). Several field-level names
(host-side department field, OpCodes "flat rate hours" field name, GL elimination mechanics
for internal work) remain unverified — see `docs/open-questions.md`.**

Covers: departments as cost/profit centres, the repair order as cost collector, technician
time, absorption.

---

## 1. Departmental accounting: the department as profit centre

Dealer accounting is legally one entity but is always operated as a set of internal
mini-P&Ls. The standard chart-of-accounts department set is: New Vehicle, Used Vehicle,
Parts, Service, Body Shop, Rental/Lease, Finance & Insurance (F&I), and
Administrative/General & Overhead
(`INFERRED (dealer-accounting norm)`, consistent with the
[NIADA Dealership Chart of Accounts Manual](https://studylib.net/doc/8765679/dealership-chart-of-accounts-manual)
and the [IRS New Vehicle Dealership Audit Techniques Guide](https://www.irs.gov/ko/businesses/new-vehicle-dealership-audit-techniques-guide-2004-chapter-3-balance-sheet-12-2004)).
Service, Parts, and Body Shop are jointly referred to as "Fixed Operations" in industry
literature ([Brady Ware CPAs](https://bradyware.com/car-dealership-financial-management/)).

| Department | Typical revenue lines | Analogous SAP object |
|---|---|---|
| New Vehicle | Unit sales, holdback, floorplan assistance | Profit centre |
| Used Vehicle | Retail/wholesale unit sales | Profit centre |
| Parts | Counter, wholesale, warranty, internal parts sales | Profit centre |
| Service | Labor: customer pay, warranty, internal | Profit centre |
| Body Shop | Collision labor, materials, insurance-paid work | Profit centre |
| Rental/Lease | Rental unit revenue | Profit centre |
| F&I | Finance reserve, insurance/VSC commissions | Profit centre |
| Admin/Overhead | None (cost pool only) | Cost centre (non-revenue) |

NADA's own 20 Group product description states the purpose is to "analyze profitability,
expense absorption and employee productivity **across each dealership department**"
([NADA 20 Group](https://www.nada.org/nada/nada-20-group)), confirming the department is the
standard unit of P&L measurement industry-wide.

## 2. The department dimension on every transaction — CDK's cost-centre analogue

In CDK Drive / Fortellis, the field that plays the SAP cost-centre role is the
**Department-Id**. The Fortellis "CDK Drive Get Customer v3" API spec states explicitly: "The
`Department-Id` request header identifies the DMS department targeted by the requests sent to
the service. The response data is filtered by the Department ID specified in the request"
([CDK Drive Get Customer v3, Fortellis API doc](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf)).
Each DMS department is configured against exactly one DMS type — Accounting, Finance,
Inventory, Parts, or Service.

Each physical store has its own set of Department-Ids
([Fortellis Community — CDK Marketplace Subscriptions](https://community.fortellis.io/community/forum/install-app-subscriptions-and-support/cdk-fortellis-marketplace-subscriptions-and-support)).

`UNVERIFIED`: the exact host-side (pre-Fortellis) field name CDK uses internally for the
department/schedule dimension on a raw GL posting line. Only the externally exposed
`Department-Id` header is documented publicly.

## 3. The repair order as SAP-internal-order analogue

CDK's Fortellis "Get Repair Order v3" schema carries three explicit boolean pay-type flags on
every RO: `hasCustPayFlag`, `hasIntPayFlag`, `hasWarrPayFlag`
([CDK Drive Get Repair Order v3, Fortellis API doc](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf)).
A single RO is a header with multiple jobs/lines, and each line independently carries a pay
type — customer pay (retail), warranty, or internal.

CDK's own pay-type/service-type code list enumerates over 40 codes bucketed into three
families: `CP*`/`SR*` (customer pay/service retail), `W*`/`SW*` (warranty by claim-payer,
e.g. `WCM`=Warranty Cummins, `WNA`=Warranty Navistar), `I*`/`SI*` (internal, further split —
`I` internal service policy, `ICV` internal company vehicle, `IDU` internal demo unit, `IGP`
internal goodwill policy, `IPW` internal parts warranty/shop supplies)
([CDK Reference — New Procede Service Types, Leonard Bus Sales](https://www.leonardbus.com/wp-content/uploads/2022/03/SERVICE-TYPE-REFERENCE-v3-3-2022.pdf)).

Each pay type resolves to a different receivable/schedule target: customer pay posts to open
trade A/R, warranty posts to warranty-company control accounts (e.g. `&WARCMN`, `&WARNAV`),
internal posts to internal cost-pool accounts (e.g. `&100SPA`, `&CVNEW`, `&NBPOL`)
([CDK Reference — New Procede Service Types](https://www.leonardbus.com/wp-content/uploads/2022/03/SERVICE-TYPE-REFERENCE-v3-3-2022.pdf)).

**The repair order is the closest object in CDK Drive to an SAP internal order:** like an SAP
internal order, it is a temporary, self-contained cost collector that accumulates multiple
cost elements (labor, parts, sublet, shop supplies) against a single header number, is closed
out and settled once, and settles/distributes to different final targets depending on a type
field — pay type here plays the role SAP's order category/settlement rule plays for an
internal order.

## 4. Technician time: flat rate vs. clock hours

Flat-rate hours are the standardized time allowance published in OEM/third-party time guides
for a given operation code (opcode); technicians are typically paid on flat-rate "hours
sold," not literal clock hours
([Liberty CDJR — What Is Labor Rate at a Dealership](https://www.libertychryslerdodgejeep.com/blog/what-is-labor-rate-at-a-dealership-2026-guide)).
CDK's opcode-level labor time standards are exposed via the **CDKDrive OpCodes API** on
Fortellis ([CDKDrive OpCodes, Fortellis Community](https://community.fortellis.io/api-reference/vehicle-service/cdkdrive-opcodes)).
`UNVERIFIED` at field-name level whether the standard-hours field is called "flat rate hours,"
"book time," or another CDK-specific label.

CDK's dealer-training material confirms technician time is captured at the RO line level in
tenths of an hour ([CDK dealer training video — closing a customer pay RO](https://www.youtube.com/watch?v=K19r_1wFi1Q)).

| Metric | Formula | Source |
|---|---|---|
| Effective Labor Rate (ELR) | Total labor sales ÷ total labor hours sold | [Liberty CDJR](https://www.libertychryslerdodgejeep.com/blog/what-is-labor-rate-at-a-dealership-2026-guide) |
| Technician efficiency | Flat-rate (sold) hours ÷ clock hours worked | `INFERRED (dealer-accounting norm)` |
| Technician proficiency | Flat-rate (sold) hours ÷ hours scheduled/available | `INFERRED (dealer-accounting norm)` |
| Labor cost per hour | Technician wage cost ÷ hours produced | `INFERRED (dealer-accounting norm)` |

Labor cost on **open** ROs must reconcile monthly to a Work-in-Process account (247), with
variances cleared to a labor adjustment account
([GM Standard Accounting Manual — Account 472/672](http://gm.acctmanual.com/Fixed_Operations/472_Warranty_Claim_Labor_Body_Shop.htm)) —
evidence that the RO functions as a WIP-bearing cost object until closed.

## 5. Internal work: charging one department for another's labor

When Service performs work for another department (reconditioning a used vehicle, PDI on a
new unit), the job is opened as an internal RO rather than a customer-pay RO. CDK's own
pay-type taxonomy has dedicated internal codes for this: `ICV`, `IDU`, `IUB`
([CDK Reference — New Procede Service Types](https://www.leonardbus.com/wp-content/uploads/2022/03/SERVICE-TYPE-REFERENCE-v3-3-2022.pdf)).
A comparable DMS (Autosoft) documents the mechanism explicitly: the receiving cost object for
internal work is the **vehicle stock number**, not a customer account
([Autosoft Repair Orders guide](https://download.autosoft-asi.com/instructions/S/RepairOrders.pdf)).

`UNVERIFIED`: whether CDK Drive posts an explicit intercompany-style elimination entry or
simply nets the two departmental lines through the vehicle inventory schedule.

## 6. Vehicle reconditioning cost and the used-vehicle inventory cost object

CDK Drive exposes a dedicated **Display Vehicle Cost** screen, accessible from the Vehicle
Dashboard, a vehicle's inventory record, or the "Acctg Cost" column in Vehicle Search results,
which "displays accurate and real-time General Ledger (GL) items, including any open Purchase
Orders or Repair Orders and their amounts," with drill-down to underlying posting documents
([CDK Display Vehicle Cost screen documentation](https://lithia.vehicle.connectcdk.com/pid1033/help/client/scr-vehcost/veh_ov_display_vehicle_cost.htm)).
This confirms the **stock number** is the cost object internal recon ROs and parts tickets
post against.

`UNVERIFIED`: the exact GL account/field names CDK uses to separate acquisition cost, pack,
reconditioning labor, reconditioning parts, and floorplan interest within that roll-up.

## 7. Overhead allocation and the 20-group/ATD composite benchmark

Overhead is allocated from the Administrative/Overhead pool to revenue departments using
dealer-defined prorate methods — gross-profit contribution share, square footage, headcount,
or a fixed historical split
([NCM Associates — How to Control Expenses Across Departments](https://ncmassociates.com/about-us/up-to-speed-blog/2018/april/how-to-control-expenses-across-departments)).
The heavy-truck-specific composite benchmark runs under NADA's **ATD (American Truck
Dealers)** division, publishing an annual "ATD Performance Measurement Guide"
([NADA — American Truck Dealers](https://www.nada.org/atd)).

## 8. Absorption rate

Absorption rate is the percentage of total dealership fixed overhead covered by
fixed-operations gross profit, before a single vehicle is sold. NADA's 2026 Slide Guide gives:

> **Total Absorption** = total used-vehicle, service, parts and body shop gross profit ÷
> total dealership expense. Guide: 100%.
> **Fixed Absorption** = total fixed gross profit ÷ total dealer expense (adjusted). Guide: 60%.
([NADA/ATD Slide Guide — Fixed Absorption](https://atdslideguide.nada.org/fixedabsorption))

It is explicitly a management-reporting KPI computed from departmental gross-profit and
overhead figures, **not a discrete GL account or journal entry**
([Journal Entries Hub — Fixed Operations Absorption](https://www.journalentrieshub.com/entries/auto-service-absorption)) —
meaning it belongs in the semantic-views layer of `ARCHITECTURE.md`, computed from posted
department and RO data rather than stored as its own object.

## 9. Proposed SAP-shape mapping

| CDK concept | CDK evidence | Proposed SAP object in the twin |
|---|---|---|
| Department (per rooftop, per DMS type) | `Department-Id` header | Cost centre / Profit centre (`KOSTL`/`PRCTR`) — one profit centre per department per site |
| Repair Order (header + pay-type-flagged lines) | `hasCustPayFlag`/`hasIntPayFlag`/`hasWarrPayFlag` | Internal Order (`AUFK`), settlement rule keyed by pay type |
| Pay type (CP/Warranty/Internal codes) | CDK Procede service-type codes | Internal order settlement receiver category (customer A/R, warranty claim account, or WBS/asset) |
| Vehicle stock number (used-vehicle cost roll-up) | Display Vehicle Cost screen | WBS element / internal order settling to Material |
| Warranty/customer/internal receivable schedules | GM warranty account 263/472/672 pattern | Three parallel FI-AR sub-ledger accounts / special G/L indicators, one per pay type |
| Department overhead allocation | NCM prorate methods | CO-OM assessment/distribution cycle from Overhead cost centre to department profit centres |
| Absorption rate | NADA/ATD Slide Guide formula | Report-only KPI (semantic view), not a stored object |
| 20-group/ATD composite | NADA 20 Group, ATD Data | External benchmark feed joined to profit-centre actuals, not a native SAP object |

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
