#!/usr/bin/env python3
"""Lightspeed DMS 3PA collector — automated read of Peterbilt Atlantic's own records.

Wire format is authoritative in ../../docs/lightspeed-3pa/developer-guide.pdf
(Service Description, pp. 6-9). This collector was written against that guide and
retracts the OData-v2 assumptions of the earlier draft.

Contract:
  - HTTP Basic authentication (guide p. 6). Credential in env LIGHTSPEED_3PA_BASIC_AUTH
    as "username:password".
  - URL shape /{base}/{DataType}/{CMF} — CMF is a segment, not a filter (guide p. 6).
  - Supported query options: $filter, $top (cap 500), $skip, $orderby (guide p. 8).
  - NOT supported: $select, $expand, $inlinecount, $format, string functions,
    arithmetic operators (guide p. 8).
  - Content: JSON default. Gzip requested via X-Accept-Encoding: gzip (guide p. 7).
  - Date literals in $filter: datetime'YYYY-MM-DDTHH:MM:SS' single-quoted (guide p. 8).
  - Bigint literals in $filter: append 'L' suffix (guide p. 9).
  - Status: 200 success, 401 auth, 403 authorization, 404 not found, 500 other
    (guide p. 9). Errors return a plain-text body, no WWW-Authenticate.

Extract layout:
  extract/out/lightspeed/<rooftop>/<UTC-date>/<endpoint>-<page>.json
  extract/out/lightspeed/<rooftop>/<UTC-date>/manifest.json
  extract/out/lightspeed/<rooftop>/watermark.json  (updated only after full success)

The collector never overwrites an existing extract file. Re-runs go to a new UTC-dated
directory. Watermark is advanced only after every configured endpoint completes for that
rooftop.

Usage:
  python -m extract.lightspeed.collect \
      --config adapters/lightspeed-3pa/config.yml \
      --rooftop moncton \
      --endpoint Customer

  python -m extract.lightspeed.collect \
      --config adapters/lightspeed-3pa/config.yml \
      --rooftop moncton  # runs all Phase-1 endpoints

  python -m extract.lightspeed.collect \
      --config adapters/lightspeed-3pa/config.yml  # runs all rooftops, Phase 1

Requires: requests, PyYAML. No other runtime deps.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import os
import sys
import time
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import requests
import yaml


# --------------------------------------------------------------------------- #
# Config                                                                      #
# --------------------------------------------------------------------------- #

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REPO_ROOT / "adapters" / "lightspeed-3pa" / "config.yml"

BASIC_AUTH_ENV = "LIGHTSPEED_3PA_BASIC_AUTH"  # "username:password"


@dataclass
class Endpoint:
    name: str
    incremental_key: str | None
    incremental_type: str  # datetime | date | bigint | none
    scope_filter_template: str | None
    guide_pages: str
    phase: float
    notes: str | None = None


@dataclass
class Rooftop:
    name: str
    cmf: str
    storename: str


@dataclass
class ApiCfg:
    base_url: str
    page_size: int
    gzip_header_name: str
    connect_timeout_s: int
    read_timeout_s: int
    retry_on_status: list[int]
    max_retries: int
    backoff_seconds: list[int]


@dataclass
class Cfg:
    api: ApiCfg
    rooftops: list[Rooftop]
    endpoints: list[Endpoint]
    output_root: Path
    never_overwrite: bool = True


def load_config(path: Path) -> Cfg:
    raw = yaml.safe_load(path.read_text())
    api = ApiCfg(**raw["api"])
    rooftops = [Rooftop(**r) for r in raw["rooftops"]]
    endpoints = [Endpoint(**e) for e in raw["endpoints"]]
    output_root = (REPO_ROOT / raw["output"]["root"]).resolve()
    never = bool(raw["output"].get("never_overwrite", True))
    return Cfg(api, rooftops, endpoints, output_root, never)


# --------------------------------------------------------------------------- #
# Credential                                                                  #
# --------------------------------------------------------------------------- #

def load_basic_auth() -> tuple[str, str]:
    raw = os.environ.get(BASIC_AUTH_ENV)
    if not raw:
        raise SystemExit(
            f"Missing credential: set {BASIC_AUTH_ENV} to 'username:password'. "
            f"See adapters/lightspeed-3pa/README.md § Sequence for connectivity, step 2."
        )
    if ":" not in raw:
        raise SystemExit(
            f"{BASIC_AUTH_ENV} must be 'username:password' (colon-separated). Got a value without ':'."
        )
    user, _, password = raw.partition(":")
    if not user or not password:
        raise SystemExit(f"{BASIC_AUTH_ENV} has an empty username or password.")
    return user, password


# --------------------------------------------------------------------------- #
# URL construction                                                            #
# --------------------------------------------------------------------------- #

def _fmt_datetime_literal(watermark_iso: str) -> str:
    # Developer guide p. 8: datetime'YYYY-MM-DDTHH:MM:SS'
    # Accept either a bare ISO date or a full datetime; render it in the guide's form.
    if len(watermark_iso) == 10:  # YYYY-MM-DD
        return f"datetime'{watermark_iso}T00:00:00'"
    # normalise Z / fractional seconds off; the guide's example has no timezone.
    v = watermark_iso.replace("Z", "").split(".")[0]
    return f"datetime'{v}'"


def _fmt_date_literal(watermark_iso: str) -> str:
    # For 'date' typed columns the guide uses ODBC yyyy-mm-dd (p. 7-8).
    # In practice InvoiceDate is returned as datetime in payloads, so a datetime
    # literal is safer for $filter comparisons. Match the guide example on p. 97:
    #   "InvoiceDate": "2018-07-31T07:11:45.017"
    # Filter with datetime literal to be strict.
    return _fmt_datetime_literal(watermark_iso[:10])


def _fmt_bigint_literal(watermark_value: str) -> str:
    # Developer guide p. 9: append 'L' suffix.
    return f"{watermark_value}L"


def build_filter(endpoint: Endpoint, watermark: str | None, rooftop: Rooftop) -> str | None:
    """Return the $filter value (unencoded), or None if there is nothing to filter."""
    parts: list[str] = []
    if endpoint.incremental_key and watermark:
        if endpoint.incremental_type == "datetime":
            parts.append(f"{endpoint.incremental_key} gt {_fmt_datetime_literal(watermark)}")
        elif endpoint.incremental_type == "date":
            parts.append(f"{endpoint.incremental_key} gt {_fmt_date_literal(watermark)}")
        elif endpoint.incremental_type == "bigint":
            parts.append(f"{endpoint.incremental_key} gt {_fmt_bigint_literal(watermark)}")
        # "none" -> no filter
    if endpoint.scope_filter_template:
        parts.append(endpoint.scope_filter_template.format(storename=rooftop.storename))
    if not parts:
        return None
    return " and ".join(parts)


def build_url(
    api: ApiCfg,
    endpoint: Endpoint,
    rooftop: Rooftop,
    watermark: str | None,
    skip: int,
) -> str:
    base = api.base_url.rstrip("/")
    path = f"{base}/{endpoint.name}/{rooftop.cmf}"
    params: list[tuple[str, str]] = []
    params.append(("$top", str(api.page_size)))
    if skip:
        params.append(("$skip", str(skip)))
    if endpoint.incremental_key and endpoint.incremental_type != "none":
        params.append(("$orderby", endpoint.incremental_key))
    f = build_filter(endpoint, watermark, rooftop)
    if f:
        params.append(("$filter", f))
    qs = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    return f"{path}?{qs}" if qs else path


# --------------------------------------------------------------------------- #
# HTTP                                                                        #
# --------------------------------------------------------------------------- #

def make_session(user: str, password: str, gzip_header: str) -> requests.Session:
    s = requests.Session()
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    s.headers.update({
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
        gzip_header: "gzip",
        "User-Agent": "EVEglyphDesign-Hawkins-Twin/1.0 (lightspeed-3pa collector; +https://github.com/EVEglyphDesign/eve-hawkins-cdk-twin)",
    })
    return s


def get_with_retry(session: requests.Session, url: str, api: ApiCfg) -> requests.Response:
    last_exc: Exception | None = None
    for attempt in range(api.max_retries + 1):
        try:
            resp = session.get(url, timeout=(api.connect_timeout_s, api.read_timeout_s))
        except requests.RequestException as e:
            last_exc = e
            if attempt < api.max_retries:
                time.sleep(api.backoff_seconds[min(attempt, len(api.backoff_seconds) - 1)])
                continue
            raise
        if resp.status_code in api.retry_on_status and attempt < api.max_retries:
            time.sleep(api.backoff_seconds[min(attempt, len(api.backoff_seconds) - 1)])
            continue
        return resp
    # unreachable
    assert last_exc is not None
    raise last_exc


# --------------------------------------------------------------------------- #
# Payload handling                                                            #
# --------------------------------------------------------------------------- #

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_row_count(body_bytes: bytes) -> tuple[int, Any]:
    """Return (row_count, parsed_json). The guide's payloads are top-level JSON arrays."""
    text = body_bytes.decode("utf-8", errors="replace")
    parsed = json.loads(text)
    if isinstance(parsed, list):
        return len(parsed), parsed
    if isinstance(parsed, dict) and isinstance(parsed.get("value"), list):
        # defensive: some deployments might wrap in {"value": [...]}
        return len(parsed["value"]), parsed
    # Some endpoints (singletons) may return an object.
    return 1, parsed


