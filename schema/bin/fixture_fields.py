#!/usr/bin/env python3
"""
fixture_fields.py — Lane F standalone fixture generator.

Emits a fields.json fixture that matches the EgD-CDK-FIELDS-v2 contract shape
(see /home/user/workspace/FIELD_CONTRACT.md) so gen_ddl.py / gen_mapping.py /
validate_load_ready.py can be built and tested BEFORE Lane D's real
docs/model/fields.json lands.

This fixture is intentionally thin (2-4 fields per entity, not a full field
dictionary) — it exists only to exercise every code path the generators must
handle: PK, FK (same-entity and cross-entity), every datatype, every unit,
every confidence level, and an enum field. It is NOT a substitute for Lane D's
real dictionary and must never be presented as one.

Usage:
    python3 fixture_fields.py > /tmp/fields.fixture.json
    python3 fixture_fields.py --out docs/model/fields.fixture.json
"""
import argparse
import json
import sys

GENERATED = "2026-07-29T00:00:00Z"
CONTRACT = "EgD-CDK-FIELDS-v2"

SRC = "https://fortellis-api-documents-prod.s3-us-west-2.amazonaws.com/f83a79c6-8cf9-4c1a-b45e-b266634eaf90/external/20251119155158640--ZuFlj8i.pdf"

# (entity_id, entity_name, dealer_name, group, sap_analogue, table_name, grain, api, sources)
ENTITY_META = [
    ("dealer-rooftop-partition", "Dealer / Rooftop Partition", "which of the 9 stores this record belongs to", "org",
     "Company Code (T001) / Plant (WERKS) plus a module-scoping flag", "cdk_dealer_rooftop_partition",
     "one row per rooftop/department scope pairing", "partial"),
    ("cost-centre-department", "Cost Centre / Department", "which part of the store a cost belongs to", "org",
     "Cost centre / profit centre (CSKS/CEPC)", "cdk_cost_centre_department",
     "one row per department per rooftop", "none"),
    ("customer-master", "Customer Master", "the customer record — fleet account, walk-in owner, or company", "master",
     "KNA1 / KNB1 / KNVV — customer master, general + company-code + sales views", "cdk_customer_master",
     "one row per customer per rooftop", "full"),
    ("vehicle-master", "Vehicle / Unit Master", "the truck or unit record, keyed by VIN", "master",
     "Equipment master (EQUI), serialized — VIN as equipment number", "cdk_vehicle_master",
     "one row per VIN", "partial"),
    ("employee-master", "Employee / Technician Identifiers", "the tech or advisor record", "master",
     "HR-adjacent Z-fields on transaction tables (no clean HR analogue)", "cdk_employee_master",
     "one row per employee per rooftop", "partial"),
    ("vendor-master", "Vendor / Supplier Master", "the supplier record for parts and services purchased", "master",
     "LFA1 / LFB1 — vendor master, general + company-code data", "cdk_vendor_master",
     "one row per vendor", "none"),
    ("gl-account-master", "GL Account Master", "the chart of accounts entry", "ledger",
     "SKA1 / SKB1 — chart of accounts + company-code GL segment", "cdk_gl_account_master",
     "one row per GL account per department suffix", "none"),
    ("accounting-schedule", "Accounting Schedule", "the open-item subledger behind one GL control account", "ledger",
     "Reconciliation-account subledger / open-item list", "cdk_accounting_schedule",
     "one row per schedule control-key entry", "none"),
    ("gl-journal-posting", "GL Journal / Posting", "one line of a journal entry", "ledger",
     "BKPF/BSEG — accounting document header + line items", "cdk_gl_journal_posting",
     "one row per journal line", "partial"),
    ("repair-order", "Repair Order", "the RO — the work order for a truck", "transaction",
     "Internal order (AUFK/COEP) with a payer settlement rule", "cdk_repair_order",
     "one row per repair order", "full"),
    ("ro-labour-line", "RO Labour Line", "one labour operation on an RO", "transaction",
     "Confirmation/activity allocation line (COEP)", "cdk_ro_labour_line",
     "one row per labour operation per RO", "full"),
    ("ro-part-line", "RO Part Line", "one part consumed on an RO", "transaction",
     "Goods movement / material consumption line (MSEG)", "cdk_ro_part_line",
     "one row per part line per RO", "full"),
    ("parts-master-inventory", "Parts Master / Inventory", "the part number record and its on-hand position", "master",
     "MARA/MARC/MBEW combined", "cdk_parts_master_inventory",
     "one row per part number per rooftop", "partial"),
    ("parts-order-supersession", "Parts Order + Supersession", "a parts order line and its supersession chain", "transaction",
     "Purchase order (EKKO/EKPO) + material supersession chain", "cdk_parts_order_supersession",
     "one row per ordered part line", "partial"),
    ("parts-pick-ticket", "Parts Pick Ticket", "the pick slip tied to an RO parts line", "transaction",
     "Reservation / goods issue slip (MB1A-style)", "cdk_parts_pick_ticket",
     "one row per pick ticket line", "partial"),
    ("counter-parts-sale", "Counter / Parts Sale", "a cash or wholesale parts sale at the counter", "transaction",
     "Sales order + billing document (VBAK/VBRK)", "cdk_counter_parts_sale",
     "one row per counter sale line", "partial"),
    ("deal-jacket-vehicle-sale", "Deal Jacket / Vehicle Sale", "the file for one truck sale", "transaction",
     "Sales order + billing document (VBAK/VBRK) + F&I lines", "cdk_deal_jacket_vehicle_sale",
     "one row per deal jacket", "partial"),
    ("technician-time-punch", "Technician Time Punch", "one clock in/out event against an RO labour line", "transaction",
     "Time confirmation (CATS-style) feeding activity allocation", "cdk_technician_time_punch",
     "one row per punch event", "partial"),
    ("work-in-process", "Work-in-Process", "an RO still open, carried as WIP on the balance sheet", "ledger",
     "WIP account tied to internal order settlement", "cdk_work_in_process",
     "one row per open RO per reporting date", "partial"),
    ("warranty-claim", "Warranty Claim", "a factory warranty claim filed against an RO", "transaction",
     "Debit memo / claims-management document vs. factory receivable", "cdk_warranty_claim",
     "one row per warranty claim", "none"),
    ("purchase-receipt-document", "Purchase / Receipt Document", "a vendor invoice or receipt document", "ledger",
     "Purchase order + goods receipt (EKKO/EKBE), 3-way match", "cdk_purchase_receipt_document",
     "one row per receipt document line", "none"),
]


