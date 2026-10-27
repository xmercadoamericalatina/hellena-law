from pathlib import Path
import json,gzip,re,sys,hashlib
import html5lib,cmarkgfm
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');A=B/'estaduais/_indice/_recuperacao-v2-20261016';O=A/'revisao-raiz-sp-res4'
sha=lambda b:hashlib.sha256(b).hexdigest()
profile=json.loads((O/'perfil4-selecionado.json').read_text());config=json.loads((O/'config4-raiz.json').read_text());suffix='final'
def flags(root):
 out=[]
 def put(text,state):
  for c in text or '':
   if not c.isspace():out.append((c,state))
 def walk(e,state):
  if e.tag in ('script','style','head'):return
  bits=state
  for tag,bit in [('strong',1),('b',1),('em',2),('i',2),('del',4),('s',4),('strike',4),('u',8),('sup',16),('sub',32)]:
   if e.tag==tag:bits|=bit
  style={k.strip().lower():v.strip().lower() for k,v in re.findall(r'([\w-]+)\s*:\s*([^;]+)',e.get('style',''))}
  weight=style.get('font-weight');italic=style.get('font-style')
  if weight in ('bold','bolder') or weight and weight.isdigit() and int(weight)>=600:bits|=1
  elif weight in ('normal','lighter') or weight and weight.isdigit() and int(weight)<=500:bits&=~1
  if italic in ('italic','oblique'):bits|=2
  elif italic=='normal':bits&=~2
  decoration=style.get('text-decoration','')+' '+style.get('text-decoration-line','')
  if 'line-through' in decoration:bits|=4
  if 'underline' in decoration:bits|=8
  if style.get('vertical-align')=='super':bits|=16
  if style.get('vertical-align')=='sub':bits|=32
  if style.get('display')=='none' or style.get('visibility')=='hidden':raise AssertionError('conteudo oculto requer criterio proprio')
  put(e.text,bits)
  for child in e:
   walk(child,bits);put(child.tail,bits)
 walk(root,0);return out
rows=[]
for r in profile['documentos']:
 raw=gzip.decompress((B/r['cache_original']).read_bytes());assert sha(raw)==r['fonte_sha256'];src=html5lib.parse(raw.decode(r['encoding_real']),namespaceHTMLElements=False).find('body');source=flags(src)
 source_string=''.join(c for c,_ in source);start=source_string.index(re.sub(r'\s+','',r['source_text'])[:60]);source=source[start:];assert ''.join(c for c,_ in source)==re.sub(r'\s+','',r['source_text'])
 candidate=B/config[r['path']];md=candidate.read_text();body=md.split('\n---\n',1)[1].lstrip().split('\n',1)[1];render=cmarkgfm.github_flavored_markdown_to_html(body,options=cmarkgfm.Options.CMARK_OPT_UNSAFE);dest=flags(html5lib.parseFragment(render,namespaceHTMLElements=False));assert ''.join(c for c,_ in source)==''.join(c for c,_ in dest),r['path']
 mismatches=[i for i,(x,y) in enumerate(zip(source,dest)) if x[1]!=y[1]];ranges=[]
 for i in mismatches:
  if ranges and i==ranges[-1][1]:ranges[-1][1]=i+1
  else:ranges.append([i,i+1])
 missing=[i for i,(x,y) in enumerate(zip(source,dest)) if x[1]&~y[1]]
 allowed=[];unexpected=[]
 for a,b in ranges:
  value=''.join(c for c,_ in source[a:b]);only_added_bold=all(x[1]==0 and y[1]==1 for x,y in zip(source[a:b],dest[a:b]))
  if only_added_bold and re.fullmatch(r'(?:Artigo\d+[.°º]*|Parágrafoúnico|§2º)',value):allowed.append({'inicio':a,'fim':b,'texto':value,'motivo':'negrito de rotulo normativo conforme convencao do repositorio'})
  elif not any(i in missing for i in range(a,b)):unexpected.append({'inicio':a,'fim':b,'texto':value})
 assert not mismatches,(r['path'],mismatches)
 rows.append({'path':r['path'],'candidato':str(candidate.relative_to(B)),'sha256_candidato':sha(candidate.read_bytes()),'sha256_fonte':sha(raw),'chars':len(source),'chars_flags_divergentes':len(mismatches),'flags_fonte_ausentes':len(missing),'Bextra_rotulos_permitidos':allowed,'flags_adicionais_inesperados':unexpected,'sha256_flags_fonte':sha(json.dumps(source,ensure_ascii=False).encode()),'sha256_flags_candidato':sha(json.dumps(dest,ensure_ascii=False).encode()),'intervalos':[{'inicio':a,'fim':b,'texto':''.join(c for c,_ in source[a:b]),'flags_fonte':sorted(set(v for _,v in source[a:b])),'flags_candidato':sorted(set(v for _,v in dest[a:b]))} for a,b in ranges]})
result={'estado':'perfil_independente_texto_e_flags_por_caractere','total':len(rows),'com_divergencia':sum(bool(r['chars_flags_divergentes']) for r in rows),'bits':{'bold':1,'italic':2,'strike':4,'underline':8,'sup':16,'sub':32},'documentos':rows,'politica':'Preserva mascaras da fonte; admite somente B adicional em rotulos ArtigoN/Paragrafo unico, convencao preexistente. Nao afirma igualdade absoluta de flags.','limite':'CSS inline e tags semanticas; nao busca stylesheet externo nem computa defaulttipografico de headings. Nao prova sozinha integralidade contextual.'}
(O/f'perfil-flags-CSS-raiz-{suffix}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'total':len(rows),'com_divergencia':result['com_divergencia'],'chars_divergentes':sum(r['chars_flags_divergentes'] for r in rows)}))
