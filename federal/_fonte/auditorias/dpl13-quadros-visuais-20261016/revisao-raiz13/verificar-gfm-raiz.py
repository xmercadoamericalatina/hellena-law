import pathlib,json,hashlib,re,datetime,importlib.util,urllib.request
import cmarkgfm,html5lib
B=pathlib.Path('/Volumes/ExternalSSD/GitHub/constituicao');A=B/'federal/_fonte/auditorias/dpl13-quadros-visuais-20261016';O=A/'revisao-raiz13'
spec=importlib.util.spec_from_file_location('auditar',B/'scripts/auditar.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
m=json.loads((A/'manifesto-final13-v2.json').read_text())
replacements={'5018':'5018-candidato-v5.md','5585':'5585-candidato-v2.md','5597':'5597-candidato-v2.md','5745':'5745-candidato-v4.md'}
acts=[];bodies=[]
def dom(s):return html5lib.parseFragment(s,namespaceHTMLElements=False)
def txt(e):return re.sub(r'\s+',' ',''.join(e.itertext())).strip()
def structure(root):
 return {'texto':txt(root),'tabelas':[[[(c.tag,c.get('rowspan','1'),c.get('colspan','1'),txt(c)) for c in row if c.tag in ('td','th')] for row in table.iter('tr')] for table in root.iter('table')], 'italicos':[txt(e) for e in root.iter('em')],'fortes':[txt(e) for e in root.iter('strong')], 'listas':[(e.tag,e.get('start','1'),txt(e)) for e in root.iter() if e.tag in ('ol','ul','li')], 'titulos':[(e.tag,txt(e)) for e in root.iter() if e.tag in ('h1','h2','h3')]}
for r in m['candidatos']:
 n=r['numero'];p=O/replacements[n] if n in replacements else B/r['path'];s=p.read_text();meta,body=s[4:].split('\n---\n',1)
 fields={}
 for line in meta.splitlines():
  k,v=line.split(':',1);v=v.strip()
  try:fields[k]=json.loads(v)
  except json.JSONDecodeError:fields[k]=v
 errors,warnings=mod.validar(s,f'federal/decretos-legislativos/{fields["data"][:4]}/dpl-{n}-{fields["data"]}.md',datetime.date(2026,10,16));assert not errors and not warnings,(n,errors,warnings)
 assert fields['numero']==n and fields['tipo']=='Decreto do Poder Legislativo' and fields['revogada'] is None
 assert fields['data'] in fields['urn'] and fields['urn'].endswith(';'+n)
 assert fields['versao_texto']=='coletanea_oficial_transcricao_cotejada'
 assert not re.search(r'<(?:u|ins|script|style)\b',body,re.I),n
 rendered=cmarkgfm.github_flavored_markdown_to_html(body,options=cmarkgfm.Options.CMARK_OPT_UNSAFE)
 (O/f'{n}-GFM-raiz.html').write_text(rendered)
 tree=structure(dom(rendered));acts.append({'numero':n,'candidato':str(p.relative_to(B)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'formato_erros':errors,'formato_avisos':warnings,'tabelas':[len(t)-1 for t in tree['tabelas']],'estrutura':tree});bodies.append(body)
body='\n\n'.join(bodies);local=cmarkgfm.github_flavored_markdown_to_html(body,options=cmarkgfm.Options.CMARK_OPT_UNSAFE)
payload=json.dumps({'text':body,'mode':'gfm','context':'ctresb/leis'}).encode();req=urllib.request.Request('https://api.github.com/markdown',data=payload,headers={'User-Agent':'leis-auditoria-raiz','Content-Type':'application/json','Accept':'application/vnd.github+json'},method='POST')
with urllib.request.urlopen(req,timeout=120) as resp: remote=resp.read().decode()
(O/'GitHub-render13.html').write_text(remote)
L=structure(dom(local));R=structure(dom(remote));assert L==R,[(k,L[k],R[k]) for k in L if L[k]!=R[k]]
result={'estado':'formato_e_render_preservados_nao_aprovacao_editorial','quantidade':len(acts),'atos':acts,'github_payload_sha256':hashlib.sha256(payload).hexdigest(),'github_HTML_sha256':hashlib.sha256(remote.encode()).hexdigest(),'github_vs_local_iguais':['texto','tabelas_celulas_spans','italicos','fortes','listas','titulos'],'limite':'Render comparado nao substitui leitura visual fonte nem prova identidade primaria; oracle324 anterior incompleto para5745.'}
(O/'verificacao-GFM-GitHub13-raiz.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'formatos':len(acts),'tabelas':sum(len(a['tabelas']) for a in acts),'GitHub':'texto/celulas/spans/formatos iguais','linhas_por_ato':{a['numero']:a['tabelas'] for a in acts}}))
