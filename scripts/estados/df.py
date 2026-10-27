"""Distrito Federal — SINJ-DF (Sistema Integrado de Normas Jurídicas do DF).

Índice: ResultadoDePesquisaNormaDatatable.ashx **sem filtro de tipo**, porque o próprio registro
traz `nm_tipo_norma`. A primeira versão filtrava por código de tipo e só pedia as cinco espécies de
lei; o SINJ tem 125 mil normas, das quais 49 mil decretos, 32 mil portarias e 5 mil resoluções —
todo o infralegal distrital, que o plano (scripts/plano.py) cobre. Paginar a base inteira e
classificar pelo nome do tipo é mais simples e não exige descobrir código nenhum.

Texto: /sinj/Norma/{ch_norma}/{arquivo}, preferindo o texto compilado (ar_atualizado).

  python3 -I scripts/estados/df.py              # índice (em cache) e baixa o que falta
  python3 -I scripts/estados/df.py --refazer    # refaz o índice antes de baixar
  python3 -I scripts/estados/df.py 50           # só as 50 normas mais recentes (teste)
"""
import collections
import gzip
import hashlib
import json
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, documento_para_md, extrair_texto, executar, gravar  # noqa: E402

from sinj_tachados import converter_html_sinj  # noqa: E402

UF = "DF"
BASE = "https://www.sinj.df.gov.br/sinj"
# nm_tipo_norma do SINJ -> (pasta, tipo canônico, prefixo do arquivo).
# Os cinco primeiros prefixos são os que o acervo já gravou e não podem mudar: é por eles que uma
# nova rodada reconhece o que já existe e pula.
TIPOS = {
    "Lei Orgânica": ("lei-organica", "Lei Orgânica", "lodf"),
    "Emenda à Lei Orgânica": ("emendas-lei-organica", "Emenda à Lei Orgânica", "elo"),
    "Lei Complementar": ("leis-complementares", "Lei Complementar", "lc"),
    "Lei": ("leis-ordinarias", "Lei Ordinária", "lei"),
    "Decreto Lei": ("decretos-lei", "Decreto-Lei", "dl"),
    "Decreto": ("decretos", "Decreto", "dec"),
    "Decreto Executivo": ("decretos", "Decreto", "dec-exec"),
    "Decreto Legislativo": ("decretos-legislativos", "Decreto Legislativo", "dlg"),
    "Resolução": ("resolucoes", "Resolução", "res"),
    "Resolução Normativa": ("resolucoes", "Resolução", "res-norm"),
    "Resolução Administrativa": ("resolucoes", "Resolução", "res-adm"),
    "Instrução Normativa": ("instrucoes-normativas", "Instrução Normativa", "in"),
    "Portaria": ("portarias", "Portaria", "port"),
    "Portaria Conjunta": ("portarias", "Portaria", "port-conj"),
    "Portaria Normativa": ("portarias", "Portaria", "port-norm"),
    "Deliberação": ("deliberacoes", "Deliberação", "delib"),
    "Parecer Normativo": ("pareceres-normativos", "Parecer Normativo", "pn"),
    "Súmula": ("sumulas", "Súmula", "sum"),
    "Súmula Administrativa": ("sumulas", "Súmula", "sum-adm"),
    "Regimento Interno": ("regimentos", "Regimento Interno", "ri"),
    "Provimento": ("provimentos", "Provimento", "prov"),
}
# O que o SINJ guarda e não é norma de caráter geral: ordem de serviço, ato de mesa diretora,
# despacho, decisão em processo, ata, edital, parecer em caso concreto, nota técnica, plano. E as
# ações de controle concentrado (ADI, ADPF), que são processo judicial, não norma distrital.
rede = Rede(rps=3)


