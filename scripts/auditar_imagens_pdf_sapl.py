"""Retém PDFs com imagens sem inspeção; camada de texto não prova imagem integral."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit

sys.path.insert(0,str(Path(__file__).resolve().parent))
from auditar_municipal import metadados
RAIZ=Path(__file__).resolve().parent.parent
CACHE=RAIZ/'municipais/_fonte/auditorias/imagens-pdf-sapl'


def sha(b):return hashlib.sha256(b).hexdigest()


def imagens(stdout):
    linhas=[]
    for line in stdout.splitlines():
        cells=line.split()
        if not cells or not cells[0].isdigit():continue
        if len(cells)<16:raise ValueError('formato pdfimages não reconhecido')
        linhas.append({'pagina':int(cells[0]),'numero':int(cells[1]),'tipo':cells[2],
                       'largura_px':int(cells[3]),'altura_px':int(cells[4]),'object_id':cells[10:12],
                       'x_ppi':cells[12],'y_ppi':cells[13],'linha_original':line})
    if 'page' not in stdout or 'num' not in stdout:raise ValueError('cabeçalho pdfimages ausente')
    return linhas


def auditar(r):
    row={'path':r['path'],'sha256':r['sha256'],'aprovado':False}
    try:
        p=RAIZ/r['path'];b=p.read_bytes();m=metadados(b.decode())
        if sha(b)!=r['sha256']:raise ValueError('MD mudou desde confronto integral')
        u=urlsplit(m['fonte']);fonte=RAIZ/'municipais/_fonte/organicas-sapl'/u.hostname/(u.path.strip('/').split('/')[-1]+'.bin');raw=fonte.read_bytes()
        if sha(raw)!=r['sha256_fonte']:raise ValueError('fonte mudou desde confronto integral')
        if not raw.startswith(b'%PDF'):
            row.update({'aprovado':True,'criterio':'não PDF; já passou controle anterior; não inferir integralidade de imagem por este controle'})
            return row
        cache=CACHE/(sha(raw)+'.json')
        if cache.exists():d=json.loads(cache.read_text())
        else:
            result=subprocess.run(['pdfimages','-list',str(fonte)],capture_output=True,check=True,timeout=90)
            stdout=result.stdout.decode();d={'sha256_fonte':sha(raw),'stdout':stdout,'imagens':imagens(stdout)}
            temp=cache.with_suffix('.tmp');temp.write_text(json.dumps(d,ensure_ascii=False));temp.replace(cache)
        row['evidencia_imagens']={'path':str(cache.relative_to(RAIZ)),'sha256':sha(cache.read_bytes())}
        row['imagens']=d['imagens'];row['aprovado']=not d['imagens']
        row['criterio']='PDF sem imagens embutidas e texto integral já confrontado' if row['aprovado'] else 'imagem embutida requer inspeção visual de seu conteúdo; pode ser brasão, tabela ou trecho normativo; não presumir decorativa'
    except Exception as e:row['erro']=str(e)
    return row


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--controle-integral',type=Path,required=True);ap.add_argument('--saida',type=Path,required=True);ap.add_argument('--trabalhadores',type=int,default=4);a=ap.parse_args()
    if not (a.controle_integral/'entrega-final.json').exists():raise ValueError('controle integral ainda não encerrado')
    a.saida.mkdir(parents=True,exist_ok=False);CACHE.mkdir(parents=True,exist_ok=True)
    rows=[json.loads(l) for l in (a.controle_integral/'resultados.jsonl').read_text().splitlines()];candidatos=[r for r in rows if r['aprovado']]
    approved=[];retained=[{'path':r['path'],'sha256':r['sha256'],'aprovado':False,'criterio':'retido pelo controle integral anterior'} for r in rows if not r['aprovado']]
    with (a.saida/'resultados.jsonl').open('x') as f,ThreadPoolExecutor(max_workers=a.trabalhadores) as pool:
        for i,r in enumerate(pool.map(auditar,candidatos),1):
            f.write(json.dumps(r,ensure_ascii=False)+'\n');f.flush();(approved if r['aprovado'] else retained).append(r)
            if i%100==0:print(json.dumps({'auditados':i,'total':len(candidatos),'aprovados':len(approved),'retidos_total':len(retained)}),flush=True)
    for nome,lista in [('aprovados',approved),('retidos',retained)]:
        with (a.saida/(nome+'.paths.txt')).open('x') as f:f.write(''.join(r['path']+'\n' for r in lista))
    receipt={'obtido_em':dt.datetime.now().isoformat(),'controle_integral':str(a.controle_integral),'sha256_controle_integral':sha((a.controle_integral/'entrega-final.json').read_bytes()),'aprovados':len(approved),'retidos':len(retained),'criterio':'Passou controle integral e proveniência anterior; PDF só aprovado se não contém imagem embutida. Imagens sem revisão, OCR e outras divergências seguem retidos.','artefatos':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in sorted(a.saida.iterdir()) if p.is_file()], 'script_sha256':sha(Path(__file__).read_bytes())}
    with (a.saida/'entrega-final.json').open('x') as f:json.dump(receipt,f,ensure_ascii=False,indent=2)
    print(json.dumps(receipt,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
