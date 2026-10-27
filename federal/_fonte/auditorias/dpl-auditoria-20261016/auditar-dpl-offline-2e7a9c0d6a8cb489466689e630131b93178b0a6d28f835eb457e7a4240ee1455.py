import sys,json,re,gzip,hashlib,subprocess,datetime as dt,collections,html,ast
from pathlib import Path
sys.path.insert(0,str(Path("scripts").resolve()))
import baixar_camara as c,baixar_federal as f,auditar
BASE=Path("federal/_fonte/auditorias/dpl-auditoria-20261016");BASE.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def snapshot(p):
 b=p.read_bytes();h=sha(b);dest=BASE/"snapshots"/(h+"-"+p.name);dest.parent.mkdir(exist_ok=True)
 if not dest.exists():dest.write_bytes(b)
 return {"path":str(p),"sha256_arquivo":h,"snapshot":str(dest)}
def metadata(raw):
 d={}
 for l in raw.decode().split("---",2)[1].strip().splitlines():
  k,v=l.split(":",1);v=v.strip();d[k]=json.loads(v) if v.startswith('"') or v in ("true","false","null") else v
 return d
profile=[snapshot(Path(p)) for p in ("scripts/baixar_camara.py","scripts/baixar_federal.py","scripts/html2md.py","scripts/comum.py","scripts/datas.py","_log_dpl_camara_dirigido.txt","federal/_indice/camara-dpl-pendencias/indice.json","federal/_falhas_camara.jsonl","federal/_identidades_camara.json")]
pri=f.carregar_indice({"DPL-n"});byurn={f.montar(d)["urn"]:d for d in pri};bynorma={d["norma"]:f.montar(d)["urn"] for d in pri}
(BASE/"primario5831.json").write_text(json.dumps(pri,ensure_ascii=False)+"\n")
log=Path("_log_dpl_camara_dirigido.txt").read_text();oks=re.findall(r"^ok (DPL-\S+) ",log,re.M);latest=set(oks[-4876:]);errlines=re.findall(r"^erro (DPL-\S+) (.+)$",log,re.M)[-467:];assert len({n for n,e in errlines})==467
consultas=json.loads(Path("federal/_indice/camara-dpl-pendencias/indice.json").read_text())["consultas"];qbyurn={q["urn"]:q for q in consultas}
paths=sorted(Path("federal/decretos-legislativos").glob("*/dpl-*.md"));head=subprocess.check_output(["rtk","proxy","git","rev-parse","HEAD"],text=True).strip();lines=subprocess.check_output(["rtk","proxy","git","cat-file","--batch-check=%(objectname) %(objecttype) %(objectsize)"],input="".join(head+":"+str(p)+"\n" for p in paths),text=True).splitlines();headmap={str(p):l for p,l in zip(paths,lines)}
class Offline:
 def get(self,*a,**k):raise RuntimeError("HTTP proibido nesta auditoria")
def cache_url(url):
 ext=".pdf.gz" if url.lower().endswith(".pdf") else ".html.gz";p=c.CACHE/(sha(url.encode())+ext)
 if not p.exists():raise ValueError("cache ausente: "+url)
 raw=gzip.decompress(p.read_bytes());proof=snapshot(p);proof.update(sha256_fonte=sha(raw),url=url)
 return raw,proof
records=[];backup=BASE/"backup-md.jsonl.gz"
assert not backup.exists(),"backup já existe; não sobrescrever"
with gzip.open(backup,"wt",encoding="utf-8") as back:
 for n,p in enumerate(paths,1):
  raw=p.read_bytes();md=metadata(raw);body=raw.decode().split("---",2)[2];norm=next((d["norma"] for d in [byurn.get(md.get("urn"),{})] if "norma" in d),None);r={"path":str(p),"urn":md.get("urn"),"sha256_md":sha(raw),"sha256_corpo":sha(raw.split(b"---",2)[2]),"head_resultado":headmap[str(p)],"presente_head":not headmap[str(p)].endswith(" missing"),"ultimo_terminal4876":norm in latest,"metadados":md,"alertas":[],"gates":{}}
  back.write(json.dumps({"path":str(p),"sha256_md":sha(raw),"texto":raw.decode()},ensure_ascii=False)+"\n")
  r["gates"]["formato"]=auditar.validar(raw.decode(),str(p),dt.date(2026,10,16))[0]
  r["gates"]["primario"]=md.get("urn") in byurn
  if md.get("fonte","").startswith(("https://www2.camara.leg.br/","https://www.camara.leg.br/")):
   try:
    fonte,proof=cache_url(md["fonte"]);r["fonte_cache"]=proof
    if md["fonte"].endswith(".pdf"):text=c.corpo_pdf(Offline(),md["fonte"]);r["alertas"].append("PDF exige conferência visual/páginas")
    else:
     fragmento=c.corpo_norma(fonte.decode());r["sha256_fragmento_html"]=sha(fragmento.encode());text=c.convert(fragmento)
     r["visuais"]=re.findall(r"<(?:img|svg|canvas|object|embed|iframe|math)\b[^>]*>",fragmento,re.I)
     r["tabelas_fonte"]=len(re.findall(r"<table\b",fragmento,re.I));r["tabelas_md"]=body.count("<table")
     r["del_fonte"]=len(re.findall(r"<(?:del|s|strike)\b",fragmento,re.I))
     if r["visuais"]:r["alertas"].append("conteúdo visual exige revisão")
     if r["tabelas_fonte"]!=r["tabelas_md"]:r["alertas"].append("estrutura de tabela diverge da fonte")
    r["sha256_convertido_core_atual"]=sha(text.encode());stored=body.lstrip();stored=stored.split("\n\n",1)[1] if stored.startswith("# ") else stored;r["conversao_byte_identica"]=stored==text
    if not r["conversao_byte_identica"]:r["alertas"].append("conversão difere do core congelado atual")
    c.conferir_data_propria({"numero":md["numero"],"data":md["data"],"urn":md["urn"]},text,md["titulo"],"dpl");r["gates"]["identidade_fecho"]=True;r["gates"]["formula_legislativa"]=c.tipo_legislativo_comprovado(text)
    if not r["gates"]["formula_legislativa"]:r["alertas"].append("tipo legislativo não comprovado")
    normal=c.unicodedata.normalize("NFKD",text).encode("ascii","ignore").decode().lower();external=re.findall(r".{0,80}(?:inteiro teor|integra|anexo.{0,30}publicad[oa].{0,30}(?:separad|boletim)).{0,200}",normal);r["trechos_integralidade"]=external
    if external:r["alertas"].append("menção de integralidade exige revisão contextual")
    if md.get("revogada") is not None and md.get("situacao","").strip().lower() not in ("revogada","vigente","em vigor"):r["alertas"].append("vigência boolean sem situação explícita")
    r["formula_preambulo"]=text.split("**Art.",1)[0][:1800];r["fecho"]=text[-1800:]
   except Exception as e:r["alertas"].append(str(e))
  else:r["alertas"].append("outra fonte: separar auditoria Planalto/primária")
  r["elegivel_proposta"]=r["ultimo_terminal4876"] and not r["presente_head"] and not r["alertas"] and not r["gates"]["formato"] and r["gates"].get("primario") and r["gates"].get("formula_legislativa")
  records.append(r)
  if n%250==0:print("AUDIT",n,"/",len(paths),flush=True)
