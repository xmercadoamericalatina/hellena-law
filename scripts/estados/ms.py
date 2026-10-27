"""Mato Grosso do Sul — Legislação da Governadoria (Lotus Notes, aacpdappls.net.ms.gov.br/.../govato.nsf).

Índice: views do Lotus via ?ReadViewEntries&ExpandView (XML), uma por tipo de norma.
Texto: documento ?OpenDocument (HTML em tabelas de diagramação).
"""
import json
import os
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, decodificar, executar, gravar, html_para_md  # noqa: E402

UF = "MS"
B = "https://aacpdappls.net.ms.gov.br/appls/legislacao/secoge/govato.nsf"
VIEWS = {
    "Web\\Constituição Estadual": ("constituicao", "Constituição Estadual", "ce"),
    "Emenda": ("emendas-constitucionais", "Emenda Constitucional", "ec"),
    "Lei Complementar": ("leis-complementares", "Lei Complementar", "lc"),
    "Lei Estadual": ("leis-ordinarias", "Lei Ordinária", "lei"),
    "Decreto-Lei": ("decretos-lei", "Decreto-Lei", "dl"),
    # a base do Lotus tem uma view "Decreto" com os decretos do governador, que ficava de fora
    "Decreto": ("decretos", "Decreto", "dec"),
}
NAVEGACAO = {"Sair", "Editar", "Excluir", "Novo Anexo", "Sair | Editar | Excluir | Novo Anexo"}
MESES = {m: i for i, m in enumerate(
    "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split(), 1)}
rede = Rede(rps=3)


def indice(refazer=False):
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice")
    arq = os.path.join(pasta, "views.json")
    if os.path.exists(arq) and not refazer:
        return json.load(open(arq, encoding="utf-8"))
    itens = []
    for view in VIEWS:
        # Start aceita a posição hierárquica ("12.40"); recomeça da última vista e descarta repetidas
        inicio, vistas = "1", set()
        while True:
            url = f"{B}/{urllib.parse.quote(view)}?ReadViewEntries&ExpandView&Start={inicio}&Count=500"
            st, dados, _ = rede.get(url, "text/xml", timeout=300)
            if st != 200:
                raise RuntimeError(f"view {view}: HTTP {st}")
            entradas = ET.fromstring(dados).findall("viewentry")
            novas = [e for e in entradas if e.get("position") not in vistas]
            for e in novas:
                vistas.add(e.get("position"))
                if not e.get("unid"):
                    continue  # linha de categoria (ano)
                campos = {d.get("name"): "".join(d.itertext()).strip() for d in e.findall("entrydata")}
                itens.append({"view": view, "unid": e.get("unid"), "titulo": campos.get("wnumero", ""), "ementa": campos.get("wementa", "")})
            if not novas or len(entradas) < 500:
                break
            inicio = entradas[-1].get("position")
        print(f"[{UF}] índice {view}: {sum(1 for i in itens if i['view'] == view)}", flush=True)
    os.makedirs(pasta, exist_ok=True)
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(itens, f, ensure_ascii=False)
    return itens


def processar(it):
    pasta, nome, prefixo = VIEWS[it["view"]]
    titulo = " ".join(it["titulo"].split()).rstrip(".") or nome
    m = re.search(r"n[º°o]\.?\s*([\d.]+)(?:,\s*de\s*(\d{1,2})[º°]?\s+de\s+(\w+)\s+de\s+(\d{4}))?", titulo, re.I)
    numero = m.group(1).replace(".", "") if m else ""
    ano = m.group(4) if m and m.group(4) else (re.search(r"(1[89]\d\d|20\d\d)", titulo).group(1) if re.search(r"(1[89]\d\d|20\d\d)", titulo) else "sem-ano")
    slug = f"{prefixo}-{numero or 'sn'}-{ano}-{it['unid'][:12].lower()}"
    md, fonte = caminhos(UF, pasta, ano, slug)
    if os.path.exists(md):
        return "pulado", None
    url = f"{B}/0/{it['unid']}?OpenDocument"
    st, bruto, ctype = rede.get(url, timeout=300)
    if st != 200:
        return "sem_texto", {"unid": it["unid"], "http": st}
    corpo = html_para_md(decodificar(bruto, ctype), NAVEGACAO)
    if len(re.sub(r"\W", "", corpo)) < 40:
        return "sem_texto", {"unid": it["unid"], "motivo": "texto vazio"}
    data = ""
    if m and m.group(4) and m.group(3).lower() in MESES:
        data = f"{m.group(4)}-{MESES[m.group(3).lower()]:02d}-{int(m.group(2)):02d}"
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", m.group(1) if m else ""),
        ("data", data),
        ("ementa", " ".join(it["ementa"].split())),
        ("versao_texto", "texto da base de legislação da Governadoria (pode conter alterações incorporadas)"),
        ("fonte", url),
    ]
    gravar(md, fonte, bruto, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice(refazer="--refazer" in sys.argv)
    print(f"[{UF}] {len(itens)} normas no índice", flush=True)
    limite = [a for a in sys.argv[1:] if a.isdigit()]
    if limite:
        itens = itens[: int(limite[0])]
    executar(UF, itens, processar, workers=3)
