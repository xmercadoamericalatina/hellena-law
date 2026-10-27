"""Consulta a relação oficial completa de anexos SAPL e sinaliza conteúdo omitido.

Cache imutável por URL, serialização por host com as travas dos coletores,1rps.
Nenhum erro/bloqueio significa ausência de anexo. Não altera documentos/lotes.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import datetime as dt
import fcntl
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit
sys.path.insert(0,str(Path(__file__).resolve().parent))
from auditar_municipal import metadados
from comum import Rede
RAIZ=Path(__file__).resolve().parent.parent
CACHE=RAIZ/'municipais/_fonte/auditorias/anexos-sapl'


def sha(b):return hashlib.sha256(b).hexdigest()


def sinais(corpo):
    regras={
      'omissao_literal':r'(?:anex[oa]s?.{0,100}n[aã]o.{0,25}(?:publicad|reproduzid|disponibilizad)|n[aã]o.{0,25}(?:publicad|reproduzid).{0,100}anex)',
      'aviso_ou_edital_possivelmente_alheio':r'(?:EDITAL\s+DISPON[IÍ]VEL|ABERTURA\s+DA\s+SESS[AÃ]O(?!\s+LEGISLATIVA)|RECEBIMENTO\s+DAS\s+PROPOSTAS|PREG[AÃ]O\s+(?:ELETR[OÔ]NICO|PRESENCIAL)\s+N[.º°O\s]*\d|EXTRATO\s+(?:DE|DO)\s+(?:CONTRATO|TERMO|DISPENSA|INEXIGIBILIDADE|ATA|ADITIVO))',
      'conteudo_somente_externo':r'(?:anex[oa]s?.{0,160}(?:https?://|www\.)|(?:exclusiv[oa]mente|somente|apenas).{0,100}(?:https?://|www\.))',
    }
    out=[]
    for nome,pattern in regras.items():
        for m in re.finditer(pattern,corpo,re.I):out.append({'regra':nome,'offset':m.start(),'trecho':corpo[max(0,m.start()-180):m.end()+300]})
    codigos=set(re.findall(r'c[oó]digo\s+identificador\s*[:\-]?\s*([a-z0-9]{6,})',corpo,re.I))
    if len(codigos)>1:out.append({'regra':'multiplos_codigos_identificadores','codigos':sorted(codigos)})
    refs=[]
    for m in re.finditer(r'\banex[oa]s?\b',corpo,re.I):
        trecho=corpo[max(0,m.start()-150):m.end()+250]
        if re.search(r'\b(?:deste|desta|este|esta|presente|integrante|integra|integrantes|aprovad[oa]|aprova)\b',trecho,re.I):refs.append({'offset':m.start(),'trecho':trecho})
    return out,refs


def consultar_host(host):
    pasta=CACHE/host;pasta.mkdir(parents=True,exist_ok=True)
    trava=RAIZ/'municipais/_indice/organicas-sapl/travas'/(host+'.lock');trava.parent.mkdir(parents=True,exist_ok=True)
    with trava.open('a') as f:
        try:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return {'host':host,'estado':'pendente_coletor_ativo','anexos':[],'evidencias':[]}
        rede=Rede(rps=1);pagina=1;vistos=set();anexos={};evidencias=[];total=None
        try:
            while pagina:
                if pagina in vistos:raise ValueError('paginação cíclica')
                vistos.add(pagina);url=f'https://{host}/api/norma/anexonormajuridica/?page_size=100&page={pagina}'
                cache=pasta/(sha(url.encode())+'.json');meta=cache.with_suffix('.meta.json')
                if cache.exists() and meta.exists():
                    info=json.loads(meta.read_text());b=cache.read_bytes()
                    if sha(b)!=info['sha256']:raise ValueError('cache de anexo mudou')
                    status=info['status']
                else:
                    status,b,ct=rede.get(url,accept='application/json',tentativas=1,timeout=35)
                    info={'url':url,'status':status,'content_type':ct,'sha256':sha(b),'capturado_em':dt.datetime.now().isoformat()}
                    with cache.open('xb') as out:out.write(b)
                    with meta.open('x') as out:json.dump(info,out,ensure_ascii=False,indent=2)
                evidencias.append({'url':url,'path':str(cache.relative_to(RAIZ)),'sha256':sha(b),'status':status,'metadata':str(meta.relative_to(RAIZ))})
                if status!=200:raise ValueError('API de anexos HTTP'+str(status))
                data=json.loads(b);pag=data.get('pagination');rows=data.get('results')
                if not isinstance(pag,dict) or not isinstance(rows,list):raise ValueError('formato/paginação de anexos não reconhecido')
                if total is None:total=int(pag['total_entries'])
                if int(pag['total_entries'])!=total:raise ValueError('índice mudou durante paginação')
                for r in rows:
                    if not all(k in r for k in ('id','norma','anexo_arquivo')):raise ValueError('registro de anexo sem identidade/arquivo')
                    if str(r['id']) in anexos:raise ValueError('anexo repetido na paginação')
                    anexos[str(r['id'])]=r
                pagina=pag.get('next_page')
                if pagina is not None:pagina=int(pagina)
            if len(anexos)!=total:raise ValueError('total de anexos diverge da paginação completa')
            return {'host':host,'estado':'indice_completo','anexos':list(anexos.values()),'evidencias':evidencias,'total':total}
        except Exception as e:return {'host':host,'estado':'pendente_api','erro':str(e),'anexos':[],'evidencias':evidencias}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--lista',type=Path,action='append',required=True);ap.add_argument('--saida',type=Path,required=True);ap.add_argument('--trabalhadores',type=int,default=4);a=ap.parse_args();a.saida.mkdir(parents=True,exist_ok=False)
    paths=list(dict.fromkeys(p for lista in a.lista for p in lista.read_text().splitlines() if p));docs=[];hosts=set()
    for rel in paths:
        p=RAIZ/rel;b=p.read_bytes();m=metadados(b.decode());corpo=b.decode().split('\n---\n',1)[1].lstrip('\n').split('\n\n',1)[1];alertas,refs=sinais(corpo)
        u=urlsplit(m['fonte']);sapl=bool(re.fullmatch(r'/norma/\d+/?',u.path))
        r={'path':rel,'sha256':sha(b),'fonte':m['fonte'],'host':u.hostname if sapl else None,'id':u.path.strip('/').split('/')[-1] if sapl else None,'alertas':alertas,'remissoes_ao_proprio_anexo_para_revisao':refs}
        docs.append(r)
        if sapl:hosts.add(u.hostname)
    results={}
    with ThreadPoolExecutor(max_workers=a.trabalhadores) as pool:
        futures={pool.submit(consultar_host,h):h for h in sorted(hosts)}
        for fut in as_completed(futures):
            r=fut.result();results[r['host']]=r;p=a.saida/('host-'+r['host']+'.json')
            with p.open('x') as f:json.dump(r,f,ensure_ascii=False,indent=2)
            print(json.dumps({'host':r['host'],'estado':r['estado'],'total':r.get('total'),'hosts_concluidos':len(results),'hosts':len(hosts)}),flush=True)
    aprovados=[];retidos=[]
    for d in docs:
        d['anexos_proprios']=[]
        if d['host']:
            result=results[d['host']];d['estado_api']=result['estado'];d['anexos_proprios']=[x for x in result['anexos'] if str(x['norma'])==d['id']]
        else:d['estado_api']='fonte_nao_sapl_requer_revisao_dos_links'
        # Qualquer ambiguidade exige revisão: inclusive remissão textual ao próprio anexo.
        d['aprovado_sem_pendencias_detectadas']=d['estado_api']=='indice_completo' and not d['anexos_proprios'] and not d['alertas'] and not d['remissoes_ao_proprio_anexo_para_revisao']
        (aprovados if d['aprovado_sem_pendencias_detectadas'] else retidos).append(d)
    with (a.saida/'overlay.json').open('x') as f:json.dump({'criterio':__doc__,'listas_substituidas_para_publicacao':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in a.lista],'aprovados':aprovados,'retidos':retidos},f,ensure_ascii=False,indent=2)
    for nome,rows in [('aprovados',aprovados),('retidos',retidos)]:
        with (a.saida/(nome+'.paths.txt')).open('x') as f:f.write(''.join(x['path']+'\n' for x in rows))
    receipt={'aprovados':len(aprovados),'retidos':len(retidos),'hosts':len(hosts),'artefatos':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in sorted(a.saida.iterdir()) if p.is_file()],'script_sha256':sha(Path(__file__).read_bytes())}
    with (a.saida/'entrega-final.json').open('x') as f:json.dump(receipt,f,ensure_ascii=False,indent=2)
    print(json.dumps(receipt,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
