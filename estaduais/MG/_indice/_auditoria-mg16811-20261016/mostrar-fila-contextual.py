import json,re,sys
from pathlib import Path
B=Path('estaduais/MG/_indice/_auditoria-mg16811-20261016');by={}
for e in map(json.loads,(B/'fila-contextual-reticencias-v5.jsonl').read_text().splitlines()):by.setdefault(e['path'],[]).append(e)
for p,es in list(by.items())[int(sys.argv[1]):int(sys.argv[2])]:
 t=Path(p).read_text();print('\nFILE',p,'LEN',len(t),'EVENTS',len(es))
 if len(t)<5000:print(t);continue
 ranges=[(0,1800),(len(t)-1500,len(t))]+[(max(0,e['inicio']-210),min(len(t),e['fim']+210)) for e in es]
 for m in re.finditer(r'passa(?:m)? a vigorar|(?:fica[m]?|ficam?|ficam) .{0,60}acrescid|publicado no MGEX|publicados no|nao digitado',t,re.I):ranges.append((max(0,m.start()-170),min(len(t),m.end()+180)))
 merged=[]
 for a,b in sorted(ranges):
  if merged and a<=merged[-1][1]+100:merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
  else:merged.append((a,b))
 for a,b in merged:print('TRECHO',a,b,'\n',t[a:b])
