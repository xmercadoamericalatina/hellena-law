from pathlib import Path
import json,hashlib,subprocess
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');O=B/'federal/_fonte/auditorias/producao-dec-rfb-20261016/revisao-raiz-DEC1951'
git=lambda *a,**kw:subprocess.check_output(['rtk','proxy','git',*a],cwd=B,**kw)
sha=lambda b:hashlib.sha256(b).hexdigest()
paths=Path('/tmp/DEC1946-publicacao-paths.txt').read_text().splitlines();assert len(paths)==len(set(paths))
changed=set(git('diff','--cached','--name-only','-z').decode().split('\0'))-{''};assert changed<=set(paths)
canonical={p for p in changed if p.startswith('federal/decretos/') and p.endswith('.md')};assert len(canonical)==1946
ledger=json.loads((O/'payload-publicacao-DEC1946-raiz.json').read_text());expected={r['path']:r['sha256'] for r in ledger['arquivos']}
approval=json.loads((O/'aprovacao-publicacao-DEC1946-raiz.json').read_text());assert {r['path'] for r in approval['documentos']}==canonical
raw=git('cat-file','--batch',input=''.join(':'+p+'\n' for p in paths).encode());offset=0;total=0
for p in paths:
 end=raw.index(b'\n',offset);header=raw[offset:end].decode().split();assert len(header)==3 and header[1]=='blob',(p,header)
 n=int(header[2]);start=end+1;blob=raw[start:start+n];assert len(blob)==n and raw[start+n:start+n+1]==b'\n';offset=start+n+1
 physical=(B/p).read_bytes();assert blob==physical,p
 if p in expected:assert sha(blob)==expected[p],p
 total+=n
assert offset==len(raw)
for r in approval['documentos']:assert expected[r['path']]==r['sha256_MD']
result={'estado':'index_igual_payload_disco_e_aprovacao','HEAD_base':approval['HEAD_base'],'paths_verificados':len(paths),'paths_alterados':len(changed),'canonicos_novos':1946,'bytes':total,'sem_paths_inesperados':True,'PROGRESSO':'Hook recalcula a partir do index no commit; verificar apos commit.'}
(O/'verificacao-index-DEC1946-raiz.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
