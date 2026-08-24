# adapters/lightspeed-3pa

**Lightspeed DMS ingestion lane — Peterbilt Atlantic self-serve read of its own records.**

Status: **wireframe, waiting on 3PA developer guide and dealer credentials from Kade Humpherys**.

Sibling to [`adapters/cdk-fortellis`](../cdk-fortellis/) and [`adapters/paccar`](../paccar/).
Same design law: one adapter per external system, SAP-shape schema on the way out, and no
invented field names. The customer twin ends as one profile per company built from the
superset of CDK Drive and Lightspeed DMS, joined on the customer identity CDK carries and
Lightspeed carries (invoice-anchored — see [Section 4 of the v0.1 finding memo][v01]).

## Why this is a first-party lane, not a third-party integration

Peterbilt Atlantic is combining its **own** dealership business data (customers, contact
history, invoices) from Lightspeed DMS with its **own** business data from CDK Drive, TELUS,
and mail — all inside dealer-controlled Azure Postgres. There is no downstream party
consuming the data. Under Lightspeed's own product taxonomy this is the internal 3PA
(Third Party Access) surface a dealer opens for its own extension work; it is not the
paid Partner Program integration that Lightspeed uses to broker access between a dealer
and an external ISV. The distinction was confirmed on the [Lightspeed DMS partners page][ls-partners]
and by [Ryker Crismon's 24 Aug 2026 email][ryker], which points the dealer at the in-app
3PA path without invoking Partner Program terms.

This matches the CDK-lane precedent recorded on
[projects/peterbilt-atlantic-digital-twin][twin-canon]:
> Dealer-controlled CDK export — the preferred extraction route is CDK Data Export Tool
> over SFTP/PGP plus Dealer Data Exchange, avoiding the per-data-type third-party-access
> path when dealer entitlement permits it.

Lightspeed's shape here is analogous: dealer-entitled reads first; Partner Program /
Managed Data Services only if Peterbilt Atlantic ever chooses to publish this data
outward.

## The channel, in the order Peterbilt Atlantic will walk it

1. **In-app entitlement inventory (dealer-operated, free).**
   Path given verbatim by Lightspeed:
   `System > Lists > Stores > your store > Third Party Access (3PA)`.
   This screen enumerates every dataset Peterbilt Atlantic is entitled to expose to itself
   under 3PA, per rooftop. That inventory becomes `docs/lightspeed-3pa-entitlements.md` —
   one table per rooftop, one row per dataset, with `entitled` / `not entitled` / `paid`
   marked from the screen.

2. **Developer guide.** The 3PA page renders a link to the Lightspeed developer guide once
   entitlement is confirmed. That guide names the base URL, the auth model (dealer-scoped
   API key or OAuth), the object catalogue, and the paging rules. It supersedes anything
   inferred here. **Do not build a client before reading it.**

3. **Contact of record.** Kade Humpherys (<Kade.Humpherys@lightspeeddms.com>) handles all
   3PA at Lightspeed per [Ryker Crismon, 24 Aug 2026][ryker]. Ryker (Account Manager) stays
   copied as the commercial owner. All correspondence lands in the
   `lweatherbie@peterbiltatlantic.com` mailbox so a Peterbilt-owned audit trail exists
   from turn one (same custody principle as the TELUS service-identity rule on
   [projects/peterbilt-atlantic-digital-twin][twin-canon]).

4. **Fallback: dealer-operated report writer + CSV.** If 3PA API entitlement is delayed
   or gated behind a fee we are not ready to authorize, Phase 1 stays on the report
   writer / CSV path Dany already blessed in the canon
   ([Lightspeed Phase 1 stays dealer-operated][twin-canon]). Same landing zone, slower cadence,
   no external dependency.

## Object scope for the customer twin (superset with CDK)

The v0.1 finding memo [What the Data Already Says][v01] states the join problem plainly:

> An email record knows an address. A phone record knows a number. Nothing in either
> says they are the same company. An invoice knows both.

So the Lightspeed lane pulls the fields that carry the invoice identity across email
and phone, and stops there for Phase 1. Everything else can wait for the wider spec.

| Object | Why we need it in Phase 1 | Maps to (SAP-shape) |
|---|---|---|
| Customer / Company account | The identity spine — one row per business, with name, mailing address, primary phone, primary email, tax id, status | `KNA1` — general customer master |
| Customer contact / person | Named contacts under each company, with email and direct phone | `KNVK` — customer contact person |
| Store / rooftop | Which Peterbilt Atlantic location owns the relationship | `T001W` — plant/store |
| Invoice header | Date, rooftop, customer, total, status — the row that resolves phone-to-email | `VBRK` — billing document header |
| Invoice line | Part/service/description, qty, net, tax — for spend attribution | `VBRP` — billing document item |
| Repair order header (if under 3PA) | Ties service work to the same customer identity | `VBAK` / dealer analogue |
| Parts sale line (if under 3PA) | Parts-vocabulary lens from the v0.1 memo Section 3 | `MSEG` / dealer analogue |

The `Customer` and `Invoice*` objects are the non-negotiable minimum. Everything else
loads only when it is already inside a page returned by those queries. Zero speculative
fan-out.

## Wire format — likely OData v2, treat as such until the guide says otherwise

Lightspeed DMS's public developer surface historically uses OData v2 semantics (paging,
projection, and filtering all done in the query string). Until the 3PA developer guide
confirms otherwise, the client assumes OData v2 as specified by
[OData v2 URI Conventions § 4 Query String Options][odata].

Read-only client contract:

