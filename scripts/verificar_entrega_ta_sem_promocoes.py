"""Confere seleção TA explícita, hashes e replay independente; não altera normas."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))


def sha(b):return hashlib.sha256(b).hexdigest()


def verificar(path,replay=False):
    manifest=json.loads(Path(path).read_text());errors=[];index={}
    for row in manifest['arquivos']:
        p=Path(row['arquivo'])
        if row['arquivo'] in index:errors.append(dict(arquivo=str(p),erro='Artefato repetido'))
        index[row['arquivo']]=row
        if not p.is_file() or sha(p.read_bytes())!=row['sha256'] or p.stat().st_size!=row['bytes']:
            errors.append(dict(arquivo=str(p),erro='Presença, SHA ou tamanho diverge'))
    mapping_path=manifest['mapeamento_fontes'];list_path=manifest['lista_normas']
    if mapping_path not in index or list_path not in index:errors.append(dict(erro='Mapa ou lista sem hash no manifesto'))
    mapping=json.loads(Path(mapping_path).read_text());norms=Path(list_path).read_text().splitlines();mapped=[r['path'] for r in mapping]
    if len(norms)!=manifest['normas'] or len(set(norms))!=len(norms) or len(mapped)!=len(norms) or set(mapped)!=set(norms):
        errors.append(dict(erro='Seleção, mapa e cardinalidade divergem'))
    results=[]
    for row in mapping:
        for key,digest in ((row['path'],row['sha256']),(row['fonte']['arquivo'],row['fonte']['sha256'])):
            if key not in index or index[key]['sha256']!=digest:errors.append(dict(arquivo=key,erro='Norma ou fonte sem vínculo exato ao manifesto'))
        if replay:
            from auditar_commonmark_ta_v2 import comparar
            from auditar_municipal import metadados
            result=dict(path=row['path'],aprovado=False)
            try:
                raw=Path(row['path']).read_bytes();source=Path(row['fonte']['arquivo']).read_bytes()
                if sha(raw)!=row['sha256'] or sha(source)!=row['fonte']['sha256']:raise ValueError('Norma ou fonte diverge')
                text=raw.decode();body=text.split('\n---\n',1)[1].lstrip('\n').split('\n\n',1)[1]
                if not body.endswith('\n'):raise ValueError('EOF sem quebra declarada')
                body=body[:-1]
                if sha(body.encode())!=metadados(text)['sha256_texto']:raise ValueError('Hash do corpo diverge')
                result.update(comparar(source.decode(),body))
            except Exception as exc:result['erro']=type(exc).__name__+': '+str(exc)
            results.append(result)
            if not result['aprovado']:errors.append(dict(arquivo=row['path'],erro='Replay diverge',detalhe=result))
    return dict(arquivos_verificados=len(manifest['arquivos']),normas=manifest['normas'],replay=len(results),
                replay_aprovados=sum(r['aprovado'] for r in results),problemas=len(errors),detalhes=errors,
                resultados_replay=results,apto_para_publicacao=bool(replay and not errors and len(results)==manifest['normas']))


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--manifesto',type=Path,required=True);ap.add_argument('--saida',type=Path,required=True);ap.add_argument('--replay',action='store_true');a=ap.parse_args();result=verificar(a.manifesto,a.replay)
    with a.saida.open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({k:result[k] for k in ('arquivos_verificados','normas','replay','replay_aprovados','problemas','apto_para_publicacao')}));return int(bool(result['problemas']))


if __name__=='__main__':raise SystemExit(main())
