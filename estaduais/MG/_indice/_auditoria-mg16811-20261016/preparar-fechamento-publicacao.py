# coding: utf-8
import json, hashlib, gzip, subprocess, collections
from pathlib import Path
B=Path("estaduais/MG/_indice/_auditoria-mg16811-20261016")
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def ref(p):
 p=Path(p);return {"path":str(p),"sha256":sha(p.read_bytes()),"bytes":p.stat().st_size}
def git(*args):
 return subprocess.check_output(["rtk","proxy","git",*args])
head=git("rev-parse","HEAD").decode().strip()
headpaths=set(git("ls-tree","-r","--name-only",head,"--","estaduais/MG").decode().splitlines())
manifest=B/"manifesto-coorte-contextual-final-20261016.json"
m=json.loads(manifest.read_text())
assert sha(manifest.read_bytes())=="c57efc897516663c5454dc9b0deda3967acbd92bf08ee5b85a26da0f40e2ed20"
rows=[json.loads(l) for l in (B/"coorte-contextual-final-14691.jsonl").open()]
held={r["path"] for r in json.load((B/"retencoes-contextuais-finais-32.json").open())}
canon={r["path"] for r in rows}
assert len(rows)==len(canon)==14691 and len(held)==32 and not canon&held
present=sorted(canon&headpaths)
assert not present, ("canonical present HEAD",present[:10])
entries={}; failures=[]; checks=collections.Counter()
def add(path,role,expected=None,related=None,decompressed=None):
 p=Path(path);raw=p.read_bytes();actual=sha(raw)
 if expected and actual!=expected:failures.append({"path":str(p),"kind":"SHA","expected":expected,"actual":actual})
 if decompressed and sha(gzip.decompress(raw))!=decompressed:failures.append({"path":str(p),"kind":"decompressed_SHA"})
 e=entries.setdefault(str(p),dict(path=str(p),sha256=actual,bytes=len(raw),roles=[],canonical_paths=[]))
 if role not in e["roles"]:e["roles"].append(role)
 if related and related not in e["canonical_paths"]:e["canonical_paths"].append(related)
 checks[role]+=1
 return raw
for i,r in enumerate(rows,1):
 md=add(r["path"],"canonical_md",r["md_sha256"],r["path"])
 snap=add(r["snapshot"],"snapshot_md",r["md_sha256"],r["path"])
 assert md==snap
 add(r["snapshot_fonte"],"source_gzip_snapshot",r["source_gzip_sha256"],r["path"],r["source_sha256"])
 add(r["XML"]["snapshot"],"source_xml_gzip_snapshot",r["XML"]["gzip_sha256"],r["path"],r["XML"]["source_sha256"])
 if i%4000==0:print("verified",i,flush=True)
profile=json.load((B/"perfil-resumo.json").open())
for src,expected in profile["csv_sha256"].items():add(B/"snapshots-indice"/Path(src).name,"source_csv_snapshot",expected)
# Dependency closure of explicit frozen proof references only. Historical cohort
# manifests retain old held paths as evidence; they are not publication payloads.
proofs=set();pending=[manifest,B/"manifesto-coorte-proposta.json"]
def references(x):
 if isinstance(x,dict):
  if isinstance(x.get("path"),str) and isinstance(x.get("sha256"),str):yield x["path"],x["sha256"]
  for k,v in x.items():
   if k.endswith("_path") and isinstance(v,str) and k[:-5]+"_sha256" in x:yield v,x[k[:-5]+"_sha256"]
   yield from references(v)
 elif isinstance(x,list):
  for v in x:yield from references(v)
while pending:
 p=Path(pending.pop())
 if str(p) in proofs:continue
 proofs.add(str(p));raw=add(p,"proof")
 # Do not traverse JSONL document rows: those contain historical held paths.
 if p.suffix==".json":
  for path,expected in references(json.loads(raw)):
   q=Path(path)
   if str(q).startswith(str(B)):
    add(q,"proof",expected)
    if str(q) not in proofs:pending.append(q)
# Reproduction dependencies not encoded as path+hash in early reports.
for name in ["perfil-documentos.jsonl","retencoes-contextuais-manuais-23.json","prova-suplementar-dec35694-parte-suprimida.json","revisar-triagem-unificada-v5.py","revisar-eventos-manuais-v5.py","mostrar-fila-contextual.py","registrar-lote-contextual.py","auditar-perfil.py","auditar-gates-contexto-final.py","preparar-coorte.py","revisar-3565-contexto-v2.py","preparar-fechamento-publicacao.py"]:
 add(B/name,"reproduction_proof",profile["perfil_sha256"] if name=="perfil-documentos.jsonl" else None)
assert not failures,failures[:20]
assert not held&{p for p,e in entries.items() if "canonical_md" in e["roles"]}
head_initial=head
head=git("rev-parse","HEAD").decode().strip()
final_headpaths=set(git("ls-tree","-r","--name-only",head,"--","estaduais/MG").decode().splitlines())
assert not canon&final_headpaths,"canonical became present in final HEAD"
assert git("rev-parse","HEAD").decode().strip()==head,"HEAD changed during final tree lookup"
listing=B/"lista-publicacao-14691.jsonl";assert not listing.exists()
with listing.open("w") as o:
 for path in sorted(entries):o.write(json.dumps(entries[path],ensure_ascii=False)+"\n")
paths=B/"lista-publicacao-14691-paths.txt";assert not paths.exists();paths.write_text("".join(p+"\n" for p in sorted(entries)))
summary={"estado":"preparacao offline para revisao independente; sem aplicacao/Git de escrita/HTTP","HEAD":head,"HEAD_inicial":head_initial,"coorte_manifesto":ref(manifest),"coorte_canonicos":14691,"retidos_contextuais":32,"retidos_incluidos_payload":0,"canonicos_presentes_HEAD":0,"canonicos_ausentes_HEAD":14691,"HEAD_estavel_na_consulta_final":True,"HEAD_avancou_durante_hashes":head_initial!=head,"lista":ref(listing),"paths":ref(paths),"arquivos_unicos":len(entries),"bytes_total":sum(e["bytes"] for e in entries.values()),"contagem_papeis_unicos":dict(collections.Counter(role for e in entries.values() for role in e["roles"])),"falhas":failures,"esquema_lista":{"path":"caminho existente relativo ao repositorio; sem copia nova","sha256":"SHA256 dos bytes fisicos, inclusive gzip comprimido","bytes":"tamanho fisico","roles":"canonical_md/snapshot_md/source_gzip_snapshot/source_xml_gzip_snapshot/source_csv_snapshot/proof/reproduction_proof","canonical_paths":"normas da coorte relacionadas; vazio em prova global"},"limites":["Lista e fechamento sao proposta, nao aprovacao juridica/editorial nem aplicacao.","Provas historicas globais contêm identificadores e snapshots referidos de retidos; nenhum MD canonico/fonte/snapshot dos32 foi acrescentado como payload por essa referencia historica.","Mantidas fontes gzip/XML e snapshots existentes; nao duplicados os caches ativos identicos.","Tamanho total refere arquivos unicos listados; lista/manifesto de fechamento sao controle adicional, fora do proprio total para evitar autorreferencia.","AusenciaHEAD e verificada contra commit exato; raiz deve fixar ou reconferir HEAD antes de aplicar."]}
out=B/"manifesto-fechamento-publicacao-14691.json";assert not out.exists();out.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(ref(out)));print(json.dumps({k:summary[k] for k in ["HEAD","arquivos_unicos","bytes_total","contagem_papeis_unicos","canonicos_ausentes_HEAD"]}))
