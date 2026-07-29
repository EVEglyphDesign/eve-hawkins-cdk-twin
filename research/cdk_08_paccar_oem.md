# Lane 8 — PACCAR and OEM Integration Surface

Client context: EVEglyphDesign's sovereign digital twin of CDK Drive for Peterbilt Atlantic
(9-site Peterbilt/PACCAR heavy-truck dealer group, Atlantic Canada). Thesis: the twin extends
the PACCAR platform rather than replacing the DMS; PACCAR's own systems ledger is SAP. This
lane maps the seam between dealer DMS and manufacturer.

## 1. PACCAR as an enterprise and its own systems

`DOCUMENTED`: PACCAR Inc's principal divisions are Kenworth, Peterbilt, DAF, PACCAR Parts, and
PACCAR Financial Services, plus PACCAR's own engine/powertrain manufacturing, confirmed in the
[2023 PACCAR Annual Report](https://www.paccar.com/media/pvzjr4ps/2023-annual-report-final.pdf)
and [PACCAR 2025 10-K coverage](https://www.stocktitan.net/sec-filings/PCAR/10-k-paccar-inc-files-annual-report-35e7cb3a77b7.html),
which report segment revenue for Truck ($19.37B, 68% of 2025 revenue), Parts ($6.87B), and
Financial Services ($2.21B).

| Division | Role | Source |
|---|---|---|
| Peterbilt | Truck OEM (US/Canada) | [Peterbilt dealer network](https://www.peterbilt.com/why-peterbilt/dealer-network) |
| Kenworth | Truck OEM (US/Canada) | [PACCAR annual report](https://www.paccar.com/media/pvzjr4ps/2023-annual-report-final.pdf) |
| DAF | Truck OEM (Europe) | [DAF PACCAR Connect support](https://www.daf.co.uk/en-gb/daf-services/connected-services/support) |
| PACCAR Parts | Global aftermarket parts distribution, 18-20 PDCs | [PACCAR Parts network](https://www.paccarparts.com/network/) |
| PACCAR Financial | Retail/wholesale finance | [PACCAR Financial](https://paccarfinancial.com/customer-service/frequently-asked-questions/login/) |

**PACCAR's internal SAP footprint — `DOCUMENTED`:**

| System / product | Evidence | Source |
|---|---|---|
| SAP S/4HANA (core ERP, run on IBM Power/HANA) | IBM case study: PACCAR "purchased SAP S/4HANA" and runs it on IBM Power Systems (E870/E880C/E980), 2TB→8-10TB per system | [Mainline/IBM case study](https://mainline.com/wp-content/uploads/PDFs/CS_PACCAR-Power.pdf) |
| SAP Integration Suite / SAP Transportation Management (S4TM) / SAP Analytics Cloud / SAP Fiori / SAP Intelligent RPA | PACCAR's "Integrated Transportation and Global Trade Platform," an SAP Innovation Awards 2021 entry, describes PACCAR ITD's SAP CoE, integration of legacy orders into S4TM via CPI, Fiori portal used by "Internal Users, Suppliers and Dealers," 0.5M records/day | [SAP Innovation Awards 2021 pitch deck](https://www.sap.com/bin/sapdxc/proxy.inmsl.attachment.11352.pitch-deck.pdf) |
| SAP BusinessObjects Financial Consolidation (BFC) | PACCAR selected BFC in 2016 for financial consolidation and close, displacing a legacy system, live 2017 | [appsruntheworld.com transaction record](https://www.appsruntheworld.com/customers-database/purchases/view/paccar-inc-united-states-selects-sap-businessobjects-financial-consolidation-bfc-for-financial-consolidation-and-close) |
| SAP Concur | PACCAR deployed SAP Concur for global travel & expense management | [SAP Concur PACCAR case study](https://www.concur.com/case-studies/paccar) |
| SAP ECC + SAP IBP (Integrated Business Planning) | LinkedIn profiles of PACCAR supply-chain analysts describe "SAP IBP demand planning," "SAP ECC master data validation," MRP work at PACCAR | [LinkedIn (Ravi Teja)](https://www.linkedin.com/in/ravi-teja27) |
| SAP GTS (Global Trade Services) | Active 2026 PACCAR job posting for "SAP GTS Implementation Business Analyst," Bellevue, to "upgrade its SAP Global Trade Services (GTS) system" | [PACCAR careers posting](https://jobs.paccar.com/job/Bellevue-SAP-GTS-Implementation-Business-Analyst-WA-98004/1417464933/) |
| SAP S/4 Order-to-Cash, SD/MM/PP/PM/FI/CO/WM/COPA modules | "Manager, SAP Application S4" posting requires experience in SAP OTC, ECC, and named modules SD, MM, PP, PM, FI, CO, WM, COPA | [Monster job posting](https://www.monster.com/job-openings/manager-sap-application-s4-bellevue-wa--30782e55-3599-4bfe-b045-ab174a8b517e?mstr_dist=true) |
| PACCAR ITD (Information Technology Division) | Self-described as "an industry leader in innovative digital technologies" supporting PACCAR business processes | [PACCAR 2023 Annual Report](https://www.paccar.com/media/pvzjr4ps/2023-annual-report-final.pdf); [PACCAR ITD careers page](https://jobs.paccar.com/content/PACCAR/?locale=en_US) |

`INFERRED (dealer-accounting norm)`: The presence of SAP OTC, MM, SD, FI/CO, and Transportation
Management modules, plus SAP IBP for demand planning, is consistent with PACCAR running its
manufacturing, parts-supply-chain, and finance-consolidation stack on SAP end-to-end — but no
single source states "PACCAR's core ERP is 100% SAP" as a blanket claim. The confirmed pieces are
S/4HANA (ERP core), SAP TM (logistics), SAP GTS (trade compliance), SAP IBP (planning), SAP BFC
(consolidation), and SAP Concur (T&E) — a materially SAP-shaped enterprise, but assembled from
several separate references rather than one master statement.

## 2. Dealer-facing PACCAR systems (real names)

| System | What it does | Who logs in | Public API? |
|---|---|---|---|
| **PACCAR eportal** (`eportal.paccar.com` / `eportal.paccar.net`, brand variants `eportal.daf.com`) | SSO gateway to DealerNet: service manuals, wiring diagrams, WebFleet eCat parts catalog, PACCAR Vehicle Pro (PVP) software downloads, bulletins | Dealer service/parts staff, via PACCAR-issued username/password and digital certificate (PACCAR Keymaster) | No public API documented; access is SSO/browser only. [`DOCUMENTED`] |
| **PACCAR Solutions / PSSM (Service Management)**, built by **Decisiv** | Fleet/customer service scheduling, case management, vehicle/VIN records across any PACCAR dealer in US/Canada | Dealers, fleets, service providers | Vendor (Decisiv) platform; no public developer API found | [PACCAR Solutions login](https://paccar.decisiv.net/), [Decisiv help center](https://support.paccar.decisiv.net/hc/en-us), [MHC description of PSSM](https://mhc.com/service/paccar-solutions-service-management), [Peterbilt dealer network page](https://www.peterbilt.com/why-peterbilt/dealer-network) |
| **Online Parts Counter (OPC) / "Next Gen OPC"** | eCommerce parts ordering, 545,000+ parts, 24/7 access; branded `PartsCounter.Kenworth.com` | Dealers and major fleet accounts | Integrates with Karmak Fusion DMS; no public REST API documented, but structured B2B order upload/download exists | [Rihm Kenworth OPC description](https://www.rihmkenworth.com/blog/the-benefits-of-online-parts-counter--55573), [Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar) |
| **Managed Dealer Inventory (MDI)** | PACCAR Parts manages each dealer's stocking algorithm; analyzes retail sell-through, transmits daily order recommendations electronically | PACCAR Parts (host side); dealer parts managers (consumer side) | Batch data exchange (stock/MKT/COF order types) documented via Karmak integration; no public API | [PACCAR Parts Technology page](https://www.paccarparts.com/technology/), [Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar) |
| **PRWS — PACCAR Registration and Warranty System** | Current warranty claim submission/adjudication system; replaced older "DWWC" long-claim input tooling | Dealer warranty administrators | **Yes** — PRWS is listed as "available on Fortellis," CDK's OEM/developer marketplace | [CDK Global Heavy Truck OEM page](https://www2.cdkglobal.com/ht-oem); [NHTSA service bulletin referencing PRWS](https://static.nhtsa.gov/odi/tsbs/2026/MC-11034059-0001.pdf); [Procede/Excede PRWS integration announcement](https://www.linkedin.com/posts/procede-software_procedesoftware-excededms-productupdate-activity-7402395748069548032-qWoj) |
| **DAVIE4** | PACCAR diagnostic/programming tool (successor to earlier Davie tools); used for engine calibration, road-speed changes, fault diagnosis | Dealer technicians | Desktop software tied to eportal credentials; no public API | [NHTSA technical bulletin using DAVIE4](https://static.nhtsa.gov/odi/tsbs/2022/MC-10209715-0001.pdf), [Diesel Diagnostic Equipment DAVIE4 login guide](https://dieseldiagnosticequipment.com/easy-fix-for-paccar-davie-4-login-error/) |
| **TruckTech+ (Kenworth) / SmartLINQ (Peterbilt)**, powered by **Decisiv** | Remote diagnostics and telematics case management; auto-creates service cases from fault codes, transfers repair estimates into the DMS | Fleet customers and dealers | Integrates bidirectionally with DMS (e.g., Karmak Fusion); no public third-party API documented | [Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar), [NHTSA bulletin mentioning TruckTech+ support](https://static.nhtsa.gov/odi/tsbs/2017/MC-10118721-9999.pdf) |
| **PACCAR Connect** (DAF brand of telematics portal) | Connected-truck data portal for DAF customers/fleet managers | Fleet owners/managers (account request workflow, 3-business-day provisioning) | Account-request web form only; no public API documented | [DAF PACCAR Connect account request](https://www.daf.global/en-us/daf-services/connected-services/support/account-request-form) |
| **FOCUS CRM** | PACCAR Parts' CRM tool receiving customer/parts sales data from dealer DMS for purchasing-pattern insight | PACCAR Parts marketing; dealer sales flows into it | One-way data feed from DMS (e.g., Karmak Fusion); no public API | [Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar) |
| **Service Gate (PACCAR Parts Fleet Services)** | Payment-card and invoice/remittance platform for fleet/national accounts | Dealer AR/service staff, fleet accounts | Structured invoice/remittance transmission via DMS integration; no public API documented | [Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar), [PACCAR Parts Fleet Services PDF](https://www.paccarpartsfleetservices.com/pdf/PACCAR.pdf) |
| **PACCAR's "B2B infrastructure"** | Source of truck build data/specifications pulled into dealer DMS | System-to-system; dealer DMS is the consumer | Named generically as "B2B infrastructure" — no further public specification found | [Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar) |
| **PacLease Rental Performance System (RPS)** | Drives rental contract/unit/customer records for PacLease franchise operations | PacLease dealer staff | DMS integration only | [Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar) |

`UNVERIFIED`: A platform literally named "PartsPRO" belonging to PACCAR was not found; "Parts
Pro" / "PACE" in search results are unrelated third-party aftermarket brands (The AAM Group). The
correct PACCAR-branded ordering platform is **Online Parts Counter (OPC)** — use that name in the
twin, not "PartsPRO."

## 3. Warranty: claim lifecycle

`DOCUMENTED` (from NHTSA technical/service bulletins and PRWS references):

1. **Repair performed** at dealer; technician runs diagnostics, often via DAVIE4, and records
   cause/correction. ([NHTSA bulletin](https://static.nhtsa.gov/odi/tsbs/2022/MC-10209715-0001.pdf))
2. **Claim entry** in PRWS: dealer selects claim type — "Quick Claim" (pre-coded campaign/failure
   code, e.g. `E286A`) or "long claim" (manual entry of Campaign #, Failure type, SRT — Standard
   Repair Time). Cross-division repairs (e.g., Kenworth dealer repairing a Peterbilt chassis) use
   a distinct claim path referencing "PACCAR Engine Claim" type. ([NHTSA bulletin](https://static.nhtsa.gov/odi/tsbs/2022/MC-10209715-0001.pdf))
3. **Data required from dealer**: VIN, causal part number/removed part, Claim Category (e.g.
   "PBSA" for steel-axle claims), Concern/Cause/Correction narrative, SRT code, claim story
   text, and — for parts warranty — copy of purchase receipt and photos in adjacent RMA-style
   flows. ([PACCAR/JW Speaker warranty portal instructions](https://paccar.jwspeaker.com/documents/JW%20Speaker%20Extended%20Warranty%20-%20Portal%20Instructions.pdf), [NHTSA bulletin MC-11034059](https://static.nhtsa.gov/odi/tsbs/2026/MC-11034059-0001.pdf))
4. **Submission window**: filing deadlines are enforced per warranty policy bulletin (example:
   "File the claim within 14 days in accordance with CA009"). ([NHTSA bulletin](https://static.nhtsa.gov/odi/tsbs/2022/MC-10209715-0001.pdf))
5. **SIR Sheets**: PRWS v1.2 (via the Procede/Excede DMS integration) added the ability to pull
   "Service Information Record" PDF sheets directly from PACCAR. ([Procede/Excede LinkedIn announcement](https://www.linkedin.com/posts/procede-software_procedesoftware-excededms-productupdate-activity-7402395748069548032-qWoj))
6. **Resubmission**: claims can be saved, resent, or given new claim numbers without re-entry.
   ([Procede/Excede LinkedIn announcement](https://www.linkedin.com/posts/procede-software_procedesoftware-excededms-productupdate-activity-7402395748069548032-qWoj))
7. **PRWS is on Fortellis**: CDK's description states PRWS "streamlines the filing of PACCAR
   warranty claims by creating drafts in the PACCAR PRWS (warranty system) with information from
   the RO and tracking via a dynamic status screen." ([CDK Global Heavy Truck OEM page](https://www2.cdkglobal.com/ht-oem))

`UNVERIFIED`: The specific chargeback mechanics (e.g., how PACCAR debits a dealer's warranty
receivable account when a claim is denied/adjusted after payment, and what GL account or DMS
screen absorbs it) were not found in any public PACCAR document. `INFERRED (dealer-accounting
norm)`: as in franchised dealer accounting generally, denied/adjusted warranty claims are charged
back against the dealer's warranty receivable and expensed to the service department; this is
standard NADA-format practice, not a PACCAR-specific disclosure.

## 4. Parts: distribution, cadence, returns

`DOCUMENTED`:

- PACCAR Parts operates a **global network of 18-20 Parts Distribution Centers (PDCs)** across
  North America, Europe, Australia, Mexico, and Central/South America, with 3.1M+ sq ft of
  warehouse space. ([PACCAR Parts services page](https://www.paccarparts.com/services/), [PACCAR Parts homepage](https://www.paccarparts.com/), [PACCAR 2023 10-K excerpt](https://s202.q4cdn.com/173635405/files/doc_financials/2023/q4/ce0914b9-5f27-4c9f-85b5-8cd0f33fabf9.pdf))
- **Stock orders** are generated through **MDI (Managed Dealer Inventory)**: PACCAR Parts analyzes
  each dealer's retail sell-through and transmits electronic order recommendations daily; Karmak
  Fusion documents three MDI order types: **Stock**, **Marketing Suggestion (MKT)**, and **Auto
  Confirmed (COF)**. ([PACCAR Parts Technology page](https://www.paccarparts.com/technology/), [Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar))
- **Emergency orders**: UK PDC processes "over 5,000 orders a day" with emergency orders received
  by 6pm delivered to the dealer by 8am the next day; the Las Vegas PDC processes "over 300
  emergency lines per day to all North American dealers." ([PACCAR Parts UK video transcript](https://www.youtube.com/watch?v=0lc6YyTaYpg), [Las Vegas PDC grand-opening video transcript](https://www.youtube.com/watch?v=Jjd9ykOXMAE))
- **Returns / obsolescence**: PACCAR's own supplier-facing Purchase Order Terms require suppliers
  to address "surplus and obsolete inventories of Product on a quarterly basis with the
  appropriate PACCAR Division Material Director," with unaddressed items becoming supplier
  responsibility after 120 days — this governs PACCAR's upstream supply, not the dealer-facing
  return policy, but shows the obsolescence-management cadence PACCAR itself uses.
  ([PACCAR Purchase Order Terms and Conditions](https://www.paccar.com/media/0s4iclwv/purchase-order-terms-conditions-022223.pdf))
- **Dealer-facing returns automation**: In 2022, PACCAR selected **Syncron Service Lifecycle
  Management (SLM)** with "Returns SmartBlox" to standardize dealer-to-OEM parts-return workflow
  and documentation; Syncron Customer Connect provides ERP/dealer-system integration.
  ([Syncron/PACCAR case study](https://www.syncron.com/resources/paccar-automates-connected-dealer-to-oem-returns-processing))
- **Electronic invoices and ASN**: PACCAR Parts sends electronic invoices (imported to DMS AP) and
  electronic packing slips (ASN) used to receive parts into dealer inventory.
  ([Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar))
- PACCAR's consolidated financials show **allowance for credit losses (Truck/Parts/Other)** of
  $1.2M (2024) and $0.9M (2023), and note revenue is "adjusted for estimated sales incentives and
  returns." ([PACCAR 2024 annual report financials](https://www.paccar.com/media/jntptvig/202-annual-report-financials-only.pdf))

`UNVERIFIED`: A dealer-facing "obsolescence allowance" percentage or buy-back schedule specific to
PACCAR Parts dealers was not found in public sources.

## 5. Vehicle ordering and configuration

`DOCUMENTED`:

- Peterbilt and Kenworth run **public online configurators** (e.g., Model 579 configurator) for
  prospective-buyer exploration, letting users choose chassis, axle, sleeper, colors, and MX-13
  performance levels, then contact a dealer. ([Truckers Logic on Peterbilt configurator](https://truckerslogic.com/peterbilt-truck-configurator/), [Heavy Duty Trucking on the 579 configurator](https://www.truckinginfo.com/news/peterbilt-customers-can-customize-their-trucks)) This is a marketing/lead tool, not the dealer order-entry system.
- **Actual factory ordering** happens through the dealer sales process: a signed sales order,
  deposit, and credit approval/proof of funds are the three requirements cited by a Rush Truck
  Centers salesperson to reserve a **build slot**. ([Rush Truck Centers/YouTube on Peterbilt build slots](https://www.youtube.com/watch?v=y3FkJdvafbc))
- **Build slots** are a scarce, allocated resource tied to plant capacity and model-year cutoffs
  (example cited: final year of Peterbilt 389 production, slots sold by half-year). ([Rush Truck Centers/YouTube on Peterbilt build slots](https://www.youtube.com/watch?v=y3FkJdvafbc))
- **Chassis/VIN and build record**: the 17-character VIN encodes model year, plant, and body
  style; the factory build record and chassis specification are retrievable from the VIN, from
  physical component/data plates on the truck, and from "the original chassis spec sheet from the
  ordering dealer or PACCAR." ([CarCheckerVIN Peterbilt build-sheet page](https://www.carcheckervin.com/build-sheet/peterbilt))
- **Chassis number for aftermarket/body-builder tools**: Peterbilt's Body Builder Programming
  Guide instructs entering "the eight character chassis number" (last 8 of VIN) into a lookup tool
  to retrieve build data for body-builder programming (e.g., PTO module setup). ([Peterbilt Body Builder PTO Programming Guide](https://www.peterbilt.com/static-assets/documents/resources/body_builder_module_programming_guide.pdf))
- **Data flow back to dealer at delivery**: Karmak's PACCAR integration explicitly states Fusion
  "retrieves truck build data and specifications" from "PACCAR's B2B infrastructure" and maps
  "key vehicle components, dates, and other information" into DMS-tracked fields. ([Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar))
- Peterbilt also offers pre-build **.dxf frame-layout files** of an ordered chassis on request,
  before the truck is built, for body-builder planning. ([Peterbilt Body Builder Manual on Scribd](https://www.scribd.com/document/433089300/Peterbilt-Body-Builder-Manuals-Peterbilt-Heavy-Duty-Body-Builder-Manual-pdf))

`UNVERIFIED`: The specific order-entry system name dealers use to submit a factory order
(distinct from the public configurator and from OPC) was not identified by name in public
sources; it is referenced only generically as part of "PACCAR's B2B infrastructure."

## 6. Telematics and connected-truck data (sovereign-data crux)

`DOCUMENTED`, from PACCAR's own **Truck Connectivity Services Terms and Conditions**, which
govern "TRUCKTECH+," "SMARTLINQ," "PACCAR Solutions," "PACCAR Connect," and "Remote Diagnostics":

- **What is collected**: vehicle description, GPS location, speed, direction and time of travel,
  odometer, start/stop events, fault codes, engine data, VIN, mechanical condition, and — per the
  terms — "any information, nonpublic or otherwise, relating to your Vehicle or its use." Location
  and diagnostic data are transmitted "regardless of your Subscription status." ([PACCAR Truck Connectivity Services Terms](https://www.paccar.com/telematicsterms))
- **Ownership**: the terms **do not state that PACCAR, the dealer, or the customer "owns" the
  data**. PACCAR frames its relationship as a right to "collect, use and retain" data, and
  explicitly notes the customer "does not own the Services software." This is a services/license
  framing, not a data-property framing. ([PACCAR Truck Connectivity Services Terms](https://www.paccar.com/telematicsterms))
- **Dealer access**: PACCAR states data "may be shared by PACCAR with its dealers and Service
  Providers to provide you with notices and reports related to service or other performance of
  your vehicle" — i.e., dealer access is PACCAR-mediated and service-purpose-limited, not a
  standing dealer data feed the dealer independently owns or controls. ([PACCAR Truck Connectivity Services Terms](https://www.paccar.com/telematicsterms))
- **Customer/fleet access**: the vehicle owner (or "anyone with access to your account") can
  remotely monitor location and operating conditions; the owner can request review/correction of
  data only "by contacting the dealership where you purchased your vehicle" — the dealer is a
  service intermediary, not a data controller. ([PACCAR Truck Connectivity Services Terms](https://www.paccar.com/telematicsterms))
- **Third parties**: PACCAR may disclose data to "wireless network service providers, suppliers,
  licensors, manufacturers, distributors, and authorized PACCAR dealers," collectively "Service
  Providers," and may use data "to develop additional products and services of PACCAR, PACCAR
  affiliates and subsidiaries, and service partners, including PACCAR's dealer network." ([PACCAR Truck Connectivity Services Terms](https://www.paccar.com/telematicsterms))
- **DMS-side integration**: In practice, TruckTech+/SmartLINQ (run on the **Decisiv** platform)
  push repair estimates into the dealer's DMS (e.g., Karmak Fusion) and pull back updates to
  open repair-order tasks; the case auto-closes when the RO is invoiced — i.e., the live
  telematics case data lives in PACCAR/Decisiv's system, with only repair-order-relevant slices
  synced into the dealer DMS. ([Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar))

**Sovereign-data crux, stated plainly**: PACCAR is the technical and contractual gatekeeper of
telematics/connectivity data. The dealer's access is a downstream, purpose-limited grant
("service or other performance" reporting) rather than an owned or exportable data asset. No
public source shows a dealer-initiated bulk export or open API for raw telematics data; dealer
visibility comes only through PACCAR-operated portals (PACCAR Solutions/Decisiv, TruckTech+,
SmartLINQ, PACCAR Connect) or through whatever slice a DMS integration like Karmak's chooses to
surface into repair orders. This is the strongest evidence in this lane that a "sovereign twin"
strategy is structurally opposed by the OEM's own data terms for anything above the parts/service
transaction layer.

## 7. Standards governing OEM-to-dealer data exchange

`DOCUMENTED`:

- **STAR (Standards for Technology in Automotive Retail)**: founded 2001, defines XML **Business
  Object Documents (BODs)** for dealer-to-OEM transactions — originally Parts Order, Parts Pick
  List, Parts Return, Repair Order, Sales Lead, Vehicle Service History, Warranty Reconciliation.
  STAR's charter explicitly lists **"Medium & Heavy-duty Trucks"** as a supported industry segment
  alongside retail auto. ([STAR homepage](https://www.starstandard.org/), [STAR About page](https://www.starstandard.org/index.php/about-us/), [OASIS/coverpages STAR history](https://xml.coverpages.org/star.html))
- STAR's **2024 STAR6 XML v6.2.4** release added BODs for Retail Delivery Report, Vehicle Invoice,
  Vehicle Order, Vehicle Price List, Vehicle Shipment, Vehicle Specifications, and Dealer Support
  Case — directly relevant object types for the vehicle-ordering lane described in section 5.
  ([PRWeb STAR XML v6.2.4 release](https://www.prweb.com/releases/leading-automotive-technical-standards-association-star-releases-star-xml-bod-updates-for-retail-delivery-vehicle-sales-pricing-and-service-302244799.html))
- STAR's **January 2026 "Automotive Retail Domain Model"** finalized domains including **Parts,
  Accounting, Payroll, and HR** — the Accounting domain is the closest public STAR artifact to a
  standardized dealer chart-of-accounts/ledger interchange model. ([STAR Domain Model announcement](https://www.starstandard.org/index.php/2026/01/27/star-unveils-industry-defining-retail-automotive-domain-model-to-advance-data-interoperability-and-ai-transformation-across-the-entire-ecosystem/))
- **No public evidence PACCAR is a named STAR member** was found in this research pass; STAR's
  own materials describe membership as open to "dealers, manufacturers, and retail system
  providers" generally, without naming PACCAR specifically. `UNVERIFIED`.
- **ODX (Open Diagnostic data eXchange, ISO 22901-1)**: this is the real standard behind the task
  brief's "ODDX" reference (no separate "ODDX" standard was found; ODX is the correct name). ODX
  is an ASAM/ISO XML format for **ECU diagnostic data exchange** between OEMs, Tier-1 suppliers,
  and diagnostic-tool vendors — it governs how diagnostic capability descriptions move from
  engineering to the shop-floor tester (e.g., DAVIE4-class tools), not commercial/dealer-ledger
  data. ([Softing ODX ISO 22901-1 overview](https://automotive.softing.com/standards/data-descriptions/odx-iso-22901-1.html), [ASAM ODX-RS Companion Standard overview](https://www.asam.net/fileadmin/Standards/MCD-2_D/ODX-RS-Companion-Standard-Overview.pdf))
- **Heavy-truck-specific equivalents**: American Trucking Associations' **Technology &
  Maintenance Council (TMC)** publishes **VMRS (Vehicle Maintenance Reporting Standards)** —
  coding for parts/components/failure modes used across fleets, dealers, and OEMs — and RP1210 /
  SAE J1939 / J2534 recommended practices for diagnostic tool interoperability, under a 2015
  voluntary "right to repair" agreement requiring OEMs to support these open interfaces. ([Heavy Duty Trucking on TMC right-to-repair agreement](https://www.truckinginfo.com/news/tmc-app-to-help-diagnostic-adapter-vendors-comply-with-new-standard), [TMC Recommended Practices Manual](https://tmc.trucking.org/sites/default/files/RP_MANUAL_DESCRIPTIONS.pdf), [Transport Topics on TMC/RP1210 history](https://www.ttnews.com/articles/data-interchangeinteroperability-challenges-carriers-take-action))
- **Karmak (Fusion DMS) licensed VMRS from TMC** in 2025 specifically to standardize
  service-intelligence data shared with "dealers, fleets and OEMs" — direct evidence VMRS is an
  active heavy-truck dealer-OEM data-exchange vocabulary today. ([Trucks, Parts, Service on Karmak/TMC VMRS licensing](https://www.truckpartsandservice.com/technology/business-operations/article/15739616/karmak-licenses-tmcs-vehicle-maintenance-standards))
- **COVESA/ACEA onboard API MoU (2025)**: a forward-looking, Europe-centered initiative to define
  a standardized onboard API for connected-commercial-vehicle fleet-management data, built on
  COVESA's Vehicle Interface Service Specification (VISS) — not yet a deployed standard, but the
  clearest public signal of where OEM-to-fleet telematics interoperability is heading. ([COVESA/ACEA commercial vehicle interoperability announcement](https://covesa.global/driving-commercial-vehicle-interoperability-forward/))

## 8. Where PACCAR constrains the dealer's ledger

`DOCUMENTED`:

- Karmak's Fusion/PACCAR integration page states plainly that **"Financial statements are
  automatically downloaded to PACCAR"** as part of the standard integration — i.e., PACCAR
  receives a periodic feed of the dealer's financial statement directly from the DMS. ([Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar))
- No public PACCAR document specifies the exact **factory financial statement format** or a
  PACCAR-specific chart of accounts. `UNVERIFIED` as a named PACCAR artifact.
- `INFERRED (dealer-accounting norm)`: Heavy-truck and auto dealer financial reporting to OEMs
  overwhelmingly follows the **NADA (National Automobile Dealers Association) standard
  financial-statement format**, which organizes the dealership into departmental profit centers
  (new vehicle, used vehicle, F&I, service, parts) mapped to a standard chart-of-accounts
  numbering scheme; NADA states this format is what "most manufacturers require for their
  reporting submissions." ([DealSpeak AI on the NADA financial-statement format](https://www.dealspeak.ai/blog/dealership-accounting-training-overview), [NADA "What's Important on the Financial Statement"](https://www.nada.org/nada/education-consulting/tailored-training/whats-important-financial-statement))
- **NADA 20 Groups** provide "industry-leading OEM-specific financial comparisons" of a dealership
  against average and best-of-class peers in the same brand — meaning PACCAR-brand dealers are
  very likely benchmarked through an OEM-specific 20-group composite, though PACCAR's exact
  submission deadline cadence (monthly vs. period-close) was not found in a public PACCAR
  document. ([NADA 20 Group page](https://www.nada.org/nada/nada-20-group))
- `UNVERIFIED`: no public source states PACCAR's required chart-of-accounts numbering scheme,
  submission deadline (e.g., "5 business days after month-end"), or penalty for late/incomplete
  factory financial statements. This is a genuine gap — likely covered only in PACCAR's dealer
  agreement / dealer operating manual, which is not a public document.

## What I could not verify

- The exact chargeback mechanism and GL treatment when PACCAR denies or adjusts a paid warranty
  claim (dealer-side accounting screen/process).
- Whether PACCAR is a formal STAR member, or which STAR BODs (if any) PACCAR implements versus
  proprietary/B2B-infrastructure formats.
- The literal name and any API surface of PACCAR's factory vehicle order-entry system (distinct
  from public configurators and from OPC).
- PACCAR's specific chart-of-accounts numbering and financial-statement submission deadline
  requirements for dealers (only the general NADA-format norm and the fact of an automated
  month-end statement download to PACCAR are documented).
- Whether the "PACCAR's B2B infrastructure" term (Karmak's phrase) refers to a single named
  platform, EDI gateway, or a family of point-to-point feeds.
- Confirmation that "PartsPRO" does not exist as a PACCAR system name (the task brief's term
  appears to conflate an unrelated third-party aftermarket brand "Parts Pro"/PACE with PACCAR's
  actual OPC platform).
- Any dealer-facing published percentage/formula for parts obsolescence-allowance buy-back
  (only the supplier-facing 120-day PACCAR Purchase Order Terms clause was found).
- Whether TruckTech+/SmartLINQ/PACCAR Connect ever expose a bulk or programmatic data-export path
  to the dealer or fleet owner, versus only portal-based viewing.

## Proposed SAP-shape mapping

| CDK / PACCAR concept | Proposed SAP table/object in the twin | Rationale |
|---|---|---|
| PACCAR Parts catalog / OPC part master | `MARA` (general material master), `MARM` (units of measure) | Parts ordered via OPC map to material master records already used in the twin's parts lane |
| Dealer-specific part data (pricing, MDI stocking class) | `MARC` (plant data), `MVKE` (sales data) | MDI's per-dealer stocking recommendation is a plant/location-specific parts attribute |
| Dealer parts inventory (MDI-driven stock) | `MARD` (storage location stock), `MBEW` (valuation) | MDI stock/MKT/COF order quantities update location stock and valuation |
| PACCAR Parts cross-reference / interchange numbers | `MFRPN` (manufacturer part number) | PACCAR-to-aftermarket part number crosswalk |
| Parts order/invoice/ASN documents (OPC, stock/emergency orders) | `MATDOC` (material document) + custom Z-table for STAR-style BOD header (order type: Stock/MKT/COF/Emergency) | `MATDOC` captures the movement; a header table should carry PACCAR order-type and PDC origin, since no native SAP field models this OEM-specific order taxonomy |
| Warranty claim (PRWS) | New custom object, e.g. `ZWARR_CLAIM`, referencing `MFRPN`/VIN and linked to the twin's service-order object (not yet defined in parts-lane scope) | No MM table models OEM warranty claims; must be modeled as a Z-object with fields: VIN, Claim Category, Campaign Code, SRT, Concern/Cause/Correction, claim status, PRWS claim number |
| Vehicle build/spec record (VIN, chassis number, options) | New custom object, e.g. `ZVEH_BUILD`, keyed by 17-char VIN and 8-char chassis number | Not a parts-lane concept; needs its own master data object referencing PACCAR's "B2B infrastructure" feed |
| Telematics/case data (TruckTech+/SmartLINQ) | Kept **outside** the twin's system of record; twin should only ingest the RO-relevant slice (estimate, parts list, labor) via `MATDOC`-linked service order, not raw telematics | Reflects the sovereign-data finding in §6: PACCAR retains the master telematics record; the dealer twin can only mirror what is synced into the DMS repair order |
| Factory financial statement extract sent to PACCAR | New custom reporting layer mapping the twin's GL to the NADA-format composite (not a native SAP FI structure) | PACCAR receives a NADA-format statement, not a native SAP FI/CO export; a translation/reporting layer is required between the twin's ledger and the OEM submission format |