- `$filter` for incremental pulls — always by a last-modified timestamp column on the
  server side, never by client-side date maths. Example against a `Customers` collection:
  `$filter=ModifiedOn gt datetime'2026-08-01T00:00:00'`.
- `$select` on every request — never `SELECT *`. Column list is stored in
  `config/lightspeed-3pa.yml` and versioned with the code.
- `$orderby` on the same timestamp column that `$filter` uses. This is what makes
  paging repeatable — the OData spec explicitly warns that `$skip` / `$top` without
  `$orderby` may not be consistent across requests.
- `$top` fixed at the guide's page size (assume 500 until told otherwise); `$skip`
  advances by exactly `$top`.
- `$inlinecount=allpages` on the first page of every extract so the extract log records
  the total count the server said existed **before** we started paging.
- `$format=json` and `Accept: application/json`. No XML/Atom parsing.

Every request, its response headers, its row count, and its SHA-256 of the returned
payload land in `extract/out/lightspeed/<rooftop>/<YYYY-MM-DD>/` — same custody shape as
the CDK export collector on [projects/peterbilt-atlantic-digital-twin][twin-canon].

## Sequence for connectivity (this week, with Shrish executing)

Ordered by cheapest-first — [EgD-BOOT-001 §1][boot].

1. **Read entitlement, 15 minutes, no external call.** Luke or a Peterbilt Atlantic
   Lightspeed admin opens `System > Lists > Stores > <rooftop> > Third Party Access (3PA)`
   for one representative rooftop (Moncton is the default anchor unless Luke says
   otherwise). Screenshot the entitlement list, drop the screenshot in
   `docs/lightspeed-3pa-entitlements/moncton.png` and the transcription in the sibling
   `.md`. This costs nothing and answers "can we even see Customer and Invoice from
   here?" before anyone writes code.

2. **Read the developer guide, 1 hour, no external call.** From the same 3PA screen,
   follow the link to the developer guide. Extract: base URL, auth model, object list,
   paging rules, rate limits, timestamp field name. Land as
   `docs/lightspeed-3pa-developer-guide-notes.md` — a summary in this repository, not a
   copy of Lightspeed's document.

3. **First correspondence to Kade Humpherys, one email, no follow-up loop.** Luke
   (from `lweatherbie@peterbiltatlantic.com`) sends the request. Cc Ryker Crismon. Ask:
   (a) confirm that under Peterbilt Atlantic's current agreement, dealer-operated read
   of Customer, Contact, Invoice, and (if entitled) Repair Order via 3PA has no
   per-object fee; (b) request the credential provisioning form for one service account
   scoped to those objects, read-only, all rooftops. **One email. Do not restate the
   entire architecture; the audit trail belongs in this repository, not in his inbox.**

4. **Provision one Peterbilt-owned service account, not a personal one.** Same custody
   rule as `entities` on the TELUS lane: the credential holder is a role mailbox, not
   Luke's personal account, so it survives him leaving. Store the client id in this
   repository; store the client secret in the GitHub environment under
   `LIGHTSPEED_3PA_CLIENT_SECRET` and in Peterbilt's Azure Key Vault under the same
   name. **Write the secret to both stores in the same action that provisions it** —
   [EgD-BOOT-003][boot] durability rule.

5. **First reconciled test pull, single rooftop, single object.** Moncton, `Customers`
   only, `$top=500`, `$inlinecount=allpages`. Compare row count against Lightspeed's own
   customer count on the in-app screen for Moncton. Do not proceed to a second object
   until the counts agree to within the reason we can explain.

6. **Widen to Customer + Contact + Invoice across all rooftops.** Same collector, one
   rooftop at a time, same reconciliation.

7. **Land in the customer sphere.** The rows arrive in dealer Azure Postgres under
   `lightspeed_raw.*`, then are projected into the SAP-shape customer sphere alongside
   the CDK projection. The join key is the invoice-anchored identity discussed on
   [projects/peterbilt-atlantic-digital-twin][twin-canon]. **Origin and confidence are
   preserved per vector** — [Customer Sphere makes disagreement visible][twin-canon].
   Nothing averages; conflicts stay visible for human resolution.

Steps 1 and 2 are free and can start today.
Step 3 is one email, cheap.
Steps 4–7 are the connectivity work Shrish will execute against this repository once
the developer guide is on file.

## Handoff to Shrish

The Shrish-facing runbook is [`docs/handoff/shrish-lightspeed-3pa.md`](../../docs/handoff/shrish-lightspeed-3pa.md).
It contains only what he needs to execute steps 1, 2, and 5; the commercial and
architectural context stays here.

## References

- [EVEglyphDesign Executive Boot Contract — EgD-BOOT-001][boot]
- [Peterbilt Atlantic Digital Twin — canonical project page][twin-canon]
- [What the Data Already Says v0.1 — 24 Aug 2026 finding memo][v01] *(local to this working set; not yet committed)*
- [OData v2 URI Conventions — Query String Options][odata]
- [Lightspeed DMS Partners page][ls-partners]
- Ryker Crismon (Lightspeed) to Luke Weatherbie, 24 Aug 2026, `Re: Data export tool options` — 3PA path and Kade Humpherys as 3PA owner

[boot]: https://eveglyphdesign.github.io/eve-glyph-boot-contract/
[twin-canon]: https://github.com/EVEglyphDesign/hawkins-twin-platform
[v01]: ../../docs/finding-memos/what-the-data-already-says-v0.1.md
[odata]: https://www.odata.org/documentation/odata-version-2-0/uri-conventions/
[ls-partners]: https://www.lightspeeddms.com/partners/
[ryker]: mailto:Ryker.Crismon@lightspeeddms.com
