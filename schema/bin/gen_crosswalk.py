#!/usr/bin/env python3
"""
gen_crosswalk.py — generate the machine-checkable CDK-twin <-> SAP-canon crosswalk.

Reads:
  docs/model/fields.json                         (this repo, contract EgD-CDK-FIELDS-v2)
  <datasphere>/schema/sap-modules/*/TABLES.yaml   (table inventories, sovereign repo)
  <datasphere>/schema/sap-modules/*/tables/*.yaml (field-level definitions, sovereign repo)

Emits:
  docs/model/sap-crosswalk.json   (contract EgD-CDK-SAP-XWALK-v1)
  docs/model/sap-crosswalk.csv    (same rows, flat)

For every CDK field that carries a `sap_field` value, this script resolves it against the
SAP canon and records a row with the CDK side, the SAP side, a resolution status, and a
type-compatibility verdict. It does not talk the mapping up or down — a field that cannot
be resolved is reported as such, not silently dropped.

Resolution statuses:
  RESOLVED                       table YAML exists in the canon and the field was found in it
  TABLE_INVENTORIED_NOT_DEFINED  table named in a TABLES.yaml inventory but no field-level
                                  tables/<TABLE>.yaml exists yet (AUFK is the known case)
  TABLE_MISSING                  table not named anywhere in the SAP canon (no inventory entry)
  FIELD_MISSING                  table is defined at the field level, but this field name
                                  is not among its fields
  NO_SAP_ANALOGUE                the CDK field's sap_field value does not parse as a
                                  TABLE-FIELD reference (freeform prose, a bare field name
                                  with no table, or an explicitly analogue-only note) — a
                                  legitimate DMS concept with no crisp SAP handle

Type-compatibility verdicts (only meaningful when RESOLVED):
  OK                    CDK length fits within SAP length, and any currency/quantity
                        decimals convention matches
  TRUNCATION_RISK       CDK field is longer than the SAP field can hold, and no
                        `widening` block is declared on the field in fields.json —
                        an undeclared truncation risk. Fatal in validate_crosswalk.py.
  WIDENED               CDK field is longer than the SAP field can hold, but the field
                        carries a declared `widening` block (docs/model/WIDENING-POLICY.md):
                        the spine keeps SAP semantics with the source-native width. Recorded,
                        not silent — a PASS in validate_crosswalk.py, never a silent drop.
  PRECISION_MISMATCH    CDK field carries currency but SAP field is not 2-decimal CURR,
                        or CDK field carries quantity but SAP field is not 3-decimal QUAN
  N_A                   type compatibility not evaluated (not RESOLVED)

Python 3 stdlib only, plus PyYAML if already installed (falls back to a tiny hand-rolled
YAML reader for the simple, regular shape these files use).

Usage:
    python3 gen_crosswalk.py --fields docs/model/fields.json \\
        --sap-modules ../eve-datasphere-sovereign/schema/sap-modules \\
        --out-dir docs/model
"""
import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timezone

try:
    import yaml as _pyyaml
    HAVE_PYYAML = True
except ImportError:
    HAVE_PYYAML = False

FIELDS_CONTRACT = "EgD-CDK-FIELDS-v2"
XWALK_CONTRACT = "EgD-CDK-SAP-XWALK-v1"

LEDGER_CRITICAL = {
    # (entity_id, path substring) — the fields the validator treats as unresolved = FAIL.
    "repair-order": ["roNumber"],
    "gl-journal-posting": ["journalNumber", "debitAmount", "creditAmount", "postingDate", "journalDate"],
    "accounting-schedule": ["scheduleControlKey", "openItemAmount", "glAccountNumber"],
}


def eprint(*a, **kw):
    print(*a, file=sys.stderr, **kw)


# --------------------------------------------------------------------------------------
# Tiny hand-rolled YAML reader, used only if PyYAML is unavailable. Handles exactly the
# shape used by TABLES.yaml and tables/<TABLE>.yaml in the sovereign repo: a top-level
# scalar map, plus one or two top-level lists of flat scalar maps (`tables:`, `fields:`,
# `foreign_keys:`). Comments (#) and blank lines are ignored. Values are unquoted, `~` is
# treated as None, true/false as booleans, and bare integers as ints.
# --------------------------------------------------------------------------------------

