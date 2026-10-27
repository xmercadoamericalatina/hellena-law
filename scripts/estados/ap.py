"""Amapá — e-Legis da Assembleia Legislativa (elegis.al.ap.leg.br/portal/legislacao).

Índice: listagem paginada por tipo (?tipo_proposicao_id=N&page=P), 20 por página.
Texto: /portal/proposicao/{id}/texto-integral (PDF ou HTML; OCR quando escaneado).
"""
import html as htmllib
import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, decodificar, documento_para_md, executar, gravar  # noqa: E402

UF = "AP"
B = "https://elegis.al.ap.leg.br/portal"
# tipo_proposicao_id no e-Legis -> (pasta, tipo canônico, prefixo). O seletor da listagem oferece
# quatro tipos; os dois primeiros prefixos já estão gravados e não mudam.
TIPOS = {
    "2": ("leis-complementares", "Lei Complementar", "lc"),
    "1": ("leis-ordinarias", "Lei Ordinária", "lei"),
    "9": ("resolucoes", "Resolução", "res"),
    "10": ("decretos-legislativos", "Decreto Legislativo", "dlg"),
}
CONSTITUICAO = "http://silegis.al.ap.leg.br/proposicaopdf/2CEatualizadaeconsolidadaateEC071comSumario.pdf"
LINHA = re.compile(
    r'<td class="ls-txt-center">([^<]+)</td>\s*<td>(.*?)</td>\s*<td>([^<]*)</td>\s*<td>([^<]*)</td>.*?'
    r'proposicao/(\d+)"[^>]*>([^<]*)</a>\s*</td>\s*<td class="ls-txt-right">(.*?)</td>',
    re.S,
)
rede = Rede(rps=3)


def limpar(s):
    return " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def indice(refazer=False):
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice")
    arq = os.path.join(pasta, "legislacao.json")
    if os.path.exists(arq) and not refazer:
        return json.load(open(arq, encoding="utf-8"))
    itens = []
    for tipo in TIPOS:
        p = 1
        while True:
            st, dados, ctype = rede.get(f"{B}/legislacao?tipo_proposicao_id={tipo}&page={p}", timeout=300)
            linhas = LINHA.findall(decodificar(dados, ctype)) if st == 200 else []
            if not linhas:
                break
            for titulo, ementa, doe, pub, prop, prop_nome, ver in linhas:
                texto = re.search(r'href="([^"]+/texto-integral)"', ver)
                itens.append({"tipo": tipo, "titulo": limpar(titulo), "ementa": limpar(ementa), "doe": doe.strip(),
                              "publicado": pub.strip(), "proposicao": prop, "texto": texto.group(1) if texto else ""})
            p += 1
        print(f"[{UF}] índice tipo {tipo}: {sum(1 for i in itens if i['tipo'] == tipo)}", flush=True)
    itens.append({"tipo": "ce", "titulo": "Constituição do Estado do Amapá", "ementa": "", "doe": "", "publicado": "",
                  "proposicao": "", "texto": CONSTITUICAO})
    os.makedirs(pasta, exist_ok=True)
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(itens, f, ensure_ascii=False)
    return itens


def processar(it):
    if it["tipo"] == "ce":
        pasta, nome, prefixo = "constituicao", "Constituição Estadual", "ce"
        numero, data, ano, slug = "", "1991-12-20", "1991", "constituicao-ap"
    else:
        pasta, nome, prefixo = TIPOS[it["tipo"]]
        m = re.search(r"nº\s*([\d.]+),\s*de\s*(\d{2})/(\d{2})/(\d{2,4})", it["titulo"])
        numero = m.group(1) if m else ""
        a = m.group(4) if m else ""
        a = ("19" if a and int(a) > 50 else "20") + a if len(a) == 2 else a
        data = f"{a}-{m.group(3)}-{m.group(2)}" if m else ""
        ano = a or "sem-ano"
        slug = f"{prefixo}-{numero.replace('.', '') or 'sn'}-{ano}-p{it['proposicao']}"
    md, fonte = caminhos(UF, pasta, ano, slug)
    if os.path.exists(md):
        return "pulado", None
    if not it["texto"]:
        return "sem_texto", {"titulo": it["titulo"], "motivo": "sem texto integral no portal"}
    st, doc, ctype = rede.get(it["texto"], timeout=300)
    if st != 200 or not doc:
        return "sem_texto", {"titulo": it["titulo"], "url": it["texto"], "http": st}
    corpo, motivo = documento_para_md(doc, it["texto"], ctype)
    if corpo is None:
        return "sem_texto", {"titulo": it["titulo"], "url": it["texto"], "motivo": motivo}
    data_na_fonte = ""
    if data:
        try:
            if dt.date.fromisoformat(data) > dt.date.today():
                raise ValueError("data futura")
        except ValueError:
            data_na_fonte, data = data, ""
    meta = [
        ("titulo", it["titulo"]),
        ("uf", UF),
        ("tipo", nome),
        ("numero", numero),
        ("data", data),
        ("ementa", it["ementa"]),
        ("publicacao", f"DOE nº {it['doe']}, {it['publicado']}" if it["doe"] else ""),
        ("versao_texto", "consolidada" if it["tipo"] == "ce" else "texto integral do e-Legis"),
        ("fonte", it["texto"]),
    ]
    if data_na_fonte:
        meta.append(("data_na_fonte", data_na_fonte))
    gravar(md, fonte, doc, meta, f"# {it['titulo']}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice(refazer="--refazer" in sys.argv)
    print(f"[{UF}] {len(itens)} normas no índice", flush=True)
    limite = [a for a in sys.argv[1:] if a.isdigit()]
    if limite:
        itens = itens[: int(limite[0])]
    executar(UF, itens, processar, workers=3)
