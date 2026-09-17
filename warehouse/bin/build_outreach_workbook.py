#!/usr/bin/env python3
"""
EVEglyphDesign — Warranty GENE
Opportunistic-diagnosis outreach workbook.

Reads the dealer-owned wireframe database and writes one worksheet per priority
band (P1..P4), each row a unit with every signal used to rank it plus the
contact details held for the customer on its most recent repair order.

Dealer payload. Never committed to a repository.
"""
import argparse, os, sqlite3, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

CREAM  = "FDFAF4"
CREAM2 = "F7F2E7"
INK    = "1A1A1A"
LINE   = "E7E1D3"
MUTE   = "6B665C"
ORANGE = "E87722"

BANDS = [
    ("P1", "P1 IN THE BAY, CLOSING",
     "On an open repair order right now with 30 days or less of coverage left on the binding axis. "
     "Diagnose before the truck leaves the property."),
    ("P2", "P2 IN THE BAY",
     "On an open repair order right now with coverage still live. The unit is already here; "
     "the only cost is diagnostic time."),
    ("P3", "P3 CALL NOW, CLOSING",
     "Known customer with service history here and 90 days or less of coverage left. "
     "Phone call, book it in."),
    ("P4", "P4 CALL, SCHEDULE",
     "Known customer with service history here and coverage still live beyond 90 days. "
     "Schedule against the next planned visit."),
]

SQL = """
WITH last_ro AS (
  SELECT f.vin8, f.customer_key, f.service_account, f.sa_key,
         COALESCE(f.closed_dt, f.open_dt) AS dt,
         ROW_NUMBER() OVER (PARTITION BY f.vin8
                            ORDER BY COALESCE(f.closed_dt, f.open_dt) DESC) AS rn
  FROM fact_repair_order f
  WHERE f.vin8 IS NOT NULL
),
open_ro AS (
  SELECT vin8,
         GROUP_CONCAT(DISTINCT ro_number)      AS open_ro_numbers,
         GROUP_CONCAT(DISTINCT service_account) AS open_rooftops,
         MIN(open_dt)                           AS open_since,
         SUM(total_sales)                       AS open_ro_sales
  FROM fact_repair_order WHERE ro_status = 'OPEN' AND vin8 IS NOT NULL
  GROUP BY vin8
)
SELECT q.band, q.priority_score, q.vin8,
       u.vin17, u.model_desc, u.in_service_dt,
       u.reg_owner_name, u.reg_owner_city, u.source_report,
       c.customer_name, c.company_name, c.customer_number, c.name_file,
       c.work_phone, c.cell_phone, c.home_phone, c.email_raw, c.address,
       o.open_ro_numbers, o.open_rooftops, o.open_since, o.open_ro_sales,
       l.service_account AS last_rooftop, sa.sa_name AS last_advisor,
       q.live_systems, q.live_coverages, q.exposure_weight,
       q.days_to_time_expiry, q.miles_remaining, q.miles_per_day, q.rate_status,
       q.days_to_mileage_ceiling, q.effective_days_remaining, q.binding_axis,
       q.ro_count, q.open_ro_count, q.last_ro_dt, q.max_odometer,
       s.first_ro_dt, s.lifetime_sales, s.lifetime_gross_profit,
       CASE WHEN d.in_closed_history = 1 THEN 'yes' ELSE 'no' END AS last_rooftop_history_present
FROM v_diagnosis_queue q
JOIN dim_unit u                ON u.vin8 = q.vin8
LEFT JOIN last_ro l            ON l.vin8 = q.vin8 AND l.rn = 1
LEFT JOIN dim_customer c       ON c.customer_key = l.customer_key
LEFT JOIN dim_service_advisor sa ON sa.sa_key = l.sa_key
LEFT JOIN dim_rooftop d        ON d.service_account = l.service_account
LEFT JOIN open_ro o            ON o.vin8 = q.vin8
LEFT JOIN v_unit_service_profile s ON s.vin8 = q.vin8
WHERE q.band = ?
ORDER BY q.priority_score DESC, q.effective_days_remaining ASC
"""

