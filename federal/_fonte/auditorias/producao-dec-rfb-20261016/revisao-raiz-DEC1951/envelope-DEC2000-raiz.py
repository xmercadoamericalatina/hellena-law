from pathlib import Path
import json,hashlib,gzip,base64,collections
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');D=B/'federal/_fonte/auditorias/producao-dec-rfb-20261016';O=D/'revisao-raiz-DEC1951'
sha=lambda b:hashlib.sha256(b).hexdigest()
seeds={'manifesto-final-DEC2000.json':'3f5dab56bef71b877ef3b68741632326fb7dc7accb4cd087e09bb988a8b8c487','overlay-contextual-DEC2000/manifesto-overlay.json':'5955ace8f2a7f5f7c26a47126807959d71b2bfc474baa2099a61c9ccbb83320f'}
checked={};pending=[]
for p,h in seeds.items():pending.append((str((D/p).relative_to(B)),h))
pending.append((str((D/'perfil-proveniencia-DEC2000.json').relative_to(B)),None))
pending.append((str((D/'indice-DEC-master-congelado.json.gz').relative_to(B)),'05bae939074ed9faf044f3738ab0a28323f298509e7445207b66b9c9a6baad2a'))
def refs(x):
 if isinstance(x,dict):
  if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str):yield x['path'],x['sha256']
  if isinstance(x.get('snapshot'),str) and isinstance(x.get('sha256'),str):yield x['snapshot'],x['sha256']
  for v in x.values():yield from refs(v)
 elif isinstance(x,list):
  for v in x:yield from refs(v)
while pending:
 p,h=pending.pop();file=B/p;data=file.read_bytes();actual=sha(data)
 assert h is None or h==actual,(p,h,actual)
 if p in checked:assert checked[p]['sha256']==actual;continue
 checked[p]={'path':p,'sha256':actual,'bytes':len(data)}
 if file.suffix=='.json':
  try:doc=json.loads(data)
  except (UnicodeDecodeError,json.JSONDecodeError):continue
  pending.extend(refs(doc))
paths=set((D/'overlay-contextual-DEC2000/paths-sem-alerta-adicional.txt').read_text().splitlines())
inventory={r['inventario']['path']:r['inventario'] for r in map(json.loads,(D/'coorte-DEC-2000/coorte2000.jsonl').read_text().splitlines())}
legal=collections.Counter();versions=collections.Counter();count=0
for l in gzip.open(D/'coorte-DEC-2000/backup-fontes.jsonl.gz','rt'):
 row=json.loads(l)
 if row['path'] not in paths:continue
 m=json.loads(gzip.decompress(base64.b64decode(row['metadata_gzip_base64'])))
 enc=m.get('encoding',[]);enc=enc if isinstance(enc,list) else [enc]
 chosen=inventory[row['path']]['encoding_escolhido'];assert chosen in enc and chosen['version']=='Original'
 value=chosen.get('legislationLegalValue');legal[json.dumps(value,ensure_ascii=False,sort_keys=True)]+=1
 for e in enc:versions[e.get('version','ausente')]+=1
 count+=1
assert count==1951
result={'estado':'envelope_conferido_sem_aprovacao','arquivos':sorted(checked.values(),key=lambda x:x['path']),'documentos_rawmetadata_censeados':count,'encoding_escolhido.legislationLegalValue':dict(legal),'encoding_versions_todos_encodings':dict(versions),'correcao_V1':'CensoV1 consultava campo ausente na raizJSON(null1951), nao campo do encoding selecionado. V2consulta exatamente encoding_escolhido e inclui snapshot primario explicitamente.','limites':'VersaoOriginal e valor juridico da API nao certificam exemplar impresso. Manifestos historicos mantem suas limitacoes, substituidos somente por overlays explicitos.'}
(O/'envelope-coorte2000-v2-raiz.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'arquivos':len(checked),'rawmetadata':count,'valor_legal':dict(legal)},ensure_ascii=False))
