import pathlib,json,gzip,hashlib,re,subprocess,datetime,importlib.util,urllib.request
import cmarkgfm,html5lib
B=pathlib.Path('/Volumes/ExternalSSD/GitHub/constituicao');A=B/'federal/_fonte/auditorias/dpl-recuperacao-restante-20261016';O=A/'revisao-raiz7';O.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
months=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']
spec=importlib.util.spec_from_file_location('auditar',B/'scripts/auditar.py');aud=importlib.util.module_from_spec(spec);spec.loader.exec_module(aud)
norm=lambda s:re.sub(r'\s+','',s)
dom=lambda s:html5lib.parseFragment(s,namespaceHTMLElements=False)
def text(e):return ''.join(e.itertext())
def structure(e):return {'texto':norm(text(e)),'em':[norm(text(x)) for x in e.iter('em')],'strong':[norm(text(x)) for x in e.iter('strong')],'tabelas':len(list(e.iter('table'))),'listas':[(x.tag,x.get('start','1'),norm(text(x))) for x in e.iter() if x.tag in ('ol','ul','li')]}
rows=[];bodies=[];manifests=[]
for folder,mname in [('candidatos3-preambulo','manifesto-congelado3.json'),('candidatos4-sem-artigos','manifesto-congelado4.json')]:
 mp=A/folder/mname;m=json.loads(mp.read_text());manifests.append({'path':str(mp.relative_to(B)),'sha256':sha(mp.read_bytes())})
 for f in m['arquivos']:assert sha((B/f['path']).read_bytes())==f['sha256'],f['path']
 for r in m['candidatos']:
  n=r['norma'].split('-')[1];p=B/r['candidato'];assert sha(p.read_bytes())==r['sha256_MD'];s=p.read_text();meta,body=s[4:].split('\n---\n',1);fields={}
  for l in meta.splitlines():
   k,v=l.split(':',1);v=v.strip()
   try:fields[k]=json.loads(v)
   except json.JSONDecodeError:fields[k]=v
  source=B/r['fonte']['path'];assert sha(source.read_bytes())==r['fonte']['sha256'];raw=gzip.decompress(source.read_bytes());assert sha(raw)==r['fonte']['sha256_HTML'];src=html5lib.parse(raw,namespaceHTMLElements=False)
  owns=[e for e in src.iter('div') if 'textoNorma' in e.get('class','').split()];assert len(owns)==1;own=owns[0]
  bad=[e.tag for e in own.iter() if e.tag in ('table','img','u','ins','del','s','strike','sup','sub','em','i')];assert not bad,(n,bad)
  md=body.lstrip().split('\n',1)[1]
  if n=='4115':
   note='> A fonte oficial apresenta 2 de outubro na ementa e 3 de outubro no dispositivo; ambas as leituras foram preservadas.'
   assert md.count(note)==1;md=md.replace(note,'',1)
  assert not re.search(r'^>',md,re.M),n
  rendered=cmarkgfm.github_flavored_markdown_to_html(md);assert norm(text(own))==norm(text(dom(rendered))),n
  mt=A/folder/n/'metadados.html';assert sha(mt.read_bytes())==r['sha256_metadados'];rt=html5lib.parse(mt.read_text(),namespaceHTMLElements=False);full=text(rt);heads=[re.sub(r'\s+',' ',text(e)).strip() for e in rt.iter('h1')];h=next(x for x in heads if x.startswith('DECRETO Nº '));match=re.fullmatch(r'DECRETO Nº ([\d.]+), DE (\d+) DE ([A-ZÇ]+) DE (\d+)',h);assert match,(n,h)
  date=f'{int(match[4]):04}-{months.index(match[3].lower())+1:02}-{int(match[2]):02}';assert match[1].replace('.','')==n==fields['numero'] and date==fields['data'],n
  assert 'Poder Legislativo' in full and 'Não consta revogação expressa' in full and fields['revogada'] is None
  assert fields['tipo']=='Decreto do Poder Legislativo' and fields['versao_texto']=='original' and fields['urn']==r['urn']
  assert any(fields['fonte'].split('/')[-1] in e.get('href','') for e in rt.iter('a')),n
  y,mo,day=map(int,date.split('-'));closing=re.search(r'(?:Rio de Janeiro|Capital Federal),\s*'+str(day)+' de '+months[mo-1]+' de '+str(y),md,re.I);assert closing,n
  target=f'federal/decretos-legislativos/{y}/dpl-{n}-{date}.md';assert not (B/target).exists(),target;assert subprocess.run(['rtk','proxy','git','cat-file','-e','HEAD:'+target],capture_output=True).returncode!=0
  errors,warnings=aud.validar(s,target,datetime.date(2026,10,16));assert not errors and not warnings,(n,errors,warnings)
  rows.append({'numero':n,'candidato':r['candidato'],'sha256':r['sha256_MD'],'destino':target,'epigrafe_primaria':h,'data':date,'fecho':closing.group(),'revogada':None,'fonte_gzip':r['fonte'],'metadados':str(mt.relative_to(B)),'SHA_metadados':r['sha256_metadados'],'leitura_integral_raiz':True,'texto_DOM_GFM_identico':True,'sem_artigos_fabricados':True});bodies.append(body)
combined='\n\n'.join(bodies);local=cmarkgfm.github_flavored_markdown_to_html(combined);payload=json.dumps({'text':combined,'mode':'gfm','context':'ctresb/leis'}).encode();req=urllib.request.Request('https://api.github.com/markdown',data=payload,headers={'User-Agent':'leis-revisao-raiz','Content-Type':'application/json'},method='POST')
with urllib.request.urlopen(req,timeout=120) as r:remote=r.read().decode()
assert structure(dom(local))==structure(dom(remote));(O/'GitHub7.html').write_text(remote);(O/'GFM7.html').write_text(local)
result={'estado':'aprovado_raiz_para_publicacao7','quantidade':len(rows),'atos':rows,'manifestos_fontes':manifests,'GitHub_vs_local_texto_formatos_listas_tabelas':True,'SHA_HTML_GitHub':sha(remote.encode()),'observacoes':['Quatro atos completos sem articulacao preservados sem fabricar Artigo unico','Tres atos com referencia a artigo na ementa nao devem perder seu preambulo legislativo proprio','4115 mantem2outubroementa e3outubrodispositivo; data propria27agosto1920 sem harmonizacao','Publicacao nao certifica juridicamente vigencia nem facsimile oficial'],'nao_aplicado':True}
(O/'aprovacao-publicacao7-raiz.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'aprovados':len(rows),'SHA_aprovacao':sha((O/'aprovacao-publicacao7-raiz.json').read_bytes())}))
