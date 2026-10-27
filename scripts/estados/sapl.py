"""Assembleias que usam o SAPL (Interlegis): índice pela API REST e texto do PDF/arquivo anexado.

Uso:
  python3 -I scripts/estados/sapl.py indice AM        # baixa o índice e mostra a cobertura
  python3 -I scripts/estados/sapl.py baixar AM [N]    # baixa e converte os textos
  python3 -I scripts/estados/sapl.py reconciliar AL [--aplicar]  # aliases comprovados
"""
import collections
import datetime as dt
import hashlib
import gzip
import json
import os
from pathlib import Path
import re
import sys
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import (  # noqa: E402
    RAIZ_ESTADUAIS, Rede, _ACENTOS, caminhos, canonico, documento_para_md, executar, gravar,
    extrair_texto, html_para_md, imagem_bruta,
)

from integridade_texto import motivo_retencao
from avisos_fonte import avisos_de_omissao
from anexos_fonte import remissoes_sem_representacao
from pdf_texto_fiel import conferir_visuais_pdf, extrair_camada_textual
from visuais_fonte import exigir_sem_imagem_omitida


HOSTS = {
    "AM": "sapl.al.am.leg.br",
    "PB": "sapl.al.pb.leg.br",
    "AL": "sapl.al.al.leg.br",
    "RR": "sapl.al.rr.leg.br",
    "AC": "sapl.al.ac.leg.br",
    "RO": "sapl.al.ro.leg.br",
    "PI": "sapl.al.pi.leg.br",
    "TO": "sapl.al.to.leg.br",
}
# Tipos do SAPL que são norma. A primeira versão do acervo só trouxe constituição, emendas, leis e
# decretos-leis; o plano (scripts/plano.py) cobre também o infralegal estadual, e o próprio SAPL
# serve parte dele: a PB publica "Decreto Executivo" ali, o PI publica "Decreto", e quase todas as
# Assembleias publicam decreto legislativo, resolução e o regimento interno da Casa.
TIPO_NORMA = re.compile(r"constitui|emenda|\blei\b|decreto|resolu|regimento", re.I)
# O que fica de fora não é norma: proposição em tramitação, veto, ato interno de mesa diretora.
TIPO_EXCLUIR = re.compile(r"projeto|proposta|veto|requerimento|indica[çc][ãa]o|mensagem"
                          r"|portaria|ato da mesa|ato normativo da mesa", re.I)
rede = Rede(rps=3)


def api(uf, caminho):
    st, dados, _ = rede.get(f"https://{HOSTS[uf]}/api/{caminho}", "application/json")
    if st != 200:
        raise RuntimeError(f"{uf} {caminho}: HTTP {st}")
    return json.loads(dados)


def tipos_lei(uf):
    tipos = {}
    pag = 1
    while True:
        d = api(uf, f"norma/tiponormajuridica/?page_size=100&page={pag}")
        for t in d["results"]:
            desc = t["descricao"].strip()
            if TIPO_NORMA.search(desc) and not TIPO_EXCLUIR.search(desc):
                tipos[t["id"]] = desc
        if not d["pagination"].get("next_page"):
            return tipos
        pag += 1


def indice(uf, refazer=False):
    pasta = os.path.join(RAIZ_ESTADUAIS, uf, "_indice")
    arq = os.path.join(pasta, "sapl.json")
    if os.path.exists(arq) and not refazer:
        return json.load(open(arq, encoding="utf-8"))
    tipos = tipos_lei(uf)
    normas = []
    for tid in tipos:
        pag = 1
        while True:
            d = api(uf, f"norma/normajuridica/?tipo={tid}&page_size=100&page={pag}")
            normas += d["results"]
            if not d["pagination"].get("next_page"):
                break
            pag += 1
    os.makedirs(pasta, exist_ok=True)
    dados = {"tipos": {str(k): v for k, v in tipos.items()}, "normas": normas}
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False)
    return dados


