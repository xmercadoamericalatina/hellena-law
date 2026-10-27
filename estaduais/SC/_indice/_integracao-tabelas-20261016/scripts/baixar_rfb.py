"""Coleta atos normativos públicos da RFB com índice e fontes retomáveis."""
import argparse
import base64
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
import subprocess
import tempfile
import shutil
import urllib.request
import unicodedata
from html.parser import HTMLParser

EQUIVALENTES = {}
DOU = {}
METAS = {}

sys.path.insert(0, str(Path(__file__).resolve().parent))

from comum import AVISO_OCR, AVISO_OCR_IMAGEM, OCR_BIN, Rede, yaml_str, texto_pdf_para_md
from html2md import convert

RAIZ = Path(__file__).resolve().parent.parent / "reguladores" / "rfb"
BUSCA = "https://normas.receita.fazenda.gov.br/api/indexacao/ato/pesquisar"
CORPO = "https://normasinternet2.receita.fazenda.gov.br/api/consulta-externa/ato/"
TIPOS = [100, 7, 9, 82, 10, 11, 42, 79, 49, 90, 56, 92, 54, 59, 57, 81, 80, 65, 67, 72, 104, 75, 73]


def salvar(path, dados):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(dados)
    tmp.replace(path)


def obter(rede, url, payload=None):
    chave = hashlib.sha256((url + (json.dumps(payload, sort_keys=True) if payload else "")).encode()).hexdigest()
    cache = RAIZ / "_fonte" / "sijut" / (chave + ".json.gz")
    if cache.exists():
        return json.loads(gzip.decompress(cache.read_bytes()))
    if payload is None:
        status, bruto, _ = rede.get(url, timeout=45)
        if status != 200:
            raise RuntimeError(f"HTTP {status}: {url}")
    else:
        rede.limite.esperar()
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={**rede.headers, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=45) as resposta:
            bruto = resposta.read()
            if resposta.headers.get("Content-Encoding") == "gzip":
                bruto = gzip.decompress(bruto)
    doc = json.loads(bruto)
    salvar(cache, gzip.compress(bruto))
    return doc


def anexo_pdf(rede, doc, anexo):
    url = CORPO + str(doc["idAto"]) + "/anexo/" + str(anexo["idArquivoBinario"])
    cache = RAIZ / "_fonte" / "sijut" / (hashlib.sha256(url.encode()).hexdigest() + ".pdf.gz")
    if cache.exists():
        bruto = gzip.decompress(cache.read_bytes())
    else:
        status, bruto, _ = rede.get(url, timeout=45)
        if status != 200 or not bruto.startswith(b"%PDF"):
            raise ValueError(f"anexo PDF inválido HTTP {status}: {url}")
        salvar(cache, gzip.compress(bruto))
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "anexo.pdf"
        path.write_bytes(bruto)
        proc = subprocess.run(["rtk", "proxy", "pdftotext", "-q", "-layout", "-enc", "UTF-8", str(path), "-"], capture_output=True, timeout=60, check=True)
        texto = proc.stdout.decode("utf-8")
        paginas = max(1, texto.count("\f"))
        extraidas = [p for p in texto.split("\f") if p.strip()]
        if len(extraidas) < paginas or any(len(p.strip()) < 80 for p in extraidas):
            ocr_cache = cache.with_name(cache.name.replace(".pdf.gz", ".ocr.txt.gz"))
            if ocr_cache.exists():
                texto = gzip.decompress(ocr_cache.read_bytes()).decode("utf-8")
            else:
                proc = subprocess.run(["rtk", "proxy", OCR_BIN, str(path)], capture_output=True, timeout=300, check=True)
                texto = proc.stdout.decode("utf-8")
                salvar(ocr_cache, gzip.compress(texto.encode()))
            doc["_ocr_pdf"] = True
            extraidas = [p for p in texto.split("\f") if p.strip()]
        if len(extraidas) < paginas or any(len(p.strip()) < 80 for p in extraidas) or "\x00" in texto:
            raise ValueError("anexo PDF sem texto suficiente em todas as páginas; original preservado")
    return texto_pdf_para_md(texto)


