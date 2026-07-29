#!/usr/bin/env python3
"""
90_counts.py — integrity control totals per class.

Status: DOCUMENTED harness-internal control-total logic (row counts, min/max
timestamps, SHA-256 per output file, read straight from each script's
.manifest.json sidecar written by extract/lib/common.NdjsonWriter). This is
NOT a financial tie-out (that lives in the tie-out workstream referenced in
the brief, module/reporting lanes) -- this script only proves the extract
harness itself moved the rows it claims to have moved, per target and phase.

Run this LAST, after 00/10/20/30/40, as the go/no-go gate before handing
output to the tie-out step.

Usage:
    python3 90_counts.py [--phase metadata|masters|transactions|ledger]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Print/write integrity control totals per extract target.")
    p.add_argument("--phase", choices=["metadata", "masters", "transactions", "ledger"], help="Restrict to one phase")
    return p


def main() -> int:
    args = build_arg_parser().parse_args()
    targets = common.load_targets()
    if args.phase:
        targets = [t for t in targets if t["phase"] == args.phase]

    control_totals = []
    for t in targets:
        out_file = common.out_path(t["output_path"].replace("extract/out/", ""))
        manifest_file = out_file.with_suffix(out_file.suffix + ".manifest.json")
        entry = {
            "target_id": t["id"],
            "phase": t["phase"],
            "source": t["source"],
            "api_reach": t.get("api_reach"),
            "output_path": str(out_file),
            "output_exists": out_file.exists(),
            "manifest_exists": manifest_file.exists(),
        }
        if manifest_file.exists():
            m = json.loads(manifest_file.read_text(encoding="utf-8"))
            entry.update(
                {
                    "row_count": m.get("row_count"),
                    "min_timestamp": m.get("min_timestamp"),
                    "max_timestamp": m.get("max_timestamp"),
                    "sha256": m.get("sha256"),
                    "status": m.get("status"),
                    "errors": m.get("errors"),
                }
            )
        else:
            entry.update({"row_count": 0, "status": "NOT_RUN"})
        control_totals.append(entry)

    report = {
        "generated_at": common.utcnow_iso(),
        "phase_filter": args.phase,
        "targets": control_totals,
        "summary": {
            "total_targets": len(control_totals),
            "targets_with_output": sum(1 for e in control_totals if e["output_exists"]),
            "targets_not_run": sum(1 for e in control_totals if e["status"] == "NOT_RUN"),
            "targets_with_errors": sum(1 for e in control_totals if e.get("errors")),
            "total_rows": sum(e.get("row_count") or 0 for e in control_totals),
        },
    }

    out_path = common.out_path("90_counts.report.json")
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report["summary"], indent=2))
    print(f"Full report -> {out_path}")
    for e in control_totals:
        flag = "OK" if e["output_exists"] and not e.get("errors") else "!!"
        print(f"  [{flag}] {e['target_id']:<28} phase={e['phase']:<13} rows={e.get('row_count', 0):<8} status={e.get('status')}")

    return 1 if report["summary"]["targets_with_errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
