#!/usr/bin/env python3
"""
reconcile.py — Peterbilt Atlantic / CDK Drive twin, tie-out reconciliation runner.

Runs the five reconciliation statements documented in tieout/README.md against the
normalised extract output under extract/out/<month>/, and emits a markdown + JSON
report with per-statement pass/fail, variance amounts, and a populated break register.

Designed to run BEFORE extract/out/ exists: every statement degrades to a clearly
labelled "NOT RUN — input file missing" result instead of raising, so this script is
safe to run, and useful to read, on day zero. Stdlib only. Uses pandas for convenience
if it happens to be installed, but never requires it.

    python3 tieout/bin/reconcile.py --help
    python3 tieout/bin/reconcile.py --month 2026-06 --extract-dir extract/out --out-dir tieout/reports

Confidence: the tolerance thresholds and file-path conventions here are INFERRED —
this repo's own proposal, not a confirmed CDK/PACCAR standard. See tieout/README.md.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

try:
    import pandas as pd  # optional — used only if present, never required
    HAVE_PANDAS = True
except ImportError:
    HAVE_PANDAS = False

# ---------------------------------------------------------------------------
# Tolerance policy — see docs/tieout/tieout-plan.json "tolerance_policy" and
# tieout/README.md. Kept in sync by hand; this is the single source of truth
# for the numbers this script actually applies.
# ---------------------------------------------------------------------------
CLEAN_TIE_PCT = 0.0005      # 0.05%
TOLERABLE_ABS = 25.00       # dollars
TOLERABLE_PCT = 0.0025      # 0.25%

BREAK_REGISTER_COLUMNS = [
    "break_id", "date_found", "chain_step", "schedule_or_account", "our_figure",
    "reported_figure", "variance_amount", "variance_pct", "tier", "root_cause",
    "owner", "status", "closed_date",
]

STATEMENTS = ["a", "b", "c", "d", "e"]
STATEMENT_TITLES = {
    "a": "Transaction counts and dollars complete for the month",
    "b": "Accounting schedule open items sum to GL account balance at month-end",
    "c": "Departmental gross profit (RO labour/parts) matches reported department income statement",
    "d": "Trial balance debits equal credits and roll to reported balance sheet",
    "e": "Absorption rate recomputed from our data matches the reported figure",
}


def eprint(*a, **k):
    print(*a, file=sys.stderr, **k)


def classify_variance(our_value, reported_value):
    """Return (variance_amount, variance_pct, tier) per the tolerance policy."""
    if our_value is None or reported_value is None:
        return None, None, "NOT RUN"
    variance = our_value - reported_value
    base = abs(reported_value) if reported_value else abs(our_value)
    pct = (abs(variance) / base) if base else (0.0 if variance == 0 else 1.0)
    if variance == 0 and pct < CLEAN_TIE_PCT:
        tier = "Clean tie"
    elif abs(variance) <= TOLERABLE_ABS or pct <= TOLERABLE_PCT:
        tier = "Tolerable variance"
    else:
        tier = "Break"
    return round(variance, 2), round(pct * 100, 4), tier


def read_jsonl(path):
    """Read a .jsonl file into a list of dicts. Returns None if the file does not exist."""
    if not os.path.isfile(path):
        return None
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                eprint(f"  ! warning: {path}:{line_no} could not be parsed as JSON ({e}) — skipped")
    return rows


def find_input(extract_dir, month, *candidates):
    """Try a list of candidate relative paths under extract_dir for a given month;
    return the first that exists, else None. Supports both a flat
    extract/out/<month>/<file>.jsonl layout and an extract/out/<file>.jsonl
    layout with an embedded month/date column, since the extract lane's exact
    layout is not fixed as of this writing."""
    month_dir = os.path.join(extract_dir, month)
    for c in candidates:
        p1 = os.path.join(month_dir, c)
        if os.path.isfile(p1):
            return p1
        p2 = os.path.join(extract_dir, c)
        if os.path.isfile(p2):
            return p2
    return None


def sum_field(rows, field):
    total = 0.0
    n = 0
    for r in rows:
        v = r.get(field)
        if isinstance(v, (int, float)):
            total += v
            n += 1
    return total, n


def not_run(statement, reason):
    return {
        "statement": statement,
        "title": STATEMENT_TITLES[statement],
        "status": "NOT RUN",
        "reason": reason,
        "variance_amount": None,
        "variance_pct": None,
        "detail": [],
    }


def run_statement_a(extract_dir, month):
    """Transaction counts and dollars complete for the month."""
    classes = {
        "repair_orders": "repair_orders.jsonl",
        "ro_labour_lines": "ro_labour_lines.jsonl",
        "ro_part_lines": "ro_part_lines.jsonl",
        "counter_parts_sales": "counter_parts_sales.jsonl",
        "deal_jackets": "deal_jackets.jsonl",
        "ap_documents": "ap_documents.jsonl",
        "gl_journal_postings": "gl_journal_postings.jsonl",
    }
    found_any = False
    detail = []
    for name, fname in classes.items():
        path = find_input(extract_dir, month, fname)
        if path is None:
            detail.append({"class": name, "status": "NOT RUN — input file missing",
                            "expected_path": os.path.join(extract_dir, month, fname)})
            continue
        found_any = True
        rows = read_jsonl(path) or []
        amt_field = "extended_amount" if any("extended_amount" in r for r in rows[:5]) else "amount"
        total, n = sum_field(rows, amt_field)
        detail.append({"class": name, "status": "READ", "path": path,
                        "row_count": len(rows), "amount_field": amt_field,
                        "amount_sum": round(total, 2)})
    if not found_any:
        return not_run("a", f"no extract files found under {os.path.join(extract_dir, month)}/")
    return {
        "statement": "a",
        "title": STATEMENT_TITLES["a"],
        "status": "READ — no CDK-side control total supplied to compare against; row/dollar counts captured for manual cross-check",
        "reason": None,
        "variance_amount": None,
        "variance_pct": None,
        "detail": detail,
    }


def run_statement_b(extract_dir, month):
    """Each accounting schedule's open items sum to its GL account balance at month-end."""
    sched_dir = os.path.join(extract_dir, month, "accounting_schedules")
    if not os.path.isdir(sched_dir):
        return not_run("b", f"schedule directory not found: {sched_dir}/")
    detail = []
    files = sorted(f for f in os.listdir(sched_dir) if f.endswith(".jsonl"))
    if not files:
        return not_run("b", f"no *.jsonl files found in {sched_dir}/")
    gl_path = find_input(extract_dir, month, "gl_journal_postings.jsonl")
    gl_rows = read_jsonl(gl_path) if gl_path else None
    for fname in files:
        rows = read_jsonl(os.path.join(sched_dir, fname)) or []
        open_total, _ = sum_field([r for r in rows if r.get("status") == "open"], "open_item_amount")
        account_no = rows[0].get("gl_account") if rows else None
        gl_balance = None
        if gl_rows and account_no:
            matched = [r for r in gl_rows if r.get("account_number") == account_no]
            debits, _ = sum_field(matched, "debit_amount")
            credits, _ = sum_field(matched, "credit_amount")
            gl_balance = debits - credits
        variance, pct, tier = classify_variance(open_total, gl_balance) if gl_balance is not None else (None, None, "NOT RUN — no matching GL account rows")
        detail.append({"schedule_file": fname, "gl_account": account_no,
                        "schedule_open_total": round(open_total, 2), "gl_balance": gl_balance,
                        "variance_amount": variance, "variance_pct": pct, "tier": tier})
    return {
        "statement": "b", "title": STATEMENT_TITLES["b"], "status": "RUN",
        "reason": None, "variance_amount": None, "variance_pct": None, "detail": detail,
    }


