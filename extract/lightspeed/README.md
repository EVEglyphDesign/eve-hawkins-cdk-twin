# extract/lightspeed

Automated collector for the Lightspeed DMS 3PA Data Warehouse Web Service.

- **Adapter spec:** [`adapters/lightspeed-3pa/README.md`](../../adapters/lightspeed-3pa/README.md)
- **Config:** [`adapters/lightspeed-3pa/config.yml`](../../adapters/lightspeed-3pa/config.yml)
- **Wire spec:** [`docs/lightspeed-3pa/developer-guide.pdf`](../../docs/lightspeed-3pa/developer-guide.pdf)
- **Runbook (Shrish):** [`docs/handoff/shrish-lightspeed-3pa.md`](../../docs/handoff/shrish-lightspeed-3pa.md)

## Run

```bash
pip install -r extract/lightspeed/requirements.txt
export LIGHTSPEED_3PA_BASIC_AUTH="username:password"

# Reconciled first pull — Moncton, Customer only
python -m extract.lightspeed.collect --rooftop moncton --endpoint Customer

# Phase-1 sweep across every configured rooftop
python -m extract.lightspeed.collect --phase 1.0
```

## Output layout

```
extract/out/lightspeed/
  <rooftop>/
    watermark.json                                  # last DateGathered / InvoiceDate per endpoint
    <UTC-date>/
      manifest.json                                 # per-run manifest, one entry per endpoint
      Customer-0000.json                            # raw JSON payload, page 0 (up to 500 rows)
      Customer-0001.json
      InvoiceSum-0000.json
      InvoiceDet-0000.json
      InvoiceDet-0001.json
      ...
      <endpoint>-<page>.error.txt                   # only present if a page returned non-200
```

The collector never overwrites an existing extract file. Same-day re-runs land in
`<UTC-date>--rerun-<HHMMSS>/`. Watermarks advance only after every configured endpoint
for a rooftop finishes cleanly.

## Tests

```bash
python -m unittest extract.lightspeed.tests.test_url_build
```

The tests pin the URL and `$filter` construction against the guide's own literal
conventions (datetime literals, `L` suffix on big ints, single-quoted strings, no
`$select` / `$expand` / `$inlinecount`).
