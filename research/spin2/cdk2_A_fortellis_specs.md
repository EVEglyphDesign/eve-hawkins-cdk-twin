# Lane A — Fortellis / CDK Drive API Field Dictionary

Primary-source retrieval exercise per `/home/user/workspace/cdk2_rules.md`. Quoted, not
paraphrased, from downloaded Fortellis API guide PDFs. Every field row carries the source URL.
Confidence tags: `[DOC]` = vendor-published with URL, `[COMM]` = practitioner/forum, `[INF]` =
reasoned inference (clearly separated), `[UNK]` = looked, could not find.

**Reader context:** Peterbilt Atlantic (nine Atlantic Canada rooftops, PACCAR/Peterbilt franchise,
runs CDK Drive + Lightspeed) — digital twin of dealership ledger/operations outside CDK.

---

## Field counts per API (top-level record attribute tables, excluding sub-object expansions counted separately below)

| API | Version | Top-level record fields | Total fields incl. all nested sub-objects (approx.) |
|---|---|---|---|
| Get Repair Order v3 | v3 | 76 | ~230 |
| CDK Drive History Setup Repair Order | v2 | ~76 (near-duplicate of v3) + unique `visitInspection` object | ~240 |
| Get Customer v3 | v3 | 33 | ~75 |
| Customers API | v1 | 4 top objects | ~35 |
| glwippost (Post Accounts GL WIP) | latest | 5 methods, 4 payload objects | ~45 |
| glpost (Post Accounts GL) | latest | Identical to glwippost + 2 additional opCodes | ~45 |
| Repair Orders v1 Dev Guide | v1 | No formal attribute table (YAML-only) | ~60 (from JSON examples) |
| CDK Drive History Setup FI Sales | v3 | 16 top-level objects | ~330 |
| CDK Drive Get FI Sales | v4 | Same 16 top-level objects as v3 (confirmed identical object list) | ~330 |

---

## 1. What I actually retrieved

All files downloaded to `/home/user/workspace/cdk2_raw/A/`, text-extracted to
`/home/user/workspace/cdk2_raw/A/txt/`:

- **Get Repair Order v3** (49 pp.) — [S3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf) `[DOC]`
- **Get Customer v3** (28 pp.) — [S3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf) `[DOC]`
- **Customers API v1** (22 pp.) — [S3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c0e82268-70cc-4d04-92c1-da9934800505/external/20220621170422548-uYfTqXe1.pdf) `[DOC]`
- **Repair Orders v1 Dev Guide** (39 pp.) — [S3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c7771500-1c95-4f8e-9241-eddc17cd55f6/external/20240227171600864-GvA-0CSi.pdf) `[DOC]`
- **glwippost — CDK Drive Post Accounts GL WIP** (29 pp.) — [S3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/0ae40bee-d879-407f-951d-beb541a3e704/external/20250828224853615-kcpN9S6F.pdf) `[DOC]`
- **glpost — CDK Drive Post Accounts GL** (29 pp.) — [S3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/2ed7a316-f952-4c81-9e2b-bc148b77c007/external/20250828224949696-jrcxa3JN.pdf) `[DOC]`
- **CDK Drive History Setup FI Sales v3** (53 pp.) — [S3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/638f1179-e2bf-4aac-b601-a9acc51247f8/external/20260713100351123-Zywvy7-P.pdf) `[DOC]`
- **CDK Drive Get FI Sales v4** (59 pp.) — [S3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/b54ba111-7874-4c25-b8d9-ba3b3eb722ef/external/20260713092924114-rlWrjbvB.pdf) `[DOC]`
- **CDK Drive History Setup Repair Order v2** (45 pp.) — [S3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/48e7060a-b828-4de5-8505-76fd9e21b3c0/external/20260615111720822-vGbyzwRH.pdf) `[DOC]`
- **CDK Modern APIs Migration Guide** (8 pp., pricing/billing) — [community.fortellis.io](https://community.fortellis.io/sites/default/files/CDK_Modern.APIs_Migration.Guide_04.14.2023.pdf) `[DOC]`
- **fortellis-parts-store-openapi_SAMPLE.yml** — retrieved but confirmed **not a real CDK API**; it is a Fortellis developer-portal tutorial/sample spec, unrelated to any actual CDK Drive Parts endpoint. Recorded here so it is not mistaken for a live spec. `[DOC]` (as to what the file is) / this is a correction, see §5.

All nine PDFs were confirmed non-trivial in page count and text-extracted in full; line counts:
get_repair_order_v3.txt=2962, get_customer_v3.txt=1641, customers_api_v1.txt=1000,
glwippost_spec_latest.txt=1428, glpost_spec_latest.txt=1440, repair_orders_v1_devguide.txt=1794,
repair_order_history_setup_latest.txt=2785, fisales_history_setup_latest.txt=3427,
fisales_bulk_delta_latest.txt=3678.

The full Fortellis API-documents S3 bucket (`fortellis-api-documents-prod.s3-us-west-2.amazonaws.com`)
is publicly listable via `?list-type=2` pagination — confirmed 28,691 keys / 9,232 unique
spec-UUID folders enumerated in this session's working data.

---

## 2. The field dictionary

### 2.1 Get Repair Order v3

Source for every field below: [Get Repair Order v3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf) `[DOC]`

**Platform mechanics (page 9–11):**

| Header | Required | Meaning as stated by source |
|---|---|---|
| `Subscription-Id` | REQUIRED | "The Subscription ID assigned to the user of the app making the request." |
| `Authorization` | REQUIRED | Bearer token via Fortellis identity server, OAuth2 client-credentials flow |
| `Department-Id` | REQUIRED | "must indicate a department that works with the Service DMS type" |
| `Request-Id` | REQUIRED | client-supplied UUID, echoed back in response |
| `Accept` | optional | MIME type negotiation |

DMS types (verbatim, page 10): "Accounting, Finance, Inventory, Parts, and Service."

Service URL: `https://api.fortellis.io/cdk/drive/servicerepairorder/v3`

Methods: `GET /open` (getOpenRepairOrdersBulk, 31-day range), `GET /open/delta`
(getOpenRepairOrdersDelta, 48hr), `GET /wip` (getWIPRepairOrders, 48hr), `GET /closed`
(getClosedRepairOrdersBulk, 31-day), `GET /closed/delta` (getClosedRepairOrdersDelta, 48hr),
`GET /long-operations/{operationId}/status`, `GET /long-operations/{operationId}/result`.

Async pattern: 202 Accepted → `operationId`/`status`/`receivedDateTime`/`updatedDateTime`/
`checkStatusAfterSeconds`/`_links` → poll status → pull result (retrievable 24 hours after
completion).

HTTP status codes returned: 200, 202, 400, 401, 403, 404, 429 (rate limiting), 500, 502, 503, 504.

**Repair Order Record Attribute Table** (top-level, 76 fields):

`addOnFlag`, `apptDate`, `apptFlag`, `apptTime`, `blockAutoMsg`, `bookedDate`, `bookedTime`,
`bookerNo`, `cashier`, `closedDate`, `comebackFlag`, `comments`, `contactEmailAddress`,
`contactPhoneNumber`, `customer` (obj), `dedMultiValueCount`, `deductibles` (array),
`discounts` (array), `disMultiValueCount`, `emailMultiValueCount`, `estimatedCompletionDate`,
`estimatedCompletionTime`, `feeMultiValueCount`, `hasCustPayFlag`, `hasIntPayFlag`,
`hasWarrPayFlag`, `hostItemId`, `hrsMultiValueCount`, `isCustomerWaiting`, `isOrigWaiter`,
`isSoldByDealer`, `isSpecialCustomer`, `lastServiceDate`, `lbrMultiValueCount`,
`linMultiValueCount`, `mileage`, `mileageLastVisit`, `mileageOut`, `mls` (obj),
`mlsMultivalueCount`, `openDate`, `openTime`, `operations` (array), `origPromisedDate`,
`origPromisedTime`, `payBalanceDue`, `payCPTotal`, `payments[]` (array), `payMultivalueCount`,
`phoneMultiValueCount`, `postedDate`, `priorityValue`, `promisedDate`, `promisedTime`,
`prtMultiValueCount`, `punMultiValueCount`, `purchaseOrderNo`, `rapApptID`, `rapMultivalueCount`,
`remarks`, `rentalFlag`, `roNumber`, `serviceAdvisor`, `statusCode`, `statusDesc`,
`tagNo` (max 7 chars), `technicianPunchTimes[]` (array), `totalPaymentMade`, `totals[]` (array),
`totMultiValueCount`, `vehicle` (obj), `visItemMultiValueCount`, `voidedDate`, `warMultivalueCount`.

**customer Object:** `custId`, `name1`, `name2`, `address` (obj: `addressLine1`, `addressLine2`,
`cityStateZip`), `emailAddresses[]` (`address`, `desc`), `phoneNumbers[]` (`description` — enum
`[MAIN, HOME, HOME FAX, BUSINESS, BUSINESS FAX, CELLULULAR` (typo preserved verbatim from source)`,
PAGER, CONTACT]`, `extension`, `number`).

**deductibles Array:** `actualAmount` (f.2), `laborAmount` (f.2), `laborType` (str),
`lineCodes` (str), `maximumAmount` (f.2), `partsAmount` (f.2), `sequenceNo` (int, "Multiple
charge distribution (MCD) sequence number").

**discounts Array:** `appliedBy`, `classOrType`, `debitAccountNo`, `debitControlNo`,
`debitTargetCo`, `desc`, `id`, `laborDiscount`, `level`, `lineCode`, `lopSeqNo`,
`managerOverride`, `originalDiscount`, `overrideAmount`, `overrideGPAmount`,
`overrideGPPercent`, `overridePercent`, `overrideTarget`, `partsDiscount`, `sequenceNo`,
`totalDiscount`, `userID`.

**mls Object:** `cost` (str), `gogCost` (str, "Sum of the lube cost"), `gogPrice` (str, "Lube
sale amount"), `laborType` (str), `lineCode` (str), `mcdPercentage` (f.2), `miscCost` (str),
`miscPrice` (str), `opCode` (str, "MLS operation code"), `opCodeDesc` (str), `sale` (str, "MLS
sale amount"), `sequenceNo` (str, "MLS operation sequence number"), `subletCost` (str),
`subletPrice` (str), `type` (str, "Code that indicates the type of operation").

**operations Array — line object:** `line.actualWork`, `line.addOnFlag`, `line.bookerNo`,
`line.campaignCode`, `line.cause`, `line.comebackFlag`, `line.complaintCode`,
`line.dispatchCode`, `line.estimatedDuration`, `line.lineCode`, `line.serviceRequest`,
`line.statusCode`, `line.statusDesc`, `line.storyEmployeeNo`, `line.storySequenceNo`,
`line.storyText`.

**line.laborOperations[]:** `actualHours`, `bookedDate`, `bookedTime`, `comebackFlag` (source
has typo `"laboOperationsr[ ].comebackFlag"`), `comebackRO`, `comebackSA`, `comebackTech`,
`cost` (f.2), `flagHours`, `forcedShopCharge` (f.2), `lineCode`, `mcdPercentage` (f.2), `opCode`,
`opCodeDesc`, `otherHours`, `sale` (f.2), `sequenceNo` (int), `soldHours`, `technicianIds[]`
(array — "If the service returns MULT, it indicates multiple technicians"), `timeCardHours`,
`type`.

**line.laborOperations[].fees[]:** `cost`, `id`, `laborType`, `lineCode`, `lopOrPartFlag` (bool,
"If true, this is a labor operation"), `lopOrPartSeqNo`, `mcdPercentage` (f.2), `opCode`,
`opCodeDesc`, `sale`, `sequenceNo`, `type` (str, "The code that indicates the type of fee").

**line.laborOperations[].hours[]:** `actualHours`, `cost`, `flagHours`, `hourType`, `laborType`,
`lineCode`, `mcdPercentage` (f.2), `otherHours`, `percentage`, `sale`, `sequenceNo` (int),
`soldHours`, `technicianId` (int), `timeCardHours`.

**line.laborOperations[].parts[]:** `bin1`, `comp`, `compLineCode`, `coreCost`, `coreSale`,
`cost`, `desc`, `employeeId` (int), `extendedCost`, `extendedSale`, `laborSequenceNo` (int),
`laborType`, `lineCode`, `list`, `mcdPercentage`, `number`, `outsideSalesmanId` (int),
`partClass`, `qtyBackordered` (int), `qtyFilled` (int), `qtyOnHand` (int), `qtyOrdered` (int),
`qtySold` (f.2), `sale`, `sequenceNo` (int), `source`, `specialStatus`,
`unitServiceCharge` (obj).

**line.laborOperations[].parts[].fees[]:** `cost`, `id`, `laborType`, `lineCode`,
`lopOrPartFlag` (str, uses "L and P to indicate either Labor or Part"), `loporPartSeqNo`,
`mcdPercentage` (f.2), `opCode`, `opCodeDesc`, `sale` (f.2), `sequenceNo`, `type` (enum:
L=Lube, M=Miscellaneous, S=Sublet).

**line.warranty[]:** `authorizationCode`, `claimType`, `conditionCode`, `failedPartNo`,
`failedPartsCount`, `failureCode`, `laborSequenceNo` ("null when warranty data is entered for a
repair line code and not a specific labor operation"), `lineCode`.

**payments Array (data[].payments[]):** `code` (str, e.g. CASH/CARD), `insuranceFlag` (bool),
`paymentAmount` (str, "Two-digit float returned as a string").

**technicianPunchTimes Array:** `alteredFlag` (bool, "hours were updated on the DMS via the
Change Technician Hours (CTH) function"), `duration`, `lineCode`, `technicianId` (int),
`timeOff` (time), `timeOn` (time), `workDate` (date), `workType`.

**totals Array:** `actualHours`, `coreCost`, `coreSale`, `discount`, `flagHours`,
`forcedShopCharge`, `laborCost`, `laborCount` (int), `laborDiscount`, `laborSale`,
`laborSalePostDed`, `localTax`, `lubeCost`, `lubeCount` (int), `lubeSale`, `miscCost`,
`miscCount` (int), `miscSale`, `otherHours`, `partsCost`, `partsCount` (int), `partsDiscount`,
`partsSale`, `partsSalePostDed`, `payType` (str, "single-character string that is also the first
character of the labor type"), `roCost`, `roSale`, `roSalePostDed`, `roTax`, `shopChargeCost`,
`shopChargeSale`, `soldHours`, `stateTax`, `subletCost`, `subletCount` (int), `subletSale`,
`supp2Tax`, `supp3Tax`, `supp4Tax`, `timeCardHours`.

**vehicle Object:** `deliveryDate`, `licenseNumber`, `lotLocation`, `make`, `makeDesc`,
`model`, `modelDesc`, `vehicleColor`, `vehId`, `vin`, `year` (int, four digits).

**Long-running Operation Response Attribute Table:** `operationId` (uuid), `status` (enum:
complete/received/error), `receivedDateTime` (date, ISO 8601), `updatedDateTime` (date, ISO
8601), `checkStatusAfterSeconds` (int, "Returned values: 30 || null"), `_links` (obj, HATEOAS),
`_links.status||result` (obj), `_links.status||.result.href` (str).

---

### 2.2 CDK Drive History Setup Repair Order v2

Source: [Repair Order History Setup PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/48e7060a-b828-4de5-8505-76fd9e21b3c0/external/20260615111720822-vGbyzwRH.pdf) `[DOC]`

Service URL: `https://api.fortellis.io/cdk/drive/servicerepairordersetup/v2` — **distinct** from
the v3 bulk/delta service (`servicerepairorder/v3`), confirming this is a separately versioned
API, not just a doc variant.

**API Method Summary** (verbatim table, page 6):

| HTTP Method + Endpoint | Operation ID | Description |
|---|---|---|
| `GET /history` | `getHistoricalRepairOrders` | "Get the historical closed repair order records within the dates you specify with a maximum timespan of 6 months per request." |
| `GET /long-operations/{operationId}/status` | `getQueryStatus` | "Get the status of long running query." |
| `GET /long-operations/{operationId}/result` | `getQueryResult` | "Get the result of long running query" |

Headers: `Subscription-Id` REQUIRED, `Authorization` REQUIRED, `Department-Id` REQUIRED ("must
indicate a department that works with the Service DMS type"), `Request-Id` REQUIRED, `Accept`
optional — identical header contract to Get Repair Order v3.

**Repair Order Record Attribute Table, `customer` Object, `deductibles`/`discounts`/`mls`/
`operations`/`payments`/`technicianPunchTimes`/`totals`/`vehicle`** — confirmed near-duplicate of
the Get Repair Order v3 schema (same field names, same types, same descriptions) — see §2.1
for the full transcription; not re-transcribed here to avoid padding a duplicate.

**The `visitInspection` Object** — **unique to this History Setup spec, not present in RO v3**
(page 45):

| Attribute | Type | Description (verbatim) |
|---|---|---|
| `data[ ].visitInspection.` | obj | "Defines a vehicle inspection." |
| `comment` | str | "A text description that captures the comments related to the inspection." |
| `formDesc` | str | "A text description of the form." |
| `formName` | str | "The name of the vehicle inspection form." |
| `itemNo` | int | "The unique number of the item." |
| `itemNotes` | str | "Notes related to an inspection item." |
| `itemOpCode` | str | "The labor operation code associated with inspection item." |
| `itemOpCodeDesc` | str | "A text description of the labor operation code associated with inspection item." |
| `itemStatus` | str | "A code that indicates the current status of an inspection item." |
| `itemStatusDesc` | str | "A text description of the inspection item status" |
| `status` | str | "A code that indicates the current status of the inspection." |
| `technicianId` | int | "The number of the technician who is performing the inspection." |
| `updateDate` | date | "The date on which the inspection was last updated." |
| `updateTime` | time | "The time of day at which the inspection was last updated." |

---

### 2.3 Get Customer v3

Source: [Get Customer v3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf) `[DOC]`

**Customer Record Attribute Table** (33 top-level fields): `balances` (f.2), `birthDate` (obj),
`comment`, `contactMethods` (obj), `commentDate` (date, format YYYY-MM-DD), `customerName` (obj),
`creditLimit` (f.2), `currentDue` (f.2), `customerId`, `dateAdded` (date), `deleteDataDate`
(date), `deleteDataTime` (date), `employer`, `gender` (enum: F=Female, M=Male), `hostItemId`,
`insurance` (obj), `isDeleteDataFlag` (bool, CCPA delete flag, default false), `language`,
`lastUpdated` (date), `mailability` (str, valid values 1-9 or X), `nameCode`, `optOutDate`
(date), `optOutFlag` (bool, default false), `optOutTime` (date, "seconds past midnight"),
`overDues` (obj), `partsCounterCode`, `partsFlag` (bool), `partsType` (enum: W=wholesale,
null=no type), `preferredContact` (enum: C=Cellular, E=email, F=Home Fax, H=Home Phone,
M=Mail, P=Pager, W=Work phone, null=No preference), `saleType`, `postalAddress` (obj),
`secondaryCustomerName` (obj), `serviceCustomer` (str, "Contains an 'S' for service-only
(non-AR/Parts) customers"), `specInstructions` (obj), `taxCode`.

**birthDate Object:** `day`, `month`, `year` (note: "API Consumers can use API Data Management to
control this PII field").

**contactMethods Object:** `blockEmailFlag`, `blockMailFlag`, `blockPhoneFlag` (all bool, default
false), `businessPhone`, `businessPhoneExt`, `homeFax`, `homePhone`, `mobilePhone`, `pager`,
`preferredDay` (enum 1-7=Mon-Sun), `preferredLanguage`, `preferredMethod` (enum: B=Work FAX,
D=Do Not Disturb, E=Main address, F=Home FAX, M=Postal mail, P=Pager, T=Main Telephone,
X=Text message), `preferredTime` (enum: AM/PM), `primaryPhone`, `secondaryHomePhone`,
`textMessageCarrier`, `textMessagePhone`, `workFax`, `emailAddresses[]` (`address` — valid
values NA/CD, `type` — enum CELL, HOME (default), WORK, PDA/LAPTOP, VEHICLE, OTHER, NA, CD).

**customerName Object:** `companyName`, `firstName`, `fullName` (format: "<fName> <mName>
<lName>"), `lastName`, `middleName`, `suffix`, `title`.

**insurance Object:** `insuranceAgency` (obj: `agencyName`, `agentName`, `phoneNumber`,
`postalAddress`[`addressLine1`, `addressLine2`, `city`, `postalCode`, `state`]),
`insuranceCompany` (obj: `name`, `phoneNumber`, `postalAddress`[same sub-fields]), `policy`
(obj: `expirationDate`, `number`, `verifiedBy`, `verifiedDate`).

**overDues Object:** `over120Due`, `over90Due`, `over60Due`, `over30Due` (all f.2 as string).

**postalAddress Object:** `addressLine1`, `addressLine2`, `city`, `country`, `county`,
`postalCode`, `state`.

**secondaryCustomerName Object:** `companyName`, `firstName`, `fullName`, `lastName`,
`middleName`, `suffix`, `title`.

**specialInstructions Object:** `line1`, `line2`, `line3`, `line4`, `line5`.

---

### 2.4 Customers API v1

Source: [Customers API v1 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c0e82268-70cc-4d04-92c1-da9934800505/external/20220621170422548-uYfTqXe1.pdf) `[DOC]`

Endpoints: `POST /` (createCustomer), `GET /` (queryCustomers), `GET /{custId}`
(queryCustomerById), `POST /{custId}` (updateCustomer). Base Path:
`https://api.fortellis.io/cdkdrive/crm/v1/customers`. Headers: `Subscription-Id` REQUIRED,
`Authorization` REQUIRED, `Request-Id` REQUIRED, `ETag`/`If-Match` (optimistic concurrency
control). "New in this Version": `companyName` attribute added to `name` object (mutually
exclusive with first/last).

**Attribute Table:** `items` (array), `customerId`, `name` (obj REQUIRED: `name.first`
[REQUIRED IF `companyName` not defined], `name.last` [REQUIRED IF `companyName` not defined],
`name.companyName` [REQUIRED IF `name.first` not defined]), `contactMethods` (obj REQUIRED:
`primaryPhone` [REQUIRED], `homePhone`, `mobilePhone`, `pager`, `pagerAccessCode`, `homeFax`,
`workFax`, `email1` [REQUIRED, valid values NA/CD], `emailDesc1` [enum HOME/WORK/OTHER, default
HOME], `email2`, `emailDesc2` [default WORK], `email3`, `emailDesc3`, `email4`, `emailDesc4`,
`email5`, `emailDesc5`, `email6`, `emailDesc6`, `preferredMethod` [enum: PRIMARYPHONE, PAGER,
HOMEFAX, WORKFAX, PRIMARYEMAIL], `blockPhoneFlag`/`blockEmailFlag`/`blockMailFlag` [flag,
default false]), `postalAddress` (obj: `street`, `city`, `county`, `state`, `postalCode`,
`country`), `links` (obj: `links.self.href`, `links.self.method`, `links.self.title`).

Dealer-configurable required fields (verbatim list): `name.first`, `name.last`,
`name.companyName`, `postalAddress.street`, `postalAddress.city`, `postalAddress.state`,
`postalAddress.county`, `postalAddress.postalCode`, `contactMethods.email1`.

HTTP status codes returned: 200 OK, 400 Bad Request, 401 Unauthorized, 403 Forbidden,
404 Not Found, 500 Internal Server Error — **no 429 documented in this API**, unlike the
Repair Order and GL Post APIs.

Related-APIs note (verbatim, page relevant to functional-area mapping): "CDK Drive Repair
Orders API relies on the Customers API to create and use customers that exist in the dealers
Customer Master File (CMF)... CDK Drive Service Vehicles: Create, update, query, and retrieve
service domain vehicle information stored in CDK Drive." This confirms a "CDK Drive Service
Vehicles" API name exists in the ecosystem, distinct from any spec located and downloaded in
this session (see §4).

---

### 2.5 glwippost — CDK Drive Post Accounts GL WIP

Source: [glwippost PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/0ae40bee-d879-407f-951d-beb541a3e704/external/20250828224853615-kcpN9S6F.pdf) `[DOC]`

Methods: `POST /startWIP` (startWIP), `POST /transWIP` (transWIP), `POST /postWIP` (postWIP),
`POST /transBatchWIP` (transBatchWIP — batch), `POST /postBatchWIP` (postBatchWIP — batch),
`GET /glSalesChain` (glSalesChain), `GET /glExpenseAllocation` (glExpenseAllocation, "DMS
Account type N"), `GET /errWIP/{tranID}` (errWIP), `GET /orgHelper` (orgHelpers),
`GET /jrnlHelper/{glCompanyNumber}` (jrnlHelpers).

Service URL: `https://api.fortellis.io/cdk/drive/glwippost`. Headers: `Subscription-Id`,
`Authorization`, `Department-Id` (REQUIRED, "must indicate a department that uses the
Accounting DMS configuration"), `Request-Id`, `Accept`, `Content-Type`.

> "Only authorized CDK Accounting users have the credentials to post transaction data to the
> DMS General Ledger. This is reflected in the OpCodes supported by the Post WIP and Post
> Batch WIP methods (they do not support U or P OpCodes)." — [glwippost PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/0ae40bee-d879-407f-951d-beb541a3e704/external/20250828224853615-kcpN9S6F.pdf)

**glExpenseAllocation Response Attributes:** `allocID` (format: Source GL CoID*Acc't),
`hostItemID`, `createDate`, `account` (obj, indexed array pattern: `account.V[].idx` [int],
`account.V[].value` [str]), `allocationPercent` (same `V[]` pattern), `company` (same pattern),
`lastUpdateDate` (same pattern), `percent` (same pattern), `trgtAcct`/`trgtAScct` (same
pattern — note source typo `trgtAScct`), `trgtCoID` (same pattern), `userId` (same pattern).

**startWIP Request Attributes:** `acctgDate` (date REQUIRED, "two open months, the Current
month and the Post Ahead month"), `desc` (str, REQUIRED IF required by dealership, max 132
chars), `docType` (enum REQUIRED, valid values: GL.VALID, DOC), `groupName` (str, max 30
chars), `m13Flag` (flag REQUIRED, "Month 13 is an optional special accounting period following
the last month of the fiscal year"), `refer` (str REQUIRED, max 10 chars, format example
"1AB-C200"), `rtnCode` (str, valid values: 0=no error, 1-900=# of GL errors, >900=error
number), `sendline` (str, error text if rtnCode≠0), `srcCo` (str REQUIRED, max 3 chars),
`srcJrnl` (str REQUIRED, max 3 chars), `transID` (str, assigned by Fortellis, max 30 chars),
`userID` (str REQUIRED, max 15 chars), `userName` (str REQUIRED, format "userName*vendorID",
max 30 chars).

**transWIP Request Attributes:** `acct` (str REQUIRED, max 7 chars, "Validated against:
ACDBn/GL.COA"), `allocID` (str, max 11 chars), `cntl` (str, REQUIRED IF indicated by
ACDB/GL.COA, max 17 chars), `cntl2` (str REQUIRED, max 17 chars), `postAmt` (f.2 REQUIRED,
"debits positive, credits negative with minus sign"), `postDesc` (str, REQUIRED IF
PostDescFlag=1, max 132 chars), `prod` (str REQUIRED, max 10 chars), `rtnCode` (same as
above), `sendline` (int), `statCnt` (str REQUIRED, max 4 chars), `transID` (str REQUIRED,
max 30 chars), `trgtCoID` (str REQUIRED, max 3 chars).

HTTP status codes returned: 200 OK, 400 Bad Request.

---

### 2.6 glpost — CDK Drive Post Accounts GL

Source: [glpost PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/2ed7a316-f952-4c81-9e2b-bc148b77c007/external/20250828224949696-jrcxa3JN.pdf) `[DOC]`

**Verbatim finding:** this document is nearly byte-identical to glwippost (diff of extracted
text = 257 lines, mostly title changes "CDK Drive Post Accounts GL WIP" →
"CDK Drive Post Accounts GL"). The example curl command still references the `glwippost`
service path:

```
curl -X POST "https://api.fortellis.io/cdk/drive/glwippost/postWIP" \
  -H 'Authorization: Bearer <token>' -H 'Subscription-Id: <subscriptionId>' \
  -H 'Department-Id: <departmentId>' -H 'Request-Id: <requestId>' \
  -H 'Accept: application/json' -H 'Content-type: application/json' \
  -d '{"opCode": "S","transID": "1*75*SAI0214*1"}'
```
— [glpost PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/2ed7a316-f952-4c81-9e2b-bc148b77c007/external/20250828224949696-jrcxa3JN.pdf)

Payload Details section (glExpenseAllocation Response Attributes, startWIP/transWIP Request
Attributes) is identical to glwippost — see §2.5, not re-transcribed.

**Key difference — the postWIP opCode table has additional values in glpost not seen in the
glwippost excerpt:**

| opCode | Meaning (verbatim) |
|---|---|
| D | delete from WIP |
| **P** | **"Validates and if valid, posts the transaction to the CDK Accounting General Ledger"** |
| S | save to WIP, validate, leave for further action |
| **U** | **"Validates and if valid, uses an unattended process to post to CDK Accounting GL"** |
| V | validates and deletes from WIP |

HTTP status codes: same base table as glwippost, plus (page 9, line 332) **429** — "Issued
when your API call use exceeds the subscribed rate limit. Make sure you are not making
unnecessary calls to the server and examine your API call limits" — plus 502 Bad Gateway,
503 Service Unavailable, 504 Gateway Timeout.

**Inference `[INF]`:** glwippost and glpost describe the same underlying service
(`glwippost` path referenced in both, identical payload schemas) documented at two different
permission tiers — glwippost's guide is written for a WIP-only tier ("do not support U or P
OpCodes"), glpost's guide documents the fuller Accounting-user tier that can actually post
(P) or auto-post (U) to the GL. This is inference from the verbatim text differences above,
not a stated fact in either document.

---

### 2.7 Repair Orders v1 Dev Guide

Source: [Repair Orders v1 Dev Guide PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c7771500-1c95-4f8e-9241-eddc17cd55f6/external/20240227171600864-GvA-0CSi.pdf) `[DOC]`

**No formal attribute table exists in this document.** Verbatim: "The API Spec is a YAML file
that acts as the contract... Find the latest API Spec on the API page here, CDK Drive Repair
Orders v1" — meaning the field dictionary lives in a separate OpenAPI YAML on the Fortellis
platform that was not located/downloaded in this session (see §4).

**Endpoints (14):** `POST /repair-orders` (createRepairOrder), `GET /repair-orders?
{serviceAdvisorId}` (queryRepairOrders), `GET /repair-orders/{repairOrderId}`
(queryRepairOrderById), `POST /repair-orders/{repairOrderId}` (updateRepairOrder),
`POST /repair-orders/{repairOrderId}/service-lines` (addServiceLine),
`GET /repair-orders/{repairOrderId}/service-lines/{serviceLineId}` (queryServiceLineById),
`POST .../service-lines/{serviceLineId}` (updateServiceLine),
`DELETE .../service-lines/{serviceLineId}` (deleteServiceLine),
`GET /repair-orders/lookups/dispatchcodes` (queryDispatchCodes),
`GET .../dispatchcodes/{dispatchCodeId}` (queryDispatchCodeById),
`GET .../dispatchmakecodes` (queryDispatchMakeCodes), `GET .../labortypes` (queryLaborTypes),
`GET .../labortypes/{laborTypesId}` (queryLaborTypeById), `GET .../serviceAdvisors`
(queryServiceAdvisors), `GET .../serviceAdvisors/{advisorId}` (queryServiceAdvisorById),
`GET .../technicians` (queryTechnicians), `GET .../technicians/{techId}`
(queryTechniciansById).

Base Path: `https://api.fortellis.io/cdkdrive/service/v1/repair-orders`.

Ecosystem diagram names (verbatim): "Repair Order API", "CDK Drive Customer API", "CDK Drive
Service Vehicles API", "CDK Drive Workshop Management API" — confirms a "Workshop Management
API" name exists in the CDK ecosystem, not independently verified/downloaded in this session.

Response codes: POST — 201 (Details of successful post), 400, 401, 403. GET (except PING) —
200, 400, 401, 403, 404. DELETE — 204 No Content, 400, 401, 403. PING — 200 Connection OK,
400 Connection Not OK.

**Example JSON fields from `createRepairOrder` request/response** (verbatim field names, real
example values in the source): `repairOrderId`, `status` (`code`, `description`),
`links.self.href`, `blockIVRFlag`, `comments`, `customerHref`, `vehicleHref`,
`dispatchMakeCode`, `customerContactInfo`, `dropOff` (`dateTime`, `address`, `city`, `note`,
`phone`, `vanNumber`), `estimate` (`authorized`, `labor`, `parts`, `misc`, `lube`, `sublet`,
`tax`), `mileageIn` (`value`, `units`), `pickUp` (`dateTime`, `address`, `city`, `note`,
`phone`, `vanNumber`), `promiseDateTime`, `serviceAdvisorId`, `tagNum`, `remarks`,
`transportType`, `serviceLineItems[]` (`cause`, `comebackFlag`, `dispatchCode`,
`estimatedDuration`, `laborEstimate`, `laborType`, `lubeEstimate`, `miscEstimate`,
`partsEstimate`, `serviceEstimate`, `serviceRequest`, `subletEstimate`, `taxEstimate`,
`technicianId`, `laborOperations[]` [`forceShopChargeFlag`, `laborType`, `opCode`,
`opCodeDesc`, `soldHours`, `saleAmount`, `saleOverrideFlag`, `includedParts[]`
{`fixedSaleFlag`, `includesCoreFlag`, `mfrCode`, `partNumber`, `partNumberDescription`,
`partQty`, `saleAmount`}]), `workorder` (`printWorkorder`, `workorderPrinter`,
`workorderCopies`, `partsPrinter`).

Vehicle Service Concepts section defines (verbatim terms): Service Appointment, Repair Order,
Service Line Item, OpCode ("short for Labor Operation Code"), Labor Type.

---

### 2.8 CDK Drive History Setup FI Sales v3

Source: [FI Sales History Setup PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/638f1179-e2bf-4aac-b601-a9acc51247f8/external/20260713100351123-Zywvy7-P.pdf) `[DOC]`

**Platform mechanics:** Service URL `https://api.fortellis.io/cdk/drive/fisalessetup/v3`.
`Department-Id` note (verbatim): "This API works with the F&I Sales DMS type, and the
Department IDs you use with this API must support the same DMS type." Method:
`GET /history` (getHistoricalVehicleSale, "maximum timespan of 6 months per request"),
`GET /long-operations/{operationId}/status`, `GET /long-operations/{operationId}/result`.
HTTP status codes: 200, 202, 400 (same async 202-Accepted long-running pattern as the Service
APIs).

**FI Sales Record Attribute Table** — top-level object list (16 objects): `data.buyer`,
`data.coBuyer`, `data.commissions`, `data.crm`, `data.deal`, `data.dealAuxiliary`,
`data.dealEvents`, `data.fees`, `data.incentives`, `data.insurance`, `data.salesPersons`,
`data.tax`, `data.totals`, `data.trades`, `data.vehicle`, `data.weOwes`.

**The buyer Object:** `businessPhone`, `custOrCompanyCode`, `customerId`, `fullName` (format
"firstName, lastName, midName"), `homePhone`, `secondaryFullName`, `birthDate` (obj: `day`,
`month`, `year` — "masked for privacy concerns"), `emailAddresses[]` (`address` [NA/CD codes],
`type` — enum CELL, HOME (default), PDA/LAPTOP, VEHICLE, WORK, OTHER, NA, CD), `postalAddress`
(obj: `addressLine1`, `city`, `country`, `county`, `postalCode`, `state`).

**The coBuyer Object:** verbatim mirror of `buyer` — same field set (`businessPhone`,
`custOrCompanyCode`, `customerId`, `fullName`, `homePhone`, `secondaryFullName`, `birthDate`,
`emailAddresses[]`, `postalAddress`).

**The commissions Object** — `commissionsBase` (obj): `addCapCostFee3DealerCommBase`,
`addCapCostFee4DealerCommBase`, `addCapCostFee5DealerCommBase`, `addCapCostFee6DealerCommBase`,
`addCapCostFee7DealerCommBase`, `annualFee3DealerCommBase`, `annualFee4DealerCommBase`,
`annualFee5DealerCommBase`, `dealerCommFeeOption1`–`dealerCommFeeOption10` (10 fields),
`initFee3DealerCommissionBase`–`initFee10DealerCommissionBase` (8 fields),
`insuranceCommDlr`, `levelizedLifeDealerComm` (f.2), `surplusCashCommBaseForGPComp`,
`texasGAPInsuranceDealerCommissionBase` (f.2). `commissionsDeal` (obj): `commissionGross` (f.2),
`commissionPack` (f.2), `commOnSaleDlr` (f.2), `surplusCash` (f.2), `optionsCommDlr` (f.2).
`commissionsSalesperson1` (obj): `bonus` (f.2), `commission` (str), `saleCreditSP` (str) — and
by extension `commissionsSalesperson2`/`3` (mirrors, per source pattern).

**The crm Object:** `crmCommissionTotal` (f.2), `crmFlag` (bool, "If true, the deal should be
sent to the CRM"), `crmSalesCreditTotal` (f.2), `crmSaleType` (str), `crmSpiffTotal` (f.2),
`crmClosingMgr` (obj: `commission` [f.2], `employeeId`, `employeeName`, `saleCredit` [f.2],
`spiff`), `crmFIMgr` (same sub-field pattern as `crmClosingMgr`), `crmSalesMgr` ("mirror the
attributes returned for crmFIMgr"), `crmSalesperson1`/`2`/`3` (each "mirror the attributes
returned for crmFIMgr").

**The deal Object** (largest single object, ~95 fields): `accountingAccount`, `accountingDate`
(date), `adjustedCapCost` (f.2, "the actual amount financed over the term of the lease"),
`adjustedCostofVehicle` (f.2), `adjustmentsDealerDefined` (f.2), `adjustmentsROPO` (f.2),
`adjustmentsStandard` (f.2), `amountDueAtStart` (f.2), `apr` (f.2), `backGross` (f.2),
`balloonAmount` (str), `balloonRate` (str), `bankFee` (str), `baseMSRP` (str),
`baseResidual` (f.2), `branch` (str), `buyRateAddOn` (f.2), `buyRateAPR` (f.2),
`buyRateLMF` (str), `calcMethod` (str), `cashCapReduction` (f.2),
`capCostReductionTax2Amount` (f.2), `cashDown` (str), `cashPrice` (f.2), `contractDate` (date),
`costPrice` (f.2), `creationDate` (date, format YYYY-MM-DD), `customerCashDown` (f.2),
`customerComments` (str), `dealerDefined1`–`dealerDefined8` (8 user-defined string fields),
`dealNo` (str), `dealSource` (str), `dealType` (str), `depositAmount` (str), `depositType`
(str), `dmvRosNumber` (str, "A unique ID assigned to the federal tax"), `dueOnDelivery` (f.2),
`fiDealType` (str), `fiIncome` (f.2, "The dealership profit on financing"), `financeAmt` (f.2),
`financeCharge` (f.2), `financeSource` (str), `finInstituteCode` (str), `firstPayDate` (date),
`fiWipStatusCode` (str, "The actual Status Code from FI-WIP record"), `frontEndGrossProfit`
(f.2), `frontGross` (f.2), `grossProfit` (f.2), `hostItemId` (str), `initialCapCost` (str),
`lastPayAmount` (f.2), `lastPayDate` (date), `leaseEndPercentageRate` (f.2), `leaseEndValue`
(f.2), `leaseMileageAllowance` (f.2), `leasePayment` (str), `leaseType` (str),
`levelizedLifeAmount` (f.2), `levelizedLifeCost` (str), `levelizedLifeIncome` (str),
`lienHolderAddress`, `lienHolderCity`, `lienHolderName`, `lienHolderName2`, `lienHolderPhone`,
`lienHolderState`, `lienHolderZip`, `mileageExpected` (int), `mileageExpectedFlag` (bool),
`mileageMonthlyLimit` (str), `mileagePenaltyAmount` (f.2), `mileagePenaltyRate` (f.2),
`miscellaneous1`–`miscellaneous10` (10 free-response fields), `msrp` (f.2), `msrpFee1`,
`msrpFee2`, `onePayAmount` (str), `outTheDoorPrice` (f.2), `paymentAmt` (f.2), `paymentCode`
(str), `payments` (int, count), `paymentStyle` (enum: Regular, Irregular), `pickupDate1`–
`pickupDate3` (date ×3), `pickupPay1`–`pickupPay3` (str ×3), `salePriceWithWeOwes` (f.2),
`salesAccount` (str), `salesDate` (date), `salesManagementDealType` (str), `saleType` (enum:
Cash, Finance, Lease), `securityDepositAmount` (f.2), `securityDepositName` (str),
`sellRateAddOn` (f.2), `sellRateAPR` (str), `sellRateLMF` (str), `slsDealType` (str),
`term` (int), `unpaidBalance` (f.2), `waqNumber` (str).

**The dealAuxiliary Object:** `fiAux1`–`fiAux50` — "There are 50 auxiliary FI Sales fields
(fiAux1 – fiAux50). The values of these fields are based on F&I configuration settings and
each of these fields can contain either a prompted value, a constant value, or a calculated
value."

**The dealEvents Object:** `events[]` (array of deal events); FI Event Codes (verbatim): P =
Pending (read only), B = Booked/Recapped, F = Finalized (read-only), D = Delivered, A =
Pending, CF = Pending, n/a = Dealer defined 1–4, CV = Pending. `events[].dealEvent` (str),
`events[].dealEventDate` (date). `specialContract1`/`specialContract2` (obj each: `date`,
`reason`).

**The fees Object:** `addToCapAmount` (f.2), `warrantyFee` (f.2), `addToCapCostFee[]` (array
of 7: `.amount` [f.2], `.name` [str], `.costAmount` [f.2], `.profitType` [str], `.flag`
[bool]), `addToPriceFeeName[]` (array of strings), `annualFee[]` (array: `.amount`, `.name`),
`feeOption[]` (array of up to 10: `.amount`, `.name`, `.costAmount`, `.profitType`),
`initialFee[]` (array: `.amount`, `.name`, `.costAmount`, `.profitType`).

**The incentives Object:** `incentiveDealer` (f.2), `incentiveProgram` (f.2), `rebateAmount`
(f.2), `commonRebateDetails[]` (array: `.id` [str, max 14 chars], `.amount` [f.2], `.code`
[str, max 30 chars], `.description` [str, max 35 chars]).

**The insurance Object:** `extWarrantyExpMilesLease` (int), `extWarrantyTermLease` (int),
`insuranceTypeCode` (str), `texasGAPInsuranceAmount` (f.2), `insurance1` (obj: `cost`,
`deductible`, `fee`, `income`, `limit`, `limitMiles` [int], `name`, `term` [int]) —
`insurance2`/`insurance3` mirror `insurance1`. `accidentalHealthInsurance` (obj: `cost`,
`income`, `monthlyMaxAmount`, `premium`, `rate`, `term`). `creditLifeInsurance` (obj: `cost`,
`income`, `insuranceType`, `monthlyMaxAmount`, `premium`, `rate`, `term`).
`mechanicalBreakDownInsurance` (obj: `carrier`, `cost`, `deductible`, `eligComment`,
`eligFlag` [bool], `fee`, `income`, `limit` [int], `limitMax`, `name`, `term` [int],
`policyNo`, `purchaseCost`).

**The salesPersons Object:** `assnSlsperson`, `billingClerk`, `closingMgr`, `deliveryCoord`,
`fIMgr1`, `fIMgr2`, `salesMgr`, `salesperson1`, `salesperson2`, `salesperson3`.

**The tax Object:** `leaseFlexibleTax1Amount` (f.2), `leaseFlexibleTax2Amount` (f.2),
`serviceTaxAmount` (f.2), `goodsAndServicesTaxDetails` (obj: `.lstgstAmount`, `.lstGSTRate`,
`.lstGSTRateFlat`, `.lstGSTType`, `.upFrontGST`, `.upFrontPST`), `luxuryTaxDetails` (obj:
`.amount`, `.financedAmount`, `.monthlyAmount`, `.totalMonthlyAmount`,
`.uSLuxuryExciseTaxAmount`, `.upFrontAmount`), `purchaseFlexibleTaxDetails[]` (array:
`.amount`, `.base`, `.max`, `.maxCode`, `.name`, `.rate`), `salesTaxDetails` (obj:
`.financedAmount`, `.monthlyAmount`, `.totalMonthlyAmount`, `.upFrontAmount`),
`taxCommonDetails[]` (array: `.amount`, `.base`, `.name`, `.rate`).

**The totals Object:** `tax` (f.2), `totalAnnFees`, `totalBackCostAdjustments`,
`totalBasePrice`, `totalCapReduction`, `totalCashSurplus`, `totalCommission`,
`totalDMVLicenseFeeCalifornia`, `totalDown`, `totalFinancedFeeOptions`,
`totalFrontCostAdjustments`, `totalInsurancePremiums`, `totalGross`, `totalInitFees`,
`totalOfMonthlyPayments`, `totalOptionsFees`, `totalTaxableFees`, `totalTaxRate`,
`totalTradeAllowance`, `totalTradesACV`, `totalTradesNet`, `totalTradesOver`,
`totalTradesPayoff`, `weOweCostTotal`, `weOweSaleTotal` (all f.2).

**The trades Object:** `tradeDealerDefined1`–`tradeDealerDefined8` (8 string fields),
`tradeDetails[]` (array): `.netTrade` (f.2), `.tradeACV` (str), `.tradeColor`, `.tradeGross`
(f.2), `.tradeMake`, `.tradeMakeName`, `.tradeMileage` (int), `.tradeModel`, `.tradeModelName`,
`.tradeModelNo`, `.tradeModelType`, `.tradeOver` (f.2), `.tradePayOff` (f.2), `.tradeStock`,
`.tradeStyle`, `.tradeVIN`, `.tradeYear` (int).

**The vehicle Object:** `age` (int, "age = vehicleEntryDate – soldContractDate"), `bodyStyle`,
`color`, `glVehicleCost` (f.2), `make`, `makeName`, `model`, `modelName`, `modelNo`,
`modelType`, `stockNo`, `vehicleMileage` (int), `vehInventoryCompany`, `vehSaleCompany`,
`vin`, `year` (int).

**The weOwes Object:** `backWeOwes` (f.2), `frontWeOwes` (f.2), `frontWeOwesGrossCost` (f.2),
`frontWeOwesGrossSales` (f.2), `weOweBackCostTotal` (f.2), `weOweBackSaleTotal` (f.2),
`weOweFrontGrossSales` (f.2), `weOweResidualTableTotal` (int), `weOweResidualTotal` (f.2),
`weOweSaleHardTotal` (f.2), `weOweSaleSoftTotal` (f.2).

**Long Running Response Attribute Table:** `operationId` (uuid), `status` (enum:
complete/received/error), `receivedDateTime` (date, ISO 8601), `updatedDateTime` (date, ISO
8601), `checkStatusAfterSeconds` (int, "Returned values: 30 || null"), `_links` (obj, HATEOAS
pattern identical to the Service APIs).

---

### 2.9 CDK Drive Get FI Sales v4

Source: [FI Sales Bulk/Delta v4 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/b54ba111-7874-4c25-b8d9-ba3b3eb722ef/external/20260713092924114-rlWrjbvB.pdf) `[DOC]`

Service URL: `https://api.fortellis.io/cdk/drive/fisales/v4` — distinct from v3's
`fisalessetup/v3`.

**API Method Summary** (verbatim): `GET /open/delta` (FISalesOpenDelta, "48 hours"),
`GET /closed/delta` (FISalesClosedDelta, "48 hours"), `GET /open` (FISalesOpenBulk, "31 days"),
`GET /closed` (FISalesClosedBulk, "31 days"), `GET /bulk` (FISalesBulk, "31 days past"),
`GET /long-operations/{operationId}/status` (queryStatus), `GET /long-operations/{operationId}
/result` (queryResult).

**Field structure:** confirmed identical top-level object list to v3 — same 16 section headers
(`The buyer Object`, `The coBuyer Object`, `The commissions Object`, `The crm Object`,
`The deal Object`, `The dealAuxiliary Object`, `The dealEvents Object`, `The fees Object`,
`The incentives Object`, `The insurance Object`, `The salesPersons Object`, `The tax Object`,
`The totals Object`, `The trades Object`, `The vehicle Object`, `The weOwes Object`), verified
by section-heading comparison between the two documents. Not re-transcribed field-by-field to
avoid padding a duplicate — see §2.8 for the full transcription, which applies to this API as
well.

Additional platform notes unique to this v4 guide (verbatim): "This API supports API Data
Management, a feature that lets API users select the attributes returned from requests to
the API." / "All timestamps and date-related fields used by this API operate in Coordinated
Universal Time (UTC)." / "This API may exclude records containing personally identifiable
information (PII), as configured by the dealer and as indicated by individual customers."

---

## 3. Verbatim quotes worth keeping

> "Only authorized CDK Accounting users have the credentials to post transaction data to the
> DMS General Ledger. This is reflected in the OpCodes supported by the Post WIP and Post
> Batch WIP methods (they do not support U or P OpCodes)."
> — [glwippost PDF, CDK Drive Post Accounts GL WIP](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/0ae40bee-d879-407f-951d-beb541a3e704/external/20250828224853615-kcpN9S6F.pdf)

> "P — Validates and if valid, posts the transaction to the CDK Accounting General Ledger." /
> "U — Validates and if valid, uses an unattended process to post to CDK Accounting GL."
> — [glpost PDF, CDK Drive Post Accounts GL](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/2ed7a316-f952-4c81-9e2b-bc148b77c007/external/20250828224949696-jrcxa3JN.pdf)

> "CDK Drive Repair Orders API relies on the Customers API to create and use customers that
> exist in the dealers Customer Master File (CMF)... CDK Drive Service Vehicles: Create,
> update, query, and retrieve service domain vehicle information stored in CDK Drive."
> — [Customers API v1 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c0e82268-70cc-4d04-92c1-da9934800505/external/20220621170422548-uYfTqXe1.pdf)

> "The API Spec is a YAML file that acts as the contract between the API Publisher and the
> API user... Find the latest API Spec on the API page here, CDK Drive Repair Orders v1."
> — [Repair Orders v1 Dev Guide PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c7771500-1c95-4f8e-9241-eddc17cd55f6/external/20240227171600864-GvA-0CSi.pdf)

> "There are 50 auxiliary FI Sales fields (fiAux1 – fiAux50). The values of these fields are
> based on F&I configuration settings and each of these fields can contain either a prompted
> value, a constant value, or a calculated value."
> — [FI Sales History Setup v3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/638f1179-e2bf-4aac-b601-a9acc51247f8/external/20260713100351123-Zywvy7-P.pdf)

> "This API may exclude records containing personally identifiable information (PII), as
> configured by the dealer and as indicated by individual customers... Personal data sharing
> preferences are configured at the dealership level and do not affect this API's
> functionality."
> — [FI Sales Get v4 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/b54ba111-7874-4c25-b8d9-ba3b3eb722ef/external/20260713092924114-rlWrjbvB.pdf)

> "429 | Too Many Requests (rate limiting) | Issued when your API call use exceeds the
> subscribed rate limit. Make sure you are not making unnecessary calls to the server and
> examine your API call limits."
> — [glpost PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/2ed7a316-f952-4c81-9e2b-bc148b77c007/external/20250828224949696-jrcxa3JN.pdf)

---

## 4. What I searched and could not find

- **Async Parts Inventory / Search Parts Pick Ticket / Async Open/Closed Parts Sales** — no
  spec PDF located on the Fortellis S3 documents bucket or apidocs.fortellis.io under these
  names. Only forum-quoted fields (`DealerId`, `PartNumber`, `Description`, `Manufacturer`,
  `DeletePartFlag`) were found on a community.fortellis.io thread — insufficient to build a
  field dictionary and not re-verified as a primary source in this pass. `[UNK]`
- **CDK Drive Service Vehicles API** — named explicitly in both the Customers API v1 guide and
  the Repair Orders v1 Dev Guide ecosystem diagram (see quoted text above), but its own spec
  document was not located. The candidate UUID folder `54b70ee1-ac17-4be2-9314-45c947692c5d`
  probed in the S3 bucket in a prior pass of this session was confirmed **not** present in
  the public bucket listing. `[UNK]`
- **CDK Drive Workshop Management API** — named in the Repair Orders v1 Dev Guide ecosystem
  diagram, no spec located. `[UNK]`
- **Repair Orders v1 formal field-level OpenAPI YAML** — the Dev Guide explicitly defers to a
  separate YAML spec on the platform ("Find the latest API Spec on the API page here"); that
  YAML file itself was not located/downloaded in this session, only the Dev Guide's JSON
  examples (§2.7). `[UNK]`
- **Full apidocs.fortellis.io API directory enumeration** — the directory page is a
  JavaScript-rendered SPA reporting "APIs (47)" but `fetch_url`/screenshot only rendered the
  first ~10 listings; the remaining ~37 listings were not enumerated in this session. `[UNK]`
- **fortellis-parts-store-openapi_SAMPLE.yml** — downloaded, but on inspection this is a
  Fortellis developer-portal tutorial/sample OpenAPI document, not a real CDK Drive Parts API.
  Recorded as a correction (§5), not counted in the field dictionary above.

**Functional areas confirmed to have NO published API found in this pass** (itemized per the
task's point 6): Parts Inventory (async), Parts Pick Ticket, Parts Sales (open/closed async),
Service Vehicles, Workshop Management. All four/five are referenced by name in other CDK
guides' ecosystem diagrams or related-APIs notes but no retrievable spec was found for any of
them.

---

## 5. Corrections to the first spin

First-spin files referenced: `/home/user/workspace/cdk_0*.md` (skimmed only where this lane
touches).

- **`fortellis-parts-store-openapi_SAMPLE.yml` is not a real CDK Drive Parts API.** It is a
  Fortellis developer-portal tutorial/sample specification. Any first-spin claim that treated
  this YAML as evidence of a live, publicly documented CDK Parts API schema should be treated
  as unsupported.
- **glwippost and glpost are the same underlying service, not two separate accounting
  endpoints**, per the verbatim curl-URL and payload evidence in §2.6. Any first-spin listing
  that counted these as two independent accounting APIs with independent field sets should be
  corrected to note they share one schema and one service path, differing only in documented
  opCode permission tier.
- **Get Repair Order v3 (bulk/delta, `servicerepairorder/v3`) and CDK Drive History Setup
  Repair Order v2 (`servicerepairordersetup/v2`) are separately versioned services with
  distinct service URLs**, even though their record schemas are near-duplicates apart from the
  History Setup spec's unique `visitInspection` object (§2.2). They should not be collapsed
  into a single API entry.
- **CDK Drive History Setup FI Sales v3 (`fisalessetup/v3`) and CDK Drive Get FI Sales v4
  (`fisales/v4`) share an identical 16-object field schema** (verified by section-heading
  comparison, §2.9) but expose different endpoint sets (`/history` only, vs.
  `/open`, `/open/delta`, `/closed`, `/closed/delta`, `/bulk`) — they are the setup/history and
  bulk/delta variants of the same data model, analogous to the Repair Order v2/v3 pairing.

---

*End of Lane A deliverable. Raw files: `/home/user/workspace/cdk2_raw/A/`. Text extractions:
`/home/user/workspace/cdk2_raw/A/txt/`.*
