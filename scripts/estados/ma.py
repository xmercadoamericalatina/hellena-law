"""Maranhão — GED da Assembleia Legislativa (arquivos.al.ma.leg.br:8443/ged/legislacao/{TIPO}_{numero}).

Não há índice público completo: percorre a numeração de cada tipo (os inexistentes dão 404).
Texto: PDF (OCR quando escaneado). Título, data e ementa saem do próprio texto.
"""
import os
import datetime as dt
import gzip
import threading
from pathlib import Path
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, documento_para_md, executar, gravar  # noqa: E402

UF = "MA"
B = "https://arquivos.al.ma.leg.br:8443/ged/legislacao"
# prefixo no GED -> (pasta, nome, maior número a tentar)
TIPOS = {
    "EC": ("emendas-constitucionais", "Emenda Constitucional", 150),
    "LC": ("leis-complementares", "Lei Complementar", 400),
    "LEI": ("leis-ordinarias", "Lei Ordinária", 13500),
}
MESES = {m: i for i, m in enumerate(
    "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split(), 1)}
MESES["marco"] = 3
rede = Rede(rps=2)
bloqueado = threading.Event()


def cabecalho_proprio(corpo, prefixo, numero):
    plano = re.sub(r"[*\\#>]", "", corpo)
    tipo = {"EC": r"EMENDA\s+(?:CONSTITUCIONAL|À\s+CONSTITUIÇÃO)(?:\s+ESTADUAL)?",
            "LC": r"LEI\s+COMPLEMENTAR", "LEI": r"LEI(?!\s+COMPLEMENTAR)"}[prefixo]
    flex = r"0*" + r"\.?".join(str(numero))
    cab = re.search(r"^" + tipo + r"\s+N[º°oO.\s]*" + flex + r"\b(?P<resto>[^\n]*)", plano, re.I | re.M)
    if not cab:
        return None
    ano = re.search(r"\b((?:18|19|20)\d{2})\b", cab["resto"])
    ano = ano[1] if ano else ""
    data = ""
    raw_data = ""
    # Apenas a epígrafe própria ou a assinatura institucional, nunca leis citadas no corpo.
    candidato = re.search(r"(\d{1,2})[º°]?\s+DE\s+([A-Za-zÀ-ÿ]+)\s+DE\s+(\d{4})", cab["resto"], re.I)
    if not candidato:
        candidato = re.search(r"(?:PLENÁRIO|PALÁCIO)[\s\S]{0,250}?\bem\s+(\d{1,2})[º°]?\s+de\s+([A-Za-zÀ-ÿ]+)\s+de\s+(\d{4})", plano[-4000:], re.I)
    if candidato and candidato[2].lower() in MESES and (not ano or candidato[3] == ano):
        raw_data = f"{candidato[3]}-{MESES[candidato[2].lower()]:02d}-{int(candidato[1]):02d}"
        try:
            d = dt.date.fromisoformat(raw_data)
            if d <= dt.date.today():
                data = d.isoformat()
        except ValueError:
            pass
    ano = ano or (data[:4] if data else "sem-ano")
    ementa = ""
    for paragrafo in plano[cab.end():].split("\n\n"):
        paragrafo = " ".join(paragrafo.split()).lstrip(".,;:- ")
        if len(paragrafo) > 20 and not re.match(r"(O|A) (GOVERNADOR|GOVERNADORA|PRESIDENTE|MESA)|Faço saber|Art\.", paragrafo, re.I):
            ementa = paragrafo[:600]
            break
    return {"data": data, "ano": ano, "ementa": ementa, "data_na_fonte": raw_data if raw_data and not data else ""}



def processar(item):
    prefixo, numero = item
    pasta, nome, _ = TIPOS[prefixo]
    url = f"{B}/{prefixo}_{numero}"
    cache = Path(RAIZ_ESTADUAIS) / UF / "_indice" / "ged" / f"{prefixo}_{numero}.pdf.gz"
    cache.parent.mkdir(parents=True, exist_ok=True)
    anteriores = list((Path(RAIZ_ESTADUAIS) / UF / "_fonte" / pasta).glob(f"*/{prefixo.lower()}-{numero}-*.html.gz"))
    if cache.exists():
        doc, ctype, st = gzip.decompress(cache.read_bytes()), "application/pdf", 200
    elif anteriores:
        doc, ctype, st = gzip.decompress(anteriores[0].read_bytes()), "application/pdf", 200
    else:
        if bloqueado.is_set():
            return "fonte_bloqueada", None
        st, doc, ctype = rede.get(url, timeout=90, tentativas=2)
    if st in (401, 403, 429):
        bloqueado.set()
    if st == 404:
        return "inexistente", None
    if st != 200 or not doc:
        return "sem_texto", {"norma": f"{prefixo}_{numero}", "http": st}
    cache.write_bytes(gzip.compress(doc))
    corpo, motivo = documento_para_md(doc, url, ctype)
    if corpo is None:
        return "sem_texto", {"norma": f"{prefixo}_{numero}", "url": url, "motivo": motivo}
    info = cabecalho_proprio(corpo, prefixo, numero)
    if info is None:
        return "sem_texto", {"norma": f"{prefixo}_{numero}", "url": url, "motivo": "epígrafe própria não reconhecida"}
    data, ano, ementa = info["data"], info["ano"], info["ementa"]
    titulo = f"{nome} nº {numero}" + (f", de {data[8:10]}/{data[5:7]}/{data[:4]}" if data else "")
    md, fonte = caminhos(UF, pasta, ano, f"{prefixo.lower()}-{numero}-{ano}")
    if os.path.exists(md):
        return "pulado", None
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", str(numero)),
        ("data", data),
        ("ementa", ementa),
        ("versao_texto", "PDF do GED da Assembleia Legislativa"),
        ("fonte", url),
    ]
    if info["data_na_fonte"]:
        meta.append(("data_na_fonte", info["data_na_fonte"]))
    gravar(md, fonte, doc, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = [(p, n) for p, (_, _, maximo) in TIPOS.items() for n in range(maximo, 0, -1)]
    if len(sys.argv) > 1:
        itens = [tuple(x.split("_")) for x in sys.argv[1].split(",")]
        itens = [(p, int(n)) for p, n in itens]
    executar(UF, itens, processar, workers=3)
