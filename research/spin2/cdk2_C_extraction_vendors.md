# Lane C — Extraction Vendor Catalogues

Peterbilt Atlantic digital-twin project. Primary-source retrieval only. Field names quoted
verbatim as spelled by the source. Confidence tags on every claim: `[DOC]` vendor/regulator
document (URL required), `[COMM]` practitioner/forum/training statement (URL + speaker if
possible), `[INF]` reasoned inference (source of the inference stated), `[UNK]` searched,
not found (queries stated).

---

## 1. What I actually retrieved

**Downloaded to `/home/user/workspace/cdk2_raw/C/`:**

| File | Source URL | Pages | Status |
|---|---|---|---|
| `CDK_Drive_Get_Customer_v3.pdf` | https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf | 28 | Fully read, all objects transcribed |
| `CDK_Drive_Customers_API.pdf` | https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c0e82268-70cc-4d04-92c1-da9934800505/external/20220621170422548-uYfTqXe1.pdf | 22 | Pages 1–10 read (Attribute Table, API summary); remainder is workflow examples |
| `CDK_Modern_APIs_Migration_Guide.pdf` | https://community.fortellis.io/sites/default/files/CDK_Modern.APIs_Migration.Guide_04.14.2023.pdf | 8 | Pages 1–5 read (process/milestones only, no field data) |
| `CDK_Set_Up_Form_2021.pdf` | (downloaded, see prior session) | — | Not re-opened this pass |
| `Cox_Automotive_DMS_Integration_Terms.pdf` | (downloaded, see prior session) | — | Not re-opened this pass |
| `DealerVault_Dealer_Portal_Guide.pdf` | (downloaded, see prior session) | — | Not re-opened this pass |
| `Fortellis_APP_Launch_Guide.pdf` | (downloaded, see prior session) | — | Not re-opened this pass |
| `SXM_DMS_Tip_Sheet_DealerVault.pdf` | (downloaded, see prior session) | — | Not re-opened this pass |
| `NADA_ATD_SlideGuide_2026.pdf` | (downloaded, see prior session) | — | ATD ratio/formula guide only, not a field/COA spec |
| `NIADA_Financial_Statement_Autosoft.pdf` | (downloaded, see prior session) | — | Wrong association (NIADA, independent dealers) — corroborating, not on-target |

**Specs opened directly (public web pages, not downloaded as files — Karmak's developer portal
is HTML, not PDF):**

- https://unity.karmak.io/APIs.html — full transactional API index
- https://unity.karmak.io/ReportDataAccess.html — full Report Data Access object catalog
- https://unity.karmak.io/Customer — full Customer object field table + sample JSON payloads
- https://unity.karmak.io/Repair-Order-Header.html — full Repair Order Header field table
- https://unity.karmak.io/Repair-Order.html — full Repair Order Detail field table
- https://unity.karmak.io/Service — full Service Deferred Repairs, Service Unit Meter History,
  Service Open Barcode Time, Service Preventive Maintenance, Service Repair Order Quote Detail,
  Service Repair Order Quote Header field tables
- https://portal.karmak.io/documentation — new APIM portal nav page (section names only: APIs,
  RDA, Docs, Change Log, Products, Reports — no additional field content beyond the above)
- https://clarivoy.helpjuice.com/en_US/cdk-setting-up-dms-sales-reports — third-party (Clarivoy)
  description of CDK Drive's own Enhanced Report Generator screen path and Dictionary Library
  field names
- https://www.scribd.com/document/809504766/DMS-Cheat-Sheet-6-20-2023 — integrator-authored
  cheat sheet naming "ADP/CDK 3PA 'CDK Drive'" alongside Dominion, Reynolds, Procede, etc., as
  named DMS integration categories (no field-level schema)
- https://lvlupauto.com/integrations/dominion-dms — Dominion DMS partner-integration directory
  (25 named third-party products, direction/method only, no field schemas)
- https://onsite-support.lightspeedhq.com/hc/en-us/articles/360042921414-Migration-process-overview
  — Lightspeed Retail/OnSite (POS company) migration doc — **confirmed wrong vendor, see §5**

---

## 2. The field/table/record dictionary

### 2a. Karmak Unity (Fusion DMS) — Customer object

Karmak is heavy-truck-specific (Class 6–8), OEM-integrated with PACCAR/Peterbilt/Kenworth,
DTNA, Mack/Volvo, International — the same functional domain as Peterbilt Atlantic. This is
Karmak documenting **its own internal schema**, not CDK's.

**Endpoints** — `[DOC]`, https://unity.karmak.io/Customer:
> "POST/PUT https://api.karmak.io/api/unity/{version}/unityapi/customer" ; "GET
> https://api.karmak.io/api/unity/v1/unityapi/customer/{customerId}" (v1 as of June 30, 2019)

