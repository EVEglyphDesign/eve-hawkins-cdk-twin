# adapters/lightspeed-3pa

**Lightspeed DMS ingestion lane — Peterbilt Atlantic self-serve read of its own records.**

Status: **collector spec, waiting on service-account HTTP Basic credentials from the
Lightspeed Data Services team via Kade Humpherys.**

Sibling to [`adapters/cdk-fortellis`](../cdk-fortellis/) and [`adapters/paccar`](../paccar/).
Same design law: one adapter per external system, SAP-shape schema on the way out, and no
invented field names. The customer twin ends as one profile per company built from the
superset of CDK Drive and Lightspeed DMS, joined on the customer identity CDK carries and
Lightspeed carries (invoice-anchored — see [Section 4 of the v0.1 finding memo][v01]).

This README supersedes the OData-v2 assumptions in commit `75d5f3c` — the correct wire
format is documented directly in the
[Lightspeed DMS — Data Warehouse Web Service Developer Guide, August 2024][ls-guide]
(committed under [`docs/lightspeed-3pa/developer-guide.pdf`][guide-local]). Where this
README and the guide disagree, the guide wins.

## Why this is a first-party lane, not a third-party integration

Peterbilt Atlantic is combining its **own** dealership business data (customers, contact
history, invoices) from Lightspeed DMS with its **own** business data from CDK Drive, TELUS,
and mail — all inside dealer-controlled Azure Postgres. There is no downstream party
consuming the data. Under Lightspeed's own product taxonomy this is the internal 3PA
(Third Party Access) surface a dealer opens for its own extension work; it is not the
paid Partner Program integration that Lightspeed uses to broker access between a dealer
and an external ISV. The distinction was confirmed on the
[Lightspeed DMS partners page][ls-partners] and by
[Ryker Crismon's 24 Aug 2026 email][ryker], which points the dealer at the in-app 3PA
path without invoking Partner Program terms.

## Wire format — verbatim from the Lightspeed developer guide

The API is **not standards-OData**. It reuses a subset of OData v2 query semantics but
disables the projection and count features. Every fact below is quoted from the
[developer guide][guide-local], sections *Service Description* (pp. 6–9) and the per-endpoint
field tables.

- **Base URL:** `https://int.lightspeeddataservices.com/lsapi`
- **URL shape:** `/{BaseURL}/{DataType}/{CMF}` — the customer master file number (CMF) is
  a **URL segment**, not a query parameter. Example:
  `https://int.lightspeeddataservices.com/lsapi/Customer/76156733`.
- **Authentication:** HTTP Basic. Username and password are issued by the Lightspeed Data
  Services team; contact Kade Humpherys for testing credentials. There is **no** OAuth,
  no API key header, no client-id / client-secret pair — the earlier assumption of
  `LIGHTSPEED_3PA_CLIENT_ID` / `LIGHTSPEED_3PA_CLIENT_SECRET` is retracted.
- **Content:** JSON by default. `Accept: text/xml` returns XML instead. Gzip supported via
  the non-standard header `X-Accept-Encoding: gzip` (the guide is explicit that this is
  `X-Accept-Encoding`, not `Accept-Encoding`).
- **Date literals on the URL:** ODBC `yyyy-mm-dd` for `date` types; datetime literal
  `datetime'2014-01-01'` (single-quoted) inside `$filter`. Response bodies return
  `yyyy-mm-ddThh:mm:ss.nn` — dealer-server timezone for every field **except**
  `DateGathered`, which is Lightspeed's Gateway-server timezone.
- **Big integer filter values need the `L` suffix** in `$filter`, e.g.
  `RowKey eq 735775383867171434L`. The suffix is not required on the newest AWS
  deployment, but including it is safe on every version.
- **Query options SUPPORTED:** `$filter`, `$top` (server cap **500** rows per page),
  `$skip`, `$orderby`, and logical operators (`and`, `or`, `not`, `eq`, `ne`, `lt`, `le`,
  `gt`, `ge`).
- **Query options NOT SUPPORTED:** `$select`, `$expand`, `$inlinecount` (in any form),
  `$format` as a query parameter, arithmetic operators, and string functions
  (`startswith`, `substringof`, `substring`, etc.). **Do not build a client that emits
  those** — the server ignores or errors on them and the earlier draft of this adapter
  was wrong to include them.
- **HTTP status codes:** `200` success (including empty result), `401` authentication
  failure, `403` authorization failure, `404` no matching endpoint / CMF, `500` other.
  Errors return a plain-string body; there is no `WWW-Authenticate` challenge.
- **Null semantics:** every non-string field is nullable — treat every numeric or date
  field as `Optional`.

### Consequences for the collector

Because `$select` is not available, every response returns the **full field set** for the
requested endpoint. The collector stores the payload as-is; column selection happens in
the projection into `lightspeed_raw.*` (SAP-shape mapping) downstream, not on the wire.

Because `$inlinecount` is not available, there is no server-declared total to reconcile
against on the first page. Reconciliation happens by paging until a partial page
(`rowcount < $top`) is returned, then comparing the collector's own row count against the
Lightspeed in-app UI count for the same rooftop and date range.

Because `$expand` is not available, related objects (e.g. `ServiceDet.Unit.Job.Parts`) are
returned as **embedded arrays inside the primary endpoint's payload** — the guide
documents these as sub-tables of the response, not as separate endpoints. `ServiceDet`
alone returns nested `Unit`, `Unit.Job`, `Unit.Job.Parts`, and `Unit.Job.Labor` levels.
The collector persists the payload whole; splitting into relational tables is a
downstream concern.

## Endpoint list and incremental key, Phase 1

Column names below are quoted verbatim from the developer guide. Phase 1 is the minimum
that closes the invoice-anchored phone-to-email join called out in
[Section 4 of the v0.1 finding memo][v01].

| Endpoint | Contract # | Incremental key | Scoping filter (rooftop) | Guide page |
|---|---|---|---|---|
| `Customer` | 4994580 | `DateGathered` (`datetime`) | `storename eq '<store>'` | 66–67 |
| `CustomerUnit` | 4994580 | *(snapshot — no timestamp; whole-set pull)* | *(scoped by parent Customer's CMF)* | 68 |
| `CustomerLastTransaction` | 4994580 | *(snapshot — no timestamp; whole-set pull)* | *(scoped by CMF only)* | 133 |
| `ServiceSum` | 4994582 | `CashieredDate` (`datetime`) or `ROHeaderId` (`bigint`, needs `L` suffix) | *(scoped by CMF only; join to Customer downstream)* | 68–69 |
| `ServiceDet` | 4994583 | `datein` (`datetime`) | *(scoped by CMF only)* | 70–75 |
| `InvoiceSum` | 4994586 | `InvoiceDate` (`date`) or `InvoiceId` (`int`) | *(scoped by CMF only)* | 96–97 |
| `InvoiceDet` | 4994587 | `InvoiceDate` (`date`) or `invoiceId` (`int`) | *(scoped by CMF only)* | 97–99 |
| `Deal` | 4994584 | `FinanceDate` (`datetime`) | *(scoped by CMF only)* | ~41–65 |
| `DealDetail` | 4994585 | *(TBD — read the guide field table when we get to it)* | *(scoped by CMF only)* | ~50–65 |

Notes:

- **The `Customer` endpoint returns every customer in the Lightspeed instance the CMF
  belongs to** — not only the ones tagged to a specific rooftop. Scoping to a single
  Peterbilt Atlantic rooftop is done client-side by `$filter=storename eq '<store>'`.
  The other endpoints scope by CMF alone; the rooftop identity attaches downstream
  through the customer join. (Guide, p. 67, `storename` field.)
- **CCPA suppressed rows** — if `optoutsharedata eq true` or
  `removepersonalinformation eq true`, only `CustomerId` comes back; every other field is
  blank/null. The collector persists these rows unchanged; the projection layer decides
  what to do with them. (Guide, p. 67, `optoutsharedata` / `removepersonalinformation`.)
- **InvoiceSum / InvoiceDet** have no last-modified column; the guide's own note is
  "Use InvoiceID or InvoiceDate to determine changes" (guide, pp. 97, 99). The collector
  uses `InvoiceDate` because it is an indexable date and matches the guide's example
  URLs. `InvoiceId` is the fallback if `InvoiceDate` proves too coarse in production.
- **`CustomerLastTransaction` and `CustomerUnit` are snapshot endpoints** — no timestamp
  column to filter on. The collector reads the whole set every run; storage cost is
  bounded because they are small compared to `ServiceDet` / `InvoiceDet`.
- Endpoint discovery on the guide page numbers marked `~` (Deal, DealDetail) still needs
  a targeted field-table read on first collector run against a live tenant — recorded as
  the Phase-1 exit criterion.

## Object → SAP-shape mapping (customer sphere projection)

Unchanged from the previous draft; the wire format was wrong, the target shape is right.
Column selection happens **after** the raw JSON lands.

| Lightspeed endpoint | Why we need it in Phase 1 | Maps to (SAP-shape) |
|---|---|---|
| `Customer` (`Cmf`, `CustomerId`, `LastName`, `FirstName`, `storename`, addresses, emails, phones, `DateGathered`) | The identity spine — one row per business/individual | `KNA1` — general customer master |
| `CustomerUnit` (customer → unit/VIN links) | Named units under each customer | `KNVK` / dealer analogue |
| `InvoiceSum` (`Cmf`, `InvoiceId`, `InvoiceNo`, `InvoiceDate`, `custid`, `Sales`, `SalesType`) | Invoice header — the row that resolves phone-to-email | `VBRK` — billing document header |
| `InvoiceDet` (`invoiceId`, `Invoicelineno`, `partno`, `qty`, `price`, `cost`, ...) | Invoice lines — spend attribution and parts identity | `VBRP` — billing document item |
| `ServiceSum` (`ROHeaderID`, `rono`, `custid`, `CashieredDate`, `CommonInvoiceId`) | RO header — joins service work to customer + invoice | `VBAK` / dealer analogue |
| `ServiceDet` (nested `Unit` → `Job` → `Parts`, `Labor`) | RO detail — parts and labor vocabulary from the v0.1 memo §3 | `MSEG` / dealer analogue |
| `Deal` / `DealDetail` (major-unit sales) | Unit-sale row that anchors the customer's ownership history | `VBAK` / `VBAP` for major-unit sales |

The `Customer` + `InvoiceSum` + `InvoiceDet` triplet is the non-negotiable minimum for
Phase 1. Everything else loads only after those three are reconciled.

## Sequence for connectivity (this week, Shrish executing)

Ordered cheapest-first — [EgD-BOOT-001 §1][boot].

1. **Provisioning email from Luke** (5 minutes, one email, from
   `lweatherbie@peterbiltatlantic.com`). Cc Ryker Crismon. Ask Kade Humpherys for:
   (a) written confirmation that dealer-operated read of `Customer`, `InvoiceSum`,
   `InvoiceDet`, `ServiceSum`, `ServiceDet`, `Deal`, `DealDetail` under 3PA carries no
   per-object fee for Peterbilt Atlantic; (b) the credential provisioning form for
   **one** read-only service account, all rooftops, scoped to those endpoints;
   (c) the CMF (Customer Master File) number(s) for Peterbilt Atlantic's rooftops.
   The credential is HTTP Basic `username:password`, not OAuth — see the guide.

2. **Store the credential in both custody stores in the same action** —
   [EgD-BOOT-003][boot] durability rule. GitHub environment secret
   `LIGHTSPEED_3PA_BASIC_AUTH` (value: `username:password`, exactly as base64 will encode)
   **and** Peterbilt Azure Key Vault same name, written in the same action. The service
   account is a role identity, not Luke's personal login.

3. **Configure `adapters/lightspeed-3pa/config.yml`** — rooftop list (`storename` values
   as they appear in Lightspeed's own store list), CMF per rooftop, endpoint list, and
   per-endpoint incremental key. Everything else is derived.

4. **First reconciled test pull, one rooftop, one endpoint.** Moncton, `Customer` only,
   `$top=500`, `$orderby=DateGathered`, `$filter=storename eq '<Moncton store>'`. Compare
   the collector's row count to Lightspeed's own in-app Moncton customer count. Do not
   proceed to a second endpoint until the counts agree.

5. **Widen to `Customer` + `InvoiceSum` + `InvoiceDet` across all rooftops.** Same
   collector, one rooftop at a time, same reconciliation, per-endpoint incremental
   watermark stored under `extract/out/lightspeed/<rooftop>/watermark.json`.

6. **Land in the customer sphere.** Rows arrive in dealer Azure Postgres under
   `lightspeed_raw.<endpoint>`, then project into the SAP-shape customer sphere
   alongside the CDK projection. The join key is the invoice-anchored identity from
   [Section 4 of the v0.1 finding memo][v01]. Origin and confidence are preserved per
   vector, per the [Customer Sphere design][twin-canon] — nothing averages; conflicts
   stay visible.

## Collector — where the code lives

- **Collector entrypoint:** [`extract/lightspeed/collect.py`](../../extract/lightspeed/collect.py)
- **Configuration:** [`config.yml`](./config.yml)
- **Extract layout:** `extract/out/lightspeed/<rooftop>/<UTC-date>/<endpoint>-<page>.json`
  + `manifest.json` (request URL, request timestamp UTC, response status, row count,
  SHA-256 of the payload) + `watermark.json` (last successful timestamp per endpoint,
  per rooftop). **The collector never overwrites an existing extract file**; a re-run
  writes to a new UTC-dated directory.

## Handoff to Shrish

The Shrish-facing runbook is [`docs/handoff/shrish-lightspeed-3pa.md`](../../docs/handoff/shrish-lightspeed-3pa.md).
It contains only what he needs to execute the automated collector against a
Peterbilt-provided credential; the commercial and architectural context stays here.

## References

- [Lightspeed DMS — Data Warehouse Web Service Developer Guide, August 2024 (repo copy)][guide-local] — the canonical wire spec
- [EVEglyphDesign Executive Boot Contract — EgD-BOOT-001][boot]
- [Peterbilt Atlantic Digital Twin — canonical project page][twin-canon]
- [What the Data Already Says v0.1 — 24 Aug 2026 finding memo][v01]
- [Lightspeed DMS Partners page][ls-partners]
- Ryker Crismon (Lightspeed) to Luke Weatherbie, 24 Aug 2026, `Re: Data export tool options` — 3PA path and Kade Humpherys as 3PA owner

[boot]: https://eveglyphdesign.github.io/eve-glyph-boot-contract/
[twin-canon]: https://github.com/EVEglyphDesign/hawkins-twin-platform
[v01]: ../../docs/finding-memos/what-the-data-already-says-v0.1.md
[ls-guide]: ../../docs/lightspeed-3pa/developer-guide.pdf
[guide-local]: ../../docs/lightspeed-3pa/developer-guide.pdf
[ls-partners]: https://www.lightspeeddms.com/partners/
[ryker]: mailto:Ryker.Crismon@lightspeeddms.com
