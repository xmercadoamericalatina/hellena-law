from pathlib import Path
import json,hashlib,shutil,subprocess
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');D=B/'estaduais/_indice/_recuperacao-v2-20261016';O=D/'revisao-raiz-df11'
sha=lambda b:hashlib.sha256(b).hexdigest()
mp=D/'manifesto-df-dlg11.json';assert sha(mp.read_bytes())=='8096499071e6877e468dc6b544041fa7fef77571870d00ffa3658eb3a2e2cf0e'
m=json.loads(mp.read_text());rows={r['path']:r for r in m['documentos']};assert len(rows)==11
text=json.loads((O/'revisao-texto-mascaras11-raiz.json').read_text());render=json.loads((O/'verificacao-GFM-GitHub11-raiz.json').read_text());identity=json.loads((O/'identidade-indice-HEAD11-raiz.json').read_text())
assert len(text['atos'])==render['quantidade']==len(identity['documentos'])==11
assert render['GitHub_vs_GFM']=='texto/bold/italic/del/u/sup/sub/titulos/listas/tabelas iguais'
for r in text['atos']:
 assert r['SHA_candidato']==rows[r['path']]['new_sha256']
 assert r['texto_ledger_igual_HTML5'] and r['texto_GFM_igual_HTML5'] and r['mascaras_fonte_incluidas']
 assert r['texto_fonte_lido_integralmente_raiz']
for r in render['atos']:
 assert not r['formato_erros'] and not r['formato_avisos'] and r['sha256_candidato']==rows[r['path']]['new_sha256']
for r in identity['documentos']:assert r['SHA_candidato']==rows[r['path']]['new_sha256']
assert identity['registros11_exatos_primario_e925'] and identity['UIDs_ausentes_HEAD']
tree=subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD:estaduais/DF'],cwd=B).decode().strip();assert tree==identity['DF_tree_oid']
files=[]
for r in m['lista_publicacao_provas']:
 p=Path(r['path']);p=p if p.is_absolute() else B/p;b=p.read_bytes();assert sha(b)==r['sha256'] and len(b)==r['bytes'];files.append(str(p.relative_to(B)))
for r in rows.values():
 assert sha((B/r['path']).read_bytes())==r['old_sha256']
 assert sha((B/r['candidato']).read_bytes())==r['new_sha256']
shutil.copyfile('/tmp/fechar-DF11-raiz.py',O/'fechar-DF11-raiz.py')
approval={'estado':'APROVADO_RAIZ_SEM_APLICACAO_AINDA','novos_documentos':11,'DF_tree_base':tree,'documentos':list(rows.values()),'provas_SHA':{p.name:sha(p.read_bytes()) for p in (mp,O/'revisao-texto-mascaras11-raiz.json',O/'verificacao-GFM-GitHub11-raiz.json',O/'identidade-indice-HEAD11-raiz.json')},'limites':['Versao fonte capturada; Publicacao no indice nao prova edicao original.','SemRevogacaoExpressa mantida null; nao inferir vigencia.','58a61semdatafechopropria:naopreencher.61sustaPortariaexterna;66formula nao exige tabelaanexa.','Sem alegacao facsimile/identidadepixels. Fontes integrais lidas11, texto e mascaras+GitHubGFM conferidos.'],'arquivos_manifesto_conferidos':files}
(O/'aprovacao-DF11-raiz.json').write_text(json.dumps(approval,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'aprovados':11,'aplicados':False,'DF_tree_base':tree,'SHA_aprovacao':sha((O/'aprovacao-DF11-raiz.json').read_bytes())}))
