# Open questions

**Status: wireframe / consolidated from the "What I could not verify" sections of all 8 lane
research files (`cdk_01_platform.md` through `cdk_08_paccar_oem.md`).** Every item below is
carried forward verbatim in substance from its source lane — nothing here is a new claim.
Items are numbered for reference from other files in this repo. `UNVERIFIED` markers below
mean "not found in any public source consulted," not "confirmed false," unless stated
otherwise.

---

## Lane 1 — Platform architecture

1. Whether "Company Number" is formally exposed anywhere in the modern Fortellis REST layer
   as its own field/header, or is purely a legacy back-office/EDI-era concept superseded by
   `Subscription-Id` + `Department-Id`. No Fortellis spec found naming a `Company-Number`
   header. (Module 01)
2. Exact OpenAPI operation names/paths for each async start→poll→pull endpoint — referenced by
   name and doc URL in third-party guides, but the raw OpenAPI YAML was not directly opened.
   (Module 01, `adapters/cdk-fortellis/README.md`)
3. "ODDX" as a named automotive data standard — no independent corroboration found distinct
   from the STAR XML/BOD family. Lane 8 separately confirmed the real standard behind this
   term is likely **ODX (ISO 22901-1)**, which governs ECU diagnostic data, not commercial/
   dealer-ledger data — treat "ODDX" as a probable misnomer for ODX. (Module 01, Module 06 §7
   via lane 8)
4. "CDK Data Cloud" as a distinct, currently marketed CDK product — not found under this name;
   may be conflated with the free CDK Data Export/Import Tool suite. (`adapters/export-fallback/README.md`)

## Lane 2 — Ledger

5. A PACCAR/Peterbilt-specific dealer accounting manual or chart-of-accounts document
   (equivalent to published GM or Ford dealer manuals) — not publicly located. (Module 02)
6. CDK Drive's actual internal accounting-schedule numbers/names (an equivalent to Ford's
   "1140" schedule or Autosoft's GLSKEDS export) — not found in any public CDK document.
   (Module 02)
7. The exact CDK Drive screen/table names for posting-period lock (closed-period enforcement)
   — current understanding is inferred from cross-DMS norms only. (Module 02)
8. Whether CDK Drive itself outputs a labeled "GAAP" or "ASPE" statement distinct from the OEM
   statement, and what that screen/report is called. (Module 02)
9. Full request/response schema of the `glpost`/`glwippost` Fortellis APIs (journal line
   fields, period fields) — only endpoint existence was confirmed via a support thread, not a
   fetched spec page. (Module 02, `adapters/cdk-fortellis/README.md`)
10. Any CDK-specific curtailment or floor-plan G/L account numbers — only generic bank/OCC-level
    curtailment mechanics and PACCAR Financial Services' existence as a wholesale lender were
    confirmed. (Module 02)

## Lane 3 — Cost objects

11. The exact CDK host-side (non-Fortellis) field/table name for the department dimension on a
    raw G/L posting line — only the externally exposed Fortellis `Department-Id` header is
    documented publicly. (Module 03)
12. The literal field name CDK uses for "flat rate hours"/"book time" inside the OpCodes API
    schema — only the API's existence is confirmed. (Module 03)
13. Whether CDK Drive posts an explicit intercompany-style elimination entry for internal work
    between departments, or nets the transfer purely through the vehicle inventory schedule —
    no public source documents the G/L mechanics at this granularity. (Module 03)
14. The specific G/L account/field breakdown (acquisition, pack, recon labor, recon parts,
    floorplan interest) inside the Display Vehicle Cost roll-up. (Module 03)
15. Whether CDK exposes a native "technician efficiency"/"technician proficiency" calculated
    field, or whether these are purely 20-group/DMS-report constructs computed downstream of
    raw clock/flag-hour data. (Module 03)
16. Whether Peterbilt/PACCAR heavy-truck dealers report into NADA's ATD 20 Group composite
    specifically, or a PACCAR-proprietary equivalent. (Module 03, Module 06 §8 via lane 8)

## Lane 4 — Materials

17. The exact schema field for the supersession-chain pointer — only the driving menu function
    (`PN`) is confirmed; the underlying field/table name is not. (Module 04)
18. Beyond store-code visibility via `DealerId`+`Department-Id`, CDK's own inter-store transfer
    mechanics (as distinct from the generically-documented DMS-class "intercompany parts
    transfer" capability) are `UNVERIFIED`. (Module 04)
19. Whether the Async Parts Inventory / Search Parts Pick Ticket Fortellis APIs are being
    replaced — a 2025 community thread raised the question with no confirming reply found.
    (Module 04, `adapters/cdk-fortellis/README.md`)
20. Any PACCAR-specific obsolescence/return-allowance percentage for dealer parts — only the
    *supplier*-facing 120-day PACCAR Purchase Order Terms clause was found, which governs
    PACCAR's upstream suppliers, not dealer-facing policy. (Module 04, confirmed again
    independently in lane 8 §4)
21. Whether a formally named "VOR" order type exists in PACCAR's North American dealer
    ordering program — VOR terminology is confirmed only for PACCAR's Australian PDC
    operations. Do not treat VOR as a confirmed NA order type anywhere in this repo. (Module
    04, `adapters/paccar/README.md`)

## Lane 5 — Master data

22. The full field list for the vehicle-inventory record (new/used truck in stock) as distinct
    from the CDK Drive Service Vehicles API record — not retrieved in this research pass.
    (Module 05 §2)
23. CDK Heavy Truck's vehicle/chassis master schema — this is a separate CDK product from the
    light-vehicle Drive DMS most of this research is grounded in; its schema is not separately
    published. (Module 05 §2)