def cobertura(uf, refazer=False):
    d = indice(uf, refazer)
    por_tipo = collections.defaultdict(lambda: [0, 0])
    for n in d["normas"]:
        t = d["tipos"][str(n["tipo"])]
        por_tipo[t][0] += 1
        por_tipo[t][1] += bool(n.get("texto_integral"))
    anos = [n["ano"] for n in d["normas"] if n.get("texto_integral")]
    print(f"{uf}: {len(d['normas'])} normas; com arquivo: {sum(v[1] for v in por_tipo.values())}"
          f" (anos {min(anos) if anos else '-'}–{max(anos) if anos else '-'})")
    for t, (tot, com) in sorted(por_tipo.items(), key=lambda x: -x[1][0]):
        print(f"   {t}: {tot} ({com} com arquivo)")


def metadados(caminho):
    texto = Path(caminho).read_text(encoding="utf-8")
    if not texto.startswith("---\n") or "\n---\n" not in texto[4:]:
        raise ValueError(f"cabeçalho inválido: {caminho}")
    campos = {}
    for linha in texto[4:].split("\n---\n", 1)[0].splitlines():
        chave, valor = linha.split(":", 1)
        valor = valor.strip()
        campos[chave] = json.loads(valor) if valor.startswith('"') else valor
    return campos


def identidade(uf, n, tipo):
    return {"uf": uf, "tipo": tipo, "numero": str(n.get("numero") or ""),
            "data": n.get("data") or "",
            "fonte": f"https://{HOSTS[uf]}/norma/{n['id']}",
            "arquivo": (n.get("texto_integral") or "").replace("http://", "https://")}


def existentes(uf, pasta, n, tipo):
    """O ID do SAPL identifica a norma mesmo se a descrição do tipo mudar de slug."""
    ano = Path(RAIZ_ESTADUAIS) / uf / pasta / str(n["ano"])
    esperada = identidade(uf, n, tipo)
    encontrados = []
    for caminho in sorted(ano.glob(f"*-id{n['id']}.md")):
        meta = metadados(caminho)
        divergencias = [f"{k}: arquivo={meta.get(k, '')!r}, índice={v!r}"
                        for k, v in esperada.items() if str(meta.get(k, "")) != str(v)]
        if divergencias:
            raise ValueError(f"ID SAPL com identidade divergente: {caminho} ({'; '.join(divergencias)})")
        encontrados.append(caminho)
    return encontrados


