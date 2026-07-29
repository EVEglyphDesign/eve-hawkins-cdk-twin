# Export-fallback adapter

**Status: wireframe / to be filled from lanes 1, 6.** Draws on CDK's own documented
non-API extract paths (lane 1) and the payroll/AP file-export findings (lane 6). `ingest.py`
and `fields.md` are not yet written.

Handles the categories of data with **no confirmed Fortellis API** — either because none was
found in the lane research, or because CDK's own alternative extract tooling is the only
documented path. This adapter exists as a first-class citizen of this repo, not an
afterthought, because two entire domains (payroll, and parts of employee/vendor master data)
have no API path at all per Module 05.

## What it ingests

| Source | Mechanism | Twin target | Module |
|---|---|---|---|
| Payroll (hours, pay-type flags) | Third-party payroll system (ADP, Netchex, Workzoom) file export — **not a CDK-native API**; CDK only supplies the RO-side flat-rate hours via `technicianIds[]` on the RO | Payroll fact table (not yet defined — feeds the labor-cost postings in `bseg.sql`) | 03, 05, 06 |
| Employee master | No confirmed CDK employee-master API; identifiers surface only as fields on other objects (`serviceAdvisor`, `cashier`, `technicianIds[]`) | Employee reference used by `PERNR`-style foreign keys across fact tables — populated from payroll export, not CDK | 05 |
| Vendor / AP master | No confirmed public CDK vendor-master API found | `lfa1.sql` / `lfb1.sql` | 05 |
| CDK Data Export Tool | CDK's own documented flat-file/bulk export tooling, referenced in lane 1 as an alternative extract path alongside the Fortellis APIs | Bulk backfill/reconciliation source for any table also fed by the CDK-Fortellis adapter | 01 |
| STAR XML (Business Object Documents) | Industry-standard XML interchange format (Parts Order, Repair Order, Sales Lead, Vehicle Service History, Warranty Reconciliation BODs, plus 2024's Retail Delivery Report / Vehicle Invoice / Vehicle Order additions) — confirmed as a cross-vendor standard CDK participates in as a DMS vendor, per lane 1 and lane 8 | Cross-check/reconciliation format, not a primary ingest path unless CDK's own STAR BOD export is confirmed live for this tenant | 01, 06 |
| Factory financial statement download to PACCAR | Karmak's PACCAR integration confirms "financial statements are automatically downloaded to PACCAR" as standard DMS-PACCAR integration behavior; CDK Drive's equivalent mechanism is `UNVERIFIED` but structurally analogous | Outbound-only — this is data the *dealer* sends to PACCAR, not data the twin ingests; documented here because it defines the NADA-format reporting layer noted in `../../schema/README.md` | 02, 06 |

## Why this adapter exists as a peer to CDK-Fortellis, not a fallback footnote

Two structural gaps make file-export a permanent part of this repo's architecture, not a
temporary workaround:

1. **Payroll has no CDK-native API at all** (Module 06 §6) — this is not a case of an API
   existing but being avoided; no such API was found in any lane's research.
2. **CDK Drive's 2024 ransomware outage** (≈19 days, ≈15,000 dealerships affected, per lane 1
   and lane 7) demonstrated that a DMS-API-only ingest strategy has a single point of failure.
   A working file-export path is also the dealer's practical continuity mechanism during any
   future CDK outage, independent of Fortellis API availability. See
   [`../../docs/current-state.md`](../../docs/current-state.md) for the full rationale.

## Auth / access

File-export mechanisms are inherently heterogeneous — SFTP drop, manual portal download, or
scheduled report email, depending on the source system (payroll vendor vs. CDK Data Export
Tool vs. STAR XML partner feed). `UNVERIFIED`: the exact mechanism CDK's Data Export Tool uses
for Peterbilt Atlantic's tenant specifically (SFTP vs. portal vs. other) — needs confirmation
against the live tenant before `ingest.py` can be written.

## Credentials

```
# Placeholder only — exact mechanism (SFTP/portal/email) not yet confirmed
# per source. Populate once each source's real access method is verified.
PAYROLL_EXPORT_SOURCE=          # e.g. adp | netchex | workzoom
PAYROLL_EXPORT_ACCESS_METHOD=   # UNVERIFIED
CDK_DATA_EXPORT_ACCESS_METHOD=  # UNVERIFIED
STAR_XML_PARTNER_FEED_ACCESS=   # UNVERIFIED
```

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
