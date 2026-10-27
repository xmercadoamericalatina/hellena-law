"""Baixa os enunciados consolidados dos tribunais superiores e grava um arquivo por enunciado.

Súmula não é lei, mas vincula: a súmula vinculante obriga a administração e o Judiciário (art.
103-A da Constituição), e as demais orientam de tal modo que ignorá-las é perder a causa. Por isso
entram no acervo.

Os temas repetitivos do STJ e as súmulas do TCU vêm dos dados abertos oficiais. As súmulas
do STM vêm dos PDFs individuais de sua biblioteca digital. Para os demais enunciados,
a fonte é o **caderno oficial de cada tribunal** — o PDF consolidado que o próprio tribunal
publica e mantém. É a melhor fonte disponível: traz, além do enunciado, a data de aprovação, o
órgão julgador, a fonte de publicação, a referência legislativa e os precedentes. Os portais de
busca dos tribunais seriam melhores por serem estruturados, mas o do STF carrega por JavaScript e
o do STJ (`scon.stj.jus.br`) devolve 403 a acesso automatizado — que este repositório não contorna.

Cada caderno tem um corte próprio, então há um analisador por tribunal. Todos devolvem pares
(número, texto) e o resto do caminho é igual.

    python3 -I scripts/baixar_jurisprudencia.py              # tudo que falta
    python3 -I scripts/baixar_jurisprudencia.py --refazer

Requer `pdftotext` (poppler), o mesmo que o resto do acervo já usa.
"""
import argparse
import csv
import html
import hashlib
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import Limitador, yaml_str  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "jurisprudencia"))
UA = "Mozilla/5.0 (compatible; constituicao-md/1.0)"


FALHAS = 0


def registrar_falha(fonte, erro, url=""):
    global FALHAS
    FALHAS += 1
    os.makedirs(RAIZ, exist_ok=True)
    with open(os.path.join(RAIZ, "_falhas.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps({"fonte": fonte, "url": url, "erro": str(erro),
                            "data": dt.datetime.now().isoformat()}, ensure_ascii=False) + "\n")
    print(f"{fonte}: falhou: {str(erro)[:160]}", flush=True)


def cortar(texto, cabecalho):
    """Divide o caderno em (número, bloco) a cada linha que é só o cabeçalho de um enunciado.

    O cabeçalho precisa casar a linha inteira: nos sumários do início do PDF a mesma palavra
    aparece com o número da página ao lado ("SÚMULA 320   184   SÚMULA 354   203"), e essas linhas
    não podem virar enunciado.

    `\x0c` entra no espaço admitido à esquerda porque é o caractere de quebra de página que o
    pdftotext emite, e ele fica grudado na primeira linha da página seguinte — que é justamente
    onde um enunciado costuma começar.
    """
    marcas = [(m.start(), m.group(1)) for m in cabecalho.finditer(texto)]
    for i, (pos, numero) in enumerate(marcas):
        fim = marcas[i + 1][0] if i + 1 < len(marcas) else len(texto)
        yield numero, texto[pos:fim]


def limpar(bloco):
    """Tira numeração de página solta e espaço de layout, preservando os parágrafos."""
    linhas = []
    for ln in bloco.split("\n"):
        ln = ln.rstrip()
        if re.fullmatch(r"\s*\d{1,4}\s*", ln):  # número de página isolado
            continue
        if re.fullmatch(r"\s*(SÚMULAS?|Súmulas do Superior Tribunal de Justiça)\s*", ln):
            continue
        linhas.append(re.sub(r"[ \t]{2,}", " ", ln).strip())
    # colapsa linhas em branco repetidas
    saida = re.sub(r"\n{3,}", "\n\n", "\n".join(linhas)).strip()
    return saida


def stf_sumulas(texto):
    return cortar(texto, re.compile(r"^[ \t\x0c]*SÚMULA[ \t]+(\d+)[ \t]*$", re.M))


def stj_sumulas(texto):
    return cortar(texto, re.compile(r"^[ \t\x0c]*Súmula[ \t]+(\d+)[ \t]*$", re.M))


# O caderno do TST termina com um índice remissivo que repete todo enunciado, por assunto, em
# forma abreviada. Sem cortar ali, a remissão do índice concorre com o enunciado de verdade — e às
# vezes vence, porque o trecho do índice vem seguido do próximo verbete e fica mais longo.
INDICE_TST = re.compile(r"^[ \t\x0c]*ÍNDICE REMISSIVO[ \t]*$", re.M)


def ate_o_indice(texto):
    m = INDICE_TST.search(texto)
    return texto[: m.start()] if m else texto


