from pathlib import Path
import subprocess,json,hashlib,stat
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');O=B/'federal/_fonte/auditorias/producao-dec-rfb-20261016/revisao-raiz-DEC1951'
def git(*args,**kw):return subprocess.check_output(['rtk','proxy','git',*args],cwd=B,**kw)
sha=lambda b:hashlib.sha256(b).hexdigest()
paths=Path('/tmp/DEC1946-publicacao-paths.txt').read_text().splitlines();assert len(paths)==len(set(paths))
assert git('rev-parse','HEAD').decode().strip()=='f5b6edc42eddff0c0259f0caec8fdac2a566ce54'
before=set(git('diff','--cached','--name-only','-z').decode().split('\0'))-{''};assert before<=set(paths)
ledger=json.loads((O/'payload-publicacao-DEC1946-raiz.json').read_text());expected={r['path']:r['sha256'] for r in ledger['arquivos']}
modes=[]
for p in paths:
 f=B/p;st=f.lstat();assert stat.S_ISREG(st.st_mode),p
 assert '\n' not in p and '\t' not in p and '\0' not in p
 if p in expected:assert sha(f.read_bytes())==expected[p],p
 modes.append('100755' if st.st_mode&0o111 else '100644')
print(json.dumps({'arquivos_conferidos':len(paths),'antes_alterados':len(before)}),flush=True)
hashes=git('hash-object','-w','--no-filters','--stdin-paths',input=''.join(json.dumps(p,ensure_ascii=False)+'\n' for p in paths).encode()).decode().splitlines();assert len(hashes)==len(paths)
assert all(len(h)==40 and set(h)<=set('0123456789abcdef') for h in hashes)
print(json.dumps({'blobs_gravados':len(hashes)}),flush=True)
entries=b''.join((mode+' '+h+'\t'+p+'\0').encode() for mode,h,p in zip(modes,hashes,paths))
git('update-index','--add','-z','--index-info',input=entries)
result={'estado':'index_atualizado_com_paths_exatos','paths':len(paths),'metodo':'hash-object --no-filters + update-index --index-info NUL, sem varredura de pathspec','causa_substituicao':'Amostra sample93857 mostrou762/762 amostras em match_pathspec. Processo Gitadd interrompido por algoritmo, nao por timeout; nenhum coletor encerrado.','registros_SHA256':sha(entries)}
(O/'stage-exato-DEC1946-raiz.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False),flush=True)