def _scalar(v):
    v = v.strip()
    if v == "" or v == "~" or v.lower() == "null":
        return None
    if v.startswith('"') and v.endswith('"') and len(v) >= 2:
        return v[1:-1]
    if v.startswith("'") and v.endswith("'") and len(v) >= 2:
        return v[1:-1]
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return v


def _strip_comment(line):
    # Strip a trailing # comment, but not one inside quotes.
    out = []
    in_s = in_d = False
    for i, ch in enumerate(line):
        if ch == "'" and not in_d:
            in_s = not in_s
        elif ch == '"' and not in_s:
            in_d = not in_d
        elif ch == "#" and not in_s and not in_d:
            return "".join(out)
        out.append(ch)
    return "".join(out)


def simple_yaml_load(text):
    lines = [_strip_comment(l).rstrip() for l in text.splitlines()]
    result = {}
    current_list_key = None
    current_item = None

    for raw in lines:
        if not raw.strip():
            continue
        stripped = raw.strip()

        # top-level "key:" starting a list (no indent)
        if not raw[0].isspace():
            if stripped.endswith(":"):
                key = stripped[:-1].strip()
                current_list_key = key
                result[key] = []
                current_item = None
                continue
            if ":" in stripped:
                key, _, val = stripped.partition(":")
                result[key.strip()] = _scalar(val)
                current_list_key = None
                current_item = None
                continue
            continue

        # indented list item start: "  - name: X" or "  - key: val"
        m = re.match(r"^(\s*)-\s*(.*)$", raw)
        if m and current_list_key is not None:
            rest = m.group(2)
            current_item = {}
            result[current_list_key].append(current_item)
            if rest.strip():
                if ":" in rest:
                    k, _, v = rest.partition(":")
                    current_item[k.strip()] = _scalar(v)
            continue

        # indented continuation "    key: val" belonging to current_item
        if current_item is not None and ":" in stripped:
            k, _, v = stripped.partition(":")
            current_item[k.strip()] = _scalar(v)
            continue

    return result


def load_yaml_file(path):
    with open(path, "r") as f:
        text = f.read()
    if HAVE_PYYAML:
        try:
            return _pyyaml.safe_load(text)
        except Exception as e:
            eprint(f"warning: PyYAML failed on {path} ({e}), falling back to hand-rolled reader")
    return simple_yaml_load(text)


# --------------------------------------------------------------------------------------
# SAP canon loading
# --------------------------------------------------------------------------------------

def load_sap_canon(sap_modules_dir):
    """
    Returns:
      inventoried: dict table_name -> list of module codes it's named in (TABLES.yaml)
      defined: dict table_name -> {module, path, fields: {field_name: field_dict}}
    """
    inventoried = {}
    defined = {}

    if not os.path.isdir(sap_modules_dir):
        eprint(f"error: sap-modules dir not found: {sap_modules_dir}")
        return inventoried, defined

    for module in sorted(os.listdir(sap_modules_dir)):
        module_dir = os.path.join(sap_modules_dir, module)
        if not os.path.isdir(module_dir):
            continue
        tables_yaml = os.path.join(module_dir, "TABLES.yaml")
        if os.path.isfile(tables_yaml):
            doc = load_yaml_file(tables_yaml) or {}
            mod_code = (doc.get("module") or module).upper()
            for t in doc.get("tables", []) or []:
                name = t.get("name")
                if not name:
                    continue
                inventoried.setdefault(name, []).append(mod_code)

        tables_dir = os.path.join(module_dir, "tables")
        if os.path.isdir(tables_dir):
            for fname in sorted(os.listdir(tables_dir)):
                if not fname.endswith(".yaml"):
                    continue
                fpath = os.path.join(tables_dir, fname)
                doc = load_yaml_file(fpath) or {}
                table_name = doc.get("table") or os.path.splitext(fname)[0]
                fields = {}
                for fld in doc.get("fields", []) or []:
                    fn = fld.get("name")
                    if fn:
                        fields[fn] = fld
                defined[table_name] = {
                    "module": (doc.get("module") or module).upper(),
                    "path": os.path.relpath(fpath),
                    "fields": fields,
                }
                # a defined table is by definition also inventoried by its own module
                inventoried.setdefault(table_name, [])
                if defined[table_name]["module"] not in inventoried[table_name]:
                    inventoried[table_name].append(defined[table_name]["module"])

    return inventoried, defined


