# Karmak Fusion ↔ PACCAR Interface Inventory

**Purpose:** Source-cited inventory of every *named* interface between Karmak Fusion DMS (Karmak Inc., employee-owned, Carlinville, IL) and PACCAR (Peterbilt/Kenworth/PACCAR Parts), compiled for reverse-specification of the incumbent "standard" DMS integration set among Kenworth and Peterbilt dealers.

**Compiled:** August 8, 2026
**Status legend:** **DOCUMENTED** = supported by a direct quote from a primary source fetched below. **UNVERIFIED** = referenced only in secondary/aggregator sources, or inferred, and not confirmed in a Karmak/PACCAR primary document.

---

## 1. Primary source used for the core interface list

The authoritative, current primary source is Karmak's own PACCAR OEM integration page (the `/oem-integrations/paccar` URL 301-redirects to this canonical page):

> "Karmak's PACCAR OEM integrations support critical parts, service, inventory, financial, and warranty workflows through seamless data exchange between PACCAR systems and Fusion."
— [PACCAR Karmak Integration, karmak.com](https://www.karmak.com/integrations/paccar)

That page's FAQ section also gives Karmak's own summary sentence, quoted here because it is the closest thing Karmak publishes to an official interface list:

> "Karmak integrates with a broad set of PACCAR programs, including Online Parts Counter (OPC), Managed Dealer Inventory (MDI), electronic parts invoices, electronic packing slips (ASN), warranty claims, PACCAR Parts Fleet Services, TruckTech+ and SmartLINQ (Decisiv), financial reporting, and truck order data."
— [PACCAR Karmak Integration, karmak.com](https://www.karmak.com/integrations/paccar)

---

## 2. Interface-by-interface inventory

### 2.1 Managed Dealer Inventory (MDI) — **DOCUMENTED** — bidirectional (dealer→PACCAR feedback loop + PACCAR→dealer)

| Field | Detail |
|---|---|
| PACCAR-side system name | Managed Dealer Inventory (MDI), also called "PACCAR Parts Managed Dealer Inventory Program" |
| Direction | **Bidirectional** — dealer sends demand data to PACCAR; PACCAR sends calculated orders back |
| Business object | Parts sales and demand data (dealer→PACCAR); calculated stock, "PACCAR Parts Marketing Suggestion" (MKT) and "Auto Confirmed" (COF) orders (PACCAR→dealer) |
| Transport/mechanism | Electronic file transmission ("transmitted electronically to the dealer daily" per PACCAR); internally, Karmak's Fusion build process names a "VMI" (Vendor Managed Inventory) header file, produced by a `CreateSendPaccarMDIDailyInventoryFile` routine in the `MgrPaccarMDI` class, and a distinct "COF file" returned from PACCAR |
| Cadence | Daily (per PACCAR's own description) |
| Karmak "certified" language | Karmak does not use the word "certified" on the PACCAR integration page itself, but a third-party DMS-comparison source (unverified, non-primary) states "PACCAR (Kenworth, Peterbilt) MDI and Service Gate certified" |
| Exact quoted wording | Karmak: *"Parts sales and demand data is sent to PACCAR. Orders are calculated and sent back to your system, saving you time and improving your inventory performance. Fusion supports all MDI order types, including stock order, PACCAR Parts Marketing Suggestion (MKT), and Auto Confirmed (COF) orders."* — [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar). PACCAR: *"PACCAR Parts Managed Dealer Inventory Program, or MDI, is one of the most advanced technologies in the supply chain. MDI allows PACCAR Parts to manage each dealer's inventory planning functions and provides visibility to retail transactions. Based on data analysis, parts order recommendations are developed for each dealer location and transmitted electronically to the dealer daily."* — [PACCAR Parts Technology page](https://www.paccarparts.com/technology/). Karmak release notes (technical/internal, but publicly hosted): *"Now when a finalized COF file comes in from PACCAR, it will automatically export a stock order from Fusion... PACCAR MDI COF has been added as a PO Source... VMI62010 Vendor Managed Inventory Order Status Report"* and *"This new scheduled job will execute the COF file without running the SOF file concurrently... Process COF has been added to the header of the VMI file produced in the 'CreateSendPaccarMDIDailyInventoryFile' in 'MgrPaccarMDI' class."* — [Karmak Fusion Release 3.59 Cumulative Release Notes, PDF](https://webhelp.karmak.com/ReleaseNotes/Fusion/3.59_cumulative.pdf) |
| **This is the key dealer→PACCAR feedback loop.** MDI is explicitly a two-way data exchange in which the dealer's Fusion system uploads parts sales/demand (i.e., retail sell-through and inventory-position data — PACCAR calls it "visibility to retail transactions") and PACCAR pushes back computed replenishment orders. Note: Karmak's public page does not use the term "Dealer Inventory File" or "DIF" by name — that specific label is **UNVERIFIED** against these sources; the confirmed named artifact for the outbound leg is the "VMI" (Vendor Managed Inventory) daily inventory file per the release notes, and PACCAR's own page describes the underlying data as "retail transactions" visibility rather than a named "DIF." | |

### 2.2 Online Parts Counter (OPC) — **DOCUMENTED** — PACCAR→dealer (order intake)

| Field | Detail |
|---|---|
| PACCAR-side system name | Online Parts Counter (OPC) — Karmak specifically calls it "PACCAR's Next Gen Online Parts Counter" |
| Direction | PACCAR (fleet customer ordering channel) → dealer (Fusion) |
| Business object | Parts orders placed by major fleet accounts (parts lookup, pricing/availability check, order) |
| Transport/mechanism | Not specified beyond "full integration"; orders are "created in Fusion without the need to rekey anything" and print to the warehouse for picking |
| Cadence | Real-time / on order placement |
| Karmak "certified" language | Not labeled "certified" on this page |
| Exact quoted wording | *"Fusion offers full integration with PACCAR's Next Gen Online Parts Counter. Major fleet accounts use Online Parts Counter to look up parts information, check pricing and availability, and place orders. Parts orders from OPC are created in Fusion without the need to rekey anything, and printed in your warehouse for picking."* — [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar) |
| Note per task instructions | **"PartsPRO" is explicitly confirmed NOT the correct name.** The correct PACCAR-side system, per Karmak's own page, is **Online Parts Counter (OPC)**. |

### 2.3 Electronic Parts Invoices — **DOCUMENTED** — PACCAR→dealer

| Field | Detail |
|---|---|
| PACCAR-side system name | PACCAR Parts Electronic Invoice(s) |
| Direction | PACCAR → dealer (Fusion) |
| Business object | Vendor invoices, matched against dealer purchase orders and receipts |
| Transport/mechanism | Built on Karmak's "Fusion eData Exchange EDI 810 Inbound Invoice" technology (EDI 810 = ANSI X12 EDI transaction set for invoices) |
| Cadence | Not stated (implied ongoing/as invoices are issued) |
| Karmak "certified" language | Not labeled "certified" |
| Exact quoted wording | Current product page: *"PACCAR Parts electronic invoices are imported directly into Fusion where they are compared to your purchase orders and receipts and can be automatically posted into Accounts Payable, freeing up your staff for other duties. You control if and when invoices are posted, within your specific percentage or dollar amount ranges."* — [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar). 2018 launch, trade press: *"Karmak announced Monday it has partnered with Paccar to bring dealers Electronic Parts Invoices within Karmak Fusion. The Paccar Parts Electronic Invoice feature is built on the Fusion eData Exchange EDI 810 Inbound Invoice technology, and gives clients the ability to process invoices from Paccar Parts, as well as other independent suppliers... available in Fusion Release 3.55."* — [Truck Parts & Service, "Karmak partners with Paccar to release parts invoice tool," March 2018](https://www.truckpartsandservice.com/economic-trends/indicators/article/14987629/karmak-partners-with-paccar-to-release-parts-invoice-tool) (note: full article body blocked by site robots.txt for direct fetch; quoted text captured via search index snippet from a trusted trade-press domain) |

### 2.4 ePacking Slip / ASN — **DOCUMENTED** — PACCAR→dealer

| Field | Detail |
|---|---|
| PACCAR-side system name | PACCAR Parts electronic packing slip (Karmak labels it "ePacking Slip (ASN)" — Advance Ship Notice) |
| Direction | PACCAR → dealer (Fusion) |
| Business object | Shipment/receiving data — allows receipt of parts shipments spanning multiple orders or split across shipments |
| Transport/mechanism | Electronic packing slip / ASN (exact wire format not stated) |
| Cadence | Per shipment |
| Karmak "certified" language | Not labeled "certified" |
| Exact quoted wording | *"Fusion leverages the PACCAR Parts electronic packing slip to allow you to quickly and easily receive parts into inventory, whether a shipment contains parts from multiple orders or orders are spread across shipments. You can receive shipments with a few clicks or update the system to process any exceptions."* — [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar) |

### 2.5 Financial Reporting (month-end financial statement upload) — **DOCUMENTED** — dealer→PACCAR (feedback loop)

| Field | Detail |
|---|---|
| PACCAR-side system name | Not given a proper-noun system name on this page; described generically as "PACCAR" financial statement upload/site. Internally, Karmak's own release notes reference an "OEM Financial - PACCAR" report/program (`GLM96520`) |
| Direction | **Dealer (Fusion) → PACCAR** — this is a feedback-loop item: dealer financial statements flow up to the OEM |
| Business object | Dealer month-end financial statements (income statement/balance sheet data); release notes further show PACCAR's financial statement template includes line items such as "Other New Class 8 Gross profit" (page 5, line 16) and "Other New Class 6 & 7 Gross profit" (page 5, line 18) |
| Transport/mechanism | Automated download/creation in Fusion, then upload/transfer to "the PACCAR site" |
| Cadence | Monthly (month-end) |
| Karmak "certified" language | Not labeled "certified" |
| Exact quoted wording | *"Automatically download your month end financial statements to PACCAR. After creation and maintenance of the statements, it takes only a few keystrokes to transfer the documents to the PACCAR site for upload."* — [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar). Release notes: *"GLM96520 OEM Financial - PACCAR — Allocations of z-expenses on PACCAR now calculates correctly and will show the correct gross profit for page 2 allocated expenses section. PACCAR's Financial page 5 line 16 'Other New Class 8 Gross profit' and page 5 line 18 'Other New Class 6 & 7 Gross profit' now reflects the corrected calculated value."* — [Karmak Fusion Release 3.59 Cumulative Release Notes, PDF](https://webhelp.karmak.com/ReleaseNotes/Fusion/3.59_cumulative.pdf) |

### 2.6 FOCUS (PACCAR Parts FOCUS CRM tool) — **DOCUMENTED** — dealer→PACCAR (feedback loop)

| Field | Detail |
|---|---|
| PACCAR-side system name | FOCUS — "PACCAR Parts FOCUS CRM tool" |
| Direction | **Dealer (Fusion) → PACCAR/FOCUS** — outbound feedback loop of customer/sales data |
| Business object | Customer and parts sales data |
| Transport/mechanism | Automated send (mechanism/cadence not further specified) |
| Cadence | Not stated ("automates sending") |
| Karmak "certified" language | Not labeled "certified" |
| Exact quoted wording | *"Fusion automates sending customer and parts sales data to the PACCAR Parts FOCUS CRM tool, where it provides insights into customer purchasing patterns so you can concentrate on increasing your sales."* — [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar) |

### 2.7 Kenworth TruckTech+ / Peterbilt SmartLINQ (Decisiv) — **DOCUMENTED** — bidirectional

| Field | Detail |
|---|---|
| PACCAR-side system name | Kenworth TruckTech+ and Peterbilt SmartLINQ, both built on the Decisiv service-relationship-management (SRM) platform, referred to on PACCAR's own support site as "DBS" integration (Dealer Business System) via "SERTI"/"Karmak" categories |
| Direction | **Bidirectional** — estimates, parts pricing/availability, new customers/assets flow Decisiv→Fusion; repair-order task/parts/charge changes and invoice/close-out data flow Fusion→Decisiv |
| Business object | Repair-order (case) data: estimates, parts pricing/availability queries, customer records, asset records, complaint/cause/correction text, invoice date/number, case status/close | 
| Transport/mechanism | System-to-system case/RO integration (API-level; PACCAR's own help portal documents specific "Integration Points" such as Customer Credit Check, Add Customer, Add Asset, Warranty Tag capture, Parts Availability/Pricing query, Superseded Part Number lookup, Core Fee support, Parts Salesman ID export, Engine Hours transfer, RO export/creation, Auto-Close on final invoice) |
| Cadence | Real time / on repair-order event ("can be updated as often as needed"; case "automatically updated and closed when the repair order is invoiced") |
| Karmak "certified" language | Not labeled "certified" by Karmak on the PACCAR page; a third-party aggregator (unverified) separately claims "certified bi-directional integrations for... PACCAR/Peterbilt/Kenworth" via "Unity Pro" |
| Exact quoted wording | Karmak: *"Estimates are transferred directly into Fusion repair orders and can be updated as often as needed. Parts pricing and availability is visible within TruckTech+ or SmartLINQ, and new customers and assets are easily added to Fusion, improving the experience for customers and your service writers. Changes to the open repair order tasks, parts, and miscellaneous charges are seamlessly sent back to TruckTech+ or SmartLINQ, keeping the case up to date so your customer always has an accurate view of the progress. The case is automatically updated and closed when the repair order is invoiced."* — [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar). PACCAR's own Decisiv support portal (PACCAR Solutions), listing granular integration points for "Karmak Fusion v. 3.55 and later," e.g.: *"This capability allows Decisiv to query the DBS for valid parts, the availability of a part at their location, as well as provide the customer specific parts pricing in the Decisiv estimate,"* and *"This capability will auto close the Decisiv case when the last invoice is processed against an RO that was created via a Decisiv case export."* — [Feature List for Karmak Fusion, PACCAR Solutions support portal](https://support.paccar.decisiv.net/hc/en-us/articles/360033879154-Feature-List-for-Karmak-Fusion); category index confirming Karmak has its own dedicated integration documentation set ("Add, Update, or Remove Parts or Operations from Karmak Fusion and Push into Decisiv Case," "Feature List for Karmak Fusion," "Setup for Karmak Fusion," "Enable Shop Part Pricing for Karmak Fusion," "Enable Parts Salesman for Karmak Fusion," "Enable Parts Source for Karmak Fusion" — "See all 12 articles") — [Help for DMS and DBS Integrations, PACCAR Solutions support portal](https://support.paccar.decisiv.net/hc/en-us/categories/360002149494-Help-for-DMS-and-DBS-Integrations). Release-notes evidence of ongoing maintenance: *"PACCAR SmartLINQ (Decisiv R/O) \| PACCAR TruckTech+ (Decisiv R/O) — When Fusion does not update the RepairOrderRemoteInformation table, it will not respond with an R/O Number, so Fusion will no longer assign the same R/O number to two different Decisiv Case estimates."* — [Karmak Fusion Release 3.59 Cumulative Release Notes, PDF](https://webhelp.karmak.com/ReleaseNotes/Fusion/3.59_cumulative.pdf) |

### 2.8 PACCAR Parts Fleet Services / Service Gate — **DOCUMENTED** — bidirectional (with dealer→PACCAR remittance/invoice leg)

| Field | Detail |
|---|---|
| PACCAR-side system name | PACCAR Parts Fleet Services, referred to by Karmak parenthetically as "Service Gate" |
| Direction | **Bidirectional** — dealer sends final invoices and PDF copies to Service Gate; Service Gate returns remittance and pre/post-authorization |
| Business object | Fleet/national-account payment-card transactions: preauthorization on estimates, authorization on completed work/parts purchases, final invoices, remittance, PDF invoice copies |
| Transport/mechanism | Secure electronic transmission ("securely transmitted") |
| Cadence | Transactional (per estimate/invoice) |
| Karmak "certified" language | Not labeled "certified" by Karmak on this page; the same unverified third-party aggregator claims PACCAR "MDI and Service Gate certified" |
| Exact quoted wording | *"Your fleet and national account customers can charge the cost of parts and service to their Fleet Services payment card. You're able to obtain preauthorization on estimates and or authorization on completed work or parts purchases. Final invoices are securely transmitted to Service Gate, and remittance is automatically retrieved for you. PDF copies of the invoices are provided to Service Gate for your customer's reference and review."* — [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar) |

### 2.9 Parts Orders (Stock/Emergency export) — **DOCUMENTED** — dealer→PACCAR

| Field | Detail |
|---|---|
| PACCAR-side system name | Not given a distinct proper-noun name beyond "PACCAR Parts" order upload; distinct from the MDI-managed order flow |
| Direction | Dealer (Fusion) → PACCAR Parts |
| Business object | Stock orders and Emergency orders |
| Transport/mechanism | Export/upload file |
| Cadence | Not stated |
| Karmak "certified" language | Not labeled "certified" |
| Exact quoted wording | *"Stock and Emergency orders can be exported from Fusion and uploaded to PACCAR Parts, eliminating the need to re enter orders."* — [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar) |

### 2.10 PRWS Warranty Claims — **DOCUMENTED** — dealer→PACCAR (feedback loop) with PACCAR→dealer campaign/recall data

| Field | Detail |
|---|---|
| PACCAR-side system name | PRWS ("PACCAR Warranty" claims system — exact expansion of the acronym is not spelled out on the Karmak page itself; Karmak refers to it simply as "PRWS Warranty Claims") |
| Direction | **Bidirectional**, dominant flow is dealer→PACCAR (claims submission = feedback loop); PACCAR→dealer for open campaigns/recalls pulled into the repair order |
| Business object | Warranty claims created/updated from Fusion repair-order data; open campaigns and recalls (optional import into RO); RO attachments added to the claim |
| Transport/mechanism | Not specified beyond "advanced integration" |
| Cadence | Per repair order / per claim |
| Karmak "certified" language | Not labeled "certified" on this page |
| Exact quoted wording | *"Warranty claims can be easily created and updated with data captured from the Fusion repair order. Open campaigns and recalls are optionally brought into the repair order, and attachments from the repair order can be added to the claim. Our advanced integration saves you time and gets you paid quickly for warranty repairs."* — [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar) |

### 2.11 Rental Performance System (RPS) — **DOCUMENTED** — PACCAR(PacLease)→dealer

| Field | Detail |
|---|---|
| PACCAR-side system name | Rental Performance System (RPS), a PacLease system |
| Direction | PacLease/RPS → dealer (Fusion) |
| Business object | Customers, units, and rental contracts |
| Transport/mechanism | Not specified |
| Cadence | Based on PacLease/RPS activity (event-driven) |
| Karmak "certified" language | Not labeled "certified" |
| Exact quoted wording | *"Our integration saves your rental managers time by creating and updating customers, units, and rental contracts in Fusion based on your activity in the PacLease RPS system."* — [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar) |

### 2.12 Truck Order Data (PACCAR B2B build-data feed) — **DOCUMENTED** — PACCAR→dealer

| Field | Detail |
|---|---|
| PACCAR-side system name | Referred to as "PACCAR's B2B infrastructure" (no more specific proper-noun system name given) |
| Direction | PACCAR → dealer (Fusion) |
| Business object | Truck build data and specifications; "key vehicle components, dates, and other information" |
| Transport/mechanism | B2B integration ("retrieve" — implies pull/API-style retrieval) |
| Cadence | Not stated |
| Karmak "certified" language | Not labeled "certified" |
| Exact quoted wording | *"Fusion's integration with PACCAR's B2B infrastructure makes it possible to retrieve truck build data and specifications and update the information in your Fusion system. Key vehicle components, dates, and other information are mapped to the fields you want to track with no double entry of data."* — [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar) |

### 2.13 Customer Loyalty Card — **DOCUMENTED** — bidirectional (lookup + redemption)

| Field | Detail |
|---|---|
| PACCAR-side system name | Not separately named beyond "PACCAR Customer Loyalty Card" / "PACCAR Price File Loyalty Card" |
| Direction | Bidirectional (discount lookup from PACCAR data; redemption recorded on dealer transactions across counter and OPC) |
| Business object | Loyalty-card discount eligibility and redemption, applied to front/back counter and OPC orders |
| Transport/mechanism | Price file / query form (Fusion "PACCAR Price File Loyalty Card form") |
| Cadence | Per transaction |
| Karmak "certified" language | Not labeled "certified" |
| Exact quoted wording | Current page: *"For your customers who are enrolled in the loyalty card program, discounts are automatically applied and redeemed, for front and back counter orders, as well as Online Parts Counter orders."* — [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar). Release notes bug-fix evidence of the underlying artifact: *"PACCAR Customer Loyalty Card — The query no longer pulls in as many results as before, the PACCAR Price File Loyalty Card form will now work as intended without getting an out of memory exception."* — [Karmak Fusion Release 3.59 Cumulative Release Notes, PDF](https://webhelp.karmak.com/ReleaseNotes/Fusion/3.59_cumulative.pdf) |

---

## 3. Interfaces named in secondary/aggregator sources only — **UNVERIFIED**

These appear in third-party comparison content, not confirmed by a Karmak or PACCAR primary-source quote fetched for this report. Flagged explicitly so they are not treated as confirmed:

- **"OEM scorecard" mechanism** — Karmak's own site includes an FAQ *headline* asking "How does Karmak perform on PACCAR's OEM integration scorecard?" and answers only in generic terms: *"PACCAR scorecard performance reflects how well a business system aligns with OEM requirements, data standards, and operational workflows. Strong scorecard results help dealers avoid integration gaps, reduce operational friction, and stay aligned as PACCAR programs and expectations change."* — [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar). This confirms a PACCAR OEM integration scorecard exists and that Karmak is evaluated against it, but Karmak does not disclose its own score or "certified" status in this text — **DOCUMENTED that the scorecard exists; UNVERIFIED what Karmak's certification status/score is.**
- A DMS-comparison/marketing aggregator site (not PACCAR or Karmak) states: *"The Unity Pro API platform carries certified bi-directional integrations for DTNA/Freightliner, PACCAR/Peterbilt/Kenworth..."* and separately *"PACCAR (Kenworth, Peterbilt) MDI and Service Gate certified."* — [Flyntlok, "Best dealer management systems"](https://www.flyntlok.com/insights/best-dealer-management-systems). This is a third-party, non-primary, competitor-comparison marketing page; treat the specific claim of formal PACCAR "certification" for MDI and Service Gate as **UNVERIFIED** until confirmed on a Karmak or PACCAR primary page.
- **"Dealer Inventory File" / "DIF"** as a named artifact — not found verbatim in any Karmak or PACCAR primary source reviewed. The confirmed named outbound file/mechanism is the **VMI (Vendor Managed Inventory) daily inventory file** created by `CreateSendPaccarMDIDailyInventoryFile`/`MgrPaccarMDI` per Karmak's own release notes (see §2.1). **"DIF" itself is UNVERIFIED as PACCAR/Karmak terminology** based on sources reviewed.

---

## 4. Feedback-loop summary: what Fusion sends UP to PACCAR

Consolidating the dealer→PACCAR (or dealer→PacLease) direction across all documented interfaces above — i.e., everything that constitutes upward reporting from the dealer DMS to the manufacturer:

| Interface | What flows dealer → PACCAR | Source |
|---|---|---|
| MDI | Parts sales and demand data (retail sell-through / inventory position) | [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar); [PACCAR Parts Technology](https://www.paccarparts.com/technology/) |
| Financial Reporting | Month-end dealer financial statements | [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar); [Release 3.59 notes](https://webhelp.karmak.com/ReleaseNotes/Fusion/3.59_cumulative.pdf) |
| FOCUS | Customer and parts sales data | [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar) |
| Parts Orders (Stock/Emergency) | Dealer-generated purchase orders | [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar) |
| PRWS Warranty Claims | Warranty claims (with repair-order data and attachments) | [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar) |
| Service Gate / Fleet Services | Final invoices and PDF invoice copies | [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar) |
| TruckTech+/SmartLINQ (Decisiv) | Repair-order task/parts/charge changes; invoice date/number; case-close signal | [karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar); [PACCAR Solutions Feature List for Karmak Fusion](https://support.paccar.decisiv.net/hc/en-us/articles/360033879154-Feature-List-for-Karmak-Fusion) |

No Karmak or PACCAR primary source names a standalone "sales/inventory file," "retail sell-through file," or "Dealer Inventory File (DIF)" as a discrete product outside of the MDI relationship described above — the retail sell-through/inventory visibility PACCAR receives is explicitly folded into the **MDI** program per PACCAR's own technology page language ("provides visibility to retail transactions").

---

## 5. Karmak partner/developer program, API documentation, VMRS, and Blaze

### 5.1 Karmak.IO developer portal / Unity & Unity Pro API platform — **DOCUMENTED**

Karmak operates a public developer portal and a documented, OAuth2-based REST/SOAP API platform:

> "Now, to make it even easier for partners (and clients) to create data integrations with Fusion, we have developed a pre-defined API framework called Unity... Unity is an API catalog for partners and developers to find, connect, and manage their API connections to Karmak Dealership Management Solutions... Unity also provides read-only access to Fusion – allowing both partners and customers to query data as the need arises."
— [Optimizing partner integrations, unity.karmak.io](https://unity.karmak.io/unity.html)

Authentication mechanics are documented in detail:

> "Before making any calls to Unity API's, you must first obtain a Bearer Token... Unity uses OAuth 2.0 compatible access control, closely resembling the standard 'client_credentials' flow (grant type)..."
— [Using Unity, unity.karmak.io](https://unity.karmak.io/Using-Unity.html)

Karmak's developer portal home page and formal Partner Alliance Program certification process are separately documented:

> "To make it even easier for partners (and clients) to create data integrations with Fusion, we have published a pre-defined easy-to-consume API Management... It's really easy to use Unity Pro to start consuming APIs."
— [Karmak.IO developer portal home](https://portal.karmak.io/)

> "This process is for 3rd Party Partners building integrations with Karmak APIs and is part of Karmak's Partner Alliance Program... Certification requires a signed NDA and an identified Karmak pilot customer... Sandbox access includes full API access at $99/month..."
— [Partner Integration Certification, portal.karmak.io](https://portal.karmak.io/certification)

The certification page lists a formal seven-step process (Discovery Call → Sandbox Access → Build and Test → Pilot Readiness Call → Pilot Phase [30–120 days] → Certification Demo and Approval → Post-Certification). No PACCAR-specific certification document was found on Karmak's own site; this program is described as OEM-agnostic (applies to all third-party/partner integrations generally, not published as PACCAR-specific).

Karmak's own company history page dates the API framework's origin:

> "2019 — Unity — Karmak announces Unity, a pre-defined API framework built to help clients leverage third-party software."
— [About, karmak.com](https://www.karmak.com/about)

### 5.2 VMRS licensing from TMC (2025) — **DOCUMENTED**

> "Karmak has taken a significant step in service intelligence standardization by licensing official VMRS (Vehicle Maintenance Reporting Standards) data from the Technology & Maintenance Council (TMC). This agreement marks the first step in Karmak's broader VMRS adoption strategy for the Fusion business system, aiming to bring more consistent, data-driven service intelligence to dealers, fleets, and OEMs. (Carlinville, IL – March 11, 2025)... Karmak will begin incorporating VMRS data into the Fusion ecosystem, with details on implementation to be announced soon... Our future goal is to further integrate VMRS into Fusion's Service and Parts modules, driving better decision-making and improved ROI for those we serve."
— [Karmak Licenses VMRS Data from TMC to Standardize Service Intelligence, karmak.com](https://www.karmak.com/karmak-licenses-vmrs-data-from-tmc-to-standardize-service-intelligence.html)

This press release does **not** mention PACCAR by name in connection with VMRS — it references "dealers, fleets, and OEMs" generically. Any specific PACCAR-VMRS linkage is **UNVERIFIED**.

### 5.3 Karmak Blaze (from DSI Solutions acquisition) — PACCAR coverage — **DOCUMENTED** (pre-acquisition) / largely **UNVERIFIED** (post-acquisition specifics)

Karmak acquired DSI Solutions, whose flagship product is Blaze, effective September 30, 2025 (announced October 14, 2025):

> "Karmak, Inc.... today announced the acquisition of long-time competitor DSI Solutions... By bringing Blaze alongside Karmak Fusion, Karmak now offers customers more flexibility and choice... Both Fusion and Blaze will continue to be sold and supported. Integration efforts will evolve gradually, focusing on collaboration, operational alignment, and the optimal use of each platform's strengths."
— [Karmak Acquires DSI Solutions, PR Newswire](https://www.prnewswire.com/news-releases/karmak-acquires-dsi-solutions-cementing-industry-leadership-and-expanding-dealer-management-offerings-302582870.html)

A third-party marketing/comparison source (unverified, not primary) characterizes the scale of the combined PACCAR footprint post-acquisition as: *"the acquisition gives Karmak over 50% of PACCAR's DMS market share"* (paraphrased from the same press release's substance per source extraction — treat this specific market-share figure as sourced to the PR Newswire release but not quoted verbatim in the release text captured). This should be **treated as UNVERIFIED at the exact-percentage level** pending direct confirmation from the original press-release text; it did not appear as a direct quotable sentence in the fetched content, only as an extracted summary.

Pre-acquisition, DSI's Blaze product had its own PACCAR/Peterbilt integration, documented in a DSI Solutions customer case study (Stahl Peterbilt, Edmonton, Alberta):

> "Vital information about Peterbilt from Paccar automatically flows into the DSI program and is immediately available for service, parts and other departments. No manual entry is required. Inventory management is automated. The system suggests what parts to order. The ordering process is completely integrated with Paccar."
— [DSI's Blaze Software Helps Build Efficiency in Edmonton, dsisolutions.biz](https://dsisolutions.biz/2017/06/20/dsis-blaze-software-helps-build-efficiency-in-edmonton/)

No Karmak-branded page found (as of this report) itemizing named PACCAR interfaces specifically for **Blaze** the way `karmak.com/integrations/paccar` does for **Fusion**. Post-acquisition Blaze-PACCAR interface names are therefore **UNVERIFIED** — the only confirmed Blaze-PACCAR linkage is the pre-acquisition DSI case-study language above, which does not name specific PACCAR systems (no MDI/OPC/PRWS names used) — it describes the integration only in generic terms ("information about Peterbilt from Paccar," "completely integrated with Paccar").

### 5.4 Karmak Xperience / user conference material — **PARTIAL / MOSTLY UNVERIFIED for PACCAR specifics**

Karmak's user conference is currently branded "Karmak Conference & Expo" (2026 edition: October 20–22, St. Louis, Union Station Hotel). The FAQ confirms OEM presence but not PACCAR-specific session content:

> "The agenda will include a mix of product updates, customer stories, industry insights, hands-on workshops, and practical sessions focused on real operational challenges."
— [Karmak Conference & Expo, karmak.com](https://www.karmak.com/conference-and-expo)

Trade press on the 2025 edition confirms an OEM-focused session existed, without PACCAR-specific detail:

> "The conference will feature sessions on the Karmak Mobile Service App, Fusion tips and tricks, and OEM/buying group roundtable discussions."
— [Karmak opens registration for 2025 conference and expo, Truck Parts & Service](https://www.truckpartsandservice.com/technology/business-operations/article/15739104/karmak-opens-registration-for-conference-and-expo) *(full article body blocked by site robots.txt; quoted text captured via trusted trade-press search snippet)*

A separate 2022 regional "Fusion Summit" event (hosted at JX Enterprises, a Peterbilt/Kenworth-affiliated dealer group) is documented as including Decisiv-focused content, though not PACCAR-branded interfaces by name:

> "Attendees also heard from the Decisiv team on maximizing integration efficiencies and participated in breakout sessions specific to operations in Parts, Service and Accounting."
— [Karmak holds Fusion summit at JX Enterprises, Truck Parts & Service](https://www.truckpartsandservice.com/technology/business-operations/article/15294012/karmak-holds-fusion-summit-at-jx-enterprises)

No primary Karmak Xperience/KUG session deck, agenda PDF, or recording naming specific PACCAR interfaces (MDI, OPC, PRWS, etc.) was located in this research pass — **UNVERIFIED** at the level of specific named interfaces being presented at these events.

---

## 6. PACCAR-side corroboration (independent of Karmak's marketing)

PACCAR's Decisiv-hosted dealer-support portal independently confirms the depth of the Karmak/Fusion-Decisiv (TruckTech+/SmartLINQ) integration, referring to Fusion by name as a supported "DBS" (Dealer Business System):

> "Help for DMS and DBS Integrations... Karmak — Add, Update, or Remove Parts or Operations from Karmak Fusion and Push into Decisiv Case; Feature List for Karmak Fusion; Setup for Karmak Fusion; Enable Shop Part Pricing for Karmak Fusion; Enable Parts Salesman for Karmak Fusion; Enable Parts Source for Karmak Fusion — See all 12 articles"
— [Help for DMS and DBS Integrations, PACCAR Solutions support portal](https://support.paccar.decisiv.net/hc/en-us/categories/360002149494-Help-for-DMS-and-DBS-Integrations)

PACCAR Parts' own technology page independently corroborates the existence and daily cadence of MDI as described by Karmak (see §2.1), giving cross-source (Karmak + PACCAR) confirmation for this specific interface:
[PACCAR Parts Technology & Innovation page](https://www.paccarparts.com/technology/)

Separately, a NHTSA-hosted PACCAR technical service bulletin documents a related but organizationally distinct integration — JPRO Professional (Noregon) diagnostic-tool check-in directly into "the PACCAR Solutions platform" (PSSM) — which is **not** a Karmak/Fusion interface and is noted here only to avoid confusing it with Fusion-specific interfaces:

> "Kenworth is pleased to announce that, working with our partners Decisiv® and Noregon®, we have developed an integration allowing Kenworth dealers to submit vehicle data to create or update a case directly to the PACCAR Solutions platform using JPRO® Professional."
— [PACCAR/Kenworth-Peterbilt Technical Information Bulletin, hosted by NHTSA](https://static.nhtsa.gov/odi/tsbs/2019/SB-10161170-9999.pdf)

---

## 7. Complete source list (all URLs cited above)

1. [PACCAR Karmak Integration — karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar) (primary, canonical destination of the /oem-integrations/paccar redirect)
2. [PACCAR Parts Technology & Innovation — paccarparts.com/technology](https://www.paccarparts.com/technology/)
3. [Karmak's Integrations and Partnerships — karmak.com/integrations](https://www.karmak.com/integrations)
4. [Karmak About page — karmak.com/about](https://www.karmak.com/about)
5. [Karmak Fusion Release 3.59 Cumulative Release Notes (PDF) — webhelp.karmak.com](https://webhelp.karmak.com/ReleaseNotes/Fusion/3.59_cumulative.pdf)
6. [Karmak Licenses VMRS Data from TMC — karmak.com](https://www.karmak.com/karmak-licenses-vmrs-data-from-tmc-to-standardize-service-intelligence.html)
7. [Karmak Acquires DSI Solutions — PR Newswire](https://www.prnewswire.com/news-releases/karmak-acquires-dsi-solutions-cementing-industry-leadership-and-expanding-dealer-management-offerings-302582870.html)
8. [DSI's Blaze Software Helps Build Efficiency in Edmonton — dsisolutions.biz](https://dsisolutions.biz/2017/06/20/dsis-blaze-software-helps-build-efficiency-in-edmonton/)
9. [Karmak.IO developer portal home — portal.karmak.io](https://portal.karmak.io/)
10. [Partner Integration Certification — portal.karmak.io/certification](https://portal.karmak.io/certification)
11. [Optimizing partner integrations (Unity) — unity.karmak.io/unity.html](https://unity.karmak.io/unity.html)
12. [Using Unity — unity.karmak.io/Using-Unity.html](https://unity.karmak.io/Using-Unity.html)
13. [Feature List for Karmak Fusion — PACCAR Solutions support portal](https://support.paccar.decisiv.net/hc/en-us/articles/360033879154-Feature-List-for-Karmak-Fusion)
14. [Help for DMS and DBS Integrations — PACCAR Solutions support portal](https://support.paccar.decisiv.net/hc/en-us/categories/360002149494-Help-for-DMS-and-DBS-Integrations)
15. [Karmak partners with Paccar to release parts invoice tool — Truck Parts & Service](https://www.truckpartsandservice.com/economic-trends/indicators/article/14987629/karmak-partners-with-paccar-to-release-parts-invoice-tool)
16. [Karmak opens registration for 2025 conference and expo — Truck Parts & Service](https://www.truckpartsandservice.com/technology/business-operations/article/15739104/karmak-opens-registration-for-conference-and-expo)
17. [Karmak holds Fusion summit at JX Enterprises — Truck Parts & Service](https://www.truckpartsandservice.com/technology/business-operations/article/15294012/karmak-holds-fusion-summit-at-jx-enterprises)
18. [Karmak Conference & Expo — karmak.com/conference-and-expo](https://www.karmak.com/conference-and-expo)
19. [PACCAR/Kenworth-Peterbilt Technical Service Bulletin re: JPRO/Decisiv (context only, not a Fusion interface) — hosted by NHTSA](https://static.nhtsa.gov/odi/tsbs/2019/SB-10161170-9999.pdf)
20. [Flyntlok — "Best dealer management systems" (secondary/aggregator, used only for flagged UNVERIFIED items)](https://www.flyntlok.com/insights/best-dealer-management-systems)

---

## 8. Key caveats for reverse-specification use

- Karmak's public marketing page is the only place a complete, current, named list of PACCAR interfaces is published; it is **not** a technical interface specification (no field-level layouts, transaction-set numbers, or full transport protocols beyond the EDI 810 reference for electronic invoices and internal class/file names visible only in release notes).
- The word "certified" is **not used by Karmak** on its own PACCAR integration page for any interface. Claims of PACCAR "certification" for specific interfaces (MDI, Service Gate) trace only to a third-party aggregator site and should be independently verified with PACCAR or Karmak directly before being treated as fact.
- "PartsPRO" is confirmed **not** a real PACCAR system name in any source reviewed; the correct, confirmed name for the fleet/major-account ordering portal is **Online Parts Counter (OPC)**.
- "Dealer Inventory File (DIF)" as a specific named artifact was **not found** in any primary source; the closest confirmed named mechanism is the **VMI (Vendor Managed Inventory) daily inventory file** tied to the MDI program.
- Blaze-specific PACCAR interface names (post-Karmak-acquisition) are largely unconfirmed in primary sources as of this report; only a generic pre-acquisition DSI case-study description was found.
