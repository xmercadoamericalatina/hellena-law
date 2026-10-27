from pathlib import Path
import subprocess,json,gzip,re,hashlib,unicodedata
from urllib.parse import unquote
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');D=B/'federal/_fonte/auditorias/producao-dec-rfb-20261016';O=D/'revisao-raiz-DEC1951';O.mkdir(exist_ok=True)
def git(*args):return subprocess.check_output(['rtk','proxy','git',*args],cwd=B)
sha=lambda b:hashlib.sha256(b).hexdigest()
paths=set((D/'overlay-contextual-DEC2000/paths-sem-alerta-adicional.txt').read_text().splitlines());rows=[json.loads(l)['inventario'] for l in (D/'coorte-DEC-2000/coorte2000.jsonl').read_text().splitlines()];targets={r['urn']:r for r in rows if r['path'] in paths};assert len(targets)==1951
byidentity={(r['meta']['numero'].replace('.',''),r['meta']['data']):u for u,r in targets.items()}
head=git('rev-parse','HEAD').decode().strip();assert head=='f5b6edc42eddff0c0259f0caec8fdac2a566ce54'
rawpaths=git('ls-tree','-r','--name-only','-z','HEAD','federal','reguladores');allpaths={p for p in rawpaths.decode().split('\0') if p.endswith('.md') and not any(x.startswith(('_','.')) for x in p.split('/'))};assert not allpaths.intersection(paths)
(O/'HEAD-paths-escopo-amplo.txt.gz').write_bytes(gzip.compress(rawpaths))
command=['rtk','proxy','git','grep','-n','-E','^(urn|numero|data|tipo|titulo|fonte):','HEAD','--',':(glob)federal/**/*.md',':(glob)reguladores/**/*.md',':(glob,exclude)**/_*/**']
p=subprocess.Popen(command,cwd=B,stdout=subprocess.PIPE,stderr=subprocess.PIPE);docs={};count=0
with gzip.open(O/'HEAD-cabecalhos-escopo-amplo.txt.gz','wb') as frozen:
 for line in p.stdout:
  frozen.write(line);count+=1;s=line.decode();m=re.match(r'HEAD:(.*?):(\d+):(urn|numero|data|tipo|titulo|fonte):\s*(.*)',s);assert m,s
  path,ln,key,value=m.groups();assert path in allpaths,path
  try:value=json.loads(value)
  except json.JSONDecodeError:value=value.strip()
  if int(ln)<40:docs.setdefault(path,{})[key]=value
  if count%100000==0:print(json.dumps({'linhas_cabecalho':count,'paths':len(docs)}),flush=True)
err=p.stderr.read();p.stdout.close();p.stderr.close();assert p.wait()==0,err
missing=allpaths-set(docs);duplicates=[]
for path,fields in docs.items():
 urn=fields.get('urn');source=unquote(str(fields.get('fonte','')))
 number=re.sub(r'\D','',str(fields.get('numero',''))).lstrip('0');date=str(fields.get('data',''));typ=str(fields.get('tipo','')).casefold();title=str(fields.get('titulo','')).casefold()
 reasons=[]
 if urn in targets:reasons.append('URN exata')
 if any(u in source for u in targets):reasons.append('URN fonte')
 if (number,date) in byidentity and (('decreto' in typ and 'legislativo' not in typ) or ('decreto' in title and 'regulamento' in typ)):reasons.append('numero/data/tipo')
 if reasons:duplicates.append({'path':path,'cabecalho':fields,'motivos':reasons})
summary={'HEAD':head,'escopo':['federal','reguladores'],'canonicos_HEAD':len(allpaths),'cabecalhos_extraidos':len(docs),'sem_cabecalho':sorted(missing),'candidatos':1951,'duplicatas':duplicates,'paths_canonicos_ausentes_HEAD':True,'comando_git_grep':command,'prova_cabecalhos_SHA256':sha((O/'HEAD-cabecalhos-escopo-amplo.txt.gz').read_bytes()),'limite':'Dedup de identidades URN e numero/data/tipo em metadados publicados; nao certifica integridade dos textos.'}
(O/'dedup-HEAD-raiz.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k not in ('comando_git_grep',)},ensure_ascii=False),flush=True)
