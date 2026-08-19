# Review — Customer Sphere v0.1 control set

**To** Tobias Polly, EVEglyphDesign
**From** Dany Thériault (via the CDK/ATD dashboard workstream)
**Date** 2026-08-19
**Reviewed** Blueprint v0.1 · Technical Specification v0.1 · Wireframe v0.1 (all dated 2026-08-18)
**Companion output landing beside this file** [`EXTERNAL-REFERENCES.md`](EXTERNAL-REFERENCES.md) · [`EXTRACTION-STAGING.md`](EXTRACTION-STAGING.md) · Luke-facing wireframe (external surface, see §7)

---

## Overall — what to keep as-is

The three documents already do the two things a control set has to do:

1. **They mark state honestly**, per document ("Built / In progress / Designed" in the Blueprint and Tech Spec; the Wireframe explicitly refuses to draw money it does not yet hold). This is the load-bearing convention. It is what makes the whole set defensible to a reader who has not been in the room, and it is the one thing that must not be softened in v0.2.
2. **They already answer the question the operator actually asks** (what did this customer earn me, what did we do to earn it) rather than the question the source systems answer (how many rows). Do not lose the inversion in §1.1 of the Blueprint under any pressure to add source-system-style tabs.

Everything below is either an addition, a wording tightening, or a reconciliation with the CDK/ATD/PACCAR extraction plan that lands in `dashboard/` this same session.

---

## 1. Blueprint v0.1 — review

### Keep

- **§0 one-page framing.** The three-word decomposition (Sovereign / Customer / Sphere) reads and prints well. The "not a report — a record, with the evidence still attached" line is the single best summary sentence in the whole set; consider promoting it to the cover of the PDF.
- **§1.2 three-source table** with per-source state (Built / In progress / Pending) is exactly the right shape for a control document — no rewrite of the concept in prose, one line per source, current numbers.
- **§1.3 anchor-in-CDK / direction-of-reasoning-runs-backward** is correct and worth defending against pressure to make the dashboard "runnable without CDK." A demonstration that reads emails and calls but never posts a dollar figure it did not receive is stronger than one that estimates.
- **§2.1 small ask** framing — five fields (customer, invoice date, department, sale amount, cost amount). Keep it exactly there. The CDK export addendum is granted faster against a small ask than an integration.

### Comment — §1.2, "104 of 343 mailboxes walked"

The number is right on 2026-08-18 but ages fast. Propose replacing the inline figure with a `MAILBOX-WALK.md` reference in the same folder, so a v0.1.n bump does not require reissuing the Blueprint. Same for the 286,972 call count in the same table.

### Comment — §2.1 "over their whole life with the dealership, not over a reporting period"

Good instinct and worth defending, but the ATD peer-comparison view (see [`EXTRACTION-STAGING.md`](EXTRACTION-STAGING.md)) is inherently period-scoped (fiscal year, trailing 12 months). Suggest the Blueprint carry one line acknowledging that the sphere holds **lifetime** but the leakage monitor / ATD-COV panels project the same underlying facts to a **rolling 12-month window** for peer comparison. Otherwise the Wireframe's Screen Three appears to contradict Blueprint §2.1.

### Comment — §2.2 truck-vs-service split

Read cleanly, but the sentence "the largest protected service market is Paccar vehicles" is cut off at the page break in the file I have — worth confirming the intended completion (…and a Kenworth in a Peterbilt shop *carries the same margin profile*, or *is fair game*, or *is a bonus*). Small; but it's the sentence that closes the argument.

### Add — reference into the extraction staging

Blueprint §2 currently ends at "the split that matters." Propose a §2.3 "the sixty ratios" pointing at [`EXTRACTION-STAGING.md`](EXTRACTION-STAGING.md) as the load-bearing spec of *which* numbers the sphere is trying to produce, and at [`EXTERNAL-REFERENCES.md`](EXTERNAL-REFERENCES.md) for *which* industry references it sits beside. Two paragraphs, one link each. This closes the loop between the sphere and the operator dashboard that consumes it.

---

## 2. Technical Specification v0.1 — review

### Keep

- **§1.1 one-shape / kind='invoice' extension point.** The observation that adding CDK is an INSERT into `twin.doc`, not a migration, is the sentence that makes the whole spec durable. It is also the argument for the small-ask in the Blueprint — the schema was designed to accept the small ask.
- **§1.2 identity rules** — the four rules (phone / email exact / domain grouping / free-mail exception) plus the D29 and D37 pointers. Do not simplify these; the reason they read as pedantic is that four rounds of failure produced them.
- **§1.3 provenance table** — verified true only when `source='cdk'`. This is the rule that lets the dashboard show a truck-margin figure beside an unverified customer-typed figure and never confuse them. Keep it inline, do not push it to an appendix.
- **§2.3 CDK path** — the SFTP-as-delivery-chute framing plus the 26-hour absence alarm is correct and matches the export-route document in the sibling `eve-hawkins-cdk-twin` repo. Cross-link it.