RECON_SQL = """
WITH cov AS (
  SELECT vin8,
         COUNT(*)                                                    AS coverage_rows,
         SUM(CASE WHEN is_time_active = 1 THEN 1 ELSE 0 END)         AS live_coverages,
         GROUP_CONCAT(DISTINCT CASE WHEN is_time_active = 1
                                    THEN warranty_sub_type_cd END)   AS live_systems,
         MIN(CASE WHEN is_time_active = 1 THEN coverage_end_dt END)  AS earliest_live_end,
         MAX(coverage_end_dt)                                        AS latest_end,
         MAX(max_miles)                                              AS highest_mile_ceiling,
         MIN(CASE WHEN is_time_active = 1 THEN miles_remaining_est END) AS miles_remaining
  FROM v_unit_coverage_state GROUP BY vin8
),
last_ro AS (
  SELECT vin8, customer_key, service_account, sa_key,
         ROW_NUMBER() OVER (PARTITION BY vin8
                            ORDER BY COALESCE(closed_dt, open_dt) DESC) AS rn
  FROM fact_repair_order WHERE vin8 IS NOT NULL
)
SELECT
  CASE WHEN u.is_warranty_registered = 1 AND u.is_service_known = 1 THEN 'BOTH SIDES'
       WHEN u.is_warranty_registered = 1                            THEN 'PACCAR ONLY'
       ELSE 'CDK ONLY' END                       AS match_status,
  u.vin8, u.vin17, u.model_desc, u.in_service_dt, u.source_report,
  u.reg_owner_name, u.reg_owner_city,
  cov.coverage_rows, cov.live_coverages, cov.live_systems,
  cov.earliest_live_end, cov.latest_end, cov.highest_mile_ceiling, cov.miles_remaining,
  CASE WHEN u.is_service_known = 1 THEN 'yes' ELSE 'no' END AS serviced_here,
  s.ro_count, s.open_ro_count, s.first_ro_dt, s.last_ro_dt, s.max_odometer,
  s.lifetime_sales, s.lifetime_gross_profit,
  l.service_account AS last_rooftop,
  CASE WHEN d.in_closed_history = 1 THEN 'yes'
       WHEN d.service_account IS NULL THEN NULL ELSE 'no' END AS last_rooftop_history_present,
  sa.sa_name AS last_advisor,
  c.customer_name, c.company_name, c.customer_number,
  CASE WHEN u.reg_owner_name IS NULL OR c.customer_name IS NULL THEN NULL
       WHEN UPPER(TRIM(u.reg_owner_name)) = UPPER(TRIM(c.customer_name)) THEN 'yes'
       ELSE 'no' END                             AS owner_name_matches_cdk,
  r.miles_per_day, r.rate_status,
  q.band, q.priority_score, q.binding_axis, q.effective_days_remaining,
  CASE
    WHEN q.band IS NOT NULL                       THEN NULL
    WHEN u.is_warranty_registered = 0             THEN 'no PACCAR registration in the extract set'
    WHEN COALESCE(cov.live_coverages, 0) = 0      THEN 'no coverage still live on the months axis'
    WHEN cov.miles_remaining IS NOT NULL
         AND cov.miles_remaining <= 0             THEN 'mileage ceiling already spent'
    WHEN LENGTH(u.vin8) <> 8                      THEN 'vehicle ID is not a VIN8, quarantined'
    ELSE 'not selected by the queue filter'
  END                                            AS excluded_because
FROM dim_unit u
LEFT JOIN cov                    ON cov.vin8 = u.vin8
LEFT JOIN v_unit_service_profile s ON s.vin8 = u.vin8
LEFT JOIN last_ro l              ON l.vin8 = u.vin8 AND l.rn = 1
LEFT JOIN dim_rooftop d          ON d.service_account = l.service_account
LEFT JOIN dim_service_advisor sa ON sa.sa_key = l.sa_key
LEFT JOIN dim_customer c         ON c.customer_key = l.customer_key
LEFT JOIN v_unit_mileage_rate r  ON r.vin8 = u.vin8
LEFT JOIN v_diagnosis_queue q    ON q.vin8 = u.vin8
ORDER BY CASE match_status WHEN 'BOTH SIDES' THEN 1 WHEN 'PACCAR ONLY' THEN 2 ELSE 3 END,
         COALESCE(q.priority_score, -1) DESC, u.vin8
"""