def reconciliar(uf, aplicar=False):
    """Remove apenas o alias com preposição de uma emenda da mesma fonte oficial.

    Número, data, UF, tipo, ficha e anexo precisam coincidir com o índice SAPL.
    Os corpos podem diferir por reconversão; o PDF original permanece em _fonte.
    Não funde normas só porque seus corpos são iguais.
    """
    d = indice(uf)
    pares = []
    for n in d["normas"]:
        pasta, tipo = canonico(d["tipos"][str(n["tipo"])])
        if pasta != "emendas-constitucionais":
            continue
        arquivos = existentes(uf, pasta, n, tipo)
        sufixo = f"{n['numero'] or 'sn'}-{n['ano']}-id{n['id']}.md"
        por_nome = {p.name: p for p in arquivos}
        antigo = por_nome.get("emenda-constituicao-" + sufixo)
        alias = por_nome.get("emenda-a-constituicao-" + sufixo)
        if antigo and alias:
            pares.append((antigo, alias))
    registros = []
    for antigo, alias in pares:
        texto_antigo, texto_alias = antigo.read_text(), alias.read_text()
        corpo_antigo = texto_antigo.split("\n---\n", 1)[1]
        corpo_alias = texto_alias.split("\n---\n", 1)[1]
        # A reconversão removeu linhas de preenchimento de assinatura. Só aceitamos
        # essa diferença gráfica; texto novo ou perdido exige revisão manual.
        normalizar = lambda t: re.sub(r"\s+", " ", re.sub(r"(?:\\_){5,}|_{5,}", "", t)).strip()
        if normalizar(corpo_antigo) != normalizar(corpo_alias):
            raise ValueError(f"corpos divergentes exigem revisão manual: {alias}")
        ma, mb = metadados(antigo), metadados(alias)
        if {k: v for k, v in ma.items() if k != "baixado_em"} != {
                k: v for k, v in mb.items() if k != "baixado_em"}:
            raise ValueError(f"metadados divergentes exigem revisão manual: {alias}")
        limpar = corpo_antigo != corpo_alias
        registros.append({"preservado": str(antigo), "removido": str(alias),
                          "identidade": {k: ma[k] for k in ("uf", "tipo", "numero", "data", "fonte", "arquivo")},
                          "sha256_anterior": hashlib.sha256(texto_antigo.encode()).hexdigest(),
                          "sha256_alias": hashlib.sha256(texto_alias.encode()).hexdigest(),
                          "corpo": "limpeza de preenchimento de assinatura" if limpar else "idêntico"})
    if aplicar and registros:
        pasta_relatorio = Path(RAIZ_ESTADUAIS) / uf / "_fonte" / "auditorias"
        pasta_relatorio.mkdir(parents=True, exist_ok=True)
        relatorio = pasta_relatorio / f"sapl-aliases-{dt.datetime.now():%Y%m%d-%H%M%S}.json"
        relatorio.write_text(json.dumps(registros, ensure_ascii=False, indent=2) + "\n")
        print(f"relatório: {relatorio}")
    for antigo, alias in pares:
        print(f"{'remover' if aplicar else 'removeria'} {alias}; preservado {antigo}")
        if aplicar:
            texto = antigo.read_text()
            cab, corpo = texto.split("\n---\n", 1)
            corpo_alias = alias.read_text().split("\n---\n", 1)[1]
            if corpo != corpo_alias:
                antigo.write_text(cab + "\n---\n" + corpo_alias)
            alias.unlink()
    print(f"{uf}: {len(pares)} aliases {'removidos' if aplicar else 'comprovados (simulação)'}")
    return pares


def converter_anexo_sem_omissoes(bruto, url):
    """Preserva números do PDF e retém conteúdo visual sem prova própria."""
    try:
        if bruto.startswith(b"%PDF"):
            conferir_visuais_pdf(bruto)
            corpo, _ = extrair_camada_textual(bruto)
        elif imagem_bruta(bruto):
            return None, "imagem normativa exige OCR e conferência de identidade próprios"
        else:
            html, texto = extrair_texto(bruto, url)
            if html is None:
                return None, "anexo sem HTML verificável; exige extração própria"
            exigir_sem_imagem_omitida(html)
            corpo = html_para_md(html)
        if len(re.sub(r"\W", "", corpo)) < 80:
            return None, "anexo sem texto normativo suficiente"
        if motivo_retencao(corpo):
            return None, motivo_retencao(corpo)
        if avisos_de_omissao(corpo):
            return None, "fonte declara material normativo não reproduzido"
        if remissoes_sem_representacao(corpo):
            return None, "remissão a anexo próprio sem representação identificável"
        return corpo, None
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        return None, str(exc)


