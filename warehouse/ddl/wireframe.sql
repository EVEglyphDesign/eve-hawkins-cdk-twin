-- ============================================================================
-- EVEglyphDesign — Hawkins Twin Platform / CDK Twin
-- Warranty GENE warehouse wireframe — v0.1
-- Grain-declared star schema over the 2026-09-17 CDK Drive + PACCAR extract set.
-- Portable ANSI-ish DDL: runs on SQLite as-is; Postgres notes inline.
-- NO DEALER ROWS ARE COMMITTED. This file is schema and rules only.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. DIMENSIONS
-- ----------------------------------------------------------------------------

-- Rooftop / accounting partition. CDK exports carry both a Service Account
-- (rooftop-scoped) and an Accounting Account (group-scoped).
--
-- SCOPE WARNING. The group operates EIGHT service accounts, all under the single
-- accounting account PNB-A. Only the Open ROs extract spans all eight; the
-- Closed ROs extract was pulled against three of them. This table is therefore
-- seeded from the UNION of both RO extracts, never from closed history alone,
-- and every row carries in_closed_history so that any query touching service
-- history can see whether that rooftop's past is actually present.
--
-- rooftop_label is left NULL where the plain-language rooftop name has not been
-- confirmed by the dealership. Codes are not decoded by guesswork.
CREATE TABLE dim_rooftop (
  service_account     TEXT PRIMARY KEY,   -- e.g. PBNS-S, PNBM-S, PQC-S, TRPDT-S
  accounting_account  TEXT NOT NULL,      -- PNB-A (single accounting account observed)
  rooftop_label       TEXT,               -- NULL until confirmed by the dealership
  province            TEXT,               -- NULL until confirmed by the dealership
  label_status        TEXT,               -- CONFIRMED | UNVERIFIED
  in_closed_history   INTEGER NOT NULL,   -- 1 = closed-RO extract covers this rooftop
  closed_ro_count     INTEGER DEFAULT 0,
  open_ro_count       INTEGER DEFAULT 0
);

-- Customer. Business key is the CDK customer number, unique within the
-- accounting account. NAME-FILE in the customer master encodes the same number
-- as '<store_prefix>*<customer_number>' — proven on 818 of 821 RO customers.
CREATE TABLE dim_customer (
  customer_key        TEXT PRIMARY KEY,   -- accounting_account || ':' || customer_number
  customer_number     TEXT NOT NULL,
  accounting_account  TEXT NOT NULL,
  name_file           TEXT,               -- CDK Pick NAME-FILE, e.g. 4*TO007
  customer_name       TEXT,
  company_name        TEXT,
  address             TEXT,
  email_raw           TEXT,               -- multi-valued in source; parsed downstream
  work_phone          TEXT,
  cell_phone          TEXT,
  home_phone          TEXT,
  entry_dt            DATE,
  ytd_purchases       NUMERIC(14,2),
  source_system       TEXT NOT NULL       -- CDK_CUSTOMER_MASTER | CDK_RO
);

-- Unit. Grain: one row per VIN8. VIN8 is the confirmed cross-source join key:
-- CDK 'Vehicle ID' on the RO carries the 8-character VIN suffix, and every
-- PACCAR warranty-registration row is keyed on VIN8.
CREATE TABLE dim_unit (
  vin8                  TEXT PRIMARY KEY,
  vin17                 TEXT,             -- when a full VIN is recoverable
  model_desc            TEXT,             -- Peterbilt model: 389, 589, 567, 579, 548 ...
  in_service_dt         DATE,
  reg_owner_name        TEXT,             -- PACCAR warranty-registration owner
  reg_owner_city        TEXT,
  source_report         TEXT,             -- P026 | P032 | P046 | P048 (disjoint partitions)
  is_warranty_registered INTEGER NOT NULL DEFAULT 0,
  is_service_known       INTEGER NOT NULL DEFAULT 0,
  first_ro_dt           DATE,
  last_ro_dt            DATE,
  max_odometer          NUMERIC(12,0)
);

-- Warranty option catalogue. Grain: one row per PACCAR warranty option code.
CREATE TABLE dim_warranty_option (
  warranty_option_cd    TEXT PRIMARY KEY, -- 9400090, 9481830, ...
  warranty_type_cd      TEXT NOT NULL,    -- BASE | EXT
  warranty_sub_type_cd  TEXT NOT NULL,    -- VEH | ENG | A/T | EMC | ELEC | TOW | CLTH | HVAC
  warranty_desc         TEXT,
  max_months            INTEGER,
  max_miles             INTEGER
);