# --------------------------------------------------------------------------------------
# sap_field parsing — the CDK fields.json carries sap_field values in several shapes:
#   "AUFK-AUFNR"                              strict TABLE-FIELD
#   "KNA1-KUNNR (alt key)"                    TABLE-FIELD with a trailing annotation
#   "BKPF-BELNR (journal-level)"              TABLE-FIELD with a trailing annotation
#   "MSEG-BWART = 101"                        TABLE-FIELD with a trailing value constraint
#   "PERNR (personnel number analogue)"       bare field name, no table — not resolvable
#   "Client (Mandant) MANDT"                  freeform prose — not resolvable
#   "GM Account 247 (WIP-Labor)"              freeform prose — not resolvable
# --------------------------------------------------------------------------------------

STRICT_RE = re.compile(r"^([A-Z][A-Z0-9_]{1,29})-([A-Z][A-Z0-9_]{1,29})")


def parse_sap_field(raw):
    """
    Returns (table, field, note) if a TABLE-FIELD pair can be extracted, else (None, None, raw).
    `note` carries any trailing annotation/qualifier text found after the core reference.
    """
    if not raw:
        return None, None, None
    s = raw.strip()
    m = STRICT_RE.match(s)
    if m:
        table, field = m.group(1), m.group(2)
        remainder = s[m.end():].strip()
        note = remainder if remainder else None
        return table, field, note
    return None, None, s


# --------------------------------------------------------------------------------------
# Type compatibility
# --------------------------------------------------------------------------------------

CDK_MAX_LEN_BY_TYPE_DEFAULT = None  # CDK length comes from the field itself


def compare_types(cdk_field, sap_field_def):
    """
    Returns (verdict, detail, widening) where verdict in
    {OK, TRUNCATION_RISK, WIDENED, PRECISION_MISMATCH} and `widening` is the
    field's declared widening block (or None).

    Widening policy (docs/model/WIDENING-POLICY.md): the sovereign spine keeps SAP
    semantics with source-native widths. A field whose CDK length exceeds its SAP
    analogue's length is only a fatal TRUNCATION_RISK when the excess is
    *undeclared*. If the field carries a `widening` block recording the SAP length,
    the source length, and the widened length actually emitted in DDL, the same
    excess is a WIDENED pass — declared, not silent.
    """
    cdk_len = cdk_field.get("length")
    cdk_unit = cdk_field.get("unit")
    cdk_datatype = cdk_field.get("datatype")
    widening = cdk_field.get("widening")

    sap_len = sap_field_def.get("length")
    sap_dec = sap_field_def.get("decimals") or 0
    sap_datatype = sap_field_def.get("datatype")

    issues = []
    is_truncation = False

    if isinstance(cdk_len, int) and isinstance(sap_len, int) and cdk_len > sap_len:
        is_truncation = True
        if (
            isinstance(widening, dict)
            and widening.get("sap_length") == sap_len
            and widening.get("source_length") == cdk_len
            and widening.get("widened_length") == cdk_len
            and widening.get("reason")
        ):
            issues.append(
                f"CDK length {cdk_len} > SAP {sap_datatype}({sap_len}) — declared widening "
                f"to {widening.get('widened_length')}, recorded in WIDENING-POLICY.md: "
                f"{widening.get('reason')}"
            )
        else:
            detail = (
                f"CDK length {cdk_len} > SAP {sap_datatype}({sap_len}) — truncation risk"
            )
            if widening is not None:
                detail += (
                    " (a `widening` block is present but does not match this pair "
                    f"— expected sap_length={sap_len}, source_length={cdk_len}, "
                    "widened_length=source_length, plus a reason; treated as undeclared)"
                )
            issues.append(detail)

    if cdk_unit == "currency":
        if sap_datatype != "CURR" or sap_dec != 2:
            issues.append(
                f"CDK field is currency but SAP field is {sap_datatype}"
                f"({sap_len},{sap_dec}) not CURR(_,2) — precision mismatch"
            )
    if cdk_unit == "quantity":
        if sap_datatype not in ("QUAN", "DEC") or sap_dec != 3:
            issues.append(
                f"CDK field is quantity but SAP field is {sap_datatype}"
                f"({sap_len},{sap_dec}) not QUAN/DEC(_,3) — precision mismatch"
            )

    if not issues:
        return "OK", None, None

    precision_issues = [i for i in issues if "precision mismatch" in i]

    if is_truncation:
        declared = (
            isinstance(widening, dict)
            and widening.get("sap_length") == sap_len
            and widening.get("source_length") == cdk_len
            and widening.get("widened_length") == cdk_len
            and widening.get("reason")
        )
        verdict = "WIDENED" if declared else "TRUNCATION_RISK"
        detail = "; ".join(issues)
        return verdict, detail, (widening if declared else None)

    verdict = "PRECISION_MISMATCH"
    return verdict, "; ".join(precision_issues), None


