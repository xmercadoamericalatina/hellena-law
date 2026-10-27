"""Tocantins — leis de 1989–2019 do portal oficial, anteriores ao acervo principal do SAPL."""
import html
import json
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, decodificar, documento_para_md, executar, gravar

B = "https://www.al.to.leg.br"
rede = Rede(rps=2)
MESES = {m: i for i, m in enumerate(
    "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split(), 1)}


def limpar(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def indice(ano):
    pasta = os.path.join(RAIZ_ESTADUAIS, "TO", "_indice", "portal-historico")
    os.makedirs(pasta, exist_ok=True)
    itens, pagina = {}, 1
    while True:
        cache = os.path.join(pasta, f"{ano}-{pagina}.html")
        if os.path.exists(cache):
            with open(cache, encoding="utf-8") as f:
                texto = f.read()
        else:
            url = f"{B}/legislacaoEstadual?documento.ano={ano}&pagPaginaAtual={pagina}"
            st, dados, ct = rede.get(url)
            if st != 200:
                raise RuntimeError(f"TO índice {ano}/{pagina}: HTTP {st}")
            texto = decodificar(dados, ct)
            if "Registros encontrados" not in texto:
                raise RuntimeError(f"TO índice {ano}/{pagina}: resposta sem listagem")
            with open(cache, "w", encoding="utf-8") as f:
                f.write(texto)
        linhas = re.findall(r'<h4><a href="(/arquivo/\d+)">(.*?)</a></h4>(.*?)(?=<h4>|<footer|$)', texto, re.S)
        novas = 0
        for href, titulo, resto in linhas:
            titulo = limpar(titulo)
            m = re.fullmatch(r"Lei nº ([\d.]+) de (\d{4}) \((ordinária|complementar)\)", titulo)
            if not m or abs(int(m.group(2)) - ano) > 1:
                raise RuntimeError(f"TO filtro anual não respeitado: {titulo}")
            if href in itens:
                continue
            novas += 1
            ementa = re.search(r"<em><strong>(.*?)</strong></em>", resto, re.S)
            itens[href] = {"url": B + href, "numero": m.group(1).replace(".", ""), "ano": m.group(2),
                           "tipo": m.group(3), "titulo": titulo, "ementa": limpar(ementa.group(1)) if ementa else ""}
        seguintes = [int(p) for p in re.findall(r'pagPaginaAtual=(\d+)', texto)]
        if not novas or not seguintes or pagina >= max(seguintes):
            break
        pagina += 1
    with open(os.path.join(pasta, f"{ano}.json"), "w", encoding="utf-8") as f:
        json.dump(list(itens.values()), f, ensure_ascii=False)
    return list(itens.values())


def processar(it):
    complementar = it["tipo"] == "complementar"
    pasta, nome, prefixo = ("leis-complementares", "Lei Complementar", "lc") if complementar else ("leis-ordinarias", "Lei Ordinária", "lei")
    md, fonte = caminhos("TO", pasta, it["ano"], f"{prefixo}-{it['numero']}-{it['ano']}")
    if os.path.exists(md):
        return "pulado", None
    st, dados, ct = rede.get(it["url"])
    if st != 200 or not dados:
        return "sem_texto", {"url": it["url"], "http": st}
    corpo, motivo = documento_para_md(dados, it["url"], ct)
    if corpo is None:
        return "sem_texto", {"url": it["url"], "motivo": motivo}
    cab = re.search(r"\bDE\s+(\d{1,2})[º°]?\s+DE\s+(\w+)\s+DE\s+(\d{4})", corpo[:2000], re.I)
    data = ""
    if cab and cab.group(2).lower() in MESES and cab.group(3) == it["ano"]:
        data = f"{cab.group(3)}-{MESES[cab.group(2).lower()]:02d}-{int(cab.group(1)):02d}"
    meta = [("titulo", it["titulo"]), ("uf", "TO"), ("tipo", nome), ("numero", it["numero"]),
            ("data", data), ("ementa", it["ementa"]), ("versao_texto", "PDF do portal da Assembleia Legislativa"), ("fonte", it["url"])]
    gravar(md, fonte, dados, meta, f"# {it['titulo']}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    anos = [int(a) for a in sys.argv[1:]] or range(1989, 2020)
    for ano in anos:
        itens = indice(ano)
        print(f"[TO] {ano}: {len(itens)} leis no índice", flush=True)
        executar("TO", itens, processar, workers=2)
