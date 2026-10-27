import json,hashlib,gzip,sys
from pathlib import Path
B=Path('estaduais/MG/_indice/_auditoria-mg16811-20261016');sha=lambda b:hashlib.sha256(b).hexdigest();by={}
for r in map(json.loads,(B/'fila-contextual-reticencias-v5.jsonl').read_text().splitlines()):by.setdefault(r['path'],[]).append(r)
config=json.load(sys.stdin);out=[]
for path,events in list(by.items())[config['inicio']:config['fim']]:
 stem=Path(path).stem;decision=config['decisoes'][stem];md=Path(path).read_bytes();t=md.decode();raw=gzip.decompress(Path(events[0]['cache']).read_bytes());assert sha(md)==events[0]['md_sha256'] and sha(raw)==events[0]['fonte_sha256'];out.append(dict(path=path,md_sha256=sha(md),fonte_sha256=sha(raw),cache=events[0]['cache'],decisao=decision['decisao'],fundamento=decision['fundamento'],cobertura_leitura=decision.get('cobertura','identidade, comando proprio, todos os eventos pendentes e seus contextos, remissoes/anexos visiveis, fecho; sem certificacao visual'),eventos_resolvidos=[dict(evento_indice=e['evento_indice'],inicio=e['inicio'],fim=e['fim'],literal_sha256=e['literal_sha256'],contexto=e['contexto'],contexto_sha256=sha(e['contexto'].encode())) for e in events],body_sha256=sha(t.split('\n---\n',1)[1].encode()),trecho_inicial=t[:2500],trecho_final=t[-2500:],aplicado=False))
f=B/('revisao-sequencial-216-lote'+config['lote']+'.json');assert not f.exists();f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(len(out),sha(f.read_bytes()))
