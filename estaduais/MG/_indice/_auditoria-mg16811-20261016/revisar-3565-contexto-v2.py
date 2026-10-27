import json,gzip,re,hashlib,collections
from pathlib import Path
from html.parser import HTMLParser
base=Path('estaduais/MG/_indice/_auditoria-mg16811-20261016');profile={x['path']:x for x in map(json.loads,(base/'perfil-documentos.jsonl').read_text().splitlines())};original=[x for x in json.load(open('estaduais/_fonte/auditorias/integralidade-snapshot-20261016.json'))['documentos'] if x['uf']=='MG' and any('sem_artigo' in a for a in x['alertas'])]
class Texto(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_starttag(self,t,a):
  if t in ('p','div','br','tr'):self.parts.append('\n')
 def handle_data(self,s):self.parts.append(s)
operator=re.compile(r'\bD\s*E\s*C\s*R\s*E\s*T\s*A\b|\bDELIBERA(?:M)?\b|\bRESOLVE(?:M)?\b|\bDETERMINA(?:M)?\b|\bCOMUNICA\s+QUE',re.I)
rows=[]
for r in original:
 p=profile[r['path']];raw=gzip.decompress(Path(p['cache']).read_bytes());text=raw.decode()
 if p['formato']=='HTMLfragmentoUTF8':parser=Texto();parser.feed(text);plain=''.join(parser.parts)
 else:plain=text
 op=operator.search(plain);after=plain[op.end():] if op else '';art=re.search(r'Art(?:igo|\.)\s*(?:\d+|[úu]nico)',after,re.I);classification='artigos_proprios_inline_apos_comando' if art else 'ato_nao_articulado_com_dispositivo_apos_comando' if op else 'incerto_sem_comando_reconhecido_revisao_individual';rows.append(dict(path=r['path'],fonte_sha256=p['source_sha256'],md_sha256=p['md_sha256'],classificacao=classification,comando=plain[max(0,op.start()-150):op.end()+300] if op else plain[:600],artigo_proprio=after[max(0,art.start()-80):art.end()+240] if art else None,fim=plain[-700:],limite='Classificação contextual do alertaoriginal; demais gates deomissão/data/renderização continuam obrigatórios.'))
p=base/'revisao-contextual-3565-sem-artigo-v2.jsonl';p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows));summary=dict(total=len(rows),classificacoes=dict(collections.Counter(r['classificacao'] for r in rows)),sha256=hashlib.sha256(p.read_bytes()).hexdigest());(base/'revisao-contextual-3565-resumo-v2.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(summary)
