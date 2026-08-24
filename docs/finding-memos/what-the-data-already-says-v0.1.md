# What the Data Already Says — v0.1, 24 Aug 2026

**Author:** Peterbilt Atlantic finding-memo lane (Prepared for Tobias).
**Status:** Draft v0.1, not approved. Recorded here so the Lightspeed lane in
[`adapters/lightspeed-3pa/`](../../adapters/lightspeed-3pa/README.md) has a stable
reference for the "why".

The PDF itself lives in the working set at `Peterbilt-Atlantic-What-the-Data-Already-Says-v0.1.pdf`
and should be committed to `docs/finding-memos/pdf/` as part of the next handoff. This
file records the numbers we cite from it so downstream code and adapters have a plain-text
source to point at without opening the PDF.

## Corpus, counted

- **2,278,720** emails, all counted; **10,320** (0.26%) read as text.
- **24,560** scored calls; **14.5%** transcripts read.
- **131,038** customer records; product surface filters that down to **6,984** (only
  companies, ≥5 pieces of mail, 25 automated senders removed, enough history to trend).
- Recording archive: **25,141 of 25,154** Peterbilt recordings held and playable; audio
  starts **7 May 2026**; TELUS retention is **90 days rolling**.

## Findings the memo publishes

1. **Callback loss (Section 1).** Of the voicemails the report can see, **59.7%**
   (368 of 616, Peterbilt only, robocalls removed) never get a callback. Returned ones
   take median **7 days**; unreturned ones have been waiting a median **109 days**.
   Blind spot: 563 of 1,232 voicemails (45.7%) carry no call reference and fall out of
   the report entirely. Site spread runs from Kentville 35.1% to Saint Pascal 63.6%
   (1.8×, not the 7× an earlier draft claimed).
2. **Silence precedes departure (Section 2).** Departing accounts show 40% three-month-silent
   before their final contact vs. 9.6% for steady accounts. A second, independent analysis
   found the same shape by gap-length rather than by silent-month count (29% vs 8% —
   3.7× more likely).
3. **Vocabulary the system does not weight (Section 3).** "Derate" appears in 8.2% of
   urgent calls and 0% of calm ones. Emission-system vocabulary runs 46% more urgent.
   Median call length: calm **97s**, very negative **209s**. Kenworth (the sister marque)
   named **149** times in the sample.
4. **Phone-to-email cannot be joined without invoices (Section 4).** 21,453 verified
   email accounts vs. 31,402 calling parties, **1** match — and it is PACCAR (the
   manufacturer), not a customer. **This is the case for CDK — and, equally, for
   Lightspeed on the rooftops it covers.**

## Where the Lightspeed lane fits

Section 4 of the memo is the load-bearing paragraph for this adapter:

> An email record knows an address. A phone record knows a number. Nothing in either
> says they are the same company. An invoice knows both. That is why CDK is not simply
> a third source of data. It is the key the other two are missing.

Lightspeed carries the same invoice-anchored identity for the customers it serves.
For the rooftops that are on Lightspeed rather than CDK, **the Lightspeed lane closes
the join** without waiting on CDK's DealerSuite entitlement queue. For the rooftops
that are on both, Lightspeed is a corroborating source and its rows enter the customer
sphere with their own origin and confidence tags — nothing averages, nothing overwrites.

## Faults the memo names, that the Lightspeed collector must not reproduce

- **`call_insight.repeat_caller` never filled in.** Do not add columns to
  `lightspeed_raw` that the loader never populates — those become the next unused
  column.
- **Call dates cluster on the import day (87%).** Every row in `lightspeed_raw` records
  its Lightspeed-side timestamp *and* its ingestion timestamp, in separate columns,
  named unambiguously.
- **Hour-of-day stored in UTC and read as local.** Every timestamp in
  `lightspeed_raw` is UTC on the wire and carries an explicit `_utc` suffix. Atlantic
  conversion happens at the presentation layer only.

## Three things the memo says can be built now, with no new access

1. Callback-owed queue.
2. Quiet-account feed.
3. Urgency vocabulary.

None of those three depend on Lightspeed. They belong to the TELUS + mail lanes and
proceed in parallel. This adapter's job is the **money question** — Section 4 — for
the Lightspeed rooftops.
