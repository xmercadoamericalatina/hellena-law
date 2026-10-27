from pathlib import Path
import json,gzip,re,html,sys
sys.path.insert(0,str(Path('scripts').resolve()));import baixar_camara as c
B=Path('federal/_fonte/auditorias/dpl-auditoria-20261016');paths={r['path'] for r in map(json.loads,(B/'verificacao-raiz-identidade-3273.jsonl').open())};rows=[]
for r in map(json.loads,(B/'inventario5409-revisado.jsonl').open()):
 if r['path'] not in paths:continue
 source=c.corpo_norma(gzip.decompress(Path(r['fonte_cache']['snapshot']).read_bytes()).decode());hits=[]
 for block in re.split(r'<br\s*/?>|</p>',source,flags=re.I):
  plain=html.unescape(re.sub('<[^>]+>',' ',block));money=re.findall(r'\d[\d.:,]*\$[\d.,]*',plain)
  if re.search(r'\.{5,}',plain) and len(money)>=2:hits.append({'trecho':plain,'valores':money})
 if hits:rows.append({'path':r['path'],'source_sha256':r['fonte_cache']['sha256_fonte'],'linhas_multiplos_valores':hits})
p=B/'triagem-quadros-lineares-raiz.json';p.write_text(json.dumps({'escopo':len(paths),'suspeitos':len(rows),'documentos':rows},ensure_ascii=False,indent=2)+'\n');print('QUADROSLINEARES',len(rows),flush=True)
