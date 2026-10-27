import pathlib,json,hashlib,gzip,re,subprocess,html5lib
B=pathlib.Path('/Volumes/ExternalSSD/GitHub/constituicao');A=B/'federal/_fonte/auditorias/dpl13-quadros-visuais-20261016';O=A/'revisao-raiz13'
g=json.loads((O/'verificacao-GFM-GitHub13-raiz.json').read_text());f=json.loads((O/'verificacao-fontes-renders-raiz.json').read_text())
assert g['quantidade']==13 and f['arquivos_manifesto']==239 and f['paginas_originais_reproduzidas']==27
sha=lambda b:hashlib.sha256(b).hexdigest()
months=['JANEIRO','FEVEREIRO','MARÇO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO']
records=[]
for a in g['atos']:
 n=a['numero'];p=B/a['candidato'];assert sha(p.read_bytes())==a['sha256'];s=p.read_text();meta,body=s[4:].split('\n---\n',1)
 fields={}
 for line in meta.splitlines():
  k,v=line.split(':',1);v=v.strip()
  try:fields[k]=json.loads(v)
  except json.JSONDecodeError:fields[k]=v
 old=json.loads((A/'atos'/n/'HTML-alternativa-md-baseline.json').read_text());target=B/old['path']
 assert target.is_file() and sha(target.read_bytes())==old['sha256_md_atual'],str(target)
 proc=subprocess.run(['rtk','proxy','git','cat-file','-e','HEAD:'+old['path']],capture_output=True);assert proc.returncode!=0,'já publicado '+n
 raw=next((A/'atos'/n).glob('alternativa-url_metadados*.gz'));html=gzip.decompress(raw.read_bytes()).decode();root=html5lib.parse(html,namespaceHTMLElements=False)
 text=re.sub(r'\s+',' ',''.join(root.itertext()));assert 'Origem: Poder Legislativo' in text and 'Não consta revogação expressa' in text,n
 year,month,day=map(int,fields['data'].split('-'));heads=[re.sub(r'\s+',' ',''.join(e.itertext())).strip() for e in root.iter('h1')]
 h=next(x for x in heads if x.startswith('DECRETO Nº '));num=re.search(r'DECRETO Nº ([\d.]+), DE (\d+) DE ([A-ZÇ]+) DE (\d+)',h);assert num,n
 assert num[1].replace('.','')==n and int(num[2])==day and months.index(num[3])+1==month and int(num[4])==year,n
 links=[e.get('href','') for e in root.iter('a')];assert any(fields['fonte_alternativa_HTML'].split('/')[-1] in v for v in links),n
 closing=re.search(r'(?:Rio de Janeiro|Senado Federal),\s*'+str(day)+r' de '+months[month-1].lower()+' de '+str(year),body,re.I);assert closing,n
 assert fields['revogada'] is None and fields['situacao']=='Não consta revogação expressa'
 records.append({'numero':n,'candidato':a['candidato'],'sha256':a['sha256'],'destino':old['path'],'antes_sha256':old['sha256_md_atual'],'metadata_primaria_sha256':sha(raw.read_bytes()),'epigrafe_primaria':h,'fecho':closing.group(),'origem':'Poder Legislativo','revogada':None,'versao':'coletanea_oficial_transcricao_cotejada'})
result={'estado':'aprovado_raiz_para_publicacao13','quantidade':13,'fonte_visual_paginas_lidas':27,'fontes_reproduzidas':f['paginas_originais_reproduzidas'],'checks_formato_GFM_GitHub':str((O/'verificacao-GFM-GitHub13-raiz.json').relative_to(B)),'atos':records,'achados_corrigidos':['5018 pontuacao e italicos','5585 pontuacao e caixa','5597 ordinal','5745 duas linhas restauradas com nome re Mesquita literal'],'observacoes':['5585 preserva18:150$561 noArt2 e18:105$651 noquadro, ambos impressos','5745 alegacao anterior diferenca de versao retratada; oraculo324 nao prova completude','Leitura visual integral dos13apos propostas; fontes coletaneas oficiais preservadas com pagina e hash, alternativas HTML mantidas','Nao fac-simile DOU nem certificacao juridica; estilos e graficos de pontilhados representados por tabelas com fonte integral'],'canonicos_ainda_nao_aplicados':True}
(O/'aprovacao-publicacao13-raiz.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'aprovados':len(records),'sha256_aprovacao':sha((O/'aprovacao-publicacao13-raiz.json').read_bytes())}))