def base_fields(entity_id, pk_len=12):
    """Every fixture entity gets a PK field plus a couple of representative fields."""
    pk_col = {
        "customer-master": "customer_id",
        "vehicle-master": "vin",
        "employee-master": "employee_id",
        "vendor-master": "vendor_id",
        "gl-account-master": "gl_account_number",
        "accounting-schedule": "schedule_id",
        "gl-journal-posting": "journal_line_id",
        "repair-order": "repair_order_number",
        "ro-labour-line": "ro_labour_line_id",
        "ro-part-line": "ro_part_line_id",
        "parts-master-inventory": "part_number",
        "parts-order-supersession": "order_line_id",
        "parts-pick-ticket": "pick_ticket_id",
        "counter-parts-sale": "sale_line_id",
        "deal-jacket-vehicle-sale": "deal_number",
        "technician-time-punch": "punch_id",
        "work-in-process": "wip_id",
        "warranty-claim": "claim_id",
        "purchase-receipt-document": "receipt_document_id",
        "dealer-rooftop-partition": "subscription_id",
        "cost-centre-department": "department_id",
    }[entity_id]

    fields = [
        {
            "seq": 1,
            "path": f"{entity_id}.{pk_col}",
            "legacy_name": pk_col.upper(),
            "label": pk_col.replace("_", " ").title(),
            "dealer_label": f"the key you'd look this record up by",
            "datatype": "string",
            "length": pk_len,
            "precision": None,
            "scale": None,
            "nullable": False,
            "key": "PK",
            "fk_target": None,
            "enum_values": [],
            "unit": None,
            "source": f"fixture source for {entity_id}",
            "source_url": SRC,
            "sap_field": None,
            "load_column": pk_col,
            "confidence": "DOCUMENTED",
            "notes": "",
        }
    ]
    return fields, pk_col