def tst_sumulas(texto):
    return cortar(ate_o_indice(texto), re.compile(r"^[ \t\x0c]*SUM-(\d+)\b", re.M))


def tst_ojs(texto):
    return cortar(ate_o_indice(texto), re.compile(r"^[ \t\x0c]*OJ-([A-Z0-9]+-\d+)\b", re.M))


# (tribunal, pasta, prefixo do arquivo, url do caderno, analisador, tipo, molde do título)
CADERNOS = [
    ("stf", "sumulas", "sumula", "https://www.stf.jus.br/arquivo/cms/jurisprudenciaSumula/anexo/"
     "Enunciados_Sumulas_STF_1_a_736_Completo.pdf", stf_sumulas, "Súmula", "Súmula nº {} do STF"),
    ("stj", "sumulas", "sumula", "https://www.stj.jus.br/docs_internet/SumulasSTJ.pdf",
     stj_sumulas, "Súmula", "Súmula nº {} do STJ"),
    ("tst", "sumulas", "sumula", "https://www.tst.jus.br/documents/10157/63003/Livro-Internet.pdf",
     tst_sumulas, "Súmula", "Súmula nº {} do TST"),
    ("tst", "orientacoes-jurisprudenciais", "oj", "https://www.tst.jus.br/documents/10157/63003/Livro-Internet.pdf",
     tst_ojs, "Orientação Jurisprudencial", "Orientação Jurisprudencial {} do TST"),
]

# As súmulas vinculantes do STF ainda não têm caderno localizado: o portal responde 200 com a
# página genérica para qualquer caminho de PDF, então não há como descobrir a URL por tentativa, e
# a lista em HTML é montada por JavaScript. Ver PROGRESSO.md.

DATA_APROVACAO = re.compile(r"(?:Data de Aprovação|Data da Decisão)\s*\n\s*(?:Sessão Plenária de\s*)?"
                            r"(\d{2})/(\d{2})/(\d{4})", re.I)
# O caderno do TST não tem campo de data: a referência da redação em vigor vem no próprio
# cabeçalho do enunciado ("Res. 174/2011, DEJT divulgado em 27, 30 e 31.05.2011"). A primeira data
# do bloco é a dessa redação — é a data que o acervo registra, e não a da redação original, que
# aparece depois, no histórico.
DATA_TST = re.compile(r"\b(\d{2})\.(\d{2})\.(\d{4})\b")


def cancelada_no_caderno(corpo, tribunal, numero):
    """Somente marcações do próprio verbete, sem propagar cancelamento de precedentes citados."""
    if tribunal == "stf":
        return bool(re.search(r"\(\s*Cancelada\s*\)", corpo.split("Data de Aprovação", 1)[0], re.I))
    if tribunal == "stj":
        enunciado = corpo.split("Órgão Julgador", 1)[0]
        return bool(re.search(r"CANCELAMENTO\s+da\s+Súmula\s+n[.ºo°\s]*" +
                              re.escape(numero) + r"\b", enunciado, re.I))
    if tribunal == "tst":
        return bool(re.search(r"\bcancelad[ao]\b", corpo.split("\n\n", 1)[0], re.I))
    return False


def data_do_enunciado(corpo):
    m = DATA_APROVACAO.search(corpo)
    if m:
        return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    m = DATA_TST.search(corpo)
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else ""


def baixar_pdf(url, destino, limite):
    if os.path.exists(destino):
        return
    limite.esperar()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*",
                                               "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=300) as r:
        dados = r.read()
    if not dados.startswith(b"%PDF"):
        raise RuntimeError(f"a resposta não é PDF ({len(dados)} bytes): {url}")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    tmp = destino + ".tmp"
    with open(tmp, "wb") as f:
        f.write(dados)
    os.replace(tmp, destino)


