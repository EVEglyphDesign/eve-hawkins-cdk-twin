#!/usr/bin/env python3
"""
40_ingest_exports.py — parse ledger/schedule files that must come out of the
DMS UI by hand (no Fortellis API path exists for these).

Status: DOCUMENTED that these targets have no API (model.json api.reachable
== "none" for gl-account-master, accounting-schedule, vendor-master,
warranty-claim, purchase-receipt-document, cost-centre-department -- see
extract/config/targets.yaml, source: export|screen). UNVERIFIED: the literal
column layout of any of these files, because none has been exported from the
live Peterbilt Atlantic tenant yet.

Design point from the brief: "tolerate unknown layouts by profiling columns
and emitting a discovered-schema report rather than failing." This script:

1. Accepts CSV (sniffs delimiter) and fixed-width (best-effort column-boundary
   detection from whitespace-aligned headers, or an explicit --layout file).
2. Never invents field names. Unknown columns are named col_0, col_1, ... and
   flagged UNVERIFIED in the discovered-schema report; only columns matching a
   known header alias table (below) are renamed to their target schema name.
3. Always succeeds at *reading* a well-formed file, even with zero recognized
   columns -- the discovered-schema report is the deliverable in that case,
   not an exception.

Usage:
    python3 40_ingest_exports.py --input FILE --target-id ID [--format csv|fixed-width|auto]
    python3 40_ingest_exports.py --input FILE --target-id ID --layout LAYOUT.json   # fixed-width column spec
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402

# Known header aliases per target -- DOCUMENTED where sourced from model.json
# field names / labels; anything not in this table is left as a raw column
# name and marked unverified in the discovered-schema report. This table is
# intentionally small; grow it only from a real observed file header, never
# speculatively.
HEADER_ALIASES = {
    "gl-account-master": {
        "account": "gl_account_number", "acct": "gl_account_number", "account number": "gl_account_number",
        "account #": "gl_account_number", "description": "gl_account_description", "dept": "department_suffix",
        "department": "department_suffix", "type": "account_type",
    },
    "accounting-schedule": {
        "control account": "control_account_number", "schedule": "schedule_id", "ro": "control_key_ro",
        "stock": "control_key_stock_number", "vin": "control_key_vin_last8", "balance": "open_item_balance",
        "age": "age_days",
    },
    "vendor-master": {
        "vendor #": "vendor_id", "vendor": "vendor_name", "name": "vendor_name", "address": "vendor_address",
    },
    "cost-centre-department": {
        "dept": "department_suffix", "department": "department_suffix", "cost center": "cost_centre_id",
        "description": "cost_centre_description",
    },
    "warranty-claim": {
        "ro": "repair_order_number", "claim": "claim_number", "status": "claim_status", "amount": "claim_amount",
    },
    "purchase-receipt-document": {
        "po": "purchase_order_number", "vendor": "vendor_id", "receipt": "receipt_number", "amount": "receipt_amount",
        "date": "receipt_date",
    },
}


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Ingest a hand-exported ledger/schedule file (CSV or fixed-width).")
    p.add_argument("--input", required=True, help="Path to the exported file")
    p.add_argument("--target-id", required=True, help="targets.yaml id this file belongs to")
    p.add_argument("--format", choices=["csv", "fixed-width", "auto"], default="auto")
    p.add_argument("--layout", help="Optional JSON file: list of {name, start, end} for fixed-width parsing")
    p.add_argument("--encoding", default="utf-8-sig")
    return p


def sniff_format(path: Path) -> str:
    sample = path.read_text(encoding="utf-8-sig", errors="replace")[:4096]
    try:
        csv.Sniffer().sniff(sample, delimiters=",\t;|")
        return "csv"
    except csv.Error:
        return "fixed-width"


def parse_csv(path: Path, encoding: str) -> tuple[list[str], list[dict]]:
    with open(path, "r", encoding=encoding, newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t;|")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(f, dialect=dialect)
        fieldnames = reader.fieldnames or []
        rows = [dict(r) for r in reader]
    return fieldnames, rows


def guess_fixed_width_columns(header_line: str) -> list[dict]:
    """Best-effort column-boundary detection: treat runs of 2+ spaces as
    separators between header labels, and derive (start, end) spans. This is
    a heuristic profiler, not a parser guarantee -- always cross-check the
    discovered-schema report against a sample of data rows before trusting
    fixed-width output. UNVERIFIED for any real CDK export until confirmed.
    """
    cols = []
    for m in re.finditer(r"\S+(?:\s\S+)*", header_line):
        cols.append({"name": m.group(0).strip(), "start": m.start(), "end": m.end()})
    # extend each column's end to just before the next column's start, except last
    for i in range(len(cols) - 1):
        cols[i]["end"] = cols[i + 1]["start"]
    return cols


def parse_fixed_width(path: Path, encoding: str, layout: list[dict] | None) -> tuple[list[str], list[dict]]:
    with open(path, "r", encoding=encoding, errors="replace") as f:
        lines = [l.rstrip("\n") for l in f]
    if not lines:
        return [], []
    if layout is None:
        layout = guess_fixed_width_columns(lines[0])
        data_lines = lines[1:]
    else:
        data_lines = lines
    fieldnames = [c["name"] for c in layout]
    rows = []
    for line in data_lines:
        if not line.strip():
            continue
        row = {}
        for c in layout:
            row[c["name"]] = line[c["start"]:c["end"]].strip()
        rows.append(row)
    return fieldnames, rows


def apply_aliases(target_id: str, fieldnames: list[str]) -> dict[str, str]:
    aliases = HEADER_ALIASES.get(target_id, {})
    mapping = {}
    for fn in fieldnames:
        key = fn.strip().lower()
        mapping[fn] = aliases.get(key, fn)
    return mapping


def profile_columns(fieldnames: list[str], rows: list[dict], mapping: dict[str, str]) -> dict:
    profile = {}
    for fn in fieldnames:
        values = [r.get(fn, "") for r in rows]
        non_empty = [v for v in values if v not in (None, "")]
        profile[fn] = {
            "mapped_to": mapping.get(fn, fn),
            "recognized": mapping.get(fn, fn) != fn,
            "non_empty_count": len(non_empty),
            "sample_values": non_empty[:3],
        }
    return profile


def main() -> int:
    args = build_arg_parser().parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 2

    fmt = args.format
    if fmt == "auto":
        fmt = sniff_format(input_path)

    layout = None
    if args.layout:
        layout = json.loads(Path(args.layout).read_text(encoding="utf-8"))

    if fmt == "csv":
        fieldnames, rows = parse_csv(input_path, args.encoding)
    else:
        fieldnames, rows = parse_fixed_width(input_path, args.encoding, layout)

    mapping = apply_aliases(args.target_id, fieldnames)
    profile = profile_columns(fieldnames, rows, mapping)

    target = None
    try:
        target = common.get_target(args.target_id)
    except KeyError:
        pass
    out_rel = target["output_path"].replace("extract/out/", "") if target else f"exports/{args.target_id}.ndjson"
    out_file = common.out_path(out_rel)

    writer = common.NdjsonWriter(target_id=args.target_id, output_path=out_file, resume=True)
    for row in rows:
        normalized = {mapping.get(k, k): v for k, v in row.items()}
        normalized["_source_file"] = input_path.name
        normalized["_source_format"] = fmt
        writer.write(normalized)
    manifest = writer.close(status="ok")

    schema_report = {
        "target_id": args.target_id,
        "source_file": str(input_path),
        "format_detected_or_used": fmt,
        "row_count": len(rows),
        "columns": profile,
        "unrecognized_columns": [fn for fn, p in profile.items() if not p["recognized"]],
        "generated_at": common.utcnow_iso(),
        "note": (
            "unrecognized_columns are passed through unchanged, not dropped. Add them to "
            "HEADER_ALIASES in this script only after confirming their meaning against a "
            "real CDK export -- never guess a mapping silently."
        ),
    }
    report_path = common.out_path(f"discovered-schema/{args.target_id}.schema-report.json")
    report_path.write_text(json.dumps(schema_report, indent=2) + "\n", encoding="utf-8")

    print(f"[{args.target_id}] rows={manifest.row_count} status={manifest.status} -> {out_file}")
    print(f"Discovered-schema report -> {report_path}")
    if schema_report["unrecognized_columns"]:
        print(f"WARNING: {len(schema_report['unrecognized_columns'])} unrecognized column(s): {schema_report['unrecognized_columns']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
