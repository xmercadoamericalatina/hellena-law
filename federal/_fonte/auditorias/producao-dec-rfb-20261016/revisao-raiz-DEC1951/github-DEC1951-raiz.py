from pathlib import Path
import json,gzip,base64,hashlib,urllib.request,re,datetime
import html5lib,cmarkgfm
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');D=B/'federal/_fonte/auditorias/producao-dec-rfb-20261016';C=D/'coorte-DEC-2000';O=D/'revisao-raiz-DEC1951/GitHub';O.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
paths=set((D/'overlay-contextual-DEC2000/paths-sem-alerta-adicional.txt').read_text().splitlines());rows={r['inventario']['path']:r['inventario'] for r in map(json.loads,(C/'coorte2000.jsonl').read_text().splitlines())}
def struct(s):
 e=html5lib.parseFragment(s,namespaceHTMLElements=False);norm=lambda e:re.sub(r'\s+',' ',''.join(e.itertext())).strip()
 return {'texto':norm(e),'bold':[norm(x) for x in e.iter('strong')],'italic':[norm(x) for x in e.iter('em')],'del':[norm(x) for x in e.iter('del')],'u':[norm(x) for x in e.iter('u')],'sup':[norm(x) for x in e.iter('sup')],'sub':[norm(x) for x in e.iter('sub')],'titulos':[(x.tag,norm(x)) for x in e.iter() if x.tag in ('h1','h2','h3')],'listas':[(x.tag,x.get('start','1'),x.get('value'),norm(x)) for x in e.iter() if x.tag in ('ol','ul','li')],'tabelas':len(list(e.iter('table')))}
source=(B/'estaduais/_indice/_recuperacao-v2-20261016/revisao-raiz-sp-res20/verificar-flags-CSS-raiz.py').read_text();exec(compile(source[source.index('def flags(root):'):source.index('rows=[]')],'<flags-raiz>','exec'))
docs=[]
for line in gzip.open(C/'backup-MDs.jsonl.gz','rt'):
 r=json.loads(line)
 if r['path'] not in paths:continue
 md=r['MD'].encode();assert sha(md)==rows[r['path']]['sha256_MD'];body=r['MD'].split('\n---\n',1)[1].lstrip('\n');docs.append({'path':r['path'],'body':body,'sha256_MD':sha(md)})
assert len(docs)==1951
chunks=[];chunk=[]
def payload(items):return json.dumps({'text':'\n\n'.join(r['body'] for r in items),'mode':'gfm','context':'ctresb/leis'},ensure_ascii=False).encode()
for r in docs:
 if chunk and len(payload(chunk+[r]))>380000:chunks.append(chunk);chunk=[]
 chunk.append(r)
if chunk:chunks.append(chunk)
print(json.dumps({'documentos':len(docs),'lotes':len(chunks)}),flush=True);results=[]
for n,chunk in enumerate(chunks,1):
 data=payload(chunk);assert len(data)<400000;checkpoint=O/f'lote-{n:03}.json'
 if checkpoint.exists():
  prev=json.loads(checkpoint.read_text());assert prev['sha256_payload']==sha(data) and prev['paths']==[r['path'] for r in chunk]
  for key,name in (('sha256_HTML_GitHub',f'lote-{n:03}-GitHub.html.gz'),('sha256_HTML_GFM',f'lote-{n:03}-GFM.html.gz')):assert sha(gzip.decompress((O/name).read_bytes()))==prev[key]
  results.append(prev);continue
 text='\n\n'.join(r['body'] for r in chunk);local=cmarkgfm.github_flavored_markdown_to_html(text,options=cmarkgfm.Options.CMARK_OPT_UNSAFE)
 independent=[]
 for r in chunk:
  html=cmarkgfm.github_flavored_markdown_to_html(r['body'],options=cmarkgfm.Options.CMARK_OPT_UNSAFE);independent+=flags(html5lib.parseFragment(html,namespaceHTMLElements=False))
 assert flags(html5lib.parseFragment(local,namespaceHTMLElements=False))==independent,'efeito entre documentos'
 request=urllib.request.Request('https://api.github.com/markdown',data=data,headers={'User-Agent':'leis-revisao-raiz','Content-Type':'application/json'},method='POST')
 with urllib.request.urlopen(request,timeout=120) as response:remote=response.read().decode();remaining=response.headers.get('X-RateLimit-Remaining')
 assert struct(local)==struct(remote),n
 (O/f'lote-{n:03}-GitHub.html.gz').write_bytes(gzip.compress(remote.encode()));(O/f'lote-{n:03}-GFM.html.gz').write_bytes(gzip.compress(local.encode()))
 result={'lote':n,'documentos':len(chunk),'paths':[r['path'] for r in chunk],'MD_SHA256':{r['path']:r['sha256_MD'] for r in chunk},'sha256_payload':sha(data),'payload_bytes':len(data),'sha256_HTML_GitHub':sha(remote.encode()),'sha256_HTML_GFM':sha(local.encode()),'estrutura_GFM_GitHub_igual':True,'sem_efeitos_entre_documentos':True,'rate_limit_remaining':remaining,'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()};checkpoint.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');results.append(result);print(json.dumps({'lote':n,'documentos':len(chunk),'bytes':len(data),'restantes_API':remaining}),flush=True)
assert sum(r['documentos'] for r in results)==1951
summary={'estado':'render_1951_conferido_sem_publicacao','documentos':1951,'lotes':results,'criterios':'Texto,B/I/del/U/sup/sub,titulos,listas-contadores,tabelas iguais no GFM local e API GitHub. Conjunto local igual a concatenacao das renderizacoes individuais, sem cruzamento de escopo.','limite':'Nao compara pixels/stylesheet da fonte; provas da fonte/metadados/dedup separadas.'}
(O/'resumo-GitHub1951-raiz.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print('GITHUB1951_COMPLETO',flush=True)
