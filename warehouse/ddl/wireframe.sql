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
CREATE TABLE dim_rooftop (
  service_account     TEXT PRIMARY KEY,   -- PBNS-S | PBDT-S | PNBDL-S
  accounting_account  TEXT NOT NULL,      -- PNB-A (single accounting account observed)
  rooftop_label       TEXT,
  province            TEXT
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

-- Whitespace: warranty-registered in the territory, never seen in the bays.
CREATE VIEW v_whitespace_registered_never_serviced AS
SELECT * FROM v_rich_target WHERE reach_class = 'REGISTERED_NEVER_SERVICED';

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
