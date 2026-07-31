#!/usr/bin/env python3
"""
validate_crosswalk.py — fail loudly on gaps that would break the SAP tie-out.

Reads docs/model/sap-crosswalk.json (contract EgD-CDK-SAP-XWALK-v1) and docs/model/fields.json
(contract EgD-CDK-FIELDS-v2), and fails (non-zero exit) if:

  1. Any CDK entity that carries at least one sap_field reference has ZERO rows that
     resolved (status == RESOLVED). An entity with sap_field annotations but no resolved
     SAP reference at all means the crosswalk is decorative for that entity.
  2. Any ledger-critical field is unresolved. Ledger-critical = repair order key
     (repair-order key fields), GL journal amount/account/date (gl-journal-posting
     debit/credit amount, GL account, posting date), and schedule control key / open
     amount (accounting-schedule control key fields and open item amount). "Unresolved"
     means: no sap_field at all, or a sap_field present but status != RESOLVED.
  3. Any RESOLVED pair carries a TRUNCATION_RISK type verdict.

This validator does not evaluate PRECISION_MISMATCH as fatal on its own (surfaced as a
warning) because a currency/quantity precision mismatch is routinely fixable at load time
with a cast, whereas truncation silently drops data. Ledger-critical failures and
truncation risk are load-breaking; precision mismatches are load-review items.

Exit code 0 = pass. Exit code 1 = fail (real gaps reported). Exit code 2 = usage/input error.

Usage:
    python3 validate_crosswalk.py --crosswalk docs/model/sap-crosswalk.json \\
        --fields docs/model/fields.json
"""
import argparse
import json
import sys

CROSSWALK_CONTRACT = "EgD-CDK-SAP-XWALK-v1"
FIELDS_CONTRACT = "EgD-CDK-FIELDS-v2"

# Ledger-critical fields, keyed by CDK entity_id, matched by path substring.
# These are the fields named explicitly in ALIGNMENT_BRIEF.md as the ones the ledger
# tie-out cannot proceed without: the repair order key, GL journal amount/account/date,
# and the schedule control key / open amount.
LEDGER_CRITICAL = [
    ("repair-order", "data[].roNumber", "repair order key"),
    ("gl-journal-posting", "debitAmount", "GL journal debit amount"),
    ("gl-journal-posting", "creditAmount", "GL journal credit amount"),
    ("gl-journal-posting", "glAccountNumber", "GL journal account"),
    ("gl-journal-posting", "postingDate", "GL journal posting date"),
    ("accounting-schedule", "controlKeyType", "schedule control key (type)"),
    ("accounting-schedule", "controlKeyValue", "schedule control key (value)"),
    ("accounting-schedule", "openItemAmount", "schedule open amount"),
]


def eprint(*a, **kw):
    print(*a, file=sys.stderr, **kw)


def load_json(path):
    with open(path) as f:
        return json.load(f)


def index_crosswalk_by_entity_path(rows):
    idx = {}
    for r in rows:
        idx.setdefault((r["cdk_entity_id"], r["cdk_path"]), []).append(r)
    return idx


