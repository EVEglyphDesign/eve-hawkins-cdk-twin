#!/usr/bin/env python3
"""
validate_load_ready.py — preflight check for "load-ready" status.

Checks (all against docs/model/fields.json, contract EgD-CDK-FIELDS-v2, and the
generated DDL/mapping artefacts):

  1. Every entity in fields.json has a generated DDL file in schema/ddl/postgres/
     and schema/ddl/snowflake/.
  2. Every load_column is unique within its entity and is a legal, unquoted,
     lowercase SQL identifier in both dialects (no reserved-word collisions).
  3. Every fk_target resolves to a real entity and a real column on it.
  4. Every extract target in extract/config/targets.yaml maps to a table that
     exists in the generated DDL (by entity id -> table_name).

Prints a pass/fail report and exits non-zero on any failure.

Usage:
    python3 validate_load_ready.py --fields docs/model/fields.json \
        --ddl-dir schema/ddl --targets extract/config/targets.yaml
"""
import argparse
import json
import os
import re
import sys

CONTRACT = "EgD-CDK-FIELDS-v2"
IDENT_RE = re.compile(r"^[a-z_][a-z0-9_]*$")

RESERVED_WORDS = {
    "select", "from", "where", "table", "order", "group", "by", "user", "date",
    "time", "timestamp", "check", "column", "default", "primary", "foreign",
    "key", "references", "unique", "null", "not", "and", "or", "in", "is",
    "as", "on", "join", "left", "right", "inner", "outer", "value", "values",
    "level", "type", "role", "grant", "revoke", "index", "view", "schema",
    "constraint", "cast", "case", "when", "then", "else", "end", "all", "any",
    "distinct", "having", "limit", "offset", "union", "insert", "update",
    "delete", "into", "set", "create", "drop", "alter", "add", "current",
    "session", "connection", "account", "number", "current_date", "current_time",
}

SYSTEM_COLUMNS = {"_rooftop_id", "_extracted_at", "_source_route", "_batch_id"}


def sql_ident_ok(name, max_len=63):
    if not name:
        return False, "empty identifier"
    if not IDENT_RE.match(name):
        return False, "not a legal unquoted lowercase identifier"
    if len(name) > max_len:
        return False, f"identifier exceeds {max_len} chars"
    if name.lower() in RESERVED_WORDS:
        return False, "reserved word collision"
    return True, ""


def load_yaml_targets(path):
    """
    Minimal stdlib-only YAML reader for extract/config/targets.yaml's specific,
    known shape (a top-level `targets:` list of flat-ish mappings). We do not
    depend on PyYAML per the stdlib-only constraint. This parses just enough:
    `- id: xxx` starts a new target; subsequent `key: value` lines (2-space
    indented under it) are attributes, until the next `- id:` or dedent.
    """
    targets = []
    current = None
    with open(path) as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")
            if not line.strip() or line.strip().startswith("#"):
                continue
            m = re.match(r"^  - id:\s*(.+)$", line)
            if m:
                if current is not None:
                    targets.append(current)
                current = {"id": m.group(1).strip().strip('"')}
                continue
            m2 = re.match(r"^    (\w+):\s*(.*)$", line)
            if m2 and current is not None:
                key, val = m2.group(1), m2.group(2).strip().strip('"')
                if val:  # skip nested-block keys like date_window with no inline value
                    current[key] = val
        if current is not None:
            targets.append(current)
    return targets


