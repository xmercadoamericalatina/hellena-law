import base64,collections,datetime,gzip,hashlib,json,re,unicodedata
from pathlib import Path
import html5lib
D=Path("federal/_fonte/auditorias/producao-dec-rfb-20261016");C=D/"coorte-DEC-2000";O=D/"overlay-contextual-DEC2000";O.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(s):return "".join(c for c in unicodedata.normalize("NFKD",s.casefold())if not unicodedata.combining(c))
def text(e):return re.sub(r"\s+"," ","".join(e.itertext())).strip()
months={m:i+1 for i,m in enumerate("janeiro fevereiro marco abril maio junho julho agosto setembro outubro novembro dezembro".split())}
records=[json.loads(l)for l in(C/"coorte2000.jsonl").open()];out=[];tags=collections.Counter();comments=collections.Counter();css=collections.defaultdict(collections.Counter)
with gzip.open(C/"backup-fontes.jsonl.gz","rt")as f:
 for row,line in zip(records,f):
  d=json.loads(line);r=row["inventario"];assert d["path"]==r["path"];raw=gzip.decompress(base64.b64decode(d["fonte_gzip_base64"]));assert sha(raw)==r["sha256_fonte"];source=raw.decode();parser=html5lib.HTMLParser(namespaceHTMLElements=False);tree=parser.parse(source);body=tree.find("body");ps=[text(e)for e in body.iter("p")if text(e)];reasons=[];alerts=[]
  closures=[]
  for i,p in enumerate(ps):
   n=norm(p);m=re.fullmatch(r"brasilia,?\s+(\d{1,2})(?:[ºo°])?\s+de\s+(\w+)\s+de\s+(\d{4})[;.,]\s*(.*)",n)
   if m:closures.append({"indice_p":i,"literal":p,"data":f"{m[3]}-{months.get(m[2],0):02d}-{int(m[1]):02d}","restante":m[4]})
  own=None
  if len(closures)==1:
   c=closures[0];tail=ps[c["indice_p"]+1:];before=ps[:c["indice_p"]];articles=[i for i,p in enumerate(before)if re.match(r"^art(?:igo)?[.\s]*[0-9úu]",norm(p))]
   checks={"data_identica":c["data"]==r["meta"]["data"],"formula_independencia_republica":bool(re.search(r"independencia.*republica",c["restante"])),"apos_articulado":bool(articles),"assinatura_presidencial_primeira":bool(tail)and norm(tail[0]).strip(" .")=="ernesto geisel","tail_so_nomes":bool(tail)and all(re.fullmatch(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .’'-]{4,120}",p)and len(p.split())>=2 for p in tail),"sem_bloco_post_assinatura":len(tail)<=8}
   if not all(checks.values()):reasons.append("fecho_terminal_assinatura_nao_comprovados_contextualmente")
   own={"fecho":c,"checagens":checks,"ultimo_artigo_e_contexto":before[max(0,articles[-1]-1):]if articles else before[-3:],"tail_integral":tail,"total_paragrafos":len(ps)}
  else:reasons.append("fecho_Brasilia_unico_nao_comprovado")
  links=[];objects=[];transforms=[];unknown=[];commentrows=[]
  for e in tree.iter():
   if not isinstance(e.tag,str):
    literal=e.text or "";typ="metadados_Office_condicionais"if re.fullmatch(r"\[if gte mso 9\]><xml><o:DocumentProperties>.*</o:DocumentProperties></xml><!\[endif\]",literal,re.S)else"outro_comentario";comments[typ]+=1;commentrows.append({"tipo":typ,"sha256":sha(literal.encode()),"literal":literal if typ!="metadados_Office_condicionais"else None})
    if typ!="metadados_Office_condicionais":reasons.append("comentario_nao_classificado")
    continue
   tags[e.tag]+=1
   if e.tag not in {"html","head","body","meta","title","style","div","p","span","br","a","b","i","strong","em","s","strike","del","sup","sub"}:unknown.append(e.tag)
   if e.tag in {"object","embed","img","svg","iframe","script","canvas","math","video","audio","form","input","textarea","button","select","link","base","template","noscript"}:objects.append({"tag":e.tag,"atributos":e.attrib})
   if e.tag=="a":links.append({"atributos":e.attrib,"literal":text(e)})
   for k,v in e.attrib.items():
    if k.lower().startswith("on")or k.lower()in {"hidden","src","srcset","data","background","poster","action","formaction"}:reasons.append("atributo_controle_midia_ou_oculto")
   style=e.attrib.get("style","")
   for pair in style.split(";"):
    if ":"not in pair:continue
    k,v=pair.split(":",1);k=k.strip().lower();v=v.strip().lower();css[k][v]+=1
    if k in {"text-transform","white-space","content","clip","clip-path","overflow","visibility","display","opacity","direction","unicode-bidi"}:
     transforms.append({"propriedade":k,"valor":v,"literal":text(e)})
     if k!="text-transform"and not(k=="display"and v=="inline-block"):reasons.append("controle_CSS_requer_revisao")
  if unknown:reasons.append("tags_fora_perfil")
  if objects:reasons.append("objeto_ou_controle_externo")
  for a in links:
   if re.search(r"anex|integra|quadro|tabela|mapa|planta|regulamento",norm(a["literal"])):reasons.append("link_possivel_conteudo_integrante")
  flat=text(body);markers=[]
  for pat in [r"\b(?:ileg[ií]vel|suprimid[oa]s?|omitid[oa]s?|vetad[oa]s?)\b",r"\[\s*(?:\.{3}|…)\s*\]|\(\s*(?:\.{3}|…)\s*\)",r"\b(?:anexo|anexa|anexos|anexas|apenso|apensa)\b"]:
   for m in re.finditer(pat,flat,re.I):markers.append(flat[max(0,m.start()-100):m.end()+150])
  if markers:reasons.append("marcador_omissao_ou_anexo_contextual")
  controls=[{"codigo":hex(ord(c)),"quantidade":source.count(c)}for c in set(source)if(ord(c)<32 and c not in "\t\r\n")or ord(c)in range(0x202a,0x202f)or ord(c)in range(0x2066,0x206a)]
  if controls:reasons.append("controle_textual")
  errors=[str(x)for x in parser.errors if x[1]not in {"expected-doctype-but-got-start-tag","expected-doctype-but-got-chars"}]
  if errors:reasons.append("HTML5_erros_estruturais")
  out.append({"path":r["path"],"sha256_MD":r["sha256_MD"],"sha256_fonte":r["sha256_fonte"],"cobertura":"HTML5 integral; fecho terminal/assinaturas/contexto, todos elementos/atributos/comentários/controles/links/markers. Triagem independente automática com contexto literal preservado; não equivale a leitura humana individual integral.","fecho_contexto":own,"fechos_candidatos":closures,"links":links,"objetos":objects,"tags_desconhecidas":unknown,"comentarios":commentrows,"CSS_exibicao":transforms,"marcadores":markers,"controles":controls,"erros_HTML5":errors,"retencoes":sorted(set(reasons))})
assert len(out)==2000
(O/"documentos.jsonl").write_text("".join(json.dumps(x,ensure_ascii=False)+"\n"for x in out));summary={"documentos":len(out),"retidos":sum(bool(x["retencoes"])for x in out),"motivos_sobrepostos":dict(collections.Counter(k for x in out for k in x["retencoes"])),"tags":dict(tags),"comentarios":dict(comments),"CSS":{k:dict(v)for k,v in css.items()},"conclusao":"Overlay de auditoria dos verificadores, sem promoção automática nem revisão humana integral2000; contexto literal de cada fecho/tail foi preservado. Datas de citações não são aceitas por simples regex: exige bloco terminal antes de assinatura presidencial explícita, anos independência/república e ausência de texto posterior além de nomes.","Git_HTTP_canonicos":False};(O/"resumo.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n");print(json.dumps(summary,ensure_ascii=False),flush=True)