def main():
    ap = argparse.ArgumentParser(
        description="Validate the CDK<->SAP crosswalk: entity coverage, ledger-critical "
        "resolution, and truncation risk. Fails loudly on real gaps."
    )
    ap.add_argument("--crosswalk", default="docs/model/sap-crosswalk.json", help="Path to sap-crosswalk.json")
    ap.add_argument("--fields", default="docs/model/fields.json", help="Path to fields.json")
    args = ap.parse_args()

    try:
        xwalk = load_json(args.crosswalk)
    except (OSError, json.JSONDecodeError) as e:
        eprint(f"error: cannot read crosswalk {args.crosswalk}: {e}")
        sys.exit(2)

    try:
        fields_doc = load_json(args.fields)
    except (OSError, json.JSONDecodeError) as e:
        eprint(f"error: cannot read fields {args.fields}: {e}")
        sys.exit(2)

    if xwalk.get("contract") != CROSSWALK_CONTRACT:
        eprint(f"warning: crosswalk contract tag is {xwalk.get('contract')!r}, expected {CROSSWALK_CONTRACT!r}")
    if fields_doc.get("contract") != FIELDS_CONTRACT:
        eprint(f"warning: fields contract tag is {fields_doc.get('contract')!r}, expected {FIELDS_CONTRACT!r}")

    rows = xwalk.get("rows", [])
    by_entity_path = index_crosswalk_by_entity_path(rows)

    failures = []
    warnings = []

    # --- Check 1: every entity with at least one sap_field row must have >=1 RESOLVED row.
    entities_with_sap_field = {}
    for r in rows:
        entities_with_sap_field.setdefault(r["cdk_entity_id"], []).append(r)

    for entity_id, entity_rows in sorted(entities_with_sap_field.items()):
        resolved = [r for r in entity_rows if r["status"] == "RESOLVED"]
        if not resolved:
            statuses = sorted(set(r["status"] for r in entity_rows))
            failures.append(
                f"[coverage] entity {entity_id!r} has {len(entity_rows)} sap_field reference(s) "
                f"but ZERO resolved against the SAP canon (statuses present: {statuses})."
            )

    # --- Check 2: ledger-critical fields must be RESOLVED.
    for entity_id, path_substr, label in LEDGER_CRITICAL:
        matches = []
        for (e_id, path), rlist in by_entity_path.items():
            if e_id == entity_id and path and path_substr in path:
                matches.extend(rlist)

        if not matches:
            failures.append(
                f"[ledger-critical] {label} ({entity_id}.*{path_substr}*) has NO sap_field "
                "reference at all in the crosswalk — cannot tie out to SAP."
            )
            continue

        resolved = [m for m in matches if m["status"] == "RESOLVED"]
        if not resolved:
            statuses = sorted(set(m["status"] for m in matches))
            raws = sorted(set(m.get("sap_field_raw") or "" for m in matches))
            failures.append(
                f"[ledger-critical] {label} ({entity_id}.*{path_substr}*) is UNRESOLVED "
                f"(status={statuses}, sap_field_raw={raws})."
            )

    # --- Check 3: any RESOLVED pair with TRUNCATION_RISK is fatal.
    truncation_rows = [r for r in rows if r["status"] == "RESOLVED" and r["type_verdict"] == "TRUNCATION_RISK"]
    for r in truncation_rows:
        failures.append(
            f"[truncation] {r['cdk_entity_id']}.{r['cdk_path']} -> {r['sap_table']}-{r['sap_field']}: "
            f"{r['type_detail']}"
        )

    # --- Non-fatal: precision mismatches, surfaced as warnings.
    precision_rows = [r for r in rows if r["status"] == "RESOLVED" and r["type_verdict"] == "PRECISION_MISMATCH"]
    for r in precision_rows:
        warnings.append(
            f"[precision] {r['cdk_entity_id']}.{r['cdk_path']} -> {r['sap_table']}-{r['sap_field']}: "
            f"{r['type_detail']}"
        )

    print(f"Crosswalk validation — {len(rows)} rows checked from {args.crosswalk}")
    print(f"  entities with sap_field references: {len(entities_with_sap_field)}")
    print(f"  ledger-critical fields checked: {len(LEDGER_CRITICAL)}")
    print(f"  truncation-risk rows: {len(truncation_rows)}")
    print(f"  precision-mismatch rows (warning only): {len(precision_rows)}")
    print()

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
        print()

    if failures:
        print(f"FAIL — {len(failures)} blocking issue(s):")
        for fmsg in failures:
            print(f"  - {fmsg}")
        sys.exit(1)

    print("PASS — no blocking gaps found.")
    sys.exit(0)


if __name__ == "__main__":
    main()
