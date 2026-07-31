# Widening Policy — sovereign spine field widths

**Status:** active · **Owner:** Lane K (crosswalk/DDL/mapping) · **Applies to:** `docs/model/fields.json`, `docs/model/sap-crosswalk.json`/`.csv`, `schema/ddl/**`, `schema/mapping/**`

## The policy, in one sentence

**The spine keeps SAP semantics with source-native widths.** When a CDK/dealer field is
the genuine structural analogue of a real SAP field, but the CDK value can legitimately
run longer than the 1970s-vintage `CHAR(n)` SAP allows, the spine does **not** truncate
the dealer's real data to fit SAP's field length. It keeps the SAP field as the semantic
anchor (same business meaning, same table-field identity for lineage and mapping
purposes) and emits the column in Postgres/Snowflake DDL at the CDK's own
**source-native length** — never shorter than the data actually requires, and never
silently dropped to force a fit.

This is a widening, not a workaround: it is declared, it is recorded in the register
below, and the validator checks that every widened field carries a matching declaration.
An undeclared truncation risk is still a hard failure. The only thing this policy changes
is that a *properly declared* one is not.

## Why not shorten the dealer data instead?

Because the data is real. A CDK company name field genuinely holds values SAP's
35-character `NAME1` cannot — that is not a data-quality defect in the dealer system, it
is SAP's field being narrower than the businesses it now has to describe. Truncating
`vendorName` or `customerName.companyName` to 35 characters to make a `TRUNCATION_RISK`
disappear would silently corrupt real vendor and customer names on every load. The
spine's job is to carry the dealer's data faithfully while still being legible against
SAP semantics — so the field keeps its SAP identity (for mapping, lineage, and reasoning
about "what SAP concept is this") and its own honest width (for correctness).

## Mechanism

1. Each affected field in `docs/model/fields.json` carries a `widening` block:
   ```json
   "widening": {
     "sap_table": "KNA1",
     "sap_field": "NAME1",
     "sap_length": 35,
     "source_length": 80,
     "widened_length": 80,
     "reason": "..."
   }
   ```
   `widened_length` always equals `source_length` — the DDL never emits anything
   narrower than the CDK's own documented/inferred length. There is no intermediate
   "compromise" width; the SAP length is retained only as the semantic anchor and the
   audit trail, not as a ceiling.

2. `schema/bin/gen_crosswalk.py`'s `compare_types()` reads this block. If a field's CDK
   length exceeds its resolved SAP field's length, and the field carries a `widening`
   block whose `sap_length`/`source_length`/`widened_length` match the actual pair and
   which states a `reason`, the row's `type_verdict` is `WIDENED` (declared, non-fatal)
   instead of `TRUNCATION_RISK` (undeclared, fatal). If the lengths don't line up or the
   block is missing, the row still gets `TRUNCATION_RISK` — declaring a widening for the
   wrong pair does not launder an undeclared one.

3. `schema/bin/validate_crosswalk.py` Check 3 fails the build on any `RESOLVED` row whose
   `type_verdict` is `TRUNCATION_RISK`. It does **not** fail on `WIDENED` rows, but it
   independently re-verifies the widening block's shape (same match rules as step 2)
   before accepting it — a `WIDENED` row with a missing or malformed block is still
   treated as an undeclared truncation risk and fails.

4. `schema/bin/gen_ddl.py` already builds Postgres/Snowflake column widths from the
   CDK field's own `length` (`varchar({length or 255})` for both dialects) — it has never
   read SAP length at all. So DDL output was already source-native by construction; this
   policy makes that behavior explicit and auditable rather than incidental, and the
   `widening` block is the documented reason a given column is wider than its SAP
   analogue when someone reads the DDL next to the crosswalk.

## The register

Every field below is a declared widening: the SAP analogue holds the semantics, the DDL
emits the CDK's own source-native length. 48 fields, generated from
`docs/model/sap-crosswalk.json` after the widening blocks were applied to
`docs/model/fields.json` — regenerate this table by re-running `gen_crosswalk.py` and
filtering rows where `type_verdict == "WIDENED"`. (43 fields were widened in the first
pass; 5 more — `dealer-rooftop-partition.header.subscriptionId`/`.companyNumber`/
`.cmfClientNumber`, `gl-account-master.accountName`, `warranty-claim.claimNumber` —
surfaced once Lane J landed `T000`/`T001`/`SKAT`/`BSID` field definitions in the fresh
Datasphere re-clone and those references resolved for the first time.)

