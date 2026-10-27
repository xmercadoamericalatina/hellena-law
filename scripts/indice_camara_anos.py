"""Indexa decretos legislativos da Câmara por ano, preservando o catálogo amplo."""
import argparse
import datetime as dt
import gzip
import hashlib
import json
import math
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import baixar_camara as camara
from comum import Rede


def pagina(rede, numero, ano, ordem="data:DESC"):
    try:
        return camara.pagina(rede, numero, "dlg", {"ano": ano, "ordenacao": ordem})
    except ValueError as exc:
        if not str(exc).startswith("busca vazia:"):
            raise
        url = camara.BUSCA + "?" + urllib.parse.urlencode(
            {"tipo": camara.TIPOS["dlg"][0], "ordenacao": ordem, "pagina": numero, "ano": ano})
        fonte = camara.obter(rede, url)
        if re.search(r"Exibindo resultados de\s+0\s+a\s+0\s+de\s+0\b", fonte):
            return 0, []
        raise


def indice_ano(rede, ano, pasta):
    path = pasta / f"{ano}.json"
    if path.exists():
        anterior = json.loads(path.read_text())
        if anterior.get("completo"):
            return anterior
    documentos, totais, vistos = [], set(), set()
    consultadas = {}
    for ordem in ("data:DESC", "data:ASC"):
        numero, paginas = 1, 1
        while numero <= paginas:
            total, lote = pagina(rede, numero, ano, ordem)
            totais.add(total)
            paginas = max(1, math.ceil(total / 20))
            if paginas > 500:
                raise ValueError(f"ano {ano} supera janela de500 páginas; subdivisão necessária")
            for doc in lote:
                ident = camara.id_camara(doc)
                if not ident or camara.identificar(doc, "dlg")["data"][:4] != str(ano):
                    raise ValueError(f"documento sem ID ou fora do ano {ano}: {doc['url']}")
                if ident not in vistos:
                    vistos.add(ident)
                    documentos.append({**doc, "id_camara": ident})
            consultadas[ordem] = numero
            completo = len(totais) == 1 and len(vistos) == total and (numero == paginas or ordem == "data:ASC")
            estado = {"ano": ano, "total_fonte": total, "totais_observados": sorted(totais),
                      "paginas_coletadas": sum(consultadas.values()), "paginas_por_ordenacao": dict(consultadas),
                      "documentos_unicos": len(vistos), "documentos": documentos, "completo": completo,
                      "consulta": {"tipo": camara.TIPOS["dlg"][0], "ano": ano},
                      "verificado_em": dt.datetime.now().isoformat()}
            camara.gravar_json(path, estado)
            if completo:
                return estado
            numero += 1

    return estado


def coletar_textos(rede, docs):
    cont = {"ok": 0, "pulado": 0, "erro": 0}
    for doc in docs:
        try:
            cont[camara.processar(rede, doc, "dlg")] += 1
        except Exception as exc:
            cont["erro"] += 1
            with (camara.RAIZ / "_falhas_camara.jsonl").open("a") as f:
                f.write(json.dumps({**doc, "fonte": "dlg", "erro": str(exc)}, ensure_ascii=False) + "\n")
            if any(c in str(exc) for c in ("HTTP 401", "HTTP 403", "HTTP 429", "bloqueio da fonte")):
                raise
        print("texto", camara.id_camara(doc), cont, flush=True)
    print("FIM TEXTOS", cont, flush=True)
    return int(bool(cont["erro"]))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--de", type=int, default=1808)
    ap.add_argument("--ate", type=int, default=dt.date.today().year)
    ap.add_argument("--rps", type=float, default=2)
    ap.add_argument("--somente-indice", action="store_true")
    ap.add_argument("--usar-indice", action="store_true")
    args = ap.parse_args()
    if not 0 < args.rps <= 4 or not 1808 <= args.de <= args.ate <= dt.date.today().year:
        ap.error("intervalo de anos ou rps inválido")
    rede = Rede(args.rps)
    pasta = camara.RAIZ / "_indice/camara-dlg-anos"
    master = camara.RAIZ / "_indice/camara-dlg/indice.json"
    if args.usar_indice:
        estado = json.loads(master.read_text())
        if not estado.get("completo") or len({camara.id_camara(d) for d in estado["documentos"]}) != estado["total_fonte"]:
            ap.error("índice anual ainda não está completo")
        return coletar_textos(rede, estado["documentos"])
    anterior_bruto = master.read_bytes() if master.exists() else b"{}"
    anterior = json.loads(anterior_bruto)
    snapshot = camara.RAIZ / "_fonte/auditorias" / ("camara-dlg-antes-particoes-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S") + ".json.gz")
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    snapshot.write_bytes(gzip.compress(anterior_bruto))
    total, _ = camara.pagina(rede, 1, "dlg")
    docs = {camara.id_camara(d): d for d in anterior.get("documentos", [])}
    partes, erros = [], []
    for ano in range(args.ate, args.de - 1, -1):
        try:
            parte = indice_ano(rede, ano, pasta)
            partes.append({k: v for k, v in parte.items() if k != "documentos"})
            for doc in parte["documentos"]:
                docs[camara.id_camara(doc)] = doc
        except Exception as exc:
            erro = {"fonte": "camara-dlg-ano", "ano": ano, "erro": str(exc)}
            erros.append(erro)
            with (camara.RAIZ / "_falhas_camara.jsonl").open("a") as f:
                f.write(json.dumps(erro, ensure_ascii=False) + "\n")
            print("erro", erro, flush=True)
            if any(c in str(exc) for c in ("HTTP 401", "HTTP 403", "HTTP 429", "bloqueio da fonte")):
                return 1
        ids_particoes = set()
        soma = 0
        for p in pasta.glob("[0-9][0-9][0-9][0-9].json"):
            j = json.loads(p.read_text())
            if j.get("completo"):
                soma += j["total_fonte"]
                ids_particoes.update(camara.id_camara(d) for d in j["documentos"])
        cobertura = args.de == 1808 and args.ate == dt.date.today().year
        completo = (cobertura and len(partes) == args.ate - args.de + 1 and not erros
                    and all(p["completo"] for p in partes) and soma == len(ids_particoes) == len(docs) == total)
        estado = {"fonte": camara.BUSCA, "total_fonte": total, "documentos_unicos": len(docs),
                  "faltantes_indice": max(0, total - len(docs)), "excedentes_indice": max(0, len(docs) - total),
                  "completo": completo, "estado": "completo" if completo else "parcial",
                  "estrategia": "partições anuais; catálogo amplo preservado por ID",
                  "snapshot_anterior": str(snapshot), "sha256_snapshot": hashlib.sha256(anterior_bruto).hexdigest(),
                  "anos_solicitados": [args.de, args.ate], "particoes": partes, "erros": erros,
                  "soma_totais_particoes_completas": soma, "ids_unicos_particoes_completas": len(ids_particoes),
                  "documentos": list(docs.values())}
        camara.gravar_json(master, estado)
        print("ano", ano, "global", len(docs), "/", total, "partições", len(partes), "completo", completo, flush=True)
    if not args.somente_indice:
        return coletar_textos(rede, docs.values()) or int(not estado["completo"])
    return int(bool(erros) or not estado["completo"])


if __name__ == "__main__":
    sys.exit(main())
