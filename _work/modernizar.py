#!/usr/bin/env python3
"""Gera ../index-moderno.html (ortografia atual) a partir de ../index.html.
Só altera o texto e os atributos alt; marcação, ids e comentários ficam intactos."""
import re
from pathlib import Path

work = Path(__file__).resolve().parent
root = work.parent
MAPA = dict(l.split("\t") for l in (work / "modernizar-mapa.tsv").read_text(encoding="utf-8").splitlines())

# trechos mantidos na grafia original: assinaturas, títulos bibliográficos, latim
PROTEGIDOS = [
    r"J\. Carvalhaes\..*?A\. Joviano\.", r"Vicente Racciopi", r"Carlos (?:Fernandes )?Góes",
    r"DIOGO DE VASCONCELLOS — Historia Antiga das Minas Geraes", r"JOSÉ PEDRO XAVIER DA VEIGA — Ephemérides Mineiras",
    r"JOAQUIM FELICIO DOS SANTOS — Memorias do Districto Diamantinense", r"IDEM — Acayaca",
    r"OLIVEIRA LIMA — Formation historique de la nationalité brésilienne", r"J\. NORBERTO — Brasileiras Celebres",
    r"ARCHIVO PUBLICO MINEIRO — Revista", r"Diogo de Vasconcellos, Historia Antiga das Minas Geraes",
    r"Revista do Archivo Publico Mineiro", r"Brasileiras Celebres", r"Libertas quae sera tamen", r"Cáput, capitis",
    r"Corpus Christi",
]

def caixa(orig, novo):
    if len(orig) > 1 and orig.isupper():
        return novo.upper()
    if orig[0].isupper():
        return novo[0].upper() + novo[1:]
    return novo

def troca(padrao, novo, t, flags=re.I):
    return re.sub(padrao, lambda m: caixa(m.group(0), m.expand(novo)), t, flags=flags)

def modernizar(t):
    guardados = []
    def guardar(m):
        guardados.append(m.group(0)); return f"\x00{len(guardados)-1}\x00"
    for p in PROTEGIDOS:
        t = re.sub(p, guardar, t, flags=re.S)

    # apóstrofos
    t = t.replace("D'EL-REY", "DEL-REI").replace("D'El-Rey", "del-Rei").replace("d'El-Rey", "del-Rei")
    t = re.sub(r"\bMãe d['’]Agua\b", "Mãe-d'Água", t)
    t = re.sub(r"\bmãe d['’]Agua\b", "mãe-d'Água", t)
    t = troca(r"\bd['’]agua\b", "d'água", t)
    t = troca(r"\bn['’]agua\b", "na água", t)
    t = troca(r"\bd['’]ahi\b", "daí", t)
    t = troca(r"\bd['’]aquell(e|a|es|as)\b", r"daquel\1", t)
    t = troca(r"\bd['’]ell(e|a|es|as)\b", r"del\1", t)
    t = troca(r"\bd['’](esse|essa|esses|essas|este|esta|estes|estas|isso|isto|antes|onde|um|uma|entre|aqui)\b", r"d\1", t)
    t = t.replace("Dê-m'as", "Dê-mas").replace("Dê-m’as", "Dê-mas")
    t = re.sub(r"\bA['’]s\b", "Às", t)
    t = re.sub(r"\bA['’](?=\s)", "À", t)
    t = re.sub(r"\bE['’](?=\s)", "É", t)

    # compostos e ênclises
    t = troca(r"\bpr[óo]to-martyr\b", "protomártir", t)
    t = t.replace("extra-matrimonial", "extramatrimonial")
    t = troca(r"\bfolk[- ]lore\b", "folclore", t)
    t = troca(r"\bzig-zags\b", "ziguezagues", t)
    t = re.sub(r"-(me|se)-ha\b", r"-\1-á", t)
    t = re.sub(r"-(me|se)-hia\b", r"-\1-ia", t)
    t = re.sub(r"\bfêl-os\b", "fê-los", t)
    def enclise(m):
        radical, v, pron = m.groups()
        if v == "i":
            v = "í" if radical[-1].lower() in "aeou" else "i"
        else:
            v = {"a": "á", "e": "ê"}[v]
        return f"{radical}{v}-l{pron}"
    t = re.sub(r"\b([^\W\d_]+)([aei])l-(os|as|o|a)\b", enclise, t)

    # "si": conjunção vira "se"; o pronome reflexivo permanece
    def si(m):
        antes = m.string[:m.start()]
        if re.search(r"\b(por|a|em|de|para|entre|sobre)\s+$", antes, re.I):
            return m.group(0)
        return caixa(m.group(0), "se")
    t = re.sub(r"\b[Ss]i\b", si, t)

    # crase
    t = re.sub(r"(?<![^\W\d_])(?<!-)([Áá])(s?)(?![^\W\d_])",
               lambda m: ("À" if m.group(1) == "Á" else "à") + m.group(2), t)

    def palavra(m):
        w = m.group(0)
        if w.lower() == "bahia" and w != "bahia":  # o estado mantém o "h"; a baía, não
            return w
        novo = MAPA.get(w.lower())
        return caixa(w, novo) if novo else w
    t = re.sub(r"[^\W\d_]+", palavra, t)

    # meses em minúscula (preserva "Rio de Janeiro")
    t = re.sub(r"(?<!Rio de )\b(Janeiro|Fevereiro|Março|Abril|Maio|Junho|Julho|Agosto|Setembro|Outubro|Novembro|Dezembro)\b",
               lambda m: m.group(1).lower(), t)

    return re.sub(r"\x00(\d+)\x00", lambda m: guardados[int(m.group(1))], t)

fonte = (root / "index.html").read_text(encoding="utf-8")
partes = re.split(r"(<style>.*?</style>|<!--.*?-->|<[^>]+>)", fonte, flags=re.S)
secao, em_strong = "", False
for i, p in enumerate(partes):
    if i % 2:  # marcação
        m = re.match(r'<section[^>]*id="([^"]+)"', p)
        if m: secao = m.group(1)
        if p == "</section>": secao = ""
        if p == "<strong>": em_strong = True
        if p == "</strong>": em_strong = False
        partes[i] = re.sub(r'alt="([^"]*)"', lambda m: f'alt="{modernizar(m.group(1))}"', p)
    elif not (secao == "obras" and em_strong):  # títulos da lista do autor ficam como impressos
        partes[i] = modernizar(p)
html = "".join(partes).replace("Carlos Góes (1938)</title>", "Carlos Góes (1938, ortografia atualizada)</title>")
# correções pontuais: hifenização, nomes e erros impressos no livro
for linha in (work / "correcoes.tsv").read_text(encoding="utf-8").splitlines():
    if not linha or linha.startswith("#"):
        continue
    antes, depois, vezes = linha.split("\t")
    if html.count(antes) != int(vezes):
        raise SystemExit(f"correção {antes!r}: esperadas {vezes} ocorrências, achadas {html.count(antes)}")
    html = html.replace(antes, depois)
(root / "index-moderno.html").write_text(html, encoding="utf-8")
print("gerado", root / "index-moderno.html")
