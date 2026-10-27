"""Monta os índices de `federal/_indice/` a partir dos dados abertos do Senado.

O serviço aceita um tipo e um ano por chamada (`legislacao/lista?tipo=X&ano=Y`) e devolve no máximo
o que couber na resposta — por isso o índice é montado ano a ano e só depois juntado num arquivo
por tipo, no mesmo formato `ListaDocumento` que `baixar_federal.py` já lê.

Cada par (tipo, ano) é gravado em `federal/_indice/_anos/TIPO-ANO.json` antes de ser juntado. Isso
torna o processo retomável: rodar de novo só busca os anos que faltam. Um ano sem norma grava uma
lista vazia, para não ser pedido de novo.

    python3 -I scripts/indice_federal.py                      # todos os tipos, 1808–hoje
    python3 -I scripts/indice_federal.py --tipos EMC,DEC       # só alguns
    python3 -I scripts/indice_federal.py --refazer             # ignora o cache de anos
    python3 -I scripts/indice_federal.py --de 2026 --refazer   # atualiza2026 e preserva anos anteriores

O parâmetro `tipo` casa por prefixo: `DEC` devolve `DEC-n` (numerado) e `DEC-sn` (não numerado),
`MPV` devolve `MPV-ss`. A separação em pastas acontece depois, em `baixar_federal.py`.
"""
import argparse
import datetime as dt
import json
import gzip
import hashlib
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import Limitador  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "federal"))
INDICE = os.path.join(RAIZ, "_indice")
CACHE = os.path.join(INDICE, "_anos")
LISTA = "https://legis.senado.leg.br/dadosabertos/legislacao/lista?tipo={}&ano={}"
UA = "Mozilla/5.0 (compatible; constituicao-md/1.0)"

# Tipos do serviço do Senado, com o primeiro ano em que a série existe — pedir anos anteriores é
# só desperdício de requisição. O ano vem da própria série: a primeira EC é de 1969 na Constituição
# de 1967 (as de 1988 em diante são a série atual, mas o serviço devolve as duas), a primeira MP é
# de 1988, as resoluções do Senado começam no Império.
TIPOS = {
    "LEI": 1808, "LCP": 1967, "LDL": 1962, "LCT": 1937, "DEL": 1937,
    "EMC": 1969, "EMR": 1994, "DEC": 1889, "DLG": 1891, "DPL": 1889,
    "MPV": 1988, "RSF": 1826, "RCN": 1891, "RRC": 1994, "AILEI": 1889,
}


def http_json(url, limite, tentativas=4):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json",
                                               "Accept-Encoding": "identity"})
    ultimo = None
    for n in range(tentativas):
        limite.esperar()
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                corpo = r.read()
            return json.loads(corpo) if corpo.strip() else {}
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 429):
                raise RuntimeError(f"fonte recusou HTTP {e.code}: {url}") from e
            if e.code in (400, 404):
                return {}
            ultimo = e
        except Exception as e:
            ultimo = e
        time.sleep(3 * (n + 1) ** 2)
    raise RuntimeError(f"falhou após {tentativas} tentativas: {url}: {ultimo}")


def documentos(resposta):
    """Normaliza a resposta: ausente vira lista vazia, documento único vira lista de um."""
    docs = (resposta.get("ListaDocumento") or {}).get("documentos")
    if not docs:
        return []
    docs = docs.get("documento")
    if not docs:
        return []
    return docs if isinstance(docs, list) else [docs]


def buscar_ano(tipo, ano, limite, refazer):
    caminho = os.path.join(CACHE, f"{tipo}-{ano}.json")
    if os.path.exists(caminho) and not refazer:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f), True
    resposta = http_json(LISTA.format(tipo, ano), limite)
    docs = documentos(resposta)
    if not isinstance(resposta, dict) or (resposta and "ListaDocumento" not in resposta):
        raise ValueError(f"resposta sem estrutura ListaDocumento: {tipo}/{ano}")
    evidencia = os.path.join(CACHE, "_fontes", f"{tipo}-{ano}-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S") + ".json.gz")
    os.makedirs(os.path.dirname(evidencia), exist_ok=True)
    with gzip.open(evidencia, "wt", encoding="utf-8") as f:
        json.dump({"fonte": LISTA.format(tipo, ano), "consultado_em": dt.datetime.now().isoformat(), "resposta": resposta}, f, ensure_ascii=False)
    if os.path.exists(caminho):
        snapshot(caminho, tipo + "-" + str(ano))
    os.makedirs(CACHE, exist_ok=True)
    tmp = caminho + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False)
    os.replace(tmp, caminho)
    return docs, False


