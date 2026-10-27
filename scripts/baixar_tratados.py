"""Coleta tratados na Receita Federal, TRT2 e PGE-SP, preservando fontes e OCR."""
import argparse
import datetime as dt
import gzip
import hashlib
import html
import http.client
import json
from pathlib import Path
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.parse
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import AVISO_OCR, Rede, decodificar, ocr_pdf, texto_pdf_para_md, yaml_str
from html2md import convert

RAIZ = Path(__file__).resolve().parent.parent / "tratados"
RFB = "https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/legislacao/acordos-internacionais/acordos-para-evitar-a-dupla-tributacao/"
INDICE_RFB = RFB + "acordos-para-evitar-a-dupla-tributacao-e-prevenir-a-evasao-fiscal"
INDICE_OIT = "https://ww2.trt2.jus.br/legislacao/convencoes-da-oit/page"
INDICE_DH = "https://www.pge.sp.gov.br/centrodeestudos/bibliotecavirtual/instrumentos/sumario.htm"
ARTIGO = re.compile(r"\b(?:Art\.?|ARTIGO|Article|Art[íi]culo)\s*(?:\d|[IVXLCDM]+\b)", re.I)


def texto(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def baixar(rede, url):
    chave = hashlib.sha256(url.encode()).hexdigest()
    path = RAIZ / "_fonte" / (chave + ".gz")
    if path.exists():
        return gzip.decompress(path.read_bytes())
    if url.lower().endswith(".pdf"):
        bruto = baixar_pdf(rede, url, path.with_suffix(".part"))
    else:
        st, bruto, _ = rede.get(url, timeout=60)
        if st != 200 or not bruto:
            raise ValueError(f"HTTP {st}: {url}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(gzip.compress(bruto))
    tmp.replace(path)
    return bruto


def baixar_pdf(rede, url, parcial):
    """Retoma PDFs grandes com Range oficial; evita perder tudo em IncompleteRead."""
    parcial.parent.mkdir(parents=True, exist_ok=True)
    offset = parcial.stat().st_size if parcial.exists() else 0
    while True:
        req = urllib.request.Request(url, headers={**rede.headers, "Accept-Encoding": "identity",
                                                   "Range": f"bytes={offset}-{offset + 1048575}"})
        ultimo = None
        for _ in range(3):
            rede.limite.esperar()
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    if r.status == 200 and offset == 0:
                        return r.read()
                    faixa = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", r.headers.get("Content-Range", ""))
                    if r.status != 206 or not faixa or int(faixa[1]) != offset:
                        raise ValueError(f"resposta Range inválida: HTTP {r.status}: {url}")
                    bloco = r.read()
                    if len(bloco) != int(faixa[2]) - offset + 1:
                        raise ValueError(f"bloco PDF incompleto: {url}")
                break
            except urllib.error.HTTPError as e:
                if e.code in (400, 401, 403, 404, 410):
                    raise ValueError(f"HTTP {e.code}: {url}") from e
                ultimo = e
            except (OSError, EOFError, http.client.IncompleteRead) as e:
                ultimo = e
        else:
            raise RuntimeError(f"PDF não pôde ser retomado em {offset}: {url}: {ultimo}")
        with parcial.open("ab") as f:
            f.write(bloco)
        offset += len(bloco)
        if offset == int(faixa[3]):
            bruto = parcial.read_bytes()
            parcial.unlink()
            return bruto


def indice_rfb(rede):
    s = decodificar(baixar(rede, INDICE_RFB))
    docs, vistos = [], set()
    for secao in re.split(r"<h2\b[^>]*>", s)[1:]:
        titulo = texto(secao.split("</h2>", 1)[0])
        for item in re.findall(r"<li\b[^>]*>(.*?)</li>", secao, re.S):
            links = re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', item, re.S)
            rotulo = next((texto(t) for _, t in links if "Decreto" in texto(t)), "")
            for url, _ in links:
                url = html.unescape(url)
                if not url.startswith(RFB) or not url.lower().endswith(".pdf") or url in vistos:
                    continue
                vistos.add(url)
                docs.append({"titulo": f"Acordo de bitributação — {titulo}" + (f" — {rotulo}" if rotulo else ""),
                             "categoria": "bitributacao", "pais": titulo, "url": url, "indice": INDICE_RFB,
                             "ato_promulgacao": rotulo})
    if not docs:
        raise ValueError("índice RFB sem textos PDF")
    return docs


def indice_oit(rede):
    s = decodificar(baixar(rede, INDICE_OIT))
    docs, vistos = [], set()
    for row in re.findall(r"<tr\b[^>]*>(.*?)</tr>", s, re.S):
        celulas = re.findall(r"<td\b[^>]*>(.*?)</td>", row, re.S)
        if len(celulas) < 2:
            continue
        titulo = texto(celulas[0])
        numero = re.match(r"(\d+)\s*-", titulo)
        if not numero or numero[1] in vistos or "Recomendação" in titulo:
            continue
        vistos.add(numero[1])
        url = f"https://trt2.jus.br/geral/tribunal2/LEGIS/CLT/OIT/OIT_{int(numero[1]):03}.html"
        # A Convenção 102 só foi promulgada em 2026 e não existe no arquivo histórico do TRT2.
        if numero[1] == "102":
            atual = re.search(r'href="([^"]+)"', celulas[0])
            if atual:
                url = html.unescape(atual[1])
        docs.append({"titulo": "Convenção OIT nº " + titulo, "categoria": "oit", "numero": numero[1],
                     "url": url,
                     "indice": INDICE_OIT, "situacao_indice": texto(celulas[1])})
    if not docs:
        raise ValueError("índice TRT2 sem convenções")
    return docs


def indice_dh(rede):
    s = decodificar(baixar(rede, INDICE_DH))
    docs = []
    for url, rotulo in re.findall(r'<a\b[^>]*href\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</a>', s, re.I | re.S):
        titulo = texto(rotulo)
        if not titulo.startswith(("Convenção", "Pacto", "Protocolo")):
            continue
        d = {"titulo": titulo, "categoria": "direitos-humanos",
             "url": urllib.parse.urljoin(INDICE_DH, url), "indice": INDICE_DH}
        # O sumário diz 1949; o cabeçalho do próprio texto identifica a Convenção de 1948.
        if url == "genocidio.htm":
            d["titulo_indice"] = titulo
            d["titulo"] = "Convenção para a Prevenção e a Repressão do Crime de Genocídio (1948)"
        docs.append(d)
    return docs


def processar(rede, d):
    slug = Path(urllib.parse.urlparse(d["url"]).path).name.rsplit(".", 1)[0]
    destino = RAIZ / d["categoria"] / (slug + ".md")
    if destino.exists():
        atualizar_metadados(destino, d)
        return "pulado"
    bruto = baixar(rede, d["url"])
    ocr = False
    if bruto.startswith(b"%PDF"):
        pdf = RAIZ / "_fonte" / (hashlib.sha256(d["url"].encode()).hexdigest() + ".pdf")
        if not pdf.exists():
            pdf.write_bytes(bruto)
        r = subprocess.run(["rtk", "proxy", "pdftotext", "-q", "-layout", "-enc", "UTF-8", str(pdf), "-"],
                           capture_output=True, check=True, timeout=60)
        t = r.stdout.decode("utf-8")
        paginas = max(1, t.count("\f"))
        if len(re.sub(r"\W", "", t)) / paginas < 300 or not ARTIGO.search(t):
            t = ocr_pdf(bruto)
            ocr = True
        corpo = texto_pdf_para_md(t)
    else:
        corpo = convert(decodificar(bruto))
    if len(corpo) < 1500 or not ARTIGO.search(corpo):
        raise ValueError(f"texto de tratado insuficiente: {d['url']}")
    tipo = {"oit": "Convenção da OIT", "direitos-humanos": "Tratado de Direitos Humanos"}.get(d["categoria"], "Acordo Internacional")
    valores = {"titulo": d["titulo"], "tipo": tipo, "fonte": d["url"],
               "numero": d.get("numero", ""), "data": "",
               "fonte_indice": d["indice"], "pais": d.get("pais", ""),
               "ato_promulgacao": d.get("ato_promulgacao", ""), "ocr": ocr,
               "baixado_em": dt.date.today().isoformat()}
    if d.get("situacao_indice"):
        valores["situacao_indice"] = d["situacao_indice"]
    if d.get("titulo_indice"):
        valores["titulo_indice"] = d["titulo_indice"]
    valores["versao_texto"] = "transcrição da fonte oficial; inclui referências históricas"
    linhas = ["---"]
    for k, v in valores.items():
        linhas.append(f"{k}: {str(v).lower() if isinstance(v, bool) else v if k == 'baixado_em' else yaml_str(v)}")
    linhas += ["---", "", "# " + d["titulo"], "", (AVISO_OCR if ocr else "") + corpo]
    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_suffix(".tmp")
    tmp.write_text("\n".join(linhas), encoding="utf-8")
    tmp.replace(destino)
    return "ok"


def atualizar_metadados(destino, d):
    s = destino.read_text(encoding="utf-8")
    partes = s.split("---", 2)
    if len(partes) != 3:
        raise ValueError(f"frontmatter inválido: {destino}")
    cab = partes[1]
    valores = {"numero": d.get("numero", ""), "data": "",
               "versao_texto": "transcrição da fonte oficial; inclui referências históricas"}
    for chave, valor in valores.items():
        if not re.search(r"^" + chave + ":", cab, re.M):
            cab += f"{chave}: {yaml_str(valor)}\n"
    if cab != partes[1]:
        tmp = destino.with_suffix(".tmp")
        tmp.write_text("---" + cab + "---" + partes[2], encoding="utf-8")
        tmp.replace(destino)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rps", type=float, default=2)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--fonte", choices=("rfb", "oit", "direitos-humanos"), default="rfb")
    a = ap.parse_args()
    if not 0 < a.rps <= 4 or a.workers < 1:
        ap.error("rps deve estar entre 0 e 4; workers deve ser positivo")
    rede = Rede(a.rps)
    docs = {"rfb": indice_rfb, "oit": indice_oit, "direitos-humanos": indice_dh}[a.fonte](rede)
    indice = RAIZ / "_indice"
    indice.mkdir(parents=True, exist_ok=True)
    (indice / (a.fonte + ".json")).write_text(json.dumps(docs, ensure_ascii=False), encoding="utf-8")
    if a.limite:
        docs = docs[:a.limite]
    cont = {"ok": 0, "pulado": 0, "erro": 0}
    with ThreadPoolExecutor(a.workers) as ex, (RAIZ / "_falhas.jsonl").open("a", encoding="utf-8") as falhas:
        futs = {ex.submit(processar, rede, d): d for d in docs}
        for n, fut in enumerate(as_completed(futs), 1):
            try:
                cont[fut.result()] += 1
            except Exception as e:
                cont["erro"] += 1
                falhas.write(json.dumps({**futs[fut], "fonte": a.fonte, "erro": str(e)}, ensure_ascii=False) + "\n")
                falhas.flush()
                if "HTTP 403" in str(e):
                    for pendente in futs:
                        pendente.cancel()
                    raise
            print(f"Tratados {n}/{len(docs)} {cont}", flush=True)
    return 1 if cont["erro"] else 0


if __name__ == "__main__":
    sys.exit(main())
