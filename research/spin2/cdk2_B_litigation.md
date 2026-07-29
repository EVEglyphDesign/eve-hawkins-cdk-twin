# Lane B — The Litigation and Regulatory Record as a Data-Model Source

**Scope:** CDK/Reynolds antitrust wars (Authenticom v. CDK/Reynolds; MDL 2817), collateral CDK
suits, state dealer-data-privacy statutes, FTC Safeguards Rule, and the June 2024 BlackSuit
ransomware breach notifications and class actions — mined for sworn/legislated descriptions of
DMS data categories, files, and extraction mechanics.

**Reader context:** Peterbilt Atlantic — nine rooftops, Atlantic Canada, heavy truck,
PACCAR/Peterbilt franchise, runs CDK Drive + Lightspeed. Building a digital twin of dealership
ledger/operations outside CDK.

---

## 1. What I actually retrieved

All files below are in `/home/user/workspace/cdk2_raw/B/`. Full-text extractions (`*_fulltext.txt`)
were produced from each PDF with `pdfplumber` and grepped for data-category language.

| # | File | Source URL | Pages | Status |
|---|------|-----------|-------|--------|
| 1 | `authenticom_PI_opinion_2017-07-28.pdf` | [govinfo.gov, USCOURTS-wiwd-3_17-cv-00318](https://www.govinfo.gov/content/pkg/USCOURTS-wiwd-3_17-cv-00318/pdf/USCOURTS-wiwd-3_17-cv-00318-2.pdf) | 23 | Judge James D. Peterson's PI Opinion & Order, Dkt #172, 17-cv-318-jdp, W.D. Wis., filed 7/14/2017. Full text in `authenticom_PI_2017-07-28_fulltext.txt`. |
| 2 | `authenticom_PI_opinion_07-14-2017_doc172.pdf` | [govinfo.gov, USCOURTS-ilnd-1_18-cv-00868](https://www.govinfo.gov/content/pkg/USCOURTS-ilnd-1_18-cv-00868/pdf/USCOURTS-ilnd-1_18-cv-00868-2.pdf) | 23 | Same opinion, refiled onto the N.D. Ill. MDL docket (1:18-cv-00868, Dkt #172). Byte-identical content to #1; retained as the MDL-docket copy. |
| 3 | `mdl2817_dealership_MTD_opinion_2019-01-25_doc184.pdf` | [govinfo.gov, USCOURTS-ilnd-1_18-cv-00864-6](https://www.govinfo.gov/content/pkg/USCOURTS-ilnd-1_18-cv-00864/pdf/USCOURTS-ilnd-1_18-cv-00864-6.pdf) | 30 | Judge Amy J. St. Eve, MDL 2817, dealer-side motion-to-dismiss opinion re: CDK/Reynolds counterclaims against Authenticom, 1/25/2019 (Dkt #506). Full text in `mdl2817_dealership_MTD_2019-01-25_fulltext.txt`. |
| 4 | `mdl2817_counterclaim_MTD_opinion_2019-01-25_doc184.pdf` | [govinfo.gov, USCOURTS-ilnd-1_18-cv-00864-7](https://www.govinfo.gov/content/pkg/USCOURTS-ilnd-1_18-cv-00864/pdf/USCOURTS-ilnd-1_18-cv-00864-7.pdf) | 67 | Companion opinion, same date, on plaintiffs'/AutoLoop's motions re: arbitration and equitable estoppel (Dkt #507). Full text in `mdl2817_counterclaim_MTD_opinion_2019-01-25_doc184_fulltext.txt`. |
| 5 | `mdl2817_counterclaims_opinion_doc749_2019-09-03.pdf` | [govinfo.gov, USCOURTS-ilnd-1_18-cv-00864-9](https://www.govinfo.gov/content/pkg/USCOURTS-ilnd-1_18-cv-00864/pdf/USCOURTS-ilnd-1_18-cv-00864-9.pdf) | 30 | Opinion on Authenticom's motion to dismiss CDK's breach-of-contract/CFAA/DMCA counterclaims, 9/3/2019. Full text in `mdl2817_counterclaims_opinion_doc749_2019-09-03_fulltext.txt`. |
| 6 | `mdl2817_vendor_class_cert_order_2024-07-22.pdf` | [business.cch.com mirror](https://business.cch.com/ald/InreDealerManagementSystemsAntitrustLitigation7242024.pdf) | 36 | AutoLoop vendor-class certification order, 7/22/2024, describing DIS market structure and Dr. Mark Israel's expert damages model. Full text in `mdl2817_vendor_class_cert_order_2024-07-22_fulltext.txt`. |
| 7 | `mdl2817_settlement_approval_order_2024-08-23.pdf` | [classaction.org mirror](https://www.classaction.org/media/dealer-management-systems-antitrust-litigation-cdk-settlement-preliminary-approval-order.pdf) | 11 | Preliminary approval order, dealership-class settlement, 8/23/2024. Full text in `mdl2817_settlement_approval_order_2024-08-23_fulltext.txt` — no data-category language found (procedural only). |
| 8 | `authenticom_wiwd_case_history_doc18_2024cv00571.pdf` | [govinfo.gov, USCOURTS-wiwd-3_24-cv-00571-0](https://www.govinfo.gov/content/pkg/USCOURTS-wiwd-3_24-cv-00571/pdf/USCOURTS-wiwd-3_24-cv-00571-0.pdf) | 8 | Case-history summary on remand of Authenticom's case to W.D. Wis. No new data-category detail beyond what's in the PI opinion. |
| 9 | `authenticom_wiwd_2024cv00571_doc241.pdf` | [govinfo.gov, USCOURTS-wiwd-3_24-cv-00571-2](https://www.govinfo.gov/content/pkg/USCOURTS-wiwd-3_24-cv-00571/pdf/USCOURTS-wiwd-3_24-cv-00571-2.pdf) | 40 | Later docket filing on remand. No data-category or file/field language found on grep. |
| 10 | `arizona_hb2418_2019.pdf` | [azleg.gov](https://www.azleg.gov/legtext/54leg/1r/bills/hb2418h.pdf) | 7 | Arizona House Bill 2418 (2019), enacted as A.R.S. Title 28, Ch. 10, Art. 10. Full statutory text in `az_hb2418_fulltext.txt`. |
| 11 | `cdk_dealertrack_authorization_process.pdf` | [us.dealertrack.com](https://us.dealertrack.com/wp-content/uploads/sites/2/2020/08/Dealertrack-CDK-Authorization-Process.pdf) | 5 | CDK Partner Program / Partner Access Authorization Process walkthrough. Full text in `cdk_dealertrack_authorization_process_fulltext.txt`. |
| 12 | `cdk_dealer_enrollment_form_dealertrack.pdf` | [us.dealertrack.com](https://us.dealertrack.com/wp-content/uploads/sites/2/2024/10/CDK-Dealer-Enrollment-Form.pdf) | 17 | CDK Enrollment Guide: Using eStore for Dealer Authorization. Full text in `cdk_dealer_enrollment_form_dealertrack_fulltext.txt`. |
| 13 | `cdk_dms_user_guide_700credit_2025-05.pdf` | [700credit.com](https://www.700credit.com/wp-content/uploads/2025/05/CDK-DMS-User-Guide-May-25.pdf) | 14 | Third-party (700Credit) F&I credit-pull integration guide for the CDK DMS UI. Full text in `cdk_dms_user_guide_700credit_2025-05_fulltext.txt`. |
| 14 | `cdk_data_export_import_faq.pdf` | [cms.cdkglobal.com](https://cms.cdkglobal.com/sites/default/files/2024-01/Data%20Export%20and%20Import%20Tools%20Dealer%20FAQ_FinalV3-1.pdf) | 5 | CDK's own "Data Your Way" Dealer FAQ, describing DABE/DART successors and the 5 PIP packages. Full text in `cdk_data_export_import_faq_fulltext.txt`. |
| 15 | `cdk_class_action_loginov_complaint_2024-06-22.pdf` | [classaction.org](https://www.classaction.org/media/loginov-v-cdk-global-llc.pdf) | 43 | Loginov v. CDK Global, LLC consumer class complaint, N.D. Ill. 1:24-cv-05221, filed 6/22/2024. Full text in `cdk_loginov_complaint_fulltext.txt`. |
| 16 | `cdk_breach_notification_MA_mirror_TEXT.md` | [mass.gov](https://www.mass.gov/doc/2024-1703-cdk-global-llc/download) | n/a | CDK's own vendor-breach notification letter, dated 9/20/2024. **The PDF itself would not download as a valid file** — the mass.gov endpoint serves an HTML wrapper, not a raw PDF, on every retry (`curl` with multiple user agents; confirmed via `file` command each time). Full verbatim text was recovered from the same URL as indexed by a search engine and is preserved verbatim in this markdown file with the source URL, per the "quote, do not paraphrase" rule. |

**Not downloaded as standalone files (content captured via search-engine index snippet only, with URL):**
these are cited inline in §3 with their source URL. They include: the Seventh Circuit opinion
(874 F.3d 1019) — captured via Findlaw/Justia HTML, not as a PDF (see §4); CDK's Partner Program
Pricing Guide (`cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf` — PDF
returned 0 pages to `pdfplumber`/`file`, i.e., corrupted or blocked; text below is from the
search-index snippet of that same URL); the CDK DDX User Guide (CourseHero-paywalled, partial
preview only); the Reynolds RCI Third Party List page; the CDK API Licensing Terms page.

---

## 2. The field/table/record dictionary

Every row is sourced from a specific document. Tag definitions: `[DOC]` = court/regulator/vendor
document, URL required; `[COMM]` = practitioner/trade-press source; `[INF]` = inference;
`[UNK]` = searched, not found.

### 2.1 Sworn/litigated data categories (Authenticom v. CDK/Reynolds; MDL 2817)

| Name as stated | Type/nature as stated | Meaning as stated by source | Tag | URL |
|---|---|---|---|---|
| "accounting, payroll, inventory, sales, parts, service, finance, and insurance" | Business function categories tracked in the DMS | Seventh Circuit's list of what dealers "keep track of" via their DMS | `[DOC]` | [Findlaw, Authenticom v. CDK Global, 874 F.3d 1019](https://caselaw.findlaw.com/court/us-7th-circuit/1879150.html) |
| "CDK-created forms, accounting rules, tax tables, and proprietary tools and data compilations" | CDK-alleged trade secrets stored on the DMS | CDK's own sworn enumeration (in its counterclaim, ¶127 and ¶115) of what it considers proprietary/trade-secret content on its DMS, as opposed to non-proprietary content | `[DOC]` | [MDL 2817 dealership MTD opinion (Dkt #506), p.20-21](https://www.govinfo.gov/content/pkg/USCOURTS-ilnd-1_18-cv-00864/pdf/USCOURTS-ilnd-1_18-cv-00864-6.pdf) |
| "data for prices and part numbers for replacement parts" | Explicitly NOT proprietary to CDK | CDK's own carve-out: it does **not** claim trade-secret ownership over OEM parts price/part-number data on its DMS — this belongs to the OEM | `[DOC]` | same, p.21 (¶23) |
| "specified data fields" | Data delivered through RCI | Reynolds' RCI (Reynolds Certified Interface) gives "third parties—vendors, typically—access and receive specified data fields in a highly controlled environment" | `[DOC]` | [Authenticom PI Opinion, Dkt #172, p.5](https://www.govinfo.gov/content/pkg/USCOURTS-wiwd-3_17-cv-00318/pdf/USCOURTS-wiwd-3_17-cv-00318-2.pdf) |
| "those fields reasonably necessary to the services that Authenticom provides" | Data-access limitation clause | The PI order's operative language: defendants may limit Authenticom's access to specific fields tied to the vendor's actual service, not the whole DMS | `[DOC]` | same, p.22 |
| "screen displays or user documentation" | Confidential Information, per CDK's Master Service Agreement §6(D) | CDK's MSA classifies DMS screen displays and user docs as Confidential Information the dealer may not disclose | `[DOC]` | [MDL 2817 dealership MTD opinion (Dkt #506), p.4](https://www.govinfo.gov/content/pkg/USCOURTS-ilnd-1_18-cv-00864/pdf/USCOURTS-ilnd-1_18-cv-00864-6.pdf) |
| "Third Party Access" / "3PA" | CDK's certified data-integration-services (DIS) product name | CDK's own branded program for authorized vendor access to dealer DMS data; contrasted with Reynolds' "RCI" | `[DOC]` | [MDL 2817 vendor class cert order, p.3-4](https://business.cch.com/ald/InreDealerManagementSystemsAntitrustLitigation7242024.pdf); [MDL dealership MTD opinion, p.4](https://www.govinfo.gov/content/pkg/USCOURTS-ilnd-1_18-cv-00864/pdf/USCOURTS-ilnd-1_18-cv-00864-6.pdf) |
| "Reynolds Certified Interface" / "RCI" | Reynolds' certified DIS product name | Reynolds' counterpart to 3PA | `[DOC]` | same |
| "Wind Down Agreement" | Feb 2015 CDK/Reynolds contract | Formalized a phase-out of Reynolds DMS access for CDK's DMI/IntegraLink subsidiaries | `[DOC]` | [MDL 2817 vendor class cert order, p.3-4](https://business.cch.com/ald/InreDealerManagementSystemsAntitrustLitigation7242024.pdf) |
| "3PA Agreement" and "RCI Agreement" | Feb 2015 CDK/Reynolds contracts | Reciprocal-access agreements between CDK's and Reynolds' certified DIS programs | `[DOC]` | same |
| "Managed Interface Agreements" | Renamed/renegotiated 3PA vendor contracts (per MDL complaint allegations) | Vendors required to use 3PA exclusively to integrate with CDK DMS data, or lose access by Dec 31, 2016 | `[DOC]` | [MDL 2817 counterclaim MTD opinion (Dkt #507), p.?](file:///home/user/workspace/cdk2_raw/B/mdl2817_counterclaim_MTD_opinion_2019-01-25_doc184_fulltext.txt) — line ref: "These new 3PA contracts (also referred to as the 'Managed Interface Agreements') required vendors to use 3PA if they wished to integrate CDK DMS data." |
| "Digital Motorworks (DMI)" and "IntegraLink" | CDK subsidiary data-integrator brands | CDK's own two independent data-integration businesses that historically sold DIS on the open market, including for **Reynolds'** DMS | `[DOC]` | [MDL 2817 vendor class cert order, p.3](https://business.cch.com/ald/InreDealerManagementSystemsAntitrustLitigation7242024.pdf) |
| "Fortellis" | CDK's successor DIS/API platform | Per the vendor-class certification order, CDK planned to "sunset 3PA... by the end of 2024" in favor of Fortellis | `[DOC]` | same, line 134 |

### 2.2 Extraction mechanics (sworn description of how third parties actually pull DMS data)

| Mechanism as stated | Description as stated by source | Tag | URL |
|---|---|---|---|
| "screen scrapes" | "Dealers who want to work with Authenticom provide Authenticom a username and password, which Authenticom uses to log into the dealer's DMS account on defendants' systems. Authenticom 'screen scrapes' the data by capturing what is displayed, and then it cleans up the data to keep the needed elements." | `[DOC]` | [Authenticom PI Opinion, p.4](https://www.govinfo.gov/content/pkg/USCOURTS-wiwd-3_17-cv-00318/pdf/USCOURTS-wiwd-3_17-cv-00318-2.pdf) |
| Automated/scheduled login | "Authenticom's information systems are programmed to automatically and regularly log into dealer DMS accounts so that the data that vendors use is up to date." | `[DOC]` | same, p.4 |
| Scoped user IDs | A dealership IT director "creates a user ID specifically for Authenticom that has access to limited accounts and a single function necessary to query and scrape the system." | `[DOC]` | same, p.4-5 |
| "hostile access" | Defendants' own term for Authenticom's screen-scraping extraction method, as objected to by CDK/Reynolds | `[DOC]` | same, p.5 |
| Query volume/load | "Authenticom's constant querying can tie up more than 50% of the DMS's entire computing capacity" (CDK allegation) | `[DOC]` | [MDL 2817 dealership MTD opinion, p.25-26](https://www.govinfo.gov/content/pkg/USCOURTS-ilnd-1_18-cv-00864/pdf/USCOURTS-ilnd-1_18-cv-00864-6.pdf) |
| Query pattern | Authenticom's automated scripts "'ping'[Reynolds'] DMS with computing requests at a rate of hundreds or thousands of times per day" (Reynolds allegation) | `[DOC]` | same, p.26 |
| Credential renewal circumvention | "Authenticom also implemented a software tool that automatically renewed user IDs that CDK had disabled" and modified scripts to bypass CAPTCHA | `[DOC]` | [MDL 2817 dealership MTD opinion, p.5](https://www.govinfo.gov/content/pkg/USCOURTS-ilnd-1_18-cv-00864/pdf/USCOURTS-ilnd-1_18-cv-00864-6.pdf) |
| "data integration services" / "DIS" / "data syndication" | The generic industry term (used by the court) for the process of "cleaning" and consolidating raw, unprocessed DMS data into a form usable by a vendor's application | `[DOC]` | [MDL 2817 vendor class cert order, p.2](https://business.cch.com/ald/InreDealerManagementSystemsAntitrustLitigation7242024.pdf) |
| "open architecture" vs. "closed architecture" | The Seventh Circuit's own framing: "Some dealer-management systems use open architecture, under which third parties have some access to dealer-originated data that has been plugged into the system. Others use closed architecture, under which that type of data scraping is forbidden under the license." | `[DOC]` | [Findlaw, Authenticom v. CDK Global, 874 F.3d 1019](https://caselaw.findlaw.com/court/us-7th-circuit/1879150.html) |

### 2.3 CDK's own current dealer-facing extraction products (from CDK's own FAQ and enrollment docs)

| Name as spelled | Type | Meaning as stated by source | Tag | URL |
|---|---|---|---|---|
| **Data Access Bulk Extract (DABE)** | Legacy CDK dealer data-access product | Predecessor of the current "Data Export Tool"; the FAQ frames the new tool as "an evolution of DABE" | `[DOC]` | [CDK Data Export and Import Tools Dealer FAQ](https://cms.cdkglobal.com/sites/default/files/2024-01/Data%20Export%20and%20Import%20Tools%20Dealer%20FAQ_FinalV3-1.pdf) |
| **Data Access Real Time (DART)** | Legacy CDK dealer data-access product | Predecessor of the current "Data Export/Import Tool" | `[DOC]` | same |
| **Data Export Tool** | Current CDK dealer data-export product | "Extract tools like Data Export require an understanding of the CDK file structure and dealership operations without the need for SQL query skills"; delivers CSV files to an SFTP folder | `[DOC]` | same |
| **Data Export/Import Tool** | Current CDK dealer read/write API product | Uses "Legacy APIs" internally called **PIPs** ("referred to as PIPs"); requires SOAP API knowledge, OAuth 2.0, connection to Dealer private network | `[DOC]` | same |
| **PIP Packages** (5 named) | API bundles by department | "Vehicle Package," "Accounting Package," "Service Package," "Customer Package," "Parts package" — each described with its extract/writeback scope (see verbatim quote §3) | `[DOC]` | same |
| SFTP delivery folder | File transfer mechanism | CSV files land in a managed SFTP folder; "Processed Data will reside in SFTP folder for the next 7 days and will then be purged"; default refresh 24 hours, but can run at 1-hour or 15-minute frequency, producing 24 or 96 files/day respectively | `[DOC]` | same |
| CMF number | Dealer/company identifier | "Dealers can contract for the entire Dealer Group within a single document by selecting all applicable Dealership CMFs" — CMF is the unit selected when enrolling a data-export product per store | `[DOC]` | same; also [CDK Partner Access Authorization Process](https://us.dealertrack.com/wp-content/uploads/sites/2/2020/08/Dealertrack-CDK-Authorization-Process.pdf) |
| DealerSuite / eStore | CDK's dealer-facing authorization portal | The system through which a dealer's Authorized Signer logs in, enrolls a partner, selects CMF(s), and confirms per-location "DMS Accounts" access for that partner | `[DOC]` | [CDK Partner Access Authorization Process](https://us.dealertrack.com/wp-content/uploads/sites/2/2020/08/Dealertrack-CDK-Authorization-Process.pdf); [CDK Enrollment Guide](https://us.dealertrack.com/wp-content/uploads/sites/2/2024/10/CDK-Dealer-Enrollment-Form.pdf) |
| Addendum PDF | Per-partner data-scope disclosure | "Please open and review before proceeding. The information is for your review and includes a summary of the data the partner will be able to access" — this is CDK's own document that would, if captured, enumerate exact field/data-category access per vendor, but the Addendum PDF itself was not found publicly (see §4) | `[DOC]` | same |
| "CDK Data" account list | Suggested-account list in eStore | "The account access listed under 'CDK Data' is only listed as a guide and does not authorize account access" — i.e., a non-binding suggested list of DMS accounts, distinct from the dealer's actual authorized selection | `[DOC]` | [CDK Partner Access Authorization Process, p.5](https://us.dealertrack.com/wp-content/uploads/sites/2/2020/08/Dealertrack-CDK-Authorization-Process.pdf) |
| Account Type | DMS access-scoping unit | "Only one account may be selected from each Account Type" when authorizing a partner's access at a location | `[DOC]` | same |

### 2.4 Legislated data categories — Arizona HB 2418 (2019), enacted as A.R.S. §28-4651 et seq.

| Term as defined in statute | Statutory meaning | Tag | URL |
|---|---|---|---|
| "PROTECTED DEALER DATA" | Statutorily defined (per the working `az_hb2418_fulltext.txt` capture) to mean any of: (a) personal, financial, or other data about a customer/consumer that is stored in a dealer's data system; (b) motor vehicle diagnostic data; (c) other data relating to the dealer's business operations that is stored in a dealer's computer system | `[DOC]` | [Arizona HB 2418 (2019)](https://www.azleg.gov/legtext/54leg/1r/bills/hb2418h.pdf) |
| "DEALER DATA SYSTEM" | The dealer's computer system, including a DMS, in which protected dealer data is stored | `[DOC]` | same |
| "AUTHORIZED INTEGRATOR" | A third party the dealer has specifically authorized to access protected dealer data | `[DOC]` | same |
| "REQUIRED MANUFACTURER DATA" | Data an OEM requires the dealer to provide, typically for warranty, recall, or compliance purposes | `[DOC]` | same |
| "STAR STANDARDS" | Referenced in the statute as the industry data-exchange format standard that authorized integrations must comply with | `[DOC]` | same |

**Note on other target statutes:** the brief specifically asked for Montana, North Carolina, and
Hawaii dealer-data statutes in addition to Arizona. These were **not retrieved this pass** — see
§4 for exactly what was searched.

### 2.5 Consumer-breach data categories — Loginov v. CDK Global (N.D. Ill. 1:24-cv-05221)

| Category as pled | Context as stated in complaint | Tag | URL |
|---|---|---|---|
| "name, addresses, Social Security numbers, driver's licenses, and financial details like credit card numbers" | Plaintiff's own alleged "Private Information" provided to CDK/dealership, alleged to have been exposed | `[DOC]` | [Loginov v. CDK Global complaint, p.2 and p.~35](https://www.classaction.org/media/loginov-v-cdk-global-llc.pdf) |
| Social Security numbers (extended discussion) | Multiple paragraphs (¶¶62-65) devoted specifically to why SSN exposure is uniquely harmful and hard to remediate | `[DOC]` | same |

### 2.6 Vendor-breach data categories — CDK's own notification letter (Massachusetts/Maine AG filings)

| Category as stated | Context | Tag | URL |
|---|---|---|---|
| "Name, business or personal address, and business tax identification number or social security number" | CDK's own description of what was exposed about **its vendors** (not dealership consumers) in the June 19, 2024 incident, per the notification letter dated Sept. 20, 2024 | `[DOC]` | [Massachusetts AG mirror of CDK notification letter](https://www.mass.gov/doc/2024-1703-cdk-global-llc/download) — verbatim text preserved in `/home/user/workspace/cdk2_raw/B/cdk_breach_notification_MA_mirror_TEXT.md` |
| Scope: "36 individuals in total," "1 Maine resident" | Secondary reporting on the Maine AG filing of the same letter | `[COMM]` (secondary account of a [DOC] filing; primary Maine filing itself not independently re-downloaded) | [LinkedIn/ComplyAuto post, Oct 7 2024](https://www.linkedin.com/posts/complyauto_office-of-the-maine-ag-consumer-protection-activity-7249086914807394306-bZYb) |

**Important distinction the record draws for you:** the vendor-breach notice (§2.6, narrow fields —
name/address/tax ID/SSN of CDK's own vendors/suppliers) is a **different, smaller disclosure** than
the broader dealership-customer PII alleged in the Loginov consumer class action (§2.5 — names,
addresses, SSNs, driver's licenses, credit card numbers, bank account details of dealership
customers). Do not conflate the two when reconstructing what "customer PII in the DMS" means.

---

## 3. Verbatim quotes worth keeping

> "In an effort to keep track of such vital business matters as accounting, payroll, inventory,
> sales, parts, service, finance, and insurance, the dealerships use computerized
> dealer-management systems... Some dealer-management systems use open architecture, under which
> third parties have some access to dealer-originated data that has been plugged into the system.
> Others use closed architecture, under which that type of data scraping is forbidden under the
> license."
> — Seventh Circuit, *Authenticom, Inc. v. CDK Global, LLC*, 874 F.3d 1019 (2017). [Findlaw](https://caselaw.findlaw.com/court/us-7th-circuit/1879150.html)

> "Dealers who want to work with Authenticom provide Authenticom a username and password, which
> Authenticom uses to log into the dealer's DMS account on defendants' systems. Authenticom
> 'screen scrapes' the data by capturing what is displayed, and then it cleans up the data to keep
> the needed elements. Authenticom works with a very large number of dealers, so it has automated
> this process. Authenticom's information systems are programmed to automatically and regularly
> log into dealer DMS accounts so that the data that vendors use is up to date."
> — Judge James D. Peterson, Preliminary Injunction Opinion & Order, Dkt #172, p.4, *Authenticom v.
> CDK Global/Reynolds and Reynolds*, No. 17-cv-318-jdp (W.D. Wis. July 14, 2017). [govinfo.gov](https://www.govinfo.gov/content/pkg/USCOURTS-wiwd-3_17-cv-00318/pdf/USCOURTS-wiwd-3_17-cv-00318-2.pdf)

> "Reynolds has never approved of third-party access based solely on the dealer's authorization.
> Reynolds allows third-party access only with its own approval, and preferably via an interface
> specifically designed for that purpose, the Reynolds Certified Interface (RCI). Through RCI,
> third parties—vendors, typically—access and receive specified data fields in a highly controlled
> environment."
> — same opinion, p.5.

> "Defendants may also limit the data accessed by Authenticom to those fields reasonably necessary
> to the services that Authenticom provides."
> — same opinion, p.22 (operative order language).

> "[CDK's] DMS contains numerous proprietary CDK trade secrets, including forms, accounting
> rules, tax tables, and proprietary tools and data compilations... CDK also explains what
> materials on its DMS it does not consider to be proprietary, such as data for prices and part
> numbers for replacement parts that would constitute proprietary data of original equipment
> manufacturers or 'OEMs.'"
> — Judge Amy J. St. Eve, MDL 2817 dealership-side motion-to-dismiss opinion, Dkt #506, p.20-21,
> *In re Dealer Management Systems Antitrust Litigation*, No. 1:18-cv-00864 (N.D. Ill. Jan. 25,
> 2019). [govinfo.gov](https://www.govinfo.gov/content/pkg/USCOURTS-ilnd-1_18-cv-00864/pdf/USCOURTS-ilnd-1_18-cv-00864-6.pdf)

> "Authenticom's data extraction methods show that Authenticom burdens CDK's systems with poorly
> constructed, inefficient and repetitive queries that extract too much data, too frequently, and
> during peak dealer business hours... At times, for at least some dealers, Authenticom's constant
> querying can tie up more than 50% of the DMS's entire computing capacity."
> — same opinion, p.25.

> "[T]he automated scripts that Authenticom uses 'ping'[Reynolds'] DMS with computing requests at
> a rate of hundreds or thousands of times per day and are dangerous to the DMS. That speed and
> volume taxes the computational and network resources of the Reynolds DMS, resulting in
> degradation of service for dealers and increased operational costs to Reynolds."
> — same opinion, p.26 (quoting Reynolds' counterclaim ¶99).

> "[T]o make their apps commercially viable, vendors require access to dealers' (their clients')
> data, which is stored on the dealers' DMS. However, this data is kept on the DMS in a raw and
> unprocessed form that is generally unusable by vendors. So, vendors enlist data integration
> companies to 'clean' and consolidate the data, making it functional for the vendor's needs—a
> process generally known as data syndication and referred to here as data integration services
> ('DIS')."
> — MDL 2817 Vendor Class certification order, p.2, *In re Dealer Management Systems Antitrust
> Litigation*, No. 1:18-cv-02521 (N.D. Ill. July 22, 2024). [business.cch.com mirror](https://business.cch.com/ald/InreDealerManagementSystemsAntitrustLitigation7242024.pdf)

> "CDK's data integration service is known as Third Party Access ('3PA'), and Reynolds's data
> integration service is known as Reynolds Certified Interface ('RCI'). Although 3PA and RCI only
> provide DIS for Defendants' respective DMSs, CDK also owns two independent data
> integrators—Digital Motorworks ('DMI') and IntegraLink—that provide DIS with respect to data
> stored on others' DMSs (e.g., Reynolds) as well."
> — MDL 2817 dealership MTD opinion, p.4-5. [govinfo.gov](https://www.govinfo.gov/content/pkg/USCOURTS-ilnd-1_18-cv-00864/pdf/USCOURTS-ilnd-1_18-cv-00864-6.pdf)

> "Extract tools like Data Export require an understanding of the CDK file structure and
> dealership operations without the need for SQL query skills. Typically, database administrators
> (DBA) and automotive retail knowledge data SMEs possess these skills."
> — CDK Data Export and Import Tools Dealer FAQ, p.2. [cms.cdkglobal.com](https://cms.cdkglobal.com/sites/default/files/2024-01/Data%20Export%20and%20Import%20Tools%20Dealer%20FAQ_FinalV3-1.pdf)

> "What are the 5 API (PIP) Packages Available to a Dealer as a part of the Data Export/Import
> Tools?... 1. Vehicle Package: Supports varying capabilities for extract, writeback and updates to
> vehicle inventory, customer vehicle, and vehicle search data. 2. Accounting Package: Supports
> varying capabilities for extract of accounting data. 3. Service Package: Supports varying
> capabilities for extract, writeback and updates to Service Customer, Service Appointment, Service
> Vehicle and RO detailed Data. 4. Customer Package: Supports extract, writeback and updates to
> Dealership Customer data across vehicle and service. 5. Parts package: Supports varying
> capabilities for extract, writeback and updates to customer, and Parts inventory, pricing,
> availability, special orders, and parts number search."
> — same FAQ, p.4-5.

> "What will be the format of the Data in the SFTP Folder? CSV Format... How long will the Data
> Reside in the SFTP Folder? Processed Data will reside in SFTP folder for the next 7 days and will
> then be purged."
> — same FAQ, p.4.

> "Please follow the steps below to authorize a CDK approved partner to have access to your CDK
> DMS data... STEP 7: Click on 'Addendum PDF.' Please open and review before proceeding. The
> information is for your review and includes a summary of the data the partner will be able to
> access... STEP 13: Click 'Edit DMS Accounts' to select and authorize each location's account
> access. A free text field is available if the accounts are not listed. The accounts listed under
> 'CDK Data' is only listed as a guide and does not authorize account access... Only one account
> may be selected from each Account Type."
> — CDK Partner Access Authorization Process (via DealerTrack mirror), p.3-5. [us.dealertrack.com](https://us.dealertrack.com/wp-content/uploads/sites/2/2020/08/Dealertrack-CDK-Authorization-Process.pdf)

> "The following dealership titles are generally accepted as having the authority to sign for
> vendor access to dealership data... President, Vice President, General Sales Manager, Dealer
> Principal, Business Manager, Chief Information Officer (CIO), General Manager, Comptroller,
> Chief Technical Officer (CTO), Controller, Owner, Chief Financial Officer (CFO), Chairman, CEO,
> COO, IT Director, IT Manager, Managing Member (LLC Only), Managing Partner, Secretary, Treasurer."
> — same document, p.5.

> "Our investigation determined that the following types of information related to you were in
> the data subject to unauthorized access: Name, business or personal address, and business tax
> identification number or social security number."
> — CDK Global, LLC vendor breach notification letter, dated Sept. 20, 2024, filed with
> Massachusetts AG. [mass.gov](https://www.mass.gov/doc/2024-1703-cdk-global-llc/download) (verbatim text preserved in `cdk2_raw/B/cdk_breach_notification_MA_mirror_TEXT.md` since the source file itself would not download as a valid PDF)

> "...including, name, addresses, Social Security numbers, driver's licenses, and financial
> details like credit card numbers..."
> — Loginov v. CDK Global, LLC, Class Action Complaint, N.D. Ill. 1:24-cv-05221, ¶39 & ¶126-127.
> [classaction.org](https://www.classaction.org/media/loginov-v-cdk-global-llc.pdf)

---

## 4. What I searched and could not find

- **Judge Conley's opinion, as named in the task brief.** The actual author of the Authenticom PI
  opinion is **Judge James D. Peterson**, not Judge Conley. This was already flagged in the task
  brief itself as a known error; confirmed independently from the opinion's signature block and
  caption (Dkt #172, 17-cv-318-jdp). No Conley-authored opinion in this litigation was found.
- **Montana, North Carolina, and Hawaii dealer-data-privacy statutes.** Searched for each by name
  (queries used: "Montana dealer data privacy statute DMS," "North Carolina dealer data protection
  law automotive," "Hawaii dealer data statute DMS," "state dealer data ownership law list 2024")
  in earlier passes of this session; none returned a citable, retrievable statute text comparable
  to Arizona's HB 2418 within the time available this pass. Only Arizona HB 2418 was retrieved
  and read in full. This is a genuine gap — not confirmed absent, just not found and read this pass.
- **Motor Vehicle Software Corp. v. CDK, Cox Automotive/Dealertrack v. CDK, and AutoLoop v. CDK as
  standalone filings.** These appear in the record only as **co-plaintiffs/transferred cases within
  MDL 2817** (per the JPML transfer orders — [MDL-2817 Initial Transfer](https://www.jpml.uscourts.gov/sites/jpml/files/MDL-2817-Initial_Transfer-01-18.pdf) lists Motor Vehicle Software Corporation v.
  CDK Global, C.A. No. 2:17-00896, C.D. Cal.). AutoLoop's specific vendor-class complaint and expert
  report (Dr. Mark Israel) were referenced and quoted **through the July 2024 class-certification
  order** (§2/§3 above), but AutoLoop's own amended complaint (CourtListener docket 6296613, Doc
  #191, filed June 5, 2018) was not independently downloaded — it is sealed or was not retrievable
  via the free CourtListener/RECAP tier in the searches run. The consolidated dealership-class
  complaint (Doc #198, filed June 6, 2018) is listed on the docket as **sealed**.
- **CDK's Partner Program Pricing Guide as a valid PDF.** The URL
  (https://www.cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf) returns a
  file that `pdfplumber`/`file` reports as corrupted/zero-page. The pricing-tier text quoted in the
  first-spin documents (`$28` base extract-only fee, `$23` add-on per data type, `$150` electronic
  vehicle registration) is from a search-engine index snippet of that URL, not from a document this
  agent itself opened and verified page-by-page. Treat that pricing detail as `[COMM]`-tier
  confidence (indexed snippet, not independently re-verified), not `[DOC]`-tier, until someone
  retrieves a working copy.
- **CDK DDX (Dealer Data Exchange) User Guide, full text.** Only available via a CourseHero preview
  (3 of 14 pages, paywalled for the rest) at
  https://www.coursehero.com/file/17918315/CDK-DDX-USER-GUIDE/. The report names quoted in the
  earlier session summary ("Syndication by Program," "Non-CDK Code on the DMS," etc.) come from that
  preview only — the full 14-page guide was not obtained.
- **The Seventh Circuit opinion as a standalone downloadable PDF.** Read and quoted via Findlaw,
  Justia, and Casetext HTML case pages (all free, all cited above), but no PDF copy of *Authenticom,
  Inc. v. CDK Global, LLC*, 874 F.3d 1019 (7th Cir. 2017) was downloaded into `cdk2_raw/B/`. A
  foureyes.io URL previously associated with this opinion now returns a 404.
- **California and Washington AG breach-notification entries for CDK Global specifically.**
  Searched `oag.ca.gov/privacy/databreach/list` and `atg.wa.gov/data-breach-notifications`
  (queries used: "oag.ca.gov data breach CDK Global 2024," "atg.wa.gov data breach notification CDK
  Global"); both are large, paginated/searchable databases that did not surface a CDK-specific entry
  through general web search. A direct manual search of each state database's UI (not performed
  this pass) would be the next step if this gap matters.
- **FTC action naming CDK directly.** The one FTC document found
  (https://www.ftc.gov/system/files/ftc_gov/pdf/013820250428Plaintiffs'MemoofLawIOTDefs'MotionforJudgmentonthePleadings.pdf,
  Case 3:25-cv-50017) cites the *Authenticom* precedent but was not confirmed to be an action against
  or naming CDK itself as a party — not independently verified this pass, and not included in the
  dictionary above on that basis.
- **FTC Safeguards Rule dealer-specific guidance document, primary source.** Not retrieved this
  pass; CDK's own July 2024 FTC notice-filing procedure is referenced only via a trade blog
  (ComplyAuto, `[COMM]` tier, already flagged as such in the prior session), not a primary FTC or
  CDK document.
- **Maine AG's actual filed PDF for the CDK vendor-breach letter** (as opposed to the Massachusetts
  mirror of the same letter). The direct Maine `agviewer` page URL previously associated with this
  filing resolved to an unrelated entity (TD Bank) when re-fetched this pass — the original page ID
  may have been superseded/renumbered on Maine's site. Not re-located this pass; the Massachusetts
  mirror of the identical letter text stands in as the primary source.

---

## 5. Corrections to the first spin

Reviewed `cdk_01_platform.md`, `cdk_06_transactions.md`, `cdk_07_landscape_exit.md`, and
`cdk_08_paccar_oem.md` for anything Lane B research touches or corrects.

1. **Judge attribution was already correctly caveated.** `cdk_07_landscape_exit.md` and this task's
   own brief do not misattribute the PI opinion to Judge Conley — the brief's own bracketed note
   already flagged Judge Peterson as the correct author. No correction needed there.

2. **`cdk_01_platform.md` line 94 mislabels a URL.** It cites
   `https://www.govinfo.gov/content/pkg/USCOURTS-ilnd-1_18-cv-00868/pdf/USCOURTS-ilnd-1_18-cv-00868-2.pdf`
   as the source for "Authenticom sues CDK and Reynolds" (May 1, 2017) — but that URL is actually
   the **July 14, 2017 PI opinion** (Dkt #172), not the original complaint. This Lane B pass
   independently downloaded and confirmed that exact PDF is the PI opinion (see item #2 in §1). The
   original complaint itself was never captured as a clean file in either spin — only as a search
   snippet from a now-404 foureyes.io URL. First spin's line 94 should be corrected to describe that
   URL as the PI opinion, and the complaint-filing citation should be flagged `[UNK]` for a working
   primary-source URL.

3. **`cdk_01_platform.md` line 96 and `cdk_07_landscape_exit.md` cite a foureyes.io URL for the
   Seventh Circuit opinion** (`https://www.lit-antitrust.aoshearman.com/siteFiles/19756/...` — note
   this is actually a different mirror domain than foureyes.io, aoshearman.com, and it was not
   independently re-verified this pass either). This Lane B pass confirms the opinion's holdings via
   Findlaw/Justia/Casetext (all live, all cited in §3), which are more reliable long-term citations
   than either mirror. Recommend citing Findlaw/Justia going forward, not the law-firm mirror.

4. **`cdk_01_platform.md` correctly anticipated DABE/DART naming** (line 113) and this Lane B pass
   independently confirms it directly from CDK's own FAQ PDF, with the added detail that first spin
   did not have: the current tools are explicitly named **"Data Export Tool"** and **"Data
   Export/Import Tool"**, the latter's underlying legacy APIs are internally called **"PIPs"**, and
   there are exactly **5 PIP packages** (Vehicle, Accounting, Service, Customer, Parts) — this level
   of detail was not in the first spin and should be added.

5. **First spin's 3PA pricing figures ($25/$50/month, $250-$300/month, $28 base fee, $23 per data
   type, $150 EVR) remain unverified `[COMM]`-tier** by this Lane B pass — the CDK Partner Program
   Pricing Guide PDF would not open cleanly here either (see §4). First spin should downgrade its
   confidence tag on these figures if it presented them as `[DOC]`.

6. **No correction needed to first spin's antitrust timeline** (`cdk_01_platform.md` lines 89-102):
   the sequence — Authenticom suit filed 2017, PI granted July 2017, Seventh Circuit vacated Nov.
   2017, MDL 2817 consolidation 2018, Tekion suit Dec. 2024 — is consistent with everything found in
   this Lane B pass. The **$600 million aggregate settlement figure** cited in the earlier session
   summary (from a secondary dealershipguy.com source) was **not independently verified against the
   settlement approval order PDF** (`mdl2817_settlement_approval_order_2024-08-23.pdf`), which turned
   out to be purely procedural (preliminary approval) with no dollar figures in its extracted text.
   Flag that number `[COMM]` pending a primary-source total (a final approval order or fairness
   hearing filing, not retrieved this pass).

7. **Vendor-breach vs. consumer-breach conflation risk:** neither spin, on the pages reviewed, was
   found to explicitly state the distinction in §2.6 above — that the CDK vendor-breach letter
   (name/address/tax ID or SSN, ~36 individuals) and the Loginov consumer-class allegations
   (name/address/SSN/driver's license/credit card/bank details, ~15,000 dealership-scale impact) are
   two different disclosures of different scope. This distinction should be added wherever the first
   spin discusses "the CDK breach" as a single undifferentiated event.

---

## Inferences (clearly separated, per rules)

- `[INF]` The "Addendum PDF" referenced in CDK's own eStore enrollment walkthrough (§2.3) is, by
  its own description, almost certainly the single most direct sworn/vendor-published enumeration of
  exact data fields released to a given third-party integration — but it is generated per-partner
  inside a login-gated eStore session and was not found published anywhere publicly. This is an
  inference about what such a document would contain, not a finding that its contents were read.
- `[INF]` The "CDK file structure" referenced in CDK's own Data Export FAQ ("Extract tools like
  Data Export require an understanding of the CDK file structure") implies CDK Drive organizes
  exported data into named files/tables recognizable to a DBA without needing SQL access — but the
  FAQ does not name those files, and no file/table name list was found in any document in this pass.
  Do not assume specific file names from this phrase.
