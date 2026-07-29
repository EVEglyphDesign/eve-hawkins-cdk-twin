# Lane 6 — CDK Drive Transaction Lifecycles (Document Flow by Functional Unit)

Client: EVEglyphDesign sovereign digital twin, Peterbilt Atlantic (9-site Peterbilt/PACCAR
heavy-truck group, Atlantic Canada). Twin exists in SAP shape (MARA/MARC/MARD/MARM/MBEW/
MVKE/MFRPN/MATDOC in `eve-dealer-parts-twin`). This lane maps the transactional document
flow — sales, service, parts, warranty, AR/cashiering, AP, payroll — the way an SAP
consultant would draw an order-to-cash / procure-to-pay chain.

## 1. Vehicle sales / deal desk

**Document chain (INFERRED, dealer-accounting norm, cross-checked against CDK's own API
naming):** Prospect/Customer record → Quote/Desk deal → Pending Deal → We-Owe(s) → Finalized
(booked) Deal → posted Vehicle Sale + F&I schedule entries.

| Step | Document / object | Status label used by CDK |
|---|---|---|
| Customer capture | Customer record (CRM/DMS) | — |
| Desking | Deal worksheet (structure: price, trade, rebates, F&I products) | "Pending" |
| Trade-in | Trade appraisal + payoff request | attached to deal |
| F&I menu | Finance/insurance product selections, rate/reserve | part of deal |
| Lien payoff | Payoff check/ACH to lienholder on the trade | linked to deal, not a ledger posting until paid |
| Finalisation ("washout") | Deal is balanced — all debits/credits on the deal net to zero before it can close | "Finalized"/"Booked" (ADP/CDK 3PA) or "Finalized & Accepted" (Dealertrack) — both mean **closed deal** ([DMS Cheat Sheet, Scribd/dealer-integrator reference](https://www.scribd.com/document/809504766/DMS-Cheat-Sheet-6-20-2023)) |
| We-Owe | Outstanding dealer obligation on the deal (accessory, service, cash-back) not yet fulfilled at delivery — tracked as its own schedule | DOCUMENTED as a distinct object in CDK's own partner-extract naming: "Pending Deals, We Owes — Update Only" ([CDK Partner Program Pricing Guide](https://www.cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf)) |

**Gross profit calculation.** `INFERRED (dealer-accounting norm)`: Front-end gross = selling
price − (vehicle cost + pack + reconditioning) at the unit level; recognized only when the
deal is finalized and the vehicle is delivered, not at contract signing ([WickedFile — Car Dealership Accounting](https://www.wickedfile.com/blogs/car-dealership-accounting/)). Back-end
gross = F&I product commissions + finance reserve + aftermarket product income, booked
against a chargeback/EPO reserve estimated from historical cancellation/early-payoff rates
([DealerInt — Car Dealership Accounting Basics](https://www.dealerint.com/blog/car-dealership-accounting-basics), [Beancount.io dealer bookkeeping guide](https://beancount.io/blog/2026/05/26/independent-used-car-dealer-bookkeeping-floorplan-financing-curtailment-fi-reserve-holdback-chargeback-recon-wip-form-8300-ftc-used-car-rule-bhph-repossession-loss-reserve-guide)). Holdback (2–3% of MSRP/invoice) is
manufacturer-paid margin that sits **outside** front-end gross and is usually booked as
"other income," reconciled against a factory-receivable schedule ([DealerInt](https://www.dealerint.com/blog/car-dealership-accounting-basics), [Kruse Control — Reading a Dealership Financial Statement](https://www.krusecontrolinc.com/how-to-read-a-dealership-financial-statement-a-practical-guide/)).

**What posts to the ledger at delivery vs. what stays in a schedule** (`INFERRED`):
- Posts at delivery: vehicle cost out of inventory, sale revenue, F&I product revenue net of
  reserve, trade-in unit into used inventory at appraised value, lien-payoff liability cleared
  against cash once wired.
- Stays in a schedule (balance-sheet detail, not a GL line): contracts-in-transit (deals sent
  to lender, cash not yet received), factory (holdback/incentive) receivables, F&I
  reserve/chargeback receivable, we-owes ([WickedFile](https://www.wickedfile.com/blogs/car-dealership-accounting/), [Spectrum CPAs — Dealership Accounting Mistakes](https://spectrumcpas.ca/the-biggest-accounting-mistakes-car-dealerships-make-and-how-to-avoid-them/)).

**Named CDK deal APIs (`DOCUMENTED`):**
- **CDK Drive FI Sales History Setup / Bulk / Delta** — retrieves FI (finance & insurance)
  vehicle sale records; statuses include `C, B, P, F, I, U` ([Fortellis CDK Drive API guide, docs.bettrdata.io](https://docs.bettrdata.io/user-docs/how-to-guides/fortellis-cdk-drive-api)).
- **CDK Drive Customer API** — creates/associates customer records used by both Deals and
  Repair Orders; explicitly documents a "DEALS" related-API section referencing a Deals spec
  at `apidocs-dev.fortellis.io/specs/91145f3f-2dd7-43fa-a63d-08908ef9e2e7` ([Microsoft Learn — CDK Drive Customer connector](https://learn.microsoft.com/en-us/connectors/cdkdrivecustomer/)).
- **CDK Drive Payment Settling API** — settles deal/RO/parts payments back into the DMS
  (PayNow, Invite-2-Pay workflows) ([CDK Global — Payment Settling API](https://www2.cdkglobal.com/payment-settling-api)).
- Partner-era (pre-Fortellis) extracts named explicitly: "Pending Deals," "Finalized Deals,"
  "We Owes," "Sales Customers," "Sales Vehicles" ([CDK Partner Program Pricing Guide](https://www.cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf)).

Deal-structure detail (menu selling, washout screen, individual We-Owe line items) is
`UNVERIFIED` at the field level — no public Fortellis spec for a general "Deals"/desking
write API was located; the FI Sales APIs are read-only extracts of already-finalized deals.

## 2. Service — repair order (RO) lifecycle

**Document chain (`DOCUMENTED`, from the CDK Drive Repair Order API family):** Service
Appointment → Repair Order (opened) → Service Line(s) (labor + preassigned parts) → Dispatch
→ Parts Request → Sublet → Additional/approved service requests (customer authorisation) →
Quality control/completion → Invoice → Cashiering (Payment Settling) → Close.

| Stage | CDK object | API |
|---|---|---|
| Appointment | Service Appointment | CDK Drive Get/Async Service Appointments ([CDK Global Fixed Ops APIs](https://www2.cdkglobal.com/api-solutions-fixed-ops)) |
| Check-in / open RO | Repair Order header (customer, vehicle, advisor, transport) | CDK Drive Repair Order API — Create Repair Order ([CDKDrive Repair Orders v1 Developer Guide](https://prod-fortellis-provider-api-reference-documents.s3-us-west-2.amazonaws.com/c7771500-1c95-4f8e-9241-eddc17cd55f6)) |
| Estimate / labor & parts lines | Service Line (labor ops + preassigned parts) | Add/Update/Query/Delete Service Line ([CDKDrive Repair Orders v1 Developer Guide](https://prod-fortellis-provider-api-reference-documents.s3-us-west-2.amazonaws.com/c7771500-1c95-4f8e-9241-eddc17cd55f6)) |
| Customer authorisation | "Additional Service Request" creation and approval | part of RO API workflow orchestration ([Fortellis blog — Driving Innovation with the CDK Repair Order API](https://fortellis.io/blog/driving-innovation-cdk-repair-order-api)) |
| Dispatch to technician / job tracking | `jobStarted` flag per service line; Workshop Management API | CDK Drive Repair Order V2 bundle ([Fortellis blog — CDK Repair Order Access Just Got Better](https://fortellis.io/blog/cdk-repair-order-access-just-got-better)) |
| Parts request | Parts Pick Ticket search | "CDK Drive Search Parts Pick Ticket" ([Fortellis Community Q&A](https://community.fortellis.io/fr/taxonomy/term/16)) |
| Op-code lookup | Op Code / labor time | CDK Drive Op Codes API ([CDKDrive OpCodes, Fortellis Community](https://community.fortellis.io/api-reference/vehicle-service/cdkdrive-opcodes)) |
| Invoice / cashiering | Payment settling on the RO | CDK Drive Payment Settling API ([CDK Global — Payment Settling API](https://www2.cdkglobal.com/payment-settling-api)) |
| Close | RO status transitions to "Closed"; retrievable via `getClosedRepairOrdersBulk`/`Delta` | CDK Drive Get Repair Order v3 ([Fortellis S3 API doc — CDK Drive Get Repair Order v3](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf)) |

**Sublet, MPI, quality control** are `UNVERIFIED` at the API-field level — no dedicated public
Fortellis endpoint names them; they are treated in the API family as line items or comments on
the Service Line and are only fully described in dealer-facing UI documentation, not public
specs.

**Work in progress (WIP).** `DOCUMENTED`/cross-DMS norm: an open RO's parts and labor are
posted to a WIP suspense account the moment parts are billed to the RO (parts billing run);
this happens **before** the RO closes and **before** the customer is invoiced. On close, the
WIP entry nets to zero and the amount is reclassified to revenue/COGS ([IntelliDealer — Work in Process](https://help.intellidealer.com/intellidealer/Content/Ref/Work_in_Process.htm)). CDK's own RO API models this same open/WIP/closed lifecycle explicitly:
`getOpenRepairOrdersBulk`, `getWIPRepairOrders` (opened/voided/closed in the past 48 hours),
`getClosedRepairOrdersBulk`/`Delta` ([Fortellis S3 — CDK Drive Get Repair Order v3](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf)).

**What posts at close (`INFERRED`):** labor revenue, parts revenue, sublet cost, COGS for
parts consumed, WIP cleared to zero, sales tax realized (tax/discounts on WIP type "S" are
only realized at close, per cross-DMS documentation) ([IntelliDealer — Work in Process](https://help.intellidealer.com/intellidealer/Content/Ref/Work_in_Process.htm)).

## 3. Parts counter

`DOCUMENTED` object names from the Fortellis Parts API family ([CDK Global Parts APIs](https://www2.cdkglobal.com/api-solutions-parts)):
- **CDK Drive Get Parts Sales / History Setup Parts Sales** — bulk/historical extract of
  parts sales records.
- **CDK Drive Async Open Parts Sales** and **CDK Drive Async Closed Parts Sales** — event
  push on open vs. closed parts sale state — this is the clearest public evidence of the
  **open vs. closed** distinction: an "Open Parts Sale" is a counter ticket / pick ticket in
  progress (allocated inventory, not yet invoiced); a "Closed Parts Sale" is invoiced and
  posted.
- **CDK Drive Search Parts Pick Ticket** — retrieves pick-ticket data, i.e., parts pulled
  against a specific RO or counter sale ([Fortellis Community Q&A](https://community.fortellis.io/fr/taxonomy/term/16)).
- **CDK Drive Async Parts Inventory** — inventory movement events tied to the ticket
  lifecycle ([Fortellis Community Q&A](https://community.fortellis.io/fr/taxonomy/term/16)).

Special order and counter-ticket header/line field names are `UNVERIFIED` — not published in
any open Fortellis spec found; only the sale-state (open/closed) and pick-ticket search
surfaces are documented publicly.

## 4. Warranty

`DOCUMENTED`, PACCAR-specific: **PRWS** (PACCAR Registration and Warranty System) —
"streamlines the filing of PACCAR warranty claims by creating drafts in the PACCAR PRWS
(warranty system) with information from the RO and tracking via a dynamic status screen,"
now available on Fortellis ([CDK Global — Heavy Truck OEM page](https://www2.cdkglobal.com/ht-oem)). This confirms the document chain: **RO → draft warranty claim (PRWS)
→ OEM submission → status tracking**, i.e. the claim is generated *from* the closed/near-close
RO, not created independently.

Generic (cross-OEM) `INFERRED`/dealer-forum evidence: warranty parts held pending OEM
disposition are tracked by RO digit/scrap report; chargebacks (OEM rejects or reduces a
claim after paying) are absorbed by whichever department (service vs. parts) failed to
retain the required stamped/signed part evidence ([r/partscounter — CDK Tracking Warranty Parts](https://www.reddit.com/r/partscounter/comments/1hs9xwc/cdk_tracking_warranty_parts/)). CDK also
sells a consulting program, **WRAP (Warranty Revenue Assistance Program)**, aimed at
improving OEM reimbursement rates and claim approval speed — evidence that warranty
receivable leakage is a known, material problem in CDK-based stores ([CDK Global — Warranty Reimbursement Explained](https://www.cdkglobal.com/insights/warranty-reimbursement-explained-wrap-questions-answered)).

**Receivable lifecycle** (`INFERRED`, standard dealer-accounting norm): claim submitted →
booked as Warranty/W&P Receivable on the balance sheet at expected reimbursement value →
OEM pays, adjusts, or charges back → receivable schedule reconciled monthly against the
factory statement; the Ford dealer accounting manual explicitly lists "W&P Claims — Claims
filed with Company on work performed under W&P program less Warranty Credit Advance" as a
distinct balance-sheet line ([Ford Online Accounting Manual — Balance Sheet Assets](https://www.fmcdealerfbmi.dealerconnection.com/AccountingManual/en/fin-stmt-prepmn5-en-htm/)).

No public Fortellis API exposes warranty-claim CRUD directly (search found none); PRWS
integration is the only documented OEM-specific warranty submission path, and it is
one-directional (RO → PRWS draft), not a general CDK warranty object.

## 5. Accounts receivable and cashiering

`DOCUMENTED`: **CDK Drive Payment Settling API** is the only public API surface touching
cashiering. It supports two workflows — **PayNow** (customer physically paying at the
dealership) and **Invite-2-Pay** (remote/contactless payment) — and enforces the business
rule that a settlement cannot exceed the amount owed. It returns a `PromiseID` that can be
polled for settlement status, and posts the result back into CDK Drive within seconds
of confirmation ([Fortellis blog — Payment Settling API](https://fortellis.io/blog/payment-settling-api-easier-payments-repair-orders-and-parts-orders), [CDK Global — Payment Settling API page](https://www2.cdkglobal.com/payment-settling-api)). It settles payments against **Repair Orders and Parts
Orders**; extract of the underlying RO/parts order still requires the respective RO/Parts
APIs.

Deposits, statements, and daily-deposit reconciliation are **not** covered by any public CDK
API found; they are `INFERRED (dealer-accounting norm)` bank/cash-office functions: cash,
check, and card receipts collected at cashiering are batched into a daily deposit, reconciled
against the day's RO/parts/deal closings, and posted to a cash-clearing account before bank
confirmation — a control cited generically across dealer-accounting guides but not tied to a
named CDK screen or table in any public source ([Fylehq — Car Dealership Accounting](https://www.fylehq.com/blog/car-dealership-accounting)).

Vehicle/parts/service AR aging schedules are explicitly named in the Ford dealer accounting
manual as distinct balance-sheet lines ("Accounts Receivable – Vehicle," "– Parts, Service,
Body," "– Other") ([Ford Online Accounting Manual](https://www.fmcdealerfbmi.dealerconnection.com/AccountingManual/en/fin-stmt-prepmn5-en-htm/)) — this is the accounting-norm receivable structure the twin should mirror even
though CDK's own AR screen/table names were not found publicly.

## 6. Accounts payable and purchasing

`DOCUMENTED` (partial): **CDK Foundations Suite** advertises "Accounts Payable" and
"multicompany Accounting" modules and states the accounting system provides "seamless data
flow from Sales and Service to Accounting" and "drill-down visibility into each department"
([CDK Global — Foundations Suite](https://www.cdkglobal.com/insights/cdk-foundations-suite-core-connected-dealership), [CDK Fundamentals Suite FAQ](https://www.cdkglobal.com/insights/unlocking-efficiency-common-questions-about-cdk-fundamentals-suite)). The **Data Extract API Bundle** explicitly lists "Foundations Suite APIs,
Including Accounting Workflows — Access extract and async APIs that support core dealership
operations, including accounting and general ledger data" ([CDK Global — Data Extract API Bundle](https://www.cdkglobal.com/data-extract-api-bundle)); a separate **General Ledger Inquiry
Workflow** is documented as "available for limited dealer testing," providing flexible
search/view of GL transaction history ([CDK Global — Accounting Workflows page](https://www2.cdkglobal.com/accounting-workflows)). No public spec names vendor-invoice or
purchase-order objects directly.

**Three-way match**: no CDK-specific public documentation found confirming a native
three-way (PO/receipt/invoice) match inside CDK Drive AP; this is `UNVERIFIED`. Three-way
matching is a documented standard AP control in ERP systems generally (e.g., Microsoft
Dynamics 365 three-way matching policies) ([Microsoft Learn — Three-way matching policies](https://learn.microsoft.com/en-us/dynamics365/finance/accounts-payable/three-way-matching-policies)), and third-party heavy-truck DMS competitor Karmak explicitly
advertises it for the OEM-parts-invoice use case: "PACCAR Parts electronic invoices are
imported directly into Fusion where they are compared to your purchase orders and receipts
and can be automatically posted into Accounts Payable" ([Karmak — PACCAR Integration](https://www.karmak.com/integrations/paccar)) — strong indirect evidence
that OEM-parts-invoice three-way match is an expected heavy-truck DMS capability, but CDK
Drive's own implementation is not publicly documented.

**OEM parts invoice reconciliation**: CDK's Heavy Truck OEM page states an "Electronic
Shipper" integration is coming, to "reconcile OEM parts shipments easily through access to
PACCAR's electronic shippers," available through Sales at time of publication ([CDK Global — Heavy Truck OEM page](https://www2.cdkglobal.com/ht-oem)) — confirms the concept exists as a
CDK roadmap item for PACCAR dealers but not yet a shipped, documented API.

## 7. Payroll

`INFERRED (dealer-accounting norm)`, consistent across DMS competitors and payroll
integrators: technician time reaches payroll via **flag hours** — the labor time billed on
a closed RO's service line (from the op-code's published flat-rate time) accumulates against
the technician; a **Technician Payroll Report** is printed and reconciled per pay period, then
a **payroll lock** finalizes the period so RO time can no longer be re-flagged into it
([Mitchell RepairCenter — Payroll: Flat Rate and Commission](http://www.mymitchell.com/tchs/helpfiles/RepairCenter/1033/Content/18128.htm)). Labor gross profit = (sold hours × retail labor rate) − (flag hours × flat-rate pay)
([Journal Entries Hub — Flat-Rate Technician Payroll](https://www.journalentrieshub.com/entries/auto-service-technician-payroll)).

Salesperson commission is computed from the finalized deal's front/back gross figures once
the deal posts; this is standard dealer-accounting practice but no public CDK-specific
commission-calculation object/table was found — `UNVERIFIED` at the CDK object-name level.

CDK itself does not appear to operate a public payroll-processing API; instead, third-party
payroll vendors (ADP Workforce Now, Netchex, Workzoom) document **import/GL-push
integrations against CDK Drive**: "ADP Workforce Now DMS Outbound Integration" pushes payroll
journal entries into CDK Drive's General Ledger ([ADP Marketplace — CDK Global DMS Outbound Integration](https://apps.adp.com/en-US/apps/292781/cdk-global-dms-outbound-integration-from-adp-workforce-now)); Netchex advertises "GL integrations tailored to
[CDK]... syncing technician time, commissions, and GL data back into the DMS" ([Netchex — Payroll Software for Automotive Dealerships](https://netchex.com/blog/the-5-best-payroll-software-platforms-for-automotive-dealerships/)); Workzoom
states flag-rate hours import from CDK Drive is currently **file-based export**, with direct
API integration only "scoped during implementation" ([Workzoom — Automotive industry payroll](https://www.workzoom.com/industries/automotive/)) — direct confirmation that payroll
data exchange with CDK Drive is largely **report/file export**, not a public API.

## 8. API vs. report-export availability by functional unit

| Functional unit | Reachable via public API (`DOCUMENTED`) | Report-export / file-only (`DOCUMENTED` or `INFERRED`) |
|---|---|---|
| Vehicle sales / deal desk | FI Sales history/bulk/delta (read-only, finalized deals); Customer API; Payment Settling | Deal desking/washout screen, We-Owe detail, menu selling — `UNVERIFIED`/no public write API found |
| Service (RO) | Full RO lifecycle: Open/WIP/Closed bulk & delta, Service Line CRUD, Op Codes, Service Appointments, Payment Settling ([Fortellis S3 doc](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf)) | MPI, sublet detail, QC sign-off — no dedicated public endpoint found |
| Parts counter | Get/Async Open & Closed Parts Sales, Pick Ticket search, Parts Inventory async | Special-order header fields, counter-ticket UI detail — `UNVERIFIED` |
| Warranty | None generic; PRWS draft creation from RO is PACCAR-specific and documented | Claim adjudication, chargeback detail — file/portal-only (PRWS UI, WRAP consulting) |
| AR / cashiering | Payment Settling API only | Deposits, statements, daily reconciliation — report/file export (`INFERRED`) |
| AP / purchasing | GL Inquiry Workflow (limited dealer testing); Data Extract Bundle "Accounting Workflows" | Vendor invoice entry, PO matching — no public API found; OEM parts invoice reconciliation is a stated roadmap item, not shipped |
| Payroll | None found | Universally file-export/GL-push via third-party payroll vendors (ADP, Netchex, Workzoom) |

## 9. Heavy-truck specifics (PACCAR / Peterbilt)

`DOCUMENTED`:
- **OPC (Online Parts Counter)** — "CDK Drive Parts and PACCAR OPC e-commerce solution
  allows customers to purchase both PACCAR and non-PACCAR parts from the dealership, at
  pricing levels from the dealer's CDK system." **Required by PACCAR**, available on
  Fortellis ([CDK Global — Heavy Truck OEM page](https://www2.cdkglobal.com/ht-oem)).
- **PRWS** — PACCAR's newest registration/warranty system; drafts claims from the RO,
  tracked via a dynamic status screen; available on Fortellis ([CDK Global — Heavy Truck OEM page](https://www2.cdkglobal.com/ht-oem)).
- **Electronic Shipper** (roadmap at time of source) — reconciles OEM parts shipments via
  PACCAR's electronic shippers ([CDK Global — Heavy Truck OEM page](https://www2.cdkglobal.com/ht-oem)).
- **Decisiv integration** — bidirectional sync of RO line-level "story" corrections between
  CDK Drive and the Decisiv interface used for fleet/mobile service coordination ([CDK Global — Heavy Truck OEM page](https://www2.cdkglobal.com/ht-oem)); Peterbilt of Atlanta itself is listed as a
  Decisiv-connected dealer ([Decisiv — Peterbilt of Atlanta](https://www.decisiv.com/peterbilt-of-atlanta/)), and PACCAR's own Decisiv portal documents how a dealer links a
  **fleet customer account to the DMS via customer number**: "Both local and fleet customers
  can connect to your dealer management system via their customer number if your location is
  integrated with the dealer management system" ([PACCAR Solutions — Manage Customers](https://support.paccar.decisiv.net/hc/en-us/articles/360025596534-Manage-Customers)).
- **PACCAR Parts Fleet Services** — national-account program for fleets "with 250 or more
  trucks domiciled at several locations," providing "consolidated billing," "Parts and Service
  transactions consolidated into one billing statement," and an EDI layer for the fleet's own
  business system ([PACCAR Parts Fleet Services — Fleet Management Solutions PDF](https://www.paccarpartsfleetservices.com/pdf/PACCAR.pdf), [PACCAR Parts — Customer Service page](https://www.paccarparts.com/services/)). This was built jointly with Multi Service Corp and
  is now called **Service Gate** for point-of-sale authorization/price verification and
  electronic remittance, integrated at the dealer business-system level (documented for the
  competing DMS Karmak, evidencing the integration pattern PACCAR dealers use industry-wide)
  ([Heavy Duty Trucking — Multi Service, Paccar Sales Integration](https://www.truckinginfo.com/articles/multi-service-paccar-sales-integration-creates-back-office-savings), [Karmak — PACCAR Integration](https://www.karmak.com/integrations/paccar)).
- Multi-unit fleet/national-account invoicing as a distinct object inside **CDK Drive itself**
  (vs. the PACCAR Fleet Services layer sitting alongside it) is `UNVERIFIED` — no public CDK
  Drive spec names a fleet-billing or national-account object.
- Mobile service: no CDK Drive-specific public documentation found; Decisiv is the documented
  mechanism for field/roadside service coordination at PACCAR dealers, but Decisiv is a
  separate PACCAR-operated platform, not a CDK Drive module — `UNVERIFIED` whether CDK Drive
  has any native mobile-service RO type.

## What I could not verify

- Field-level or table-level names for the deal desk/washout screen, We-Owe line-item
  structure, or any general-purpose "Deals" write API (only a read-only FI Sales extract and
  a referenced-but-unconfirmed Deals spec ID were found).
- Any public API for MPI (multi-point inspection), sublet lines, or RO quality-control
  sign-off as distinct objects.
- Special-order and counter-ticket header/line field names in Parts.
- A generic (non-PACCAR) warranty-claim CRUD API in CDK Drive.
- Named AR screens/tables for statements, deposits, and daily deposit reconciliation.
- Confirmation of three-way match logic natively inside CDK Drive AP (only inferred from ERP
  norms and a competitor DMS's PACCAR integration).
- Any CDK Drive-native payroll or commission-calculation API — all evidence points to
  file/GL-push integration via third-party payroll vendors.
- Whether CDK Drive itself (as opposed to the PACCAR Fleet Services/Decisiv layer) has a
  native multi-unit fleet billing or mobile-service RO object.

## Proposed SAP-shape mapping

| CDK/dealer concept | Proposed SAP object in the twin | Rationale |
|---|---|---|
| Deal (pending → finalized) | Sales order (VBAK/VBAP) header/line, with a custom `ZDEAL` status field for Pending/Booked/We-Owe | Mirrors CDK's own Pending→Finalized status semantics |
| We-Owe | Open sales-order line held back post-billing (or `ZWEOWE` sub-table) | Distinct receivable-like obligation, not a GL posting until fulfilled |
| F&I product / finance reserve | Condition records on the sales order (KONV) + a chargeback reserve GL account | Reserve accrual behaves like a rebate/accrual condition |
| Repair Order (open/WIP/closed) | Service order (AUFK/AFKO) with WIP settled via results analysis (like CO-PA/WIP settlement) | CDK's WIP-then-close pattern maps directly to SAP service-order WIP settlement |
| Service Line (labor/parts) | Order operations (AFVC) and components (RESB) under the service order | 1:1 with CDK service line semantics |
| Parts sale (open/closed) — counter/pick ticket | Sales order or delivery (LIPS) against MARA/MARD parts master already in the twin | Reuses existing SAP MM shape; "open" = allocated/reserved, "closed" = PGI'd and billed |
| Warranty claim (PRWS draft → OEM) | Debit memo request / claim object (analogous to VBRK claim type) with a receivable GL account | Claims behave like a customer (OEM) receivable with adjustment/chargeback postings |
| Cashiering / Payment Settling | FI document (BKPF/BSEG) posted via a custom payment-clearing interface | PromiseID pattern maps to an async payment-clearing idoc |
| AP vendor invoice (incl. OEM parts) | MM invoice verification (MIRO) against PO (EKKO/EKPO) and goods receipt (MSEG) | Matches the three-way-match norm even though CDK's native equivalent is unverified |
| Payroll flag hours / commission | HR time evaluation feed (via a custom `ZFLAGHRS` staging table) into FI/CO, since no native CDK API exists | Reflects the file/GL-push reality documented for ADP/Netchex/Workzoom |
| Fleet/national account (PACCAR) | Customer master extension (KNA1/KNVV) with a fleet hierarchy flag + EDI billing interface | Mirrors PACCAR Parts Fleet Services' consolidated-billing/EDI pattern layered outside CDK Drive |
