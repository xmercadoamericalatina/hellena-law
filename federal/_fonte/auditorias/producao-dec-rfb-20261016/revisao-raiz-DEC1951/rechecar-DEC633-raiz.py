from pathlib import Path
import json,gzip,base64,hashlib,re,unicodedata,collections,datetime,importlib.util
import html5lib,cmarkgfm
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');D=B/'federal/_fonte/auditorias/producao-dec-rfb-20261016';C=D/'coorte-DEC-2000';O=D/'revisao-raiz-DEC1951/rechecagem633';O.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
def plain(e):return re.sub(r'\s+',' ',''.join(e.itertext())).strip()
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.casefold()) if not unicodedata.combining(c))
def arr(v):return v if isinstance(v,list) else [] if v is None else [v]
src=(B/'estaduais/_indice/_recuperacao-v2-20261016/revisao-raiz-sp-res20/verificar-flags-CSS-raiz.py').read_text();exec(compile(src[src.index('def flags(root):'):src.index('rows=[]')],'<flags-raiz>','exec'))
spec=importlib.util.spec_from_file_location('auditar',B/'scripts/auditar.py');aud=importlib.util.module_from_spec(spec);spec.loader.exec_module(aud)
plist=D/'overlay-contextual-DEC2000/paths-sem-alerta-adicional.txt';assert sha(plist.read_bytes())=='553b9947ee5978f5e0ecb1111a6d22ecb16eaf55694168c489153182778ef403';paths=set(plist.read_text().splitlines());assert len(paths)==1951
paths=set(json.loads((D/'revisao-raiz-DEC1951/paths-rechecagem633.json').read_text()));assert len(paths)==633
catalogue_raw=gzip.decompress((D/'indice-DEC-master-congelado.json.gz').read_bytes());assert sha(catalogue_raw)=='ee4da737474800846c2634f64d6af6d8bc9d37f8bfca670e27f012594d2e4fef'
catalogue=json.loads(catalogue_raw)['ListaDocumento']['documentos']['documento'];assert len(catalogue)==153637;catalogue={r['norma']:r for r in catalogue if r['tipo']=='DEC-n'};assert len(catalogue)==139127
rows=[json.loads(l) for l in (C/'coorte2000.jsonl').read_text().splitlines()];assert len(rows)==2000
months={m:i+1 for i,m in enumerate('janeiro fevereiro marco abril maio junho julho agosto setembro outubro novembro dezembro'.split())}
results=[];globalcss=collections.Counter();globalcss_literals={};inline=collections.defaultdict(collections.Counter);spatial=[];article_alerts=[]
with gzip.open(C/'backup-MDs.jsonl.gz','rt') as mds,gzip.open(C/'backup-fontes.jsonl.gz','rt') as sources,(O/'documentos-raiz.jsonl').open('w') as out:
 for row,ml,sl in zip(rows,mds,sources):
  d=row['inventario'];md_record=json.loads(ml);pack=json.loads(sl);assert pack['path']==md_record['path']==d['path']
  if d['path'] not in paths:continue
  result={'path':d['path'],'erros':[]}
  try:
   md=(B/d['path']).read_bytes();assert md==md_record['MD'].encode() and sha(md)==d['sha256_MD']
   gz=base64.b64decode(pack['fonte_gzip_base64'],validate=True);mgz=base64.b64decode(pack['metadata_gzip_base64'],validate=True);assert sha(gz)==d['sha256_fonte_gzip'] and sha(mgz)==d['sha256_metadados_gzip']
   raw=gzip.decompress(gz);mr=gzip.decompress(mgz);assert sha(raw)==d['sha256_fonte'] and sha(mr)==d['meta']['sha256_metadados_fonte'];meta=json.loads(mr)
   assert (B/d['fonte_cache']).read_bytes()==gz and (B/d['metadados_cache']).read_bytes()==mgz
   fields={}
   for line in md.decode()[4:].split('\n---\n',1)[0].splitlines():
    k,v=line.split(':',1);v=v.strip()
    try:fields[k]=json.loads(v)
    except json.JSONDecodeError:fields[k]=v
   assert fields==d['meta'] and fields['urn']==meta['legislationIdentifier'] and fields['data']==meta['legislationDate']
   primary=d['primario'];assert catalogue[primary['norma']]==primary and primary['tipo']=='DEC-n';day,month,year=primary['dataassinatura'].split('/');assert f'{year}-{month}-{day}'==fields['data'] and str(primary['numero'])==fields['numero'];assert fields['urn']==f"urn:lex:br:federal:decreto:{fields['data']};{fields['numero']}"
   encs=[e for e in arr(meta.get('encoding')) if isinstance(e,dict) and e.get('contentUrl') and 'html' in (e.get('encodingFormat') or 'text/html')];current=[e for e in encs if e.get('version')=='Current'];chosen=current[0] if current else sorted(encs,key=lambda e:e.get('datePublished') or '')[-1]
   assert chosen==d['encoding_escolhido'] and chosen.get('version')=='Original' and fields['versao_texto']=='original';assert chosen['contentUrl'].startswith('https://normas.leg.br/api/binario/')
   force=arr(meta.get('legislationLegalForce'));assert force==json.loads(fields['forca_legal_fonte']) and fields['revogada'] is (False if force==['InForce'] else None)
   assert fields['tipo']=='Decreto' and fields['fonte']=='https://normas.leg.br/?urn='+fields['urn'] and fields['titulo']==primary['normaNome'].strip()
   parser=html5lib.HTMLParser(namespaceHTMLElements=False);tree=parser.parse(raw.decode('utf-8').lstrip('\ufeff'));body=tree.find('body');assert body is not None
   for style in tree.find('head').iter('style'):
    s=style.text or '';globalcss[sha(s.encode())]+=1;globalcss_literals[sha(s.encode())]=s
    assert not re.search(r'font\s*:|font-weight|font-style|text-decoration|vertical-align|display|visibility|opacity|position|content\s*:|@import|url\s*\(',s,re.I),s
   unknown=[]
   for e in tree.iter():
    if not isinstance(e.tag,str):continue
    if e.tag not in ('html','head','meta','title','style','body','div','p','span'):unknown.append(e.tag)
    for key,value in re.findall(r'([\w-]+)\s*:\s*([^;]+)',e.get('style','')):
     key=key.lower();value=value.strip().lower();inline[key][value]+=1
     assert key not in ('position','visibility','opacity','white-space','clip','content','background-image','float'),(key,value)
     if key in ('width','display','padding-left','margin-left') and e.tag=='span':
      assert ''.join(e.itertext())=='\xa0',(e.tag,e.attrib,plain(e));spatial.append({'path':d['path'],'style':e.get('style'),'literal':'1NBSP','parent_context':'epigrafe/assinatura; source SHA bound'})
    assert not any(k.lower().startswith('on') or k.lower() in ('hidden','src','href','data','srcset') for k in e.attrib),e.attrib
   assert not unknown,unknown
   ps=[e for e in body.iter('p') if plain(e)];marker=None
   if ps and re.fullmatch(r'###DEC-\d+-\d+-\d+-\d{2}-\d{2}-\d{4}@@@',plain(ps[0])):
    marker=plain(ps[0]);parts=marker[3:-3].split('-');assert int(parts[1])==int(fields['numero']) and parts[2:4]==['0','000'] and '-'.join(reversed(parts[-3:]))==fields['data'];ps[0].clear()
   assert not re.search(r'###[A-Z0-9-]*@@@',''.join(body.itertext()))
   ps=[plain(e) for e in body.iter('p') if plain(e)];ep=norm(ps[0]);n=re.search(r'^decreto\s+(?:n[ºo°.\s]*)?([\d.]+)',ep);date=re.search(r'(\d{1,2})(?:[ºo°])?\s+de\s+(\w+)\s+de\s+(\d{4})',ep);assert n and n[1].replace('.','')==fields['numero'] and date
   assert f'{date[3]}-{months[date[2]]:02}-{int(date[1]):02}'==fields['data']
   closes=[(i,p,re.fullmatch(r'brasilia,?\s+(\d{1,2})(?:[ºo°])?\s+de\s+(\w+)\s+de\s+(\d{4})[;.,]\s*(.*)',norm(p))) for i,p in enumerate(ps) if norm(p).startswith('brasilia')];closes=[x for x in closes if x[2]];assert len(closes)==1
   ci,close,cm=closes[0];assert f'{cm[3]}-{months[cm[2]]:02}-{int(cm[1]):02}'==fields['data'] and re.search('independencia.*republica',cm[4])
   tail=ps[ci+1:];assert tail and (norm(tail[0]).strip(' .')=='ernesto geisel' or (re.fullmatch(r'adalberto p\.?\s*santos',norm(tail[0]).strip(' .')) and re.search(r'vice[\s-]*presidente.*(?:exercicio|exercendo)',norm(' '.join(ps[:ci])))))
   assert all(re.fullmatch(r'[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .’\x27-]{4,120}',p) and len(p.split())>=2 for p in tail)
   articles=[(i,re.match(r'^Art(?:igo)?[.\s]*(\d+)[º°o]?',p,re.I),p) for i,p in enumerate(ps[:ci])];articles=[(i,int(m[1]),p) for i,m,p in articles if m];assert articles
   nums=[n for _,n,_ in articles]
   if nums!=list(range(1,max(nums)+1)):article_alerts.append({'path':d['path'],'numeros':nums,'artigos_literais':[p for _,_,p in articles]})
   assert not re.search(r'\b(?:anex[oa]s?|apens[oa]s?|ilegivel|omitid[oa]|suprimid[oa])\b|\(\s*\.\s*\.\s*\.\s*\)',norm(' '.join(ps)))
   src=flags(body);prefix='# '+fields['titulo']+'\n\n';rest=md.decode().split('\n---\n',1)[1].lstrip('\n');assert rest.startswith(prefix);rest=rest[len(prefix):];render=cmarkgfm.github_flavored_markdown_to_html(rest,options=cmarkgfm.Options.CMARK_OPT_UNSAFE);dst=flags(html5lib.parseFragment(render,namespaceHTMLElements=False));assert ''.join(c for c,_ in src)==''.join(c for c,_ in dst)
   chars=''.join(c for c,_ in src);allowed=set()
   for m in re.finditer(r'(?:Art(?:igo)?\.?\d+[º°o.]*|Parágrafoúnico[-–—.:]?|§\d+[º°o.]*)',chars,re.I):allowed.update(range(m.start(),m.end()))
   differences=[i for i,(x,y) in enumerate(zip(src,dst)) if x[1]!=y[1]]
   assert all(not (src[i][1]&~dst[i][1]) and (src[i][1]^dst[i][1])==1 and i in allowed for i in differences),[(i,chars[max(0,i-10):i+20],src[i],dst[i]) for i in differences[:20]]
   er,wa=aud.validar(md.decode(),d['path'],datetime.date(2026,10,16));assert not er and not wa,(er,wa)
   result.update({'sha256_MD':sha(md),'sha256_fonte':sha(raw),'sha256_metadata':sha(mr),'fonte_encoding_URL':chosen['contentUrl'],'versao':'original_por_API','revogada':fields['revogada'],'IdSenado':primary['id'],'numero':fields['numero'],'data':fields['data'],'URN':fields['urn'],'marker_tecnico_removido':marker,'epigrafe':ps[0],'fecho':close,'assinaturas':tail,'artigos':nums,'Bextra_rotulos':len(differences),'caracteres':len(src),'SHA_GFM':sha(render.encode()),'SHA_flags_fonte':sha(json.dumps(src,ensure_ascii=False).encode()),'SHA_flags_MD':sha(json.dumps(dst,ensure_ascii=False).encode())})
  except Exception as e:result['erros'].append(__import__('traceback').format_exc())
  out.write(json.dumps(result,ensure_ascii=False)+'\n');out.flush();results.append(result)
  if len(results)%200==0:print(json.dumps({'lidos':len(results),'falhas':sum(bool(r['erros']) for r in results)}),flush=True)
 assert len(results)==633 and not mds.readline() and not sources.readline()
summary={'estado':'revisao_raiz_independente_nao_aprovacao','documentos':len(results),'com_erros':sum(bool(r['erros']) for r in results),'falhas':[r for r in results if r['erros']],'CSS_head':[{'sha256':h,'qtd':n,'literal':globalcss_literals[h]} for h,n in globalcss.items()],'CSS_inline':{k:dict(v) for k,v in inline.items()},'spans_espaciais':spatial,'sequencias_artigos_requerem_contexto':article_alerts,'limites':['Sem revisao humana integral1951 ou facsimiles; valida snapshot oficial HTML+JSON e sequencia literal GFM.','CSS text-transform/posicao/size nao sao alegados identicos em pixels.','Marcador administrativo so retirado de P inicial inteiro, vinculado a numero/data propria.','Dedup HEAD atual e GitHub ainda pendentes.']}
(O/'resumo-raiz.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'documentos':len(results),'falhas':summary['com_erros'],'sequencias_artigos_alerta':len(article_alerts),'CSS_head_variantes':len(globalcss),'spans_espaciais':len(spatial)}),flush=True)
