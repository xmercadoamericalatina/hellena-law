"""Baixa atos infralegais federais do Diário Oficial da União e grava em `reguladores/`.

Por que o DOU e não um raspador por órgão: todo ato infralegal federal com efeito externo —
resolução do CONTRAN, RDC da ANVISA, instrução normativa da Receita, resolução do CMN, portaria do
Ministério da Saúde — nasce publicado no DOU. Um portal por órgão significaria sessenta raspadores,
cada um com seu formato e sua instabilidade; o DOU é uma fonte só, estável e aberta, e já traz o
tipo do ato (`artType`) e a cadeia do órgão emissor (`hierarchyList`) prontos para classificar.

A LexML seria o índice ideal, por já normalizar a URN, mas está atrás de um desafio anti-bot do
Senado — e este repositório não contorna bloqueio de acesso automatizado.

Como funciona: `leiturajornal?data=DD-MM-AAAA&secao=do1` devolve, num `<script id="params">`, o
JSON de todos os atos publicados naquele dia. Para cada ato do tipo que interessa, busca-se o texto
integral em `/web/dou/-/<urlTitle>`.

O que entra: só a Seção 1, que é a dos atos normativos. A Seção 2 é pessoal (nomeações,
exonerações) e a 3 é licitação e contrato — nenhuma das duas é norma. Dentro da Seção 1, só os
tipos de TIPOS_NORMATIVOS: despacho, decisão, pauta de julgamento e extrato de ata ficam de fora
pelo mesmo motivo.

    python3 -I scripts/baixar_dou.py --de 2026-01-01 --ate 2026-10-15
    python3 -I scripts/baixar_dou.py --de 2024-01-01 --ate 2024-12-31 --orgaos anvisa,contran
    python3 -I scripts/baixar_dou.py --de 2026-10-01 --ate 2026-10-15 --listar   # só conta

O texto online do DOU começa em 2002; antes disso a Imprensa Nacional só tem a imagem digitalizada
da edição, que é outro problema (ver as pendências de OCR no README).
"""
import argparse
import datetime as dt
import gzip
import hashlib
import json
import os
import re
import sys
import threading
import urllib.error
import urllib.request
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import CANONICO, Limitador, normalizar_chave, slugify, yaml_str  # noqa: E402
from datas import data_do_texto  # noqa: E402
from html2md import convert  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reguladores"))
DIA = "https://www.in.gov.br/leiturajornal?data={}&secao=do1"
ATO = "https://www.in.gov.br/web/dou/-/{}"
UA = "Mozilla/5.0 (compatible; constituicao-md/1.0)"
ACESSO_RECUSADO = threading.Event()


class AcessoHTTPRecusado(RuntimeError):
    pass

# Tipos de ato (campo artType) que são norma. O DOU publica muito que não é: despacho, decisão em
# processo, pauta de julgamento, extrato de ata, aviso, edital. Esses não entram.
TIPOS_NORMATIVOS = {
    "resolução": "resolucao",
    "resolução normativa": "resolucao normativa",
    "resolução de diretoria colegiada": "resolucao da diretoria colegiada",
    "portaria": "portaria",
    "portaria normativa": "portaria",
    "instrução normativa": "instrucao normativa",
    "deliberação": "deliberacao",
    "circular": "circular",
    "provimento": "provimento",
    "parecer normativo": "parecer normativo",
    "súmula": "sumula",
    "decreto": "decreto",
    "solução de consulta": "solucao de consulta",
    "ato normativo": "ato normativo",
    "recomendação": "recomendacao",
}

