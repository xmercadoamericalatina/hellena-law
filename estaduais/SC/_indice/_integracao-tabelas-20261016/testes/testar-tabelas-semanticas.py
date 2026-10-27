import json,re,gzip,hashlib,importlib.util
from pathlib import Path
from html.parser import HTMLParser
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(path,name):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
new=load('scripts/html2md.py','new');old=load('/tmp/html2md-5f175-congelado.py','old')
class Modelo(HTMLParser):
 def __init__(self):super().__init__();self.tables=[];self.ts=[];self.cells=[];self.stack=[]
 def handle_starttag(self,t,a):
  a=dict(a);parent=self.stack[-1][1] if self.stack else (False,False,False);style=a.get('style','').lower().replace(' ','');f=(parent[0] or t in ('b','strong') or 'font-weight:bold' in style or 'font-weight:700' in style,parent[1] or t in ('i','em') or 'font-style:italic' in style,parent[2] or t in ('s','strike','del') or 'line-through' in style)
  if t not in ('br','col','img','hr','input','meta','link','wbr'):self.stack.append((t,f))
  if t=='table':
   self.tables.append(dict(rows=[],sections=[]));self.ts.append(self.tables[-1])
  elif t in ('thead','tbody','tfoot','caption') and self.ts:self.ts[-1]['sections'].append(t)
  elif t=='tr' and self.ts:self.ts[-1]['rows'].append([])
  elif t in ('td','th') and self.ts:
   c=dict(tag=t,rowspan=int(a.get('rowspan','1')),colspan=int(a.get('colspan','1')),scope=a.get('scope'),headers=a.get('headers'),id=a.get('id'),chars=[],blocks=[])
   assert self.ts[-1]['rows'],'célula semlinha';self.ts[-1]['rows'][-1].append(c);self.cells.append(c)
  if t in ('p','br','ul','ol','li','blockquote','sup','sub'):
   for c in self.cells:c['blocks'].append('+'+t)
 def handle_endtag(self,t):
  if t in ('p','ul','ol','li','blockquote','sup','sub'):
   for c in self.cells:c['blocks'].append('-'+t)
  if t in ('td','th') and self.cells:self.cells.pop()
  if t=='table' and self.ts:self.ts.pop()
  for k in range(len(self.stack)-1,-1,-1):
   if self.stack[k][0]==t:del self.stack[k:];break
 def handle_data(self,s):
  f=self.stack[-1][1] if self.stack else (False,False,False)
  for c in self.cells:c['chars'].extend((ch,*f) for ch in s if not ch.isspace())
def model(s):
 p=Modelo();p.feed(s);return p.tables
def grids(tables):
 result=[]
 for t in tables:
  occupied={};rows=t['rows']
  for y,row in enumerate(rows):
   x=0
   for n,c in enumerate(row):
    while (y,x) in occupied:x+=1
    height=c['rowspan'] or len(rows)-y;width=c['colspan'];assert width>0
    for dy in range(height):
     for dx in range(width):
      key=(y+dy,x+dx);assert key not in occupied,('overlap',key);occupied[key]=(y,n)
    x+=width
  result.append(sorted((list(k),list(v)) for k,v in occupied.items()))
 return result
