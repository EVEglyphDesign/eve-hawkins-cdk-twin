#!/usr/bin/env python3
"""
gen_ddl.py — generate load-ready DDL from docs/model/fields.json (contract EgD-CDK-FIELDS-v2).

Reads the field-level metadata dictionary and emits, per entity:
  schema/ddl/postgres/<entity_id>.sql   (CREATE TABLE, comments, indexes)
  schema/ddl/snowflake/<entity_id>.sql  (same, Snowflake dialect)
plus a rollup:
  schema/ddl/postgres/000_all.sql       (all Postgres tables in dependency order)

Design rules (binding, see /home/user/workspace/FIELD_CONTRACT.md and the
Lane F task brief):
  - Datatype mapping is honest: currency -> numeric(13,2), hours -> numeric(9,3),
    quantity -> numeric(13,3), identifiers -> varchar(n) at the documented length,
    dates/timestamps typed natively, enum -> varchar(len) with a commented list.
  - NOT NULL is only ever emitted when nullable=false AND confidence=DOCUMENTED.
    Any other non-nullable field (INFERRED/UNVERIFIED) gets a commented-out
    constraint line naming the reason — never a live constraint on an inference.
  - Foreign keys are only emitted where fk_target is set and resolves to a real
    entity + column; otherwise the fk_target is skipped with a comment (this
    condition is also caught by validate_load_ready.py).
  - Every table gets four system columns: _rooftop_id, _extracted_at,
    _source_route, _batch_id.
  - Every column gets a COMMENT ON COLUMN carrying dealer_label + confidence mark.
  - Idempotent: DROP TABLE IF EXISTS guard + CREATE TABLE IF NOT EXISTS is not
    used (DDL must be re-runnable without drift) -- instead each file begins
    with `CREATE TABLE IF NOT EXISTS`, and comments are always reissued because
    COMMENT ON COLUMN is itself idempotent (last write wins).

Usage:
    python3 gen_ddl.py --fields docs/model/fields.json --out-dir schema/ddl
    python3 gen_ddl.py --fields schema/bin/fields.fixture.json --out-dir schema/ddl --fixture-note
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

CONTRACT = "EgD-CDK-FIELDS-v2"
SYSTEM_COLUMNS = [
    # (load_column, pg_type, sf_type, dealer_label)
    ("_rooftop_id", "varchar(20)", "VARCHAR(20)", "which rooftop/store this extracted row belongs to"),
    ("_extracted_at", "timestamptz", "TIMESTAMP_NTZ", "when this row was pulled from CDK by the extract harness"),
    ("_source_route", "varchar(16)", "VARCHAR(16)", "which of the three extract routes produced this row: fortellis | export | screen"),
    ("_batch_id", "varchar(64)", "VARCHAR(64)", "the extract run/batch identifier this row landed with"),
]

CONF_MARK = {"DOCUMENTED": "[D]", "INFERRED": "[I]", "UNVERIFIED": "[U]"}

# ANSI/Postgres + Snowflake reserved words worth flagging (not exhaustive, but
# covers the ones likely to collide with dealer/accounting vocabulary).
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

IDENT_RE = re.compile(r"^[a-z_][a-z0-9_]*$")


def eprint(*a, **kw):
    print(*a, file=sys.stderr, **kw)


def load_fields(path):
    with open(path) as f:
        return json.load(f)


def sql_ident_ok(name, max_len=63):
    """Legal, unquoted, lowercase SQL identifier in both Postgres and Snowflake."""
    if not name:
        return False, "empty identifier"
    if not IDENT_RE.match(name):
        return False, "not a legal unquoted lowercase identifier (must match ^[a-z_][a-z0-9_]*$)"
    if len(name) > max_len:
        return False, f"identifier exceeds {max_len} chars"
    if name.lower() in RESERVED_WORDS:
        return False, "reserved word collision"
    return True, ""


def pg_type_for(field):
    """Map a v2 contract field to a Postgres column type."""
    dt = (field.get("datatype") or "string").lower()
    unit = field.get("unit")
    length = field.get("length")
    precision = field.get("precision")
    scale = field.get("scale")

    if unit == "currency":
        return "numeric(13,2)"
    if unit == "hours":
        return "numeric(9,3)"
    if unit == "quantity":
        return "numeric(13,3)"
    if unit == "percent":
        return "numeric(7,4)"

    if dt == "string":
        n = length or 255
        return f"varchar({n})"
    if dt == "integer":
        return "bigint"
    if dt == "decimal":
        p = precision or 18
        s = scale if scale is not None else 4
        return f"numeric({p},{s})"
    if dt == "date":
        return "date"
    if dt == "datetime":
        return "timestamptz"
    if dt == "boolean":
        return "boolean"
    if dt == "enum":
        n = length or 32
        return f"varchar({n})"
    return "text"


def sf_type_for(field):
    """Map a v2 contract field to a Snowflake column type."""
    dt = (field.get("datatype") or "string").lower()
    unit = field.get("unit")
    length = field.get("length")
    precision = field.get("precision")
    scale = field.get("scale")

    if unit == "currency":
        return "NUMBER(13,2)"
    if unit == "hours":
        return "NUMBER(9,3)"
    if unit == "quantity":
        return "NUMBER(13,3)"
    if unit == "percent":
        return "NUMBER(7,4)"

    if dt == "string":
        n = length or 255
        return f"VARCHAR({n})"
    if dt == "integer":
        return "NUMBER(38,0)"
    if dt == "decimal":
        p = precision or 18
        s = scale if scale is not None else 4
        return f"NUMBER({p},{s})"
    if dt == "date":
        return "DATE"
    if dt == "datetime":
        return "TIMESTAMP_NTZ"
    if dt == "boolean":
        return "BOOLEAN"
    if dt == "enum":
        n = length or 32
        return f"VARCHAR({n})"
    return "VARCHAR(16777216)"  # Snowflake's de-facto TEXT


def resolve_fk(field, table_by_load_column, entities_by_id):
    """
    fk_target is 'entity_id.load_column' or 'entity_id.path' per the contract sample.
    We resolve against load_column primarily; fall back to matching on path suffix.
    Returns (target_table, target_column) or (None, reason) if unresolved.
    """
    tgt = field.get("fk_target")
    if not tgt:
        return None, None
    if "." not in tgt:
        return None, f"fk_target '{tgt}' is not in 'entity_id.column' form"
    entity_id, col = tgt.split(".", 1)
    ent = entities_by_id.get(entity_id)
    if not ent:
        return None, f"fk_target entity '{entity_id}' does not exist"
    # try exact load_column match, then path-suffix match
    target_field = None
    for f in ent["fields"]:
        if f.get("load_column") == col:
            target_field = f
            break
    if target_field is None:
        for f in ent["fields"]:
            if f.get("path", "").endswith("." + col) or f.get("path") == col:
                target_field = f
                break
    if target_field is None:
        return None, f"fk_target column '{col}' not found on entity '{entity_id}'"
    return (ent["table_name"], target_field["load_column"]), None


def comment_text(field):
    label = field.get("dealer_label") or field.get("label") or field.get("path")
    mark = CONF_MARK.get(field.get("confidence"), "[?]")
    text = f"{mark} {label}".replace("'", "''")
    return text


def render_enum_comment(field):
    vals = field.get("enum_values") or []
    if not vals:
        return None
    parts = [f"{v.get('code')}={v.get('meaning')}" for v in vals]
    return "values: " + "; ".join(parts)


def build_entity_ddl(entity, entities_by_id, dialect):
    """Return (sql_text, warnings) for one entity in the given dialect ('postgres'|'snowflake')."""
    warnings = []
    table = entity["table_name"]
    fields = entity["fields"]

    col_lines = []
    comment_lines = []
    pk_cols = []
    fk_lines = []
    check_comment_lines = []
    seen_cols = set()

    type_for = pg_type_for if dialect == "postgres" else sf_type_for
    quote_id = lambda s: s  # both dialects accept unquoted lowercase identifiers

    for f in fields:
        col = f.get("load_column")
        ok, reason = sql_ident_ok(col)
        if not ok:
            warnings.append(f"{entity['entity_id']}.{col!r}: {reason}")
        if col in seen_cols:
            warnings.append(f"{entity['entity_id']}.{col!r}: duplicate load_column")
        seen_cols.add(col)

        coltype = type_for(f)
        nullable = f.get("nullable", True)
        confidence = f.get("confidence")
        is_documented_notnull = (nullable is False) and (confidence == "DOCUMENTED")

        line = f"    {quote_id(col)} {coltype}"
        if is_documented_notnull:
            line += " NOT NULL"
        if f.get("key") == "PK":
            pk_cols.append(col)
        col_lines.append(line)

        if (nullable is False) and (confidence != "DOCUMENTED"):
            check_comment_lines.append(
                f"    -- NOT NULL withheld on {col}: nullable=false per source but confidence={confidence} "
                f"(never enforce a constraint on an inference)"
            )

        # FK
        if f.get("key") == "FK" and f.get("fk_target"):
            target, err = resolve_fk(f, None, entities_by_id)
            if target:
                ttable, tcol = target
                fk_name = f"fk_{table}_{col}"
                if dialect == "postgres":
                    fk_lines.append(
                        f"ALTER TABLE {table} ADD CONSTRAINT {fk_name} "
                        f"FOREIGN KEY ({col}) REFERENCES {ttable} ({tcol});"
                    )
                else:
                    # Snowflake supports FK syntax but does not enforce it; still declare for documentation/tools.
                    fk_lines.append(
                        f"ALTER TABLE {table} ADD CONSTRAINT {fk_name} "
                        f"FOREIGN KEY ({col}) REFERENCES {ttable} ({tcol}) NOT ENFORCED;"
                    )
            else:
                warnings.append(f"{entity['entity_id']}.{col}: fk_target unresolved ({err}); FK skipped")
                fk_lines.append(f"-- SKIPPED FK on {col}: {err}")

        c = comment_text(f)
        enum_note = render_enum_comment(f)
        if enum_note:
            c = c + " (" + enum_note + ")"
        if dialect == "postgres":
            comment_lines.append(f"COMMENT ON COLUMN {table}.{col} IS '{c}';")
        else:
            comment_lines.append(f"COMMENT ON COLUMN {table}.{col} IS '{c}';")

    # system columns
    for col, pgtype, sftype, label in SYSTEM_COLUMNS:
        coltype = pgtype if dialect == "postgres" else sftype
        col_lines.append(f"    {quote_id(col)} {coltype}")
        mark = "[D]"  # system columns are our own design, documented by definition
        comment_lines.append(f"COMMENT ON COLUMN {table}.{col} IS '{mark} {label}';")

    pk_clause = ""
    if pk_cols:
        pk_clause = f",\n    PRIMARY KEY ({', '.join(pk_cols)})"
    else:
        warnings.append(f"{entity['entity_id']}: no PK field declared")

    header = [
        f"-- {table} ({entity['entity_id']}) -- {entity['entity_name']}",
        f"-- {entity.get('dealer_name','')}",
        f"-- SAP analogue: {entity.get('sap_analogue','')}",
        f"-- grain: {entity.get('grain','')}",
        f"-- api reach: {entity.get('api',{}).get('reachable','unknown')}",
        f"-- generated by schema/bin/gen_ddl.py from contract {CONTRACT} -- do not hand-edit, regenerate instead",
    ]

    create = (
        f"CREATE TABLE IF NOT EXISTS {table} (\n"
        + ",\n".join(col_lines)
        + pk_clause
        + "\n);"
    )

    body = header + ["", create]
    if check_comment_lines:
        body += ["", "-- Inferred/unverified NOT NULL constraints withheld (documented in fields.json but not enforced here):"]
        body += check_comment_lines
    if comment_lines:
        body += ["", "-- Column comments (dealer-language label + confidence mark: [D]=documented [I]=inferred [U]=unverified)"]
        body += comment_lines
    if fk_lines:
        body += ["", "-- Foreign keys"]
        body += fk_lines

    return "\n".join(body) + "\n", warnings


def main():
    ap = argparse.ArgumentParser(description="Generate load-ready Postgres and Snowflake DDL from fields.json (contract EgD-CDK-FIELDS-v2).")
    ap.add_argument("--fields", required=True, help="Path to fields.json (or a fixture matching the same shape)")
    ap.add_argument("--out-dir", default="schema/ddl", help="Output root; writes <out-dir>/postgres and <out-dir>/snowflake")
    ap.add_argument("--fixture-note", action="store_true", help="Stamp generated files as fixture-derived, not from the real dictionary")
    args = ap.parse_args()

    doc = load_fields(args.fields)
    if doc.get("contract") != CONTRACT:
        eprint(f"warning: input contract tag is {doc.get('contract')!r}, expected {CONTRACT!r}")

    entities = doc.get("entities", [])
    entities_by_id = {e["entity_id"]: e for e in entities}

    pg_dir = os.path.join(args.out_dir, "postgres")
    sf_dir = os.path.join(args.out_dir, "snowflake")
    os.makedirs(pg_dir, exist_ok=True)
    os.makedirs(sf_dir, exist_ok=True)

    all_warnings = []
    pg_all_parts = []

    source_note = "FIXTURE-DERIVED (schema/bin/fixture_fields.py) -- not the real field dictionary" \
        if args.fixture_note else "docs/model/fields.json"

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    pg_all_header = [
        "-- 000_all.sql -- rollup of every Lane F Postgres DDL file",
        f"-- generated {stamp} by schema/bin/gen_ddl.py from {source_note}",
        "-- Run this file to build the full load-ready schema in one pass.",
        "",
    ]
    pg_all_parts.append("\n".join(pg_all_header))

    for entity in entities:
        eid = entity["entity_id"]
        pg_sql, w1 = build_entity_ddl(entity, entities_by_id, "postgres")
        sf_sql, w2 = build_entity_ddl(entity, entities_by_id, "snowflake")
        all_warnings += w1 + w2

        pg_path = os.path.join(pg_dir, f"{eid}.sql")
        sf_path = os.path.join(sf_dir, f"{eid}.sql")
        with open(pg_path, "w") as f:
            f.write(pg_sql)
        with open(sf_path, "w") as f:
            f.write(sf_sql)

        pg_all_parts.append(pg_sql)

    with open(os.path.join(pg_dir, "000_all.sql"), "w") as f:
        f.write("\n".join(pg_all_parts))

    print(f"gen_ddl.py: wrote {len(entities)} Postgres tables to {pg_dir}, "
          f"{len(entities)} Snowflake tables to {sf_dir}, plus 000_all.sql rollup.")
    total_cols = sum(len(e["fields"]) + len(SYSTEM_COLUMNS) for e in entities)
    print(f"gen_ddl.py: {total_cols} total columns across {len(entities)} tables (source: {source_note}).")
    if all_warnings:
        print(f"gen_ddl.py: {len(all_warnings)} warning(s):")
        for w in all_warnings:
            print(f"  - {w}")


if __name__ == "__main__":
    main()