def imagem_segmento(doc, anexo):
    bruto = base64.b64decode(anexo.get("arquivoBinario") or "", validate=True)
    if not bruto.startswith((b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n")):
        raise ValueError("anexo de imagem sem bytes reconhecíveis")
    programa = shutil.which("tesseract")
    dados = Path(OCR_BIN).parent / "tessdata"
    modelo = dados / "por.traineddata"
    if not programa or not modelo.exists() or hashlib.sha256(modelo.read_bytes()).hexdigest() != "711de9dbb8052067bd42f16b9119967f30bada80d57e2ef24f65d09f531adb04":
        raise ValueError("OCR português verificado indisponível para imagem anexa")
    import os
    proc = subprocess.run(["rtk", "proxy", programa, "stdin", "stdout", "--tessdata-dir", str(dados), "-l", "por", "--oem", "1", "--psm", "6"],
                          input=bruto, capture_output=True, timeout=60, check=True, env={**os.environ, "OMP_THREAD_LIMIT": "1"})
    texto = proc.stdout.decode("utf-8").strip()
    fonte = CORPO + str(doc["idAto"]) + "/anexo/" + str(anexo["idArquivoBinario"])
    if len(re.sub(r"\W", "", texto)) < 80:
        verificados = json.loads((RAIZ / "_anexos_graficos_verificados.json").read_text())
        prova = verificados.get(str(doc["idAto"]) + ":" + str(anexo["idArquivoBinario"]), {})
        if prova.get("sha256_original") != hashlib.sha256(bruto).hexdigest():
            raise ValueError("OCR insuficiente em imagem anexa sem comprovação visual; original preservado")
        doc.setdefault("_anexos_graficos", []).append(fonte)
    if texto:
        doc["_ocr"] = True
    return "![Anexo original da fonte](" + fonte + ")" + ("\n\n" + texto if texto else "")


def extrair(doc, rede=None):
    if not doc.get("integro") or not doc.get("publicado") or not doc.get("internet"):
        raise ValueError("fonte não declara texto íntegro e público")
    segmentos = sorted(doc.get("ementas", []) + doc.get("outrosSegmentos", []), key=lambda x: x.get("ordemSegmentoAto", 0))
    partes = []
    for segmento in segmentos:
        if segmento.get("omitir") or not segmento.get("original"):
            continue
        texto = segmento.get("textoIntegra", "")
        anexo = segmento.get("arquivoBinario")
        if anexo:
            if anexo.get("idTipoArquivo") == 2:
                partes.append(texto)
                partes.append(imagem_segmento(doc, anexo))
                continue
            if anexo.get("idTipoArquivo") == 6 and rede:
                partes.append(texto)
                partes.append(anexo_pdf(rede, doc, anexo))
                continue
            if anexo.get("idTipoArquivo") not in (4, 5) or not anexo.get("arquivoBinario"):
                raise ValueError("anexo binário exige extração própria; ato não contado como completo")
            texto += "\n" + base64.b64decode(anexo["arquivoBinario"], validate=True).decode("utf-8")
        if texto:
            partes.append(convert(texto).strip())
    corpo = "\n\n".join(partes)
    if doc.get("_anexos_graficos"):
        texto_base = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", corpo)
        if len(texto_base) < 200 or not re.search(r"(?m)^(?:\*\*)?Art(?:igo)?[*.\s]{0,8}(?:\d|[úu]nico)", texto_base, re.I):
            raise ValueError("anexo gráfico sem corpo normativo textual comprovado")
    if doc.get("_ocr"):
        corpo = AVISO_OCR_IMAGEM + corpo
    if doc.get("_ocr_pdf"):
        corpo = AVISO_OCR + corpo
    if len(corpo) < 100 or "\x00" in corpo or not doc.get("outrosSegmentos"):
        raise ValueError("texto integral insuficiente")
    return corpo


def assinatura(corpo):
    class Tabelas(HTMLParser):
        def __init__(self, texto):
            super().__init__(convert_charrefs=True)
            self.texto = texto
            self.offsets = [0]
            self.offsets.extend(m.end() for m in re.finditer("\n", texto))
            self.nivel = 0
            self.trechos = []
            self.partes = []

        def posicao(self):
            linha, coluna = self.getpos()
            return self.offsets[linha - 1] + coluna

        def handle_starttag(self, tag, attrs):
            if tag == "table":
                if not self.nivel:
                    self.inicio = self.posicao()
                    self.partes = []
                self.nivel += 1
            if self.nivel and tag in {"table", "tr", "td", "th", "p", "div", "br", "li", "caption"}:
                self.partes.append("\n")

        def handle_endtag(self, tag):
            if self.nivel and tag in {"table", "tr", "td", "th", "p", "div", "li", "caption"}:
                self.partes.append("\n")
            if tag == "table" and self.nivel:
                self.nivel -= 1
                if not self.nivel:
                    fim = self.texto.index(">", self.posicao()) + 1
                    self.trechos.append((self.inicio, fim, "".join(self.partes)))

        def handle_data(self, data):
            if self.nivel:
                self.partes.append(data)

    tabelas = Tabelas(corpo)
    tabelas.feed(corpo)
    for inicio, fim, texto in reversed(tabelas.trechos):
        corpo = corpo[:inicio] + texto + corpo[fim:]
    linhas = corpo.splitlines()
    while linhas and (not linhas[0].strip() or linhas[0].startswith("#")):
        linhas.pop(0)
    if linhas and re.match(r"(?:INSTRUÇÃO NORMATIVA|ATO DECLARATÓRIO|PORTARIA|SOLUÇÃO DE|PARECER NORMATIVO).*N[º°.]", linhas[0], re.I):
        linhas.pop(0)
    return hashlib.sha256(re.sub(r"\W+", "", unicodedata.normalize("NFKD", "\n".join(linhas)).casefold()).encode()).hexdigest()


def normalizar(s):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", str(s)).casefold())


def metadados_md(texto):
    partes = texto.split("---", 2)
    if len(partes) != 3:
        return {}, ""
    meta = {}
    for linha in partes[1].splitlines():
        if ":" not in linha:
            continue
        chave, valor = linha.split(":", 1)
        try:
            meta[chave] = json.loads(valor.strip())
        except (ValueError, TypeError):
            meta[chave] = valor.strip()
    return meta, partes[2]


def identidade(doc):
    ep = doc["epigrafe"]
    return {"tipo": ep["tipoAto"]["nomeTipoAto"], "numero": str(ep.get("numeroAto", "")),
            "data": ep.get("dataAto", ""), "orgaos": [o["nomeOrgao"] for o in ep.get("orgaos", [])]}


def mesma_identidade(doc, path):
    origem = identidade(doc)
    meta = METAS.get(path, {})
    if not origem["orgaos"] or any(not str(origem[k]).strip() for k in ("tipo", "numero", "data")):
        return False
    if any(normalizar(origem[k]) != normalizar(meta.get(k, "")) for k in ("tipo", "numero", "data")):
        return False
    orgaos_md = {normalizar(p) for p in re.split(r"[;/]", str(meta.get("orgao", ""))) if p.strip()}
    return all(normalizar(orgao) in orgaos_md for orgao in origem["orgaos"])


def equivalentes():
    EQUIVALENTES.clear()
    DOU.clear()
    METAS.clear()
    for path in RAIZ.rglob("*.md"):
        meta, corpo = metadados_md(path.read_text())
        if not meta:
            continue
        METAS[path] = meta
        fonte = str(meta.get("fonte", ""))
        if re.match(r"https?://(?:www\.)?in\.gov\.br/", fonte):
            DOU.setdefault(fonte.split("?")[0].rstrip("/"), []).append(path)
        EQUIVALENTES.setdefault(assinatura(corpo), []).append(path)


def encontrar_equivalente(doc, corpo):
    chave = assinatura(corpo)
    # Apenas o campo de publicação própria; citações no texto não provam identidade.
    for url in re.findall(r'https?://(?:www\.)?in\.gov\.br/[^\s"<>]+', str(doc.get("dadosPublicacao") or "")):
        for path in DOU.get(url.split("?")[0].rstrip("/"), []):
            if mesma_identidade(doc, path):
                return path, "mesma identidade oficial e URL da publicação própria no DOU"
    for path in EQUIVALENTES.get(chave, []):
        if mesma_identidade(doc, path):
            return path, "mesma identidade oficial e corpo integral normalizado idêntico"
    return None, None


def estrutura_tabelas(corpo):
    class Estrutura(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.nivel = 0
            self.eventos = []

        def handle_starttag(self, tag, attrs):
            if tag == "table":
                self.nivel += 1
            if self.nivel:
                self.eventos.append(("inicio", tag, sorted(attrs)))

        def handle_endtag(self, tag):
            if self.nivel:
                self.eventos.append(("fim", tag))
                if tag == "table":
                    self.nivel -= 1

        def handle_data(self, texto):
            if self.nivel:
                self.eventos.append(("texto", texto))

    parser = Estrutura()
    parser.feed(corpo)
    return parser.eventos if not parser.nivel else None


def scripts_processamento():
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (Path(__file__), *(Path(__file__).with_name(n) for n in ("html2md.py", "comum.py", "datas.py")))}


def reter_estrutura(doc, corpo, existente, criterio, url):
    ident = doc["idAto"]
    pendencia = RAIZ / "_indice/sijut/pendencias-estrutura" / f"{ident}.json"
    estrutura = estrutura_tabelas(corpo)
    canonico = existente.read_bytes()
    estrutura_anterior = estrutura_tabelas(canonico.decode())
    if estrutura is None or (estrutura and estrutura != estrutura_anterior):
        cache = RAIZ / "_fonte/sijut" / (hashlib.sha256(url.encode()).hexdigest() + ".json.gz")
        registro = {"estado": "pendente_estrutura", "id_rfb": ident, "fonte_api": url,
                    "arquivo": str(existente.relative_to(RAIZ)), "criterio_vinculo_textual": criterio,
                    "identidade_oficial": identidade(doc), "metadata_fonte": doc["epigrafe"],
                    "sourcecache": str(cache.relative_to(RAIZ)),
                    "sourcecache_gzip_sha256": hashlib.sha256(cache.read_bytes()).hexdigest(),
                    "source_sha256": hashlib.sha256(gzip.decompress(cache.read_bytes())).hexdigest(),
                    "canonico_sha256": hashlib.sha256(canonico).hexdigest(), "snapshot_canonico": canonico.decode(),
                    "corpo_candidato": corpo, "bodycandidate_sha256": hashlib.sha256(corpo.encode()).hexdigest(),
                    "estrutura_candidata": estrutura, "estrutura_canonica": estrutura_anterior,
                    "scripts_sha256": scripts_processamento(),
                    "fundamento": "Vínculo de identidade/texto não comprova árvore de tabelas; GFM anterior exige revisão explícita. Canônico preservado."}
        if pendencia.exists():
            anterior = pendencia.read_bytes()
            salvar(pendencia.parent / "originais" / f"{ident}-{hashlib.sha256(anterior).hexdigest()}.json", anterior)
        salvar(pendencia, json.dumps(registro, ensure_ascii=False, indent=2).encode())
        referencia = RAIZ / "_indice/sijut/equivalentes" / f"{ident}.json"
        if referencia.exists():
            anterior = referencia.read_bytes()
            snapshot = referencia.parent.parent / "equivalencias-originais" / f"{ident}-{hashlib.sha256(anterior).hexdigest()}.json"
            salvar(snapshot, anterior)
            ref = json.loads(anterior)
            ref.update(estado="pendente_estrutura", integralidade_confirmada=False,
                       pendencia_estrutura=str(pendencia.relative_to(RAIZ)),
                       snapshot_referencia_anterior=str(snapshot.relative_to(RAIZ)))
            salvar(referencia, json.dumps(ref, ensure_ascii=False, indent=2).encode())
        return True
    return False


def revogacao(doc):
    if doc.get("vigente") is True:
        return False, "vigente:true"
    for ancora in doc.get("ancorasNoAto", []):
        texto = ancora.get("texto") or ""
        data = ancora.get("dataInicioVigencia") or ""
        try:
            efetiva = dt.datetime.strptime(data, "%d/%m/%Y").date() <= dt.date.today()
        except ValueError:
            efetiva = False
        if re.match(r"^\[?Revogado\(a\) pelo\(a\)", texto) and efetiva and not ancora.get("ehAgendamento"):
            return True, texto
    return None, "vigente:false sem anotação explícita de revogação" if doc.get("vigente") is False else "vigente ausente ou desconhecido"


def auditar_vigencia():
    class Offline:
        def get(self, *args, **kwargs):
            raise ValueError("cache ausente; auditoria não faz HTTP")
    resumo = {"true": 0, "false": 0, "unknown": 0, "revogada_true": 0, "revogada_false": 0, "revogada_null": 0, "corrigidos": 0}
    for path in RAIZ.rglob("rfb-sijut-*.md"):
        original = path.read_bytes()
        meta, _ = metadados_md(original.decode())
        doc = obter(Offline(), meta["fonte_api"])
        valor = doc.get("vigente")
        resumo[str(valor).lower() if isinstance(valor, bool) else "unknown"] += 1
        revogada, prova = revogacao(doc)
        resumo["revogada_" + ("null" if revogada is None else str(revogada).lower())] += 1
        partes = original.split(b"---", 2)
        corpo_sha = hashlib.sha256(partes[2]).hexdigest()
        cab = partes[1].decode()
        for chave, valor in {"revogada": revogada, "vigente_fonte": valor if isinstance(valor, bool) else None, "evidencia_revogacao": prova}.items():
            linha = chave + ": " + ("null" if valor is None else str(valor).lower() if isinstance(valor, bool) else yaml_str(str(valor)))
            if re.search(r"^" + chave + r":", cab, re.M):
                cab = re.sub(r"^" + chave + r":.*$", lambda _: linha, cab, count=1, flags=re.M)
            else:
                cab += linha + "\n"
        partes[1] = cab.encode()
        novo = b"---".join(partes)
        assert hashlib.sha256(novo.split(b"---", 2)[2]).hexdigest() == corpo_sha
        if novo != original:
            salvar(path, novo)
            resumo["corrigidos"] += 1
    salvar(RAIZ / "_indice/sijut/auditoria-vigencia.json", json.dumps(resumo, ensure_ascii=False, indent=2).encode())
    print("VIGÊNCIA", resumo, flush=True)
    return resumo


def processar(rede, item):
    ident = int(item["idAto"])
    data = item.get("dataAto", "")
    ano = str(item.get("anoAto") or "sem-ano")
    path = RAIZ / ano / f"rfb-sijut-{ident}.md"
    if path.exists():
        return "skip"
    pendencia = RAIZ / "_indice/sijut/pendencias-estrutura" / f"{ident}.json"
    doc_pendente = None
    if pendencia.exists():
        registro = json.loads(pendencia.read_text())
        cache = RAIZ / registro["sourcecache"]
        canonico = RAIZ / registro["arquivo"]
        if (cache.exists() and canonico.exists()
                and hashlib.sha256(cache.read_bytes()).hexdigest() == registro["sourcecache_gzip_sha256"]
                and hashlib.sha256(canonico.read_bytes()).hexdigest() == registro["canonico_sha256"]
                and hashlib.sha256(registro["corpo_candidato"].encode()).hexdigest() == registro["bodycandidate_sha256"]
                and registro.get("scripts_sha256") == scripts_processamento()):
            return "pendente_estrutura"
        if not cache.exists():
            raise ValueError("pendência estrutural exige cache original para reavaliação offline; HTTP recusado")
        doc_pendente = json.loads(gzip.decompress(cache.read_bytes()))
    url = CORPO + str(ident) + "/visao/original"
    doc = doc_pendente if doc_pendente is not None else obter(rede, url)
    if doc.get("idAto") != ident:
        raise ValueError("identificador do texto difere do índice")
    if doc_pendente is not None:
        class Offline:
            def get(self, *args, **kwargs):
                raise ValueError("anexo ausente no cache durante reavaliação de pendência; HTTP recusado")
        corpo = extrair(doc, Offline())
    else:
        corpo = extrair(doc, rede)
    ep = doc["epigrafe"]
    tipo = ep["tipoAto"]
    if tipo["idTipoAto"] not in TIPOS:
        raise ValueError("espécie fora do recorte normativo")
    hash_corpo = assinatura(corpo)
    existente, criterio = encontrar_equivalente(doc, corpo)
    if existente:
        if reter_estrutura(doc, corpo, existente, criterio, url):
            return "pendente_estrutura"
        salvar(RAIZ / "_indice" / "sijut" / "equivalentes" / f"{ident}.json",
               json.dumps({"id_rfb": ident, "fonte_api": url, "arquivo": str(existente.relative_to(RAIZ)),
                           "criterio": criterio, "identidade_oficial": identidade(doc), "sha256_normalizado": hash_corpo}, ensure_ascii=False).encode())
        return "equivalente"
    fonte = f"https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/{ident}/visao/original"
    meta = {"titulo": doc["epigrafeCompleta"], "orgao": "; ".join(o["nomeOrgao"] for o in ep.get("orgaos", [])),
            "tipo": tipo["nomeTipoAto"], "numero": str(ep.get("numeroAto", "")), "data": ep.get("dataAto", ""),
            "revogada": revogacao(doc)[0], "evidencia_revogacao": revogacao(doc)[1],
            "vigente_fonte": doc.get("vigente") if isinstance(doc.get("vigente"), bool) else None, "versao_texto": "publicação original — visão original da fonte",
            "publicacao": doc.get("dadosPublicacao", ""), "data_publicacao": doc.get("dataPublicacao", ""),
            "fonte": fonte, "fonte_api": url, "fonte_indice": BUSCA, "id_rfb": ident,
            "sha256_texto": hashlib.sha256(corpo.encode()).hexdigest(), "baixado_em": dt.date.today().isoformat()}
    if doc.get("_ocr"):
        meta["ocr"] = "Tesseract português; anexo original preservado na fonte e no cache"
    if doc.get("_ocr_pdf"):
        meta["ocr_pdf"] = "Vision macOS português; todas as páginas do anexo conferidas quanto à presença de texto"
    if doc.get("_anexos_graficos"):
        meta["anexos_graficos"] = "; ".join(doc["_anexos_graficos"])
        meta["observacao_anexos"] = "Anexo gráfico original preservado; OCR parcial não substitui a representação visual"
    cab = "---\n" + "".join(f"{k}: {'null' if v is None else str(v).lower() if isinstance(v, bool) else yaml_str(str(v))}\n" for k, v in meta.items()) + "---\n"
    salvar(path, (cab + "# " + doc["epigrafeCompleta"] + "\n\n" + corpo + "\n").encode())
    EQUIVALENTES.setdefault(hash_corpo, []).append(path)
    METAS[path] = meta
    return "ok"


def auditar_equivalencias():
    class Offline:
        def get(self, *args, **kwargs):
            raise ValueError("cache ausente; auditoria não faz HTTP")
    equivalentes()
    pasta = RAIZ / "_indice" / "sijut" / "equivalentes"
    arquivos = sorted(pasta.glob("*.json"))
    originais = [json.loads(p.read_text()) for p in arquivos]
    snapshot = RAIZ / "_fonte" / "sijut" / "auditorias" / ("equivalencias-originais-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S") + ".json.gz")
    salvar(snapshot, gzip.compress(json.dumps(originais, ensure_ascii=False, indent=2).encode()))
    contagem = {"confirmadas": 0, "recuperadas": 0, "redirecionadas": 0, "pendentes_estrutura": 0, "erros": 0}
    offline = Offline()
    diario = RAIZ / "_equivalencias_auditoria.jsonl"
    for path in arquivos:
        original = json.loads(path.read_text())
        registro = {"id_rfb": original["id_rfb"], "equivalencia_anterior": original}
        try:
            doc = obter(offline, original["fonte_api"])
            corpo = extrair(doc, offline)
            existente, criterio = encontrar_equivalente(doc, corpo)
            anterior = RAIZ / original["arquivo"]
            registro["identidade_oficial"] = identidade(doc)
            registro["metadados_anterior"] = {k: METAS.get(anterior, {}).get(k) for k in ("tipo", "numero", "data", "orgao", "titulo", "fonte")}
            if existente:
                if reter_estrutura(doc, corpo, existente, criterio, original["fonte_api"]):
                    estado = "pendentes_estrutura"
                    registro["motivo"] = "Vínculo textual conservado; integralidade estrutural pendente, canônico preservado."
                else:
                    novo = {"id_rfb": doc["idAto"], "fonte_api": original["fonte_api"], "arquivo": str(existente.relative_to(RAIZ)),
                            "criterio": criterio, "identidade_oficial": identidade(doc), "sha256_normalizado": assinatura(corpo)}
                    salvar(path, json.dumps(novo, ensure_ascii=False).encode())
                    estado = "confirmadas" if existente == anterior else "redirecionadas"
                    registro["arquivo_confirmado"] = novo["arquivo"]
            else:
                rejeitado = pasta.parent / "equivalencias_rejeitadas" / path.name
                salvar(rejeitado, path.read_bytes())
                path.unlink()
                resultado = processar(offline, {"idAto": doc["idAto"], "anoAto": doc["epigrafe"]["dataAto"][:4]})
                if resultado not in ("ok", "skip"):
                    raise ValueError("reparo não criou texto próprio: " + resultado)
                estado = "recuperadas"
                registro["motivo"] = "identidade oficial ou corpo não comprovam equivalência anterior"
                registro["arquivo_recuperado"] = str(Path(doc["epigrafe"]["dataAto"][:4]) / f"rfb-sijut-{doc['idAto']}.md")
            contagem[estado] += 1
            registro["decisao"] = estado
        except Exception as exc:
            contagem["erros"] += 1
            registro.update(decisao="erro", erro=str(exc))
        with diario.open("a") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
        print("equivalência", registro["id_rfb"], registro["decisao"], contagem, flush=True)
    vigencia = auditar_vigencia()
    resultado = {"equivalencias_auditadas": len(arquivos), "contagem": contagem, "vigente_json": vigencia,
                 "snapshot_original": str(snapshot), "diario": str(diario)}
    salvar(RAIZ / "_indice" / "sijut" / "auditoria-equivalencias.json", json.dumps(resultado, ensure_ascii=False, indent=2).encode())
    print("FIM AUDITORIA", resultado, flush=True)
    return int(bool(contagem["erros"]))


def indexar(rede, ate):
    inicio = dt.date(1800, 1, 1)
    fim = dt.datetime.strptime(ate, "%d/%m/%Y").date()
    base = dict(tipoPesquisa="formulario", termo="", tipoData="dataPublicacao", dataInicio=inicio.strftime("%d/%m/%Y"), dataFim=ate,
                anoAto="", numeroAto="", apenasAtosVigentes=False, apenasAtosInternos=False, publicado=True, internet=True,
                orgaosSelecionados="", tiposAtosSelecionados=";".join(map(str, TIPOS)), refino={}, ordenacaoColuna="publicacao",
                ordenacaoDirecao="desc", paginacaoPaginaAtual=1, paginacaoQuantidadePorPagina=100)
    global_ = obter(rede, BUSCA, base)
    total = int(global_["quantidadeTotal"])
    docs = {}
    campos = ("idAto", "numeroAto", "anoAto", "dataAto", "dataPublicacao", "tipoAto", "urlVisualizacao")
    anterior = RAIZ / "_indice" / "sijut" / "indice.json"
    anteriores = json.loads(anterior.read_text()).get("documentos", []) if anterior.exists() else []
    for item in anteriores:
        data = dt.datetime.strptime(item["dataPublicacao"], "%d/%m/%Y").date()
        if inicio <= data <= fim and item["tipoAto"]["idTipoAto"] in TIPOS:
            docs[str(item["idAto"])] = {k: item.get(k) for k in campos}
    partes = []
    estado = {}
    anos_concluidos = 0

    def checkpoint():
        nonlocal estado
        completas = bool(partes) and all(p["completo"] for p in partes)
        estado = {"fonte": BUSCA, "filtros": base, "tipos_incluidos": TIPOS, "total_fonte": total,
                  "documentos_unicos": len(docs), "faltantes_indice": max(0, total-len(docs)),
                  "completo": completas and len(docs) == total and anos_concluidos == fim.year-inicio.year+1,
                  "anos_concluidos": anos_concluidos,
                  "estrategia": "partições anuais inclusivas; mês/dia quando janela supera50000",
                  "particoes": partes, "documentos": list(docs.values())}
        salvar(RAIZ / "_indice" / "sijut" / "indice.json", json.dumps(estado, ensure_ascii=False).encode())

    def intervalo(de, a, nivel):
        payload = {**base, "dataInicio": de.strftime("%d/%m/%Y"), "dataFim": a.strftime("%d/%m/%Y")}
        primeiro = obter(rede, BUSCA, payload)
        esperado = int(primeiro["quantidadeTotal"])
        if esperado > 50000 and de != a:
            if nivel == "ano":
                import calendar
                for mes in range(1, 13):
                    primeiro_dia = dt.date(de.year, mes, 1)
                    ultimo_dia = min(a, dt.date(de.year, mes, calendar.monthrange(de.year, mes)[1]))
                    if primeiro_dia <= ultimo_dia:
                        intervalo(primeiro_dia, ultimo_dia, "mes")
            else:
                dia = de
                while dia <= a:
                    intervalo(dia, dia, "dia")
                    dia += dt.timedelta(days=1)
            return
        parte = {"inicio": de.isoformat(), "fim": a.isoformat(), "total_fonte": esperado, "paginas": int(primeiro["quantidadePaginas"]),
                 "paginas_coletadas": 0, "documentos_unicos": 0, "totais_observados": [esperado], "completo": False}
        partes.append(parte)
        vistos, totais = set(), {esperado}
        paginas = max(1, int(primeiro["quantidadePaginas"]))
        for pagina in range(1, paginas+1):
            payload["paginacaoPaginaAtual"] = pagina
            resposta = primeiro if pagina == 1 else obter(rede, BUSCA, payload)
            totais.add(int(resposta["quantidadeTotal"]))
            anteriores = len(vistos)
            for item in resposta["atos"]:
                data = dt.datetime.strptime(item["dataPublicacao"], "%d/%m/%Y").date()
                if not de <= data <= a or item["tipoAto"]["idTipoAto"] not in TIPOS:
                    raise ValueError(f"ato fora dos filtros declarados: {item['idAto']}")
                ident = str(item["idAto"])
                vistos.add(ident)
                docs[ident] = {k: item.get(k) for k in campos}
            parte.update(paginas_coletadas=pagina, documentos_unicos=len(vistos), totais_observados=sorted(totais))
            if pagina == paginas:
                parte["completo"] = len(vistos) == esperado and len(totais) == 1
            if pagina % 10 == 0 or (pagina == paginas and (esperado > 0 or de.year % 10 == 0)):
                checkpoint()
            if pagina > 1 and len(vistos) == anteriores and esperado > len(vistos):
                parte["motivo"] = "janela de paginação não avança"
                checkpoint()
                break
        print(f"índice {de}..{a}: {len(vistos)}/{esperado}; global{len(docs)}/{total}; completo={parte['completo']}", flush=True)

    for ano in range(inicio.year, fim.year+1):
        intervalo(dt.date(ano, 1, 1), min(fim, dt.date(ano, 12, 31)), "ano")
        anos_concluidos += 1
    checkpoint()
    return estado


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rps", type=float, default=2)
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--auditar-equivalencias", action="store_true")
    ap.add_argument("--auditar-vigencia", action="store_true")
    ap.add_argument("--usar-indice", action="store_true", help="retoma corpos de índice completo já validado, sem HTTP de indexação")
    ap.add_argument("--somente-indice", action="store_true")
    ap.add_argument("--ate", default="15/10/2026")
    args = ap.parse_args()
    if not 0 < args.rps <= 4:
        ap.error("rps deve estar entre0 e4")
    if args.auditar_vigencia:
        auditar_vigencia()
        return 0
    if args.auditar_equivalencias:
        return auditar_equivalencias()
    rede = Rede(args.rps)
    try:
        if args.usar_indice:
            estado = json.loads((RAIZ / "_indice" / "sijut" / "indice.json").read_text())
            if (not estado.get("completo") or estado["filtros"]["dataFim"] != args.ate or estado["tipos_incluidos"] != TIPOS
                    or len({d["idAto"] for d in estado["documentos"]}) != estado["total_fonte"]):
                raise ValueError("índice não está completo ou não corresponde ao recorte solicitado")
        else:
            estado = indexar(rede, args.ate)
    except Exception as exc:
        RAIZ.mkdir(parents=True, exist_ok=True)
        with (RAIZ / "_falhas_sijut.jsonl").open("a") as f:
            f.write(json.dumps({"fonte": "rfb-sijut-indice", "erro": str(exc)}, ensure_ascii=False) + "\n")
        print("erro índice:", exc, flush=True)
        return 1
    if args.somente_indice:
        print("FIM ÍNDICE", estado["documentos_unicos"], "/", estado["total_fonte"], "completo", estado["completo"], flush=True)
        return int(not estado["completo"])
    equivalentes()
    contagem, erros = {"ok": 0, "skip": 0, "equivalente": 0, "pendente_estrutura": 0}, 0
    docs = sorted(estado["documentos"], key=lambda d: (dt.datetime.strptime(d["dataPublicacao"], "%d/%m/%Y").date(), int(d["idAto"])), reverse=True)
    for item in docs:
        try:
            resultado = processar(rede, item)
            contagem[resultado] += 1
            print(resultado, item["idAto"], contagem, flush=True)
        except Exception as exc:
            erros += 1
            with (RAIZ / "_falhas_sijut.jsonl").open("a") as f:
                f.write(json.dumps({"fonte": "rfb-sijut", "idAto": item["idAto"], "erro": str(exc)}, ensure_ascii=False) + "\n")
            print("erro", item["idAto"], str(exc), flush=True)
            if "403" in str(exc) or "401" in str(exc):
                return 1
        if args.limite and sum(contagem.values()) + erros >= args.limite:
            break
    print("FIM", contagem, "erros", erros, "índice completo", estado["completo"], flush=True)
    return int(bool(erros) or not estado["completo"])


if __name__ == "__main__":
    sys.exit(main())