def snapshot(caminho, nome):
    bruto = open(caminho, "rb").read()
    pasta = os.path.join(INDICE, "_snapshots")
    os.makedirs(pasta, exist_ok=True)
    destino = os.path.join(pasta, nome + "-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + hashlib.sha256(bruto).hexdigest()[:12] + ".json.gz")
    with gzip.open(destino, "wb") as f:
        f.write(bruto)
    return destino


def ano_documento(doc):
    return str(doc.get("dataassinatura", ""))[-4:]


def gravar_indice(tipo, docs, anos=None):
    """Grava no formato ListaDocumento que `baixar_federal.carregar_indice` espera."""
    caminho = os.path.join(INDICE, f"{tipo}.json")
    anteriores, preservados = [], []
    anos = {str(a) for a in anos} if anos is not None else None
    copia = None
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8") as f:
            anteriores = documentos(json.load(f))
        copia = snapshot(caminho, tipo)
        if anos is not None:
            preservados = [d for d in anteriores if ano_documento(d) not in anos]
    novos = {d["id"]: d for d in docs}
    anteriores_recorte = {d["id"]: d for d in anteriores if anos is None or ano_documento(d) in anos}
    auditoria = {"tipo": tipo, "anos_consultados": sorted(anos or []), "snapshot_anterior": copia,
                 "historicos_preservados": len(preservados), "recorte_anterior": len(anteriores_recorte), "recorte_atual": len(novos),
                 "adicionados": sorted(set(novos) - set(anteriores_recorte)), "retirados_da_fonte": sorted(set(anteriores_recorte) - set(novos)),
                 "alterados": sorted(i for i in set(novos) & set(anteriores_recorte) if novos[i] != anteriores_recorte[i])}
    docs = preservados + docs
    # a mesma norma pode aparecer em mais de um ano quando a fonte corrige a data; o id é único
    unicos, vistos = [], set()
    for d in docs:
        if d.get("id") in vistos:
            continue
        vistos.add(d["id"])
        unicos.append(d)
    unicos.sort(key=lambda d: (d.get("dataassinatura", "")[6:], d.get("dataassinatura", "")[3:5],
                               d.get("dataassinatura", "")[:2], d.get("id", "")))
    saida = {
        "ListaDocumento": {
            "noNamespaceSchemaLocation": "https://legis.senado.leg.br/dadosabertos/dados/ListaDocumentov3.xsd",
            "Metadados": {"Versao": dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "VersaoServico": "3",
                          "DescricaoDataSet": f"Índice de {tipo}, montado por scripts/indice_federal.py", "AtualizacaoIncremental": auditoria},
            "documentos": {"documento": unicos},
        }
    }
    caminho = os.path.join(INDICE, f"{tipo}.json")
    tmp = caminho + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False)
    os.replace(tmp, caminho)
    relatorio = os.path.join(INDICE, "_snapshots", tipo + "-atualizacao-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S") + ".json")
    os.makedirs(os.path.dirname(relatorio), exist_ok=True)
    with open(relatorio, "w", encoding="utf-8") as f:
        json.dump(auditoria, f, ensure_ascii=False, indent=2)
    return len(unicos)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tipos", default="", help="lista separada por vírgula; vazio = todos")
    ap.add_argument("--de", type=int, default=0, help="ano inicial; vazio = o primeiro de cada série")
    ap.add_argument("--ate", type=int, default=dt.date.today().year)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--rps", type=float, default=3)
    ap.add_argument("--refazer", action="store_true", help="ignora o cache por ano e busca tudo de novo")
    a = ap.parse_args()

    if not 0 < a.rps <= 4 or a.workers <= 0:
        ap.error("rps deve ser positivo e no máximo4; workers deve ser positivo")
    if a.ate > dt.date.today().year or (a.de and a.de > a.ate):
        ap.error("intervalo de anos inválido")
    tipos = [t.strip().upper() for t in a.tipos.split(",") if t.strip()] or list(TIPOS)
    desconhecidos = [t for t in tipos if t not in TIPOS]
    if desconhecidos:
        ap.error(f"tipo não conhecido: {', '.join(desconhecidos)}. Conhecidos: {', '.join(TIPOS)}")

    limite = Limitador(a.rps)
    os.makedirs(INDICE, exist_ok=True)
    for tipo in tipos:
        anos = range(max(a.de or TIPOS[tipo], TIPOS[tipo]), a.ate + 1)
        docs, cache, inicio = [], 0, time.time()
        with ThreadPoolExecutor(a.workers) as ex:
            futs = {ex.submit(buscar_ano, tipo, ano, limite, a.refazer): ano for ano in anos}
            for n, fut in enumerate(as_completed(futs), 1):
                do_ano, veio_do_cache = fut.result()
                docs += do_ano
                cache += veio_do_cache
                if n % 25 == 0:
                    print(f"  {tipo}: {n}/{len(futs)} anos, {len(docs)} normas", flush=True)
        total = gravar_indice(tipo, docs, anos)
        print(f"{tipo}: {total} normas em {len(anos)} anos ({cache} do cache, "
              f"{time.time() - inicio:.0f}s) -> _indice/{tipo}.json", flush=True)


if __name__ == "__main__":
    main()