def main():
    ap = argparse.ArgumentParser(description="Preflight check that the DDL/mapping is load-ready.")
    ap.add_argument("--fields", required=True, help="Path to fields.json")
    ap.add_argument("--ddl-dir", default="schema/ddl", help="DDL root (expects postgres/ and snowflake/ subdirs)")
    ap.add_argument("--targets", default="extract/config/targets.yaml", help="Path to extract targets.yaml")
    args = ap.parse_args()

    failures = []
    warnings = []

    with open(args.fields) as f:
        doc = json.load(f)
    if doc.get("contract") != CONTRACT:
        warnings.append(f"input contract tag is {doc.get('contract')!r}, expected {CONTRACT!r}")

    entities = doc.get("entities", [])
    entities_by_id = {e["entity_id"]: e for e in entities}

    # --- Check 1: every entity has generated DDL in both dialects ---
    pg_dir = os.path.join(args.ddl_dir, "postgres")
    sf_dir = os.path.join(args.ddl_dir, "snowflake")
    for e in entities:
        eid = e["entity_id"]
        pg_path = os.path.join(pg_dir, f"{eid}.sql")
        sf_path = os.path.join(sf_dir, f"{eid}.sql")
        if not os.path.isfile(pg_path):
            failures.append(f"[DDL] missing Postgres DDL for entity '{eid}' (expected {pg_path})")
        if not os.path.isfile(sf_path):
            failures.append(f"[DDL] missing Snowflake DDL for entity '{eid}' (expected {sf_path})")

    # --- Check 2: load_column uniqueness + legal identifier, both dialects ---
    for e in entities:
        eid = e["entity_id"]
        seen = set()
        for fld in e.get("fields", []):
            col = fld.get("load_column")
            if col in seen:
                failures.append(f"[COLUMN] duplicate load_column '{col}' in entity '{eid}'")
            seen.add(col)
            ok, reason = sql_ident_ok(col)
            if not ok:
                failures.append(f"[COLUMN] entity '{eid}' load_column '{col}': {reason}")
        # system columns must not collide with field-declared load_columns
        collide = seen & SYSTEM_COLUMNS
        if collide:
            failures.append(f"[COLUMN] entity '{eid}' declares field(s) colliding with system columns: {sorted(collide)}")

    # --- Check 3: fk_target resolves to a real entity + column ---
    for e in entities:
        eid = e["entity_id"]
        for fld in e.get("fields", []):
            tgt = fld.get("fk_target")
            if not tgt:
                continue
            if "." not in tgt:
                failures.append(f"[FK] entity '{eid}' field '{fld.get('load_column')}': fk_target '{tgt}' not in 'entity_id.column' form")
                continue
            tgt_entity_id, tgt_col = tgt.split(".", 1)
            tgt_entity = entities_by_id.get(tgt_entity_id)
            if not tgt_entity:
                failures.append(f"[FK] entity '{eid}' field '{fld.get('load_column')}': fk_target entity '{tgt_entity_id}' does not exist")
                continue
            cols = {f.get("load_column") for f in tgt_entity.get("fields", [])}
            paths = {f.get("path") for f in tgt_entity.get("fields", [])}
            if tgt_col not in cols and not any(p and p.endswith("." + tgt_col) for p in paths):
                failures.append(f"[FK] entity '{eid}' field '{fld.get('load_column')}': fk_target column '{tgt_col}' not found on entity '{tgt_entity_id}'")

    # --- Check 4: every extract target maps to a table that exists ---
    if os.path.isfile(args.targets):
        yaml_targets = load_yaml_targets(args.targets)
        for t in yaml_targets:
            tid = t.get("id")
            if not tid:
                continue
            if tid not in entities_by_id:
                failures.append(f"[TARGETS] extract target '{tid}' has no matching entity in fields.json")
                continue
            table_name = entities_by_id[tid].get("table_name")
            pg_path = os.path.join(pg_dir, f"{tid}.sql")
            if not os.path.isfile(pg_path):
                failures.append(f"[TARGETS] extract target '{tid}' -> table '{table_name}' has no generated DDL at {pg_path}")
    else:
        warnings.append(f"targets file not found at {args.targets}, skipping check 4")

    # --- Report ---
    print("=" * 72)
    print("validate_load_ready.py -- preflight report")
    print(f"fields source: {args.fields}")
    print(f"entities checked: {len(entities)}")
    print("=" * 72)

    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  ! {w}")

    if failures:
        print(f"\n{len(failures)} FAILURE(S):")
        for x in failures:
            print(f"  x {x}")
        print("\nVERDICT: FAIL — not load-ready. Fix the above before extraction lands.")
        sys.exit(1)
    else:
        print("\nVERDICT: PASS — every entity has DDL in both dialects, every load_column")
        print("is unique and legal in both dialects, every fk_target resolves, and every")
        print("extract target maps to an existing table. Load-ready.")
        sys.exit(0)


if __name__ == "__main__":
    main()
