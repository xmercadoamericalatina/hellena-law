"""Libera só PDFs já integrais cujas imagens exatas receberam revisão visual."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit
sys.path.insert(0,str(Path(__file__).resolve().parent))
from auditar_municipal import metadados
RAIZ=Path(__file__).resolve().parent.parent


def sha(b):return hashlib.sha256(b).hexdigest()


def objetos_validos(imagens):
    return all(len(i['object_id'])==2 and all(x.isdigit() for x in i['object_id']) and int(i['object_id'][0])>0 for i in imagens)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--catalogo',type=Path,required=True);ap.add_argument('--revisao',type=Path,action='append',required=True);ap.add_argument('--controle-imagens',type=Path,required=True);ap.add_argument('--saida',type=Path,required=True);a=ap.parse_args()
    cat=a.catalogo/'catalogo.json';revisoes=[json.loads(p.read_text()) for p in a.revisao];permitidos={}
    for rev in revisoes:
        if rev['catalogo_sha256']!=sha(cat.read_bytes()):raise ValueError('revisão pertence a outro catálogo')
        for r in rev['imagens']:
            if not r.get('aprovado_como_decorativo'):continue
            if sha((RAIZ/r['path']).read_bytes())!=r['sha256']:raise ValueError('imagem revisada mudou')
            permitidos[r['sha256']]=r
    gate={r['path']:r for r in map(json.loads,(a.controle_imagens/'resultados.jsonl').read_text().splitlines())}
    documentos=[json.loads(l) for l in (a.catalogo/'documentos.jsonl').read_text().splitlines()]
    aprovados=[];retidos=[];a.saida.mkdir(parents=True,exist_ok=False)
    for d in documentos:
        r=gate[d['path']]
        if r['aprovado']:continue
        try:
            if d.get('erro'):raise ValueError(d['erro'])
            if not objetos_validos(r['imagens']):raise ValueError('identidade de objetoPDF não determinada')
            if {tuple(x['object_id']) for x in r['imagens']}!={tuple(x['object_id']) for x in d['imagens']}:raise ValueError('objetos de imagem não cobertos integralmente')
            faltam=[im['sha256'] for im in d['imagens'] if im['sha256'] not in permitidos]
            if faltam:raise ValueError('imagem sem revisão visual exata: '+','.join(sorted(set(faltam))))
            p=RAIZ/d['path'];b=p.read_bytes()
            if sha(b)!=r['sha256'] or sha(b)!=d['sha256_md_revisado']:raise ValueError('MD mudou desde confronto/revisão')
            m=metadados(b.decode());u=urlsplit(m['fonte']);raw=RAIZ/'municipais/_fonte/organicas-sapl'/u.hostname/(u.path.strip('/').split('/')[-1]+'.bin')
            if sha(raw.read_bytes())!=d['sha256_fonte']:raise ValueError('fonte mudou')
            aprovados.append({'path':d['path'],'sha256':sha(b),'sha256_fonte':d['sha256_fonte'],'fonte':m['fonte'],'codigo_ibge':m['codigo_ibge'], 'imagens_revisadas':[{'sha256':im['sha256'],'object_id':im['object_id'],'pagina':im['pagina'],'path':im['path'],'classificacao':permitidos[im['sha256']]['tipo']} for im in d['imagens']], 'criterio':'Texto já conferido integralmente; todosobjetos de imagem identificados e cobertos por hashes vistos como brasões/marcas institucionais, sem redação normativa. Nenhum recorte ou alteração do MD.'})
        except Exception as e:retidos.append({'path':d['path'],'motivo':str(e)})
    lotes=[]
    for i,start in enumerate(range(0,len(aprovados),1000),1):
        prefix=a.saida/f'lote-{i:04d}';rows=aprovados[start:start+1000];manifesto=prefix.with_suffix('.json');lista=prefix.with_suffix('.paths.txt')
        with manifesto.open('x') as f:json.dump({'aprovados':rows,'revisoes':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in a.revisao],'catalogo_sha256':sha(cat.read_bytes())},f,ensure_ascii=False,indent=2)
        with lista.open('x') as f:f.write(''.join(r['path']+'\n' for r in rows))
        lotes.append({'manifesto':str(manifesto),'sha256_manifesto':sha(manifesto.read_bytes()),'lista':str(lista),'sha256_lista':sha(lista.read_bytes()),'aprovados':len(rows)})
    with (a.saida/'retidos.json').open('x') as f:json.dump(retidos,f,ensure_ascii=False,indent=2)
    recibo={'lotes':lotes,'aprovados':len(aprovados),'retidos':len(retidos),'criterio':__doc__,'sha256_controle_imagens':sha((a.controle_imagens/'entrega-final.json').read_bytes()),'sha256_catalogo':sha(cat.read_bytes()),'script_sha256':sha(Path(__file__).read_bytes())}
    with (a.saida/'entrega-final.json').open('x') as f:json.dump(recibo,f,ensure_ascii=False,indent=2)
    print(json.dumps(recibo,ensure_ascii=False))


if __name__=='__main__':main()
