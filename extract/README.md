# Extract harness — operator runbook

**Status: wireframe, built ahead of credentials landing.** This is Lane B's deliverable:
a runnable extract harness for the CDK Twin Day-1 pull, written against the documented
Fortellis CDK Drive API surface in [`../docs/model/model.json`](../docs/model/model.json)
(21 entities) and the [shared brief](../CDK_EXTRACT_BRIEF.md). Every script in
[`bin/`](bin/) imports cleanly and runs `--help` today, with no credentials. Nothing here
has been run against a live Peterbilt Atlantic tenant — see the `UNVERIFIED` markers in each
script's module docstring before trusting a payload shape.

## What this is for

Tomorrow (2026-07-29 business hours, US Central) the operator expects a CDK Drive
user-admin login and Fortellis credentials for Peterbilt Atlantic. The moment they land,
this harness should require zero new code — only environment variables — to start pulling
metadata, then master data, then transactions, while the ledger-side objects that have
**no API path** (per `docs/model/model.json`, `api.reachable: none`) get queued for manual
export capture through [`../adapters/export-fallback/`](../adapters/export-fallback/README.md).

## Environment variables required

### Fortellis (CDK Drive REST) — `adapters/cdk-fortellis/`

| Variable | Purpose |
|---|---|
| `FORTELLIS_APP_ID` | Fortellis marketplace app client ID (OAuth2 client-credentials) |
| `FORTELLIS_APP_SECRET` | Fortellis marketplace app client secret |
| `FORTELLIS_SUBSCRIPTION_ID` | `Subscription-Id` header — identifies the store/app pairing making the call |
| `CDK_DEPT_ID_<SITE>` | One per site/functional-area pair, e.g. `CDK_DEPT_ID_PA01`. `Department-Id` header — CDK scopes every response by department (Accounting/Finance/Inventory/Parts/Service). Exact taxonomy per site is `UNVERIFIED` until confirmed against the live tenant — see [`../adapters/cdk-fortellis/README.md`](../adapters/cdk-fortellis/README.md) |
| `FORTELLIS_BASE_URL` | Optional override; defaults to `https://api.fortellis.io` (documented Fortellis marketplace base, not tenant-specific) |
| `FORTELLIS_TOKEN_URL` | Optional override for the OAuth2 token endpoint; default in `00_validate_access.py` is `UNVERIFIED` against this specific tenant's Okta authorization-server ID — confirm from the app's Fortellis marketplace credentials page on day one |

At least one `CDK_DEPT_ID_*` variable must be set for `00_validate_access.py` to attempt
an entitlement probe. Nine Peterbilt Atlantic rooftops means up to nine (or more, if
functional areas are split) department IDs.

### Export fallback — `adapters/export-fallback/`

No API credentials — these are file-drop paths. See
[`../adapters/export-fallback/README.md`](../adapters/export-fallback/README.md) for the
per-source access mechanism (`UNVERIFIED` until confirmed: SFTP vs. portal vs. manual
download for the CDK Data Export Tool specifically).

## Exact order of execution

Metadata before transactions, always — this mirrors the brief and the numeric prefix on
each script:

```
1. python3 extract/bin/00_validate_access.py         # auth handshake + entitlement probe -- go/no-go gate
2. python3 extract/bin/10_extract_metadata.py         # GL accounts, schedules, dept, employee, dealer-partition
3. python3 extract/bin/20_extract_masters.py          # customer, vehicle, vendor, parts master/inventory
4. python3 extract/bin/30_extract_transactions.py     # repair orders + nested labor/parts/punches, parts sales, deal jackets
5. python3 extract/bin/40_ingest_exports.py --input FILE --target-id ID   # once export files exist (repeatable, per file)
6. python3 extract/bin/90_counts.py                   # integrity control totals -- run last, and after any re-run
```

Do not skip step 1. `00_validate_access.py` exits non-zero (`NO-GO`) if credentials are
missing or the entitlement probe fails — that is the intended behavior, not a bug. Do not
proceed to step 3+ on a `NO-GO`.

Run everything with `--dry-run` first if you want to see the target list and output paths
without making a network call — every script in `bin/` supports it.

## What to do when a lane returns 401 / 403 vs 404 vs empty

These three failure modes mean different things and call for different actions. Do not
retry blindly through any of them.

### 401 / 403 — stop, this is not a rate limit

- **Meaning:** auth or entitlement failure. Either the OAuth2 token request itself failed
  (bad `FORTELLIS_APP_ID`/`FORTELLIS_APP_SECRET`), or the token is valid but the
  `Subscription-Id`/`Department-Id` pair is not entitled to that endpoint.