def run_statement_c(extract_dir, month):
    """Departmental gross profit rebuilt from RO labour/parts lines vs reported department income statement."""
    labour_path = find_input(extract_dir, month, "ro_labour_lines.jsonl")
    parts_path = find_input(extract_dir, month, "ro_part_lines.jsonl")
    counter_path = find_input(extract_dir, month, "counter_parts_sales.jsonl")
    reported_path = find_input(extract_dir, month, "reported_department_income_statement.jsonl",
                                "department_income_statement.jsonl")
    if labour_path is None and parts_path is None:
        return not_run("c", "ro_labour_lines.jsonl and ro_part_lines.jsonl both missing")

    dept_gp = {}

    def accumulate(rows, sale_field, cost_field):
        for r in rows or []:
            dept = r.get("department") or r.get("department_id") or "UNKNOWN"
            sale = r.get(sale_field) or 0
            cost = r.get(cost_field) or 0
            dept_gp[dept] = dept_gp.get(dept, 0.0) + (sale - cost)

    accumulate(read_jsonl(labour_path), "labour_sale_amount", "labour_cost_amount")
    accumulate(read_jsonl(parts_path), "parts_sale_amount", "parts_cost_amount")
    accumulate(read_jsonl(counter_path), "sale_amount", "cost_amount")

    reported_rows = read_jsonl(reported_path) if reported_path else None
    detail = []
    for dept, gp in sorted(dept_gp.items()):
        reported_gp = None
        if reported_rows:
            match = next((r for r in reported_rows if r.get("department") == dept), None)
            if match:
                reported_gp = match.get("gross_profit")
        variance, pct, tier = classify_variance(gp, reported_gp)
        detail.append({"department": dept, "rebuilt_gross_profit": round(gp, 2),
                        "reported_gross_profit": reported_gp,
                        "variance_amount": variance, "variance_pct": pct,
                        "tier": tier if reported_gp is not None else "NOT RUN — no reported figure supplied"})
    if reported_path is None:
        note = ("reported_department_income_statement.jsonl not found — rebuilt gross profit "
                "captured for manual cross-check against the report-export figure")
    else:
        note = None
    return {
        "statement": "c", "title": STATEMENT_TITLES["c"],
        "status": "RUN" if reported_path else "PARTIAL — rebuild only, no reported figure to compare",
        "reason": note, "variance_amount": None, "variance_pct": None, "detail": detail,
    }


