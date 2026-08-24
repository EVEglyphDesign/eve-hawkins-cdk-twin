# Shrish — Lightspeed 3PA automated collector runbook

You are executing the read-only Lightspeed DMS ingestion lane for Peterbilt Atlantic.
The architectural and commercial context is in
[`adapters/lightspeed-3pa/README.md`](../../adapters/lightspeed-3pa/README.md);
the wire spec is [`docs/lightspeed-3pa/developer-guide.pdf`](../lightspeed-3pa/developer-guide.pdf).
This page is the shortest possible path from "credentials in hand" to "reconciled first
page of Moncton `Customer` in the repository."

**This is an automated data extraction, not a manual click-through.** You will run one
Python script. You will not open the Lightspeed web UI at any point. The only human
inside the Lightspeed session is Luke Weatherbie, and only for provisioning (Step 1).

## What we are doing, in one sentence

Peterbilt Atlantic is reading its own customer, contact, invoice, and service records
out of Lightspeed DMS through the **Third Party Access (3PA) Data Warehouse Web
Service** into dealer Azure Postgres, so the Hawkins customer twin has one profile per
company built from the superset of Lightspeed DMS + CDK Drive.

This is **not** the paid Partner Program path. The dealer is combining its own data with
its own data. Do not treat Lightspeed or CDK as external parties for the purpose of this
pull. Every request the collector issues is `GET`. There are no writes.

## Wire format facts you actually need

All quoted from [the developer guide][guide], § *Service Description* (pp. 6–9).

- **Base URL:** `https://int.lightspeeddataservices.com/lsapi`
- **URL shape:** `/lsapi/{DataType}/{CMF}` — CMF (Customer Master File number) is a URL
  segment, never a query parameter.
- **Auth:** HTTP Basic (`username:password`). No OAuth, no client-id/secret, no API key.
- **Content:** JSON default; gzip requested with the non-standard header
  `X-Accept-Encoding: gzip`.
- **Query options SUPPORTED:** `$filter`, `$top` (server cap **500**), `$skip`, `$orderby`,
  logical operators.
- **Query options NOT SUPPORTED:** `$select`, `$expand`, `$inlinecount`, `$format`,
  arithmetic operators, string functions (`startswith`, `substringof`, etc.). The
  collector must never emit these.
- **Datetime literals in `$filter`:** `datetime'YYYY-MM-DDTHH:MM:SS'` (single-quoted).
- **Big integer literals in `$filter`:** append the `L` suffix.

The collector at [`extract/lightspeed/collect.py`](../../extract/lightspeed/collect.py)
already encodes all of the above. You do not have to build URLs by hand.

## Step 1 — Luke sends the provisioning email (Luke, not you)

Luke (from `lweatherbie@peterbiltatlantic.com`) sends **one** email to
`Kade.Humpherys@lightspeeddms.com`, cc `Ryker.Crismon@lightspeeddms.com`, asking for:

1. Written confirmation that dealer-operated read of `Customer`, `InvoiceSum`,
   `InvoiceDet`, `ServiceSum`, `ServiceDet`, `Deal`, `DealDetail` under 3PA carries no
   per-object fee for Peterbilt Atlantic.
2. The credential-provisioning form for **one** read-only service account, all
   rooftops, scoped to those endpoints. The credential is HTTP Basic
   `username:password`.
3. The CMF (Customer Master File) number(s) for each Peterbilt Atlantic rooftop.
4. The exact `storename` values as they appear in Lightspeed's own store list, per
   rooftop.

**Do not send this email yourself.** It has to come from Luke's mailbox for the audit
trail. When items 2–4 land, proceed to Step 2.

## Step 2 — Store the credential in both custody stores, in the same action

[EgD-BOOT-003 durability rule][boot]: never encrypt with a key that has not already
been persisted, and never rely on a single store.

1. In the `EVEglyphDesign/eve-hawkins-cdk-twin` GitHub repository, add an environment
   secret named `LIGHTSPEED_3PA_BASIC_AUTH`. Value: `<username>:<password>`, exactly as
   base64 will encode. Do **not** paste it into a repo file or a chat transcript.
2. In Peterbilt Atlantic's Azure Key Vault, add a secret named
   `LIGHTSPEED-3PA-BASIC-AUTH` with the same value.
3. Both must be written **in the same working session**. If Step 2.2 fails, delete Step
   2.1 immediately — do not leave a single-custody credential.

The service account is a role identity, never Luke's personal login.

## Step 3 — Fill in the rooftop config

Open [`adapters/lightspeed-3pa/config.yml`](../../adapters/lightspeed-3pa/config.yml)
in a branch:

```bash
git checkout -b lightspeed-3pa/rooftop-config
```

Replace every `TBD-*` value under `rooftops:` with the real CMF and storename Kade
provided. **Do not guess.** If Kade returned only some of the rooftops, leave the
missing ones with `TBD-*` values so the collector will refuse to run against them.

Commit and open a PR:

```bash
git commit -am "lightspeed 3pa: fill rooftop CMF and storename from Kade provisioning"
git push -u origin lightspeed-3pa/rooftop-config
gh pr create --base main \
  --title "Lightspeed 3PA: rooftop CMF and storename" \
  --body "CMF and storename per rooftop, from Kade Humpherys provisioning email. Credential is in the GitHub environment as LIGHTSPEED_3PA_BASIC_AUTH; no secret material in this PR."
```