def texto_do_pdf(caminho):
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as t:
        saida = t.name
    try:
        subprocess.run(["pdftotext", "-layout", caminho, saida], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open(saida, encoding="utf-8", errors="replace") as f:
            return f.read()
    finally:
        os.unlink(saida)


def bnp_stf(limite, refazer=False, tribunal="STF", atualizar_indice=False):
    tribunal = tribunal.upper()
    """Precedentes STF do Banco Nacional de Precedentes do CNJ, com paginação e JSON original."""
    url = "https://pangeabnp.pdpj.jus.br/api/v1/precedentes"
    grupos = [("sumulas-vinculantes", ["SV"]), ("repercussao-geral", ["RG"]),
              ("controle-concentrado", ["ADI", "ADPF", "ADC", "ADO"])]
    if tribunal != "STF":
        grupos = [("uniformizacao", ["PUIL"])] if tribunal == "TNU" else [("sumulas", ["SUM"])]
    tipos = {"SV": "Súmula vinculante", "RG": "Tema de repercussão geral", "ADI": "ADI",
             "ADPF": "ADPF", "ADC": "ADC", "ADO": "ADO", "SUM": "Súmula", "PUIL": "PUIL"}
    cont = {"ok": 0, "pulado": 0}
    for pasta, especies in grupos:
        pagina = 1
        vistos = set()
        while True:
            filtro = {"buscaGeral": "", "todasPalavras": "", "quaisquerPalavras": "", "semPalavras": "",
                      "trechoExato": "", "atualizacaoDesde": "", "atualizacaoAte": "", "cancelados": True,
                      "ordenacao": "Text", "nr": "", "pagina": pagina, "tamanhoPagina": 50,
                      "orgaos": [tribunal], "tipos": especies}
            cache = os.path.join(RAIZ, "_fonte", "bnp", (pasta if tribunal == "STF" else tribunal.lower() + "-" + pasta) + "-todos", f"pagina-{pagina}.json")
            try:
                if os.path.exists(cache) and not refazer and not atualizar_indice:
                    with open(cache, encoding="utf-8") as f:
                        dados = json.load(f)
                else:
                    limite.esperar()
                    req = urllib.request.Request(url, data=json.dumps({"filtro": filtro}).encode(),
                                                 headers={"Content-Type": "application/json", "Accept": "application/json"})
                    with urllib.request.urlopen(req, timeout=90) as r:
                        bruto_resposta = r.read()
                    dados = json.loads(bruto_resposta)
                    if not isinstance(dados.get("resultados"), list) or "total" not in dados:
                        raise RuntimeError("BNP sem esquema de resultados esperado")
                    os.makedirs(os.path.dirname(cache), exist_ok=True)
                    # O índice atualizado não pode apagar a evidência das versões
                    # anteriores nem alterar o corpo de enunciados idênticos.
                    capturas = os.path.join(RAIZ, "_fonte", "bnp-capturas")
                    os.makedirs(capturas, exist_ok=True)
                    brutos = [bruto_resposta]
                    if os.path.exists(cache):
                        with open(cache, "rb") as f:
                            brutos.append(f.read())
                    for bruto in brutos:
                        digest = hashlib.sha256(bruto).hexdigest()
                        captura = os.path.join(capturas, digest + ".json")
                        if not os.path.exists(captura):
                            with open(captura, "xb") as f:
                                f.write(bruto)
                    with open(os.path.join(capturas, "consultas.jsonl"), "a", encoding="utf-8") as f:
                        f.write(json.dumps({"fonte": url, "filtro": filtro, "consultado_em": dt.datetime.now().isoformat(),
                                           "sha256_resposta": hashlib.sha256(bruto_resposta).hexdigest(),
                                           "total_informado": dados["total"]}, ensure_ascii=False) + "\n")
                    with open(cache + ".tmp", "w", encoding="utf-8") as f:
                        json.dump(dados, f, ensure_ascii=False)
                    os.replace(cache + ".tmp", cache)
                if not dados["resultados"]:
                    if len(vistos) < dados["total"]:
                        raise RuntimeError("BNP encerrou paginação antes do total informado")
                    break
                for registro in dados["resultados"]:
                    if registro["orgao"] != tribunal or registro["tipo"] not in especies:
                        raise RuntimeError("BNP retornou registro fora do filtro")
                    if registro["id"] in vistos:
                        raise RuntimeError("BNP repetiu registro entre páginas")
                    vistos.add(registro["id"])
                    numero, tipo = str(registro["nr"]), registro["tipo"]
                    if not numero.isdigit():
                        raise RuntimeError("BNP sem número válido")
                    prefixo = "sumula-vinculante" if tipo == "SV" else ("tema" if tipo == "RG" else ("sumula" if tipo == "SUM" else tipo.lower()))
                    destino = os.path.join(RAIZ, "stf", pasta, f"{prefixo}-{numero}.md") if tribunal == "STF" else (
                        os.path.join(RAIZ, "tnu", pasta, f"{prefixo}-{numero}.md") if tribunal == "TNU" else
                        os.path.join(RAIZ, "outros-tribunais", tribunal.lower(), f"{prefixo}-{numero}.md"))
                    versoes_anteriores = []
                    if os.path.exists(destino):
                        with open(destino, encoding="utf-8") as f:
                            anterior = f.read()
                        versoes_anteriores = [json.loads(t) for t in re.findall(r"```json\n(.*?)\n```", anterior, re.S)]
                        if not refazer:
                            if registro in versoes_anteriores:
                                cont["pulado"] += 1
                            else:
                                adicional = "\n## Outra versão oficial capturada pelo CNJ\n\n```json\n" + json.dumps(
                                    registro, ensure_ascii=False, indent=2) + "\n```\n"
                                with open(destino + ".tmp", "w", encoding="utf-8") as f:
                                    f.write(anterior + adicional)
                                os.replace(destino + ".tmp", destino)
                                cont["ok"] += 1
                            continue
                    titulo = f"{tipos[tipo]} nº {numero} do {tribunal}"
                    cab = ["---", f"titulo: {yaml_str(titulo)}", f"tribunal: {yaml_str(tribunal)}",
                           f"tipo: {yaml_str(tipos[tipo])}", f"numero: {yaml_str(numero)}", "data:",
                           f"situacao: {yaml_str(registro.get('situacao', ''))}",
                           f"id_bnp: {yaml_str(registro['id'])}",
                           f"atualizacao_fonte: {yaml_str(registro.get('ultimaAtualizacao', ''))}",
                           'versao_texto: "Banco Nacional de Precedentes do CNJ"', f"fonte: {yaml_str(url)}",
                           f"baixado_em: {dt.date.today().isoformat()}", "---", "", f"# {titulo}", ""]
                    for campo, titulo_campo in [("questao", "Questão"), ("tese", "Tese"), ("situacao", "Situação")]:
                        if registro.get(campo):
                            cab.extend([f"## {titulo_campo}", "", registro[campo], ""])
                    cab.extend(["## Registro original do CNJ", "", "```json",
                                json.dumps(registro, ensure_ascii=False, indent=2), "```", ""])
                    for anterior in versoes_anteriores:
                        if anterior != registro:
                            cab.extend(["## Outra versão oficial capturada pelo CNJ", "", "```json",
                                        json.dumps(anterior, ensure_ascii=False, indent=2), "```", ""])
                    os.makedirs(os.path.dirname(destino), exist_ok=True)
                    with open(destino + ".tmp", "w", encoding="utf-8") as f:
                        f.write("\n".join(cab))
                    os.replace(destino + ".tmp", destino)
                    cont["ok"] += 1
                print(f"bnp/{tribunal.lower()}/{pasta}: {len(vistos)}/{dados['total']} registros", flush=True)
                if len(vistos) >= dados["total"]:
                    break
                pagina += 1
            except Exception as e:
                registrar_falha(f"bnp/{tribunal.lower()}/{pasta}/pagina-{pagina}", e, url)
                break
    return cont


def tnu_sumulas(limite, refazer=False):
    url = "https://www.cjf.jus.br/cjf/corregedoria-da-justica-federal/turma-nacional-de-uniformizacao/publicacoes-1/comentarios-as-sumulas-da-turma-nacional-de-uniformizacao.pdf"
    pdf = os.path.join(RAIZ, "_fonte", "tnu", "sumulas-edicao-2016.pdf")
    baixar_pdf(url, pdf, limite)
    texto = texto_do_pdf(pdf)
    # A seção inicial contém os enunciados; os comentários autorais ficam fora do acervo.
    secao = texto.split("SÚMULAS DA TNU", 1)[1].split("COMENTÁRIOS ÀS SÚMULAS", 1)[0]
    secao = re.sub(r"\f[ \t]*\d+[ \t]*\n", "\n", secao)
    itens = list(re.finditer(r"(?m)^Súmula (\d+)\s*$", secao))
    if [int(m.group(1)) for m in itens] != list(range(1, 84)):
        raise RuntimeError("seção histórica TNU não contém exatamente os enunciados 1 a 83")
    cont = {"ok": 0, "pulado": 0}
    for i, m in enumerate(itens):
        numero = m.group(1)
        corpo = limpar(secao[m.end():itens[i + 1].start() if i + 1 < len(itens) else len(secao)])
        destino = os.path.join(RAIZ, "tnu", "sumulas", f"sumula-{numero}.md")
        if os.path.exists(destino) and not refazer:
            cont["pulado"] += 1
            continue
        titulo = f"Súmula nº {numero} da TNU"
        cab = ["---", f"titulo: {yaml_str(titulo)}", 'tribunal: "TNU"', 'tipo: "Súmula"',
               f"numero: {yaml_str(numero)}", 'data:',
               'versao_texto: "enunciado reproduzido na edição histórica CJF de 2016"',
               'situacao: "situação atual não verificada; texto histórico de 2016"',
               f"fonte: {yaml_str(url)}", f"baixado_em: {dt.date.today().isoformat()}"]
        if re.search(r"[Cc]ancelad[ao]", corpo):
            cab.append('revogada: true')
        cab.extend(["---", "", f"# {titulo}", "", corpo, ""])
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino + ".tmp", "w", encoding="utf-8") as f:
            f.write("\n".join(cab))
        os.replace(destino + ".tmp", destino)
        cont["ok"] += 1
    print("tnu/sumulas (edição 2016):", cont, flush=True)
    return cont