### Comment — §2.2 "By hand. There is no scheduled job yet"

Fair state today. Given the mail twin is now the pacing item for the leakage monitor and the customer-sphere completeness metric, propose the spec name the *decision* (D-#) rather than just the state: "D-40 — scheduled Graph pull cadence, blocked on tenant consent." Otherwise a reader treats "no scheduled job yet" as a to-do rather than a decision awaiting an owner.

### Comment — §2.1 "roughly a fifth of calls carry no external number"

Worth stating the corollary: those calls **cannot join** to a customer sphere and are counted in a separate `unresolved_calls` metric that the operator sees on the completeness tile. Otherwise a reader assumes the sphere silently drops them.

### Add — cross-link to the CDK dictionary

The wiki records "the CDK dictionary covers 21 objects and 443 confidence-tagged fields, with generated Postgres/Snowflake DDL and a preflight validator." The Tech Spec §2.3 currently names the CDK Data Export Tool path but not the field dictionary. Propose one sentence: "The invoice payload from the export maps to the 443-field CDK dictionary in `eve-hawkins-cdk-twin/schema/`; the dictionary is the authoritative source for CDK field names, widths, and confidence."

### Add — SAP-shape line

Nowhere in the Tech Spec does the phrase *ACDOCA* or *SAP-shape* appear, though the sibling twin uses it and the extraction staging assumes it. Recommend a single paragraph in §1.1 or §2.3: "twin.doc(kind='invoice') materialises the ACDOCA row shape from the sibling CDK twin; every posting from CDK enters the sphere as one document, and every ATD COV in the dashboard reads from those documents rather than from CDK directly." This is what makes the dashboard universal in nature (the point Dany raised in the working note): a Karmak dealership, a Procede dealership, a Lightspeed dealership would all land into the same twin.doc(kind='invoice') shape.

---

## 3. Wireframe v0.1 — review

### Keep

- **Three screens, real numbers, no invented money.** The rule "Where money belongs, the screen says what it is waiting for" is the single strongest thing about this control set. It is what a reviewer trusts on second reading.
- **Screen 1 sphere as three-axis carrier** (people-count / recency / weight / direction). The sentence "Relationship width is the axis worth defending" is a candidate for a whole talk of its own. Keep.
- **Screen 2 middle column read bottom-up** — the trailer / statements / FINAL NOTICE / silence chain is the single best demonstration in the whole document that this system finds absences no dashboard can. Do not shorten the walk-through.
- **Screen 3 empty-column-is-honest.** ATD 2025 total-dealer + best-of-class on the left, our column empty and labelled *waiting on CDK*. This is exactly the pattern the operator dashboard also enforces. See §7 below — Luke's dashboard wireframe reuses the pattern.

### Comment — Screen 3 mentions only ATD COVs

The Wireframe §3.1 speaks of "the ATD Critical Operating Variables with the industry's own 2025 figures." Excellent. But the Peterbilt Standards of Excellence scorecard (P026, P032, P040, P041, P046, P047, P048 — seven rooftops in the last drop) is the other axis Tim's dashboard is measured on, and it is not currently in the Wireframe.

Propose a Screen 3b (or an extension of Screen 3) with **the Peterbilt scorecard** laid out the same honest way: manufacturer's number on the left (already delivered per rooftop), our derivation column on the right (empty until CDK + PACCAR training portal + PACCAR MDI access are granted), and the operating threshold in the middle. The seven current-period rooftop totals are already known and can populate the header today:

| DCODE | Location | Type | Score |
|---|---|---|---|
| P026 | Fredericton | Full service | 52.8% |
| P032 | Moncton | Full service | 64.9% |
| P040 | Kentville | P&S | 60.9% |
| P041 | Peterbilt Quebec East | P&S | 48.0% |
| P046 | Dartmouth | Full service | 38.7% |
| P047 | Deer Lake | P&S | 72.2% |
| P048 | Saint-Pascal | Full service | 33.4% |

The wiki previously noted **eight** billed CMFs on invoice 10002236 and eight published rooftops. Only seven scorecards landed this drop. **Open question for Craig — which rooftop is missing and is its 2026 scorecard available?** Would suggest calling this out inside the Wireframe rather than only in the extraction plan, because the rooftop leaderboard tile is the first thing Tim will look for.

### Comment — Screen 1 sphere: what happens on a phone

The sphere is described as three-axis (longitude / latitude / size / colour). Fine on desktop. On a phone in Peter Keirstead's server room at 6 a.m., the sphere reduces to a list — recommend the Wireframe explicitly state the mobile-degraded view (a sorted list with the direction chip in the leading column) so the mobile fallback is a design decision rather than an accident.

### Comment — Screen 2 evidence box

The Wireframe §2.3 says "A quoted figure stays a quote. The evidence box shows a real subject line and says the amount behind it lives in CDK, not here." Recommend the evidence box explicitly show *the phrase Graph returned*, not a paraphrase. This is what makes the difference between an assertion and a receipt.

---

## 4. State reconciliation across the three documents

I ran the three state markers against each other; only one substantive mismatch:

- **CDK — Blueprint §1.2 says "Pending — the export is ordered and not yet granted."**
- **Tech Spec §2.3 says "State: ordered, not granted. Nothing built."**
- **Wireframe §3.1 (implied) says "waiting on CDK."**

Consistent so far. But the sibling `eve-hawkins-cdk-twin/docs/export-route.md` describes the full data-path with commands, storage accounts, PGP key handling. That's design-level detail, still consistent with *nothing built*, but a reader flipping between the two repos might read the export-route document as "built" because of its specificity. Propose one line in the Blueprint pointing at the export-route document with the marker "**Designed, awaiting CDK grant**" so the state carries across repositories, not just within.

---

## 5. Naming and canon check

- "EVEglyphDesign" — used consistently across all three files. Correct.
- Companion documents are cross-referenced by title, not URL. Recommend adding relative-path links (`Blueprint v0.1 · [Technical Specification v0.1](CUSTOMER-SPHERE-TECHNICAL-SPEC.md) · [Wireframe v0.1](CUSTOMER-SPHERE-WIREFRAME.md)`) so the set stays navigable when it lands on the public surface.
- Palette / typography — the three source documents are Word; when converted to PDF for the public surface they must inherit the cream / orange / Fraunces / Inter canon from the boot contract. Recommend a single conversion pipeline lands them into `docs/customer-sphere/*.pdf` beside the export-route PDFs.
- Closing mark — none of the three currently carries *Pour le bien-être du peuple*. Propose adding it as the closing line of each.

---

## 6. Two things Luke will ask about that the current set does not answer

Reviewing the three documents for Luke's questions (see §7), two gaps stand out:

1. **The sphere shows silence. Luke's next question is "what is my worklist this week?"** — a list, in priority order, of the customers a service writer should call today. The Wireframe stops at *screen three is the leakage monitor* and names four customers *worth a phone call this week* — but the pathway from the sphere to a phone-call worklist is implied, not drawn. Propose Screen 2b (or a Screen 4) explicitly named *The call sheet*, with the same "no invented figures" rule.
2. **The sphere is about customers. Luke is also measured on parts and technicians.** — The Peterbilt scorecard for P040 (Kentville, Luke's home rooftop when he was operating it) is 60.9%, with Parts at a group-level number and Service depending on Platinum Score, warranty submission time, and warranty approval rate. A "how am I doing on things Peterbilt scores me on" view is not currently in the Wireframe. This is what Luke's external surface (§7) leads with.

---

## 7. Luke's surface — external, public, mobile-first

Lands beside this review as `dashboard/luke-wireframe/` in the repo and publishes to
`https://eveglyphdesign.github.io/eve-hawkins-cdk-twin/dashboard/luke-wireframe/`.

Same rules as the Customer Sphere wireframe: nothing estimated, empty tiles say what they are waiting for, real numbers where they are held (the seven rooftop scores from the current Peterbilt Standards of Excellence drop, the ATD 2025 total-dealer averages and best-of-class thresholds, the eleven ATD operating guides). Cream and orange, Fraunces and Inter, mobile-first — a rail on the left on desktop, a stack on the phone.

Three panels, top to bottom:

1. **Rooftop leaderboard** — the seven Standards of Excellence scores, sorted, with the missing eighth rooftop shown as an open question rather than omitted. The panel Luke looks at first because he is measured on it.
2. **The seven-tile operator ladder** — six Key COVs (Return on Assets, Net Profit % Sales, Parts & Service Absorption, Total Dealership Absorption, P&S Receivables Past Due, Warranty Receivables % Sales) plus the total-dealer / best-of-class band, dealership column empty and labelled *waiting on CDK*. This is Luke's own dashboard once the extraction lands.
3. **Peterbilt scorecard axes** — Operating Standards / Facility / Financial for the current period, the same seven rows, so Luke can see what PACCAR sees and what the twin will independently reproduce.

A footer note names the three client-asks the dashboard depends on and points at [`EXTERNAL-REFERENCES.md`](EXTERNAL-REFERENCES.md).

---

## What I need from you next

- A call on Blueprint §2.1 (lifetime vs. rolling-12) — one paragraph either way, so the Wireframe Screen 3 is not read as contradicting the Blueprint.
- A call on the eighth rooftop — do we hold that scorecard anywhere, or is it a Craig-side item to chase?
- A call on Wireframe Screen 3b — should the Peterbilt scorecard sit inside the same Wireframe document as a new section, or as a companion Wireframe (v0.1 *Manufacturer axis*)? I have drafted it as a companion in Luke's public surface; happy either way.

Everything else in this review is either a wording nudge or an addition, both safe to defer to a v0.2 pass.

---

*Pour le bien-être du peuple.*
