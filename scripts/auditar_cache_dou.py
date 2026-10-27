"""Prepara lotes do cache DOU sem rede nem alterações nos documentos.

Valida publicação, órgão, título, corpo integral e tabelas contra o HTML oficial.
Retém publicações com múltiplas epígrafes ou identidade já publicada. Não afirma
vigência nem confunde ausência de erro de formato com integralidade jurídica.
"""
import argparse
import collections
import datetime as dt
import gzip
import hashlib
import html
import json
from pathlib import Path
import re
import sys
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar import validar
from baixar_dou import assinatura_do_ato, pendencia_integralidade
from comum import normalizar_chave
from html2md import convert
from representacao_html_dou import representar_fragmento
from metadados_lotes import carregar as carregar_headers

RAIZ = Path(__file__).resolve().parent.parent


def meta_corpo(texto):
    cab, corpo = texto[4:].split("\n---\n", 1)
    meta = {}
    for linha in cab.splitlines():
        chave, valor = linha.split(":", 1)
        valor = valor.strip()
        try:
            meta[chave] = json.loads(valor)
        except ValueError:
            meta[chave] = valor
    return meta, corpo


def identidade(meta):
    return tuple(normalizar_chave(str(meta.get(k, ""))) for k in ("orgao", "tipo", "numero", "data"))


def campo_html(texto, classe):
    m = re.search(r'<span\b[^>]*class=["\']' + re.escape(classe) + r'["\'][^>]*>(.*?)</span>', texto, re.S)
    if not m:
        raise ValueError("campo HTML ausente: " + classe)
    return html.unescape(re.sub(r"<[^>]+>", "", m[1])).strip()


