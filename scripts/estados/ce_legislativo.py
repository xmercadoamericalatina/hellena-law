"""Ceará — decretos legislativos do índice oficial histórico da ALECE."""
import html
import json
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, decodificar, executar, gravar, html_para_md

URL = "https://www2.al.ce.gov.br/legislativo/decleg/decleg.htm"
rede = Rede(rps=2)


def limpar(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def indice():
    pasta = os.path.join(RAIZ_ESTADUAIS, "CE", "_indice")
    os.makedirs(pasta, exist_ok=True)
    cache = os.path.join(pasta, "decretos-legislativos.html")
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as f:
            pagina = f.read()
    else:
        st, dados, ct = rede.get(URL)
        if st != 200:
            raise RuntimeError(f"índice ALECE: HTTP {st}")
        pagina = decodificar(dados, ct)
        with open(cache, "w", encoding="utf-8") as f:
            f.write(pagina)
    itens = {}
    for href, texto in re.findall(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', pagina, re.S | re.I):
        titulo = limpar(texto)
        m = re.search(r"DECRETO\s+LEGISLATIVO.*?(\d+),?\s+DE\s+(\d{1,2})\.(\d{1,2})\.(\d{2,4})", titulo, re.I)
        if not m:
            m = re.search(r"(\d+),?\s+(?:DE\s+)?(\d{1,2})\.(\d{1,2})\.(\d{2,4})", titulo, re.I)
        if not m or not re.fullmatch(r"dl\d+\.htm", href, re.I):
            continue
        numero, dia, mes, ano = m.groups()
        if len(ano) == 2:
            ano = ("19" if int(ano) > 30 else "20") + ano
        url = urllib.parse.urljoin(URL, href)
        itens[url] = {"url": url, "titulo": titulo, "numero": numero,
                      "data": f"{ano}-{int(mes):02d}-{int(dia):02d}"}
    lista = list(itens.values())
    if not lista:
        raise RuntimeError("índice ALECE sem decretos legislativos reconhecidos")
    with open(os.path.join(pasta, "decretos-legislativos.json"), "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False)
    return lista


def processar(it):
    ano = it["data"][:4]
    md, fonte = caminhos("CE", "decretos-legislativos", ano, f"dlg-{it['numero']}-{ano}")
    if os.path.exists(md):
        return "pulado", None
    st, dados, ct = rede.get(it["url"])
    if st != 200:
        return "sem_texto", {"url": it["url"], "http": st}
    pagina = decodificar(dados, ct)
    corpo = html_para_md(pagina, {"VOLTAR", "Voltar"})
    if len(re.sub(r"\W", "", corpo)) < 80:
        return "sem_texto", {"url": it["url"], "motivo": "texto vazio"}
    meta = [("titulo", it["titulo"]), ("uf", "CE"), ("tipo", "Decreto Legislativo"),
            ("numero", it["numero"]), ("data", it["data"]), ("ementa", ""),
            ("versao_texto", "texto do repositório legislativo da ALECE"), ("fonte", it["url"])]
    gravar(md, fonte, dados, meta, f"# {it['titulo']}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice()
    print(f"[CE] {len(itens)} decretos legislativos no índice", flush=True)
    if len(sys.argv) > 1:
        itens = itens[:int(sys.argv[1])]
    executar("CE", itens, processar, workers=2)
