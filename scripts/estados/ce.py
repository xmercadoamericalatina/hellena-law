"""Ceará — BELT, Banco Eletrônico de Leis Temáticas da Assembleia Legislativa (belt.al.ce.gov.br).

O acervo é organizado por tema (Joomla/K2); percorre os itens pelo ID (index.php?option=com_k2&view=item&id=N)
e classifica pelo título. Texto: bloco itemFullText da página do item.
"""
import html as htmllib
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import Rede, caminhos, decodificar, executar, gravar, html_para_md  # noqa: E402

UF = "CE"
B = "https://belt.al.ce.gov.br/index.php"
ID_MAX = 13000
TIPOS = [
    (r"^CONSTITUI", "constituicao", "Constituição Estadual", "ce"),
    (r"^EMENDA", "emendas-constitucionais", "Emenda Constitucional", "ec"),
    (r"^LEI COMPLEMENTAR", "leis-complementares", "Lei Complementar", "lc"),
    (r"^LEI DELEGADA", "leis-delegadas", "Lei Delegada", "ld"),
    (r"^DECRETO[- ]LEI", "decretos-lei", "Decreto-Lei", "dl"),
    (r"^LEI\b", "leis-ordinarias", "Lei Ordinária", "lei"),
]
MESES = {m: i for i, m in enumerate(
    "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split(), 1)}
MESES["marco"] = 3
rede = Rede(rps=3)


def bloco(html, classe, fim_classes):
    i = html.find(f'class="{classe}')
    if i < 0:
        return ""
    i = html.find(">", i) + 1
    fins = [html.find(f'class="{c}', i) for c in fim_classes]
    fins = [f for f in fins if f > 0]
    fim = min(fins) if fins else len(html)
    return html[i:html.rfind("<div", i, fim) if html.rfind("<div", i, fim) > i else fim]


def processar(id_):
    url = f"{B}?option=com_k2&view=item&id={id_}"
    st, bruto, ctype = rede.get(url, timeout=180)
    if st == 404:
        return "inexistente", None
    if st != 200:
        return "sem_texto", {"id": id_, "http": st}
    html = decodificar(bruto, ctype)
    m = re.search(r'class="itemTitle">(.*?)(?:<a class="itemPrintLink|</h2>)', html, re.S)
    titulo = " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).split()) if m else ""
    titulo = re.sub(r"\s*tamanho da fonte.*$", "", titulo)
    tipo = next(((p, n, pre) for rx, p, n, pre in TIPOS if re.match(rx, titulo.upper())), None)
    if not tipo:
        return "fora_escopo", None
    pasta, nome, prefixo = tipo
    d = re.search(r"(\d{1,2})[º°]?\s+de\s+([a-zçA-ZÇ]+)\s+de\s+(\d{4})", titulo)
    data = f"{d.group(3)}-{MESES[d.group(2).lower()]:02d}-{int(d.group(1)):02d}" if d and d.group(2).lower() in MESES else ""
    if not data:  # "DE 08.10.09"
        d2 = re.search(r"DE\s+(\d{1,2})\.(\d{1,2})\.(\d{2,4})\b", titulo, re.I)
        if d2:
            a = d2.group(3) if len(d2.group(3)) == 4 else ("19" if int(d2.group(3)) > 50 else "20") + d2.group(3)
            data = f"{a}-{int(d2.group(2)):02d}-{int(d2.group(1)):02d}"
    num = re.search(r"N[º°o.]*\s*([\d.]+)", titulo, re.I)
    ano = data[:4] or "sem-ano"
    md, fonte = caminhos(UF, pasta, ano, f"{prefixo}-{num.group(1).replace('.', '') if num else 'sn'}-{ano}-id{id_}")
    if os.path.exists(md):
        return "pulado", None
    texto_html = bloco(html, "itemFullText", ["itemExtraFields", "itemAttachments", "itemLinks", "itemBottom"])
    corpo = html_para_md(texto_html, {"O texto desta Lei não substitui o publicado no Diário Oficial", "O texto desta Lei não substitui o publicado no Diário Oficial."})
    if len(re.sub(r"\W", "", corpo)) < 40:
        return "sem_texto", {"id": id_, "titulo": titulo, "motivo": "sem texto na página"}
    extra = bloco(html, "itemExtraFields", ["itemAttachments", "itemLinks", "itemBottom"])
    ementa = " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", extra)).split())
    ementa = re.sub(r"^Informações adicionais\s*\.?:?\s*", "", ementa)
    ementa = re.split(r"\s+Lido \d+ vezes", ementa)[0]
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", num.group(1) if num else ""),
        ("data", data),
        ("ementa", ementa[:1000]),
        ("versao_texto", "texto do BELT (Assembleia Legislativa)"),
        ("fonte", url),
    ]
    gravar(md, fonte, texto_html, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    ids = list(range(ID_MAX, 0, -1))
    if len(sys.argv) > 1:
        ids = [int(x) for x in sys.argv[1].split(",")]
    executar(UF, ids, processar, workers=3)
