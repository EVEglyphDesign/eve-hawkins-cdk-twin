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

> **SUPERSEDED, 24 Aug 2026.** This step is being rewritten as an
> **automated extraction** driven by the Lightspeed 3PA developer guide, not a
> manual click-through. Do not execute the sub-steps below. Dany is supplying
> the guide; when it lands, this section will be replaced by the collector
> spec and Shrish will run the collector, not the browser.
>
> The read-only, no-buttons-clicked posture and the Customer / Contact /
> Invoice minimum both carry over unchanged into the collector.

### 1.0  Who does what

This step needs a Lightspeed **admin** login. Shrish does not have one and should not
be issued one. Two working shapes:

- **Shape A — screenshare (preferred).** Luke Weatherbie opens the screen on his own
  machine. Shrish joins on Teams / Meet and drives the transcription; Luke drives the
  mouse and clicks. Luke owns the credential; Shrish owns the write-up.
- **Shape B — Luke solo.** Luke does the whole thing and pastes the screenshot into
  the ticket. Shrish picks it up from the ticket. Use this if the screenshare cannot
  be scheduled today.

Either way, **only Luke clicks inside Lightspeed**. Shrish never touches the
Lightspeed session.

### 1.1  Get to the Stores list

1. Open Lightspeed DMS in a browser and sign in as a Peterbilt Atlantic admin.
2. On the top menu bar, click **System**. A dropdown opens.
3. In that dropdown, click **Lists**. A submenu opens.
4. In the submenu, click **Stores**. The Stores list opens, showing one row per
   Peterbilt Atlantic rooftop.

If **System → Lists → Stores** does not exist under exactly those labels on this
tenant, do not guess. Stop and read §1.6 ("If the menu is different") before doing
anything else.

### 1.2  Open Moncton

5. On the Stores list, find the Moncton row. If there is more than one row that
   mentions Moncton, pick the one whose CMF / store number matches the Moncton CMF on
   Peterbilt Atlantic's current DealerSuite screen. Ask Luke — do not choose by feel.
6. Click the Moncton row to open the store detail page.

### 1.3  Open the 3PA panel

7. On the Moncton store detail page, find the tab, button, or side link labelled
   **Third Party Access**. It may render as `Third Party Access`, `Third Party Access (3PA)`,
   or `3PA` — Ryker's email uses the last form, but the label in the product may be
   any of the three.
8. Click it. A panel opens listing the datasets this store is entitled to expose
   under 3PA.

**Do not click any button labelled `Enable`, `Provision`, `Add`, `Add integration`,
`Grant access`, `Invite partner`, or anything similar on this screen.** This step is
**read-only inventory**. Clicking those would send a request to Lightspeed we are
not ready to send.

### 1.4  Screenshot everything visible on that panel

9. Take a screenshot of the entire 3PA panel, including any counts, fees, status
   badges, and dates shown next to each dataset. If the panel scrolls, take one
   screenshot per screenful and number them `moncton-01.png`, `moncton-02.png`, …
   so no row is left out.
10. If any dataset row expands into more detail on hover or click, screenshot the
    expanded state too — same numbering, add `-detail` (e.g. `moncton-01-detail.png`).
11. If the panel shows a link labelled `Developer guide`, `API documentation`,
    `Integration guide`, or similar, **do not click it in this step.** Just note that
    it exists; Step 2 will follow it.

### 1.5  Save the screenshots and the transcription into the repo

On Shrish's machine, in a local clone of
`EVEglyphDesign/eve-hawkins-cdk-twin`, on a branch (never straight to `main`):

```bash
git checkout -b lightspeed-3pa/moncton-entitlement
mkdir -p docs/lightspeed-3pa-entitlements
```

12. Save every screenshot from §1.4 into `docs/lightspeed-3pa-entitlements/` with
    the filenames from §1.4 (`moncton-01.png`, `moncton-02.png`, `moncton-01-detail.png`,
    …). Nothing about the filenames is decorative — the collector in Step 5 reads
    this directory to know what it is allowed to pull.
