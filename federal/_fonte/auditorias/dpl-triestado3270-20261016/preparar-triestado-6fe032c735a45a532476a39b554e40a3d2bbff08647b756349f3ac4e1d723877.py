"""Prepara candidatos isolados; não aplica aos MDs canônicos nem acessa rede."""
from pathlib import Path
import json,gzip,re,hashlib,html,argparse,datetime as dt,sys
ROOT=Path.cwd();B=ROOT/"federal/_fonte/auditorias/dpl-auditoria-20261016";OUT=ROOT/"federal/_fonte/auditorias/dpl-triestado3270-20261016"
MANIFEST="d8c469c92a6a7b2a9ebad67fc6bcca22428767b14b76cdd508bd05912dc8aec2"
def sha(x):return hashlib.sha256(x).hexdigest()
def gravar(p,b,auditar):
 if auditar or p.exists():assert p.read_bytes()==b,"divergência/sobrescrita recusada: "+str(p)
 else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def preparar(auditar=False):
 assert sha((ROOT/"federal/_preparacao_dpl_20261016.json").read_bytes())==MANIFEST
 cohort=json.loads((B/"coorte-verificada_corpo_pendente_triestado.json").read_text());ready=json.loads((B/"coorte-verificada_sem_alteracao.json").read_text());assert len(cohort)==3270 and len(ready)==5
 OUT.mkdir(exist_ok=True);ledger=[]
 for r in cohort:
  path=Path(r["path"]);assert str(path).startswith("federal/decretos-legislativos/") and path.suffix==".md" and ".." not in path.parts
  old=(ROOT/path).read_bytes();assert sha(old)==r["sha256_md"]
  split=old.index(b"\n---\n",4);header=old[:split];match=re.search(rb"(?m)^revogada: false$",header);assert match and len(re.findall(rb"(?m)^revogada:",header))==1
  assert b'situacao: "N' in header and 'situacao: "Não consta revogação expressa"' in header.decode()
  source=Path(r["metadados"]["snapshot"]);sourcebytes=gzip.decompress(source.read_bytes());assert sha(sourcebytes)==r["metadados"]["sha256_fonte_html"]
  sourceplain=html.unescape(re.sub("<[^>]+>"," ",sourcebytes.decode()));literal="Não consta revogação expressa";i=sourceplain.find(literal);extra=None
  if i<0:
   assert str(path)=="federal/decretos-legislativos/1922/dpl-4492-1922-01-18.md"
   evidence=(OUT/"evidencia-busca4492.json").read_bytes();assert sha(evidence)=="1d6486253867823c6478a7a8e76a8e493306ca9ed738909af5844b7f3720b228";extra=json.loads(evidence)
   packed=(OUT/"fonte-busca4492.html.gz").read_bytes();assert sha(packed)==extra["sha256_gzip"];sourcebytes=gzip.decompress(packed);assert sha(sourcebytes)==extra["sha256_fonte"]
   assert extra["documento_proprio_parser_real"]["url"]==r["metadados"]["url"] and extra["documento_proprio_parser_real"]["situacao"]==literal
   sourceplain=html.unescape(re.sub("<[^>]+>"," ",sourcebytes.decode()));i=sourceplain.find(literal)
  assert i>=0
  new=old[:match.start()]+b"revogada: null"+old[match.end():];assert new[:match.start()]+b"revogada: false"+new[match.start()+len(b"revogada: null"):] == old
  bodysha=sha(old.split(b"---",2)[2]);assert sha(new.split(b"---",2)[2])==bodysha==r["sha256_corpo"]
  target=OUT/"candidatos"/path;gravar(target,new,auditar)
  ledger.append({"path_canonico":str(path),"path_candidato":str(target.relative_to(ROOT)),"sha256_antes":sha(old),"sha256_depois":sha(new),"sha256_corpo_inalterado":bodysha,"delta_bytes":len(new)-len(old),"offset_byte_inicio":match.start(),"linha":old[:match.start()].count(b"\n")+1,"antes":"revogada: false","depois":"revogada: null","outros_headers_e_corpo_identicos":True,"situacao_fonte_literal":literal,"contexto_situacao_fonte":sourceplain[max(0,i-100):i+len(literal)+100],"metadados_fonte":r["metadados"],"fonte_situacao_adicional":extra,"texto_fonte":r["fonte"],"backup_integral":str((B/"backup-md.jsonl.gz").relative_to(ROOT)),"aplicado":False})
 for r in ready:assert sha((ROOT/r["path"]).read_bytes())==r["sha256_md"]
 data=("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in ledger)).encode();gravar(OUT/"ledger3270.jsonl",data,auditar)
 manifest={"estado":"candidatos_isolados_sem_aplicar","manifesto_auditoria_sha256":MANIFEST,"candidatos_metadata_only":3270,"documentos_sem_alteracao":ready,"ledger":str((OUT/"ledger3270.jsonl").relative_to(ROOT)),"sha256_ledger":sha(data),"backup_integral":str((B/"backup-md.jsonl.gz").relative_to(ROOT)),"retidos_preservados":115,"pendencias_primarias_preservadas":467,"fora_primario_preservados":45,"canônicos_alterados":0,"HTTP":0,"Git_mutacoes":0,"limites":["Somente revogada:false para null; nenhuma inferência de vigência.","Corpos e demais headers idênticos por byte; situação literal permanece.","Aplicação/publicação dependem de revisão raiz; não há comando de aplicar."]}
 gravar(OUT/"manifesto.json",(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n").encode(),auditar)
 return manifest
if __name__=="__main__":
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("--auditar",action="store_true");a=ap.parse_args();m=preparar(a.auditar);print(json.dumps({"candidatos":m["candidatos_metadata_only"],"sem_alteracao":len(m["documentos_sem_alteracao"]),"aplicados":0,"ledger_sha256":m["sha256_ledger"]},ensure_ascii=False))
