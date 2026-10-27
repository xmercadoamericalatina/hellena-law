"""Recupera RSFs públicas do catálogo administrativo oficial do Senado."""
import argparse
import datetime as dt
import gzip
import hashlib
import http.cookiejar
import json
from pathlib import Path
import re
import sys
import urllib.request
sys.path.insert(0,str(Path(__file__).resolve().parent))
from baixar_federal import carregar_indice,montar,numero_oficial
from baixar_rsf_coletaneas import MESES
from comum import Rede,yaml_str
from html2md import convert

RAIZ=Path(__file__).resolve().parent.parent/"federal"
CACHE=RAIZ/"_fonte/senado-administrativo"


def extrair(html):
    texto=convert(html).split("Texto da Norma",1)[-1]
    m=re.search(r"(?m)^(?:\*\*)?RESOLUÇÃO Nº (\d+), DE (\d{4})(?:\*\*)?",texto)
    if not m:
        raise ValueError("epígrafe de resolução não identificada")
    ini=texto.rfind("Faço saber",0,m.start())
    if ini<0:
        ini=m.start()
    fim=re.search(r"Senado Federal, em (\d+) de ([a-zç]+) de (\d{4})\.[\s\S]{0,200}?Presidente do Senado Federal\.",texto[m.end():])
    if not fim:
        raise ValueError("fecho próprio completo não identificado")
    data=dt.date(int(fim[3]),MESES[fim[2].replace("ç","c")],int(fim[1])).isoformat()
    corpo=texto[ini:m.end()+fim.end()].strip()
    if int(m[2])!=int(data[:4]) or len(corpo)<200 or "\x00" in corpo or not re.search(r"Art\. 1",corpo):
        raise ValueError("texto normativo insuficiente")
    return m[1],data,corpo


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("ids",nargs="+",type=int)
    a=ap.parse_args()
    r=Rede(1)
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    primario={(numero_oficial(d),montar(d)["data"]):(d,montar(d)) for d in carregar_indice({"RSF"})}
    for ident in a.ids:
        url="https://adm.senado.leg.br/normas/ui/pub/normaConsultada?0=&idNorma="+str(ident)
        cache=CACHE/(hashlib.sha256(url.encode()).hexdigest()+".html.gz")
        if cache.exists():
            bruto=gzip.decompress(cache.read_bytes())
        else:
            r.limite.esperar()
            with opener.open(url,timeout=45) as resposta:
                if resposta.status!=200:
                    raise RuntimeError(f"HTTP {resposta.status}")
                bruto=resposta.read()
            CACHE.mkdir(parents=True,exist_ok=True)
            cache.write_bytes(gzip.compress(bruto))
        numero,data,corpo=extrair(bruto.decode("utf-8"))
        if (numero,data) not in primario:
            raise ValueError("identidade não consta no índice primário")
        d,info=primario[numero,data]
        path=Path(info["md"])
        if path.exists():
            continue
        meta={"titulo":d["normaNome"],"tipo":info["nome"],"numero":numero,"data":data,"ementa":d.get("ementa",""),"urn":info["urn"],"revogada":None,"versao_texto":"texto original na página pública de normas administrativas do Senado","fonte":url,"id_senado":d["id"],"id_administrativo":str(ident),"sha256_html_fonte":hashlib.sha256(bruto).hexdigest(),"sha256_texto":hashlib.sha256(corpo.encode()).hexdigest(),"baixado_em":dt.date.today().isoformat()}
        cab="---\n"+"".join(k+": "+("null" if v is None else yaml_str(str(v)))+"\n" for k,v in meta.items())+"---\n"
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(cab+"\n# "+d["normaNome"]+"\n\n"+corpo+"\n")
        with (RAIZ/"_recuperacoes_rsf_administrativo.jsonl").open("a") as f:
            f.write(json.dumps({"urn":info["urn"],"fonte":url,"sha256_texto":meta["sha256_texto"],"md":str(path)},ensure_ascii=False)+"\n")
        print("ok",info["slug"],len(corpo),flush=True)


if __name__=="__main__":
    main()