def tnu_sumulas_complementares(limite, refazer=False):
    pasta = os.path.join(RAIZ, "_fonte", "tnu")
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados", "tnu-sumulas-manual2026.json"), encoding="utf-8") as f:
        dados = json.load(f)
    pdf = os.path.join(pasta, "manual-admissibilidade-recursal.pdf")
    baixar_pdf(dados["fonte"], pdf, limite)
    with open(pdf, "rb") as f:
        if hashlib.sha256(f.read()).hexdigest() != dados["sha256"]:
            raise RuntimeError("PDF CJF mudou; transcrição manual precisa ser novamente conferida")
    if [n["numero"] for n in dados["sumulas"]] != list(range(84, 90)):
        raise RuntimeError("complemento TNU sem sequência 84–89")
    cont = {"ok": 0, "pulado": 0}
    for n in dados["sumulas"]:
        destino = os.path.join(RAIZ, "tnu", "sumulas", f"sumula-{n['numero']}.md")
        if os.path.exists(destino) and not refazer:
            cont["pulado"] += 1
            continue
        titulo = f"Súmula nº {n['numero']} da TNU"
        meta = {"titulo": titulo, "tribunal": "TNU", "tipo": "Súmula", "numero": str(n["numero"]),
                "data": n.get("data", ""), "data_publicacao": n["data_publicacao"],
                "versao_texto": "enunciado no Manual de Admissibilidade Recursal TNU, 11ª edição, junho de 2026",
                "fonte": dados["fonte"], "pagina_pdf": str(n["pagina_pdf"]),
                "baixado_em": dt.date.today().isoformat()}
        if n.get("data_cancelamento"):
            meta["data_cancelamento"] = n["data_cancelamento"]
        cab = ["---"] + [f"{k}: {yaml_str(v)}" for k, v in meta.items()]
        if n.get("data_cancelamento"):
            cab.append("revogada: true")
        cab.extend(["---", "", f"# {titulo}", "", n["texto"], ""])
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino + ".tmp", "w", encoding="utf-8") as f:
            f.write("\n".join(cab))
        os.replace(destino + ".tmp", destino)
        cont["ok"] += 1
    print("tnu/sumulas (complemento 2026):", cont, flush=True)
    return cont