- **Action:** `extract/lib/common.request_with_backoff` does **not** retry 401/403 — it
  raises immediately. Check, in this order: (1) credentials are the ones issued for
  Peterbilt Atlantic specifically, not a sandbox/demo app; (2) the Fortellis marketplace
  subscription for this API is **Active**, not **Pending approval** — some CDK Drive APIs
  require a manual approval step after subscribing; (3) the `Department-Id` in use actually
  matches a department this subscription covers (a Service-scoped subscription will 403 on
  an Accounting-scoped call). Re-run `00_validate_access.py` after any credential change —
  never skip straight back to `30_extract_transactions.py`.

### 404 — check the URL, not the data

- **Meaning:** per this harness's own docstrings, every literal REST path in `bin/*.py` is
  marked `UNVERIFIED` — API *names* are documented (per `docs/model/model.json`), but the
  literal path segments are inferred from common Fortellis URL conventions, not confirmed
  against a live OpenAPI spec. A 404 most likely means the path or API version segment is
  wrong, not that the data doesn't exist.
- **Action:** pull the real OpenAPI/Swagger spec from the Fortellis developer portal for
  the specific API named in `extract/config/targets.yaml`'s `endpoint` field, fix the
  `RESOURCE_PATH` constant in the relevant script, and re-run. Do not silently swap in a
  guessed alternate path — update the script and note the fix in its docstring so the next
  operator isn't guessing twice.

### Empty (200 with zero rows) — check the window and the department scope before assuming "no data"

- **Meaning:** either genuinely no data in the requested window/department, or a
  parameter mismatch (wrong `Department-Id` for that data type, or a date-window parameter
  name that silently doesn't filter the way assumed — several are marked `UNVERIFIED` in
  `30_extract_transactions.py`).
- **Action:** re-run the same target with a deliberately wide window (e.g. one full year)
  and no department filter narrowing, if the API allows it. If rows come back, the original
  window/department params were wrong — fix them, don't conclude the dealership has zero
  repair orders. If still empty, treat it as a genuine finding and record it in the target's
  manifest (`extract/out/<phase>/<target>.ndjson.manifest.json`) rather than silently moving
  on — `90_counts.py` surfaces `NOT_RUN`/zero-row targets so this doesn't get lost.

## Resumability and idempotency

Every writer in `extract/lib/common.py` (`NdjsonWriter`) reads its own existing output file
on start and skips rows it has already written, keyed by a per-target natural key
(RO number, VIN, part number, etc.). Re-running any script after an interruption is safe —
it continues, it does not duplicate or restart from zero. `30_extract_transactions.py`
additionally supports resuming a specific date window: re-run with the same `--from`/`--to`
and it will only add rows not already captured.

## Rate limits

`extract/lib/common.request_with_backoff` honors a `Retry-After` header on `429` and backs
off exponentially (capped at 60s between attempts, 6 retries by default) on `429`/`5xx`.
It does not retry `401`/`403`/`404` — see above.

## Output layout

```
extract/out/
  <phase>/<target-id>.ndjson                 # newline-delimited JSON, one row per line
  <phase>/<target-id>.ndjson.manifest.json   # row count, min/max timestamp, SHA-256, status
  discovered-schema/<target-id>.schema-report.json   # from 40_ingest_exports.py only
  00_validate_access.report.json             # go/no-go report
  90_counts.report.json                      # integrity control totals across all targets
```

`<phase>` is one of `metadata`, `masters`, `transactions`, `ledger`, per
[`config/targets.yaml`](config/targets.yaml).

## Declarative manifest

[`config/targets.yaml`](config/targets.yaml) is the single source of truth for what gets
extracted, from where, and how — one entry per target, `api_reach` copied honestly from
[`../docs/model/model.json`](../docs/model/model.json). Add a new extraction target by
adding a row there, not by hardcoding a new endpoint inside a script.

## Dependencies

Python 3 standard library, plus:

- `requests` — HTTP client (`pip install requests`)
- `pyyaml` — YAML config loading (`pip install pyyaml`); if unavailable, `extract/lib/common.py`
  falls back to a minimal built-in YAML-subset parser sufficient for `config/targets.yaml`'s
  flat list-of-mappings shape only.

No build step, no framework. Every script in `bin/` is directly runnable:
`python3 extract/bin/<script>.py --help`.

## Where the real payload shape is unknown

Every script's module docstring states its `UNVERIFIED` assumptions explicitly (resource
paths, pagination parameter names, response envelope field names). This harness codes
against the **documented** shape from
[`../docs/model/model.json`](../docs/model/model.json) and public Fortellis material, and
never invents a field name to fill a gap — see
[`40_ingest_exports.py`](bin/40_ingest_exports.py)'s column-profiling approach for the same
principle applied to hand-exported files.

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
