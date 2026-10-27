# -*- coding: utf-8 -*-
from pathlib import Path
import sys,json,re,gzip,hashlib,base64,urllib.parse,collections,concurrent.futures,signal
sys.path[:0]=['/tmp/constituicao-markdown-qa-20261020','scripts','scripts/estados']
from markdown_it import MarkdownIt
from comum import decodificar
from rj import corpo_normativo,FORMS
from pe_fidelidade_visivel import texto_visivel_html,assinatura_numerica,_heading_comprovado
from auditar_pe_cache import APP,FOREIGN,MONTH
from integridade_texto import verificar_integridade_texto
from avisos_fonte import avisos_de_omissao
from anexos_fonte import remissoes_sem_representacao
from visuais_fonte import imagens_html
from tabelas_estrutura import conferir_tabelas_complexas
R=Path.cwd();sha=lambda b:hashlib.sha256(b).hexdigest();parser=MarkdownIt('commonmark',{'html':True}).enable('table');catalog={}
for p in (R/'estaduais/RJ/_indice/paginas-wrapper').glob('*/*.json'):
 try:
  for x in json.loads(p.read_text()).get('itens',[]):catalog[x['href'].split('/')[-1].split('?')[0]]=x
 except Exception:pass
EP=re.compile(r'\b(LEI(?:\s+COMPLEMENTAR)?|EMENDA(?:\s+CONSTITUCIONAL)?)\s+N[º°o.\s]*\s*([\d.]+)\s*,?\s*DE\s+(\d{1,2})[º°o]?\s+DE\s+(\w+)\s+DE\s+(\d{4})',re.I)
def timeout(*args):raise TimeoutError('20 segundos de auditoria por norma')
def one(p):
 signal.signal(signal.SIGALRM,timeout);signal.alarm(20);ret=[];ev={};result=dict(path=p)
 try:
  raw=(R/p).read_bytes();result['sha256_md']=sha(raw);text=raw.decode();meta={}
  for line in text.split('\n---\n',1)[0].splitlines():
   k,sep,v=line.partition(':')
   if sep:
    try:meta[k]=json.loads(v.strip())
    except:meta[k]=v.strip()
  sourceurl=meta.get('fonte_original','');uid=re.search(r'/([0-9a-f]{32})(?:\?|$)',sourceurl,re.I);assert uid,'sem UID Lotus Notes oficial completo';uid=uid[1].lower();it=catalog.get(uid);result.update(id_oficial=uid,metadata=meta,indice=it)
  if not it:ret.append('UID ausente do índice oficial em cache')
  else:
   if re.sub(r'\D','',it['numero'])!=re.sub(r'\D','',str(meta['numero'])) or it['ano']!=str(meta['data'])[:4] or FORMS[it['form']][2]!=meta['tipo']:ret.append('identidade número/ano/tipo no índice e MD diverge')
  cache=R/'estaduais/RJ/_fonte'/Path(p).relative_to('estaduais/RJ').with_suffix('.html.gz');z=cache.read_bytes();rawsrc=gzip.decompress(z);s=decodificar(rawsrc,'text/html; charset=utf-8');a=re.search(r'<a\s+name\s*=\s*["\']TOPO["\']',s,re.I);assert a,'sem delimitador inicial TOPO';part=s[a.start():];b=re.search(r'<a\s+name=["\']_Section2["\']|<a[^>]+id="A2"',part,re.I);assert b,'sem limite final comprovado';field=part[:b.start()];after=texto_visivel_html(part[b.start():b.start()+1300]);assert re.search('Ficha T[eé]cnica',after,re.I),'limite final não identificado como ficha técnica';result.update(cache=str(cache.relative_to(R)),sha256_cache=sha(z),sha256_fonte=sha(rawsrc),sha256_campo=sha(field.encode()),limite_campo=[a.start(),a.start()+b.start()],prova_fim_ficha_tecnica=after[:250])
  converted=corpo_normativo(s);body=text.split('\n---\n',1)[1].split('\n',1)[1];body=re.sub(r'^# [^\n]*\n','',body,count=1).strip();source=texto_visivel_html(field);pl=' '.join(source.split());ep=EP.search(pl[:2500]);ev['inicio_fonte']=pl[:1200]
  if not ep:ret.append('epígrafe própria número/tipo/data não comprovada')
  else:
   date=f'{ep[5]}-{MONTH.get(ep[4].lower(),0):02d}-{int(ep[3]):02d}';result['epigrafe_literal']=ep[0]
   expected={'Lei Ordinária':'LEI','Lei Complementar':'LEI COMPLEMENTAR','Emenda Constitucional':'EMENDA CONSTITUCIONAL'}.get(meta['tipo']);got=' '.join(ep[1].upper().split())
   if re.sub(r'\D','',ep[2])!=re.sub(r'\D','',str(meta['numero'])) or date!=str(meta['data']) or got!=expected:ret.append('epígrafe própria diverge do metadado número/data/tipo')
  issue,proof=verificar_integridade_texto(converted);result['dispositivo_proprio']=proof
  if issue:ret.append(issue)
  imgs=imagens_html(field);unknown=[]
  for image in imgs:
   # O recibo registra todas as imagens. Só caminhos/dimensões Notes já comprovados como interface são dispensados.
   src=str(image.get('src',''));alt=str(image.get('alt',''))
   if not (src.endswith('/icons/ecblank.gif') and str(image.get('height',''))=='1' or src.endswith('/icons/collapse.gif') and alt=='Hide details for Texto da Lei   [ Em Vigor ]'):unknown.append(image)
  ev['imagens']=imgs
  if unknown:ret.append('imagem no campo sem representação normativa ou identidade de interface comprovada');ev['imagens_nao_comprovadas']=unknown
  if re.search(r'<(?:strike|s|del)\b|line-through',field,re.I):ret.append('tachado no campo requer separar redação histórica/compilada')
  if re.search(r'(?:class|style)\s*=\s*["\'][^"\']*(?:tachad|revogad|riscad|desativad|deleted|deletion)|display\s*:\s*none|visibility\s*:\s*hidden',field,re.I):ret.append('marcação CSS contextual potencialmente histórica/oculta exige revisão')
  avis=avisos_de_omissao(converted)
  if avis:ret.append('aviso explícito de material omitido');ev['avisos']=avis
  ann=remissoes_sem_representacao(converted)
  if ann:ret.append('remissão própria a anexo sem representação comprovada');ev['anexos']=ann
  app=APP.search(pl)
  if app and not re.search(r'(?im)^\s*[#*\s]*(?:ANEXO|REGULAMENTO|REGIMENTO|ESTATUTO|PLANO|MANUAL)\b|<table\b|^\s*\|',converted):ret.append('objeto aprovado sem representação própria comprovada');ev['objeto']=app[0]
  foreign=[m[0] for m in FOREIGN.finditer(converted.replace('*','')) if re.sub(r'\D','',m[2])!=re.sub(r'\D','',str(meta['numero']))]
  if foreign:ret.append('outra epígrafe completa exige granularidade contextual');ev['outras_epigrafes']=foreign
  tables=conferir_tabelas_complexas(field,body);result['tabelas_complexas_conferidas']=len(tables)
  rendered=parser.render(body);visible=texto_visivel_html(rendered);visible,headings=_heading_comprovado(visible,body,source);result.update(sha256_html_renderizado=sha(rendered.encode()),sha256_visivel_fonte=sha(source.encode()),sha256_visivel_md=sha(visible.encode()),normalizacoes_heading=headings,igualdade_visivel=source==visible,assinatura_numerica_confere=assinatura_numerica(source)==assinatura_numerica(visible))
  if source!=visible:
   ret.append('texto visível CommonMark diverge da fonte');i=next((i for i,(x,y) in enumerate(zip(source,visible)) if x!=y),min(len(source),len(visible)));ev['divergencia_visivel']={'fonte':source[max(0,i-100):i+200],'md':visible[max(0,i-100):i+200]}
  if not result['assinatura_numerica_confere']:ret.append('assinatura numérica/sinais/moeda/percentuais diverge')
 except Exception as e:ret.append(type(e).__name__+': '+str(e))
 signal.alarm(0);result.update(publicavel=not ret,problemas=ret,evidencias=ev);return result
if __name__=='__main__':
 paths=[p for p in Path('/tmp/rj-canonicos-cache-auditoria-20261020-001.txt').read_text().splitlines() if '/constituicao/' not in p]
 with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool,Path('/tmp/rj-cache-auditoria-20261020-001.jsonl').open('x') as out:
  for r in pool.map(one,paths,chunksize=10):out.write(json.dumps(r,ensure_ascii=False)+'\n');out.flush()
 print('FINAL',len(paths))
