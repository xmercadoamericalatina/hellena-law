from pathlib import Path
import json,hashlib,subprocess,shutil,collections
B=Path('estaduais/MG/_indice/_auditoria-mg16811-20261016');sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args,input=None):return subprocess.run(['rtk','proxy','git',*args],input=input,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
assert not git('diff','--cached','--name-only').strip()
head=git('rev-parse','HEAD').decode().strip();assert head=='c6dd4f2372ac23f00db298159b3759c68f333824'
approval=B/'aprovacao-publicacao14691-raiz.json';assert sha(approval.read_bytes())=='571489cb793f046856ecbfa73257f7408a7c8792cf23c23909c743f8db3f060b'
a=json.loads(approval.read_text());assert a['HEAD_ausencia']==head
m=Path(a['manifesto']);assert sha(m.read_bytes())==a['sha256_manifesto'];d=json.loads(m.read_text())
for key in ['lista','paths','coorte_manifesto']:
    f=d[key];assert sha(Path(f['path']).read_bytes())==f['sha256']
payload=[json.loads(x) for x in Path(d['lista']['path']).open()];assert len(payload)==58924
expected={r['path']:r['sha256'] for r in payload}
for n,r in enumerate(payload,1):
    p=Path(r['path']);raw=p.read_bytes();assert p.is_file() and not p.is_symlink() and len(raw)==r['bytes'] and sha(raw)==r['sha256'],str(p)
    if n%10000==0:print('PRE_STAGE_SHA',n,flush=True)
shutil.copyfile('/tmp/stage-MG14691-raiz.py',B/'stage-publicacao-raiz.py')
publication=Path('estaduais/MG/_publicacao_mg14691_20261016.json')
publication.write_text(json.dumps({'estado':'aprovado_raiz_aguarda_stage_formato_commit_push','novos_documentos':14691,'HEAD_base':head,'aprovacao':str(approval),'sha256_aprovacao':sha(approval.read_bytes()),'manifesto':str(m),'sha256_manifesto':sha(m.read_bytes()),'coorte':d['coorte_manifesto'],'retidos_anteriores':2088,'retidos_contextuais':32,'retidos_total':2120,'progresso':'Recalculado no indice pelo hook em cada commit; meta original preservada.','limites':a['limites']},ensure_ascii=False,indent=2)+'\n')
wl=Path('WORKLOG.md');s=wl.read_text();entry='## MG14691 em preparação do índice — 16/10/2026\n\n- Raiz conferiu novamente58.924SHA físicos e encadeou aprovação571489cb…f060b aoHEADc6dd4f2372a. Payload14691MD/14691snapshots/14691rawgzip/14691XML+80CSV+80provas;58924arquivos/560MB,maior98MB. Controles ehelper/publicação/WORKLOG adicionais explícitos.\n- Stageúnico /tmp/stage-MG14691-raiz.py emexecução; aguardarSTAGED/exit0 antesformato/commit. O script confere tambémSHA256 deTODOSblobs doíndiceapóshash-object/update-index, preservandoCRLF/fontes. NadaMGcommitado/enviadoainda.\n- Original14723menos32retenções;2120pendências permanecemfora. Provas anteriorescorpo/texto/identidade/status e revisão contextual encadeadas semnovacorreçãoeditorial. Meta100%original segueativa.\n\n';wl.write_text(s.replace('# Continuação da coleta\n\n','# Continuação da coleta\n\n'+entry,1))
paths=[r['path'] for r in payload]+[str(m),d['lista']['path'],d['paths']['path'],str(approval),str(B/'preflight-publicacao-raiz.py'),str(B/'stage-publicacao-raiz.py'),str(publication),'WORKLOG.md']
assert len(paths)==len(set(paths))
for p in paths:
    assert '\n' not in p and Path(p).is_file() and not Path(p).is_symlink() and Path(p).stat().st_size<100000000
    if p not in expected:expected[p]=sha(Path(p).read_bytes())
Path('/tmp/MG14691-publicacao-paths.txt').write_text('\n'.join(paths)+'\n')
oids=git('hash-object','-w','--stdin-paths',input=('\n'.join(paths)+'\n').encode()).decode().splitlines();assert len(oids)==len(paths)
print('OBJETOS',len(oids),flush=True)
git('update-index','--add','-z','--index-info',input=b''.join(('100644 '+oid+'\t'+path+'\0').encode() for path,oid in zip(paths,oids)))
print('INDICE_GRAVADO;conferindo_todos_blobs',flush=True)
data=git('cat-file','--batch',input=''.join(':'+p+'\n' for p in paths).encode());pos=0
for p in paths:
    end=data.index(b'\n',pos);header=data[pos:end].split();assert len(header)==3 and header[1]==b'blob',(p,header);size=int(header[2]);pos=end+1;assert sha(data[pos:pos+size])==expected[p],p;pos+=size;assert data[pos:pos+1]==b'\n';pos+=1
assert pos==len(data)
print('STAGED',len(paths),'arquivos;14691canonicos;TODOS_SHA256_indice_exatos',flush=True)
