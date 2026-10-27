"""Baixa do Planalto os documentos que o índice do Senado não alcança.

Duas famílias, ambas fora do serviço `legislacao/lista` do Senado:

- **as constituições anteriores a 1988**, que não são "normas" no índice e só existem como páginas
  próprias do Portal da Legislação;
- **os regulamentos consolidados** — RIR, RIPI, Regulamento Aduaneiro, RPS e afins. Esses até são
  decretos e entram pelo índice, mas o texto que importa é o compilado que o Planalto mantém, com
  as alterações já embutidas: é por ele que se trabalha, não pela publicação original.

Cada documento é declarado em DOCUMENTOS, com o caminho de destino e os metadados que a página não
traz em forma legível por máquina. Retomável: pula o que já existe. O HTML original fica em
`federal/_fonte/planalto/`.

    python3 -I scripts/baixar_planalto.py                # tudo que falta
    python3 -I scripts/baixar_planalto.py --refazer      # regrava mesmo o que já existe
"""
import argparse
import datetime as dt
import gzip
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import Limitador, decodificar  # noqa: E402
from html2md import convert  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "federal"))
BASE = "https://www.planalto.gov.br/ccivil_03/"
UA = "Mozilla/5.0 (compatible; constituicao-md/1.0)"

# (pasta, nome do arquivo, URL relativa ao ccivil_03, título, tipo, número, data, ementa)
DOCUMENTOS = [
    ("constituicoes-historicas", "constituicao-1824", "constituicao/constituicao24.htm",
     "Constituição Política do Império do Brasil de 1824", "Constituição", "", "1824-03-25",
     "Constituição Política do Império do Brasil, outorgada em 25 de março de 1824."),
    ("constituicoes-historicas", "constituicao-1891", "constituicao/constituicao91.htm",
     "Constituição da República dos Estados Unidos do Brasil de 1891", "Constituição", "", "1891-02-24",
     "Constituição da República dos Estados Unidos do Brasil, de 24 de fevereiro de 1891."),
    ("constituicoes-historicas", "constituicao-1934", "constituicao/constituicao34.htm",
     "Constituição da República dos Estados Unidos do Brasil de 1934", "Constituição", "", "1934-07-16",
     "Constituição da República dos Estados Unidos do Brasil, de 16 de julho de 1934."),
    ("constituicoes-historicas", "constituicao-1937", "constituicao/constituicao37.htm",
     "Constituição dos Estados Unidos do Brasil de 1937", "Constituição", "", "1937-11-10",
     "Constituição dos Estados Unidos do Brasil, de 10 de novembro de 1937."),
    ("constituicoes-historicas", "constituicao-1946", "constituicao/constituicao46.htm",
     "Constituição dos Estados Unidos do Brasil de 1946", "Constituição", "", "1946-09-18",
     "Constituição dos Estados Unidos do Brasil, de 18 de setembro de 1946."),
    ("constituicoes-historicas", "constituicao-1967", "constituicao/constituicao67.htm",
     "Constituição da República Federativa do Brasil de 1967", "Constituição", "", "1967-01-24",
     "Constituição da República Federativa do Brasil, de 24 de janeiro de 1967."),
    ("constituicoes-historicas", "constituicao-1967-emenda-1-1969", "constituicao/constituicao67emc69.htm",
     "Constituição da República Federativa do Brasil de 1967, com a redação da Emenda Constitucional nº 1 de 1969",
     "Constituição", "", "1969-10-17",
     "Texto constitucional de 1967 com a redação dada pela Emenda Constitucional nº 1, de 17 de outubro de 1969."),

    ("regulamentos", "rir-decreto-9580-2018", "_ato2015-2018/2018/decreto/d9580.htm",
     "Regulamento do Imposto de Renda — Decreto nº 9.580 de 22/11/2018", "Decreto", "9580", "2018-11-22",
     "Regulamenta a tributação, a fiscalização, a arrecadação e a administração do Imposto sobre a Renda e Proventos de Qualquer Natureza."),
    ("regulamentos", "ripi-decreto-7212-2010", "_ato2007-2010/2010/decreto/d7212.htm",
     "Regulamento do IPI — Decreto nº 7.212 de 15/06/2010", "Decreto", "7212", "2010-06-15",
     "Regulamenta a cobrança, fiscalização, arrecadação e administração do Imposto sobre Produtos Industrializados - IPI."),
    ("regulamentos", "regulamento-aduaneiro-decreto-6759-2009", "_ato2007-2010/2009/decreto/d6759.htm",
     "Regulamento Aduaneiro — Decreto nº 6.759 de 05/02/2009", "Decreto", "6759", "2009-02-05",
     "Regulamenta a administração das atividades aduaneiras e a fiscalização, o controle e a tributação das operações de comércio exterior."),
    ("regulamentos", "rps-decreto-3048-1999", "decreto/d3048.htm",
     "Regulamento da Previdência Social — Decreto nº 3.048 de 06/05/1999", "Decreto", "3048", "1999-05-06",
     "Aprova o Regulamento da Previdência Social e dá outras providências."),
    ("regulamentos", "processo-administrativo-fiscal-decreto-70235-1972", "decreto/d70235cons.htm",
     "Processo Administrativo Fiscal — Decreto nº 70.235 de 06/03/1972 (texto consolidado)",
     "Decreto", "70235", "1972-03-06",
     "Dispõe sobre o processo administrativo fiscal e dá outras providências."),
    ("regulamentos", "riof-decreto-6306-2007", "_ato2007-2010/2007/decreto/d6306.htm",
     "Regulamento do IOF — Decreto nº 6.306 de 14/12/2007", "Decreto", "6306", "2007-12-14",
     "Regulamenta o Imposto sobre Operações de Crédito, Câmbio e Seguro, ou relativas a Títulos ou Valores Mobiliários - IOF."),
    ("regulamentos", "ritr-decreto-4382-2002", "decreto/2002/d4382.htm",
     "Regulamento do ITR — Decreto nº 4.382 de 19/09/2002", "Decreto", "4382", "2002-09-19",
     "Regulamenta a tributação, fiscalização, arrecadação e administração do Imposto sobre a Propriedade Territorial Rural - ITR."),
    ("regulamentos", "pis-cofins-decreto-4524-2002", "decreto/2002/d4524.htm",
     "Regulamento do PIS/Pasep e da Cofins — Decreto nº 4.524 de 17/12/2002", "Decreto", "4524", "2002-12-17",
     "Regulamenta a Contribuição para o PIS/Pasep e a Cofins devidas pelas pessoas jurídicas em geral."),
    ("regulamentos", "processo-administrativo-fiscal-decreto-7574-2011", "_ato2011-2014/2011/decreto/d7574.htm",
     "Regulamento do Processo Administrativo Fiscal — Decreto nº 7.574 de 29/09/2011", "Decreto", "7574", "2011-09-29",
     "Regulamenta o processo de determinação e de exigência de créditos tributários da União, o processo de consulta sobre a aplicação da legislação tributária federal, e outros processos que especifica."),
    ("regulamentos", "riispoa-decreto-9013-2017", "_ato2015-2018/2017/decreto/d9013.htm",
     "Regulamento da Inspeção Industrial e Sanitária de Produtos de Origem Animal — Decreto nº 9.013 de 29/03/2017", "Decreto", "9013", "2017-03-29",
     "Regulamenta a inspeção industrial e sanitária de produtos de origem animal."),
    ("regulamentos", "mineracao-decreto-9406-2018", "_ato2015-2018/2018/decreto/d9406.htm",
     "Regulamento do Código de Mineração — Decreto nº 9.406 de 12/06/2018", "Decreto", "9406", "2018-06-12",
     "Regulamenta o Decreto-Lei nº 227, de 28 de fevereiro de 1967, e as leis sobre exploração mineral que especifica."),
    ("regulamentos", "produtos-controlados-decreto-10030-2019", "_ato2019-2022/2019/decreto/d10030.htm",
     "Regulamento de Produtos Controlados — Decreto nº 10.030 de 30/09/2019", "Decreto", "10030", "2019-09-30",
     "Aprova o Regulamento de Produtos Controlados."),
    ("regulamentos", "agricultura-organica-decreto-6323-2007", "_ato2007-2010/2007/decreto/d6323.htm",
     "Regulamento da Agricultura Orgânica — Decreto nº 6.323 de 27/12/2007", "Decreto", "6323", "2007-12-27",
     "Regulamenta a Lei nº 10.831, de 23 de dezembro de 2003, que dispõe sobre a agricultura orgânica."),
    ("regulamentos", "sementes-mudas-decreto-10586-2020", "_ato2019-2022/2020/decreto/d10586.htm",
     "Regulamento do Sistema Nacional de Sementes e Mudas — Decreto nº 10.586 de 18/12/2020", "Decreto", "10586", "2020-12-18",
     "Regulamenta a Lei nº 10.711, de 5 de agosto de 2003, que dispõe sobre o Sistema Nacional de Sementes e Mudas."),
    ("regulamentos", "produtos-vegetais-decreto-12709-2025", "_ato2023-2026/2025/decreto/d12709.htm",
     "Regulamento de Fiscalização de Produtos de Origem Vegetal — Decreto nº 12.709 de 31/10/2025", "Decreto", "12709", "2025-10-31",
     "Regulamenta a fiscalização de produtos de origem vegetal, incluindo vinhos, bebidas e classificação vegetal."),
    ("regulamentos", "alimentacao-animal-decreto-12031-2024", "_ato2023-2026/2024/decreto/d12031.htm",
     "Regulamento da Inspeção e Fiscalização de Produtos para Alimentação Animal — Decreto nº 12.031 de 28/05/2024", "Decreto", "12031", "2024-05-28",
     "Regulamenta a inspeção e a fiscalização obrigatórias dos produtos destinados à alimentação animal."),
    ("regulamentos", "defesa-sanitaria-animal-decreto-24548-1934", "decreto/1930-1949/d24548.htm",
     "Regulamento do Serviço de Defesa Sanitária Animal — Decreto nº 24.548 de 03/07/1934", "Decreto", "24548", "1934-07-03",
     "Aprova o Regulamento do Serviço de Defesa Sanitária Animal."),
    ("regulamentos", "defesa-sanitaria-vegetal-decreto-24114-1934", "decreto/1930-1949/d24114.htm",
     "Regulamento de Defesa Sanitária Vegetal — Decreto nº 24.114 de 12/04/1934", "Decreto", "24114", "1934-04-12",
     "Aprova o Regulamento de Defesa Sanitária Vegetal."),
    ("regulamentos", "biosseguranca-decreto-5591-2005", "_ato2004-2006/2005/decreto/d5591.htm",
     "Regulamento de Biossegurança — Decreto nº 5.591 de 22/11/2005", "Decreto", "5591", "2005-11-22",
     "Regulamenta dispositivos da Lei nº 11.105, de 24 de março de 2005, sobre biossegurança."),
    ("regulamentos", "suasa-decreto-5741-2006", "_ato2004-2006/2006/decreto/d5741.htm",
     "Regulamento do Sistema Unificado de Atenção à Sanidade Agropecuária — Decreto nº 5.741 de 30/03/2006", "Decreto", "5741", "2006-03-30",
     "Regulamenta os arts. 27-A, 28-A e 29-A da Lei nº 8.171, de 17 de janeiro de 1991, e organiza o Sistema Unificado de Atenção à Sanidade Agropecuária."),
]