def post_datatable(ch_tipo, inicio, tamanho):
    """Uma página do resultado. `ch_tipo` None traz a base inteira, de todos os tipos."""
    import urllib.request

    url = f"{BASE}/ashx/Datatable/ResultadoDePesquisaNormaDatatable.ashx?tipo_pesquisa=norma"
    if ch_tipo:
        url += f"&ch_tipo_norma={ch_tipo}"
    corpo = urllib.parse.urlencode(
        {"bbusca": "sinj_norma", "sEcho": "1", "iDisplayStart": inicio, "iDisplayLength": tamanho}
    ).encode()
    rede.limite.esperar()
    req = urllib.request.Request(url, data=corpo, headers={**rede.headers, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        dados = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            import gzip

            dados = gzip.decompress(dados)
    return json.loads(dados)


def indice(refazer=False):
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice")
    arq = os.path.join(pasta, "sinj.json")
    if os.path.exists(arq) and not refazer:
        return json.load(open(arq, encoding="utf-8"))
    normas, inicio, total = {}, 0, None
    while True:
        d = post_datatable(None, inicio, 1000)
        lote = [x["_source"] for x in d.get("aaData") or []]
        if total is None:
            total = int(d.get("iTotalDisplayRecords") or 0)
            print(f"[{UF}] a base tem {total} normas", flush=True)
        for s in lote:
            if s.get("nm_tipo_norma") in TIPOS:
                s["_ch_tipo"] = s["nm_tipo_norma"]
                normas[s["ch_norma"]] = s
        inicio += len(lote)
        if not lote or inicio >= total:
            break
        if inicio % 10000 == 0:
            print(f"[{UF}] índice {inicio}/{total}, {len(normas)} normas", flush=True)
    itens = list(normas.values())
    por_tipo = collections.Counter(s["_ch_tipo"] for s in itens)
    for t, n in por_tipo.most_common():
        print(f"[{UF}]   {t}: {n}", flush=True)
    os.makedirs(pasta, exist_ok=True)
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(itens, f, ensure_ascii=False)
    return itens


def arquivo_texto(s):
    """Prefere o texto compilado; senão, o arquivo da publicação mais recente."""
    at = s.get("ar_atualizado") or {}
    if at.get("filename"):
        return at["filename"], True
    for f in reversed(s.get("fontes") or []):
        ar = f.get("ar_fonte") or {}
        if ar.get("filename"):
            return ar["filename"], False
    return None, False


def processar(s):
    pasta, nome, prefixo = TIPOS[s["_ch_tipo"]]
    d, m, a = (s.get("dt_assinatura") or "01/01/0000").split("/")
    numero = s.get("nr_norma") or ""
    slug = f"{prefixo}-{numero or 'sn'}-{a}-{m}-{d}"
    if s.get("nr_sequencial"):
        slug += f"-s{s['nr_sequencial']}"
    md, fonte = caminhos(UF, pasta, a, slug)
    if os.path.exists(md):
        return "pulado", None
    nome_arq, compilado = arquivo_texto(s)
    if not nome_arq:
        return "sem_texto", {"ch": s["ch_norma"], "motivo": "sem arquivo"}
    url = f"{BASE}/Norma/{s['ch_norma']}/{urllib.parse.quote(nome_arq)}"
    st, bruto, ctype = rede.get(url, timeout=180)
    if st != 200 or not bruto:
        return "sem_texto", {"ch": s["ch_norma"], "url": url, "http": st}
    parece_html = not bruto.startswith((b"%PDF", b"PK", b"\xd0\xcf\x11\xe0")) and (
        "html" in ctype.lower() or bruto.lstrip().startswith(b"<"))
    html, texto = extrair_texto(bruto, url, ctype) if parece_html else (None, None)
    edicao = "compilada (SINJ-DF)" if compilado else "original"
    if html is not None:
        try:
            corpo, edicao, prova_edicao = converter_html_sinj(html, compilado=compilado, situacao=s.get("nm_situacao") or "")
            if prova_edicao["edicao"] == "sem tachado ativo":
                corpo, motivo = documento_para_md(bruto, url, ctype, {"Texto Compilado", "Texto Original"})
            elif len(re.sub(r"\W", "", corpo)) < 40:
                corpo, motivo = None, "documento vazio"
            else:
                motivo = None
        except ValueError as exc:
            sha = hashlib.sha256(bruto).hexdigest()
            evidencia = os.path.join(RAIZ_ESTADUAIS, UF, "_fonte", "auditorias", "css-nao-comprovado", f"{s['ch_norma']}-{sha}.html.gz")
            os.makedirs(os.path.dirname(evidencia), exist_ok=True)
            if not os.path.exists(evidencia):
                with gzip.open(evidencia, "wb") as arq:
                    arq.write(bruto)
            return "sem_texto", {"ch": s["ch_norma"], "url": url, "motivo": str(exc), "cache": evidencia, "sha256_fonte": sha}
    else:
        corpo, motivo = documento_para_md(bruto, url, ctype, {"Texto Compilado", "Texto Original"})
    if corpo is None:
        return "sem_texto", {"ch": s["ch_norma"], "url": url, "motivo": motivo}
    corpo = corpo.replace("\x00", "")
    titulo = "Lei Orgânica do Distrito Federal" if nome == "Lei Orgânica" else f"{nome} nº {numero}, de {d}/{m}/{a}"
    situacao = s.get("nm_situacao") or ""
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", numero),
        ("data", f"{a}-{m}-{d}"),
        ("ementa", " ".join((s.get("ds_ementa") or "").split())),
        ("situacao", situacao),
        ("revogada", {"revogada": True, "revogado": True, "vigente": False, "em vigor": False}.get(situacao.strip().lower())),
        ("versao_texto", edicao),
        ("fonte", f"{BASE}/Norma/{s['ch_norma']}/{nome_arq}"),
    ]
    gravar(md, fonte, bruto, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice(refazer="--refazer" in sys.argv)
    itens.sort(key=lambda s: "".join(reversed((s.get("dt_assinatura") or "").split("/"))), reverse=True)
    print(f"[{UF}] {len(itens)} normas no índice", flush=True)
    limite = [a for a in sys.argv[1:] if a.isdigit()]
    if limite:
        itens = itens[: int(limite[0])]
    executar(UF, itens, processar, workers=3)
