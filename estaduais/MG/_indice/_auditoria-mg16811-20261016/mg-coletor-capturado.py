"""Minas Gerais — ALMG (dadosabertos.almg.gov.br).

Índice: CSV anual da "Legislação mineira" (desde 1947), com links para texto original e atualizado.
Texto: API v2 da ALMG; XML com o HTML da norma em <conteudo>.
"""
import csv
import datetime as dt
import gzip
import os
import re
import sys
import threading
import urllib.parse
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, executar, gravar, html_para_md  # noqa: E402

UF = "MG"
CSV_URL = "https://dadosabertos.almg.gov.br/arquivo/legislacao-mineira/download?ano={}"
TIPOS = {
    "CON": ("constituicao", "Constituição Estadual"),
    "EMC": ("emendas-constitucionais", "Emenda Constitucional"),
    "LCO": ("leis-constitucionais", "Lei Constitucional"),
    "LCP": ("leis-complementares", "Lei Complementar"),
    "LEI": ("leis-ordinarias", "Lei Ordinária"),
    "LDL": ("leis-delegadas", "Lei Delegada"),
    "LEA": ("leis-adicionais", "Lei Adicional"),
    "DEL": ("decretos-lei", "Decreto-Lei"),
    "DEC": ("decretos", "Decreto"),
    "RAL": ("resolucoes", "Resolução"),
    "PRT": ("portarias", "Portaria"),
    "DNE": ("decretos", "Decreto"),
    "DSN": ("decretos-nao-numerados", "Decreto (não numerado)"),
    "DLB": ("deliberacoes", "Deliberação"),
}
rede = Rede(rps=4)
bloqueado = threading.Event()


class TextoNorma(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.nivel = 0
        self.partes = []

    def handle_starttag(self, tag, attrs):
        if self.nivel or (tag == "span" and "textNorma" in dict(attrs).get("class", "").split()):
            if tag == "span":
                self.nivel += 1
            self.partes.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.nivel:
            self.partes.append(f"</{tag}>")
            if tag == "span":
                self.nivel -= 1

    def handle_data(self, texto):
        if self.nivel:
            self.partes.append(texto)

    def handle_entityref(self, nome):
        self.handle_data(f"&{nome};")

    def handle_charref(self, nome):
        self.handle_data(f"&#{nome};")


def indice():
    itens = []
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice")
    os.makedirs(pasta, exist_ok=True)
    for ano in range(1947, dt.date.today().year + 1):
        arq = os.path.join(pasta, f"{ano}.csv")
        if not os.path.exists(arq):
            st, dados, _ = rede.get(CSV_URL.format(ano))
            if st != 200 or not dados.strip():
                continue
            with open(arq, "wb") as f:
                f.write(dados)
        with open(arq, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["Tipo"] in TIPOS:
                    itens.append(r)
    return list({(r["Tipo"], r["Numero"], r["Ano"], r["Complemento"]): r for r in itens}.values())


def processar(r):
    pasta, nome = TIPOS[r["Tipo"]]
    if pasta == "constituicao" and int(r["Ano"]) < 1988:
        pasta = "constituicoes-historicas"
    comp = f"-{r['Complemento']}" if r["Complemento"] else ""
    slug = f"{r['Tipo'].lower()}-{r['Numero']}{comp}-{r['Ano']}"
    md, fonte = caminhos(UF, pasta, r["Ano"], slug)
    if os.path.exists(md):
        return "pulado", None
    if bloqueado.is_set():
        return "fonte_bloqueada", None
    url = r["LinkTextoAtualizado"] or r["LinkTextoOriginal"]
    if not url:
        return "sem_texto", {"norma": slug, "motivo": "sem link"}
    cache = os.path.join(RAIZ_ESTADUAIS, UF, "_indice", "documentos", slug + ".xml.gz")
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    if os.path.exists(cache):
        with gzip.open(cache, "rb") as f:
            dados = f.read()
        st = 200
    else:
        st, dados, _ = rede.get(url, "application/xml")
        if st in (401, 403, 429):
            bloqueado.set()
            return "sem_texto", {"norma": slug, "url": url, "http": st}
        if st == 200 and dados:
            with gzip.open(cache, "wb") as f:
                f.write(dados)
    try:
        conteudo = ET.fromstring(dados).findtext(".//conteudo") or "" if st == 200 and dados else ""
    except ET.ParseError:
        conteudo = ""
    # A página HTML oficial também serve o original; nunca trocar uma compilação por original.
    if not conteudo.strip() and not r["LinkTextoAtualizado"]:
        url_html = f"https://www.almg.gov.br/legislacao-mineira/texto/{r['Tipo']}/{r['Numero']}/{r['Ano']}/"
        if r["Complemento"]:
            url_html += "?comp=" + urllib.parse.quote(r["Complemento"])
        sh, pagina, _ = rede.get(url_html)
        if sh in (401, 403, 429):
            bloqueado.set()
        if sh == 200:
            with gzip.open(cache.replace(".xml.gz", ".pagina.html.gz"), "wb") as f:
                f.write(pagina)
            parser = TextoNorma()
            parser.feed(pagina.decode("utf-8", errors="replace"))
            conteudo = "".join(parser.partes)
            url = url_html
    if not conteudo.strip():
        return "sem_texto", {"norma": slug, "url": url, "motivo": "conteúdo vazio"}
    corpo = html_para_md(conteudo)
    if len(re.sub(r"\W", "", corpo)) < 20:
        return "sem_texto", {"norma": slug, "url": url, "motivo": "conteúdo sem texto normativo após conversão"}
    d, m, a = r["DataLegislacao"].split("/") if r["DataLegislacao"] else ("", "", "")
    try:
        data = dt.date(int(a), int(m), int(d))
        data = data.isoformat() if data <= dt.date.today() else ""
    except ValueError:
        data = ""
    numero = r["Numero"] + (f"-{r['Complemento']}" if r["Complemento"] else "")
    titulo = f"{nome} nº {numero}, de {r['DataLegislacao']}" if r["Tipo"] != "CON" else f"Constituição do Estado de Minas Gerais ({r['Ano']})"
    situacao = (r.get("Situacao") or "").strip()
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", numero),
        ("data", data),
        ("ementa", " ".join((r["Ementa"] or "").split())),
        ("situacao", situacao.capitalize()),
        ("revogada", {"revogada": True, "revogado": True, "vigente": False, "em vigor": False}.get(situacao.strip().lower())),
        ("versao_texto", "atualizada" if r["LinkTextoAtualizado"] else "original"),
        ("fonte", url.replace("conteudo=true&", "")),
    ]
    if r["DataLegislacao"] and not data:
        meta.append(("data_na_fonte", r["DataLegislacao"]))
    gravar(md, fonte, conteudo, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice()
    itens.sort(key=lambda r: (r["Ano"], r["DataLegislacao"][3:5], r["DataLegislacao"][:2]), reverse=True)
    if len(sys.argv) > 1:
        itens = itens[: int(sys.argv[1])]
    executar(UF, itens, processar)
