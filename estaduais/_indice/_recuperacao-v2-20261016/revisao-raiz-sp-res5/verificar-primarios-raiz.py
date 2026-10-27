from pathlib import Path
import json,re,zipfile,xml.etree.ElementTree as ET,hashlib,subprocess
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');A=B/'estaduais/_indice/_recuperacao-v2-20261016';O=A/'revisao-raiz-sp-res5'
p=json.loads((O/'perfil5-selecionado.json').read_text());m=json.loads((A/'manifesto-sp-res5-tachado.json').read_text());cfg=json.loads((O/'config5-raiz.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest();zpath=B/'estaduais/SP/_indice/legislacao_normas.zip';assert sha(zpath.read_bytes())==p['indice_zip_sha256'];ids={r['indice_registro']['IdNorma'] for r in p['documentos']};index={};xmls=[]
with zipfile.ZipFile(zpath) as z:
 assert z.namelist()==['legislacao_normas.xml']
 with z.open('legislacao_normas.xml') as f:
  for _,e in ET.iterparse(f):
   if e.tag=='LegislacaoNorma':
    row={c.tag:c.text for c in e}
    if row.get('IdNorma') in ids:index.setdefault(row['IdNorma'],[]).append(row);xmls.append(ET.tostring(e,encoding='unicode'))
    e.clear()
assert len(index)==5
head=subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'],text=True,cwd=B).strip();rawpaths=subprocess.check_output(['rtk','proxy','git','ls-tree','-r','--name-only','HEAD','estaduais/SP'],cwd=B);hp=rawpaths.decode().splitlines();(O/'SP-paths-HEAD-raiz.txt').write_bytes(rawpaths)
months=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'];records=[]
for r in p['documentos']:
 ident=r['indice_registro']['IdNorma'];indices=index[ident];assert r['indice_registro'] in indices
 s=(B/cfg[r['path']]).read_text();header=s[4:].split('\n---\n',1)[0];fields={}
 for l in header.splitlines():
  k,v=l.split(':',1);v=v.strip()
  try:fields[k]=json.loads(v)
  except json.JSONDecodeError:fields[k]=v
 text=re.sub(r'\s+',' ',r['source_text']).strip();match=re.search(r'RESOLUÇÃO\s*-?\s*(?:DA\s+)?ALESP\s+N[.°ºo\s]*([\d.]+)\s*,?\s*DE\s+(\d+)\s+DE\s+([A-ZÇ]+)\s+DE\s+(\d{4})',text[:500],re.I);assert match,r['path'];date=f'{int(match[4]):04}-{months.index(match[3].lower())+1:02}-{int(match[2]):02}';n=match[1].replace('.','')
 for idx in indices:
  assert n==fields['numero']==idx['Numero'];assert date==fields['data']==idx['Data'][:10];assert idx['IdTipo']=='19';assert idx['URLFicha'].endswith('/norma/'+ident)
 assert fields['tipo']=='Resolução' and fields['uf']=='SP';assert fields['revogada'] is None and fields['versao_texto']=='compilada (edição capturada)';assert fields['fonte'].endswith('/norma/'+ident)
 assert re.search(r'(?:Última atualização|Atualizada até)',text,re.I),r['path']
 close=re.search(r'Assembl[eé]ia Legislativa do Estado de São Paulo,\s*(?:aos|em)\s*(\d+)\s+de\s+(\w+)\s+de\s+(\d{4})',text,re.I);assert close,r['path']
 close_date=f'{int(close[3]):04}-{months.index(close[2].lower())+1:02}-{int(close[1]):02}'
 if n=='808':assert date=='2000-10-18' and close_date=='2000-05-03'
 else:assert close_date==date,(r['path'],date,close_date)
 duplicates=[x for x in hp if x==r['path'] or x.endswith('-id'+ident+'.md') or re.search('/resolucoes/'+date[:4]+'/res-alesp-'+n+'-',x)];assert not duplicates,(r['path'],duplicates);assert re.search(r'(Presidente|Secret[áa]ri|VAZ DE LIMA|SIDNEY BERALDO)',text[close.end():],re.I),r['path']
 records.append({'path':r['path'],'IdNorma':ident,'numero':n,'data':date,'XML_registros':indices,'epigrafe':match.group(),'fecho':close.group(),'status':None,'versao':'compilada (edição capturada)','data_fecho_literal':close_date,'divergencia_autoral_808':n=='808','HEAD_duplicatas':duplicates,'leitura_integral_raiz':True})
(O/'selecao5-XML-raiz.xml').write_text('<RegistrosSelecionados>\n'+'\n'.join(xmls)+'\n</RegistrosSelecionados>\n')
out={'estado':'identidade_datas_tipo_status_e_dedup_conferidos_nao_aprovacao_render','HEAD':head,'SHA_indice_zip':p['indice_zip_sha256'],'indice_zip':str(zpath.relative_to(B)),'indice_zip_sera_preservado_publicacao':True,'quantidade':len(records),'registros_XML':len(xmls),'atos':records,'leitura_contextual':'Todos5corpos primarios lidos integralmente, incluindo redacoes antigas tachadas e notas de alteracao.808preserva epigrafe18outubro e fecho03maio, sem normalizar. Relatorios/estatutos/contas citados sao objetos externos e nao anexos proprios declarados ausentes.','limites':['Compilacao expressa no HTML capturado, sem afirmar versao corrente posterior ou vigencia juridica','Índice contém repetições de IdNorma por relacionamento; todos os registros selecionados devem concordar em número/data/tipo/URL; não multiplicam atos','Flags e GitHub verificados separadamente; nenhuma aplicacao neste helper']}
(O/'verificacao-primarios5-raiz.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'quantidade':len(records),'registros_XML':len(xmls),'ZIP_SHA':p['indice_zip_sha256'],'HEAD':head,'duplicatas_HEAD':0}))
