"""Mato Grosso — Legislação da Assembleia Legislativa (www.al.mt.gov.br/norma-juridica).

Índice: listagem paginada /norma-juridica?page=N (10 por página, todos os tipos), cada norma com URN LexML.
Texto: PDF gerado pelo site com a redação atual (/norma-juridica/{urn}/gerar-pdf-redacao).
"""
import html as htmllib
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, decodificar, documento_para_md, executar, gravar  # noqa: E402

UF = "MT"
B = "https://www.al.mt.gov.br"
# tipo na URN LexML -> (pasta, tipo canônico, prefixo do arquivo). Os cinco primeiros prefixos já
# estão gravados e não mudam. Resolução é 44% do que a Assembleia publica e ficava toda de fora;
# "ato" fica fora de propósito: é ato de administração interna da Casa ("Ato - 078/2026"), sem
# ementa e sem efeito normativo geral.
TIPOS = {
    "emenda.constitucional": ("emendas-constitucionais", "Emenda Constitucional", "ec"),
    "lei.complementar": ("leis-complementares", "Lei Complementar", "lc"),
    "lei.ordinaria": ("leis-ordinarias", "Lei Ordinária", "lei"),
    "lei.delegada": ("leis-delegadas", "Lei Delegada", "ld"),
    "decreto.lei": ("decretos-lei", "Decreto-Lei", "dl"),
    "resolucao": ("resolucoes", "Resolução", "res"),
    "decreto.legislativo": ("decretos-legislativos", "Decreto Legislativo", "dlg"),
}
CONSTITUICAO = "https://storage.al.mt.gov.br/api/v1/download/default/958660"
CARD = re.compile(
    r'<h5 class="fw-bold">\s*(.*?)\s*</h5>\s*<div class="text-muted mb-2">(.*?)</div>.*?'
    r'href="/norma-juridica/(urn:lex:[^"/]+)/gerar-pdf-redacao"',
    re.S,
)
rede = Rede(rps=3)


def indice(refazer=False):
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice")
    arq = os.path.join(pasta, "normas.json")
    if os.path.exists(arq) and not refazer:
        return json.load(open(arq, encoding="utf-8"))
    st, dados, ctype = rede.get(f"{B}/norma-juridica")
    ultima = max(int(p) for p in re.findall(r"norma-juridica\?page=(\d+)", decodificar(dados, ctype)))
    itens = {}
    for p in range(1, ultima + 1):
        for _ in range(4):
            st, dados, ctype = rede.get(f"{B}/norma-juridica?page={p}")
            if st == 200:
                break
        for titulo, ementa, urn in CARD.findall(decodificar(dados, ctype)):
            tipo = urn.split(":")[4]
            if tipo in TIPOS:
                itens[urn] = {"urn": urn, "titulo": " ".join(htmllib.unescape(titulo).split()),
                              "ementa": " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", ementa)).split())}
        if p % 200 == 0:
            print(f"[{UF}] índice página {p}/{ultima}: {len(itens)} leis", flush=True)
    lista = list(itens.values()) + [{"urn": "constituicao", "titulo": "Constituição do Estado de Mato Grosso", "ementa": ""}]
    os.makedirs(pasta, exist_ok=True)
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False)
    return lista


def processar(it):
    if it["urn"] == "constituicao":
        pasta, nome, prefixo, data, numero, url = "constituicao", "Constituição Estadual", "ce", "1989-10-05", "", CONSTITUICAO
        titulo, ano, slug = it["titulo"], "1989", "constituicao-mt"
        fonte_pagina = CONSTITUICAO
    else:
        # urn:lex:br;mato.grosso:estadual:lei.ordinaria:2026-09-22;13563
        tipo, resto = it["urn"].split(":")[4], it["urn"].split(":")[5]
        pasta, nome, prefixo = TIPOS[tipo]
        data, numero = (resto.split(";") + [""])[:2]
        ano = data[:4] or "sem-ano"
        slug = f"{prefixo}-{numero or 'sn'}-{data or ano}"
        titulo = f"{nome} nº {numero}, de {data[8:10]}/{data[5:7]}/{data[:4]}" if numero and data else it["titulo"]
        url = f"{B}/norma-juridica/{it['urn']}/gerar-pdf-redacao"
        fonte_pagina = f"{B}/norma-juridica/{it['urn']}"
    md, fonte = caminhos(UF, pasta, ano, slug)
    if os.path.exists(md):
        return "pulado", None
    st, doc, ctype = rede.get(url, timeout=300)
    if st != 200 or not doc:
        return "sem_texto", {"urn": it["urn"], "http": st}
    corpo, motivo = documento_para_md(doc, url, ctype)
    if corpo is None:
        return "sem_texto", {"urn": it["urn"], "motivo": motivo}
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", numero),
        ("data", data),
        ("ementa", it["ementa"]),
        ("versao_texto", "redação atual (PDF gerado pela ALMT)"),
        ("urn", it["urn"] if it["urn"] != "constituicao" else ""),
        ("fonte", fonte_pagina),
    ]
    gravar(md, fonte, doc, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice(refazer="--refazer" in sys.argv)
    print(f"[{UF}] {len(itens)} normas no índice", flush=True)
    limite = [a for a in sys.argv[1:] if a.isdigit()]
    if limite:
        itens = itens[: int(limite[0])]
    executar(UF, itens, processar, workers=3)
