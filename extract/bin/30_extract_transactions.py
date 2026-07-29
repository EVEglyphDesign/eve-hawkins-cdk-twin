#!/usr/bin/env python3
"""
30_extract_transactions.py — pull transaction-class targets for a date window.

Status: DOCUMENTED endpoint for the richest object on the platform, CDK Drive
Get Repair Order v3 (repair-order, ro-labour-line, ro-part-line,
technician-time-punch all nest inside this one call, per model.json). Other
transaction targets in this phase (parts-pick-ticket, counter-parts-sale,
deal-jacket-vehicle-sale) are `partial`/documented-at-workflow-level only;
warranty-claim is `none` (no API) and is skipped here -- see
adapters/export-fallback/README.md and 40_ingest_exports.py.

Default window: prior three full months, per the brief's worked example
(May/June/July 2026 when run in July 2026) -- see
extract/lib/common.py:prior_three_full_months. Override with --from/--to.

Resumable: re-running with the same window and target continues appending
new rows and skips rows already captured (dedupe on repairOrderNumber /
per-target natural key) -- see extract/lib/common.NdjsonWriter.

Rate-limit aware: uses extract/lib/common.request_with_backoff, which honors
Retry-After on 429 and backs off exponentially on 5xx. 401/403 abort
immediately (auth problem, not a rate limit) -- see extract/README.md.

Usage:
    python3 30_extract_transactions.py [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--only ID] [--dry-run]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402

DEFAULT_BASE_URL = "https://api.fortellis.io"

# UNVERIFIED exact resource path -- see model.json api.endpoints for the
# documented API *names* only; the literal REST path is inferred from common
# Fortellis URL conventions and must be confirmed against the live spec.
RESOURCE_PATH = {
    "repair-order": "/cdk/v3/repair-orders",  # nested labor/parts/punches come along in one response
    "parts-pick-ticket": "/cdk/parts/pick-tickets",
    "counter-parts-sale": "/cdk/parts/sales",
    "deal-jacket-vehicle-sale": "/cdk/fi/sales-history/delta",
}

# repair-order response is expected (per model.json) to carry laborOperations[],
# parts[], and technicianPunchTimes[] nested arrays -- these three targets are
# derived from the SAME repair-order payload, not fetched separately.
DERIVED_FROM_REPAIR_ORDER = {"ro-labour-line", "ro-part-line", "technician-time-punch"}


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Extract transaction-class targets for a date window (repair orders, parts sales, deal jackets, etc.)."
    )
    p.add_argument("--from", dest="date_from", help="Window start (YYYY-MM-DD). Default: prior three full months.")
    p.add_argument("--to", dest="date_to", help="Window end (YYYY-MM-DD). Default: prior three full months.")
    p.add_argument("--only", help="Restrict to a single target id from targets.yaml")
    p.add_argument("--dry-run", action="store_true", help="Skip network calls; write a stub row per target")
    p.add_argument("--base-url", default=DEFAULT_BASE_URL)
    p.add_argument("--page-size", type=int, default=100)
    return p


def fetch_repair_orders_page(base_url, token, subscription_id, department_id, date_from, date_to, page, page_size):
    """UNVERIFIED pagination params -- guessing `page`/`pageSize`/`updatedFrom`/
    `updatedTo` as the most common REST convention; Get Repair Order v3's real
    query parameters are documented only at the field level for the response
    body in public material, not the request query string. Confirm against
    the live OpenAPI spec and update this function's `params` dict -- do not
    silently rename fields elsewhere in the pipeline to compensate.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Subscription-Id": subscription_id,
        "Department-Id": department_id,
        "Request-Id": f"30-extract-tx-{int(time.time())}-{page}",
    }
    params = {
        "updatedFrom": date_from,
        "updatedTo": date_to,
        "page": page,
        "pageSize": page_size,
    }
    resp = common.request_with_backoff("GET", f"{base_url}{RESOURCE_PATH['repair-order']}", headers=headers, params=params, max_retries=6)
    body = resp.json()
    rows = body.get("results") or body.get("data") or body.get("repairOrders") or []
    if not isinstance(rows, list):
        raise RuntimeError("UNVERIFIED response shape: no list found under results/data/repairOrders.")
    has_more = bool(body.get("hasMore") or (len(rows) == page_size))
    return rows, has_more


