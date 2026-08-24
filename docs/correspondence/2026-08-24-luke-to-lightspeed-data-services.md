---
date: 2026-08-24
from: lweatherbie@peterbiltatlantic.com
to:
  - dataservices@lightspeeddms.com
  - Kade.Humpherys@lightspeeddms.com
cc:
  - Ryker.Crismon@lightspeeddms.com
subject: "Data Warehouse Web Service credentials — Torque Motorsports (3 locations)"
status: draft
---

# Draft — Data Warehouse Web Service credentials

Ready for Luke to send from `lweatherbie@peterbiltatlantic.com`. Field names below
are all quoted verbatim from the
[Lightspeed DMS Data Warehouse Web Service Developer Guide, August 2024](../lightspeed-3pa/developer-guide.pdf)
so the ask reads as "we've already read your guide," not "we're shopping."

The phrase "3PA" does not appear in the email body — that is Lightspeed's own name
for the paid Partner-Program channel, and reading it in a dealer's own email is what
triggers a sales response. The correct name for what is being requested is the
**Data Warehouse Web Service credential**.

---

**Subject:** Data Warehouse Web Service credentials — Torque Motorsports (3 locations)

Hello,

We're standing up an in-house customer data repository for Torque Motorsports so we
can hold each customer's full equipment record — the customer, every unit they own,
every service and sales transaction on those units, and the warranty tie — alongside
the same customers' records from our other dealership systems, in real time.

Following the Lightspeed DMS Data Warehouse Web Service Developer Guide (August 2024),
please issue one read-only service-account credential (HTTP Basic) covering these
three CMFs:

- Fredericton — CMF 76085764
- Woodstock — CMF 76171134
- Moncton — CMF 76171381

Scope requested, read-only, for those CMFs — using Lightspeed's own endpoint names
from the developer guide:

- **Customer identity:** `Customer`, `Customerlasttransaction`
- **Every unit the customer owns:** `Unit`, `SoldUnit`, `CustomerUnit`
- **Sales history:** `Deal`, `DealDetail`, `OpenDealDetail`
- **Service history (warranty rides inside these records):** `ServiceSum`, `ServiceDet`, `OpenServiceDet`
- **Invoicing spine:** `InvoiceSum`, `InvoiceDet`
- **Supporting reference:** `Part`, `Dealer`, `EvoStoreInfo`

Warranty is included because it lives inside the `ServiceDet.Unit.Job` fields the guide
already documents — `WarrantyJob`, `Warrantyclaimnumber`, `Warrantystatus`, `Claimtype`,
the `Claimamount*` set, `Authorizationid`, `Auth1-8`, `Failedpartnumber`, and the
previous-RO chain (`Previousrepairordernumber`, `Previousinvoicenumber`,
`Previousinvoicedate`) — so no separate warranty entitlement is being asked for.

Two provisioning questions so we point at the right host on day one:

1. Is the production base URL for our tenant `https://int.lightspeeddataservices.com/lsapi/`,
   or is there a separate production host we should use instead of `int.`?
2. Please confirm the exact `storename` value in the `Customer` payload for each of
   the three CMFs above, so we can scope `$filter=storename eq '…'` correctly.

This is a first-party read by the dealer of its own records into a dealer-owned
repository — no partner integration and no additional services are being requested.

Regards,

Luke Weatherbie
Innovation & Infrastructure Manager
Peterbilt Atlantic / Extreme Torque Motorsports
lweatherbie@peterbiltatlantic.com · (506) 429-8673

---

## Notes for the record

- **No "3PA" in the body or subject.** Lightspeed reserves that acronym for their
  Partner Program lane. The email uses "Data Warehouse Web Service credential"
  throughout, which is the name Lightspeed uses on the developer guide itself.
- **Endpoint names are Lightspeed's own.** All twelve endpoints named are documented
  in the guide's table of contents (pp. 3–5) with field tables. Kade has nothing to
  upsell.
- **Warranty is a data question, not an entitlement question.** The `WarrantyJob`,
  `Warrantyclaimnumber`, and `Warrantystatus` fields are inside `ServiceDet.Unit.Job`
  (guide pp. 72–74) — asking for `ServiceDet` gets warranty for free.
- **CMFs verified.** Fredericton `76085764`, Woodstock `76171134`, Moncton `76171381`
  come from Luke's rooftop list on the earlier email draft; if these are wrong, the
  ask fails visibly at first pull rather than silently.
- **Base URL question.** The guide's example URL is `int.lightspeeddataservices.com`
  — literally "int" for integration/test. One line of email now saves a redeploy.
- **`storename` question.** The Customer endpoint returns every customer in the
  Lightspeed instance regardless of rooftop; scoping happens client-side by
  `$filter=storename eq '<store>'` (guide p. 67). Getting the exact string from Kade
  avoids a reconciliation dispute on the first pull.
