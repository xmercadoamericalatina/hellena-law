import json,gzip,hashlib,re,sys,datetime,collections,concurrent.futures,difflib,unicodedata
from pathlib import Path
from html.parser import HTMLParser
from cmarkgfm import github_flavored_markdown_to_html as render
from cmarkgfm.cmark import Options
sys.path.insert(0,str(Path('scripts').resolve()));import html2md
base=Path('estaduais/MG/_indice/_auditoria-mg16811-20261016');rows=[json.loads(x) for x in (base/'perfil-documentos.jsonl').read_text().splitlines()];sha=lambda b:hashlib.sha256(b).hexdigest();assert sha(Path('scripts/html2md.py').read_bytes())=='bb85371750359042e0636ae0adc206cb0c353c6b6586c8d46e60a5257633ed3c';oldgate={r['path']:r for r in json.load(open('estaduais/_fonte/auditorias/integralidade-snapshot-20261016.json'))['documentos'] if r['uf']=='MG'};months={m:n for n,m in enumerate('janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro'.split(),1)}
class Texto(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.stack=[];self.runs=[];self.parts=[]
 def handle_starttag(self,t,attrs):
  if t in ('p','div','tr','br','li'):self.parts.append('\n')
  if t in ('img','br','hr','meta','link','col','input'):return
  a=dict(attrs);self.stack.append((t,t in ('s','strike','del') or bool(re.search('line-through',a.get('style',''),re.I))))
 def handle_endtag(self,t):
  if t in ('p','div','tr','li'):self.parts.append('\n')
  for k in range(len(self.stack)-1,-1,-1):
   if self.stack[k][0]==t:self.stack=self.stack[:k];break
 def handle_data(self,text):
  if any(t in ('head','script','style','title') for t,_ in self.stack):return
  self.parts.append(text);strike=any(b for _,b in self.stack);self.runs.extend((c,strike) for c in text if not c.isspace() and c!='\ufeff')
omission=re.compile(r'(?:anex[oa]s?|tabelas?|quadros?|mapas?|plantas?|volumes?).{0,100}?(?:n[aã]o.{0,16}(?:digitad|transcrit|reproduzid|dispon[ií]v)|dispon[ií]ve[li]s? (?:no|em)|publicad.{0,40}(?:[aà] parte|separad))|impossibilidade t[eé]cnica|imagem d[oa] anex[oa]',re.I|re.S)
fecho=re.compile(r'(?:Pal[aá]cio|Sala d[ae]|Secretaria|Diretoria|Belo Horizonte)[^\n]{0,180}?(\d{1,2})\s+de\s+('+'|'.join(months)+r')\s+de\s+(\d{4})',re.I)
def audit(r):
 raw=gzip.decompress(Path(r['cache']).read_bytes());src=raw.decode();a=Texto()
 if r['formato']=='outrotextoUTF8':
  a.parts=[src];a.runs=[(c,False) for c in src if not c.isspace() and c!='\ufeff']
 else:a.feed(src)
 candidate=html2md.convert(src);b=Texto();b.feed(render(candidate,options=Options.CMARK_OPT_UNSAFE));plain=''.join(a.parts);holds=[];om=[]
 for match in omission.finditer(plain):om.append(dict(pos=match.start(),trecho=plain[max(0,match.start()-120):match.end()+180]))
 if om:holds.append('conteudo_proprio_omitido_ou_externo_explicito_exige_contexto')
 if re.search(r'aos\s*\.',plain,re.I) and re.search(r'_{5,}',plain):holds.append('template_sem_dispositivo_data_assinaturas')
 text_equal=a.runs==b.runs;diff=[]
 if not text_equal:
  holds.append('divergencia_caracteres_ou_tachado_GFM')
  aa=''.join(x[0] for x in a.runs);bb=''.join(x[0] for x in b.runs)
  first=next((j for j,(x,y) in enumerate(zip(a.runs,b.runs)) if x!=y),min(len(a.runs),len(b.runs)))
  diff.append(dict(primeira_posicao=first,fonte=aa[max(0,first-60):first+180],candidato=bb[max(0,first-60):first+180]))
 fechos=[]
 for m in fecho.finditer(plain):
  try:date=datetime.date(int(m[3]),months[m[2].lower()],int(m[1])).isoformat()
  except ValueError:continue
  fechos.append(dict(data=date,trecho=m[0]))
 if fechos and all(x['data']!=r['data'] for x in fechos):holds.append('data_csv_diverge_de_fecho_proprio_exige_contexto')
 old=oldgate[r['path']];root_noart=any('sem_artigo' in x for x in old['alertas']);device=bool(re.search(r'(?:D\s*E\s*C\s*R\s*E\s*T\s*A|DELIBERA|RESOLVE|determinam|fica(?:m)? aprovad[ao]s?|comunica que|dispensa|designa|nomeia)',plain,re.I));ownart=bool(re.search(r'Art(?:igo|\.)\s*(?:\d|[úu]nico)',plain,re.I));classify='articulado_inline_ou_artigo_unico' if ownart else 'nao_articulado_com_dispositivo' if device else 'sem_dispositivo_reconhecido_exige_contexto'
 if not ownart and not device:holds.append('dispositivo_nao_reconhecido_exige_contexto')
 if not fechos:holds.append('fecho_data_literal_nao_reconhecido_exige_contexto')
 if not all(r[k] for k in ['snapshot_md_sha_confere','numero_csv_confere','data_csv_confere','xml_identidade_conteudo_confere','baseline95_corpo_exato']):holds.append('proveniencia_baseline_divergente')
 result=dict(path=r['path'],md_sha256=r['md_sha256'],source_sha256=r['source_sha256'],source_gzip_sha256=r['source_gzip_sha256'],xml=r['xml'],data=r['data'],CSV=r['indice_csv'],texto_tachado_GFM_identico=text_equal,source_runs_sha256=sha(json.dumps(a.runs,ensure_ascii=False).encode()),candidato_runs_sha256=sha(json.dumps(b.runs,ensure_ascii=False).encode()),source_caracteres=len(a.runs),oracle_fonte='raw_literal_decodificado' if r['formato']=='outrotextoUTF8' else 'HTMLParserindependente',candidate_body_sha256=sha(candidate.encode()),candidate_igual_baseline=r['novo_igual_baseline'],tabelas_HTML=r['tabelas'],imagens=r['graficos'],sem_artigo_gate_original=root_noart,classificacao_dispositivo=classify,fechos=fechos,omissoes=om,gate_remissao_original=any('remissao' in x for x in old['alertas']),retencoes=holds,diferencas_render=diff)
 return result
out=base/'gates-contexto-documentos.jsonl';records=[json.loads(x) for x in out.read_text().splitlines()];counts=collections.Counter()
for r in records:
 counts.update(r['retencoes']);counts['GFM_identico:'+str(r['texto_tachado_GFM_identico'])]+=1;counts['dispositivo:'+r['classificacao_dispositivo']]+=1
completed=len(records);assert [r['path'] for r in records]==[r['path'] for r in rows[:completed]];print('RETOMAR',completed,flush=True)
with out.open('a') as log,concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for n,r in enumerate(pool.map(audit,rows[completed:]),completed+1):
  records.append(r);log.write(json.dumps(r,ensure_ascii=False)+'\n');counts.update(r['retencoes']);counts['GFM_identico:'+str(r['texto_tachado_GFM_identico'])]+=1;counts['dispositivo:'+r['classificacao_dispositivo']]+=1
  if n%1000==0:log.flush();print('GATESMG',n,dict(counts),flush=True)
(base/'gates-contexto-resumo.json').write_text(json.dumps(dict(total=len(records),contagem=dict(counts),sem_retencoes=sum(not r['retencoes'] for r in records),com_retencoes=sum(bool(r['retencoes']) for r in records),perfil_sha256=sha(out.read_bytes()),limites=['Gates conservadores; retenções de remissão/data/fecho exigem contexto. Igualdade de caracteres não prova sozinha integralidade.','Candidato semmudança em16811; nenhuma aplicação ouHTTP.']),ensure_ascii=False,indent=2));print('FINALGATES',dict(counts))
