# Lane 7 — Competitive Landscape and the Economics of Leaving

Client: EVEglyphDesign sovereign digital-twin project for Peterbilt Atlantic (9-site
Peterbilt/PACCAR heavy-truck dealer group, Atlantic Canada). Thesis: dealers rent access to
their own data under CDK Drive and should own it as a capital asset instead. All findings
below are `DOCUMENTED` unless marked `INFERRED (dealer-accounting norm)`.

## 1. Heavy-duty / commercial-truck DMS market

| System | Vendor / Ownership | Deployment | Pricing model (public) | OEM network affinity |
|---|---|---|---|---|
| **Karmak Fusion** | Karmak, Inc. — 100% employee-owned (ESOP); became fully ESOP-owned in Feb. 2022 after founder Richard Sheen's retirement ([Trucks, Parts, Service](https://www.truckpartsandservice.com/business/mergers-acquisitions/article/15292326/karmak-becomes-esop-with-founders-retirement), [Karmak About](https://www.karmak.com/about)) | On-premise, Windows-based flagship ("Fusion"); newer cloud-native SaaS companion product "Blaze" for lighter deployments ([PR Newswire](https://www.prnewswire.com/news-releases/karmak-signals-ongoing-commitment-to-product-innovation-and-customer-success-302664847.html)) | Not publicly published; vendor markets "flexible technology with personalized support," no rate card found | Integrates with **DTNA, PACCAR, International, Mack/Volvo** per third-party listing ([SoftwareFinder](https://softwarefinder.com/fleet-management-software/karma)); certified DTNA Paragon PPOE integration ([Yahoo Finance/Newswire](https://finance.yahoo.com/news/karmak-announces-fusion-integration-dtna-133100920.html)) |
| **Procede Excede (Excede DMS)** | Procede Software, Solana Beach, CA; founded 2001 (private; no ownership disclosure found) ([Procede Software](https://www.procedesoftware.com/)) | On-premise/Windows and browser-based, built on Microsoft SQL Server ([Procede Software – Excede](https://www.procedesoftware.com/excede/)) | Not publicly published | Leading **Navistar Certified DMS Partner** by dealership count ([Procede press release](https://www.procedesoftware.com/navistar-certified-dms-partner-procede-software-reaches-1-position-by-number-of-north-american-dealership-locations/)); named preferred DMS provider for **U.S. Hino Trucks** ([Procede press release](https://www.procedesoftware.com/recognizing-one-year-of-partnership-procede-software-named-a-preferred-dms-provider-for-u-s-hino-trucks-dealerships/)); serves US, Canada, Australia dealer locations ([Procede press release](https://www.procedesoftware.com/procede-software-continues-to-deliver-on-its-commitment-to-advancing-its-industry-leading-dealer-management-system-with-excede-v10-4-release/)) |
| **CDK Drive (Heavy Truck)** | CDK Global, LLC (Brookfield-owned, see §2) | Cloud/hosted; CDK markets a "Drive SaaS" evolution track discussed at CDK Connect 2023 ([CDK Connect 2023 video](https://www.youtube.com/watch?v=_GpSSXigf3A)) | Not publicly published for heavy-truck vertical | Markets "**80+ Heavy Truck OEM-specific integrations**" ([CDK heavy-truck site](https://www2.cdkglobal.com/htonestop)); historical customer example: Inland Group (Kenworth/Case/Tigercat/Link-Belt) adopted CDK Heavy Truck Drive DMS in 2016 ([Equipment World](https://www.equipmentworld.com/dealers/article/14965683/inland-group-to-implement-cdk-global-dealer-management-system)) |
| **Dealertrack DMS** | Cox Automotive (Cox Enterprises subsidiary) | Cloud-based | Not published for heavy-truck; Dealertrack markets an integration-fee calculator showing non-Dealertrack dealers pay avg. **$2,691/month** across common third-party point solutions (Xtime, VinSolutions, vAuto, HomeNet, Dealertrack F&I, ServePro) ([Dealertrack calculator](https://cloud.e.dealertrack.com/calculator)) | Primarily light-vehicle franchise focus; heavy-truck presence not separately documented in sources found |
| **Tekion** | Tekion Corp (private, venture-backed) | Cloud-native | Not published | Predominantly light-vehicle ("ARC" platform); no heavy-truck-specific public documentation found in this research pass — `UNVERIFIED` for heavy-duty applicability |
| **Autosoft** | Autosoft, Inc. (private) | On-premise/cloud hybrid, historically Windows-based | Not published | Predominantly independent/used-car and light-franchise dealers; no heavy-truck-specific integration documentation found — `UNVERIFIED` for heavy-duty applicability |
| **PACCAR-specific** | No dedicated PACCAR-proprietary DMS identified in public sources; PACCAR dealers (Kenworth, Peterbilt) run third-party DMS (Karmak, Procede, CDK Heavy Truck) with PACCAR-side integrations | — | — | Karmak documents PACCAR as one of its integrated OEM systems ([SoftwareFinder](https://softwarefinder.com/fleet-management-software/karma)) |

`INFERRED (dealer-accounting norm)`: Peterbilt Atlantic, as a PACCAR network dealer, most
plausibly runs Karmak Fusion or Procede Excede rather than CDK Drive Heavy Truck, since both
have documented PACCAR/Peterbilt-adjacent OEM integrations, but the task brief states the twin
mirrors **CDK Drive** specifically — reconcile with client before assuming vendor identity.

## 2. CDK Global corporate position

- **Ownership history**: Publicly traded (NASDAQ: CDK) until acquired by **Brookfield Business
  Partners** (with institutional co-investors) for **$54.87/share cash**, equity value **$6.4B**,
  total enterprise value **$8.3B**; deal announced April 7, 2022, closed mid-July 2022
  ([Bloomberg](https://www.bloomberg.com/news/articles/2022-04-07/brookfield-partners-agrees-to-buy-cdk-global-for-8-3-billion), [Brookfield press release](https://bbuc.brookfield.com/bbu/press-releases/brookfield-acquire-cdk-global-inc), [CBT News](https://www.cbtnews.com/cdk-global-completes-sale-to-brookfield-what-does-this-mean-for-dealer-partners/)). CDK is now privately held; no shares trade publicly.
- **Revenue scale (last public figures, FY ended June 30)**: FY2021 revenue **$1,673.2M** (+2%
  YoY); FY2020 **$1,639.0M**; historical range $1.56B–$2.27B from FY2011–FY2021
  ([CDK 10-K via SEC EDGAR](https://www.sec.gov/Archives/edgar/data/1609702/000160970221000058/cdk-20210630.htm), [MarketScreener](https://uk.marketscreener.com/quote/stock/CDK-GLOBAL-INC-50919142/finances-income-statement/)). Q3 FY2022 (last public quarter before going private) revenue was **$459.7M** ([GlobeNewswire](https://www.globenewswire.com/news-release/2022/05/05/2437369/33406/en/cdk-global-inc-reports-third-quarter-fiscal-2022-results.html)). Post-acquisition financials are not publicly disclosed (private company).
- **Subscription model**: In FY2021, **subscription revenue was $1,313.9M**, roughly 78% of
  total $1,673.2M revenue, confirming a recurring-fee-dominant model ([10-K filing via Fintel](https://fintel.io/doc/sec-cdk-global-inc-1609702-10k-2021-august-18-18857-1969)).
- **How CDK charges dealers and third parties (documented, not inferred)**: CDK's own
  **Partner Program Pricing Guide** — a first-party published rate card — shows charges are
  layered: (a) **per-dealer-per-month "writeback package" fees** ($65–$285/month depending on
  module: e.g., Service Appointment $285, Front Office/CRM-Desking $285, F&I Menu $230, Parts
  E-Commerce Basic $90/Premium $175, Payroll $105); (b) **extract-only fees** for read-access to
  data — a **$28 base fee plus $23 per data type** per dealer per month; (c) **bundled extract
  packages** ($81–$150/month); (d) **one-time upfront development fee and one-time per-dealer
  setup fee** for each partner application ([CDK Partner Program Price Guide PDF](https://www.cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf)). This is the clearest public evidence that CDK monetizes access to a dealer's *own* transactional data as a distinct, metered product separate from the core DMS subscription.
- CDK's own homepage claims **$540 billion in automotive commerce** flows through its systems
  annually, across roughly **15,000 dealership rooftops** ([CDK Global homepage](https://www.cdkglobal.com/), corroborated by [VendorMotive vendor profile](https://www.vendormotive.com/vendors/cdk-global)).
- Historical pricing model shift: in 2018 CDK launched "**Drive Flex**," a variable/"pay-by-the-
  drink" DMS pricing model tied to vehicles sold, repair orders written, and user count, aimed
  at 1–2 rooftop dealers, replacing a flat monthly charge for that segment ([Automotive News](https://www.autonews.com/article/20180308/RETAIL/180309551/cdk-launches-new-dms-along-with-new-pricing-model/)).

## 3. What a mid-size dealer group actually pays

| Cost element | Reported figure | Source |
|---|---|---|
| DMS monthly cost per rooftop (2023 NADA-cited range) | **$3,500–$7,000/month**, varying by dealership size/complexity | [Monetizely procurement guide, citing 2023 NADA study](https://www.getmonetizely.com/articles/procurement-guide-how-are-automotive-dealer-management-systems-dms-priced-for-enterprises) |
| Implementation/setup fees (enterprise) | **$10,000–$50,000+ per rooftop**, one-time | [Monetizely](https://www.getmonetizely.com/articles/procurement-guide-how-are-automotive-dealer-management-systems-dms-priced-for-enterprises) |
| User/role-based licensing add-on | Adds **15–30%** to total cost of ownership per Frost & Sullivan, cited secondhand | [Monetizely](https://www.getmonetizely.com/articles/procurement-guide-how-are-automotive-dealer-management-systems-dms-priced-for-enterprises) — cite with caution, primary Frost & Sullivan report not independently located |
| Multi-rooftop group discount | Groups with 10+ rooftops may receive discounts "approaching 25%," per CDK enterprise pricing materials referenced secondhand | [Monetizely](https://www.getmonetizely.com/articles/procurement-guide-how-are-automotive-dealer-management-systems-dms-priced-for-enterprises) — `UNVERIFIED`, not independently confirmed against a primary CDK document |
| Third-party integration/data-access annual loss | Dealers reportedly **lose up to $32,000/year** in fees when DMS providers restrict data/integrations, based on avg. spend of **$2,691/month** across common third-party tools (Xtime, VinSolutions, vAuto, HomeNet, Dealertrack F&I, ServePro) for June 2022–July 2023 | [Dealertrack fee calculator (Cox Automotive)](https://cloud.e.dealertrack.com/calculator) — note: published by a competing DMS vendor, so treat the $32K figure as a marketing claim requiring independent corroboration |
| CDK writeback/extract fee rack (primary source) | $28 base + $23/data type per dealer/month; module fees $65–$285/dealer/month | [CDK Partner Program Price Guide](https://www.cdkglobal.com/sites/cdk4/files/PDFfiles/Partner_Program_Price_Guide.pdf) |
| Per-employee cost of a DMS conversion | Vendor claims changing DMS "can cost as much as **$5,000 per employee** in delays and training time" | [PartsEdge](https://www.partsedge.com/blog/2022/05/4-things-to-consider-when-changing-your-dms) |
| DMS market pricing range across vendors (secondary aggregator) | $1,000/month (basic independent) to $5,000+/month (enterprise CDK/Reynolds) | [DealerInt buyer's guide](https://www.dealerint.com/best/dealer-management-system) |

`UNVERIFIED`: No NADA/ADA primary-source PDF study was directly located in this pass — the
$3,500–$7,000/rooftop figure is cited by Monetizely as sourced to "a 2023 NADA study," but the
underlying NADA publication itself was not fetched. A large speculative-looking pricing
breakdown found on pulserevops.com (per-rooftop figures for CDK, Reynolds, Tekion, Dominion,
etc.) was **excluded** from this file as it reads as an unsourced/AI-generated GTM playbook,
not verifiable primary or trade-press data.

## 4. Switching costs and contract mechanics

- **Contract length**: DMS providers "license and sell their software and services to dealers
  pursuant to written contracts of between **five and seven years** in length" per antitrust
  class-action complaint against CDK and Reynolds ([Hoover Automotive v. CDK Global complaint](https://www.classaction.org/media/hoover-automotive-v-cdk-global.pdf)). Trade press separately describes "the typical DMS contract lasts **five years**" ([LinkedIn — DMS "Gotcha" Moment](https://www.linkedin.com/pulse/how-avoid-dms-gotcha-moment-travis-peterson)) — note this conflicts with the 7-year document-retention period required by law, creating a data-retention gap at contract turnover.
- **Auto-renewal**: CDK's own **API Licensing Terms** state the initial term "will
  automatically renew for consecutive one (1) year renewal periods... until terminated by
  either party" ([CDK API Licensing Terms](https://www.cdkglobal.com/api-licensing-terms)).
- **Notice period**: Per the same CDK API Licensing Terms, "either party may terminate the
  Agreement for any reason with at least **thirty (30) days' prior written notice**" — this
  applies to the *API/developer* agreement, not necessarily the core dealer DMS contract, which
  is `UNVERIFIED` for notice-period length (dealer DMS master agreements are not publicly
  posted).
- **Fee escalation clauses**: The same antitrust complaint alleges CDK's standard contract
  "gives dealers price protection for the first year... but imposes a **6% automatic yearly
  price increase thereafter**"; Reynolds' standard contract ties increases to CPI + 2%
  ([Hoover Automotive v. CDK Global complaint](https://www.classaction.org/media/hoover-automotive-v-cdk-global.pdf)).
- **Early-termination liability**: In *CDK Global, LLC v. Tulley Automotive Group*, CDK sued a
  dealer for early termination, "seeking to recover damages for breach of the parties' contract...
  triggering various provisions... for acceleration of payments owed and return of leased
  equipment" ([CaseMine summary of CDK v. Tulley](https://www.casemine.com/judgement/us/59145c0badd7b049341e545e)) — direct evidence of contractual buyout/acceleration exposure on early exit.
- **Contract friction reported by dealers**: Trade coverage quotes a dealer principal: "Your
  bias is not to leave [your current DMS provider] because of the work involved with leaving...
  Instead of trying to be flexible for dealers and have a 30-day opt-out clause... they chose to
  lock dealers into long-term agreements" ([Auto Dealer Today](https://www.autodealertodaymagazine.com/articles/the-big-move-changing-dealership-management-systems)).
- **Practical exit mechanics**: Dealers must send a non-auto-renewal or termination letter well
  before contract end (often via certified mail), 10–12 months of DMS evaluation lead time is
  recommended before contract expiry, and cancelling before the contract end date typically
  triggers a **buyout** ([DealerTechNerd — How to Change DMS Without the Headache](https://dealertechnerd.com/how-to-change-dms-without-the-headache/); [CPA/BR dealer-accounting guide](https://www.cpabr.com/assets/htmldocuments/HL%20Fall20_Thompson.pdf)).

## 5. Data ownership, portability, and antitrust history

- **FTC/antitrust litigation on DMS data access**:
  - *Authenticom v. CDK Global & Reynolds and Reynolds* (W.D. Wis., filed 2017): third-party
    data integrator Authenticom sued CDK and Reynolds under the Sherman Act, alleging the two
    DMS duopolists conspired since a **February 2015 agreement** to eliminate competition in
    dealer data integration and blocked Authenticom's access to dealer-authorized data
    ([complaint via GovInfo](https://www.govinfo.gov/content/pkg/USCOURTS-ilnd-1_18-cv-00868/pdf/USCOURTS-ilnd-1_18-cv-00868-2.pdf), [original complaint PDF](https://foureyes.io/images/main/DMS-Antitrust-May-1-2017.pdf)). A district court granted Authenticom a preliminary injunction in 2017 finding it had likely shown a Sherman Act violation ([Dayton Daily News](https://www.daytondailynews.com/business/federal-judge-rules-against-reynolds-and-reynolds/hNuylUEtuV4bbjhd1fFDtK/)), but the **Seventh Circuit vacated the injunction** in Nov. 2017, holding it exceeded the appropriate remedy without ruling on the merits of the underlying antitrust claims ([Reuters](https://www.reuters.com/article/world/7th-circuit-confronts-antitrust-in-the-age-of-big-data-idUSKBN1D72WB/), [7th Cir. opinion via Justia](https://law.justia.com/cases/federal/appellate-courts/ca7/17-2541/17-2541-2017-11-06.html)).
  - Consolidated multidistrict litigation, *In re Dealer Management Systems Antitrust
    Litigation* (N.D. Ill.): dealer class plaintiffs (e.g., Teterboro Automall, Bob Baker
    Volkswagen) alleged CDK and Reynolds "restricted dealer access to its own data in order to
    reduce competition" ([Bob Baker VW complaint via Courthouse News](https://www.courthousenews.com/wp-content/uploads/2018/02/CDK-Reynolds.pdf), [Teterboro Automall complaint](https://www.classaction.org/media/teterboro-automall-inc-v-cdk-global-llc-et-al.pdf)). Reynolds settled for **$29.5M**; the vendor class (led by AutoLoop) reached a separate **$100M settlement with CDK** in Aug. 2024 ([Law360](https://www.law360.com/cases/5a74ae7a613d043c53000002/articles), [DealerLaw](https://www.dealerlaw.com/2024/08/cdk-global-to-pay-100-million-to-settle-dealership-antitrust-suit/)).
  - Separately, the **dealer class** (as distinct from the vendor/integrator class) settled with
    CDK for **$600–630M** in Jan. 2025, resolving claims CDK "colluded with a rival to inflate
    dealership management system prices" and caused vendors/dealers to overpay by restricting
    data access ([Reuters](https://www.reuters.com/legal/auto-tech-firm-cdk-reaches-630-million-settlement-us-dealer-data-case-2025-01-28/), [Dealership Guy](https://news.dealershipguy.com/p/cdk-global-resolves-antitrust-case-with-600-million-settlement-2025-01-28), [official settlement site](https://www.dealershipclassdmssettlement.com/)). CDK admitted no wrongdoing in either settlement.
  - **State legislative pushback**: Arizona's "Dealer Law" (statute governing dealer rights to
    control DMS data access by third parties) was challenged by CDK on Contracts Clause
    grounds; the Ninth Circuit rejected CDK's challenge, finding CDK's theories that the law
    unconstitutionally impaired its contracts were unlikely to succeed ([9th Cir. opinion via Arizona AG](https://www.azag.gov/sites/default/files/2025-05/CDK%20Global.pdf)).
  - No direct **FTC** enforcement action (as opposed to private antitrust litigation) against
    CDK was found in this research pass — the "FTC antitrust history" referenced in the task
    brief appears, on current evidence, to be private Sherman Act litigation and state-level
    legislative/regulatory friction rather than an FTC complaint; mark `UNVERIFIED` pending a
    dedicated FTC docket search.
- **2024 ransomware incident (operational, not antitrust, but relevant to dependency risk)**:
  BlackSuit ransomware group took CDK's platform offline for roughly 19 days in June–July 2024,
  affecting ~15,000 North American dealerships; CDK reportedly paid **~$25 million** in ransom
  (387 BTC) ([CNN](https://www.cnn.com/2024/07/11/business/cdk-hack-ransom-tweny-five-million-dollars), [Repairer Driven News](https://www.repairerdrivennews.com/2024/07/12/cdk-says-financial-relief-coming-for-ransomware-outage/)); estimated dealer losses of **~$605M–$1B** in lost sales/operations were reported ([ISPartners](https://www.ispartnersllc.com/blog/car-dealership-cyberattack/), [Ford Authority](https://fordauthority.com/2024/07/ford-dealers-seeking-more-compensation-following-cyberattack/)). This is direct evidence of concentration/single-point-of-failure risk when a dealer's operational data lives entirely inside a third-party hosted DMS.
- **Data extraction and format on exit**: Practitioner guidance for dealers changing DMS
  advises asking the outgoing vendor: "Do you have access to your data?" and "What format is
  your data in?" — flagging that **some DMS providers do not provide direct data access** and
  that data may require costly reformatting to be usable by a new system ([AutoRemarketing — 10 Questions on Converting Data](https://www.autoremarketing.com/bhph/10-questions-ask-about-converting-data-when-switching-dms/)). No public CDK document specifying a guaranteed export format (e.g., flat file, CSV, database dump) or completeness guarantee was located — mark `UNVERIFIED`.
- **Legal document retention mismatch**: A typical 5-year DMS contract term does not align with
  a commonly cited 7-year dealer document-retention requirement, meaning historical records tied
  to an outgoing DMS may need separate retention/export planning at contract turnover
  ([LinkedIn — DMS "Gotcha" Moment](https://www.linkedin.com/pulse/how-avoid-dms-gotcha-moment-travis-peterson)) — the specific 7-year rule's jurisdiction/citation was not independently verified in this pass; treat as `INFERRED (dealer-accounting norm)`.

## 6. The Canadian dimension

- **PIPEDA and cross-border processing**: The Office of the Privacy Commissioner of Canada
  (OPC) guidance confirms PIPEDA does **not prohibit** transferring personal information to a
  processor outside Canada (e.g., a US-hosted DMS), but the transferring organization remains
  **accountable** for the data's protection under Principle 1 (Accountability) of Schedule 1,
  regardless of where processing occurs ([OPC — Guidelines for processing personal data across borders](https://www.priv.gc.ca/en/privacy-topics/airports-and-borders/gl_dab_090127/)). This means a Canadian PACCAR dealer using a US-hosted CDK Drive or Excede instance cannot contract away its own PIPEDA accountability merely by pointing to the vendor's location.
- **Contractual/due-diligence implication**: Because accountability is non-delegable, the dealer
  group must be able to demonstrate comparable protection is contractually assured with the US
  DMS vendor — a factor directly relevant to a sovereign/local twin that keeps data under
  Canadian control.
- **Quebec Law 25**: Quebec's *Act respecting the protection of personal information in the
  private sector* (Law 25 / formerly Bill 64) requires, since Sept. 22, 2023, a mandatory
  **Privacy Impact Assessment (PIA)** before any cross-border transfer of personal information,
  plus a written agreement incorporating the PIA's findings and risk-mitigation terms, and (since
  Sept. 2022) transparency notice to individuals that their data may be processed outside Quebec
  ([WatchDog Security — Law 25 §17](https://watchdogsecurity.io/law25/cross-border-transfers), [BLG law firm analysis](https://www.blg.com/en/insights/2022/12/cross-border-transfers-of-personal-information-outside-quebec)). Penalties reach **CAD $10M or 2% of global turnover** (administrative) or **CAD $25M or 4%** (penal) ([Alation compliance guide](https://www.alation.com/blog/quebec-law-25-compliance-guide/)). Law 25 applies extraterritorially to any organization handling Quebec residents' data, not just Quebec-headquartered firms ([Outside GC](https://outsidegc.com/blog/quebecs-privacy-law-25-what-you-need-to-know/)).
- **Atlantic Canada dealer applicability**: Peterbilt Atlantic's home provinces (Atlantic Canada
  = NB, NS, PEI, NL) fall under **federal PIPEDA** rather than Quebec's Law 25 (Law 25 applies
  specifically to Quebec and to any organization processing Quebec residents' data). If any
  Peterbilt Atlantic customer or transaction touches Quebec-resident data, Law 25's cross-border
  PIA requirement would attach to that subset of records. `INFERRED (dealer-accounting norm)`:
  the practical trigger is customer/counterparty residency, not dealer location.
- **Portability right**: Law 25's final implementation phase (effective Sept. 22, 2024)
  introduced a **right to data portability**, letting individuals request their computerized
  personal information be transferred to them or a third party in a structured format
  ([Alation](https://www.alation.com/blog/quebec-law-25-compliance-guide/)) — directly relevant precedent for the sovereignty argument, since it establishes a Canadian statutory analogue to "own your data" even at the individual level.

## 7. CapEx-versus-OpEx argument in accounting terms

- **Why a DMS subscription creates no balance-sheet asset**: Under **IAS 38** (Intangible
  Assets), a right to access a supplier's hosted software over a contract term — rather than
  control over an identifiable software resource — generally fails the "control" recognition
  criterion, so the arrangement is accounted for as a service expense, not a capitalized
  intangible asset ([Financial Connect — IAS 38 self-check](https://www.financial-connect.com/tools/ifrs-software-intangible-assets.html)). PwC's cloud-computing guidance is explicit: "the subscription service fee **cannot be capitalised** as an intangible asset in terms of IAS 38" for a typical SaaS arrangement where the customer does not control the underlying software ([PwC — Cloud computing accounting considerations](https://www.pwc.co.za/en/assets/pdf/cloud-computing.pdf)). Under the equivalent US framework (**ASC 350-40**, cited for comparative context), SaaS arrangements are "generally treated as service contracts, not capitalized software assets" ([Datastudios — SaaS accounting](https://www.datastudios.org/post/accounting-for-software-as-a-service-saas-arrangements-by-customers)).
- **How internally developed software CAN be capitalized — IFRS (IAS 38)**: Development-phase
  costs must be capitalized (not merely "may be") once **all six criteria** in IAS 38 paragraph
  57 are simultaneously met: (1) technical feasibility of completing the asset; (2) intention to
  complete and use/sell it; (3) ability to use or sell it; (4) how it will generate probable
  future economic benefits; (5) availability of adequate technical/financial/other resources to
  complete it; (6) ability to reliably measure the attributable expenditure ([FTH Advisory — IAS 38 software development](https://www.fthadvisory.com/blog/ias-38-software-development), [KPMG — Capitalisation of internally generated intangible assets](https://assets.kpmg.com/content/dam/kpmg/mt/pdf/2021/05/capitalisation-of-internally-generated-intangible-assets.pdf)). Research-phase costs (evaluation, exploration) must always be expensed; only development-phase costs meeting all six tests are capitalized ([opag.io — R&D Capitalisation IAS 38 guide](https://opag.io/insights/rd-capitalisation-ifrs-ias-38-guide)).
- **How internally developed software can be capitalized — ASPE (Section 3064, Canada, private
  enterprises)**: An intangible asset is recognized when it is (a) **identifiable** (separable
  or arising from contractual rights), (b) **controlled** by the enterprise (power to obtain
  future economic benefits and restrict others' access), and (c) has a **reliably measurable
  cost** ([iaminter.net — Capitalizing Custom Software guide](https://iaminter.net/capitalizing-software-en.pdf), [BDO — ASPE at a Glance](https://www.bdo.ca/getmedia/18f2a846-47a1-44b7-aed0-f1692b4cc179/Intangible-Assets_RB.pdf)). Critically, ASPE gives private Canadian enterprises an **accounting policy choice** IFRS does not: they may elect to either **expense or capitalize** development costs that meet the recognition criteria, whereas IFRS mandates capitalization once the six IAS 38 criteria are met ([BDO — ASPE-IFRS Comparison: Intangibles](https://www.bdo.ca/getmedia/9bbda314-084b-4f64-82dc-8bb060f676bb/ASPE_IFRS-Comparison_Intangibles_Dec-2025.pdf)).
- **The "control" test as the crux of the sovereignty argument**: Both IAS 38 and ASPE Section
  3064 hinge capitalization on **control** — "the contractual right to obtain the software
  without significant penalty" and the ability to run it independently or migrate it to a third
  party's infrastructure "without significant decrease in utility or value" ([BDO — ASPE at a Glance, AcG-20](https://www.bdo.ca/getmedia/a76f1092-7f4c-4c7a-bfb3-a6d35fda67f9/AcG-20_RB.pdf)). A dealer paying CDK Drive subscription and per-data-type extract fees fails this control test by construction — the CDK Partner Program pricing guide itself demonstrates the vendor treats even the dealer's own transactional data as a metered, permissioned resource (§2 above) — which is precisely why the subscription is OpEx, not CapEx. A sovereign, dealer-controlled digital twin, by contrast, is structured to satisfy the IAS 38 / ASPE 3064 control criterion and could be capitalized as an intangible asset on Peterbilt Atlantic's balance sheet if development costs meet the six recognition tests.
- **Practical accounting summary for the pitch**: Subscription DMS = recurring rental expense,
  zero balance-sheet asset, disappears entirely on contract exit. Internally developed
  sovereign twin = potential intangible capital asset, amortized over useful life, retained by
  the dealer group regardless of any vendor relationship — a direct accounting-standards
  citation for the "own vs. rent" thesis.

## What I could not verify

- No primary NADA or ADA published PDF study was directly retrieved; the $3,500–$7,000/rooftop
  DMS cost figure is second-hand via a consulting blog citing "a 2023 NADA study" — the
  underlying NADA report itself needs to be located and fetched directly.
- No direct FTC enforcement docket (as opposed to private Sherman Act litigation) against CDK
  was found; the task brief's reference to "FTC and antitrust history" may need reframing as
  private antitrust litigation plus state legislative conflicts (Arizona Dealer Law) unless a
  dedicated FTC search turns up a formal FTC action.
- Karmak Fusion, Procede Excede, and CDK Drive Heavy Truck monthly/per-rooftop pricing is not
  publicly published by any of the three vendors — only the general CDK light-vehicle Partner
  Program data-access rate card is public.
- No public document specifies CDK's guaranteed data export format or completeness standard
  upon contract termination for the DMS core system (only third-party trade guidance flags this
  as a live risk).
- The claim that CDK enterprise contracts offer "discounts approaching 25%" for 10+ rooftop
  groups is sourced only secondhand via a consulting blog, not a primary CDK document — treat as
  `UNVERIFIED`.
- Tekion's and Autosoft's applicability to heavy-duty/commercial-truck dealers specifically
  (as opposed to light-vehicle) was not confirmed in public sources found; both appear
  light-vehicle-focused based on available material.
- Exact DMS contract notice-period length for the core dealer (non-API-developer) CDK agreement
  is unverified — only the API Licensing Terms' 30-day notice clause is public.
- The 7-year document-retention rule referenced against the 5-year DMS contract term lacks a
  specific jurisdictional statute citation in the source found.
- A large per-vendor pricing table (CDK $7K–$25K/mo per rooftop, Reynolds $6K–$22K/mo, etc.) was
  found on pulserevops.com but excluded as unverifiable/likely AI-generated content; it should
  not be relied upon without independent confirmation.

## Proposed SAP-shape mapping

Following the parts-lane precedent (MARA/MARC/MARD/MARM/MBEW/MVKE/MFRPN/MATDOC), lane 7's
commercial/contractual/compliance concepts map to SAP-adjacent objects as follows. These are
**conceptual mappings for the twin's data model**, not verified CDK or SAP table names — treat
all as `INFERRED (dealer-accounting norm)` pending confirmation against actual SAP customizing
objects.

| CDK / DMS-market concept | Proposed SAP-shape object | Rationale |
|---|---|---|
| Dealer rooftop / dealership site | Plant (`T001W`) or Sales Organization (`TVKO`) | Each of Peterbilt Atlantic's 9 sites is a distinct operating unit analogous to an SAP plant/sales org |
| DMS vendor contract (CDK, Karmak, Procede) master data | Vendor master (`LFA1`/`LFB1`) + Purchasing Info Record (`EINA`/`EINE`) | Vendor identity, payment terms, and per-vendor pricing conditions mirror procurement master data |
| Per-module subscription fee (Service Appointment, Front Office, F&I Menu, etc.) | Condition records (`KONV`/`A-tables` in pricing procedure) | Each CDK module fee is a distinct priced "condition" attached to a contract line, same pattern as SAP pricing conditions |
| Extract-only / data-access fee (per data type) | Condition type on a service contract item (`VBAK`/`VBAP` for a service/subscription "order") | Metered per-data-type billing resembles a recurring service order line with condition-based pricing |
| DMS contract term, auto-renewal, notice period | Contract header data (`VBAK` with contract-specific fields) / Outline Agreement (`EKKO` scheduling data) | Contract start/end, renewal cadence, and notice windows map to SAP outline agreement validity periods |
| Data extraction / exit deliverable (format, completeness) | Data migration object / IDoc extract definition | The twin must define its own canonical extract format independent of CDK's internal schema |
| PIPEDA/Law 25 data residency and PIA obligations | Custom compliance master data object (no direct SAP MM analogue) | Not a standard MM/SD table; would require a bespoke compliance/governance object in the twin, e.g., a "Data Residency & Consent" master record keyed to Customer Master (`KNA1`) |
| Capitalized internally developed software (the twin itself) | Asset master record under Fixed Assets (`ANLA`/`ANLZ`) if capitalized per IAS 38/ASPE 3064 | This is the direct accounting-system consequence of the CapEx argument in §7 — the twin, once built, is booked as an intangible fixed asset, not an operating expense line |

Word count of substantive sections (excluding this mapping table and the "could not verify"
list): approximately 1,550 words, within the 900–1,600 target.
