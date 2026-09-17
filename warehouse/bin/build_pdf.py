#!/usr/bin/env python3
"""Build the EVEglyphDesign canon PDF for the Warranty GENE warehouse wireframe.
Two-pass: pass 1 discovers the page count, pass 2 stamps it into the footer."""
import hashlib, datetime, pathlib, re, markdown
from weasyprint import HTML, CSS

BASE = pathlib.Path("/home/user/workspace/twin/warehouse")
FONTS = pathlib.Path("/home/user/workspace/fonts")
OUT = pathlib.Path("/home/user/workspace/twin/docs/warehouse/EVEglyphDesign_Warranty_GENE_Warehouse_Wireframe.pdf")
DOC_ID = "EgD-HAW-CDK-WH-001 r1"

parts = []
for name in ["README.md", "DATA-QUALITY.md"]:
    t = (BASE / name).read_text()
    t = re.sub(r"^© 2026 EVEglyphDesign.*$", "", t, flags=re.M | re.S)
    parts.append(t)
raw = "\n\n---\n\n".join(parts)
sha = hashlib.sha256(raw.encode()).hexdigest()
ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# drop the H1 (rendered as cover) and the mermaid-only ERD reference lines
body_md = re.sub(r"^# Warranty GENE Warehouse Wireframe — v0\.1\n", "", raw)
body_md = body_md.replace(
    "**Lane:** Hawkins Twin Platform / CDK Twin · **Extract set:** 2026-09-17 · **Status:** wireframe, proven against real extracts",
    "<p class=\"meta-line\"><b>Lane</b> Hawkins Twin Platform / CDK Twin &nbsp;·&nbsp; <b>Extract set</b> 2026-09-17 &nbsp;·&nbsp; <b>Status</b> wireframe, proven against real extracts</p>")
body_md = body_md.replace("# Data Quality — 2026-09-17 extract set", "# Data Quality — 2026-09-17 extract set {: .pagebreak }")
html_body = markdown.markdown(body_md, extensions=["tables", "attr_list", "sane_lists", "md_in_html", "fenced_code"])
# strip local repo links that cannot be clicked from a PDF, keep the text
html_body = re.sub(r'<a href="(?!https?:)([^"]*)">([^<]*)</a>',
                   lambda m: '<span class="mono">%s</span>' % (m.group(1) if "/" in m.group(1) or m.group(1).endswith(".md") else m.group(2)),
                   html_body)