def conferir(path, existentes, urls, hoje, bruto_md=None, fonte_bytes=None):
    # Permite validar uma proposta em memória antes de substituir um arquivo.
    if bruto_md is None:
        bruto_md = path.read_bytes()
    texto = bruto_md.decode("utf-8")
    nome = str(path.relative_to(RAIZ))
    erros, avisos = validar(texto, nome, hoje)
    if erros:
        raise ValueError("; ".join(erros))
    meta, corpo = meta_corpo(texto)
    if not str(meta["fonte"]).startswith("https://www.in.gov.br/web/dou/-/"):
        raise ValueError("fonte fora do DOU")
    if meta["fonte"] in urls:
        raise ValueError("URL da publicação já presente no index/lote")
    chave = identidade(meta)
    if all(chave) and chave in existentes:
        raise ValueError("identidade órgão/tipo/número/data já presente no index/lote")
    if meta.get("revogada") is not None:
        raise ValueError("vigência sem evidência: campo revogada deve ser null")
    sha = meta.get("sha256_html_fonte")
    if not re.fullmatch(r"[0-9a-f]{64}", str(sha or "")):
        raise ValueError("snapshot imutável sem SHA-256 registrado")
    partes = path.relative_to(RAIZ).parts
    cache = RAIZ / "reguladores/_fonte" / partes[1] / partes[3] / (path.stem + "-" + sha + ".html.gz")
    fonte = gzip.decompress(cache.read_bytes()) if fonte_bytes is None else fonte_bytes
    if hashlib.sha256(fonte).hexdigest() != sha:
        raise ValueError("SHA-256 do HTML divergente")
    source = fonte.decode("utf-8")
    pub = dt.datetime.strptime(campo_html(source, "publicado-dou-data"), "%d/%m/%Y").date().isoformat()
    if pub != meta.get("data_publicacao"):
        raise ValueError("publicação diverge do HTML")
    if campo_html(source, "orgao-dou-data") != meta.get("orgao"):
        raise ValueError("órgão diverge do HTML")
    if campo_html(source, "edicao-dou-data") != str(meta.get("edicao")):
        raise ValueError("edição diverge do HTML")
    m = re.search(r'<div[^>]+class="[^\"]*texto-dou[^\"]*".*?</div>\s*(?=<div|</section|</main)', source, re.S)
    if not m:
        raise ValueError("bloco texto-dou ausente")
    fragmento = m[0]
    if len(re.findall(r'<div\b', fragmento, re.I)) != len(re.findall(r'</div\s*>', fragmento, re.I)):
        raise ValueError('bloco texto-dou não fechado; possível truncamento exige revisão estrutural')
    if re.search(r"<(?:img|svg|canvas|object|embed|iframe|math|v:\w+|m:oMath)\b", fragmento, re.I):
        raise ValueError("elemento visual exige revisão")
    titulos = re.findall(r'<p\b[^>]*class=["\']identifica["\'][^>]*>(.*?)</p>', fragmento, re.S)
    titulos = [html.unescape(re.sub(r"<[^>]+>", "", t)).strip() for t in titulos]
    if len(titulos) != 1:
        raise ValueError("epígrafes próprias múltiplas/ausentes: " + str(len(titulos)))
    if normalizar_chave(titulos[0]) != normalizar_chave(meta["titulo"]):
        raise ValueError("epígrafe própria diverge do título cadastrado")
    if re.match(r"^(retifica|despacho|extrato|aviso|edital|comunicado|apostila)", normalizar_chave(titulos[0])):
        raise ValueError("tipo fora do recorte normativo")
    convertido = convert(fragmento)
    representado = (representar_fragmento(fragmento, modo=meta["representacao_corpo"])
                   if "representacao_corpo" in meta else convertido)
    if corpo != "# " + meta["titulo"] + "\n\n" + representado:
        raise ValueError("corpo diverge da reconversão integral do HTML")
    if pendencia_integralidade(convertido):
        raise ValueError("íntegra externa pendente")
    assinatura = assinatura_do_ato(meta["titulo"], convertido)
    if assinatura and assinatura > pub:
        raise ValueError("assinatura posterior à publicação")
    if (assinatura or "") != (meta.get("data") or ""):
        raise ValueError("data de assinatura não reproduzível")
    if assinatura is None:
        raise ValueError("assinatura inconclusiva exige revisão individual")
    return {"path": nome, "sha256_md": hashlib.sha256(bruto_md).hexdigest(),
            "fonte": meta["fonte"], "cache": str(cache.relative_to(RAIZ)),
            "sha256_html": sha, "data": assinatura, "publicacao": pub,
            "identidade": list(chave), "tabelas": convertido.count("<table"),
            "avisos_formato": avisos}, meta


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--candidatos", required=True, help="JSON com paths relativos")
    ap.add_argument("--baseline", required=True, help="git ls-files -z congelado")
    ap.add_argument("--manifesto", required=True)
    ap.add_argument("--lista", required=True)
    ap.add_argument("--limite", type=int, default=2000)
    ap.add_argument("--reservados", action="append", default=[], help="listas congeladas de lotes anteriores ainda em publicação")
    args = ap.parse_args()
    baseline_raw = (RAIZ / args.baseline).read_bytes()
    baseline = baseline_raw.decode().split("\0")
    headers = carregar_headers(RAIZ, baseline_raw)
    reservas = {}
    for lista in args.reservados:
        raw = Path(lista).read_bytes()
        reservas[lista] = hashlib.sha256(raw).hexdigest()
        for p in raw.decode().splitlines():
            if p.startswith("reguladores/") and p.endswith(".md"):
                baseline.append(p)
                with (RAIZ / p).open() as f:
                    meta, _ = meta_corpo(f.read(16384))
                headers.append({"path": p, "meta": meta})
    tracked = set(baseline)
    existentes, urls = set(), set()
    for registro in headers:
        meta = registro["meta"]
        chave = identidade(meta)
        if all(chave):
            existentes.add(chave)
        urls.add(meta.get("fonte"))
    aceitos, retidos, motivos = [], [], collections.Counter()
    hoje = dt.datetime.now(ZoneInfo("America/Recife")).date()
    for nome in json.loads((RAIZ / args.candidatos).read_text()):
        if nome in tracked:
            continue
        try:
            registro, meta = conferir(RAIZ / nome, existentes, urls, hoje)
            aceitos.append(registro)
            existentes.add(identidade(meta))
            urls.add(meta["fonte"])
        except (ValueError, OSError, KeyError, EOFError) as exc:
            motivo = str(exc)
            motivos[motivo.split(":")[0]] += 1
            retidos.append({"path": nome, "motivo": motivo})
        if len(aceitos) >= args.limite:
            break
        if (len(aceitos) + len(retidos)) % 100 == 0:
            print(len(aceitos), "aceitos", len(retidos), "retidos", flush=True)
    manifesto = RAIZ / args.manifesto
    manifesto.parent.mkdir(parents=True, exist_ok=True)
    manifesto.write_text(json.dumps({"data": str(hoje), "baseline_sha256": hashlib.sha256(baseline_raw).hexdigest(), "reservas_sha256": reservas,
                                     "origem": "cache preexistente; sem rede ou alteração no corpus",
                                     "total": len(aceitos), "documentos": aceitos,
                                     "retidos": retidos, "motivos": motivos}, ensure_ascii=False, indent=2) + "\n")
    (RAIZ / args.lista).write_text("\n".join(r["path"] for r in aceitos) + "\n" + str(manifesto.relative_to(RAIZ)) + "\n")
    print("FIM", len(aceitos), "aceitos", len(retidos), "retidos", dict(motivos), flush=True)


if __name__ == "__main__":
    main()