fixtures=[
 '<table><caption>Título</caption><thead><tr><th scope="col">A</th><th>B</th></tr></thead><tbody><tr><td rowspan="2">X</td><td>1</td></tr><tr><td>2</td></tr></tbody></table>',
 '<table><tr><td colspan="2">A</td><td rowspan="2">B</td></tr><tr><td>C</td><td>D</td></tr></table>',
 '<table><tr><td><p>A</p><p>B</p><p>C</p><p>D</p></td><td>E</td></tr></table>',
 '<table><tr><td>A<table><tr><td>B</td></tr></table>C</td><td>D</td></tr></table>',
 '<div style="text-decoration:line-through"><table><tr><td>−</td><td><strong>B</strong></td></tr></table></div>',
 '<table style="text-decoration:line-through"><tr><td>A</td><td>B</td></tr></table>',
 '<table><tr style="text-decoration:line-through"><td>A</td></tr><tr><td style="text-decoration:line-through">B</td></tr></table>',
 '<table><tr><td><em>i <strong>b</strong></em><del>−</del>5<br>x<sup>2</sup></td></tr></table>',
 '<p>Antes</p><table><tr><td>A</td></tr></table><p>Depois</p>',
 '<table onclick="evil()"><tr><td style="color:red" id="a" onmouseover="evil()">A<script>evil()</script></td></tr></table>'
]
results=[]
for i,s in enumerate(fixtures):
 out=new.convert(s)
 if i==9:assert 'script' not in out and 'onclick' not in out and 'style=' not in out and 'evil' not in out
 else:assert model(s)==model(out),(i,model(s),model(out));assert grids(model(s))==grids(model(out))
 results.append(dict(id=i,saida=out))
for s in ['<table><tr><td>A</td></tr>','<table><tr><td rowspan="x">A</td></tr></table>','<table><tr><td><img src="x"></td></tr></table>']:
 try:new.convert(s)
 except ValueError:continue
 raise AssertionError('não recusou tabela inválida/visual')
rows=[r for r in json.load(open('estaduais/SC/_indice/_reparos-tachado-20261016/manifesto-preparado.json'))['documentos'] if r['tabelas_HTML']];real=[];errors=[]
for r in rows:
 raw=gzip.decompress(Path(r['cache']).read_bytes());s=raw.decode();s=re.sub(r'<s>\s*(&deg;|&ordm;|&ordf;|°|º|ª|o|a)\s*</s>',r'\1',s);out=new.convert(s);a=model(s);b=model(out)
 try:assert a==b,'árvore/células/formatos divergentes';assert grids(a)==grids(b),'grade divergente'
 except Exception as e:errors.append(dict(path=r['path'],erro=str(e)))
 path=Path('estaduais/SC/_indice/_reparos-tachado-tabelas-20261016/candidatos')/r['path'];path.parent.mkdir(parents=True,exist_ok=True);before=Path(r['path']).read_text();front,body=before.split('\n---\n',1);newbody=body.splitlines()[0]+'\n\n'+out;candidate=front+'\n---\n'+newbody;path.write_text(candidate)
 real.append(dict(path=r['path'],fonte_sha256=sha(raw),tabelas_fonte=len(a),tabelas_saida=len(b),celulas=sum(len(row) for t in a for row in t['rows']),arvore_celulas_igual=a==b,grade_igual=not any(e['path']==r['path'] for e in errors),candidato=str(path),sha256_candidato=sha(candidate.encode()),sha256_antes=sha(before.encode())))
 print(r['path'],len(a),'erros',len(errors),flush=True)
unchanged=[]
for r in json.load(open('/tmp/html2md-tachado-regressoes-final.json'))['reais_sem_tachado']:
 raw=gzip.decompress(Path(r['cache_original']).read_bytes());s=raw.decode('utf8',errors='replace')
 if re.search(r'<table\b',s,re.I):continue
 assert new.convert(s)==old.convert(s),r['path'];unchanged.append(r['path'])
d=dict(conversor_sha256=sha(Path('scripts/html2md.py').read_bytes()),baseline_sha256=sha(Path('/tmp/html2md-5f175-congelado.py').read_bytes()),fixtures=results,negativos_recusados=3,reais=real,total_tabelas=sum(r['tabelas_fonte'] for r in real),sem_tabelas_byteidenticos=unchanged,erros=errors);Path('/tmp/html2md-tabelas-regressoes.json').write_text(json.dumps(d,ensure_ascii=False,indent=2));print('FINAL',len(real),d['total_tabelas'],'erros',errors,'nontable',len(unchanged))
