import json,gzip,hashlib,re,csv,sys,datetime,importlib.util,collections,concurrent.futures,xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
sys.path.insert(0,str(Path('scripts').resolve()))
def load(p,n):
 spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
old=load('/tmp/html2md-antes-tachado.py','old');new=load('scripts/html2md.py','new');assert hashlib.sha256(Path('scripts/html2md.py').read_bytes()).hexdigest()=='bb85371750359042e0636ae0adc206cb0c353c6b6586c8d46e60a5257633ed3c';assert hashlib.sha256(Path('/tmp/html2md-antes-tachado.py').read_bytes()).hexdigest()=='95aadd3b5daa2422b01ae194cdf9a1a87998165fb12e6a789fd1db558c69789e'
base=Path('estaduais/MG/_indice/_auditoria-mg16811-20261016');sha=lambda b:hashlib.sha256(b).hexdigest();rows=[r for r in json.load(open('estaduais/_snapshot_coletas_20261016_visual_v2.json'))['publicaveis'] if r['uf']=='MG'];index={};csvshas={}
for p in sorted(Path('estaduais/MG/_indice').glob('*.csv')):
 csvshas[str(p)]=sha(p.read_bytes())
 for r in csv.DictReader(p.open()):
  slug=r['Tipo'].lower()+'-'+r['Numero']+('-'+r['Complemento'] if r['Complemento'] else '')+'-'+r['Ano'];index[slug]=(r,str(p))
