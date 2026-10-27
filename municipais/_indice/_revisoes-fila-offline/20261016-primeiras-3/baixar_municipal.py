"""Baixa legislação municipal dos diários oficiais das associações estaduais de municípios.

O direito municipal é a maior lacuna do acervo — 5.570 municípios, nenhum índice nacional. Mas ele
não está espalhado em 5.570 portais: a maioria dos municípios publica no **diário oficial da
associação estadual** a que pertence, e todas essas associações usam a mesma plataforma, reunida
em `diariomunicipal.com.br`. São ~24 diários que, somados, cobrem milhares de municípios — o
equivalente municipal do que o DOU é para a União.

Cada edição é um PDF único com todos os atos do dia, de todos os municípios daquela associação,
na forma:

    ESTADO DO RIO GRANDE DO SUL
    PREFEITURA MUNICIPAL DE SANTA CRUZ DO SUL
    ...
    PROCURADORIA GERAL DO MUNICÍPIO
    LEI Nº 10.574, DE 14 DE OUTUBRO DE 2026.
    <ementa e texto>
    Publicado por:
    <nome>
    Código Identificador:481AA0F1

O `Código Identificador` fecha cada ato e divide a edição; a identidade inclui também a fonte/edição, pois códigos podem reaparecer em dias diferentes. O município
vem do cabeçalho de seção mais recente.

O PDF é reconstruído por coordenadas de palavras e diagramação vetorial: colunas são
lidas da esquerda para a direita, com tabelas e faixas em largura total preservadas.
Layouts ambíguos falham explicitamente. O cache textual é versionado e os documentos
anteriores exigem reconciliação por edição/código, em vez de serem pulados por caminho.

O calendário público permite consultar edições históricas por data. `--de` e `--ate`
consultam esse formulário, preservando cookie e token CSRF, e guardam os resultados para retomar
sem repetir consultas. Também são incluídas as edições extraordinárias do dia.

    python3 -I scripts/baixar_municipal.py              # a edição de hoje de todas as associações
    python3 -I scripts/baixar_municipal.py --listar     # só mostra as associações e o que acharia
    python3 -I scripts/baixar_municipal.py --assoc famurs,amm-mg
"""
import argparse
import datetime as dt
import html
import gzip
import hashlib
from http.cookiejar import CookieJar
import json
from pathlib import Path
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import CANONICO, Limitador, normalizar_chave, slugify, yaml_str  # noqa: E402
from extrair_diario_municipal import VERSAO, caminhos_cache, texto_colunas_cache

CLASSIFICADOR_SHA = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
EXTRACAO_ATUAL = {}

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "municipais"))
PORTAL = "https://www.diariomunicipal.com.br/"
UA = "Mozilla/5.0 (compatible; constituicao-md/1.0)"

UFS = {
    "acre": "AC", "alagoas": "AL", "amapa": "AP", "amazonas": "AM", "bahia": "BA", "ceara": "CE",
    "distrito federal": "DF", "espirito santo": "ES", "goias": "GO", "maranhao": "MA",
    "mato grosso": "MT", "mato grosso do sul": "MS", "minas gerais": "MG", "para": "PA",
    "paraiba": "PB", "parana": "PR", "pernambuco": "PE", "piaui": "PI", "rio de janeiro": "RJ",
    "rio grande do norte": "RN", "rio grande do sul": "RS", "rondonia": "RO", "roraima": "RR",
    "santa catarina": "SC", "sao paulo": "SP", "sergipe": "SE", "tocantins": "TO",
}

# Só o que é norma. A edição municipal é dominada por extrato de contrato, aviso de licitação,
# portaria de nomeação e resultado de concurso — nenhum deles é norma de caráter geral.
TIPOS = [
    (re.compile(r"^LEI\s+COMPLEMENTAR\s+N", re.I), "lei complementar"),
    (re.compile(r"^LEI\s+ORG[ÂA]NICA", re.I), "lei organica"),
    (re.compile(r"^EMENDA\s+[ÀA]\s+LEI\s+ORG[ÂA]NICA", re.I), "emenda a lei organica"),
    (re.compile(r"^LEI\s+(?:(?:MUNICIPAL|ORDIN[ÁA]RIA)\s+)?N", re.I), "lei ordinaria"),
    (re.compile(r"^DECRETO\s+LEGISLATIVO\s+N", re.I), "decreto legislativo"),
    (re.compile(r"^RESOLU[ÇC][ÃA]O\s+N", re.I), "resolucao"),
    (re.compile(r"^DECRETO\s+(?:MUNICIPAL\s+)?N", re.I), "decreto"),
]

