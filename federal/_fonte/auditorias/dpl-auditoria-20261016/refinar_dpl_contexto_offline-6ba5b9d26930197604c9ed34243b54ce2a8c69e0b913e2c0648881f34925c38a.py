from pathlib import Path
import json,re,gzip,hashlib,sys,collections
sys.path.insert(0,str(Path("scripts").resolve()));import baixar_camara as c
B=Path("federal/_fonte/auditorias/dpl-auditoria-20261016");rs=[json.loads(l) for l in (B/"inventario5409-com-gates.jsonl").read_text().splitlines()];revisoes=[]
for r in rs:
 trechos=r.get("trechos_integralidade",[])
 if trechos:
  real=any("tabellas explicativas foram publicadas na integra" in x for x in trechos)
  referencia=any("fica mantido, em seu inteiro teor" in x for x in trechos)
  if not real and not referencia:assert not any(re.search(r"\b(?:integra|inteiro teor)\b",x) for x in trechos)
  decisao="reter_tabelas_explicativas_externas" if real else "referencia_a_dispositivo_anterior_sem_remissao_externa" if referencia else "falso_positivo_lexico_integral_reintegracao"
  revisoes.append({"path":r["path"],"sha256_md":r["sha256_md"],"sha256_fonte":r.get("fonte_cache",{}).get("sha256_fonte"),"trechos_literais_normalizados":trechos,"decisao":decisao})
  if not real:r["alertas"].remove("menção de integralidade exige revisão contextual")
  else:r["alertas"].append("tabelas explicativas publicadas externamente: DOU12agosto1922/avulso")
 if any("fecho não comprova" in x for x in r["alertas"]):
  s=gzip.decompress(Path(r["fonte_cache"]["snapshot"]).read_bytes()).decode();fragmento=c.corpo_norma(s);flat=c.html.unescape(re.sub("<[^>]+>"," ",fragmento));flat=" ".join(flat.split());md=r["metadados"]
  c.conferir_data_propria({"numero":md["numero"],"data":md["data"],"urn":r["urn"]},flat,md["titulo"],"dpl")
  proof=[flat[max(0,m.start()-30):m.start()+190] for m in re.finditer(r"(?:Rio de Janeiro|Capital Federal),? \d",flat)]
  assert proof
  revisoes.append({"path":r["path"],"sha256_fonte":r["fonte_cache"]["sha256_fonte"],"decisao":"fecho_proprio_comprovado_textualmente_HTML_tabela_interrompe_regex_do_MD_atual","fechos_literais":proof,"gate_funcao_real":"conferir_data_propria passou sobre texto do mesmo HTML sem markup","retencao_tabela_preservada":True})
  r["alertas"]=[a for a in r["alertas"] if "fecho não comprova" not in a];r["gates"]["identidade_fecho"]=True;r["gates"]["formula_legislativa"]=c.tipo_legislativo_comprovado(flat)
 latest=r["ultimo_terminal4876"] and not r["presente_head"]
 gate=not r["gates"]["formato"] and r["gates"]["primario"] and r["gates"].get("identidade_fecho") and r["gates"].get("formula_legislativa") and all(v is True for v in r.get("gates_metadados",{}).values())
 r["coorte"]= "verificada_sem_alteracao" if latest and gate and not r["alertas"] else "verificada_corpo_pendente_triestado" if latest and gate and r["alertas"] and all(a=="vigência boolean sem situação explícita" for a in r["alertas"]) else "retido_revisao" if latest else "fora_da_coorte_ultimo_terminal_novo"
(B/"revisoes-contextuais.json").write_text(json.dumps(revisoes,ensure_ascii=False,indent=2)+"\n")
(B/"inventario5409-revisado.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in rs))
cohort={}
for label in ("verificada_sem_alteracao","verificada_corpo_pendente_triestado","retido_revisao"):
 rows=[r for r in rs if r["coorte"]==label];cohort[label]=len(rows)
 (B/("coorte-"+label+".json")).write_text(json.dumps([{"path":r["path"],"urn":r["urn"],"sha256_md":r["sha256_md"],"sha256_corpo":r["sha256_corpo"],"metadados":r.get("metadados_cache"),"fonte":r.get("fonte_cache"),"alertas":r["alertas"],"acao_proposta":"nenhuma_alteracao" if label=="verificada_sem_alteracao" else "metadata_only_revogada_null_apos_root_aprovar" if label=="verificada_corpo_pendente_triestado" else "reter_sem_aplicar"} for r in rows],ensure_ascii=False,indent=2)+"\n")
summary={"head_baseline":json.loads((B/"resumo.json").read_text())["head"],"coortes":cohort,"saldo_publico_aprovado":None,"integralidade_contextual":dict(collections.Counter(r["decisao"] for r in revisoes)),"pendencia_imagem":{"path":"federal/decretos-legislativos/1920/dpl-4182-1920-11-13.md","classificacao_visual":"brasao_da_Republica_sem_texto_normativo","sha256_png":"3b55666043cb13efec43565bf2815ca8e64de431f96564f09ae4d6ec65eb43f2","decisao":"aguarda_aprovacao_root_especifica_sem_allowlist_generica"},"alertas_coorte_retida":dict(collections.Counter(a for r in rs if r["coorte"]=="retido_revisao" for a in r["alertas"])),"limites":["Só proposição: nenhum MD,flag,conversão,scriptcoletor ou Git alterado.","Metas preservadas;4876éterminal,3390nãoHEADnobaseline.","Corpo verificado não implica vigência jurídica ou aprovação de publicação.","45documentos fora do catálogo primário exato separados; não reinterpretados.","467pendências primárias mantidas sem relaxar fórmula legislativa."]}
(B/"proposta-conservadora.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n");print(json.dumps(summary,ensure_ascii=False,indent=2))
