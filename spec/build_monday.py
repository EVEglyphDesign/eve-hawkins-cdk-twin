#!/usr/bin/env python3
"""Build the EVEglyphDesign canon PDF for EgD-HAW-CDK-PLUG-001.

Two-pass: pass 1 discovers page count, pass 2 stamps it into the footer.
"""
import hashlib, re, subprocess, sys, datetime, pathlib
import markdown
from weasyprint import HTML, CSS

BASE = pathlib.Path(__file__).parent
SRC = BASE / "CDK-MONDAY-APPROACH.md"
OUT = BASE / "EVEglyphDesign_CDK_Monday_Approach.pdf"

raw = SRC.read_text()
sha = hashlib.sha256(raw.encode()).hexdigest()
ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# strip the leading title block; we render it as a cover
body_md = raw.split("---\n", 1)[1] if raw.startswith("# ") else raw
body_md = re.sub(r"^# The CDK Monday Runbook.*?\n---\n", "", raw, flags=re.S)

html_body = markdown.markdown(
    body_md, extensions=["tables", "attr_list", "sane_lists", "md_in_html"]
)

CSS_TEXT = """
@font-face { font-family:'Fraunces'; src:url('../../fonts/Fraunces.ttf'); }
@font-face { font-family:'Inter'; src:url('../../fonts/Inter.ttf'); }
@font-face { font-family:'Inter'; font-style:italic; src:url('../../fonts/Inter-Italic.ttf'); }

:root {
  --cream:#fdfaf4; --cream2:#f7f2e7; --ink:#1a1a1a;
  --line:#e7e1d3; --mute:#6b665c; --accent:#e87722;
}

@page {
  size: A4; margin: 20mm 16mm 20mm 16mm;
  background: var(--cream);
  @bottom-left {
    content: "EVEglyphDesign · EgD-HAW-CDK-OUT-003 r2";
    font-family:'Inter'; font-size:7pt; color:#6b665c;
  }
  @bottom-right {
    content: "Page " counter(page) " of __PAGES__";
    font-family:'Inter'; font-size:7pt; color:#6b665c;
  }
}
@page :first { @bottom-left { content:""; } @bottom-right { content:""; } }

html { background: var(--cream); }
body {
  font-family:'Inter', sans-serif; font-size:8.6pt; line-height:1.5;
  color: var(--ink); background: var(--cream);
  -weasy-hyphens: none;
}

/* ---- cover ---- */
.cover { page-break-after: always; padding-top: 34mm; }
.cover .rule { height:3px; background:var(--accent); width:52mm; margin-bottom:11mm; }
.cover h1 {
  font-family:'Fraunces', serif; font-weight:600; font-size:34pt;
  line-height:1.1; margin:0 0 5mm 0; letter-spacing:-0.4pt;
}
.cover h2 {
  font-family:'Fraunces', serif; font-weight:400; font-size:14.5pt;
  color:var(--mute); margin:0 0 16mm 0; line-height:1.32; border:0; padding:0;
}
.cover dl { margin:0; font-size:8.6pt; }
.cover dt {
  font-weight:600; color:var(--accent); text-transform:uppercase;
  letter-spacing:0.9pt; font-size:6.8pt; margin-top:5mm;
}
.cover dd { margin:0.7mm 0 0 0; }
.cover .foot {
  margin-top:32mm; padding-top:4mm; border-top:1px solid var(--line);
  font-size:6.8pt; color:var(--mute); line-height:1.6;
}
.cover .mark { font-style:italic; color:var(--accent); }

/* ---- headings ---- */
h2 {
  font-family:'Fraunces', serif; font-weight:600; font-size:16pt;
  margin:9mm 0 3mm 0; padding-bottom:1.6mm;
  border-bottom:2px solid var(--accent); page-break-after:avoid;
  line-height:1.22;
}
h3 {
  font-family:'Fraunces', serif; font-weight:600; font-size:11pt;
  margin:6mm 0 2mm 0; page-break-after:avoid; line-height:1.25;
}
h2 + h3 { margin-top:4mm; }
p { margin:0 0 2.6mm 0; }
strong { font-weight:600; }
em { font-style:italic; }
a { color:var(--accent); text-decoration:none; }

ul, ol { margin:0 0 3mm 0; padding-left:5mm; }
li { margin-bottom:1.4mm; }

hr { border:0; border-top:1px solid var(--line); margin:7mm 0; }

/* ---- tables ---- */
table {
  width:100%; border-collapse:collapse; margin:3mm 0 5mm 0;
  font-size:7.1pt; line-height:1.38; table-layout:auto;
}
thead { background:var(--cream2); }
th {
  text-align:left; font-weight:600; padding:1.8mm 1.6mm;
  border-bottom:1.6px solid var(--accent); vertical-align:bottom;
  font-size:6.9pt; text-transform:uppercase; letter-spacing:0.4pt;
}
td {
  padding:1.7mm 1.6mm; border-bottom:1px solid var(--line);
  vertical-align:top; word-wrap:break-word; overflow-wrap:break-word;
}
tr { page-break-inside:avoid; }
table a { word-break:break-word; }

blockquote {
  margin:3mm 0; padding:2mm 0 2mm 4mm; border-left:2.5px solid var(--accent);
  color:var(--mute); font-style:italic;
}
"""


def build(pages_token):
    css = CSS_TEXT.replace("__PAGES__", str(pages_token))
    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"></head><body>
<section class="cover">
  <div class="rule"></div>
  <h1>The CDK<br>Monday Runbook</h1>
  <h2>Six emails, two calls, one day.<br>Fill three blanks and run it.</h2>
  <dl>
    <dt>Document</dt><dd>EgD-HAW-CDK-OUT-003 · revision 2</dd>
    <dt>Client context</dt><dd>Peterbilt Atlantic — eight locations, five provinces — eight CDK accounts on invoice 10002236</dd>
    <dt>Companion to</dt><dd>EgD-HAW-CDK-PLUG-001 — The PACCAR Feedback Standard<br>EgD-HAW-CDK-OUT-002 — The CDK Outreach, Reframed</dd>
    <dt>Prepared by</dt><dd>EVEglyph Design</dd>
    <dt>Status</dt><dd>Working runbook for Monday 10 August 2026. Send-ready copy.</dd>
  </dl>
  <div class="foot">
    Key ID EgD-KEY-2026-07 · {ts}<br>
    SHA-256 {sha}<br>
    © 2026 EVEglyphDesign. All rights reserved. Controlled copy.<br>
    <span class="mark">Pour le bien-être du peuple.</span>
  </div>
</section>
{html_body}
</body></html>"""
    h = HTML(string=doc, base_url=str(BASE))
    return h.render(stylesheets=[CSS(string=css)])


d1 = build("N")
n = len(d1.pages)
d2 = build(n)
d2.write_pdf(str(OUT))
print(f"pages={len(d2.pages)}  sha={sha}  out={OUT}")