def regimentos(limite, refazer=False):
    fontes = [
        ("tst", "Tribunal Superior do Trabalho", "2017-11-20",
         "https://juslaboris.tst.jus.br/bitstream/handle/20.500.12178/116169/2017_ra1937_ri_tst_livro_vigente.pdf?sequence=22&isAllowed=y",
         "Última alteração: Emenda Regimental n. 11, de 20 de maio de 2026."),
        ("tcu", "Tribunal de Contas da União", "2011-11-30",
         "https://portal.tcu.gov.br/uploads/RITCU_2025_a6a18744fc.pdf", "Edição consolidada de 2025."),
    ]
    cont = {"ok": 0, "pulado": 0}
    for slug, nome, data, url, versao in fontes:
        destino = os.path.join(RAIZ, "regimentos", f"regimento-{slug}.md")
        if os.path.exists(destino) and not refazer:
            cont["pulado"] += 1
            continue
        try:
            pdf = os.path.join(RAIZ, "_fonte", "regimentos", f"regimento-{slug}.pdf")
            baixar_pdf(url, pdf, limite)
            corpo = limpar(texto_do_pdf(pdf))
            if len(corpo) < 10000 or "REGIMENTO" not in corpo.upper():
                raise RuntimeError("PDF sem regimento completo reconhecível")
            titulo = f"Regimento Interno do {nome}"
            cab = ["---", f"titulo: {yaml_str(titulo)}", f"tribunal: {yaml_str(slug.upper())}",
                   'tipo: "Regimento interno"', 'numero: ""', f"data: {data}", 'revogada: false',
                   f"versao_texto: {yaml_str(versao)}", f"fonte: {yaml_str(url)}",
                   f"baixado_em: {dt.date.today().isoformat()}", "---", "", f"# {titulo}", "", corpo, ""]
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            with open(destino + ".tmp", "w", encoding="utf-8") as f:
                f.write("\n".join(cab))
            os.replace(destino + ".tmp", destino)
            cont["ok"] += 1
        except Exception as e:
            registrar_falha(f"regimento/{slug}", e, url)
    print("regimentos:", cont, flush=True)
    return cont


