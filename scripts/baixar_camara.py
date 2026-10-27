"""Coleta resoluções da Câmara na busca oficial e textos Legin, com cache e retomada.

    python3 -I scripts/baixar_camara.py --rps 2 --workers 4
"""
import argparse
import datetime as dt
import gzip
import hashlib
import html
import json
import math
import os
from pathlib import Path
import re
import sys
import subprocess
import tempfile
import urllib.parse
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import Rede, decodificar, yaml_str, texto_pdf_para_md
from html2md import convert

RAIZ = Path(__file__).resolve().parent.parent / "federal"
CACHE = RAIZ / "_fonte" / "camara"
INDICE = RAIZ / "_indice" / "camara"
BUSCA = "https://www.camara.leg.br/legislacao/busca"
MESES = {m: n for n, m in enumerate(("janeiro", "fevereiro", "marco", "abril", "maio", "junho",
                                    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"), 1)}
TIPOS = {
    "camara": ("Resolução da Câmara dos Deputados", "resolucoes-camara", "rcd", "resolucaodacamaradosdeputados"),
    "senado": ("Resolução do Senado Federal", "resolucoes-senado", "rsf", "resolucao"),
    "congresso": ("Resolução do Congresso Nacional", "resolucoes-congresso", "rcn", "resolucao"),
    "mpv": ("Medida Provisória", "medidas-provisorias", "mpv", "medidaprovisoria"),
    "dlg": ("Decreto Legislativo", "decretos-legislativos", "dlg", "decretolegislativo"),
    "dpl": ("Decreto do Poder Legislativo", "decretos-legislativos", "dpl", "decreto"),
    "lei": ("Lei", "leis-ordinarias", "lei", "lei"),
    "lcp": ("Lei Complementar", "leis-complementares", "lcp", "leicomplementar"),
    "del": ("Decreto-Lei", "decretos-lei", "del", "decreto-lei"),
    "lct": ("Lei Constitucional", "leis-constitucionais", "lct", "leiconstitucional"),
}


def texto(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def gravar_json(path, valor):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(valor, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def id_camara(d):
    m = re.search(r"-(\d+)-norma(?:-|\.)", d["url"])
    return m[1] if m else None


def resumo_indice(total, docs, paginas, totais=None):
    unicos, vistos, sem_id = [], set(), 0
    for d in docs:
        ident = id_camara(d)
        chave = ident or d["url"]
        if chave in vistos:
            continue
        vistos.add(chave)
        sem_id += ident is None
        unicos.append({**d, "id_camara": ident})
    totais = sorted(set(totais or [total]))
    completo = (paginas == math.ceil(total / 20) and len(unicos) == total and sem_id == 0
                and len(totais) == 1)
    return {"total_fonte": total, "totais_observados": totais, "paginas_coletadas": paginas,
            "documentos_unicos": len(unicos), "faltantes_indice": max(0, total - len(unicos)),
            "sem_identificador": sem_id, "completo": completo,
            "estado": "completo" if completo else "parcial", "documentos": unicos}


@lru_cache(maxsize=None)
def equivalencias(tipo):
    """URN do índice Senado aponta ao mesmo arquivo, incluindo reedições e séries DPL/DLG."""
    fontes = {"senado": ("RSF",), "congresso": ("RCN",), "mpv": ("MPV",), "dlg": ("DLG", "DPL"), "dpl": ("DLG", "DPL"),
              "lei": ("LEI",), "lcp": ("LCP",), "del": ("DEL",), "lct": ("LCT",)}
    if tipo not in fontes:
        return {}
    from baixar_federal import montar
    tipos = fontes[tipo]
    por_urn = {}
    for nome in tipos:
        path = RAIZ / "_indice" / (nome + ".json")
        for d in json.loads(path.read_text(encoding="utf-8"))["ListaDocumento"]["documentos"]["documento"]:
            info = montar(d)
            if d.get("complemento") and not Path(info["md"]).exists():
                legado = dict(d)
                legado.pop("complemento")
                caminho_antigo = Path(montar(legado)["md"])
                if caminho_antigo.exists():
                    with caminho_antigo.open(encoding="utf-8") as f:
                        cab = f.read(8192).split("---", 2)[1]
                    m = re.search(r"^urn: (.+)$", cab, re.M)
                    if m and json.loads(m[1]) == info["urn"]:
                        info["md"] = str(caminho_antigo)
            por_urn.setdefault(info["urn"], []).append(info)
    return por_urn


@lru_cache(maxsize=1)
def identidades_conferidas():
    path = RAIZ / "_identidades_camara.json"
    return json.loads(path.read_text()) if path.exists() else {}


def identificar(d, tipo):
    nome_tipo, pasta, prefixo, prefixo_url = TIPOS[tipo]
    m = re.search(re.escape(prefixo_url) + r'-([\w.-]+?)-(\d+)-([a-z]+)-(\d{4})-(\d+)-norma', d["url"])
    if not m:
        raise ValueError(f"data/número ausentes da URL: {d['url']}")
    numero, dia, mes, ano, ident = m.groups()
    numero = numero.replace(".", "")
    data = dt.date(int(ano), MESES[mes], int(dia)).isoformat()
    alias = identidades_conferidas().get(ident)
    if alias:
        if alias["url"] != d["url"] or alias["tipo"] != tipo or alias["numero"] != numero:
            raise ValueError("identidade auditada da Câmara não corresponde ao documento")
        data = alias["data"]
        ano = data[:4]
    slug = f"{prefixo}-{numero}-{data}" + (f"-{ident}" if tipo == "camara" else "")
    info = {"numero": numero, "data": data, "md": RAIZ / pasta / ano / (slug + ".md"), "nome": nome_tipo}
    if tipo in ("senado", "congresso"):
        autoridade = "senado.federal" if tipo == "senado" else "congresso.nacional"
        info["urn"] = f"urn:lex:br:{autoridade}:resolucao:{data};{numero}"
    if tipo in ("mpv", "dlg", "dpl", "lei", "lcp", "del", "lct"):
        lex = {"mpv": "medida.provisoria", "dlg": "decreto.legislativo", "dpl": "decreto.legislativo",
               "lei": "lei", "lcp": "lei.complementar", "del": "decreto.lei", "lct": "lei.constitucional"}[tipo]
        info["urn"] = f"urn:lex:br:federal:{lex}:{data};{numero}"
        iguais = equivalencias(tipo).get(info["urn"], [])
        if tipo in ("dpl", "lei", "lcp", "del", "lct") and not iguais:
            raise ValueError("norma fora da série primária esperada: " + info["urn"])
        if iguais:
            canonico = next((i for i in iguais if Path(i["md"]).exists()), iguais[0])
            info.update({"md": Path(canonico["md"]), "nome": canonico["nome"]})
    return info


def obter(rede, url):
    if urllib.parse.urlparse(url).hostname not in {"www.camara.leg.br", "www2.camara.leg.br"}:
        raise ValueError(f"fonte não autorizada: {url}")
    path = CACHE / (hashlib.sha256(url.encode()).hexdigest() + ".html.gz")
    if path.exists():
        return gzip.decompress(path.read_bytes()).decode("utf-8")
    st, bruto, ct = rede.get(url, timeout=60)
    if st != 200 or not bruto:
        raise RuntimeError(f"HTTP {st}, {len(bruto)} bytes: {url}")
    s = decodificar(bruto, ct)
    if any(x in s.lower() for x in ("verify you are human", "verifique que você é humano", "captcha-container")):
        raise RuntimeError(f"bloqueio da fonte: {url}")
    CACHE.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(gzip.compress(s.encode("utf-8")))
    tmp.replace(path)
    return s


def pagina(rede, numero, tipo="camara", filtros=None):
    params = {"tipo": TIPOS[tipo][0], "ordenacao": "data:DESC", "pagina": numero}
    params.update(filtros or {})
    url = BUSCA + "?" + urllib.parse.urlencode(params)
    s = obter(rede, url)
    total = re.search(r"Exibindo resultados de\s+[\d.]+\s+a\s+[\d.]+\s+de\s+([\d.]+)", s)
    if not total:
        raise ValueError(f"busca sem total reconhecível: {url}")
    docs = []
    for item in re.findall(r'<li class="busca-resultados__item[^\"]*">(.*?)</li>', s, re.S):
        link = re.search(r'<a[^>]+href="([^"]+/legin/[^"]+)"[^>]*>(.*?)</a>', item, re.S)
        ementa = re.search(r'busca-resultados__descricao[^>]*>(.*?)</p>', item, re.S)
        situacao = re.search(r'busca-resultados__situacao[^>]*>(.*?)</p>', item, re.S)
        if not link:
            raise ValueError("resultado sem link Legin")
        docs.append({"url": html.unescape(link[1]), "titulo": texto(link[2]),
                     "ementa": re.sub(r"^Ementa:\s*", "", texto(ementa[1])) if ementa else "",
                     "situacao": re.sub(r"^Situação:\s*", "", texto(situacao[1])) if situacao else ""})
    if not docs:
        raise ValueError(f"busca vazia: {url}")
    return int(total[1].replace(".", "")), docs


def corpo_norma(s):
    inicio = re.search(r'<div\b[^>]*class=["\']textoNorma["\'][^>]*>', s)
    if not inicio:
        # O Legin também publica compilações como HTML autônomo exportado do Word/LibreOffice.
        if re.search(r'<meta\b[^>]*name=["\']generator["\'][^>]*content=["\'][^"\']*(?:LibreOffice|Microsoft Word)', s, re.I):
            body = re.search(r'<body\b[^>]*>(.*?)</body>', s, re.I | re.S)
            if body and not re.search(r'id=["\'](?:portal-header|main-nav)["\']', body[1]):
                return body[1]
        raise ValueError("página sem textoNorma")
    nivel = 1
    for tag in re.finditer(r"</?div\b[^>]*>", s[inicio.end():], re.I):
        nivel += -1 if tag[0].startswith("</") else 1
        if nivel == 0:
            return s[inicio.end():inicio.end() + tag.start()]
    raise ValueError("textoNorma incompleto")


def corpo_pdf(rede, url):
    if urllib.parse.urlparse(url).hostname not in {"www.camara.leg.br", "www2.camara.leg.br"}:
        raise ValueError(f"fonte não autorizada: {url}")
    path = CACHE / (hashlib.sha256(url.encode()).hexdigest() + ".pdf.gz")
    if path.exists():
        bruto = gzip.decompress(path.read_bytes())
    else:
        status, bruto, _ = rede.get(url, timeout=60)
        if status in (401, 403):
            raise RuntimeError(f"HTTP {status}: {url}")
        if status != 200 or not bruto.startswith(b"%PDF"):
            raise ValueError(f"PDF inválido HTTP {status}: {url}")
        CACHE.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_bytes(gzip.compress(bruto))
        tmp.replace(path)
    with tempfile.TemporaryDirectory() as pasta:
        pdf = Path(pasta) / "norma.pdf"
        pdf.write_bytes(bruto)
        proc = subprocess.run(["rtk", "proxy", "pdftotext", "-q", "-layout", "-enc", "UTF-8", str(pdf), "-"],
                              capture_output=True, timeout=60, check=True)
    corpo = texto_pdf_para_md(proc.stdout.decode("utf-8"))
    if len(corpo.strip()) < 200 or "\x00" in corpo or not re.search(r"\bArt(?:igo)?[*.\s]{0,8}(?:\d|[úu]nico)", corpo, re.I):
        raise ValueError(f"PDF sem texto normativo extraível: {url}")
    return corpo


def conferir_data_propria(info, corpo, titulo=None, tipo="dlg"):
    if titulo is not None:
        prefixo = {"dlg": r"Decreto Legislativo", "dpl": r"Decreto", "senado": r"Resolução(?: do Senado Federal)?", "congresso": r"Resolução(?: do Congresso Nacional)?", "lei": r"Lei", "lcp": r"Lei Complementar", "del": r"Decreto-Lei", "lct": r"Lei Constitucional", "mpv": r"Medida Provisória"}[tipo]
        numero = re.search(prefixo + r"\s+n[º°o.]?\s*([\d.]+(?:-[a-z0-9]+)?)", titulo, re.I)
        if not numero or numero[1].replace(".", "").lower() != info["numero"].lower():
            raise ValueError("epígrafe oficial não comprova tipo/número primário")
    normal = unicodedata.normalize("NFKD", corpo).encode("ascii", "ignore").decode().lower()
    datas = set()
    for dia, mes, ano in re.findall(r"(?:senado federal|congresso nacional|rio de janeiro|brasilia|capital federal),?\s*(?:em\s*)?(\d{1,2})\s+de\s+([a-z]+)\s+de\s*(\d{4})", normal):
        if mes in MESES:
            datas.add(dt.date(int(ano), MESES[mes], int(dia)).isoformat())
    if not datas or datas != {info["data"]}:
        raise ValueError("data própria do fecho não comprova identidade primária: " + str(sorted(datas)))
    if not equivalencias(tipo).get(info["urn"]):
        raise ValueError("identidade do ato ausente do índice primário")


def tipo_legislativo_comprovado(corpo):
    cabeca = re.split(r"\bArt(?:igo)?[*.\s]{0,8}(?:1|[úu]nico)\b", corpo, maxsplit=1, flags=re.I)[0][:5000]
    normal = re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", cabeca).lower())
    return bool(re.search(r"(?:faco|faz)saber.{0,80}que.{0,80}congressonacional.{0,80}(?:decret|resolv)|congressonacional(?:decreta|decretou).{0,20}(?:sanccio|sancio|promulg)|heiporbem(?:sanccion|sancion)aremandarqueseexecute.{0,40}(?:resolucao|decreto).{0,20}assemble(?:i)?ageral", normal))


def processar(rede, d, tipo="camara"):
    info = identificar(d, tipo)
    path, numero, data, nome_tipo = info["md"], info["numero"], info["data"], info["nome"]
    if path.exists():
        return "pulado"
    s = obter(rede, d["url"])
    links = [html.unescape(u) for u in re.findall(r'href=["\']([^"\']+)["\']', s)]
    ident = id_camara(d)
    links = [u for u in links if f"-{ident}-" in u]
    candidatos = [(u, compilada) for marcador, compilada in (("-normaatualizada-", True), ("-publicacaooriginal-", False), ("-textopublicacaooriginal-", False))
                  for extensao in (".html", ".pdf") for u in links if marcador in u and u.lower().endswith(extensao)]
    if not candidatos:
        raise ValueError(f"norma sem texto HTML/PDF: {d['url']}")
    erros = []
    for candidato, compilada in candidatos:
        url_texto = urllib.parse.urljoin(d["url"], candidato)
        try:
            corpo = corpo_pdf(rede, url_texto) if candidato.lower().endswith(".pdf") else convert(corpo_norma(obter(rede, url_texto)))
            if len(corpo.strip()) < 80 or "\x00" in corpo or (tipo in ("lei", "lcp", "del", "lct", "dpl") and not re.search(r"\bArt(?:igo)?[*.\s]{0,8}(?:\d|[úu]nico)", corpo, re.I)):
                raise ValueError("texto insuficiente")
            break
        except ValueError as exc:
            erros.append(str(exc))
    else:
        raise ValueError("nenhum texto íntegro HTML/PDF: " + "; ".join(erros))
    if len(corpo.strip()) < 80 or (tipo in ("lei", "lcp", "del", "lct", "dpl") and not re.search(r"\bArt(?:igo)?[*.\s]{0,8}(?:\d|[úu]nico)", corpo, re.I)):
        raise ValueError(f"texto insuficiente: {url_texto}")
    if "-textopublicacaooriginal-" in candidato and tipo in ("lei", "lcp", "del", "lct", "mpv"):
        conferir_data_propria(info, corpo, d["titulo"], tipo)
    if tipo == "dlg":
        conferir_data_propria(info, corpo, d["titulo"])
    if tipo == "senado":
        conferir_data_propria(info, corpo, d["titulo"], "senado")
        if not (re.search(r"Senado Federal,?\s*(?:em\s*)?\d", corpo[-2500:], re.I) or re.search(r"Presidente do Senado Federal", corpo[-800:], re.I)):
            raise ValueError("autoria Senado não comprovada no fecho próprio")
    if tipo == "dpl":
        conferir_data_propria(info, corpo, d["titulo"], "dpl")
        if not tipo_legislativo_comprovado(corpo):
            raise ValueError("tipo legislativo não comprovado na fórmula de promulgação")
    valores = {"titulo": d["titulo"], "tipo": nome_tipo, "numero": numero,
               "data": data, "ementa": d["ementa"], "situacao": d["situacao"],
               "revogada": True if d["situacao"].strip().lower() == "revogada" else False if d["situacao"].strip().lower() in ("vigente", "em vigor") else None,
               "versao_texto": "compilada" if compilada else "original", "fonte": url_texto,
               "url_metadados": d["url"], "baixado_em": dt.date.today().isoformat()}
    if info.get("urn"):
        valores["urn"] = info["urn"]
    linhas = ["---"]
    for k, v in valores.items():
        linhas.append(f"{k}: {'null' if v is None else str(v).lower() if isinstance(v, bool) else v if k in ('data', 'baixado_em') else yaml_str(v)}")
    linhas += ["---", "", "# " + d["titulo"], "", corpo]
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text("\n".join(linhas), encoding="utf-8")
    tmp.replace(path)
    return "ok"


def coletar_pendencias(rede, tipo, limite=0):
    from baixar_federal import carregar_indice, montar
    recorte = {"lei": {"LEI-n"}, "lcp": {"LCP"}, "del": {"DEL"}, "lct": {"LCT"},
               "dlg": {"DLG"}, "dpl": {"DPL-n"}, "mpv": {"MPV-cs", "MPV-ss"}}
    if tipo not in recorte:
        raise ValueError("tipo sem índice primário para pendências")
    alvos = [d for d in carregar_indice(recorte[tipo]) if not Path(montar(d)["md"]).exists()]
    if limite:
        alvos = alvos[:limite]
    cont = {"ok": 0, "pulado": 0, "erro": 0}
    consultas = []
    for d in alvos:
        esperado = montar(d)
        numero = d["numero"] + ("-" + d["complemento"] if d.get("complemento") else "")
        try:
            filtros = {"numero": d["numero"] if tipo == "dpl" else numero, "ano": esperado["data"][:4]}
            if tipo == "dpl":
                filtros["tipo"] = "Decreto"
            total, lote = pagina(rede, 1, tipo, filtros)
            consultas.append({"id_senado": d["id"], "urn": esperado["urn"], "total_fonte": total, "documentos": lote})
            candidatos = []
            for item in lote:
                try:
                    if identificar(item, tipo).get("urn") == esperado["urn"]:
                        candidatos.append(item)
                except ValueError:
                    continue
            if len(candidatos) != 1:
                raise ValueError(f"consulta não identificou norma única: {len(candidatos)}/{total}")
            st = processar(rede, candidatos[0], tipo)
            cont[st] += 1
            print(st, d["norma"], cont, flush=True)
        except Exception as exc:
            cont["erro"] += 1
            with (RAIZ / "_falhas_camara.jsonl").open("a") as f:
                f.write(json.dumps({"fonte": "camara-" + tipo, "id_senado": d["id"], "norma": d["norma"],
                                    "urn": esperado["urn"], "erro": str(exc)}, ensure_ascii=False) + "\n")
            print("erro", d["norma"], str(exc), flush=True)
            if re.search(r"\bHTTP\s+(?:401|403|429)\b", str(exc)) or "bloqueio da fonte" in str(exc):
                break
        gravar_json(RAIZ / "_indice" / ("camara-" + tipo + "-pendencias") / "indice.json",
                    {"fonte": BUSCA, "recorte": sorted(recorte[tipo]), "completo": False, "consultas": consultas})
    print("FIM PENDENCIAS", tipo, cont, flush=True)
    return int(bool(cont["erro"]))


def reparar_falhas(rede, tipo):
    alvos = {}
    for linha in (RAIZ / "_falhas_camara.jsonl").read_text().splitlines():
        registro = json.loads(linha)
        if registro.get("fonte") == tipo and registro.get("url"):
            alvos[registro["url"]] = registro
    cont = {"ok": 0, "pulado": 0, "erro": 0}
    for d in alvos.values():
        registro = {"fonte": "camara-" + tipo, "url": d["url"], "erro_anterior": d.get("erro"), "verificado_em": dt.datetime.now().isoformat()}
        try:
            estado = processar(rede, d, tipo)
            cont[estado] += 1
            registro["resultado"] = estado
        except Exception as exc:
            cont["erro"] += 1
            registro.update(resultado="erro", erro=str(exc))
        with (RAIZ / "_reparos_camara.jsonl").open("a") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
        print(registro, flush=True)
        if registro.get("erro") and any(c in registro["erro"] for c in ("HTTP 401", "HTTP 403", "HTTP 429", "bloqueio da fonte")):
            break
    print("FIM REPAROS", tipo, cont, flush=True)
    return int(bool(cont["erro"]))


def completar_urns():
    from baixar_federal import carregar_indice, montar
    primarios = {montar(d)["urn"]: montar(d) for d in carregar_indice({"RSF", "RCN"})}
    atualizados, conflitos = [], []
    for tipo in ("senado", "congresso"):
        indice = RAIZ / "_indice" / ("camara-" + tipo) / "indice.json"
        if not indice.exists():
            continue
        for d in json.loads(indice.read_text())["documentos"]:
            try:
                info = identificar(d, tipo)
            except ValueError:
                continue
            if info["urn"] not in primarios or Path(primarios[info["urn"]]["md"]) != info["md"] or not info["md"].exists():
                continue
            path = info["md"]
            bruto = path.read_bytes()
            partes = bruto.split(b"---", 2)
            if len(partes) != 3 or d["url"].encode() not in partes[1]:
                continue
            cab = partes[1].decode()
            urn = re.search(r"^urn:\s*(.+)$", cab, re.M)
            if urn:
                if json.loads(urn[1]) != info["urn"]:
                    conflitos.append(str(path))
                continue
            corpo_hash = hashlib.sha256(partes[2]).hexdigest()
            partes[1] += ("urn: " + yaml_str(info["urn"]) + "\n").encode()
            tmp = path.with_suffix(".tmp")
            tmp.write_bytes(b"---".join(partes))
            tmp.replace(path)
            assert hashlib.sha256(path.read_bytes().split(b"---", 2)[2]).hexdigest() == corpo_hash
            atualizados.append({"arquivo": str(path.relative_to(RAIZ)), "urn": info["urn"], "fonte_indice": d["url"], "sha256_corpo": corpo_hash})
    cache = RAIZ / "_fonte" / "auditorias" / ("urns-completadas-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S") + ".json.gz")
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(gzip.compress(json.dumps({"atualizados": atualizados, "conflitos": conflitos}, ensure_ascii=False).encode()))
    print("URNs completadas", len(atualizados), "conflitos", len(conflitos), flush=True)
    return int(bool(conflitos))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rps", type=float, default=2)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--completar-urns", action="store_true")
    ap.add_argument("--pendencias", action="store_true")
    ap.add_argument("--limite", type=int, default=0, help="limita apenas a fila de pendências")
    ap.add_argument("--reparar-falhas", action="store_true")
    ap.add_argument("--pagina-inicial", type=int, default=1)
    ap.add_argument("--paginas", type=int, default=0, help="limita páginas para amostra")
    ap.add_argument("--tipo", choices=TIPOS, default="camara")
    ap.add_argument("--auditar-indices", action="store_true", help="corrige cobertura dos índices em cache sem rede")
    a = ap.parse_args()
    if a.completar_urns:
        return completar_urns()
    if a.auditar_indices:
        for path in (RAIZ / "_indice").glob("camara*/indice.json"):
            j = json.loads(path.read_text(encoding="utf-8"))
            if not {"total_fonte", "documentos", "paginas_coletadas"}.issubset(j):
                continue
            resumo = resumo_indice(j["total_fonte"], j["documentos"], j["paginas_coletadas"], j.get("totais_observados"))
            gravar_json(path, resumo)
            print(path.parent.name, resumo["documentos_unicos"], "/", resumo["total_fonte"], resumo["estado"], flush=True)
        return
    if not 0 < a.rps <= 4 or a.workers < 1:
        ap.error("rps deve estar entre 0 e 4; workers deve ser positivo")
    rede = Rede(a.rps)
    if a.reparar_falhas:
        return reparar_falhas(rede, a.tipo)
    if a.pendencias:
        return coletar_pendencias(rede, a.tipo, a.limite)
    cont = {"ok": 0, "pulado": 0, "erro": 0}
    docs, vistos, n, paginas, totais = [], set(), 1, 1, set()
    indice = INDICE if a.tipo == "camara" else INDICE.with_name("camara-" + a.tipo)
    indice.mkdir(parents=True, exist_ok=True)
    if a.pagina_inicial > 1:
        anterior = json.loads((indice / "indice.json").read_text())
        if anterior["paginas_coletadas"] < a.pagina_inicial - 1:
            ap.error("índice anterior não cobre as páginas omitidas")
        docs = anterior["documentos"]
        vistos = {id_camara(d) or d["url"] for d in docs}
        n = a.pagina_inicial
        paginas = math.ceil(anterior["total_fonte"] / 20)
        totais = set(anterior.get("totais_observados", [anterior["total_fonte"]]))
    with ThreadPoolExecutor(a.workers) as ex, (RAIZ / "_falhas_camara.jsonl").open("a", encoding="utf-8") as falhas:
        while n <= paginas:
            total, lote = pagina(rede, n, a.tipo)
            totais.add(total)
            paginas = math.ceil(total / 20)
            if a.paginas:
                paginas = min(paginas, a.paginas)
            for d in lote:
                ident = id_camara(d) or d["url"]
                if ident not in vistos:
                    vistos.add(ident)
                    docs.append(d)
            gravar_json(indice / f"pagina-{n:04}.json", {"total_fonte": total, "documentos": lote})
            gravar_json(indice / "indice.json", resumo_indice(total, docs, n, totais))
            futs = {ex.submit(processar, rede, d, a.tipo): d for d in lote}
            for fut in as_completed(futs):
                try:
                    cont[fut.result()] += 1
                except Exception as e:
                    cont["erro"] += 1
                    falhas.write(json.dumps({**futs[fut], "fonte": a.tipo, "erro": str(e)}, ensure_ascii=False) + "\n")
                    falhas.flush()
                    if "HTTP 403" in str(e) or "bloqueio da fonte" in str(e):
                        raise
            print(f"{a.tipo} página {n}/{paginas}, índice {len(docs)}/{total}: {cont}", flush=True)
            n += 1
    print("FIM", cont, flush=True)
    return int(bool(cont["erro"]))


if __name__ == "__main__":
    sys.exit(main())