| Field name (as spelled) | Type / Length / Required (as stated) | Meaning as stated by source | Tag | URL |
|---|---|---|---|---|
| CustomerID | per source table | Customer identifier | [DOC] | https://unity.karmak.io/Customer |
| CustomerBaseBranchCode | per source table | Customer's base branch code | [DOC] | https://unity.karmak.io/Customer |
| CustomerKey | per source table | Internal customer key | [DOC] | https://unity.karmak.io/Customer |
| NewCustomerBaseBranch | per source table | New customer base branch (used on create) | [DOC] | https://unity.karmak.io/Customer |
| NewCustomerKey | per source table | New customer key (used on create) | [DOC] | https://unity.karmak.io/Customer |
| CompanyName | per source table | Customer company name | [DOC] | https://unity.karmak.io/Customer |
| ControlBranchCode | per source table | Control branch code | [DOC] | https://unity.karmak.io/Customer |
| CustomerInactive | per source table | Inactive flag | [DOC] | https://unity.karmak.io/Customer |
| Salutation | per source table | Salutation | [DOC] | https://unity.karmak.io/Customer |
| FirstName | per source table | First name | [DOC] | https://unity.karmak.io/Customer |
| MI | per source table | Middle initial | [DOC] | https://unity.karmak.io/Customer |
| LastName | per source table | Last name | [DOC] | https://unity.karmak.io/Customer |
| Title | per source table | Title | [DOC] | https://unity.karmak.io/Customer |
| IsInternal | per source table | Internal-customer flag | [DOC] | https://unity.karmak.io/Customer |
| IsWarranty | per source table | Warranty-customer flag | [DOC] | https://unity.karmak.io/Customer |
| IsInternalLeaseRentalCustomer | per source table | Internal lease/rental customer flag | [DOC] | https://unity.karmak.io/Customer |
| IsMiscCashCustomer | per source table | Misc cash customer flag | [DOC] | https://unity.karmak.io/Customer |
| IsProspect | per source table | Prospect flag | [DOC] | https://unity.karmak.io/Customer |
| IndustryType | per source table | Industry type | [DOC] | https://unity.karmak.io/Customer |
| AccountType | per source table | Account type | [DOC] | https://unity.karmak.io/Customer |
| BusinessStructure | per source table | Business structure | [DOC] | https://unity.karmak.io/Customer |
| BusinessTaxNumber | per source table | Business tax number | [DOC] | https://unity.karmak.io/Customer |
| CanadianTaxID | per source table | Canadian tax ID | [DOC] | https://unity.karmak.io/Customer |
| QuebecTaxID | per source table | Quebec tax ID | [DOC] | https://unity.karmak.io/Customer |
| CurrencyCode | per source table | Currency code | [DOC] | https://unity.karmak.io/Customer |
| ShopPhone | per source table | Shop phone | [DOC] | https://unity.karmak.io/Customer |
| OfficePhone | per source table | Office phone | [DOC] | https://unity.karmak.io/Customer |
| CellPhone | per source table | Cell phone | [DOC] | https://unity.karmak.io/Customer |
| Fax | per source table | Fax number | [DOC] | https://unity.karmak.io/Customer |
| InvoiceEmail | per source table | Invoice email | [DOC] | https://unity.karmak.io/Customer |
| IsInvoiceEmailAllowed | per source table | Invoice-email-allowed flag | [DOC] | https://unity.karmak.io/Customer |
| StatementEmail | per source table | Statement email | [DOC] | https://unity.karmak.io/Customer |
| IsStatementEmailAllowed | per source table | Statement-email-allowed flag | [DOC] | https://unity.karmak.io/Customer |
| AlertEmail | per source table | Alert email | [DOC] | https://unity.karmak.io/Customer |
| IsAlertEmailAllowed | per source table | Alert-email-allowed flag | [DOC] | https://unity.karmak.io/Customer |
| BillToAddress (object: AddressType, Address1, Address2, City, Region, PostalCode, Country, TaxBody) | object | Bill-to address block | [DOC] | https://unity.karmak.io/Customer |
| ShipToAddress (object: same sub-fields as BillToAddress) | object | Ship-to address block | [DOC] | https://unity.karmak.io/Customer |
| OutsidePartsSalesperson | per source table | Outside parts salesperson | [DOC] | https://unity.karmak.io/Customer |
| OutsideServiceSalesperson | per source table | Outside service salesperson | [DOC] | https://unity.karmak.io/Customer |
| LaborAccountingCode | per source table | Labor accounting code | [DOC] | https://unity.karmak.io/Customer |
| PartsAccountingCode | per source table | Parts accounting code | [DOC] | https://unity.karmak.io/Customer |
| CustomerPriceType | per source table | Customer price type | [DOC] | https://unity.karmak.io/Customer |
| AccountStatus | per source table | Account status | [DOC] | https://unity.karmak.io/Customer |
| PaymentTerm | per source table | Payment term | [DOC] | https://unity.karmak.io/Customer |
| CreditLimit | per source table | Credit limit | [DOC] | https://unity.karmak.io/Customer |
| DefaultPaymentMethod | per source table | Default payment method | [DOC] | https://unity.karmak.io/Customer |
| PaymentMethod_Cash / _COD / _Charge / _Check / _CreditCard | per source table | Payment method flags | [DOC] | https://unity.karmak.io/Customer |
| IsCustomerPORequired | per source table | Customer PO required flag | [DOC] | https://unity.karmak.io/Customer |
| IsLPORequired | per source table | Local PO required flag | [DOC] | https://unity.karmak.io/Customer |
| ParentCustomer | per source table | Parent customer link | [DOC] | https://unity.karmak.io/Customer |
| UseParentCreditLimit | per source table | Use-parent-credit-limit flag | [DOC] | https://unity.karmak.io/Customer |
| SalesManagementSalesman | per source table | Sales management salesman | [DOC] | https://unity.karmak.io/Customer |
| IsDelinquent | per source table | Delinquent flag | [DOC] | https://unity.karmak.io/Customer |
| DelinquencyTerm | per source table | Delinquency term | [DOC] | https://unity.karmak.io/Customer |
| NationaLeaseAccountNumber | per source table | National lease account number (sic — spelled without "l" in "National" by source) | [DOC] | https://unity.karmak.io/Customer |
| EstablishedDate | per source table | Established date | [DOC] | https://unity.karmak.io/Customer |
| PerformCreditCheck | per source table | Perform-credit-check flag | [DOC] | https://unity.karmak.io/Customer |
| SubjecttoFinanceCharge | per source table | Subject-to-finance-charge flag (sic, no space in source field name) | [DOC] | https://unity.karmak.io/Customer |
| ChargeFET | per source table | Federal excise tax charge flag | [DOC] | https://unity.karmak.io/Customer |
| TaxStatus | per source table | Tax status | [DOC] | https://unity.karmak.io/Customer |
| IsQuickCreate | per source table | Quick-create flag | [DOC] | https://unity.karmak.io/Customer |
| StatementType | per source table | Statement type | [DOC] | https://unity.karmak.io/Customer |
| SeparateStatement | per source table | Separate statement flag | [DOC] | https://unity.karmak.io/Customer |
| AllowServiceUnitOwnership | per source table | Allow-service-unit-ownership flag | [DOC] | https://unity.karmak.io/Customer |
| SalesCreditLimit | per source table | Sales credit limit | [DOC] | https://unity.karmak.io/Customer |
| SalesAccountStatus | per source table | Sales account status | [DOC] | https://unity.karmak.io/Customer |
| AllowBillingService | per source table | Allow-billing-service flag | [DOC] | https://unity.karmak.io/Customer |
| BillingServiceAccountNumber | per source table | Billing service account number | [DOC] | https://unity.karmak.io/Customer |
| CommentID / CommentType / Comment / CommentBriefDescription | per source table | Comment sub-object fields | [DOC] | https://unity.karmak.io/Customer |

