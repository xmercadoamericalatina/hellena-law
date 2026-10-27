from pathlib import Path
import json,gzip,re,html,sys
sys.path.insert(0,str(Path('scripts').resolve()));import baixar_camara as c
B=Path('federal/_fonte/auditorias/dpl-auditoria-20261016');paths={r['path'] for r in map(json.loads,(B/'verificacao-raiz-identidade-3273.jsonl').open())};rows=[];pattern=re.compile(r'\d[\d.:]*\$[0-9]{0,3}[\s\u00a0]*\d[\d.:]*\$[0-9]{0,3}')
for r in map(json.loads,(B/'inventario5409-revisado.jsonl').open()):
 if r['path'] not in paths:continue
 source=c.corpo_norma(gzip.decompress(Path(r['fonte_cache']['snapshot']).read_bytes()).decode());hits=[]
 for block in re.split(r'<br\s*/?>|</p>',source,flags=re.I):
  plain=html.unescape(re.sub('<[^>]+>',' ',block));ms=list(pattern.finditer(plain))
  if ms:hits.append({'trecho':plain,'pares':[m.group() for m in ms]})
 if hits:rows.append({'path':r['path'],'source_sha256':r['fonte_cache']['sha256_fonte'],'hits':hits})
p=B/'triagem-valores-adjacentes-raiz.json';p.write_text(json.dumps({'escopo':len(paths),'suspeitos':len(rows),'documentos':rows},ensure_ascii=False,indent=2)+'\n');print('VALORESADJACENTES',len(rows),flush=True)
