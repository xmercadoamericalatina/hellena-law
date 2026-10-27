import json,re,gzip,hashlib,collections
from pathlib import Path
BASE=Path('estaduais/MG/_indice/_auditoria-mg16811-20261016');sha=lambda b:hashlib.sha256(b).hexdigest();triage=BASE/'triagem-omissoes-raiz.json';records=json.load(open(triage));extra=BASE/'triagem-adicional-raiz.json';by={r['path']:r for r in records};
for r in json.load(open(extra)):
 if r['path'] in by:by[r['path']]['hits']+=r['hits']
 else:records.append(r);by[r['path']]=r
profiles={r['path']:r for r in map(json.loads,(BASE/'perfil-documentos.jsonl').read_text().splitlines())}
intro=re.compile(r'passa(?:m)? (?:a )?(?:vigorar|viger|ter).{0,200}(?:reda[cç][aã]o|altera[cç][oõ]es|acrescid)|fica[m]? .{0,180}(?:acrescid|acrescentad|alterad).{0,200}(?:reda[cç][aã]o|seguintes?)|tem a seguinte redação',re.I|re.S)
rows=[]
for rec in records:
 p=profiles[rec['path']];md=Path(rec['path']).read_bytes();assert sha(md)==p['md_sha256'];raw=gzip.decompress(Path(p['cache']).read_bytes());assert sha(raw)==p['source_sha256'];text=md.decode();paras=[dict(start=m.start(),end=m.end(),text=m[0]) for m in re.finditer(r'[^\n](?:[^\n]|\n(?!\n))*(?=\n\n|$)',text)];zones=[]
 # A instrução é localizada globalmente: algumas fontes oficiais são texto puro sem parágrafos.
 for ins in intro.finditer(text):
  qmatch=re.search(r'[“\"]\s*(?:Art\.?|ANEXO|[IVXLCDM]+\s*[–—-]|§|[0-9]+\s*[.\-])',text[ins.end():ins.end()+600],re.I)
  if not qmatch:continue
  start=ins.end()+qmatch.start();tail=text[start:];cap=len(text)
  ownfecho=re.search(r'(?:Palácio da Liberdade|Belo Horizonte,? (?:aos?|\d))',tail,re.I)
  if ownfecho:cap=start+ownfecho.start()
  # NR delimita a redação citada mesmo quando nomes/segundos usam aspas internas.
  nr=re.search(r'[”\"]\s*[,.;]?\s*\(nr\)',text[start:cap],re.I)
  if nr:finish=start+nr.end()
  else:
   closing=re.search(r'[”\"][.;,]?\s*(?=\n\n\*\*Art\.)',text[start+1:cap]) or re.search(r'[”\"]',text[start+1:cap]);found=start+1+closing.start() if closing else -1
   if found<0:continue
   finish=found+1
  instart=max(text.rfind('\n\n',0,ins.start())+2,text.rfind('**Art.',0,ins.start()))
  if ins.start()-instart>1800:instart=max(0,ins.start()-700)
  instruction=dict(start=instart,end=ins.end(),text=text[instart:ins.end()])
  zones.append(dict(inicio=start,fim=finish,instrucao=instruction,quote_sha256=sha(text[start:finish].encode()),quote_inicio=text[start:start+180],quote_fim=text[max(start,finish-180):finish]))
 ellipses=list(re.finditer(r'(?:\.(?:[.\s]*\.){2,}|…+)',text));events=[]
 for match in ellipses:
  ids=[j for j,h in enumerate(rec['hits']) if re.fullmatch(r'[.\s…]+',h['marcador']) and match.start()<=h['posicao']<match.end()]
  if not ids:continue
  zone=next((z for z in zones if z['inicio']<=match.start() and match.end()<=z['fim']),None);decision='reticencias_em_alteracao_expressa_citada' if zone else 'incerto_reticencias_fora_aspas_com_instrucao_comprovada';events.append(dict(tipo='reticencias',inicio=match.start(),fim=match.end(),literal=match[0],literal_sha256=sha(match[0].encode()),hits_origem=ids,contexto=text[max(0,match.start()-350):match.end()+350],decisao=decision,prova_alteracao=zone))
 lexical=[dict(hit_indice=j,**h) for j,h in enumerate(rec['hits']) if not re.fullmatch(r'[.\s…]+',h['marcador'])]
 rows.append(dict(path=rec['path'],md_sha256=sha(md),fonte_sha256=sha(raw),cache=p['cache'],numero_hits_origem=len(rec['hits']),reticencias=events,marcadores_lexicais=lexical,zonas_alteracao=zones))
path=BASE/'revisao-unificada-contexto-v5.jsonl';path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows));counts=collections.Counter(e['decisao'] for r in rows for e in r['reticencias']);summary=dict(triagem_sha256=sha(triage.read_bytes()),documentos=len(rows),eventos=dict(counts),com_incertos=sum(any(e['decisao'].startswith('incerto') for e in r['reticencias']) for r in rows),prova_sha256=sha(path.read_bytes()));(BASE/'revisao-unificada-contexto-v5-resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(summary)