def run_statement_d(extract_dir, month):
    """Trial balance debits equal credits and roll to reported balance sheet."""
    gl_path = find_input(extract_dir, month, "gl_journal_postings.jsonl")
    if gl_path is None:
        return not_run("d", "gl_journal_postings.jsonl not found")
    rows = read_jsonl(gl_path) or []
    debits, _ = sum_field(rows, "debit_amount")
    credits, _ = sum_field(rows, "credit_amount")
    internal_variance = round(debits - credits, 2)
    internal_tier = "Clean tie" if internal_variance == 0 else "Break — extract not internally balanced"

    bs_path = find_input(extract_dir, month, "reported_balance_sheet.jsonl")
    bs_rows = read_jsonl(bs_path) if bs_path else None
    detail = [{
        "check": "debits = credits (internal identity)",
        "total_debits": round(debits, 2), "total_credits": round(credits, 2),
        "variance_amount": internal_variance, "tier": internal_tier,
    }]
    if bs_rows:
        by_account = {}
        for r in rows:
            acct = r.get("account_number")
            by_account[acct] = by_account.get(acct, 0.0) + (r.get("debit_amount") or 0) - (r.get("credit_amount") or 0)
        for bl in bs_rows:
            acct = bl.get("account_number")
            reported_balance = bl.get("balance")
            our_balance = by_account.get(acct)
            variance, pct, tier = classify_variance(our_balance, reported_balance)
            detail.append({"check": "balance sheet roll-up", "account_number": acct,
                            "our_balance": our_balance, "reported_balance": reported_balance,
                            "variance_amount": variance, "variance_pct": pct, "tier": tier})
    else:
        detail.append({"check": "balance sheet roll-up",
                        "status": "NOT RUN — reported_balance_sheet.jsonl not found"})
    return {
        "statement": "d", "title": STATEMENT_TITLES["d"],
        "status": "RUN" if bs_rows else "PARTIAL — internal identity checked, no reported balance sheet to roll up to",
        "reason": None, "variance_amount": internal_variance, "variance_pct": None, "detail": detail,
    }