def processar_factory(uf, tipos):
    def processar(n):
        bruto = tipos[str(n["tipo"])]
        pasta, tipo = canonico(bruto)
        if pasta == "constituicao" and "CONSTITUIÇÃO FEDERAL" in (n.get("ementa") or "").upper():
            return "fora_escopo", None
        if pasta == "constituicao" and int(n["ano"]) < 1988:
            pasta = "constituicoes-historicas"
        if pasta == "constituicao":
            corrente = os.path.join(RAIZ_ESTADUAIS, uf, "constituicao")
            if any(nome.endswith(".md") for _, _, nomes in os.walk(corrente) for nome in nomes):
                return "pulado", None
        try:
            if existentes(uf, pasta, n, tipo):
                return "pulado", None
        except ValueError as erro:
            # A fonte pode ter corrigido número/data/anexo. Não recriar nem
            # substituir silenciosamente; registrar e deixar a fila continuar.
            return "sem_texto", {"id": n["id"], "motivo": str(erro)}
        # o prefixo do nome do arquivo vem do nome que a Assembleia usa, não do canônico:
        # os arquivos já gravados se chamam lei-ordinaria-N-AAAA-idX.md e precisam ser
        # reconhecidos como existentes numa nova rodada.
        prefixo = re.sub(r"[^a-z0-9]+", "-", bruto.translate(_ACENTOS).lower()).strip("-")
        slug = f"{prefixo}-{n['numero'] or 'sn'}-{n['ano']}-id{n['id']}"
        md, fonte = caminhos(uf, pasta, n["ano"], slug)
        if os.path.exists(md):
            return "pulado", None
        url = n.get("texto_integral")
        if not url:
            return "sem_texto", {"id": n["id"], "norma": n["__str__"], "motivo": "sem arquivo"}
        url = url.replace("http://", "https://")
        st, bruto, _ = rede.get(url)
        if st != 200 or not bruto:
            return "sem_texto", {"id": n["id"], "url": url, "http": st}
        # Guardar também as fontes retidas evita redownload e permite recuperação posterior.
        Path(fonte).parent.mkdir(parents=True, exist_ok=True)
        if Path(fonte).exists():
            try:
                with gzip.open(fonte, "rb") as arquivo:
                    anterior = arquivo.read()
            except (OSError, EOFError):
                anterior = None
            if anterior != bruto:
                divergente = Path(RAIZ_ESTADUAIS) / uf / "_fonte" / "auditorias" / "anexos-divergentes" / (slug + "-" + hashlib.sha256(bruto).hexdigest() + ".gz")
                divergente.parent.mkdir(parents=True, exist_ok=True)
                with gzip.open(divergente, "wb") as arquivo:
                    arquivo.write(bruto)
                return "sem_texto", {"id": n["id"], "url": url,
                                     "motivo": ("cache anterior ilegível; candidato atual preservado separadamente"
                                                if anterior is None else
                                                "cache anterior diverge do anexo atual; ambos preservados"),
                                     "nova_fonte": str(divergente)}
        else:
            with gzip.open(fonte, "wb") as arquivo:
                arquivo.write(bruto)
        corpo, motivo = converter_anexo_sem_omissoes(bruto, url)
        if corpo is None:
            return "sem_texto", {"id": n["id"], "url": url, "motivo": motivo}
        titulo = n["__str__"]
        meta = [
            ("titulo", titulo),
            ("uf", uf),
            ("tipo", tipo),
            ("numero", n.get("numero") or ""),
            ("data", n.get("data") or ""),
            ("ementa", " ".join((n.get("ementa") or "").split())),
            ("publicacao", n.get("veiculo_publicacao") or ""),
            ("revogada", None),
            ("versao_texto", "arquivo anexado ao SAPL; edição e compilação não verificadas"
             if pasta == "constituicao" else "original (arquivo anexado ao SAPL)"),
            ("fonte", f"https://{HOSTS[uf]}/norma/{n['id']}"),
            ("arquivo", url),
        ]
        gravar(md, fonte, bruto, meta, f"# {titulo}\n\n{corpo}")
        return "ok", None

    return processar


if __name__ == "__main__":
    acao, uf = sys.argv[1], sys.argv[2].upper()
    refazer = "--refazer" in sys.argv
    if acao == "indice":
        cobertura(uf, refazer)
    elif acao == "reconciliar":
        reconciliar(uf, "--aplicar" in sys.argv)
    elif acao == "baixar":
        d = indice(uf, refazer)
        itens = sorted(d["normas"], key=lambda n: n.get("data") or "", reverse=True)
        if len(sys.argv) > 3:
            itens = itens[: int(sys.argv[3])]
        executar(uf, itens, processar_factory(uf, d["tipos"]), workers=3)
