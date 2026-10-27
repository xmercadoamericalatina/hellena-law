from pathlib import Path
import subprocess,json,hashlib,stat,shutil
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');O=B/'estaduais/_indice/_recuperacao-v2-20261016/revisao-raiz-df11'
git=lambda *a,**kw:subprocess.check_output(['rtk','proxy','git',*a],cwd=B,**kw)
sha=lambda b:hashlib.sha256(b).hexdigest()
assert git('rev-parse','HEAD').decode().strip()=='7abcccab19ed386a0fa3c0ba6f4c8af97e851e50' and not git('diff','--cached','--name-only').strip()
paths=Path('/tmp/DF11-publicacao-paths.txt').read_text().splitlines();assert len(set(paths))==len(paths)
expected={r['path']:r['sha256'] for r in json.loads((O/'payload-DF11-raiz.json').read_text())['arquivos']}
mode=[]
for p in paths:
 f=B/p;st=f.lstat();assert stat.S_ISREG(st.st_mode)
 if p in expected:assert sha(f.read_bytes())==expected[p],p
 mode.append('100755' if st.st_mode&0o111 else '100644')
hashes=git('hash-object','-w','--no-filters','--stdin-paths',input=''.join(json.dumps(p,ensure_ascii=False)+'\n' for p in paths).encode()).decode().splitlines();assert len(hashes)==len(paths)
assert all(len(h)==40 and set(h)<=set('0123456789abcdef') for h in hashes)
entries=b''.join((m+' '+h+'\t'+p+'\0').encode() for m,h,p in zip(mode,hashes,paths));git('update-index','--add','-z','--index-info',input=entries)
report={'estado':'paths_exatos_no_index','paths':len(paths),'metodo':'hash-object --no-filters + update-index --index-info NUL','registros_SHA256':sha(entries)}
(O/'stage-DF11-raiz.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report))
