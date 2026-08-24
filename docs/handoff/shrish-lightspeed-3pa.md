# Shrish — Lightspeed 3PA connectivity, first three steps

You are executing the read-only Lightspeed DMS ingestion lane for Peterbilt Atlantic.
The full architectural context is in
[`adapters/lightspeed-3pa/README.md`](../../adapters/lightspeed-3pa/README.md).
This page is only what you need to complete steps 1, 2, and 5 of that plan.

## What we are doing, in one sentence

Peterbilt Atlantic is reading its own customer, contact, and invoice records out of
Lightspeed DMS through the in-app **Third Party Access (3PA)** channel, into dealer
Azure Postgres, so the Hawkins customer twin has one profile per company built from
the superset of Lightspeed DMS + CDK Drive.

This is **not** the paid Partner Program path. The dealer is combining its own data
with its own data. Do not treat Lightspeed or CDK as external parties for the purpose
of this pull.

## What you need before you start

- A Lightspeed DMS admin login for Peterbilt Atlantic with visibility of `System >
  Lists > Stores`. Luke Weatherbie or a delegate will screenshare / provide.
- Read access to this repository (`EVEglyphDesign/eve-hawkins-cdk-twin`) with write
  permission to `adapters/lightspeed-3pa/`, `extract/`, `schema/mapping/`, and
  `docs/lightspeed-3pa-*`.
- Nothing else. In particular, **do not request the API client secret yet** — the
  developer guide has to be read first.

## Step 1 — Read the entitlement screen, one rooftop (15 minutes)

1. Log in to Lightspeed DMS as a Peterbilt Atlantic admin.
2. Navigate: `System` → `Lists` → `Stores` → *pick Moncton* → `Third Party Access (3PA)`.
3. Screenshot the full page — the list of datasets Peterbilt Atlantic is entitled to
   expose to itself under 3PA. Save as
   `docs/lightspeed-3pa-entitlements/moncton.png`.
4. Transcribe the same list into `docs/lightspeed-3pa-entitlements/moncton.md` with
   this table, one row per dataset:

   | Dataset name (as shown) | Entitled? | Fee? | Notes |
   |---|---|---|---|
   | *e.g. Customers* | yes | none shown | — |

5. Commit with message: `lightspeed 3pa: moncton entitlement, as-of <date>`.

**Do not** click "enable", "provision", or "add integration" on that screen. This step
is inventory-only.

## Step 2 — Read the developer guide (1 hour)

The 3PA screen renders a link to Lightspeed's 3PA developer guide. Follow it while
logged in as the same admin.

Extract, into `docs/lightspeed-3pa-developer-guide-notes.md`, only these facts:

1. **Base URL** of the 3PA API (probably ends in `/odata/` or similar).
2. **Auth model** — API key header? OAuth 2 client credentials? Something else?
3. **Object list** — exact names of the endpoints for at least these targets:
   Customer, Customer Contact, Store, Invoice header, Invoice line, Repair Order
   header, Repair Order line. Copy Lightspeed's names verbatim; do not translate them
   yet.
4. **Paging rules** — page size limit, `$top` max, `$skip` allowed, cursor-based
   alternative if any.
5. **Rate limits** — requests per minute per credential.
6. **Timestamp field** — the last-modified column on Customer and Invoice, exactly as
   Lightspeed spells it. This is the field we filter on for incremental pulls.
7. **Sandbox** — is there a Lightspeed 3PA sandbox we can hit before pointing at the
   live Peterbilt Atlantic tenant? If yes, note the base URL.

If the guide contradicts anything in
[`adapters/lightspeed-3pa/README.md`](../../adapters/lightspeed-3pa/README.md), **the
guide wins**. Update the README in the same PR.

Commit with message: `lightspeed 3pa: developer guide notes, as-of <date>`.

## Step 3 — Wait, do not email Kade yet

Once steps 1 and 2 are on `main`, Luke sends one email to
`Kade.Humpherys@lightspeeddms.com` (cc `Ryker.Crismon@lightspeeddms.com`) asking for:

- Written confirmation that dealer-operated read of Customer, Contact, Invoice under
  3PA carries no per-object fee.
- The credential-provisioning form for **one** service account, read-only, scoped to
  the objects listed in step 2 (§3), all rooftops.

Do not send this email yourself. It has to come from Luke's mailbox for the audit
trail.

## Step 5 — The first reconciled test pull

*(Step 4 is credential provisioning by Luke and the Lightspeed team, not you.)*

Once you have the client id / secret in the GitHub environment as
`LIGHTSPEED_3PA_CLIENT_ID` and `LIGHTSPEED_3PA_CLIENT_SECRET`, write the collector at
`extract/lightspeed/collect.py`. Contract:

- Reads its config from `adapters/lightspeed-3pa/config.yml` — rooftop list, object
  list, column selection.
- Assumes OData v2 semantics until the guide says otherwise; see the URI conventions
  reference on
  [OData v2 URI Conventions](https://www.odata.org/documentation/odata-version-2-0/uri-conventions/).
- First call, per rooftop, per object:
  `GET {base}/Customers?$select=<cols>&$orderby=ModifiedOn&$top=500&$inlinecount=allpages&$format=json`
  with `ModifiedOn` replaced by the actual timestamp column from step 2 (§6).
- Follows-up: same URL with `$skip=500`, `$skip=1000`, …, until fewer than `$top` rows
  come back.
- Writes each page as-is to `extract/out/lightspeed/<rooftop>/<UTC-date>/<object>-<page>.json`
  plus a `manifest.json` recording: request URL, request timestamp, response status,
  `inlinecount` first-page value, number of rows on this page, SHA-256 of the payload.
- **Never overwrites** an existing extract file. Re-runs go into a new `<UTC-date>`
  directory.

Run it once, Moncton, Customers only. Then reconcile against the in-app customer
count for Moncton. If the counts do not match, stop and post the delta in the PR —
do not paper over it.

## What not to do

- Do not enable Partner Program integrations from the 3PA screen.
- Do not write to Lightspeed — every request is `GET`. If the collector ever issues
  a non-GET, that is a defect and it must be logged under
  [`registry/SIN-DEFECTS.md`](https://github.com/EVEglyphDesign/eve-glyph-boot-contract/blob/main/registry/SIN-DEFECTS.md).
- Do not store the client secret anywhere except the two locations named above —
  GitHub environment secret and Peterbilt Azure Key Vault. Never in a `.env` file
  committed to a repo, never in a chat transcript, never in a wiki page.
- Do not try to join Lightspeed rows to CDK rows in this repository. The join lives
  in the customer sphere in
  [`hawkins-twin-platform/customer-sphere`](https://github.com/EVEglyphDesign/hawkins-twin-platform/blob/main/customer-sphere/CUSTOMER-SPHERE-DESIGN.md).
  This adapter is a source lane, not a resolver.

## Who to ping

- Blockers on the Lightspeed side: Luke Weatherbie
  (`lweatherbie@peterbiltatlantic.com`) — he owns the correspondence with Kade and
  Ryker.
- Blockers on the repository / schema side: Dany Theriault via this repository's
  issue tracker.
- Blockers on Azure Postgres landing zone: Luke, then Hawkins IT.

Read the executive boot contract before you commit:
[EgD-BOOT-001](https://eveglyphdesign.github.io/eve-glyph-boot-contract/). The
cheapest-rung-first rule and the durability rules apply to every commit you make in
this repository.
