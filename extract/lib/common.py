"""
extract/lib/common.py — shared helpers for the CDK Twin extract harness.

Status: DOCUMENTED implementation detail of this harness (not a CDK/Fortellis claim).
Provides: config loading, NDJSON writers, run manifests (row counts, min/max
timestamp, SHA-256), simple retry/backoff, and env-var lookups used by every
script in extract/bin/.

No third-party dependency beyond `requests` (see extract/README.md). Everything
else is Python 3 standard library, by design, so this harness runs on whatever
box gets handed the Fortellis credentials tomorrow without a build step.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import urllib.parse
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Optional

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - fallback path documented in README
    yaml = None

REPO_ROOT = Path(__file__).resolve().parents[2]
EXTRACT_ROOT = REPO_ROOT / "extract"
CONFIG_PATH = EXTRACT_ROOT / "config" / "targets.yaml"
OUT_ROOT = EXTRACT_ROOT / "out"


# --------------------------------------------------------------------------
# Config loading (targets.yaml)
# --------------------------------------------------------------------------

def _minimal_yaml_load(text: str) -> Any:
    """Extremely small YAML subset loader used only if PyYAML is unavailable.

    DOCUMENTED LIMITATION: this fallback supports the flat list-of-mappings
    shape used by extract/config/targets.yaml and nothing more exotic. It
    exists so `pip install pyyaml` is not a hard blocker on day one. If
    PyYAML is installed (recommended), it is always preferred.
    """
    import re

    lines = text.splitlines()
    root: list[dict[str, Any]] = []
    stack: list[tuple[int, Any]] = [(-1, root)]
    current_item: Optional[dict[str, Any]] = None
    for raw in lines:
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if stripped.startswith("- "):
            current_item = {}
            root.append(current_item)
            stripped = stripped[2:].strip()
            if ":" in stripped:
                k, v = stripped.split(":", 1)
                current_item[k.strip()] = _yaml_scalar(v.strip())
            continue
        if ":" in stripped and current_item is not None:
            k, v = stripped.split(":", 1)
            v = v.strip()
            if v == "" :
                # nested block (e.g. date_window: / control_key:) — collect
                # subsequent more-indented "key: value" lines into a dict.
                nested: dict[str, Any] = {}
                current_item[k.strip()] = nested
                current_item = current_item  # keep top item as current
                _pending_nested = nested
                _pending_indent = indent
                # store on the item so following lines can find it
                current_item.setdefault("__nested_stack__", []).append(
                    (indent, nested)
                )
            else:
                # if we are inside a nested block, attach there
                nstack = current_item.get("__nested_stack__") or []
                target = current_item
                for nindent, nested in nstack:
                    if indent > nindent:
                        target = nested
                target[k.strip()] = _yaml_scalar(v)
    for item in root:
        item.pop("__nested_stack__", None)
    return root


def _yaml_scalar(v: str) -> Any:
    if v in ("null", "~", ""):
        return None
    if v in ("true", "True"):
        return True
    if v in ("false", "False"):
        return False
    if v.startswith('"') and v.endswith('"'):
        return v[1:-1]
    if v.startswith("'") and v.endswith("'"):
        return v[1:-1]
    try:
        if "." in v:
            return float(v)
        return int(v)
    except ValueError:
        return v


def load_targets(config_path: Path = CONFIG_PATH) -> list[dict[str, Any]]:
    """Load extract/config/targets.yaml and return the `targets` list."""
    text = config_path.read_text(encoding="utf-8")
    if yaml is not None:
        doc = yaml.safe_load(text)
        return doc.get("targets", [])
    doc = _minimal_yaml_load(text)
    return doc


def get_target(target_id: str, config_path: Path = CONFIG_PATH) -> dict[str, Any]:
    for t in load_targets(config_path):
        if t.get("id") == target_id:
            return t
    raise KeyError(f"target id {target_id!r} not found in {config_path}")


# --------------------------------------------------------------------------
# Env var access
# --------------------------------------------------------------------------

REQUIRED_FORTELLIS_ENV = [
    "FORTELLIS_APP_ID",
    "FORTELLIS_APP_SECRET",
    "FORTELLIS_SUBSCRIPTION_ID",
]

# Department-Id is per-site/per-functional-area; see extract/README.md.
# CDK_DEPT_ID_<SITE> vars are discovered dynamically, not hardcoded here.


def env(name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    val = os.environ.get(name, default)
    if required and not val:
        raise SystemExit(
            f"Missing required environment variable: {name}. "
            f"See extract/README.md for the full credential list."
        )
    return val


def department_ids() -> dict[str, str]:
    """Return every CDK_DEPT_ID_* env var found, keyed by site suffix."""
    out = {}
    for k, v in os.environ.items():
        if k.startswith("CDK_DEPT_ID_") and v:
            out[k[len("CDK_DEPT_ID_"):]] = v
    return out


# --------------------------------------------------------------------------
# NDJSON writer + run manifest
# --------------------------------------------------------------------------

@dataclass
class RunManifest:
    target_id: str
    output_path: str
    started_at: str
    finished_at: str = ""
    row_count: int = 0
    min_timestamp: Optional[str] = None
    max_timestamp: Optional[str] = None
    sha256: str = ""
    status: str = "incomplete"
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_id": self.target_id,
            "output_path": self.output_path,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "row_count": self.row_count,
            "min_timestamp": self.min_timestamp,
            "max_timestamp": self.max_timestamp,
            "sha256": self.sha256,
            "status": self.status,
            "errors": self.errors,
            "notes": self.notes,
        }


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class NdjsonWriter:
    """Append-only, resumable NDJSON writer with manifest bookkeeping.

    Idempotency contract: callers pass a `dedupe_key` extractor; rows whose key
    was already seen in the existing output file (if resuming) are skipped
    rather than duplicated. This makes re-running a script after an interrupted
    run safe.
    """

    def __init__(
        self,
        target_id: str,
        output_path: Path,
        timestamp_field: Optional[str] = None,
        dedupe_key: Optional[Callable[[dict], str]] = None,
        resume: bool = True,
    ):
        self.target_id = target_id
        self.output_path = output_path
        self.timestamp_field = timestamp_field
        self.dedupe_key = dedupe_key
        self.manifest = RunManifest(
            target_id=target_id,
            output_path=str(output_path),
            started_at=utcnow_iso(),
        )
        self._seen: set[str] = set()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if resume and output_path.exists():
            with open(output_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    self._absorb_existing(row)
            self._fh = open(output_path, "a", encoding="utf-8")
        else:
            self._fh = open(output_path, "w", encoding="utf-8")

    def _absorb_existing(self, row: dict) -> None:
        self.manifest.row_count += 1
        self._update_timestamps(row)
        if self.dedupe_key is not None:
            self._seen.add(self.dedupe_key(row))

    def _update_timestamps(self, row: dict) -> None:
        if not self.timestamp_field:
            return
        ts = row.get(self.timestamp_field)
        if not ts:
            return
        if self.manifest.min_timestamp is None or ts < self.manifest.min_timestamp:
            self.manifest.min_timestamp = ts
        if self.manifest.max_timestamp is None or ts > self.manifest.max_timestamp:
            self.manifest.max_timestamp = ts

    def already_seen(self, row: dict) -> bool:
        if self.dedupe_key is None:
            return False
        return self.dedupe_key(row) in self._seen

    def write(self, row: dict) -> bool:
        """Write one row. Returns False if skipped as a duplicate."""
        if self.dedupe_key is not None:
            key = self.dedupe_key(row)
            if key in self._seen:
                return False
            self._seen.add(key)
        self._fh.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
        self.manifest.row_count += 1
        self._update_timestamps(row)
        return True

    def close(self, status: str = "ok") -> RunManifest:
        self._fh.close()
        self.manifest.finished_at = utcnow_iso()
        self.manifest.status = status
        if self.output_path.exists():
            self.manifest.sha256 = sha256_of_file(self.output_path)
        manifest_path = self.output_path.with_suffix(self.output_path.suffix + ".manifest.json")
        manifest_path.write_text(
            json.dumps(self.manifest.to_dict(), indent=2) + "\n", encoding="utf-8"
        )
        return self.manifest


# --------------------------------------------------------------------------
# HTTP with retry/backoff (rate-limit aware)
# --------------------------------------------------------------------------

class HttpError(RuntimeError):
    def __init__(self, status: int, body: str, url: str):
        super().__init__(f"HTTP {status} for {url}: {body[:300]}")
        self.status = status
        self.body = body
        self.url = url


def request_with_backoff(
    method: str,
    url: str,
    *,
    headers: Optional[dict] = None,
    params: Optional[dict] = None,
    json_body: Optional[dict] = None,
    max_retries: int = 6,
    base_delay: float = 1.5,
    timeout: float = 30.0,
    sleep_fn: Callable[[float], None] = time.sleep,
):
    """requests wrapper with exponential backoff on 429/5xx.

    DOCUMENTED behavior for Fortellis-style APIs: 429 responses commonly carry
    a `Retry-After` header; we honor it when present, otherwise back off
    exponentially. 401/403 are NOT retried — those are auth/entitlement
    failures that need a human, not a retry loop (see extract/README.md,
    "what to do when a lane returns 401/403 vs 404 vs empty").
    """
    import requests  # imported lazily so --help works with no deps installed

    attempt = 0
    while True:
        attempt += 1
        resp = requests.request(
            method, url, headers=headers, params=params, json=json_body, timeout=timeout
        )
        if resp.status_code < 400:
            return resp
        if resp.status_code in (401, 403):
            raise HttpError(resp.status_code, resp.text, url)
        if resp.status_code == 404:
            raise HttpError(404, resp.text, url)
        if resp.status_code == 429 or resp.status_code >= 500:
            if attempt > max_retries:
                raise HttpError(resp.status_code, resp.text, url)
            retry_after = resp.headers.get("Retry-After")
            if retry_after:
                try:
                    delay = float(retry_after)
                except ValueError:
                    delay = base_delay * (2 ** (attempt - 1))
            else:
                delay = base_delay * (2 ** (attempt - 1))
            sleep_fn(min(delay, 60.0))
            continue
        raise HttpError(resp.status_code, resp.text, url)


# --------------------------------------------------------------------------
# Date window helpers (used by 30_extract_transactions.py)
# --------------------------------------------------------------------------

def prior_three_full_months(today: Optional[datetime] = None) -> tuple[str, str]:
    """Return (from_date, to_date) ISO dates covering the prior three full
    calendar months relative to `today` (defaults to real today, UTC).

    Per the brief's default: if today is in July 2026, the window is
    2026-05-01 through 2026-07-31 (May, June, July) — i.e. "prior three full
    months" is read here as the three months immediately preceding and
    including the current month's start, matching the brief's own worked
    example (May/June/July 2026 evaluated from within July 2026). Confirm the
    exact window on the day per the brief.
    """
    today = today or datetime.now(timezone.utc)
    first_of_this_month = today.replace(day=1)
    # step back three months from the first of this month to get window start
    m = first_of_this_month.month - 2
    y = first_of_this_month.year
    while m <= 0:
        m += 12
        y -= 1
    from_date = f"{y:04d}-{m:02d}-01"
    # window end = last day of the current month (brief says "prior full
    # months" but worked example includes the current month; see docstring)
    if first_of_this_month.month == 12:
        next_month = first_of_this_month.replace(year=y + 1, month=1)
    else:
        next_month = first_of_this_month.replace(month=first_of_this_month.month + 1)
    from datetime import timedelta
    last_day_this_month = next_month - timedelta(days=1)
    to_date = last_day_this_month.strftime("%Y-%m-%d")
    return from_date, to_date


def out_path(rel_path: str) -> Path:
    p = OUT_ROOT / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    return p
