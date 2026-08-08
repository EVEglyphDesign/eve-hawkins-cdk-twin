# The PACCAR Feedback Standard

## Design specification for a CDK Drive dealer-feedback plug-in

**Document** EgD-HAW-CDK-PLUG-001 · r1
**Client context** Peterbilt Atlantic (9 rooftops, Atlantic Canada) — CDK Drive Heavy Truck incumbent
**Prepared by** EVEglyph Design
**Status** Design specification. Reverse-specified from public incumbent documentation. Not a PACCAR-endorsed document.

---

## 1. Why this document exists

The prior CDK research lane established what CDK Drive holds and how to get it out. It did not
establish what a PACCAR dealer's management system is *expected to send back to the manufacturer* —
and that is the thing that determines whether a dealer's system is considered whole by the OEM.

There is no published PACCAR interface specification. There is, however, a functioning de-facto
standard, and it is legible: two vendors — **Karmak Fusion** and **Procede Excede** — hold the
majority of Kenworth and Peterbilt rooftops between them, and both publish enough about their PACCAR
integrations that the required surface can be reconstructed from their marketing, their release notes,
their versioned product posts, and PACCAR's own Decisiv-hosted dealer support portal.

This document reconstructs that surface, names the gap between it and what CDK publishes, and turns
the gap into a build specification.

**Framing note.** Everything below is derived from public sources. Nothing here asserts a data-rights
position, an ownership thesis, or a migration intent. It is an integration-parity specification and
should be handed to any third party in exactly that form.

---

## 2. The incumbent field

| Vendor | Product | PACCAR posture in public materials | Named PACCAR interfaces published |
|---|---|---|---|
| **Karmak, Inc.** (Carlinville, IL; 100% employee-owned ESOP) | **Fusion** (on-prem Windows), **Blaze** (acquired with DSI Solutions, effective 2025-09-30) | Publishes a dedicated PACCAR integration page as a sales instrument; openly references a PACCAR "OEM integration scorecard" | **13** |
| **Procede Software** (Solana Beach, CA) | **Excede** (SQL Server, on-prem + browser) | Publishes versioned point-products (v1.1 / v1.2 / v1.3) via product-update posts; open, Swagger-documented **Excede API** and a Certified Partner Program | **3 named + 3 corroborated** |
| **CDK Global** (Brookfield-owned) | **CDK Drive Heavy Truck** | Markets "80+ Heavy Truck OEM-specific integrations" as a headline with no itemised public list | **4** |

Karmak states its own scope plainly: *"Karmak's PACCAR OEM integrations support critical parts,
service, inventory, financial, and warranty workflows through seamless data exchange between PACCAR
systems and Fusion."* ([Karmak — PACCAR integration](https://www.karmak.com/integrations/paccar))

Note the five words in that sentence: **parts, service, inventory, financial, warranty**. That is the
shape of the standard. CDK's public record covers parts and warranty. It does not cover inventory
replenishment or financial reporting at all.

---

## 3. The register — what a PACCAR dealer system is expected to exchange

Fourteen interfaces. Direction is stated from the dealer's point of view. **↑** = dealer to PACCAR
(the feedback leg). **↓** = PACCAR to dealer. **⇅** = both.