CREATE TABLE dim_service_advisor (
  sa_key                TEXT PRIMARY KEY, -- service_account || ':' || sa_id
  sa_id                 TEXT,
  sa_name               TEXT,
  service_account       TEXT REFERENCES dim_rooftop(service_account)
);

CREATE TABLE dim_date (
  date_key    DATE PRIMARY KEY,
  year        INTEGER, quarter INTEGER, month INTEGER,
  month_name  TEXT,    day_of_month INTEGER, day_of_week INTEGER,
  fiscal_year INTEGER
);

-- ----------------------------------------------------------------------------
-- 2. FACTS
-- ----------------------------------------------------------------------------

-- Manufacturer truth. Grain: one row per VIN8 x warranty option.
-- Sourced from the PACCAR warranty-registration extracts (P026/P032/P046/P048).
CREATE TABLE fact_warranty_registration (
  warranty_reg_key    TEXT PRIMARY KEY,   -- vin8 || ':' || warranty_option_cd
  vin8                TEXT NOT NULL REFERENCES dim_unit(vin8),
  warranty_option_cd  TEXT NOT NULL REFERENCES dim_warranty_option(warranty_option_cd),
  in_service_dt       DATE,
  coverage_start_dt   DATE,               -- = in_service_dt
  coverage_end_dt     DATE,               -- in_service_dt + max_months
  max_miles           INTEGER,
  source_report       TEXT NOT NULL,
  loaded_at           TIMESTAMP
);

-- Dealer truth. Grain: one row per repair order (open and closed unioned,
-- discriminated by ro_status). Business key ro_number is unique within rooftop.
CREATE TABLE fact_repair_order (
  ro_key              TEXT PRIMARY KEY,   -- service_account || ':' || ro_number
  ro_number           TEXT NOT NULL,
  ro_status           TEXT NOT NULL,      -- OPEN | CLOSED
  service_account     TEXT REFERENCES dim_rooftop(service_account),
  accounting_account  TEXT,
  vin8                TEXT,               -- FK to dim_unit when 8 chars; else DQ-quarantined
  vehicle_id_raw      TEXT NOT NULL,      -- as exported, before VIN8 normalisation
  customer_key        TEXT REFERENCES dim_customer(customer_key),
  sa_key              TEXT REFERENCES dim_service_advisor(sa_key),
  open_dt             DATE,
  closed_dt           DATE,
  odometer            NUMERIC(12,0),
  total_sales         NUMERIC(14,2), total_gross_profit  NUMERIC(14,2),
  labor_sales         NUMERIC(14,2), labor_gross_profit  NUMERIC(14,2),
  parts_sales         NUMERIC(14,2), parts_gross_profit  NUMERIC(14,2),
  misc_sales          NUMERIC(14,2), misc_gross_profit   NUMERIC(14,2),
  sublet_sales        NUMERIC(14,2), sublet_gross_profit NUMERIC(14,2),
  actual_hours        NUMERIC(10,2), sold_hours          NUMERIC(10,2),
  tech_effective_labor_rate NUMERIC(10,2),
  ro_effective_labor_rate   NUMERIC(10,2),
  efficiency_pct      NUMERIC(8,2),
  parts_to_labor_pct  NUMERIC(8,2),
  loaded_at           TIMESTAMP
);
CREATE INDEX ix_ro_vin8     ON fact_repair_order(vin8);
CREATE INDEX ix_ro_customer ON fact_repair_order(customer_key);
CREATE INDEX ix_ro_closed   ON fact_repair_order(closed_dt);