24. Whether CDK Drive exposes any employee-master API at all — no "Get Employee" or
    "Employee Master" Fortellis API was found; employee identity today surfaces only as
    fields on other objects (RO's `serviceAdvisor`, `cashier`, `technicianIds[]`). (Module 05
    §3)
25. Whether any public CDK vendor-master API exists — none was found. (Module 05 §4)
26. Fleet-account hierarchy modeling (parent account → multiple VINs/drivers) beyond the flat
    business-customer record — not confirmed. (Module 05 §1)

## Lane 6 — Document flow

27. The exact chargeback mechanism and G/L treatment when PACCAR denies or adjusts a paid
    warranty claim after submission via PRWS — not found in any public PACCAR or CDK document;
    current treatment in Module 06 §4 is inferred from general franchised-dealer accounting
    norms, not a PACCAR-specific disclosure. (Module 06 §4, also flagged independently in lane
    8 §3)
28. Whether three-way match (PO → receipt → invoice) is a *native* CDK AP capability inside the
    Foundations Suite, versus a manual process using the GL Inquiry Workflow as a lookup tool
    only. (Module 06 §6)
29. "Electronic Shipper," referenced as a roadmap item — treat as forward-looking/unconfirmed
    rather than a live document type. (Module 06 §7)
30. Whether Peterbilt Atlantic (Atlantic Canada) specifically is a named Decisiv-connected
    dealer — only "Peterbilt of Atlanta" is confirmed by name in Decisiv's own materials; do
    not conflate the two when citing this fact. (Module 06 §7)

## Lane 7 — Competitive landscape and exit economics

31. No primary NADA or ADA published PDF study was directly retrieved — the $3,500–$7,000/
    rooftop DMS cost figure is second-hand via a consulting blog citing "a 2023 NADA study."
32. No direct FTC enforcement docket (as opposed to private Sherman Act litigation) against
    CDK was found — the antitrust history documented in this repo is private litigation
    (Authenticom, the MDL, the dealer-class and vendor-class settlements) and state
    legislative friction (Arizona's Dealer Law), not a formal FTC action.
33. Karmak Fusion, Procede Excede, and CDK Drive Heavy Truck monthly/per-rooftop pricing is not
    publicly published by any of the three vendors.
34. No public document specifies CDK's guaranteed data export format or completeness standard
    upon core DMS contract termination — only third-party trade guidance flags this as a live
    risk. Directly relevant to this repo's own exit-path design.
35. The claim that CDK enterprise contracts offer "discounts approaching 25%" for 10+ rooftop
    groups is sourced only secondhand via a consulting blog — `UNVERIFIED` against a primary
    CDK document.
36. Tekion's and Autosoft's applicability to heavy-duty/commercial-truck dealers specifically
    was not confirmed; both appear light-vehicle-focused based on available material.
37. Exact DMS contract notice-period length for the core dealer (non-API-developer) CDK
    agreement — only the API Licensing Terms' 30-day notice clause is public.
38. The 7-year document-retention rule referenced against the 5-year typical DMS contract term
    lacks a specific jurisdictional statute citation in the source found.
39. **Which DMS Peterbilt Atlantic's 9 sites actually run** — the task brief specifies CDK
    Drive, but lane 7's competitive-landscape research found Karmak Fusion and Procede Excede
    to be the vendors with the most *documented* PACCAR/Peterbilt-specific integrations,
    while CDK Drive Heavy Truck's PACCAR integration depth is comparatively thin in public
    sources. This should be reconciled directly with the client before further build-out (see
    `docs/current-state.md` §1).

## Lane 8 — PACCAR and OEM integration

40. Whether PACCAR is a formal STAR member, or which STAR BODs (if any) PACCAR implements
    versus proprietary/B2B-infrastructure formats.
41. The literal name and any API surface of PACCAR's factory vehicle order-entry system,
    distinct from the public configurators and from OPC — referenced only generically as part
    of "PACCAR's B2B infrastructure." (Module 05 §2, `adapters/paccar/README.md`)
42. PACCAR's specific chart-of-accounts numbering and financial-statement submission deadline
    requirements for dealers — only the general NADA-format norm and the fact of an automated
    month-end statement download to PACCAR are documented. (`docs/current-state.md` §1)
43. Whether "PACCAR's B2B infrastructure" (Karmak's phrase) refers to a single named platform,
    EDI gateway, or a family of point-to-point feeds. (`adapters/paccar/README.md`)
44. Whether TruckTech+/SmartLINQ/PACCAR Connect ever expose a bulk or programmatic data-export
    path to the dealer or fleet owner, versus only portal-based viewing — current evidence
    suggests portal-only, but no source explicitly rules out a bulk path.

---

## Confirmed non-facts — do not reintroduce these anywhere in this repo

- **"PartsPRO" is not a real PACCAR system name.** The real PACCAR dealer parts-ordering
  platform is **Online Parts Counter (OPC)**. (Items 21, 41; `adapters/paccar/README.md`)
- **"VOR" is not confirmed as a North American PACCAR order type.** Confirmed NA order types
  are **Stock, Emergency, MKT, COF** (via Karmak). VOR is confirmed only for PACCAR's
  Australian PDC operations. (Item 21)
- **No formal FTC enforcement action against CDK was found** — the antitrust history in this
  repo is private Sherman Act litigation and state legislative friction, not an FTC docket.
  (Item 32)

---

© 2026 Dany Theriault. EVE "digital stem cell" glyph and glyph-based design principles — all rights reserved. Stewardship of rights of use and assignment for large public and institutional usage rests with the Pacific Utilities Design Council. Published as a time-stamped record of authorship and intent.
