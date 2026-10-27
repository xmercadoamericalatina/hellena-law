"""Revisão offline independente de propostas, sem aplicação canônica."""
from pathlib import Path
import sys,json,gzip,re,hashlib,html,argparse,datetime
from html.parser import HTMLParser
from cmarkgfm import github_flavored_markdown_to_html as render
from cmarkgfm.cmark import Options
ROOT=Path.cwd();B=ROOT/"federal/_fonte/auditorias/dpl-auditoria-20261016";OLD=ROOT/"federal/_fonte/auditorias/dpl-tabelas114-20261016";OUT=ROOT/"federal/_fonte/auditorias/dpl-tabelas114-revisao-final-20261016"
sys.path.insert(0,str(ROOT/"scripts"));import baixar_camara as cam, auditar
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,b,a):
 if a or p.exists():assert p.read_bytes()==b,str(p)
 else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
class Chars(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.stack=[];self.chars=[];self.tags=[];self.plain=[];self.ol=[];self.feed(s);self.close()
 def handle_starttag(self,t,a):
  self.tags.append(t)
  if t=='ol':self.ol.append(int(dict(a).get('start','1')))
  if t=='li' and self.ol:
   self.handle_data(str(self.ol[-1])+'.');self.ol[-1]+=1
  if t not in ('br','hr','img','meta','link','input','col','wbr'):self.stack.append((t,dict(a)))
 def handle_endtag(self,t):
  if t=='ol' and self.ol:self.ol.pop()
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==t:self.stack=self.stack[:i];break
 def handle_data(self,d):
  if any(t in ('head','script','style','title') for t,_ in self.stack):return
  f=(any(t in ('s','strike','del') or 'line-through' in a.get('style','') for t,a in self.stack),any(t=='sup' for t,_ in self.stack),any(t=='sub' for t,_ in self.stack),any(t in ('b','strong') or re.search(r'font-weight\s*:\s*(?:bold|[7-9]00)',a.get('style','')) for t,a in self.stack),any(t in ('i','em') or re.search(r'font-style\s*:\s*italic',a.get('style','')) for t,a in self.stack))
  self.plain.append(d);self.chars.extend((c,f) for c in d if not c.isspace() and c!='\ufeff')
def run(audit=False):
 assert sha((ROOT/"scripts/html2md.py").read_bytes())=='bb85371750359042e0636ae0adc206cb0c353c6b6586c8d46e60a5257633ed3c'
 rs={r['path']:r for r in map(json.loads,(B/'inventario5409-revisado.jsonl').read_text().splitlines())};ls=list(map(json.loads,(OLD/'ledger114.jsonl').read_text().splitlines()));assert len(ls)==114
 rows=[]
 for l in ls:
  r=rs[l['path']];old=(ROOT/r['path']).read_bytes();assert sha(old)==r['sha256_md'];candidate=(ROOT/l['candidato']).read_bytes();assert sha(candidate)==l['sha256_candidato']
  gz=(ROOT/r['fonte_cache']['snapshot']).read_bytes();assert sha(gz)==r['fonte_cache']['sha256_arquivo'];raw=gzip.decompress(gz);assert sha(raw)==r['fonte_cache']['sha256_fonte'];frag=cam.corpo_norma(raw.decode());source=Chars(frag)
  body=candidate.decode().split('---',2)[2].lstrip().split('\n\n',1)[1];target=Chars(render(body,options=Options.CMARK_OPT_UNSAFE));holds=[]
  diffs=[]
  for i,(a,b) in enumerate(zip(source.chars,target.chars)):
   if a!=b:
    if len(diffs)<8:diffs.append({'offset':i,'fonte':source.chars[max(0,i-15):i+30],'GFM':target.chars[max(0,i-15):i+30]})
  samechars=''.join(c for c,f in source.chars)==''.join(c for c,f in target.chars);sameformat=source.chars==target.chars
  lost=[];added=[];chunk=''
  if samechars:
   for (ch,fs),(ch2,ft) in zip(source.chars,target.chars):
    if any(fs[i] and not ft[i] for i in range(5)) or any(fs[i]!=ft[i] for i in (0,1,2,4)):lost.append(ch)
    if not fs[3] and ft[3]:chunk+=ch
    elif chunk:added.append(chunk);chunk=''
   if chunk:added.append(chunk)
  permitted=re.compile(r'(?:Art\.\d+[ºo°.]*|§\d+[ºo°.]*|Par[aá]gra(?:ph|f)o[uú]nico[.:]?|\d+[ºo°])',re.I)
  editorial=all(permitted.fullmatch(x) for x in added)
  semloss=samechars and not lost and editorial
  if not semloss:holds.append('DOM/GFM perda textual ou formatação não explicada')
  if not l['estrutura_celulas_span_texto_identicos']:holds.append('uma das quatro tabelas complexas preservadas')
  plain=' '.join(' '.join(source.plain).split());markers=[{'literal':m[0],'contexto':plain[max(0,m.start()-100):m.end()+180]} for m in re.finditer(r'\bileg[ií]vel\b|\bsuprimid\w*|\bomitid\w*|\bomiss[aã]o\b|\bsupress[aã]o\b|n[aã]o.{0,30}(?:digitad|reproduzid|transcrit)|impossibilidade.t[eé]cnica|\[\s*(?:\.\s*){3,}\]|(?:\.\s*){3,}|…',plain,re.I)]
  # Nenhum marcador contextual é autoaprovado.
  for marker in markers:
   if re.fullmatch(r'[.\s]+',marker['literal']):marker['decisao']='pontilhado de alinhamento tabular/valor; literal integral preservado, sem preenchimento'
   else:marker['decisao']='retido para revisão contextual'
  if any(x['decisao'].startswith('retido') for x in markers):holds.append('marcadores contextuais requerem decisão individual')
  if l['anexo_externo_ausente']:holds.append('anexo externo ausente')
  if set(source.tags)&{'img','svg','object','embed','iframe','math','canvas'}:holds.append('visual não textual')
  m=r['metadados'];proof=r['metadados_cache'];packed=(ROOT/proof['snapshot']).read_bytes();assert sha(packed)==proof['sha256_arquivo'];meta=gzip.decompress(packed);assert sha(meta)==proof['sha256_fonte_html'];metaplain=cam.texto(meta.decode());status=m['situacao'];assert status in metaplain
  if status=='Não consta revogação expressa':replacement=b'revogada: null';vig=None
  elif status=='Revogada':replacement=b'revogada: true';vig=True
  elif status.lower() in ('vigente','em vigor'):replacement=b'revogada: false';vig=False
  else:replacement=b'revogada: null';vig=None;assert not status,'situação não reconhecida'
  boundary=candidate.index(b'\n---\n',4);header=candidate[:boundary];match=re.search(rb'(?m)^revogada: (?:false|true|null)$',header);assert match
  normalized=candidate[:match.start()]+replacement+candidate[match.end():];assert normalized.split(b'---',2)[2]==candidate.split(b'---',2)[2]
  assert candidate[:match.start()]+replacement+candidate[match.end():]==normalized
  targetpath=OUT/'candidatos'/r['path'];write(targetpath,normalized,audit)
  errors,warnings=auditar.validar(normalized.decode(),r['path'],datetime.date(2026,10,16));assert not errors,(r['path'],errors)
  # Reexecuta identidade/data pelo texto integral desmarcado, mantendo fecho próprio.
  dateerror=None
  try:cam.conferir_data_propria({'numero':m['numero'],'data':m['data'],'urn':m['urn']},cam.texto(frag),m['titulo'],'dpl')
  except Exception as e:dateerror=str(e);holds.append('identidade/data: '+dateerror)
  assert all(r['gates_metadados'].values());assert r['gates']['primario'];assert r['gates']['formula_legislativa']
  # Confere vínculo próprio e versão literal na página de metadados congelada.
  ownlink=m['fonte'] in html.unescape(meta.decode()) or m['fonte'].split('/')[-1] in html.unescape(meta.decode());assert ownlink
  version=(m['versao_texto']=='original' and ('-publicacaooriginal-' in m['fonte'] or '-textopublicacaooriginal-' in m['fonte'])) or (m['versao_texto']=='compilado' and '-normaatualizada-' in m['fonte']);assert version,(m['versao_texto'],m['fonte'])
  rows.append({'path':r['path'],'candidato':str(targetpath.relative_to(ROOT)),'sha256_canonico':sha(old),'sha256_candidato':sha(normalized),'sha256_corpo_candidato':sha(normalized.split(b'---',2)[2]),'fonte':r['fonte_cache'],'metadados':proof,'status_literal':status,'revogada_candidata':vig,'outros_headers_identicos_ao_ensaio':normalized[:match.start()]==candidate[:match.start()] and normalized[match.start()+len(replacement):]==candidate[match.end():],'corpo_identico_ao_ensaio':True,'DOM_GFM_texto_pontuacao_identicos':samechars,'DOM_GFM_formatacao_identica':sameformat,'sem_perda_formatacao':semloss,'enfases_editoriais_core':added,'perda_formatacao_caracteres':len(lost),'primeiras_divergencias':diffs,'tabelas_celulas_spans_identicos':l['estrutura_celulas_span_texto_identicos'],'marcadores_contextuais':markers,'primario_e_identidade_metadata_link_versao_formula':True,'identidade_data_fecho_erro':dateerror,'formato_erros':errors,'formato_avisos':warnings,'retencoes':holds,'estado':'condicional_revisao_raiz' if not holds else 'retido','backup_integral':l['backup'],'aplicado':False})
 data=''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows).encode();write(OUT/'revisao114.jsonl',data,audit)
 summary={'total':114,'condicionais':sum(not x['retencoes'] for x in rows),'retidos':sum(bool(x['retencoes']) for x in rows),'DOM_GFM_texto_pontuacao_identicos':sum(x['DOM_GFM_texto_pontuacao_identicos'] for x in rows),'DOM_GFM_formatacao_identica':sum(x['DOM_GFM_formatacao_identica'] for x in rows),'marcadores_contextuais':sum(bool(x['marcadores_contextuais']) for x in rows),'ledger_sha256':sha(data),'HTTP':0,'canonicos_alterados':0};write(OUT/'resumo.json',(json.dumps(summary,ensure_ascii=False,indent=2)+'\n').encode(),audit);print(json.dumps(summary))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--auditar',action='store_true');run(ap.parse_args().auditar)
