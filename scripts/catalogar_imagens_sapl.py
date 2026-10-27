"""Extrai imagens pequenas de PDFs SAPL para revisão visual por hash, sem aprovar.

Só inclui documentos cujo texto já passou o confronto integral. A dimensão é um
filtro de triagem, nunca prova de decoração. Imagens só serão liberadas após
revisão explícita de pixels; tabelas/páginas rasterizadas continuam retidas.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

sys.path.insert(0,str(Path(__file__).resolve().parent))
from auditar_municipal import metadados
RAIZ=Path(__file__).resolve().parent.parent
CACHE=RAIZ/'municipais/_fonte/auditorias/catalogo-imagens-sapl'


def sha(b):return hashlib.sha256(b).hexdigest()


def extrair(row):
    p=RAIZ/row['path'];m=metadados(p.read_text());h=m['sha256_fonte']
    d={'path':row['path'],'sha256_md_revisado':sha(p.read_bytes()),'sha256_fonte':h,'imagens':[]}
    try:
        cap=RAIZ/'municipais/_fonte/auditorias/integralidade-pdf-sapl'/(h+'.json.gz')
        with gzip.open(cap,'rt') as f:captura=json.load(f)
        pages=[x for x in ET.fromstring(captura['bbox']).iter() if x.tag.rsplit('}',1)[-1]=='page']
        for image in row['imagens']:
            xppi,yppi=abs(float(image['x_ppi'])),abs(float(image['y_ppi']))
            if not xppi or not yppi:raise ValueError('resolução de imagem não determinada')
            pg=pages[image['pagina']-1]
            area=image['largura_px']/xppi*72*image['altura_px']/yppi*72/(float(pg.attrib['width'])*float(pg.attrib['height']))
            if area>.05:raise ValueError('imagem acima de5%da página; revisão própria, não triagem de brasão')
        u=urlsplit(m['fonte']);fonte=RAIZ/'municipais/_fonte/organicas-sapl'/u.hostname/(u.path.strip('/').split('/')[-1]+'.bin')
        if sha(fonte.read_bytes())!=h:raise ValueError('fonte bruta mudou')
        base=CACHE/h;base.mkdir(parents=True,exist_ok=True)
        porpagina={i['pagina'] for i in row['imagens']}
        # Um mesmo objeto repetido em várias páginas é extraído só na primeira.
        objetos={}
        for im in row['imagens']:objetos.setdefault(tuple(im['object_id']),im['pagina'])
        porpagina=set(objetos.values())
        for page in sorted(porpagina):
            pasta=base/str(page);pasta.mkdir(exist_ok=True);prefix=pasta/'imagem'
            expected=[im for im in row['imagens'] if im['pagina']==page]
            files=sorted(pasta.glob('imagem-*.png'))
            if not files:
                subprocess.run(['pdfimages','-png','-f',str(page),'-l',str(page),str(fonte),str(prefix)],capture_output=True,check=True,timeout=90)
                files=sorted(pasta.glob('imagem-*.png'))
            if len(files)!=len(expected):raise ValueError('número de imagens extraídas diverge')
            for im,f in zip(expected,files):d['imagens'].append({**im,'path':str(f.relative_to(RAIZ)),'sha256':sha(f.read_bytes())})
    except Exception as e:d['erro']=str(e)
    return d


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--controle-imagens',type=Path,required=True);ap.add_argument('--saida',type=Path,required=True);ap.add_argument('--trabalhadores',type=int,default=4);a=ap.parse_args()
    if not (a.controle_imagens/'entrega-final.json').exists():raise ValueError('controle de imagens incompleto')
    a.saida.mkdir(parents=True,exist_ok=False);CACHE.mkdir(parents=True,exist_ok=True)
    rows=[json.loads(l) for l in (a.controle_imagens/'resultados.jsonl').read_text().splitlines()];rows=[r for r in rows if not r['aprovado'] and r.get('imagens')]
    catalogo={};pendentes=0
    with (a.saida/'documentos.jsonl').open('x') as f,ThreadPoolExecutor(max_workers=a.trabalhadores) as pool:
        for i,r in enumerate(pool.map(extrair,rows),1):
            f.write(json.dumps(r,ensure_ascii=False)+'\n');f.flush()
            if r.get('erro'):pendentes+=1
            else:
                for im in r['imagens']:
                    x=catalogo.setdefault(im['sha256'],{'sha256':im['sha256'],'imagem':im['path'],'fontes':[]})
                    if r['path'] not in [s['norma'] for s in x['fontes']]:x['fontes'].append({'norma':r['path'],'sha256_fonte':r['sha256_fonte'],'pagina':im['pagina'],'object_id':im['object_id']})
            if i%100==0:print(json.dumps({'documentos':i,'total':len(rows),'imagens_unicas':len(catalogo),'pendentes':pendentes}),flush=True)
    with (a.saida/'catalogo.json').open('x') as f:json.dump({'criterio':__doc__,'imagens':sorted(catalogo.values(),key=lambda x:-len(x['fontes'])),'documentos':len(rows),'pendentes':pendentes},f,ensure_ascii=False,indent=2)
    print(json.dumps({'documentos':len(rows),'imagens_unicas':len(catalogo),'pendentes':pendentes}),flush=True)


if __name__=='__main__':main()