| # | PACCAR system | Dir | Business object | Mechanism (where published) | Karmak | Procede | CDK |
|---|---|:--:|---|---|:--:|:--:|:--:|
| 1 | **MDI** — Managed Dealer Inventory | ⇅ | Parts sales + demand/inventory position up; calculated Stock / MKT / COF replenishment orders down | Daily electronic file. Karmak's own release notes name a **VMI daily inventory file** built by `CreateSendPaccarMDIDailyInventoryFile` in class `MgrPaccarMDI`, and a returned **COF file** | **Yes** — all order types | **Yes** — testimonial | **No** |
| 2 | **OPC** — Online Parts Counter | ⇅ | Fleet/major-account parts orders at dealer pricing; availability and supersession lookups | Procede: "a Windows application, web service, and Excede API"; CDK: "required by PACCAR and available on Fortellis" | **Yes** | **Yes** v1.1/1.2 | **Yes** |
| 3 | **PRWS** — Registration & Warranty System | ⇅ | Warranty claim drafted from the repair order; SIR sheets, campaigns and recalls returned | Claim draft from RO, real-time response, resubmission; on Fortellis for CDK | **Yes** | **Yes** v1.2 | **Yes** |
| 4 | **Financial Reporting** | ↑ | **Dealer month-end financial statements uploaded to PACCAR** | Karmak generates the statement in-system (`GLM96520 OEM Financial – PACCAR`) and transfers to the PACCAR site | **Yes** | **No** | **No** |
| 5 | **FOCUS** — PACCAR Parts CRM | ↑ | Customer and parts sales data for purchasing-pattern analysis | Automated send | **Yes** | **No** | **No** |
| 6 | **Service Gate** — PACCAR Parts Fleet Services | ⇅ | Pre-authorisation on estimates, authorisation on completed work, final invoices + PDF copies up, remittance down | Secure electronic transmission | **Yes** | **Yes** — testimonial | **No** |
| 7 | **Decisiv** — PACCAR Solutions / TruckTech+ / SmartLINQ | ⇅ | Service case ⇄ repair order: estimate in, parts pricing/availability query, line-level corrections, invoice number/date, auto-close on invoicing | System-to-system case integration. PACCAR's own support portal publishes a per-vendor feature list | **Yes** — deep | **Yes** — deep | *Thin* — 1 para |
| 8 | **Electronic Parts Invoices** | ↓ | PACCAR Parts invoices matched to PO and receipt, posted to AP | **ANSI X12 EDI 810 inbound invoice** — the only wire-format either vendor names | **Yes** | **Yes** | *Partial* — "coming soon" |
| 9 | **ePacking Slip / ASN** | ↓ | Advance ship notice; receive against split or multi-order shipments | Electronic packing slip | **Yes** | *Partial* | *Partial* |
| 10 | **Parts Orders** (Stock / Emergency) | ↑ | Dealer-generated purchase orders outside the MDI-managed flow | Export/upload | **Yes** | **Yes** | **No** |
| 11 | **Truck Order Data** — "PACCAR's B2B infrastructure" | ↓ | Chassis build data and specifications mapped into vehicle master at delivery | Retrieval from B2B infrastructure; no named platform | **Yes** | **No** | **No** |
| 12 | **PacLease RPS** — Rental Performance System | ↓ | Rental customers, units and contracts created/updated in the DMS | Event-driven | **Yes** | **No** | **No** |
| 13 | **Customer Loyalty Card** | ⇅ | Loyalty eligibility, coupon application and redemption at counter and through OPC | Price file / query form; Procede tracks redemption in a temp table with an `Expired` column | **Yes** | **Yes** v1.3 | **No** |
| 14 | **eInvoicing to PACCAR** (D/C memo automation) | ↑ | Debit/credit memos created and balanced against posted POs | EDI 810 + Excede API | *Partial* | **Yes** v1.2 | **No** |

