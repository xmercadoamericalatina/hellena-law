"""Fila sequencial retomável de SAPLs descobertos no catálogo oficial SIGI."""
import argparse
import collections
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime as dt
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from urllib.parse import urlsplit

RAIZ = Path(__file__).resolve().parent.parent

def guardar_resultado(arq, estado, item, resultado):
    resultado.update({"codigo_ibge": item["codigo_ibge"], "verificado_em": dt.datetime.now().isoformat()})
    estado[item["url"]] = resultado
    tmp = arq.with_suffix(".tmp")
    tmp.write_text(json.dumps(estado, ensure_ascii=False))
    tmp.replace(arq)
    print(item["municipio"], resultado["estado"], flush=True)


def executar_host(host, itens, modo, pasta):
    resultados = []
    logs = pasta / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    with (logs / (modo + "-" + host + ".log")).open("a") as log:
        for item in itens:
            log.write(f"\nFONTE {host} IBGE {item['codigo_ibge']}\n")
            log.flush()
            r = subprocess.run([sys.executable, "-I", str(RAIZ / "scripts/baixar_organicas_sapl.py"),
                                "--descobrir", host, "--rps", "1", "--modo", modo], stdout=log, stderr=log)
            resultados.append((item, {"estado": "execução concluída" if r.returncode == 0 else "execução parcial; revisar falhas",
                                      "exit_code": r.returncode, "url": item["url"]}))
    return resultados


def executar_paralelo(candidatos, arq, estado, args, pasta):
    grupos = collections.defaultdict(list)
    selecionados = 0
    for item in candidatos:
        if item["url"] in estado:
            continue
        u = urlsplit(item["url"] if "://" in item["url"] else "https://" + item["url"])
        if u.path.strip("/") or not u.hostname or not u.hostname.endswith(".leg.br"):
            guardar_resultado(arq, estado, item, {"estado": "requer adaptador para URL oficial", "url": item["url"]})
            continue
        if args.limite_fontes and selecionados >= args.limite_fontes:
            break
        grupos[u.hostname].append(item)
        selecionados += 1
    # Um trabalho por host mantém aliases do mesmo servidor em sequência.
    with ThreadPoolExecutor(max_workers=args.trabalhadores) as executor:
        futuros = {executor.submit(executar_host, host, itens, args.modo, pasta): itens
                   for host, itens in grupos.items()}
        for futuro in as_completed(futuros):
            try:
                resultados = futuro.result()
            except Exception as e:
                resultados = [(item, {"estado": "execução parcial; falha da fila", "erro": str(e),
                                      "exit_code": 1, "url": item["url"]}) for item in futuros[futuro]]
            for item, resultado in resultados:
                guardar_resultado(arq, estado, item, resultado)
    return int(any(x.get("exit_code", 0) != 0 or "adaptador" in x["estado"] for x in estado.values()))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--trabalhadores", type=int, default=1, help="1 a 4 hosts distintos; cada host a 1 rps")
    ap.add_argument("--modo", choices=["organicas", "legislacao"], default="organicas")
    ap.add_argument("--aguardar-pid", type=int)
    ap.add_argument("--limite-fontes", type=int, default=0)
    a = ap.parse_args()
    if not 1 <= a.trabalhadores <= 4:
        ap.error("trabalhadores deve estar entre 1 e 4")
    if a.limite_fontes < 0:
        ap.error("limite deve ser não negativo")
    if a.aguardar_pid:
        while True:
            try:
                os.kill(a.aguardar_pid, 0)
            except ProcessLookupError:
                break
            time.sleep(5)
    pasta = RAIZ / "municipais/_indice/organicas-sapl"
    pasta.mkdir(parents=True, exist_ok=True)
    trava = (pasta / "fila.lock").open("a")
    try:
        fcntl.flock(trava, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        ap.error("já existe fila SAPL em execução")
    if a.modo == "legislacao":
        sys.path.insert(0, str(RAIZ / "scripts"))
        from plano import PLANO
        for categoria in ("decretos-legislativos", "resolucoes"):
            caminho = "municipais/*/*/" + categoria
            if not any(caminho in item.caminho for item in PLANO):
                ap.error(f"categoria ainda não incluída no plano: {caminho}")
    candidatos = json.loads((pasta / "sigi/catalogo.json").read_text())["candidatos_sapl"]
    arq = pasta / ("fila.json" if a.modo == "organicas" else "fila-legislacao.json")
    estado = json.loads(arq.read_text()) if arq.exists() else {}
    if a.trabalhadores > 1:
        return executar_paralelo(candidatos, arq, estado, a, pasta)
    rodadas = 0
    for item in candidatos:
        u = urlsplit(item["url"] if "://" in item["url"] else "https://" + item["url"])
        host = u.hostname
        if item["url"] in estado:
            continue
        if a.limite_fontes and rodadas >= a.limite_fontes:
            break
        if u.path.strip("/") or not host or not host.endswith(".leg.br"):
            resultado = {"estado": "requer adaptador para URL oficial", "url": item["url"]}
        else:
            with (RAIZ / "_log_organicas_sapl.txt").open("a") as log:
                log.write(f"\nFONTE {host} IBGE {item['codigo_ibge']}\n")
                log.flush()
                r = subprocess.run([sys.executable, "-I", str(RAIZ / "scripts/baixar_organicas_sapl.py"),
                                    "--descobrir", host, "--rps", "1", "--modo", a.modo], stdout=log, stderr=log)
            resultado = {"estado": "execução concluída" if r.returncode == 0 else "execução parcial; revisar falhas",
                         "exit_code": r.returncode, "url": item["url"]}
            rodadas += 1
        resultado.update({"codigo_ibge": item["codigo_ibge"], "verificado_em": dt.datetime.now().isoformat()})
        estado[item["url"]] = resultado
        tmp = arq.with_suffix(".tmp")
        tmp.write_text(json.dumps(estado, ensure_ascii=False))
        tmp.replace(arq)
        print(item["municipio"], resultado["estado"], flush=True)
    return int(any(x.get("exit_code", 0) != 0 or "adaptador" in x["estado"] for x in estado.values()))

if __name__ == "__main__":
    raise SystemExit(main())
