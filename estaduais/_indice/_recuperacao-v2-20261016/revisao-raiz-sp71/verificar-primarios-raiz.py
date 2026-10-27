from pathlib import Path
import json,re,zipfile,xml.etree.ElementTree as ET,hashlib,subprocess
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');A=B/'estaduais/_indice/_recuperacao-v2-20261016';O=A/'revisao-raiz-sp71'
p=json.loads((A/'sp-dlg71-perfil.json').read_text());m=json.loads((A/'manifesto-sp-dlg70-versao-capturada.json').read_text());cfg={r['path_canonico']:r['candidato'] for r in m['documentos']};cfg[p['documentos'][0]['path']]=str((O/'dlg-705-2000-12-21-id5227.md').relative_to(B))
sha=lambda b:hashlib.sha256(b).hexdigest();zpath=B/'estaduais/SP/_indice/legislacao_normas.zip';assert sha(zpath.read_bytes())==p['indice_zip_sha256'];ids={r['indice_registro']['IdNorma'] for r in p['documentos']};index={};xmls=[]
with zipfile.ZipFile(zpath) as z:
 assert z.namelist()==['legislacao_normas.xml']
 with z.open('legislacao_normas.xml') as f:
  for _,e in ET.iterparse(f):
   if e.tag=='LegislacaoNorma':
    row={c.tag:c.text for c in e}
    if row.get('IdNorma') in ids:index.setdefault(row['IdNorma'],[]).append(row);xmls.append(ET.tostring(e,encoding='unicode'))
    e.clear()
assert len(index)==71
head=subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'],text=True,cwd=B).strip();rawpaths=subprocess.check_output(['rtk','proxy','git','ls-tree','-r','--name-only','HEAD','estaduais/SP'],cwd=B);hp=rawpaths.decode().splitlines();(O/'SP-paths-HEAD-raiz.txt').write_bytes(rawpaths)
months=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'];records=[]
for r in p['documentos']:
 ident=r['indice_registro']['IdNorma'];indices=index[ident];assert r['indice_registro'] in indices
 s=(B/cfg[r['path']]).read_text();header=s[4:].split('\n---\n',1)[0];fields={}
 for l in header.splitlines():
  k,v=l.split(':',1);v=v.strip()
  try:fields[k]=json.loads(v)
  except json.JSONDecodeError:fields[k]=v
 text=re.sub(r'\s+',' ',r['source_text']).strip();match=re.search(r'DECRETO\s+LEGISLATIVO\s+N[.°ºo\s]*([\d.]+)\s*,?\s*DE\s+(\d+)\s+DE\s+([A-ZÇ]+)\s+DE\s+(\d{4})',text[:500],re.I);assert match,r['path'];date=f'{int(match[4]):04}-{months.index(match[3].lower())+1:02}-{int(match[2]):02}';n=match[1].replace('.','')
 for idx in indices:
  assert n==fields['numero']==idx['Numero'];assert date==fields['data']==idx['Data'][:10];assert idx['IdTipo']=='28';assert idx['URLFicha'].endswith('/norma/'+ident)
 assert fields['tipo']=='Decreto Legislativo' and fields['uf']=='SP';assert fields['revogada'] is None and fields['versao_texto']=='fonte capturada';assert fields['fonte'].endswith('/norma/'+ident)
 close=re.search(r'Assembl[eé]ia Legislativa do Estado de São Paulo,\s*(?:aos\s+)?0?'+str(int(match[2]))+r'\s+de\s+'+match[3]+r'\s+de\s+'+match[4],text,re.I);assert close,r['path']
 duplicates=[x for x in hp if x==r['path'] or x.endswith('-id'+ident+'.md') or re.search('/decretos-legislativos/'+date[:4]+'/dlg-'+n+'-',x)];assert not duplicates,(r['path'],duplicates);assert re.search(r'(Presidente|Secret[áa]ri|VAZ DE LIMA|SIDNEY BERALDO)',text[close.end():],re.I),r['path']
 records.append({'path':r['path'],'IdNorma':ident,'numero':n,'data':date,'XML_registros':indices,'epigrafe':match.group(),'fecho':close.group(),'status':None,'versao':'fonte capturada','HEAD_duplicatas':duplicates,'leitura_integral_raiz':True})
(O/'selecao71-XML-raiz.xml').write_text('<RegistrosSelecionados>\n'+'\n'.join(xmls)+'\n</RegistrosSelecionados>\n')
out={'estado':'identidade_datas_tipo_status_e_dedup_conferidos_nao_aprovacao_render','HEAD':head,'SHA_indice_zip':p['indice_zip_sha256'],'indice_zip':str(zpath.relative_to(B)),'indice_zip_sera_preservado_publicacao':True,'quantidade':len(records),'registros_XML':len(xmls),'atos':records,'leitura_contextual':'Todos71comandos/fechos lidos; balanços/processos/contratos citados são objetos externos, não anexos próprios novos.','limites':['Versionamento jurídico indeterminado sem JSON seletor; rótulo fonte capturada','Overlay narrativo corrige716 e742, sem alterar normas','Índice contém repetições de IdNorma por relacionamento; todos os registros selecionados devem concordar em número/data/tipo/URL; não multiplicam atos','Flags fonte ainda em fechamento; nenhuma aplicação']}
(O/'verificacao-primarios71-raiz.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'quantidade':len(records),'registros_XML':len(xmls),'ZIP_SHA':p['indice_zip_sha256'],'HEAD':head,'duplicatas_HEAD':0}))
