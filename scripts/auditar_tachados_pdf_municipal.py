"""Detecta possíveis tachados vetoriais em PDFs para revisão visual.

Linhas horizontais que cruzam o miolo de três ou mais caracteres e anotações
StrikeOut são suspeitas. Não remove texto nem decide vigência jurídica.
"""
import argparse
import hashlib
import json
from pathlib import Path
import pdfplumber

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def analisar_pagina(page):
    hits=[];seen=set()
    for e in page.edges:
        if e.get('orientation')!='h' or float(e.get('linewidth',1) or 0)>2:continue
        x0,x1=sorted((float(e['x0']),float(e['x1'])));y=float(e['top'])
        if x1-x0<6:continue
        key=tuple(round(v,2) for v in (x0,x1,y))
        if key in seen:continue
        seen.add(key)
        chars=[c for c in page.chars if c.get('text','').strip() and c['x1']>x0 and c['x0']<x1 and c['top']+(c['bottom']-c['top'])*.2<y<c['bottom']-(c['bottom']-c['top'])*.2]
        if len(chars)<3:continue
        chars.sort(key=lambda c:c['x0']);hits.append({'tipo':'linha_cruza_caracteres','x0':x0,'x1':x1,'y':y,'texto':''.join(c['text'] for c in chars),'fontes':sorted({c['fontname'] for c in chars})})
    for a in page.annots or []:
        if 'StrikeOut' in str(a.get('data',{}).get('Subtype','')):hits.append({'tipo':'anotacao_StrikeOut','rect':[a.get(k) for k in ['x0','x1','top','bottom']]})
    return hits

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--pdf',type=Path,action='append',required=True);ap.add_argument('--saida',type=Path,required=True);a=ap.parse_args();a.saida.mkdir(exist_ok=False,parents=True);allrows=[]
    for path in a.pdf:
        result={'pdf':str(path),'sha256_fonte':sha(path),'paginas':[]}
        with pdfplumber.open(path) as doc:
            result['total_paginas']=len(doc.pages)
            for i,p in enumerate(doc.pages,1):
                h=analisar_pagina(p)
                if h:result['paginas'].append({'pagina':i,'suspeitas':h})
                p.close()
                if i%40==0:print(json.dumps({'pdf':str(path),'pagina':i,'paginas_com_suspeita':len(result['paginas'])}),flush=True)
        allrows.append(result);(a.saida/(path.stem+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({'pdf':str(path),'fim':True,'paginas':result['total_paginas'],'paginas_com_suspeita':len(result['paginas'])}),flush=True)
    (a.saida/'controle.json').write_text(json.dumps({'criterio':__doc__,'documentos':allrows,'script_sha256':sha(Path(__file__))},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
