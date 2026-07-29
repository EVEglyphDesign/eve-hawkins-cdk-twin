# Lane F — CDK Drive Platform Heritage: What It Actually Is, Underneath

Prepared for: Peterbilt Atlantic digital-twin workstream (nine rooftops, Atlantic Canada, heavy truck, PACCAR/Peterbilt franchise, runs CDK Drive + Lightspeed).
Confidence tags: `[DOC]` vendor/regulator/court/OEM published, URL required · `[COMM]` practitioner/forum/training, URL + standing required · `[INF]` reasoned inference, source of reasoning stated · `[UNK]` searched, not found, location of search stated.

---

## 1. What I actually retrieved

Files downloaded to `/home/user/workspace/cdk2_raw/F/`:

| File | What it is | Source URL |
|---|---|---|
| `patent_US11514021B2_scanning_legacy_database_extract.md` | Verbatim extraction of CDK patent "Systems, methods, and apparatuses for scanning a legacy database" (assignee CDK GLOBAL, LLC; inventors Bruce Bailey, Mark Helzer; filed Jan 22 2021, granted Nov 29 2022) — confirms Pick/MultiValue legacy layer in CDK's own words, sample XML/JSON payloads, dbsync API path | [Google Patents US11514021B2](https://patents.google.com/patent/US11514021B2/en) |
| `patent_US11803535B2_parallel_databases_extract.md` | Verbatim extraction of CDK patent "Systems, methods, and apparatuses for simultaneously running parallel databases" (same assignee/inventors; filed May 24 2021, granted Oct 31 2023) | [Google Patents US11803535B2](https://patents.google.com/patent/US11803535B2/en) |
| `CDK_10K_FY2020_AnnualReportsArchive.pdf` | Full FY2020 10-K (period ended June 30 2020) PDF mirror | [AnnualReports.com](https://www.annualreports.com/HostedData/AnnualReportArchive/c/NASDAQ_CDK_2020.PDF) |
| `CDK_10K_FY2017_AnnualReportsArchive.pdf` | Full FY2017 10-K PDF mirror | [AnnualReports.com](https://www.annualreports.com/HostedData/AnnualReportArchive/c/NASDAQ_CDK_2017.pdf) |
| `CDK_Partner_Program_Price_Guide.pdf` | Official CDK 3PA/Partner Program Pricing Guide, 2 pages, © 2022 CDK Global LLC, doc code 22-5709 | [cdkglobal.com](https://www.cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf) |
| `Fortellis_CDKDrive_Customers_API_v1.pdf` | Fortellis "CDK Drive Customers API" spec PDF, 22 pages, with full field dictionary and example JSON request/response payloads (real sample names e.g. "JEFFREY DALTON," "CINDY DILDINE") | [Fortellis API Documents S3](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c0e82268-70cc-4d04-92c1-da9934800505/external/20220621170422548-uYfTqXe1.pdf) |
| `Fortellis_CDKDrive_GetCustomer_v3.pdf` | Fortellis "CDK Drive Get Customer v3" spec PDF, 28 pages, with Department-Id header requirement and DMS-type enum | [Fortellis API Documents S3](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf) |
| `DDX_report_names_verbatim.md` | Verbatim capture of CDK's Dealer Data Exchange (DDX) user-guide report table (2016 doc code 16-0280), via a third-party mirror — flagged for provenance in the table | [CourseHero mirror](https://www.coursehero.com/file/17918315/CDK-DDX-USER-GUIDE/) |

Additional primary sources opened and quoted from but not saved as separate raw files (page content captured inline below, each with its own URL): the CDK–ADP IP Transfer Agreement exhibit list (Justia Contracts), CDK Global's FY2019 10-K (SEC EDGAR direct HTML), CDK's "Data - Your Way" product page, the Microsoft Power Platform "CDK Drive Customer" connector reference page, the Fortellis "Connection Update Notifications" and "API Request and Response Components" docs pages, several ransomware post-mortem articles, and Wikipedia/WardsAuto/Daily Standard sources on the UCS/Reynolds corporate history (used for the Section 5 correction).

Patent US11616856B2 ("Systems and methods for an automotive commerce exchange," describing Fortellis architecture) was located at [Google Patents](https://patents.google.com/patent/US11616856B2/en) but not fetched in this pass — noted under Section 4 as unexplored.

---

## 2. The field/table/record dictionary

### 2a. Legacy Pick layer — from CDK's own patents

| Name as spelled | Type if stated | Meaning as stated by source | Tag | URL |
|---|---|---|---|---|
| `NAME-FILE` | Pick file | Legacy Pick data file queried for updates via dbsync URI, e.g. `http://localhost:10229/dbsync/v1/D100093794/NAME-FILE?sel=1565724886.475` | [DOC] | [US11514021B2](https://patents.google.com/patent/US11514021B2/en) |
| `service-names` | Pick file | Legacy data file combined with `NAME-FILE` and `customer comments` to assemble a Customer update message | [DOC] | [US11514021B2](https://patents.google.com/patent/US11514021B2/en) |
| `customer comments` | Pick file | As above | [DOC] | [US11514021B2](https://patents.google.com/patent/US11514021B2/en) |
| `id` (item ID) | Pick item identifier | Format `<type>*<number>`, e.g. `4*9014`, `4*11341` — "type" and sequence number joined by an asterisk, the classic MultiValue/Pick item-ID convention | [DOC] | [US11514021B2](https://patents.google.com/patent/US11514021B2/en) |
| `ts` | Unix epoch, fractional seconds | Timestamp of last update to a Pick item, e.g. `1603193254.561832` | [DOC] | [US11514021B2](https://patents.google.com/patent/US11514021B2/en) |
| `accountname` | string | Example value `"TEST-A"` in the sample XML response envelope | [DOC] | [US11514021B2](https://patents.google.com/patent/US11514021B2/en) |
| `timerangebegin` / `timerangeend` | Unix epoch | Bounds of the update-scan window in the XML response | [DOC] | [US11514021B2](https://patents.google.com/patent/US11514021B2/en) |
| `dictrequested` | boolean | Whether the Pick file's dictionary (schema) was requested alongside data | [DOC] | [US11514021B2](https://patents.google.com/patent/US11514021B2/en) |
| `domain` | string | JSON update-message field, example value `"Customer"` | [DOC] | [US11514021B2](https://patents.google.com/patent/US11514021B2/en) |
| `enterprise_id` | string | JSON field, example `"E207187"` — top-level tenant identifier | [DOC] | [US11514021B2](https://patents.google.com/patent/US11514021B2/en) |
| `store_id` | string | JSON field, example `"S100023739"` — rooftop/store identifier | [DOC] | [US11514021B2](https://patents.google.com/patent/US11514021B2/en) |
| `depts` | array | JSON field, example `["D100093794"]` — almost certainly the legacy-layer origin of the Fortellis "Department-Id" concept (see 2b) | [DOC] | [US11514021B2](https://patents.google.com/patent/US11514021B2/en) |
| `type` | string | Pick file-type code, example `"4"` | [DOC] | [US11514021B2](https://patents.google.com/patent/US11514021B2/en) |

### 2b. Fortellis API layer — CDK Drive Customer object (from Microsoft connector docs + Fortellis PDF spec)

| Name as spelled | Type if stated | Meaning as stated by source | Tag | URL |
|---|---|---|---|---|
| `customerId` | string | "The unique ID of the customer record" | [DOC] | [Microsoft Learn — CDK Drive Customer connector](https://learn.microsoft.com/en-us/connectors/cdkdrivecustomer/) |
| `name.first` / `name.last` / `name.companyName` | string | Customer or company name; `companyName` mutually exclusive with `first`/`last` | [DOC] | [Fortellis CDK Drive Customers API PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c0e82268-70cc-4d04-92c1-da9934800505/external/20220621170422548-uYfTqXe1.pdf) |
| `contactMethods.primaryPhone`, `.homePhone`, `.mobilePhone`, `.pager`, `.pagerAccessCode`, `.homeFax`, `.workFax` | string | Contact numbers for the customer | [DOC] | same as above |
| `contactMethods.email1`–`email6`, `.emailDesc1`–`.emailDesc6` | string / enum | Up to six emails; description enum `HOME`, `WORK`, `OTHER`; `email1` accepts `NA` (Non-Applicable) or `CD` (Customer Declined) | [DOC] | same as above |
| `contactMethods.preferredMethod` | enum | `PRIMARYPHONE`, `PAGER`, `HOMEFAX`, `WORKFAX`, `PRIMARYEMAIL` | [DOC] | same as above |
| `contactMethods.blockPhoneFlag` / `.blockEmailFlag` / `.blockMailFlag` | boolean | Advertising opt-out flags, default `false` | [DOC] | same as above |
| `postalAddress.street`, `.city`, `.county`, `.state`, `.postalCode`, `.country` | string | Standard postal address fields; each dealer can mark any as required | [DOC] | same as above |
| `links.self.href` / `.method` / `.title` | string | HATEOAS-style link object to the resource itself | [DOC] | same as above |
| Endpoint base path | — | `https://api.fortellis.io/cdkdrive/crm/v1/customers` | [DOC] | same as above |
| `Subscription-Id`, `Authorization`, `Request-Id` | HTTP headers | Required on every Fortellis API call; `Subscription-Id` is per-dealer-subscription, `Authorization` is an OAuth2 client-credentials Bearer token, `Request-Id` is a client-supplied correlation UUID | [DOC] | [Fortellis — API Request and Response Components](https://docs.fortellis.io/docs/general/making-calls/request-components/) |
| `Department-Id` | HTTP header | "The response data is filtered by the Department ID specified in the request. Note: The Department ID specified with this parameter must indicate a department that works with the [given] DMS type." | [DOC] | [Fortellis CDK Drive Get Customer v3 PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf) |
| `dmsType` enum | enum | `Accounting`, `Finance`, `Inventory`, `Parts`, `Service` — each Department-Id is bound to exactly one of these | [DOC] | [Fortellis — Connection Update Notifications](https://docs.fortellis.io/docs/tutorials/admin-api/connection-update-notifications/) |
| `ETag` / `If-Match` | HTTP headers | Optimistic-concurrency-control checksums on update requests | [DOC] | [Fortellis CDK Drive Customers API PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/c0e82268-70cc-4d04-92c1-da9934800505/external/20220621170422548-uYfTqXe1.pdf) |

### 2c. Enhanced Report Generator / Report Builder in-DMS field names (practitioner-documented, cross-checked)

| Name as spelled | Type if stated | Meaning as stated by source | Tag | URL |
|---|---|---|---|---|
| `ItemID` | field | Report column | [COMM] Clarivoy (CDK-integration vendor support doc, practitioner-authored setup instructions) | [Clarivoy support](https://clarivoy.helpjuice.com/en_US/cdk-setting-up-dms-sales-reports) |
| `ACCOUNTING DATE` | field | Used as the date-range selection-criteria field, with `GREATER THAN OR EQUAL TO` / `LESS THAN OR EQUAL TO` conditions | [COMM] same | same |
| `BUYER FIRST NAME`, `BUYER LAST NAME`, `BUYER STREET ADDRESS`, `BUYER CITY`, `BUYER STATE`, `BUYER ZIP CODE`, `BUYER CELL`, `BUYER BUSINESS TELEPHONE`, `BUYER HOME TELEPHONE` | fields | Buyer contact/address fields | [COMM] same | same |
| `E-MAIL ADDRESS 1/2/3`, `CO-BUYER NAME`, `CO-BUYER STREET ADDRESS`, `CO-BUYER CITY`, `CO-BUYER STATE`, `CO-BUYER ZIP CODE`, `COBUYER CELL` | fields | Email/co-buyer fields | [COMM] same | same |
| `BACK GROSS`, `FRONT GROSS`, `TOTAL GROSS`, `TOTAL SELLING PRICE`, `SALES TYPE` | fields | Deal financial/type fields | [COMM] same | same |
| `SERIAL NUMBER-NEW`, `MAKE DESCRIPTION-NEW`, `MODEL DESCRIPTION-NEW`, `MODEL YEAR-NEW`, `STOCK TYPE-NEW` | fields | Vehicle fields, "-NEW" suffix pattern | [COMM] same | same |
| Menu path | screen names | `Login to CDK drive` → right-side icon menu `REPORT AND ANALYZE` (pie-chart icon) → `ENHANCED REPORT GENERATOR` under "General" → `NEW REPORT` → `Select Application` = `FINANCE AND INSURANCE` → `File Name` = `FI-WIP` → left panel `Dictionary Library` → top panel `Report Columns` → `Selection Criteria` → `SAVE` / `RUN` / `EXPORT CSV` / `MODIFY REPORT` | [COMM] same | same |
| Report Builder screens (different tool, seen at a Lithia-branded connectCDK help subdomain) | screen names | `Report Builder` main screen → `Create` → `Business Data` screen → `Select Report Layout` screen (Title, Description, Report Header, Public/Private report, field checklist) → `Select Report Filter` screen (Condition, Value, and/or, Prompt box) → `Group and Summary` screen (Group, Sum, Average, Count) → `Select Sort` screen (Ascending/Descending) → `Save` / `Run` | [DOC] hosted on a `connectcdk.com` help subdomain branded for the "Lithia" dealer group — this is CDK's own hosted help content, reached via a customer-specific URL | [connectCDK help](https://lithia.vehicle.connectcdk.com/pid1033/help/client/scr-reportbuilder/tasks/veh_tk_reportbuilder_creating_a_report.htm) |

Note on naming: the source material uses "Enhanced Report Generator" (Clarivoy instructions, current-dated to 2025 report examples) and "Report Builder" (connectCDK help page) — these read as two distinct in-DMS report tools, or possibly the same tool renamed/rebranded between versions. Not resolved — see Section 4.

### 2d. 3PA / extract-fee schedule (verbatim, from CDK's own published PDF)

| Package name as spelled | Price (per dealer/month) | Extracts included | Writebacks included | Tag | URL |
|---|---|---|---|---|---|
| SERVICE APPOINTMENT | $285 (first app.) + $100/additional app. | Service Customers, Service Vehicles, Service Appointments, Op Codes, Open Repair Orders, Closed Repair Orders | Service Customers, Service Vehicles, Service Appointments (limited) | [DOC] | [CDK Partner Program Pricing Guide](https://www.cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf) |
| FRONT OFFICE | $285 (first app.) + $100/additional app. | Customers, Vehicle Inventory, Pending Deals, Finalized Deals, Closed Repair Orders | Customers, Pending Deals (to F&I or CDK Desking), CDK Credit | [DOC] | same |
| F&I MENU/AFTERMARKET PRODUCT SALES | $230 | Pending Deals, Finalized Deals, We Owes | Pending Deals, We Owes — Update Only | [DOC] | same |
| VEHICLE MERCHANDISING | $110 | Vehicle Inventory (incl. CDK-managed syndication of data) | Vehicle Inventory — Pricing Updates | [DOC] | same |
| CUSTOMER WRITEBACK | $65 | Customers | Customers | [DOC] | same |
| PARTS E-COMMERCE — BASIC | $90 | Parts Inventory, Pricing and Availability | Parts Quote/Invoice | [DOC] | same |
| PARTS E-COMMERCE — PREMIUM | $175 (+$100 if EPC integration) | Parts Inventory, Pricing and Availability, Parts Customer, Parts Sales, Part Number Lookup, Open Repair Orders | Parts Quote/Invoice, Parts Special Orders | [DOC] | same |
| PAYROLL | $105 | Accounting GL, Employee, ETC Timecard Totals | Accounting GL | [DOC] | same |
| BODY SHOP | $180 | "Ability to integrate Body Shop Management stand-alone applications" | — | [DOC] | same |
| BUY HERE/PAY HERE | $90 | "Ability to integrate Buy Here/Pay Here applications" | — | [DOC] | same |
| DSDA INSERT | $65 | "Ability to insert documents into CDK Document Storage/Document Archive products" | — | [DOC] | same |
| FLUID MANAGEMENT | $95 | "Ability to integrate Fluid Management applications" | — | [DOC] | same |
| VEHICLE LOANERS/RENTALS | $70 | "Ability to integrate Vehicle Loaners/Rentals" | — | [DOC] | same |
| VEHICLE RECONDITIONING | $180 | "Ability to integrate Vehicle Reconditioning" | — | [DOC] | same |
| PARTS INVENTORY PLANNING | $46 | "Ability to integrate Parts Inventory Planning" | — | [DOC] | same |
| PARTS STORAGE | $175 | "Integration to Parts Storage applications" | — | [DOC] | same |
| PARTS DEALER AS BUYER | $90 | "Ability for dealers to buy parts from aftermarket parts providers" | — | [DOC] | same |
| BASE EXTRACT-ONLY FEE | $28 | Per application, before add-ons | — | [DOC] | same |
| ADD-ON FEE PER DATA TYPE | $23 | e.g. "Vehicle Inventory, Closed Repair Orders, Finalized Deals" | — | [DOC] | same |
| SALES REPORTING (extract package) | $81 | Finalized Deals, Sales Vehicles, Sales Customers, We Owes, Employees and Helpers | — | [DOC] | same |
| SERVICE REPORTING (extract package) | $81 | Closed Repair Orders, Service Vehicles, Service Customers, Inventory Vehicles, Employees and Helpers | — | [DOC] | same |
| AFTERMARKET PRODUCT SALES (extract package) | $101 | Finalized or Pending Deals | — | [DOC] | same |
| ELECTRONIC VEHICLE REGISTRATION (extract package) | $150 | Finalized Deals, Customers and Vehicles | — | [DOC] | same |

Document footer: `© 2022 CDK Global, LLC / CDK Global is a registered trademark of CDK Global, LLC. 22-5709` — dating this specific price list to 2022. `[DOC]` [CDK Partner Program Pricing Guide PDF](https://www.cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf), also saved at `/home/user/workspace/cdk2_raw/F/CDK_Partner_Program_Price_Guide.pdf`.

Superseding/complicating fact: CDK's 2020 "Customer Rewards Program" press release states CDK began "the elimination of most third-party data access fees through the CDK Partner Program for eligible customers" `[DOC]` [Business Wire, Feb 15 2020](https://www.businesswire.com/news/home/20200215005009/en/CDK-Global-Introduces-New-Pricing-Structure-With-its-Customer-Rewards-Program) — meaning the 2022 price sheet above may not reflect what a "Customer Rewards Program" enrolled dealer (or their 3PA vendor) actually pays; whether Peterbilt Atlantic dealerships are enrolled is `[UNK]`.

### 2e. Dealer Data Exchange (DDX) reports (verbatim, 2016-dated user guide)

| Reporting Name (verbatim) | Description (verbatim) | Tag | URL |
|---|---|---|---|
| Syndication by Program | "Provides a list of successful data exports to OEMs and Third Parties by Program" | [DOC]-adjacent — see provenance note | [CourseHero mirror of CDK DDX User Guide](https://www.coursehero.com/file/17918315/CDK-DDX-USER-GUIDE/) |
| Syndication by Dealer | "Provides a list of successful data exports to OEMs and Third Parties by individual dealership" | same | same |
| Syndication History | "Provides a list of all data exports to OEMs and Third Parties including failed exports" | same | same |
| Syndication Enrollments | "Provides a list of all enrolled OEM and Third Party programs" | same | same |
| Third-Party Access Enrollments | "Provides a list of all Third-Party Access enrolled programs" | same | same |
| Third-Party Access Transactions | "Provides a list of all Third-Party Access program successful transactions" | same | same |
| DCS Transactions | "Provides a log of transactions that occur between the DMS and OEM applications" | same | same |
| Non-Authorized Access | "Provides a list of non-authorized user IDs used to access the DMS and extract data" | same | same |
| Non-CDK Code on the DMS | "Provides a list of Non-CDK installed code on the DMS that may be used to extract data" | same | same |
| FTP Activity | "Provides a log of FTP transfers between the DMS and external servers" | same | same |

Provenance caveat, stated once here and not repeated: this table was retrieved from a CourseHero mirror of a CDK-authored PDF, not from a CDK-controlled URL. The document's own footer text (visible in the mirror) reads "© 2016 CDK Global, LLC ... cdkglobal.com 16-0280," which is internally consistent with a real CDK publication, but no live cdkglobal.com copy was found to cross-verify. Treat the report names/descriptions as high-confidence but not independently re-confirmed on a CDK-controlled domain.

DDX is confirmed to still exist as a current product: `[DOC]` [CDK Dealer Data Exchange (DDX) product page](https://www.cdkglobal.com/dealership-operations/data-management/cdk-dealer-data-exchange), which states "With CDK Drive, DMS clients get unrivaled control for how data is shared, at no additional cost" and "Know where your data is and with whom it's being shared with DDX." DDX is also named on the CDK Heavy Truck product page: `[DOC]` [CDK Drive DMS Heavy Truck](https://www.cdkglobalheavytruck.com/heavy-truck-dms/drive-dms-heavy-truck) — "Dealer Data Exchange (DDX) — Review all data with DDX."

---

## 3. Verbatim quotes worth keeping

### Platform architecture / hosting model — SEC 10-Ks (CDK's own regulatory language)

> "Our flagship Dealer Management System ('DMS') software solutions are hosted enterprise resource planning applications tailored to the unique requirements of the retail automotive industry."
`[DOC]` FY2020 10-K, [AnnualReports.com PDF mirror of SEC filing](https://www.annualreports.com/HostedData/AnnualReportArchive/c/NASDAQ_CDK_2020.PDF), saved at `/home/user/workspace/cdk2_raw/F/CDK_10K_FY2020_AnnualReportsArchive.pdf`.

> "...we have developed Drive Flex, a cloud-based DMS."
`[DOC]` same source, Product Development and Innovation section.

> "DMSs and layered applications, which may be installed on-site at the customer's location, or hosted and provided on a SaaS basis, including ongoing maintenance and support"
`[DOC]` FY2019 10-K, [SEC EDGAR direct filing](https://www.sec.gov/Archives/edgar/data/1609702/000160970219000015/cdkq4fy1910-k.htm).

> "Dealer Management Systems ('DMSs') are enterprise technology solutions that provide an integrated suite of features and services that enable our customers to manage the information systems and process workflows involved in running automotive retail operations."
`[DOC]` FY2017 10-K, [AnnualReports.com PDF mirror](https://www.annualreports.com/HostedData/AnnualReportArchive/c/NASDAQ_CDK_2017.pdf), saved at `/home/user/workspace/cdk2_raw/F/CDK_10K_FY2017_AnnualReportsArchive.pdf`.

> "The Company entered into a data services agreement with ADP prior to the spin-off under which ADP will provide the Company with certain data center sharing services relating to the provision of information technology, platform support, hosting and network services."
`[DOC]` FY2017 10-K, same source. This confirms CDK's post-spinoff (2014) hosting was contractually tied to ADP-shared data centers for a transition period, and is the closest the 10-Ks come to naming actual hosting infrastructure.

> "Prior to the spin-off, certain systems development functions were outsourced to an ADP shared services facility located in India."
`[DOC]` FY2017 10-K, same source.

> "The Company performed these functions using internal resources or purchased services, certain of which were provided by ADP during a transitional period that ended September 30, 2015 pursuant to the transition services agreement."
`[DOC]` FY2017 10-K, same source.

None of the retrieved 10-K language names a specific database engine (Oracle, SQL Server, AIX) or a specific data-center provider by name for the core Drive DMS — see Section 4 for what was searched and not found.

### Legacy database architecture — CDK's own patents

> "A Pick environment includes an operating system for databases that was developed decades ago."
`[DOC]` US Patent 11,514,021 B2, assignee CDK GLOBAL, LLC, [Google Patents](https://patents.google.com/patent/US11514021B2/en).

> "The Pick environment has an architecture with a centralized dealer management system 110 with applications and a legacy Pick database 102."
`[DOC]` same source.

> "The update decipherer 210 may be able to search for Pick files, items within the Pick files, and the timestamps stored with items."
`[DOC]` same source.

> "the update decipherer 210 may send a URI, such as http://localhost:10229/dbsync/v1/D100093794/NAME-FILE?sel=1565724886.475, to the sync tool 208."
`[DOC]` same source — a literal, citable, internal API path pattern from CDK's own patent filing.

> "In some embodiments, the update message 212 may use Kafka messaging to send information from the legacy system to the new microservice system."
`[DOC]` same source — confirms CDK's modernization layer is Kafka-based event streaming bridging the Pick legacy core.

### 3PA program — CDK's own pricing philosophy language

> "Our pricing philosophy is simple: standardized pricing for all partners. Our goal? To provide the most secure way to access CDK systems while delivering efficient integration and marketing advantages."
`[DOC]` [CDK Partner Program Pricing Guide PDF](https://www.cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf).

> "Note: Prices are per dealer, per month, and are subject to change... Other program fees per partner application include a one-time upfront development fee and a one-time per dealer setup fee. Pricing is exclusive to CDK data access services and does not include Managed Data Services."
`[DOC]` same source.

### Data Export Tool / Data Export-Import Tool — CDK's current no-fee extract paths

> "CDK offers a powerful tool for dealers to export data from CDK products to their in-house data systems via SFTP. Dealers can securely export data across all their CDK dealerships using a common UI and PGP encryption... A comprehensive understanding of CDK file structure and dealership operations is required, and users must have the ability to create an in-house data warehouse to store the data they extract."
`[DOC]` [CDK "Data - Your Way" product page](https://www2.cdkglobal.com/data-your-way).

> "For dealers who have a need for more workflow-driven integration, our Export/Import tool will allow you to export and import data directly into the CDK Drive DMS across your dealership locations. The Data Export/Import tool is available through a variety of packages for our Legacy APIs to support operations across each desired department. This tool best serves dealers who have resources with SOAP API knowledge... Requires comprehensive knowledge base of CDK files structure, dealership operations, and automotive retail data types."
`[DOC]` same source. This is a direct, dated (page still live) confirmation that CDK's own "Legacy APIs" are SOAP-based, distinct from the newer Fortellis REST layer, and that CDK explicitly warns integrators they need deep internal-file-structure knowledge — corroborating the patent evidence of a non-trivial legacy record layout underneath.

> "No Fees From CDK - CDK is eliminating our license fees to dealers to use these tools, and your ISVs pay no CDK fees when you share your data with them directly."
`[DOC]` same source.

### CDK Drive Flex — the "other" DMS product, and why it is not what a nine-rooftop heavy-truck dealer runs

> "The new DMS, being called DriveFlex, will be built from the ground up on the Amazon Web Services Cloud platform... The new system comes with the typical termed contract but with a unique monthly pricing model which will be based on how many vehicles the dealer sells, how many repair orders are written and on the number of licensed users."
`[COMM]` [The Banks Report, auto-retail trade press, Mar 8 2018](https://thebanksreport.com/news/cdk-introduce-dms-flex-pricing-smaller-dealer-groups/).

> "CDK Drive Flex is an innovative web-based DMS perfect for dealers with just one or two locations... Drive Flex is available on Amazon Web Services (AWS) for a reliable and secure experience."
`[COMM]` quoting CDK Global CEO Brian MacDonald, via [Trucks, Parts, Service trade press, Mar 9 2018](https://www.truckpartsandservice.com/economic-trends/indicators/article/14987597/cdk-global-adds-to-dealer-management-system-offering.html).

> "Operating with web-based architecture, Drive Flex allows secure, 256-bit encrypted access from any internet connected device, helping to reduce infrastructure costs and provide greater operating flexibility."
`[COMM]` [MarketScreener, quoting a CDK Global press release, Jan 23 2019](https://www.marketscreener.com/quote/stock/CDK-GLOBAL-INC-18052701/news/CDK-Global-Inc-Announces-the-Next-Generation-of-the-Dealer-Management-System-Drive-Flex-34449166/).

**Reading for Peterbilt Atlantic:** Drive Flex is explicitly targeted at "one or two locations" and is AWS-hosted with a ground-up rewrite. A nine-rooftop heavy-truck operation is far outside that stated target market. The CDK Heavy Truck product page names the product simply "CDK Drive" / "CDK Drive for Heavy Truck," never "Drive Flex" — `[DOC]` [CDK Drive DMS Heavy Truck](https://www.cdkglobalheavytruck.com/heavy-truck-dms/drive-dms-heavy-truck). `[INF]`, reasoned from those two facts together: Peterbilt Atlantic is almost certainly running standard (legacy-lineage, Pick-underpinned) CDK Drive, not Drive Flex — meaning the Pick/legacy-layer patent evidence above is the architecturally relevant one for this twin, not the AWS/Drive-Flex path. This has not been confirmed against Peterbilt Atlantic's own contract or a dealer-login screen, which would be the only way to settle it definitively.

### Ransomware incident — architecture evidence, not merely event timeline

> "the reported 'always-on VPN' tunnel that dealerships must configure to access CDK's data centers"
`[DOC]` [ExtraHop, "CDK Global Ransomware Attack Sends Shockwaves," Jul 10 2024](https://www.extrahop.com/blog/CDK-Global-Ransomware-Attack-Sends-Shockwaves), itself citing Bleeping Computer reporting.

> "This arrangement enables auto dealers' 'locally installed applications to access the platform'"
`[DOC]` same source.

> "the dealer-to-CDK VPN link presents the risk that BlackSuit, using human and non-human credentials such as API keys or session IDs compromised in the first breach, could penetrate external networks and unleash downstream ransomware attacks on CDK's customers."
`[DOC]` same source.

**Reading:** this is the one piece of hard evidence, outside CDK's own marketing, that a dealership's on-site "locally installed applications" (i.e., the client software a dealer's workstations run) reach CDK's hosted DMS core over a dedicated, always-on, dealer-configured VPN tunnel into CDK data centers (plural, unnamed) — consistent with a hosted/multi-tenant-per-dealer-group architecture rather than a public multi-tenant SaaS model with no dedicated network path. This is `[DOC]` in the sense that ExtraHop is a cybersecurity vendor publishing analysis, not CDK itself — treat as strong secondary reporting, not CDK's own statement.

> "Blacksuit operators demonstrated a sophisticated understanding of data center architecture by targeting VMware ESXi servers... By attacking the hypervisor, Blacksuit would then bypass traditional security agents that reside only within guest virtual machines."
`[COMM]` [ExtraHop, "CHAOS in a BLACKSUIT," on BlackSuit's general tradecraft](https://www.extrahop.com/blog/chaos-in-a-blacksuit-triple-extortion-ransomware) — this describes BlackSuit's general modus operandi across victims, not a CDK-specific confirmation that CDK ran VMware ESXi. Tagged `[COMM]`/general threat-intel, not `[DOC]` for CDK specifically, because the article does not state CDK's environment used ESXi — it is generic BlackSuit tradecraft reporting.

> "BlackSuit primarily targets Linux and Windows systems, and prevents victims from accessing their files by encrypting them."
`[DOC]` [U.S. HHS HC3 Analyst Note on BlackSuit Ransomware](https://www.hhs.gov/sites/default/files/blacksuit-ransomware-analyst-note-tlpclear.pdf) — a federal health-sector threat-intel bulletin, general to BlackSuit as a strain, not CDK-specific.

No source found that states explicitly which hypervisor, cloud provider, or specific data-center operator hosted CDK Drive's production environment at the time of the June 2024 attack — see Section 4.

### Corporate history correction context — UCS / Reynolds and Reynolds (kept here for completeness; full correction in Section 5)

> [Reynolds and Reynolds was acquired by Universal Computer Systems, Inc. (UCS), led by Robert Brockman, in a deal completed in October 2006, for approximately $2.8 billion; the Reynolds and Reynolds name was retained and the UCS name was retired.]
`[DOC]` (paraphrased from) [Wikipedia — Reynolds and Reynolds](https://en.wikipedia.org/wiki/Reynolds_and_Reynolds) and [Wikipedia — Robert Brockman](https://en.wikipedia.org/wiki/Robert_Brockman).

---

## 4. What I searched and could not find

- **A named database engine or OS for the current production CDK Drive core** (e.g. explicit "Oracle," "SQL Server," "IBM AIX," or a named Pick/MultiValue product such as UniData, UniVerse, jBASE, or D3). Searched: SEC 10-K full text (FY2017, FY2019, FY2020) for "Oracle," "SQL Server," "AIX," "Unix," "database" — the 10-Ks discuss hosting/SaaS/data-center-sharing arrangements but never name a specific database product or operating system for the DMS core. The word "Pick" and the architecture it implies come only from CDK's own 2021–2023-filed patents, not from any 10-K, press release, or SEC filing. `[UNK]`.
- **A named hypervisor, cloud provider, or specific data-center operator/location for CDK Drive's production hosting**, either in general or specifically at the time of the June 2024 BlackSuit attack. Searched: "CDK Global data center location," "CDK Global AWS Azure hosting," ransomware post-mortem articles (ExtraHop, CRN, Cybersecurity Dive, Reuters, CNN, SecurityWeek, BlackFog, dataconomy, kapacyber, fairtprm). Found only "data centers" (plural, unnamed) and an "always-on VPN" tunnel description; no named provider, no named facility, no confirmation of on-prem-owned vs. colocation vs. public cloud for the Drive (non-Flex) product specifically. `[UNK]`.
- **A formal technical post-mortem or root-cause disclosure from CDK itself** about the June 2024 attack. CDK's own public statements (quoted across CRN, Cybersecurity Dive, etc.) describe recovery phasing and timelines but not the initial access vector, the exploited vulnerability, or internal architecture. Searched: "CDK Global ransomware root cause report," "CDK Global BlackSuit technical disclosure," "CDK Global SEC 8-K cybersecurity incident report." `[UNK]` — no such document located; class-action complaints allege inadequate security but do not supply architecture detail beyond what is already quoted above.
- **Whether "Enhanced Report Generator" and "Report Builder" are the same tool, two names for the same tool across versions, or genuinely two different tools.** Searched: "CDK Drive Enhanced Report Generator vs Report Builder," "CDK Drive report writer name history." Found both names in independent, credible sources (Clarivoy support docs referencing 2025-dated report examples; a `connectcdk.com`-hosted help page for the "Lithia" dealer group) but no CDK document reconciling or distinguishing the two names. `[UNK]`.
- **A CDK-published, field-level data dictionary for the legacy Pick file layer** (i.e., an official schema reference naming every Pick file and its fields, analogous to the Fortellis API's published JSON schemas). Searched: "CDK Drive file layout documentation," "CDK Drive Pick file dictionary," "CDK Global file structure reference." Only the patent-derived sample field names (`NAME-FILE`, `enterprise_id`, `store_id`, `depts`, etc.) and DMS-generated report-column names (`BUYER FIRST NAME` etc., which are report-tool output labels, not necessarily literal underlying file/field names) were found. `[UNK]` — this level of detail (the literal Pick file names and their internal field lists, comparable to what the patent showed for `NAME-FILE`) would very likely require a dealer login to CDK Drive's "Dictionary Library" screen itself, per the Clarivoy instructions, which describes but does not enumerate that dictionary's full contents.
- **ODBC or direct-database access as a published CDK offering.** Searched: "CDK Drive ODBC," "CDK Global direct database access," "CDK 3PA ODBC connection." No CDK-published ODBC driver, connection string format, or direct-database-access program was found. The closest analog found is the SFTP-based "Data Export Tool" and the SOAP-based "Data Export/Import Tool" (Section 3), neither of which is ODBC/direct-database access in the traditional sense. `[UNK]`.
- **CDK patent US11616856B2** ("Systems and methods for an automotive commerce exchange," describing Fortellis architecture) was located ([Google Patents](https://patents.google.com/patent/US11616856B2/en)) but not fetched/transcribed in this research pass due to time. Noted as an unexplored lead, not a negative finding.
- **A CDK-hosted (not third-party-mirrored) copy of the DDX user guide.** Searched: "site:cdkglobal.com DDX user guide," "CDK Dealer Data Exchange user guide PDF." Only the CourseHero mirror (Section 2e) was found; current CDK marketing pages describe DDX's existence and purpose but do not republish the 2016 report-list document. `[UNK]` for a first-party-hosted copy.
- **Brookfield take-private materials beyond the merger agreement's per-share price term and the 6-K business-acquisition report.** The merger agreement itself ([SEC EDGAR](https://www.sec.gov/Archives/edgar/data/1609702/000160970222000021/cdk_q3fy228-kexhibit21.htm)) and the tender-offer Schedule TO amendment ([SEC EDGAR](https://www.sec.gov/Archives/edgar/data/1609702/000110465922058052/tm2213233d3_sctota.htm)) were located via search but their technology/architecture-relevant content (if any — merger agreements of this type rarely discuss product architecture) was not deeply mined in this pass, since these are deal-mechanics documents, not technical disclosures. Financial/deal-structure terms were captured (Section 3 of the earlier research, preserved from the prior turn: $54.87/share, $8.3B total enterprise value, 30% premium, closed July 6 2022, Brookfield holds 100% voting / initially 48% economic interest per the 6-K). No architecture-relevant content found in the deal documents themselves — this is expected, not a gap. `[UNK]` only in the narrow sense that a full line-by-line read of the merger agreement exhibit was not performed.

---

## 5. Corrections to the first spin

The first-spin file `/home/user/workspace/cdk_01_platform.md` was skimmed for lane-relevant parts.

**Correction 1 — the task brief's own premise about UCS/Power is factually wrong, and the first-spin file does not contain this correction.** The Lane F task brief states: "the Universal Computer Systems / UCS 'Power' lineage that CDK also absorbed." This did not happen. Universal Computer Systems, Inc. (UCS), led by Robert Brockman, acquired **Reynolds and Reynolds** — CDK's direct competitor — in a deal completed October 2006 for approximately $2.8 billion; the UCS "Power" DMS product continued life under the Reynolds and Reynolds brand, not under ADP/CDK. `[DOC]` [Wikipedia — Reynolds and Reynolds](https://en.wikipedia.org/wiki/Reynolds_and_Reynolds); `[DOC]` [Wikipedia — Robert Brockman](https://en.wikipedia.org/wiki/Robert_Brockman); `[COMM]` [WardsAuto, "The Low-Profile Guy Behind the UCS Hookup"](https://www.wardsauto.com/retail/the-low-profile-guy-behind-the-ucs-hookup); `[COMM]` [Daily Standard, Aug 8 2006](https://www.dailystandard.com/date/2006/08/08/news/headline2.htm). Reynolds and Reynolds remains CDK's principal competitor today in the DMS duopoly (~40% CDK vs. ~30% Reynolds market share per academic analysis) — `[COMM]` [Columbia Business School case analysis](https://business.columbia.edu/sites/default/files-efs/imce-uploads/Brian%20Waterhouse%20-%20CDK.pdf). No credible source found linking UCS or its "Power" product to CDK's or ADP's corporate lineage at any point. This means: **any digital-twin architecture assumption built on "CDK absorbed UCS/Power" is unsupported and should be discarded.** CDK's real, documented lineage is ADP Dealer Services (formed 1973, itself built from National Inventory Control System + Computer System Inc.), plus 30+ further acquisitions over 41 years, spun off as CDK Global on October 1, 2014 — the name "CDK" derives from **C**obalt (Cobalt Digital Marketing, acquired 2010) + **D**ealer Services + **K**erridge (Kerridge Computer Company, UK, acquired 2005). `[DOC]` [Wikipedia — CDK Global](https://en.wikipedia.org/wiki/CDK_Global); `[DOC]` [Wikipedia — ADP (company)](https://en.wikipedia.org/wiki/ADP_(company)).

**Correction 2 — the first-spin file's treatment of the Pick/MultiValue question was speculative; this pass found direct primary-source confirmation.** The task brief itself frames the underlying file system as something "reports variously mention" — i.e., unconfirmed at the time of the brief. This pass found two CDK-assigned, CDK-inventor patents (US11,514,021 B2 and US11,803,535 B2, filed 2021, granted 2022–2023) that state outright, in CDK's own patent language: "A Pick environment includes an operating system for databases that was developed decades ago," and "The Pick environment has an architecture with a centralized dealer management system 110 with applications and a legacy Pick database 102." `[DOC]` [US11514021B2](https://patents.google.com/patent/US11514021B2/en). This upgrades the Pick/MultiValue claim from rumor to documented fact, sourced directly from CDK Global, LLC's own patent filings — not from a forum post or an integrator's guess. Any prior file that hedged this as unconfirmed should be updated to cite these two patents directly.

**Correction 3 — the first-spin 3PA fee citations should be treated as re-verified, not re-derived, and are now supplemented with the actual downloaded PDF.** The first-spin file's citation of `https://www.cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf` was checked against a fresh fetch in this pass; the URL is live and the PDF content matches (Section 2d above is the full verbatim transcription, and the file itself is now saved at `/home/user/workspace/cdk2_raw/F/CDK_Partner_Program_Price_Guide.pdf`, which the first spin apparently cited but did not download). The 2020 fee-waiver context (CDK's "Customer Rewards Program") was independently found and added in this pass (Section 2d) — if the first spin did not carry this caveat, it should be added, since without it the 2022 price sheet may overstate what a given dealer group actually pays.

**Correction 4 — Drive Flex vs. standard Drive is now more precisely bounded.** If the first-spin file discusses Drive Flex at all, this pass adds a specific, sourced boundary: Drive Flex is stated by CDK's own CEO (via trade press) to be "perfect for dealers with just one or two locations," built "from the ground up" on AWS. `[COMM]` [Trucks, Parts, Service, Mar 9 2018](https://www.truckpartsandservice.com/economic-trends/indicators/article/14987597/cdk-global-adds-to-dealer-management-system-offering.html). A nine-rooftop heavy-truck dealer group falls well outside that stated target segment, and CDK's own Heavy Truck product page names the product simply "CDK Drive" — never "Drive Flex." `[DOC]` [CDK Drive DMS Heavy Truck](https://www.cdkglobalheavytruck.com/heavy-truck-dms/drive-dms-heavy-truck). This is an `[INF]` conclusion (Peterbilt Atlantic is on legacy-lineage Drive, not Drive Flex), not a confirmed fact — no source states Peterbilt Atlantic's product edition directly.

No other corrections identified; other lane-relevant claims in the first-spin file (Fortellis API architecture, header contracts, the 2024 ransomware timeline) were consistent with what this pass independently found and are not contradicted.

---

## Summary defensible statement of the platform stack

- **Legacy core:** a MultiValue/Pick-style database ("Pick environment," "legacy Pick database"), confirmed in CDK's own 2021–2023 patent filings, with file-based storage (e.g. `NAME-FILE`), item IDs in `<type>*<number>` format, and a `dbsync`-named internal HTTP sync API. `[DOC]`
- **Modernization layer:** a microservice architecture bridging the Pick core, using Kafka messaging for update propagation, per the same patents. `[DOC]`
- **External API layer:** Fortellis — a REST/OAuth2 API marketplace with a `Department-Id` header concept that traces conceptually to the legacy `depts` field seen in the patent's JSON payloads, and enum-typed DMS domains (`Accounting`, `Finance`, `Inventory`, `Parts`, `Service`). `[DOC]` / `[INF]` (the trace-back from `depts` to `Department-Id` is reasoned, not stated by CDK as a direct lineage).
- **Legacy/SOAP API layer:** CDK's own "Legacy APIs," exposed via the free "Data Export/Import Tool," explicitly described by CDK as requiring "SOAP API knowledge." `[DOC]`
- **Bulk/file-based exit path:** the free "Data Export Tool," SFTP-delivered, PGP-encrypted, covering "Service, Sales, Parts and Accounting data." `[DOC]`
- **Fee-based exit path:** the 3PA program, with a published per-dealer-per-month fee schedule for named extract/writeback packages (Section 2d), subject to a 2020 fee-waiver program of unclear present-day scope for any specific dealer. `[DOC]` + `[UNK]` on current applicability.
- **In-DMS report tools:** "Enhanced Report Generator" and/or "Report Builder" (relationship between the two names unresolved), both producing user-defined, exportable-to-CSV/Excel reports drawn from a "Dictionary Library" of named fields. `[COMM]` / `[DOC]`
- **Transparency/audit tool:** Dealer Data Exchange (DDX), a free, CDK-published report suite tracking syndication, 3PA transactions, non-authorized access, non-CDK code, and FTP activity. `[DOC]` for current existence; `[DOC]-adjacent` for the specific 2016 report-name list.
- **Product edition for a nine-rooftop heavy-truck dealer:** standard CDK Drive (branded "CDK Drive for Heavy Truck" in that vertical), not Drive Flex — Drive Flex is AWS-hosted and explicitly scoped to one-to-two-rooftop operations. `[DOC]` + `[INF]` for the specific applicability conclusion.
- **Hosting topology:** hosted, SaaS-delivered, accessed by dealers over an "always-on VPN" tunnel into CDK data centers (plural, unnamed); no named cloud provider, hypervisor, or specific facility confirmed for the core Drive product. `[DOC]` for the VPN-tunnel fact; `[UNK]` for the specific infrastructure.
- **Database/OS for the core product, in exact vendor terms (Oracle/SQL Server/AIX):** not found in any SEC filing, patent, or press material. The only concrete, sourced architectural claim is "Pick environment" from CDK's own patents. `[UNK]` beyond that.

---

*Report compiled 2026-07-29. All URLs above were fetched live during this research session; PDF/document artifacts are saved under `/home/user/workspace/cdk2_raw/F/`.*
