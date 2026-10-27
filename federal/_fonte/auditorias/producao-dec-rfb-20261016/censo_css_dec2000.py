import base64,gzip,json,re,hashlib,collections
from html.parser import HTMLParser
from pathlib import Path
D=Path("federal/_fonte/auditorias/producao-dec-rfb-20261016");C=D/"coorte-DEC-2000"
class P(HTMLParser):
 def __init__(self):super().__init__();self.values=collections.defaultdict(collections.Counter);self.external=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=="link" and "stylesheet" in a.get("rel","").lower():self.external.append(a)
  for pair in a.get("style","").split(";"):
   if ":" not in pair:continue
   k,v=pair.split(":",1);k=k.strip().lower();v=v.strip().lower()
   if k in ("font-weight","font-style","text-decoration","text-decoration-line","vertical-align","font-family"):self.values[k][v]+=1
values=collections.defaultdict(collections.Counter);external=[];unknown=[];n=0
allowed={"font-weight":{"bold","normal","400","700","800","900"},"font-style":{"normal","italic","oblique"},"text-decoration":{"none","line-through"},"text-decoration-line":{"none","line-through"},"vertical-align":{"baseline","super","sub"}}
with gzip.open(C/"backup-fontes.jsonl.gz","rt") as f:
 for line in f:
  d=json.loads(line);s=gzip.decompress(base64.b64decode(d["fonte_gzip_base64"])).decode();p=P();p.feed(s);n+=1
  for k,c in p.values.items():
   values[k].update(c)
   if k in allowed:
    for v in c:
     if v not in allowed[k]:unknown.append({"path":d["path"],"property":k,"value":v})
  if p.external or re.search(r"@import",s,re.I):external.append(d["path"])
assert n==2000
r={"documentos":n,"valores":{k:dict(v) for k,v in values.items()},"CSS_externo_ou_import":external,"valores_nao_suportados":unknown,"observacao":"Censo literal independente do conversor. Herança/reset comuns aferidos pelo parser Forma; valores não suportados exigem revisão individual."}
(D/"censo-CSS-DEC2000.json").write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n");print(json.dumps(r,ensure_ascii=False))
