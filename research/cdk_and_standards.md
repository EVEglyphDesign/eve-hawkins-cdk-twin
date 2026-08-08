# CDK Drive Heavy Truck ↔ PACCAR, and the Underlying Data-Exchange Standards Layer

*Research compiled August 8, 2026. Every finding below is tagged **DOCUMENTED** (a direct primary-source quote is available) or **UNVERIFIED** (no public primary source located, or the source is silent). All URLs are live public pages fetched directly unless otherwise noted.*

---

## PART A — CDK Drive Heavy Truck ↔ PACCAR

### A.1 What CDK's own Heavy Truck OEM pages actually say

CDK Global runs at least three distinct "Heavy Truck" marketing/newsletter pages with materially different levels of detail, plus a newer dedicated microsite. They do not all agree with each other, and only one names PACCAR at all.

**[www2.cdkglobal.com/htonestop](https://www2.cdkglobal.com/htonestop)** — this is the source of the "80+" claim:

> "80+ Heavy Truck OEM-specific integrations are available for you." — [CDK Global, Heavy Truck](https://www2.cdkglobal.com/htonestop)

> "Having established close relationships with our OEMs, we combine their input with your feedback and what's going on in the broader industry to create tight integrations that help you work efficiently and effectively." — [CDK Global, Heavy Truck](https://www2.cdkglobal.com/htonestop)

**DOCUMENTED finding:** the "80+" figure exists exactly as a round, unitemized headline number. **PACCAR is not named anywhere on this page.** No specific OEM systems are listed. There is no enumeration, table, or breakdown by OEM (PACCAR vs. DTNA vs. Navistar vs. Volvo/Mack) anywhere on this page or linked from it. The "80+" claim is therefore **UNVERIFIED as an itemized list** — CDK publishes the number but not the underlying inventory of what the 80+ integrations are.

A CDK Connect webinar recording corroborates the same order of magnitude conversationally but adds informal color not found in any written CDK document:

> "...the OEM Integrations in the heavy truck space we have over 80 of those six of those were launched in the last uh four months while I've been here um another 15 are in the pipeline..." — [CDK Global Heavy Truck Team webinar, YouTube, Oct. 2022](https://www.youtube.com/watch?v=5BjvDxTD7hs)

This is **DOCUMENTED as spoken content** but is not a written CDK publication and gives no OEM-by-OEM breakdown either — it only splits the 80+ into "over 80 total," "six launched in the last four months," and "15 in the pipeline," with no OEM attribution.

### A.2 The one page that actually names PACCAR systems: the Heavy Truck newsletter

**[www2.cdkglobal.com/ht-oem](https://www2.cdkglobal.com/ht-oem)** (captured as CDK's "Heavy Truck Winter 23 Newsletter") is the only CDK page located that names specific PACCAR systems by name, with per-integration descriptions:

| Integration | Exact CDK language |
|---|---|
| **OPC (Online Parts Counter)** | "This CDK Drive Parts and PACCAR OPC e-commerce solution allows customers to purchase both PACCAR and non-PACCAR parts from the dealership, at pricing levels from the dealer's CDK system. It's required by PACCAR and available on Fortellis." |
| **PRWS (PACCAR's newest Registration and Warranty system)** | "Streamlines the filing of PACCAR warranty claims by creating drafts in the PACCAR PRWS (warranty system) with information from the RO and tracking via a dynamic status screen. PRWS is now available on Fortellis." |
| **Electronic Shipper** | "Coming soon, this integration reconciles OEM parts shipments easily through access to PACCAR's electronic shippers. This will be available through Sales." |
| **Decisiv Integration** | "This integration will allow users to send line level corrections thru the Decisiv interface and update the DMS appropriately. This will in turn update the line level story on a repair order. In addition the updated sync process will allow any story changes in the DMS to be reflected in Decisiv." |

Source: [CDK Global, Heavy Truck (ht-oem)](https://www2.cdkglobal.com/ht-oem) — **DOCUMENTED**.

**This directly answers the task's Decisiv question.** CDK's own newsletter language on "line-level corrections" is exactly as quoted above: *"This integration will allow users to send line level corrections thru the Decisiv interface and update the DMS appropriately. This will in turn update the line level story on a repair order. In addition the updated sync process will allow any story changes in the DMS to be reflected in Decisiv."* This is a two-way sync description (Decisiv→DMS corrections; DMS story changes→Decisiv), but CDK's page gives no field-level detail (which RO fields constitute a "story," what a "line level correction" actually updates in the ledger, or transaction cadence). **DOCUMENTED but shallow** relative to what Karmak publishes for the analogous Decisiv integration (see A.5 below).

### A.3 Only four named PACCAR items across all CDK Heavy Truck web pages found

Across every CDK Heavy Truck web property fetched — ht-oem, htonestop, [cdkglobalheavytruck.com/oem-integrations](https://www.cdkglobalheavytruck.com/oem-integrations), and [www2.cdkglobal.com/stability](https://www2.cdkglobal.com/stability) — the **complete inventory of named PACCAR systems is:**

1. **PACCAR OPC** (Online Parts Counter)
2. **PACCAR PRWS** (Registration and Warranty System)
3. **PACCAR's electronic shippers** (unnamed system, "coming soon" as of the newsletter capture)
4. **Decisiv** (third-party platform PACCAR uses for service; not a PACCAR-branded system per se)

The dedicated OEM/ISV integrations page at [cdkglobalheavytruck.com/oem-integrations](https://www.cdkglobalheavytruck.com/oem-integrations) has a "Paccar" section heading but **degrades to generic language with zero systems named**:

> "The PACCAR integration helps dealers keep key workflows connected across systems." / "By reducing duplicate entry and improving data consistency, teams can work more efficiently while staying aligned with OEM expectations." — [CDK Global Heavy Truck, OEM & ISV Integrations](https://www.cdkglobalheavytruck.com/oem-integrations) — **DOCUMENTED as vague**; it explicitly does **not** mention OPC, PRWS, electronic shipper, DIF/SOF, or financial statements.

The [www2.cdkglobal.com/stability](https://www2.cdkglobal.com/stability) page does not mention PACCAR by name at all — it speaks only generically of "major OEMs":

> "Our relationships with major OEMs help enable simple, secure OEM integrations." — [CDK Global, Heavy Truck (stability)](https://www2.cdkglobal.com/stability) — **DOCUMENTED as generic; PACCAR absent**.

**Not found anywhere in CDK's public Heavy Truck materials:** Managed Dealer Inventory (MDI), Dealer Inventory File (DIF), Suggested Order File (SOF), COF (Auto Confirmed) orders, PACCAR Parts FOCUS CRM tool, PACCAR Loyalty Card, PACCAR Parts Fleet Services/Service Gate, Rental Performance System (RPS), or **any mention of financial statement transmission to PACCAR**. This absence is treated below as the central A/B comparison point against Karmak. **UNVERIFIED / absent from CDK's public materials.**

### A.4 Fortellis: what CDK's developer platform documents about PACCAR

The Fortellis blog contains CDK's most specific and dated public commitment on PACCAR integration scope, published when Heavy Truck was first onboarded to the Fortellis exchange:

> "Heavy Truck has come to Fortellis — the secure, open-exchange marketplace used by the automotive industry to promote and inspire innovation and collaboration. With more standardized APIs, and app marketplace options, CDK Global is committed to expanding the Fortellis offerings that connect software developers, OEMs and dealers to create new digital tools for the Heavy Truck industry." — [Fortellis, "Meeting the Unique Needs of Heavy Truck Dealers," Jan. 7, 2022](https://fortellis.io/blog/meeting-unique-needs-heavy-truck-dealers)

> "We're hoping to launch at least five integrations this summer with two major OEMs — PACCAR and DTNA. Three will be offered on Fortellis, with even more coming in the second half of the year." — [same source](https://fortellis.io/blog/meeting-unique-needs-heavy-truck-dealers)

> "**CDK Integration With PACCAR PRWS (Warranty System)**: As repair orders with warranty lines are closed, the CDK integration with PACCAR PRWS uses information from the RO to create a draft claim on the PACCAR PRWS warranty system. Rather than rekeying information on the RO to create the draft claim, the user reviews the supplied information, edits as needed, and sends it to PACCAR. CDK Drive integration also provides a status screen, verifying the success of creating each draft claim in the PACCAR warranty system." — [same source](https://fortellis.io/blog/meeting-unique-needs-heavy-truck-dealers)

> "**CDK Integration With PACCAR OPC (Online Parts Counter)**: CDK Drive's integration with PACCAR OPC will allow customers to easily purchase both PACCAR and non-PACCAR parts (when available) from the dealership, at pricing levels from their CDK system." — [same source](https://fortellis.io/blog/meeting-unique-needs-heavy-truck-dealers)

**DOCUMENTED.** This 2022 post is the single most specific piece of CDK public writing found on PACCAR integration mechanics — but note it is: (a) four years old as of this research; (b) framed prospectively ("hoping to launch... this summer"), not as a completed-integration status report; and (c) does not specify how many of the "at least five" integrations were PACCAR-specific versus DTNA-specific.

**Fortellis API Directory / developer docs**, separately, confirm the existence of generic "CDK Drive" API products (not OEM-specific) that a PACCAR-facing app would sit on top of:

- **CDK Drive Get Repair Order v3** — service URL `https://api.fortellis.io/cdk/drive/servicerepairorder/v3` — [Fortellis API PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf) — **DOCUMENTED**.
- **CDKDrive Repair Orders v1** — a transactional API supporting "Query, Add, Update, or Delete Service Lines," request URL pattern `https://api.fortellis.io/cdkdrive/service/v1/repair-orders/` — [Fortellis developer guide](https://prod-fortellis-provider-api-reference-documents.s3-us-west-2.amazonaws.com/c7771500-1c95-4f8e-9241-eddc17cd55f6) — **DOCUMENTED**.
- Fortellis's own **API Directory** documentation confirms APIs are browsable "in alphabetical order" and filterable "by API Category," and a separate **Marketplace** (marketplace.fortellis.io) lists apps "discoverable by category, publisher or key word search." — [Fortellis Docs, API Directory](https://docs.fortellis.io/docs/general/api-directory-marketplace/api-directory/); [Fortellis App Listing Guide PDF](https://community.fortellis.io/sites/default/files/Fortellis_App.Listing.Guide_.pdf) — **DOCUMENTED** as a mechanism, but **no PACCAR-branded API product listing page** (i.e., an API literally named "PACCAR PRWS API" or "PACCAR OPC API" in the Directory) was found via search or fetch — the PRWS/OPC integrations are described in CDK marketing copy as "available on Fortellis," but the actual Fortellis Directory/Marketplace listing pages for those specific PACCAR-named products were not locatable in this research. **UNVERIFIED** whether PRWS/OPC are separately listed, discoverable Fortellis catalog entries versus bundled into CDK's general Drive API/app products.

### A.5 The Decisiv↔CDK Drive integration: what's documented, and its limits

Beyond the newsletter quote in A.2, no additional CDK-published detail on the Decisiv integration was found (no field mapping, no API spec, no cadence). By contrast, Karmak documents the equivalent Decisiv integration (with PACCAR's TruckTech+/SmartLINQ branding) in far more procedural detail:

> "**Kenworth TruckTech+ / Peterbilt SmartLINQ (Decisiv)**: Estimates are transferred directly into Fusion repair orders and can be updated as often as needed. Parts pricing and availability is visible within TruckTech+ or SmartLINQ, and new customers and assets are easily added to Fusion, improving the experience for customers and your service writers. Changes to the open repair order tasks, parts, and miscellaneous charges are seamlessly sent back to TruckTech+ or SmartLINQ, keeping the case up to date so your customer always has an accurate view of the progress. The case is automatically updated and closed when the repair order is invoiced." — [Karmak, PACCAR Integration page](https://www.karmak.com/integrations/paccar)

PACCAR's own Decisiv support site independently documents line-level operational mechanics for the Karmak Fusion↔Decisiv integration that have no CDK Drive equivalent published anywhere:

> "All operations and parts should be entered in Decisiv and then exported to Karmak Fusion to add them to the RO." / "To remove parts, users must remove the part in both Decisiv and Karmak Fusion." — [PACCAR/Decisiv support site, "Feature List for Karmak Fusion"](https://support.paccar.decisiv.net/hc/en-us/articles/360033879154-Feature-List-for-Karmak-Fusion)

**DOCUMENTED conclusion:** CDK's public Decisiv documentation is a single paragraph of marketing prose describing what the integration does in general terms ("line level corrections... update the DMS appropriately"). Karmak's public documentation for the functionally equivalent PACCAR-Decisiv integration is more granular (naming specific PACCAR brand touchpoints TruckTech+/SmartLINQ, describing bidirectional field flows for tasks/parts/miscellaneous charges, and specifying auto-close behavior on invoicing), and PACCAR's own support portal publishes step-level operational rules for the Karmak variant that have no published CDK counterpart.

### A.6 Where CDK's published PACCAR coverage is thinner than Karmak's

**Karmak's PACCAR integration page** ([karmak.com/integrations/paccar](https://www.karmak.com/integrations/paccar)) is a single, dense page naming **13 distinct PACCAR-specific integrations** with a description of the business mechanics of each:

> "Karmak's PACCAR OEM integrations support critical parts, service, inventory, financial, and warranty workflows through seamless data exchange between PACCAR systems and Fusion." — [Karmak](https://www.karmak.com/integrations/paccar)

The 13 named items, verbatim from Karmak: Customer Loyalty Card, Electronic Parts Invoices, ePacking Slip (ASN), **Financial Reporting**, FOCUS (PACCAR Parts CRM), Kenworth TruckTech+/Peterbilt SmartLINQ (Decisiv), **Managed Dealer Inventory (MDI)** — explicitly stating "Fusion supports all MDI order types, including stock order, PACCAR Parts Marketing Suggestion (MKT), and Auto Confirmed (COF) orders" — Online Parts Counter (OPC), PACCAR Parts Fleet Services (Service Gate), Parts Orders, PRWS Warranty Claims, Rental Performance System (RPS), and Truck Order Data. Source: [Karmak, PACCAR page](https://www.karmak.com/integrations/paccar) — **DOCUMENTED**.

Critically, Karmak explicitly claims automated financial statement transmission to PACCAR — the specific claim referenced in the task:

> "**Financial Reporting**: Automatically download your month end financial statements to PACCAR. After creation and maintenance of the statements, it takes only a few keystrokes to transfer the documents to the PACCAR site for upload." — [Karmak, PACCAR page](https://www.karmak.com/integrations/paccar) — **DOCUMENTED**.

Karmak also references a **PACCAR OEM integration scorecard**, implying PACCAR formally grades DMS vendors on integration quality — something with no public CDK counterpart found:

> "PACCAR scorecard performance reflects how well a business system aligns with OEM requirements, data standards, and operational workflows." — [Karmak, PACCAR page FAQ](https://www.karmak.com/integrations/paccar) — **DOCUMENTED** (Karmak's characterization; PACCAR's own scorecard methodology is not independently published and is therefore **UNVERIFIED** as to its criteria).

**Procede Software's PACCAR page** is comparatively closer to CDK's level of specificity than Karmak's — its October 2023 press release uses largely generic language ("PACCAR's proprietary systems," "critical processes and operations for key departments") — [Procede Software press release, Oct. 31, 2023](https://www.procedesoftware.com/paccar-integrations-three-new-releases/) — **DOCUMENTED as comparably thin**. However, Procede's product-update communications on LinkedIn/Facebook are considerably more granular than anything CDK publishes, down to named settings and file-naming behavior:

> "**PRWS Integration is a powerful Excede solution**... SIR Sheet Access: Pull Service Information Record (SIR) Sheets (PDF) directly from PACCAR... File Claim Feature: Resend claims and generate new Claim Numbers without re-entering data." — [Procede Software, LinkedIn product update, Dec. 2025](https://www.linkedin.com/posts/procede-software_procedesoftware-excededms-productupdate-activity-7402395748069548032-qWoj)

> "**PACCAR OPC Integration v1.2**... Improved Visibility for Failed Part Insertions: Two new BCS settings (OPC\\MissingPartCommentId and OPC\\MissingPartCommentNote)... OPC Order ID in File Names: The OPC Order ID is now included alongside the timestamp in parts order request and response file names, improving file traceability..." — [Procede Software, Facebook product update](https://www.facebook.com/procedesoftwareofficial/posts/congratulations-to-scott-coleson-of-our-customer-fourstar-freightliner-for-being/2998645510231135/)

**DOCUMENTED, direct comparison summary — where CDK is thinner:**

| Dimension | CDK Drive (public) | Karmak (public) | Procede (public) |
|---|---|---|---|
| Named PACCAR systems | 3–4 (OPC, PRWS, electronic shipper, Decisiv) | 13 named integrations | PRWS, OPC named with version numbers (v1.2) |
| Financial statement transmission to PACCAR | **Not mentioned anywhere** | Explicitly documented ("Automatically download... to PACCAR") | Not found in public materials |
| MDI / DIF / SOF / COF orders | **Not mentioned** | Explicitly named ("stock order, PACCAR Parts Marketing Suggestion (MKT), and Auto Confirmed (COF)") | Not found in public materials |
| PACCAR scorecard / OEM grading | Not mentioned | Referenced explicitly | Not found |
| Field/setting-level integration detail | None found (marketing prose only) | Moderate (workflow narrative) | High (named settings, file-naming conventions, version numbers) |
| Decisiv/TruckTech+/SmartLINQ detail | One paragraph, no OEM branding named | Names both OEM-branded portals (TruckTech+, SmartLINQ) explicitly | Not found |

**Conclusion for A.6 (DOCUMENTED):** CDK's public Heavy Truck web content is materially thinner than Karmak's on exactly the dimensions the task flags — financial statement upload, MDI/DIF/SOF/COF mechanics, and PACCAR's own dealer-facing "scorecard" — none of which appear anywhere in CDK's public Heavy Truck marketing, newsletter, or Fortellis materials found in this research. This may reflect either (a) CDK genuinely lacking these integrations, (b) CDK choosing not to publish this level of technical detail publicly (unlike Karmak, which uses a detailed integrations page as a sales tool), or (c) this material existing behind CDK's dealer/partner login walls. **This distinction cannot be resolved from public sources and is flagged as UNVERIFIED as to root cause**, though the *absence from CDK's public record* itself is DOCUMENTED.

### A.7 CDK Partner Program, rate card, and third-party data-access terms

CDK publishes an actual **Partner Program Pricing Guide** PDF with itemized monthly per-dealer fees for third-party data access:

> "PARTS E-COMMERCE — BASIC $90 / Parts Inventory, Pricing and Availability, Parts Quote/Invoice" ... "PARTS E-COMMERCE — PREMIUM $175 / Note: Additional $100 fee may apply if Parts e-commerce solution includes EPC integration." ... "PARTS INVENTORY PLANNING $46 / Ability to integrate Parts Inventory Planning" — [CDK Global, Partner Program Pricing Guide PDF](https://www.cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf) — **DOCUMENTED**.

> "BASE EXTRACT-ONLY FEE $28 / If a third party is contracting for data extract fees only, one Base Extract-only fee per application will be included and then an add-on fee for each data type extracted." / "ADD-ON FEES PER DATA TYPE $23" — [same source](https://www.cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf) — **DOCUMENTED**.

This rate card is generic to the whole CDK Partner Program (light/automotive), not specific to Heavy Truck or PACCAR — no Heavy-Truck-specific or PACCAR-specific line items were found.

CDK's separate **API Licensing Terms** page is a full legal contract template, not a Heavy Truck-specific document, but establishes the general legal posture governing any PACCAR-related Fortellis integration:

> "CDK... grants to Developer a limited, revocable, non-exclusive, non-sublicensable, non-transferable, non-assignable license... to access and use the API(s) and Data solely for the purposes of providing the applicable Developer App(s)..." — [CDK Global, API Licensing Terms](https://www.cdkglobal.com/api-licensing-terms) — **DOCUMENTED**.

> "Developer shall not... sell, resell, license, sublicense, distribute, make available, rent or lease or otherwise commercially exploit to any Third Party the CDK Interface Property..." — [same source](https://www.cdkglobal.com/api-licensing-terms) — **DOCUMENTED**.

> "Developer shall complete Certification, at its own cost, prior to consumption of any API." / recertification "shall be limited to once per calendar year for each Developer App, except that Fortellis may also make such requests any time integration is added..." — [same source](https://www.cdkglobal.com/api-licensing-terms) — **DOCUMENTED**.

CDK's 2020 **Customer Rewards Program** announcement confirms that CDK has, at the policy level, moved to **waive most third-party data access fees** for participating dealers (a change relevant to any PACCAR-facing plug-in vendor's cost model), though "CDK is not altering its data access offerings or support levels":

> "...a new program and pricing structure for CDK solutions that better aligns pricing to the value of CDK solutions and includes the elimination of most third-party data access fees through the CDK Partner Program for eligible customers." — [BusinessWire, CDK Global press release, Feb. 15, 2020](https://www.businesswire.com/news/home/20200215005009/en/CDK-Global-Introduces-New-Pricing-Structure-With-its-Customer-Rewards-Program) — **DOCUMENTED**.

No Heavy-Truck-specific or PACCAR-specific rate card variant was found; the general Partner Program rate card and the 2020 rewards-program fee waiver appear to be the operative public financial terms. **UNVERIFIED** whether Heavy Truck/PACCAR integrations carry different (e.g., higher, given OEM-mandated status of OPC) pricing than the generic light-vehicle rate card shown.

### A.8 CDK press releases on heavy-truck OEM integration

The clearest press-release-level evidence of CDK's heavy-truck OEM strategy is the annual **CDK Truck Connect** conference announcement, which explicitly names PACCAR as a session partner alongside other Heavy Truck OEMs:

> "AUSTIN, Texas – March 25, 2025 – CDK, the leading truck and automotive retail software provider, will host its third annual heavy truck industry conference, CDK TRUCK CONNECT... OEM Sessions with DTNA, Mack Volvo, International and PACCAR / Key Accounting Updates and Insights with Forvis Mazars, including up to 11 Hours of CPE Credits" — [CDK Global press release, March 25, 2025](https://www.cdkglobal.com/media-center/cdk-hosts-3rd-annual-truck-connect-conference-april-8-10) — **DOCUMENTED**.

Note the explicit accounting-focused session ("Key Accounting Updates and Insights with Forvis Mazars") appearing on the same agenda as the PACCAR OEM session — this is circumstantial corroboration that dealer accounting/financial-statement workflows are an active industry topic at the CDK-hosted PACCAR-adjacent conference, but the press release does **not** state that CDK Drive itself transmits financial statements to PACCAR. **UNVERIFIED** beyond the conference-agenda juxtaposition.

A separate 2025–2026 CDK CONNECT presentation video describes a newer, unnamed OEM accounting-workflow integration in two phases, without naming PACCAR specifically:

> "One example is a recent two phase integration that we had with our OEM partner that's making accounting workflows even smoother... For phase one, parts receding and reconciliation got a major upgrade. Dealers can now import electronic packing slips directly into Drive DMS... Phase two automatically posts electronic invoices straight into drive accounting... we're working to bring this integration to all major OEMs." — [CDK CONNECT 2025 video, YouTube](https://www.youtube.com/watch?v=OyQmaCKa4oU) — **DOCUMENTED as spoken content, OEM unnamed**; likely refers to the "Electronic Shipper" item named on the ht-oem newsletter page for PACCAR specifically, but CDK's own spoken description in this video deliberately withholds the OEM's name ("our OEM partner") and frames PACCAR-wide rollout as future work ("working to bring this integration to all major OEMs"). No CDK press release using the terms "PACCAR" and "financial statement" together was located. **UNVERIFIED / not found**: any CDK press release specifically confirming automated financial-statement upload to PACCAR analogous to Karmak's claim.

---

## PART B — The Standards Layer

### B.1 STAR (Standards for Technology in Automotive Retail) — relevant BODs

STAR's XML BOD catalog is organized by domain area. STAR states its overall scope directly:

> "STAR has worked with its membership to develop over 200 XML message formats covering over 35 business areas from customer relationship management to fixed and variable operations. These specifications have been designed to leverage the globally-recognized UN/CEFACT Core Component Technical Specification (CCTS) and the Open Application Group Integration Specification (OAGIS) Business Object Document (BOD) Methodology." — [STAR, "STAR XML BODs"](https://www.starstandard.org/index.php/star-xml-bods/) — **DOCUMENTED**.

The specific BODs the task asked about, with STAR's own scope-description text:

| BOD (task's requested item) | STAR's exact name | Exact scope text | Status |
|---|---|---|---|
| Parts Order | **Parts Order** | Listed in the STAR6 6.2.4 repository table; full scope text not separately captured in this fetch (BOD exists and is titled exactly "Parts Order") | DOCUMENTED (existence); scope text UNVERIFIED at full length |
| Parts Inventory | **Parts Inventory** | STAR's public catalog page's description field for "Parts Inventory" is corrupted/mismatched in the live HTML (it duplicates the Credit Application description verbatim: "The scope of this BOD is to define the Credit Application process for individual consumers apply for vehicle financing through their Dealer.") — this is very likely a publishing/table-rendering error on STAR's own site, not the real scope of Parts Inventory | DOCUMENTED (BOD exists and is titled "Parts Inventory"); **the description text visible on STAR's own page is evidently erroneous** — flagged, not resolved, since no separate authoritative Parts Inventory scope statement was independently located |
| Parts Sales / PartsSalesActivity | **Not found under this name** | No "Parts Sales" or "PartsSalesActivity" BOD name appears in the STAR XML BOD catalog page fetched | **UNVERIFIED / likely does not exist as a named BOD** — parts sales activity may be captured via Parts Invoice or Parts Inventory BODs instead, but this could not be confirmed |
| Repair Order | **Repair Order** | "The scope of this BOD is to define the Repair Order process for individual consumers who service their automobiles through their OEM's authorized Dealers. The focus is on Dealer and OEM interactions, not third party repair organizations." | DOCUMENTED — [STAR XML BODs](https://www.starstandard.org/index.php/star-xml-bods/) |
| Vehicle Sales / Retail Delivery Report | **Retail Delivery Reporting** | "The scope of this BOD is to report the "sale" of a vehicle at the dealership. Retail Delivery Reporting is the task of sending the Retail Delivery Reporting information electronically between Dealer and OEM systems." | DOCUMENTED — [STAR XML BODs](https://www.starstandard.org/index.php/star-xml-bods/) |
| Warranty Claim | **Not a standalone named BOD** — appears only inside "Service Processing Advisory & Receipt Acknowledgment" | "The scope of the Service Processing Advisory BOD is to send an advisory to a Dealer from an OEM on the status of a Warranty Claim submitted to the OEM by the Dealer... The scope of the Service Advisory Receipt Acknowledgment BOD is to send a confirmation to a Dealer from an OEM acknowledging receipt of request for payment for a Warranty Claim." | DOCUMENTED — [STAR XML BODs](https://www.starstandard.org/index.php/star-xml-bods/). Separately, a dedicated **WarrantyPayment** specification (v1.6.1) exists: "This specification will be in effect on 7/4/2007... file format must conform to the 'STAR General File Format Requirements'." — [STAR Warranty Payment spec PDF](https://qa.starstandard.org/images/SIGDTS/STARWarrantyPayments.pdf) — DOCUMENTED. A **WarrantyClaimReconciliation** schema element also exists within the Components.xsd of STAR5: "Warranty Claim information associated with a Repair Order." — [Liquid Technologies STAR schema docs](https://schemas.liquid-technologies.com/LibraryDocs/STAR/5.3.4/warrantyclaimreconciliation.html) — DOCUMENTED |
| Financial Statement | **Financial Statement** (Dealer domain) | "The scope of this BOD is to transmit dealer Financial Statement information. This may include Balance Sheet, Profit and Loss, and any other Financial Statement related information." | **DOCUMENTED** — [STAR XML BODs](https://www.starstandard.org/index.php/star-xml-bods/). A companion "Financial Metrics" BOD also exists ("FinancialMetrics is used to transmit dealer Financial Metrics information") but its sequence diagram is marked "Coming Soon" on STAR's own page, implying it is less mature/complete than Financial Statement. |

So: **a STAR "Financial Statement" BOD does formally exist** as a named XML Business Object Document, explicitly scoped to Balance Sheet and Profit & Loss transmission between dealer and OEM systems. This is a materially important finding for Part B.2 below.

### B.2 Does a standard DEALER FINANCIAL STATEMENT upload format to OEMs exist?

This is a three-layer answer:

**(1) STAR does publish a Financial Statement BOD** (see table above) — **DOCUMENTED** as existing, scoped to "Balance Sheet, Profit and Loss, and any other Financial Statement related information." Its practical adoption/usage rate by heavy-truck OEMs (PACCAR, DTNA, etc.) specifically was **not** found in any source in this research — **UNVERIFIED whether PACCAR or any heavy-truck OEM actually consumes the STAR Financial Statement BOD** as opposed to a proprietary upload mechanism.

**(2) NADA does not publish a single universal "standard financial statement format."** What exists instead is a **NADA "20 Group"** benchmarking/peer-comparison program and associated definitions guide:

> "FORMULA DEFINITION... Asset Utilization: Annualized total dealership sales ÷ total assets less land and buildings... Current Ratio (current assets to current liabilities): Total current assets + LIFO (if included in current assets) ÷ total current liabilities." — [NADA, 2026 Formulas, Definitions, Guides PDF](https://slideguide.nada.org/NADASlideGuide.pdf) — **DOCUMENTED** as a set of standardized *ratio definitions and benchmarking formulas*, not a file-transfer format or upload schema. **This is a data-dictionary of accounting ratios, not a transmission standard.**

**(3) A "composite" financial statement upload mechanism does exist, but it is vendor/consultant-specific, not an industry standard.** NCM Associates (a dealer 20-group consulting firm) publishes an explicit DMS-to-NCM upload workflow:

> "Step 1 – Access the Accounting Module... Step 3 – Processing: When your dealership has completed its month end processing and is ready to transmit to NCM20... Step 4 – NCM20 Upload: Perform Option 3: Send Financial Statement Data to NCM20 Group. A file will be created and transferred to the NCM20 folder..." — [NCM Associates, Financial Statement Submission Guide PDF](https://portal.ncmassociates.com/content/help/docs/FinancialStatementSubmissionGuide.pdf) — **DOCUMENTED**, but this is NCM's proprietary composite/benchmarking format (a private 20-group consultancy's format), not a NADA-issued or STAR-issued universal standard. A parallel NIADA (independent dealers) financial-statement compile/download workflow exists similarly: "Generate the download file, and download the file using the NIADA DISC application." — [Autosoft, NIADA Financial Statement guide PDF](https://download.autosoft-asi.com/instructions/NIA/NIADAFS.pdf) — **DOCUMENTED**, same caveat (proprietary composite process, not a universal cross-OEM standard).

**Conclusion for B.2:** There is **no single, universally adopted "dealer financial statement upload format to OEMs."** What exists is: (a) a STAR XML "Financial Statement" BOD that is technically capable of serving this purpose but whose actual OEM-side adoption is unverified; (b) NADA's standardized *ratio/formula definitions* (a semantic standard for what the numbers mean, not a file standard for transmitting them); and (c) proprietary composite/20-group upload mechanisms run by NCM and NIADA that are specific to those consultancies' benchmarking programs, not OEM-facing. **Karmak's claim that "financial statements are automatically downloaded to PACCAR" therefore very likely describes a PACCAR-proprietary or Karmak-proprietary file/portal transfer mechanism, not participation in any named public industry standard** — this is the most important gap the task asked to be flagged honestly, and it is confirmed: **no public standard for OEM-bound dealer financial statement upload was found**, despite a STAR BOD nominally covering the domain.

### B.3 STAR6 XML v6.2.4 release and the January 2026 Automotive Retail Domain Model

**STAR6 6.2.4** is a real, dated, currently-published release:

> "STAR6 is the next generation of the STAR XML BOD Repository. STAR has refactored the STAR5 XML BODs in the Parts, Credit, and Vehicle Domain based on best practices established by the STAR Members... STAR6 solves many of these issues by removing deprecated and duplicate attributes as well as harmonizing design patterns and components used across these BODs." — [STAR, STAR6 6.2.4 XML Schema Repository Page](https://www.starstandard.org/index.php/star6-6-2-4-xml-schema-repository-page/) — **DOCUMENTED**.

> "STAR Version 6.2.4 - Based on OAGI's 10.5 and UNEFACT Core Component" ... Repository table: "STAR6 Schema Repository | 6.2.4 | 2024-07-04" — [same source](https://www.starstandard.org/index.php/star6-6-2-4-xml-schema-repository-page/) — **DOCUMENTED**. The effective date is **July 4, 2024**, not a 2026 date — the task's phrasing ("the STAR6 XML v6.2.4 release") is confirmed to refer to this July 2024 release, which remains STAR's current published repository as of this research. STAR6 is licensed under the **Eclipse Public License 1.0**: "All STAR schema repositories are available under the terms of the Eclipse Public License 1.0." — [same source](https://www.starstandard.org/index.php/star6-6-2-4-xml-schema-repository-page/) — **DOCUMENTED**.

**The January 2026 Automotive Retail Domain Model** is a separate, more recent, and more significant release — STAR's press release is unambiguous and detailed:

> "MCLEAN, Va., January 27, 2026 — The Standards for Technology in Automotive Retail (STAR) today announced the publication of its groundbreaking Automotive Retail Domain Model; a comprehensive and unified data architecture designed to both modernize and standardize data exchange across the automotive retail industry." — [STAR press release, Jan. 27, 2026](https://www.starstandard.org/index.php/2026/01/27/star-unveils-industry-defining-retail-automotive-domain-model-to-advance-data-interoperability-and-ai-transformation-across-the-entire-ecosystem/) — **DOCUMENTED**.

> "The project introduces multiple core domain schemas including Parts, Accounts Payable, Accounting, Payroll, Human Resources, representing the industry's first coordinated effort to capture and standardize the operational data structures that power both dealership and OEM systems... The following domains have been finalized: Parts / Accounts Payable (AP) / Accounting / Payroll / Human Resources (HR)." — [same source](https://www.starstandard.org/index.php/2026/01/27/star-unveils-industry-defining-retail-automotive-domain-model-to-advance-data-interoperability-and-ai-transformation-across-the-entire-ecosystem/) — **DOCUMENTED**. **This confirms the task's premise directly: an "Accounting" domain is explicitly one of the five finalized Version 1.0 domains**, alongside a separate "Accounts Payable" domain.

> "In addition to the new schemas, STAR's service standard has transitioned from XML to JSON and is included in the domain model, providing a complete representation of automotive retail." — [same source] — **DOCUMENTED**. This signals a strategic shift away from the STAR6 XML format described above toward JSON/OpenAPI for new domain-model work, even though STAR6 XML 6.2.4 remains the live legacy repository.

> "The STAR Domain Model is accessible to all automotive industry organizations, regardless of membership status... However, only STAR's member organizations are allowed to create pieces of the existing domain model or participate in future updates." — [same source] — **DOCUMENTED**: read access is open, contribution/write access is members-only.

**No mention of a medium/heavy-duty-truck-specific carve-out** appears in the January 2026 Domain Model press release — the Accounting/AP/Payroll/HR/Parts domains are described industry-wide, not truck-segment-specific. **UNVERIFIED** whether or how the new Accounting domain differentiates light-vehicle dealer accounting from heavy-truck dealer accounting (e.g., PACCAR-specific chart-of-accounts mapping).

### B.4 STAR's medium/heavy-duty truck segment coverage

STAR's own XML BOD catalog page explicitly lists medium/heavy-duty trucks as one of its covered industry segments, alongside several others:

> Cross-industry coverage listed on STAR's site: "Marine," "Medium & Heavy-duty Trucks," "Powersports," "Construction Equipment," plus geographic coverage "Asia-Pacific," "Canada," "Central America," "South America," "Europe." — [STAR, XML BODs page](https://www.starstandard.org/index.php/star-xml-bods/) — **DOCUMENTED**.

This confirms STAR does formally scope "Medium & Heavy-duty Trucks" as a covered segment of its standard-setting activity. However, **no separate truck-specific BOD variant, truck-specific schema extension, or truck-segment implementation guide was located** in this research — the same general-purpose BODs (Parts Order, Repair Order, Warranty-related BODs, Financial Statement, etc.) appear to be the segment's coverage, rather than truck-specific BODs analogous to, say, a PACCAR-specific PRWS schema. **UNVERIFIED / not found:** any document showing PACCAR, DTNA, Navistar, or Volvo/Mack as active STAR members contributing truck-segment requirements, or any truck-specific STAR working group output distinct from the general automotive BOD catalog.

### B.5 The Dealer Inventory File (DIF) / Suggested Order File (SOF) — PACCAR Parts MDI mechanics

The TU Eindhoven master's thesis by Jessica Verhoijsen provides by far the most detailed, primary-source-quality description of the DIF/SOF mechanism found anywhere in this research. **Important scoping note:** the thesis studies the **MDI department in Eindhoven, Netherlands, managing DAF dealers** (DAF being PACCAR's European truck brand) — it is the PACCAR Parts MDI *methodology*, documented via its European (DAF) implementation, not the North American PACCAR/Kenworth/Peterbilt dealer network specifically. The mechanics described are presented as the general MDI department process.

**Core mechanism, exact quotes:**

> "Every day the dealer collects information about, for example, the daily sales per part and the inventory levels." — [TU Eindhoven, Verhoijsen thesis](https://pure.tue.nl/ws/portalfiles/portal/163151681/Master_Thesis_Jessica_Verhoijsen.pdf)

> "This information is stored in the Dealer Management System (DMS) that automatically generates a Dealer Inventory File (DIF) containing the daily information of the dealer." — [same source]

> "This DIF is send every night to the MDI department and the information in this DIF is used to determine whether a part needs to be ordered." — [same source]

> "Subsequently, a Suggested Order File (SOF) is created and send to the dealer." — [same source]

> "The dealer can accept or manually override the suggestion whereafter an order is placed at PACCAR parts." — [same source]

**Cadence — DOCUMENTED as strictly daily on both legs:** DIF transmission is "every night"; SOF generation and transmission is "once a day"; the review period in the underlying inventory policy is explicitly stated as "one day since the DIF is received once a day and an order is suggested once a day by creating a SOF." — [same source]

**Fields identified — DOCUMENTED but limited:** the thesis explicitly names only "the daily sales per part" and "the inventory levels" as DIF contents. It does **not** provide an exhaustive field-level layout, file format, encoding, or transmission protocol — the thesis itself is a business/operations-research document, not a technical interface specification, so this level of detail (file schema, delimiters, transport mechanism) is simply **UNVERIFIED / not published** in this or any other source found.

**Order-quantity mechanics (DOCUMENTED, unusually granular for a public source):** the MDI department uses an "(R,s,nQ)" inventory policy — periodic review (R = 1 day), reorder point (s), and order quantity as an integer multiple of a Standard Packaging Quantity (nQ). Class B parts: quantity is "the amount of units the inventory position falls below the reorder level" summed with "the maximum of the Economic Order Quantity (EOQ) and the MOQ [Minimum Order Quantity]," rounded up to the nearest SPQ multiple. Class A (fast-moving) parts use a forecast-driven variant based on the "Lewandowski algorithm," described as "based on Holt Winter's forecasting method, which applies triple exponential smoothing to the data," with a four-week (28-day) forecast bucket. — [same source] — **DOCUMENTED**.

**MDI order types corroborated independently by Karmak:** Karmak's own PACCAR page corroborates and names the order types the DIF/SOF cycle feeds into, terminology absent from the thesis:

> "Fusion supports all MDI order types, including stock order, PACCAR Parts Marketing Suggestion (MKT), and Auto Confirmed (COF) orders." — [Karmak, PACCAR page](https://www.karmak.com/integrations/paccar) — **DOCUMENTED**. Karmak's release notes independently confirm the COF (Auto Confirmed) file mechanic operationally: "Now when a finalized COF file comes in from PACCAR, it will automatically export a stock order from Fusion and place a file export timestamp on the Parts Purchase Order created by the COF process. PACCAR MDI COF has been added as a PO Source..." — [Karmak Fusion 3.59 cumulative release notes PDF](https://webhelp.karmak.com/ReleaseNotes/Fusion/3.59_cumulative.pdf) — **DOCUMENTED**. Neither the thesis nor Karmak's materials use the terms "DIF" and "COF" together in one document — the DIF/SOF terminology (thesis) and the stock/MKT/COF order-type terminology (Karmak) appear to describe the same MDI pipeline from two different vantage points (analytical/European vs. dealer-DMS/North American), and this research could not locate a single source unifying both vocabularies. **Flagged as a minor terminology-reconciliation gap, not a contradiction.**

**Scale (DOCUMENTED):** "Currently, the MDI department in Eindhoven manages the inventory of 530 DAF dealers." — [same source].

**No CDK-specific DIF/SOF integration was found anywhere in CDK's public materials** (see A.6 above) — CDK Drive's Heavy Truck pages never use the terms DIF, SOF, MDI, COF, or MKT order. This is a direct, confirmed gap in CDK's public documentation relative to both the underlying PACCAR mechanism (per the thesis) and Karmak's explicit support claims.

### B.6 VMRS (TMC) coding as the shared service vocabulary

VMRS (Vehicle Maintenance Reporting Standards) is maintained by the American Trucking Associations' Technology & Maintenance Council (TMC), and is unambiguously the shared cross-OEM/cross-DMS/cross-fleet vocabulary layer underneath repair-order and parts-classification data exchange in trucking:

> "Developed in 1970, the Vehicle Maintenance Reporting Standards (VMRS) provides a single, concise coding convention to manage fleets' assets and analyze maintenance operation costs. VMRS provides a vital communication link between maintenance personnel, computers, and management. It establishes a 'universal' language for fleets, original equipment manufacturers' (OEMs), industry suppliers, computers, and the people whose responsibility it is to specify, purchase, operate, and maintain equipment." — [TMC, VMRS Overview](https://tmc.trucking.org/VMRS-Overview) — **DOCUMENTED**.

> "VMRS is a collection of 84 Code Keys (only 58 of which are currently active) used to describe commercial assets and their related service and repair activities." — [Aspire/VMRS white paper PDF](https://dev-aspire.imgix.net/files/base/cygnus/vspc/document/2025/08/68927fc64f44ac85a2b60911-2017_02_vmrs_nextlevel_whitepaper_interactive.pdf) — **DOCUMENTED**.

> "VMRS codes are made up of nine digits, grouped in threes (###-###-###)... System level: This first three-digit segment identifies the vehicle's main system... Assembly level... Component level: The last three-digit segment specifies the exact part or component..." — [Geotab, VMRS glossary](https://www.geotab.com/glossary/vmrs/) — **DOCUMENTED**.

> "Part Description Codes—ATA's VMRS contains more than 34,000 universal descriptor codes to identify individual parts found on a piece of equipment. These codes do not replace the manufacturer's part number, but rather provide your fleet one standard item number to describe the same part regardless of the manufacturer." — [TMC, VMRS flyer PDF](https://tmc.trucking.org/sites/default/files/VMRS_flyer_2021_web.pdf) — **DOCUMENTED**.

VMRS's relevance to the STAR/CDK/PACCAR data layer is corroborated by an independent enterprise integration reference showing VMRS deployed *inside* STAR-XML-based warranty transactions:

> "This API follows SOAP 1.1 conventions and uses Standards for Technology in Automotive Retail (STAR) XML schemas for interoperability across automotive service systems... STAR schema version 5.13.4." — [ServiceNow, Warranty Claims SOAP API docs](https://www.servicenow.com/docs/r/manufacturing/warranty-claims-SOAP-API.html) — **DOCUMENTED** as an example of STAR-XML-plus-warranty-claim integration in production enterprise software (illustrative of the pattern; not itself a PACCAR or CDK system).

**Conclusion for B.6:** VMRS is **DOCUMENTED** as the standard part/component/labor/failure-cause vocabulary used across the heavy-truck service ecosystem — it functions as the shared "nouns and verbs" that populate the value/code fields inside STAR BODs like Repair Order and Warranty Claim/Warranty Payment, rather than as a competing transport-format standard. No evidence was found that CDK Drive, Karmak Fusion, or Procede Excede diverge from VMRS as the base part/labor coding system, though **none of the three vendors' public marketing pages explicitly confirm "we use VMRS codes"** — this reliance is treated industry-wide as assumed/background rather than a marketed feature, so vendor-level VMRS conformance claims are **UNVERIFIED** at the individual-vendor level even though VMRS's role as the standard is itself well-documented.

### B.7 PACCAR's developer API catalog (developers.paccar.cloud) and licensing posture

**Direct access to `developers.paccar.cloud` is blocked by the site's own robots.txt** (`disallow_by_robots`), so its live API catalog contents (specific API product names/endpoints) could not be directly enumerated in this research. **UNVERIFIED** as to exact catalog listing.

However, PACCAR's own **API License Agreement**, hosted on a PACCAR digital-services domain, explicitly references and defines the developer portal and establishes PACCAR's licensing posture in detail:

> "This API License Agreement (this "Agreement") is a binding contract between you ("you" or "your") and PACCAR Inc ("PACCAR," "we," or "us"). This Agreement governs your access to and use of the Connected Truck APIs." — [PACCAR, Digital Services Terms, last modified March 6, 2025](https://staging-paccar.anthology-digital.com/digital-services-terms/) — **DOCUMENTED**.

> "'API' means the Connected Truck APIs and any API Documentation or other API materials made available by PACCAR on its PACCAR API Catalog, available at https://developers.paccar.cloud." — [same source] — **DOCUMENTED**. This confirms `developers.paccar.cloud` is indeed PACCAR's official, named "PACCAR API Catalog" for its "Connected Truck APIs" line (telematics/connected-vehicle data, not explicitly confirmed to include PRWS/OPC/MDI dealer-systems APIs — those may be a separate, non-public-facing integration channel; **UNVERIFIED** whether PRWS/OPC/MDI are exposed via this same catalog or via a separate dealer-only integration mechanism, given that CDK/Karmak/Procede all describe PRWS/OPC/MDI access as mediated through their own DMS-vendor integrations rather than direct third-party API subscription).

> "Subject to and conditioned on your compliance with all terms and conditions set forth in this Agreement, we hereby grant you a limited, revocable, non-exclusive, non-transferable, non-sublicensable license during the term of the Agreement to use the API solely for your internal business purposes in developing Your Applications that will communicate and interoperate with the PACCAR Offering. You acknowledge that there are no implied licenses granted under this Agreement. We reserve all rights that are not expressly granted." — [same source] — **DOCUMENTED**.

> "You must obtain an API Token to use and access the API. You may not share your API Token with any third party... Your API Token may be revoked at any time by us." — [same source] — **DOCUMENTED**.

> "Except as expressly authorized under this Agreement, you may not: (a) copy, modify, or create derivative works of the API... (c) reverse engineer, disassemble, decompile, decode, adapt, or otherwise attempt to derive or gain access to any software component of the API... (f) combine or integrate the API with any software, technology, services, or materials not authorized by PACCAR." — [same source] — **DOCUMENTED**.

> "This Agreement does not entitle you to any support for the API." — [same source] — **DOCUMENTED**.

**Licensing posture summary (DOCUMENTED):** PACCAR's API licensing model is a standard restrictive, revocable, non-exclusive, token-gated developer agreement — structurally very similar to CDK's own API Licensing Terms (A.7 above): no implied rights, no sublicensing, no reverse engineering, unilateral revocation, and (notably) **no guaranteed support**. This is consistent with an OEM that treats its API catalog as a controlled-access mechanism for vetted integration partners (DMS vendors like CDK/Karmak/Procede, and telematics/fleet-app developers) rather than an open public API ecosystem.

A related PACCAR/DAF **"Data Integration Partner Program"** (documented on DAF's global sites, since DAF is a PACCAR subsidiary using shared "PACCAR Connect" branding) confirms a formal partner-onboarding process gating third-party data access broadly across the PACCAR family:

> "This form is the start of becoming a data integration partner of the PACCAR Connect Open Platform. If you want to make use of rFMS, dedicated Webshop, or dedicated Appstore please consider being an official partner of PACCAR Connect." — [DAF/PACCAR Connect, Data Integration Partner Program](https://www.daf.com/en/products-and-services/daf-services/connected-services/paccar-connect-partners) — **DOCUMENTED**. This program, however, is explicitly framed around **telematics/connected-truck data** (rFMS = "remote Fleet Management System" standard, webshop, appstore) rather than dealer-management-system-level parts/warranty/financial integration — it is **UNVERIFIED** whether this is the same gate a PACCAR dealer-feedback (PRWS/OPC/MDI) plug-in would need to pass through, or a separate/parallel PACCAR access program specific to DMS vendors.

---

## Summary Table: DOCUMENTED vs. UNVERIFIED at a Glance

| Finding | Status |
|---|---|
| CDK's "80+ Heavy Truck OEM-specific integrations" headline number | DOCUMENTED (as an unitemized claim) |
| An itemized public list of what the 80+ integrations are | UNVERIFIED / not found |
| CDK names PACCAR OPC, PRWS, electronic shipper, Decisiv by name | DOCUMENTED |
| CDK newsletter language on Decisiv line-level corrections | DOCUMENTED (quoted verbatim) |
| CDK publishes MDI/DIF/SOF/COF terminology anywhere | UNVERIFIED — not found; confirmed absent |
| CDK publishes PACCAR financial-statement transmission | UNVERIFIED — not found; confirmed absent |
| Karmak names 13 PACCAR integrations incl. financial reporting, MDI/COF | DOCUMENTED |
| Karmak's "financial statements automatically downloaded to PACCAR" claim | DOCUMENTED as Karmak's claim; underlying standard is UNVERIFIED |
| Procede's PACCAR integration detail level | DOCUMENTED (press release generic; product-update posts granular) |
| STAR Financial Statement BOD exists | DOCUMENTED |
| A universal cross-OEM dealer financial-statement transmission standard | **UNVERIFIED / does not appear to exist as a unified public standard** |
| NADA 20-Group / composite formats | DOCUMENTED as ratio-definition and proprietary-consultancy upload standards, not a universal OEM-facing file standard |
| STAR6 XML v6.2.4 release, effective 2024-07-04 | DOCUMENTED |
| January 2026 STAR Automotive Retail Domain Model incl. Accounting domain | DOCUMENTED |
| STAR's "Medium & Heavy-duty Trucks" segment coverage | DOCUMENTED (named as covered segment; no truck-specific BOD variants found) |
| DIF/SOF mechanics, fields, cadence (via TU Eindhoven thesis on DAF/MDI) | DOCUMENTED at business-process level; file-format/schema level UNVERIFIED |
| VMRS as shared service/parts vocabulary | DOCUMENTED |
| Vendor-level (CDK/Karmak/Procede) explicit VMRS conformance claims | UNVERIFIED |
| developers.paccar.cloud catalog contents | UNVERIFIED (blocked by robots.txt) |
| PACCAR API License Agreement terms | DOCUMENTED |
| Whether PRWS/OPC/MDI are exposed via developers.paccar.cloud vs. a separate DMS-vendor-only channel | UNVERIFIED |

---

## Source List (all fetched directly)

- [CDK Global, Heavy Truck (ht-oem newsletter)](https://www2.cdkglobal.com/ht-oem)
- [CDK Global, Heavy Truck (htonestop)](https://www2.cdkglobal.com/htonestop)
- [CDK Global Heavy Truck, OEM & ISV Integrations](https://www.cdkglobalheavytruck.com/oem-integrations)
- [CDK Global, Heavy Truck (stability)](https://www2.cdkglobal.com/stability)
- [CDK Global press release, Truck Connect Conference, March 25, 2025](https://www.cdkglobal.com/media-center/cdk-hosts-3rd-annual-truck-connect-conference-april-8-10)
- [Fortellis blog, "Meeting the Unique Needs of Heavy Truck Dealers," Jan. 7, 2022](https://fortellis.io/blog/meeting-unique-needs-heavy-truck-dealers)
- [Fortellis Docs, API Directory](https://docs.fortellis.io/docs/general/api-directory-marketplace/api-directory/)
- [Fortellis App Listing Guide PDF](https://community.fortellis.io/sites/default/files/Fortellis_App.Listing.Guide_.pdf)
- [CDK Drive Get Repair Order v3 API PDF](https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/cf3e1079-e617-4e4d-acd0-21e991f60408/external/20251117202238328-ze9Edh5W.pdf)
- [CDKDrive Repair Orders v1 API Developer Guide](https://prod-fortellis-provider-api-reference-documents.s3-us-west-2.amazonaws.com/c7771500-1c95-4f8e-9241-eddc17cd55f6)
- [CDK Global, Partner Program Pricing Guide PDF](https://www.cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf)
- [CDK Global, API Licensing Terms](https://www.cdkglobal.com/api-licensing-terms)
- [BusinessWire, CDK Global Customer Rewards Program press release, Feb. 15, 2020](https://www.businesswire.com/news/home/20200215005009/en/CDK-Global-Introduces-New-Pricing-Structure-With-its-Customer-Rewards-Program)
- [Karmak, PACCAR Integration page](https://www.karmak.com/integrations/paccar)
- [Karmak Fusion 3.59 cumulative release notes PDF](https://webhelp.karmak.com/ReleaseNotes/Fusion/3.59_cumulative.pdf)
- [PACCAR/Decisiv support site, Feature List for Karmak Fusion](https://support.paccar.decisiv.net/hc/en-us/articles/360033879154-Feature-List-for-Karmak-Fusion)
- [Procede Software press release, Oct. 31, 2023](https://www.procedesoftware.com/paccar-integrations-three-new-releases/)
- [Procede Software, LinkedIn PRWS product update](https://www.linkedin.com/posts/procede-software_procedesoftware-excededms-productupdate-activity-7402395748069548032-qWoj)
- [Procede Software, Facebook OPC product update](https://www.facebook.com/procedesoftwareofficial/posts/congratulations-to-scott-coleson-of-our-customer-fourstar-freightliner-for-being/2998645510231135/)
- [STAR, XML BODs page](https://www.starstandard.org/index.php/star-xml-bods/)
- [STAR, STAR6 6.2.4 XML Schema Repository Page](https://www.starstandard.org/index.php/star6-6-2-4-xml-schema-repository-page/)
- [STAR press release, Automotive Retail Domain Model, Jan. 27, 2026](https://www.starstandard.org/index.php/2026/01/27/star-unveils-industry-defining-retail-automotive-domain-model-to-advance-data-interoperability-and-ai-transformation-across-the-entire-ecosystem/)
- [STAR Warranty Payment specification PDF](https://qa.starstandard.org/images/SIGDTS/STARWarrantyPayments.pdf)
- [Liquid Technologies, STAR WarrantyClaimReconciliation schema docs](https://schemas.liquid-technologies.com/LibraryDocs/STAR/5.3.4/warrantyclaimreconciliation.html)
- [ServiceNow, Warranty Claims SOAP API docs](https://www.servicenow.com/docs/r/manufacturing/warranty-claims-SOAP-API.html)
- [NADA, 2026 Formulas, Definitions, Guides PDF](https://slideguide.nada.org/NADASlideGuide.pdf)
- [NCM Associates, Financial Statement Submission Guide PDF](https://portal.ncmassociates.com/content/help/docs/FinancialStatementSubmissionGuide.pdf)
- [Autosoft, NIADA Financial Statement guide PDF](https://download.autosoft-asi.com/instructions/NIA/NIADAFS.pdf)
- [TU Eindhoven, Verhoijsen Master Thesis PDF](https://pure.tue.nl/ws/portalfiles/portal/163151681/Master_Thesis_Jessica_Verhoijsen.pdf)
- [TMC, VMRS Overview](https://tmc.trucking.org/VMRS-Overview)
- [TMC, VMRS Introduction Handbook PDF](https://tmc.trucking.org/sites/default/files/VMRS_INTRO.pdf)
- [TMC, VMRS Flyer PDF](https://tmc.trucking.org/sites/default/files/VMRS_flyer_2021_web.pdf)
- [Geotab, VMRS glossary](https://www.geotab.com/glossary/vmrs/)
- [Aspire/VMRS white paper PDF](https://dev-aspire.imgix.net/files/base/cygnus/vspc/document/2025/08/68927fc64f44ac85a2b60911-2017_02_vmrs_nextlevel_whitepaper_interactive.pdf)
- [PACCAR, Digital Services Terms / API License Agreement](https://staging-paccar.anthology-digital.com/digital-services-terms/)
- [DAF/PACCAR Connect, Data Integration Partner Program](https://www.daf.com/en/products-and-services/daf-services/connected-services/paccar-connect-partners)
- [CDK Global Heavy Truck Team webinar, YouTube, Oct. 2022](https://www.youtube.com/watch?v=5BjvDxTD7hs)
- [CDK CONNECT 2025 presentation, YouTube](https://www.youtube.com/watch?v=OyQmaCKa4oU)

`developers.paccar.cloud` was attempted directly but returned `disallow_by_robots`; its contents are therefore characterized only via the PACCAR API License Agreement's references to it, not by direct enumeration.
