exec(open('/tmp/varrer-epigrafes-colunas-v2.py').read().split('rows=[]')[0])
months={'janeiro':1,'fevereiro':2,'marco':3,'abril':4,'maio':5,'junho':6,'julho':7,'agosto':8,'setembro':9,'outubro':10,'novembro':11,'dezembro':12};import unicodedata,datetime
rows=[];checked=0
for path in sel:
 if path not in evid:continue
 md=(ROOT/path).read_text();m=metadados(md);own=re.sub(r'\D','',str(m['numero'])).lstrip('0')
 with gzip.open(ROOT/evid[path],'rt') as f:raw=json.load(f)['layout']
 for a in pattern.finditer(raw[:5000]):
  if re.sub(r'\D','',a['numero']).lstrip('0')!=own:continue
  post=raw[a.end():a.end()+190];dm=re.match(r'\s*(?:/\s*\d{2,4})?\s*[,.-]?\s*(?:DE\s+)?(\d{1,2})[º°]?\s+DE\s+(\w+)\s+DE\s+(\d{4})',post,re.I)
  if not dm:continue
  month=''.join(c for c in unicodedata.normalize('NFD',dm[2]).lower() if unicodedata.category(c)!='Mn')
  if month not in months:continue
  checked+=1
  try:d=datetime.date(int(dm[3]),months[month],int(dm[1])).isoformat()
  except ValueError:d='data_inválida'
  if d!=m.get('data'):rows.append({'path':path,'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),'data_metadado':m.get('data'),'data_epigrafe':d,'trecho':raw[a.start():a.end()+190],'evidencia':evid[path]})
  break
out=ROOT/'municipais/_lotes/20261020-gate-cabecalhos-estranhos';(out/'datas-epigrafes.json').write_text(json.dumps({'datas_claras_conferidas':checked,'divergencias':rows},ensure_ascii=False,indent=2));print('datasconferidas',checked,'divergencias',len(rows));print(json.dumps(rows,ensure_ascii=False,indent=2)[:20000])
