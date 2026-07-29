#!/usr/bin/env python3
"""
gen_mapping.py — generate the CDK -> SAP field mapping artefact for enterprise architects.

Reads docs/model/fields.json (contract EgD-CDK-FIELDS-v2) and emits:
  schema/mapping/cdk_to_sap_field_map.csv  -- one row per field
  schema/mapping/README.md                 -- human-readable summary + how to read the CSV

Usage:
    python3 gen_mapping.py --fields docs/model/fields.json --out-dir schema/mapping
"""
import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone

CONTRACT = "EgD-CDK-FIELDS-v2"

CSV_COLUMNS = [
    "entity_id",
    "entity_name",
    "cdk_path",
    "legacy_name",
    "datatype",
    "unit",
    "load_column",
    "target_table",
    "sap_analogue_entity",
    "sap_field",
    "confidence",
    "source_url",
]


def eprint(*a, **kw):
    print(*a, file=sys.stderr, **kw)


def main():
    ap = argparse.ArgumentParser(description="Generate the CDK-to-SAP field mapping CSV and README from fields.json.")
    ap.add_argument("--fields", required=True, help="Path to fields.json (or a fixture matching the same shape)")
    ap.add_argument("--out-dir", default="schema/mapping", help="Output directory")
    ap.add_argument("--fixture-note", action="store_true", help="Stamp output as fixture-derived")
    args = ap.parse_args()

    with open(args.fields) as f:
        doc = json.load(f)
    if doc.get("contract") != CONTRACT:
        eprint(f"warning: input contract tag is {doc.get('contract')!r}, expected {CONTRACT!r}")

    entities = doc.get("entities", [])
    os.makedirs(args.out_dir, exist_ok=True)

    csv_path = os.path.join(args.out_dir, "cdk_to_sap_field_map.csv")
    row_count = 0
    conf_counts = {"DOCUMENTED": 0, "INFERRED": 0, "UNVERIFIED": 0}

    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(CSV_COLUMNS)
        for e in entities:
            for fld in e.get("fields", []):
                conf = fld.get("confidence", "UNVERIFIED")
                conf_counts[conf] = conf_counts.get(conf, 0) + 1
                w.writerow([
                    e["entity_id"],
                    e["entity_name"],
                    fld.get("path", ""),
                    fld.get("legacy_name", ""),
                    fld.get("datatype", ""),
                    fld.get("unit") or "",
                    fld.get("load_column", ""),
                    e.get("table_name", ""),
                    e.get("sap_analogue", ""),
                    fld.get("sap_field") or "",
                    conf,
                    fld.get("source_url", ""),
                ])
                row_count += 1

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    source_note = "a Lane F fixture (schema/bin/fixture_fields.py), not the real field dictionary" \
        if args.fixture_note else "[`docs/model/fields.json`](../../docs/model/fields.json)"

    readme_lines = []
    readme_lines.append("# CDK → SAP field map — enterprise architect reference")
    readme_lines.append("")
    readme_lines.append(
        f"Generated {stamp} by [`schema/bin/gen_mapping.py`](../bin/gen_mapping.py) from {source_note}, "
        f"contract `{CONTRACT}`. Regenerate, do not hand-edit."
    )
    readme_lines.append("")
    readme_lines.append(
        "This is the artefact for the operator's enterprise architects: one row per CDK field, "
        "its legacy DMS name, its data type, the column it lands in on load, the SAP field it maps "
        "to in the operator's native vocabulary, and the confidence behind that mapping."
    )
    readme_lines.append("")
    readme_lines.append(f"**Total fields mapped: {row_count} across {len(entities)} entities.**")
    readme_lines.append("")
    readme_lines.append("## Confidence mix (per field, never per object)")
    readme_lines.append("")
    readme_lines.append("| Confidence | Meaning | Count |")
    readme_lines.append("|---|---|---|")
    readme_lines.append(f"| DOCUMENTED | A field-level CDK/Fortellis source states this field exists with this shape | {conf_counts.get('DOCUMENTED',0)} |")
    readme_lines.append(f"| INFERRED | The object is documented but this field's type/length is reasoned from ERP/dealer-accounting convention | {conf_counts.get('INFERRED',0)} |")
    readme_lines.append(f"| UNVERIFIED | Expected but not yet confirmed — to be validated on the CDK admin login | {conf_counts.get('UNVERIFIED',0)} |")
    readme_lines.append("")
    readme_lines.append("## Reading `cdk_to_sap_field_map.csv`")
    readme_lines.append("")
    readme_lines.append("| Column | Meaning |")
    readme_lines.append("|---|---|")
    readme_lines.append("| `entity_id` | Fixed CDK Twin entity id (one of the 21 canonical entities) |")
    readme_lines.append("| `entity_name` | Dealer-facing entity name |")
    readme_lines.append("| `cdk_path` | Literal CDK/Fortellis field path, e.g. `customer.customerId` |")
    readme_lines.append("| `legacy_name` | The DMS legacy/EDI-era field name where documented |")
    readme_lines.append("| `datatype` | Contract datatype (string, integer, decimal, date, datetime, boolean, enum) |")
    readme_lines.append("| `unit` | currency \\| hours \\| quantity \\| percent \\| blank |")
    readme_lines.append("| `load_column` | The snake_case column this field lands in — what the DDL and the extract both key off |")
    readme_lines.append("| `target_table` | The load-ready table name (`schema/ddl/postgres/<entity_id>.sql`) |")
    readme_lines.append("| `sap_analogue_entity` | The SAP object/table set this whole entity maps to |")
    readme_lines.append("| `sap_field` | The specific SAP field analogue, where one exists |")
    readme_lines.append("| `confidence` | DOCUMENTED \\| INFERRED \\| UNVERIFIED, per field |")
    readme_lines.append("| `source_url` | The source document this field's shape was taken from |")
    readme_lines.append("")
    readme_lines.append(
        "See [`cdk_to_sap_field_map.csv`](./cdk_to_sap_field_map.csv) for the full row set, and "
        "[`../ddl/postgres/000_all.sql`](../ddl/postgres/000_all.sql) for the DDL these columns land in."
    )
    readme_lines.append("")
    readme_lines.append(
        "For the object-level (not field-level) CDK-to-SAP mapping narrative, see "
        "[`../README.md`](../README.md)."
    )
    readme_lines.append("")

    readme_path = os.path.join(args.out_dir, "README.md")
    with open(readme_path, "w") as f:
        f.write("\n".join(readme_lines))

    print(f"gen_mapping.py: wrote {row_count} rows to {csv_path}")
    print(f"gen_mapping.py: wrote {readme_path}")
    print(f"gen_mapping.py: confidence mix -> {conf_counts}")


if __name__ == "__main__":
    main()
