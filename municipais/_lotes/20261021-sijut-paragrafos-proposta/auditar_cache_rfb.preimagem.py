"""Audita lotes SIJUT a partir do JSON oficial em cache, sem fazer HTTP.

O arquivo de entrada e o baseline são congelados; nenhuma norma é reescrita.
Texto, identidade, catálogo, tabelas e prova de revogação precisam coincidir.
"""
import argparse
import base64
import collections
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import baixar_rfb as rfb
from auditar import validar
from metadados_lotes import carregar as carregar_headers

RAIZ = Path(__file__).resolve().parent.parent


class Offline:
    def get(self, *args, **kwargs):
        raise ValueError("anexo ausente no cache; HTTP não autorizado na auditoria")


def pendencia_visual(doc):
    for segmento in doc.get('ementas', []) + doc.get('outrosSegmentos', []):
        if segmento.get('omitir') or not segmento.get('original'):
            continue
        if re.search(r'<(?:img|svg|canvas|object|embed|iframe|math|v:\w+|m:oMath)\b', segmento.get('textoIntegra', ''), re.I):
            return 'elemento visual no segmento exige conferência própria'
        anexo = segmento.get('arquivoBinario') or {}
        if anexo.get('idTipoArquivo') in (2, 6):
            return 'anexo imagem/PDF exige conferência visual e paginação própria'
        if anexo.get('idTipoArquivo') in (4, 5) and anexo.get('arquivoBinario'):
            conteudo = base64.b64decode(anexo['arquivoBinario'], validate=True).decode('utf-8')
            if re.search(r'<(?:img|svg|canvas|object|embed|iframe|math|v:\w+|m:oMath)\b', conteudo, re.I):
                return 'elemento visual em anexo HTML exige conferência própria'
    return None


def chave(meta):
    return tuple(rfb.normalizar(meta.get(k, "")) for k in ("orgao", "tipo", "numero", "data"))


