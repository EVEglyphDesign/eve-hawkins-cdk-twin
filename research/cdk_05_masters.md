# CDK Lane 5 — Master Records (Customer, Vehicle, Employee, Vendor, GL)

Client: EVEglyphDesign digital twin for Peterbilt Atlantic (9-site Peterbilt/PACCAR heavy-truck
dealer group, Atlantic Canada). Public sources only. `DOCUMENTED` = verified from a named CDK/
Fortellis source; `INFERRED (dealer-accounting norm)` = industry-standard inference, not confirmed
in CDK material.

## 1. Customer master

**Primary source:** the Fortellis-published **CDK Drive Get Customer v3** developer guide, base URL
`https://api.fortellis.io/cdk/drive/customer/v3` — `DOCUMENTED` ([CDK Drive Get Customer v3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf)).
A second, older read/write API — **CDK Drive Customers API**, base URL
`https://api.fortellis.io/cdkdrive/crm/v1/customers` — supports search, create, and update
`DOCUMENTED` ([CDK Drive Customers API PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c0e82268-70cc-4d04-92c1-da9934800505/external/20220621170422548-uYfTqXe1.pdf)).

CDK defines a "customer" as an individual in the DMS who has been sold a vehicle, is a sales
prospect, has bought parts, or has had a vehicle serviced through the dealership `DOCUMENTED`
([CDK Drive Get Customer v3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf); [CDK Drive Customer PowerApps connector](https://www.carlosag.net/PowerApps/Connectors/CDK-Drive-Customer)).

### 1.1 Top-level customer attribute table (Get Customer v3)

| Field | Type | Notes |
|---|---|---|
| `customerId` | str | Unique DMS ID — **the customer number key** |
| `hostItemId` | str | Also documented as "the DMS customer ID" |
| `customerName` | obj | Full name or company name |
| `secondaryCustomerName` | obj | Co-buyer / associated customer name |
| `postalAddress` | obj | Address; per-dealer configurable required fields |
| `contactMethods` | obj | Phones, emails, consent/block flags |
| `birthDate` | obj | day/month/year, flagged PII controllable via API Data Management |
| `insurance` | obj | Agency, company, policy sub-objects |
| `overDues` | obj | Aging buckets 30/60/90/120+ days |
| `gender` | enum | `F`/`M` |
| `employer`, `language`, `comment`, `commentDate` | str/date | Free-text/profile fields |
| `dateAdded`, `lastUpdated` | date | Record lifecycle timestamps |
| `partsFlag`, `partsType`, `partsCounterCode` | bool/str | Parts customer classification (`W`=wholesale) |
| `serviceCustomer` | str | `"S"` = service-only, non-AR/Parts customer |
| `mailability`, `nameCode`, `taxCode`, `saleType` | str | Mailing/tax/name-control codes |
| `isDeleteDataFlag`, `deleteDataDate/Time` | bool/date | **CCPA** right-to-delete flag and timestamp |
| `optOutFlag`, `optOutDate/Time` | bool/date | Privacy opt-out (sale/sharing of personal info) |
| `preferredContact` | enum | `C/E/F/H/M/P/W/null` |
| `balances`, `creditLimit`, `currentDue` | f.2 | AR financial fields on the customer record itself |
| `specInstructions` | obj | 5 free-text lines |

Full field-level tables (`birthDate`, `contactMethods`, `customerName`, `insurance`, `overDues`,
`postalAddress`, `secondaryCustomerName`, `specialInstructions` objects) are all `DOCUMENTED` in the
same source ([CDK Drive Get Customer v3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf)).

### 1.2 Business vs. individual customer

Both APIs use the same mutual-exclusivity rule: `DOCUMENTED`

| Customer type | Fields populated | Rule |
|---|---|---|
| Individual | `customerName.firstName` / `lastName` (v3) or `name.first` / `name.last` (v1 CRM) | `lastName` (or `name.last`) required if no company name |
| Business | `customerName.companyName` or `name.companyName` | Populate only this; do not populate first/last name at the same time |

Source: [CDK Drive Get Customer v3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf); [CDK Drive Customers API PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c0e82268-70cc-4d04-92c1-da9934800505/external/20220621170422548-uYfTqXe1.pdf).

### 1.3 Phone / email / consent flags

`DOCUMENTED` in `contactMethods`: `primaryPhone`, `homePhone`, `mobilePhone`, `businessPhone` (+ext),
`homeFax`, `workFax`, `pager` (+access code), `secondaryHomePhone`, up to 6 `email` addresses each
with a `HOME/WORK/OTHER` descriptor (or `NA`/`CD` = declined), `preferredMethod`, `preferredDay`,
`preferredTime`, `textMessagePhone`/`textMessageCarrier`, and three **advertising block flags**:
`blockEmailFlag`, `blockMailFlag`, `blockPhoneFlag` (all boolean, default `false`) — these are the
closest documented analog to a consent/opt-out flag set, alongside the customer-level `optOutFlag`
(sale/sharing of personal data) and `isDeleteDataFlag` (CCPA deletion request) ([CDK Drive Get Customer v3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf)).

### 1.4 Customer number key and duplicates

`customerId` (aka `hostItemId`) is the DMS-assigned unique key; the older CRM v1 API exposes it as
the path parameter for `GET /{custId}` and `POST /{custId}` `DOCUMENTED` ([CDK Drive Customers API PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c0e82268-70cc-4d04-92c1-da9934800505/external/20220621170422548-uYfTqXe1.pdf)).

**Duplicate customer records** are widely described as the chronic DMS data-quality problem.
Dealer-facing guidance identifies the main causes as front-line staff (cashiers, credit-bureau
lookups, F&I) creating a new customer number instead of searching for an existing one, and
recommends merge rules keyed on which record has the more recent sale/service activity or an
active assigned salesperson, with the DMS merge routine consolidating deal, repair-order, and
parts-ticket history onto the surviving `customerId` `INFERRED (dealer-accounting norm)` ([Digital Dealer, "Duplicate Customers – Cleaning your Customer Database"](https://digitaldealer.com/news/duplicate-customers-cleaning-your-customer-database/46962/)).
In practice, dedup normally keys on a composite of **last name + phone number + postal
address/ZIP**, and secondarily on **email**, since VIN/deal history is attached only after the
duplicate already exists — CDK Drive itself does not document an automated fuzzy-match dedup
API; merge is a DMS screen-driven manual/semi-automated action `INFERRED (dealer-accounting norm)`.

## 2. Vehicle master

Two related but distinct CDK objects: **CDK Drive Service Vehicles** (service/ownership-facing
vehicle record, base path under `cdkdrive/servicevehicles`, Fortellis spec `54b70ee1-ac17-4be2-9314-45c947692c5d`)
and the inventory-side **vehicle inventory record** used in stock/AUN screens — these are not the
same object `DOCUMENTED` ([CDK Drive Service Vehicles — Microsoft Learn connector doc](https://learn.microsoft.com/en-us/connectors/cdkdriveservicevehicles/); [Fortellis Repair Orders API Developer Guide](https://prod-fortellis-provider-api-reference-documents.s3-us-west-2.amazonaws.com/c7771500-1c95-4f8e-9241-eddc17cd55f6)).

### 2.1 Service Vehicles API — documented fields

| Field | Notes |
|---|---|
| `vehicleId` | DMS vehicle record identifier |
| `identification.vin` | VIN — "at least one of the identification properties must be defined" |
| `identification.licensePlateNum` | License plate |
| `specification.makeCode`/`make`/`modelCode`/`model`/`modelYear` | Spec block |
| `exteriorColor` | — |
| `mileage.value`/`mileage.units` | Measurement object |
| `status` | "Is the status of the vehicle new, used, or certified?" |
| `dates.delivered`/`dates.inService`/`dates.warrantyExpiration` | Lifecycle dates |
| `ownerHref`, `primaryDriverHref` | Hyperlinks to the customer resource — **this is how a vehicle links to a customer master record**, not an embedded customer object |

Source: [CDK Drive Service Vehicles — Microsoft Learn connector doc](https://learn.microsoft.com/en-us/connectors/cdkdriveservicevehicles/). **Stock number is explicitly not present in this
API's documented schema** — confirmed absent on the same page.

### 2.2 VIN vs. stock number

VIN is the natural, universal key (17-character, cross-system). **Stock number** is a
dealer/inventory-scoped identifier assigned at intake and configurable per Location/Inventory
Type/Acquired Type via the "Stock Number Definition" screen, and can be changed independently of
VIN (e.g., after a used-to-wholesale reclass) `DOCUMENTED` ([Lithia connectCDK — Vehicle Inventory Setups, Stock Number Definition](https://lithia.vehicle.connectcdk.com/pid1033/help/client/scr-vehsetups-inventory/veh_ov_vehicle_inventory_setups_-_stock_number_definition.htm); [Lithia connectCDK — Changing a Vehicle's Stock Number](https://lithia.vehicle.connectcdk.com/pid1033/help/client/scr-vehinventory/tasks/veh_tk_changing_a_vehicle_s_stock_number.htm)).
Vehicle search screens accept partial VIN or partial stock number `DOCUMENTED` ([Lithia connectCDK — Quickly Search for Vehicles](https://lithia.vehicle.connectcdk.com/pid1033/help/client/scr-vehinquiry/tasks/veh_tk_quick_search_for_vehicles.htm)).
Third-party integration guidance shows the AUN (add-unit) workflow requiring Stock Number,
Inventory Type (new/used/demo), and VIN, then a separate step ("F8–VEH") to push the vehicle into
the service-domain vehicle record — direct evidence that **inventory record and service/customer-
owned vehicle record are separate objects that must be explicitly linked** `DOCUMENTED` ([Intercom/deskit — Inventory Process, DMS: CDK](https://intercom.help/dealercorp-59050c60031b/en/articles/4565345-deskit-inventory-process-dms-cdk)).

### 2.3 New / used / wholesale status

`status` on the Service Vehicles schema is limited to "new, used, or certified" `DOCUMENTED`
([CDK Drive Service Vehicles connector doc](https://learn.microsoft.com/en-us/connectors/cdkdriveservicevehicles/)). Wholesale is documented at the *customer* level instead —
`partsType = "W"` denotes a wholesale **parts** customer on the Get Customer v3 schema, and
"acquired type" (a distinct inventory-setup dimension alongside inventory type) is the
documented lever used to range stock numbers for wholesale-acquired units `DOCUMENTED` ([CDK Drive Get Customer v3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf); [Lithia connectCDK Stock Number Definition](https://lithia.vehicle.connectcdk.com/pid1033/help/client/scr-vehsetups-inventory/veh_ov_vehicle_inventory_setups_-_stock_number_definition.htm)). A distinct "wholesale vehicle inventory status" field name is
`UNVERIFIED`.

### 2.4 Service history attachment to a VIN

The **Get Repair Order v3** API embeds a `vehicle` object on every repair order
(`vehicle.vin`, `vehicle.vehId`, make/model/year, color, license, lot location), confirming
service (repair order) history is attached to the vehicle record via VIN/`vehId`, alongside the
`customer` object on the same RO (`customer.customerId`, name, address, phones, emails)
`DOCUMENTED` ([CDK Drive Get Repair Order v3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf)).

### 2.5 Heavy trucks vs. light vehicles

CDK operates a distinct **Heavy Truck DMS** product line (separate site, `cdkglobalheavytruck.com`)
for Peterbilt/Kenworth/International/Mack-Volvo/Isuzu dealers, with named OEM integrations, implying
a materially different data model from light-vehicle CDK Drive, though CDK does not publicly
document heavy-truck-specific field names for chassis/unit number, body builder, or spec
configuration in any source found `DOCUMENTED` (existence of separate product) / `UNVERIFIED`
(field-level schema) ([CDK Global Heavy Truck — Heavy Truck DMS](https://www.cdkglobalheavytruck.com/heavy-truck-dms); [CDK Global Heavy Truck — OEM & ISV Integrations](https://www.cdkglobalheavytruck.com/oem-integrations)).
Industry norm for heavy-truck DMS/OEM systems (not confirmed as CDK screen/field names) is that a
**chassis number** (the OEM VIN of the incoming cab-chassis) is tracked separately from a dealer-
assigned **unit number**, and a **body builder** record captures the upfitter and the completed
spec configuration once the chassis leaves the factory incomplete — this is standard body-builder-
manual practice across truck OEMs, not a CDK-specific artifact `INFERRED (dealer-accounting norm)`
([Volvo Trucks — Body Builder Manuals](https://www.volvotrucks.us/parts-and-services/services/body-builder-support/manuals/)).

## 3. Employee master

CDK has publicly announced (not detailed field-by-field in a public developer guide found) a
**"CDK Get Employee"** extract API on Fortellis, alongside CDK Get Customer, Get Repair Order,
Get F&I Sales, Get Part Sales, Get Service Appointment, Get Op Code Lite, and Get Make Model Lite
— confirmed by a CDK/Fortellis-affiliated LinkedIn announcement naming the real published API set
`DOCUMENTED` (existence/name) / `UNVERIFIED` (full field schema) ([LinkedIn — Ankit R., CDK Fortellis extract APIs announcement](https://www.linkedin.com/posts/ankitraheja_apis-data-automotivecommerce-activity-7053939674595155968-KyYH)).

Employee/technician identifiers **do** surface, field-by-field, inside the Get Repair Order v3
schema, which is the best-documented view into how CDK represents "who did what" on a transaction:

| Field | Meaning |
|---|---|
| `serviceAdvisor` (int) | Service advisor number on the RO header |
| `cashier` (str) | DMS employee ID of the cashier who closed the RO |
| `bookerNo` (int) | Employee number of the booker who posted labor |
| `line.storyEmployeeNo` | Employee who last updated the technician's story/notes |
| `line.laborOperations[].technicianIds[]` | Technician(s) assigned to a labor line (`"MULT"` if more than one) |
| `line.laborOperations[].comebackSA` / `comebackTech` | SA/technician numbers from the original RO for a comeback repair |
| `line.laborOperations[].hours[].technicianId` | Technician on a specific hours split |
| `line.laborOperations[].parts[].employeeId` | Parts counter person who sold the part |
| `line.laborOperations[].parts[].outsideSalesmanId` | Outside salesperson assigned to the customer |
| `technicianPunchTimes[].technicianId` | Technician clock-punch records, with `workType` code |
| `discounts[].userID`/`appliedBy` | Employee who applied a discount |

Source: [CDK Drive Get Repair Order v3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf). This confirms that CDK Drive answers "who sold it / who
wrote it / who turned the wrench" via **numeric employee IDs embedded directly on transaction
records** rather than by joining a public employee-master API — no separate documented
"employee master" schema was found in any public source. A separate **CDKDrive Repair Orders v1**
guide documents dedicated lookup endpoints — `Query technicians` / `Query a technician`
(`technicianId`), `Query service advisors` / `Query a service advisor` (`serviceAdvisorId`) — as
distinct from the customer/vehicle lookups `DOCUMENTED` ([CDKDrive Repair Orders v1 API Developer Guide](https://prod-fortellis-provider-api-reference-documents.s3-us-west-2.amazonaws.com/c7771500-1c95-4f8e-9241-eddc17cd55f6)).

**Pay plans and payroll integration** are documented only at the product-marketing level: CDK
sells a **"Payroll Plus"** module `DOCUMENTED` ([CDK Global — Payroll Plus](https://www.cdkglobal.com/dealership-operations/operations/payroll)), and third-party commission
platforms integrate against CDK Drive report outputs (Advisor Daily Sales Summary, Tech
Performance Report, RTH — technician hours report, PDA report) to compute pay-plan-driven
commission, rather than against a documented "employee master" API field set `DOCUMENTED`
([Nimble Compensation — CDK Drive DMS integration](https://www.nimblecompensation.com/how-we-help/dms-integrations/cdk-drive)). Dealer/technician forum discussion confirms operationally that technician numbers,
labor rates (C/W/I), and flat-rate costing live in DMS functions `TSS`/`RTH`/`ULT`, gated by
manager-level access, separate from advisor-visible reports — screen/function names as used by
practitioners, not vendor-published documentation `DOCUMENTED` (screen names exist) but sourced
from a forum, so treat function-level detail as lower confidence ([Reddit r/serviceadvisors — CDK tech number / labor rate discussion](https://www.reddit.com/r/serviceadvisors/comments/1fas1r1/cdk_help/)).
An ADP payroll interface exists (`Earnings and Deductions Quick Reference` for CDK) confirming a
real payroll-export integration path `DOCUMENTED` ([ADP — CDK Earnings and Deductions Quick Reference](https://support.adp.com/adp_payroll/content/hybrid/EDQR/EDQR_CDK.pdf)).

## 4. Vendor / supplier master

No public Fortellis developer guide for a vendor/AP master API was found. CDK's own marketing
page for **Accounting Workflows** confirms a "new Vendor workflow" exists in-DMS ("provides an
updated ability to view and edit vendor information quickly and easily") but does not publish
field names, and states dealer training/documentation is "coming soon" `DOCUMENTED` (existence,
no schema) ([CDK Global — Accounting Workflows](https://www2.cdkglobal.com/accounting-workflows)). CDK Heavy Truck's OEM integrations page separately confirms a
**Corpay** integration "to simplify vendor payments and boost AP efficiency," which is direct
evidence of an AP vendor record integrating to an external payment processor `DOCUMENTED`
([CDK Global Heavy Truck — OEM & ISV Integrations](https://www.cdkglobalheavytruck.com/oem-integrations)). Multiple independent AP-automation vendors (OnPhase, CloudX, Repay/REPAY) advertise
integration to "CDK" vendor/invoice data, confirming a vendor master object exists and is
externally addressable via ISV partnership, but none publish the CDK vendor field schema publicly
`DOCUMENTED` (existence) / `UNVERIFIED` (field names) ([OnPhase — AP & Payments Automation for CDK Dealerships](https://www.onphase.com/partners/cdk); [CloudX — AP Automation for CDK Global](https://www.cloudxdpo.com/integrations/automotive/cdk-global)).

**OEM as a vendor** and **sublet vendors** (outside repair shops used for warranty/sublet labor) are
standard dealer-accounting concepts — OEM parts/warranty payables and sublet payables both post
through the same AP vendor master by convention — but CDK does not publicly document a field or
flag that classifies a vendor record as "OEM" vs. "sublet" vs. general trade payable
`INFERRED (dealer-accounting norm)`.

## 5. Account / GL master (structure only)

CDK Drive's GL is described only at a marketing/workflow level, not schema level: "General
Ledger Inquiry Workflow," "Create Journal Entries" workflow, and "General Ledger Adjustments and
Reversals Workflow," each stated to maintain "a clear audit trail for compliance and
accountability" `DOCUMENTED` ([CDK Global — Accounting Workflows](https://www2.cdkglobal.com/accounting-workflows)). Vehicle inventory setup screens reference an
"Account Mapping" function that interfaces to "the Accounting subsystem to retrieve GL codes,
journals and chart of accounts," confirming a **chart-of-accounts / GL-code master exists and is
distinct from the inventory account-mapping template**, but no field-level GL master schema (account
number format, account type, natural-account vs. cost-center split) is publicly documented
`DOCUMENTED` (existence) / `UNVERIFIED` (schema) ([Lithia connectCDK — Vehicle Inventory Setups, Account Mapping](https://lithia.vehicle.connectcdk.com/pid1033/help/client/scr-vehsetups-inventory/old_veh_ov_vehicle_inventory_setups_-_account_mapping.htm)). Third-party audit-analytics
vendor MindBridge documents extracting the CDK "AGMT" function's general-ledger export via
`Transfer` to produce audit data files by company number — confirming a **company number**
dimension exists above the account number, consistent with multi-rooftop GL segregation
`DOCUMENTED` ([MindBridge — CDK ERP: Export the general ledger](https://support.mindbridge.ai/hc/en-us/articles/360058269153-CDK-ERP-Export-the-general-ledger)).

## 6. Cross-cutting: how CDK keys these records across a 9-rooftop tenant

- **Customer key:** `customerId`/`hostItemId` — `DOCUMENTED` as unique "assigned to the customer,"
  with no published statement that it is globally unique across a multi-store tenant; Fortellis
  bulk/delta customer retrieval is scoped by **Subscription ID** and **Department ID**, and a
  single Fortellis org can hold multiple `orgName`/subscription entries — one per dealership/
  department — implying customer numbering is **store- or department-scoped**, not tenant-global,
  unless the dealer group runs a single shared DMS company `DOCUMENTED` (subscription/department
  scoping mechanism) / `INFERRED (dealer-accounting norm)` (customer number uniqueness scope)
  ([BettrData — Fortellis CDK Drive API integration guide](https://docs.bettrdata.io/user-docs/how-to-guides/fortellis-cdk-drive-api)).
- **Vehicle key:** VIN is globally unique by definition (17-char, OEM-issued); `vehicleId`/`vehId`
  is a DMS-internal identifier layered on top, and stock number is explicitly store/location-
  scoped via the Stock Number Definition screen (ranges configured per Location) `DOCUMENTED`
  ([Lithia connectCDK — Stock Number Definition](https://lithia.vehicle.connectcdk.com/pid1033/help/client/scr-vehsetups-inventory/veh_ov_vehicle_inventory_setups_-_stock_number_definition.htm)).
- **Employee/technician key:** technician/service-advisor numbers are queried via dedicated
  lookup endpoints scoped to the API subscription context; forum evidence shows tech numbers
  looked up per-store report run (`RTH`), consistent with **store-scoped** numbering
  `DOCUMENTED` (lookup mechanism) / `INFERRED (dealer-accounting norm)` (uniqueness scope)
  ([CDKDrive Repair Orders v1 API Developer Guide](https://prod-fortellis-provider-api-reference-documents.s3-us-west-2.amazonaws.com/c7771500-1c95-4f8e-9241-eddc17cd55f6); [Reddit r/serviceadvisors — CDK tech number discussion](https://www.reddit.com/r/serviceadvisors/comments/1fas1r1/cdk_help/)).
- **GL key:** the MindBridge extract confirms a **company number** groups GL data per legal
  entity/rooftop, meaning a 9-rooftop group either runs 9 company numbers under one CDK
  environment or consolidates through a group chart of accounts — CDK does not publicly document
  which pattern Peterbilt Atlantic-scale groups use `DOCUMENTED` (company-number dimension exists)
  / `UNVERIFIED` (multi-rooftop consolidation pattern) ([MindBridge — CDK ERP: Export the general ledger](https://support.mindbridge.ai/hc/en-us/articles/360058269153-CDK-ERP-Export-the-general-ledger)).
- **What changes at 9 rooftops in one tenant:** every one of the above keys (customer, stock
  number, technician number, company number) is evidence-consistent with **per-store or
  per-department scoping**, not per-tenant. A 9-site group therefore likely has 9 parallel
  customer number spaces (risk: the same real-world customer gets 9 different `customerId`
  values, one per rooftop they've transacted with — a materially worse version of the standard
  duplicate-customer problem), 9 stock-number ranges, and department-scoped Fortellis
  Subscription/Department IDs to manage per integration `INFERRED (dealer-accounting norm)`.

## 7. Publicly documented Fortellis master-data APIs, by real name

| Published API name | Domain | Read-only or read/write | Source |
|---|---|---|---|
| **CDK Drive Get Customer** (v3; also seen as v1/v2) | Customer | Read-only (bulk/delta extract) | `DOCUMENTED` ([Get Customer v3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf)) |
| **CDK Drive Customers API** (CRM v1, `cdkdrive/crm/v1/customers`) | Customer | Read/write — search, create, update | `DOCUMENTED` ([Customers API PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c0e82268-70cc-4d04-92c1-da9934800505/external/20220621170422548-uYfTqXe1.pdf)) |
| **CDKDrive Customer API V1** (Microsoft connector name) | Customer | Read/write | `DOCUMENTED` ([Microsoft Learn — CDK Drive Customer](https://learn.microsoft.com/en-us/connectors/cdkdrivecustomer/)) |
| **CDK Drive Service Vehicles** | Vehicle | Read/write — create, update, query | `DOCUMENTED` ([Microsoft Learn — CDK Drive Service Vehicles](https://learn.microsoft.com/en-us/connectors/cdkdriveservicevehicles/)) |
| **Vehicle Specifications API** | Vehicle | Read-only — retrieve by VIN/SpecId/make/model | `DOCUMENTED` ([Fortellis App Listing Guide](https://community.fortellis.io/sites/default/files/Fortellis_App.Listing.Guide_.pdf)) |
| **CDK Get Employee** | Employee | Extract API — read-only (bulk/delta pattern consistent with sibling "Get" APIs) | `DOCUMENTED` (name only) ([LinkedIn — CDK Fortellis extract APIs announcement](https://www.linkedin.com/posts/ankitraheja_apis-data-automotivecommerce-activity-7053939674595155968-KyYH)) |
| **CDK Drive Workshop Management API** | Employee (advisor/tech reference data) | Read-only — query dispatch code, dispatch make code, labor type, service advisor, technician | `DOCUMENTED` ([Fortellis App Listing Guide](https://community.fortellis.io/sites/default/files/Fortellis_App.Listing.Guide_.pdf)) |
| **CDKDrive Repair Orders V1 / CDK Drive Repair Order V2** | Transaction (references employee IDs) | Read/write | `DOCUMENTED` ([Repair Orders v1 Developer Guide](https://prod-fortellis-provider-api-reference-documents.s3-us-west-2.amazonaws.com/c7771500-1c95-4f8e-9241-eddc17cd55f6); [Fortellis — CDK Repair Order Access Just Got Better](https://fortellis.io/blog/cdk-repair-order-access-just-got-better)) |
| **Elead Product Reference Data API** | Employee (CRM-side reference) | Read-only — "provides details on opportunity, employee and vehicle data" | `DOCUMENTED` ([BusinessWire — CDK Global Launches Advanced CRM Data Capabilities](https://www.businesswire.com/news/home/20210209005197/en/CDK-Global-Launches-Advanced-CRM-Data-Capabilities-with-Four-New-Elead-APIs)) |
| **Elead Sales Customer API** | Customer (CRM-side) | Read/write — "management of prospect and customer data," includes Elead customer ID | `DOCUMENTED` ([BusinessWire, same](https://www.businesswire.com/news/home/20210209005197/en/CDK-Global-Launches-Advanced-CRM-Data-Capabilities-with-Four-New-Elead-APIs)) |

No publicly documented Fortellis **vendor/AP master** API or **GL account master** API by name was
found in any public source. `UNVERIFIED` — treat as a gap.

## 8. CASL and the customer master (Canada)

Canada's Anti-Spam Legislation (CASL) is enforced by the CRTC. Two consent bases apply to any
commercial electronic message (CEM) — email, SMS — sent by the dealership: `DOCUMENTED`
([Canada.ca / CRTC — Enforcement Advisory on record-keeping for consent](https://www.canada.ca/en/radio-television-telecommunications/news/2016/07/enforcement-advisory-notice-for-businesses-and-individuals-on-how-to-keep-records-of-consent.html)).

- **Express consent** — an explicit opt-in (written or oral); does not expire until withdrawn, but
  the sender must be able to prove it.
- **Implied consent** — arises from an existing business relationship (time-limited, commonly
  cited as up to 2 years from the last transaction) or an inquiry (shorter window); it lapses and
  must be renewed or converted to express consent.
- **Burden of proof is always on the sender.** The CRTC's guidance is explicit: "the onus is on
  the person who alleges they have consent... to prove that they have proper consent, either
  implied or express, to send each message," and recommends dealerships retain a hard-copy or
  electronic record of all consent evidence (signed forms, call recordings, web-form logs),
  the method used to collect it, CASL compliance policies, and all unsubscribe requests and the
  resulting actions taken `DOCUMENTED` ([Canada.ca / CRTC Enforcement Advisory](https://www.canada.ca/en/radio-television-telecommunications/news/2016/07/enforcement-advisory-notice-for-businesses-and-individuals-on-how-to-keep-records-of-consent.html)).

**Constraint on the customer master:** CASL requires the customer master to hold, at minimum, a
timestamped consent record per contact channel (not just a single yes/no flag), the **source/date
of consent or the qualifying transaction date** that started an implied-consent clock, and an
audit trail of opt-out/unsubscribe events. CDK Drive's documented `contactMethods` block only
exposes static boolean block flags (`blockEmailFlag`, `blockMailFlag`, `blockPhoneFlag`) and does
not document a consent-timestamp, consent-source, or consent-expiry field — meaning, on the
public schema alone, CDK Drive's customer master **does not appear to natively store what CASL
record-keeping requires**, and a dealership operating in Canada would need a supplementary consent
log (CRM add-on, marketing platform, or manual store of record) layered on top of the DMS block
flags `DOCUMENTED` (CDK schema gap, by omission) + `INFERRED (dealer-accounting norm)` (compliance
consequence). This is a direct field-for-field mismatch the digital twin must flag: `optOutFlag`
and the `block*Flag` fields answer "may we contact them," but not "when/how did we get permission,"
which is what CASL record-keeping demands.

## What I could not verify

- Full field schema for the "CDK Get Employee" Fortellis API (name confirmed via a LinkedIn
  announcement only; no public developer-guide PDF located).
- Any public field-level vendor/AP master schema (vendor number format, 1099/GST-HST fields,
  remit-to address structure).
- Any public field-level GL account master schema (account number length/segmentation, account
  type codes, cost-center or store-segment structure).
- Whether `customerId` is unique per Drive "company number" (rooftop) or can be shared/synced
  across rooftops in a single Fortellis tenant/subscription — not stated in any source found.
- CDK Heavy Truck-specific field names for chassis number, unit number, or body-builder/spec
  configuration records — the product line's existence is documented, its schema is not.
- Whether CDK Drive has a documented automated/fuzzy-match customer deduplication tool (vs.
  manual merge screens) — no public source confirms or denies this.
- Whether CDK Drive's Get Customer v3 `optOutFlag`/`isDeleteDataFlag` fields are also used
  operationally for CASL compliance in Canadian dealerships, or whether Canadian CDK dealers rely
  entirely on external CRM/consent-management layers — not stated in any CDK source (only CCPA,
  a US statute, is named in the schema).

## Proposed SAP-shape mapping

| CDK Drive concept | Proposed SAP-shape object | Rationale |
|---|---|---|
| Customer master (`customerId`, name, address, contact) | **KNA1** (general customer master) + **KNVV**-style store-scoping if per-rooftop | KNA1 is SAP's central customer-independent-of-sales-org table; per-store scoping mirrors KNVV's sales-org dependency |
| `contactMethods` block flags / consent | **KNA1**-adjacent Z-table `ZCASL_CONSENT` (custom) | No native SAP consent-timestamp field maps cleanly; needs a bolt-on table capturing channel, timestamp, source, expiry |
| Business vs. individual flag | KNA1 `KTOKD` (customer account group) analog | Distinguishes company vs. person accounts the way CDK's `companyName` vs. `firstName/lastName` mutual exclusivity does |
| Vehicle inventory record (stock #, new/used, lot) | **MARA/MARC**-style material master record (serialized), keyed by VIN as the SAP **equipment number (EQUI)** | Matches existing parts-lane MM shape; VIN plays the role of an SAP serial/equipment master, stock number plays the role of a plant-specific MARC extension |
| Customer-owned vehicle (service side) | **EQUI** (equipment master) linked to KNA1 via install-base/functional-location tables | SAP's standard pattern for "who owns/uses this serialized asset" |
| Employee/technician/advisor identifiers on transactions | HR-adjacent Z-fields on transaction tables (no MM equivalent) | Parts-lane precedent (MATDOC) already carries user/employee stamps; extend the same pattern to RO/labor tables |
| Vendor/AP master | **LFA1** (vendor master, general data) | Direct SAP analog; OEM and sublet vendors become account-group-differentiated LFA1 records |
| GL account master | **SKA1/SKB1** (chart-of-accounts and company-code GL master) | Matches CDK's undocumented but confirmed company-number + chart-of-accounts structure |
| Multi-rooftop company number | SAP **company code (BUKRS)**, one per rooftop | Matches MindBridge's confirmed per-company-number GL export pattern for 9-site consolidation |