CODIGO = re.compile(r"^Código Identificador:\s*(\w+)\s*$", re.M)
# Os cabeçalhos variam por diário: "ESTADO DE MINAS GERAIS", "ESTADO DO RIO GRANDE DO SUL",
# "ESTADO DA BAHIA"; e "PREFEITURA MUNICIPAL DO CARPINA" ao lado de "MUNICÍPIO DE ALEXÂNIA-GO".
# A preposição entra como D[AEO]S? e o nome do estado é validado contra UFS — assim uma linha que
# só começa igual ("ESTADO DE GOIÁS, E A EMPRESA...") não vira cabeçalho.
ENTIDADE = re.compile(r"^(?:PREFEITURA\s+DO\s+MUNIC[ÍI]PIO|PREFEITURA\s+MUNICIPAL|PREFEITURA|MUNIC[ÍI]PIO|C[ÂA]MARA\s+MUNICIPAL"
                      r"|C[ÂA]MARA|GOVERNO\s+MUNICIPAL)\s+D[AEO]S?\s+(.+?)\s*$", re.M)
ESTADO = re.compile(r"^ESTADO\s+D[AEO]S?\s+(.+?)\s*$", re.M)
# "ALEXÂNIA-GO", "SÃO PAULO/SP": a sigla do estado no fim do nome do município
SUFIXO_UF = re.compile(r"\s*[-/]\s*[A-Z]{2}\s*$")
NUMERO = re.compile(r"\bN[.ºo°\s]{0,4}(\d[\d.]*)", re.I)
DATA_EXTENSO = re.compile(r"(\d{1,2})\s+DE\s+([A-ZÀ-Ÿa-zà-ÿ]+)\s+DE\s+(\d{4})", re.I)
DATA_BARRA = re.compile(r"\b(\d{1,4})\s*/\s*(\d{4})\b")
MESES = {m: i + 1 for i, m in enumerate(
    "janeiro fevereiro marco abril maio junho julho agosto setembro outubro novembro dezembro".split())}


def http(url, limite, tentativas=3, timeout=300):
    import time
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*",
                                               "Accept-Encoding": "identity"})
    ultimo = None
    for n in range(tentativas):
        limite.esperar()
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read()
        except Exception as e:
            ultimo = e
            time.sleep(3 * (n + 1) ** 2)
    raise RuntimeError(f"falhou após {tentativas} tentativas: {url}: {ultimo}")


def associacoes(limite):
    """Os diários listados no portal: ('famurs', 'https://…/famurs/')."""
    st, bruto = http(PORTAL, limite, timeout=90)
    pagina = bruto.decode("utf-8", errors="replace")
    vistos, saida = set(), []
    for href in re.findall(r'href="(https://www\.diariomunicipal\.com\.br/([a-z0-9-]+)/)"', pagina):
        url, slug = href
        if slug not in vistos:
            vistos.add(slug)
            saida.append((slug, url))
    return saida


def link_da_edicao(url_assoc, limite):
    """A URL do PDF da edição corrente, que a página da associação expõe."""
    st, bruto = http(url_assoc, limite, timeout=90)
    pagina = bruto.decode("utf-8", errors="replace")
    for href in re.findall(r'href="([^"]*voxtecnologia[^"]*\.pdf[^"]*)"', pagina):
        return html.unescape(href)
    return None


def limites_da_pagina(slug, url, pagina):
    """Só o calendário e o card explicitamente chamado 'ultima-edicao' definem limites."""
    anos = re.search(r'<select[^>]*name="calendar\[year\]"[^>]*>(.*?)</select>', pagina, re.S)
    valores = [int(a) for a in re.findall(r'<option value="(\d{4})"', anos.group(1))] if anos else []
    card = re.search(r'<figure[^>]*id="ultima-edicao"[^>]*>(.*?)</figure>', pagina, re.S)
    ultima = fonte = None
    if card:
        data = re.search(r'<span[^>]*>\s*(\d{2})/(\d{2})/(\d{4})\s*</span>', card.group(1))
        link = re.search(r'<a[^>]*href="([^"]+)"', card.group(1))
        if data:
            try:
                ultima = dt.date(int(data.group(3)), int(data.group(2)), int(data.group(1))).isoformat()
            except ValueError:
                pass
        if link:
            fonte = html.unescape(link.group(1))
    return {"assoc": slug, "fonte": url, "primeiro_ano_calendario": min(valores) if valores else None,
            "ultima_circulacao": ultima, "pdf_ultima_edicao": fonte,
            "evidencia": 'select calendar[year] e figure id="ultima-edicao"',
            "pagina_sha256": hashlib.sha256(pagina.encode()).hexdigest(),
            "consultado_em": dt.date.today().isoformat()}