# --------------------------------------------------------------------------------------
# Main crosswalk build
# --------------------------------------------------------------------------------------

def build_rows(fields_doc, inventoried, defined):
    rows = []
    for e in fields_doc.get("entities", []):
        entity_id = e.get("entity_id")
        entity_name = e.get("entity_name")
        for f in e.get("fields", []):
            raw_sap = f.get("sap_field")
            if not raw_sap:
                continue  # only fields that carry a sap_field are in scope for the crosswalk

            table, field, note = parse_sap_field(raw_sap)

            row = {
                "cdk_entity_id": entity_id,
                "cdk_entity_name": entity_name,
                "cdk_path": f.get("path"),
                "cdk_load_column": f.get("load_column"),
                "cdk_datatype": f.get("datatype"),
                "cdk_length": f.get("length"),
                "cdk_unit": f.get("unit"),
                "cdk_confidence": f.get("confidence"),
                "sap_field_raw": raw_sap,
                "sap_table": table,
                "sap_field": field,
                "sap_annotation": note if table else None,
                "sap_data_element": None,
                "sap_datatype": None,
                "sap_length": None,
                "sap_decimals": None,
                "sap_is_key": None,
                "sap_module": None,
                "status": None,
                "type_verdict": "N_A",
                "type_detail": None,
                "resolution_detail": None,
                "widening": None,
            }

            if table is None:
                row["status"] = "NO_SAP_ANALOGUE"
                row["resolution_detail"] = (
                    f"sap_field value {raw_sap!r} does not parse as TABLE-FIELD; "
                    "treated as a dealer/DMS concept without a crisp SAP handle."
                )
                rows.append(row)
                continue

            if table not in inventoried and table not in defined:
                row["status"] = "TABLE_MISSING"
                row["resolution_detail"] = (
                    f"{table} is not named in any schema/sap-modules/*/TABLES.yaml inventory."
                )
                rows.append(row)
                continue

            if table not in defined:
                mods = inventoried.get(table, [])
                row["status"] = "TABLE_INVENTORIED_NOT_DEFINED"
                row["sap_module"] = ",".join(mods) if mods else None
                row["resolution_detail"] = (
                    f"{table} is named in TABLES.yaml ({','.join(mods) or 'unknown module'}) "
                    "but has no field-level tables/<TABLE>.yaml yet."
                )
                rows.append(row)
                continue

            tdef = defined[table]
            row["sap_module"] = tdef["module"]
            fdef = tdef["fields"].get(field)
            if fdef is None:
                row["status"] = "FIELD_MISSING"
                row["resolution_detail"] = (
                    f"{table} is defined at {tdef['path']} but has no field named {field}."
                )
                rows.append(row)
                continue

            row["status"] = "RESOLVED"
            row["sap_data_element"] = fdef.get("data_element")
            row["sap_datatype"] = fdef.get("datatype")
            row["sap_length"] = fdef.get("length")
            row["sap_decimals"] = fdef.get("decimals")
            row["sap_is_key"] = bool(fdef.get("key"))
            row["resolution_detail"] = f"resolved against {tdef['path']}"

            verdict, detail, widening = compare_types(f, fdef)
            row["type_verdict"] = verdict
            row["type_detail"] = detail
            row["widening"] = widening

            rows.append(row)

    return rows