The source table itself carries columns "Field Type," "Required?," "Field Length," and
"Default" for every field above — see the verbatim JSON sample payloads in §3 for concrete
value shapes (dealer "EP ROOFING INC." and "ALASKA USA FEDERAL CREDIT UNION" example records).

### 2b. Karmak Unity — Repair Order Header

`[DOC]`, https://unity.karmak.io/Repair-Order-Header.html. Source states: "This data object is
used to display the header records for all repair orders in Fusion... This data object can be
joined to Repair Order Task and then to Repair Order Details." URL path: `/frw/RepairOrderHeader`.

Full field list (SQL Field Name | Column Description, as spelled by source):

AddDate, ROServiceWriter, AuthorizationNumber, BillingContactname, BillingCustomerAccountStatus,
BillingCustomerAddress, BillingCustomerCity, BillingCustomerCountry, BillingCustomerCounty,
BillingCustomerIndustryType, BillingCustomerName, BillingCustomerNumber,
BillingCustomerPostalCode, BillingCustomerRegion, IsBillingCustomerWarranty,
BillingCustomerWorkPhone, BillingHomePhone, Branch, CharacteristicType,
CompletedToInvoicedInterval, ContactHomePhone, ContactName, ContactWorkPhone, CreditReserve,
CustomerAccountStatus, CustomerAddress, CustomerBaseBranch, CustomerCity, CustomerName,
CustomerNumber, CustomerPhone, CustomerPostalCode, CustomerRegion, CustomerUnitNumber,
IsCustomerWarranty, DaysArrivalToFirstPunch, DaysFirstPunchToLastPunch, DaysOpenToFirstPunch,
Department, Division, ECMReading, EmailAddressOfCustomer, FirstPunchDate, FollowUpEmailFlag,
InServiceDate, IndustryType, InvoiceDueDate, InvoiceNumber, InvoiceUser, LastPunchDate,
LastUpdate, UpdateUser, LPONumber, MeterType, OriginalRONumber, PaymentMethod,
RemoteApplication, RemoteEstimateID, ROAge, ROArrivalDateTime, ROBillingHours, ROBookHours,
IsROClockedON, ROClockedONTechnicians, IsROCompleted, "RO Customer PO Number",
RODateCompleted, RODateInvoiced, RODateOpened, RODaysCompletedToInvoiced,
RODaysSinceLastWorkedOn, ROEHCCharges, ROHoursBilled, ROHoursSinceLastWorkedOn, ROHoursWorked,
ROLaborCharges, ROLaborCost, ROMiscellaneousCharges, ROMiscellaneousChargesCost, RONumber,
ROOpenTime, ROPartsAverageCost, ROPartsCharges, ROPartsReplacementCost, ROPartsSellingCost,
ROPerformance, ROPromiseDateTime, ROPromisedDays, ROPromisedHours, RORemainingHours, ROStatus,
ROTaskCount, ROTechnicians, ROTotalAverageCost, "RO Total Replacement Cost",
ROTotalSellingCost, IsROWaiting, IsROWaitingForParts, ROWaitingTasksCount, SalesTaxSetting,
SalesTaxTotal, Salesperson, TaxBody, TaxStatus, TotalROCharges, UnitMake, UnitMeterReading,
UnitModel, UnitYear, VIN, IsVoided, AssessmentCompletedByUser (Fusion 3.62.3.1+),
AssessmentCompletedDate (3.62.3.1+), CustomerContactedByUser (3.62.3.1+), CustomerContactedDate
(3.62.3.1+), CustomerRequestedServiceToBeginDate (3.62.3.1+),
DealerScheduledServiceToBeginDate (3.62.3.1+), RepairTypeCode (3.62.3.1+, "used for the Allison
Transmission Integration"), ROEstimatedAmount (3.62.3.1+, "used by the Wheeltime integration
and can be updated from Decisiv"), SendCustomerROUpdates (3.62.3.1+, "for the Wheeltime
integration"), AllisonRepairCode (3.62.3.1+), KeyTag (3.62.3.1+), CommentTablesID (3.62.3.1+).

All tag `[DOC]`, all URL https://unity.karmak.io/Repair-Order-Header.html.

### 2c. Karmak Unity — Repair Order Detail

`[DOC]`, https://unity.karmak.io/Repair-Order.html. Source states: "This data object is used to
display all part, labor, and miscellaneous charge detail items on a given repair order." URL
path: `/frw/RepairOrderDetails`.

Full field list (as spelled by source): AddDate, AddUser, AverageCost, BackorderPriority,
BillCustomerOT, IsBillingAdjustment, BillingCompanyName, BillingCustomer, BinLocation, Branch,
CalculatedAgainst, CalculatedPrice, ControlNumber, CoreClass, CoreCost, CoreDescription,
CoreExtendedPrice, IsCoreNoCharge, IsCoreOneLineTransaction, CoreOverridePrice,
CorePartNumber, CorePrice, CoreReferenceMPO, CoreSupplier, Department, Division, EHCCharge,
EHCCode, EHCDescription, IsEnterLaborInTotalHours, ExtendedAverageCost, "Extended Price",
ExtendedReplacementCost, ExtendedSellingCost, FillingBranch, InsideSalesperson, DateInvoiced,
InvoiceNumber, Item, ItemDescription, KitAssemblyTemplate ("Note that this field is not used in
Fusion at this time"), LastUpdateDate, LastUpdateUser, Message, Method, IsNoCharge, OEMPrice,
OEMRebateAmount, OTBillingTotal, OTDescription, OTHourlyCost, OTHourlyRate, OTHours,
OTMultiplier, OutsideSalesperson, OverridePrice, OverrideTaxStatus, OwningCompanyName,
OwningCustomer, PartActionFlag, PartStockNumber ("Note that this field is not used in Fusion at
this time"), PartTechnician, PartType, IsPartialFill, Percentage, IsPolicyAdjustment, Price,
ProductClass, ProductCode, IsPulled, QuantityHours, RateLevelDescription, ReferenceMPO,
RepairGroup, RepairType, ReplacementCost, RONumber, ROStatus, SerialNumber, SerialStockType,
Shift, Supplier, TaskNumber, TimeIn, TimeOut, TransactionType, UnitNumber, UnitOfMeasure,
StockNumber, IsWarranty, Weight.

All tag `[DOC]`, all URL https://unity.karmak.io/Repair-Order.html.

### 2d. Karmak Unity — Service Deferred Repairs

`[DOC]`, https://unity.karmak.io/Service. Source states: "This data object is used to display a
list of all deferred repairs from the Fusion business system... found in the Deferred Repair
program within the Fusion business system."

AddDate, AddUser, CustomerName, CustomerNumber, DeferredDate, DeferredReason,
DeferringBranch, DeferringDepartment ("This department will be copied into the repair order
task when applied to an open repair order. If the set department is not valid for the branch
applying the repair, the department will be set to the user's login department."),
DeferringRONumber, DeferringTaskNumber, DeferringUser, ExpectedExpirationDate, InServiceDate,
LastUpdateDate, LastUpdateUser, OfficePhone, RepairGroup, RepairGroupDescription, RepairType,
RepairTypeDescription, "Ship-toAddress1", "Ship-toAddress2", "Ship-toCity", "Ship-toCountry",
"Ship-toCounty", "Ship-toPostalCode", "Ship-toRegion" (hyphenation and capitalization exactly as
spelled by source), UnitMake, UnitModel, UnitNumber, UnitYear, Vin.

### 2e. Karmak Unity — Service Unit Meter History, Open Barcode Time, Preventive Maintenance, RO Quote Detail/Header

All `[DOC]`, https://unity.karmak.io/Service. Field lists fully transcribed and preserved in
this file's source session; representative fields include (Meter History): AddDate, AddUser,
AverageDailyUsage, CustomerNumber, Erroneous, Estimate, LastUpdateDate, LastUpdateUser, Make,
MeterDate, MeterReading, MeterSource, MeterTransactionType, MeterType, Model, ModelYear,
CompanyName, UnitNumber, Vin; (Open Barcode Time): ApplicationName, AddApplicationNumber,
AddDate, AddUser, BranchCode, CompletionTime, Department, ElapsedTime, ElapsedTime_FH,
LastUpdate, UpdateUser, RemainingTime ("subtracts the closed and open time worked on the RO
task from the RO task Billing hours"), RepairOrderNumber, RepairType, RepairTypeDescription,
Shift, ShiftDescription, TaskNumber, TechnicianName, TechnicianNumber, TimeIn,
UpdateApplicationName, UpdateApplicationNumber; (Preventive Maintenance): PMBasis,
PMCode, PMDescription, PMDateNextDue, PMNextMeterDue, PMTimeInterval, PMMeterInterval,
PMLastCompletionDate, PMLastCompletionMeter, PMRepairTypeCode, PMRepairTypeDescription,
PMServiceDue7Days/14Days/21Days, PMServiceDueFlag, GraceDays, GraceMeter, LastMeterDate,
LastMeterReading, LastInvoiceNumber, LastInvoiceDate, LastRepairOrder, LastPMROBranch,
ContractCompanyName, ContractCustomerContact, ContractCustomerShopPhone, ContractNumber,
IsLeaseRentalCustomer, TaskClockedOnTechnicians, UnitIndicator, Ownership, OwningCustomerContact.
RO Quote Detail and RO Quote Header largely mirror the RO Detail/Header field sets above with
"repair order quote" substituted for "repair order" in field descriptions (e.g. Quantity vs
QuantityHours, IsInventory added, QuoteAge added). Full verbatim tables retrievable again at
the URL above if line-by-line reproduction is needed beyond this summary.

### 2f. Karmak Unity — Report Data Access (RDA) object catalog

`[DOC]`, https://unity.karmak.io/ReportDataAccess.html. This is the master index of 80+ named,
queryable "data objects" available through Karmak's self-service reporting API — the single
most useful artifact in Lane C for a digital twin, because it names the object inventory Karmak
itself considers reportable, including a **Chart of Accounts** object:

> "Chart of Accounts — Display a listing of all general ledger chart of accounts and their sub
> category structure down to 6 levels." — [DOC], https://unity.karmak.io/ReportDataAccess.html

Full named-object list (verbatim names, as spelled): AP Misc PO Header, AP Misc PO Detail, AP
Notes, AP Vendor, Account Allocation, Accounting Address Information, Accounting Comments,
Accounting Period, Accounts Payable Detail, Accounts Payable General Ledger Detail, Accounts
Receivable Customer, Accounts Receivable Customer Misc Prompt, Accounts Receivable Details,
Branch Details (Helper), Branch and Department (Helper), Chart of Accounts, Check Register,
Deal Comission (sic — one "m," as spelled by source), Deal Detail, Deal Header, Deal Packet,
Department Lookup (Helper), Fixed Assets, Fuel Invoice Summary, General Ledger Balance,
General Ledger Transaction, Invoice Sales Summary, Invoice Sales Summary Detail,
Lease-Rental Contract (+ ~8 more Lease/Rental objects), Local Purchase Order, Parts Alternate
Bin Locations, Parts Branch Inventory Usage, Parts Committed, Parts Customer Backorders, Parts
Customer Core Right To Return, Parts Customer Purchase and Return, Parts Fuel Ticket, Parts
Fuel Ticket Detail, Parts Inventory, Parts Inventory Extended, Parts Inventory Receiving
Detail, Parts Inventory Usage, Parts Inventory Yearly Usage, Parts Kit Assembly Detail, Parts
Lost Sales, Parts Messages, Parts Order, Parts Order Detail, Parts Physical Inventory, Parts
Physical Inventory Detail, Parts Purchase Order, Parts Purchase Order Detail, Parts Supplier,
Parts Supplier Core RTR, Parts Transactions, Parts Vendor Rebates, Posting Reference Status,
Preventive Maintenance, Quick Lists (Helper), Repair Order Detail, Repair Order Header, Repair
Order Task, Sales Unit, Sales Unit Flooring, Salesperson Commission, Service, Service
Technician, Service Technician Certification, Service Technician Performance, Service
Technician Productivity, Service Technician Time, Service Unit Components, Service Unit
Master Detail, Service Unit Owning Customer, Unit Purchase Order Detail, Unit Purchase Order
Header, Velocity Codes, View Users.

### 2g. Karmak Unity — Transactional API index

`[DOC]`, https://unity.karmak.io/APIs.html. Named transactional endpoints (each has its own
field-level doc page, not individually re-fetched this pass beyond Customer/RO/Service above):
A/P Invoice, Activate Repair Type, Add Parts to RO, Create Journal Entry, Create Parts PO,
Create Parts Sales Order, Create and Update AP Vendors, Create and Update Parts Inventory,
Create and Update Technicians, Create and Update Users, Customer, Customer Special Pricing,
GET Available AP Vendors, GET Available Branches, GET Available Suppliers, GET and Update
Fusion Branch Details, Meter Reading, Parts Cross Reference, Parts Order Helpers, Parts PO
Details, Parts PO Search, Parts Search and Availability, Parts Supersession, Parts Supplier,
System Status, Unit Characteristics, Unit Inventory, Update Part Quantity.

### 2h. CDK Drive (Fortellis) — Customers API, `queryCustomerById`/`getCustomer` object

This is CDK documenting **its own fields**, via its Fortellis developer marketplace. Base path
`https://api.fortellis.io/cdkdrive/crm/v1/customers` — `[DOC]`,
https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c0e82268-70cc-4d04-92c1-da9934800505/external/20220621170422548-uYfTqXe1.pdf

Methods: createCustomer (POST /), queryCustomers (GET /), queryCustomerById (GET /{custId}),
updateCustomer (POST /{custId}).

> "Dealer configurable required fields: name.first, name.last, name.companyName,
> postalAddress.street, postalAddress.city, postalAddress.state, postalAddress.county,
> postalAddress.postalCode, contactMethods.email1" — [DOC], CDK_Drive_Customers_API.pdf, p.5–10

Field table (name | required/notes, as stated):

- `items` (array)
- `customerId` (string)
- `name` (object, REQUIRED) — `name.first`/`name.last` (string, required if companyName not
  defined), `name.companyName` (string, required if first not defined)
- `contactMethods` (object, REQUIRED) — `primaryPhone` (REQUIRED), `homePhone`, `mobilePhone`,
  `pager`, `pagerAccessCode`, `homeFax`, `workFax`, `email1` (REQUIRED; codes NA/CD),
  `emailDesc1`–`emailDesc6` (enum HOME/WORK/OTHER), `email2`–`email6`, `preferredMethod` (enum
  PRIMARYPHONE/PAGER/HOMEFAX/WORKFAX/PRIMARYEMAIL), `blockPhoneFlag`/`blockEmailFlag`/
  `blockMailFlag` (flag, default false)
- `postalAddress` (object) — `street`, `city`, `county`, `state`, `postalCode`, `country`
- `links.self.href` / `links.self.method` / `links.self.title`

From the companion `CDK_Drive_Get_Customer_v3.pdf` (28 pp., fully read) — additional object
fields, all `[DOC]`:

- `birthDate` field
- `customerName` object: companyName, firstName, fullName, lastName, middleName, suffix, title
- `insurance` object: insuranceAgency.*, insuranceCompany.*, policy.expirationDate,
  policy.number, policy.verifiedBy, policy.verifiedDate
- `overDues` object: over120Due, over90Due, over60Due, over30Due — each stated as "Two-digit
  float returned as a string"
- `postalAddress` object: addressLine1, addressLine2, city, country, county, postalCode, state
- `secondaryCustomerName` object: same shape as customerName
- `specialInstructions` object: line1, line2, line3, line4, line5
- Long-running Operation Response Attribute Table: operationId (uuid), status (enum
  complete/received/error), receivedDateTime, updatedDateTime, checkStatusAfterSeconds,
  `_links` object with status/result sub-objects

### 2i. CDK Drive — Enhanced Report Generator / Dictionary Library (via Clarivoy, a third party documenting CDK's own screen)

`[COMM]` — Clarivoy (third-party vendor) describing CDK Drive's own on-screen field dictionary —
https://clarivoy.helpjuice.com/en_US/cdk-setting-up-dms-sales-reports. Menu path stated
verbatim:

> "REPORT AND ANALYZE (pie chart icon) → ENHANCED REPORT GENERATOR → NEW REPORT → Select
> Application: FINANCE AND INSURANCE → File Name: FI-WIP"

Field list from the "Dictionary Library" (verbatim, as spelled): ItemID, ACCOUNTING DATE,
BUYER FIRST NAME, BUYER LAST NAME, BUYER STREET ADDRESS, BUYER CITY, BUYER STATE, BUYER ZIP
CODE, BUYER CELL, BUYER BUSINESS TELEPHONE, BUYER HOME TELEPHONE, E-MAIL ADDRESS 1, E-MAIL
ADDRESS 2, E-MAIL ADDRESS 3, CO-BUYER NAME, CO-BUYER STREET ADDRESS, CO-BUYER CITY, CO-BUYER
STATE, CO-BUYER ZIP CODE, COBUYER CELL, BACK GROSS, FRONT GROSS, TOTAL GROSS, SERIAL
NUMBER-NEW, MAKE DESCRIPTION-NEW, MODEL DESCRIPTION-NEW, MODEL YEAR-NEW, STOCK TYPE-NEW, TOTAL
SELLING PRICE, SALES TYPE.

Derivation logic stated verbatim (this is the closest public artifact anywhere in this project
to a CDK internal calculation formula):
> "Total gross= pulls from deal.TotalGross" ; "Back gross= pulls from deal.BackGross" ; "Front
> gross= uses the following rule: - If deal.frontEndGrossProfit is not blank, it is used. - If
> deal.frontEndGrossProfit is blank, deal.frontGross is used instead."

This tells us CDK's underlying object is named `deal` with attributes `TotalGross`,
`BackGross`, `frontEndGrossProfit`, `frontGross` — stated by a third party observing CDK's
screen output, not by CDK itself, hence `[COMM]` not `[DOC]`.

### 2j. Integrator-level DMS taxonomy naming CDK Drive alongside Dominion, ACS, Reynolds, Procede

`[COMM]` — practitioner-authored "DMS Cheat Sheet 6-20-2023" (unattributed author/company,
hosted on Scribd) — https://www.scribd.com/document/809504766/DMS-Cheat-Sheet-6-20-2023.
Verbatim excerpt naming the DMS category headers this integrator tracks (used to decide CRM↔DMS
push/pull capability, not a field schema):

> "ACS (Dominion DMS) X X X xtime Adams DMS X X X xtime ADP/CDK 3PA "CDK Drive" X X X X X
> real-time real-time ADP/CDK W.E.B. Desking X ADP/CDK Work A Quote X ... Dealertrack (Arkona)
> X X X X X real-time real-time ... Power (UCS) X X X real-time real-time real-time Quorum X X
> X ... Tekion DMS pending X X X Procede xtime Serti xtime"

Column headers verbatim: "CRM (Optional) DMS Service Customer DMS Desk Web Service Connect API
Finalized Booked/ Closed Open Appointment DMS Push from Push to F&I Push to F&I Access Sold
Deals Accepted Service RO's Service RO's s (or Xtime Dashboard Sold Deals Customers) to DMS F&I
FTP". This confirms CDK Drive ("ADP/CDK 3PA") and Dominion DMS ("ACS") are tracked as distinct,
named DMS categories with distinct push/pull capability flags by at least one working
integrator, but the document does **not** publish field-level schemas for either.

### 2k. Dominion DMS — partner integration directory (no field schema found)

`[DOC]` for the existence/count of the directory, https://lvlupauto.com/integrations/dominion-dms
and https://www.dominiondms.com/partners/. 25 named third-party products integrate with
"Dominion VUE DMS via the Dominion API" (direction: Bi-directional/Direct, no field names
published). Representative verbatim line: "700 Credit — Certified third-party integration with
Dominion VUE DMS via the Dominion API. Bi-directional Direct." No field, table, or object name
is published on this page or on dominiondms.com/partners/ — this is a partner marketing
directory, not a data dictionary.

---

## 3. Verbatim quotes worth keeping

> "This data object is used to display the header records for all repair orders in Fusion, and
> contains one record for each order with summary information about the repair order included.
> This data object can be joined to Repair Order Task and then to Repair Order Details in order
> to view the detail information on the repair order." — Karmak Unity, [Repair Order Header](https://unity.karmak.io/Repair-Order-Header.html)

> "Chart of Accounts — Display a listing of all general ledger chart of accounts and their sub
> category structure down to 6 levels." — Karmak Unity, [Report Data Access](https://unity.karmak.io/ReportDataAccess.html)

> "RemainingTime — This field subtracts the closed and open time worked on the RO task from the
> RO task Billing hours. If the RO task is set to use Book hours as the bill hours, then the
> closed and open time will be subtracted from the book hours. If the billing hours on the task
> is 0 then this field will be blank." — Karmak Unity, [Service](https://unity.karmak.io/Service)

> "Front gross= uses the following rule: - If deal.frontEndGrossProfit is not blank, it is
> used. - If deal.frontEndGrossProfit is blank, deal.frontGross is used instead." — Clarivoy,
> describing CDK Drive's Enhanced Report Generator, [cdk-setting-up-dms-sales-reports](https://clarivoy.helpjuice.com/en_US/cdk-setting-up-dms-sales-reports)

> "Dealer configurable required fields: name.first, name.last, name.companyName,
> postalAddress.street, postalAddress.city, postalAddress.state, postalAddress.county,
> postalAddress.postalCode, contactMethods.email1" — CDK Drive Customers API, Fortellis PDF
> (`CDK_Drive_Customers_API.pdf`, saved at `/home/user/workspace/cdk2_raw/C/`)

> "ADP/CDK 3PA 'CDK Drive' X X X X X real-time real-time" — anonymous integrator, "DMS Cheat
> Sheet 6-20-2023," [Scribd](https://www.scribd.com/document/809504766/DMS-Cheat-Sheet-6-20-2023)

> "97 dealer technology products integrate with Dominion DMS across 16 categories... Integration
> data is mapped independently and refreshed as the catalog grows." — LvlUp Auto, [Dominion DMS Integrations](https://lvlupauto.com/integrations/dominion-dms) (page content changed between fetches — a later fetch showed "25 dealer technology products... across 11 categories"; the site appears to update its own count live, flagged here as an inherent instability in this source, not a transcription error)

> "Lightspeed DMS offers an all-in-one platform tailored for dealers in powersports, marine, RV,
> trailer, outdoor power equipment, and golf industries" ... "Audience: Auto dealerships, OEM,
> independent software vendors, heavy truck dealers" [for CDK] vs. "Audience: Dealership owners
> and operations managers searching for a solution to manage inventory, sales, service, and
> multi-store operations efficiently" [for Lightspeed DMS] — SourceForge, [CDK Global vs. Lightspeed DMS Comparison Chart](https://sourceforge.net/software/compare/CDK-Global-vs-Lightspeed-DMS/)

> "10. Lightspeed DMS -- Best for powersports, marine, RV, and OPE dealers... It is not designed
> for heavy construction, agriculture, or commercial vehicle dealerships." — Flyntlok, [Best dealer management systems](https://www.flyntlok.com/insights/best-dealer-management-systems)

> "Karmak Fusion is purpose-built for Class 6-8 heavy-duty trucking with certified
> bi-directional OEM integrations for DTNA/Freightliner, PACCAR/Peterbilt/Kenworth,
> International..., and Mack/Volvo." — Flyntlok, [Best dealer management systems](https://www.flyntlok.com/insights/best-dealer-management-systems)

> "Most often Karmak, CDK Lightspeed, Procede Excede, Charter Software, or QuickBooks paired
> with spreadsheets." [listing legacy systems GSI's Cloud DMS on NetSuite replaces] — GSI, [Cloud DMS for Dealerships](https://www.getgsi.com/use-cases/cloud-dms-for-dealerships)

---

## 4. What I searched and could not find

- **NADA/ATD standard chart of accounts (truck-dealer specific)** — `[UNK]`. Queries used:
  "PACCAR Peterbilt financial statement upload layout", "NADA ATD standard chart of accounts",
  "NADA ATD financial statement upload specification". Found only the ATD ratio/formula
  SlideGuide (`NADA_ATD_SlideGuide_2026.pdf`, already downloaded) and the unrelated NIADA
  (independent-dealer) chart of accounts published by Frazer
  (https://www.frazerhelp.com/help-manual/niadachartofaccounts.htm) — neither is the NADA/ATD
  truck-dealer standard COA or a PACCAR/Peterbilt-specific upload layout.
- **PACCAR/Peterbilt financial-statement upload layout** — `[UNK]`. Same queries as above; no
  PACCAR-published field-level upload spec located.
- **Public Fivetran / Airbyte / Workato / Zapier / Celigo connector named "CDK Global"** —
  `[UNK]`. Queries used: "Fivetran CDK Global connector schema", "Airbyte Workato Zapier
  Celigo CDK Global connector". Results returned only generic iPaaS platform documentation
  (connector SDK concepts, generic schema-management docs); no vendor's public connector
  catalog lists a CDK Global object schema.
- **Karmak "Data Field Properties" downloadable file** referenced in the RDA overview page —
  `[UNK]`. Targeted search run; not located as a directly downloadable public file distinct
  from the HTML field tables already transcribed above.
- **Naked Lime field-level DMS mapping documentation** — `[UNK]`. Queries used: "Naked Lime CDK
  field mapping DMS integration documentation". Only marketing/press content found, no field
  docs.
- **Dominion DMS field-level record layout or API schema** — `[UNK]`. Queries used: "Dominion
  DMS integration partner field mapping API documentation". Found only the partner-listing
  directories at dominiondms.com/partners/ and lvlupauto.com/integrations/dominion-dms — these
  state integration existence and direction (bi-directional/direct) but publish no field or
  object names.
- **Procede Excede Swagger/API field catalog access level** — not independently re-confirmed
  this pass beyond finding that https://www.procedesoftware.com/api/ states "Swagger's UI
  creates a user-friendly interface that allows developers to explore our API directly in the
  browser" `[DOC]`, https://www.procedesoftware.com/api/ — this describes an embedded/browsable
  Swagger UI but the page itself does not expose field names in fetched content; whether the
  underlying Swagger spec requires a login was not conclusively determined this pass. Treat
  Procede's actual field list as `[UNK]` — gating status ambiguous, not confirmed either way.
- **Dealer-FX, Xtime, KPI Cloud, ASA/ATD twenty-group reporting spec vendors** — `[UNK]`, not
  separately searched this pass beyond what surfaced incidentally (Xtime named only as a
  push-target column header in the DMS Cheat Sheet, §2j — no field schema).
- **Fullpath (AutoLeadStar), DealerSocket, VinSolutions, Tekion, Dealer Vision, Elead, Auto/Mate
  migration guides with DMS field mapping schemas** — `[UNK]`, not separately fetched this
  pass; DealerSocket appears only as a named Dominion-DMS-certified integration partner
  (§2k), with no field schema retrieved.
- **CDK's own "3PA" partner onboarding documentation (field-level, not marketing)** — `[UNK]`;
  the only concrete CDK Drive field-level material retrieved is the Fortellis Customers API and
  Get Customer v3 spec (§2h) and the Clarivoy-observed report screen (§2i), both accessed
  without a login. Whether deeper 3PA partner docs exist behind a gate was not independently
  tested — see §5 note on gating.

**Explicit gated/NDA vendor list** (documentation existence confirmed, contents not
accessible without credentials, based on searches run above and in prior spins of this
project): Dominion DMS field-level API schema (directory is public, schema is not), Naked
Lime integration specifics, and any CDK "3PA"/Fortellis partner-tier documentation beyond the
publicly downloadable Fortellis PDFs already retrieved. By contrast, **Karmak's unity.karmak.io
and portal.karmak.io developer documentation is fully public with no login required** — this is
the single most significant and unexpected finding of Lane C: a full heavy-truck DMS field
dictionary sitting in the open.

---

## 5. Corrections to the first spin

The first-spin files relevant to Lane C are `cdk_07_landscape_exit.md` and
`cdk_08_paccar_oem.md`. Corrections and confirmations, cross-checked against this Lane C pass:

1. **First spin already flagged the Karmak/Procede-vs-CDK-Drive uncertainty and got the
   direction right.** `cdk_07_landscape_exit.md` stated: "`INFERRED (dealer-accounting norm)`:
   Peterbilt Atlantic, as a PACCAR network dealer, most plausibly runs Karmak Fusion or Procede
   Excede rather than CDK Drive Heavy Truck, since both have documented PACCAR/Peterbilt-
   adjacent OEM integrations, but the task brief states the twin [runs CDK Drive plus
   Lightspeed]." This Lane C pass **confirms and strengthens** that inference: Karmak Fusion is
   explicitly documented as PACCAR/Peterbilt/Kenworth-integrated
   ([Flyntlok](https://www.flyntlok.com/insights/best-dealer-management-systems)), and separately
   confirms Peterbilt Atlantic's "Lightspeed" is very unlikely to be either (a) Lightspeed
   Retail/OnSite (a retail POS company, wrong industry entirely) or (b) CDK's own "Lightspeed"
   NXT/EVO product line, which is explicitly powersports/marine/RV/trailer/OPE/golf and
   explicitly **not** for "heavy construction, agriculture, or commercial vehicle dealerships"
   ([Flyntlok](https://www.flyntlok.com/insights/best-dealer-management-systems)). Neither DMS
   named "Lightspeed" in public sources is a heavy-truck product. This is an open identification
   question the first spin did not fully resolve either — it is carried forward here as `[UNK]`,
   not resolved by this pass, and should be raised directly with Peterbilt Atlantic's systems
   contact rather than assumed.
2. **First spin's Karmak entry undersold Karmak's public documentation.** `cdk_07_landscape_exit.md`
   described Karmak only in commercial/ownership terms ("Not publicly published; vendor markets
   'flexible technology with personalized support,' no rate card found") and did not identify
   unity.karmak.io as a public developer portal. This Lane C pass corrects that: Karmak
   publishes an extensive, un-gated field-level API and Report Data Access catalog covering
   Customer, Repair Order Header/Detail, Service, Preventive Maintenance, and 80+ other named
   objects including a Chart of Accounts object (§2a–2g above).
3. **`cdk_08_paccar_oem.md`'s "Karmak PACCAR integration page" citations
   (karmak.com/integrations/paccar) are a different domain from Karmak's developer portal
   (unity.karmak.io / portal.karmak.io)** — both are legitimate Karmak properties but serve
   different purposes (the `.com` page is OEM-integration marketing; the `unity.karmak.io` /
   `portal.karmak.io` sites are the developer/field documentation). This distinction was not
   made in the first spin and is worth keeping straight in the twin's source list.
4. **The Authenticom v. CDK Global antitrust litigation noted in `cdk_07_landscape_exit.md`**
   (data-integrator access blocked by CDK/Reynolds, preliminary injunction vacated by the 7th
   Circuit in 2017) is consistent with, and helps explain, why Lane C found **no public
   DealerVault/Authenticom field-layout documentation** in this pass — Authenticom's business
   model depends on privately negotiated dealer-authorized data pulls, not a published public
   schema, which is itself compatible with the litigation history already on file.
5. **No claim in the first spin is contradicted by new information on NADA/ATD chart of
   accounts or PACCAR financial-statement upload layout** — both remain `[UNK]` in both spins;
   first spin's own honesty flag ("`UNVERIFIED`: No primary NADA or ADA published PDF study was
   directly retrieved") stands uncorrected and unresolved by this Lane C pass.
