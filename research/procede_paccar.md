# Procede Software (Excede DMS) ↔ PACCAR Interface Inventory

**Prepared for:** reverse-specification of Procede/Excede's PACCAR (Kenworth/Peterbilt/PACCAR Parts) integration footprint
**Scope:** Every named interface between Excede DMS (Procede Software, Solana Beach/San Diego, CA) and PACCAR-side systems, sourced from Procede's own site, press releases, LinkedIn/Facebook product-update posts, and the Decisiv/Peterbilt of Atlanta case study. Each row is marked **DOCUMENTED** (direct primary-source quote) or **UNVERIFIED** (inferred/no direct Procede-side quote found).

---

## 1. Master interface inventory

### 1.1 PACCAR OPC (Online Parts Counter) Integration

| Field | Detail |
|---|---|
| PACCAR-side system | PACCAR Online Parts Counter (OPC) — "an eCommerce platform built to help dealerships and their customers find and order the parts they need, with visibility into available inventory across a company's network" |
| Direction | Bidirectional (Excede ⇄ OPC): parts search/pricing pulled from Excede into OPC storefront; orders pushed from OPC into Excede |
| Business object / fields | Parts orders, order status, loyalty coupons/offers, Canadian customer & CAD currency fields, "OPC Order ID," line-item comments for failed part insertions |
| Transport/mechanism | "A Windows application, web service, and Excede API" |
| Cadence | Real-time ("real-time order status updates"; "Real-time integration ensures loyalty members receive accurate pricing") |
| Certification status | Named Procede product line (v1.1, v1.2 documented); no separate certifying body named beyond PACCAR/Procede partnership |
| Exact quoted wording | "The PACCAR OPC Integration is an add-on tool for Excede that combines a Windows application, web service, and Excede API to exchange data between Excede and the PACCAR Online Parts Counter (OPC) platform. PACCAR OPC is an eCommerce platform built to help dealerships and their customers find and order the parts they need, with visibility into available inventory across a company's network. Coupled with the PACCAR Loyalty Program Integration, it delivers faster performance and significantly reduces the steps required for logging in, searching for parts, ordering, and tracking shipments." — Procede Software, PACCAR OPC Integration v1.2 product-update post |
| URL | [Procede Software LinkedIn – PACCAR OPC Integration v1.2](https://www.linkedin.com/posts/procede-software_procede-product-paccar-opc-integration-activity-7478509316933578753-_7Wc) ; also [Facebook mirror](https://www.facebook.com/procedesoftwareofficial/posts/congratulations-to-scott-coleson-of-our-customer-fourstar-freightliner-for-being/2998645510231135/) ; earlier version [PACCAR OPC Integration v1.1](https://www.linkedin.com/posts/procede-software_procedesoftware-excededms-productupdate-activity-7425278583058804737-qq_b) |
| Status | **DOCUMENTED** |

Additional v1.2 detail (exact quote): "Improved Visibility for Failed Part Insertions: Two new BCS settings (OPC\MissingPartCommentId and OPC\MissingPartCommentNote) add line-item comments in Excede when parts fail to be added to an order... Canadian Customer and Currency Support: The integration now supports Canadian customers and Canadian Dollar (CAD) currency... OPC Order ID in File Names: The OPC Order ID is now included alongside the timestamp in parts order request and response file names." — [Procede Software LinkedIn – PACCAR OPC Integration v1.2](https://www.linkedin.com/posts/procede-software_procede-product-paccar-opc-integration-activity-7478509316933578753-_7Wc)

### 1.2 PACCAR Loyalty Program Integration

| Field | Detail |
|---|---|
| PACCAR-side system | PACCAR Loyalty Program (Kenworth Privileges / Peterbilt Preferred / TRP Performance — named generically by PACCAR Parts; not spelled out on Procede's own pages) |
| Direction | Excede ⇄ OPC/Loyalty Program — Excede checked for loyalty offers; coupons applied to pricing/orders |
| Business object / fields | Loyalty offers, coupons, "Expired" column in temp table, customer orders |
| Transport/mechanism | Real-time integration; Excede "temp table" for coupon tracking/redemption |
| Cadence | Real-time |
| Certification status | Versioned Procede product (v1.1, v1.3 referenced) |
| Exact quoted wording | "Enhanced OPC Parts Search for Loyalty Members: The OPC website now communicates directly with Excede to check for available loyalty offers, applying coupons to parts pricing and customer orders seamlessly. Loyalty Card Offer Redemption: OPC orders with loyalty coupons are inserted into Excede's temp table for streamlined tracking and redemption... Schema Updates: Added an 'Expired' column to the temp table for compatibility with PACCAR Loyalty Program Integration v1.3, ensuring reliable coupon tracking and redemption." — Procede Software, PACCAR OPC Integration v1.1 post |
| URL | [Procede Software LinkedIn – PACCAR OPC Integration v1.1](https://www.linkedin.com/posts/procede-software_procedesoftware-excededms-productupdate-activity-7425278583058804737-qq_b) |
| Status | **DOCUMENTED** (as a companion/adjacent integration referenced inside the OPC posts; no dedicated standalone Procede post found for "PACCAR Loyalty Program Integration" itself) |

### 1.3 PRWS — PACCAR Registration and Warranty System Integration (warranty claims + feedback loop)

| Field | Detail |
|---|---|
| PACCAR-side system | PACCAR Registration and Warranty System (PRWS) |
| Direction | **Bidirectional — this is the core dealer→OEM feedback loop.** Dealer transmits warranty claims to PACCAR; PACCAR returns real-time claim responses/Claim Numbers; dealer pulls SIR sheets down from PACCAR |
| Business object / fields | Warranty claims; Concern, Cause, and Correction fields; Campaign Code; Claim Category (including "PBSA for Steel Axle claims"); Claim Numbers; Service Information Record (SIR) Sheets (PDF) |
| Transport/mechanism | Automated claim transmission with resubmission/save-for-later capability; PDF retrieval of SIR sheets directly from PACCAR |
| Cadence | Real-time responses on submission; claims can be saved and resubmitted |
| Certification status | Versioned Procede product (v1.2 documented); framed explicitly around "compliance with PACCAR requirements" |
| Exact quoted wording | "PRWS Integration is a powerful Excede solution that streamlines PACCAR warranty claim processing. It allows dealerships to automatically transmit claims, receive real-time responses, resubmit as needed, and even save claims for later submission, reducing manual effort and improving efficiency... SIR Sheet Access: Pull Service Information Record (SIR) Sheets (PDF) directly from PACCAR. File Claim Feature: Resend claims and generate new Claim Numbers without re-entering data. Enhanced Accuracy: Updates to Concern, Cause, and Correction fields, corrected Campaign Code formatting, and improved Claim Category options (including PBSA for Steel Axle claims)." — "PRWS v1.2 enhances warranty claim management with new automation, accuracy, and access features, helping dealerships save time and ensure compliance with PACCAR requirements," – Rodrigo Piccini, MSc, VP of Integrations, Procede Software |
| URL | [Procede Software LinkedIn – PRWS v1.2](https://www.linkedin.com/posts/procede-software_procedesoftware-excededms-productupdate-activity-7402395748069548032-qWoj) |
| Status | **DOCUMENTED** — this is the clearest named dealer-to-OEM feedback interface in the corpus (warranty claim data flowing up to PACCAR, with PACCAR return responses) |

Cross-reference (not a Procede-Excede citation, provided only as corroborating context on the PACCAR-side taxonomy — see §4): a rival DMS vendor's PACCAR integration page separately confirms "PRWS Warranty Claims: Warranty claims can be easily created and updated with data captured from the [DMS] repair order. Open campaigns and recalls are optionally brought into the repair order, and attachments from the repair order can be added to the claim." — [Karmak – PACCAR Karmak Integration](https://www.karmak.com/integrations/paccar)

### 1.4 PACCAR eInvoicing Integration (Electronic Invoices)

| Field | Detail |
|---|---|
| PACCAR-side system | PACCAR electronic parts/vehicle invoicing system |
| Direction | PACCAR → Excede (invoice import); Excede matches to PO/receiving data |
| Business object / fields | Debit/credit (D/C) memos; purchase orders (POs); core charges; invoice number vs. shipping reference; MemTypIDs (parts, cores, credits); invoice due dates and posting dates |
| Transport/mechanism | "A Windows application that uses ... EDI 810 Inbound Invoice technology"; updated to use the Excede API |
| Cadence | Not stated as batch/real-time explicitly, but v1.2 description implies transactional import per invoice |
| Certification status | Versioned Procede product (base version + v1.2 documented) |
| Exact quoted wording (base) | "PACCAR eInvoicing Integration automates the import and processing of PACCAR invoices into Excede using EDI technology. It creates debit and credit memos, matches them to purchase orders, and helps ensure dealerships only pay for the parts they receive." — Procede Software, PACCAR eInvoicing Integration post |
| Exact quoted wording (v1.2) | "PACCAR eInvoicing Integration includes a Windows application that uses Fusion eData Exchange EDI 810 Inbound Invoice technology to electronically import and process PACCAR invoices. It automatically creates debit/credit (D/C) memos in Excede, finds posted purchase orders (POs) to balance those memos, and ensures your dealership only pays for the PACCAR parts you received." — "PACCAR eInvoicing Integration v1.2 brings a wide range of enhancements that give dealerships more control, accuracy, and efficiency across the entire invoice processing workflow. From smarter PO matching to flexible accounting rules, teams can spend less time on manual corrections and more time focused on what matters," – Danielle Castaing, Integrations Product Manager, Procede Software |
| URL | Base: [Procede Software LinkedIn – PACCAR eInvoicing Integration](https://www.linkedin.com/posts/procede-software_procede-product-paccar-einvoicing-integration-activity-7453449699602239488-Wt5v) ; v1.2: [Procede Software LinkedIn – PACCAR eInvoicing Integration v1.2](https://www.linkedin.com/posts/procede-software_procede-product-paccar-einvoicing-integration-activity-7489057857422696448-2mIw) |
| Status | **DOCUMENTED**. Note: the "Fusion eData Exchange" phrase appears verbatim in the Procede v1.2 post, but "Fusion" is also the brand name of a competing DMS (Karmak's Fusion) — this may reflect PACCAR's own EDI gateway naming shared across DMS vendors, or a labeling artifact in Procede's post; flagged for reader awareness rather than silently corrected. |

Corresponds to the general "ELECTRONIC INVOICES" and "PARTS PO EXPORT" categories on Procede's integrations page: "These integrations allow your OEM to invoice you for vehicle and/or parts orders. With Electronic Invoices integration within Excede, the invoice is automatically compared to the original purchase order and receiving reference number, ensuring you only pay for parts that were actually delivered." — [Procede Software – OEM Integrations for Dealers](https://www.procedesoftware.com/integrations/)

### 1.5 PACCAR MDI — Managed Dealer Inventory

| Field | Detail |
|---|---|
| PACCAR-side system | PACCAR Parts Managed Dealer Inventory (MDI) |
| Direction | Bidirectional: Excede parts sales/demand data → PACCAR; PACCAR order recommendations → Excede |
| Business object / fields | Parts inventory stocking recommendations, order recommendations, retail transaction visibility |
| Transport/mechanism | Not explicitly named on Procede's own pages (no dedicated Procede press release/LinkedIn post found describing MDI's transport mechanism); PACCAR's own page states recommendations are "transmitted electronically to the dealer daily" |
| Cadence | Daily, per PACCAR's own description: "Based on data analysis, parts order recommendations are developed for each dealer location and transmitted electronically to the dealer daily." |
| Certification status | Listed as a core, long-standing Procede/Excede–PACCAR interface; explicitly praised by a named PACCAR dealer customer |
| Exact quoted wording (Procede customer testimonial) | "Using the PACCAR integrations has greatly improved our overall business process and customer satisfaction. The MDI interface has helped improve our inventory accuracy and levels for better customer satisfaction, and the Service Gate interface makes it seamless for customers that charge with the OEM. Our receivables are paid timely through this process, and this contributes to improved cash flow. A must-have for any PACCAR dealer." — Kent Arcement, Business System Analyst, Performance Truck |
| Exact quoted wording (Procede integrations page, general MDI category) | "MANAGED DEALER INVENTORY: An advanced inventory program that uses forecasting and replenishment to help dealers effectively manage parts inventory using Excede data. Better manage your inventory through integration with OEM MDI to help with inventory stocking recommendations." |
| Exact quoted wording (PACCAR's own description of MDI, non-Procede source) | "PACCAR Parts Managed Dealer Inventory Program, or MDI, is one of the most advanced technologies in the supply chain. MDI allows PACCAR Parts to manage each dealer's inventory planning functions and provides visibility to retail transactions. Based on data analysis, parts order recommendations are developed for each dealer location and transmitted electronically to the dealer daily." |
| URL | [Procede Software – OEM Integrations for Dealers](https://www.procedesoftware.com/integrations/) ; [Procede Software – Testimonials Archive](https://www.procedesoftware.com/testimonials/page/2/) ; [Procede Software – Dealer Management Service Solutions](https://www.procedesoftware.com/solutions/service/) ; PACCAR-side description: [PACCAR Parts – Technology and Innovation](https://www.paccarparts.com/technology/) |
| Status | **DOCUMENTED** for existence/business value and PACCAR-side cadence; **UNVERIFIED** for the specific transport mechanism/protocol as implemented on the Excede side (no Procede-authored technical description of file format found) |

### 1.6 PACCAR Parts Fleet Services / Service Gate

| Field | Detail |
|---|---|
| PACCAR-side system | PACCAR Parts Fleet Services ("Service Gate") |
| Direction | Bidirectional: Excede sends invoices to Service Gate; Service Gate returns remittance/payment authorization to Excede |
| Business object / fields | Repair-order/invoice charges for fleet and national-account customers; preauthorization on estimates; authorization on completed work; remittance |
| Transport/mechanism | Not explicitly detailed in Procede's own materials (no dedicated Procede press release found); described generically as an "interface" |
| Cadence | Transactional, tied to repair-order completion/invoicing; described as ensuring "receivables are paid timely" |
| Certification status | Named, long-standing Procede/Excede–PACCAR interface, customer-validated |
| Exact quoted wording | "...the Service Gate interface makes it seamless for customers that charge with the OEM. Our receivables are paid timely through this process, and this contributes to improved cash flow. A must-have for any PACCAR dealer." — Kent Arcement, Business System Analyst, Performance Truck |
| URL | [Procede Software – OEM Integrations for Dealers](https://www.procedesoftware.com/integrations/) ; [Procede Software – Dealer Management Service Solutions](https://www.procedesoftware.com/solutions/service/) |
| Status | **DOCUMENTED** for existence and business value; **UNVERIFIED** for transport/technical mechanism on the Excede side. (A competing DMS vendor's PACCAR page separately describes the PACCAR-side workflow as: "Your fleet and national account customers can charge the cost of parts and service to their Fleet Services payment card. You're able to obtain preauthorization on estimates and or authorization on completed work or parts purchases. Final invoices are securely transmitted to Service Gate, and remittance is automatically retrieved for you." — [Karmak – PACCAR Karmak Integration](https://www.karmak.com/integrations/paccar) — cited only as corroborating context on the PACCAR-side system's general behavior, not as a Procede-Excede-specific claim.) |

### 1.7 Financial Statements (Financial Statement Download to PACCAR)

| Field | Detail |
|---|---|
| PACCAR-side system | PACCAR financial-statement collection portal (unnamed on Procede's site) |
| Direction | Excede → PACCAR (dealer financial data upload/download to OEM) |
| Business object / fields | Financial statement line items required by OEM reporting format |
| Transport/mechanism | "Dynamic Excel spreadsheets that extract, calculate and format financial information" |
| Cadence | Not stated (implied periodic/monthly, consistent with standard OEM financial reporting cycles) |
| Certification status | Listed as a general OEM integration category, not PACCAR-exclusive |
| Exact quoted wording | "FINANCIAL STATEMENTS: Dynamic Excel spreadsheets that extract, calculate and format financial information required by your OEM." |
| URL | [Procede Software – OEM Integrations for Dealers](https://www.procedesoftware.com/integrations/) ; also listed at [Procede Software – DMS Accounting Software](https://www.procedesoftware.com/solutions/accounting/) |
| Status | **DOCUMENTED** as a general OEM interface category; **UNVERIFIED** as PACCAR-specific (Procede's page does not name PACCAR explicitly in this category, though PACCAR's supplier requirements confirm PACCAR does require annual financial statement submission from suppliers/dealers: "PACCAR suppliers are expected to make their Annual Financial Statements available to PACCAR Purchasing for review of their financial position." — [PACCAR – Supplier Requirements](https://www.paccar.com/products-services/paccar-purchasing/supplier-requirements/), a general supplier-relations page, not dealer-DMS-specific) |

### 1.8 Parts PO Export / Parts Orders (Stock & Emergency Orders)

| Field | Detail |
|---|---|
| PACCAR-side system | PACCAR Parts ordering system |
| Direction | Excede → PACCAR |
| Business object / fields | Parts, quantities, and order metadata from Excede parts purchase orders |
| Transport/mechanism | Export file (format unspecified in Procede materials) |
| Cadence | Not stated |
| Certification status | General OEM integration category |
| Exact quoted wording | "PARTS PO EXPORT: Easily export parts, quantities and other needed information from Excede parts purchase order to send to OEMs" |
| URL | [Procede Software – OEM Integrations for Dealers](https://www.procedesoftware.com/integrations/) |
| Status | **DOCUMENTED** as general OEM category; **UNVERIFIED** as PACCAR-specific by name (not explicitly tied to PACCAR in Procede's own copy, though PACCAR is a named PACCAR-integration customer elsewhere on the same page) |

### 1.9 Price Tapes / Cross-Reference / Preferred Pricing / POS Reconciliation / National Account Invoicing / Portal Billing (general OEM categories, PACCAR applicability unstated by name)

| Field | Detail |
|---|---|
| Direction & mechanism | Per Procede's integrations page: <br>• "PRICE TAPES: The Price Tape Import Wizard enables processing and uploading of regular price tapes from the OEMs to Excede to support parts pricing updates and keep your parts inventory profitable." (OEM → Excede) <br>• "CROSS-REFERENCE: Some OEM integrations provide parts cross reference database to/from alternate providers, making it easier to locate parts." <br>• "PREFERRED PRICING: Support special pricing programs your OEM has with key customers... Posted orders are transmitted securely to the OEM for payment at time of invoice." (Excede → OEM) <br>• "POS RECONCILIATION: Selected OEMs provide a settlement file that is used by Excede to help you reconcile all POS transactions." (OEM → Excede) <br>• "NATIONAL ACCOUNT INVOICING: Facilitate the billing of national accounts that lease trucks across multiple dealerships." <br>• "PORTAL BILLING: Portal Billing allows dealerships to send and receive the billing information for rented truck repair orders and rental billing information for selected OEMs." |
| URL | [Procede Software – OEM Integrations for Dealers](https://www.procedesoftware.com/integrations/) |
| Status | **DOCUMENTED** as general Procede/Excede OEM-integration categories; **UNVERIFIED** as specifically applying to PACCAR (Procede's page explicitly attributes "selected OEMs" / "some OEM integrations" rather than confirming PACCAR by name for these particular line items — task requirement is to mark named-but-unattributed items as unverified for PACCAR specificity) |

### 1.10 Standard Repair Time Updates (Labor Guides)

| Field | Detail |
|---|---|
| Direction | OEM → Excede |
| Business object / fields | OEM-specified labor guide standard repair times |
| Exact quoted wording | "STANDARD REPAIR TIME UPDATES: Keep your Labor Guides current with OEM specified guides that are auto-created and updated in Excede." |
| URL | [Procede Software – OEM Integrations for Dealers](https://www.procedesoftware.com/integrations/) |
| Status | **DOCUMENTED** as general category; **UNVERIFIED** as PACCAR-specific by name |

### 1.11 Service Communications (repair order/estimate ingestion from OEM system)

| Field | Detail |
|---|---|
| Direction | OEM → Excede |
| Business object / fields | Service data pulled in as a repair order or estimate |
| Exact quoted wording | "SERVICE COMMUNICATIONS: Quickly pull service data from your OEM system into Excede as a repair order or estimate." |
| URL | [Procede Software – OEM Integrations for Dealers](https://www.procedesoftware.com/integrations/) |
| Status | **DOCUMENTED** as general category; **UNVERIFIED** as PACCAR-specific by name (though functionally this is the same category into which the Decisiv↔Excede case-export flow, §2 below, fits for PACCAR dealers) |

### 1.12 Warranty Claim Export Wizard (general, cross-OEM label — corroborates PRWS mechanics)

| Field | Detail |
|---|---|
| Exact quoted wording | "WARRANTY CLAIMS: The Warranty Claim Export wizard is used to prepare and export Excede warranty claims to your OEM." |
| URL | [Procede Software – OEM Integrations for Dealers](https://www.procedesoftware.com/integrations/) |
| Status | **DOCUMENTED** as general category; corroborates §1.3 (PRWS) mechanics for PACCAR specifically, since PRWS is confirmed by name as the PACCAR-specific warranty product |

### 1.13 Truck build data / B2B feed (PACCAR B2B infrastructure)

| Field | Detail |
|---|---|
| PACCAR-side system | PACCAR B2B infrastructure (truck build data/specifications) |
| Direction | PACCAR → dealer DMS |
| Business object / fields | Truck build data, specifications, key vehicle components, order dates |
| Transport/mechanism | Not documented on any Procede-authored source found |
| Certification status | No Procede press release, product page, or LinkedIn post naming a PACCAR build-data/B2B integration for Excede was located in this research |
| Corroborating (non-Procede) source | A competing DMS vendor documents this exact PACCAR-side capability for its own product: "Truck Order Data: Fusion's integration with PACCAR's B2B infrastructure makes it possible to retrieve truck build data and specifications and update the information in your Fusion system. Key vehicle components, dates, and other information are mapped to the fields you want to track with no double entry of data." — [Karmak – PACCAR Karmak Integration](https://www.karmak.com/integrations/paccar) |
| Status | **UNVERIFIED for Procede/Excede.** No primary Procede source documents an equivalent "Truck Order Data"/build-data/B2B feed interface. Flagged as a likely gap in Procede's public-facing documentation rather than an absent capability — Procede's October 2023 press release references "three new integrations" without naming all three (see §3), so a build-data interface may exist undocumented publicly. |

### 1.14 FOCUS CRM

| Field | Detail |
|---|---|
| PACCAR-side system | PACCAR Parts FOCUS CRM tool |
| Direction | Dealer DMS → FOCUS (customer/parts sales data feed for purchasing-pattern insights) |
| Certification status | No Procede-authored press release, product page, or LinkedIn/Facebook post naming a "FOCUS" or "FOCUS CRM" integration with Excede was found in this research |
| Corroborating (non-Procede) source | "FOCUS: Fusion automates sending customer and parts sales data to the PACCAR Parts FOCUS CRM tool, where it provides insights into customer purchasing patterns so you can concentrate on increasing your sales." — [Karmak – PACCAR Karmak Integration](https://www.karmak.com/integrations/paccar) |
| Status | **UNVERIFIED for Procede/Excede.** No primary-source evidence Procede has a named FOCUS CRM interface; only confirmed for a competing DMS. |

### 1.15 PacLease RPS (Rental/Lease Performance System)

| Field | Detail |
|---|---|
| PACCAR-side system | PacLease Rental Performance System (RPS) |
| Direction | RPS → dealer DMS (customer, unit, and rental contract sync) |
| Certification status | No Procede-authored source found naming an RPS/PacLease integration with Excede |
| Corroborating (non-Procede) source | "Rental Performance System (RPS): Our integration saves your rental managers time by creating and updating customers, units, and rental contracts in Fusion based on your activity in the PacLease RPS system." — [Karmak – PACCAR Karmak Integration](https://www.karmak.com/integrations/paccar) |
| Status | **UNVERIFIED for Procede/Excede.** Procede's own site does document a general "Lease-Rental" solution module ("Manage reservations, billing, and fleet history with centralized, multi-location lease and rental tools" — [Procede Software – Excede Dealer Management System](https://www.procedesoftware.com/excede/)), but no PACCAR/PacLease-RPS-specific interface is named in any Procede primary source located. |

### 1.16 Decisiv / PACCAR Solutions (real-time bidirectional service-event sync) — see full detail in §2

| Field | Detail |
|---|---|
| PACCAR-side system | Decisiv Service Relationship Management (SRM), which serves as the platform underlying PACCAR's dealer-facing service tools (branded for Kenworth as TruckTech+ and for Peterbilt as SmartLINQ, per a competing DMS's PACCAR page) |
| Direction | Fully bidirectional, real-time |
| Certification status | Confirmed, named, ongoing product partnership between Decisiv and Procede — see §2 |
| Status | **DOCUMENTED** — detailed in §2 |

---

## 2. Decisiv ↔ Excede real-time bidirectional sync (Peterbilt of Atlanta case study) — verbatim detail

Source: [Decisiv – Peterbilt of Atlanta case study (web)](https://www.decisiv.com/peterbilt-of-atlanta/) and identical [Decisiv – Peterbilt of Atlanta case study (PDF)](https://www.decisiv.com/wp-content/uploads/2024/09/Decisiv-Case-Study-Peterbilt-Atlanta.pdf)

- **Case export / creation:** "For existing customers, the information is then used to open a service case in the Decisiv SRM application at the truck. Service events for new customers are added at a desktop terminal. In both instances, the service event is immediately exported to Excede for pricing, including costs for fleets participating in PACCAR national fleet programs."
- **National fleet program costs:** confirmed in the same sentence above — the export to Excede specifically carries "costs for fleets participating in PACCAR national fleet programs."
- **Line-level updates / parts and diagnostics flow:** "Information from technicians is then used by the foremen to start the estimate process. Included are diagnostic data, photos and parts requests, which are sent automatically to the parts department. There, items are added directly into the Decisiv SRM case and sent to Excede for invoicing."
- **Invoicing:** confirmed above — parts items are "added directly into the Decisiv SRM case and sent to Excede for invoicing."
- **Warranty check:** "The workflow also connects to the dealership's warranty department to verify any existing coverage."
- **Approval routing:** "Once the shop foreman reviews the work order and verifies that all the correct jobs and parts have been added to the case, the estimate is sent to the service advisor who sets an estimated time of completion for the repair and requests approval via text, email or by phone depending on the customer's communication preference."
- **Bidirectional real-time sync (explicit claim):** "With the use of Decisiv SRM and Excede, Peterbilt of Atlanta benefits from the ability to sync real-time information between the applications and reduce errors from duplicate data entries."
- **Quantified outcomes:** "there has been as much as an 80% improvement in reduced dwell time because we can turn around estimates that much faster" (Wes Gayhart, VP of Operations, Peterbilt of Atlanta); "as much as 90% success meeting the dealership's goal of providing repair estimates to customers within 4-1/2 hours of check in"; approvals via text "80% faster than with email."
- **Scale:** "manages over 450 service events monthly with the integrated solutions across six service locations."

**Corroborating Procede-Decisiv partnership press release** (names the integration as an ongoing, expanding joint product, not one-off): "Dealers using the Procede enterprise software solution Excede with Decisiv's SRM platform have a more efficient means of managing the entire service event process from vehicle check-in to return to service. With the integrated solutions, all service event information necessary to generate a repair order is captured in SRM and is used to create a case where key data is passed seamlessly to the Excede DMS... Future feature integrations being developed by Decisiv and Procede will further enhance the accuracy of information in both systems by describing repairs in notes entered by technicians. Additionally, Decisiv SRM and Excede will support non-VIN entry and allow the creation of repair orders for managing the service event process for serial number-based assets." — Larry Kettler, CEO of Procede, and Dick Hyatt, President and CEO of Decisiv. Decisiv is separately described as certified: "Decisiv and Procede, a Gold-level certified DMS partner, are firmly committed on continuing to streamline the management of commercial vehicle service events..." — [Decisiv – Decisiv and Procede are Delivering Streamlined Service Management Solutions](https://www.decisiv.com/decisiv-and-procede-are-delivering-streamlined-service-management-solutions/) (January 30, 2024)

**Status: DOCUMENTED** with precise, quoted, primary-source wording on all requested elements (case export, pricing, national fleet program costs, invoicing, line-level updates).

*Note on PACCAR branding:* Decisiv's platform underlies PACCAR's own dealer/fleet-facing service tools. A competing DMS vendor's PACCAR integration page names these PACCAR-branded front ends explicitly: "Kenworth TruckTech+ / Peterbilt SmartLINQ (Decisiv): Estimates are transferred directly into Fusion repair orders and can be updated as often as needed... Changes to the open repair order tasks, parts, and miscellaneous charges are seamlessly sent back to TruckTech+ or SmartLINQ, keeping the case up to date." — [Karmak – PACCAR Karmak Integration](https://www.karmak.com/integrations/paccar). No Procede-authored source in this research names "TruckTech+" or "SmartLINQ" directly; Procede/Decisiv materials consistently refer only to "Decisiv SRM." This PACCAR-branding detail is flagged **UNVERIFIED for Procede specifically** even though the underlying Decisiv relationship is confirmed.

---

## 3. October 2023 PACCAR press release — "three new integrations" (names not fully enumerated)

Procede's October 31, 2023 press release confirms an active, ongoing expansion of the PACCAR interface set but — notably — does **not name all three new integrations** in the surviving text: "Procede Software, a leading heavy-duty commercial vehicle dealer business system (DBS) and solutions provider, today announced the release of three new integrations between its Excede software platform and PACCAR's proprietary systems. Together with Procede's existing PACCAR-specific integrations, they build on an already comprehensive integration set designed to streamline operations for dealerships across North America... Procede's comprehensive set of integrations between Excede and PACCAR's proprietary systems supports critical processes and operations for key departments across the dealership. From parts and service to accounting and sales, the integrations enable cross-platform analytics that drive deeper business insights to facilitate improved eCommerce and streamlined parts and service processes." — [PR Newswire – Procede Software Adds Key Functionality to Comprehensive Set of PACCAR Integrations with Three New Releases](https://www.prnewswire.com/news-releases/procede-software-adds-key-functionality-to-comprehensive-set-of-paccar-integrations-with-three-new-releases-301971861.html) (mirrored at [Procede Software – same release](https://www.procedesoftware.com/paccar-integrations-three-new-releases/))

Quoted supporting testimonial from a named PACCAR dealer in the same release: "Tight integrations with our OEM-proprietary business systems are so important. They provide us with a means to do things better, faster, and more cost-efficiently in an ever-changing environment... I appreciate how responsive Procede is in integrating new OEM applications with Excede." — Scott Pearson, Dealer Principal, Peterbilt of Atlanta

**Status: DOCUMENTED** for the fact of three new PACCAR integrations released in October 2023; **UNVERIFIED** as to which three specific named products they were (plausibly overlapping with the OPC, eInvoicing, or PRWS products documented via later LinkedIn posts, but no direct evidence ties this release to those specific product names).

---

## 4. General certification pattern with other OEMs (evidence of Procede's certification model)

| OEM | Quoted evidence | URL |
|---|---|---|
| Navistar (International, IC Bus) | "Procede Software has been a Navistar Certified Dealer Management System Partner since 2019." Also: "Procede Software, a leading heavy-duty commercial vehicle dealer management system (DMS) and solutions provider, today announced it is the leading Navistar Certified DMS Partner in terms of the number of International and IC Bus dealership locations using its Excede business system." | [Procede Software – Navistar Certified DMS Partner, Procede Software, Reaches #1 Position](https://www.procedesoftware.com/navistar-certified-dms-partner-procede-software-reaches-1-position-by-number-of-north-american-dealership-locations/) |
| Navistar (open-API framing) | "But when it comes to integrating with Navistar's systems, it's our open API that really sets us apart. The interoperability of the API means that not only can we integrate with Navistar's proprietary systems, pulling information into Excede when and where you need it, Navistar can integrate with Excede, pulling appropriate and approved information out of it and into their systems." | [Procede Software – When It Comes to Being the #1 Navistar-Certified DMS](https://www.procedesoftware.com/when-it-comes-to-being-the-1-navistar-certified-dms-by-number-of-rooftops-integrations-are-just-the-start/) |
| Hino | "Hino recently named Procede its preferred DMS provider." And: "Procede not only carried Mack and Volvo certification but had a comprehensive set of Hino integrations in place." (David Kriete, President & CEO, Kriete Truck Centers) | [Procede Software – Hino Names Procede Software a Preferred DMS Provider](https://www.procedesoftware.com/hino-names-procede-software-a-preferred-dms-provider-for-kriete-truck-centers-its-a-partnership-that-drives-business-impact/) |
| Daimler Truck North America (DTNA) | "Daimler Truck North America relies on Procede's API for many critical dealer applications, from parts inventory and sales, to managing service communications and throughput. Our dealers and customers benefit from the ecosystem Procede created that integrates with DTNA systems allowing for real-time information and data flow." — Kelly Gedert, GM of Strategic Value Chain & Technology, DTNA. Also: DTNA's own e-commerce platform, "Excelerator," is named directly: "Daimler Trucks North America (DTNA) operates Excelerator, an online parts store for browsing inventory, viewing customer-specific pricing, and placing orders fulfilled by dealers or PDCs. It integrates with Excede for real-time quantities and pricing, supports creating Front Counter Orders (FCOs) and Parts Purchase Orders (POs), and synchronizes order status." | [Procede Software – Five-Year Anniversary of the Excede API](https://www.procedesoftware.com/procede-software-celebrates-the-five-year-anniversary-of-the-excede-api-as-extensive-adoption-by-oems-solution-providers-and-dealerships-speeds-the-pace-of-industry-innovation/) ; DTNA Excelerator detail: [Procede Software LinkedIn company page](https://www.linkedin.com/company/procede-software) |
| Volvo / Mack | "Procede not only carries a Mack/Volvo certification, but is also committed to a forward-thinking relationship with our OEMs." — David Kriete, President & CEO, Kriete Truck Centers. Also a named product: "Mack Volvo PartsASIST Integration: ... connects Excede with the PartsASIST platform, automating parts lookup, ordering, and management ... enables real-time price tape uploads, inventory updates, pricing synchronization, and seamless creation of Front Counter Orders (FCOs)." | [Procede Software – OEM Integrations for Dealers](https://www.procedesoftware.com/integrations/) ; PartsASIST: [Procede Software LinkedIn – Mack Volvo PartsASIST Integration](https://www.linkedin.com/posts/procede-software_procedesoftware-excededms-oemintegrations-activity-7377042730990018561-Q_Uq) |
| PACCAR (Gold-level certification, via Decisiv) | "Decisiv and Procede, a Gold-level certified DMS partner, are firmly committed on continuing to streamline the management of commercial vehicle service events..." | [Decisiv – Decisiv and Procede are Delivering Streamlined Service Management Solutions](https://www.decisiv.com/decisiv-and-procede-are-delivering-streamlined-service-management-solutions/) |
| General OEM attendance/cadence | "The event also featured OEM-focused sessions—Daimler Truck North America, International Motors, LLC, Mack Trucks and Volvo Trucks North America, and PACCAR were all in attendance—and an expanded Pit Stop Expo where Procede Certified Partners showcased their solutions and integrations with Excede." | [Procede Software – Listening, Learning, and Delivering Product Advancements](https://www.procedesoftware.com/listening-learning-delivering-product-advancements-take-center-stage-annual-procede-software-conference/) |

**Pattern observed:** Procede's certification model is consistently framed around (1) a formal "Certified DMS Partner" or "preferred DMS provider" designation from the OEM, (2) the open Excede API as the shared technical substrate for building/maintaining OEM-specific interfaces, and (3) named, versioned point-products (e.g., PRWS, OPC, PartsASIST, Excelerator integrations) that are iterated on a rolling release cadence (v1.1, v1.2, v1.3, etc.) documented via LinkedIn product-update posts. PACCAR fits this same pattern (named integrations: OPC, PRWS, eInvoicing; named dealer testimonials referencing MDI and Service Gate; a "Gold-level" Decisiv-Procede certification), but Procede has not published a single-source "PACCAR Certified DMS Partner" press release comparable to the Navistar and Hino ones found in this research.

---

## 5. Open API / developer program / ExcedeConnect

- **No product literally named "ExcedeConnect" was found.** The task's target term does not appear on Procede's own site, in press releases, or in the LinkedIn corpus reviewed. Procede's equivalent, and only publicly documented, open integration platform is the **Excede API**.
- **Excede API — nature and history:** "Our RESTful API uses standard HTTP methods for lightweight, flexible, and easy integration. Swagger's UI creates a user-friendly interface that allows developers to explore our API directly in the browser." — [Procede Software – Dealership API Solution](https://www.procedesoftware.com/api/)
- **REST architecture, confirmed at launch of v2.0:** "Built using the REST development model, the Excede API provides the standard call format and parameters needed for software programmers to build integrations... Procede says that the API is available to all industry OEMs and Procede Certified Partners to facilitate integration development of their applications and new initiatives with Excede. Procede plans to release an API Developer's guide and open the API to include customers and other third-party developers to facilitate more seamless application interoperability in the future." — [Procede Software – Procede Software Releases Excede API v2.0](https://www.procedesoftware.com/procede-software-releases-excede-api-v2-0/) (originally also on [PR Newswire](https://www.prnewswire.com/news-releases/procede-software-releases-excede-api-v2-0--an-integration-acceleration-platform-for-partners-300793717.html), February 12, 2019)
- **Getting-started / access process (not fully "open" self-serve — gated via commercial work order):** "If you are interested in leveraging the Excede API, please submit a work order via our Customer & Resource Portal (login required). Our Customer Success team will review pricing details and provide a quote and/or contract terms." Also: "Procede also provides system and database administration support to establish a safe and secure sandbox environment during the initial development and testing phases. Throughout the development process, your project team will have direct access to Procede Developers and Product Owners via a messaging channel." — [Procede Software – Streamline Your Operations with the Excede API](https://www.procedesoftware.com/streamline-your-operations-with-the-excede-api/)
- **Certified Partner Program (formal third-party developer program):** "Procede Software's Certified Partner Program provides approved third-party software developers' access to a certified API, product management, and integration development resources allowing them to leverage the flexibility and power of Excede DMS's Microsoft SQL Server database engine and proactively and collaboratively develop certified integrations... To ensure third-party integrations work seamlessly with Excede, each integration will undergo rigorous QA testing before becoming Procede-certified and released to the market." — [Procede Software – Procede Software Announces Certified Partner Program](https://www.procedesoftware.com/procede-software-announces-certified-partner-program/)
- **Adoption evidence:** "Trusted by hundreds of developers and industry leaders, it delivers consistent performance, reliability, and scalability." — [Procede Software – Dealership API Solution](https://www.procedesoftware.com/api/); "the Excede API, which has seen rapid, widespread adoption by OEMs, third-party solution providers, and dealerships since its introduction" (5-year anniversary release, June 13, 2023) — [Procede Software – Five-Year Anniversary of the Excede API](https://www.procedesoftware.com/procede-software-celebrates-the-five-year-anniversary-of-the-excede-api-as-extensive-adoption-by-oems-solution-providers-and-dealerships-speeds-the-pace-of-industry-innovation/)
- **SQL Server direct access:** Procede does not market a formal "direct SQL access" developer product distinct from the API, but repeatedly emphasizes the underlying Microsoft SQL Server database as a source of data accessibility: "Excede DMS relies on a SQL Server database, and it is extremely well-structured and reliable. A benefit of the database is easier access to data and more flexibility in reporting." — Ken Ables, Director of Parts Operations, Performance Truck, quoted at [Procede Software – Excede Dealer Management System](https://www.procedesoftware.com/excede/)

**Status: DOCUMENTED** — Procede has a formally named, versioned, REST/Swagger-documented API (the "Excede API," not "ExcedeConnect") plus a "Certified Partner Program," both used as the technical substrate for all PACCAR (and other OEM) integrations described above; access is gated through a commercial work-order/quote process rather than fully self-service/public.

---

## 6. Dealer data ownership and data access/export

- **Explicit ownership claim (25th-anniversary retrospective):** "Procede took a different approach, prioritizing transparency, data ownership, and systems designed to align with real-world operations rather than requiring customers to adapt to rigid technology... The company also established a model in which customers retained ownership of their data while maintaining direct access to it. This approach continues to be a core part of Procede's platform and philosophy." — [Procede Software – Procede Software Marks 25 Years of Innovation and Industry Partnership](https://www.procedesoftware.com/procede-software-marks-25-years-of-innovation-and-industry-partnership/) (also syndicated at [National Law Review](https://natlawreview.com/press-releases/procede-software-marks-25-years-innovation-and-industry-partnership))
- **Customer testimonial reinforcing data access:** "Excede DMS opens up a whole new world of data availability. It provides the flexibility to manage both inventory and personnel and empowers managers to make good business decisions... With parts, there is so much opportunity for data analysis—parts turns, stocking requirements, outside sales, back counter sales, commissions. We've literally built hundreds of different types of custom reports." — Ken Ables, Director of Parts Operations, Performance Truck, [Procede Software – Excede Dealer Management System](https://www.procedesoftware.com/excede/)
- **Recent customer reinforcement (2026):** "Their platform gives us the visibility and control we need to manage operations effectively, and their team understands how dealerships actually run." — Brad Heil, Vice President of IT, McCoy Group, [Procede Software – 25 Years](https://www.procedesoftware.com/procede-software-marks-25-years-of-innovation-and-industry-partnership/)
- **Hosted/cloud caveat:** Procede also offers a hosted option in which Procede itself manages the database: "With Excede Hosted Services, Procede Software hosts the dealer's Excede database and Excede web applications in the cloud, providing 24/7 monitoring, secure unparalleled data access, data backups, and the management of software updates and upgrades." — [Procede Software – Procede Software Announces Its Latest Excede Hosted Services](https://www.procedesoftware.com/procede-software-announces-its-latest-excede-hosted-services/)

**Status: DOCUMENTED** — Procede explicitly and repeatedly (across a 2026 anniversary release and multiple customer testimonials spanning years) frames dealer data ownership and direct data access as a core differentiator, tied to the underlying Microsoft SQL Server architecture.

---

## 7. Summary table (condensed, for quick reference)

| # | Interface name | Direction | Mechanism | Cadence | Certification | Status |
|---|---|---|---|---|---|---|
| 1 | PACCAR OPC Integration | Bidirectional | Windows app + web service + Excede API | Real-time | Versioned Procede product (v1.1, v1.2) | DOCUMENTED |
| 2 | PACCAR Loyalty Program Integration | Bidirectional (via OPC) | Excede temp table + real-time comms | Real-time | Versioned (v1.1, v1.3 ref.) | DOCUMENTED |
| 3 | PRWS (PACCAR Registration and Warranty System) | Bidirectional — dealer→OEM feedback loop | Automated claim transmission + PDF pull (SIR sheets) | Real-time claim responses | Versioned (v1.2); "compliance with PACCAR requirements" | DOCUMENTED |
| 4 | PACCAR eInvoicing Integration | PACCAR → Excede | Windows app, EDI (810 Inbound Invoice referenced), Excede API | Transactional | Versioned (base + v1.2) | DOCUMENTED |
| 5 | PACCAR MDI | Bidirectional | Not detailed by Procede; PACCAR states "transmitted electronically... daily" | Daily (PACCAR-stated) | Long-standing named interface, customer-validated | DOCUMENTED (existence); UNVERIFIED (Excede-side mechanism) |
| 6 | PACCAR Service Gate (Fleet Services) | Bidirectional | Not detailed by Procede | Transactional | Long-standing named interface, customer-validated | DOCUMENTED (existence); UNVERIFIED (Excede-side mechanism) |
| 7 | Financial Statements | Excede → OEM | Dynamic Excel spreadsheets | Not stated | General OEM category | DOCUMENTED (general); UNVERIFIED (PACCAR-specific) |
| 8 | Parts PO Export | Excede → OEM | Export file | Not stated | General OEM category | DOCUMENTED (general); UNVERIFIED (PACCAR-specific) |
| 9 | Price Tapes / Cross-Reference / Preferred Pricing / POS Reconciliation / National Account Invoicing / Portal Billing | Mixed | File/settlement-based | Not stated | General "selected OEM" categories | DOCUMENTED (general); UNVERIFIED (PACCAR-specific) |
| 10 | Standard Repair Time Updates | OEM → Excede | Auto-created/updated labor guides | Not stated | General category | DOCUMENTED (general); UNVERIFIED (PACCAR-specific) |
| 11 | Service Communications | OEM → Excede | Pulls into RO/estimate | Not stated | General category | DOCUMENTED (general); UNVERIFIED (PACCAR-specific) |
| 12 | Warranty Claim Export Wizard | Excede → OEM | Export wizard | Not stated | General category (corroborates PRWS) | DOCUMENTED (general) |
| 13 | Truck build data / B2B feed | PACCAR → DMS | Not documented by Procede | Not stated | No Procede source found | UNVERIFIED for Procede (confirmed only for a competing DMS) |
| 14 | FOCUS CRM | DMS → PACCAR | Not documented by Procede | Not stated | No Procede source found | UNVERIFIED for Procede (confirmed only for a competing DMS) |
| 15 | PacLease RPS | PACCAR → DMS | Not documented by Procede | Not stated | No Procede source found | UNVERIFIED for Procede (confirmed only for a competing DMS) |
| 16 | Decisiv SRM ↔ Excede (PACCAR service ecosystem) | Fully bidirectional, real-time | Case sync (check-in → estimate → parts → invoice) | Real-time | "Gold-level certified DMS partner" (Decisiv) | DOCUMENTED |

---

## 8. Key gaps and caveats

1. **"ExcedeConnect" does not appear to exist as a Procede product name.** The only documented open developer platform is the "Excede API" (REST, Swagger-documented, gated via a commercial work-order process) plus the "Certified Partner Program."
2. **PACCAR's own system names for MDI, Service Gate, FOCUS CRM, PacLease RPS, and build-data/B2B feeds are independently confirmed by a competing DMS vendor's PACCAR integration page** ([Karmak – PACCAR Karmak Integration](https://www.karmak.com/integrations/paccar)), which is useful as corroborating evidence of the PACCAR-side taxonomy and general certification/scorecard pattern ("How does Karmak perform on PACCAR's OEM integration scorecard?") but is **not a Procede/Excede source** and must not be read as confirming Procede has built equivalent FOCUS CRM, PacLease RPS, or B2B build-data interfaces — those three remain unverified for Procede specifically.
3. **Procede has not published a single dedicated "PACCAR Certified DMS Partner" press release** analogous to its Navistar (#1 by rooftops, certified since 2019) and Hino ("preferred DMS provider") announcements, despite PACCAR clearly being one of Procede's most actively developed OEM relationships (three named, actively versioned 2023–2026 product lines: OPC, PRWS, eInvoicing).
4. **The October 31, 2023 press release announcing "three new integrations"** with PACCAR does not name the three products in the surviving text — a gap between the press release's existence and full interface-level attribution.
5. **MDI and Service Gate interface mechanics** (file format, transport protocol, batch vs. real-time) are attested only through customer testimonials and Procede's generic integration-category copy, not through a dedicated technical Procede press release or LinkedIn product-update post (unlike OPC, PRWS, and eInvoicing, each of which has version-numbered technical release notes).
