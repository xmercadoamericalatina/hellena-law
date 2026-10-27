from pathlib import Path
from html.parser import HTMLParser
import re,json,gzip,sys,hashlib
from cmarkgfm import github_flavored_markdown_to_html as render
from cmarkgfm.cmark import Options
sys.path.insert(0,str(Path('scripts').resolve()));import baixar_camara as cam
B=Path('federal/_fonte/auditorias/dpl-auditoria-20261016');passed={r['path'] for r in map(json.loads,(B/'verificacao-raiz-identidade-3273.jsonl').open())};inv={r['path']:r for r in map(json.loads,(B/'inventario5409-revisado.jsonl').open())}
class P(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.stack=[];self.chars=[];self.feed(s)
 def handle_starttag(self,t,a):
  if t not in ('br','hr','img','col','input','wbr','meta','link'):self.stack.append((t,dict(a)))
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==t:self.stack=self.stack[:i];break
 def handle_data(self,d):
  if any(t in ('head','script','style','title') for t,_ in self.stack):return
  bold=any(t in ('b','strong') or re.search(r'font-weight:(?:bold|[7-9]00)',re.sub(r'\s+','',a.get('style','').lower())) for t,a in self.stack);italic=any(t in ('i','em') or 'font-style:italic' in re.sub(r'\s+','',a.get('style','').lower()) for t,a in self.stack)
  self.chars.extend((c,bool(bold),italic) for c in d if not c.isspace() and c!='\ufeff')
rows=[]
for n,path in enumerate(sorted(passed),1):
 r=inv[path];src=cam.corpo_norma(gzip.decompress(Path(r['fonte_cache']['snapshot']).read_bytes()).decode());md=Path(path).read_text().split('\n---\n',1)[1].lstrip().split('\n\n',1)[1];a=P(src).chars;b=P(render(md,options=Options.CMARK_OPT_UNSAFE)).chars;assert ''.join(c for c,_,_ in a)==''.join(c for c,_,_ in b)
 losses=[{'offset':i,'caractere':x[0],'fonte':x[1:],'GFM':y[1:]} for i,(x,y) in enumerate(zip(a,b)) if (x[1] and not y[1]) or (x[2] and not y[2])];rows.append({'path':path,'caracteres_negrito':sum(x[1] for x in a),'caracteres_italico':sum(x[2] for x in a),'perdas':losses})
 if n%750==0:print('BOLDITALIC',n,flush=True)
p=B/'verificacao-raiz-negrito-italico-3273.jsonl';p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows));print('FINAL',len(rows),'comperdas',sum(bool(r['perdas']) for r in rows),flush=True)