CSS_TEXT = """
@font-face { font-family:'Fraunces'; src:url('FONTDIR/Fraunces.ttf'); }
@font-face { font-family:'Inter'; src:url('FONTDIR/Inter.ttf'); }
@font-face { font-family:'Inter'; font-style:italic; src:url('FONTDIR/Inter-Italic.ttf'); }
:root{--cream:#fdfaf4;--cream2:#f7f2e7;--ink:#1a1a1a;--line:#e7e1d3;--mute:#6b665c;--accent:#e87722}
@page{size:A4;margin:19mm 16mm 18mm 16mm;background:#fdfaf4;
  @bottom-left{content:"EVEglyphDesign · DOCID";font-family:'Inter';font-size:7pt;color:#6b665c}
  @bottom-right{content:"Page " counter(page) " of __PAGES__";font-family:'Inter';font-size:7pt;color:#6b665c}}
@page :first{@bottom-left{content:""}@bottom-right{content:""}}
html{background:#fdfaf4}
body{font-family:'Inter',sans-serif;font-size:8.7pt;line-height:1.52;color:#1a1a1a;background:#fdfaf4}
.pb{page-break-after:always;height:0}
.cover{page-break-after:always;padding-top:32mm}
.cover .rule{height:3px;background:#e87722;width:52mm;margin-bottom:11mm}
.cover h1{font-family:'Fraunces',serif;font-weight:600;font-size:33pt;line-height:1.08;margin:0 0 6mm 0;letter-spacing:-.4pt}
.cover h2{font-family:'Fraunces',serif;font-weight:400;font-size:14pt;color:#6b665c;margin:0 0 15mm 0;line-height:1.32;border:0;padding:0}
.cover dl{margin:0;font-size:8.6pt}
.cover dt{font-weight:600;color:#e87722;text-transform:uppercase;letter-spacing:.09em;font-size:6.8pt;margin-top:4.5mm}
.cover dd{margin:.7mm 0 0 0}
.cover .wm{margin-top:26mm;font-family:'Fraunces',serif;font-size:9pt;color:#c9c0ad;letter-spacing:.22em;text-transform:uppercase}
h1{font-family:'Fraunces',serif;font-weight:600;font-size:17pt;margin:0 0 3mm;padding-bottom:2mm;border-bottom:1.4px solid #e87722}
h2{font-family:'Fraunces',serif;font-weight:600;font-size:13.5pt;margin:8mm 0 2.5mm;padding-bottom:1.5mm;border-bottom:1px solid #e7e1d3;page-break-after:avoid}
h3{font-family:'Fraunces',serif;font-weight:600;font-size:10.5pt;margin:6mm 0 2mm;page-break-after:avoid}
p{margin:0 0 2.6mm}
strong{font-weight:600}
ul,ol{margin:0 0 3mm;padding-left:5.2mm}
li{margin-bottom:1.4mm}
code,.mono{font-family:'DejaVu Sans Mono',monospace;font-size:7.9pt;background:#f7f2e7;padding:.3mm 1mm;border-radius:1.4mm}
pre{background:#f7f2e7;border-left:2.4px solid #e87722;padding:3mm 3.5mm;margin:0 0 3.5mm;font-size:6.6pt;line-height:1.5;white-space:pre;overflow:hidden}
h1.pagebreak{page-break-before:always}
pre code{background:none;padding:0}
table{width:100%;border-collapse:collapse;font-size:7.9pt;margin:0 0 4mm;page-break-inside:avoid}
th{text-align:left;font-size:6.6pt;letter-spacing:.09em;text-transform:uppercase;color:#6b665c;font-weight:600;border-bottom:1px solid #e7e1d3;padding:0 2.5mm 1.6mm 0}
td{border-bottom:1px solid #e7e1d3;padding:1.6mm 2.5mm 1.6mm 0;vertical-align:top}
a{color:#e87722;text-decoration:none;border-bottom:.5px solid rgba(232,119,34,.4)}
.meta-line{color:#6b665c;font-size:8pt}
hr{border:0;border-top:1px solid #e7e1d3;margin:6mm 0}
.closing{margin-top:8mm;padding-top:3.5mm;border-top:1px solid #e7e1d3;font-size:7.2pt;color:#6b665c;line-height:1.6}
.closing .mark{font-family:'Fraunces',serif;font-style:italic;font-size:8.4pt;color:#1a1a1a;display:block;margin-top:1.8mm}
""".replace("FONTDIR", FONTS.as_uri()).replace("DOCID", DOC_ID)

COVER = f"""<div class="cover">
<div class="rule"></div>
<h1>Warranty GENE<br>Warehouse Wireframe</h1>
<h2>A grain-declared structured database over the CDK Drive<br>and PACCAR warranty extract set — v0.1</h2>
<dl>
<dt>Programme</dt><dd>Hawkins Twin Platform · CDK Twin · Peterbilt Atlantic</dd>
<dt>Document</dt><dd>{DOC_ID}</dd>
<dt>Extract set</dt><dd>2026-09-17 — 11 source files, 2,991 units, 7,794 repair orders</dd>
<dt>Join spine</dt><dd>VIN8 — manufacturer registration to dealer repair order</dd>
<dt>Repository</dt><dd>EVEglyphDesign/eve-hawkins-cdk-twin · warehouse/</dd>
<dt>Public surface</dt><dd>eveglyphdesign.github.io/eve-hawkins-cdk-twin/warehouse/</dd>
<dt>Custody</dt><dd>Schema and rules published · dealer payload never committed</dd>
</dl>
<div class="wm">EVEglyphDesign · Controlled Copy</div>
</div>"""

CLOSING = f"""<div class="closing">
© 2026 EVEglyphDesign. All rights reserved. Controlled copy — {DOC_ID}.<br>
Key ID EgD-KEY-2026-07 · {ts}<br>
SHA-256 {sha}
<span class="mark">Pour le bien-être du peuple.</span>
</div>"""

def build(pages_token):
    doc = f"<!doctype html><html lang='en'><head><meta charset='utf-8'></head><body>{COVER}{html_body}{CLOSING}</body></html>"
    css = CSS(string=CSS_TEXT.replace("__PAGES__", pages_token))
    return HTML(string=doc, base_url=str(BASE)).render(stylesheets=[css])

n = len(build("?").pages)
build(str(n)).write_pdf(str(OUT))
print(f"{OUT} — {n} pages, sha256 {sha[:16]}…")
