# The export route — dealer-initiated SFTP extraction from CDK Drive

**EVEglyphDesign · CDK Twin · operational analysis**
Last revised 2026-07-29.

This document sets out the route by which Peterbilt Atlantic can take a complete, scheduled,
encrypted copy of its own DMS record out of CDK Drive, without a Fortellis API licence, without
a third-party integrator being named on a CDK Order, and — on CDK's own published terms —
without a licence fee.

It is written as an operating runbook, not a recommendation paper. Every factual claim about
CDK's tooling is sourced to CDK's own published material.

---

## 1. Why this route and not the API

There are two doors out of CDK Drive and they are governed by different instruments.

**The Fortellis door.** CDK's API Licensing Terms bind a "Developer" named in an Order. The
licence is revocable, non-sublicensable and non-transferable, and is granted "solely for the
purposes of providing the applicable Developer App(s) as set forth in the Order." CDK asserts
that nothing in the agreement gives the Developer any right "to any data residing on any CDK
Systems." A catch-all bars the Developer from causing "any Third Party" to do anything the
Developer may not do. On termination the Developer must "immediately stop using the API(s),
Data… for any purpose whatsoever" and return or certify destruction of all materials. Access is
gated behind certification, and certification requirements are defined by reference to an
external web page rather than by contract text.

**The export door.** CDK's Data Export Tool is licensed to *the dealer*, not to a developer. It
is contracted through eStore as an addendum to the dealership's existing Master Service
Agreement. It delivers CSV to an SFTP folder. It is encrypted with a key pair the dealer
generates, and CDK states plainly that it cannot read the result.

The difference is not one of convenience. Under the API door the dealership's data is
reconstructed by a licensee at CDK's sufferance. Under the export door the dealership takes
delivery of its own records, encrypted to its own key, into infrastructure it owns. Only the
second produces an asset.

---

## 2. What CDK publishes about the tool

All quotations in this section are from CDK's own documents.