| Entity | Field | SAP ref (semantic anchor) | SAP length | Source (CDK) length | Widened length emitted in DDL |
|---|---|---|---|---|---|
| accounting-schedule | `controlKeyValue` | `BSEG-ZUONR` | 18 | 32 | 32 |
| cost-centre-department | `departmentId` | `CSKS-KOSTL` | 10 | 32 | 32 |
| cost-centre-department | `departmentName` | `CSKT-KTEXT` | 20 | 60 | 60 |
| customer-master | `data[].contactMethods.mobilePhone` | `KNA1-TELF2` | 16 | 20 | 20 |
| customer-master | `data[].contactMethods.primaryPhone` | `KNA1-TELF1` | 16 | 20 | 20 |
| customer-master | `data[].customerId` | `KNA1-KUNNR` | 10 | 32 | 32 |
| customer-master | `data[].customerName.companyName` | `KNA1-NAME1` | 35 | 80 | 80 |
| customer-master | `data[].customerName.firstName` | `KNA1-NAME2` | 35 | 40 | 40 |
| customer-master | `data[].customerName.lastName` | `KNA1-NAME1` | 35 | 40 | 40 |
| customer-master | `data[].hostItemId` | `KNA1-KUNNR` | 10 | 32 | 32 |
| customer-master | `data[].postalAddress.addressLine1` | `KNA1-STRAS` | 35 | 60 | 60 |
| customer-master | `data[].postalAddress.city` | `KNA1-ORT01` | 35 | 40 | 40 |
| customer-master | `data[].postalAddress.country` | `KNA1-LAND1` | 3 | 40 | 40 |
| customer-master | `data[].postalAddress.postalCode` | `KNA1-PSTLZ` | 10 | 15 | 15 |
| customer-master | `data[].postalAddress.state` | `KNA1-REGIO` | 3 | 10 | 10 |
| dealer-rooftop-partition | `cmfClientNumber` | `T000-MANDT` | 3 | 10 | 10 |
| dealer-rooftop-partition | `companyNumber` | `T001-BUKRS` | 4 | 10 | 10 |
| dealer-rooftop-partition | `header.departmentId` | `CSKS-KOSTL` | 10 | 32 | 32 |
| dealer-rooftop-partition | `header.subscriptionId` | `T000-MANDT` | 3 | 64 | 64 |
| gl-account-master | `accountName` | `SKAT-TXT50` | 50 | 60 | 60 |
| gl-journal-posting | `documentNumber` | `BKPF-BELNR` | 10 | 20 | 20 |
| gl-journal-posting | `journalNumber` | `BKPF-BELNR` | 10 | 20 | 20 |
| gl-journal-posting | `scheduleField` | `BSEG-ZUONR` | 18 | 32 | 32 |
| parts-master-inventory | `PartNumber` | `MARA-MATNR` | 18 | 20 | 20 |
| purchase-receipt-document | `movementTypeSapAnalogue` | `MSEG-BWART` | 3 | 4 | 4 |
| purchase-receipt-document | `partNumber` | `EKPO-MATNR` | 18 | 20 | 20 |
| purchase-receipt-document | `purchaseOrderNumber` | `EKKO-EBELN` | 10 | 20 | 20 |
| purchase-receipt-document | `receiptDocumentNumber` | `MKPF-MBLNR` | 10 | 20 | 20 |
| purchase-receipt-document | `vendorId` | `EKKO-LIFNR` | 10 | 20 | 20 |
| repair-order | `data[].roNumber` | `AUFK-AUFNR` | 12 | 20 | 20 |
| ro-labour-line | `data[].operations[].line.laborOperations[].opCode` | `AFVC-STEUS` | 4 | 10 | 10 |
| ro-part-line | `...parts[].number` | `MARA-MATNR` | 18 | 20 | 20 |
| ro-part-line | `...parts[].partClass` | `MARA-MTPOS_MARA` | 4 | 10 | 10 |
| vehicle-master | `vehicleId` | `EQUI-EQUNR` | 18 | 32 | 32 |
| vendor-master | `gstHstNumber` | `LFA1-STCD3` | 18 | 20 | 20 |
| vendor-master | `paymentTerms` | `LFB1-ZTERM` | 4 | 20 | 20 |
| vendor-master | `remitToAddressLine1` | `LFA1-STRAS` | 35 | 60 | 60 |
| vendor-master | `remitToCity` | `LFA1-ORT01` | 35 | 40 | 40 |
| vendor-master | `remitToPostalCode` | `LFA1-PSTLZ` | 10 | 15 | 15 |
| vendor-master | `remitToState` | `LFA1-REGIO` | 3 | 10 | 10 |
| vendor-master | `taxId1099` | `LFA1-STCD1` | 16 | 20 | 20 |
| vendor-master | `vendorId` | `LFA1-LIFNR` | 10 | 20 | 20 |
| vendor-master | `vendorName` | `LFA1-NAME1` | 35 | 80 | 80 |
| warranty-claim | `causalPartNumber` | `MARA-MATNR` | 18 | 20 | 20 |
| warranty-claim | `claimNumber` | `BSID-XBLNR` | 16 | 20 | 20 |
| warranty-claim | `failureCode` | `QMFE-FEGRP` | 8 | 10 | 10 |
| warranty-claim | `roNumber` | `AUFK-AUFNR` | 12 | 20 | 20 |
| warranty-claim | `srtCode` | `AFVC-STEUS` | 4 | 10 | 10 |