RECON_HEADERS = [
    ("Match status", 14),
    ("VIN8", 11), ("VIN17", 20), ("Model", 8),
    ("In service (PACCAR)", 17), ("PACCAR report", 13),
    ("Registered owner (PACCAR)", 30), ("Owner city", 16),
    ("Coverage rows (PACCAR)", 19), ("Live coverages", 13), ("Live covered systems", 20),
    ("Earliest live coverage end", 22), ("Latest coverage end", 18),
    ("Highest mileage ceiling", 20), ("Miles remaining", 15),
    ("Serviced here (CDK)", 17), ("RO count", 9), ("Open ROs", 9),
    ("First visit", 11), ("Last visit", 11), ("Last odometer", 14),
    ("Lifetime service sales", 20), ("Lifetime gross profit", 20),
    ("Last rooftop", 13), ("Last rooftop history in extract", 26), ("Last advisor", 22),
    ("Customer name (CDK)", 30), ("Company", 30), ("Customer no.", 13),
    ("Owner name matches CDK", 20),
    ("Measured miles/day", 17), ("Rate status", 17),
    ("Band", 22), ("Priority score", 13), ("Binding axis", 12), ("EFFECTIVE DAYS LEFT", 20),
    ("Why not in the queue", 40),
]

HEADERS = [
    ("Rank", 6), ("Priority score", 13), ("VIN8", 11), ("VIN17", 20),
    ("Model", 8), ("In service", 11),
    ("Registered owner (PACCAR)", 30), ("Owner city", 16), ("PACCAR report", 13),
    ("Customer name (CDK)", 30), ("Company", 30), ("Customer no.", 13), ("NAME-FILE", 13),
    ("Work phone", 15), ("Cell phone", 15), ("Home phone", 15),
    ("Email", 32), ("Address", 34),
    ("Open RO no.", 14), ("Open RO rooftop", 15), ("Open since", 11), ("Open RO sales", 14),
    ("Last rooftop", 13), ("Last advisor", 22),
    ("Live covered systems", 20), ("Live coverages", 13), ("Exposure weight", 14),
    ("Days left — months axis", 20), ("Miles remaining", 15),
    ("Measured miles/day", 17), ("Rate status", 17),
    ("Days left — miles axis", 20), ("EFFECTIVE DAYS LEFT", 20), ("Binding axis", 12),
    ("RO count", 9), ("Open ROs", 9), ("Last visit", 11), ("Last odometer", 14),
    ("First visit", 11), ("Lifetime service sales", 20), ("Lifetime gross profit", 20),
    ("Last rooftop history in extract", 26),
]