Source basis: [Karmak's PACCAR integration page](https://www.karmak.com/integrations/paccar),
[Karmak Fusion 3.59 cumulative release notes](https://webhelp.karmak.com/ReleaseNotes/Fusion/3.59_cumulative.pdf),
[Procede's integrations catalogue](https://www.procedesoftware.com/integrations/),
[Procede's PRWS v1.2 product update](https://www.linkedin.com/posts/procede-software_procedesoftware-excededms-productupdate-activity-7402395748069548032-qWoj),
[PACCAR Parts' technology page](https://www.paccarparts.com/technology/),
[PACCAR Solutions' feature list for Karmak Fusion](https://support.paccar.decisiv.net/hc/en-us/articles/360033879154-Feature-List-for-Karmak-Fusion),
[CDK's Heavy Truck OEM newsletter](https://www2.cdkglobal.com/ht-oem) and
[Fortellis' heavy-truck launch post](https://fortellis.io/blog/meeting-unique-needs-heavy-truck-dealers).

---

## 4. The feedback leg, isolated

Strip out everything PACCAR pushes down and what remains is the actual "feedback standard" — the
seven flows that run **up** from the dealer's system to the manufacturer:

| Flow | Cadence | Grain | Financial materiality |
|---|---|---|---|
| Parts sales + demand → **MDI** | Daily | Line, by rooftop | Sets replenishment; drives obsolescence and turn |
| Month-end statements → **Financial Reporting** | Monthly | NADA-style departmental P&L and balance sheet | Determines OEM standing, floor-plan and 20-Group position |
| Customer + parts sales → **FOCUS** | Continuous | Customer × SKU | Feeds OEM-side marketing back at the dealer's own customers |
| Warranty claims → **PRWS** | Per RO | Claim, coded | Direct receivable |
| Final invoices → **Service Gate** | Per invoice | Invoice + PDF | Direct receivable, national accounts |
| RO line corrections, invoice, close → **Decisiv** | Real time | RO line | Case truth for fleet customers |
| Stock/Emergency POs → **Parts Orders** | As raised | PO | Working capital |

**The observation that matters for the build.** Six of these seven are transactional and already have
a defined counterpart. The odd one out is **Financial Reporting** — it is periodic, it is the only flow
carrying the dealership's whole financial position rather than a transaction, it is the one Karmak
singles out on its own page, and it is the one CDK has never mentioned in public. It is also the one
that maps directly onto work already built in this repository: the ledger model, the accounting-schedule
objects, and the June 2026 tie-out. If a plug-in is going to be built, that is where it starts.

---

## 5. What CDK actually publishes, and where the floor sits

Across every public CDK Heavy Truck property, the complete set of named PACCAR systems is four:
**OPC**, **PRWS**, **electronic shippers** (marked "coming soon"), and **Decisiv**. The dedicated
OEM integrations page carries a "Paccar" heading and then degrades to *"The PACCAR integration helps
dealers keep key workflows connected across systems"* — naming nothing
([CDK Heavy Truck OEM & ISV integrations](https://www.cdkglobalheavytruck.com/oem-integrations)).

The most specific CDK writing found anywhere is a 2022 Fortellis post that is four years old and framed
prospectively: *"We're hoping to launch at least five integrations this summer with two major OEMs —
PACCAR and DTNA"* ([Fortellis](https://fortellis.io/blog/meeting-unique-needs-heavy-truck-dealers)).

Three honest readings of that silence, none of which the public record can settle:

1. CDK genuinely does not have MDI, Financial Reporting, FOCUS, Service Gate, RPS or Loyalty.
2. CDK has them and does not publish at Karmak's level of detail, because Karmak uses its integration
   page as a sales weapon and CDK does not.
3. The material exists behind CDK's dealer and partner login walls.

**This is the single highest-value question to put to CDK, and it is a completely neutral one to ask.**
A dealer asking "which of these fourteen do we already have entitlement to?" is asking a support
question, not making an argument.

---

## 6. The acceptance test already exists: the PACCAR scorecard

Karmak's own FAQ confirms the grading instrument: *"PACCAR scorecard performance reflects how well a
business system aligns with OEM requirements, data standards, and operational workflows. Strong
scorecard results help dealers avoid integration gaps, reduce operational friction, and stay aligned
as PACCAR programs and expectations change."* ([Karmak](https://www.karmak.com/integrations/paccar))

PACCAR does not publish the scorecard's criteria. But its existence changes the design brief: the
plug-in is not being built against a spec document, it is being built against an **evaluation** — and
the register in §3 is the best available reconstruction of what that evaluation covers. Design to
the register, and the scorecard follows.

**Verification target.** Ask PACCAR, through the dealer's own OEM contact, for the scorecard's
dimensions and Peterbilt Atlantic's current result. This is a dealer's own performance record. It
costs nothing to request and it converts a reconstruction into a specification.

---

## 7. The standards layer — what the plug-in can actually speak

| Layer | Standard | Status for this build |
|---|---|---|
| Parts invoice | **ANSI X12 EDI 810** | Real and named by both incumbents. The only confirmed wire format in the whole register. Build to it. |
| Service vocabulary | **VMRS** (ATA Technology & Maintenance Council) | Live heavy-truck vocabulary. Karmak licensed it from TMC in March 2025 to standardise service intelligence shared with "dealers, fleets and OEMs." Adopt VMRS coding on the twin's labour and part lines. |
| Warranty coding | PACCAR's own claim schema | Campaign Code, Campaign Type, Claim Category, Repair Type, Customer Concern Code, Causal Code, Corrective Action Code, Responsibility Code, Failure Location, Causal Part, Supplier Code, SRT. Mandated by PACCAR, evidenced in its own technical bulletins. Not negotiable, and not a standard — a format. |
| Dealer↔OEM messaging | **STAR** — Standards for Technology in Automotive Retail | STAR6 XML v6.2.4 (2024) and the January 2026 Automotive Retail Domain Model, which finalised a **Parts, AP, Accounting, Payroll and HR** domain set. STAR names "Medium & Heavy-duty Trucks" as a covered segment, but **no truck-specific BOD variants were found** and no public evidence names PACCAR as a member. Use STAR as the vocabulary of the design, not as a claim of compliance. |
| Inventory replenishment | **DIF / SOF** pattern | Documented for DAF/Europe: dealer DMS generates a nightly **Dealer Inventory File**, PACCAR returns a **Suggested Order File**, dealer accepts or overrides. Consistent with — but terminologically distinct from — Karmak's North American **VMI file** and Stock/MKT/COF order types. Treat DIF/SOF as the pattern, VMI/COF as the North American names. |
| Financial statement | **No public standard found** | STAR has a Financial Statement BOD scoped to balance sheet and P&L, and NADA contributes standardised *ratio definitions* — but no universal cross-OEM dealer-statement transmission format exists. Karmak's "automatically download to PACCAR" therefore rests on a **proprietary PACCAR mechanism**, and that mechanism is the specification gap at the centre of this build. |

---

## 8. Design specification — the CDK plug-in

### 8.1 Shape

A **sidecar**, not a modification. It reads CDK Drive through entitled dealer-authorised routes
already established in this repository — the CDK Data Export Tool over SFTP/PGP, Dealer Data Exchange,
and Fortellis where an API exists — lands in the dealer's own Azure Postgres, and emits PACCAR-shaped
artefacts. It writes nothing back into CDK. It asks CDK for no new privilege beyond the dealer's
existing entitlement.

### 8.2 Lanes, in build order

**Lane F — Financial Reporting (first).** Highest value, largest published gap, and the only lane whose
input already exists in this repository. Generate the PACCAR month-end statement from the twin's own
ledger extract, tie it to the June 2026 tie-out month, and reconcile it against whatever Peterbilt
Atlantic files today. Deliverable: a statement the controller can compare line for line against the
manual one. If it matches, the twin has proven it holds the dealership's financial truth.

**Lane I — Inventory / MDI.** Reconstruct the daily outbound demand-and-position file and the inbound
order-recommendation handling, carrying the order-type distinction (Stock / MKT / COF) as a header
field on the parts-order record. Note the twin does not need to *transmit* to prove value: it needs
to show whether the recommendations the dealer accepts are the right ones. **The read-only version of
this lane is a variance report, and a variance report requires no PACCAR permission at all.**

**Lane W — Warranty / PRWS.** Already partly reachable through Fortellis. Model the full claim schema
as a first-class object so claim quality, rejection rates and days-to-payment become measurable.

**Lane S — Service case / Decisiv.** Mirror the case↔RO shape. CDK's published behaviour is one
paragraph; Karmak's and PACCAR's own portal documentation is the better specification of what the
integration is *supposed* to do, and is a fair benchmark to hold CDK's to.

**Lane R — Receivables / Service Gate + eInvoicing.** EDI 810 in, invoice and PDF out, remittance
matched. Straight cash-cycle value, and the easiest lane to quantify.

**Lane C — Customer / FOCUS + Loyalty.** Lowest priority and the one to think hardest about, because
this is the lane where the dealer's own customer and sales data flows outward to the manufacturer.
Model it; do not rush to widen it.

### 8.3 Per-lane contract

Every lane ships with the same six artefacts, no exceptions:

1. **Object model** — the records and fields, source-native widths preserved, every widening logged.
2. **Provenance** — for each field, the CDK object it came from and the extraction route used.
3. **Confidence tag** — DOCUMENTED or INFERRED, carried through to the surface.
4. **Reconciliation** — a tie-out against the dealer's existing reported figure.
5. **Variance record** — disagreements held and shown, never averaged away.
6. **Access gate** — the named entitlement, credential and approval each lane depends on, stated before build.

### 8.4 What is explicitly out of scope

Raw telematics ingestion. Write-back to CDK. Any route that requires a per-data-type third-party
access fee while a dealer-entitled export route exists. Anything that asks Peterbilt Atlantic staff
to change how they work before the value is demonstrated.

---

## 9. Engagement question set

To be put to CDK — and, where noted, to PACCAR through the dealer's own channel. Every question is
one a dealer is entitled to ask about its own systems. None of them reveals a design intent, a
data-rights position, or a comparison being run. Ask them as an existing customer improving its
own operation.

**To CDK, on entitlement (neutral, answerable, high yield):**

1. Which PACCAR integrations are included in Peterbilt Atlantic's current subscription across all
   eight billed accounts, and which are separately licensed?
2. Does CDK Drive Heavy Truck support PACCAR Managed Dealer Inventory — the daily inventory and demand
   file and the Stock / MKT / COF order types? If so, is it active on our rooftops?
3. Does CDK Drive generate the PACCAR month-end financial statement, and does it transmit it to PACCAR
   automatically or does our controller still upload it manually?
4. Does CDK support PACCAR Parts Fleet Services (Service Gate) invoice transmission and remittance
   retrieval, and the FOCUS customer/parts sales feed?
5. Which of the "80+ Heavy Truck OEM-specific integrations" are PACCAR-specific? Is there a current
   list we can be given for our own planning?
6. Is the PACCAR electronic shipper integration, described as "coming soon," now generally available?
7. Which PACCAR-related APIs are available to us on Fortellis today, and under which subscription?

**To CDK, on mechanics (still neutral — these read as an integration-hygiene review):**

8. For each active PACCAR interface: what is the transport, what is the schedule, and where do failures
   surface for our staff to see?
9. Where can our accounting team see a transmission log and a failure/retry history for OEM interfaces?
10. Which PACCAR interfaces run on EDI, which on file exchange, and which on API?
11. What is the documented behaviour when a PACCAR interface fails mid-month — is there a replay?

**To PACCAR, through the dealer's own OEM contact:**

12. What are the dimensions of the PACCAR OEM integration scorecard, and what is Peterbilt Atlantic's
    current standing?
13. Which PACCAR programs are we eligible for that our current DMS configuration does not enable?
14. Is there a PACCAR-published interface specification available to dealers, as distinct from one
    available only to DMS vendors?

**Posture.** Additive and curious throughout. Every answer improves the dealership's operation whether
or not anything else is ever built, and that is a true statement — which is what makes the posture
sustainable rather than a tactic. If CDK's answers are strong, the register in §3 becomes a validated
inventory. If they are thin, the register becomes the gap analysis. Both outcomes are useful, and
neither requires a card to be shown.

---

## 10. Open questions and verification targets

| # | Question | How to close it | Cost |
|---|---|---|---|
| 1 | Does CDK Drive have MDI and Financial Reporting at all? | CDK question 2 and 3 | Free |
| 2 | What are the PACCAR scorecard dimensions? | PACCAR question 12, through the dealer | Free |
| 3 | What is the PACCAR financial-statement file format? | Ask PACCAR; failing that, inspect what the controller uploads today | Free |
| 4 | Is the VMI daily file layout obtainable? | Karmak release notes name the routine but not the layout; ask PACCAR | Free |
| 5 | Are PRWS and OPC discoverable Fortellis catalogue entries or bundled into CDK's general Drive products? | Authenticated Fortellis directory check | Cheap |
| 6 | Post-acquisition, do Karmak Blaze rooftops carry the same 13 interfaces as Fusion? | Karmak publishes nothing yet | Cheap |
| 7 | Is PACCAR a STAR member? | No public evidence found | Cheap |
| 8 | Which of the eight CDK billed accounts carry which integration entitlements? | Requires the CDK Billing Center itemisation absent from the summary invoice | Free, but gated on access |

---

## 11. Provenance

Reconstructed from public vendor and OEM documentation on 2026-08-08. Full source-cited working papers
are held in this repository at `research/karmak_paccar.md`, `research/procede_paccar.md` and
`research/cdk_and_standards.md`. Every claim in this specification is traceable to a quoted primary
source in those files, and each is tagged there as DOCUMENTED or UNVERIFIED. Where a vendor's claim
could not be confirmed against a primary source, it is not asserted here.

No confidential Peterbilt Atlantic, CDK, Karmak, Procede or PACCAR material was used in its preparation.
