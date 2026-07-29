#!/usr/bin/env python3
"""
20_extract_masters.py — pull master-data targets (customer, vehicle, vendor,
parts master/inventory, parts order/supersession).

Status: DOCUMENTED endpoints for customer-master (CDK Drive Get Customer v3)
and parts-master-inventory (CDK Drive Async Parts Inventory API, bulk).
UNVERIFIED field-level response schema for vehicle-master (no stock number in
documented schema per model.json) and parts-order-supersession (workflow-level
only). vendor-master has `api_reach: none` -- no stub network call is made for
it; see extract/README.md and adapters/export-fallback/README.md.

Fortellis bulk APIs follow the async start -> poll -> pull pattern documented
in adapters/cdk-fortellis/README.md. This script implements that loop once and
reuses it per target. UNVERIFIED: exact operation names/paths (model.json /
open-questions.md item 2) -- placeholders below are marked accordingly.

Usage:
    python3 20_extract_masters.py [--only ID] [--dry-run]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402

DEFAULT_BASE_URL = "https://api.fortellis.io"

# UNVERIFIED exact resource path per target -- documented only at the API-name
# level (see model.json api.endpoints); confirm real paths against the live
# OpenAPI spec before removing this UNVERIFIED marker.
RESOURCE_PATH = {
    "customer-master": "/cdk/v3/customers/bulk",
    "vehicle-master": "/cdk/service-vehicles/bulk",
    "parts-master-inventory": "/cdk/parts/inventory/async/bulk",
    "parts-order-supersession": "/cdk/parts/orders/bulk",
}


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Extract master-data targets via Fortellis async bulk pattern.")
    p.add_argument("--only", help="Restrict to a single target id from targets.yaml")
    p.add_argument("--dry-run", action="store_true", help="Skip network calls; write a stub row per target")
    p.add_argument("--base-url", default=DEFAULT_BASE_URL)
    p.add_argument("--poll-interval", type=float, default=5.0)
    p.add_argument("--poll-timeout", type=float, default=600.0)
    return p


def async_bulk_pull(base_url: str, resource_path: str, token: str, subscription_id: str, department_id: str,
                     poll_interval: float, poll_timeout: float) -> list[dict]:
    """DOCUMENTED pattern: POST start -> GET long-operations/{id}/status (poll)
    -> GET long-operations/{id}/result. UNVERIFIED exact field names in the
    status/result envelopes -- this function only assumes `operationId`,
    `status` in {"READY","PENDING","FAILED"}, and a `results`/`data` list in
    the result body, per common third-party Fortellis integration guides.
    Falls back to raising HttpError with actionable status if any assumption
    breaks, rather than guessing further.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Subscription-Id": subscription_id,
        "Department-Id": department_id,
        "Request-Id": f"20-extract-masters-{int(time.time())}",
    }
    start = common.request_with_backoff("POST", f"{base_url}{resource_path}", headers=headers, max_retries=3)
    op = start.json()
    operation_id = op.get("operationId") or op.get("id")
    if not operation_id:
        raise RuntimeError(
            "UNVERIFIED response shape: no operationId/id found in bulk-start response. "
            "Inspect the raw payload and update this function -- do not guess field names."
        )

    status_url = f"{base_url}{resource_path.rsplit('/bulk', 1)[0]}/long-operations/{operation_id}/status"
    deadline = time.time() + poll_timeout
    while time.time() < deadline:
        status_resp = common.request_with_backoff("GET", status_url, headers=headers, max_retries=3)
        status_body = status_resp.json()
        state = status_body.get("status")
        if state == "READY":
            break
        if state == "FAILED":
            raise RuntimeError(f"Bulk operation failed: {status_body}")
        time.sleep(poll_interval)
    else:
        raise TimeoutError(f"Bulk operation {operation_id} did not become READY within {poll_timeout}s")

    result_url = f"{base_url}{resource_path.rsplit('/bulk', 1)[0]}/long-operations/{operation_id}/result"
    result_resp = common.request_with_backoff("GET", result_url, headers=headers, max_retries=3)
    body = result_resp.json()
    rows = body.get("results") or body.get("data") or []
    if not isinstance(rows, list):
        raise RuntimeError("UNVERIFIED response shape: result body has no list under results/data.")
    return rows


def main() -> int:
    args = build_arg_parser().parse_args()
    targets = [t for t in common.load_targets() if t["phase"] == "masters"]
    if args.only:
        targets = [t for t in targets if t["id"] == args.only]
        if not targets:
            print(f"No masters target with id={args.only}", file=sys.stderr)
            return 2

    token = None
    subscription_id = common.env("FORTELLIS_SUBSCRIPTION_ID")
    dept_ids = common.department_ids()

    overall_ok = True
    for t in targets:
        out_file = common.out_path(t["output_path"].replace("extract/out/", ""))
        writer = common.NdjsonWriter(
            target_id=t["id"],
            output_path=out_file,
            dedupe_key=lambda r: str(r.get("id") or r.get("customerId") or r.get("vehicleId") or r.get("partNumber") or r),
        )
        try:
            if t["source"] != "fortellis":
                writer.write(
                    {
                        "target_id": t["id"],
                        "status": "NOT_YET_INGESTED",
                        "reason": f"source={t['source']}, api_reach={t.get('api_reach')} -- see adapters/export-fallback/README.md",
                    }
                )
                manifest = writer.close(status="skipped-non-api-source")
            elif args.dry_run or not (token and subscription_id and dept_ids):
                writer.write({"target_id": t["id"], "status": "DRY_RUN_OR_NO_CREDS", "endpoint": t["endpoint"]})
                manifest = writer.close(status="dry-run")
            else:
                resource_path = RESOURCE_PATH.get(t["id"])
                if not resource_path:
                    raise RuntimeError(f"No RESOURCE_PATH mapping for {t['id']} -- add it, do not guess inline.")
                for site, dept_id in dept_ids.items():
                    rows = async_bulk_pull(
                        args.base_url, resource_path, token, subscription_id, dept_id,
                        args.poll_interval, args.poll_timeout,
                    )
                    for row in rows:
                        row["_site"] = site
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
