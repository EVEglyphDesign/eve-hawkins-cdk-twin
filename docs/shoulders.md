# Shoulders to stand on

**EVEglyphDesign · CDK Twin · foundations analysis**
Last revised 2026-07-29.

The question put was direct: has CDK been open-sourced, is there something close enough to start
from, and what does the long-term route to SAP Datasphere and the PACCAR platform actually
require. Four research lanes went out. This is what came back.

---

## 1. The short answers

**CDK has never been open-sourced.** Neither has ADP Dealer Services, from which it descends, nor
Reynolds ERA. All access is certification-gated through Fortellis or the Reynolds Certified
Interface. The one project ever branded "the first Open Source Web Dealership Management System"
— [Automotis](https://github.com/SirLouen/automotis) — has one star and was last pushed on
7 November 2011.

**There is no open-source dealer management system worth forking.** Seven general-purpose open
ERPs were surveyed — [Apache OFBiz](https://ofbiz.apache.org/download.html),
[Odoo Community](https://github.com/odoo/odoo), [ERPNext](https://github.com/frappe/erpnext),
[Tryton](https://www.tryton.org/), [Dolibarr](https://github.com/Dolibarr/dolibarr),
[Metasfresh](https://github.com/metasfresh/metasfresh),
[iDempiere](https://github.com/idempiere/idempiere) and the Compiere lineage behind it. All are
license-clean and several are genuinely alive. None carries dealership transactional logic — no
deal jacket, no F&I, no VIN-decoded repair order, no dealership-grade parts catalogue.

**No open-source project anywhere addresses heavy truck.** Not one. That is the decisive finding
for this group, because heavy truck is the core of it.

So the shoulders are not code. They are three vocabularies, one architectural fact, and one
integration surface that is hiding under someone else's brand name.

---

## 2. The vocabularies worth adopting

### STAR — the transaction shapes

[STAR](https://www.starstandard.org/) is a dues-funded nonprofit that publishes Business Object
Documents: XML message definitions for repair orders, vehicle service history, parts management,
vehicle inventory and sales, credit, service appointments, and dealer financial statements — over
200 message formats across 35-plus business areas, catalogued
[publicly](https://www.starstandard.org/index.php/star-xml-bods/). STAR XML 6.2.4 shipped
[September 2024](https://www.starstandard.org/index.php/2024/09/12/leading-automotive-technical-standards-association-star-releases-star-xml-bod-updates-for-retail-delivery-vehicle-sales-pricing-and-service/),
and an
[Automotive Retail Domain Model](https://www.starstandard.org/index.php/2026/01/27/star-unveils-industry-defining-retail-automotive-domain-model-to-advance-data-interoperability-and-ai-transformation-across-the-entire-ecosystem/)
followed in January 2026 — viewable by the whole industry regardless of membership, editable only
by members.

The schemas themselves carry a real open licence. A published STAR schema states: "This schema is
made available under an Eclipse Public Licenses 1.0"
([Liquid Technologies STAR schema documentation](https://schemas.liquid-technologies.com/STAR/5.3.4/processrepairorder_xsd.html)).
That is permissive open source. Membership — $10,000 to $20,000 a year for dealers — buys voting
rights and early access, not the right to read the schema.

**Limit:** STAR's own language is car-retail. No STAR source reviewed states Class 8 scope. Treat
it as a reference shape for retail transactions, not as heavy-truck canon.

### VMRS — the language PACCAR already speaks

[VMRS](https://tmc.trucking.org/VMRS-Overview) is the ATA Technology & Maintenance Council's
maintenance coding system: equipment vocation, reason for repair, work accomplished, technician
failure, and a three-level system/assembly/component hierarchy running to more than 34,000
component codes.

It is not optional vocabulary for this group, because PACCAR is already using it. PACCAR Parts
Fleet Services' electronic catalogue uses VMRS codes for Kenworth and Peterbilt dealers, per
PACCAR's own marketing manager quoted in
[Trailer Body Builders](https://www.trailer-bodybuilders.com/equipment-parts/aftermarket-parts/article/21732413/paccar-parts-fleet-services-enhances-electronic-catalog).
PACCAR Solutions' own service portal carries dedicated
[VMRS code search fields](https://support.paccar.decisiv.net/hc/en-us/articles/360026414773-Use-the-Search-Page).
Decisiv's Platform API carries VMRS codes on line items. Peterbilt of Alaska appears on
[TMC's licensee list](https://tmc.trucking.org/blog/tmc-announces-news-licensees-latest-vmrs).

**It is not free.** Four paid annual tiers, from $350 for the smallest electronic catalogue up to
$51,000 for full distribution rights, per
[TMC's own pricing flyer](https://tmc.trucking.org/sites/default/files/VMRS_flyer_2021_web.pdf).
The Complete Developer tier is a flat $1,500 to $2,250 with no redistribution rights — which is
the shape of what a dealer-owned twin needs. Karmak had to license VMRS from TMC to embed it in
Fusion; [it did so in March 2025](https://www.truckpartsandservice.com/technology/business-operations/article/15739616/karmak-licenses-tmcs-vehicle-maintenance-standards).
There is no open substitute. This is a purchase, not a fork, and it is a cheap one.

### ACES and PIES — the only standard that covers both halves of the group

The Auto Care Association's [ACES](https://www.autocare.org/aces) (fitment) and
[PIES](https://www.autocare.org/pies) (product attributes) standards cover, in the association's
own words, light, medium and heavy duty as well as powersport, off-highway and equipment. ACES 5.0
and PIES 8.0 [released 2 April 2026](https://www.autocare.org/news/latest-news/details/2026/04/02/auto-care-association-releases-aces--5.0-and-pies--8.0).
A separate vehicle-database tier exists specifically for GVW classes 4 through 8.

This is the only vocabulary found that spans both Peterbilt Atlantic and Extreme Torque. Entry
subscription is $2,500 a year at member rates
([Auto Care subscriptions](https://www.autocare.org/data-standards/subscriptions)).

### Genuinely open, if telematics later matters

[COVESA's Vehicle Signal Specification](https://github.com/COVESA/vehicle_signal_specification) is
MPL-2.0, at v5.1 as of July 2025, and
[explicitly supports commercial vehicles](https://covesa.global/project/vehicle-signal-specification/).
[rFMS 5.0.0](https://www.fms-standard.com/Truck/down_load/Technical_Specification_rFMS_vehicle_data_V5.0.0_25.07.2025.pdf),
the European truck OEMs' RESTful successor to the FMS Standard, is free to download and
heavy-truck native. Both are signal vocabularies, not transaction models — they complement STAR
rather than replace it.

---

## 3. The Datasphere plan needs correcting

Two findings change it.

**SAP Datasphere is no longer a product you can buy.** As of 1 January 2026 it was removed from
the list of eligible cloud services for new BTPEA, CPEA and PAYG subscriptions
([SAP Community announcement](https://community.sap.com/t5/technology-blog-posts-by-sap/announcement-sap-datasphere-and-sap-analytics-cloud-availability-via-sap/ba-p/14140920)),
and SAP's own support knowledge base records it as a deprecated BTP service as of 31 December 2025
([SAP KBA 3630656](https://userapps.support.sap.com/sap/support/knowledge/en/3630656)). It has been
absorbed into **SAP Business Data Cloud**, announced February 2025 with Databricks as a first-party
service ([SAP News](https://news.sap.com/2025/02/sap-databricks-open-bold-new-era-data-ai/)). SAP's
current product page frames Datasphere as "a key component in SAP Business Data Cloud, serving as
the knowledge core" ([SAP Datasphere](https://www.sap.com/products/data-cloud/datasphere.html)).
Existing tenants keep working. New procurement goes through Business Data Cloud.

**There is no public evidence PACCAR runs Datasphere.** PACCAR is verifiably deep in SAP — S/4HANA
on IBM Power per an [IBM/Mainline case study](https://mainline.com/wp-content/uploads/PDFs/CS_PACCAR-Power.pdf),
plus Integrated Business Planning, Global Trade Services, Transportation Management, HCM and
[Concur](https://www.concur.com/resource-center/casestudy/paccar). But PACCAR's
[2024 Annual Report](https://www.paccar.com/media/1aml4ipx/2024-annual-report.pdf) does not mention
Datasphere, BTP or Business Network, and no SAP customer reference, press release or PACCAR job
posting naming them was found. This is absence of evidence rather than proof of absence — but it
means there is no confirmed PACCAR-side Datasphere endpoint to integrate into today.

**And a partner cannot write into someone else's tenant anyway.** Cross-tenant space sharing is
not supported; cross-tenant content movement goes through the Content Network transport
application with matching space and connection names
([SAP, Transporting Content Between Tenants](https://help.sap.com/docs/SAP_DATASPHERE/be5967d099974c69b77f4549425ca4c0/df12666cf98e41248ef2251c564b0166.html));
and the sanctioned route for cross-organisation exchange is the
[Data Marketplace](https://help.sap.com/docs/SAP_DATASPHERE/e4059f908d16406492956e5dbcf142dc/e479b7b4c95741c7a7a1d42397984c7e.html),
where a provider publishes licensed data products a consumer joins. If a Datasphere tenant ever
exists on the PACCAR side, the twin's role is **data-product provider or replication source**, not
co-tenant.

**Therefore Datasphere is a compatibility requirement, not a build target.** And compatibility is
cheap. Parquet is Datasphere's default replication output format, and Datasphere has native
connections for S3, Azure Blob, ADLS Gen2 and Google Cloud Storage, reading JSON, JSONL, CSV, ORC
and Parquet ([SAP, connection file formats](https://help.sap.com/docs/SAP_DATASPHERE/be5967d099974c69b77f4549425ca4c0/b645de78a8374c24871ab6169be40d35.html)).
One documented trap: Parquet on ADLS Gen2 is readable through Data Flows but
[not through Replication Flows](https://community.sap.com/t5/technology-q-a/how-to-use-azure-data-lake-gen2-parquet-files-as-source-for-sap-datasphere/qaq-p/14293169).
Iceberg and Delta are not first-class inbound connection types.

There is also no SAP dealer model to conform to. Datasphere's
[Automotive content package](https://help.sap.com/docs/SAP_DATASPHERE/cb7a0296feb849089b00d461168e3e69/3263c997716210148212b18947049c44.html)
is OEM supply-chain scope — sales, purchasing and production orders out of S/4HANA. SAP's actual
dealer product,
[Dealer Business Management](https://help.sap.com/docs/SAP_DEALER_BUSINESS_MANAGEMENT/54c1b516c0fa4eb7a893ff13dcf76e7d/1378c2e8692e41da9384b03c2e861522.html),
is an on-premise ERP add-on whose most recent documentation is version 8.1 SP01, dated February
2016.

**Net:** land the twin as Parquet on object storage the dealership owns. That is the format
Datasphere prefers, it is the format Databricks and every lakehouse reads, and it commits to
nothing. If a Datasphere or Business Data Cloud endpoint appears on the PACCAR side, the bridge is
a connection definition, not a rebuild.

---

## 4. Where the PACCAR integration surface actually is

The "PACCAR platform" is not one system. It is five, and the most useful one is not branded
PACCAR.

**PACCAR Solutions is Decisiv.** Decisiv states it plainly: "The PACCAR Solutions Service
Management (PSSM) platform is developed by Decisiv for PACCAR"
([Decisiv — PACCAR Solutions](https://paccar.decisiv.net/)). The login lives on
`paccar.decisiv.net`. And Decisiv publishes
[five documented APIs](https://api-docs.decisiv.net/) — a Platform API for service providers and
dealer systems covering line items, parts, VMRS codes, notes, attachments and estimate approval; an
SRM Connect API; a Global Assets API exposing warranties, recalls and build information; an
authentication API; and a Service Provider API. Access appears gated behind a commercial
relationship rather than self-serve signup, but this is a real, specified integration programme,
and it is materially more concrete than PACCAR's own.

**PACCAR's own API catalogue exists and is licensed.** The PACCAR API License Agreement governs
"Connected Truck APIs" at `developers.paccar.cloud`, granting a limited, revocable,
non-transferable token-based licence restricted to internal business purposes, fee-bearing under a
subscription order form, revocable at any time
([PACCAR Digital Services Terms](https://staging-paccar.anthology-digital.com/digital-services-terms/)).
Same shape as the CDK API terms. The catalogue itself would not load.

**SmartLINQ and TruckTech+ do not give the dealer raw data.** Peterbilt's own operators manual
describes the chain: the truck transmits to PACCAR's back office, which "translates the data into
user-friendly text and graphics" and generates the portal view
([SmartLINQ Operators Manual](https://www.peterbilt.com/static-assets/documents/resources/smartlinq_operators_manual.pdf)).
The dealer sees the interpretation, never the stream. Dealer visibility to a customer's trucks is
opt-in.

**MDI is already a daily dealer-to-PACCAR data flow.** The dealer's DMS generates a nightly Dealer
Inventory File of sales and inventory; PACCAR returns a Suggested Order File
([TU Eindhoven study of PACCAR Parts MDI](https://pure.tue.nl/ws/portalfiles/portal/163151681/Master_Thesis_Jessica_Verhoijsen.pdf);
[PACCAR Parts Technology](https://www.paccarparts.com/technology/)). A daily structured export out
of the dealership already exists and already runs. It just does not belong to the dealership.

**PRWS is the warranty channel and its schema is public in fragments.** PACCAR's Registration and
Warranty System requires every claim to carry campaign code, campaign type, claim category, repair
type, customer concern code, causal code, corrective action code, responsibility code, failure
location, causal part number, supplier code and SRT code — visible across NHTSA-hosted Peterbilt
and Kenworth bulletins such as
[MC-10185190](https://static.nhtsa.gov/odi/tsbs/2020/MC-10185190-0001.pdf) and
[MC-11034059](https://static.nhtsa.gov/odi/tsbs/2026/MC-11034059-0001.pdf). CDK Drive, Excede and
Karmak Fusion all publish certified PRWS integrations. On CDK Drive, PRWS and the Online Parts
Counter run through Fortellis, and CDK states OPC integration is
[required by PACCAR](https://www2.cdkglobal.com/ht-oem).

---

## 5. The last mile, evidenced

The strongest single piece of evidence in this entire sweep is a dealer notice.

Peterbilt's engine warranty does not cover damage from insufficient maintenance, and for repair
orders opened after 15 November 2024, major-component claims — camshaft, crankshaft, cylinder
block and head, connecting rods, gears — require preventative-maintenance documentation, receipts,
logbooks and repair orders, attached to a Prior Approval request **before the repair begins**, or
the claim is denied ([Ohio Peterbilt — Warranty Updates](https://ohiopeterbilt.com/pages/warranty-updates)).

PACCAR is demanding, as a condition of paying money, a record that PACCAR's own systems do not
hold. If PACCAR held it, PACCAR would not ask for it.

That is the last mile, stated by the OEM itself. And around it sits everything else the PACCAR
platform does not capture: technician labour detail, bay and stall assignment, shop scheduling,
job costing, customer-pay work with no warranty component, the dealership's own financial record
of any of it, sales pipeline and customer relationship history, parts counter transactions outside
the replenishment signal, raw telemetry, and — structurally, since PACCAR has no relationship with
BRP or Lightspeed — anything at all from the powersports side of the group.

---

## 6. What to build on

| Layer | Stand on | Why |
|---|---|---|
| Storage format | **Parquet on object storage the dealership owns** | Datasphere's own default replication format; read by every lakehouse; commits to no vendor |
| Maintenance vocabulary | **VMRS, licensed at the Developer tier** | PACCAR already speaks it, in ECAT, in PACCAR Solutions, in the Decisiv API. No open substitute exists |
| Transaction shapes | **STAR BODs as reference schemas** | Eclipse Public License 1.0, 200+ published message formats, a 2026 domain model readable without membership |
| Parts and fitment | **ACES / PIES** | The only vocabulary covering both heavy duty and powersports |
| Service events | **Decisiv Platform API** | The actual PACCAR service platform, with documented APIs carrying VMRS-coded line items |
| Extraction | **CDK dealer SFTP export** | Already analysed at [the export route](../export-route/); free, dealer-licensed, no developer agreement |
| Application code | **Nothing** | No open-source DMS exists worth forking, at any scale, in any vertical, least of all heavy truck |

The honest conclusion from four lanes of searching: there is no codebase to inherit. There are
vocabularies to license and conform to, an OEM service platform with a real API sitting under a
name nobody recognises as PACCAR's, and a warranty rule that proves the OEM needs a record the
dealership alone can produce. That is enough to stand on.

---

© 2026 EVEglyphDesign. All rights reserved. Controlled copy · Key ID `EgD-KEY-2026-07`
*Pour le bien-être du peuple.*
