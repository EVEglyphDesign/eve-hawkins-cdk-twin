# CDK second spin — shared rules for every lane

The first spin was judged, correctly, as too thin on the actual source data model. It leaned on
vendor marketing pages and inference. This spin is a **primary-source retrieval exercise**, not a
writing exercise. You are being paid for artefacts you pull down, not for prose you compose.

## The one rule

**Bring back raw material, verbatim, with the URL it came from.** Field names exactly as the
source spells them, including case. Table names, file names, record layouts, screen names, menu
paths, account numbers. If you find a downloadable spec, PDF, schema, or exhibit — download it
into `/home/user/workspace/cdk2_raw/` and say where it is. Quote, do not paraphrase.

## Prohibited

- Inventing a field, table, endpoint, screen, or file name. Never. Not once.
- Presenting an inference as a finding. Inferences go in a clearly separated section.
- Padding a thin result to look productive. **"I searched X, Y, Z and this does not appear to be
  public" is a valuable, acceptable, wanted answer.** Say it plainly and name what you tried.
- Reusing claims from the first spin without re-verifying them against a primary source.

## Confidence tags — put one on every single claim

- `[DOC]` — the vendor, a regulator, a court exhibit, or an OEM published it. URL required.
- `[COMM]` — a practitioner, integrator, forum post, training video, or job posting states it.
  URL required. Name the speaker and their standing if you can.
- `[INF]` — you reasoned it. Say from what.
- `[UNK]` — you looked and could not find it. Say where you looked.

## Output

Write one file, path given in your brief. Structure:

1. **What I actually retrieved** — a list of files downloaded and specs opened, with URLs.
2. **The field/table/record dictionary** — the substance. Tables, one row per field:
   name as spelled | type if stated | meaning as stated by the source | tag | URL.
3. **Verbatim quotes worth keeping** — blockquotes with attribution.
4. **What I searched and could not find** — explicit, itemised, with the queries used.
5. **Corrections to the first spin** — anything the first spin got wrong or overstated.
   The first-spin files are `/home/user/workspace/cdk_0*.md`. Skim only what your lane touches.

## Context

Peterbilt Atlantic: nine rooftops in Atlantic Canada, heavy truck, PACCAR/Peterbilt franchise,
runs CDK Drive plus Lightspeed. We are building a digital twin that reconstructs the dealership
ledger and operations outside CDK. The reader is a parts and service director, and a systems
architect who spent thirty years in enterprise integration and will spot a bluff instantly.
