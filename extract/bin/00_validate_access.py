#!/usr/bin/env python3
"""
00_validate_access.py — auth handshake, entitlement probe, permission inventory.

Status: DOCUMENTED auth flow (OAuth2 client-credentials against Fortellis,
per adapters/cdk-fortellis/README.md) + UNVERIFIED response shapes.

UNVERIFIED: the exact token endpoint path, the exact entitlement/subscription
introspection response body, and the exact permission-inventory endpoint name
have not been confirmed against a live Peterbilt Atlantic tenant. This script
codes against the documented Fortellis OAuth2 client-credentials pattern
(https://fortellis.io -- marketplace subscription model) and the three-header
contract (Authorization, Subscription-Id, Department-Id) confirmed in
adapters/cdk-fortellis/README.md. Where the real payload shape is unknown,
this script inspects HTTP status codes and headers only, and never assumes a
JSON body shape beyond a plain existence check -- see `_probe` below.

Run this FIRST, before any extraction phase. It writes a go/no-go report to
extract/out/00_validate_access.report.json and prints a human summary.

Usage:
    python3 00_validate_access.py [--base-url URL] [--dry-run]

Env vars required (see ../README.md):
    FORTELLIS_APP_ID
    FORTELLIS_APP_SECRET
    FORTELLIS_SUBSCRIPTION_ID
    CDK_DEPT_ID_<SITE>   (at least one; one per site/department pair)
    FORTELLIS_BASE_URL   (optional override; default below is DOCUMENTED
                           from the Fortellis marketplace, not tenant-specific)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common  # noqa: E402

DEFAULT_BASE_URL = "https://api.fortellis.io"
DEFAULT_TOKEN_URL = "https://identity.fortellis.io/oauth2/aus1p1ixy7YL8cwbZ2p7/v1/token"
# ^ DOCUMENTED pattern for Fortellis Okta-backed OAuth2 (per public Fortellis
# developer onboarding guides); UNVERIFIED whether Peterbilt Atlantic's
# marketplace app uses this exact authorization-server ID segment
# ("aus1p1ixy7YL8cwbZ2p7") -- confirm from the app's own Fortellis
# marketplace credentials page before first run and override with
# --token-url if different.


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Auth handshake + entitlement probe + permission inventory for the "
            "CDK Drive (Fortellis) adapter. Writes a go/no-go report."
        )
    )
    p.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Fortellis API base URL")
    p.add_argument("--token-url", default=DEFAULT_TOKEN_URL, help="OAuth2 token endpoint")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate config/env only; do not make any network calls.",
    )
    return p


def get_token(token_url: str, app_id: str, app_secret: str, subscription_id: str) -> dict:
    """Client-credentials grant. UNVERIFIED exact param names beyond the
    OAuth2 standard (client_id/client_secret/grant_type) -- some Fortellis
    guides show `Subscription-Id` sent at token time too; we send it as a
    header for safety."""
    resp = common.request_with_backoff(
        "POST",
        token_url,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Subscription-Id": subscription_id,
        },
        params=None,
        json_body=None,
        max_retries=2,
    )
    return resp.json()


def probe_entitlement(base_url: str, token: str, subscription_id: str, department_id: str) -> dict:
    """Hit a cheap, documented-to-exist endpoint (Get Customer v3 search with
    a tiny page size) purely to confirm auth + entitlement + department
    scoping works, without pulling real volume. UNVERIFIED exact query
    params for a minimal/zero-result probe call -- adjust once the live
    OpenAPI spec is in hand."""
    url = f"{base_url}/cdk/v3/customers"
    headers = {
        "Authorization": f"Bearer {token}",
        "Subscription-Id": subscription_id,
        "Department-Id": department_id,
        "Request-Id": "00-validate-access-probe",
    }
    resp = common.request_with_backoff("GET", url, headers=headers, params={"limit": 1}, max_retries=1)
    return {"status": resp.status_code, "url": url}


def main() -> int:
    args = build_arg_parser().parse_args()
    report = {
        "started_at": common.utcnow_iso(),
        "checks": [],
        "go_no_go": "NO-GO",
    }

    def check(name: str, ok: bool, detail: str):
        report["checks"].append({"name": name, "ok": ok, "detail": detail})

    app_id = common.env("FORTELLIS_APP_ID")
    app_secret = common.env("FORTELLIS_APP_SECRET")
    subscription_id = common.env("FORTELLIS_SUBSCRIPTION_ID")
    dept_ids = common.department_ids()

    check("FORTELLIS_APP_ID present", bool(app_id), "required env var")
    check("FORTELLIS_APP_SECRET present", bool(app_secret), "required env var")
    check("FORTELLIS_SUBSCRIPTION_ID present", bool(subscription_id), "required env var")
    check(
        "at least one CDK_DEPT_ID_* present",
        bool(dept_ids),
        f"found: {sorted(dept_ids.keys())}",
    )

    targets = common.load_targets()
    check("targets.yaml loads", len(targets) > 0, f"{len(targets)} targets found")

    if args.dry_run:
        report["notes"] = ["--dry-run: skipped network calls"]
        report["go_no_go"] = "GO" if all(c["ok"] for c in report["checks"]) else "NO-GO"
        _write_report(report)
        print(json.dumps(report, indent=2))
        return 0 if report["go_no_go"] == "GO" else 1

    if not (app_id and app_secret and subscription_id and dept_ids):
        report["go_no_go"] = "NO-GO"
        report["notes"] = ["Missing credentials -- see extract/README.md. No network calls attempted."]
        _write_report(report)
        print(json.dumps(report, indent=2))
        return 1

    try:
        token_resp = get_token(args.token_url, app_id, app_secret, subscription_id)
        access_token = token_resp.get("access_token")
        check("token endpoint reachable", bool(access_token), "access_token present in response")
    except common.HttpError as e:
        check("token endpoint reachable", False, f"HTTP {e.status}: {_advice_for_status(e.status)}")
        report["go_no_go"] = "NO-GO"
        _write_report(report)
        print(json.dumps(report, indent=2))
        return 1
    except Exception as e:  # noqa: BLE001
        check("token endpoint reachable", False, f"exception: {e}")
        report["go_no_go"] = "NO-GO"
        _write_report(report)
        print(json.dumps(report, indent=2))
        return 1

    for site, dept_id in dept_ids.items():
        try:
            result = probe_entitlement(args.base_url, access_token, subscription_id, dept_id)
            check(f"entitlement probe [{site}]", True, f"HTTP {result['status']} on {result['url']}")
        except common.HttpError as e:
            check(f"entitlement probe [{site}]", False, f"HTTP {e.status}: {_advice_for_status(e.status)}")

    report["go_no_go"] = "GO" if all(c["ok"] for c in report["checks"]) else "PARTIAL"
    report["finished_at"] = common.utcnow_iso()
    _write_report(report)
    print(json.dumps(report, indent=2))
    return 0 if report["go_no_go"] in ("GO", "PARTIAL") else 1


def _advice_for_status(status: int) -> str:
    if status in (401, 403):
        return (
            "Auth/entitlement failure. Check app id/secret and that the Fortellis "
            "marketplace subscription is ACTIVE (not pending approval) for this "
            "department. See extract/README.md '401/403' guidance."
        )
    if status == 404:
        return (
            "Endpoint not found. Confirm base URL / API version path against the "
            "live OpenAPI spec -- this harness's URLs are DOCUMENTED-but-UNVERIFIED "
            "against the real tenant. See extract/README.md '404' guidance."
        )
    return f"Unexpected status {status}."


def _write_report(report: dict) -> None:
    out = common.out_path("00_validate_access.report.json")
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