# Órgãos que têm identidade normativa própria e merecem pasta própria, mesmo aparecendo sob um
# ministério na hierarquia do DOU. A chave casa por substring, sem acento e em minúsculas, contra
# qualquer nível de `hierarchyList` — do mais específico para o mais geral.
ORGAOS = {
    "agencia nacional de vigilancia sanitaria": "anvisa",
    "agencia nacional de energia eletrica": "aneel",
    "agencia nacional do petroleo": "anp",
    "agencia nacional de telecomunicacoes": "anatel",
    "agencia nacional de saude suplementar": "ans",
    "agencia nacional de aviacao civil": "anac",
    "agencia nacional de transportes terrestres": "antt",
    "agencia nacional de transportes aquaviarios": "antaq",
    "agencia nacional de aguas": "ana",
    "agencia nacional do cinema": "ancine",
    "agencia nacional de mineracao": "anm",
    "agencia brasileira de promocao internacional do turismo": "turismo",
    "embratur": "turismo",
    "agencia nacional de telecomunicac": "anatel",
    "banco central do brasil": "bcb",
    "conselho monetario nacional": "bcb",
    "comissao de valores mobiliarios": "cvm",
    "superintendencia de seguros privados": "susep",
    "superintendencia nacional de previdencia complementar": "previc",
    "secretaria especial da receita federal": "rfb",
    "receita federal do brasil": "rfb",
    "procuradoria geral da fazenda nacional": "pgfn",
    "secretaria do tesouro nacional": "stn",
    "conselho administrativo de recursos fiscais": "carf",
    "conselho nacional de politica fazendaria": "confaz",
    "instituto brasileiro do meio ambiente": "ibama",
    "instituto chico mendes": "icmbio",
    "conselho nacional do meio ambiente": "conama",
    "conselho nacional de transito": "contran",
    "secretaria nacional de transito": "senatran",
    "departamento nacional de transito": "senatran",
    "instituto nacional do seguro social": "inss",
    "instituto nacional de metrologia": "inmetro",
    "conselho nacional de saude": "cns",
    "conselho nacional de educacao": "cne",
    "instituto nacional de estudos e pesquisas": "inep",
    "coordenacao de aperfeicoamento de pessoal": "capes",
    "instituto do patrimonio historico": "iphan",
    "conselho administrativo de defesa economica": "cade",
    "conselho de controle de atividades financeiras": "coaf",
    "controladoria geral da uniao": "cgu",
    "servico florestal brasileiro": "sfb",
    "conselho nacional do ministerio publico": "cnmp",
    "tribunal de contas da uniao": "tcu",
    "defensoria publica da uniao": "dpu",
    "ministerio publico da uniao": "mpu",
    "conselho federal de contabilidade": "cfc",
    "conselho federal de medicina": "conselhos-profissionais",
    "conselho federal de enfermagem": "conselhos-profissionais",
    "conselho federal de engenharia": "conselhos-profissionais",
    "entidades de fiscalizacao do exercicio das profissoes": "conselhos-profissionais",
    "conselho nacional de recursos hidricos": "ana",
    "conselho nacional de politica energetica": "mme",
    "advocacia geral da uniao": "agu",
    "agencia nacional de aguas e saneamento": "ana",
}

# Ministérios: a pasta de recuo quando nenhum órgão específico casa. Mantém o número de pastas
# limitado — sem isso, cada superintendência estadual viraria uma pasta.
MINISTERIOS = {
    "ministerio da saude": "ms",
    "ministerio da educacao": "mec",
    "ministerio do trabalho": "mte",
    "ministerio da previdencia social": "sprev",
    "ministerio da fazenda": "fazenda",
    "ministerio da agricultura": "mapa",
    "ministerio do meio ambiente": "mma",
    "ministerio dos transportes": "transportes",
    "ministerio de minas e energia": "mme",
    "ministerio da justica": "mj",
    "ministerio da defesa": "defesa",
    "ministerio das comunicacoes": "comunicacoes",
    "ministerio do desenvolvimento agrario": "mda",
    "ministerio da cultura": "cultura",
    "ministerio do turismo": "turismo",
    "ministerio das cidades": "cidades",
    "ministerio da integracao": "integracao",
    "ministerio da ciencia": "mcti",
    "ministerio do desenvolvimento social": "mds",
    "ministerio das mulheres": "mulheres",
    "ministerio dos direitos humanos": "mdh",
    "ministerio dos povos indigenas": "mpi",
    "ministerio da igualdade racial": "igualdade-racial",
    "ministerio do esporte": "esporte",
    "ministerio do planejamento": "planejamento",
    "ministerio da gestao": "gestao",
    "ministerio de portos e aeroportos": "portos-aeroportos",
    "ministerio do desenvolvimento industria": "mdic",
    "ministerio do desenvolvimento e assisten": "mds",
    "ministerio publico da uniao": "mpu",
    "ministerio das relacoes exteriores": "mre",
    "ministerio do empreendedorismo": "empreendedorismo",
    "ministerio da pesca": "pesca",
    "presidencia da republica": "presidencia",
    "banco nacional de desenvolvimento": "bndes",
    "ministerio da agricultura e pecuaria": "mapa",
    "ministerio da pesca e aquicultura": "pesca",
    "ministerio das cidades": "cidades",
    "poder judiciario": "poder-judiciario",
    "poder legislativo": "poder-legislativo",
    "atos do senado federal": "poder-legislativo",
    "atos da camara dos deputados": "poder-legislativo",
    "senado federal": "poder-legislativo",
    "camara dos deputados": "poder-legislativo",
    "congresso nacional": "poder-legislativo",
    "tribunal de contas da uniao": "tcu",
    "ministerio da fazenda": "fazenda",
}