def yaml_str(v):
    return json.dumps(v if v is not None else "", ensure_ascii=False)


def baixar(limite, pasta, nome, rel, titulo, tipo, numero, data, ementa, refazer):
    md = os.path.join(RAIZ, pasta, data[:4], nome + ".md")
    if os.path.exists(md) and not refazer:
        return "pulado"
    url = BASE + rel
    limite.esperar()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=180) as r:
        bruto = r.read()
        ct = r.headers.get("Content-Type") or ""

    fonte = os.path.join(RAIZ, "_fonte", "planalto", nome + ".html.gz")
    os.makedirs(os.path.dirname(fonte), exist_ok=True)
    with gzip.open(fonte, "wb") as f:
        f.write(bruto)

    corpo = convert(decodificar(bruto, ct))
    if not re.search(r"\bArt(?:igo)?\.?\s*\d", corpo, re.I):
        raise ValueError(f"fonte sem corpo normativo extraível: {url}")
    historica = pasta == "constituicoes-historicas"
    revogada = historica or bool(re.search(r"Revogad[oa]\s+pel[oa]\s+(?:Decreto|Lei)", corpo.split("Art. 1", 1)[0], re.I))
    cab = ["---", f"titulo: {yaml_str(titulo)}", f"tipo: {yaml_str(tipo)}", f"numero: {yaml_str(numero)}",
           f"data: {data}", f"ementa: {yaml_str(ementa)}", f"revogada: {'true' if revogada else 'false'}",
           f"versao_texto: {yaml_str('texto histórico' if revogada else 'compilada (texto vigente)')}", f"fonte: {yaml_str(url)}",
           f"baixado_em: {dt.date.today().isoformat()}", "---", ""]
    os.makedirs(os.path.dirname(md), exist_ok=True)
    tmp = md + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(cab) + f"# {titulo}\n\n" + corpo)
    os.replace(tmp, md)
    return "ok"


