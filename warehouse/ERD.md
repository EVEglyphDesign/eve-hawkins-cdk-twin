# Warranty GENE Warehouse Wireframe — ERD

Grain is declared on every fact. VIN8 is the cross-source spine; the customer number
(recovered from the CDK `NAME-FILE`) is the secondary spine.

```mermaid
erDiagram
    dim_unit ||--o{ fact_warranty_registration : "VIN8"
    dim_unit ||--o{ fact_repair_order          : "VIN8"
    dim_warranty_option ||--o{ fact_warranty_registration : "warranty_option_cd"
    dim_customer ||--o{ fact_repair_order              : "customer_key"
    dim_customer ||--o{ agg_customer_service_period    : "customer_key"
    dim_customer ||--o{ agg_customer_total_sales       : "customer_key"
    dim_rooftop  ||--o{ fact_repair_order              : "service_account"
    dim_rooftop  ||--o{ dim_service_advisor            : "service_account"
    dim_service_advisor ||--o{ fact_repair_order       : "sa_key"
    dim_date     ||--o{ fact_repair_order              : "open_dt / closed_dt"
    dim_date     ||--o{ fact_warranty_registration     : "coverage_start_dt / coverage_end_dt"

    dim_unit {
        TEXT vin8 PK "8-char VIN suffix — the join spine"
        TEXT model_desc
        DATE in_service_dt
        TEXT reg_owner_name "manufacturer side"
        TEXT reg_owner_city
        TEXT source_report "P026 P032 P046 P048 — disjoint"
        INT  is_warranty_registered
        INT  is_service_known
        DATE first_ro_dt
        DATE last_ro_dt
        NUM  max_odometer
    }
    dim_warranty_option {
        TEXT warranty_option_cd PK
        TEXT warranty_type_cd "BASE | EXT"
        TEXT warranty_sub_type_cd "VEH ENG A/T EMC ELEC TOW CLTH HVAC"
        TEXT warranty_desc
        INT  max_months "time axis"
        INT  max_miles  "distance axis"
    }
    dim_customer {
        TEXT customer_key PK "accounting_account:customer_number"
        TEXT customer_number
        TEXT name_file "CDK Pick key store*number"
        TEXT customer_name
        TEXT company_name
        DATE entry_dt
    }
    dim_rooftop {
        TEXT service_account PK "PBNS-S PBDT-S PNBDL-S"
        TEXT accounting_account "PNB-A"
        TEXT rooftop_label
    }
    fact_warranty_registration {
        TEXT warranty_reg_key PK "vin8:option — grain"
        TEXT vin8 FK
        TEXT warranty_option_cd FK
        DATE coverage_start_dt
        DATE coverage_end_dt "start + max_months"
        INT  max_miles
        TEXT source_report
    }
    fact_repair_order {
        TEXT ro_key PK "service_account:ro_number — grain"
        TEXT ro_status "OPEN | CLOSED"
        TEXT vin8 FK "null when vehicle id is not 8 or 17 chars"
        TEXT vehicle_id_raw "verbatim, pre-normalisation"
        TEXT customer_key FK
        TEXT sa_key FK
        DATE open_dt
        DATE closed_dt
        NUM  odometer
        NUM  total_sales
        NUM  total_gross_profit
        NUM  labor_sales
        NUM  parts_sales
        NUM  sold_hours
    }
    agg_customer_service_period {
        TEXT customer_key FK
        DATE period_start_dt
        DATE period_end_dt
        INT  ro_count
        NUM  warranty_sales "tie-out only"
        NUM  cp_sales
        NUM  internal_sales
    }
    dq_exception {
        INT  dq_id PK
        TEXT source_file
        TEXT rule_code "VIN8_LENGTH VIN_UNREGISTERED CUST_UNKNOWN DATE_PARSE RO_DUPLICATE SOURCE_MISSING"
        TEXT severity "BLOCK | WARN | INFO"
        TEXT observed_value
    }
```

## Mart lineage

```mermaid
flowchart LR
    A[fact_warranty_registration] --> C[v_unit_coverage_state]
    B[dim_warranty_option] --> C
    U[dim_unit] --> C
    R[fact_repair_order] --> S[v_unit_service_profile]
    C --> T[v_rich_target]
    S --> T
    U --> T
    T --> W[v_whitespace_registered_never_serviced]
    T --> E[v_coverage_expiring_180d]
    S --> N[v_serviced_unregistered]
    A --> N
```
