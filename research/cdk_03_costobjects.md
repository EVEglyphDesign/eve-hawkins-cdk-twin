# CDK Drive — Cost Objects (Lane 3)
### SAP CO equivalence: cost centres, profit centres, internal orders, WBS elements

Client context: EVEglyphDesign is extending its SAP-shaped digital twin of CDK Drive for
Peterbilt Atlantic, a 9-site Peterbilt/PACCAR heavy-truck dealer group. This lane maps CDK's
department/RO/stock-number architecture onto SAP CO objects.

---

## 1. Departmental accounting: the department as profit centre

`DOCUMENTED` / `INFERRED (dealer-accounting norm)` — Dealer accounting is legally one
entity but is always operated as a set of internal mini-P&Ls. The standard NADA/NIADA
chart-of-accounts department set is: New Vehicle, Used Vehicle, Parts, Service, Body Shop,
Rental/Lease, Finance & Insurance (F&I), and Administrative/General & Overhead
(`INFERRED (dealer-accounting norm)`, consistent with the [NIADA Dealership Chart of Accounts Manual](https://studylib.net/doc/8765679/dealership-chart-of-accounts-manual) and the [IRS New Vehicle Dealership Audit Techniques Guide](https://www.irs.gov/ko/businesses/new-vehicle-dealership-audit-techniques-guide-2004-chapter-3-balance-sheet-12-2004)).
Service, Parts, and Body Shop are jointly referred to as "Fixed Operations" in industry
literature ([Brady Ware CPAs](https://bradyware.com/car-dealership-financial-management/)).
Each department carries its own sales, cost-of-sales, gross profit, and (in more mature
setups) its own direct-expense block, which is exactly the SAP profit-centre pattern of a
mini income statement inside one company code.

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

`DOCUMENTED`: NADA's own 20 Group product description states the purpose is to "analyze
profitability, expense absorption and employee productivity **across each dealership
department**" ([NADA 20 Group](https://www.nada.org/nada/nada-20-group)), confirming the
department is the standard unit of P&L measurement in the industry, not just an internal
convention.

---

## 2. The department dimension on every transaction — CDK's cost-centre analogue

`DOCUMENTED` — In CDK Drive / Fortellis, the field that plays the SAP cost-centre role is
the **Department-Id**. The Fortellis "CDK Drive Get Customer v3" API spec states explicitly:
"The `Department-Id` request header identifies the DMS department targeted by the requests
sent to the service. The response data is filtered by the Department ID specified in the
request" ([CDK Drive Get Customer v3, Fortellis API doc](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf)).
The same document states each DMS department is configured against exactly one **DMS
type** — Accounting, Finance, Inventory, Parts, or Service — and that an API call must
target a Department-Id that supports the Accounting DMS type to post/read accounting data.

`DOCUMENTED`: Fortellis community guidance confirms each physical store ("rooftop") has its
own set of Department-Ids: "each store will have their own set of departments-id's ... you
can download the subscription report of the App ... it has all the details of the store
associated with each api under DMS attributes column against each subscription-id"
([Fortellis Community — CDK Marketplace Subscriptions](https://community.fortellis.io/community/forum/install-app-subscriptions-and-support/cdk-fortellis-marketplace-subscriptions-and-support)). The BettrData integration guide for Fortellis/CDK confirms departments are enumerated per
dealership subscription and named by function, e.g. "CDK Drive History Setup FI Sales"
([BettrData Fortellis CDK Drive API guide](https://docs.bettrdata.io/user-docs/how-to-guides/fortellis-cdk-drive-api)).

`INFERRED (dealer-accounting norm)`: On the legacy/host side (pre-Fortellis, terminal-style
CDK Drive, formerly ADP/CDK "Drive"), the department is coded as a numeric or short
alphanumeric **schedule/department number** attached to every GL account and every posting
line, matching the general dealer-DMS pattern documented for the comparable Autosoft DMS:
GL accounts are tagged with a **Schedule Index** (0 = No Schedule, 1 = Vehicle Inventory,
2 = A/R, 3 = A/P, 4 = Misc Balance Forward, 5 = Misc Detail Forward, 6 = Combination) so that
every subsidiary-ledger posting is automatically routed to the correct department/schedule
combination ([Autosoft Accounting setup guide](https://download.autosoft-asi.com/instructions/A/Accounting.pdf)).
CDK's own architecture is not published at this level of table/field granularity in public
sources — mark as `UNVERIFIED` the exact host-side field name CDK uses internally (Fortellis
confirms only the externally exposed `Department-Id` header).

**CDK cost-centre analogue: `Department-Id` (Fortellis) / department-schedule number (host)** — carried as a mandatory tag on every accounting-type API call and, by dealer-accounting
convention, on every journal line, exactly as an SAP cost centre is mandatory on every FI/CO
line item.

---

## 3. The repair order as SAP-internal-order analogue

`DOCUMENTED` — CDK's Fortellis "Get Repair Order v3" schema carries three explicit boolean
pay-type flags on every RO: `hasCustPayFlag`, `hasIntPayFlag`, `hasWarrPayFlag` ("If true,
the repair order has customer pay charges" / "internal pay charges" / "warranty pay
charges") ([CDK Drive Get Repair Order v3, Fortellis API doc](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf)).
A single RO is a header with multiple **jobs/lines**, and each line independently carries a
pay type — customer pay (retail), warranty, or internal — which is how one RO can be "split"
across three revenue/receivable streams simultaneously ([Motility Software RO documentation](https://help.motilitysoftware.com/hc/en-us/articles/360060548292-Repair-Order-Service-Invoice-RO); [CDK dealer training video — closing a customer pay RO](https://www.youtube.com/watch?v=K19r_1wFi1Q)).

`DOCUMENTED`: CDK's own pay-type/service-type code list (from a live dealer's CDK Procede
reference sheet) enumerates over 40 codes bucketed into three families: **CP\* / SR\*** =
customer pay/service retail; **W\* / SW\*** = warranty by claim-payer (e.g. WCM=Warranty
Cummins, WNA=Warranty Navistar); **I\* / SI\*** = internal, further split by purpose (I =
internal service policy, ICV = internal company vehicle, IDU = internal demo unit, IGP =
internal goodwill policy, IPW = internal parts warranty/shop supplies) ([CDK Reference — New Procede Service Types, Leonard Bus Sales](https://www.leonardbus.com/wp-content/uploads/2022/03/SERVICE-TYPE-REFERENCE-v3-3-2022.pdf)).

`DOCUMENTED`: Each pay type resolves to a different receivable/schedule target: customer
pay posts to "ANY CUSTOMER ACCOUNT" (open trade A/R), warranty posts to warranty-company
control accounts (e.g. `&WARCMN`, `&WARNAV`), and internal posts to internal cost-pool
accounts (e.g. `&100SPA`/`101SPA`, `&CVNEW`, `&NBPOL`) — confirming three parallel
receivable/absorption schedules can be driven from a single RO ([CDK Reference — New Procede Service Types](https://www.leonardbus.com/wp-content/uploads/2022/03/SERVICE-TYPE-REFERENCE-v3-3-2022.pdf)).
The generic dealer-accounting pattern (Autosoft) confirms the same three-way split exists
industry-wide: "filter the list based on the repair type: customer pay (C/P), warranty
(W/C), internal" ([Autosoft Repair Orders guide](https://download.autosoft-asi.com/instructions/S/RepairOrders.pdf)).
Parts consumed on an RO carry their own transaction-code suffix mirroring the RO's pay type
— blank/N = normal, W/NW = warranty, DS/DW = warranty drop-ship — so a parts sale is coded
to match its parent RO line ([CDK Transaction Codes reference, Total Dealer Solutions](https://totaldealersolutions.zendesk.com/hc/en-us/articles/360060331572-CDK-Transaction-Codes)).

**RO as internal-order analogue — say so explicitly**: the repair order is the closest
object in CDK Drive to an SAP internal order. Like an SAP internal order, it is a
temporary, self-contained cost collector that (a) accumulates multiple cost elements
(labor, parts, sublet, shop supplies) against a single header number, (b) is closed out and
settled once, and (c) settles/distributes to different final targets depending on a
type field — pay type here plays the role SAP's order category/settlement rule plays for an
internal order. `INFERRED (dealer-accounting norm)`: sublet (outside vendor labor) and shop
supplies post as additional cost lines on the same RO number, alongside labor and parts,
consistent with the RO's role as the shop-floor cost object; a Reddit dealer-forum thread on
CDK usage corroborates sublet as a distinct RO line type separate from labor ([r/serviceadvisors — CDK sublet in internal line](https://www.reddit.com/r/serviceadvisors/comments/1to4b52/cdk_users_sublet_in_customer_pay_in_an_internal/)).

---

## 4. Technician time: flat rate vs. clock hours

`DOCUMENTED`/`INFERRED (dealer-accounting norm)` — Flat-rate hours are the standardized time
allowance published in OEM/third-party time guides for a given operation code (opcode);
technicians are typically paid on flat-rate "hours sold," not literal clock hours: "Flat-rate
labor charges are calculated from industry-standard time guides or manufacturer-published
repair times, so a job estimated at 2.5 hours costs 2.5 hours of labor whether the
technician finishes in 90 minutes or three hours" ([Liberty CDJR — What Is Labor Rate at a Dealership](https://www.libertychryslerdodgejeep.com/blog/what-is-labor-rate-at-a-dealership-2026-guide)).
CDK's opcode-level labor time standards are exposed via the **CDKDrive OpCodes API**
on Fortellis ([CDKDrive OpCodes, Fortellis Community](https://community.fortellis.io/api-reference/vehicle-service/cdkdrive-opcodes)) — `UNVERIFIED` at field-name level whether the standard-hours field
is called "flat rate hours," "book time," or another CDK-specific label; mark for
verification against the OpCodes schema.

CDK's dealer-training material confirms technician time is captured at the RO line level in
tenths of an hour ("technician hours in this particular case we're going to put 120 which
stands for 1.2") and can be corrected by amount independent of hours via a `CSA` (change sale
amount) command ([CDK dealer training video — closing a customer pay RO](https://www.youtube.com/watch?v=K19r_1wFi1Q)).

Key fixed-ops KPIs built on technician time (`DOCUMENTED`, industry-standard formulas, not
CDK-specific):

| Metric | Formula | Source |
|---|---|---|
| Effective Labor Rate (ELR) | Total labor sales ÷ total labor hours sold | [Liberty CDJR](https://www.libertychryslerdodgejeep.com/blog/what-is-labor-rate-at-a-dealership-2026-guide); [Vision Management](https://www.visionmgroup.com/post/fixed-ops-kpis) |
| Technician efficiency | Flat-rate (sold) hours ÷ clock hours worked | `INFERRED (dealer-accounting norm)` |
| Technician proficiency | Flat-rate (sold) hours ÷ hours scheduled/available | `INFERRED (dealer-accounting norm)` |
| Labor cost per hour | Technician wage cost ÷ hours produced | `INFERRED (dealer-accounting norm)` |

Labor cost lands in the ledger as **Cost of Sales — Labor**, split by the same pay-type the
RO carries: e.g. GM's standard chart posts warranty body-shop labor cost to account 672
("Cost of Sales — Warranty Claim Labor — Paint & Body") against a receivable debit to account
263 ("Warranty Claims"), with technician incentive pay also charged to cost-of-labor-sales,
while non-productive pay (holiday/vacation/sick) is excluded and expensed instead
([GM Standard Accounting Manual — Account 472/672, Warranty Claim Labor Body Shop](http://gm.acctmanual.com/Fixed_Operations/472_Warranty_Claim_Labor_Body_Shop.htm)). The same manual notes labor cost on **open** ROs
must reconcile monthly to a Work-in-Process account (247), with variances cleared to a labor
adjustment account — direct evidence that the RO functions as a WIP-bearing cost object
until closed.

---

## 5. Internal work: charging one department for another's labor

`DOCUMENTED`/`INFERRED (dealer-accounting norm)` — When Service performs work for another
department (classically, reconditioning a used vehicle in Used Vehicle inventory, or PDI on
a new unit), the job is opened as an **internal RO** rather than a customer-pay RO. CDK's own
pay-type taxonomy has dedicated internal codes for this: `ICV` (internal company vehicle,
routing to `&CVNEW`/`&CVUSED`/`&CVPARTS`/`&CVSERV`), `IDU` (internal demo unit), `IUB`
(internal trade bus/used-unit work) ([CDK Reference — New Procede Service Types](https://www.leonardbus.com/wp-content/uploads/2022/03/SERVICE-TYPE-REFERENCE-v3-3-2022.pdf)). A comparable DMS (Autosoft) documents the
mechanism explicitly: "When you start a repair order for a vehicle in your inventory
(internal), use the vehicle's stock number as the customer number ... The repair total for
the vehicle is added to the Internal amount, which is the total value of all internal
repairs for the vehicle" ([Autosoft Repair Orders guide](https://download.autosoft-asi.com/instructions/S/RepairOrders.pdf)) — i.e., the receiving cost object for
internal work is the **vehicle stock number**, not a customer account.

`INFERRED (dealer-accounting norm)`: To avoid double-counting revenue at the dealership
level, the internal RO posts labor/parts **cost** as a debit to the receiving department's
inventory or expense account (e.g., used-vehicle inventory for recon, or a fixed asset/
expense account for PDI) and posts an offsetting **internal sale** in Service at a
discounted/cost-plus internal rate; because both the internal "sale" (Service revenue) and
the internal "cost" (Used Vehicle inventory addition) sit inside the same legal entity, they
net to zero at the whole-dealership P&L even though Service still reports internal-pay gross
for departmental scorecarding. The GM manual's parallel warranty entry shows the same
double-sided posting logic (debit a receivable/inventory, credit a departmental sales
account, debit departmental cost-of-sales) applied to warranty; the internal case substitutes
a used-vehicle inventory debit for the warranty receivable debit ([GM Standard Accounting Manual — Account 472/672](http://gm.acctmanual.com/Fixed_Operations/472_Warranty_Claim_Labor_Body_Shop.htm)). `UNVERIFIED`: whether CDK Drive
posts an explicit intercompany-style elimination entry or simply nets the two departmental
lines through the vehicle inventory schedule — no public CDK source documents the exact GL
elimination mechanics; treat as open question.

---

## 6. Vehicle reconditioning cost and the used-vehicle inventory cost object

`DOCUMENTED` — CDK Drive exposes a dedicated **Display Vehicle Cost** screen, accessible
from the Vehicle Dashboard, a vehicle's inventory record ("Vehicle Cost" tab), or the "Acctg
Cost" column in Vehicle Search results, which "displays accurate and real-time General
Ledger (GL) items, including any open Purchase Orders or Repair Orders and their amounts,"
with drill-down to the underlying posting documents ([CDK Display Vehicle Cost screen documentation](https://lithia.vehicle.connectcdk.com/pid1033/help/client/scr-vehcost/veh_ov_display_vehicle_cost.htm)). This confirms the **stock number** (vehicle
inventory record) is the cost object that internal recon ROs and parts tickets post against,
functioning as a running, real-time WIP roll-up analogous to an SAP internal order settling
to an asset/inventory object. `UNVERIFIED`: the exact GL account/field names CDK uses to
separate acquisition cost, pack, reconditioning labor, reconditioning parts, and floorplan
interest within that vehicle cost roll-up are not disclosed on the public help page —
flagged for direct verification against a live CDK instance or a fuller help-doc capture.

`INFERRED (dealer-accounting norm)`, consistent with generic dealer-accounting practice:
reconditioning cost accumulates through internal ROs charged to the vehicle's stock number,
increasing the vehicle's carrying value in the used-vehicle inventory schedule; each vehicle
inventory record functions as its own mini WIP/cost object until the unit is sold, at which
point the accumulated cost (acquisition + recon + pack) becomes cost of sales ([Ford accounting manual — Office Management, vehicle inventory record card](https://www.fmcdealerfbmi.dealerconnection.com/AccountingManual/en/ofc-mgmt-inventrs-en-htm/) — cross-industry OEM
accounting manual, cited as generic norm evidence, not CDK-specific).

---

## 7. Overhead allocation and the 20-group/ADA composite benchmark

`INFERRED (dealer-accounting norm)` — Overhead (rent, utilities, administrative salaries,
insurance) is allocated from the Administrative/Overhead pool to revenue departments using
dealer-defined prorate methods — gross-profit contribution share, square footage, headcount,
or a fixed historical "Z-split" percentage set by the dealer principal and revisited
periodically ([NCM Associates — How to Control Expenses Across Departments](https://ncmassociates.com/about-us/up-to-speed-blog/2018/april/how-to-control-expenses-across-departments)). This is the accounting-standard analogue of SAP overhead cost-centre
assessment/distribution cycles pushing cost-centre balances onto profit centres.

`DOCUMENTED` — The industry benchmark vehicle for this is the **20 Group / composite**
concept: NADA's 20 Group program pools ~20 non-competing, similarly sized, same-franchise
dealers who submit full financial statements to "analyze profitability, expense absorption
and employee productivity across each dealership department" against the peer composite
([NADA 20 Group](https://www.nada.org/nada/nada-20-group); [NADA 20 Group Live](https://www.nada.org/nada/education-consulting/20-group-live)). The heavy-truck-specific version runs under NADA's
**ATD (American Truck Dealers)** division, publishing an annual "ATD Performance
Measurement Guide" and its own composite-based Fixed/Total Absorption slide guide
([NADA — American Truck Dealers](https://www.nada.org/atd); [ATD Data](https://www.nada.org/atd/research/atd-data); [2017 ATD Performance Measurement Guide](https://www.scribd.com/document/356135941/2017-ATD-Performance-Measurement-Guide)). Composite reports show
composite average, median, and quartile breakdowns per expense/department line so an
individual dealer (or Peterbilt Atlantic site) can benchmark its department P&L against
peers ([Rework — Dealership Benchmarking](https://resources.rework.com/libraries/automotive-sales-growth/dealership-benchmarking)). NCM Associates runs a parallel commercial composite
service using top-half-of-performers averaging by franchise ([NCM Associates — Automotive Benchmark Reports](https://ncmassociates.com/dealer-solutions/benchmark-reports)).

---

## 8. Absorption rate

`DOCUMENTED` — Absorption rate (a.k.a. fixed absorption or service absorption) is the
percentage of total dealership fixed overhead covered by fixed-operations gross profit,
before a single vehicle is sold. NADA's own 2026 Slide Guide gives two explicit versions:

> **Total Absorption** = total used-vehicle, service, parts and body shop gross profit ÷
> total dealership expense. Guide: 100%.
> **Fixed Absorption** = total fixed gross profit ÷ total dealer expense, excluding lease &
> rental, minus new- & used-sales commissions, delivery & policy expense. Guide: 60%.
([NADA/ATD Slide Guide — Fixed Absorption](https://atdslideguide.nada.org/fixedabsorption); [2026 NADA Slide Guide PDF](https://slideguide.nada.org/NADASlideGuide.pdf))

Manufacturer-specific variants adjust the denominator: Ford dealers divide combined parts,
service, and body shop gross profit by total overhead expenses plus dealer salary plus
parts/mechanical/body-shop sales expense; Toyota dealers use "unabsorbed expenses" minus
new/used sales compensation, supervision compensation, and F&I commissions ([Kruse Control Inc. — Fixed Absorption Rate](https://www.krusecontrolinc.com/in-uncertain-times-steady-habits-win/)).
National benchmark: NADA's 2025 guide cites 60% as the fixed-absorption target while CBT
News reported a 63.9% national average in August 2025 ([Automotive KPI Calculators — Absorption Rate Calculator](https://automotivecalcs.com/dealer/absorption-rate-calculator/)).

**Why it is the single most watched metric by a dealer principal**: absorption directly
answers whether the store survives a slow vehicle-sales month — at 100% absorption, every
dollar of new/used/F&I gross becomes pure incremental profit because fixed operations alone
already covers all overhead ([Dynatron — How Do You Calculate Absorption Rate](https://www.dynatronsoftware.com/calculate-absorption-rate-for-dealerships/); [Rework — Service Absorption Rate](https://resources.rework.com/libraries/automotive-sales-growth/service-absorption-rate)). It is explicitly a **management-reporting KPI
computed from departmental gross-profit and overhead figures, not a discrete GL account or
journal entry** ([Journal Entries Hub — Fixed Operations Absorption](https://www.journalentrieshub.com/entries/auto-service-absorption)) — meaning it is calculated *on top of* the same
department/RO/vehicle-cost-object data documented in sections 1–6 above, making it the
natural top-level report the SAP-shape twin should compute from posted department and RO
data rather than store as its own object.

---

## What I could not verify

1. The exact CDK host-side (non-Fortellis) field/table name for the department dimension on
   a raw GL posting line (only the externally exposed Fortellis `Department-Id` header is
   documented publicly).
2. The literal field name CDK uses for "flat rate hours" / "book time" inside the OpCodes
   API schema (only the API's existence is confirmed).
3. Whether CDK Drive posts an explicit intercompany-style elimination entry for internal
   work between departments, or nets the transfer purely through the vehicle inventory
   schedule — no public source documents the GL mechanics at this granularity.
4. The specific GL account/field breakdown (acquisition, pack, recon labor, recon parts,
   floorplan interest) inside the Display Vehicle Cost roll-up.
5. Whether CDK exposes a native "technician efficiency"/"technician proficiency" calculated
   field, or whether these are purely 20-group/DMS-report constructs computed downstream of
   raw clock/flag-hour data.
6. Whether Peterbilt/PACCAR heavy-truck dealers report into NADA's ATD 20 Group composite
   specifically, or a PACCAR-proprietary equivalent — not found in public sources.

## Proposed SAP-shape mapping

| CDK concept | CDK evidence | Proposed SAP object in the twin |
|---|---|---|
| Department (per rooftop, per DMS type) | `Department-Id` header ([Fortellis Get Customer v3](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf)) | Cost centre / Profit centre (KOSTL / PRCTR) — one profit centre per department per site |
| Repair Order (header + pay-type-flagged lines) | `hasCustPayFlag/hasIntPayFlag/hasWarrPayFlag` ([Fortellis Get RO v3](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf)) | Internal Order (AUFK), settlement rule keyed by pay type |
| Pay type (CP/Warranty/Internal codes) | CDK Procede service-type codes ([Leonard Bus reference](https://www.leonardbus.com/wp-content/uploads/2022/03/SERVICE-TYPE-REFERENCE-v3-3-2022.pdf)) | Internal order settlement receiver category (customer A/R, warranty claim account, or WBS/asset) |
| Vehicle stock number (used-vehicle cost roll-up) | Display Vehicle Cost screen ([CDK help doc](https://lithia.vehicle.connectcdk.com/pid1033/help/client/scr-vehcost/veh_ov_display_vehicle_cost.htm)) | WBS element / internal order settling to Material (used-vehicle inventory, MARA/MARC-analogue in the existing parts-twin shape) |
| Warranty/customer/internal receivable schedules | GM warranty account 263/472/672 pattern; Autosoft schedule index ([GM manual](http://gm.acctmanual.com/Fixed_Operations/472_Warranty_Claim_Labor_Body_Shop.htm); [Autosoft Accounting guide](https://download.autosoft-asi.com/instructions/A/Accounting.pdf)) | Three parallel FI-AR sub-ledger accounts / special G/L indicators, one per pay type |
| Department overhead allocation | NCM prorate methods ([NCM Associates](https://ncmassociates.com/about-us/up-to-speed-blog/2018/april/how-to-control-expenses-across-departments)) | CO-OM assessment/distribution cycle from Overhead cost centre to department profit centres |
| Absorption rate | NADA/ATD Slide Guide formula ([atdslideguide.nada.org](https://atdslideguide.nada.org/fixedabsorption)) | Report-only KPI (CO-PA derived report), not a stored object |
| 20-group/ADA composite | NADA 20 Group, ATD Data ([NADA 20 Group](https://www.nada.org/nada/nada-20-group); [ATD Data](https://www.nada.org/atd/research/atd-data)) | External benchmark feed joined to profit-centre actuals, not a native SAP object |
