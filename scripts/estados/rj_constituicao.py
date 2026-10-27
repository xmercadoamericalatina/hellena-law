"""Constituição RJ pelo wrapper público da ALERJ, com índice paginado e cache."""
import base64
import fcntl
import gzip
import hashlib
import html
import json
import os
import re
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, decodificar, caminhos, gravar, html_para_md

BASE = "https://www3.alerj.rj.gov.br/lotus_notes/default.asp?id=73"
CACHE = Path(RAIZ_ESTADUAIS) / "RJ" / "_indice" / "constituicao"
rede = Rede(rps=2)


def obter(route):
    CACHE.mkdir(parents=True, exist_ok=True)
    cache = CACHE / (hashlib.sha256(route.encode()).hexdigest() + ".html.gz")
    if cache.exists():
        return gzip.decompress(cache.read_bytes())
    url = BASE + "&url=" + urllib.parse.quote(base64.b64encode(route.encode()).decode(), safe="")
    st, raw, ct = rede.get(url)
    if st != 200:
        raise RuntimeError(f"ALERJ HTTP {st}: {route}")
    cache.write_bytes(gzip.compress(raw))
    return raw


def main():
    route = "/constest.nsf/IndiceInt?OpenForm&ExpandView"
    paginas, docs, visitados = [], [], set()
    while route not in visitados:
        visitados.add(route)
        raw = obter(route)
        paginas.append(raw)
        s = decodificar(raw, "text/html; charset=utf-8")
        fim_constituicao = False
        for item, titulo in re.findall(r'<a[^>]+data-role="([^"]+)"[^>]*>(.*?)</a>', s, re.S | re.I):
            item = html.unescape(item)
            if "EMENDAS CONSTITUCIONAIS" in re.sub(r"<[^>]+>", "", titulo).upper():
                fim_constituicao = True
                continue
            if "constest.nsf/" in item and "OpenDocument" in item and item not in docs:
                docs.append(item)
        rotas = [html.unescape(x) for x in re.findall(r'data-role="([^"]+)"[^>]*shape=', s)]
        prox = next((x for x in rotas if "Start=" in x and "ExpandView" in x
                     and "Start=1&" not in x and x not in visitados), None)
        print(f"[RJ] índice {len(paginas)}: {len(docs)} seções", flush=True)
        if fim_constituicao or not prox or prox in visitados:
            break
        route = prox
    if len(docs) < 20:
        raise RuntimeError("índice constitucional incompleto: menos de 20 seções")
    (CACHE / "secoes.json").write_text(json.dumps(docs, ensure_ascii=False))
    with ThreadPoolExecutor(max_workers=2) as pool:
        fontes = list(pool.map(obter, docs))
    corpos = []
    for raw in fontes:
        s = decodificar(raw, "text/html; charset=utf-8")
        start = re.search(r'<A NAME\s*=\s*"TOPO"', s, re.I)
        if not start:
            raise RuntimeError("seção sem início de conteúdo")
        s = s[start.start():]
        end = re.search(r'<a[^>]+id="A2"|<div[^>]+class="alert alert-warning"', s, re.I)
        if end:
            s = s[:end.start()]
        corpo = html_para_md(s, set())
        # Capítulos sem artigos próprios têm só título; os artigos estão nas seções filhas.
        if len(corpo) < 40:
            raise RuntimeError("seção sem texto")
        corpos.append(corpo)
    corpo = "\n\n".join(corpos)
    if not re.search(r"Art\.\s*369", corpo) or "TRANSITÓRIAS" not in corpo:
        raise RuntimeError("compilação sem artigo final 369 ou ADCT; revisar índice")
    md, fonte = caminhos("RJ", "constituicao", "1989", "constituicao-rj-alerj")
    meta = [("titulo", "Constituição do Estado do Rio de Janeiro"), ("uf", "RJ"),
            ("tipo", "Constituição Estadual"), ("numero", ""), ("data", "1989-10-05"),
            ("ementa", ""), ("versao_texto", "Compilação ALERJ; data-limite global não declarada"),
            ("fonte", BASE)]
    gravar(md, fonte, b"\n".join(fontes), meta, "# Constituição do Estado do Rio de Janeiro\n\n" + corpo)
    print(f"[RJ] salvo: {len(docs)} seções, {len(corpo)} caracteres", flush=True)


if __name__ == "__main__":
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    trava = (CACHE.parent / "rj-coleta.lock").open("w")
    fcntl.flock(trava, fcntl.LOCK_EX | fcntl.LOCK_NB)
    main()
