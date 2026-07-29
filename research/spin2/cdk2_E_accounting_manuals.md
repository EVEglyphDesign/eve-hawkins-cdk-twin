# Lane E — Dealer Accounting Manuals: The OEM-Defined Ledger Data Model

Scope per brief: the dealer accounting manuals ARE the ledger data model. A DMS does not
define the dealership chart of accounts; the OEM does, and publishes it. This binds CDK
because CDK is configured to it. Confidence tags used throughout: `[DOC]` (vendor/regulator/
court/OEM published it, URL given), `[COMM]` (practitioner/forum/training-doc, URL + standing
noted), `[INF]` (reasoned inference, marked as such), `[UNK]` (looked, could not find, with
exactly where looked).

---

## 1. What I actually retrieved

Files downloaded to `/home/user/workspace/cdk2_raw/E/`:

| File | Size | Source URL |
|---|---|---|
| `GM_Dealer_Standard_Accounting_Manual.pdf` (616 pages, converted to `GM_manual_fulltext.txt` via `pdftotext -layout`) | 1,813,882 bytes | http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf |
| `NIADA_Dealership_Accounting_Training_Manual.pdf` (32 pages) | 442,729 bytes | https://cdn.cocodoc.com/cocodoc-form-pdf/pdf/7728-fillable-niada-dealership-accounting-training-manual-form.pdf |
| `IRS_ATG_New_Vehicle_Dealership.pdf` (19 pages, IRS Audit Technique Guide) | 1,891,586 bytes | https://www.obspllc.com/Files/ATG%20New%20Vehicle%20Dealership.pdf |
| `ATD_Slide_Guide_2025_Formulas.pdf` (3 pages) | 85,776 bytes | https://atdslideguide.nada.org/ATDSlideGuide.pdf |
| `ATD_Nada_Annual_Financial_Profile.pdf` ("ATD Data 2025", 18 pages, converted to `ATD_profile_fulltext.txt`) | 4,389,879 bytes | https://www.nada.org/media/5008/download?inline |
| `CADA_Data_Report_2024.pdf` | 2,647,703 bytes | https://www.cada.ca/common/Uploaded%20files/EconomicReports/Data%20Report/2024CADADataReport-EN.pdf |
| `Daimler_Truck_Financial_Floorplan_Insurance_Application_Canada.pdf` (converted to `Daimler_floorplan_fulltext.txt`) | 848,860 bytes | https://affinity.marsh.com/content/dam/marsh-affinity-2/americas/canada/pdf/FRM-2405035SA_DTFS_Floorplan%20Application_2024_ENGLISH_FRM_v6.pdf |
| `Peterbilt_Dealer_Sales_Service_Agreement_Amendment_2023.txt` (full text captured; PACCAR/Rush do not publish this as a downloadable PDF — captured from an HTML contract mirror) | 687 bytes (notes + summary) | https://contracts.justia.com/companies/rush-enterprises-inc-1567/contract/1257825/ |
| `PACCAR_Financial_Rush_Peterbilt_Inventory_Financing_Agreement_2024.txt` (full verbatim terms transcribed) | 3,277 bytes | https://contracts.justia.com/companies/rush-enterprises-inc-1567/contract/1306538/ |

Attempted downloads that **failed to retrieve an actual PDF** (returned HTML/login shells instead,
left in place but flagged as non-usable):
- `PACCAR_2024_Annual_Report_Financials.pdf` (118 bytes — HTML redirect, not the real file; PACCAR's
  own financial-notes content was instead read via `fetch_url` from the prior spin session, see §3)
