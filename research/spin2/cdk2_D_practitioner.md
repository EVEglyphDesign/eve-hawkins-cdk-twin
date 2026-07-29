# CDK second spin — Lane D: Practitioner and training material

Client: EVEglyphDesign digital twin for Peterbilt Atlantic (nine rooftops, Atlantic Canada, heavy
truck, PACCAR/Peterbilt franchise, CDK Drive + Lightspeed). Reader: parts and service director,
and a systems architect who spent thirty years in enterprise integration.

Scope discipline per `/home/user/workspace/cdk2_rules.md`: this is a primary-source retrieval
exercise. Every claim below is tagged `[DOC]` / `[COMM]` / `[INF]` / `[UNK]`. Nothing here is
invented; where a name could not be verified it is marked `[UNK]` and the search is itemised.

---

## 1. What I actually retrieved

**yt-dlp attempts — failed, documented explicitly:**

The brief instructed `yt-dlp --write-auto-sub --skip-download --sub-format vtt` against CDK Drive
training videos. This was attempted in-sandbox against two video IDs (`FKAZDyqSZ38`,
`kf_iaL47qpc`). Both attempts failed with YouTube's bot-detection error, *"Sign in to confirm
you're not a bot."* No `.vtt` file was produced by yt-dlp for any video. This is recorded as a
tool limitation, not suppressed — see `/home/user/workspace/cdk2_raw/D/README.md`.

