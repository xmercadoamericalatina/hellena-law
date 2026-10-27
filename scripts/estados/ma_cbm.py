"""Decretos estaduais disponíveis na biblioteca oficial do CBMMA."""
import html
import json
import os
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, decodificar, documento_para_md, executar, gravar
from datas import data_do_texto

URL = "https://cbm.ssp.ma.gov.br/cbmma/institucional/legislacao/"
rede = Rede(rps=2)


def indice():
    cache = Path(RAIZ_ESTADUAIS) / "MA" / "_indice" / "cbm-legislacao.html"
    cache.parent.mkdir(parents=True, exist_ok=True)
    if not cache.exists():
        st, raw, ct = rede.get(URL)
        if st != 200:
            raise RuntimeError(f"CBMMA índice HTTP {st}")
        cache.write_bytes(raw)
    s = decodificar(cache.read_bytes(), "text/html; charset=utf-8")
    itens = {}
    for url, texto in re.findall(r"<a[^>]+href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", s, re.S | re.I):
        texto = html.unescape(re.sub(r"<[^>]*>", " ", texto)).strip()
        url = html.unescape(url)
        m = re.match(r"Decreto\s+(?:n[º°]\s*)?([\d.]+).*?(\d{4})", texto, re.I)
        if m and "cbm.ssp.ma.gov.br/" in url and url.lower().endswith(".pdf"):
            itens[url] = {"url": url, "titulo": texto, "numero": m[1].replace(".", ""), "ano": m[2]}
    lista = list(itens.values())
    cache.with_suffix(".json").write_text(json.dumps(lista, ensure_ascii=False))
    return lista


def processar(it):
    md, fonte = caminhos("MA", "decretos", it["ano"], f"dec-{it['numero']}-{it['ano']}")
    if os.path.exists(md):
        return "pulado", None
    url = urllib.parse.quote(it["url"], safe=":/?=&%")
    st, raw, ct = rede.get(url)
    if st != 200:
        return "sem_texto", {"url": url, "http": st}
    corpo, motivo = documento_para_md(raw, url, ct, set())
    if corpo is None:
        return "sem_texto", {"url": url, "motivo": motivo}
    data = data_do_texto(corpo, it["numero"])
    meta = [("titulo", it["titulo"]), ("uf", "MA"), ("tipo", "Decreto"),
            ("numero", it["numero"]), ("data", data or ""), ("ementa", ""),
            ("versao_texto", "Documento da biblioteca oficial do CBMMA"), ("fonte", url)]
    gravar(md, fonte, raw, meta, f"# {it['titulo']}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    executar("MA", indice(), processar, workers=2)
