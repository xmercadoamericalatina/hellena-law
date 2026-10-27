exec(open('/tmp/varrer-epigrafes-colunas.py').read().split('rows=[]')[0])
rows=[];pattern=re.compile(r'^\s*DI[ÁA]RIO\s+OFICIAL.{0,160}',re.M|re.I)
for path in sel:
 if path not in evid:continue
 with gzip.open(ROOT/evid[path],'rt') as f:raw=json.load(f)['layout']
 hits=[{'offset':a.start(),'trecho':a.group(0)} for a in pattern.finditer(raw)]
 if hits:rows.append({'path':path,'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),'evidencia':evid[path],'hits':hits,'paginas':len(raw.rstrip('\f').split('\f'))})
out=ROOT/'municipais/_lotes/20261020-gate-cabecalhos-estranhos';(out/'diarios-cabecalho.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print('docs',len(rows));
for i,r in enumerate(rows):print(i,r['path'],r['paginas'],[a['trecho'].strip()[:140] for a in r['hits'][:2]])