def stm_sumulas(limite, refazer=False):
    base = "https://dspace.stm.jus.br"
    links = {}
    for offset in (0,):
        url = base + "/handle/123456789/247/browse?type=title"
        indice = os.path.join(RAIZ, "_fonte", "stm", "indice.html")
        if os.path.exists(indice) and not refazer:
            with open(indice, encoding="utf-8") as f:
                pagina = f.read()
        else:
            limite.esperar()
            with urllib.request.urlopen(url, timeout=90) as r:
                pagina = r.read().decode("utf-8", errors="replace")
            os.makedirs(os.path.dirname(indice), exist_ok=True)
            with open(indice, "w", encoding="utf-8") as f:
                f.write(pagina)
        for href in re.findall(r'href="([^"]*bitstream[^"]+)"', pagina):
            href = html.unescape(href)
            nome = urllib.parse.unquote(href)
            m = re.search(r"Súmula\s+n[°º]\s*(\d+)", nome, re.I)
            if m:
                links[m.group(1)] = base + href
    if not links:
        raise RuntimeError("coleção STM sem PDFs de súmulas")
    cont = {"ok": 0, "pulado": 0}
    for numero, url in links.items():
        destino = os.path.join(RAIZ, "outros-tribunais", "stm", f"sumula-{numero}.md")
        if os.path.exists(destino) and not refazer:
            cont["pulado"] += 1
            continue
        pdf = os.path.join(RAIZ, "_fonte", "stm", f"sumula-{numero}.pdf")
        try:
            baixar_pdf(url, pdf, limite)
        except Exception as e:
            registrar_falha(f"stm/sumula-{numero}", e, url)
            continue
        corpo = limpar(texto_do_pdf(pdf))
        if len(corpo) < 50:
            raise RuntimeError(f"PDF STM {numero} sem texto suficiente")
        cancelada = bool(re.search(r"S[ÚU]MULA[^\n]*Cancelada", corpo, re.I))
        titulo = f"Súmula nº {numero} do STM"
        cab = ["---", f"titulo: {yaml_str(titulo)}", 'tribunal: "STM"', 'tipo: "Súmula"',
               f"numero: {yaml_str(numero)}", "data:",
               f"revogada: {'true' if cancelada else 'false'}",
               'versao_texto: "publicação do tribunal"', f"fonte: {yaml_str(url)}",
               f"baixado_em: {dt.date.today().isoformat()}", "---", "", f"# {titulo}", "", corpo, ""]
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino + ".tmp", "w", encoding="utf-8") as f:
            f.write("\n".join(cab))
        os.replace(destino + ".tmp", destino)
        cont["ok"] += 1
    print("outros-tribunais/stm:", cont, flush=True)
    return cont


def tcu_sumulas(limite, refazer=False):
    url = "https://sites.tcu.gov.br/dados-abertos/jurisprudencia/arquivos/sumula/sumula.csv"
    cache = os.path.join(RAIZ, "_fonte", "tcu", "sumula.csv")
    if not os.path.exists(cache) or refazer:
        limite.esperar()
        with urllib.request.urlopen(url, timeout=120) as r:
            dados = r.read()
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        with open(cache + ".tmp", "wb") as f:
            f.write(dados)
        os.replace(cache + ".tmp", cache)
    with open(cache, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f, delimiter="|"))
    if not linhas or "ENUNCIADO" not in linhas[0]:
        raise RuntimeError("CSV de súmulas do TCU sem esquema esperado")
    grupos = {}
    for linha in linhas:
        if not linha["NUMERO"].isdigit():
            raise RuntimeError("Súmula TCU sem número válido")
        grupos.setdefault(linha["NUMERO"], []).append(linha)
    cont = {"ok": 0, "pulado": 0}
    for numero, historico in grupos.items():
        destino = os.path.join(RAIZ, "outros-tribunais", "tcu", f"sumula-{numero}.md")
        if os.path.exists(destino) and not refazer:
            cont["pulado"] += 1
            continue
        historico.sort(key=lambda r: dt.datetime.strptime(r["DATASESSAOFORMATADA"], "%d/%m/%Y"), reverse=True)
        atual = historico[0]
        data = dt.datetime.strptime(atual["DATASESSAOFORMATADA"], "%d/%m/%Y").date().isoformat()
        titulo = f"Súmula nº {numero} do TCU"
        cab = ["---", f"titulo: {yaml_str(titulo)}", 'tribunal: "TCU"', 'tipo: "Súmula"',
               f"numero: {yaml_str(numero)}", f"data: {data}",
               f"revogada: {'true' if atual['VIGENTE'] == 'false' else 'false'}",
               'versao_texto: "dados abertos do tribunal"', f"fonte: {yaml_str(url)}",
               f"baixado_em: {dt.date.today().isoformat()}", "---", "", f"# {titulo}", ""]
        for registro in historico:
            cab.extend(["## Registro " + registro["KEY"], ""])
            for campo, valor in registro.items():
                if valor:
                    valor = re.sub(r"</(?:p|div|li)>|<br\s*/?>", "\n\n", valor, flags=re.I)
                    valor = html.unescape(re.sub(r"<[^>]+>", "", valor)).strip()
                    cab.extend([f"### {campo}", "", valor, ""])
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino + ".tmp", "w", encoding="utf-8") as f:
            f.write("\n".join(cab))
        os.replace(destino + ".tmp", destino)
        cont["ok"] += 1
    print("outros-tribunais/tcu:", cont, flush=True)
    return cont


