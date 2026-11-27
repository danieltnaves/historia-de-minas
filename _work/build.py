#!/usr/bin/env python3
"""Assemble _work/text/p*.html into ../index-original.html (run from anywhere)."""
import re, sys
from pathlib import Path

work = Path(__file__).resolve().parent
root = work.parent
frags = sorted((work / "text").glob("p[0-9][0-9][0-9].html"))
body = "\n".join(f.read_text(encoding="utf-8") for f in frags)

# --- merge paragraphs split across page breaks --------------------------------
CONT = "</p><!--cont-->"
while True:
    i = body.find(CONT)
    if i < 0:
        break
    j = body.find('<p class="c">', i)
    if j < 0:
        sys.exit(f"cont marker without continuation near: {body[max(0,i-80):i+20]!r}")
    between = body[i + len(CONT):j]
    # the continuation must follow directly, with only comments/figures/footnotes between
    stripped = re.sub(r"<!--.*?-->|<figure.*?</figure>|<p class=\"fn\".*?</p>", "", between, flags=re.S)
    if stripped.strip():
        sys.exit(f"unexpected content between cont and continuation: {stripped.strip()[:120]!r}")
    k = body.find("</p>", j)
    inner = body[j + len('<p class="c">'):k]
    tail = "</p>"
    if body.startswith("<!--cont-->", k + 4):
        tail = CONT
        end = k + 4 + len("<!--cont-->")
    else:
        end = k + 4
    body = body[:i] + " " + inner + tail + between + body[end:]

if '<p class="c">' in body or "<!--cont-->" in body:
    sys.exit("unmerged continuation left over")

# --- table of contents -----------------------------------------------------------
titles = re.findall(r'<h2 id="(c\d\d)">(.*?)</h2>', body)
if len(titles) != 24:
    sys.exit(f"expected 24 stories, found {len(titles)}")
toc = ['<li><span class="rn"></span> <a href="#certidao">Certidão</a></li>',
       '<li><span class="rn"></span> <a href="#obras-consultadas">Obras Consultadas</a></li>',
       '<li><span class="rn"></span> <a href="#prefacio">Prefacio da 1.ª Edição</a></li>']
def roman(n):
    out=""
    for v,r in [(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]:
        while n>=v: out+=r; n-=v
    return out
toc += [f'<li><span class="rn">{roman(i)}</span> <a href="#{cid}">{t}</a></li>' for i,(cid,t) in enumerate(titles,1)]
toc += ['<li><span class="rn"></span> <a href="#indice">Indice</a></li>',
        '<li><span class="rn"></span> <a href="#obras">Obras do mesmo Auctor</a></li>']

css = """
:root{--bg:#f6f1e4;--fg:#222;--muted:#666;--rule:#c9bfa5;--accent:#7a2e1c;--paper:#fffdf6}
@media (prefers-color-scheme:dark){:root{--bg:#1c1b19;--fg:#e8e2d3;--muted:#a39d8d;--rule:#4a463c;--accent:#e0a98f;--paper:#26241f}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:19px/1.65 Georgia,"Times New Roman",serif}
main{max-width:40rem;margin:0 auto;padding:1.5rem 16px 4rem}
h1,h2{font-family:Georgia,serif;line-height:1.2}
h2{font-size:1.9rem;margin:4rem 0 1.2rem;padding-top:1.5rem;border-top:1px solid var(--rule);color:var(--accent)}
h2.front-title{font-size:1.5rem;margin-top:2.5rem}
p{margin:0 0 .9rem;text-align:justify;hyphens:auto}
a{color:var(--accent)}
.versao{text-align:right;font-size:.9rem;margin:0 0 .5rem}
.cover{text-align:center;margin:1rem 0 2rem}
.cover img{max-width:100%;height:auto;max-height:80vh;box-shadow:0 2px 14px #0005}
.titlepage{text-align:center;margin:2rem 0 3rem;padding:2rem 1rem;border:1px solid var(--rule);background:var(--paper)}
.titlepage h1{font-size:2.6rem;margin:.5rem 0}.titlepage h1 small{font-size:1.1rem;font-weight:400}
.titlepage p{text-align:center}.titlepage .author{font-size:1.5rem}
.series,.edition,.imprint{font-variant:small-caps;letter-spacing:.05em}
nav.toc{margin:2rem 0;padding:1rem 1.5rem;border:1px solid var(--rule);background:var(--paper);border-radius:6px}
nav.toc h2{margin:0 0 .5rem;padding:0;border:0;font-size:1.3rem}
nav.toc ol{columns:2;column-gap:2rem;margin:0;padding-left:0;list-style:none;font-size:.95rem}
nav.toc .rn{display:inline-block;min-width:3.2rem;text-align:right;color:var(--muted);margin-right:.4rem}
nav.toc li{break-inside:avoid;margin:.15rem 0}
figure{margin:1.5rem 0;text-align:center}
figure img{max-width:100%;height:auto;background:#fff;border:1px solid var(--rule)}
figure.vignette{width:min(42%,280px);margin:.3rem 0 .6rem;clear:both}
figure.vignette.left{float:left;margin-right:1.2rem}
figure.vignette.right{float:right;margin-left:1.2rem}
figure.vignette:not(.left):not(.right),figure.vignette.center{float:none;width:min(80%,420px);margin:1.2rem auto}
figure.portrait img{max-width:min(100%,420px)}
figcaption{font-size:.9rem;color:var(--muted);margin-top:.4rem}
p.fn{font-size:.85rem;color:var(--muted);border-top:1px solid var(--rule);padding-top:.4rem;margin:1rem 0}
p.note{font-size:.95rem;border-left:3px solid var(--rule);padding-left:.8rem;color:var(--muted)}
p.verse{margin-left:2rem;text-align:left;font-style:italic}
p.speech,p.shout{margin-left:1.5rem}
p.shout{margin-bottom:.2rem;text-align:left}
p.signature{text-align:right;font-style:italic}
p.fim{text-align:center;letter-spacing:.3em;margin:2rem 0}
.numero{text-align:right;font-size:.9rem;color:var(--muted)}
.legal{font-size:.8rem;color:var(--muted);margin-top:2rem}
ul.stages{margin:0 0 1rem 1rem}
table.idx{width:100%;border-collapse:collapse;font-size:.95rem}
table.idx td{padding:.15rem .4rem;vertical-align:top;border-bottom:1px dotted var(--rule)}
table.idx td:first-child{white-space:nowrap;text-align:right;color:var(--muted)}
table.idx td:last-child{text-align:right;white-space:nowrap}
.sc{font-variant:small-caps}
@media(max-width:520px){body{font-size:17px}nav.toc ol{columns:1}p{text-align:left}
figure.vignette,figure.vignette.left,figure.vignette.right{float:none;width:min(80%,300px);margin:1rem auto}}
"""

html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Historias da Terra Mineira — Carlos Góes (1938)</title>
<style>{css}</style>
</head>
<body>
<main>
<p class="versao"><a href="index.html">Ler na ortografia atual</a></p>
<div class="cover"><img src="images/cover.jpg" alt="Capa de Historias da Terra Mineira"></div>
<nav class="toc" id="top"><h2>Conteúdo</h2><ol>
{chr(10).join(toc)}
</ol></nav>
{body}
</main>
</body>
</html>
"""
(root / "index-original.html").write_text(html, encoding="utf-8")
print(f"wrote {root/'index-original.html'}  ({len(html)//1024} KiB, {len(frags)} fragments, {len(titles)} stories)")
