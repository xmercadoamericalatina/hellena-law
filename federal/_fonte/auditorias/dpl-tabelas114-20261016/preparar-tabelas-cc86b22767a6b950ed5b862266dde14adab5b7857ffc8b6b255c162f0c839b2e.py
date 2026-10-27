"""Propostas estruturais isoladas; nunca aplica MD canônico ou acessa rede."""
from pathlib import Path
import json,gzip,hashlib,sys,re,html,argparse
from html.parser import HTMLParser
ROOT=Path.cwd();B=ROOT/"federal/_fonte/auditorias/dpl-auditoria-20261016";OUT=ROOT/"federal/_fonte/auditorias/dpl-tabelas114-20261016"
sys.path.insert(0,str(ROOT/"scripts"));import baixar_camara as c
CORE="bb85371750359042e0636ae0adc206cb0c353c6b6586c8d46e60a5257633ed3c"
def sha(x):return hashlib.sha256(x).hexdigest()
def write(p,b,audit):
 if audit or p.exists():assert p.read_bytes()==b,str(p)
 else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
class Tables(HTMLParser):
 def __init__(self):super().__init__();self.sig=[];self.depth=0
 def handle_starttag(self,t,a):
  if t=="table":self.depth+=1
  if self.depth and t in ("table","tr","td","th"):self.sig.append(("start",t,tuple(sorted((k,v) for k,v in a if k in ("rowspan","colspan")))))
 def handle_endtag(self,t):
  if self.depth and t in ("table","tr","td","th"):self.sig.append(("end",t))
  if t=="table":self.depth-=1
 def handle_data(self,d):
  if self.depth:
   d=" ".join(d.split())
   if d:self.sig.append(("text",d))
def sig(s):p=Tables();p.feed(s);return p.sig
def run(audit=False):
 assert sha((ROOT/"scripts/html2md.py").read_bytes())==CORE
 rows=[json.loads(x) for x in (B/"inventario5409-revisado.jsonl").read_text().splitlines()];rows=[r for r in rows if r.get("coorte")=="retido_revisao" and r.get("tabelas_fonte")];assert len(rows)==114
 ledger=[]
 for r in rows:
  old=(ROOT/r["path"]).read_bytes();assert sha(old)==r["sha256_md"]
  source=ROOT/r["fonte_cache"]["snapshot"];packed=source.read_bytes();assert sha(packed)==r["fonte_cache"]["sha256_arquivo"]
  raw=gzip.decompress(packed);assert sha(raw)==r["fonte_cache"]["sha256_fonte"]
  fragment=c.corpo_norma(raw.decode());body=c.convert(fragment).strip();same=sig(fragment)==sig(body)
  boundary=old.index(b"\n---\n",4)+5;tail=old[boundary:].decode();h1=re.match(r"\s*(# [^\n]+)\n",tail);assert h1
  candidate=old[:boundary]+("\n"+h1[1]+"\n\n"+body+"\n").encode();path=OUT/"candidatos"/r["path"];write(path,candidate,audit)
  backup=OUT/"backups"/(sha(old)+".md.gz");write(backup,gzip.compress(old,mtime=0),audit)
  missing="dpl-4555-" in r["path"];illegible=bool(re.search(r"ileg[ií]vel",html.unescape(re.sub("<[^>]+>"," ",fragment)),re.I))
  ledger.append({"path":r["path"],"candidato":str(path.relative_to(ROOT)),"sha256_antes":sha(old),"sha256_candidato":sha(candidate),"sha256_corpo_antes":r["sha256_corpo"],"sha256_corpo_candidato":sha(candidate.split(b"---",2)[2]),"headers_identicos":candidate[:boundary]==old[:boundary],"fonte":r["fonte_cache"],"sha256_fragmento":sha(fragment.encode()),"tabelas_fonte":r["tabelas_fonte"],"estrutura_celulas_span_texto_identicos":same,"sha256_assinatura_tabelas_fonte":sha(json.dumps(sig(fragment),ensure_ascii=False).encode()),"sha256_assinatura_tabelas_candidato":sha(json.dumps(sig(body),ensure_ascii=False).encode()),"backup":str(backup.relative_to(ROOT)),"anexo_externo_ausente":missing,"ilegivel_fonte":illegible,"vigencia_nao_corrigida_neste_ensaio":r["metadados"].get("revogada"),"estado":"retido_ate_revisao","aplicado":False})
 data="".join(json.dumps(r,ensure_ascii=False)+"\n" for r in ledger).encode();write(OUT/"ledger114.jsonl",data,audit)
 summary={"propostas":114,"assinatura_tabelas_identica":sum(x["estrutura_celulas_span_texto_identicos"] for x in ledger),"anexos_ausentes_retidos":sum(x["anexo_externo_ausente"] for x in ledger),"ilegivel_retido":sum(x["ilegivel_fonte"] for x in ledger),"core_sha256":CORE,"ledger_sha256":sha(data),"canonicos_alterados":0,"HTTP":0,"aprovacao_automatica":False};write(OUT/"resumo.json",(json.dumps(summary,ensure_ascii=False,indent=2)+"\n").encode(),audit);print(json.dumps(summary))
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--auditar",action="store_true");run(ap.parse_args().auditar)