def auditar(path, indice, identidades, urls, hoje):
    raw = path.read_bytes()
    texto = raw.decode()
    nome = str(path.relative_to(RAIZ))
    erros, avisos = validar(texto, nome, hoje)
    if erros:
        raise ValueError("; ".join(erros))
    meta, corpo = rfb.metadados_md(texto)
    ident = int(meta["id_rfb"])
    if ident not in indice:
        raise ValueError("ID ausente do catálogo oficial congelado")
    url = rfb.CORPO + str(ident) + "/visao/original"
    if meta.get("fonte_api") != url:
        raise ValueError("URL da API diverge do ID")
    cache = rfb.RAIZ / "_fonte/sijut" / (hashlib.sha256(url.encode()).hexdigest() + ".json.gz")
    fonte = gzip.decompress(cache.read_bytes())
    doc = json.loads(fonte)
    if doc.get("idAto") != ident:
        raise ValueError("ID do texto diverge do catálogo")
    pendencia = pendencia_visual(doc)
    if pendencia:
        raise ValueError(pendencia)
    extraido = rfb.extrair(doc, Offline())
    if re.match(r"^\s*(?:Retifica[çc][ãa]o|Onde se l[êe])\b", extraido, re.I):
        raise ValueError("visão contém apenas retificação; exige classificação própria")
    if corpo != "\n# " + doc["epigrafeCompleta"] + "\n\n" + extraido + "\n":
        raise ValueError("corpo difere da reextração integral da API")
    if meta.get("sha256_texto") != hashlib.sha256(extraido.encode()).hexdigest():
        raise ValueError("hash do texto extraído diverge do cabeçalho")
    original = rfb.identidade(doc)
    expected = {"titulo": doc["epigrafeCompleta"], "tipo": original["tipo"],
                "numero": original["numero"], "data": original["data"],
                "orgao": "; ".join(original["orgaos"]),
                "data_publicacao": doc.get("dataPublicacao", ""),
                "publicacao": doc.get("dadosPublicacao", "")}
    for k, v in expected.items():
        if str(meta.get(k, "")) != str(v):
            raise ValueError("metadado difere da API: " + k)
    for campo_item, campo_meta in (("dataAto", "data"), ("numeroAto", "numero"), ("anoAto", None)):
        item = indice[ident].get(campo_item)
        if item is not None and campo_meta and str(item) != str(meta[campo_meta]):
            # O catálogo utiliza DD/MM/AAAA; o JSON do texto utiliza ISO.
            if campo_item == "dataAto" and re.fullmatch(r"\d{2}/\d{2}/\d{4}", str(item)):
                item = dt.datetime.strptime(item, "%d/%m/%Y").date().isoformat()
            if str(item) != str(meta[campo_meta]):
                raise ValueError("identidade diverge do catálogo: " + campo_item)
    revogada, prova = rfb.revogacao(doc)
    if meta.get("revogada") != revogada or meta.get("evidencia_revogacao") != prova:
        raise ValueError("revogação difere da prova explícita da API")
    if meta.get("vigente_fonte") != doc.get("vigente"):
        raise ValueError("vigente_fonte difere do JSON oficial")
    identity = chave(meta)
    if not all(identity):
        raise ValueError("identidade incompleta")
    if identity in identidades or meta["fonte"] in urls:
        raise ValueError("identidade/URL já presente no index ou lote")
    if "<table" in extraido and rfb.estrutura_tabelas(corpo) != rfb.estrutura_tabelas(extraido):
        raise ValueError("estrutura de tabelas divergente")
    return {"path": nome, "id_rfb": ident, "fonte": meta["fonte"], "fonte_api": url,
            "cache": str(cache.relative_to(RAIZ)), "sha256_fonte": hashlib.sha256(fonte).hexdigest(),
            "sha256_md": hashlib.sha256(raw).hexdigest(), "sha256_texto": meta["sha256_texto"],
            "identidade": original, "revogada": revogada, "evidencia_revogacao": prova,
            "tabelas": extraido.count("<table"), "avisos": avisos}, meta


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--candidatos", required=True)
    ap.add_argument("--manifesto", required=True)
    ap.add_argument("--lista", required=True)
    ap.add_argument("--limite", type=int, default=2000)
    ap.add_argument("--reservados", action="append", default=[], help="listas congeladas de lotes anteriores ainda em publicação")
    args = ap.parse_args()
    baseline = Path(args.baseline).read_bytes()
    headers = carregar_headers(RAIZ, baseline)
    tracked = set(baseline.decode().split("\0"))
    reservas = {}
    for lista in args.reservados:
        raw = Path(lista).read_bytes()
        reservas[lista] = hashlib.sha256(raw).hexdigest()
        for p in raw.decode().splitlines():
            if p.startswith("reguladores/") and p.endswith(".md"):
                tracked.add(p)
                with (RAIZ / p).open() as f:
                    meta, _ = rfb.metadados_md(f.read(16384))
                headers.append({"path": p, "meta": meta})
    estado_path = rfb.RAIZ / "_indice/sijut/indice.json"
    estado_raw = estado_path.read_bytes()
    estado = json.loads(estado_raw)
    if not estado.get("completo") or len({d["idAto"] for d in estado["documentos"]}) != estado["total_fonte"]:
        raise ValueError("catálogo oficial incompleto ou com IDs repetidos")
    indice = {int(d["idAto"]): d for d in estado["documentos"]}
    identidades, urls = set(), set()
    for registro in headers:
        if not registro["path"].startswith("reguladores/rfb/"):
            continue
        meta = registro["meta"]
        identidades.add(chave(meta))
        urls.add(meta.get("fonte"))
    rows, retidos, motivos = [], [], collections.Counter()
    hoje = dt.datetime.now(ZoneInfo("America/Recife")).date()
    for nome in json.loads(Path(args.candidatos).read_text()):
        if nome in tracked or "/rfb-sijut-" not in nome:
            continue
        try:
            row, meta = auditar(RAIZ / nome, indice, identidades, urls, hoje)
            rows.append(row)
            identidades.add(chave(meta))
            urls.add(meta["fonte"])
        except Exception as exc:
            motivo = str(exc)
            motivos[motivo.split(":")[0]] += 1
            retidos.append({"path": nome, "motivo": motivo})
        if len(rows) >= args.limite:
            break
        if (len(rows) + len(retidos)) % 100 == 0:
            print(len(rows), "aceitos", len(retidos), "retidos", flush=True)
    manifest = RAIZ / args.manifesto
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps({"data": str(hoje), "origem": "JSON oficial em cache; sem HTTP ou reescrita do corpus",
                                    "baseline_sha256": hashlib.sha256(baseline).hexdigest(), "reservas_sha256": reservas,
                                    "indice_sha256": hashlib.sha256(estado_raw).hexdigest(),
                                    "total_indice": estado["total_fonte"], "total": len(rows),
                                    "documentos": rows, "retidos": retidos, "motivos": motivos}, ensure_ascii=False, indent=2) + "\n")
    Path(args.lista).write_text("\n".join(r["path"] for r in rows) + "\n" + str(manifest.relative_to(RAIZ)) + "\n")
    print("FIM", len(rows), "aceitos", len(retidos), "retidos", dict(motivos), flush=True)


if __name__ == "__main__":
    main()
