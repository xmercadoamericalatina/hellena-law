from pathlib import Path
import sys,json,hashlib,re,importlib.util,datetime,urllib.request
import html5lib,cmarkgfm
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');O=B/'estaduais/_indice/_recuperacao-v2-20261016/revisao-raiz-sp-res5';config=json.loads(Path(sys.argv[1]).read_text());assert len(config)==5
spec=importlib.util.spec_from_file_location('auditar',B/'scripts/auditar.py');aud=importlib.util.module_from_spec(spec);spec.loader.exec_module(aud)
dom=lambda s:html5lib.parseFragment(s,namespaceHTMLElements=False)
norm=lambda e:re.sub(r'\s+',' ',''.join(e.itertext())).strip()
def struct(e):return {'texto':norm(e),'bold':[norm(x) for x in e.iter('strong')],'italic':[norm(x) for x in e.iter('em')],'del':[norm(x) for x in e.iter('del')],'u':[norm(x) for x in e.iter('u')],'sup':[norm(x) for x in e.iter('sup')],'sub':[norm(x) for x in e.iter('sub')],'titulos':[(x.tag,norm(x)) for x in e.iter() if x.tag in ('h1','h2','h3')],'listas':[(x.tag,x.get('start','1'),norm(x)) for x in e.iter() if x.tag in ('ol','ul','li')],'tabelas':len(list(e.iter('table')))}
bodies=[];rows=[]
for target,candidate in sorted(config.items()):
 p=B/candidate;s=p.read_text();errors,warnings=aud.validar(s,target,datetime.date(2026,10,16));assert not errors and not warnings,(target,errors,warnings);body=s.split('\n---\n',1)[1];bodies.append(body);rows.append({'path':target,'candidato':candidate,'sha256_candidato':hashlib.sha256(p.read_bytes()).hexdigest(),'formato_erros':errors,'formato_avisos':warnings})
combined='\n\n'.join(bodies);local=cmarkgfm.github_flavored_markdown_to_html(combined,options=cmarkgfm.Options.CMARK_OPT_UNSAFE);payload=json.dumps({'text':combined,'mode':'gfm','context':'ctresb/leis'}).encode();assert len(payload)<400000
req=urllib.request.Request('https://api.github.com/markdown',data=payload,headers={'User-Agent':'leis-revisao-raiz','Content-Type':'application/json'},method='POST')
with urllib.request.urlopen(req,timeout=120) as r:remote=r.read().decode()
(O/'GFM5-raiz.html').write_text(local);(O/'GitHub5-raiz.html').write_text(remote);assert struct(dom(local))==struct(dom(remote))
result={'estado':'formato_e_render_conferidos_sem_aplicacao','quantidade':5,'atos':rows,'GitHub_vs_GFM':'texto/bold/italic/del/u/sup/sub/titulos/listas/tabelas iguais','payload_bytes':len(payload),'SHA_HTML_GitHub':hashlib.sha256(remote.encode()).hexdigest(),'limite':'Nao certifica CSS externo/pixels da fonte; mascara fonte inline verificada em prova separada; leitura integral contextual e identidade primaria separadas'}
(O/'verificacao-GFM-GitHub5-raiz.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'formatos':len(rows),'GitHub':'texto e marcas iguais','payload_bytes':len(payload)}))
