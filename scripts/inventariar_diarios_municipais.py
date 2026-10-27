"""Inventaria PDFs e calendários locais para reconstrução, sem rede nem Git."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import slugify


def inventario(raiz):
    encontrados = {}
    problemas = []
    for calendario in sorted((raiz / "municipais/_indice").glob("*/????-??-??.json")):
        try:
            dados = json.loads(calendario.read_text())
        except Exception as erro:
            problemas.append({"calendario":str(calendario), "erro":str(erro)})
            continue
        if not isinstance(dados,list):
            continue
        for edicao in dados:
            if not isinstance(edicao,dict) or not edicao.get("fonte") or not edicao.get("data"):
                continue
            numero = edicao.get("numero", "")
            pdf = raiz / "municipais/_fonte" / calendario.parent.name / (edicao["data"] + ("-" + slugify(numero) if numero else "") + ".pdf")
            if not pdf.exists():
                continue
            registro = {"pdf":str(pdf),"fonte":edicao["fonte"],"data":edicao["data"],
                        "numero":numero,"assoc":calendario.parent.name,"prova_calendario":str(calendario),
                        "sha256_pdf":hashlib.sha256(pdf.read_bytes()).hexdigest()}
            anteriores = encontrados.setdefault(str(pdf),[])
            if not any(x["fonte"] == registro["fonte"] for x in anteriores):
                anteriores.append(registro)
    validos = []
    for pdf,registros in encontrados.items():
        if len(registros) == 1:
            validos.append(registros[0])
        else:
            problemas.append({"pdf":pdf,"erro":"mais de uma fonte oficial para o mesmo caminho","registros":registros})
    sem_mapa = [str(p) for p in sorted((raiz / "municipais/_fonte").glob("*/*.pdf")) if str(p) not in encontrados]
    return {"edicoes":validos,"pdfs_sem_calendario":sem_mapa,"problemas":problemas,
            "observacao":"PDFs sem calendário exigem prova adicional de fonte e circulação antes da reconciliação."}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raiz",type=Path,default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--saida",type=Path,required=True)
    a=ap.parse_args()
    dados=inventario(a.raiz.resolve())
    a.saida.parent.mkdir(parents=True,exist_ok=True)
    temporario=a.saida.with_suffix(a.saida.suffix+".tmp")
    temporario.write_text(json.dumps(dados,ensure_ascii=False,indent=2))
    temporario.replace(a.saida)
    print(json.dumps({k:len(dados[k]) for k in ("edicoes","pdfs_sem_calendario","problemas")}))
    return bool(dados["problemas"])

if __name__ == "__main__":
    raise SystemExit(main())
