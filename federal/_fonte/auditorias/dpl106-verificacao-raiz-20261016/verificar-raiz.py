from pathlib import Path
import sys,json,gzip,re,hashlib,subprocess,datetime,html,importlib.util
from html.parser import HTMLParser
import html5lib
from cmarkgfm import github_flavored_markdown_to_html as render
from cmarkgfm.cmark import Options
sys.path.insert(0,str(Path('scripts').resolve()));import baixar_camara as cam
B=Path('federal/_fonte/auditorias/dpl-tabelas114-revisao-final-20261016');A=Path('federal/_fonte/auditorias/dpl-auditoria-20261016');sha=lambda b:hashlib.sha256(b).hexdigest()
m=Path('federal/_preparacao_dpl_tabelas109_condicional_20261016.json');assert sha(m.read_bytes())=='258fa544d3604db9ff35513f260f177963698cc21d35bbe974d1e8fa85100671'
for f in json.loads(m.read_text())['arquivos']:assert sha(Path(f['path']).read_bytes())==f['sha256']
overlay=json.loads(Path('federal/_overlay_dpl_tabelas109_sublinhado_20261016.json').read_text());excluded={r['path'] for r in overlay['retidos_adicionais']};rows=[r for r in map(json.loads,(B/'revisao114.jsonl').open()) if not r['retencoes'] and r['path'] not in excluded];assert len(rows)==106
spec=importlib.util.spec_from_file_location('independent_tables','estaduais/SC/_indice/_revisao-independente-tabelas-20261016/reproduzir_comparacao.py');model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
class Text(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.stack=[];self.out=[];self.ol=[];self.feed(s);self.close()
 def handle_starttag(self,t,a):
  attrs=dict(a)
  if t=='ol':
   assert attrs.get('type','1')=='1';self.ol.append(int(attrs.get('start','1')))
  if t=='li' and self.ol:
   if 'value' in attrs:self.ol[-1]=int(attrs['value'])
   self.handle_data(str(self.ol[-1])+'.');self.ol[-1]+=1
  if t not in ('br','hr','img','col','link','meta','wbr','input'):self.stack.append((t,dict(a)))
 def handle_endtag(self,t):
  if t=='ol' and self.ol:self.ol.pop()
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==t:self.stack=self.stack[:i];break
 def handle_data(self,d):
  if any(t in ('head','script','style','title') for t,a in self.stack):return
  style=';'.join(re.sub(r'\s+','',a.get('style','').lower()) for t,a in self.stack)
  flags=(any(t in ('del','s','strike') for t,a in self.stack) or 'line-through' in style,any(t=='sup' for t,a in self.stack),any(t=='sub' for t,a in self.stack),any(t in ('b','strong') for t,a in self.stack) or bool(re.search(r'font-weight:(?:bold|[7-9]00)',style)),any(t in ('i','em') for t,a in self.stack) or 'font-style:italic' in style)
  self.out.extend((c,flags) for c in d if not c.isspace() and c!='\ufeff')
def normalized_dom(s):return html5lib.serialize(html5lib.parseFragment(s,namespaceHTMLElements=False),quote_attr_values='always',omit_optional_tags=False)
def meta(raw):
 d={}
 for line in raw.decode().split('---',2)[1].strip().splitlines():
  k,v=line.split(':',1);v=v.strip()
  try:d[k]=json.loads(v)
  except ValueError:d[k]=v
 return d
primary={}
for r in json.loads((A/'primario5831.json').read_text()):
 date=datetime.datetime.strptime(r['dataassinatura'],'%d/%m/%Y').date().isoformat();num=str(r['numero']).replace('.','').lower()+('-'+r['complemento'].lower() if r.get('complemento') else '');primary['urn:lex:br:federal:decreto.legislativo:'+date+';'+num]=r
queries={r['urn']:r for r in json.loads(Path('federal/_indice/camara-dpl-pendencias/indice.json').read_text())['consultas']};head=subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'],text=True).strip();checks=subprocess.check_output(['rtk','proxy','git','cat-file','--batch-check=%(objectname) %(objecttype) %(objectsize)'],input=''.join(head+':'+r['path']+'\n' for r in rows),text=True).splitlines();assert all(l.endswith(' missing') for l in checks)
report=[]
for r in rows:
 old=Path(r['path']).read_bytes();new=Path(r['candidato']).read_bytes();assert sha(old)==r['sha256_canonico'] and sha(new)==r['sha256_candidato'];assert gzip.decompress(Path(r['backup_integral']).read_bytes())==old
 om=meta(old);nm=meta(new);assert {k:v for k,v in om.items() if k!='revogada'}=={k:v for k,v in nm.items() if k!='revogada'};assert nm['revogada'] is r['revogada_candidata'];assert nm['urn'] in primary
 doc=next(d for d in queries[nm['urn']]['documentos'] if d['url']==nm['url_metadados']);info=cam.identificar(doc,'dpl');assert info['urn']==nm['urn'] and info['data']==nm['data'] and info['numero']==nm['numero'] and doc['titulo']==nm['titulo'] and doc['situacao']==nm['situacao']
 f=r['fonte'];gz=Path(f['snapshot']).read_bytes();assert sha(gz)==f['sha256_arquivo'];raw=gzip.decompress(gz);assert sha(raw)==f['sha256_fonte'];frag=cam.corpo_norma(raw.decode());assert not re.search(r'<(?:u|ins|img|svg|object|embed|iframe|math|canvas)(?:\s|>)|text-decoration[^;"\'>]*underline',frag,re.I)
 body=new.decode().split('---',2)[2].lstrip().split('\n\n',1)[1];assert body==cam.convert(frag),(r['path'],'perfil_core');rendered=render(body,options=Options.CMARK_OPT_UNSAFE);a=Text(frag).out;b=Text(rendered).out;
 if ''.join(c for c,f in a)!=''.join(c for c,f in b):
  x=''.join(c for c,f in a);y=''.join(c for c,f in b);i=next((i for i,(c,d) in enumerate(zip(x,y)) if c!=d),min(len(x),len(y)));print('FIRSTDIFF',r['path'],repr(x[max(0,i-60):i+150]),repr(y[max(0,i-60):i+150]));raise AssertionError('textoGFM')
 assert all(all(not s or t for s,t in zip(x[1],y[1])) for x,y in zip(a,b)),(r['path'],'lostformat')
 sa=model.table_signature(model.DOM(normalized_dom(frag)));sb=model.table_signature(model.DOM(normalized_dom(rendered)));assert sa==sb,(r['path'],'rich_table_signature');assert not any(t['overlap'] for t in sa)
 mf=r['metadados'];mgz=Path(mf['snapshot']).read_bytes();assert sha(mgz)==mf['sha256_arquivo'];mr=gzip.decompress(mgz);assert sha(mr)==mf['sha256_fonte_html'];s=mr.decode();links=[cam.urllib.parse.urljoin(mf['url'],html.unescape(u)) for u in re.findall(r'href=["\']([^"\']+)["\']',s)];assert nm['fonte'] in links and '-'+cam.id_camara(doc)+'-' in nm['fonte'];status=nm['situacao'];plain=cam.texto(s)
 if status:assert status in plain
 expected=True if status=='Revogada' else False if status.lower() in ('vigente','em vigor') else None;assert nm['revogada'] is expected
 assert nm['versao_texto']==('compilada' if '-normaatualizada-' in nm['fonte'] else 'original')
 cam.conferir_data_propria({'numero':nm['numero'],'data':nm['data'],'urn':nm['urn']},cam.texto(frag),nm['titulo'],'dpl');assert cam.tipo_legislativo_comprovado(cam.texto(frag))
 report.append({'path':r['path'],'candidato':r['candidato'],'sha256_antes':sha(old),'sha256_depois':sha(new),'fonte_sha256':sha(raw),'metadata_sha256':sha(mr),'revogada':expected,'situacao':status,'tabelas':len(sa),'celulas':sum(len(t['cells']) for t in sa),'tabelas_rich_DOM_HTML5_GFM_iguais':True,'caracteres_formatos_proveniencia_iguais':True})
out=Path('federal/_fonte/auditorias/dpl106-verificacao-raiz-20261016');out.mkdir(exist_ok=True);p=out/'verificacao.json';p.write_text(json.dumps({'estado':'confronto106concluido_nao_aplicado','HEAD':head,'documentos':report,'limites':['Sem validação visual GitHub de todos os106; árvoresGFM/HTML5 e caracteres/máscaras conferidos.','Sublinhados/ilegíveis/anexos externos da coorte114 seguem retidos emdossiês próprios.','Situação vazia permanece desconhecida; nãoafirma vigência.']},ensure_ascii=False,indent=2)+'\n');print('FINAL106',len(report),'tabelas',sum(r['tabelas'] for r in report),'celulas',sum(r['celulas'] for r in report),'SHA',sha(p.read_bytes()),flush=True)
