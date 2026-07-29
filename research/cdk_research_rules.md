# Shared rules for all six CDK research lanes

Client context: EVEglyphDesign is building a sovereign digital twin of the CDK Drive DMS
for Peterbilt Atlantic (a 9-site Peterbilt/PACCAR heavy-truck dealer group in Atlantic
Canada, owner Tim Hawkins, GM Luke Weatherbie). The twin already exists in **SAP shape** —
the parts lane uses SAP MM table names (MARA, MARC, MARD, MARM, MBEW, MVKE, MFRPN, MATDOC)
in `github.com/EVEglyphDesign/eve-dealer-parts-twin`. Your findings will be used to extend
that shape to the whole DMS.

## Non-negotiable rules

1. **Public sources only.** CDK Global product pages, Fortellis / CDK developer and API
   docs, apis.io / Postman collections, STAR and ODDX standards, dealer-forum and
   third-party integrator documentation, SEC filings, training vendors, job postings that
   name modules, university/state dealer-accounting curricula.
2. **Every factual claim carries an inline markdown link to the URL it came from.** Anchor
   text is the source name. No bare URLs. No uncited assertions.
3. **Never invent a field name, table name, endpoint or screen name.** If you cannot verify
   the real CDK name, write the concept and mark it `UNVERIFIED`.
4. **Separate what is documented from what is industry-standard inference.** Use two
   explicit labels: `DOCUMENTED` and `INFERRED (dealer-accounting norm)`.
5. End your file with a section `## What I could not verify` listing every open question,
   and a section `## Proposed SAP-shape mapping` mapping each CDK concept to the SAP table
   or object the twin should use.
6. Prefer tables over prose. Dense, factual, no marketing language.
7. Target 900–1600 words of substance. Depth over breadth. Do not pad.

## Naming

`EVEglyphDesign` exactly. Never "Eve Glyph" as one vendor word in prose except the
permitted prose form `EVEglyph Design`.
