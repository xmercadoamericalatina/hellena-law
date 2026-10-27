import base64,gzip,hashlib,json,re
from pathlib import Path
from html.parser import HTMLParser
D=Path("federal/_fonte/auditorias/producao-dec-rfb-20261016");C=D/"coorte-DEC-2000";O=D/"overlay-contextual-DEC2000"
class P(HTMLParser):
 def __init__(self,s):super().__init__();self.rows=[];self.feed(s)
 def handle_starttag(self,t,a):
  for k,v in a:
   v=v or ""
   if k.lower()in {"hidden","inert"}or(k.lower()=="aria-hidden"and v.lower()=="true")or(k.lower()in {"href","src","data"}and re.match(r"^(?:javascript|data|blob|file|vbscript):",v,re.I)):self.rows.append({"tag":t,"atributo":k,"literal":v})
rows=[]
with gzip.open(C/"backup-fontes.jsonl.gz","rt")as f:
 for line in f:
  d=json.loads(line);b=gzip.decompress(base64.b64decode(d["fonte_gzip_base64"]));s=b.decode();p=P(s);hits=[]
  for pattern in [r"(?:url|expression)\s*\(",r"@(?:import|font-face)\b",r"(?:behavior|-moz-binding)\s*:",r"(?:ap[eê]ndice|separata|n[aã]o\s+(?:inclu[ií]d[oa]|reproduzid[oa]|publicad[oa]))"]:
   for m in re.finditer(pattern,s,re.I):hits.append({"padrao":pattern,"literal_contexto":s[max(0,m.start()-100):m.end()+150]})
  rows.append({"path":d["path"],"sha256_fonte":hashlib.sha256(b).hexdigest(),"atributos_ocultos_protocolos":p.rows,"CSS_externo_e_omissoes_adicionais":hits,"retido":bool(p.rows or hits)})
assert len(rows)==2000
p=O/"controles-complementares.json";p.write_text(json.dumps({"documentos":len(rows),"retidos":sum(x["retido"]for x in rows),"registros":rows},ensure_ascii=False,indent=2)+"\n");print("CONTROLES",len(rows),sum(x["retido"]for x in rows))