def guardar_limites(slug, limites):
    destino = os.path.join(RAIZ, "_indice", "_limites", slug + ".json")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino + ".tmp", "w", encoding="utf-8") as f:
        json.dump(limites, f, ensure_ascii=False, indent=2)
    os.replace(destino + ".tmp", destino)


def intervalo_disponivel(slug, inicio, fim, limites):
    """O índice local confirmado nunca é invalidado por um card mais antigo do portal."""
    ano = limites.get("primeiro_ano_calendario")
    ultima = limites.get("ultima_circulacao")
    inicio_disponivel = dt.date(ano, 1, 1) if ano else inicio
    fim_disponivel = dt.date.fromisoformat(ultima) if ultima else fim
    conhecidos = []
    pasta = os.path.join(RAIZ, "_indice", slug)
    if os.path.isdir(pasta):
        for arquivo in os.listdir(pasta):
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}\.json", arquivo):
                continue
            with open(os.path.join(pasta, arquivo), encoding="utf-8") as f:
                edicoes = json.load(f)
            conhecidos.extend(dt.date.fromisoformat(e["data"]) for e in edicoes)
    if conhecidos:
        inicio_disponivel = min(inicio_disponivel, min(conhecidos))
        if max(conhecidos) > fim_disponivel:
            # O card contradiz uma edição efetivamente localizada: o limite superior é incerto.
            fim_disponivel = fim
    return max(inicio, inicio_disponivel), min(fim, fim_disponivel)


def edicoes_historicas(slug, url, inicio, fim, limite, total=None):
    """Consulta o mesmo formulário e os mesmos endpoints usados pelo calendário público."""
    limites_cache = os.path.join(RAIZ, "_indice", "_limites", slug + ".json")
    if os.path.exists(limites_cache):
        with open(limites_cache, encoding="utf-8") as f:
            limites_anteriores = json.load(f)
        if limites_anteriores.get("consultado_em") == dt.date.today().isoformat():
            de, ate = intervalo_disponivel(slug, inicio, fim, limites_anteriores)
            if de > ate:
                print(f"{slug}: intervalo fora dos limites oficiais conhecidos; sem consultas diárias", flush=True)
                return
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
    limite.esperar()
    with opener.open(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=90) as r:
        pagina = r.read().decode("utf-8", errors="replace")
    token = re.search(r'name="calendar\[_token\]"[^>]*value="([^"]+)"', pagina)
    if not token:
        raise RuntimeError("formulário do calendário sem token CSRF")
    limites = limites_da_pagina(slug, url, pagina)
    guardar_limites(slug, limites)
    inicio, fim = intervalo_disponivel(slug, inicio, fim, limites)
    if inicio > fim:
        print(f"{slug}: intervalo fora dos limites oficiais conhecidos; sem consultas diárias", flush=True)
        return
    n_falhas = 0
    dia = inicio
    while dia <= fim:
        cache = os.path.join(RAIZ, "_indice", slug, dia.isoformat() + ".json")
        if os.path.exists(cache):
            with open(cache, encoding="utf-8") as f:
                edicoes = json.load(f)
        else:
            edicoes = []
            consulta_completa = True
            dados = urllib.parse.urlencode({"calendar[day]": dia.day, "calendar[month]": dia.month,
                    "calendar[year]": dia.year, "calendar[_token]": html.unescape(token.group(1))}).encode()
            for sufixo in ("", "/extra"):
                limite.esperar()
                req = urllib.request.Request(url.rstrip("/") + "/materia/calendario" + sufixo,
                                             data=dados, headers={"User-Agent": UA})
                try:
                    with opener.open(req, timeout=90) as r:
                        resultado = json.load(r)
                except Exception as e:
                    resultado = {"error": str(e)}
                if resultado.get("error") or "edicao" not in resultado:
                    consulta_completa = False
                    n_falhas += 1
                    if total is not None:
                        total["erro"] += 1
                    os.makedirs(RAIZ, exist_ok=True)
                    with open(os.path.join(RAIZ, "_calendario_falhas.jsonl"), "a", encoding="utf-8") as f:
                        f.write(json.dumps({"assoc": slug, "data": dia.isoformat(), "endpoint": sufixo,
                                            "resposta": resultado}, ensure_ascii=False) + "\n")
                    continue
                for edicao in resultado["edicao"]:
                    link = resultado["url_arquivos"] + edicao["link_diario"] + ".pdf"
                    edicoes.append({"fonte": link, "data": edicao.get("data_circulacao", dia.isoformat()),
                                    "numero": edicao["numero_edicao"]})
            if consulta_completa:
                os.makedirs(os.path.dirname(cache), exist_ok=True)
                with open(cache + ".tmp", "w", encoding="utf-8") as f:
                    json.dump(edicoes, f, ensure_ascii=False)
                os.replace(cache + ".tmp", cache)
        for edicao in edicoes:
            yield edicao["fonte"], dt.date.fromisoformat(edicao["data"]), edicao["numero"]
        dia += dt.timedelta(days=1)
    if n_falhas:
        print(f"{slug}: {n_falhas} consultas de calendário inconclusivas; ver _calendario_falhas.jsonl", flush=True)


