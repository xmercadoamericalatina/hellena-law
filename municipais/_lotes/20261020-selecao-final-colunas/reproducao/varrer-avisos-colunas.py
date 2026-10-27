exec(open('/tmp/varrer-epigrafes-colunas.py').read().split('rows=[]')[0])
pattern=re.compile(r'(?:^|\s{2,})(?:EXTRATO\s+(?:DE|DO|DA)\s+(?:CONTRATO|TERMO|DISPENSA|INEXIGIBILIDADE|ATA|ADITIVO)|AVISO\s+(?:DE|DO)\s+(?:LICITA[ÇC][ÃA]O|CONTRATA[ÇC][ÃA]O|DISPENSA|PREG[ÃA]O|TOMADA|CHAMADA)|EDITAL\s+(?:DE\s+)?(?:COMUNICA[ÇC][ÃA]O|LICITA[ÇC][ÃA]O|PREG[ÃA]O|CHAMAMENTO|CONVOCA[ÇC][ÃA]O)|PREG[ÃA]O\s+(?:ELETR[ÔO]NICO|PRESENCIAL)\s+N[º°.\s]*\d)',re.M)
rows=[]
for path in sel:
 if path not in evid:continue
 with gzip.open(ROOT/evid[path],'rt') as f:raw=json.load(f)['layout']
 hits=[{'offset':a.start(),'trecho':raw[max(0,a.start()-130):a.end()+270]} for a in pattern.finditer(raw)]
 codes=set(re.findall(r'[Cc][óo]digo\s+[Ii]dentificador\s*[:.\-]?\s*([A-Za-z0-9]{6,})',raw));
 if len(codes)>1:hits.append({'codigos_distintos':sorted(codes)})
 if hits:rows.append({'path':path,'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),'evidencia':evid[path],'hits':hits})
out=ROOT/'municipais/_lotes/20261020-gate-cabecalhos-estranhos';(out/'avisos-outras-colunas.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print('docs',len(rows),'hits',sum(len(r['hits']) for r in rows))
for i,r in enumerate(rows):print(i,r['path']);print(' | '.join(re.sub(r'\s+',' ',a.get('trecho',str(a)))[:500] for a in r['hits'][:3]))