def style_sheet(ws, nrows, ncols):
    thin = Side(style="thin", color=LINE)
    hdr_fill = PatternFill("solid", fgColor=INK)
    for ci in range(1, ncols + 1):
        c = ws.cell(row=4, column=ci)
        c.font = Font(name="Inter", bold=True, size=9, color=CREAM)
        c.fill = hdr_fill
        c.alignment = Alignment(vertical="center", wrap_text=True)
        c.border = Border(bottom=Side(style="medium", color=ORANGE))
    ws.row_dimensions[4].height = 34
    band_fill = PatternFill("solid", fgColor=CREAM2)
    for ri in range(5, 5 + nrows):
        for ci in range(1, ncols + 1):
            c = ws.cell(row=ri, column=ci)
            c.font = Font(name="Inter", size=9, color=INK)
            c.border = Border(bottom=thin)
            if ri % 2 == 1:
                c.fill = band_fill
            c.alignment = Alignment(vertical="center")
    for ci, (_, w) in enumerate(HEADERS, start=1):
        ws.column_dimensions[get_column_letter(ci)].width = w
    ws.freeze_panes = "D5"
    ws.auto_filter.ref = f"A4:{get_column_letter(ncols)}{4 + nrows}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    con = sqlite3.connect(a.db)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    wb = Workbook()
    wb.remove(wb.active)

    counts = {}
    for short, band, blurb in BANDS:
        rows = cur.execute(SQL, (band,)).fetchall()
        counts[short] = len(rows)
        ws = wb.create_sheet(f"{short} ({len(rows)})")
        ws.sheet_properties.tabColor = ORANGE

        t = ws.cell(row=1, column=1, value=band)
        t.font = Font(name="Georgia", bold=True, size=15, color=INK)
        b = ws.cell(row=2, column=1, value=blurb)
        b.font = Font(name="Inter", size=9, color=MUTE)
        m = ws.cell(row=3, column=1,
                    value=f"{len(rows)} units · Warranty GENE · EVEglyphDesign · "
                          f"generated {stamp} · ranked by priority score, then by "
                          f"effective days remaining · dealer-confidential")
        m.font = Font(name="Inter", size=8, color=MUTE)

        for ci, (h, _) in enumerate(HEADERS, start=1):
            ws.cell(row=4, column=ci, value=h)

        for ri, r in enumerate(rows, start=5):
            vals = [ri - 4] + [r[k] for k in r.keys()][1:]
            for ci, v in enumerate(vals, start=1):
                ws.cell(row=ri, column=ci, value=v)

        style_sheet(ws, len(rows), len(HEADERS))

        for ci, (h, _) in enumerate(HEADERS, start=1):
            if "sales" in h.lower() or "profit" in h.lower():
                for ri in range(5, 5 + len(rows)):
                    ws.cell(row=ri, column=ci).number_format = '#,##0.00'
            if h in ("Miles remaining", "Last odometer"):
                for ri in range(5, 5 + len(rows)):
                    ws.cell(row=ri, column=ci).number_format = '#,##0'
            if h == "EFFECTIVE DAYS LEFT":
                for ri in range(5, 5 + len(rows)):
                    c = ws.cell(row=ri, column=ci)
                    c.font = Font(name="Inter", size=9, bold=True, color=INK)

    # ---- coverage detail ---------------------------------------------------
    ws = wb.create_sheet("Coverage detail")
    ws.sheet_properties.tabColor = LINE
    ch = ["VIN8", "Band", "Option code", "Type", "System", "Description",
          "Max months", "Max miles", "Coverage start", "Coverage end",
          "Days to expiry", "Time active", "Max odometer", "Miles remaining"]
    ws.cell(row=1, column=1, value="Coverage detail — every live coverage behind the P1–P4 rows").font = \
        Font(name="Georgia", bold=True, size=15, color=INK)
    ws.cell(row=2, column=1,
            value="One row per unit × warranty option. A unit appears once per covered system; "
                  "the band sheets collapse these to the binding axis.").font = \
        Font(name="Inter", size=9, color=MUTE)
    for ci, h in enumerate(ch, start=1):
        ws.cell(row=4, column=ci, value=h)
    det = cur.execute("""
        SELECT c.vin8, q.band, c.warranty_option_cd, c.warranty_type_cd,
               c.warranty_sub_type_cd, c.warranty_desc, c.max_months, c.max_miles,
               c.coverage_start_dt, c.coverage_end_dt, c.days_to_expiry,
               c.is_time_active, c.max_odometer, c.miles_remaining_est
        FROM v_unit_coverage_state c
        JOIN v_diagnosis_queue q ON q.vin8 = c.vin8
        WHERE c.is_time_active = 1
          AND (c.miles_remaining_est IS NULL OR c.miles_remaining_est > 0)
          AND (q.band LIKE 'P1%' OR q.band LIKE 'P2%'
               OR q.band LIKE 'P3%' OR q.band LIKE 'P4%')
        ORDER BY q.priority_score DESC, c.vin8, c.warranty_sub_type_cd
    """).fetchall()
    for ri, r in enumerate(det, start=5):
        for ci, v in enumerate(list(r), start=1):
            ws.cell(row=ri, column=ci, value=v)
    thin = Side(style="thin", color=LINE)
    for ci in range(1, len(ch) + 1):
        c = ws.cell(row=4, column=ci)
        c.font = Font(name="Inter", bold=True, size=9, color=CREAM)
        c.fill = PatternFill("solid", fgColor=INK)
        c.alignment = Alignment(vertical="center", wrap_text=True)
    for ri in range(5, 5 + len(det)):
        for ci in range(1, len(ch) + 1):
            cc = ws.cell(row=ri, column=ci)
            cc.font = Font(name="Inter", size=9, color=INK)
            cc.border = Border(bottom=thin)
    widths = [11, 22, 13, 8, 9, 34, 11, 11, 14, 14, 13, 11, 13, 15]
    for ci, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(ci)].width = w
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:{get_column_letter(len(ch))}{4 + len(det)}"

    # ---- CDK vs PACCAR reconciliation -------------------------------------
    rec = cur.execute(RECON_SQL).fetchall()
    ws = wb.create_sheet(f"CDK vs PACCAR ({len(rec)})")
    ws.sheet_properties.tabColor = ORANGE
    ws.cell(row=1, column=1,
            value="CDK service history compared with the PACCAR warranty extract").font = \
        Font(name="Georgia", bold=True, size=15, color=INK)
    tally = {}
    for r in rec:
        tally[r["match_status"]] = tally.get(r["match_status"], 0) + 1
    ws.cell(row=2, column=1,
            value="One row per unit across both sources. BOTH SIDES = registered with PACCAR and "
                  "serviced at a rooftop whose history was extracted. PACCAR ONLY = registered in "
                  "the territory, no service history here. CDK ONLY = serviced here, no PACCAR "
                  "registration in this extract set. "
                  + " · ".join(f"{k} {v}" for k, v in sorted(tally.items()))).font = \
        Font(name="Inter", size=9, color=MUTE)
    ws.cell(row=3, column=1,
            value=f"{len(rec)} units · truck business only · Warranty GENE · EVEglyphDesign · "
                  f"generated {stamp} · dealer-confidential").font = \
        Font(name="Inter", size=8, color=MUTE)
    for ci, (h, _) in enumerate(RECON_HEADERS, start=1):
        ws.cell(row=4, column=ci, value=h)
    for ri, r in enumerate(rec, start=5):
        for ci, v in enumerate([r[k] for k in r.keys()], start=1):
            ws.cell(row=ri, column=ci, value=v)
    thin = Side(style="thin", color=LINE)
    for ci in range(1, len(RECON_HEADERS) + 1):
        c = ws.cell(row=4, column=ci)
        c.font = Font(name="Inter", bold=True, size=9, color=CREAM)
        c.fill = PatternFill("solid", fgColor=INK)
        c.alignment = Alignment(vertical="center", wrap_text=True)
        c.border = Border(bottom=Side(style="medium", color=ORANGE))
    ws.row_dimensions[4].height = 34
    band_fill = PatternFill("solid", fgColor=CREAM2)
    for ri in range(5, 5 + len(rec)):
        for ci in range(1, len(RECON_HEADERS) + 1):
            cc = ws.cell(row=ri, column=ci)
            cc.font = Font(name="Inter", size=9, color=INK)
            cc.border = Border(bottom=thin)
            if ri % 2 == 1:
                cc.fill = band_fill
    for ci, (h, w) in enumerate(RECON_HEADERS, start=1):
        ws.column_dimensions[get_column_letter(ci)].width = w
        if "sales" in h.lower() or "profit" in h.lower():
            for ri in range(5, 5 + len(rec)):
                ws.cell(row=ri, column=ci).number_format = '#,##0.00'
        if h in ("Miles remaining", "Last odometer", "Highest mileage ceiling"):
            for ri in range(5, 5 + len(rec)):
                ws.cell(row=ri, column=ci).number_format = '#,##0'
    ws.freeze_panes = "C5"
    ws.auto_filter.ref = f"A4:{get_column_letter(len(RECON_HEADERS))}{4 + len(rec)}"

    # ---- method and limits ------------------------------------------------
    ws = wb.create_sheet("Method and limits")
    ws.sheet_properties.tabColor = INK
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 108
    ws.cell(row=1, column=1, value="Method and limits").font = \
        Font(name="Georgia", bold=True, size=15, color=INK)
    lines = [
        ("Scope",
         "TRUCK BUSINESS ONLY. Every row is a Peterbilt carrying PACCAR coverage — MX-11 and MX-13 "
         "engine, aftertreatment, PACCAR TX-12 transmission and clutch, harness, tow, base vehicle. "
         "TRPDT-S is TRP Dartmouth, PACCAR's all-makes truck parts and service brand, and its "
         "customers are fuel haulers and transport fleets. The BRP powersports lane — Advantage Plus "
         "and Canada General contracts, Warranty on Demand claims, the Torque Motorsports retention "
         "reports — is excluded by design and logged as SCOPE_EXCLUDED in the wireframe. No "
         "powersports unit, contract or claim appears anywhere in this workbook."),
        ("Purpose",
         "Rank units for opportunistic diagnosis before a repair order is written. This workbook is a "
         "review filter for a service writer, not a verdict. Nothing here submits, adjudicates or "
         "authorises a warranty claim — PACCAR PRWS remains authoritative on claim filing."),
        ("Population",
         "703 units whose manufacturer coverage is alive on BOTH axes — months remaining AND miles "
         "remaining. 70 units with live months but a spent mileage ceiling are excluded on purpose."),
        ("Band definitions",
         "P1 on an open RO now with 30 days or less left · P2 on an open RO now · P3 known customer "
         "with 90 days or less left · P4 known customer, coverage live. P5 and P6 (cold, 508 units) "
         "are excluded from this workbook: no phone or email exists for them, only registered owner "
         "name and city."),
        ("Priority score",
         "0-100. Perishability on the binding axis 60 points, diagnostic exposure by covered system "
         "25 points, cost of contact 15 points. System weights: ENG 4, EMC 4, A/T 3, VEH 2, ELEC 2, "
         "TOW 1, CLTH 1. Weights are policy, stated so they can be argued with."),
        ("Binding axis",
         "MONTHS = the calendar kills coverage first. MILES = the odometer kills it first. 17 units in "
         "the full queue read as safe on months and are inside 90 days on miles; eleven of those show "
         "more than six months remaining on the calendar. A months-only report ranks them low."),
        ("Measured miles/day",
         "Derived from that unit's own odometer readings across its repair orders — at least two "
         "readings, at least 60 days apart, positive mileage gain. Rates above 1,200 miles/day are "
         "flagged SUSPECT_ODOMETER and not used to date expiry. NO_RATE means the mileage axis has no "
         "clock and the effective date falls back to the months axis."),
        ("Contact data",
         "Taken from the CDK customer master via the customer on the unit's most recent repair order. "
         "Email is multi-valued in the source and is carried through raw. Group-wide fill: 10,200 of "
         "16,022 customers have at least one phone, 3,928 have an email."),
        ("Extract coverage — read this",
         "The group runs EIGHT service accounts. Closed repair-order history was extracted for only "
         "three (PBNS-S, PBDT-S, PNBDL-S). PNBM-S, PNBF-S, PQSP-S, PQC-S and TRPDT-S appear in open "
         "ROs only. Twelve of the thirteen covered units on an open RO at Moncton have no mileage "
         "clock for exactly this reason, and their priority is understated."),
        ("What is missing",
         "No repair-order line detail — no labour operation codes, SRT hours, part numbers or 3-C "
         "text — so no row carries an estimated claim value. No PRWS claim history on the Peterbilt "
         "lane. No SmartLINQ or PACCAR Solutions fault feed, so there is no event-driven trigger."),
        ("CDK vs PACCAR tab",
         "One row per unit across both sources, all units in the model, not just the queue. It shows "
         "what the manufacturer extract says about a unit beside what the dealer system says, and "
         "for every unit outside P1-P4 it names the reason in 'Why not in the queue'."),
        ("Custody",
         "Dealer-confidential. This file contains customer contact details and is not committed to any "
         "repository. The published wireframe holds schema, rules and aggregate counts only."),
        ("Source",
         "Built from the 2026-09-17 CDK Drive and PACCAR warranty-registration extracts by "
         "EVEglyphDesign. Model, DDL and lineage: "
         "https://eveglyphdesign.github.io/eve-hawkins-cdk-twin/warehouse/"),
        ("Generated", stamp),
        ("Row counts",
         " · ".join(f"{k} {v}" for k, v in counts.items()) + f" · coverage detail {len(det)}"),
    ]
    r = 3
    for k, v in lines:
        a1 = ws.cell(row=r, column=1, value=k)
        a1.font = Font(name="Inter", bold=True, size=9, color=INK)
        a1.alignment = Alignment(vertical="top", wrap_text=True)
        b1 = ws.cell(row=r, column=2, value=v)
        b1.font = Font(name="Inter", size=9, color=INK)
        b1.alignment = Alignment(vertical="top", wrap_text=True)
        ws.row_dimensions[r].height = max(14, 12 * (1 + len(v) // 105))
        r += 1
    f = ws.cell(row=r + 1, column=2,
                value="© 2026 EVEglyphDesign. All rights reserved. Controlled copy. "
                      "Key ID EgD-KEY-2026-07. Pour le bien-être du peuple.")
    f.font = Font(name="Inter", size=8, italic=True, color=MUTE)

    for w in wb.worksheets:
        w.sheet_view.showGridLines = False

    wb.save(a.out)
    print(f"{a.out}")
    for k, v in counts.items():
        print(f"  {k}: {v} rows")
    print(f"  Coverage detail: {len(det)} rows")


if __name__ == "__main__":
    main()