13. Create `docs/lightspeed-3pa-entitlements/moncton.md` with exactly this frontmatter
    plus one row of the table per dataset shown on the panel. Copy Lightspeed's
    labels **verbatim**. If a column is not shown on screen, leave the cell blank —
    do not infer.

```markdown
---
rooftop: Moncton
tenant: Peterbilt Atlantic
cmf: <the CMF number from §1.2, exactly as shown>
captured_by: <Luke or the admin who ran the screen>
captured_at_utc: <YYYY-MM-DDTHH:MM:SSZ, when the screenshot was taken>
source_screen: System > Lists > Stores > Moncton > Third Party Access (3PA)
screenshots:
  - moncton-01.png
  # (list every png saved in §1.4, one per line)
---

# Moncton — Lightspeed 3PA entitlement, as-of <date>

| Dataset name (verbatim) | Status shown | Fee shown | Partner named | Notes |
|---|---|---|---|---|
| <e.g. Customers> | <e.g. Available> | <e.g. Included> | <e.g. — > | <e.g. no fee visible, no action buttons other than "View"> |
```

**Rules for the transcription table:**

- One row per line item on the panel, in the order shown.
- Copy every column label from the panel; the four above are the minimum. Add more
  columns to the right if the panel shows more.
- If the panel shows a partner name next to a dataset (e.g. `Alliance RV`,
  `Service Manager Pro`), put it in the `Partner named` column. That marks it as a
  Partner Program integration, **not** a first-party 3PA read for our purposes.
- If a dataset has no partner named and no `Enable` action visible against it,
  the notes should say "first-party, ready to authorize".
- If a dataset says something like `Fee applies` / `Additional charge` / a dollar
  amount, that goes in the `Fee shown` column verbatim. Do not translate it.
- If you can't tell what a column means, write down what you see and add a
  `- open question:` line under the table. Do not guess.

### 1.6  If the menu is different

Product UIs drift. If any of `System`, `Lists`, `Stores`, or `Third Party Access`
does not appear under exactly those names:

1. Do **not** hunt around clicking things trying to find it.
2. Screenshot whatever menu you *do* see, save as
   `docs/lightspeed-3pa-entitlements/moncton-menu-actual.png`.
3. Add a short section to `moncton.md` under a heading `## Menu mismatch` describing
   what the menu actually shows.
4. Commit that as-is (§1.7) and stop. Do not proceed to Step 2. Ping Luke via the
   PR — he will re-derive the path with the Lightspeed side and we will update this
   runbook in the same PR.

### 1.7  Commit and open a PR

```bash
git add docs/lightspeed-3pa-entitlements/
git commit -m "lightspeed 3pa: moncton entitlement, as-of <YYYY-MM-DD>"
git push -u origin lightspeed-3pa/moncton-entitlement
gh pr create \
  --base main \
  --title "Lightspeed 3PA: Moncton entitlement inventory" \
  --body "Screenshots and verbatim transcription of the Third Party Access panel
          for Moncton, per Step 1 of docs/handoff/shrish-lightspeed-3pa.md.
          Read-only inventory. No buttons clicked on the Lightspeed side."
```

Ask Luke to review the PR. Merge only after Luke confirms the screenshot matches
what he sees on his own screen — that is the check that this transcription actually
corresponds to Peterbilt Atlantic's Moncton entitlement and not to some other
rooftop's screen we captured by mistake.

### 1.8  What "done" looks like for Step 1

All three must be true before Step 2 starts:

- `docs/lightspeed-3pa-entitlements/moncton.md` on `main`, with at minimum a
  `Customer` (or `Customers`) row, a `Contact` (or equivalent) row, and an
  `Invoice` (or `Sales` / `Billing`) row. If any of those three is missing from
  the panel entirely, that itself is the finding — record it as "not visible on
  panel" and raise it in the PR body. Luke needs to know before he emails Kade.
- At least one screenshot of the panel committed alongside the `.md`.
- No `Enable` / `Provision` / `Add integration` button was clicked on the
  Lightspeed side. Confirm this in the PR body verbatim: `no state-changing
  actions taken on Lightspeed`.

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
