from pathlib import Path
import json,gzip,hashlib,sys,html,re,urllib.parse,collections
sys.path.insert(0,str(Path("scripts").resolve()));import baixar_camara as c
B=Path("federal/_fonte/auditorias/dpl-auditoria-20261016")
def sha(x):return hashlib.sha256(x).hexdigest()
rs=[json.loads(l) for l in (B/"inventario5409.jsonl").read_text().splitlines()];q={r["urn"]:r for r in json.loads(Path("federal/_indice/camara-dpl-pendencias/indice.json").read_text())["consultas"]}
for n,r in enumerate(rs,1):
 if not r["ultimo_terminal4876"]:continue
 md=r["metadados"];url=md.get("url_metadados");gate={"consulta_primaria_preservada":False,"link_proprio_texto":False,"versao_corresponde_link":False,"identidade_metadados":False}
 try:
  d=next(x for x in q.get(r["urn"],{}).get("documentos",[]) if x["url"]==url);gate["consulta_primaria_preservada"]=True
  info=c.identificar(d,"dpl");gate["identidade_metadados"]=(info["urn"]==r["urn"] and d["titulo"]==md["titulo"] and d["situacao"]==md["situacao"])
  p=c.CACHE/(sha(url.encode())+".html.gz");z=p.read_bytes();raw=gzip.decompress(z);dest=B/"snapshots"/(sha(z)+"-"+p.name)
  if not dest.exists():dest.write_bytes(z)
  r["metadados_cache"]={"path":str(p),"snapshot":str(dest),"sha256_arquivo":sha(z),"sha256_fonte_html":sha(raw),"url":url}
  links=[urllib.parse.urljoin(url,html.unescape(x)) for x in re.findall(r"href=[\"']([^\"']+)[\"']",raw.decode())];ident=c.id_camara(d)
  gate["link_proprio_texto"]=md["fonte"] in links and ("-"+ident+"-") in md["fonte"]
  gate["versao_corresponde_link"]=(md["versao_texto"]==("compilada" if "-normaatualizada-" in md["fonte"] else "original"))
 except Exception as e:gate["erro"]=str(e)
 r["gates_metadados"]=gate
 if not all(v is True for v in gate.values()):r["alertas"].append("metadados/link/versão precisam revisão")
 r["elegivel_proposta"]=bool(r.get("elegivel_proposta")) and all(v is True for v in gate.values())
 if n%500==0:print("META",n,flush=True)
(B/"inventario5409-com-gates.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in rs))
latest=[r for r in rs if r["ultimo_terminal4876"]];nonhead=[r for r in latest if not r["presente_head"]]
allowed=["vigência boolean sem situação explícita"]
ready=[r for r in rs if r["elegivel_proposta"]];metaonly=[r for r in nonhead if r["alertas"] and all(a in allowed for a in r["alertas"]) and all(v is True for v in r["gates_metadados"].values()) and not r["gates"]["formato"] and r["gates"].get("formula_legislativa")]
for label,rows in (("proposta-verificada",ready),("proposta-correcao-triestado",metaonly)):
 (B/(label+".json")).write_text(json.dumps([{"path":r["path"],"urn":r["urn"],"sha256_md":r["sha256_md"],"sha256_corpo":r["sha256_corpo"],"fonte":r.get("fonte_cache"),"metadados":r.get("metadados_cache"),"acao_proposta":"publicar_apos_revisao_root" if label=="proposta-verificada" else "corrigir_apenas_revogada_para_null_com_backup_antes_de_publicar"} for r in rows],ensure_ascii=False,indent=2)+"\n")
proof={"ultimo_terminal_encontrados":len(latest),"ultimo_terminal_ja_head":len(latest)-len(nonhead),"ultimo_terminal_fora_head":len(nonhead),"prontos_sem_alteracao":len(ready),"prontos_somente_apos_correcao_triestado":len(metaonly),"alertas_ultimo_terminal":dict(collections.Counter(a for r in latest for a in r["alertas"])),"gates_metadados":{k:sum(r["gates_metadados"].get(k) is True for r in latest) for k in ("consulta_primaria_preservada","link_proprio_texto","versao_corresponde_link","identidade_metadados")},"aplicados":0,"HTTP":0}
(B/"resumo-gates-metadados.json").write_text(json.dumps(proof,ensure_ascii=False,indent=2)+"\n");print(json.dumps(proof,ensure_ascii=False,indent=2),flush=True)
