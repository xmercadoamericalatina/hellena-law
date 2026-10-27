"""Santa Catarina — Legislação SC (ALESC, leis.alesc.sc.gov.br).

Não há índice estruturado público: percorre os IDs de /ato-normativo/legislativo/{id}, que devolvem o
documento (Word convertido, com anotações de alterações) e classifica pelo título.
"""
import html as htmllib
import datetime as dt
import gzip
import hashlib
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, decodificar, executar, gravar, html_para_md  # noqa: E402
from datas import data_do_texto as data_da_epigrafe

UF = "SC"
BASE = "https://leis.alesc.sc.gov.br"
ID_MAX = 56000
# (regex do título, pasta, nome, prefixo) — a ordem importa
# Classificação pelo título, na ordem: o específico antes do geral, porque a primeira regra que
# casar vence. Os decretos do Executivo chegam com título "DEC-000120" — é a convenção de nome do
# arquivo Word de origem, e por isso escapavam de qualquer padrão que esperasse "DECRETO".
TIPOS = [
    (r"^CONSTITUI", "constituicao", "Constituição Estadual", "ce"),
    (r"^EMENDA", "emendas-constitucionais", "Emenda Constitucional", "ec"),
    (r"^LEI COMPLEMENTAR", "leis-complementares", "Lei Complementar", "lc"),
    (r"^LEI DELEGADA", "leis-delegadas", "Lei Delegada", "ld"),
    (r"^LEI PROMULGADA", "leis-promulgadas", "Lei Promulgada", "leip"),
    (r"^DECRETO[- ]LEI", "decretos-lei", "Decreto-Lei", "dl"),
    (r"^DECRETO LEGISLATIVO", "decretos-legislativos", "Decreto Legislativo", "dlg"),
    (r"^DEC-\d", "decretos", "Decreto", "dec"),
    (r"^DECRETO\b", "decretos", "Decreto", "dec"),
    (r"^RESOLU[ÇC][ÃA]O", "resolucoes", "Resolução", "res"),
    (r"^LEI\b", "leis-ordinarias", "Lei Ordinária", "lei"),
]
MESES = {m: i for i, m in enumerate(
    "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split(), 1)}
MESES["marco"] = 3
rede = Rede(rps=3)


def classificar(titulo):
    t = titulo.upper()
    for rx, pasta, nome, prefixo in TIPOS:
        if re.match(rx, t):
            return pasta, nome, prefixo
    return None


def data_do_texto(texto, html="", titulo=""):
    m = re.search(r'<meta\s+name="Emissao"\s+content="(\d{4})/(\d{2})/(\d{2})"', html, re.I)
    if m:
        try:
            data = dt.date(*map(int, m.groups()))
            if data <= dt.date.today():
                return data.isoformat()
        except ValueError:
            pass
    primeira = next((ln.strip() for ln in texto.splitlines() if ln.strip()), "")
    data = data_da_epigrafe(primeira, linhas=1)
    if data and dt.date.fromisoformat(data) <= dt.date.today():
        return data
    data = data_da_epigrafe(titulo, linhas=1)
    if data and dt.date.fromisoformat(data) <= dt.date.today():
        return data
    return ""


def norma_revogada(html, cabeca):
    partes = re.split(r"\nFONTE\b", cabeca, maxsplit=1)
    notas = partes[0] if len(partes) > 1 else ""
    if re.search(r"(?m)^\s*(?:REVOGAD[AO] PARCIALMENTE|RESTABELECID[AO])\b", notas):
        return None
    if re.search(r'<(?:body|div)\b[^>]*(?:class|id)=["\'][^"\']*\blei-revogada\b', html, re.I):
        return True
    return True if re.search(r"(?m)^\s*(?:CONSOLIDADA E )?REVOGAD[AO] (?:PELAS?|PELOS?|INTEGRALMENTE|TOTALMENTE)\b", notas) else None


def processar(id_):
    url = f"{BASE}/ato-normativo/legislativo/{id_}"
    st, bruto, ctype = rede.get(url, timeout=180)
    if st == 404:
        return "inexistente", None
    if st != 200 or not bruto:
        return "sem_texto", {"id": id_, "http": st}
    captura = os.path.join(RAIZ_ESTADUAIS, UF, "_fonte", "respostas", str(id_), hashlib.sha256(bruto).hexdigest() + ".html.gz")
    os.makedirs(os.path.dirname(captura), exist_ok=True)
    try:
        with gzip.open(captura, "rb") as f:
            integra = hashlib.sha256(f.read()).digest() == hashlib.sha256(bruto).digest()
    except (OSError, EOFError):
        integra = False
    if not integra:
        with tempfile.NamedTemporaryFile(dir=os.path.dirname(captura), delete=False) as f:
            temporario = f.name
            f.write(gzip.compress(bruto))
        os.replace(temporario, captura)
    html = decodificar(bruto, ctype)
    # a ALESC usa <s> para o "º/°" sobrescrito, não para texto riscado
    html = re.sub(r"<s>\s*(&deg;|&ordm;|&ordf;|°|º|ª|o|a)\s*</s>", r"\1", html)
    m = re.search(r'<meta name="dc:title" content="([^"]*)"', html)
    titulo = " ".join(htmllib.unescape(m.group(1)).split()) if m else ""
    corpo = html_para_md(html)
    if not titulo:
        titulo = re.sub(r"[*\\]", "", corpo.strip().split("\n", 1)[0])[:150]
    tipo = classificar(titulo) or classificar(re.sub(r"[*\\]", "", corpo.strip())[:80])
    if not tipo:
        return "fora_escopo", None
    pasta, nome, prefixo = tipo
    texto_plano = re.sub(r"[*\\#]", "", corpo)
    data = data_do_texto(texto_plano, html, titulo=titulo)
    ano = data[:4] or "sem-ano"
    # "LEI Nº 8.575" e "DEC-000120" são as duas formas em que o número aparece
    num = re.search(r"N[º°o.]*\s*([\d.]+)", titulo, re.I) or re.search(r"^[A-Z]{3}-0*(\d+)", titulo)
    num_meta = re.search(r'<meta\s+name="Numero"\s+content="0*(\d+)"', html, re.I)
    numero = num_meta.group(1) if num_meta else num.group(1).replace(".", "") if num else ""
    slug = f"{prefixo}-{numero or 'sn'}-{ano}-id{id_}"
    md, fonte = caminhos(UF, pasta, ano, slug)
    if os.path.exists(md):
        return "pulado", None
    if len(re.sub(r"\W", "", corpo)) < 40:
        return "sem_texto", {"id": id_, "motivo": "texto vazio"}
    cabeca = texto_plano[:2000].upper()
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", numero),
        ("data", data),
        ("revogada", norma_revogada(html, cabeca)),
        ("versao_texto", "texto anotado da ALESC"),
        ("fonte", f"{BASE}/ato-normativo/{id_}"),
    ]
    gravar(md, fonte, bruto, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    ids = list(range(ID_MAX, 0, -1))
    if "--inicio" in sys.argv:
        inicio = int(sys.argv[sys.argv.index("--inicio") + 1])
        ids = list(range(inicio, 0, -1))
    elif len(sys.argv) > 1:
        ids = [int(x) for x in sys.argv[1].split(",")] if "," in sys.argv[1] else ids[-int(sys.argv[1]):]
    executar(UF, ids, processar, workers=3)