def stj_repetitivos(limite, refazer=False):
    """Temas do conjunto oficial CKAN; inclui a situação para distinguir teses e afetações."""
    catalogo = "https://dadosabertos.web.stj.jus.br/api/3/action/package_show?id=precedentes-qualificados"
    cache = os.path.join(RAIZ, "_fonte", "stj", "Temas.csv")
    meta = cache + ".json"
    if not os.path.exists(cache) or refazer:
        limite.esperar()
        with urllib.request.urlopen(catalogo, timeout=90) as r:
            pacote = json.load(r)
        recurso = next(r for r in pacote["result"]["resources"] if r["name"].lower() == "temas.csv")
        limite.esperar()
        with urllib.request.urlopen(recurso["url"], timeout=120) as r:
            dados = r.read()
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        with open(cache + ".tmp", "wb") as f:
            f.write(dados)
        os.replace(cache + ".tmp", cache)
        with open(meta, "w", encoding="utf-8") as f:
            json.dump(recurso, f, ensure_ascii=False)
    with open(meta, encoding="utf-8") as f:
        recurso = json.load(f)
    with open(cache, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f))
    if not linhas or "tipoPrecedente" not in linhas[0]:
        raise RuntimeError("CSV de temas sem esquema esperado")
    cont = {"ok": 0, "pulado": 0}
    grupos = {}
    for linha in linhas:
        if linha["tipoPrecedente"] == "Tema":
            grupos.setdefault(linha["numeroPrecedente"], []).append(linha)
    for numero, historico in grupos.items():
        historico.sort(key=lambda r: (r["dataJulgamento"], int(r["sequencialPrecedente"])), reverse=True)
        linha = historico[0]
        numero = linha["numeroPrecedente"]
        if not numero.isdigit():
            raise RuntimeError("Tema sem número válido")
        destino = os.path.join(RAIZ, "stj", "repetitivos", f"tema-{numero}.md")
        if os.path.exists(destino) and not refazer:
            cont["pulado"] += 1
            continue
        titulo = f"Tema repetitivo nº {numero} do STJ"
        cab = ["---", f"titulo: {yaml_str(titulo)}", 'tribunal: "STJ"',
               'tipo: "Tema repetitivo"', f"numero: {yaml_str(numero)}",
               f"data: {linha['dataJulgamento']}", f"situacao: {yaml_str(linha['situacao'])}",
               f"sequencial_precedente: {yaml_str(linha['sequencialPrecedente'])}",
               'versao_texto: "dados abertos do tribunal"', f"fonte: {yaml_str(recurso['url'])}",
               f"fonte_atualizada_em: {yaml_str(recurso['last_modified'])}",
               f"baixado_em: {dt.date.today().isoformat()}", "---", "", f"# {titulo}", ""]
        # Todos os campos não vazios são preservados; nenhuma data de afetação vira julgamento.
        for registro in historico:
            cab.extend(["## Registro " + registro["sequencialPrecedente"], ""])
            for campo, valor in registro.items():
                if valor:
                    cab.extend([f"### {campo}", "", valor.strip(), ""])
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino + ".tmp", "w", encoding="utf-8") as f:
            f.write("\n".join(cab))
        os.replace(destino + ".tmp", destino)
        cont["ok"] += 1
    print("stj/repetitivos:", cont, flush=True)
    return cont


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refazer", action="store_true")
    ap.add_argument("--atualizar-indice", action="store_true", help="atualiza páginas BNP, preserva capturas e acrescenta somente registros/versões novos")
    ap.add_argument("--rps", type=float, default=1)
    ap.add_argument("--somente", choices=["cadernos", "stj-repetitivos", "tcu-sumulas", "stm-sumulas", "tnu-sumulas", "regimentos", "bnp-stf", "bnp-outros"], help="limita a coleta à fonte indicada")
    a = ap.parse_args()
    if not 0 < a.rps <= 4:
        ap.error("--rps deve ser maior que zero e no máximo 4")
    limite = Limitador(a.rps)
    cont = {"ok": 0, "pulado": 0}

    if a.somente in (None, "stj-repetitivos"):
        try:
            resultado = stj_repetitivos(limite, a.refazer)
            for chave in cont:
                cont[chave] += resultado[chave]
        except Exception as e:
            registrar_falha("stj/repetitivos", e)
    if a.somente in (None, "tcu-sumulas"):
        try:
            resultado = tcu_sumulas(limite, a.refazer)
            for chave in cont:
                cont[chave] += resultado[chave]
        except Exception as e:
            registrar_falha("tcu/sumulas", e)
    if a.somente in (None, "stm-sumulas"):
        try:
            resultado = stm_sumulas(limite, a.refazer)
            for chave in cont:
                cont[chave] += resultado[chave]
        except Exception as e:
            registrar_falha("stm/sumulas", e)
    if a.somente in (None, "tnu-sumulas"):
        try:
            resultado = tnu_sumulas(limite, a.refazer)
            for chave in cont:
                cont[chave] += resultado[chave]
            resultado = tnu_sumulas_complementares(limite, a.refazer)
            for chave in cont:
                cont[chave] += resultado[chave]
        except Exception as e:
            registrar_falha("tnu/sumulas", e)
    if a.somente in (None, "regimentos"):
        resultado = regimentos(limite, a.refazer)
        for chave in cont:
            cont[chave] += resultado[chave]
    if a.somente in (None, "bnp-stf"):
        resultado = bnp_stf(limite, a.refazer, atualizar_indice=a.atualizar_indice)
        for chave in cont:
            cont[chave] += resultado[chave]
    if a.somente in (None, "bnp-outros"):
        for tribunal in ("TNU", "TSE", "STM"):
            resultado = bnp_stf(limite, a.refazer, tribunal, atualizar_indice=a.atualizar_indice)
            for chave in cont:
                cont[chave] += resultado[chave]
    for tribunal, pasta, prefixo, url, analisar, tipo, molde in CADERNOS if a.somente in (None, "cadernos") else []:
        pdf = os.path.join(RAIZ, "_fonte", tribunal, os.path.basename(url.split("?")[0]))
        try:
            baixar_pdf(url, pdf, limite)
        except Exception as e:
            registrar_falha(f"{tribunal}/{pasta}", e, url)
            continue
        texto = texto_do_pdf(pdf)

        # o mesmo número aparece mais de uma vez no caderno — no sumário por assunto e no corpo.
        # Fica o bloco mais longo, que é sempre o do enunciado de verdade; os outros são remissões.
        melhor = {}
        for numero, bloco in analisar(texto):
            if len(bloco) > len(melhor.get(numero, "")):
                melhor[numero] = bloco

        n_ok = n_pulado = 0
        for numero, bloco in sorted(melhor.items(), key=lambda x: (len(x[0]), x[0])):
            slug = f"{prefixo}-{numero.lower()}"
            md = os.path.join(RAIZ, tribunal, pasta, slug + ".md")
            if os.path.exists(md) and not a.refazer:
                n_pulado += 1
                continue
            corpo = limpar(bloco)
            titulo = molde.format(numero)
            data = data_do_enunciado(corpo)
            cab = ["---", f"titulo: {yaml_str(titulo)}", f"tribunal: {yaml_str(tribunal.upper())}",
                   f"tipo: {yaml_str(tipo)}", f"numero: {yaml_str(numero)}", f"data: {data}",
                   f"revogada: {'true' if cancelada_no_caderno(corpo, tribunal, numero) else 'false'}", 'versao_texto: "caderno consolidado do tribunal"',
                   f"fonte: {yaml_str(url)}", f"baixado_em: {dt.date.today().isoformat()}", "---", ""]
            os.makedirs(os.path.dirname(md), exist_ok=True)
            tmp = md + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                f.write("\n".join(cab) + f"# {titulo}\n\n" + corpo + "\n")
            os.replace(tmp, md)
            n_ok += 1
        cont["ok"] += n_ok
        cont["pulado"] += n_pulado
        print(f"{tribunal}/{pasta}: {n_ok} gravados, {n_pulado} já existiam", flush=True)
    cont["erro"] = FALHAS
    print("FIM PARCIAL" if FALHAS else "FIM", cont, flush=True)
    return 1 if FALHAS else 0


if __name__ == "__main__":
    sys.exit(main())
