"""Decretos do Poder Legislativo no índice oficial do Planalto, sem duplicar a URN do Senado."""
import argparse
import datetime as dt
import gzip
import hashlib
import html
import json
from pathlib import Path
import re
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(Path(__file__).resolve().parent))
from baixar_camara import equivalencias, gravar_json
from comum import Rede, decodificar, yaml_str
from html2md import convert
from identidade_decreto import extrair_epigrafe_decreto, numero_normalizado

RAIZ = Path(__file__).resolve().parent.parent / "federal"
CACHE = RAIZ / "_fonte" / "dpl-planalto"
INDICE = "https://www.planalto.gov.br/ccivil_03/decreto/historicos/dpl/_dpl-ano.htm"


def obter(rede, url, path):
    if path.exists():
        return gzip.decompress(path.read_bytes())
    st, bruto, _ = rede.get(url, timeout=60)
    if st != 200 or not bruto:
        raise ValueError(f"HTTP {st}: {url}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(gzip.compress(bruto))
    tmp.replace(path)
    return bruto


def texto(s):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def indice(rede):
    s = decodificar(obter(rede, INDICE, CACHE / "indice.html.gz"))
    docs, vistos = [], set()
    for row in re.findall(r"<tr\b[^>]*>(.*?)</tr>", s, re.I | re.S):
        celulas = re.findall(r"<td\b[^>]*>(.*?)</td>", row, re.I | re.S)
        if not celulas:
            continue
        for href, rotulo in re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', celulas[0], re.I | re.S):
            if not re.match(r"DPL.*\.htm$", href, re.I):
                continue
            titulo = texto(rotulo)
            data = re.search(r"\bde\s+(\d{1,2})[ºo°]?[./](\d{1,2})[./](\d{4})", titulo, re.I)
            if not data:
                raise ValueError(f"data ausente do índice: {titulo}")
            dia, mes, ano = map(int, data.groups())
            num = re.search(r"n[ºo°]\s*([\d.]+(?:\s*-\s*[a-z]|[a-z])?)", titulo, re.I)
            numero = re.sub(r"\s+", "", num[1].replace(".", "")).lower() if num else ""
            numero = re.sub(r"^(\d+)([a-z])$", r"\1-\2", numero)
            url = urllib.parse.urljoin(INDICE, href)
            if url in vistos:
                continue
            vistos.add(url)
            docs.append({"titulo": titulo, "numero": numero, "data": dt.date(ano, mes, dia).isoformat(),
                         "ementa": texto(celulas[-1]) if len(celulas) > 1 else "", "url": url})
    if not docs:
        raise ValueError("índice Planalto sem DPL reconhecíveis")
    return docs


def conferir_epigrafe(d, corpo):
    """Recusa conflito explícito entre a epígrafe própria e o cadastro do índice."""
    epigrafe = extrair_epigrafe_decreto(corpo)
    if epigrafe and (epigrafe["data"] != d["data"] or
                     epigrafe["numero"] != numero_normalizado(d["numero"])):
        raise ValueError("Epígrafe própria diverge do índice Planalto: " +
                         json.dumps(epigrafe, ensure_ascii=False))


def processar(rede, d):
    urn = f"urn:lex:br:federal:decreto.legislativo:{d['data']};{d['numero']}" if d["numero"] else ""
    iguais = equivalencias("dpl").get(urn, []) if urn else []
    if iguais:
        info = next((i for i in iguais if Path(i["md"]).exists()), iguais[0])
        destino = Path(info["md"])
    else:
        slug = f"dpl-{d['numero'] or 'sn'}-{d['data']}"
        destino = RAIZ / "decretos-legislativos" / d["data"][:4] / (slug + ".md")
    if destino.exists():
        return "pulado"
    fonte = CACHE / (hashlib.sha256(d["url"].encode()).hexdigest() + ".html.gz")
    bruto = obter(rede, d["url"], fonte)
    s = decodificar(bruto)
    cab = texto(s[:20000])
    revogada = bool(re.search(r"Revogad[oa]\s+pel[oa]\s+(?:Decreto|Lei)", cab, re.I))
    # Em atos revogados, preserva o texto histórico que o portal exibe integralmente riscado.
    if revogada:
        s = re.sub(r"</?(?:strike|del|s)\b[^>]*>", "", s, flags=re.I)
        s = re.sub(r"text-decoration\s*:\s*line-through", "", s, flags=re.I)
    corpo = convert(s)
    conferir_epigrafe(d, corpo)
    historico_integral = (d["data"] in ("1827-10-15", "1821-05-26") and len(corpo) > 800
                          and re.search(r"(?:tenha o seu devido cumprimento|Com as rubricas dos Membros da Regencia)", corpo, re.I))
    if not re.search(r"\bArt(?:igo)?\.?\s*(?:\d|[úu]nico)", corpo, re.I) and not historico_integral:
        raise ValueError(f"fonte sem artigos extraíveis: {d['url']}")
    valores = {"titulo": d["titulo"], "tipo": "Decreto do Poder Legislativo", "numero": d["numero"],
               "data": d["data"], "ementa": d["ementa"], "revogada": revogada,
               "versao_texto": "texto histórico da fonte oficial", "fonte": d["url"],
               "fonte_indice": INDICE, "baixado_em": dt.date.today().isoformat()}
    if urn:
        valores["urn"] = urn
    linhas = ["---"]
    for chave, valor in valores.items():
        linhas.append(f"{chave}: {str(valor).lower() if isinstance(valor, bool) else valor if chave in ('data', 'baixado_em') else yaml_str(valor)}")
    linhas += ["---", "", "# " + d["titulo"], "", corpo]
    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_suffix(".tmp")
    tmp.write_text("\n".join(linhas), encoding="utf-8")
    tmp.replace(destino)
    return "ok"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rps", type=float, default=1)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--limite", type=int, default=0)
    a = ap.parse_args()
    if not 0 < a.rps <= 4 or a.workers < 1:
        ap.error("rps deve estar entre 0 e 4; workers deve ser positivo")
    rede = Rede(a.rps)
    docs = indice(rede)
    gravar_json(RAIZ / "_indice" / "planalto-dpl" / "indice.json", {"fonte": INDICE, "documentos": docs})
    if a.limite:
        docs = docs[:a.limite]
    cont = {"ok": 0, "pulado": 0, "erro": 0}
    with ThreadPoolExecutor(a.workers) as ex, (RAIZ / "_falhas_dpl_planalto.jsonl").open("a", encoding="utf-8") as falhas:
        futs = {ex.submit(processar, rede, d): d for d in docs}
        for n, fut in enumerate(as_completed(futs), 1):
            try:
                cont[fut.result()] += 1
            except Exception as e:
                cont["erro"] += 1
                falhas.write(json.dumps({**futs[fut], "erro": str(e)}, ensure_ascii=False) + "\n")
                falhas.flush()
                if "HTTP 403" in str(e):
                    for pendente in futs:
                        pendente.cancel()
                    raise
            print(f"DPL Planalto {n}/{len(docs)} {cont}", flush=True)
    return 1 if cont["erro"] else 0


if __name__ == "__main__":
    sys.exit(main())
