from pathlib import Path
import json,hashlib,subprocess,gzip,shutil
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');D=B/'estaduais/_indice/_recuperacao-v2-20261016';O=D/'revisao-raiz-df11'
sha=lambda b:hashlib.sha256(b).hexdigest()
git=lambda *a:subprocess.check_output(['rtk','proxy','git',*a],cwd=B)
assert not git('diff','--cached','--name-only').strip()
head=git('rev-parse','HEAD').decode().strip();assert head=='7abcccab19ed386a0fa3c0ba6f4c8af97e851e50'
assert git('branch','--show-current').decode().strip()=='main'
ap=O/'aprovacao-DF11-raiz.json';assert sha(ap.read_bytes())=='09f380cf47b337bd3e7213644cb830a67f85e6edbd63d8cef2e6e55c04906345'
a=json.loads(ap.read_text());assert git('rev-parse','HEAD:estaduais/DF').decode().strip()==a['DF_tree_base']=='5c8d81dbd24c14d50652b555663c6c84d57fb649'
mp=D/'manifesto-df-dlg11.json';m=json.loads(mp.read_text());assert sha(mp.read_bytes())=='8096499071e6877e468dc6b544041fa7fef77571870d00ffa3658eb3a2e2cf0e'
for name,h in a['provas_SHA'].items():
 p=mp if name==mp.name else O/name;assert sha(p.read_bytes())==h,name
payload={str(mp.relative_to(B))}
for r in m['lista_publicacao_provas']:
 p=Path(r['path']);p=p if p.is_absolute() else B/p;data=p.read_bytes();assert sha(data)==r['sha256'] and len(data)==r['bytes'];payload.add(str(p.relative_to(B)))
overlay=D/'df11-overlay-indice-UID-selecao-v2.json';assert sha(overlay.read_bytes())=='779d1db814229fbfa36c5ac3b1319a494ad6015e9a74ee9177e977a20eb7920f';v=json.loads(overlay.read_text());mapfile=B/v['mapa'];assert sha(mapfile.read_bytes())==v['mapa_sha256'];payload.add(str(mapfile.relative_to(B)))
payload.update(str(p.relative_to(B)) for p in D.glob('df11-overlay-indice-UID-selecao*.json'))
wide=D/'df-dlg925-indice-subconjunto.json';assert sha(wide.read_bytes())=='4d5f11f0d3fecfdb216d22fe4ced475dd82d5e7d52b2848e77f9a3840e88b576';payload.add(str(wide.relative_to(B)))
snapshot=O/'indice-SINJ-106683-fd4d1652.json.gz';hasher=hashlib.sha256();size=0
with (B/'estaduais/DF/_indice/sinj.json').open('rb') as src,snapshot.open('wb') as dest,gzip.GzipFile(filename='',mode='wb',fileobj=dest,mtime=0,compresslevel=6) as out:
 for chunk in iter(lambda:src.read(1024*1024),b''):hasher.update(chunk);size+=len(chunk);out.write(chunk)
assert hasher.hexdigest()=='fd4d1652e2db6eb53fade3ebeb83d398fc0a3df9d563d748cdfd5533c52496c5';assert snapshot.stat().st_size<100*1024*1024
prepared=[]
for r in a['documentos']:
 candidate=(B/r['candidato']).read_bytes();assert sha(candidate)==r['new_sha256'];assert sha((B/r['path']).read_bytes()) in (r['old_sha256'],r['new_sha256']);prepared.append((r,candidate))
for r,candidate in prepared:(B/r['path']).write_bytes(candidate);assert sha((B/r['path']).read_bytes())==r['new_sha256'];payload.add(r['path'])
shutil.copyfile('/tmp/preparar-publicacao-DF11-raiz.py',O/'preparar-publicacao-DF11-raiz.py')
application={'estado':'11aplicados_somente_candidatos_aprovados','HEAD_base':head,'DF_tree_base':a['DF_tree_base'],'documentos':[{'path':r['path'],'sha256':r['new_sha256'],'baseline_sha256':r['old_sha256']} for r,_ in prepared],'indice_primario_snapshot':{'path':str(snapshot.relative_to(B)),'raw_SHA256':hasher.hexdigest(),'raw_bytes':size,'gzip_SHA256':sha(snapshot.read_bytes()),'gzip_bytes':snapshot.stat().st_size,'registros':106683},'limite':'Sem nova inferencia/reconversao/HTTP; copias exatas dos11aprovados. Snapshots antigos integrais preservados. Nenhum outro canônico alterado.'}
(O/'aplicacao-DF11-raiz.json').write_text(json.dumps(application,ensure_ascii=False,indent=2)+'\n')
payload.update(str(p.relative_to(B)) for p in O.rglob('*') if p.is_file())
payload.add('federal/_fonte/auditorias/producao-dec-rfb-20261016/revisao-raiz-DEC1951/publicacao-confirmada-DEC1946-raiz.json')
assert {p for p in payload if p.startswith('estaduais/DF/') and p.endswith('.md')}=={r['path'] for r,_ in prepared}
ledger={'estado':'payload_disco_conferido_antes_stage','HEAD_base':head,'novos_documentos':11,'arquivos':[{'path':p,'sha256':sha((B/p).read_bytes()),'bytes':(B/p).stat().st_size} for p in sorted(payload)]}
lp=O/'payload-DF11-raiz.json';lp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n');payload.add(str(lp.relative_to(B)));payload.add('WORKLOG.md')
Path('/tmp/DF11-publicacao-paths.txt').write_text('\n'.join(sorted(payload))+'\n')
Path('/tmp/DF11-commit.txt').write_text('Publica 11 decretos legislativos do Distrito Federal\n\nPreserva fontes integrais e cadastro SINJ congelado; confere texto, formatação, identidade e ausência de duplicatas.\n')
p=B/'WORKLOG.md';s=p.read_text();note='''## DF11 aprovado e aplicado para publicação — 16/10/2026

-11cópias exatas doscandidatos aprovados SHA09f380cf47b337bd3e7213644cb830a67f85e6edbd63d8cef2e6e55c04906345:DLG56–66/1995,fontecapturada,revogada null. Normativos/rodapés conforme fonte integral lida11;sem inferir datas ausentes58–61. Baselinesintegrais preservados. Aplicação/provas em revisao-raiz-df11;lista/tmp/DF11-publicacao-paths.txt. HEADbase7ab,DFtree5c8d81dbd24c14d50652b555663c6c84d57fb649 confirmado;index estava vazio. Stage/auditoria/commit/pushpendentes.
-SINJ primário integral106683 agora comprimido e congelado na revisão raiz, rawSHAfd4d1652e2db6eb53fade3ebeb83d398fc0a3df9d563d748cdfd5533c52496c5, sem novoHTTP. Subsets11/925 e mapa65976fontesHEAD preservadosjuntoàs37provasoriginais/overlays/revisãoraiz. Não importar restante925 ou canônicos semaprovação. Publicação1946jáconfirmada719290docs;goal100%ativo.

''';p.write_text(s.replace('# Continuação da coleta\n\n','# Continuação da coleta\n\n'+note,1))
print(json.dumps({'aplicados':11,'paths':len(payload),'bytes_payload':sum(r['bytes'] for r in ledger['arquivos']),'SINJ_gzip_bytes':snapshot.stat().st_size},ensure_ascii=False))