def sem_acento(s):
    return normalizar_chave(s)


def orgao_de(hierarquia):
    """Decide a pasta do órgão: o mais específico que reconhecemos, senão o ministério, senão outros."""
    niveis = [sem_acento(n) for n in hierarquia or []]
    for nivel in reversed(niveis):  # do mais específico para o mais geral
        for chave, slug in ORGAOS.items():
            if chave in nivel:
                return slug
    for nivel in niveis:
        for chave, slug in MINISTERIOS.items():
            if chave in nivel:
                return slug
    return slugify(niveis[0])[:40] if niveis else "outros"


def http(url, limite, accept="text/html", tentativas=4):
    if ACESSO_RECUSADO.is_set():
        raise AcessoHTTPRecusado("coleta suspensa após recusa HTTP da fonte")
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept,
                                               "Accept-Encoding": "identity"})
    import time
    ultimo = None
    for n in range(tentativas):
        if ACESSO_RECUSADO.is_set():
            raise AcessoHTTPRecusado("coleta suspensa após recusa HTTP da fonte")
        limite.esperar()
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 429):
                ACESSO_RECUSADO.set()
                raise AcessoHTTPRecusado(f"HTTP {e.code}: {url}; coleta interrompida sem contornar recusa") from e
            if e.code in (400, 404, 410):
                return e.code, b""
            ultimo = e
        except Exception as e:
            ultimo = e
        time.sleep(3 * (n + 1) ** 2)
    raise RuntimeError(f"falhou após {tentativas} tentativas: {url}: {ultimo}")


def extrair_indice(bruto):
    html = bruto.decode("utf-8", errors="replace")
    m = re.search(r'<script\b[^>]*\bid=[\"\']params[\"\'][^>]*>(.*?)</script>', html, re.S | re.I)
    if not m:
        raise ValueError("índice sem script params; não comprova dia sem edição")
    dados = json.loads(m.group(1))
    if not isinstance(dados, dict) or not isinstance(dados.get("jsonArray"), list):
        raise ValueError("índice sem lista jsonArray")
    if any(not isinstance(ato, dict) or not ato.get("urlTitle") for ato in dados["jsonArray"]):
        raise ValueError("índice contém ato sem urlTitle")
    return dados["jsonArray"]


def atos_do_dia(data, limite):
    """Lista validada da Seção 1; falha de página não é dia sem edição."""
    st, bruto = http(DIA.format(data.strftime("%d-%m-%Y")), limite)
    if st != 200 or not bruto:
        raise ValueError(f"HTTP {st} ou resposta vazia no índice do dia")
    lista = extrair_indice(bruto)
    sha = hashlib.sha256(bruto).hexdigest()
    pasta = os.path.join(RAIZ, "_indice", "dou", data.isoformat())
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, sha + ".html.gz")
    if not os.path.exists(caminho):
        with gzip.open(caminho + ".tmp", "wb") as f:
            f.write(bruto)
        os.replace(caminho + ".tmp", caminho)
    return lista


def tipo_de(ato):
    titulo = normalizar_chave(ato.get("title"))
    if re.match(r"^(?:retificac|despachos?\b|decis(?:ao|oes)\b|extratos?\b|avisos?\b|edita(?:l|is)\b|apostilas?\b|comunicados?\b|atas?\b)", titulo):
        return None
    # Convênios administrativos não são os convênios tributários do CONFAZ.
    for inicio, chave in (("convenio icms ", "convenio icms"),
                          ("protocolo icms ", "protocolo icms"),
                          ("ajuste sinief ", "ajuste sinief"),
                          ("ato declaratorio interpretativo ", "ato declaratorio interpretativo"),
                          ("ato declaratorio normativo ", "ato declaratorio normativo")):
        if titulo.startswith(inicio):
            return chave
    return TIPOS_NORMATIVOS.get((ato.get("artType") or "").strip().lower())


def caminho_do_ato(ato, orgao, pasta, ano):
    slug = slugify(ato["urlTitle"])
    antigo = os.path.join(RAIZ, orgao, pasta, ano, slug[:120] + ".md")
    if len(slug) <= 120:
        return antigo
    # As URLs terminam no identificador do DOU; truncar esse trecho fundia atos distintos.
    if os.path.isfile(antigo):
        with open(antigo, encoding="utf-8") as f:
            if f"fonte: {yaml_str(ATO.format(ato['urlTitle']))}\n" in f.read():
                return antigo
    identificador = re.search(r"-(\d+)$", slug)
    sufixo = identificador.group(1) if identificador else hashlib.sha256(slug.encode()).hexdigest()[:16]
    return os.path.join(RAIZ, orgao, pasta, ano, slug[:100] + "-" + sufixo + ".md")


