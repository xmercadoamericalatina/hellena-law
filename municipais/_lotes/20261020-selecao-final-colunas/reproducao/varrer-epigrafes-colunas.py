import json,gzip,re,sys,hashlib
from pathlib import Path
ROOT=Path('/Volumes/ExternalSSD/GitHub/constituicao');sys.path.insert(0,str(ROOT/'scripts'));from auditar_municipal import metadados
lists=['20261020-gate-anexos-primeira-publicacao/aprovados.paths.txt','20261020-gate-anexos-qualificacao-contextual/aprovados.paths.txt','20261020-recuperacao-pdf-final/lote-0001.paths.txt','20261020-decorativos004-final/lote-0001.paths.txt'];sel=[s for f in lists for s in (ROOT/'municipais/_lotes'/f).read_text().splitlines()];evid={r['path']:r['evidencia_extracao']['path'] for l in (ROOT/'municipais/_lotes/20261020-overlay-integralidade-pdf/resultados.jsonl').read_text().splitlines() if (r:=json.loads(l)).get('evidencia_extracao')};pattern=re.compile(r'(?:^|\s{2,})(?P<tipo>PORTARIA|RESOLU[ÇC][ÃA]O|DECRETO(?:\s+LEGISLATIVO)?|LEI(?:\s+COMPLEMENTAR)?|EMENDA(?:\s+[ÀA]\s+LEI\s+ORG[ÂA]NICA)?)\s+(?:N[º°oO.\s]*\s*)?(?P<numero>\d[\d.]*)\s*(?=[/,]|$|\bDE\b)',re.M)
rows=[]
for path in sel:
 if path not in evid:continue
 md=(ROOT/path).read_text();m=metadados(md);own=re.sub(r'\D','',str(m['numero'])).lstrip('0');tip=str(m['tipo']).lower();tip='EMENDA' if 'emenda' in tip else 'DECRETO' if 'decreto' in tip else 'RESOLU' if 'resolu' in tip else 'LEI'
 with gzip.open(ROOT/evid[path],'rt') as f:raw=json.load(f)['layout']
 hits=[]
 for a in pattern.finditer(raw):
  n=re.sub(r'\D','',a['numero']).lstrip('0');t=a['tipo']
  if n==own and t.startswith(tip):continue
  hits.append({'tipo':t,'numero':n,'offset':a.start(),'trecho':raw[max(0,a.start()-120):a.end()+220]})
 if hits:rows.append({'path':path,'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),'evidencia':evid[path],'hits':hits})
out=ROOT/'municipais/_lotes/20261020-gate-cabecalhos-estranhos';(out/'epigrafes-outras-colunas.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print('docs',len(rows),'hits',sum(len(r['hits']) for r in rows))
for i,r in enumerate(rows):print(i,r['path'],[(a['tipo'],a['numero']) for a in r['hits']]);print(' | '.join(re.sub(r'\s+',' ',a['trecho'])[:300] for a in r['hits'][:2]))
