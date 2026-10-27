import ast,datetime,difflib,gzip,hashlib,html,json,re,sys,urllib.parse
from pathlib import Path
import html5lib
from cmarkgfm import github_flavored_markdown_to_html as render
from cmarkgfm.cmark import Options
sys.path.insert(0,'scripts')
import baixar_camara as c
import auditar
B=Path('federal/_fonte/auditorias/dpl-recuperacao-restante-20261016');D=B/'candidatos3-preambulo';D.mkdir(exist_ok=True)
AUDIT='--auditar' in sys.argv
def sha(raw):return hashlib.sha256(raw).hexdigest()
def put(p,raw):
 if isinstance(raw,dict) or isinstance(raw,list):raw=json.dumps(raw,ensure_ascii=False,indent=2)+'\n'
 if isinstance(raw,str):raw=raw.encode()
 if AUDIT:assert p.read_bytes()==raw,str(p)
 else:p.write_bytes(raw)
def plain(text):return re.sub(r'\s+','',html.unescape(text))
out=[]
for r in json.loads((B/'triagem467-ranking.json').read_text()):
 if r['prioridade']!=1:continue
 n=r['urn'].split(';')[-1];date=r['urn'].split(':')[-1].split(';')[0];P=D/n;P.mkdir(exist_ok=True)
 source=r['fontes'][0];raw=gzip.decompress(Path(source['path']).read_bytes()).decode();assert sha(raw.encode())==source['sha256_HTML'];frag=c.corpo_norma(raw);body=c.convert(frag);assert sha(frag.encode())==source['sha256_fragmento']
 mp=Path(r['metadados_cache']['snapshot']);meta=gzip.decompress(mp.read_bytes()).decode();urlmeta=r['metadados_cache']['url'];links=[urllib.parse.urljoin(urlmeta,html.unescape(u)) for u in re.findall(r'href=["\']([^"\']+)["\']',meta)]
 assert source['URL'] in links,(n,'link proprio ausente');assert 'Não consta revogação expressa' in html.unescape(meta),n
 info={'urn':r['urn'],'numero':n,'data':date};c.conferir_data_propria(info,body,r['titulo'],'dpl');assert not c.tipo_legislativo_comprovado(body),n
 start=re.search(r'(?im)^O Presidente da Republica',body);assert start,n;own=body[start.start():];assert c.tipo_legislativo_comprovado(own),n
 assert not re.search(r'<(?:table|img|svg|object|embed)\b',frag,re.I),n
 assert not re.search(r'ileg[ií]vel|\(\s*omiss|\[\s*\.\.\.',body,re.I),n
 dom=html5lib.parseFragment(frag,namespaceHTMLElements=False);rendered=render(body,options=Options.CMARK_OPT_UNSAFE);gfm=html5lib.parseFragment(rendered,namespaceHTMLElements=False)
 before=''.join(dom.itertext());after=''.join(gfm.itertext());assert plain(before)==plain(after),(n,list(difflib.ndiff([before],[after])))
 critical={}
 for tags in [('u',),('del','s','strike'),('sup',),('sub',),('i','em')]:
  def segments(tree):return [plain(''.join(el.itertext())) for el in tree.iter() if el.tag in tags]
  a,z=segments(dom),segments(gfm);assert a==z,(n,tags,a,z);critical['/'.join(tags)]={'fonte':a,'GFM':z}
 assert not re.search(r'text-decoration[^;\"\']*underline',frag,re.I),n
 ementa=body[:start.start()].strip();header={'titulo':r['titulo'],'tipo':'Decreto do Poder Legislativo','numero':n,'data':date,'ementa':ementa,'situacao':'Não consta revogação expressa','revogada':None,'versao_texto':'original','fonte':source['URL'],'url_metadados':urlmeta,'baixado_em':'2026-10-16','urn':r['urn']}
 text='---\n'+''.join(k+': '+('null' if v is None else (v if k in ('data','baixado_em') else json.dumps(v,ensure_ascii=False)))+'\n' for k,v in header.items())+'---\n\n# '+r['titulo']+'\n\n'+body.rstrip()+'\n'
 path=P/('dpl-'+n+'-'+date+'.md');errs,warns=auditar.validar(text,str(path),datetime.date(2026,10,16));assert not errs and not warns,(n,errs,warns);put(path,text)
 put(P/'fonte.html',raw);put(P/'fragmento-proprio.html',frag);put(P/'metadados.html',meta);put(P/'render-corpo-GFM.html',rendered)
 proof={'norma':r['norma'],'urn':r['urn'],'candidato':str(path),'sha256_MD':sha(text.encode()),'sha256_corpo':sha(text.encode().split(b'---',2)[2]),'fonte':source,'sha256_metadados':sha(meta.encode()),'link_proprio_literal':source['URL'],'ementa_literal':ementa,'preambulo_literal':own[:own.index('\n\nArt') if '\n\nArt' in own else 400],'fecho_literal':body[-750:],'gate_formula_documento_inteiro':False,'gate_mesma_funcao_preambulo_proprio':True,'causa':'Referência a artigo na ementa antecede preâmbulo e aciona divisão prematura do gate; texto e função não alterados. Exceção contextual individual aguarda raiz.','wholetext_DOM_GFM_identico':True,'formatos_criticos':critical,'formato':{'erros':errs,'avisos':warns},'vigencia':'Literal próprio Não consta revogação expressa → null; sem inferir vigente.','publicado':False,'aprovacao_independente':False}
 put(P/'prova.json',proof);out.append(proof)
put(D/'manifesto-candidatos3.json',{'estado':'isolados_aguarda_revisao_contextual_independente','candidatos':out,'sem_HTTP':True,'canonicos_alterados':0,'nao_altera_gate_generico':True})
print([(r['norma'],r['sha256_MD']) for r in out])
