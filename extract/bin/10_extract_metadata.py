#!/usr/bin/env python3
"""
10_extract_metadata.py — pull every schema/definition/setup target.

Status: DOCUMENTED target list (extract/config/targets.yaml, phase=metadata),
UNVERIFIED payload shapes for every `source: export` / `source: screen` target
in this phase (GL account master, accounting schedule, cost-centre/department,
employee master) -- per model.json these have `api_reach: none` or `partial`
with no field-level public schema. This script does NOT invent field names for
those; it emits a stub row per target documenting the gap and defers the real
parse to 40_ingest_exports.py once files exist.

For the one `source: fortellis` metadata target (dealer-rooftop-partition) it
performs the documented Subscriptions API / header-scoping probe pattern.

Metadata always runs before transactions (see extract/README.md, "order of
execution") -- this script has no dependency on 20/30 and should be run second,
right after 00_validate_access.py reports GO.

Usage:
    python3 10_extract_metadata.py [--only ID] [--dry-run]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Extract metadata-phase targets (schema/setup tables).")
    p.add_argument("--only", help="Restrict to a single target id from targets.yaml")
    p.add_argument("--dry-run", action="store_true", help="Do not call any network endpoint; write stub manifests only")
    return p


def extract_fortellis_metadata(target: dict, dry_run: bool) -> list[dict]:
    """dealer-rooftop-partition: Subscriptions API + header inventory.

    UNVERIFIED response shape -- see model.json note: 'no public REST field
    named Company Number'. This function returns one synthetic row per known
    CDK_DEPT_ID_* env var, which is the only DOCUMENTED-reachable signal for
    this entity today (the headers themselves), not a real API payload.
    """
    rows = []
    for site, dept_id in common.department_ids().items():
        rows.append(
            {
                "site": site,
                "department_id": dept_id,
                "subscription_id": common.env("FORTELLIS_SUBSCRIPTION_ID"),
                "source": "env-header-inventory",
                "confidence": "documented",
                "note": (
                    "Row reflects the Subscription-Id/Department-Id header pair "
                    "configured for this harness, not a fetched API payload. "
                    "model.json confirms no public 'Company Number' REST field exists."
                ),
            }
        )
    if not rows:
        rows.append(
            {
                "site": None,
                "department_id": None,
                "note": "No CDK_DEPT_ID_* env vars configured yet.",
                "confidence": "unverified",
            }
        )
    return rows


def extract_stub(target: dict) -> list[dict]:
    """For export/screen-sourced metadata with no field-level schema:
    emit one explicit stub row rather than inventing fields. This is the
    'make the unknown explicit' contract from the task brief.
    """
    return [
        {
            "target_id": target["id"],
            "status": "NOT_YET_INGESTED",
            "reason": (
                f"api_reach={target.get('api_reach')} (source: {target.get('source')}). "
                "No API payload exists for this target per model.json; the real file "
                "must be dropped for 40_ingest_exports.py to parse, or captured by hand "
                "per adapters/export-fallback/README.md."
            ),
            "endpoint_or_screen": target.get("endpoint"),
            "confidence": "unverified",
        }
    ]


def main() -> int:
    args = build_arg_parser().parse_args()
    targets = [t for t in common.load_targets() if t["phase"] == "metadata"]
    if args.only:
        targets = [t for t in targets if t["id"] == args.only]
        if not targets:
            print(f"No metadata target with id={args.only}", file=sys.stderr)
            return 2

    overall_ok = True
    for t in targets:
        out_file = common.out_path(t["output_path"].replace("extract/out/", ""))
        writer = common.NdjsonWriter(target_id=t["id"], output_path=out_file, resume=True)
        try:
            if t["source"] == "fortellis":
                rows = extract_fortellis_metadata(t, args.dry_run)
            else:
                rows = extract_stub(t)
            for row in rows:
                writer.write(row)
            manifest = writer.close(status="ok")
        except Exception as e:  # noqa: BLE001
            manifest = writer.close(status="error")
            manifest.errors.append(str(e))
            overall_ok = False
        print(f"[{t['id']}] rows={manifest.row_count} status={manifest.status} -> {out_file}")

    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
