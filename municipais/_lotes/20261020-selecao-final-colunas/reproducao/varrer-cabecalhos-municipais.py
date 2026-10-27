from pathlib import Path
import re,sys,json,unicodedata,hashlib
ROOT=Path('/Volumes/ExternalSSD/GitHub/constituicao');sys.path.insert(0,str(ROOT/'scripts'));from auditar_municipal import metadados
lists=['20261020-gate-anexos-primeira-publicacao/aprovados.paths.txt','20261020-gate-anexos-qualificacao-contextual/aprovados.paths.txt','20261020-recuperacao-pdf-final/lote-0001.paths.txt','20261020-decorativos004-final/lote-0001.paths.txt']
normal=lambda s:''.join(c for c in unicodedata.normalize('NFD',s).lower() if unicodedata.category(c)!='Mn')
sel=[s for f in lists for s in (ROOT/'municipais/_lotes'/f).read_text().splitlines()];rows=[]
pattern=r'\b(?:PREFEITURA|C[ÂA]MARA)\s+MUNICIPAL\s+(?:DE|DA|DO)\s+'
for p in sel:
 s=(ROOT/p).read_text();m=metadados(s);body=s.split('\n---\n',1)[1].lstrip('\n').split('\n\n',1)[1];hits=[]
 for a in re.finditer(pattern,body,re.I):
  tail=body[a.end():a.end()+110];town=normal(m['municipio']);t=normal(tail)
  if not t.startswith(town):hits.append({'offset':a.start(),'trecho':body[max(0,a.start()-90):a.end()+160]})
 if hits:rows.append({'path':p,'municipio':m['municipio'],'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),'alertas':hits})
out=ROOT/'municipais/_lotes/20261020-gate-cabecalhos-estranhos';out.mkdir(exist_ok=False);(out/'suspeitos.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print('suspeitos',len(rows));print(json.dumps(rows,ensure_ascii=False,indent=2)[:40000])