-- Third-party / OEM service contracts. Grain: one row per contract.
-- BRP / Torque Motorsports lane; VIN17-keyed, VIN8 derived for cross-lane joins.
CREATE TABLE fact_service_contract (
  contract_key      TEXT PRIMARY KEY,
  contract_source   TEXT NOT NULL,        -- BRP_ADVANTAGE_PLUS | CANADA_GENERAL
  contract_number   TEXT,
  vin17             TEXT,
  vin8              TEXT,                 -- right(vin17,8)
  customer_name     TEXT,
  dealer            TEXT,
  sales_rep         TEXT,
  vehicle_desc      TEXT,
  model_year        INTEGER,
  component_code    TEXT,
  product_codes     TEXT,
  term_desc         TEXT,                 -- '60m/0km'
  term_months       INTEGER,
  start_dt          DATE,
  delivery_dt       DATE,
  status            TEXT,
  payment_status    TEXT,
  loaded_at         TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 3. RECONCILIATION AGGREGATES (tie-out only — never a scoring input)
-- ----------------------------------------------------------------------------

-- Grain: one row per customer per extract period, service lane.
CREATE TABLE agg_customer_service_period (
  customer_key      TEXT NOT NULL,
  period_start_dt   DATE NOT NULL,
  period_end_dt     DATE NOT NULL,
  accounting_account TEXT,
  ro_count          INTEGER,
  total_sales       NUMERIC(14,2), total_gross_profit    NUMERIC(14,2),
  cp_sales          NUMERIC(14,2), cp_gross_profit       NUMERIC(14,2),
  internal_sales    NUMERIC(14,2), internal_gross_profit NUMERIC(14,2),
  warranty_sales    NUMERIC(14,2), warranty_gross_profit NUMERIC(14,2),
  PRIMARY KEY (customer_key, period_start_dt, period_end_dt)
);

-- Grain: one row per customer per extract period, all lanes (top-N ranked).
CREATE TABLE agg_customer_total_sales (
  customer_key      TEXT NOT NULL,
  period_start_dt   DATE NOT NULL,
  period_end_dt     DATE NOT NULL,
  rank_basis        TEXT,
  total_sales       NUMERIC(14,2), total_gross_profit NUMERIC(14,2),
  service_sales     NUMERIC(14,2), service_gross_profit NUMERIC(14,2),
  parts_sales       NUMERIC(14,2), parts_gross_profit   NUMERIC(14,2),
  new_vehicle_sales NUMERIC(14,2), used_vehicle_sales   NUMERIC(14,2),
  doc_refer_count   INTEGER,
  PRIMARY KEY (customer_key, period_start_dt, period_end_dt)
);

-- ----------------------------------------------------------------------------
-- 4. DATA-QUALITY QUARANTINE — nothing is silently dropped
-- ----------------------------------------------------------------------------
CREATE TABLE dq_exception (
  dq_id           INTEGER PRIMARY KEY,
  source_file     TEXT NOT NULL,
  source_rowid    TEXT,
  rule_code       TEXT NOT NULL,   -- VIN8_LENGTH | VIN_UNREGISTERED | CUST_UNKNOWN | DATE_PARSE
  severity        TEXT NOT NULL,   -- BLOCK | WARN | INFO
  detail          TEXT,
  observed_value  TEXT,
  detected_at     TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 5. GENE MARTS — the only shapes the worklist, dashboard and alerts may read
-- ----------------------------------------------------------------------------

-- Coverage state per VIN8 x option, evaluated against a run date.
CREATE VIEW v_unit_coverage_state AS
SELECT r.vin8, r.warranty_option_cd, o.warranty_type_cd, o.warranty_sub_type_cd,
       o.warranty_desc, o.max_months, r.max_miles,
       r.coverage_start_dt, r.coverage_end_dt,
       CAST(julianday(r.coverage_end_dt) - julianday('now') AS INTEGER) AS days_to_expiry,
       CASE WHEN date(r.coverage_end_dt) >= date('now') THEN 1 ELSE 0 END AS is_time_active,
       u.max_odometer,
       CASE WHEN r.max_miles IS NULL OR u.max_odometer IS NULL THEN NULL
            ELSE r.max_miles - u.max_odometer END AS miles_remaining_est
FROM fact_warranty_registration r
JOIN dim_warranty_option o ON o.warranty_option_cd = r.warranty_option_cd
JOIN dim_unit u            ON u.vin8 = r.vin8;

-- Service profile per VIN8, from dealer-side RO history.
CREATE VIEW v_unit_service_profile AS
SELECT vin8,
       COUNT(*)                                        AS ro_count,
       SUM(CASE WHEN ro_status='OPEN' THEN 1 ELSE 0 END) AS open_ro_count,
       MIN(open_dt)   AS first_ro_dt,
       MAX(COALESCE(closed_dt, open_dt)) AS last_ro_dt,
       MAX(odometer)  AS max_odometer,
       SUM(total_sales)        AS lifetime_sales,
       SUM(total_gross_profit) AS lifetime_gross_profit
FROM fact_repair_order
WHERE vin8 IS NOT NULL
GROUP BY vin8;

-- Rich target: manufacturer-visible active coverage on a unit the dealership
-- can actually reach. Pre-RO by construction — PRWS stays authoritative on claims.
CREATE VIEW v_rich_target AS
SELECT c.vin8, u.model_desc, u.in_service_dt, u.reg_owner_name, u.reg_owner_city,
       COUNT(*)                          AS active_coverage_count,
       MIN(c.days_to_expiry)             AS days_to_nearest_expiry,
       GROUP_CONCAT(DISTINCT c.warranty_sub_type_cd) AS active_sub_types,
       COALESCE(s.ro_count,0)            AS ro_count,
       COALESCE(s.open_ro_count,0)       AS open_ro_count,
       s.last_ro_dt, s.max_odometer,
       CASE WHEN COALESCE(s.open_ro_count,0) > 0 THEN 'ON_SITE_NOW'
            WHEN s.ro_count > 0                  THEN 'KNOWN_CUSTOMER'
            ELSE 'REGISTERED_NEVER_SERVICED' END AS reach_class
FROM v_unit_coverage_state c
JOIN dim_unit u          ON u.vin8 = c.vin8
LEFT JOIN v_unit_service_profile s ON s.vin8 = c.vin8
WHERE c.is_time_active = 1
GROUP BY c.vin8;

-- Whitespace: warranty-registered in the territory, with no service history in
-- the extract set.
--
-- SCOPE WARNING. 'Never serviced' means never serviced at a rooftop whose
-- history is present. Closed history covers three of eight service accounts, so
-- this view is an UPPER BOUND: a unit serviced only at PNBM-S, PNBF-S, PQSP-S,
-- PQC-S or TRPDT-S looks like whitespace here and is not. Do not campaign off
-- this view until closed ROs arrive for all eight service accounts.
CREATE VIEW v_whitespace_registered_never_serviced AS
SELECT * FROM v_rich_target WHERE reach_class = 'REGISTERED_NEVER_SERVICED';

-- Extract coverage, queryable. One row per service account with whether its
-- closed history is present.
CREATE VIEW v_rooftop_extract_coverage AS
SELECT service_account, accounting_account, rooftop_label, label_status,
       in_closed_history, closed_ro_count, open_ro_count,
       CASE WHEN in_closed_history = 1 THEN 'HISTORY_PRESENT'
            ELSE 'OPEN_ONLY — closed history not extracted' END AS coverage_state
FROM dim_rooftop;

-- Expiry pressure: active coverage closing inside 180 days.
CREATE VIEW v_coverage_expiring_180d AS
SELECT * FROM v_rich_target WHERE days_to_nearest_expiry BETWEEN 0 AND 180;

-- Units serviced here with no manufacturer warranty registration on file:
-- either out-of-territory, out of PACCAR scope, or a registration gap.
CREATE VIEW v_serviced_unregistered AS
SELECT s.vin8, s.ro_count, s.last_ro_dt, s.lifetime_sales
FROM v_unit_service_profile s
LEFT JOIN fact_warranty_registration r ON r.vin8 = s.vin8
WHERE r.vin8 IS NULL;
-- ---------------------------------------------------------------------------
-- Opportunistic-diagnosis priority. One row per unit that still has coverage
-- alive on BOTH axes. Ordering is explicit and auditable: perishability on the
-- binding axis, then diagnostic exposure, then cost of contact.
-- ---------------------------------------------------------------------------

-- Measured mileage accrual, from consecutive odometer readings on this unit's
-- own ROs. Without it the mileage axis has no clock and expiry cannot be dated.
CREATE VIEW v_unit_mileage_rate AS
WITH r AS (
  SELECT vin8, odometer, COALESCE(closed_dt, open_dt) AS dt
  FROM fact_repair_order
  WHERE vin8 IS NOT NULL AND odometer > 0 AND COALESCE(closed_dt, open_dt) IS NOT NULL
), s AS (
  SELECT vin8, COUNT(*) AS reading_count,
         MAX(odometer) - MIN(odometer) AS span_miles,
         julianday(MAX(dt)) - julianday(MIN(dt)) AS span_days
  FROM r GROUP BY vin8
)
SELECT vin8, reading_count, span_miles, span_days,
       ROUND(span_miles / span_days, 1) AS miles_per_day,
       CASE WHEN span_miles / span_days > 1200 THEN 'SUSPECT_ODOMETER'
            ELSE 'MEASURED' END AS rate_status
FROM s
WHERE reading_count >= 2 AND span_days >= 60 AND span_miles > 0;

-- Diagnostic exposure by covered system. Engine, aftertreatment and emissions
-- carry the labour and parts weight; trim and towing lines do not. Weights are
-- policy, stated here so they can be argued with rather than inferred.
CREATE VIEW v_system_weight AS
SELECT 'ENG' AS sub_type, 4 AS weight UNION ALL SELECT 'EMC', 4 UNION ALL
SELECT 'A/T', 3 UNION ALL SELECT 'VEH', 2 UNION ALL SELECT 'ELEC', 2 UNION ALL
SELECT 'TOW', 1 UNION ALL SELECT 'CLTH', 1;

CREATE VIEW v_pre_ro_priority AS
WITH live AS (
  SELECT c.vin8, c.warranty_sub_type_cd AS sub_type, c.days_to_expiry,
         c.miles_remaining_est, COALESCE(w.weight, 1) AS weight
  FROM v_unit_coverage_state c
  LEFT JOIN v_system_weight w ON w.sub_type = c.warranty_sub_type_cd
  WHERE c.is_time_active = 1
    AND (c.miles_remaining_est IS NULL OR c.miles_remaining_est > 0)
), unit AS (
  SELECT l.vin8,
         COUNT(*)                        AS live_coverages,
         SUM(l.weight)                   AS exposure_weight,
         GROUP_CONCAT(DISTINCT l.sub_type) AS live_systems,
         MIN(l.days_to_expiry)           AS days_to_time_expiry,
         MIN(l.miles_remaining_est)      AS miles_remaining
  FROM live l GROUP BY l.vin8
)
SELECT u.vin8,
       t.reach_class,
       u.live_coverages, u.live_systems, u.exposure_weight,
       u.days_to_time_expiry,
       u.miles_remaining,
       m.miles_per_day, COALESCE(m.rate_status, 'NO_RATE') AS rate_status,
       CASE WHEN m.miles_per_day IS NOT NULL AND m.rate_status = 'MEASURED'
                 AND u.miles_remaining IS NOT NULL
            THEN CAST(u.miles_remaining / m.miles_per_day AS INTEGER) END AS days_to_mileage_ceiling,
       MIN(u.days_to_time_expiry,
           COALESCE(CASE WHEN m.rate_status = 'MEASURED' AND u.miles_remaining IS NOT NULL
                         THEN CAST(u.miles_remaining / m.miles_per_day AS INTEGER) END,
                    u.days_to_time_expiry)) AS effective_days_remaining,
       CASE WHEN m.rate_status = 'MEASURED' AND u.miles_remaining IS NOT NULL
                 AND u.miles_remaining / m.miles_per_day < u.days_to_time_expiry
            THEN 'MILES' ELSE 'MONTHS' END AS binding_axis,
       t.ro_count, t.open_ro_count, t.last_ro_dt, t.max_odometer,
       -- Priority score, 0-100. Perishability 60, exposure 25, reachability 15.
       CAST(ROUND(
         60.0 * (365 - MIN(365, MAX(0, MIN(u.days_to_time_expiry,
             COALESCE(CASE WHEN m.rate_status = 'MEASURED' AND u.miles_remaining IS NOT NULL
                           THEN CAST(u.miles_remaining / m.miles_per_day AS INTEGER) END,
                      u.days_to_time_expiry))))) / 365.0
       + 25.0 * MIN(1.0, u.exposure_weight / 12.0)
       + CASE t.reach_class WHEN 'ON_SITE_NOW' THEN 15.0
                            WHEN 'KNOWN_CUSTOMER' THEN 9.0 ELSE 3.0 END
       ) AS INTEGER) AS priority_score
FROM unit u
JOIN v_rich_target t ON t.vin8 = u.vin8
LEFT JOIN v_unit_mileage_rate m ON m.vin8 = u.vin8;

-- The banded work queue. A band is an instruction to a service writer; the
-- score only orders work inside a band.
CREATE VIEW v_diagnosis_queue AS
SELECT CASE
    WHEN reach_class = 'ON_SITE_NOW' AND effective_days_remaining <= 30  THEN 'P1 IN THE BAY, CLOSING'
    WHEN reach_class = 'ON_SITE_NOW'                                     THEN 'P2 IN THE BAY'
    WHEN reach_class = 'KNOWN_CUSTOMER' AND effective_days_remaining <= 90 THEN 'P3 CALL NOW, CLOSING'
    WHEN reach_class = 'KNOWN_CUSTOMER'                                  THEN 'P4 CALL, SCHEDULE'
    WHEN effective_days_remaining <= 90                                  THEN 'P5 COLD, CLOSING'
    ELSE 'P6 COLD, CAMPAIGN'
  END AS band, *
FROM v_pre_ro_priority;
