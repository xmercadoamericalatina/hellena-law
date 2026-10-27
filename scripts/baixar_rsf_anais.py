"""Recupera resolução individual de página identificada dos Anais oficiais do Senado."""
import argparse
from collections import Counter
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import urllib.parse
sys.path.insert(0,str(Path(__file__).resolve().parent))
from baixar_federal import carregar_indice,montar,numero_oficial
from baixar_rsf_coletaneas import blocos,markdown
from comum import Rede,yaml_str

RAIZ=Path(__file__).resolve().parent.parent/"federal"
CACHE=RAIZ/"_fonte/senado-anais"


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("urn")
    ap.add_argument("url")
    ap.add_argument("pagina",type=int)
    ap.add_argument("--auditar",action="store_true")
    a=ap.parse_args()
    if urllib.parse.urlparse(a.url).hostname!="www.senado.leg.br" or "/publicacoes/anais/" not in a.url or a.pagina<1:
        ap.error("fonte deve ser publicação pública dos Anais e página positiva")
    candidatos=[d for d in carregar_indice({"RSF"}) if montar(d)["urn"]==a.urn]
    if len(candidatos)!=1:
        ap.error("URN não identificada de forma única no índice primário")
    d=candidatos[0]
    info=montar(d)
    path=Path(info["md"])
    if path.exists() and not a.auditar:
        print("pulado",path)
        return
    if not a.auditar:
        CACHE.mkdir(parents=True,exist_ok=True)
    cache=CACHE/(hashlib.sha256(a.url.encode()).hexdigest()+".pdf.gz")
    if cache.exists():
        bruto=gzip.decompress(cache.read_bytes())
    else:
        if a.auditar:
            raise ValueError(f"cache ausente em auditoria offline: {cache}")
        st,bruto,_=Rede(1).get(a.url,timeout=60,tentativas=1)
        if st!=200 or not bruto.startswith(b"%PDF"):
            raise ValueError(f"HTTP{st}/fonte nãoPDF")
        cache.write_bytes(gzip.compress(bruto))
    with tempfile.TemporaryDirectory() as tmp:
        pdf=Path(tmp)/"anais.pdf"
        pdf.write_bytes(bruto)
        texto=subprocess.check_output(["rtk","proxy","pdftotext","-f",str(a.pagina),"-l",str(a.pagina),"-raw",str(pdf),"-"],timeout=60).decode()
    fonte_texto=CACHE/(hashlib.sha256(bruto).hexdigest()+f"-page{a.pagina}-"+hashlib.sha256(texto.encode()).hexdigest()+".raw.txt.gz")
    if not a.auditar and not fonte_texto.exists():
        fonte_texto.write_bytes(gzip.compress(texto.encode()))
    opcoes=blocos(texto).get((numero_oficial(d).lower(),int(info["data"][:4])),[])
    validos=[b for b in opcoes if b["datas"]==[info["data"]]]
    if len(validos)!=1:
        raise ValueError("epígrafe/fecho próprios não comprovam norma única")
    corpo=markdown(validos[0]["corpo"]).strip()
    numeros=lambda s:Counter(re.findall(r"\d[\d.,]*",s))
    if numeros(validos[0]["corpo"])-numeros(corpo):
        raise ValueError("conversão perdeu valores numéricos")
    if a.auditar:
        existente=path.read_text().split("---\n",2)[2].strip().split("\n\n",1)[1]
        if existente!=corpo:
            raise ValueError("corpo armazenado diverge da fonte reextraída")
        print("auditado",path,hashlib.sha256(corpo.encode()).hexdigest())
        return
    meta={"titulo":d["normaNome"],"tipo":info["nome"],"numero":numero_oficial(d),"data":info["data"],"ementa":d.get("ementa",""),"urn":info["urn"],"revogada":None,"versao_texto":"transcrição oficial dos Anais do Senado; texto promulgado com fecho próprio","fonte":a.url+f"#page={a.pagina}","id_senado":d["id"],"sha256_pdf_fonte":hashlib.sha256(bruto).hexdigest(),"sha256_texto":hashlib.sha256(corpo.encode()).hexdigest(),"baixado_em":dt.date.today().isoformat()}
    cab="---\n"+"".join(k+": "+("null" if v is None else yaml_str(str(v)))+"\n" for k,v in meta.items())+"---\n"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(cab+"# "+d["normaNome"]+"\n\n"+corpo+"\n")
    with (RAIZ/"_recuperacoes_rsf_anais.jsonl").open("a") as f:
        f.write(json.dumps({"path":str(path.relative_to(RAIZ.parent)),"urn":a.urn,"fonte":meta["fonte"],"sha256_pdf_fonte":meta["sha256_pdf_fonte"],"sha256_texto":meta["sha256_texto"],"pagina":a.pagina,"perda_numerica":0},ensure_ascii=False)+"\n")
    print("ok",path,len(corpo))


if __name__=="__main__":
    main()