def make_entities():
    entities = []
    for entity_id, entity_name, dealer_name, group, sap_analogue, table_name, grain, reach in ENTITY_META:
        fields, pk_col = base_fields(entity_id)

        # Add a currency field (DOCUMENTED)
        fields.append({
            "seq": 2, "path": f"{entity_id}.amount", "legacy_name": "AMT",
            "label": "Amount", "dealer_label": "the dollar amount on this line",
            "datatype": "decimal", "length": None, "precision": 13, "scale": 2,
            "nullable": True, "key": "none", "fk_target": None, "enum_values": [],
            "unit": "currency", "source": f"fixture source for {entity_id}", "source_url": SRC,
            "sap_field": "BSEG-DMBTR", "load_column": "amount", "confidence": "DOCUMENTED", "notes": "",
        })

        # Add a date field (INFERRED)
        fields.append({
            "seq": 3, "path": f"{entity_id}.createdDate", "legacy_name": "CREATE-DT",
            "label": "Created Date", "dealer_label": "when this record was first created",
            "datatype": "date", "length": None, "precision": None, "scale": None,
            "nullable": True, "key": "none", "fk_target": None, "enum_values": [],
            "unit": None, "source": f"fixture source for {entity_id}", "source_url": SRC,
            "sap_field": None, "load_column": "created_date", "confidence": "INFERRED",
            "notes": "reasoned from ERP convention, not a documented CDK field",
        })

        # Add an enum field (UNVERIFIED) — status code
        fields.append({
            "seq": 4, "path": f"{entity_id}.statusCode", "legacy_name": "STATUS-CD",
            "label": "Status Code", "dealer_label": "the status shown on the screen",
            "datatype": "enum", "length": 2, "precision": None, "scale": None,
            "nullable": True, "key": "none", "fk_target": None,
            "enum_values": [{"code": "O", "meaning": "Open"}, {"code": "C", "meaning": "Closed"}],
            "unit": None, "source": f"fixture source for {entity_id}", "source_url": SRC,
            "sap_field": None, "load_column": "status_code", "confidence": "UNVERIFIED",
            "notes": "expected, to be confirmed on tenant login",
        })

        entities.append({
            "entity_id": entity_id,
            "entity_name": entity_name,
            "dealer_name": dealer_name,
            "group": group,
            "sap_analogue": sap_analogue,
            "table_name": table_name,
            "grain": grain,
            "api": {"reachable": reach, "endpoints": [], "note": "fixture"},
            "sources": [{"label": "fixture", "url": SRC}],
            "field_count": len(fields),
            "fields": fields,
        })

    # Add one deliberate cross-entity FK to test fk_target resolution:
    # ro-labour-line.repair_order_number -> repair-order.repair_order_number
    for e in entities:
        if e["entity_id"] == "ro-labour-line":
            e["fields"].append({
                "seq": 5, "path": "ro-labour-line.repairOrderNumber", "legacy_name": "RO-NO",
                "label": "Repair Order Number", "dealer_label": "which RO this labour line belongs to",
                "datatype": "string", "length": 12, "precision": None, "scale": None,
                "nullable": False, "key": "FK", "fk_target": "repair-order.repair_order_number",
                "enum_values": [], "unit": None, "source": "fixture", "source_url": SRC,
                "sap_field": "AUFK-AUFNR", "load_column": "repair_order_number",
                "confidence": "DOCUMENTED", "notes": "",
            })
            e["field_count"] = len(e["fields"])

    return entities


def main():
    ap = argparse.ArgumentParser(description="Emit an EgD-CDK-FIELDS-v2 fixture for Lane F generator development.")
    ap.add_argument("--out", default=None, help="Output path; default stdout")
    args = ap.parse_args()

    doc = {"generated": GENERATED, "contract": CONTRACT, "entities": make_entities()}
    text = json.dumps(doc, indent=2) + "\n"
    if args.out:
        with open(args.out, "w") as f:
            f.write(text)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
