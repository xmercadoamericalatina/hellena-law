exec(open('/tmp/varrer-epigrafes-colunas.py').read().split('rows=[]')[0])
rows=[]
pattern=re.compile(r'(?:^|\s{2,})(?:PROJETO\s+DE\s+(?:LEI|RESOLU[ÇC][ÃA]O|DECRETO)|MINUTA\b|ANTEPROJETO\b)',re.M)
for path in sel:
 if path not in evid:continue
 with gzip.open(ROOT/evid[path],'rt') as f:raw=json.load(f)['layout']
 hits=[{'offset':a.start(),'trecho':raw[max(0,a.start()-100):a.end()+400]} for a in pattern.finditer(raw[:2500])]
 if hits:rows.append({'path':path,'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),'evidencia':evid[path],'hits':hits})
out=ROOT/'municipais/_lotes/20261020-gate-cabecalhos-estranhos';(out/'objetos-projetos-suspeitos.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print('docs',len(rows));print(json.dumps(rows,ensure_ascii=False,indent=2)[:16000])
