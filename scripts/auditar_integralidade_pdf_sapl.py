"""Confronta PDFs SAPL integrais com Markdown, descontando só margens comprovadas.

Não reconverte via comum.py: extrai layout e coordenadas independentemente. Não
altera documentos nem listas entregues. Divergências são retidas para revisão.
"""
import argparse
import collections
from concurrent.futures import ThreadPoolExecutor
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_municipal import metadados

RAIZ=Path(__file__).resolve().parent.parent
CACHE=RAIZ/'municipais/_fonte/auditorias/integralidade-pdf-sapl'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def normal(s):
    return re.sub(r'\s+',' ',s).strip()


def confrontar(layout,bbox,corpo):
    root=ET.fromstring(bbox)
    geometria=[]
    for pg in root.iter():
        if pg.tag.rsplit('}',1)[-1]!='page':continue
        altura=float(pg.attrib['height']);mapa=collections.defaultdict(list)
        for linha in pg.iter():
            if linha.tag.rsplit('}',1)[-1]!='line':continue
            txt=normal(' '.join(''.join(w.itertext()) for w in linha if w.tag.rsplit('}',1)[-1]=='word'))
            mapa[txt].append({'yMin':float(linha.attrib['yMin']),'yMax':float(linha.attrib['yMax']),'altura':altura})
        geometria.append(mapa)
    paginas=[p for p in layout.split('\f') if p.strip()]
    if len(paginas)!=len(geometria):raise ValueError('páginas layout e coordenadas divergem')
    freq=collections.Counter(x for p in paginas for x in {normal(y) for y in p.splitlines()} if x)
    repetidas={x for x,n in freq.items() if len(paginas)>=2 and n>len(paginas)/2 and not re.match(r'^(Art|§)',x)}
    retidos=[];excluidas=[];mantidas=[]
    for numero,(pagina,mapa) in enumerate(zip(paginas,geometria),1):
        for linha in pagina.splitlines():
            texto=normal(linha)
            coords=mapa.get(texto,[])
            margem=bool(coords) and all(p['yMax']<=p['altura']*.10 or p['yMin']>=p['altura']*.90 for p in coords)
            folio=bool(re.fullmatch(r'\d{1,3}',texto)) and texto==str(numero) and margem
            if re.fullmatch(r'\d{1,3}',texto) and not folio:
                retidos.append({'pagina':numero,'linha':texto,'coordenadas':coords,'motivo':'número isolado sem prova de fólio sequencial na margem'})
            if folio or (texto in repetidas and margem):
                excluidas.append({'pagina':numero,'linha':texto,'coordenadas':coords,'criterio':'fólio sequencial na margem' if folio else 'linha repetida em mais de metade das páginas, situada na margem'})
            else:
                mantidas.append(re.sub(r'_{5,}|[-–—=]{8,}',' ',linha))
    a=re.findall(r'\w+','\n'.join(mantidas));b=re.findall(r'\w+',corpo)
    iguais=a==b
    diferenca=None
    if not iguais:
        i=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
        diferenca={'primeiro_token_divergente':i,'fonte':a[max(0,i-8):i+16],'md':b[max(0,i-8):i+16]}
    return {'paginas':len(paginas),'tokens_fonte_sem_margens_comprovadas':len(a),'tokens_md':len(b),
            'tokens_em_ordem_identicos':iguais,'numeros_sem_prova_de_folio':retidos,'margens_excluidas':excluidas,
            'primeira_divergencia':diferenca}


def auditar(rel):
    p=RAIZ/rel;b=p.read_bytes();texto=b.decode();m=metadados(texto)
    row={'path':rel,'sha256':sha(b),'sha256_fonte':m.get('sha256_fonte')}
    try:
        host=urlsplit(m['fonte']).hostname;idnorma=urlsplit(m['fonte']).path.strip('/').split('/')[-1]
        fonte=RAIZ/'municipais/_fonte/organicas-sapl'/host/(idnorma+'.bin')
        bruto=fonte.read_bytes()
        if sha(bruto)!=m['sha256_fonte']:raise ValueError('hash da fonte diverge')
        if not bruto.startswith(b'%PDF'):
            row.update({'aprovado':True,'criterio':'fonte não é PDF; exclusão numérica de texto_pdf_para_md não se aplica'})
            return row
        capt=CACHE/(sha(bruto)+'.json.gz')
        if capt.exists():
            with gzip.open(capt,'rt') as f:d=json.load(f)
        else:
            d={}
            for tipo,args in [('layout',['-layout']),('bbox',['-bbox-layout'])]:
                r=subprocess.run(['pdftotext','-q','-enc','UTF-8']+args+[str(fonte),'-'],capture_output=True,check=True,timeout=90)
                d[tipo]=r.stdout.decode()
            tmp=capt.with_suffix('.tmp')
            with gzip.open(tmp,'wt') as f:json.dump(d,f,ensure_ascii=False)
            tmp.replace(capt)
        row['evidencia_extracao']={'path':str(capt.relative_to(RAIZ)),'sha256':sha(capt.read_bytes()),'sha256_layout':sha(d['layout'].encode()),'sha256_bbox':sha(d['bbox'].encode())}
        corpo=texto.split('\n---\n',1)[1].lstrip('\n').split('\n\n',1)[1]
        resultado=confrontar(d['layout'],d['bbox'],corpo)
        row.update(resultado)
        row['aprovado']=resultado['tokens_em_ordem_identicos'] and not resultado['numeros_sem_prova_de_folio'] and resultado['tokens_fonte_sem_margens_comprovadas']>30
    except Exception as e:
        row.update({'aprovado':False,'erro':str(e)})
    return row


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lista',type=Path,action='append',required=True)
    ap.add_argument('--saida',type=Path,required=True)
    ap.add_argument('--trabalhadores',type=int,default=4)
    a=ap.parse_args();a.saida.mkdir(parents=True,exist_ok=False);CACHE.mkdir(parents=True,exist_ok=True)
    paths=list(dict.fromkeys(p for lista in a.lista for p in lista.read_text().splitlines() if p))
    aprovados=[];retidos=[]
    with (a.saida/'resultados.jsonl').open('x') as log,ThreadPoolExecutor(max_workers=a.trabalhadores) as ex:
        for i,r in enumerate(ex.map(auditar,paths),1):
            log.write(json.dumps(r,ensure_ascii=False)+'\n');log.flush()
            (aprovados if r['aprovado'] else retidos).append(r)
            if i%100==0:print(json.dumps({'auditados':i,'total':len(paths),'aprovados':len(aprovados),'retidos':len(retidos)}),flush=True)
    for nome,rows in [('aprovados',aprovados),('retidos',retidos)]:
        with (a.saida/(nome+'.paths.txt')).open('x') as f:f.write(''.join(r['path']+'\n' for r in rows))
    receipt={'verificado_em':dt.datetime.now().isoformat(),'listas_substituidas':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in a.lista], 'aprovados':len(aprovados),'retidos':len(retidos), 'criterio':'Confronto integral de tokens fonte/Markdown; somente margens repetidas com coordenadas e fólios sequenciais comprovados podem ser descontados; nenhuma norma é recortada.', 'artefatos':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in sorted(a.saida.iterdir()) if p.is_file()], 'script_sha256':sha(Path(__file__).read_bytes())}
    with (a.saida/'entrega-final.json').open('x') as f:json.dump(receipt,f,ensure_ascii=False,indent=2)
    print(json.dumps(receipt,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