def extract_watermark_from_rows(
    rows: Iterable[dict[str, Any]], key: str
) -> str | None:
    max_value: str | None = None
    for row in rows:
        v = row.get(key)
        if v is None:
            continue
        v_str = str(v)
        if max_value is None or v_str > max_value:
            max_value = v_str
    return max_value


# --------------------------------------------------------------------------- #
# Collection                                                                  #
# --------------------------------------------------------------------------- #

def collect_endpoint(
    cfg: Cfg,
    session: requests.Session,
    rooftop: Rooftop,
    endpoint: Endpoint,
    watermark: str | None,
    utc_date_dir: Path,
) -> dict[str, Any]:
    """Page through one endpoint, writing per-page JSON and returning a manifest entry."""
    print(f"  · {endpoint.name}  (watermark={watermark or 'none'})", flush=True)
    pages: list[dict[str, Any]] = []
    skip = 0
    page_no = 0
    new_watermark = watermark
    while True:
        url = build_url(cfg.api, endpoint, rooftop, watermark, skip)
        started_at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
        resp = get_with_retry(session, url, cfg.api)
        finished_at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

        # Non-200 handling — do not paper over. Write the error body and stop.
        if resp.status_code != 200:
            err_path = utc_date_dir / f"{endpoint.name}-{page_no:04d}.error.txt"
            err_path.write_text(
                f"URL: {url}\nStatus: {resp.status_code}\nBody:\n{resp.text}\n",
                encoding="utf-8",
            )
            pages.append({
                "page": page_no,
                "url": url,
                "requested_at_utc": started_at,
                "responded_at_utc": finished_at,
                "status": resp.status_code,
                "row_count": 0,
                "sha256": None,
                "error_body_path": str(err_path.relative_to(REPO_ROOT)),
            })
            print(f"      ! HTTP {resp.status_code} — stopping at page {page_no}", flush=True)
            break

        body = resp.content  # raw bytes, gzip already handled by requests
        row_count, parsed = parse_row_count(body)

        page_path = utc_date_dir / f"{endpoint.name}-{page_no:04d}.json"
        if cfg.never_overwrite and page_path.exists():
            raise SystemExit(
                f"Refusing to overwrite existing extract file: {page_path}. "
                f"The collector never overwrites — see README."
            )
        page_path.write_bytes(body)
        digest = sha256_hex(body)

        rows_iter: Iterable[dict[str, Any]] = (
            parsed if isinstance(parsed, list)
            else parsed.get("value", []) if isinstance(parsed, dict) else []
        )
        if endpoint.incremental_key and endpoint.incremental_type != "none":
            page_max = extract_watermark_from_rows(rows_iter, endpoint.incremental_key)
            if page_max and (new_watermark is None or page_max > new_watermark):
                new_watermark = page_max

        pages.append({
            "page": page_no,
            "url": url,
            "requested_at_utc": started_at,
            "responded_at_utc": finished_at,
            "status": 200,
            "row_count": row_count,
            "sha256": digest,
            "path": str(page_path.relative_to(REPO_ROOT)),
        })
        print(f"      p{page_no:04d}  rows={row_count}  sha256={digest[:12]}…", flush=True)

        # Partial page => end of stream.
        if row_count < cfg.api.page_size:
            break

        skip += cfg.api.page_size
        page_no += 1

        # Safety: never page forever without a watermark advancing.
        if page_no > 10_000:
            raise SystemExit(
                f"Refusing to page past 10,000 pages on {endpoint.name} — abort."
            )

    return {
        "endpoint": endpoint.name,
        "phase": endpoint.phase,
        "incremental_key": endpoint.incremental_key,
        "watermark_before": watermark,
        "watermark_after": new_watermark,
        "pages": pages,
        "total_rows": sum(p["row_count"] for p in pages),
        "guide_pages": endpoint.guide_pages,
    }