class Fonte(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.stack=[];self.parts=[];self.strike=0;self.img=[];self.tables=0;self.spans=[];self.links=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t in ('img','svg','object','embed','iframe','canvas','math') or t.startswith('v:'):self.img.append(dict(tag=t,attrs=a,pos=len(''.join(self.parts))))
  if t=='table':self.tables+=1
  if t in ('td','th') and any(k in a for k in ('rowspan','colspan')):self.spans.append({k:v for k,v in a.items() if k in ('rowspan','colspan')})
  if t=='a' and a.get('href'):self.links.append(a['href'])
  if t in ('p','div','tr','h1','h2','h3','br','li'):self.parts.append('\n')
  if t not in ('img','br','hr','meta','link','col','input'):self.stack.append((t,t in ('s','del','strike') or bool(re.search('line-through',a.get('style',''),re.I))))
 def handle_endtag(self,t):
  if t in ('p','div','tr','h1','h2','h3','li'):self.parts.append('\n')
  for k in range(len(self.stack)-1,-1,-1):
   if self.stack[k][0]==t:self.stack=self.stack[:k];break
 def handle_data(self,s):
  if any(t in ('script','style','head','title') for t,_ in self.stack):return
  self.parts.append(s)
  if any(b for _,b in self.stack):self.strike+=sum(not c.isspace() for c in s)
def audit(row):
 result=dict(path=row['path'],cache=row['cache_original'],fonte=row['fonte']);errors=[]
 try:
  md=Path(row['path']).read_bytes();gz=Path(row['cache_original']).read_bytes();raw=gzip.decompress(gz);source=raw.decode('utf8');front,body=md.decode().split('\n---\n',1);meta={}
  for line in front.splitlines()[1:]:
   k,v=line.split(':',1)
   try:meta[k]=json.loads(v.strip())
   except ValueError:meta[k]=v.strip()
  parser=Fonte();parser.feed(source);plain=''.join(parser.parts);lines=[x.strip() for x in plain.splitlines() if x.strip()];baseline=body.splitlines()[0]+'\n\n'+old.convert(source);entry=index.get(Path(row['path']).stem);xmlpath=Path('estaduais/MG/_indice/documentos')/(Path(row['path']).stem+'.xml.gz');xmlproof=None
  if xmlpath.exists():
   xmlraw=gzip.decompress(xmlpath.read_bytes());xml=ET.fromstring(xmlraw);docs=[]
   for node in xml.findall('.//normaDocumento'):
    if node.findtext('conteudo')==source:docs.append({k:node.findtext(k) for k in ['siglaTipoNorma','numero','ano','codTipoDocumento','dataAtualizacao']})
   xmlproof=dict(path=str(xmlpath),sha256=sha(xmlraw),matching_conteudo=docs)
  ix=entry[0] if entry else {};expectednum=ix.get('Numero','')+('-'+ix['Complemento'] if ix.get('Complemento') else '');date=''
  if ix.get('DataLegislacao'):
   try:date=datetime.datetime.strptime(ix['DataLegislacao'],'%d/%m/%Y').date().isoformat()
   except ValueError:pass
  ownxml=bool(xmlproof and any(d['siglaTipoNorma']==ix.get('Tipo') and d['numero']==ix.get('Numero') and d['ano']==ix.get('Ano') for d in xmlproof['matching_conteudo']))
  try:candidate=new.convert(source);candidate_error=None
  except Exception as e:candidate='';candidate_error=type(e).__name__+': '+str(e)
  annex=[dict(linha=j,texto=line[:1000]) for j,line in enumerate(lines) if re.search(r'anex|volume|croqui|mapa|planta',line,re.I)];external=[x for x in annex if re.search(r'(?:constam?|publicad[oa]s?|arquivad[oa]s?|dispon[ií]ve[li]s?|vide|ver).*?(?:di[aá]rio|original|publicaç|arquivo|[íi]ntegra)|(?:anexos?|volumes?).{0,80}(?:parte integrante|integra[mn]?(?:te)?|deste|desta|I\b|II\b)',x['texto'],re.I)]
  result.update(md_sha256=sha(md),snapshot_md_sha_confere=sha(md)==row['sha256_arquivo'],body_sha256=sha(body.encode()),header_sha256=sha(front.encode()),source_sha256=sha(raw),source_gzip_sha256=sha(gz),magic32_hex=raw[:32].hex(),formato='HTMLfragmentoUTF8' if re.search(r'<(?:p|span|div|table|html|body)\b',source,re.I) else 'outrotextoUTF8',numero=meta.get('numero'),data=meta.get('data'),tipo=meta.get('tipo'),versao=meta.get('versao_texto'),indice_csv=entry[1] if entry else None,indice_registro=ix,numero_csv_confere=expectednum==str(meta.get('numero')),data_csv=date,data_csv_confere=date==meta.get('data'),xml_identidade_conteudo_confere=ownxml,xml=xmlproof,baseline95_corpo_exato=baseline==body,baseline95_body_sha256=sha(baseline.encode()),tachado_caracteres=parser.strike,tabelas=parser.tables,spans=parser.spans,graficos=parser.img,links=parser.links,artigo_presente_fonte=bool(re.search(r'\bArt(?:igo|\.)\s*\d',plain,re.I)),artigo_presente_md=bool(re.search(r'\bArt(?:igo|\.)[*.\s]*\d',body,re.I)),inicio=lines[:4],fim=lines[-7:],remissoes=annex,remissoes_proprias_ou_externas_alerta=external,novo_convert_erro=candidate_error,novo_corpo_convert_sha256=sha(candidate.encode()) if not candidate_error else None,novo_igual_baseline=candidate==old.convert(source),NUL_source='\x00' in source,NUL_md='\x00' in body)
 except Exception as e:errors.append(type(e).__name__+': '+str(e))
 result['erros']=errors;return result
records=[];counts=collections.Counter();out=base/'perfil-documentos.jsonl'
with out.open('w') as log,concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for n,r in enumerate(pool.map(audit,rows),1):
  log.write(json.dumps(r,ensure_ascii=False)+'\n');records.append(r)
  for flag in ['snapshot_md_sha_confere','numero_csv_confere','data_csv_confere','xml_identidade_conteudo_confere','baseline95_corpo_exato','novo_igual_baseline']:counts[flag+':'+str(r.get(flag))]+=1
  for flag in ['tachado_caracteres','tabelas','graficos','remissoes','remissoes_proprias_ou_externas_alerta','novo_convert_erro','erros']:
   if r.get(flag):counts[flag]+=1
  if not r.get('artigo_presente_md'):counts['sem_artigo_md']+=1
  if n%500==0:log.flush();print('MG',n,'/',len(rows),dict(counts),flush=True)
summary=dict(total=len(records),contagem=dict(counts),formatos=dict(collections.Counter(x.get('formato','erro') for x in records)),tipos=dict(collections.Counter(x.get('tipo','erro') for x in records)),csv_sha256=csvshas,perfil_sha256=sha(out.read_bytes()),conversor95_sha256=sha(Path('/tmp/html2md-antes-tachado.py').read_bytes()),conversor_candidato_sha256=sha(Path('scripts/html2md.py').read_bytes()),limites=['Inventário/gates automáticos; não é certificação de integralidade. Ausência deartigo não rejeita ato. Remissões exigem contexto individual.','Nenhum MD/código do acervo alterado; semHTTP/Git.'])
(base/'perfil-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print('FINAL',summary['contagem'])