def summarize(rows):
    by_status = {}
    by_module = {}
    type_mismatch = 0
    for r in rows:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1
        mod = r.get("sap_module") or "UNRESOLVED"
        by_module[mod] = by_module.get(mod, 0) + 1
        if r["type_verdict"] in ("TRUNCATION_RISK", "PRECISION_MISMATCH"):
            type_mismatch += 1
    widened_count = sum(1 for r in rows if r["type_verdict"] == "WIDENED")
    return {
        "total_rows": len(rows),
        "by_status": dict(sorted(by_status.items())),
        "by_module": dict(sorted(by_module.items())),
        "type_mismatch_count": type_mismatch,
        "widened_count": widened_count,
    }


CSV_COLUMNS = [
    "cdk_entity_id", "cdk_entity_name", "cdk_path", "cdk_load_column",
    "cdk_datatype", "cdk_length", "cdk_unit", "cdk_confidence",
    "sap_field_raw", "sap_table", "sap_field", "sap_annotation",
    "sap_module", "sap_data_element", "sap_datatype", "sap_length",
    "sap_decimals", "sap_is_key", "status", "type_verdict", "type_detail",
    "resolution_detail", "widened_length", "widening_reason",
]


def main():
    ap = argparse.ArgumentParser(
        description="Generate the CDK-twin <-> SAP-canon crosswalk (docs/model/sap-crosswalk.json + .csv)."
    )
    ap.add_argument("--fields", default="docs/model/fields.json", help="Path to fields.json")
    ap.add_argument(
        "--sap-modules",
        default="../eve-datasphere-sovereign/schema/sap-modules",
        help="Path to the sovereign repo's schema/sap-modules directory",
    )
    ap.add_argument("--out-dir", default="docs/model", help="Output directory for sap-crosswalk.json/.csv")
    args = ap.parse_args()

    with open(args.fields) as f:
        fields_doc = json.load(f)
    if fields_doc.get("contract") != FIELDS_CONTRACT:
        eprint(f"warning: input contract tag is {fields_doc.get('contract')!r}, expected {FIELDS_CONTRACT!r}")

    inventoried, defined = load_sap_canon(args.sap_modules)
    if not inventoried and not defined:
        eprint("error: SAP canon appears empty — check --sap-modules path")
        sys.exit(2)

    rows = build_rows(fields_doc, inventoried, defined)
    summary = summarize(rows)

    os.makedirs(args.out_dir, exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_doc = {
        "generated": stamp,
        "contract": XWALK_CONTRACT,
        "source": {
            "cdk_fields": args.fields,
            "cdk_fields_contract": fields_doc.get("contract"),
            "sap_modules_dir": args.sap_modules,
        },
        "summary": summary,
        "rows": rows,
    }

    json_path = os.path.join(args.out_dir, "sap-crosswalk.json")
    with open(json_path, "w") as f:
        json.dump(out_doc, f, indent=2)
        f.write("\n")

    csv_path = os.path.join(args.out_dir, "sap-crosswalk.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        w.writeheader()
        for r in rows:
            flat = dict(r)
            widening = r.get("widening") or {}
            flat["widened_length"] = widening.get("widened_length")
            flat["widening_reason"] = widening.get("reason")
            w.writerow({k: ("" if flat.get(k) is None else flat.get(k)) for k in CSV_COLUMNS})

    eprint(f"wrote {json_path} ({len(rows)} rows)")
    eprint(f"wrote {csv_path}")
    eprint(f"summary: {json.dumps(summary)}")


if __name__ == "__main__":
    main()
