"""Recupera resoluções nas páginas institucionais públicas dos conselhos do Senado."""
import argparse
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
import urllib.parse
sys.path.insert(0, str(Path(__file__).resolve().parent))
from baixar_federal import carregar_indice, montar, numero_oficial
from baixar_rsf_coletaneas import MESES
from comum import Rede, yaml_str
from html2md import convert

RAIZ = Path(__file__).resolve().parent.parent / "federal"
CACHE = RAIZ / "_fonte/senado-paginas"


def extrair(html):
    texto = convert(html)
    blocos = []
    for m in re.finditer(r"(?m)^(?:\*\*)?R[ \t]*E[ \t]*S[ \t]*O[ \t]*L[ \t]*U[ \t]*Ç[ \t]*Ã[ \t]*O(?:\*\*)?\s+(?:\*\*)?N[º°o.]?\s*(\d+),? DE (\d{4})(?:\*\*)?", texto):
        inicio = texto.rfind("Faço saber", max(0, m.start()-500), m.start())
        if inicio < 0:
            inicio = m.start()
        fim = re.search(r"Senado Federal, em (\d+) de ([a-zç]+) de (\d{4})\.[\s\S]{0,160}?Presidente do Senado Federal(?:,?\s*\n+\s*no exercício da Presidência)?", texto[m.end():])
        if not fim:
            continue
        mes = fim[2].replace("ç", "c")
        data = dt.date(int(fim[3]), MESES[mes], int(fim[1])).isoformat()
        corpo = texto[inicio:m.end()+fim.end()].strip()
        if len(corpo)<200 or "\x00" in corpo or not re.search(r"Art\. 1", corpo):
            continue
        if int(data[:4]) != int(m[2]):
            continue
        blocos.append((m[1],data,corpo))
    return blocos


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("urls",nargs="+")
    ap.add_argument("--rps",type=float,default=1)
    a=ap.parse_args()
    if not 0<a.rps<=1:
        ap.error("taxa deve ser positiva e no máximo1rps")
    rede=Rede(a.rps)
    primario={(numero_oficial(d),montar(d)["data"]):(d,montar(d)) for d in carregar_indice({"RSF"})}
    for url in a.urls:
        if urllib.parse.urlparse(url).hostname != "www25.senado.leg.br" or "/conselho/" not in url:
            ap.error("URL deve ser página institucional de conselho do Senado")
        cache=CACHE/(hashlib.sha256(url.encode()).hexdigest()+".html.gz")
        if cache.exists():
            bruto=gzip.decompress(cache.read_bytes())
        else:
            status,bruto,_=rede.get(url,timeout=45,tentativas=1)
            if status!=200:
                raise RuntimeError(f"HTTP {status}: {url}")
            CACHE.mkdir(parents=True,exist_ok=True)
            cache.write_bytes(gzip.compress(bruto))
        for numero,data,corpo in extrair(bruto.decode("utf-8")):
            if (numero,data) not in primario:
                continue
            d,info=primario[numero,data]
            path=Path(info["md"])
            if path.exists():
                continue
            meta={"titulo":d["normaNome"],"tipo":info["nome"],"numero":numero,"data":data,"ementa":d.get("ementa",""),"urn":info["urn"],"revogada":None,"versao_texto":"reprodução na página institucional oficial do Senado","fonte":url,"id_senado":d["id"],"sha256_html_fonte":hashlib.sha256(bruto).hexdigest(),"sha256_texto":hashlib.sha256(corpo.encode()).hexdigest(),"baixado_em":dt.date.today().isoformat()}
            cab="---\n"+"".join(k+": "+("null" if v is None else yaml_str(str(v)))+"\n" for k,v in meta.items())+"---\n"
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(cab+"\n# "+d["normaNome"]+"\n\n"+corpo+"\n")
            with (RAIZ/"_recuperacoes_rsf_conselhos.jsonl").open("a") as f:
                f.write(json.dumps({"urn":info["urn"],"fonte":url,"sha256_texto":meta["sha256_texto"],"md":str(path)},ensure_ascii=False)+"\n")
            print("ok",info["slug"],len(corpo),flush=True)


if __name__=="__main__":
    main()
