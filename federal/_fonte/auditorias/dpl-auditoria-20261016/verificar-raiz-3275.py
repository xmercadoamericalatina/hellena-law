from pathlib import Path
import sys,json,gzip,re,hashlib,concurrent.futures,subprocess,threading
from html.parser import HTMLParser
from cmarkgfm import github_flavored_markdown_to_html as render
from cmarkgfm.cmark import Options
sys.path.insert(0,str(Path('scripts').resolve()));import baixar_camara as cam
B=Path('federal/_fonte/auditorias/dpl-auditoria-20261016');T=Path('federal/_fonte/auditorias/dpl-triestado3270-20261016');sha=lambda b:hashlib.sha256(b).hexdigest()
m=Path('federal/_preparacao_dpl_triestado3270_20261016.json');assert sha(m.read_bytes())=='52ecd68b15dea2f68cb49d5c836cb6183ec96f4d0fa908074be6bad2a3ae90dd';manifest=json.loads(m.read_text())
for f in manifest['arquivos']:assert sha(Path(f['path']).read_bytes())==f['sha256']
ledger=[json.loads(x) for x in (T/'ledger3270.jsonl').open()];ready=json.loads((B/'coorte-verificada_sem_alteracao.json').read_text());meta={r['path']:r for r in json.loads((B/'coorte-verificada_corpo_pendente_triestado.json').read_text())+ready};assert len(meta)==3275
back={r['path']:r for r in map(json.loads,gzip.decompress((B/'backup-md.jsonl.gz').read_bytes()).decode().splitlines())};ld={r['path_canonico']:r for r in ledger}
render_lock=threading.Lock()
def safe_render(body):
 with render_lock:return render(body,options=Options.CMARK_OPT_UNSAFE)
class Chars(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.stack=[];self.chars=[];self.tags=[];self.feed(s);self.close()
 def handle_starttag(self,t,a):
  self.tags.append(t)
  if t not in ('br','hr','img','meta','link','input','col','wbr'):self.stack.append((t,dict(a)))
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==t:self.stack=self.stack[:i];break
 def handle_data(self,d):
  if any(t in ('head','script','style','title') for t,_ in self.stack):return
  f=(any(t in ('s','strike','del') or 'line-through' in a.get('style','') for t,a in self.stack),any(t=='sup' for t,_ in self.stack),any(t=='sub' for t,_ in self.stack))
  self.chars.extend((c,f) for c in d if not c.isspace() and c!='\ufeff')
def check(item):
 path,r=item;old=Path(path).read_bytes();assert sha(old)==r['sha256_md'];assert back[path]['texto'].encode()==old and back[path]['sha256_md']==sha(old)
 if path in ld:
  d=ld[path];new=Path(d['path_candidato']).read_bytes();assert sha(new)==d['sha256_depois'];a=d['offset_byte_inicio'];assert old[:a]+b'revogada: null'+old[a+len(b'revogada: false'):]==new
 else:new=old
 body=new.decode().split('\n---\n',1)[1].lstrip().split('\n\n',1)[1]
 f=r['fonte'];gz=Path(f['snapshot']).read_bytes();assert sha(gz)==f['sha256_arquivo'];raw=gzip.decompress(gz);assert sha(raw)==f['sha256_fonte'];frag=cam.corpo_norma(raw.decode());source=Chars(frag);target=Chars(safe_render(body));holds=[]
 assert body==cam.convert(frag)
 if source.chars!=target.chars:
  a=source.chars;b=target.chars;k=next((i for i,(c,d) in enumerate(zip(a,b)) if c!=d),min(len(a),len(b)));holds.append({'gate':'caracteres_formato_GFM','offset':k,'fonte':source.chars[max(0,k-30):k+80],'GFM':target.chars[max(0,k-30):k+80]})
 visual=set(source.tags)&{'table','img','svg','object','embed','canvas','iframe','math'}
 if visual:holds.append({'gate':'estrutura_visual_inesperada','tags':sorted(visual)})
 plain=''.join(c for c,_ in source.chars)
 markers=re.findall(r'(?:suprimid|omitid|ileg[ií]vel|n[aã]o.{0,15}(?:digitad|reproduzid|transcrit)|impossibilidade.t[eé]cnica|\[\.\.\.\])',plain,re.I)
 if markers:holds.append({'gate':'lacuna_contextual','marcadores':markers})
 return {'path':path,'sha256_antes':sha(old),'sha256_depois':sha(new),'source_sha256':sha(raw),'caracteres':len(source.chars),'retencoes':holds,'corpo_exato_core':True,'backup_e_delta_integral_conferidos':True}
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for n,r in enumerate(pool.map(check,meta.items()),1):
  rows.append(r)
  if n%500==0:print('RAIZDPL',n,'retidos',sum(bool(x['retencoes']) for x in rows),flush=True)
out=B/'verificacao-raiz-3275.jsonl';out.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows));print('FINAL',len(rows),'retidos',sum(bool(x['retencoes']) for x in rows),flush=True)