def extrair_anexos(html, url, rede):
    import hashlib
    import subprocess
    import tempfile
    import urllib.parse
    from html import unescape
    from pathlib import Path
    from comum import OCR_BIN, AVISO_OCR, texto_pdf_para_md
    links = re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>\s*Download\s+para\s+(?:o\s+)?anexo\s*</a>', html, re.I)
    if not links:
        raise ValueError("anexo externo sem link reconhecível")
    partes, fontes, usou_ocr = [], [], False
    for href in dict.fromkeys(links):
        fonte = urllib.parse.urljoin(url, unescape(href))
        if urllib.parse.urlparse(fonte).hostname != "www.planalto.gov.br" or not fonte.lower().endswith(".pdf"):
            raise ValueError("formato ou fonte de anexo não suportados: " + fonte)
        chave = hashlib.sha256(fonte.encode()).hexdigest()
        cache = Path(RAIZ) / "_fonte/planalto-pendencias" / (chave + ".pdf.gz")
        if cache.exists():
            bruto = gzip.decompress(cache.read_bytes())
        else:
            status, bruto, _ = rede.get(fonte, timeout=45, tentativas=1)
            if status != 200 or not bruto.startswith(b"%PDF"):
                raise ValueError(f"anexo PDF inválido HTTP {status}: {fonte}")
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_bytes(gzip.compress(bruto))
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "anexo.pdf"
            pdf.write_bytes(bruto)
            proc = subprocess.run(["rtk", "proxy", "pdftotext", "-q", "-layout", "-enc", "UTF-8", str(pdf), "-"], capture_output=True, timeout=60, check=True)
            texto = proc.stdout.decode("utf-8")
            paginas = max(1, texto.count("\f"))
            aviso = ""
            if len(texto.strip()) < 200:
                ocr_cache = cache.with_name(chave + ".ocr.txt.gz")
                if ocr_cache.exists():
                    texto = gzip.decompress(ocr_cache.read_bytes()).decode("utf-8")
                else:
                    proc = subprocess.run(["rtk", "proxy", OCR_BIN, str(pdf)], capture_output=True, timeout=1800, check=True)
                    texto = proc.stdout.decode("utf-8")
                    ocr_cache.write_bytes(gzip.compress(texto.encode()))
                usou_ocr, aviso = True, AVISO_OCR
            extraidas = [p for p in texto.split("\f") if p.strip()]
            if len(extraidas) < paginas or any(len(p.strip()) < 80 for p in extraidas) or "\x00" in texto:
                raise ValueError("anexo sem texto suficiente em todas as páginas: " + fonte)
        partes.append("## Anexo\n\n" + aviso + texto_pdf_para_md(texto))
        fontes.append(fonte)
    return "\n\n".join(partes), fontes, usou_ocr