def data_do_link(link):
    m = re.search(r"_(\d{4}-\d{2}-\d{2})_", link)
    return dt.date.fromisoformat(m.group(1)) if m else dt.date.today()


def texto_do_pdf(caminho):
    """Geometria por página, com cache versionado e prova do PDF/texto."""
    global EXTRACAO_ATUAL
    texto = texto_colunas_cache(caminho)
    _, meta = caminhos_cache(caminho)
    EXTRACAO_ATUAL = json.loads(meta.read_text())
    return texto


MUNICIPIOS = {}
IBGE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios?orderBy=nome"


def chaves_municipio(nome):
    nome = re.sub(r"['’‘´ʼ]\s*", "'", nome)
    formas = {nome, nome.replace("'", "")}
    # Grafia expandida dos nomes oficiais D'Oeste encontrada nos próprios diários.
    formas.add(re.sub(r"\bD'OESTE\b", "DO OESTE", nome, flags=re.I))
    return {normalizar_chave(x) for x in formas}


def municipios_ibge():
    """Vocabulário oficial por UF, baixado uma vez e reutilizado nas retomadas."""
    if MUNICIPIOS:
        return MUNICIPIOS
    cache = os.path.join(RAIZ, "_indice", "ibge-municipios.json")
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as f:
            dados = json.load(f)
    else:
        with urllib.request.urlopen(IBGE_URL, timeout=90) as r:
            bruto = r.read()
        if bruto.startswith(b"\x1f\x8b"):
            bruto = gzip.decompress(bruto)
        dados = json.loads(bruto)
        if not isinstance(dados, list) or len(dados) < 5000:
            raise RuntimeError("IBGE não devolveu o cadastro esperado de municípios")
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        with open(cache + ".tmp", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
        os.replace(cache + ".tmp", cache)
    for registro in dados:
        regiao = registro.get("microrregiao")
        uf = regiao["mesorregiao"]["UF"]["sigla"] if regiao else registro["regiao-imediata"]["regiao-intermediaria"]["UF"]["sigla"]
        for chave in chaves_municipio(registro["nome"]):
            nomes = MUNICIPIOS.setdefault(uf, {})
            if chave in nomes and nomes[chave] != registro["nome"].upper():
                raise RuntimeError("alias IBGE ambíguo: " + chave)
            nomes[chave] = registro["nome"].upper()
    return MUNICIPIOS


def municipio_oficial(uf, candidato, prefixo=False):
    nomes = municipios_ibge().get(uf, {})
    chaves = chaves_municipio(SUFIXO_UF.sub("", candidato))
    encontrados = {nomes[c] for c in chaves if c in nomes}
    if len(encontrados) == 1:
        return encontrados.pop()
    chave = max(chaves, key=len)
    if prefixo:
        candidatos = [n for n in nomes if chave.startswith(n + " ")]
        if candidatos:
            return nomes[max(candidatos, key=len)]
    return None


def atos(texto):
    """Divide a edição em atos, carregando a UF e o município da seção corrente."""
    uf = municipio = None
    pos = 0
    for m in CODIGO.finditer(texto):
        bloco = texto[pos:m.start()]
        pos = m.end()
        # Uma citação dentro da própria norma não pode mudar o município da seção.
        titulo, _, inicio = epigrafe(bloco)
        cabecalho = bloco[:inicio] if titulo else bloco
        for e in ESTADO.finditer(cabecalho):
            uf = UFS.get(normalizar_chave(e.group(1))) or uf
        for e in ENTIDADE.finditer(cabecalho):
            candidato = e.group(1)
            proxima = cabecalho[e.end():].lstrip("\n").split("\n", 1)[0].strip()
            nome = municipio_oficial(uf, candidato + " " + proxima) if proxima else None
            municipio = nome or municipio_oficial(uf, candidato, prefixo=True)
        yield uf, municipio, bloco, m.group(1)


def linha_epigrafe(linhas, indice):
    linha = linhas[indice].strip()
    if re.search(r"\bDE(?:\s+\d{1,2}(?:\s+DE)?)?$", linha, re.I) and indice + 1 < len(linhas):
        continuacao = linhas[indice + 1].strip()
        if re.fullmatch(r"(?:\d{1,2}\s+DE\s+)?(?:[A-ZÀ-Ÿa-zà-ÿ]+\s+DE\s+)?\d{4}[.,]?", continuacao, re.I):
            linha += " " + continuacao
    return linha


def epigrafe_contextual(linhas, indice):
    linha=linhas[indice].strip()
    if not re.fullmatch(r"LEI(?:\s+(?:MUNICIPAL|ORDIN[ÁA]RIA|COMPLEMENTAR))?\s+N[.ºo°\s]{0,4}\d[\d.]*/\d{4}(?:[-/][A-Z]+)?[.]?",linha,re.I):
        return False
    anterior="\n".join(linhas[:indice])
    if re.search(r"^\s*(?:PORTARIA|AVISO|CONTRATO|CONSIDERANDO|RESOLVE|Art\.)\b",anterior,re.M|re.I):
        return False
    abertura=" ".join(linhas[indice+1:indice+18])
    return bool(re.search(r"\bsanciono\b",abertura,re.I) and re.search(r"\bArt\.\s*1[º°.]?\b",abertura,re.I))


def epigrafe(bloco):
    """Epígrafe e posição original; repetições próprias podem completar seus metadados."""
    pos = 0
    linhas = bloco.split("\n")
    for indice, bruta in enumerate(linhas):
        linha = linha_epigrafe(linhas, indice)
        if 6 <= len(linha) <= 200 and (e_epigrafe(linha) or epigrafe_contextual(linhas, indice)):
            for padrao, chave in TIPOS:
                if padrao.match(linha):
                    numero = NUMERO.search(linha)
                    if numero and not DATA_EXTENSO.search(linha):
                        for proximo in range(indice + 1, min(indice + 9, len(linhas))):
                            repetida = linha_epigrafe(linhas, proximo)
                            if re.match(r"^(?:Art\.|CONSIDERANDO|RESOLVE|DECRETA|O PREFEITO)\b", repetida, re.I):
                                break
                            outro = NUMERO.search(repetida)
                            if (padrao.match(repetida) and outro
                                    and outro.group(1).replace(".", "") == numero.group(1).replace(".", "")
                                    and DATA_EXTENSO.search(repetida) and e_epigrafe(repetida)):
                                return repetida, chave, pos
                    return linha, chave, pos
        pos += len(bruta) + 1
    return None, None, 0


def cabecalho_normativo_pendente(bloco):
    possivel = re.search(r"^\s*(?:LEI(?:\s+(?:ORDIN[ÁA]RIA|COMPLEMENTAR|MUNICIPAL))?|DECRETO(?:\s+LEGISLATIVO)?|RESOLU[ÇC][ÃA]O|EMENDA\s+[ÀA]\s+LEI)\s+(?:N[.ºo°\s]|\d)", bloco, re.M|re.I)
    return bloco[possivel.start():].splitlines()[0] if possivel else ""


def cobertura_bloco(bloco):
    titulo, _, inicio = epigrafe(bloco)
    cabecalho = bloco[:inicio] if titulo else bloco[:600]
    if re.search(r"^\s*ANEXO(?:\s+[ÚU]NICO|\s+[IVXLC\d]+)?\s*(?:[-–:]|$)", cabecalho, re.M|re.I):
        return "anexo; documento vinculado ao ato principal, sem contagem como nova norma"
    if re.search(r"^\s*EXTRATO\s+DE\s+(?:LEI|DECRETO|RESOLU[ÇC][ÃA]O)\b", cabecalho, re.M|re.I):
        return "extrato; texto integral e anexos externos pendentes de verificação"
    if re.search(r"^\s*(?:ERRATA|RETIFICA[ÇC][ÃA]O)\b", cabecalho, re.M|re.I):
        return "retificação; não substitui a publicação integral do ato"
    return ""


def gravar_referencia(uf, municipio, bloco, codigo, data, fonte, cobertura):
    titulo, tipo, _ = epigrafe(bloco)
    numero = NUMERO.search(titulo or "")
    dados = {"uf":uf,"municipio":municipio,"codigo_identificador":codigo,
             "titulo":titulo,"tipo":tipo,"numero":numero.group(1).replace(".", "") if numero else "",
             "data_publicacao":str(data),"fonte":fonte,"cobertura":cobertura,
             "extrator":VERSAO,"sha256_classificador":CLASSIFICADOR_SHA,"sha256_extrator":EXTRACAO_ATUAL["sha256_extrator"],"sha256_pdf":EXTRACAO_ATUAL["sha256_pdf"],
             "sha256_bloco":hashlib.sha256(bloco.encode()).hexdigest(),"texto":bloco}
    caminho = Path(RAIZ)/"_referencias/diarios"/VERSAO/EXTRACAO_ATUAL["sha256_pdf"]/(codigo+".json")
    caminho.parent.mkdir(parents=True,exist_ok=True)
    temporario=caminho.with_suffix(".json.tmp")
    temporario.write_text(json.dumps(dados,ensure_ascii=False,indent=2))
    temporario.replace(caminho)
    return caminho


def e_epigrafe(linha):
    """Distingue a epígrafe de uma citação à mesma norma no meio de uma frase.

    O texto corrido quebra onde calha, e uma linha pode começar em "Lei Orgânica do Município e
    Constituição Federal, FAZ SABER que" — que casa com o padrão de tipo mas não é epígrafe
    nenhuma. Duas exigências separam uma coisa da outra: a epígrafe municipal é escrita em caixa
    alta, e traz o número da norma. A lei orgânica é a exceção ao número, porque não tem; dela se
    exige, em troca, que a linha seja curta — citação costuma continuar a frase.
    """
    if linha != linha.upper():
        # Certos diários mantêm LEI em caixa alta e escrevem somente a data em caixa mista.
        # A frase deve encerrar na data, para não aceitar citações dentro de portarias.
        if (not re.match(r"^(?:LEI|DECRETO|RESOLUÇÃO)\s+", linha)
                or not NUMERO.search(linha)
                or not DATA_EXTENSO.search(linha)
                or not re.search(r"\b\d{4}[.,\s]*$", linha)):
            return False
    if NUMERO.search(linha) or DATA_BARRA.search(linha):
        return True
    return len(linha) <= 60 and not linha.rstrip().endswith((",", ";", ":", "E", "QUE", "DO", "DE"))


def data_da_epigrafe(linha, ano_padrao):
    m = DATA_EXTENSO.search(linha)
    if m:
        mes = MESES.get(normalizar_chave(m.group(2)))
        if mes:
            return f"{int(m.group(3)):04d}-{mes:02d}-{int(m.group(1)):02d}"
    # "LEI MUNICIPAL Nº 4120/2026": só o ano é afirmado pela fonte
    m = DATA_BARRA.search(linha)
    if m and 1800 <= int(m.group(2)) <= ano_padrao:
        return ""
    return ""


def gravar(uf, municipio, titulo, chave, bloco, codigo, data_edicao, link):
    municipio = municipio_oficial(uf, municipio)
    if not municipio:
        raise RuntimeError("município sem correspondência exata no cadastro IBGE da UF")
    pasta, tipo_nome = CANONICO[chave]
    num = NUMERO.search(titulo)
    numero = num.group(1).replace(".", "") if num else ""
    data = data_da_epigrafe(titulo, data_edicao.year)
    data_na_fonte = ""
    observacao_data = ""
    if data:
        try:
            invalida = dt.date.fromisoformat(data) > data_edicao
        except ValueError:
            invalida = True
        if invalida:
            data_na_fonte = data
            data = ""
            for assinatura in DATA_EXTENSO.finditer(bloco):
                prefixo = bloco[max(0, assinatura.start() - 80):assinatura.start()]
                if assinatura.start() < len(bloco) / 2 or not re.search(r"(?:\bEm|,)\s*$", prefixo, re.I):
                    continue
                candidata = data_da_epigrafe(assinatura.group(0), data_edicao.year)
                try:
                    if candidata and dt.date.fromisoformat(candidata) <= data_edicao:
                        data = candidata
                except ValueError:
                    pass
            observacao_data = "Data da epígrafe posterior à publicação ou inválida; " + (
                "data registrada conforme assinatura no corpo." if data else "data não determinada.")
    ano_citado = re.search(r"/(?:[A-Z.-]+/)*(\d{4})\b", titulo, re.I)
    ano = data[:4] if data else (ano_citado.group(1) if ano_citado else data_na_fonte[:4])
    if not ano:
        raise RuntimeError("ano da norma não determinado na epígrafe; exige revisão da assinatura")
    # o nome do arquivo sai da chave canônica ("lei ordinaria"), não da pasta no plural; e o
    # nome do município perde o acento, para que o caminho seja o mesmo em qualquer sistema
    slug = slugify(f"{slugify(chave)}-{numero or codigo}-{ano}-{codigo}")[:110]
    md = os.path.join(RAIZ, uf, slugify(normalizar_chave(municipio))[:60], pasta, ano, slug + ".md")
    corpo = re.sub(r"\n{3,}", "\n\n", bloco.strip())
    if os.path.exists(md):
        anterior = Path(md).read_text()
        if (f'extrator: "{VERSAO}"' in anterior
                and f'sha256_classificador: {yaml_str(CLASSIFICADOR_SHA)}' in anterior
                and f'sha256_extrator: {yaml_str(EXTRACAO_ATUAL.get("sha256_extrator", ""))}' in anterior
                and f'fonte: {yaml_str(link)}' in anterior
                and f'sha256_pdf: {yaml_str(EXTRACAO_ATUAL.get("sha256_pdf", ""))}' in anterior
                and anterior.split("\n# ",1)[-1].split("\n\n",1)[-1].strip()==corpo.strip()):
            return False
        raise RuntimeError("documento existente exige reconciliação por fonte/edição+código: " + md)
    if not EXTRACAO_ATUAL.get("sha256_pdf"):
        raise RuntimeError("extração sem proveniência verificável do PDF")
    cab = ["---", f"titulo: {yaml_str(titulo)}", f"uf: {yaml_str(uf)}",
           f"municipio: {yaml_str(municipio)}", f"tipo: {yaml_str(tipo_nome)}",
           f"numero: {yaml_str(numero)}", f"data: {data if data else yaml_str('')}", f"ano: {yaml_str(ano)}",
           "revogada: null", 'versao_texto: "publicação original"',
           f"extrator: {yaml_str(VERSAO)}", f"sha256_classificador: {yaml_str(CLASSIFICADOR_SHA)}", f"sha256_extrator: {yaml_str(EXTRACAO_ATUAL['sha256_extrator'])}", f"sha256_pdf: {yaml_str(EXTRACAO_ATUAL['sha256_pdf'])}",
           f"sha256_texto_pdf: {yaml_str(EXTRACAO_ATUAL['sha256_texto'])}",
           f"publicacao: {yaml_str('Diário Oficial de ' + data_edicao.strftime('%d/%m/%Y'))}",
           f"data_publicacao: {data_edicao.isoformat()}",
           f"codigo_identificador: {yaml_str(codigo)}", f"fonte: {yaml_str(link)}",
           f"baixado_em: {dt.date.today().isoformat()}", "---", ""]
    if data_na_fonte:
        cab[-2:-2] = [f"data_na_epigrafe: {yaml_str(data_na_fonte)}",
                      f"observacao_data: {yaml_str(observacao_data)}"]
    os.makedirs(os.path.dirname(md), exist_ok=True)
    tmp = md + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(cab) + f"# {titulo}\n\n" + corpo + "\n")
    os.replace(tmp, md)
    return True


