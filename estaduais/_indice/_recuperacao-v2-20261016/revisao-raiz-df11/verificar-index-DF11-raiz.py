from pathlib import Path
import subprocess,json,hashlib
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');O=B/'estaduais/_indice/_recuperacao-v2-20261016/revisao-raiz-df11'
git=lambda *a,**kw:subprocess.check_output(['rtk','proxy','git',*a],cwd=B,**kw)
sha=lambda b:hashlib.sha256(b).hexdigest()
paths=Path('/tmp/DF11-publicacao-paths.txt').read_text().splitlines();changed=set(git('diff','--cached','--name-only','-z').decode().split('\0'))-{''};assert changed<=set(paths)
a=json.loads((O/'aprovacao-DF11-raiz.json').read_text());canonical={p for p in changed if p.startswith('estaduais/DF/') and p.endswith('.md')};assert canonical=={r['path'] for r in a['documentos']} and len(canonical)==11
expected={r['path']:r['sha256'] for r in json.loads((O/'payload-DF11-raiz.json').read_text())['arquivos']}
raw=git('cat-file','--batch',input=''.join(':'+p+'\n' for p in paths).encode());offset=0;total=0
for p in paths:
 end=raw.index(b'\n',offset);head=raw[offset:end].decode().split();assert head[1]=='blob';size=int(head[2]);start=end+1;blob=raw[start:start+size];assert blob==(B/p).read_bytes(),p
 if p in expected:assert sha(blob)==expected[p],p
 offset=start+size+1;total+=size
assert offset==len(raw)
for r in a['documentos']:assert sha((B/r['path']).read_bytes())==expected[r['path']]==r['new_sha256']
report={'estado':'index_disco_payload_aprovacao_exatos','paths_verificados':len(paths),'paths_alterados':len(changed),'canônicos_novos':11,'bytes':total,'sem_paths_inesperados':True}
(O/'verificacao-index-DF11-raiz.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
