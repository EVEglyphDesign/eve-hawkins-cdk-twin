# PACCAR adapter

**Status: wireframe / to be filled from lane 8 (`cdk_08_paccar_oem.md`).** No public REST API
was found for the majority of PACCAR's dealer-facing systems — this adapter is scoped
narrower than the CDK-Fortellis adapter and, for most systems below, describes an integration
gap rather than a callable endpoint. `ingest.py` and `fields.md` are not yet written.

Bridges the seam between CDK Drive (dealer-side DMS) and PACCAR's own systems, which run on
an SAP-shape enterprise stack (S/4HANA, SAP TM, SAP GTS, SAP IBP, SAP BFC, SAP Concur — see
[`../../modules/01-organization.md`](../../modules/01-organization.md) and lane 8 for the
full PACCAR SAP footprint evidence).

## What it ingests — real PACCAR system names only

| PACCAR system (real, confirmed name) | What it does | Public API? | Adapter posture |
|---|---|---|---|
| **Online Parts Counter (OPC)** | eCommerce parts ordering, 545,000+ parts, dealer/fleet 24/7 access | No public REST API documented; structured B2B order upload/download exists via DMS integration (confirmed for Karmak Fusion) | Ingest via DMS-side order/ASN records already landing in `matdoc.sql` through the CDK-Fortellis adapter, not a direct OPC call |
| **Managed Dealer Inventory (MDI)** | PACCAR Parts' daily automated stock-order recommendation engine (Stock / MKT / COF order types, confirmed via Karmak's integration docs) | No public API; batch data exchange | Same as OPC — order-type metadata (`Stock`/`MKT`/`COF`) should be captured as a header field on the twin's parts-order record, not invented as a CDK-native field |
| **PRWS — PACCAR Registration and Warranty System** | Warranty claim submission/adjudication | **Yes** — listed as available on Fortellis; CDK creates PRWS drafts from RO data | This is the one PACCAR-adjacent system reachable through the CDK-Fortellis adapter (see [`../cdk-fortellis/README.md`](../cdk-fortellis/README.md)) — tracked here because the claim's *target* system of record is PACCAR's, not CDK's |
| **PACCAR Solutions / PSSM (built by Decisiv)** | Fleet/customer service scheduling and case management | No public developer API found; vendor platform | Out of scope for direct ingest — only the RO-relevant slice synced into CDK (estimate, parts list, labor) should be captured, per lane 8's sovereign-data finding in Module 06 §7 |
| **TruckTech+ (Kenworth) / SmartLINQ (Peterbilt)**, via Decisiv | Remote diagnostics/telematics case management, auto-creates service cases from fault codes | No public third-party API documented | Same posture as PSSM — do not attempt to ingest raw telematics; PACCAR's own Truck Connectivity Services Terms frame this as a PACCAR-retained data asset, not a dealer-owned one |
| **DAVIE4** | Diagnostic/programming tool (desktop, technician-facing) | No public API; desktop software tied to eportal credentials | Out of scope — no ingest path exists; referenced only as the tool that produces the diagnosis recorded on the RO |
| **PACCAR eportal** (`eportal.paccar.com`) | SSO gateway to service manuals, wiring diagrams, WebFleet eCat, PVP downloads | No public API; SSO/browser only | Out of scope for automated ingest |
| **Syncron Service Lifecycle Management (SLM) / Returns SmartBlox** | Standardized dealer-to-OEM parts-return workflow (adopted by PACCAR in 2022) | Syncron Customer Connect provides ERP/dealer-system integration; no public dealer-side API confirmed | Flagged for future investigation — returns automation could reduce the manual reconciliation burden `docs/open-questions.md` currently lists for the `161` return movement type |
| **"PACCAR's B2B infrastructure"** (Karmak's generic term for the factory build-data feed) | Feeds truck build/spec data into DMS at delivery | No named platform or public API found | Target for `zveh_build.sql` (Module 05 §2) once a named integration point is confirmed — currently only reachable, if at all, through whatever a DMS vendor's own integration (e.g., Karmak Fusion) exposes |

**Confirmed non-existent name — do not use:** "PartsPRO" does not exist as a PACCAR system.
The real system is **Online Parts Counter (OPC)**. Likewise, do not assert a confirmed North
American PACCAR order type of "VOR" — only **Stock, Emergency, MKT (Marketing Suggestion),
COF (Auto Confirmed)** are confirmed via Karmak's PACCAR integration documentation.

Refs:
- [Karmak PACCAR integration page](https://www.karmak.com/integrations/paccar)
- [Rihm Kenworth — Online Parts Counter](https://www.rihmkenworth.com/blog/the-benefits-of-online-parts-counter--55573)
- [PACCAR Parts Technology page](https://www.paccarparts.com/technology/)
- [CDK Global Heavy Truck OEM page](https://www2.cdkglobal.com/ht-oem) (PRWS)
- [PACCAR Solutions login](https://paccar.decisiv.net/)
- [PACCAR Truck Connectivity Services Terms](https://www.paccar.com/telematicsterms)
- [Syncron/PACCAR returns case study](https://www.syncron.com/resources/paccar-automates-connected-dealer-to-oem-returns-processing)

## Auth

No unified PACCAR auth pattern exists across these systems — each is a separate credential
surface (eportal SSO + digital certificate for portal tools; Decisiv account credentials for
PSSM/TruckTech+/SmartLINQ; Fortellis OAuth2 for PRWS, inherited from the CDK-Fortellis
adapter). `UNVERIFIED`: whether any of these support a service-account/machine-to-machine
auth flow suitable for unattended ingest, as opposed to interactive dealer-staff login only.

## Credentials

```
# PRWS is reached via the Fortellis credentials already defined in
# ../cdk-fortellis/README.md — not duplicated here.

# All other PACCAR systems in the table above have no confirmed public
# API and therefore no credential contract to define yet.
PACCAR_EPORTAL_USERNAME=   # interactive SSO only — not suitable for automated ingest
PACCAR_EPORTAL_CERT_PATH=  # PACCAR Keymaster digital certificate, if applicable
```

## Sovereign-data posture

Per lane 8's telematics findings (Module 06 §7): PACCAR's own Truck Connectivity Services
Terms state PACCAR "collects, uses and retains" vehicle/telematics data and does not frame
dealer or customer access as ownership. This adapter's design intentionally does **not**
attempt to bulk-export raw telematics, warranty adjudication internals, or factory
order-entry data beyond what CDK's own Fortellis-reachable APIs (PRWS drafts, RO-linked
estimates) already expose. Anything beyond that boundary is out of scope until PACCAR
publishes a dealer-facing API or a documented bulk-export mechanism is found.

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
