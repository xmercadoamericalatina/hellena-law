"""Prepara candidatos isolados; não aplica aos MDs canônicos nem acessa rede."""
from pathlib import Path
import json,gzip,re,hashlib,html,argparse,datetime as dt,sys
ROOT=Path.cwd();B=ROOT/"federal/_fonte/auditorias/dpl-auditoria-20261016";OUT=ROOT/"federal/_fonte/auditorias/dpl-triestado315-head-20261016"
MANIFEST="d8c469c92a6a7b2a9ebad67fc6bcca22428767b14b76cdd508bd05912dc8aec2"
def sha(x):return hashlib.sha256(x).hexdigest()
def gravar(p,b,auditar):
 if auditar or p.exists():assert p.read_bytes()==b,"divergência/sobrescrita recusada: "+str(p)
 else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def preparar(auditar=False):
 assert sha((ROOT/"federal/_preparacao_dpl_20261016.json").read_bytes())==MANIFEST
 records=[json.loads(x) for x in (B/"inventario5409-revisado.jsonl").read_text().splitlines()]
 cohort=[r for r in records if r["presente_head"] and "vigência boolean sem situação explícita" in r["alertas"]];ready=[];assert len(cohort)==315
 OUT.mkdir(exist_ok=True);ledger=[]
 for r in cohort:
  path=Path(r["path"]);assert str(path).startswith("federal/decretos-legislativos/") and path.suffix==".md" and ".." not in path.parts
  old=(ROOT/path).read_bytes();assert sha(old)==r["sha256_md"]
  split=old.index(b"\n---\n",4);header=old[:split];match=re.search(rb"(?m)^revogada: false$",header);assert match and len(re.findall(rb"(?m)^revogada:",header))==1
  assert b'situacao: "N' in header and 'situacao: "Não consta revogação expressa"' in header.decode()
  u=r["metadados"]["url_metadados"];cache=ROOT/"federal/_fonte/camara"/(sha(u.encode())+".html.gz");packed=cache.read_bytes();sourcebytes=gzip.decompress(packed)
  snapshot=OUT/"fontes"/(sha(packed)+".html.gz");gravar(snapshot,packed,auditar)
  sourceplain=html.unescape(re.sub("<[^>]+>"," ",sourcebytes.decode()));literal="Não consta revogação expressa";i=sourceplain.find(literal);extra={"url":u,"cache":str(cache.relative_to(ROOT)),"snapshot":str(snapshot.relative_to(ROOT)),"sha256_gzip":sha(packed),"sha256_html":sha(sourcebytes)};assert i>=0
  backup=OUT/"backups"/(sha(old)+".md.gz");gravar(backup,gzip.compress(old,mtime=0),auditar)
  new=old[:match.start()]+b"revogada: null"+old[match.end():];assert new[:match.start()]+b"revogada: false"+new[match.start()+len(b"revogada: null"):] == old
  bodysha=sha(old.split(b"---",2)[2]);assert sha(new.split(b"---",2)[2])==bodysha==r["sha256_corpo"]
  target=OUT/"candidatos"/path;gravar(target,new,auditar)
  ledger.append({"path_canonico":str(path),"path_candidato":str(target.relative_to(ROOT)),"sha256_antes":sha(old),"sha256_depois":sha(new),"sha256_corpo_inalterado":bodysha,"delta_bytes":len(new)-len(old),"offset_byte_inicio":match.start(),"linha":old[:match.start()].count(b"\n")+1,"antes":"revogada: false","depois":"revogada: null","outros_headers_e_corpo_identicos":True,"situacao_fonte_literal":literal,"contexto_situacao_fonte":sourceplain[max(0,i-100):i+len(literal)+100],"metadados_fonte":r["metadados"],"fonte_situacao_adicional":extra,"texto_fonte":r["fonte_cache"],"backup_integral":str(backup.relative_to(ROOT)),"aplicado":False})
 for r in ready:assert sha((ROOT/r["path"]).read_bytes())==r["sha256_md"]
 data=("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in ledger)).encode();gravar(OUT/"ledger315.jsonl",data,auditar)
 manifest={"estado":"candidatos_isolados_sem_aplicar","manifesto_auditoria_sha256":MANIFEST,"candidatos_metadata_only":315,"documentos_sem_alteracao":ready,"coorte":"315 já presentes em HEAD no inventário ancorado","ledger":str((OUT/"ledger315.jsonl").relative_to(ROOT)),"sha256_ledger":sha(data),"backup_integral":str((B/"backup-md.jsonl.gz").relative_to(ROOT)),"retidos_preservados":115,"pendencias_primarias_preservadas":467,"fora_primario_preservados":45,"canônicos_alterados":0,"HTTP":0,"Git_mutacoes":0,"limites":["Somente revogada:false para null; nenhuma inferência de vigência.","Corpos e demais headers idênticos por byte; situação literal permanece.","Aplicação/publicação dependem de revisão raiz; não há comando de aplicar."]}
 gravar(OUT/"manifesto.json",(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n").encode(),auditar)
 return manifest
if __name__=="__main__":
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("--auditar",action="store_true");a=ap.parse_args();m=preparar(a.auditar);print(json.dumps({"candidatos":m["candidatos_metadata_only"],"sem_alteracao":len(m["documentos_sem_alteracao"]),"aplicados":0,"ledger_sha256":m["sha256_ledger"]},ensure_ascii=False))
