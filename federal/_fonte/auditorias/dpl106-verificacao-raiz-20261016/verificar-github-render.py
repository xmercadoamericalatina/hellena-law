from pathlib import Path
import json,urllib.request,hashlib,time
ns={};exec(Path('/tmp/verificar-dpl106-raiz.py').read_text().split('primary={}')[0],ns);model=ns['model'];normalized_dom=ns['normalized_dom'];Text=ns['Text'];B=Path('federal/_fonte/auditorias/dpl106-verificacao-raiz-20261016');j=json.loads((B/'verificacao.json').read_text());chunks=[];part=[];size=0
for r in j['documentos']:
 body=Path(r['candidato']).read_text().split('---',2)[2].lstrip().split('\n\n',1)[1];assert len(body.encode())<200000
 if part and size+len(body.encode())>200000:chunks.append(part);part=[];size=0
 part.append((r,body));size+=len(body.encode())+2
if part:chunks.append(part)
report=[]
for n,chunk in enumerate(chunks,1):
 s='\n\n'.join(body for r,body in chunk);payload={'text':s,'mode':'gfm','context':'ctresb/leis'};req=urllib.request.Request('https://api.github.com/markdown',data=json.dumps(payload).encode(),headers={'User-Agent':'leis-auditoria','Content-Type':'application/json'},method='POST');response=urllib.request.urlopen(req,timeout=40);out=response.read().decode();before=model.table_signature(model.DOM(normalized_dom(s)));after=model.table_signature(model.DOM(normalized_dom(out)));a=Text(s).out if False else None
 # GFM esperado local é comparado ao render oficial, mantendo contadores reais de listas.
 from cmarkgfm import github_flavored_markdown_to_html as render
 from cmarkgfm.cmark import Options
 expected=render(s,options=Options.CMARK_OPT_UNSAFE);ea=Text(expected).out;eb=Text(out).out;chars=''.join(c for c,f in ea)==''.join(c for c,f in eb);formats=chars and all(all(not v or w for v,w in zip(x[1],y[1])) for x,y in zip(ea,eb))
 p=B/('github-lote-'+str(n)+'.html');p.write_text(out);report.append({'lote':n,'documentos':[r['path'] for r,body in chunk],'input_sha256':hashlib.sha256(s.encode()).hexdigest(),'input_bytes':len(s.encode()),'http':response.status,'output':str(p),'output_sha256':hashlib.sha256(out.encode()).hexdigest(),'tabelas':len(before),'celulas':sum(len(t['cells']) for t in before),'assinatura_rica_tabelas_igual':before==after,'texto_com_contadores_igual':chars,'formatacao_sem_perda':formats,'tabelas_antes':before if before!=after else None,'tabelas_depois':after if before!=after else None});print('GITHUB106',n,len(chunk),len(before),'tableequal',before==after,'chars',chars,'styles',formats,flush=True);time.sleep(.35)
(B/'verificacao-github-render.json').write_text(json.dumps({'endpoint':'https://api.github.com/markdown','context':'ctresb/leis','modo':'gfm','lotes':report,'limite':'ComparaHTMLsanitizadooficial, não CSS/viewport/interação emnavegador.'},ensure_ascii=False,indent=2)+'\n');print('FINAL',len(report),sum(len(r['documentos']) for r in report),sum(r['tabelas'] for r in report),flush=True)