> "Beginning March 2023, CDK is offering a suite of enhanced and secure Data Export and Import
> Tools as a free software license to CDK Dealers. Dealers can now easily export and import
> information from their CDK Systems to their in-house data systems and share it with their
> desired third-party vendors, with no fees from CDK."
> — [CDK Data Export and Import Tools Dealer FAQ](https://cms.cdkglobal.com/sites/default/files/2024-01/Data%20Export%20and%20Import%20Tools%20Dealer%20FAQ_FinalV3-1.pdf), p.2

> "No Fees From CDK — CDK is eliminating our license fees to dealers to use these tools, and your
> ISVs pay no CDK fees when you share your data with them directly."
> — [CDK, Data – Your Way](https://www2.cdkglobal.com/data-your-way)

> "The Data Export Tool is an evolution of DABE… The Data Export Tool provides Dealers with the
> robust ability to extract large amounts of data from CDK products to an SFTP folder for their
> in-house data systems. Through a common UI and PGP encryption, Dealers can securely export data
> across all their CDK Dealerships."
> — [Dealer FAQ](https://cms.cdkglobal.com/sites/default/files/2024-01/Data%20Export%20and%20Import%20Tools%20Dealer%20FAQ_FinalV3-1.pdf), p.2

### The operating parameters, as published

| Parameter | Published value | Source |
|---|---|---|
| Licence fee | None. "Free software license" to CDK dealers | Dealer FAQ p.2 |
| Fee to third parties receiving the data | None. "your ISVs pay no CDK fees" | Data – Your Way |
| Scope | "a comprehensive DMS data set including service, sales, parts and accounting data across multiple store locations" | Dealer FAQ p.3 |
| Transport | SFTP folder managed by CDK | Dealer FAQ p.3–4 |
| Format | CSV | Dealer FAQ p.4 |
| Encryption | Dealer adds its own public key to the Data Export instance; "Only the Dealer (not even CDK) can access the data by using the dealer-generated private decryption key" | Dealer FAQ p.4 |
| Recommended refresh | 24 hours | Dealer FAQ p.4 |
| Maximum refresh | 15 minutes — "96 files (24 hours x 4 files/hour)"; hourly yields 24 files/day | Dealer FAQ p.4 |
| On-demand jobs | Separate SFTP section, so they do not corrupt scheduled jobs | Dealer FAQ p.4 |
| Retention in the SFTP folder | **7 days, then purged** | Dealer FAQ p.4 |
| Authentication to the UI | Simple ID, or multifactor authentication through CDK Connect | Dealer FAQ p.3 |
| Storage responsibility | The dealer's. "CDK Dealers will need to build or leverage a Data system/data warehouse to store all the exported DMS Data" | Dealer FAQ p.3 |
| Skills required | "an understanding of the CDK file structure and dealership operations without the need for SQL query skills" | Dealer FAQ p.3 |
| Enrolment channel | eStore, self-service, with "the addendum to Master Service Agreement needed to implement the offering" | Dealer FAQ p.4 |
| Group contracting | "Dealers can contract for the entire Dealer Group within a single document by selecting all applicable Dealership CMFs" | Dealer FAQ p.4 |

The seven-day purge is the single most important line in that table. CDK holds the extract for a
week and then destroys it. Whoever is pulling it every day is the only party with a durable
record. That is precisely the position the twin is built to occupy.

The line about needing "an understanding of the CDK file structure" is the second most important.
That understanding is exactly what the [model explorer](model/) already documents — 33 records
and 1,023 fields with per-field provenance. The prerequisite CDK names as a barrier is work this
project has already done.

---

## 3. What the tool is not

- **It is not writeback.** Export only. Pushing data back into Drive is the separate Data
  Export/Import Tool, which uses the legacy SOAP PIP packages, requires routing across the
  dealer's private network and OAuth 2.0, and is contracted separately. Nothing in the twin's
  current scope needs writeback.
- **It is not real time.** Recommended cadence is daily; the floor is fifteen minutes. It is a
  file drop, not an event stream.
- **It is not a schema contract.** CDK publishes no field dictionary for the export. The column
  set has to be discovered from the first extract and reconciled against the model.
- **It is not the Fortellis Data Extract API Bundle**, which is a separate, marketed CDK product
  on the Dealership Xperience platform and is governed by the API terms discussed above.

---

## 4. The enrolment path, step by step

CDK's Dealer FAQ states that enrolment is self-service through eStore, using ConnectCDK
credentials, and results in an addendum to the dealership's Master Service Agreement covering
whichever CMFs are selected.

The published eStore flow, documented for the adjacent Partner Program authorization process,
runs as follows and is the same storefront:

1. Log completely out of DealerSuite and close all browser windows.
2. Navigate to the eStore product at `portal.dealersuite.com/eStore`.
3. Log in with an existing **DealerSuite ID** and password.
4. Click through to view available CMFs.
5. Begin enrolling.
6. Select the product.
7. Open and review the **Addendum PDF** before proceeding.
8. Add to cart.
9. Check out — "There is no charge for this authorization process and your purchase will display
   a price of $0.00."
10. Select the CMFs to enrol. If a CMF cannot be selected, "open a case in Service Connect and
    select DealerSuite as the 'area of impact' to have the CMF number added to your login."
11. Place the order. A pending-order confirmation is emailed.
12. Confirm account access and authorise each location's DMS accounts.
13. Save and confirm — after which no further edits are possible.

> "By completing these steps, an addendum will be added to your existing Master Service Agreement
> to be reviewed and finalized by CDK contracting."
> — [CDK Global Partner Program Partner Access Authorization Process](https://go.oeconnection.com/hubfs/LinkIQ/CDK%20Partner%20Program%20eStore%20Authorization%20Process.pdf)

### The signature gate

The same published process states who may do this:

> "To provide access to a partner, a Corporate Officer from your dealership, with the
> authorization to sign the CDK Master Service Agreement, must complete the authorization
> process… you must have a title in the list of Authorized Signers."

That requirement is stated for partner authorisation. Because Data Export enrolment likewise
produces an addendum to the Master Service Agreement, the same signer constraint should be
assumed to apply until CDK confirms otherwise. **This, not the technology, is the critical path.**
The order must be placed by someone whose title appears on CDK's Authorized Signers list, from a
DealerSuite login that already has every relevant CMF attached to it. Neither condition is
currently confirmed for anyone at Peterbilt Atlantic.

---

## 5. What has to exist on our side before the first file lands

| # | Item | Owner | Notes |
|---|---|---|---|
| 1 | PGP key pair | Peterbilt Atlantic | Generated in the dealership's custody. The public key is loaded into the Data Export instance; the private key never leaves dealership control. This is the mechanism by which CDK is locked out of the dealership's own extract, and it only works if the dealership, not a contractor, holds the private half. |
| 2 | Landing zone | Peterbilt Atlantic tenancy | Storage the dealership owns, under its own subscription, receiving the pull. Same principle already applied to the TELUS service identity: company custody, attributable audit trail. |
| 3 | Pull agent | EVEglyph Design | Scheduled SFTP client. Must run at least daily, and must alert on failure, because the source purges after seven days. |
| 4 | Decrypt and land raw | EVEglyph Design | Ciphertext retained alongside plaintext. The encrypted original is the evidentiary copy. |
| 5 | Manifest and hash ledger | EVEglyph Design | Every file recorded with size, row count, SHA-256 and retrieval timestamp before parsing. Provenance is the product. |
| 6 | Schema discovery | EVEglyph Design | First extract profiled column by column and reconciled against the 1,023-field model; every unmatched column logged rather than dropped. |
| 7 | Load to the warehouse | EVEglyph Design | The Postgres and Snowflake DDL for 21 entities already exists in `schema/ddl/`. |
| 8 | Tie-out | Joint | Financial reconciliation against a closed month. Row counts and dollar totals must agree with the dealership's own reporting before anything downstream is trusted. |

---

## 6. Sequence and honest timing

The technical work is small. The dependencies are administrative, and they are the timeline.

| Gate | What it needs | Realistic duration |
|---|---|---|
| A. Identify the authorised signer and confirm the DealerSuite login carries all CMFs | Internal to Peterbilt Atlantic | 1–5 business days, unknown until asked |
| B. Obtain and read the eStore Addendum PDF and product guide before signing | Requires eStore login; the addendum is visible at step 7 without ordering | Same day once inside |
| C. Confirm the offer applies to this platform and this country — CDK Drive for Heavy Truck, billed by CDK Global Canada | CDK account representative | 1–5 business days |
| D. Place the eStore order across all CMFs | Authorised signer | Under an hour |
| E. CDK contracting finalises the addendum | CDK, not us | **Unpublished. No SLA is stated anywhere.** |
| F. Provision the export instance, load the public key, define jobs | Dealership admin with our support | 1–2 days |
| G. First scheduled extract and profiling | EVEglyph Design | 1 day |
| H. Tie-out against a closed month | Joint | 3–5 days |

Gate E is the only genuinely open variable, and CDK publishes no commitment against it. Everything
either side of it is measured in days. Any estimate of the whole path that ignores gate E is a
guess dressed up as a plan.

---

## 7. Risks, stated plainly

1. **The Master Service Agreement is unseen.** Peterbilt Atlantic's own CDK contract has been
   requested and has not arrived. The export addendum attaches to it. Until it is read, no one can
   say what it already permits or already forbids.
2. **The addendum itself is unseen.** It is behind the eStore login. It is the governing text for
   this entire route and it must be read before it is signed, not after.
3. **The account is in arrears.** The March 2026 invoice carries $22,227.77 past due. A dealer
   storefront that requires contracting approval is a poor place to arrive with an aged balance.
   Clear it, or know why it stands, before placing the order.
4. **Platform coverage is unconfirmed.** CDK's material describes Drive. The group runs the heavy
   truck configuration, billed through CDK Global Canada. Coverage should be confirmed by the
   account representative rather than assumed from marketing copy.
5. **Seven-day purge means silent failure is data loss.** A pull agent that fails quietly for eight
   days loses a day permanently. Alerting is not optional.
6. **No published field dictionary for the export.** The column set is discovered, not documented.
   Budget for reconciliation, and treat the first month as calibration.
7. **The signer may not be available.** If the only authorised titles sit with people who are away
   or unaware of the project, the timeline is theirs, not ours.

---

## 8. What this route delivers when it works

A daily, encrypted, dealer-owned copy of the service, sales, parts and accounting record for every
enrolled rooftop, landing in infrastructure the dealership owns, decryptable only with a key the
dealership holds, retained for as long as the dealership chooses rather than for seven days, with
a hash ledger proving what arrived and when.

That is the substrate the manufacturer reporting obligations require, the substrate a call-
verification question can be answered against, and the substrate that does not disappear when a
vendor relationship ends. It costs nothing in licence fees, by CDK's own published commitment.

---

## Sources

- [CDK Data Export and Import Tools — Dealer FAQ](https://cms.cdkglobal.com/sites/default/files/2024-01/Data%20Export%20and%20Import%20Tools%20Dealer%20FAQ_FinalV3-1.pdf)
- [CDK — Data – Your Way](https://www2.cdkglobal.com/data-your-way)
- [CDK — Data Export and Import Tools product page](https://www.cdkglobal.com/dealership-operations/data-management/cdk-data-export-import-tools)
- [CDK — Manage Dealership Data With Ease, solution overview](https://www.cdkglobal.com/sites/cdk4/files/2023-03/23-2459%20Data%20Import_Exporttoolssolutionoverview.pdf)
- [CDK Global Partner Program — Partner Access Authorization Process](https://go.oeconnection.com/hubfs/LinkIQ/CDK%20Partner%20Program%20eStore%20Authorization%20Process.pdf)
- [CDK CONNECT 2022 — "Data – Your Way" announcement](https://www.cdkglobal.com/media-center/cdk-connect-2022)
- CDK API Licensing Terms, as supplied by Luke Weatherbie on 2026-07-29 — held privately in `hawkins-twin-compliance-vault`

---

© 2026 EVEglyphDesign. All rights reserved. Controlled copy · Key ID `EgD-KEY-2026-07`
*Pour le bien-être du peuple.*
