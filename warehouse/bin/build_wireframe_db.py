#!/usr/bin/env python3
"""
EVEglyphDesign — CDK Twin / Warranty GENE warehouse wireframe loader.

Builds the star schema in ddl/wireframe.sql from a dealer-owned extract
directory and loads it. The database file is dealer property: it is written
outside the repository and is never committed.

Usage:
  python bin/build_wireframe_db.py --src /path/to/extracts --db /path/out/cdk_wireframe.db
"""
import argparse, csv, datetime, calendar, hashlib, json, os, sqlite3, sys

RUN_TS = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

FILES = {
    "closed_ro":    "Closed ROs.csv",
    "open_ro":      "Open ROs.csv",
    "customers":    "Customers.csv",
    "svc_cust":     "service customer sales.csv",
    "tot_cust":     "Customer total sales.csv",
}
PACCAR_REPORTS = ["P026", "P032", "P046", "P048"]

# Truck business only. The powersports lane is a separate domain on a separate VIN
# space and is excluded here by design, not by omission. Each excluded file is
# logged so the exclusion is visible in dq_exception rather than silent.
OUT_OF_SCOPE = {
    "Advantage plus customers.csv":  "BRP Advantage Plus service contracts — powersports lane",
    "Canada General contracts.csv":  "Canada General powersports service contracts",
    "All ~ Warranty On Demand.pdf":  "BRP Warranty on Demand claim records — powersports lane",
    "Warranty Guide EN_REV6 2021 (1).pdf": "BRP powersports warranty policy guide",
    "Moncton Retention_1787839708703.pdf": "Torque Motorsports Moncton retention report",
    "Retention_1787836691996.pdf":   "Torque Motorsports Woodstock retention report",
}

