from pathlib import Path
from html.parser import HTMLParser
import gzip,json,hashlib,re,subprocess,zipfile,xml.etree.ElementTree as ET,collections
import cmarkgfm
B=Path('estaduais/_indice/_recuperacao-v2-20261016'); sha=lambda b:hashlib.sha256(b).hexdigest()
class Text(HTMLParser):
 def __init__(self,source=False):
  super().__init__(convert_charrefs=True);self.source=source;self.body=not source;self.skip=[];self.text=[];self.assets=[];self.tags=collections.Counter();self.links=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='body':self.body=True
  if not self.body:return
  self.tags[t]+=1
  if t in ('script','style','head'):self.skip.append(t)
  if t=='a':self.links.append(d)
  if t in ('img','svg','object','iframe','embed'):self.assets.append({'tag':t,'attrs':d,'antecedente':''.join(self.text)[-200:]})
 def handle_endtag(self,t):
  if self.skip and t==self.skip[-1]:self.skip.pop()
  if t=='body':self.body=False
 def handle_data(self,d):
  if self.body and not self.skip:self.text.append(d)
def chars(s):return re.sub(r'\s+','',s)
snap=json.loads(Path('estaduais/_snapshot_coletas_20261016_visual_v2.json').read_text());xs=[r for r in snap['publicaveis'] if '/SP/resolucoes/' in r['path']];ids={re.search(r'id(\d+)\.md$',r['path']).group(1) for r in xs};index={}
zpath=Path('estaduais/SP/_indice/legislacao_normas.zip')
with zipfile.ZipFile(zpath) as z,z.open(z.namelist()[0]) as f:
 for _,e in ET.iterparse(f):
  if e.tag=='LegislacaoNorma':
   r={c.tag:c.text for c in e}
   if r.get('IdNorma') in ids:index[r['IdNorma']]=r
   e.clear()
rows=[];review=[]
for r in xs:
 p=Path(r['path']);md=p.read_text();header,body=md.split('\n---\n',1);normbody=body.split('\n',1)[1];rawgz=Path(r['cache_original']).read_bytes();raw=gzip.decompress(rawgz)
 try:html=raw.decode('utf-8');encoding='utf-8'
 except UnicodeDecodeError:html=raw.decode('cp1252');encoding='cp1252'
 src=Text(True);src.feed(html);text=''.join(src.text)
 for nav in ('Assembleia Legislativa do Estado de São Paulo','Ficha informativa'):
  if text.lstrip().startswith(nav):text=text.lstrip()[len(nav):]
 rendered=cmarkgfm.github_flavored_markdown_to_html(normbody)
 dst=Text();dst.feed(rendered);out=''.join(dst.text);source_full=text;gfm_full=out;sm=re.search(r'RESOLU[ÇC][ÃA]O',text);gm=re.search(r'RESOLU[ÇC][ÃA]O',out);assert sm and gm;text=text[sm.start():];out=out[gm.start():];ident=re.search(r'id(\d+)\.md$',str(p)).group(1);idx=index[ident]
 meta={m.group(1):m.group(2) for m in re.finditer(r'^([a-z_]+): (.*)$',header,re.M)}
 articles=re.findall(r'Artigo\s+(\d+)',text,re.I);closing=re.search(r'Assembl[eéÉ]ia Legislativa do Estado de S[ãÃ]o Paulo,.*',text,re.S)
 mismatch=None
 if chars(text)!=chars(out):
  a,b=chars(text),chars(out);n=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)));mismatch={'pos':n,'fonte':a[max(0,n-60):n+120],'gfm':b[max(0,n-60):n+120]}
 row={**r,'md_sha256_atual':sha(md.encode()),'fonte_sha256':sha(raw),'cache_gzip_sha256':sha(rawgz),'encoding_real':encoding,'indice_registro':idx,'metadata':meta,'fonte_corpo_chars_sha256':sha(chars(text).encode()),'gfm_corpo_chars_sha256':sha(chars(out).encode()),'caracteres_fonte_gfm_iguais':mismatch is None,'divergencia':mismatch,'tags_body':dict(src.tags),'assets_body':src.assets,'links_body':src.links,'artigos_detectados':articles,'fecho_fonte':closing.group(0) if closing else None,'source_text':text,'gfm_text':out,'source_text_integral':source_full,'gfm_text_integral':gfm_full,'gfm_tags':dict(dst.tags),'revisao_contextual_pendente':True}
 rows.append(row);review.append('\nPATH '+str(p)+'\n'+text+'\nASSETS '+json.dumps(src.assets,ensure_ascii=False)+'\nGFM '+str(mismatch))
outp=B/'sp-res52-perfil.json';assert not outp.exists();outp.write_text(json.dumps({'script_sha256':sha(Path(__file__).read_bytes()),'indice_zip_sha256':sha(zpath.read_bytes()),'documentos':rows,'limites':['Perfil técnico, não aprova por igualdade de caracteres.','Situação desconhecida deve continuar null; API JSON não está em cache.','A versão original declarada pelo coletor não prova atualização jurídica presente.']},ensure_ascii=False,indent=2)+'\n');(B/'sp-res52-leitura-fonte.txt').write_text('\n'.join(review));print(outp,sha(outp.read_bytes()),collections.Counter(str(r['caracteres_fonte_gfm_iguais']) for r in rows),flush=True)