Luke reviews and merges.

## Step 4 — Reconciled first pull, Moncton `Customer` only

This is the go/no-go gate. Do this before running anything else.

```bash
# Local shell on a machine with the credential exported.
export LIGHTSPEED_3PA_BASIC_AUTH="<username>:<password>"

python -m extract.lightspeed.collect \
  --rooftop moncton \
  --endpoint Customer
```

Expected outputs:

- `extract/out/lightspeed/moncton/<UTC-date>/Customer-0000.json`,
  `Customer-0001.json`, … one file per 500-row page. The last page has fewer than 500
  rows.
- `extract/out/lightspeed/moncton/<UTC-date>/manifest.json` — request URL, request
  timestamp UTC, response status, row count per page, SHA-256 per page.
- `extract/out/lightspeed/moncton/watermark.json` — the maximum `DateGathered` the
  collector saw across all pages.

Reconciliation:

1. Sum the `row_count` fields across every page in the manifest.
2. Ask Luke for Moncton's in-app Lightspeed customer count as-of the same UTC date.
3. If the two agree within a delta Luke can explain, proceed to Step 5.
4. If they do not agree, **stop.** Post the delta in a new issue titled
   `lightspeed 3pa: moncton customer count mismatch`. Do not paper over it and do not
   proceed. Common explanations Luke may confirm:
   - CCPA-suppressed rows (the guide says these come back with only `CustomerId`
     populated — they still count in the row total).
   - Timezone edge (Lightspeed's UI count runs to local midnight; the collector runs
     to UTC-now).
   - Customers deleted between the UI-count and the collector run.
   None of those are reasons to skip reconciliation.

Commit the first-run manifests to the repository so the audit trail is durable:

```bash
git checkout -b lightspeed-3pa/moncton-first-pull
git add extract/out/lightspeed/moncton/
git commit -m "lightspeed 3pa: first reconciled pull, moncton Customer, <UTC-date>"
git push -u origin lightspeed-3pa/moncton-first-pull
gh pr create --base main \
  --title "Lightspeed 3PA: Moncton Customer first pull, reconciled" \
  --body "First reconciled test pull per docs/handoff/shrish-lightspeed-3pa.md § Step 4. Row count agreed with Lightspeed UI to within <delta>, explanation from Luke: <explanation>."
```

## Step 5 — Widen to Phase 1 across all rooftops

Once Step 4 is merged, run the full Phase-1 sweep. `--phase 1.0` is already the default;
this is explicit for the record.

```bash
python -m extract.lightspeed.collect --phase 1.0
```

That runs `Customer`, `InvoiceSum`, and `InvoiceDet` for every configured rooftop, in
order. Each rooftop gets its own `<UTC-date>/manifest.json` and its own
`watermark.json`, so subsequent runs are incremental automatically.

Reconcile every rooftop's `Customer` count against Luke's in-app count before the PR
merges. The `InvoiceSum` count reconciles against Lightspeed's own invoice-report count
for the same rooftop and date range.

## Step 6 — Schedule the collector

Once Step 5 is green for at least two consecutive runs, schedule the collector to run
nightly via a GitHub Actions workflow that:

1. Loads `LIGHTSPEED_3PA_BASIC_AUTH` from the environment secret.
2. Runs `python -m extract.lightspeed.collect --phase 1.0`.
3. Commits new `extract/out/lightspeed/...` files under a `bot/lightspeed-nightly`
   branch and opens (or updates) a PR for Luke to spot-check row counts before merge.

The nightly workflow is intentionally left as a Phase-1.5 task — the collector itself
is dry-runnable on any developer's machine first, and durability of the extract lives
in git, not in CI.

## Rules that do not change

- **Every request is `GET`.** If the collector ever issues a non-`GET`, that is a
  defect; log it under [`registry/SIN-DEFECTS.md`][sin].
- **Never overwrite an extract file.** The collector refuses to; do not work around it.
  Re-runs write to a suffixed directory.
- **Never store the credential outside the two custody stores in Step 2.** Not in a
  `.env` committed to the repo, not in a chat, not in a wiki.
- **The join to CDK does not live in this repository.** This adapter is a source lane.
  Join logic lives in the customer sphere of
  [`hawkins-twin-platform`][twin-canon].

## Who to ping

- Blockers on the Lightspeed side (credential, CMF, storename, fee dispute):
  Luke Weatherbie (`lweatherbie@peterbiltatlantic.com`) — he owns the correspondence
  with Kade and Ryker.
- Blockers on the repository, schema, or collector code: Dany Theriault via this
  repository's issue tracker.
- Blockers on Azure Postgres landing zone or Key Vault: Luke, then Hawkins IT.

Read the executive boot contract before you commit:
[EgD-BOOT-001][boot]. The cheapest-rung-first rule and the durability rules apply to
every commit you make in this repository.

[boot]: https://eveglyphdesign.github.io/eve-glyph-boot-contract/
[guide]: ../lightspeed-3pa/developer-guide.pdf
[twin-canon]: https://github.com/EVEglyphDesign/hawkins-twin-platform
[sin]: https://github.com/EVEglyphDesign/eve-glyph-boot-contract/blob/main/registry/SIN-DEFECTS.md