def complementar_pendencias(rps, maximo=0, tipos=None):
    import hashlib
    import unicodedata
    import urllib.parse
    from html import unescape
    from pathlib import Path
    from comum import Rede
    from baixar_federal import carregar_indice, montar, numero_oficial
    rede = Rede(rps)
    tipos = tipos or {"LEI-n", "LCP"}
    lct_urls = {}
    indice_lct = BASE + "LEIS/LCT/Quadro_Lct.htm"
    if "LCT" in tipos:
        cache = Path(RAIZ) / "_fonte" / "planalto-pendencias" / (hashlib.sha256(indice_lct.encode()).hexdigest() + ".html.gz")
        if cache.exists():
            bruto = gzip.decompress(cache.read_bytes())
        else:
            status, bruto, _ = rede.get(indice_lct, timeout=45, tentativas=2)
            if status != 200:
                raise ValueError(f"HTTP {status}: {indice_lct}")
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_bytes(gzip.compress(bruto))
        for href in re.findall(r'href=["\']([^"\']+)["\']', decodificar(bruto), re.I):
            match = re.search(r"LCT(\d+)\.htm$", href, re.I)
            if match:
                lct_urls[str(int(match[1]))] = urllib.parse.urljoin(indice_lct, href)
    alvos = []
    for d in carregar_indice(tipos):
        info = montar(d)
        if Path(info["md"]).exists():
            continue
        ano = int(info["data"][:4])
        numero = d["numero"] + ("-" + d["complemento"].lower() if d.get("complemento") else "")
        if d["tipo"] == "LCT":
            if d["numero"] not in lct_urls:
                raise ValueError("LCT do índice primário ausente do índice Planalto: " + d["norma"])
            rel = lct_urls[d["numero"]].removeprefix(BASE)
        elif d["tipo"] == "LCP":
            rel = "leis/lcp/lcp01-62.htm" if d["numero"] == "1" and ano == 1962 else f"leis/lcp/lcp{numero}.htm"
        elif ano >= 2004:
            inicio = ((ano - 2003) // 4) * 4 + 2003
            rel = (f"_ato2004-2006/{ano}/lei/l{numero}.htm" if ano <= 2006 else f"_ato{inicio}-{inicio + 3}/{ano}/lei/l{numero}.htm")
        elif 1970 <= ano <= 2003:
            rel = f"leis/{ano}/l{numero}.htm" if ano >= 2001 else f"leis/l{numero}.htm"
        elif 1950 <= ano <= 1969:
            rel = f"leis/1950-1969/l{numero}.htm"
        elif 1930 <= ano <= 1949:
            rel = f"leis/1930-1949/l{d['numero'].zfill(4)}" + ("-" + d["complemento"].lower() if d.get("complemento") else "") + ".htm"
        else:
            continue
        alvos.append((d, info, BASE + rel))
    alvos.sort(key=lambda x: x[1]["data"], reverse=True)
    if maximo:
        alvos = alvos[:maximo]
    cont = {"ok": 0, "erro": 0}
    meses = ["janeiro", "fevereiro", "marco", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    for d, info, url in alvos:
        try:
            cache = Path(RAIZ) / "_fonte" / "planalto-pendencias" / (hashlib.sha256(url.encode()).hexdigest() + ".html.gz")
            if cache.exists():
                bruto = gzip.decompress(cache.read_bytes())
                ct = ""
            else:
                status, bruto, ct = rede.get(url, timeout=45, tentativas=2)
                if status != 200:
                    raise ValueError(f"HTTP {status}: {url}")
                cache.parent.mkdir(parents=True, exist_ok=True)
                cache.write_bytes(gzip.compress(bruto))
            html = decodificar(bruto, ct)
            html = re.sub(r"<(?:style|script)\b[^>]*>.*?</(?:style|script)>", "", html, flags=re.I | re.S)
            texto = unescape(re.sub(r"<[^>]+>", " ", html))
            normal = re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", texto.lower()))
            ano, mes, dia = map(int, info["data"].split("-"))
            numero = d["numero"] + (d.get("complemento", "").lower())
            identidade = rf"lei(?:complementar|constitucional)?(?:no?)?{numero}de0?{dia}de{meses[mes-1]}de{ano}"
            excecao_lct4 = (d["tipo"] == "LCT" and d["numero"] == "4" and info["data"] == "1940-09-20"
                            and re.search(r"leino?4de18desetembrode1940", normal) and "riodejaneiro20desetembrode1940" in normal)
            if not re.search(identidade, normal) and not excecao_lct4:
                raise ValueError("número/data do título oficial não conferem com índice")
            anexos, fontes_anexos, ocr_anexos = "", [], False
            if re.search(r"Download\s+para\s+(?:o\s+)?anexo", texto, re.I):
                anexos, fontes_anexos, ocr_anexos = extrair_anexos(html, url, rede)
            cabeca = re.split(r"\bArt(?:igo)?\.?\s*1\b", texto, maxsplit=1, flags=re.I)[0]
            revogada = bool(re.search(r"Revogad[oa]\s+pel[oa]\s+(?:Decreto|Lei)", cabeca, re.I))
            if revogada:
                html = re.sub(r"</?(?:strike|del|s)\b[^>]*>", "", html, flags=re.I)
                html = re.sub(r"text-decoration\s*:\s*line-through", "", html, flags=re.I)
            corpo = convert(html) + ("\n\n" + anexos if anexos else "")
            if "\x00" in corpo or len(corpo) < 150 or (not re.search(r"\bArt(?:igo)?[*.\s]{0,8}(?:\d|[úu]nico)", corpo, re.I)
                               and not (excecao_lct4 and re.search(r"Par[áa]grafo\s+[úu]nico", corpo, re.I))):
                raise ValueError("fonte sem corpo normativo extraível")
            valores = {"titulo": d["normaNome"], "tipo": info["nome"], "numero": numero_oficial(d), "data": info["data"],
                       "ementa": d.get("ementa", ""), "revogada": revogada, "versao_texto": "texto histórico da fonte oficial" if revogada else "texto da fonte oficial",
                       "urn": info["urn"], "fonte": url, "id_senado": d["id"], "baixado_em": dt.date.today().isoformat()}
            if fontes_anexos:
                valores["fontes_anexos"] = "; ".join(fontes_anexos)
                if ocr_anexos:
                    valores["ocr"] = "Anexo PDF escaneado; OCR Vision; original preservado"
            if d["tipo"] == "LCT":
                valores["fonte_indice"] = indice_lct
            if excecao_lct4:
                valores["observacao_fonte"] = "Cabeçalho Planalto: Lei nº 4 de 18/9/1940; índice oficial LCT, fecho e publicação indicam 20/9/1940. Corpo preservado."
            cab = "---\n" + "".join(f"{k}: {str(v).lower() if isinstance(v, bool) else yaml_str(v)}\n" for k, v in valores.items()) + "---\n"
            path = Path(info["md"])
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_suffix(".tmp")
            tmp.write_text(cab + "# " + d["normaNome"] + "\n\n" + corpo + "\n")
            tmp.replace(path)
            cont["ok"] += 1
            print("ok", info["slug"], flush=True)
        except Exception as exc:
            cont["erro"] += 1
            with open(os.path.join(RAIZ, "_falhas_planalto.jsonl"), "a") as f:
                f.write(json.dumps({"fonte": url, "norma": d["norma"], "urn": info["urn"], "erro": str(exc)}, ensure_ascii=False) + "\n")
            print("erro", info["slug"], str(exc), flush=True)
            if "403" in str(exc) or "401" in str(exc):
                break
    print("FIM PENDENCIAS", cont, flush=True)
    return int(bool(cont["erro"]))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tipos", default="LEI-n,LCP")
    ap.add_argument("--pendencias", action="store_true")
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--refazer", action="store_true")
    ap.add_argument("--rps", type=float, default=1, help="o Planalto é lento e não gosta de pressa")
    a = ap.parse_args()
    if a.pendencias:
        return complementar_pendencias(a.rps, a.limite, set(a.tipos.split(",")))
    limite = Limitador(a.rps)
    cont = {"ok": 0, "pulado": 0, "erro": 0}
    for doc in DOCUMENTOS:
        try:
            st = baixar(limite, *doc, refazer=a.refazer)
        except Exception as e:
            st = "erro"
            print(f"  erro em {doc[1]}: {str(e)[:120]}", flush=True)
            with open(os.path.join(RAIZ, "_falhas_planalto.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps({"fonte": BASE + doc[2], "documento": doc[1], "erro": str(e)}, ensure_ascii=False) + "\n")
        cont[st] += 1
        print(f"{st:7} {doc[0]}/{doc[1]}", flush=True)
    print("FIM", cont)
    return 1 if cont["erro"] else 0


if __name__ == "__main__":
    sys.exit(main())