def run_statement_e(statement_c_result, statement_d_result, extract_dir, month):
    """Absorption rate recomputed from statements (c) and (d), vs reported figure."""
    if statement_c_result.get("status") == "NOT RUN" or statement_d_result.get("status") == "NOT RUN":
        return not_run("e", "requires statements (c) and (d) to have run first")

    fixed_ops = {"Parts", "Service", "Body Shop"}
    total_gp = sum(d.get("rebuilt_gross_profit", 0) or 0 for d in statement_c_result.get("detail", []))
    fixed_gp = sum(d.get("rebuilt_gross_profit", 0) or 0
                   for d in statement_c_result.get("detail", []) if d.get("department") in fixed_ops)

    total_expense = None
    for d in statement_d_result.get("detail", []):
        if d.get("account_number") in ("TOTAL_EXPENSE", "total_expense"):
            total_expense = d.get("our_balance")

    reported_path = find_input(extract_dir, month, "reported_absorption.jsonl")
    reported_rows = read_jsonl(reported_path) if reported_path else None
    reported_total = reported_rows[0].get("total_absorption_pct") if reported_rows else None
    reported_fixed = reported_rows[0].get("fixed_absorption_pct") if reported_rows else None

    detail = []
    if total_expense:
        our_total_absorption = round(100 * total_gp / total_expense, 2)
        our_fixed_absorption = round(100 * fixed_gp / total_expense, 2)
        v1, p1, t1 = classify_variance(our_total_absorption, reported_total)
        v2, p2, t2 = classify_variance(our_fixed_absorption, reported_fixed)
        detail.append({"metric": "Total Absorption %", "our_value": our_total_absorption,
                        "reported_value": reported_total, "variance_amount": v1, "tier": t1})
        detail.append({"metric": "Fixed Absorption %", "our_value": our_fixed_absorption,
                        "reported_value": reported_fixed, "variance_amount": v2, "tier": t2})
        status = "RUN" if reported_rows else "PARTIAL — recomputed, no reported figure to compare"
        reason = None if reported_rows else "reported_absorption.jsonl not found"
    else:
        status = "NOT RUN"
        reason = "total dealership expense (TOTAL_EXPENSE row) not available from statement (d)"
    return {
        "statement": "e", "title": STATEMENT_TITLES["e"], "status": status,
        "reason": reason, "variance_amount": None, "variance_pct": None, "detail": detail,
    }


def build_break_register(results):
    """Flatten every 'Break' tier finding across all statements into the register schema."""
    register = []
    break_id = 1
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for stmt_key, result in results.items():
        for d in result.get("detail", []):
            tier = d.get("tier", "")
            if not tier or "Break" not in tier:
                continue
            register.append({
                "break_id": f"BRK-{break_id:03d}",
                "date_found": now,
                "chain_step": stmt_key,
                "schedule_or_account": d.get("schedule_file") or d.get("department") or d.get("account_number") or d.get("metric") or "",
                "our_figure": d.get("schedule_open_total") or d.get("rebuilt_gross_profit") or d.get("our_balance") or d.get("our_value"),
                "reported_figure": d.get("gl_balance") or d.get("reported_gross_profit") or d.get("reported_balance") or d.get("reported_value"),
                "variance_amount": d.get("variance_amount"),
                "variance_pct": d.get("variance_pct"),
                "tier": tier,
                "root_cause": "",
                "owner": "",
                "status": "OPEN",
                "closed_date": "",
            })
            break_id += 1
    return register