NUMERO = re.compile(r"n[ºo°]\s*([\d.]+)", re.I)


def pendencia_integralidade(corpo):
    texto = normalizar_chave(corpo)
    for m in re.finditer(r"\b(?:integras?|inteiro teor)\b", texto):
        trecho = texto[max(0, m.start() - 80):m.end() + 240]
        if re.search(r"dispon|biblioteca|constam|site|consult|encontr", trecho):
            return "texto integral externo exige revisão: " + trecho
    return ""


def assinatura_do_ato(titulo, corpo):
    data = data_do_texto(titulo, linhas=1)
    if data:
        return data
    tipo = normalizar_chave(titulo).split()[:1]
    numero = NUMERO.search(titulo)
    linhas = [l.strip().strip("*") for l in corpo.splitlines() if l.strip() and not l.lstrip().startswith("#")][:6]
    for linha in linhas:
        if normalizar_chave(linha).split()[:1] == tipo:
            data = data_do_texto(linha, numero=numero.group(1).replace(".", "") if numero else None, linhas=1)
            if data:
                return data
    return None


def processar(ato, data, limite, orgaos_alvo):
    tipo_chave = tipo_de(ato)
    if not tipo_chave:
        return "ignorado", None
    orgao = orgao_de(ato.get("hierarchyList"))
    if orgaos_alvo and orgao not in orgaos_alvo:
        return "ignorado", None

    pasta, tipo_nome = CANONICO[tipo_chave]
    ano = data.strftime("%Y")
    md = caminho_do_ato(ato, orgao, pasta, ano)
    slug = os.path.basename(md)[:-3]
    if os.path.exists(md):
        return "pulado", None

    url = ATO.format(ato["urlTitle"])
    st, bruto = http(url, limite)
    if st != 200 or not bruto:
        return "sem_texto", {"urlTitle": ato["urlTitle"], "titulo": ato.get("title"), "http": st}
    html = bruto.decode("utf-8", errors="replace")
    sha_fonte = hashlib.sha256(bruto).hexdigest()
    fonte = os.path.join(RAIZ, "_fonte", orgao, ano, slug + "-" + sha_fonte + ".html.gz")
    os.makedirs(os.path.dirname(fonte), exist_ok=True)
    if not os.path.exists(fonte):
        with gzip.open(fonte, "wb") as f:
            f.write(bruto)

    m = re.search(r'<div[^>]+class="[^"]*texto-dou[^"]*".*?</div>\s*(?=<div|</section|</main)', html, re.S)
    if not m:
        return "sem_texto", {"urlTitle": ato["urlTitle"], "titulo": ato.get("title"),
                              "motivo": "sem bloco texto-dou", "fonte_preservada": fonte}

    if re.search(r"<(?:img|svg|canvas|object|embed|iframe|math|v:\w+|m:oMath)\b", m.group(0), re.I):
        return "sem_texto", {"urlTitle": ato["urlTitle"],
                              "motivo": "conteúdo visual no ato exige extração ou revisão antes de contar texto integral",
                              "fonte_preservada": fonte}

    titulo = (ato.get("title") or "").strip()
    num = NUMERO.search(titulo)
    # o título do DOU é a própria epígrafe, e traz a data de assinatura — que não é a da
    # publicação: um ato assinado no dia 13 costuma sair no dia 14. O acervo data a norma pela
    # assinatura, como nas leis; a publicação fica nos campos `publicacao`/`data_publicacao`.
    corpo = convert(m.group(0))
    if not corpo.strip():
        return "sem_texto", {"urlTitle": ato["urlTitle"], "motivo": "bloco texto-dou vazio"}
    pendencia = pendencia_integralidade(corpo)
    if pendencia:
        return "sem_texto", {"urlTitle": ato["urlTitle"], "motivo": pendencia, "fonte_preservada": fonte}
    assinatura = assinatura_do_ato(titulo, corpo)
    data_na_fonte = assinatura if assinatura and assinatura > data.isoformat() else None
    if data_na_fonte:
        assinatura = ""
    cab = ["---", f"titulo: {yaml_str(titulo)}", f"orgao: {yaml_str(ato.get('hierarchyStr') or '')}",
           f"tipo: {yaml_str(tipo_nome)}", f"numero: {yaml_str(num.group(1).replace('.', '') if num else '')}",
           f"data: {assinatura or yaml_str('')}", "revogada: null", 'versao_texto: "publicação original"',
           f"publicacao: {yaml_str('DOU de ' + data.strftime('%d/%m/%Y') + ', seção 1, p. ' + str(ato.get('numberPage') or ''))}",
           f"data_publicacao: {data.isoformat()}", f"edicao: {yaml_str(ato.get('editionNumber') or '')}",
           f"fonte: {yaml_str(url)}", f"sha256_html_fonte: {sha_fonte}",
           f"baixado_em: {dt.date.today().isoformat()}", "---", ""]
    if data_na_fonte:
        cab[-2:-2] = [f"data_na_fonte: {data_na_fonte}",
                       'observacao_data: "A data declarada na fonte é posterior à publicação; assinatura não confirmada."']
    os.makedirs(os.path.dirname(md), exist_ok=True)
    tmp = md + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(cab) + f"# {titulo}\n\n" + corpo)
    os.replace(tmp, md)
    return "ok", None


