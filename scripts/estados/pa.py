"""Pará — Banco de Leis da ALEPA (bancodeleis.alepa.pa.gov.br).

Índice: listagem paginada index.php?p=N (10 por página, todos os tipos; o filtro por tipo limita a 50).
Texto: PDF de cada norma (OCR quando escaneado).
"""
import html as htmllib
import json
import datetime as dt
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, decodificar, documento_para_md, executar, gravar  # noqa: E402
from datas import TIPO_EPIGRAFE, data_do_texto

UF = "PA"
BASE = "https://bancodeleis.alepa.pa.gov.br"
TIPOS = {
    "Emendas Constitucionais Estaduais": ("emendas-constitucionais", "Emenda Constitucional", "ec"),
    "Lei Complementar": ("leis-complementares", "Lei Complementar", "lc"),
    "Lei Ordinária": ("leis-ordinarias", "Lei Ordinária", "lei"),
    # a listagem do Banco de Leis traz também estes dois, que ficavam de fora
    "Decreto Estadual": ("decretos", "Decreto", "dec"),
    "Decreto Legislativo": ("decretos-legislativos", "Decreto Legislativo", "dlg"),
}
rede = Rede(rps=3)
LINHA = re.compile(
    r'class="td-num">Nº ([^<]*)<small>(\d*)</small>.*?class="badge[^"]*">([^<]+)<.*?'
    r'class="td-ementa-txt"[^>]*>(.*?)</div>.*?href="(arquivos/[^"]+\.pdf)"',
    re.S,
)


def indice(refazer=False):
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice")
    arq = os.path.join(pasta, "banco.json")
    if os.path.exists(arq) and not refazer:
        return json.load(open(arq, encoding="utf-8"))
    st, dados, _ = rede.get(f"{BASE}/index.php?p=1")
    ultima = max(int(p) for p in re.findall(r"[?&]p=(\d+)", decodificar(dados)))
    itens = {}
    for p in range(1, ultima + 1):
        for _ in range(4):
            st, dados, _ = rede.get(f"{BASE}/index.php?p={p}")
            if st == 200:
                break
        for numero, ano, tipo, ementa, pdf in LINHA.findall(decodificar(dados)):
            if tipo.strip() in TIPOS:
                itens[pdf] = {"numero": numero.strip(), "ano": ano, "tipo": tipo.strip(), "pdf": pdf,
                              "ementa": " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", ementa)).split())}
        if p % 200 == 0:
            print(f"[{UF}] índice página {p}/{ultima}: {len(itens)} leis", flush=True)
    lista = list(itens.values())
    os.makedirs(pasta, exist_ok=True)
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False)
    return lista


# epígrafe do PDF: "LEI N° 9.016, DE 30 DE JANEIRO DE 2020". A data tem de vir ancorada no número
# da própria norma: qualquer lei citada no corpo do texto traz data no mesmo formato.
def data_da_epigrafe(corpo, numero):
    """(AAAA-MM-DD, AAAA) a partir da epígrafe da norma `numero`, ou (None, None)."""
    if not numero:
        return None, None
    linhas = [ln.strip() for ln in corpo.splitlines() if ln.strip() and not ln.strip().startswith(("#", ">"))][:6]
    for linha in linhas:
        linha = re.sub(r"[*\\]", "", linha).strip()
        if not TIPO_EPIGRAFE.match(linha):
            continue
        data = data_do_texto(linha, numero=re.sub(r"[.\s]", "", str(numero)), linhas=1)
        if data and dt.date.fromisoformat(data) <= dt.date.today():
            return data, data[:4]
    return None, None


def processar(it):
    pasta, nome, prefixo = TIPOS[it["tipo"]]
    ano = it["ano"] or "sem-ano"
    arq_id = re.sub(r"\W+", "-", os.path.splitext(os.path.basename(it["pdf"]))[0])[-40:]
    slug = f"{prefixo}-{it['numero'] or 'sn'}-{ano}-{arq_id}"
    # alguns PDFs da ALEPA trazem o ano truncado na própria URL (lei9016_202_85959.pdf). Nesse caso
    # o ano sai da epígrafe do texto, o que só se sabe depois de baixar — daí não haver "pulado".
    truncado = not re.fullmatch(r"\d{4}", ano)
    if not truncado:
        md, fonte = caminhos(UF, pasta, ano, slug)
        if os.path.exists(md):
            return "pulado", None
    url = f"{BASE}/{it['pdf']}"
    st, doc, ctype = rede.get(url, timeout=300)
    if st != 200 or not doc:
        return "sem_texto", {"pdf": it["pdf"], "http": st}
    corpo, motivo = documento_para_md(doc, url, ctype)
    if corpo is None:
        return "sem_texto", {"pdf": it["pdf"], "norma": f"{nome} {it['numero']}/{ano}", "motivo": motivo}
    data, achado = data_da_epigrafe(corpo, it["numero"])
    data = data or ""
    if truncado:
        ano = achado or ano
        md, fonte = caminhos(UF, pasta, ano, slug)
    titulo = f"{nome} nº {it['numero']}, de {ano}"
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", it["numero"]),
        ("data", data),
        ("ano", ano),
        ("ementa", it["ementa"]),
        ("versao_texto", "PDF do Banco de Leis da ALEPA"),
        ("fonte", url),
    ]
    gravar(md, fonte, doc, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice(refazer="--refazer" in sys.argv)
    print(f"[{UF}] {len(itens)} leis no índice", flush=True)
    limite = [a for a in sys.argv[1:] if a.isdigit()]
    if limite:
        itens = itens[: int(limite[0])]
    executar(UF, itens, processar, workers=3)
