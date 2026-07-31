# CDK → SAP field map — enterprise architect reference

Generated 2026-07-31T05:02:05Z by [`schema/bin/gen_mapping.py`](../bin/gen_mapping.py) from [`docs/model/fields.json`](../../docs/model/fields.json), contract `EgD-CDK-FIELDS-v2`. Regenerate, do not hand-edit.

This is the artefact for the operator's enterprise architects: one row per CDK field, its legacy DMS name, its data type, the column it lands in on load, the SAP field it maps to in the operator's native vocabulary, and the confidence behind that mapping.

**Total fields mapped: 443 across 21 entities.**

## Confidence mix (per field, never per object)

| Confidence | Meaning | Count |
|---|---|---|
| DOCUMENTED | A field-level CDK/Fortellis source states this field exists with this shape | 320 |
| INFERRED | The object is documented but this field's type/length is reasoned from ERP/dealer-accounting convention | 86 |
| UNVERIFIED | Expected but not yet confirmed — to be validated on the CDK admin login | 37 |

## Reading `cdk_to_sap_field_map.csv`

| Column | Meaning |
|---|---|
| `entity_id` | Fixed CDK Twin entity id (one of the 21 canonical entities) |
| `entity_name` | Dealer-facing entity name |
| `cdk_path` | Literal CDK/Fortellis field path, e.g. `customer.customerId` |
| `legacy_name` | The DMS legacy/EDI-era field name where documented |
| `datatype` | Contract datatype (string, integer, decimal, date, datetime, boolean, enum) |
| `unit` | currency \| hours \| quantity \| percent \| blank |
| `load_column` | The snake_case column this field lands in — what the DDL and the extract both key off |
| `target_table` | The load-ready table name (`schema/ddl/postgres/<entity_id>.sql`) |
| `sap_analogue_entity` | The SAP object/table set this whole entity maps to |
| `sap_field` | The specific SAP field analogue, where one exists |
| `confidence` | DOCUMENTED \| INFERRED \| UNVERIFIED, per field |
| `source_url` | The source document this field's shape was taken from |

See [`cdk_to_sap_field_map.csv`](./cdk_to_sap_field_map.csv) for the full row set, and [`../ddl/postgres/000_all.sql`](../ddl/postgres/000_all.sql) for the DDL these columns land in.

For the object-level (not field-level) CDK-to-SAP mapping narrative, see [`../README.md`](../README.md).