As a substitute, the web-search tool's own transcript/caption extraction returned substantial
timestamped transcript fragments (`{ts:N}` markers, taken from YouTube's own caption track) for
several videos. This is not a yt-dlp download, but it is the same underlying caption data,
fetched from the same public YouTube page. Video IDs where transcript text was obtained this way:

| Video ID | Title | Channel | Date | URL |
|---|---|---|---|---|
| `FKAZDyqSZ38` | How to make an appointment in CDK DMS | Dan's VW channel | 2020-09-18 | https://www.youtube.com/watch?v=FKAZDyqSZ38 |
| `tIHjc7F5aWg` | Making a repair order in CDK for a drive-in customer that is in the system | Dan's VW channel | 2020-09-18 | https://www.youtube.com/watch?v=tIHjc7F5aWg |
| `H9Le0PvLbi4` | CDK Global Heavy Truck Success Stories – Jackson Group Peterbilt | CDK Global | 2023-06-26 | https://www.youtube.com/watch?v=H9Le0PvLbi4 |
| `kf_iaL47qpc` | CDK How-To: CDK Scheduler Quick Guide for Service Advisors & BDC Agents | CDK Global | 2025-09-10 | https://www.youtube.com/watch?v=kf_iaL47qpc |
| `-RF8nUtGGjo` | Fixed Ops Innovations for Smarter Scheduling and Parts Efficiency (CDK CONNECT session) | CDK Global | 2025-12-23 | https://www.youtube.com/watch?v=-RF8nUtGGjo |
| `DeBkzct6-vo` | CDK How-To: Scheduler New Workflow | CDK Global | — | https://www.youtube.com/watch?v=DeBkzct6-vo |
| `j4kzCJv42q0` | CDK How-To: New Service Dashboard Features | CDK Global | — | https://www.youtube.com/watch?v=j4kzCJv42q0 |
| `UaTpTpWef-w` | CDK Fixed Operations Suite - Forward Focused Webinar | CDK Global | — | https://www.youtube.com/watch?v=UaTpTpWef-w |
| `_5uQppzAW20` | Unlocking Innovation With Fortellis: CDK CONNECT 2025 | CDK Global | — | https://www.youtube.com/watch?v=_5uQppzAW20 |
| `czyOfweYgoM` | CDK CONNECT 2023: Independent Software Vendors | CDK Global | 2023 | https://www.youtube.com/watch?v=czyOfweYgoM |
| `8yY-43Wb4HA` | CDK CONNECT 2023: Dealership Operations | CDK Global | 2023 | https://www.youtube.com/watch?v=8yY-43Wb4HA |
| `OT_C-pUxX14` | CDK Dealership Tutorial \|\| CDK Automotive Dealership Software | third-party | 2025-10-04 | https://www.youtube.com/watch?v=OT_C-pUxX14 |

Vimeo: searched directly (`Vimeo CDK Drive DMS training video`) — no CDK Drive training content
located on Vimeo. `[UNK]` — see §4.

**Pages fetched and read in full (not just snippet):**

- DealersEdge Dealership Accounting Guide (glossary/index) — https://www.dealersedge.com/accountingguide
- Total Dealer Solutions Zendesk, "CDK Transaction Codes" — https://totaldealersolutions.zendesk.com/hc/en-us/articles/360060331572-CDK-Transaction-Codes
- Total Dealer Solutions Zendesk, "CDK Partial Quantities Sold on RO/Invoice" — https://totaldealersolutions.zendesk.com/hc/en-us/articles/15121824426900-CDK-Partial-Quantities-Sold-on-RO-Invoice
- Total Dealer Solutions Zendesk, "Rules for Automatic PO Matching" — https://totaldealersolutions.zendesk.com/hc/en-us/articles/360026931512-Rules-for-Automatic-PO-Matching
- PartsEdge blog, "Navigating CDK's MSDA Setting Update" — https://www.partsedge.com/blog/2018/08/navigating-cdks-msda-setting-update
- CDK Global "Automotive Dealer" ABM eBook (PDF) — https://www.cdkglobal.com/sites/cdk4/files/2022-01/21-1300%20ABM%20eBook%20Rebrand_v2.pdf
- Corpay/nvpsupport Zendesk, "Viewing CDK Usernames for Creating User Accounts in AP Assist 2.0" — https://nvpsupport.zendesk.com/hc/en-us/articles/27280103073677-Viewing-CDK-Usernames-for-Creating-User-Accounts-in-AP-Assist-2-0
- Nimble Compensation, "Dealer Connected Commissions – DMS Integrations" — https://www.nimblecompensation.com/how-we-help/dms-integrations
- DealersEdge Substack, "Exploring Daily Operating Control" — https://dealersedge.substack.com/p/exploring-daily-operating-control-102
- CDK Global blog, "4 CRM Reports [That] Boost Efficiency and Oversight" — https://www.cdkglobal.com/insights/4-crm-reports-boost-efficiency-and-oversight
- DealerRefresh forum, "Community Review: CDK Global" — https://forum.dealerrefresh.com/threads/community-review-cdk-global.11705/
- DealSpeak AI blog, "Onboarding Dealership Staff on CDK Drive in 2026" — https://www.dealspeak.ai/blog/cdk-dms-training
- DealersEdge Professional Forums thread — https://forums.dealersedge.com/viewtopic.php?f=3&t=10736
- Reddit r/MechanicAdvice, "Anyone have a cheat sheet for CDK?" — https://www.reddit.com/r/MechanicAdvice/comments/1aqostf/anyone_have_a_cheat_sheet_for_cdk/
- Reddit r/serviceadvisors, "New to CDK..." — https://www.reddit.com/r/serviceadvisors/comments/1gh4z7b/new_to_cdk/
- Reddit r/serviceadvisors, "I once shared a CDK cheat sheet, knew everything..." — https://www.reddit.com/r/serviceadvisors/comments/1ijx7cf/i_once_shared_a_cdk_cheat_sheet_knew_everything/
- Reddit r/sysadmin, "CDK Global DMS print management" — https://www.reddit.com/r/sysadmin/comments/1ja1hpc/cdk_global_dms_print_management/
- Reddit r/partscounter thread — https://www.reddit.com/r/partscounter/comments/1s6l0f0/
- Fortellis developer community — https://community.fortellis.io/
- automotivemcp.ai directory entry for CDK Drive Op Codes API — https://automotivemcp.ai/directory/cdk-global-fortellis
- Vaia/Analytic Search Group job posting, "CDK DMS Systems Lead & Data Reporting" — https://talents.vaia.com/companies/analytic-search-group-princeton-nj/little-falls/cdk-dms-systems-lead-data-reporting-117214603/
- LinkedIn profile, Jumaane Driver (CDK Global Client Implementation Manager, prior Controller) — https://www.linkedin.com/in/jumaane-driver-2806b024

No spec, schema, or PDF exhibit beyond the CDK ABM eBook PDF was found downloadable in this lane;
the ABM eBook is the one PDF artefact retrieved. It is a marketing eBook, not a technical spec —
noted plainly.

---

## 2. Field / screen / report / code dictionary

### 2a. Screen and function-code catalogue (legacy command-line / "green-screen" layer)

This layer is the one the first-spin lanes (which focused on the Fortellis REST API) did not
capture at all. Practitioners describe CDK Drive's operational front end as a keyboard-command,
DOS-style interface layered under (or alongside) the modern browser UI ("CDK Service" /
"CDK Drive"). Table rows below are function/command codes as spelled by named posters, tagged
`[COMM]`.

| Code / screen as spelled | Meaning as stated | Tag | Source |
|---|---|---|---|
| SDL | "your main screen that you will work from"; also stated elsewhere as "Summary of jobs" / service daily log; used to check pending repair orders | `[COMM]` | Reddit r/MechanicAdvice (poster, thread title "Anyone have a cheat sheet for CDK?") — https://www.reddit.com/r/MechanicAdvice/comments/1aqostf/anyone_have_a_cheat_sheet_for_cdk/ ; Reddit r/serviceadvisors, Federal-Effect-8201 — https://www.reddit.com/r/serviceadvisors/comments/1gh4z7b/new_to_cdk/ |
| DS | "display subtotal" | `[COMM]` | r/MechanicAdvice, as above |
| FNL | "finish line" | `[COMM]` | r/MechanicAdvice, as above |
| ASL | "add sublet" | `[COMM]` | r/MechanicAdvice, as above |
| CSA | "change sell amount" | `[COMM]` | r/MechanicAdvice, as above |
| FC | "Final close" | `[COMM]` | r/MechanicAdvice, as above |
| DTO | "display total with tax" | `[COMM]` | r/MechanicAdvice, as above |
| VEH | "to add vehicle"; elsewhere: "denotes vehicle information" | `[COMM]` | r/MechanicAdvice, as above; Federal-Effect-8201, r/serviceadvisors |
| TK | "launch time-clock app" — service advisors say this legacy function is being phased out in favor of the RO dashboard | `[COMM]` | r/MechanicAdvice, as above; ScienceRules195, r/serviceadvisors, "I once shared a CDK cheat sheet" — https://www.reddit.com/r/serviceadvisors/comments/1ijx7cf/i_once_shared_a_cdk_cheat_sheet_knew_everything/ |
| SA + tech# | "clock in/tech sign-in" | `[COMM]` | r/MechanicAdvice, as above |
| L + tech# | "locate next job" | `[COMM]` | r/MechanicAdvice, as above |
| PREQ + tech# | "send parts request" | `[COMM]` | r/MechanicAdvice, as above |
| H | "hold line" | `[COMM]` | r/MechanicAdvice, as above |
| O | "un-hold line" | `[COMM]` | r/MechanicAdvice, as above |
| SC + tech# | "sign out" | `[COMM]` | r/MechanicAdvice, as above |
| SB + tech# | "break" | `[COMM]` | r/MechanicAdvice, as above |
| SBO + tech# | "off break" | `[COMM]` | r/MechanicAdvice, as above |
| D + line# | "expand line description" | `[COMM]` | r/MechanicAdvice, as above |
| LRO + tech# | "show job stack" | `[COMM]` | r/MechanicAdvice, as above |
| FLAG + tech# | "show clocked time" | `[COMM]` | r/MechanicAdvice, as above |
| HIST | "vehicle history" | `[COMM]` | r/MechanicAdvice, as above |
| RO + work order# | "go to RO" | `[COMM]` | r/MechanicAdvice, as above |
| T + tag# | "go to RO" (by tag number) | `[COMM]` | r/MechanicAdvice, as above |
| G + tech# | "assign self to RO" | `[COMM]` | r/MechanicAdvice, as above |
| W + line letter (A,B,C) | "work on line" | `[COMM]` | r/MechanicAdvice, as above |
| F | "finish line" | `[COMM]` | r/MechanicAdvice, as above |
| PFC | posting/pricing/editing/finalizing/printing screen; "type `?` on command line for options"; "`GO CAS`" is a shortcut to the CAS app from PFC | `[COMM]` | r/MechanicAdvice, as above; multiple posters, r/serviceadvisors "New to CDK" |
| SAC | "represents appointments" | `[COMM]` | Federal-Effect-8201, r/serviceadvisors "New to CDK" |
| SWR | "used for modifications"; "adding services, editing descriptions, and incorporating technologies" | `[COMM]` | Federal-Effect-8201; Sufficient-Phone-237, both r/serviceadvisors "New to CDK" |
| CUST | "refers to customer data" | `[COMM]` | Federal-Effect-8201, as above |
| SPI | "checking parts for inventory or orders" | `[COMM]` | Federal-Effect-8201, as above |
| DSP | "relates to dispatching work" | `[COMM]` | Federal-Effect-8201, as above |
| PRO | "for adding parts" | `[COMM]` | Sufficient-Phone-237, r/serviceadvisors "New to CDK" |
| CAS | cashiering screen; used with PFC to close/cashier tickets | `[COMM]` | duster74gold, r/serviceadvisors "I once shared a CDK cheat sheet" |
| RAP | "how I track my sales" (report/tool referenced by name, no further detail given) | `[COMM]` | Deadlight44, r/serviceadvisors "New to CDK" |
| DSDA | "quick access to DSDA, allowing me to easily retrieve invoices" — Data Storage and Data Archiving | `[COMM]` | OptoSmash (self-identified as ex-Freightliner, heavy truck), r/serviceadvisors "New to CDK"; corroborated independently by a CDK job posting, "Data Analyst / Programmer (DSDA) - BPC" — https://www.dice.com/job-detail/d6231410-ab2d-4545-9347-83c1e4307e66 |
| CPC, ECM, TCM | referenced as flash/module types kept accessible via RO for "quickly creating tickets related to CPC, ECM, and TCM flashes" | `[COMM]` | OptoSmash, r/serviceadvisors "New to CDK" |
| UUP | "the dealership administrator within CDK needs to execute the UUP function and modify the form queue settings" | `[COMM]` | OrbitalAlpaca, r/sysadmin "CDK Global DMS print management" — https://www.reddit.com/r/sysadmin/comments/1ja1hpc/cdk_global_dms_print_management/ |
| F7 (in user profile) | "press F7 while in the user profile to update the 'laser formq' to reflect the new printer" | `[COMM]` | OrbitalAlpaca, as above |
| DA/RO/A | legacy DMS command sequence that "CDK Service has existed since around 2012" to substitute for | `[COMM]` | SheWantsTheDan, r/serviceadvisors "I once shared a CDK cheat sheet" |
| CSPO | named alongside PFC/SDL/DSP as a screen still in use under CDK Service | `[COMM]` | SheWantsTheDan, as above |
| SF7 | alternative to F5 for "adding or modifying lines" | `[COMM]` | KingofthenortMTWF, r/serviceadvisors "New to CDK" |
| ADM | screen/menu used to create a "new appointment" | `[COMM]` | transcript, "How to make an appointment in CDK DMS," https://www.youtube.com/watch?v=FKAZDyqSZ38 |
| APPT | function typed at the appointment log to flag a customer who has "not been here before" (new customer intake path) | `[COMM]` | same transcript, `FKAZDyqSZ38` |
| S | keyboard command to save and create the appointment ("hit S to save and it creates the appointment") | `[COMM]` | same transcript, `FKAZDyqSZ38` |

Menu path stated verbatim in the same training video: *"this will open the service appointment
log which is sac service daily log sdl and post final charges which is pfc"* — i.e. the desktop
quick-launch groups **SAC** (appointment log), **SDL** (service daily log) and **PFC** (post final
charges) together as the three screens a service advisor opens first (`[COMM]`, `FKAZDyqSZ38`).

### 2b. CDK Drive/legacy transaction codes — parts module (Total Dealer Solutions)

Source: Total Dealer Solutions Zendesk, "CDK Transaction Codes" —
https://totaldealersolutions.zendesk.com/hc/en-us/articles/360060331572-CDK-Transaction-Codes.
Tag `[COMM]` (third-party CDK integrator/support-documentation site, not CDK itself; treated as
practitioner-tier, not vendor-tier, since it is not published by CDK Global).

| Program (screen) as spelled | Code | Meaning as stated |
|---|---|---|
| RA (Adjust and Receipt) | R | Receipt or arrived order |
| RA (Adjust and Receipt) | R | Manual receipt |
| RA (Adjust and Receipt) | E | Emergency receipt |
| RA (Adjust and Receipt) | O | Other receipt |
| RA (Adjust and Receipt) | ADD | Add a new part |
| RA (Adjust and Receipt) | CAN | Cancel order |
| RA (Adjust and Receipt) | B | Backorder of N, T, or blank type order |
| RA (Adjust and Receipt) | I | Increase or add order |
| PO (Post Orders) | I | Increase or add order |
| PO (Post Orders) | D | Decrease order |
| PO (Post Orders) | CAN | Cancel order |
| PO (Post Orders) | T | Transfer order |
| PO (Post Orders) | B | Backorder of N, T, or blank type order |
| PO (Post Orders) | X | Backorder of S type order |
| PO (Post Orders) | K | Backorder of C type order |
| PO (Post Orders) | ADD | Add a new part |
| PS (Post Sales) | (blank) | Normal sale or return sale |
| PS (Post Sales) | N | No-history sale or return sale (does not affect sales demand history) |
| PS (Post Sales) | W | Warranty sale or return sale (part sale/return on an RO Warranty Pay labor line) |
| PS (Post Sales) | NW | No-history warranty or return sale |
| PS (Post Sales) | H | Wholesale sale or return sale (defined by entering H transaction code) |
| PS (Post Sales) | NH | No-history wholesale or return sale |
| PS (Post Sales) | L | Lost sale ("true" lost sale, not lost sale due to price) |
| PS (Post Sales) | M | Minus adjustment |
| PS (Post Sales) | P | Plus adjustment |
| PS (Post Sales) | ADD | Add a new part |
| PS (Post Sales) | DC | Dirty core on-hand increased or decreased |
| PRO (Parts Charges on Repair Orders) | (blank) | Normal sale, return sale, void sale, or canceled sale |
| PRO | N | No-history sale or return sale |
| PRO | DS | Drop shipment or defective return |
| PRO | W | Warranty sale or return sale (part sale/return on an RO Warranty Pay labor line) |
| PRO | NW | No-history warranty or return sale |
| PRO | DW | Warranty drop shipment or defective return |
| PRO | H | Wholesale sale or return sale (defined by the customer's W wholesale customer code set up in OCCU) |
| PRO | NH | No-history wholesale or return sale |
| PRO | DH | Wholesale drop shipment or defective return |
| PRO | L | Lost sale |
| PRO | ADD | Add a new part |
| PRO | DC | Dirty core on-hand increased or decreased |
| NP (new part, Part Maintenance, Add option) | ADD | Add part |
| DP (delete part, PM, Change option) | DEL | Delete part |
| MT (master tape — price changes) | — | "Price changes indicating appreciation/depreciations — comes from manufactures [sic]" |
| PM (Parts Master Update) | $ | Cost added to non-costed part |
| PM (Parts Master Update) | $+ | Cost increased |
| PM (Parts Master Update) | $- | Cost decreased |
| ST or STK (IRE Finalize option or STK) | I | Add new order |
| ES (excess stock in MSR) | Q | Excess stock returned |
| PN (Part Number Change) | PNC | On-hand quantity transferred from old part number to new part number |
| PN (Part Number Change) | UPN | PNC changes to new part number undone |
| PN (Part Number Change) | UPO | PNC changes to old part number undone |

Note: `OCCU` is named inline as the screen where a customer's wholesale (`W`) code is set up
(`[COMM]`, same source). `IRE` and `MSR` are named inline as source screens for `ST/STK` and `ES`
respectively but not otherwise defined by the source — carried through verbatim, not expanded.

### 2c. Parts inventory fields (PartsEdge blog)

Source: https://www.partsedge.com/blog/2018/08/navigating-cdks-msda-setting-update — tag `[COMM]`
(PartsEdge is a third-party parts-inventory consulting firm, not CDK).

| Field/setting as spelled | Meaning as stated |
|---|---|
| MSDA | Name of the CDK setting update discussed ("MSDA setting") — exact expansion not given by the source |
| MNR | Months No Receipt |
| MNS | Months No Sale |
| RESET: MNS WHEN PART WITH 0 ON HAND IS RECEIPTED (Y/N)? | Verbatim on-screen prompt text |
| MGR | Referenced field/code name — not expanded by the source beyond the bare acronym |

Report names in the same source: **Inventory Movement - Sales** report, **Monthly Summary
Report**, **Annual Activity and Benchmark Report** — all `[COMM]`, same URL.

### 2d. Report catalogue

| Report name as spelled | Vendor/DMS | What it shows (as stated) | Tag | Source |
|---|---|---|---|---|
| MGR Parts Report | CDK | Listed in a dealership-accounting glossary index (pages 25, 45, 47); no description text captured beyond the index entry | `[COMM]` | DealersEdge Accounting Guide glossary — https://www.dealersedge.com/accountingguide |
| REX Exceptions Report | CDK | Listed in the same glossary index (pages 47, 59, 136) | `[COMM]` | same |
| ROV Exceptions Report | CDK | Listed in the same glossary index (pages 47, 59, 136) | `[COMM]` | same |
| 2213 Parts Inventory Report | Reynolds & Reynolds (explicitly tagged "(R&R)" in the source, **not CDK**) | Listed in glossary index | `[COMM]` | same — kept here only to show the source's own R&R vs. CDK tagging discipline |
| 2542 Exception Report | Reynolds & Reynolds ("(R&R)") | Listed in glossary index | `[COMM]` | same |
| 3619 Exception Report | Reynolds & Reynolds ("(R&R)") | Listed in glossary index | `[COMM]` | same |
| Report By Employee (RBE) | CDK Drive (light auto) and CDK Heavy Truck — identical list on both pages | Listed under Service/Parts/Sales/F&I/Management/Accounting department headings | `[COMM]` | Nimble Compensation, "Dealer Connected Commissions – DMS Integrations" — https://www.nimblecompensation.com/how-we-help/dms-integrations |
| Advisor Daily Sales Summary | CDK Drive / CDK Heavy Truck | Same list, same source | `[COMM]` | same; independently named again by a named practitioner: "we can see it from the side bar when you click report and analyze and go to advisor daily sales summary" — Independent-Wait-390, r/serviceadvisors "New to CDK" |
| Tech Performance Report | CDK Drive / CDK Heavy Truck | Same list, same source | `[COMM]` | Nimble Compensation, as above |
| RTH Reports | CDK Drive / CDK Heavy Truck | Named, no further description given | `[COMM]` | Nimble Compensation, as above |
| Master Daily DOC | CDK Drive / CDK Heavy Truck | Named in vendor-comparison list; separately, CDK's own blog describes it as "also known as the traffic management report" — see §3 quotes | `[COMM]`/`[DOC]` (cross-confirmed) | Nimble Compensation, as above; CDK Global blog, https://www.cdkglobal.com/insights/4-crm-reports-boost-efficiency-and-oversight |
| PDA Report | CDK Drive / CDK Heavy Truck | Named, no further description given | `[COMM]` | Nimble Compensation, as above |

**Discrepancy flagged, not resolved:** DealersEdge's Substack names CDK's DOC-equivalent report
differently from CDK's own blog — see verbatim quotes in §3. Both are kept, tagged separately, and
the conflict is stated rather than silently resolved.

### 2e. CDK ABM eBook (PDF) — exception/report categories by department

Source: CDK Global, "Automotive Dealer" ABM eBook (PDF), https://www.cdkglobal.com/sites/cdk4/files/2022-01/21-1300%20ABM%20eBook%20Rebrand_v2.pdf
— tag `[DOC]` (CDK-published PDF). This is a sales/marketing eBook aimed at DMS buyers, not a
technical manual, and is labeled as such.

| Department | Report / exception category as spelled | Threshold stated |
|---|---|---|
| Sales | Used inventory > 120 days | > 120 days |
| Sales | Booked but not posted deals (not in general ledger and not on financial statement) | none stated |
| Parts | Special-order request (SOR) for parts sitting on shelf > 25 days | > 25 days |
| Parts | Overrides made by counter personnel | none stated |
| Parts | SORs received but waiting on customer pickup | none stated |
| Parts | Warranty parts tracking | none stated |
| Service | Internal repair orders (ROs) > 5 days | > 5 days |
| Service | ROs closed but not picked up | none stated |
| Service | Appointments that were no-shows | none stated |
| Service | Overrides made by counter personnel | none stated |
| Accounting | Contracts in transit (CIT) > 5 days | > 5 days |
| Accounting | Service policy > $5,000.00 | > $5,000.00 |
| Financial statements | Exception reports — deals, names, schedule and key accounts, parts and service | none stated |
| Financial statements | "A financial statement that can be viewed, printed, downloaded and drilled into for immediate account details" | n/a |

This is generic DMS-buyer messaging, not confirmed as naming specific CDK Drive screens — it is
kept as `[DOC]` for "CDK Global published this exception taxonomy," and explicitly not upgraded to
a screen-name claim.

### 2f. Fortellis developer-community names (cross-reference to Lane B/C territory, kept minimal here)

| Name as spelled | Type | Tag | Source |
|---|---|---|---|
| CDK Drive Repair Order (v1→v2 migration) | API product name | `[COMM]` | Fortellis community — https://community.fortellis.io/ |
| CDK Drive Workshop Management | API product name | `[COMM]` | same |
| CDK Drive Customers | API product name | `[COMM]` | same |
| CDK Drive Service Vehicle | API product name | `[COMM]` | same |
| CDKDrive OpCodes v1 | API product name, confirmed as a real, distinct read-only API | `[COMM]` | automotivemcp.ai directory — https://automotivemcp.ai/directory/cdk-global-fortellis |
| Vehicle Specifications API | API product name | `[COMM]` | Fortellis community, as above |
| ConnectCDK | Credential set used to sign into the Fortellis Dealer Portal | `[COMM]` | Fortellis community, as above |

Endpoint path change documented on the forum: v1 `https://api.fortellis.io/cdkdrive/service/v1/repair-orders/`
→ v2 `https://api.fortellis.io/service/cdk-drive/v2/repair-orders/` (`[COMM]`, Fortellis community).

### 2g. Job-posting and resume evidence

| Source | What it names | Tag | URL |
|---|---|---|---|
| Vaia/Analytic Search Group, "CDK DMS Systems Lead & Data Reporting" (Little Falls, NJ, posted 2026-05-25) | Names "CDK Drive platform" as the system administered; duties: "Build, maintain, and extract customized reports from CDK and third-party applications... Design and distribute scheduled data reports" | `[COMM]` | https://talents.vaia.com/companies/analytic-search-group-princeton-nj/little-falls/cdk-dms-systems-lead-data-reporting-117214603/ |
| ZipRecruiter, "DMS Application Manager (CDK)" | Names departmental modules: "accounting, sales, service, parts, payroll, and reporting" | `[COMM]` | (captured in prior research pass — full text on file; ZipRecruiter listing) |
| Dice.com, "Data Analyst / Programmer (DSDA) - BPC - CDK Global" | Names CDK's "DSDA platform" (Data Storage and Data Archiving) explicitly as a distinct CDK architecture component requiring "an advanced level of experience with Data Storage and Data Archiving (DSDA)"; also requires "Knowledge of Linux and PICK, SQL Server" | `[COMM]` | https://www.dice.com/job-detail/d6231410-ab2d-4545-9347-83c1e4307e66 |
| LinkedIn, Jumaane Driver — CDK Global Client Implementation Manager, prior Controller at East Brunswick Pontiac Buick GMC | Resume lists dealership-controller duties in generic ledger/reconciliation language: "Meticulous schedules and reconciliations... Payroll, accounts payable/receivable, general ledger journal entries... Reconcile and post payroll to general ledger (G/L)" — does not name specific CDK screens | `[COMM]` | https://www.linkedin.com/in/jumaane-driver-2806b024 |

**Corroboration:** the Dice.com posting's naming of "DSDA" as a CDK platform component
independently confirms the Reddit poster OptoSmash's "quick access to DSDA" claim in §2a — two
independent `[COMM]` sources naming the same acronym the same way. This is the strongest
cross-corroborated finding in this lane.

### 2h. Practitioner-training-blog evidence (DealSpeak AI)

Source: https://www.dealspeak.ai/blog/cdk-dms-training — tag `[COMM]` (third-party CDK
onboarding/consulting content publisher).

Verbatim-adjacent terms named: "opening an RO," "writing op-codes," "CDK's scheduling and dispatch
tools within the service module," parts-counter training on "OEM number," "bin locations,"
"internal versus external sale orders," and the existence of **CDK University** role-based
learning paths, described as: *"CDK Global operates CDK University, its official learning
management system for dealership staff. CDK University includes role-based learning paths, video
modules, guided simulations, and assessments."*

---

## 3. Verbatim quotes worth keeping

> "CDK is DOS base, so keyboard commands are crucial over using your mouse. CDK will not allow you
> to move forward, and the program will notify what command is needed."
— unnamed poster, r/MechanicAdvice, "Anyone have a cheat sheet for CDK?" — https://www.reddit.com/r/MechanicAdvice/comments/1aqostf/anyone_have_a_cheat_sheet_for_cdk/

> "SDL stands for summary of jobs. SAC represents appointments. SWR is used for modifications.
> CUST refers to customer data. VEH denotes vehicle information. SPI indicates checking parts for
> inventory or orders. PFC is for posting or editing. DSP relates to dispatching work."
— Federal-Effect-8201, r/serviceadvisors, "New to CDK" — https://www.reddit.com/r/serviceadvisors/comments/1gh4z7b/new_to_cdk/

> "Configure the startup profile with the following settings:, RO SWR PFC and H."
— pepsibottle1, same thread

> "when it comes to adding or modifying lines, instead of using F5, try SF7... If you're looking to
> find out which technology is being used on a vehicle, SDL is your best bet... If you have a
> booker, they can assist you with CAS and PFC."
— KingofthenortMTWF, same thread

> "SWR for adding services, editing descriptions, and incorporating technologies; PRO for adding
> parts; and PFC for adjusting prices, finalizing, and printing documents... SDL just to check which
> repair orders I still have pending."
— Sufficient-Phone-237, same thread

> "we can see it from the side bar when you click report and analyze and go to advisor daily sales
> summary"
— Independent-Wait-390, same thread

> "RAP is how I track my sales"
— Deadlight44, same thread

> "primarily utilized PFC, SWR, and VEH... We relied on the Decisive program for estimates...
> quick access to DSDA, allowing me to easily retrieve invoices... kept RO open for quickly
> creating tickets related to CPC, ECM, and TCM flashes."
— OptoSmash (self-identified as ex-Freightliner, heavy truck), same thread

> "CDK Service has existed since around 2012 and serves as a substitute for DMS commands such as
> DA/RO/A... you will still utilize commands like PFC, SDL, DSP, and CSPO."
— SheWantsTheDan, r/serviceadvisors, "I once shared a CDK cheat sheet, knew everything..." — https://www.reddit.com/r/serviceadvisors/comments/1ijx7cf/i_once_shared_a_cdk_cheat_sheet_knew_everything/

> "I follow my customer cars through the CDK Service dashboard then cashier all my tickets through
> PFC, CAS, etc."
— duster74gold, same thread

> "In the coming years, all the legacy DMS 'functions' will be phased out. This year, technicians
> will stop using TK for tracking their hours... everything will be integrated into the RO
> dashboard within CDK Service... the parts screens will undergo modifications, eliminating the
> need to switch back and forth between CDK Service and PRO."
— ScienceRules195, same thread

> "If your 7th box on the RO dash says REVIEW, then booking is currently turned off."
— ScienceRules195, same thread

> "the dealership administrator within CDK needs to execute the UUP function and modify the form
> queue settings for their printer... press F7 while in the user profile to update the 'laser
> formq' to reflect the new printer."
— OrbitalAlpaca, r/sysadmin, "CDK Global DMS print management" — https://www.reddit.com/r/sysadmin/comments/1ja1hpc/cdk_global_dms_print_management/

> "this will open the service appointment log which is sac service daily log sdl and post final
> charges which is pfc"
— transcript, "How to make an appointment in CDK DMS," https://www.youtube.com/watch?v=FKAZDyqSZ38 (Dan's VW channel, 2020-09-18)

> "all of our parts invoices our services are all run through ucdk that tracks our inventory...
> we've embraced the parts camp... a few years ago we decided to implement corepay through AP
> assist... there's consolidation modules inside of cdk that allow us to put all those financial
> statements together as one report... there are nightly Transmissions between cdk and paccar and
> Peterbilt."
— transcript, "CDK Global Heavy Truck Success Stories – Jackson Group Peterbilt," https://www.youtube.com/watch?v=H9Le0PvLbi4 (CDK Global channel, 2023-06-26). This is a named, real Peterbilt dealer group describing CDK↔PACCAR/Peterbilt nightly data transmission — directly relevant to Peterbilt Atlantic.

> "CDK calls the report: MIS – Management Information System. Dealer Track calls the report:
> Financial Analysis."
— DealersEdge Substack, "Exploring Daily Operating Control" — https://dealersedge.substack.com/p/exploring-daily-operating-control-102 (conflicts with the Nimble Compensation "Master Daily DOC" naming and with CDK's own blog quote below — kept as an open discrepancy, not resolved)

> "The Master Daily DOC (Daily Operating Control) also known as the traffic management report...
> Most DOCs can be sectioned by department or category... Front-end sales, Sales forecast, Service
> productivity and revenue, Parts revenue, Overhead expenses, Payroll."
— CDK Global blog, https://www.cdkglobal.com/insights/4-crm-reports-boost-efficiency-and-oversight (`[DOC]`)

> "RESET: MNS WHEN PART WITH 0 ON HAND IS RECEIPTED (Y/N)?"
— on-screen CDK prompt text, quoted by PartsEdge, https://www.partsedge.com/blog/2018/08/navigating-cdks-msda-setting-update

> "Log in to CDK Drive → in the MAINT account enter UUP function code → MAINT UUP page → User
> Setup Reports page → select Access to Function on Specific Acct report from Select Report
> list → Account selection list → select [LOGON ACCOUNT NAME]-A logon account (example:
> MARTOY-A) → F3 to save → Main Functions list → select AP Accounts Payable Open-Item function →
> F3 opens report on Terminal tab → output methods: Report_printer, Override (F1 for printer
> list), Excel_export (CSV/XLS)."
— paraphrased-but-exact menu path reconstructed from Corpay/nvpsupport Zendesk, "Viewing CDK
Usernames for Creating User Accounts in AP Assist 2.0" — https://nvpsupport.zendesk.com/hc/en-us/articles/27280103073677-Viewing-CDK-Usernames-for-Creating-User-Accounts-in-AP-Assist-2-0
(this is the single most complete verbatim menu path retrieved in this lane, tag `[COMM]` since
the publisher is Corpay/nvpsupport, a third-party AP-automation vendor's support site, not CDK
itself)

> "CDK Global operates CDK University, its official learning management system for dealership
> staff. CDK University includes role-based learning paths, video modules, guided simulations, and
> assessments."
— DealSpeak AI, "Onboarding Dealership Staff on CDK Drive in 2026" — https://www.dealspeak.ai/blog/cdk-dms-training

---

## 4. What I searched and could not find

- **yt-dlp transcript downloads** — attempted on two video IDs (`FKAZDyqSZ38`, `kf_iaL47qpc`) using
  `yt-dlp --write-auto-sub --skip-download --sub-format vtt`. Both blocked by YouTube's bot
  detection ("Sign in to confirm you're not a bot") in this sandbox. `[UNK]` — no local `.vtt` file
  produced. Search-tool caption extraction was used as a substitute (see §1).
- **Vimeo CDK Drive training videos** — searched directly ("Vimeo CDK Drive DMS training video").
  No CDK Drive-specific training content found on Vimeo; only Vimeo's own developer/help pages
  surfaced. `[UNK]`.
- **ADAM (dealer-controller community)** — searched directly ("ADAM automotive dealer accounting
  managers CDK forum"). No such community or forum with that acronym was located; search returned
  unrelated results. `[UNK]`.
- **Automotive Dealership Institute** — searched directly ("Automotive Dealership Institute CDK
  Drive course"). The only close match found was "Automotive Dealership Institute" branded as an
  F&I manager training school (autodealerinstitute.com) with no CDK Drive-specific screen or
  report content — it teaches F&I sales process, not DMS mechanics. `[UNK]` for CDK-specific
  content from this source.
- **r/DealershipLife** — not located as an active distinct subreddit with CDK-specific content in
  this pass; general automotive-career subreddits (r/askcarsales, r/serviceadvisors,
  r/partscounter, r/MechanicAdvice, r/sysadmin) were the productive ones instead. `[UNK]` for
  r/DealershipLife specifically.
- **DealersEdge Professional Forums thread** (https://forums.dealersedge.com/viewtopic.php?f=3&t=10736)
  — fetched; yielded a thin result: poster "AL" mentions "CDK Service Connect" and "ABCD fields" with
  no further elaboration captured. Recorded as thin, not padded.
- **CDK-specific PACCAR/Peterbilt chart-of-accounts or schedule-number document** — searched in
  this lane via the Jackson Group Peterbilt video and general search; the video confirms nightly
  CDK↔PACCAR/Peterbilt data transmission exists (`ucdk`, "consolidation modules," "nightly
  Transmissions") but does not name specific file, table, or schedule numbers. `[UNK]` for the
  underlying record/table names — this matches the same gap flagged in the first-spin ledger file
  (see §5).
- **Community-college CDK Drive courses** — no community-college-specific CDK Drive course
  syllabus was located in this pass; the only formal-education CDK tie found was CDK Ireland
  providing Autoline Drive DMS licenses to a BSc Automotive Technology and Management program
  (careersnews.ie) — a different CDK product (Autoline Drive, not CDK Drive US) and a different
  market (Ireland). Kept for completeness, tagged `[COMM]`, not treated as CDK Drive US evidence.
- **LinkedIn posts by CDK-certified consultants naming specific screens** — two LinkedIn posts by
  the CDK North America corporate account were found (https://www.linkedin.com/posts/cdknorthamerica_automotiveindustry-dealership-carsales-activity-7315123789057445888-Ad2E
  and https://www.linkedin.com/posts/cdknorthamerica_dealership-carsales-dealershipaccounting-activity-7266874045923475458-tlpb)
  but these are CDK's own corporate marketing posts, not independent consultant posts, and neither
  names a specific screen or report beyond generic hashtags. `[UNK]` for an independent
  CDK-certified consultant's screen-naming LinkedIn post.

---

## 5. Corrections to the first spin

The first-spin ledger file (`/home/user/workspace/cdk_02_ledger.md`) explicitly flags several
items as `UNVERIFIED`:

1. "CDK Drive's own internal schedule numbers (equivalent to Autosoft's GLSKEDS export or Ford's
   1140) were not located in any public CDK/Fortellis document" (line 43).
2. "No CDK Drive screen name for period-lock was found in public materials" (line 51).
3. "No CDK-specific screen name for the submission step is publicly documented" re: OEM factory
   statement transmission (line 69).
4. "A PACCAR/Peterbilt-specific dealer accounting manual or chart-of-accounts document... not
   publicly located; PACCAR's factory-statement format and account numbers are UNVERIFIED" (line
   102).
5. "CDK Drive's actual internal schedule numbers/names... not found in any public CDK document"
   (line 103).
6. "The exact CDK Drive screen/table names for posting-period lock (closed-period enforcement)...
   architecture is INFERRED from cross-DMS norms only" (line 104).

**Lane D did not resolve any of these six gaps with a primary-source screen or table name.** No
practitioner source located in this lane names a CDK schedule number, a period-lock screen, or a
PACCAR-specific chart of accounts. The first spin's `UNVERIFIED` tags stand unchanged for these
six items — this is stated plainly rather than papered over.

**What Lane D adds that the first spin did not have at all:** the first-spin ledger file's own
scope note (line 53, "Fortellis journal-entry / GL posting APIs") shows that lane focused
exclusively on the Fortellis REST API layer (`glpost`/`glwippost` endpoints). It contains **no
mention whatsoever** of the legacy command-line/function-code layer documented in §2a-§2c above
(SDL, PFC, SWR, CAS, DSP, PRO, UUP, and the parts transaction codes). This is a material gap in
the first spin's coverage, not a correction of an error — the first spin was silent on this layer,
not wrong about it. Practitioners are unambiguous that this command-driven layer is the one they
actually operate day-to-day ("CDK is DOS base, so keyboard commands are crucial over using your
mouse" — r/MechanicAdvice), and that the newer browser-based "CDK Service" front end is a
still-incomplete wrapper over it ("CDK Service has existed since around 2012 and serves as a
substitute for DMS commands... you will still utilize commands like PFC, SDL, DSP, and CSPO" —
SheWantsTheDan, r/serviceadvisors). For a digital-twin reconstruction, this command-code layer is
the stronger data-model evidence of the two, because each function code maps to a specific,
narrow, named on-screen transaction (e.g., `PS` transaction codes `W`/`NW`/`H`/`NH`/`L`/`M`/`P`/`DC`
directly describe stored sale-type flags on the parts-sale record) — this is exactly the kind of
"a screen field is a stored field" evidence the brief asked this lane to prioritize.

**Discrepancy introduced, not present in the first spin:** the first spin does not address DOC
(Daily Operating Control) naming at all. Lane D found two conflicting practitioner-tier names for
CDK's DOC-equivalent report — DealersEdge's Substack says *"CDK calls the report: MIS – Management
Information System"*, while CDK's own blog names it *"the Master Daily DOC... also known as the
traffic management report"* and the Nimble Compensation vendor-comparison page lists it simply as
"Master Daily DOC." These are not reconciled here; both are recorded with their tags and sources so
a later lane or the operator can adjudicate.

**One heavy-truck-specific finding not present in the first spin's PACCAR section:** a named,
real Peterbilt dealer group (Jackson Group Peterbilt) states on camera, in a CDK-published video,
that "there are nightly Transmissions between cdk and paccar and Peterbilt" and references
`ucdk`, "parts camp," and "corepay through AP assist" as components of their CDK-based operation.
This does not supply a table or file name, but it is a stronger primary-source anchor than
anything the first spin had for the PACCAR-integration gap (the first spin relied on PACCAR's SEC
10-K describing floor-plan financing generally, not on any dealer describing the actual CDK-PACCAR
data flow). This raises the `[UNK]` gap on PACCAR-specific record/table names to a slightly better
evidentiary state (a named real-world confirmation that the transmission exists) without closing
it.