def collect_rooftop(
    cfg: Cfg,
    session: requests.Session,
    rooftop: Rooftop,
    endpoint_filter: set[str] | None,
    phase_filter: float | None,
) -> None:
    rooftop_dir = cfg.output_root / rooftop.name
    rooftop_dir.mkdir(parents=True, exist_ok=True)

    watermark_path = rooftop_dir / "watermark.json"
    watermarks: dict[str, str] = {}
    if watermark_path.exists():
        watermarks = json.loads(watermark_path.read_text())

    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    utc_date_dir = rooftop_dir / today
    if cfg.never_overwrite and utc_date_dir.exists() and any(utc_date_dir.iterdir()):
        # Same-day re-runs write to a suffixed directory instead of overwriting.
        suffix = dt.datetime.now(dt.timezone.utc).strftime("%H%M%S")
        utc_date_dir = rooftop_dir / f"{today}--rerun-{suffix}"
    utc_date_dir.mkdir(parents=True, exist_ok=True)

    print(f"[{rooftop.name}] CMF={rooftop.cmf} storename={rooftop.storename} -> {utc_date_dir.relative_to(REPO_ROOT)}", flush=True)

    endpoint_manifests: list[dict[str, Any]] = []
    for endpoint in cfg.endpoints:
        if endpoint_filter and endpoint.name not in endpoint_filter:
            continue
        if phase_filter is not None and endpoint.phase > phase_filter:
            continue
        wm = watermarks.get(endpoint.name)
        entry = collect_endpoint(cfg, session, rooftop, endpoint, wm, utc_date_dir)
        endpoint_manifests.append(entry)
        # advance watermark only if this endpoint succeeded end-to-end
        if entry["watermark_after"] and (
            not entry["pages"] or all(p["status"] == 200 for p in entry["pages"])
        ):
            watermarks[endpoint.name] = entry["watermark_after"]

    manifest = {
        "rooftop": rooftop.name,
        "cmf": rooftop.cmf,
        "storename": rooftop.storename,
        "run_utc_date": today,
        "run_directory": str(utc_date_dir.relative_to(REPO_ROOT)),
        "endpoints": endpoint_manifests,
    }
    (utc_date_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
    )
    watermark_path.write_text(json.dumps(watermarks, indent=2, sort_keys=True), encoding="utf-8")
    print(f"[{rooftop.name}] done. manifest -> {utc_date_dir.relative_to(REPO_ROOT)}/manifest.json", flush=True)


# --------------------------------------------------------------------------- #
# Entry point                                                                 #
# --------------------------------------------------------------------------- #

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Lightspeed DMS 3PA collector")
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    ap.add_argument("--rooftop", action="append", help="rooftop name (repeatable); default = all")
    ap.add_argument("--endpoint", action="append", help="endpoint name (repeatable); default = all in phase")
    ap.add_argument("--phase", type=float, default=1.0, help="max phase to include; default 1.0 (Phase 1)")
    args = ap.parse_args(argv)

    cfg = load_config(args.config)
    user, password = load_basic_auth()
    session = make_session(user, password, cfg.api.gzip_header_name)

    rooftops = cfg.rooftops
    if args.rooftop:
        wanted = set(args.rooftop)
        rooftops = [r for r in rooftops if r.name in wanted]
        missing = wanted - {r.name for r in rooftops}
        if missing:
            raise SystemExit(f"Unknown rooftop(s): {sorted(missing)}")

    endpoint_filter = set(args.endpoint) if args.endpoint else None

    cfg.output_root.mkdir(parents=True, exist_ok=True)

    for rooftop in rooftops:
        collect_rooftop(cfg, session, rooftop, endpoint_filter, args.phase)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
