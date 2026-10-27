from pathlib import Path
import json,gzip,base64,hashlib,re,unicodedata
import html5lib
D=Path('federal/_fonte/auditorias/producao-dec-rfb-20261016');O=D/'revisao-raiz-DEC1951';paths=set((D/'overlay-contextual-DEC2000/paths-sem-alerta-adicional.txt').read_text().splitlines());refs={r['inventario']['path']:r['inventario'] for r in map(json.loads,(D/'coorte-DEC-2000/coorte2000.jsonl').read_text().splitlines())}
sha=lambda b:hashlib.sha256(b).hexdigest()
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.casefold()) if not unicodedata.combining(c))
rows=[];alerts=[]
with gzip.open(D/'coorte-DEC-2000/backup-fontes.jsonl.gz','rt') as f,(O/'artigos1951-raiz.jsonl').open('w') as out:
 for line in f:
  r=json.loads(line)
  if r['path'] not in paths:continue
  raw=gzip.decompress(base64.b64decode(r['fonte_gzip_base64']));assert sha(raw)==refs[r['path']]['sha256_fonte'];body=html5lib.parse(raw.decode().lstrip('\ufeff'),namespaceHTMLElements=False).find('body');ps=[re.sub(r'\s+',' ',''.join(e.itertext())).strip() for e in body.iter('p')];ps=[p for p in ps if p];articles=[]
  for i,p in enumerate(ps):
   m=re.match(r'^art(?:igo)?[.\s]*(\d+|unico)(?:[º°o.\s-]|$)',norm(p))
   if m:articles.append({'indice_p':i,'numero':int(m[1]) if m[1].isdigit() else 'unico','literal':p})
  nums=[a['numero'] for a in articles];good=nums==['unico'] or bool(nums) and all(isinstance(n,int) for n in nums) and nums==list(range(1,max(nums)+1))
  row={'path':r['path'],'sha256_fonte':sha(raw),'numeros':nums,'sequencia_contigua':good,'artigos':articles};out.write(json.dumps(row,ensure_ascii=False)+'\n');out.flush();rows.append(row)
  if not good:alerts.append({**row,'texto_fonte_integral':'\n\n'.join(ps)})
  if len(rows)%300==0:print(json.dumps({'artigos_revistos':len(rows),'alertas':len(alerts)}),flush=True)
assert len(rows)==1951
(O/'artigos-alertas-contexto-raiz.json').write_text(json.dumps({'documentos':1951,'alertas':alerts,'politica':'Reconhece espacos entre Art e ponto sem modificar literal; unico e numeracao sequencial. Gaps/duplicatas exigem contexto proprio, nao correcao automatica.'},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'documentos':len(rows),'alertas':len(alerts)}),flush=True)
