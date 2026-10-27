"""Congela a revisão offline de retenções antigas por epígrafe, sem recaptura.

Não seleciona identidades já aprovadas em qualquer gate nem casos previamente
examinados nesta recuperação. Cada lote preserva origem e índice de anexos.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parent.parent


def sha(b):return hashlib.sha256(b).hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--saida',type=Path,required=True)
    ap.add_argument('--tamanho-lote',type=int,default=1000)
    a=ap.parse_args()
    base=ROOT/'municipais/_lotes';pool={};approved=set();excluded=set();origins=[]
    for p in sorted(base.glob('*-textos-articulados-gates-*/resultados.jsonl')):
        if not (p.parent/'manifesto.json').exists():continue
        raw=p.read_bytes();origins.append(dict(arquivo=str(p.relative_to(ROOT)),sha256=sha(raw)))
        for r in map(json.loads,raw.decode().splitlines()):
            key=(r['host'],r['ta_id'])
            if r.get('aprovado_nestes_gates'):approved.add(key)
            elif r.get('pendencia_gate')=='Epígrafe literal não confirma número e data':pool.setdefault(key,(r,p))
    for p in sorted(base.glob('*-recuperacao-identidade-ta-gates-*/resultados.jsonl')):
        if (p.parent/'manifesto.json').exists():excluded.update((r['host'],r['ta_id']) for r in map(json.loads,p.read_text().splitlines()))
    hosts={}
    for key,(r,p) in pool.items():
        if key not in approved and key not in excluded:hosts.setdefault(r['host'],[]).append((r,p))
    selected=[]
    for group in itertools.zip_longest(*(hosts[h] for h in sorted(hosts))):
        for row in group:
            if row:selected.append(row)
            if len(selected)==a.tamanho_lote:break
        if len(selected)==a.tamanho_lote:break
    if not selected:raise ValueError('Nenhuma retenção ainda não revista')
    # A relação de anexos de um host precisa ser o mesmo snapshot para todos os
    # registros selecionados; não mesclar silenciosamente duas edições.
    annex={}
    for r,p in selected:
        src=p.parent/(r['host']+'.anexos.json');raw=src.read_bytes();digest=sha(raw)
        if r['host'] in annex and annex[r['host']][1]!=digest:raise ValueError('Índices de anexos distintos: '+r['host'])
        annex[r['host']]=(src,digest)
    a.saida.mkdir(exist_ok=False)
    for host,(src,digest) in annex.items():
        folder=a.saida/host;folder.mkdir()
        clean=[{k:v for k,v in r.items() if k not in ('aprovado_nestes_gates','pendencia_gate','gates')} for r,p in selected if r['host']==host]
        (folder/'resultados.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in clean))
        shutil.copyfile(src,folder/'anexos-index.json')
    snapshot=dict(criterio=__doc__,selecionados=len(selected),retidos_disponiveis=sum(map(len,hosts.values())),
        origens=origins,identidades=[dict(host=r['host'],ta_id=r['ta_id'],norma_id=r['norma_id'],gate_anterior=str(p.relative_to(ROOT)),pendencia_anterior=r['pendencia_gate']) for r,p in selected],
        anexos=[dict(host=h,arquivo=str(p.relative_to(ROOT)),sha256=s) for h,(p,s) in annex.items()],codigo_sha256=sha(Path(__file__).read_bytes()),limite='Reanálise de candidatos antigos retidos, sem alteração das fontes, datas de captura, textos ou listas anteriores. Não é coleta nova nem aprovação automática.')
    (a.saida/'snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(selecionados=len(selected),disponiveis=snapshot['retidos_disponiveis'])))


if __name__=='__main__':main()