def main() -> int:
    args = build_arg_parser().parse_args()
    date_from = args.date_from
    date_to = args.date_to
    if not date_from or not date_to:
        default_from, default_to = common.prior_three_full_months()
        date_from = date_from or default_from
        date_to = date_to or default_to

    all_targets = {t["id"]: t for t in common.load_targets() if t["phase"] == "transactions"}
    requested_ids = [args.only] if args.only else list(all_targets.keys())

    subscription_id = common.env("FORTELLIS_SUBSCRIPTION_ID")
    dept_ids = common.department_ids()
    token = None  # obtained via 00_validate_access.py's flow; wire in real token retrieval here

    overall_ok = True

    ro_writer = None
    labour_writer = None
    parts_writer = None
    punch_writer = None

    if "repair-order" in requested_ids and all_targets["repair-order"]["source"] == "fortellis":
        t = all_targets["repair-order"]
        ro_writer = common.NdjsonWriter(
            "repair-order", common.out_path(t["output_path"].replace("extract/out/", "")),
            timestamp_field="updatedAt", dedupe_key=lambda r: str(r.get("repairOrderNumber")),
        )
    if "ro-labour-line" in requested_ids:
        t = all_targets["ro-labour-line"]
        labour_writer = common.NdjsonWriter(
            "ro-labour-line", common.out_path(t["output_path"].replace("extract/out/", "")),
            dedupe_key=lambda r: f"{r.get('repairOrderNumber')}::{r.get('opCode')}::{r.get('lineNumber')}",
        )
    if "ro-part-line" in requested_ids:
        t = all_targets["ro-part-line"]
        parts_writer = common.NdjsonWriter(
            "ro-part-line", common.out_path(t["output_path"].replace("extract/out/", "")),
            dedupe_key=lambda r: f"{r.get('repairOrderNumber')}::{r.get('partNumber')}::{r.get('lineNumber')}",
        )
    if "technician-time-punch" in requested_ids:
        t = all_targets["technician-time-punch"]
        punch_writer = common.NdjsonWriter(
            "technician-time-punch", common.out_path(t["output_path"].replace("extract/out/", "")),
            dedupe_key=lambda r: f"{r.get('repairOrderNumber')}::{r.get('technicianId')}::{r.get('startTime')}",
        )

    try:
        if ro_writer is not None:
            if args.dry_run or not (token and subscription_id and dept_ids):
                ro_writer.write({"target_id": "repair-order", "status": "DRY_RUN_OR_NO_CREDS", "from": date_from, "to": date_to})
            else:
                for site, dept_id in dept_ids.items():
                    page = 1
                    while True:
                        rows, has_more = fetch_repair_orders_page(
                            args.base_url, token, subscription_id, dept_id, date_from, date_to, page, args.page_size
                        )
                        for ro in rows:
                            ro["_site"] = site
                            ro_writer.write(ro)
                            for lab in ro.get("laborOperations", []) or []:
                                lab["repairOrderNumber"] = ro.get("repairOrderNumber")
                                if labour_writer:
                                    labour_writer.write(lab)
                            for part in ro.get("parts", []) or []:
                                part["repairOrderNumber"] = ro.get("repairOrderNumber")
                                if parts_writer:
                                    parts_writer.write(part)
                            for punch in ro.get("technicianPunchTimes", []) or []:
                                punch["repairOrderNumber"] = ro.get("repairOrderNumber")
                                if punch_writer:
                                    punch_writer.write(punch)
                        if not has_more:
                            break
                        page += 1
            manifest = ro_writer.close(status="ok")
            print(f"[repair-order] rows={manifest.row_count} status={manifest.status}")
    except Exception as e:  # noqa: BLE001
        if ro_writer:
            m = ro_writer.close(status="error")
            m.errors.append(str(e))
        overall_ok = False
        print(f"[repair-order] ERROR: {e}", file=sys.stderr)

    for writer, name in [(labour_writer, "ro-labour-line"), (parts_writer, "ro-part-line"), (punch_writer, "technician-time-punch")]:
        if writer is not None:
            m = writer.close(status="ok")
            print(f"[{name}] rows={m.row_count} status={m.status}")

    # Remaining partial/workflow-level transaction targets: emit explicit stubs.
    for tid in requested_ids:
        if tid == "repair-order" or tid in DERIVED_FROM_REPAIR_ORDER:
            continue
        t = all_targets[tid]
        out_file = common.out_path(t["output_path"].replace("extract/out/", ""))
        w = common.NdjsonWriter(tid, out_file)
        if t["source"] != "fortellis":
            w.write({"target_id": tid, "status": "NOT_YET_INGESTED", "reason": f"source={t['source']} -- see adapters/export-fallback/README.md"})
            m = w.close(status="skipped-non-api-source")
        else:
            w.write({"target_id": tid, "status": "STUB_UNVERIFIED_ENDPOINT", "endpoint": t["endpoint"], "from": date_from, "to": date_to})
            m = w.close(status="stub")
        print(f"[{tid}] rows={m.row_count} status={m.status} -> {out_file}")

    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