### Reading the register

- **Names/addresses/companies (KNA1, LFA1 rows):** SAP's `NAME1`/`NAME2`/`STRAS`/`ORT01`
  are all `CHAR(35)`, a 1970s-era constraint. Real dealer customer, vendor, and company
  names and street addresses routinely exceed that. Widened to CDK's own field length in
  every case (40–80 chars depending on the field).
- **Keys that changed identity space (KNA1-KUNNR, AUFK-AUFNR, EQUI-EQUNR, MARA-MATNR,
  LFA1-LIFNR):** SAP's classic numeric-keyed master-data identifiers (10–18 chars) are
  narrower than the CDK/DMS's own alphanumeric identifiers for the same concept (20–32
  chars). The SAP field is still the right semantic anchor — it is the same "customer
  number" / "material number" concept — but the dealer system's own key format is wider.
- **Free-text / reference fields (BSEG-ZUONR, BKPF-BELNR, LFB1-ZTERM):** SAP's assignment
  and document-number fields (4–18 chars) are narrower than the CDK schedule/document
  reference values (20–32 chars) that get written into them.
- **Codes (AFVC-STEUS, MARA-MTPOS_MARA, MSEG-BWART, QMFE-FEGRP):** short SAP code fields
  (3–8 chars) widened modestly (4–10 chars) to accommodate CDK's own code vocabulary,
  which is not a strict subset of SAP's.

## What this policy does *not* cover

- **PRECISION_MISMATCH** rows (currency/quantity decimal convention mismatches) are a
  separate, non-fatal warning category in `validate_crosswalk.py` — not a widening. There
  are currently zero of these in the crosswalk.
- **NO_SAP_ANALOGUE**, **TABLE_MISSING**, and **TABLE_INVENTORIED_NOT_DEFINED** rows are
  resolution-status gaps, not width gaps. They are tracked in
  `schema/mapping/crosswalk_gaps.md`, not here.
- A field that is merely *shorter* than or equal to its SAP analogue never gets a
  `widening` block — this policy only fires on genuine excess.

## Adding a new widening

1. Confirm the field is a genuine SAP semantic analogue (has a real `TABLE-FIELD`
   reference that resolves), not a `NO_SAP_ANALOGUE` case.
2. Add the `widening` block to the field in `docs/model/fields.json`: `sap_table`,
   `sap_field`, `sap_length` (from the Datasphere canon), `source_length` (the field's own
   `length`), `widened_length` (always equal to `source_length`), and a `reason`.
3. Re-run `schema/bin/gen_crosswalk.py` — the row will reclassify from
   `TRUNCATION_RISK` to `WIDENED` automatically if the block matches.
4. Re-run `schema/bin/validate_crosswalk.py` — it will confirm the block is well-formed.
5. Add the row to the register table above and regenerate DDL (`gen_ddl.py`).

---
Source of truth: [`docs/model/fields.json`](fields.json) ·
[`docs/model/sap-crosswalk.json`](sap-crosswalk.json) ·
[`schema/bin/gen_crosswalk.py`](../../schema/bin/gen_crosswalk.py) ·
[`schema/bin/validate_crosswalk.py`](../../schema/bin/validate_crosswalk.py)