def render_markdown(month, results, register, extract_dir):
    lines = []
    lines.append(f"# Tie-out reconciliation report — {month}")
    lines.append("")
    lines.append(f"Generated {datetime.now(timezone.utc).isoformat()} by `tieout/bin/reconcile.py`.")
    lines.append(f"Extract source directory: `{extract_dir}`.")
    lines.append("")
    lines.append("See [`tieout/README.md`](../README.md) for the method behind each statement, and")
    lines.append("[the Tie-Out Board](https://eveglyphdesign.github.io/eve-hawkins-cdk-twin/tieout/) for the clickable chain.")
    lines.append("")
    lines.append("## Statement results")
    lines.append("")
    lines.append("| Statement | Title | Status |")
    lines.append("|---|---|---|")
    for key in STATEMENTS:
        r = results[key]
        lines.append(f"| ({key}) | {r['title']} | {r['status']} |")
    lines.append("")
    for key in STATEMENTS:
        r = results[key]
        lines.append(f"### ({key}) {r['title']}")
        lines.append("")
        lines.append(f"**Status:** {r['status']}")
        if r.get("reason"):
            lines.append(f"**Reason:** {r['reason']}")
        lines.append("")
        if r.get("detail"):
            lines.append("```json")
            lines.append(json.dumps(r["detail"], indent=2, default=str))
            lines.append("```")
        else:
            lines.append("_No detail rows — nothing was found to reconcile._")
        lines.append("")
    lines.append("## Break register")
    lines.append("")
    if register:
        lines.append("| " + " | ".join(BREAK_REGISTER_COLUMNS) + " |")
        lines.append("|" + "---|" * len(BREAK_REGISTER_COLUMNS))
        for row in register:
            lines.append("| " + " | ".join(str(row.get(c, "")) for c in BREAK_REGISTER_COLUMNS) + " |")
    else:
        lines.append("No breaks logged. Either every statement passed within tolerance, or every")
        lines.append("statement is `NOT RUN` because the relevant extract file does not exist yet.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("© 2026 EVEglyphDesign. Controlled copy. *Pour le bien-être du peuple.*")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Reconcile the dealer's reported June 2026 financials against our own "
                     "extracted CDK Drive / PACCAR data, per tieout/README.md statements (a)-(e).",
    )
    parser.add_argument("--month", default="2026-06",
                         help="Tie-out month, YYYY-MM (default: 2026-06, the middle of the "
                              "default three-month extraction window).")
    parser.add_argument("--extract-dir", default="extract/out",
                         help="Root directory of normalised extract output (default: extract/out). "
                              "Expected layout: <extract-dir>/<month>/<file>.jsonl")
    parser.add_argument("--out-dir", default="tieout/reports",
                         help="Directory to write the markdown + JSON report into "
                              "(default: tieout/reports). Created if missing.")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress messages on stderr.")
    args = parser.parse_args()

    if not args.quiet:
        eprint(f"tieout/bin/reconcile.py — month={args.month} extract_dir={args.extract_dir} "
               f"pandas={'available' if HAVE_PANDAS else 'not installed, degrading to stdlib'}")

    if not os.path.isdir(args.extract_dir):
        eprint(f"note: extract directory '{args.extract_dir}' does not exist yet — "
               f"every statement below will report NOT RUN. This is expected before the "
               f"extract lane's output lands.")

    results = {}
    results["a"] = run_statement_a(args.extract_dir, args.month)
    results["b"] = run_statement_b(args.extract_dir, args.month)
    results["c"] = run_statement_c(args.extract_dir, args.month)
    results["d"] = run_statement_d(args.extract_dir, args.month)
    results["e"] = run_statement_e(results["c"], results["d"], args.extract_dir, args.month)

    register = build_break_register(results)

    os.makedirs(args.out_dir, exist_ok=True)
    md = render_markdown(args.month, results, register, args.extract_dir)
    md_path = os.path.join(args.out_dir, f"reconcile-{args.month}.md")
    json_path = os.path.join(args.out_dir, f"reconcile-{args.month}.json")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    json_report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "month": args.month,
        "extract_dir": args.extract_dir,
        "statements": results,
        "break_register": register,
        "break_register_columns": BREAK_REGISTER_COLUMNS,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_report, f, indent=2, default=str)

    if not args.quiet:
        eprint(f"wrote {md_path}")
        eprint(f"wrote {json_path}")
        for key in STATEMENTS:
            eprint(f"  ({key}) {results[key]['status']}")
        eprint(f"  break register: {len(register)} OPEN row(s)")

    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
