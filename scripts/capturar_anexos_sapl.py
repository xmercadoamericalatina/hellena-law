"""Preserva os arquivos adicionais declarados na API SAPL, sem publicar normas."""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import datetime as dt
import fcntl
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit
sys.path.insert(0,str(Path(__file__).resolve().parent))
from comum import Rede
RAIZ=Path(__file__).resolve().parent.parent


def sha(b):return hashlib.sha256(b).hexdigest()


def baixar_host(host,items,pasta):
    trava=RAIZ/'municipais/_indice/organicas-sapl/travas'/(host+'.lock');out=[]
    with trava.open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return [{'host':host,'estado':'pendente_coletor_ativo','itens':items}]
        rede=Rede(rps=1)
        for item in items:
            r={**item,'estado':'pendente'};a=item['anexo'];url=a['anexo_arquivo'];u=urlsplit(url)
            if u.hostname==host:url='https://'+url.split('://',1)[1]
            base=pasta/host;base.mkdir(parents=True,exist_ok=True);p=base/(str(a['id'])+'.bin');meta=p.with_suffix('.meta.json')
            try:
                if p.exists() and meta.exists():
                    info=json.loads(meta.read_text());b=p.read_bytes()
                    if sha(b)!=info['sha256']:raise ValueError('arquivo de anexo mudou no cache')
                else:
                    status,b,ct=rede.get(url,tentativas=1,timeout=90)
                    if status!=200:raise ValueError('anexo HTTP'+str(status))
                    info={'url_original':a['anexo_arquivo'],'url_captura':url,'status':status,'content_type':ct,'sha256':sha(b),'capturado_em':dt.datetime.now().isoformat()}
                    with p.open('xb') as f:f.write(b)
                    with meta.open('x') as f:json.dump(info,f,ensure_ascii=False,indent=2)
                r.update({'estado':'capturado','path':str(p.relative_to(RAIZ)),'sha256':sha(b),'metadata':str(meta.relative_to(RAIZ)),'url':url,'bytes':len(b)})
            except Exception as e:r['erro']=str(e)
            out.append(r)
    return out


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--overlay',type=Path,required=True);ap.add_argument('--saida',type=Path,required=True);a=ap.parse_args();a.saida.mkdir(parents=True,exist_ok=False)
    dados=json.loads(a.overlay.read_text());grupos={}
    for norma in dados['retidos']+dados['aprovados']:
        for anexo in norma.get('anexos_proprios',[]):grupos.setdefault(norma['host'],[]).append({'norma':norma['path'],'anexo':anexo,'host':norma['host']})
    registros=[];pasta=RAIZ/'municipais/_fonte/auditorias/anexos-sapl/arquivos'
    with ThreadPoolExecutor(max_workers=4) as pool:
        futs=[pool.submit(baixar_host,h,items,pasta) for h,items in grupos.items()]
        for fut in as_completed(futs):
            rows=fut.result();registros.extend(rows)
            print(json.dumps([{'norma':r.get('norma'),'id':r.get('anexo',{}).get('id'),'estado':r['estado'],'bytes':r.get('bytes')} for r in rows],ensure_ascii=False),flush=True)
    with (a.saida/'manifesto.json').open('x') as f:json.dump({'overlay':str(a.overlay),'sha256_overlay':sha(a.overlay.read_bytes()),'arquivos':registros,'critério':'Apenas captura; nenhum arquivo é norma adicional nem conteúdo declarado integrado sem revisão.'},f,ensure_ascii=False,indent=2)


if __name__=='__main__':main()