def dias(de, ate):
    d = de
    while d <= ate:
        yield d
        d += dt.timedelta(days=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--de", required=True, help="AAAA-MM-DD")
    ap.add_argument("--ate", required=True, help="AAAA-MM-DD")
    ap.add_argument("--orgaos", default="", help="só estes (ex.: anvisa,contran); vazio = todos")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--rps", type=float, default=3)
    ap.add_argument("--listar", action="store_true", help="conta o que seria baixado, sem baixar")
    a = ap.parse_args()

    de = dt.date.fromisoformat(a.de)
    ate = min(dt.date.fromisoformat(a.ate), dt.datetime.now(ZoneInfo("America/Recife")).date())
    if de > ate or not 0 < a.rps <= 4 or a.workers < 1:
        ap.error("intervalo de datas inválido; rps deve estar entre 0 e 4 e workers ser positivo")
    alvo = {s.strip() for s in a.orgaos.split(",") if s.strip()}
    limite = Limitador(a.rps)
    os.makedirs(RAIZ, exist_ok=True)
    falhas_path = os.path.join(RAIZ, "_falhas.jsonl")
    cont = {"ok": 0, "pulado": 0, "sem_texto": 0, "ignorado": 0, "erro": 0}
    por_orgao = {}

    with open(falhas_path, "a", encoding="utf-8") as falhas:
        for data in dias(de, ate):
            try:
                lista = atos_do_dia(data, limite)
            except AcessoHTTPRecusado as e:
                falhas.write(json.dumps({"status": "acesso_recusado", "data": data.isoformat(),
                                         "erro": str(e)}, ensure_ascii=False) + "\n")
                print(str(e), flush=True)
                return 77
            except Exception as e:
                print(f"{data} erro no índice do dia: {str(e)[:120]}", flush=True)
                cont["erro"] += 1
                falhas.write(json.dumps({"status": "indice", "data": data.isoformat(),
                                         "url": DIA.format(data.strftime("%d-%m-%Y")),
                                         "erro": str(e)[:300]}, ensure_ascii=False) + "\n")
                falhas.flush()
                continue
            if a.listar:
                for ato in lista:
                    if tipo_de(ato):
                        o = orgao_de(ato.get("hierarchyList"))
                        if not alvo or o in alvo:
                            por_orgao[o] = por_orgao.get(o, 0) + 1
                            cont["ok"] += 1
                print(f"{data} {len(lista)} atos, {cont['ok']} normativos acumulados", flush=True)
                continue
            acesso_recusado = False
            with ThreadPoolExecutor(a.workers) as ex:
                futs = {ex.submit(processar, ato, data, limite, alvo): ato for ato in lista}
                for fut in as_completed(futs):
                    ato = futs[fut]
                    try:
                        st, extra = fut.result()
                    except AcessoHTTPRecusado as e:
                        acesso_recusado = True
                        st, extra = "erro", {"urlTitle": ato.get("urlTitle"), "erro": str(e),
                                             "acesso_recusado": True}
                    except Exception as e:
                        st, extra = "erro", {"urlTitle": ato.get("urlTitle"), "erro": str(e)[:300]}
                    cont[st] += 1
                    if extra:
                        extra["status"] = st
                        extra["data"] = data.isoformat()
                        falhas.write(json.dumps(extra, ensure_ascii=False) + "\n")
                        falhas.flush()
            print(f"{data} {cont}", flush=True)
            if acesso_recusado:
                print("DOU interrompido após recusa de acesso da fonte", flush=True)
                return 77

    if a.listar:
        for o, n in sorted(por_orgao.items(), key=lambda x: -x[1]):
            print(f"  {n:6} {o}")
    print("FIM", cont, flush=True)
    return 1 if cont["erro"] or cont["sem_texto"] else 0


if __name__ == "__main__":
    sys.exit(main())