def verificar_edicao_reconciliada(link):
    resultado = subprocess.run(
        ["rtk", "proxy", "rg", "-l", "-F", "--glob", "*.md",
         "fonte: " + yaml_str(link), RAIZ], capture_output=True, text=True)
    if resultado.returncode not in (0, 1):
        raise RuntimeError("não foi possível verificar documentos anteriores da edição")
    for caminho in resultado.stdout.splitlines():
        anterior = Path(caminho).read_text()
        if (f'extrator: "{VERSAO}"' not in anterior
                or f'sha256_classificador: {yaml_str(CLASSIFICADOR_SHA)}' not in anterior
                or f'sha256_extrator: {yaml_str(EXTRACAO_ATUAL.get("sha256_extrator", ""))}' not in anterior
                or f'sha256_pdf: {yaml_str(EXTRACAO_ATUAL["sha256_pdf"])}' not in anterior):
            raise RuntimeError("edição possui versão anterior não reconciliada: " + caminho)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--assoc", default="", help="só estas associações (ex.: famurs,amm-mg)")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--rps", type=float, default=1, help="o portal é lento; uma por segundo basta")
    ap.add_argument("--de", type=dt.date.fromisoformat, help="início do calendário histórico (AAAA-MM-DD)")
    ap.add_argument("--ate", type=dt.date.fromisoformat, help="fim do calendário histórico (AAAA-MM-DD)")
    a = ap.parse_args()
    if not 0 < a.rps <= 4:
        ap.error("--rps deve ser maior que zero e no máximo 4")
    if a.ate and not a.de:
        ap.error("--ate exige --de")
    if a.de and (a.ate or dt.date.today()) < a.de:
        ap.error("--ate deve ser igual ou posterior a --de")

    municipios_ibge()
    limite = Limitador(a.rps)
    alvo = {s.strip() for s in a.assoc.split(",") if s.strip()}
    lista = [(s, u) for s, u in associacoes(limite) if not alvo or s in alvo]
    print(f"{len(lista)} diários: {', '.join(s for s, _ in lista)}", flush=True)
    if a.listar:
        return

    os.makedirs(RAIZ, exist_ok=True)
    falhas_path = os.path.join(RAIZ, "_falhas.jsonl")
    total = {"ok": 0, "pulado": 0, "sem_norma": 0, "referencias_parciais": 0, "sem_edicao": 0, "erro": 0}
    with open(falhas_path, "a", encoding="utf-8") as falhas:
        for slug, url in lista:
            try:
                edicoes = edicoes_historicas(slug, url, a.de or dt.date.today(), a.ate or dt.date.today(), limite, total)
                for link, data_circulacao, numero_edicao in edicoes:
                    try:
                        if not link:
                            total["sem_edicao"] += 1
                            falhas.write(json.dumps({"assoc": slug, "status": "sem_edicao",
                                                     "data": dt.date.today().isoformat()}, ensure_ascii=False) + "\n")
                            print(f"{slug}: sem edição publicada hoje", flush=True)
                            continue
                        data_edicao = data_circulacao or data_do_link(link)
                        pdf = os.path.join(RAIZ, "_fonte", slug, f"{data_edicao.isoformat()}{'-' + slugify(numero_edicao) if numero_edicao else ''}.pdf")
                        if not os.path.exists(pdf):
                            st, dados = http(link, limite)
                            if not dados.startswith(b"%PDF"):
                                raise RuntimeError("a edição não veio como PDF")
                            os.makedirs(os.path.dirname(pdf), exist_ok=True)
                            with open(pdf + ".tmp", "wb") as f:
                                f.write(dados)
                            os.replace(pdf + ".tmp", pdf)

                        n_ok = n_pulado = n_sem = n_ref = 0
                        texto = texto_do_pdf(pdf)
                        verificar_edicao_reconciliada(link)
                        for uf, municipio, bloco, codigo in atos(texto):
                            titulo, chave, inicio = epigrafe(bloco)
                            cobertura = cobertura_bloco(bloco)
                            if cobertura:
                                gravar_referencia(uf,municipio,bloco,codigo,data_edicao,link,cobertura)
                                n_ref += 1
                                continue
                            if not titulo:
                                pendente = cabecalho_normativo_pendente(bloco)
                                if pendente:
                                    raise RuntimeError("cabeçalho normativo não reconhecido, código " + codigo + ": " + pendente)
                                n_sem += 1
                                continue
                            if not uf or not municipio:
                                raise RuntimeError("norma sem cabeçalho municipal confirmado, código " + codigo)
                            if gravar(uf, municipio, titulo, chave, bloco[inicio:], codigo, data_edicao, link):
                                n_ok += 1
                            else:
                                n_pulado += 1
                        total["ok"] += n_ok
                        total["pulado"] += n_pulado
                        total["sem_norma"] += n_sem
                        total["referencias_parciais"] += n_ref
                        print(f"{slug} {data_edicao}: {n_ok} normas novas, {n_pulado} já tinha, "
                              f"{n_sem} atos fora do recorte, {n_ref} referências parciais", flush=True)
                    except Exception as e:
                        total["erro"] += 1
                        falhas.write(json.dumps({"assoc": slug, "fonte": link, "erro": str(e)}, ensure_ascii=False) + "\n")
                        falhas.flush()
                        print(f"{slug}: edição falhou: {str(e)[:120]}", flush=True)
            except Exception as e:
                total["erro"] += 1
                falhas.write(json.dumps({"assoc": slug, "erro": str(e)}, ensure_ascii=False) + "\n")
                falhas.flush()
                print(f"{slug}: calendário falhou: {str(e)[:120]}", flush=True)
    print("FIM PARCIAL" if total["erro"] else "FIM", total, flush=True)
    return 1 if total["erro"] else 0


if __name__ == "__main__":
    sys.exit(main())