(BASE/"inventario5409.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in records))
print("MD_FIM",len(records),flush=True)
# As falhas são evidências de retenção; não se reinterpreta o tipo primário.
errors=[]
for norma,erro in errlines:
 urn=bynorma.get(norma);q=qbyurn.get(urn);matches=[r for r in records if r["urn"]==urn];r={"norma":norma,"urn":urn,"erro_terminal":erro,"consulta_cache":q,"documentos_atuais":[{"path":d["path"],"sha256_md":d["sha256_md"],"presente_head":d["presente_head"]} for d in matches],"classe":"resolvido_texto_presente" if matches else "tipo_legislativo_nao_comprovado" if "tipo legislativo" in erro else "data_fecho_ausente_ou_divergente" if "data própria" in erro else "busca_ambigua_ou_identidade_divergente" if "norma única" in erro else "http_fonte" if "HTTP" in erro else "indice_busca_vazia" if "busca vazia" in erro else "texto_ausente_ou_insuficiente"}
 if q:
  for d in q["documentos"]:
   try:
    info=c.identificar(d,"dpl")
    if info.get("urn")!=urn:continue
    meta,proof=cache_url(d["url"]);r["metadados_cache"]=proof
    links=[html.unescape(u) for u in re.findall(r"href=[\"']([^\"']+)[\"']",meta.decode())];ident=c.id_camara(d);links=[u for u in links if "-"+ident+"-" in u]
    candidatos=[(u,comp) for mark,comp in (("-normaatualizada-",True),("-publicacaooriginal-",False),("-textopublicacaooriginal-",False)) for ext in (".html",".pdf") for u in links if mark in u and u.lower().endswith(ext)]
    r["fontes_texto_cache"]=[]
    for u,comp in candidatos:
     url=c.urllib.parse.urljoin(d["url"],u)
     try:
      raw,prova=cache_url(url);r["fontes_texto_cache"].append(prova)
      if url.endswith(".pdf"):continue
      frag=c.corpo_norma(raw.decode());t=c.convert(frag);r["texto_diagnostico"]={"sha256_fragmento":sha(frag.encode()),"sha256_convertido":sha(t.encode()),"formula_legislativa":c.tipo_legislativo_comprovado(t),"inicio":t[:2200],"fecho":t[-1800:],"visuais":re.findall(r"<(?:img|svg|canvas|object|embed)\b[^>]*>",frag,re.I),"tabelas":len(re.findall(r"<table\b",frag,re.I)),"compilada":comp};break
     except Exception as e:r.setdefault("alertas_cache",[]).append(str(e))
   except Exception as e:r.setdefault("alertas_cache",[]).append(str(e))
 errors.append(r)
(BASE/"pendencias467.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in errors))
summary={"head":head,"indice_primario":len(pri),"consultas_dirigidas_preservadas":len(consultas),"log_ok_acumulados":len(set(oks)),"ultimo_terminal_ok":len(latest),"acervo_dpl":len(records),"acervo_head":sum(r["presente_head"] for r in records),"ultimo_terminal_presentes":sum(r["ultimo_terminal4876"] for r in records),"ultimo_terminal_ja_head":sum(r["ultimo_terminal4876"] and r["presente_head"] for r in records),"proposta_verificada":sum(bool(r["elegivel_proposta"]) for r in records),"alertas":dict(collections.Counter(a for r in records for a in r["alertas"])),"pendencias_classes":dict(collections.Counter(r["classe"] for r in errors)),"perfil":profile,"backup_md":snapshot(backup),"limites":["Não altera MD,script,Git nem consulta rede.","Decisão legislativa exige fórmula própria e identidade primária; conflitos retidos.","Alertas de íntegra são revisão contextual, não descarte automático."]}
(BASE/"resumo.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n");print(json.dumps({k:v for k,v in summary.items() if k not in ("perfil","alertas")},ensure_ascii=False,indent=2),flush=True)
