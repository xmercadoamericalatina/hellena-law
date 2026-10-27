from pathlib import Path
import json,gzip,re,sys,hashlib
sys.path.insert(0,str(Path('scripts').resolve()));import baixar_camara as c
B=Path('federal/_fonte/auditorias/dpl-auditoria-20261016');paths={r['path'] for r in map(json.loads,(B/'verificacao-raiz-identidade-3273.jsonl').open())};rows=[]
for r in map(json.loads,(B/'inventario5409-revisado.jsonl').open()):
 if r['path'] not in paths:continue
 source=c.corpo_norma(gzip.decompress(Path(r['fonte_cache']['snapshot']).read_bytes()).decode());hits=[{'posicao':m.start(),'trecho':source[max(0,m.start()-100):m.end()+180]} for m in re.finditer(r'<u(?:\s|>)|text-decoration[^;"\'>]*underline',source,re.I)]
 if hits:rows.append({'path':r['path'],'source_sha256':r['fonte_cache']['sha256_fonte'],'hits':hits})
p=B/'triagem-sublinhado-raiz-3273.json';p.write_text(json.dumps({'escopo':len(paths),'com_marcador':len(rows),'documentos':rows},ensure_ascii=False,indent=2)+'\n');print('U3273',len(rows),flush=True)