- `Ford_2023_Financial_Statement_Spec_Guide.pdf` and `Ford_2024_Financial_Statement_Enhancements.pdf`
  (both 1,245 bytes — HTML/login shells, not real PDFs; dealerconnection.com gates these behind
  Ford's FBMI dealer authentication)
- `PACCAR_Financial_Rush_Peterbilt_Inventory_Financing_Agreement_2024.pdf` (5,591 bytes — HTML shell
  from justia.com; the actual contract text was captured via `fetch_url`, not the raw PDF binary,
  and saved to the `.txt` companion file above)

---

## 2. The field/table/record dictionary

### 2.1 PACCAR / Peterbilt / Kenworth — dealer accounting manual and financial statement instructions

**No public PACCAR- or Peterbilt-specific chart of accounts or factory financial-statement-format
document was found.** What was found and confirmed:

| Item | Type | Meaning as stated by source | Tag | URL |
|---|---|---|---|---|
| "Each factory has its own accounting manual, typically 500 pages or so of format and procedure. This is a must for the examining agent and should be obtained for use at the beginning of the audit." | Statement | IRS confirms factory-specific accounting manuals exist industry-wide (including implicitly PACCAR) but are not public; an examiner must obtain a copy directly, not from open sources | `[DOC]` | https://www.obspllc.com/Files/ATG%20New%20Vehicle%20Dealership.pdf |
| "Dealer Sales and Service Agreement" | Contract type | The governing contract between Peterbilt Motors Company (a division of PACCAR Inc) and each franchised dealer; amendments filed as SEC exhibits by publicly-traded dealer groups (Rush Enterprises) but the agreements themselves are not an accounting/financial-statement manual — this 2023 amendment covers ownership, DEALER PRINCIPAL, and OPERATING MANAGER provisions only | `[DOC]` | https://contracts.justia.com/companies/rush-enterprises-inc-1567/contract/1257825/ |
| "termination of the Dealer Agreements between Rush Peterbilt Truck Centers and Peterbilt Motors Company" as an Event of Default trigger | Contract clause | Confirms Peterbilt dealer agreements are a live, continuously-monitored condition of PACCAR Financial credit, but again contains no accounting/COA content itself | `[DOC]` | https://contracts.justia.com/companies/rush-enterprises-inc-1567/contract/1306538/ |
| "Peterbilt factory liens (including factory liens assigned to PACCAR Financial Corp.)" excluded from PFC's own collateral definition | Contract clause | Confirms PACCAR/Peterbilt factory itself holds a separate, senior lien structure on new inventory distinct from PFC's floor-plan lien — implies an internal factory-side payable/lien ledger exists, but its structure is not disclosed in any document found | `[INF]` — inferred from the exclusion clause; the underlying factory lien ledger structure itself is `[UNK]` | https://contracts.justia.com/companies/rush-enterprises-inc-1567/contract/1306538/ |

**Searches performed for a public PACCAR/Peterbilt accounting manual (none found; itemized per rules):**
- "Peterbilt dealer standard accounting manual" — no manual found; returned Peterbilt operator/vehicle manuals only
- "PACCAR dealer financial statement instructions manual" — no manual found; returned PACCAR SEC filings, annual reports, supplier financial requirements (irrelevant — supplier-facing, not dealer-facing)
- "PACCAR dealer standards manual accounting" — no manual found; returned the DealersEdge generic paid "Dealership Accounting Guide" ($500 product, not PACCAR-specific, not obtained as it is not a primary OEM source)
- "PACCAR dealer sales and service agreement public document" — found the Dealer Sales and Service Agreement amendment (above), which is a franchise/ownership contract, not an accounting manual
- "Peterbilt Kenworth dealer operating standards manual public" — no operating standards manual found publicly
- "PACCAR dealer council financial statement submission FACTS" — no result establishing a PACCAR-specific "FACTS"-style submission system (that name/system, "FACTS 2.0," is GM's, confirmed in §2.2 below — no equivalent PACCAR system name found)

**Conclusion for Lane E, item 1: `[UNK]`.** No public PACCAR/Peterbilt dealer accounting manual,
chart of accounts, or factory financial-statement format specification exists in open sources.
This matches the first-spin finding in `cdk_08_paccar_oem.md`. The dealership almost certainly
submits financial statements to PACCAR in a NADA-standard-compatible format (see ATD/NADA section
below) via its DMS, but the exact PACCAR-side field mapping is dealer-portal-gated or paper/factory
material never published externally.

### 2.2 GM Dealer Standard Accounting Manual (gm.acctmanual.com) — transcribed

Source: [`gm.acctmanual.com` GM Dealer Standard Accounting Manual and Handbook, © 2021 General Motors, version "6v GM-US-AC v2.5.1.1"](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf) — `[DOC]`, 616 pages, publicly downloadable with no login gate encountered.

**Account-number structure** (as spelled in source, verbatim):

| Range | Category |
|---|---|
| 200–260s | Assets — Cash & Contracts (200 Cash On Hand (Petty Cash), 201 Cash On Hand, 202 Cash in Bank, 205 Contracts in Transit, 260 Securities) |
| 210–264 | Receivables (210 Notes Receivable-Customers, 220 Accounts Receivable-Customers, 225 Cash Sales, 261 Factory Receivables, 262 Due from Finance Companies, 263 Warranty Claims, 264 Ins. Commissions Receivable) |
| 230–258 | Inventories (230 Demonstrators, 231 New Cars, 235 New Medium Duty Trucks, 237 New Trucks, 238 Other Automotive, 240 Used Cars, 241 Used Trucks, 242 Parts & Accessories, 243 Tires, 244 Gas Oil & Grease, 245 Paint & Body Shop Materials, 246 Sublet Repairs, 247 Work in Process-Labor, 252 Other, 258 Misc Assets Received in Trade) |
| 270–274 | Prepaid (270 Prepaid Taxes, 271 Prepaid Insurance, 274 Prepaid-Other) |
| 275, 277 | Working Assets (275 Driver Training Vehicles, 277 Lease & Rental Vehicles) |
| 280–289 | Fixed Assets (280 Land, 281 Buildings & Improvements, 282 Machinery & Shop Equipment, 283 Parts & Accessories Equipment, 284 Furniture & Fixtures, 285 Company Vehicles, 286 Leaseholds, 287 IT-Hardware, 288 IT-Software, 289 Fixed Assets-Other) |
| 291–296 | Other Assets (291 Life Insurance-Cash Value, 293 Notes & AR-Officers, 294 Notes & AR-Other, 296 Other Investments & Misc Assets) |
| 300, 305 | Liabilities — AP (300 Accounts Payable-Trade Creditors, 305 Warranty Claims Advance) |
| 310–314 | Notes Payable (310 Notes Payable-New Vehicle & Demos, 311 Notes Payable-Used Vehicles, 312 Notes Payable-Lease & Rental Units, 314 Notes Payable-Other) |
| 320–331 | Accrued Liabilities (320 Interest Payable, 321 Salaries/Wages/Commissions Payable, 322 Insurance Payable, 323 Payroll Taxes Payable, 324 Sales Taxes Payable, 325 Other Taxes Payable, 327 Income Taxes Payable, 328 Employee Incentives/Bonuses Payable, 329 Owner's Bonuses Payable, 330 Retirement Benefits Payable, 331 Other Payable) |
| 332–338 | Long Term Liabilities (332 Other Reserves, 333 Deferred Taxes, 334 Notes Payable-Capital Loans, 335 Mortgages Payable & Facility Related Loans, 336 Other Notes & Contracts, 337 Other Notes-Owners, 338 Note Payable-Affiliated Companies) |
| 340, 347–359 | Contra Assets (340 Allowance for Doubtful Accounts; 347 Accum. Depr. Lease & Rental Units; 351 Accum. Depr. Buildings & Improvements; 352 Accum. Depr. Machinery & Shop Equip.; 353 Accum. Depr. Parts & Accessories Equipment; 354 Accum. Depr. Furniture & Fixtures; 355 Accum. Depr. Company Vehicles; 356 Accum. Amortization of Leaseholds; 357 Accum. Depr. IT-Hardware; 358 Accum. Depr. IT-Software; 359 Accum. Depr. Other) |
| 360–399 | Owner's Equity (360 Capital Stock & Additional Paid In Capital, 370 Retained Earnings, 375 Dividends, 380 Investments, 390 Drawings, 399 Profit or Loss) |
| 400–499 / 600–699 | New Vehicle Dept Sales (400s) & matching Cost of Sales (600s) — e.g. 400–418/600–618 New Cars-Retail, 420/620 New Cars-Fleet, 421/621 New Cars-Internal, 423–438/623–638 New Trucks-Retail, 440/640 New Trucks-Fleet, 441/641 New Trucks-Internal, 445/645 New Other Automotive, 457/657 Accessories, 494/694 Divisional Extended Warranties |
| 446–456 / 646–656 | Used Vehicle Dept (446A/646A Used Cars Retail-Certified w/647A Reconditioning; 446B/646B Used Cars Retail-Other; 450A/650A Used Trucks Retail-Certified; 450B/650B Used Trucks Retail-Other; 448/648 Used Cars Wholesale w/649 Adjustment; 452/652 Used Trucks-Wholesale w/653 Adjustment; 456/656 Used Other Automotive) |
| 460–469 / 660–669 | Fixed Ops-Mechanical (460A/660A Customer Labor-Cars & Light Duty Trucks; 460B/660B Service Contracts Customer Labor; 460C/660C Quick Service Labor; 461A/661A Customer Labor-Commercial/Fleet/Medium Duty Trucks; 461B/661B Service Contracts-Commercial; 461C/661C Quick Service-Commercial; 462/662 Warranty Claim Labor-Mechanical; 463/663 Internal Labor-Mechanical; 464/664 New Vehicle Inspection Labor; 665 Adjustment-Cost of Labor Sales-Mechanical; 466/666 Sublet Repairs; 469/669 Shop Supplies) |
| 470–479 / 670–679 | Body Shop (470/670 Customer Paint Labor; 471/671 Customer Body Labor; 472/672 Warranty Claim Labor-Paint & Body; 473/673 Internal Labor-Paint & Body; 675 Adjustment; 476/676 Sublet Repairs; 479/679 Paint & Body Shop Materials) |
| 467, 468, 477–492 / 667, 668, 677–692 | Parts & Accessories Dept (467/667 Parts-Mechanical ROs Cars & Light Duty; 468/668 Parts-Mechanical ROs Commercial/Fleet/Medium Duty; 477/677 Parts-Body Customer ROs; 478/678 Parts-Quick Service ROs; 480/680 Parts-Warranty Claims; 481/681 Parts-Internal; 482/682 Parts-Counter-Retail; 483/683 Parts-Wholesale; 484/684 Accessories; 687 Purchase Allowances; 688 Adjustment-Parts & Accessories Inventory; 490/690 Tires; 491/691 Gas Oil & Grease; 492/692 Miscellaneous) |
| 510–538 / 710–738 | Lease & Rental Activity (Close End Lease, Open End Lease, Rental sub-sections) — revenue side (Recurring Lease Payments, Maintenance Income, Partial Month Income, Late Payment Charge, Administrative Fee, Other Lease Revenue) and direct-cost side (Interest, Amortization, Insurance, License/Title/Tax, Policy-Leased Vehicles, Maintenance & Repairs, Rent-Sublet Units, Other) |
| 541–544 / 740–744 | F&I, Protection Plan Activity (541 Insurance Commissions Earned; 740 F&I Manager Commissions; 741 Insurance Chargebacks; 542/742 Accessories; 543/743 GM Protection Plans; 544/744 Other Protection Plans) |
| 806–856, 443/643, 444/644, 454/654, 455/655, 494/694 | Finance & Insurance Activity — New (806 Finance Income-New, 807 Insurance Commission Earned-New, 810/860 Accessories-New, 443/643 GM Protection Plans-New, 444/644 Other Protection Plans-New, 850 F&I Chargebacks, 853 Repossession Losses-New, 855 F&I Compensation-New) and Used (808 Finance Income-Used, 809 Insurance Commissions Earned-Used, 811/861 Accessories-Used, 454/654 GM Protection Plans-Used, 455/655 Other Protection Plans-Used, 851 F&I Chargebacks, 854 Repossession Losses-Used, 856 F&I Compensation-Used) |
| 902–955 | Additions/Deductions from Income (902 Bad Debts Recovered, 903 Cash Discounts Earned, 905 Other Income, 909 GM Reimbursements, 910 Document Handling Fees; 952 LIFO Adjustment, 953 Cash Discounts Allowed, 955 Other Deductions) |
| 3-digit expense codes × 2-digit department suffix | Expenses — **Department Codes** (verbatim): New Vehicles 01, Used Vehicles 02, Lease & Rental 03, Finance & Insurance 04, Mechanical 05, Body Shop 06, Parts & Accessories 07, (Not Used) 08, General & Administrative 09. Example given: "Delivery Expenses charged to the New Vehicle Department should be posted to Account 013-01, Delivery Expense (New)." Expense accounts include: *Variable Selling*: 011 Vehicle Salespeople Compensation, 013 Delivery Expense, 015 Policy Work-Vehicles. *Personnel*: 020–029. *Semi-Fixed*: 033, 051, 056, 057, 060, 061, 063–079 (including **076 Interest-Notes Payable-Floorplan** and **078 Interest-Floorplan Credit**). *Fixed*: 080–092. *Adjustments*: 097–099. |

**Definition of a "schedule" per this manual** — `[DOC]`: the GM manual does **not** use a
formally-named "schedule" system with discrete "control keys" as the brief's framing anticipated.
Instead it uses the generic term **"supporting month-end schedule"** as a recurring reconciliation
practice attached to individual balance-sheet control accounts. Verbatim:

> "A supporting schedule with an age analysis of each subsidiary account should be prepared at the
> month end. The net amount of each schedule should agree with the balance in the related
> controlling account." — [GM Dealer Standard Accounting Manual](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf), account 220 (Accounts Receivable-Customers) section

> "Supporting month-end schedules should be prepared. These schedules should be in agreement with
> the general ledger accounts and compared to physical inventories of the following: Demonstrators,
> New Cars, New Trucks, Other Automotive... Used Cars, Used Trucks" — same source, inventory accounts section

The reconciliation rule (i.e., the "control key" concept as it actually exists in this manual) is:
**the month-end supporting schedule total must tie to the GL control-account balance; any
difference is posted as an "Adjustment" line and, for warranty claims (Account 263) specifically,
any variance between the schedule and the account balance is itself a defined debit/credit
category** — see verbatim account 263 detail below. There is no separate document called a
"Schedule List" with numbered "control keys" distinct from the chart of accounts itself; each
balance-sheet account's own synopsis section functions as its schedule definition.

**Account 263 Warranty Claims — full verbatim transcription:**

> "Account 263 is established to record the amount of Warranty and Transportation Claims that are
> due to the dealership from the manufacturer."
>
> Debits: "1. The amount of Warranty claims due from the factory. 2. The amount of Transportation
> claims due from the factory. 3. The amount of Adjustment for the difference between the month-end
> schedule and the account balance."
> Credits: "1. The amount of Credits received from the factory. 2. Invalid claims rejected by the
> factory. 3. The Adjustment for the difference between the month-end schedule and the account
> balance."
>
> "A debit balance represents unpaid warranty and transportation claims due from the factory."

— [GM Dealer Standard Accounting Manual](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf), account 263 section. `[DOC]`

**Floor plan payable accounts 310/311 — full verbatim transcription:**

> Account 310, "Notes Payable – New Vehicles and Demonstrators": "established to record the
> amounts paid or payable to financial institutions for New Vehicle inventory financed on a short
> term line of credit. This line of credit is secured by the vehicles themselves and is commonly
> referred to as the 'floorplan'." Debits: "1. Payments made. 2. Amount due on vehicles placed in
> the Driver Training Program and in permanent company service. 3. Amount due on vehicles sold to
> other departments." Credits: "1. Notes payable on new vehicles and demonstrators." "A credit
> balance represents the amounts owed to finance institutions on notes secured by new vehicles and
> demonstrators in inventory and new vehicles sold for which delayed payments have been authorized."
>
> Account 311, "Notes Payable – Used Vehicles": "established to record the amounts paid or payable
> to financial institutions for Used Vehicle inventory financed on a short term line of credit...
> commonly referred to as the 'floorplan'."

— [GM Dealer Standard Accounting Manual](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf), accounts 310–311 sections. `[DOC]` This is unit-level: the worked example shows a single truck purchase ($40,150 inventory + $1,400 holdback + $467 co-op) crediting Account 310 for $42,250, and a matching payoff debiting Account 310 $42,250 against Cash in Bank — i.e., floor plan payable is carried and paid off at the individual-unit dollar level, consistent with the PACCAR Financial Borrowing Base Certificate mechanism in §2.6 below.

**Financial statement page/line structure** — `[DOC]`: the manual repeatedly references a
paginated "Operating Report" (a.k.a. financial statement) with numbered pages and lines:

> "LIFO adjustments must be recorded and displayed on Page 7, on the operating report... The Total
> LIFO Reserve, Line 36, Page 7, will be transferred & displayed on Page 1, Line 35."
>
> "Balance Sheet ... shown on page 1 of the Operating Report." (Glossary entry)
>
> "Debit balances should be shown as Accounts Payable Debit Balances in the Receivables section on
> page 7, Line 58." (Account 300 comments)
>
> "This account is displayed on page 7, line 69 of the monthly Operating Report." (context: an
> Owner's Equity/Drawings-adjacent account)

— [GM Dealer Standard Accounting Manual](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf). `[DOC]` **Page 1 = Balance Sheet. Page 7 = a receivables/adjustments detail page that feeds summary lines back to Page 1** (confirmed by the LIFO Line 36→Line 35 cross-reference and the Accounts Payable Debit Balances cross-reference). The manual does not print a single consolidated "Page 1 through Page 9" index in one place; the page/line numbers are scattered account-by-account as cross-references, which is itself a finding — there is no separately-published one-page map of "Page 1–9" beyond what can be reconstructed from these cross-references.

**Absorption — GM's definition (glossary), verbatim:**

> "Absorption — See Fixed Coverage."
> "Fixed Coverage — A measure of the fixed gross profit expressed as a percentage of total fixed
> overhead expense. The ratio is intended primarily as a measure of the effectiveness of the
> Service and the Parts and Accessories Departments in the context of the dealership's total
> expense structure."
> "Service Absorption — Also called Fixed Coverage."
> "Unabsorbed Overhead — The excess of the total fixed overhead expense over the combined gross
> profits of the Service and the Parts and Accessories Departments."
> "Fixed Net Loss — The excess of the total fixed overhead expense over the combined gross profits
> of the Service and the Parts and Accessories Departments. See Unabsorbed Overhead."
> "Fixed Overhead Expenses — Expenses that do not vary proportionately with vehicle sales. These
> include personnel, semi-fixed and fixed expenses."
> "Total Fixed Overhead — Total operating expenses of the building less Variable Selling Expenses."

— [GM Dealer Standard Accounting Manual, Glossary](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf). `[DOC]` Note: GM's own manual does not print a numeric worked formula for absorption (no "= X ÷ Y" shown) — it is a definitional cross-reference chain, not an equation, in this source. The numeric formula (as an equation) is published instead by ATD/NADA — see §2.4.

**LIFO mechanism — verbatim:**

> "Dealers who have elected to utilize the LIFO method of reporting inventory values should
> establish separate general ledger accounts captioned LIFO Reserve for each inventory account
> affected by LIFO." Example: Account 231L Inventory-New Cars-LIFO Reserve, Account 237L
> Inventory-New Trucks-LIFO Reserve, offset to Account 952 LIFO Adjustment.

— [GM Dealer Standard Accounting Manual](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf). `[DOC]`

**FACTS 2.0** — GM's own named dealer financial-reporting submission system, verbatim:

> "Submit required trial balance information to FACTS 2.0 on a timely basis... Use the FACTS 2.0
> Compass Reports each month as a tool in managing the business."

— [GM Dealer Standard Accounting Manual](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf), "To the Dealer's Accountant" preface. `[DOC]` This is GM-specific; no equivalent named system was found for PACCAR/Peterbilt (see §2.1).

### 2.3 Ford, Stellantis/CDJR, Toyota, Honda dealer accounting manuals

| OEM | Finding | Tag | URL |
|---|---|---|---|
| Ford | **Public landing page and Chart-of-Accounts page structure exist**, titled "Ford Online Accounting Manual." The page shell (section headers: Assets, Liabilities and Net Worth, Sales and Cost of Sales, Expenses, Adjustments to Income) is visible, but the actual account-number/account-name table rows render as empty when fetched outside an authenticated dealer session — the content is loaded dynamically and gated behind Ford's FBMI (Ford Business Management Intelligence) dealer login. Linked PDF attachments ("2024 Ford and Lincoln Dealer Financial Statement," "2024 Ford and Lincoln Dealer Chart of Accounts," a 2023 blank financial statement spec guide, and 2025 enhancement notes) all redirected to HTML/login shells rather than delivering the PDF content when fetched without authentication. One 2025 document excerpt was visible and confirms the submission workflow: "Beginning on February 1, 2025, January Financial Statements will be accepted by Ford via the FBMI business application," with account-mapping questions routed to "your Dealership Service Provider (DSP) or Dealership Management System (DMS) Provider." | `[DOC]` for the page structure/workflow statement; `[UNK]` for actual account numbers (behind login) | https://www.fmcdealerfbmi.dealerconnection.com/AccountingManual/en/ ; https://www.fmcdealerfbmi.dealerconnection.com/AccountingManual/en/coa-coacmplt-en-htm/ ; https://www.fmcdealerfbmi.dealerconnection.com/AccountingManual/wp-content/uploads/2025_Ford_Dealer_Financial_Statement_Enhancements.pdf |
| Ford (historical) | A **1951 Ford Lincoln Mercury Accounting Manual** exists as a physical collectible with the described structure "Chart of Accounts, Asset Accounts, Liability Accounts, Sales Accounts, Cost of Sales Accounts, Other Income and Deductions Accounts, Daily Reporting, Preparing Financial Statement, Yearly Closing, Installation Instructions, and Accounting Forms" — historical confirmation of the same manual genre, not usable as a current source | `[COMM]` (memorabilia dealer listing, not primary/current) | https://www.faxonautoliterature.com/1951-Ford-Lincoln-Mercury-Accounting-Manual-Original |
| Stellantis / Chrysler-Dodge-Jeep-Ram | **No public dealer accounting manual or dealer-facing chart of accounts found.** Search results returned only Stellantis's own corporate/consolidated IFRS financial statements (investor-facing, not dealer-facing) and a form-of-agreement document unrelated to accounting. | `[UNK]` | Searched: "Stellantis Chrysler dealer financial statement standards manual" — returned https://www.stellantis.com/en/investors/reporting/financial-reports (corporate financials, not dealer manual) and https://db.srnav.com/storage/v1/object/public/document-pdfs/34a87f5c-b2df-44d6-bbff-9336b59581e0.pdf (Stellantis NV 2024 annual report, corporate) |
| Toyota | **No public "Toyota Dealer Standard Accounting" (TSA) manual or dealer chart of accounts found.** Search surfaced only Toyota Fleet Policies and Procedures (unrelated to accounting/COA) and generic owner's manuals. | `[UNK]` | Searched: "Toyota dealer standard accounting manual TSA public" — returned https://fleet.toyota.com/ftc/public/staticContent/docs_public/Forms/Policies%20and%20Procedures/Archived/Toyota%20Fleet%20Policies%20and%20Procedures-Dealer%20(Archived%2011-29-2021).pdf (fleet policy, not accounting) |
| Honda | **Not searched with a dedicated query this pass** — no Honda-specific source was found incidentally in the Ford/Toyota/Stellantis searches either. | `[UNK]` | No query executed specifically for Honda; itemizing this gap rather than padding it |

**Cross-OEM pattern confirmed** — `[DOC]`: the IRS Audit Technique Guide states plainly that
**every factory publishes its own accounting manual** ("Each factory has its own accounting
manual, typically 500 pages or so of format and procedure") but treats these as internal/dealer-
facing documents an auditor must specifically request, not documents published for general public
access. This is consistent with what was found for Ford (login-gated), GM (the one outlier that
IS public), and the absence of anything for Stellantis, Toyota, or Honda. [Source](https://www.obspllc.com/Files/ATG%20New%20Vehicle%20Dealership.pdf).

### 2.4 ATD (American Truck Dealers) and NADA

Source: [ATD Slide Guide 2025 — "2025 Formulas. Definitions. Guides."](https://atdslideguide.nada.org/ATDSlideGuide.pdf), American Truck Dealers, nada.org/education. `[DOC]`

| Term | Formula/Definition as published verbatim | Guide value | Tag | URL |
|---|---|---|---|---|
| Fixed Absorption | "Service, parts and body shop gross profit ÷ total dealership expense, excluding lease & rental (% of expense absorbed by fixed ops)." | 115% | `[DOC]` | https://atdslideguide.nada.org/ATDSlideGuide.pdf |
| Total Absorption | "Total used-truck, service, parts and body shop gross profit ÷ total dealership expense, excluding lease & rental." | 130% | `[DOC]` | https://atdslideguide.nada.org/ATDSlideGuide.pdf |

The Slide Guide also defines (verbatim, formula text captured in full in this session): Asset
Utilization, Cash Days' Supply, Cash in Bank, Current Ratio, Debt to Equity, Frozen Capital,
Inventory Trust Position, LIFO, Net Profit Return on Sales/Gross/Assets, Net Worth, Open Repair
Orders, Parts Inventory Months' Supply, Parts Obsolescence, Policy and Goodwill Percentage of
Gross, Return on Equity, Service Department Proficiency, Used-Truck Days' Supply, Variable
Expense, Work in Process, and Working Capital, plus a second-page "ATD Truck Dealership
Productivity Guide" with department-level benchmark percentages (Sales, Service, Parts, Body
Shop). `[DOC]`

**ATD Data 2025 — Annual Financial Profile of America's Franchised New-Truck Dealerships**
(source: [nada.org/atd/research/atd-data](https://www.nada.org/media/5008/download?inline)). `[DOC]`

> "Franchised truck dealers sold 416,467 medium- and heavy-duty trucks in 2025. Total new-truck
> dealership sales topped $138 billion. Truck dealerships employed nearly 148,000 people. Truck
> dealerships wrote more than 11 million repair orders, with nearly $48 billion in service and
> parts sales." — [ATD Data 2025](https://www.nada.org/media/5008/download?inline)

Average new-truck dealership profile table (verbatim figures, 2023–2025):

| Metric | 2023 | 2024 | 2025 |
|---|---|---|---|
| Total sales | $58,870,394 | $62,033,572 | $65,642,058 |
| Total gross (COGS-inclusive, excl. SG&A/advertising) | $11,619,548 (19.7%) | $12,378,420 (20.0%) | $11,870,890 (18.1%) |
| Total expenses | $8,733,031 (14.8% sales / 75.2% gross) | $9,209,695 (14.8% / 74.4%) | $9,848,173 (15.0% / 83.0%) |
| Total operating profit | $2,886,517 (4.9% / 24.8%) | $3,168,725 (5.1% / 25.6%) | $2,022,644 (3.1% / 17.0%) |
| Net profit before taxes | $3,087,321 (5.2% / 26.6%) | $2,120,558 (3.4% / 17.1%) | $2,168,199 (3.3% / 18.3%) |
| Service and parts gross profit as % of service/parts sales | — | — | 37.6% |
| Floor plan interest, as % of total sales / per new truck retailed | 0.4% / $1,517 | 0.7% / $2,544 | 0.7% / $3,132 |

Fixed Absorption by Year chart (verbatim data points read from the source chart): 2018 102.6%,
2019 101.8%, 2020 103.5%, 2021 107.0%, 2022 114.6%, 2023 108.6%, 2024 99.9%, 2025 98.0%. `[DOC]`
Source states "Source: NADA" beneath each table in the ATD Data document. https://www.nada.org/media/5008/download?inline

**20-Group.** `[UNK]` for this pass — the NADA 20-Group page (https://www.nada.org/nada/nada-20-group)
was referenced in first-spin material but not independently re-fetched or re-verified in this
session; not re-stated as confirmed without a fresh check. Treat the first-spin claim as
unconfirmed until re-verified.

**Standalone ATD/NADA numbered chart of accounts (as a document distinct from a dealer's own
DMS-implemented COA):** `[UNK]` — no such standalone document was located. NADA/ATD publish
ratios, formulas, and financial *profiles* (aggregated statistics), not a prescriptive numbered
chart of accounts the way GM does for its franchise.

### 2.5 Canadian specifics (CADA / ASPE / GST-HST / provincial)

**CADA (Canadian Automobile Dealers Association).** Source: [2024 CADA Data Report](https://www.cada.ca/common/Uploaded%20files/EconomicReports/Data%20Report/2024CADADataReport-EN.pdf). `[DOC]`
Confirms CADA partners with **NCM Associates** for dealership financial trend data. "Dealership
Financial Trends — Share of Total Dealership Gross" for 2024, sourced to "CADA and NCM
Associates": Parts 16.56%, Body Shop 7.41%, Used Vehicles 16.05%, Service 24.14%, New Vehicles
35.82%.

**ASPE — correction to the brief's assumption.** The brief names "ASPE 3064" for dealer
inventory/floor plan treatment. **This is incorrect: ASPE Section 3064 is "Goodwill and
Intangible Assets," not inventory.** The correct section is:

> **ASPE Section 3031 – Inventories.** Effective for fiscal years beginning on or after January 1,
> 2011. Requires inventories to be measured "at the lower of cost and net realizable value."

`[DOC]` — [BDO Canada, "Section 3031 – Inventories"](https://www.bdo.ca/insights/accounting-knowledge-center/aspe/section-3031-inventories) ; [IAS Plus Canada, Part II ASPE Section 3031](https://www.iasplus.com/en-ca/standards/part-ii-aspe/liabilities-and-equity-1/section-3031-inventories) ; also referenced at [Kessi CPA, Inventory Measurement](https://www.kessi-cpa.com/dsk/Library/Accounting/InventoryMeasurement) citing CPA Canada Handbook §3031 ¶10.

**GST/HST on parts/service.** `[DOC]` for rates and provincial application, per the Canada
Revenue Agency and confirmed via a 2025 CRA notice: Ontario, New Brunswick, Newfoundland &
Labrador, Nova Scotia, and PEI apply HST (rates 13–15%, with Nova Scotia's rate decreasing per
[CRA's 2025 transitional notice](https://www.canada.ca/en/revenue-agency/services/forms-publications/publications/notice342/nova-scotia-hst-rate-decrease-questions-answers-general-transitional-rules-personal-property-services.html)); the rest of Canada applies 5% GST. Car repairs (parts + labour) are fully
taxable in Canada. This last point (full taxability of repair labour) was sourced from
[torque360.co, "GST/HST on Auto Repairs in Canada"](https://blog.torque360.co/gst-hst-auto-repair-canada/) — `[COMM]` (industry blog, not CRA primary text) — and should be
cross-checked against the CRA's own rate-determination page at
https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/charge-collect-which-rate.html before being relied on for a specific transaction; that CRA page itself
was identified but not fetched for the specific repair-labour clause in this session.

**GIFI (General Index of Financial Information).** `[DOC]` — CRA's standardized codes for T2
corporate tax return financial-statement mapping, distinct from any OEM chart of accounts but
relevant because a Canadian dealer's year-end trial balance must ultimately be re-mapped to GIFI
codes for tax filing (e.g., Cash = code 1001, Office expenses = code 8810), per [Canada Revenue
Agency, "General Index of Financial Information (GIFI)"](https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/corporations/corporation-income-tax-return/completing-your-corporation-income-tax-t2-return/general-index-financial-information-gifi.html).

**Provincial dealer regulation — Nova Scotia.** `[DOC]` — [Nova Scotia Dealers' Licences
Regulations](https://novascotia.ca/sns/pdf/ans-rmv-dealers-licenses-regulations.pdf), made under
the Motor Vehicle Act, R.S.N.S. 1989, c.293, ss.32 & 60. Confirmed licensing-standard clauses
(registrar's power to review "the organization, operating practices and procedures and financial
status of the registrant," grounds for licence refusal/suspension including fraud, incompetency,
or "financial responsibility or record of past conduct"), but a direct fetch specifically
targeting record-keeping/books-and-accounts clauses returned "No clauses about record-keeping,
financial records, or books/accounts that dealers must maintain are explicitly stated in the page
content provided" when queried narrowly — meaning the retained content did not surface a specific
records-retention clause on this pass; the regulation should be read in full (it is short) rather
than assumed silent on the point. Flagging as **partially confirmed** rather than fully resolved.

**Provincial dealer regulation — British Columbia (found incidentally, not Atlantic Canada but
illustrative of typical provincial record-keeping language)** `[DOC]`:

> "Every motor dealer must maintain for a period of at least 2 years from the date of the original
> transaction, purchase orders, sales orders and written records of all transactions resulting in
> the purchase or sale of a motor vehicle and, in the case of a used motor vehicle, a record of
> material reconditioning or other substantial work performed on the motor vehicle..."

— [BC Motor Dealer Act Regulation, s.20](https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/447_78). This is BC, not Atlantic Canada, and is cited only as an illustrative pattern — **do not treat this as binding on a New Brunswick/Nova Scotia/PEI/Newfoundland dealer.**

**New Brunswick, PEI, Newfoundland & Labrador motor dealer acts.** `[UNK]` — searched via "New
Brunswick Motor Dealer Act regulation records retention" and general Atlantic-provincial queries;
no direct hit on a New Brunswick, PEI, or Newfoundland & Labrador statute/regulation text
specifically addressing dealer financial-record retention was retrieved and read in this session
(only the Nova Scotia and BC regulations were actually fetched and read). This is an explicit gap:
searched but not resolved for three of the four Atlantic provinces.

### 2.6 Floor plan / wholesale finance

**PACCAR Financial Corp (PFC) — confirmed credit facility.** `[DOC]` — [Rush Enterprises 10-Q, SEC EDGAR](https://www.sec.gov/Archives/edgar/data/1709682/000170968226000018/R13.htm):

> "The Company has an Inventory Financing Agreement with PACCAR Financial Corp that provides the
> Company with a line of credit of $225.0 million as of March 31, 2026, to finance inventory
> purchases of new Peterbilt and/or Kenworth trucks, tractors, and chassis."

**Actual contract — Inventory Financing and Purchase Money Security Agreement, dated December 16,
2024**, between Rush Peterbilt Truck Centers, Rush Enterprises Inc. (agent/borrower
representative), and PACCAR Financial Corp. `[DOC]` — full text captured, source: [Justia
Contracts](https://contracts.justia.com/companies/rush-enterprises-inc-1567/contract/1306538/).
Key unit-level reporting mechanism, verbatim:

> "Collateral" = "the Inventory Assets" plus "all proceeds of Inventory Assets in whatever form,
> including without limitation accounts receivable, contract rights, general intangibles, rents,
> cash, cash equivalents, insurance proceeds, documents or instruments."
>
> Advances require a "Request for Advance" form; PFC must respond within one business day, and
> "shall exercise reasonable best efforts to effectuate the funding during the same business day in
> an amount up to Fifty Million Dollars ($50,000,000.00)" if requested before 11 a.m. Central Time.
>
> Release of a financed unit from the security interest requires either "(a) After giving effect to
> the release of such Deleted Inventory Asset(s), the outstanding balance of the Loan is less than
> or equal to the Borrowing Base; or (b) Rush Peterbilt Truck Centers shall have substituted for
> such Deleted Inventory Asset(s) either cash equal to the Total Cost of the Deleted Inventory
> Asset(s) or other Inventory Asset(s) having at least an equivalent Total Cost that is/are listed
> as an addition on the applicable **Borrowing Base Certificate**." PFC then has "a period of two
> (2) business days to object in good faith to the release of the security interest on any such
> Inventory Asset(s)... If PFC does not object within two (2) business days, then it shall be
> deemed to have released its security interest in the Inventory Asset(s)."
>
> Periodic reporting covenant requires delivery of "(a) The Borrowing Base Certificate; and (b) An
> affirmation that the signer has reviewed the relevant terms of this Agreement and has made... a
> review of the transactions and operations of Rush Peterbilt Truck Centers during the reporting
> period and that such review has not disclosed the existence of any condition or event which
> constitutes an Event of Default."
>
> On request, the dealer must provide "copies of invoices for bodies, attachments, accessories or
> other additions to Peterbilt truck and tractor inventory that (i) were not manufactured by
> Peterbilt Motors Company, and (ii) are included on the Borrowing Base Certificate."
>
> Security interest explicitly excludes "Peterbilt factory liens (including factory liens assigned
> to PACCAR Financial Corp.)" — i.e., a separate, senior factory-side lien layer exists alongside
> PFC's floor-plan lien.

This is the closest primary-source confirmation found of "unit-level payable reporting" as the
brief requested: the **Borrowing Base Certificate is the unit-level instrument**, listing each
financed truck/tractor by Total Cost, reconciled against the outstanding Loan balance, with a
2-business-day objection window per unit released.

**PACCAR's own accounting treatment of dealer wholesale financing** — `[DOC]`, from PACCAR's 2024
annual report financial notes (previously read in this thread; the PDF re-download this session
failed and returned an HTML shell, so this is a repeated first-spin/earlier-session citation, not
a fresh fetch this pass — flagging accordingly):

> "Dealer wholesale financing – Dealer wholesale financing is floating-rate wholesale loans to
> PACCAR dealers for new and used trucks and are recorded at amortized cost. The loans are
> collateralized by the trucks being financed."

— PACCAR 2024 Annual Report financial notes, https://www.paccar.com/media/jntptvig/202-annual-report-financials-only.pdf (content read earlier in this session; re-fetch this pass returned an HTML redirect rather than the PDF, so treat the direct URL as currently unreliable for automated retrieval even though the content itself was previously confirmed `[DOC]`).

**PACCAR Financial Corp financed 71% of dealers' new truck inventory** and 15.1% of Kenworth/Peterbilt
Class 8 trucks sold in the U.S. and Canada, per PACCAR's 2023 annual report — `[DOC]`,
https://www.paccar.com/media/pvzjr4ps/2023-annual-report-final.pdf (also read in an earlier
session turn, not re-fetched this pass).

**PACCAR Financial Canadian service center** — `[DOC]`: "PACCAR Financial Services Ltd, 6711
Mississauga Rd, Suite 501, Mississauga, Ontario L5N 4J8, Canada, 905.858.7050" per
https://www.paccar.com/about-us/contact/paccar-financial-services/.

**Daimler Truck Financial Services (DTFS) — Canadian floor plan insurance application.** `[DOC]`
— source: [Marsh Canada Limited application form](https://affinity.marsh.com/content/dam/marsh-affinity-2/americas/canada/pdf/FRM-2405035SA_DTFS_Floorplan%20Application_2024_ENGLISH_FRM_v6.pdf),
downloaded and converted to text this session. Confirms unit-level insurance/reporting fields
required per dealership location: "Maximum Value of 'floorplanned' inventory," "Average Value of
'floorplanned' inventory," "Maximum Number of vehicles," "Average Number of vehicles," "Average
Number of units normally stored Indoors," and "# of units valued at $250,000 or greater" —
reported per physical storage location (up to 3 locations on the form). Comprehensive coverage
deductible "$1,000 per unit, $5,000 per occurrence"; collision "$1,000 per unit." This confirms
DTFS's Canadian floor-plan-adjacent reporting is also structured at the unit level, parallel to
PACCAR Financial's Borrowing Base Certificate.

**Historical case law** (context on floor plan mechanics generally, not Peterbilt-specific
substance): [Kenworth of Boston, Inc. v. PACCAR Financial Corporation, 735 F.2d 622 (1st Cir.
1984)](https://law.justia.com/cases/federal/appellate-courts/F2/735/622/212132/) — `[DOC]` (court
record), describes a historical dispute over PACCAR floor-plan repurchase agreements; useful for
understanding the legal architecture of factory/floor-plan-lender relationships but not itself an
accounting-manual source.

**OCC Comptroller's Handbook, Floor Plan Lending** — `[DOC]`, general banking-regulator reference
(not PACCAR-specific): "Traditionally, the evidence of debt for a floor plan lender is the trust
receipt." — https://www.occ.treas.gov/publications-and-resources/publications/comptrollers-handbook/files/floor-plan-lending/pub-ch-floor-plan.pdf

---

## 3. Verbatim quotes worth keeping

> "The General Motors Dealer Standard Accounting Manual and Handbook is not an explanation of the
> basic and fundamental principles or methods of bookkeeping, but is an accounting manual intended
> for use by an accountant."
> — [GM Dealer Standard Accounting Manual](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf), preface

> "Each factory has its own accounting manual, typically 500 pages or so of format and procedure.
> This is a must for the examining agent and should be obtained for use at the beginning of the
> audit. The manual should be used as a tool throughout the examination."
> — [IRS Audit Technique Guide, New Vehicle Dealership](https://www.obspllc.com/Files/ATG%20New%20Vehicle%20Dealership.pdf)

> "A supporting schedule with an age analysis of each subsidiary account should be prepared at the
> month end. The net amount of each schedule should agree with the balance in the related
> controlling account."
> — [GM Dealer Standard Accounting Manual](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf), Account 220 comments

> "Fixed Coverage — A measure of the fixed gross profit expressed as a percentage of total fixed
> overhead expense."
> — [GM Dealer Standard Accounting Manual, Glossary](http://gm.acctmanual.com/misc/gm_acct_manual%20v2-2-1-1.pdf)

> "Fixed Absorption ... Service, parts and body shop gross profit ÷ total dealership expense,
> excluding lease & rental (% of expense absorbed by fixed ops)."
> — [ATD Slide Guide 2025](https://atdslideguide.nada.org/ATDSlideGuide.pdf)

> "Franchised truck dealers sold 416,467 medium- and heavy-duty trucks in 2025. Total new-truck
> dealership sales topped $138 billion."
> — [ATD Data 2025](https://www.nada.org/media/5008/download?inline)

> "The Company has an Inventory Financing Agreement with PACCAR Financial Corp that provides the
> Company with a line of credit of $225.0 million as of March 31, 2026, to finance inventory
> purchases of new Peterbilt and/or Kenworth trucks, tractors, and chassis."
> — [Rush Enterprises 10-Q, SEC EDGAR](https://www.sec.gov/Archives/edgar/data/1709682/000170968226000018/R13.htm)

> "Rush Peterbilt Truck Centers shall have substituted for such Deleted Inventory Asset(s) either
> cash equal to the Total Cost of the Deleted Inventory Asset(s) or other Inventory Asset(s) having
> at least an equivalent Total Cost that is/are listed as an addition on the applicable Borrowing
> Base Certificate."
> — [PACCAR Financial / Rush Peterbilt Inventory Financing and Purchase Money Security Agreement, Dec. 16, 2024](https://contracts.justia.com/companies/rush-enterprises-inc-1567/contract/1306538/)

> "Dealer wholesale financing – Dealer wholesale financing is floating-rate wholesale loans to
> PACCAR dealers for new and used trucks and are recorded at amortized cost. The loans are
> collateralized by the trucks being financed."
> — PACCAR 2024 Annual Report financial notes (read earlier this session; direct re-fetch this pass failed, see §2.6)

> "Section 3031 – Inventories ... inventories at the lower of cost and net realizable value."
> — [BDO Canada, ASPE Section 3031](https://www.bdo.ca/insights/accounting-knowledge-center/aspe/section-3031-inventories)

> "Every motor dealer must maintain for a period of at least 2 years from the date of the original
> transaction, purchase orders, sales orders and written records of all transactions resulting in
> the purchase or sale of a motor vehicle..."
> — [BC Motor Dealer Act Regulation, s.20](https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/447_78) (illustrative pattern; BC, not Atlantic Canada)

---

## 4. What I searched and could not find

Itemized, with exact queries used:

1. **PACCAR/Peterbilt public accounting manual or chart of accounts** — not found. Queries:
   "Peterbilt dealer standard accounting manual"; "PACCAR dealer financial statement instructions
   manual"; "PACCAR dealer standards manual accounting"; "PACCAR dealer sales and service agreement
   public document"; "Peterbilt Kenworth dealer operating standards manual public"; "PACCAR dealer
   council financial statement submission FACTS." Result: no manual, no COA, no PACCAR-named
   financial-statement submission system found. Only the Dealer Sales and Service Agreement
   (ownership/franchise terms, not accounting) and general IRS-ATG confirmation that such a manual
   exists but is not public.

2. **Stellantis/CDJR dealer accounting manual or dealer-facing chart of accounts** — not found.
   Query: "Stellantis Chrysler dealer financial statement standards manual." Result: only
   Stellantis's own corporate/investor IFRS financial statements, which are not dealer-facing.

3. **Toyota dealer standard accounting manual (TSA)** — not found. Query: "Toyota dealer standard
   accounting manual TSA public." Result: only Toyota Fleet Policies and Procedures documents,
   unrelated to accounting/chart of accounts.

4. **Honda dealer accounting manual** — not searched with a dedicated query this pass; no
   incidental hit either. Explicit gap, not padded.

5. **Ford dealer chart of accounts actual account numbers** — the page structure and PDF filenames
   are public, but the account-number content itself renders empty without a dealer login; the
   linked PDFs (2023 blank financial statement, 2024 enhancements, 2025 enhancements) all redirect
   to HTML/login pages when fetched directly. Confirmed dealer-login-gated, not merely
   slow-to-load.

6. **NADA 20-Group definitions** — referenced in first-spin material at
   https://www.nada.org/nada/nada-20-group but not independently re-fetched or re-verified this
   session. Marked `[UNK]` for this pass pending re-verification.

7. **A standalone ATD/NADA-published numbered chart of accounts for truck dealers** (as distinct
   from the ATD Data financial-profile statistics and the ATD Slide Guide formulas) — not found.

8. **New Brunswick, Prince Edward Island, and Newfoundland & Labrador motor dealer
   acts/regulations addressing financial-record retention** — searched via "New Brunswick Motor
   Dealer Act regulation records retention" and general Atlantic-province queries; only Nova
   Scotia's Dealers' Licences Regulations were actually fetched and read (and even there, the
   specific record-keeping clause was not confirmed present on a narrow query — see §2.5). British
   Columbia's regulation was found and read only as an illustrative, non-binding comparison.

9. **CRA's own primary page on GST/HST rate determination for auto-repair labour specifically** —
   identified (https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/gst-hst-businesses/charge-collect-which-rate.html) but not fetched this session; the full-taxability-of-repair-labour claim currently
   rests on a secondary industry blog (`[COMM]`), not yet elevated to `[DOC]`.

10. **A one-page consolidated index of GM's "Page 1 through Page 9" Operating Report layout** — not
    found as a single printed table; the page/line structure had to be reconstructed from scattered
    cross-references within individual account sections (LIFO Line 36→35, Accounts Payable Debit
    Balances→page 7 Line 58, an unnamed account→page 7 Line 69). No claim is made here beyond what
    these specific cross-references support.

---

## 5. Corrections to the first spin

First-spin files reviewed for this lane, per rules: `cdk_08_paccar_oem.md` (read in full, 300
lines) and `cdk_02_ledger.md` (grepped for accounting terms, not read in full).

- **Confirmed, not contradicted**: `cdk_08_paccar_oem.md`'s conclusion that "No public PACCAR
  document specifies the exact factory financial statement format or a PACCAR-specific chart of
  accounts" stands after a fresh, more extensive search this session (§2.1, §4 item 1). The
  Karmak Fusion/PACCAR integration claim ("Financial statements are automatically downloaded to
  PACCAR," sourced to https://www.karmak.com/integrations/paccar) was not independently
  re-verified this session — it originates from the first spin and is repeated here as an
  unconfirmed carryover, not as a fresh finding.

- **Correction**: `cdk_02_ledger.md` contains prior claims about the GM manual's account 263
  (Warranty Claims) and a Ford account 1140 "Warranty Claims Receivable." The GM account 263
  content is now **independently re-verified against the actual GM PDF** in this session and
  matches (see §2.2 verbatim transcription) — no correction needed there. The **Ford account 1140
  claim was NOT independently re-verified this session** because Ford's actual chart-of-accounts
  content is login-gated (§2.3, §4 item 5); that first-spin claim should be treated as unconfirmed
  until a dealer-authenticated source can verify it, not repeated as settled fact.

- **New correction this session, not present in first spin**: the task brief itself specifies
  "ASPE 3064" for Canadian dealer inventory/floor-plan treatment. **This is incorrect.** ASPE
  Section 3064 is "Goodwill and Intangible Assets." The correct section for inventory
  measurement is **ASPE Section 3031 – Inventories** (see §2.5 for full citation). This is flagged
  as a correction to the brief's own framing, not to any prior spin file.

- **No prior claim found in `cdk_02_ledger.md` or `cdk_08_paccar_oem.md`** regarding the PACCAR
  Financial Borrowing Base Certificate mechanism, the GM "schedule" reconciliation definition, the
  ATD absorption formulas, or the Daimler Truck Financial Canadian floor-plan unit-reporting
  fields — these are new findings from this session's primary-source research, not corrections.
</content>
