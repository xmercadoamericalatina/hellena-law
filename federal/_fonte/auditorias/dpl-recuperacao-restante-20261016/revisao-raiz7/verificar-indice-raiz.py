import pathlib,subprocess,json,hashlib,re,gzip
P=pathlib.Path('/tmp/recuperacao7-publicacao-paths.txt');paths=P.read_text().splitlines();actual=set(subprocess.check_output(['rtk','proxy','git','diff','--cached','--name-only','-z']).decode().split('\0'))-{''};assert not actual-set(paths)
proc=subprocess.Popen(['rtk','proxy','git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
def read(name):
 proc.stdin.write((name+'\n').encode());proc.stdin.flush();h=proc.stdout.readline().split();assert h[1]==b'blob',name;b=proc.stdout.read(int(h[2]));assert proc.stdout.read(1)==b'\n';return b
unchanged=[]
for name in paths:
 data=pathlib.Path(name).read_bytes();assert read(':'+name)==data,name
 if name not in actual:
  assert read('HEAD:'+name)==data,name;unchanged.append(name)
proc.stdin.close();assert proc.wait()==0
B=pathlib.Path('federal/_fonte/auditorias/dpl-recuperacao-restante-20261016');frozen={}
for folder,mn in [('candidatos3-preambulo','manifesto-congelado3.json'),('candidatos4-sem-artigos','manifesto-congelado4.json')]:frozen.update({r['path']:r['sha256'] for r in json.loads((B/folder/mn).read_text())['arquivos']})
r=subprocess.run(['rtk','proxy','git','diff','--cached','--check'],capture_output=True);warnings=[]
for line in r.stdout.decode().splitlines():
 m=re.match(r'(.+):(\d+): (.+)',line)
 if not m:continue
 path,num,kind=m.groups();p=pathlib.Path(path);s=p.read_text().splitlines()[int(num)-1]
 if path in frozen:
  assert hashlib.sha256(p.read_bytes()).hexdigest()==frozen[path];reason='fonte/candidato congelado SHA exato'
 elif kind=='trailing whitespace.' and s.endswith('  ') and not s.endswith('   ') and s.strip():reason='hardbreak GFM'
 elif kind=='new blank line at EOF.' and not s.strip():reason='linha final preservada'
 else:raise AssertionError((path,num,kind,s))
 warnings.append({'path':path,'linha':int(num),'motivo':reason})
assert r.returncode in (0,2) and (not r.returncode or warnings)
O=B/'revisao-raiz7';result={'paths_lista':len(paths),'paths_alterados_indice':len(actual),'blobs_bytes_exatos':len(paths),'fontes_ja_HEAD_bytes_exatos':unchanged,'diffcheck_exit':r.returncode,'whitespace_preservados':warnings,'nota':'Lista inclui7fontesgzip ja publicadas; ausencia no diff nao e ausencia na publicacao. HEAD e indice conferidos byte a byte.'}
(O/'verificacao-indice-whitespace.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');(O/'diffcheck.txt.gz').write_bytes(gzip.compress(r.stdout,mtime=0));print(json.dumps({'blobs_exatos':len(paths),'alterados':len(actual),'ja_HEAD_exatos':len(unchanged),'whitespace_preservados':len(warnings)}))
