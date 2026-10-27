"""Sinaliza cabeçalho de município diferente, sem corrigir o texto oficial.

Só há correspondência com nome real do cadastro IBGE. Menções genéricas a
projetos, vereadores ou iniciativa de lei não viram municípios inventados.
O resultado é triagem para revisão, nunca autorização automática de publicação.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata
sys.path.insert(0,str(Path(__file__).resolve().parent))
from auditar_municipal import metadados
RAIZ=Path(__file__).resolve().parent.parent

def normal(s):
    s=''.join(c for c in unicodedata.normalize('NFD',str(s)).lower() if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-z0-9]+',' ',s).strip()

def analisar(texto,municipio,nomes):
    own=normal(municipio);nomes=sorted({normal(n) for n in nomes},key=len,reverse=True);out=[]
    for a in re.finditer(r'\b(?:PREFEITURA|C[ÂA]MARA)\s+MUNICIPAL\s+(?:DE|DA|DO)\s+',texto,re.I):
        tail=normal(texto[a.end():a.end()+180]);tail=re.sub(r'^(?:vereadores|cidade|municipio)\s+(?:de|da|do)\s+','',tail)
        found=next((n for n in nomes if tail==n or tail.startswith(n+' ')),None)
        if found and found!=own:out.append({'municipio_declarado':municipio,'municipio_no_cabecalho_normalizado':found,'offset':a.start(),'trecho':texto[max(0,a.start()-90):a.end()+180]})
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--lista',type=Path,required=True);ap.add_argument('--evidencias',type=Path,required=True);ap.add_argument('--saida',type=Path,required=True);a=ap.parse_args();a.saida.mkdir(parents=True,exist_ok=False)
    f=RAIZ/'municipais/_indice/ibge-municipios.json';nomes=[x['nome'] for x in json.loads(f.read_text())];data=[json.loads(s) for s in a.evidencias.read_text().splitlines()];evid={r['path']:r['evidencia_extracao'] for r in data if r.get('evidencia_extracao')};rows=[]
    for rel in a.lista.read_text().splitlines():
        p=RAIZ/rel;b=p.read_bytes();m=metadados(b.decode());r={'path':rel,'sha256':hashlib.sha256(b).hexdigest()}
        try:
            e=evid[rel];raw=(RAIZ/e['path']).read_bytes()
            if hashlib.sha256(raw).hexdigest()!=e['sha256']:raise ValueError('evidência mudou')
            layout=json.loads(gzip.decompress(raw))['layout'];r['alertas']=analisar(layout,m['municipio'],nomes);r['evidencia']=e
        except Exception as err:r['pendencia']=str(err)
        rows.append(r)
    (a.saida/'controle.json').write_text(json.dumps({'cadastro_ibge':{'path':str(f.relative_to(RAIZ)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()},'resultados':rows,'limite':__doc__},ensure_ascii=False,indent=2));print(json.dumps({'documentos':len(rows),'suspeitos':sum(bool(x.get('alertas') or x.get('pendencia')) for x in rows)}))
if __name__=='__main__':main()