def rows(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for i, r in enumerate(csv.DictReader(fh), start=2):
            yield i, { (k.strip() if k else k): v for k, v in r.items() }

def money(s):
    if s is None: return None
    s = str(s).replace("$", "").replace(",", "").strip()
    if s in ("", "."): return None
    neg = s.startswith("-") or (s.startswith("(") and s.endswith(")"))
    s = s.strip("-()")
    try: v = float(s)
    except ValueError: return None
    return -v if neg else v

def num(s):
    return money(s)

def d(s):
    if not s: return None
    s = str(s).split(" ")[0].strip()
    for f in ("%m/%d/%Y", "%Y-%m-%d", "%m/%d/%y"):
        try: return datetime.datetime.strptime(s, f).date().isoformat()
        except ValueError: pass
    return None

def long_date(s):
    # 'Sunday, July 26, 2026'
    if not s: return None
    try: return datetime.datetime.strptime(s.strip(), "%A, %B %d, %Y").date().isoformat()
    except ValueError: return d(s)

def add_months(iso, m):
    if not iso or m is None: return None
    y, mo, day = (int(x) for x in iso.split("-"))
    tot = (mo - 1) + int(m); y += tot // 12; mo = tot % 12 + 1
    return datetime.date(y, mo, min(day, calendar.monthrange(y, mo)[1])).isoformat()

class DQ:
    def __init__(self): self.rows = []
    def add(self, src, rowid, rule, sev, detail, val):
        self.rows.append((src, str(rowid), rule, sev, detail, str(val)[:200], RUN_TS))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--db", required=True)
    ap.add_argument("--ddl", default=os.path.join(os.path.dirname(__file__), "..", "ddl", "wireframe.sql"))
    ap.add_argument("--profile-out", default=None, help="write aggregate-only profile JSON here")
    a = ap.parse_args()

    if os.path.exists(a.db): os.remove(a.db)
    con = sqlite3.connect(a.db); con.executescript(open(a.ddl).read())
    cur = con.cursor(); dq = DQ()
    src = lambda n: os.path.join(a.src, n)

    # ---- dim_rooftop -------------------------------------------------------
    # Derived, never hardcoded. Seeded from the UNION of the closed and open RO
    # extracts: the closed extract was pulled against a subset of the group's
    # service accounts, so seeding from it alone silently shrinks the dealership.
    # Labels stay NULL until the dealership confirms them; codes are not decoded
    # by guesswork.
    roof = {}
    for fname, ctr in (("Closed ROs.csv", "closed"), ("Open ROs.csv", "open")):
        p = src(fname)
        if not os.path.exists(p):
            dq.add(fname, "", "SOURCE_MISSING", "WARN", "RO extract not present", ""); continue
        for _rid, r in rows(p):
            sa = (r.get("Service Account") or "").strip()
            aa = (r.get("Accounting Account") or "").strip()
            if not sa:
                continue
            rd = roof.setdefault(sa, {"aa": aa, "closed": 0, "open": 0})
            rd[ctr] += 1
    for sa in sorted(roof):
        rd = roof[sa]
        cur.execute("INSERT INTO dim_rooftop VALUES (?,?,?,?,?,?,?,?)",
                    (sa, rd["aa"], None, None, "UNVERIFIED",
                     1 if rd["closed"] else 0, rd["closed"], rd["open"]))
        if not rd["closed"]:
            dq.add("Open ROs.csv", sa, "ROOFTOP_CLOSED_HISTORY_MISSING", "WARN",
                   "service account appears in open ROs but has no closed-RO history "
                   "in this extract set; service-history and whitespace measures "
                   "understate activity at this rooftop", sa)
    print(f"dim_rooftop: {len(roof)} service accounts "
          f"({sum(1 for v in roof.values() if v['closed'])} with closed history)")

    # ---- PACCAR warranty registrations -> dim_unit, dim_warranty_option, fact
    opts, units, wreg = {}, {}, {}
    for rep in PACCAR_REPORTS:
        p = src(f"{rep}.csv")
        if not os.path.exists(p):
            dq.add(f"{rep}.csv", "", "SOURCE_MISSING", "WARN", "report not present in extract set", ""); continue
        for rid, r in rows(p):
            vin8 = (r.get("VIN8") or "").strip().upper()
            if len(vin8) != 8:
                dq.add(f"{rep}.csv", rid, "VIN8_LENGTH", "BLOCK", "VIN8 not 8 characters", vin8); continue
            oc = (r.get("WARRANTY_OPTION_CD") or "").strip()
            isd = d(r.get("IN_SERVICE_DT"))
            mm  = int(float(r["WARRANTY_MAX_MONTHS_NUM"])) if (r.get("WARRANTY_MAX_MONTHS_NUM") or "").strip() else None
            mi  = int(float(r["WARRANTY_MAX_MILES_NUM"]))  if (r.get("WARRANTY_MAX_MILES_NUM")  or "").strip() else None
            opts.setdefault(oc, (oc, (r.get("WARRANTY_TYPE_CD") or "").strip(),
                                 (r.get("WARRANTY_SUB_TYPE_CD") or "").strip(),
                                 (r.get("WARRANTY_DESC") or "").strip(), mm, mi))
            city = (r.get("CUSTOMER_WARR_REG_CITY_NAME") or "").strip()
            units.setdefault(vin8, {"vin8": vin8, "model": (r.get("MODEL_DESC") or "").strip(),
                                    "isd": isd, "owner": (r.get("CUSTOMER_NAME_WARR_REG") or "").strip(),
                                    "city": None if city in ("", "N/A") else city, "rep": rep})
            if isd is None:
                dq.add(f"{rep}.csv", rid, "DATE_PARSE", "WARN", "in-service date missing/unparseable", r.get("IN_SERVICE_DT"))
            key = f"{vin8}:{oc}"
            wreg[key] = (key, vin8, oc, isd, isd, add_months(isd, mm), mi, rep, RUN_TS)
    cur.executemany("INSERT INTO dim_warranty_option VALUES (?,?,?,?,?,?)", list(opts.values()))

    # ---- customer master ---------------------------------------------------
    customers = {}
    p = src(FILES["customers"])
    if os.path.exists(p):
        for rid, r in rows(p):
            nf = (r.get("NAME-FILE") or "").strip()
            cnum = nf.split("*")[-1] if "*" in nf else nf
            if not cnum: continue
            ck = f"PNB-A:{cnum}"
            customers[ck] = (ck, cnum, "PNB-A", nf, (r.get("NAME") or "").strip(),
                             (r.get("COMPANYNAME") or "").strip(), (r.get("ADDRESS") or "").strip(),
                             (r.get("EMAIL") or "").strip(), (r.get("WORKPHONE") or "").strip(),
                             (r.get("CELLULAR") or "").strip(), (r.get("HOMEPHONE") or "").strip(),
                             d(r.get("ENTRY")), money(r.get("YTD-PURCH")), "CDK_CUSTOMER_MASTER")

    # ---- repair orders (closed + open) ------------------------------------
    advisors, ro_rows = {}, []
    def load_ro(fname, status):
        p = src(fname)
        if not os.path.exists(p):
            dq.add(fname, "", "SOURCE_MISSING", "WARN", "RO extract not present", ""); return
        for rid, r in rows(p):
            ron = (r.get("RO Number") or "").strip()
            if not ron: continue
            sa_acct = (r.get("Service Account") or "").strip()
            acct    = (r.get("Accounting Account") or "").strip()
            raw     = (r.get("Vehicle     ID") or r.get("Vehicle ID") or "").strip().upper()
            vin8 = None
            if len(raw) == 8: vin8 = raw
            elif len(raw) == 17: vin8 = raw[-8:]
            else:
                dq.add(fname, rid, "VIN8_LENGTH", "WARN",
                       f"vehicle id is {len(raw)} chars; not joinable to warranty registration", raw)
            cnum = (r.get("Customer Number") or "").strip()
            ck = f"{acct or 'PNB-A'}:{cnum}" if cnum else None
            if ck and ck not in customers:
                customers[ck] = (ck, cnum, acct or "PNB-A", None, (r.get("Customer Name") or "").strip(),
                                 None, None, None, None, None, None, None, None, "CDK_RO")
                dq.add(fname, rid, "CUST_UNKNOWN", "INFO", "customer on RO absent from customer master", cnum)
            sa_id = (r.get("SA ID") or "").strip()
            sa_key = f"{sa_acct}:{sa_id}" if sa_id else None
            if sa_key: advisors.setdefault(sa_key, (sa_key, sa_id, (r.get("SA Name") or "").strip(), sa_acct))
            ro_rows.append((f"{sa_acct}:{ron}", ron, status, sa_acct, acct, vin8, raw, ck, sa_key,
                            d(r.get("Open Date")), d(r.get("Closed Date")), num(r.get("Mileage")),
                            money(r.get("Total Sales")), money(r.get("Total Gross Profit")),
                            money(r.get("Labor Sales")), money(r.get("Labor Gross Profit")),
                            money(r.get("Parts Sales")), money(r.get("Parts Gross Profit")),
                            money(r.get("Misc Sales")), money(r.get("Misc Gross Profit")),
                            money(r.get("Sublet Sales")), money(r.get("Sublet Gross Profit")),
                            num(r.get("Actual Hours")), num(r.get("Sold Hours")),
                            money(r.get("Tech Effective Labor Rate")), money(r.get("RO Effective Labor Rate")),
                            num(r.get("Efficiency Percent")), num(r.get("Parts to Labor %")), RUN_TS))
    load_ro(FILES["closed_ro"], "CLOSED")
    load_ro(FILES["open_ro"],   "OPEN")

    cur.executemany("INSERT INTO dim_customer VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", list(customers.values()))
    cur.executemany("INSERT INTO dim_service_advisor VALUES (?,?,?,?)", list(advisors.values()))
    seen = set(); dedup = []
    for row in ro_rows:
        if row[0] in seen:
            dq.add("RO extracts", row[1], "RO_DUPLICATE", "WARN", "ro_key seen twice across open/closed", row[0]); continue
        seen.add(row[0]); dedup.append(row)
    cur.executemany(f"INSERT INTO fact_repair_order VALUES ({','.join('?'*29)})", dedup)

    # ---- dim_unit: union of registered units and serviced units -----------
    cur.execute("SELECT vin8, MIN(open_dt), MAX(COALESCE(closed_dt,open_dt)), MAX(odometer) "
                "FROM fact_repair_order WHERE vin8 IS NOT NULL GROUP BY vin8")
    svc = {v: (a, b, c) for v, a, b, c in cur.fetchall()}
    unit_rows = []
    for vin8 in set(units) | set(svc):
        u = units.get(vin8); s = svc.get(vin8)
        unit_rows.append((vin8, None, u["model"] if u else None, u["isd"] if u else None,
                          u["owner"] if u else None, u["city"] if u else None, u["rep"] if u else None,
                          1 if u else 0, 1 if s else 0,
                          s[0] if s else None, s[1] if s else None, s[2] if s else None))
    cur.executemany(f"INSERT INTO dim_unit VALUES ({','.join('?'*12)})", unit_rows)
    cur.executemany(f"INSERT INTO fact_warranty_registration VALUES ({','.join('?'*9)})", list(wreg.values()))

    # ---- out-of-scope sources, logged not loaded -------------------------
    for fname, why in OUT_OF_SCOPE.items():
        if os.path.exists(src(fname)):
            dq.add(fname, None, "SCOPE_EXCLUDED", "INFO",
                   "present in the extract set and deliberately not loaded: "
                   "this wireframe is the truck business only — " + why, fname)

    # ---- reconciliation aggregates --------------------------------------
    p = src(FILES["svc_cust"]); agg1 = []
    if os.path.exists(p):
        for rid, r in rows(p):
            cnum = (r.get("Customer Number") or "").strip()
            if not cnum: continue
            acct = (r.get("Account") or "PNB-A").strip()
            agg1.append((f"{acct}:{cnum}", d(r.get("Start Date:")), d(r.get("End Date:")), acct,
                         int(num(r.get("ROs")) or 0), money(r.get("Total Sales")), money(r.get("Total Gross Profit")),
                         money(r.get("Customer Pay Sales")), money(r.get("Customer Pay Gross Profit")),
                         money(r.get("Internal Sales")), money(r.get("Internal Gross Profit")),
                         money(r.get("Warranty Sales")), money(r.get("Warranty Gross Profit"))))
    cur.executemany(f"INSERT OR REPLACE INTO agg_customer_service_period VALUES ({','.join('?'*13)})", agg1)

    p = src(FILES["tot_cust"]); agg2 = []
    if os.path.exists(p):
        for rid, r in rows(p):
            cnum = (r.get("Customer Number") or "").strip()
            if not cnum: continue
            acct = (r.get("Account") or "PNB-A").strip()
            agg2.append((f"{acct}:{cnum}", d(r.get("Start Date:")), d(r.get("End Date:")),
                         (r.get("Ranked:") or "").strip(), money(r.get("Total Sales")),
                         money(r.get("Total Gross Profit")), money(r.get("Service Sales")),
                         money(r.get("Service Gross Profit")), money(r.get("Parts Sales")),
                         money(r.get("Parts Gross Profit")), money(r.get("New Vehicle Sales")),
                         money(r.get("Used Vehicle Sales")), int(num(r.get("Doc Refer Count")) or 0)))
    cur.executemany(f"INSERT OR REPLACE INTO agg_customer_total_sales VALUES ({','.join('?'*13)})", agg2)

    # ---- date dimension --------------------------------------------------
    cur.execute("SELECT MIN(x), MAX(x) FROM (SELECT open_dt x FROM fact_repair_order UNION "
                "SELECT closed_dt FROM fact_repair_order UNION SELECT coverage_start_dt FROM fact_warranty_registration "
                "UNION SELECT coverage_end_dt FROM fact_warranty_registration) WHERE x IS NOT NULL")
    lo, hi = cur.fetchone()
    if lo and hi:
        cur_d = datetime.date.fromisoformat(lo); end = datetime.date.fromisoformat(hi); dr = []
        while cur_d <= end:
            dr.append((cur_d.isoformat(), cur_d.year, (cur_d.month-1)//3+1, cur_d.month,
                       cur_d.strftime("%B"), cur_d.day, cur_d.isoweekday(), cur_d.year))
            cur_d += datetime.timedelta(days=1)
        cur.executemany("INSERT INTO dim_date VALUES (?,?,?,?,?,?,?,?)", dr)

    cur.executemany("INSERT INTO dq_exception (source_file,source_rowid,rule_code,severity,detail,"
                    "observed_value,detected_at) VALUES (?,?,?,?,?,?,?)", dq.rows)
    con.commit()

    # ---- aggregate-only profile (safe to publish) ------------------------
    prof = {"generated_utc": RUN_TS, "tables": {}, "marts": {}, "dq": {}}
    for t in ["dim_rooftop","dim_customer","dim_unit","dim_warranty_option","dim_service_advisor",
              "dim_date","fact_warranty_registration","fact_repair_order",
              "agg_customer_service_period","agg_customer_total_sales","dq_exception"]:
        prof["tables"][t] = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    for v in ["v_rich_target","v_whitespace_registered_never_serviced","v_coverage_expiring_180d",
              "v_serviced_unregistered","v_unit_service_profile"]:
        prof["marts"][v] = cur.execute(f"SELECT COUNT(*) FROM {v}").fetchone()[0]
    prof["marts"]["v_rich_target_by_reach_class"] = dict(
        cur.execute("SELECT reach_class, COUNT(*) FROM v_rich_target GROUP BY 1").fetchall())
    prof["dq"] = dict(cur.execute("SELECT rule_code||'/'||severity, COUNT(*) FROM dq_exception GROUP BY 1").fetchall())
    prof["ro_financials"] = dict(zip(["closed_ro_count","total_sales","total_gross_profit"],
        cur.execute("SELECT COUNT(*), ROUND(SUM(total_sales),2), ROUND(SUM(total_gross_profit),2) "
                    "FROM fact_repair_order WHERE ro_status='CLOSED'").fetchone()))
    print(json.dumps(prof, indent=2))
    if a.profile_out:
        with open(a.profile_out, "w") as fh: json.dump(prof, fh, indent=2)
    con.close()

if __name__ == "__main__":
    main()
