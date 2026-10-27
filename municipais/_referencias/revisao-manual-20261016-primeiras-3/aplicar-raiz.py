from pathlib import Path
import json,hashlib,gzip,re,subprocess,datetime,fcntl
B=Path('municipais/_indice/_revisoes-fila-offline/20261016-primeiras-3');S=Path('municipais/_referencias/revisao-manual-20261016-primeiras-3');S.mkdir(parents=True,exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest()
p=B/'overlay-travessoes/proposta.json';j=json.loads(p.read_text());assert sha(p.read_bytes())=='4ca49e37c561fd074d12e4b205c5049b55fbf9b57aae3be31368558d51b9486f'
for name,h in j['provas_compartilhadas'].items():assert sha((B/name).read_bytes())==h
for source in json.loads((B/'renders.json').read_text()):
 assert sha(Path(source['pdf']).read_bytes())==source['sha256_pdf']
 for pg in source['paginas']:assert sha(Path(pg['png']).read_bytes())==pg['sha256_png']
rows=[];writes=[]
for r in j['documentos']:
 orig=Path(r['candidato_original']).read_bytes();before=Path(r['candidato_corrigido']).read_bytes();overlay=Path(r['overlay']).read_bytes();assert sha(orig)==r['sha256_candidato_original'];assert sha(before)==r['sha256_antes_overlay'];assert sha(overlay)==r['sha256_overlay']
 patched=orig.decode()
 for c in r['correcoes']:assert patched.count(c['antes'])==c['ocorrencias'];patched=patched.replace(c['antes'],c['depois'])
 assert patched.encode()==before
 strip=lambda b:re.sub(rb'\s|\xe2\x80\x93',b'',b)
 assert strip(before)==strip(overlay) and before.count('–'.encode())==overlay.count('–'.encode())
 assert not re.search(r'^\s*–\s*$',overlay.decode(),re.M)
 dest=Path(r['destino']);actual=dest.read_bytes() if dest.exists() else None;assert (sha(actual) if actual is not None else None)==r['sha256_canonico_atual']
 git=subprocess.run(['rtk','proxy','git','cat-file','-e','HEAD:'+str(dest)],capture_output=True);assert git.returncode==128
 final=overlay.rstrip(b'\n')+b'\n';old=S/(r['codigo']+'-antes-canonico.md.gz') if actual is not None else None
 rows.append({'path':str(dest),'acao_worktree':r['acao'],'acao_publica':'A','sha256_antes_worktree':sha(actual) if actual is not None else None,'sha256_antes_HEAD':None,'sha256_depois':sha(final),'sha256_overlay_antes_EOF':sha(overlay),'snapshot_anterior_worktree':str(old) if old else None,'fonte_sha256':r['fonte_sha256'],'data_propria':r['data_propria'],'codigo':r['codigo']});writes.append((dest,final,old,actual))
ledgerp=Path('municipais/_reparos_colunas.json');oldledger=ledgerp.read_bytes();ledger=json.loads(oldledger)
for r,decision in zip(j['documentos'],rows):
 source=next(x for x in json.loads((B/'revisao.json').read_text())['documentos'] if x.get('codigo')==r['codigo']);snapdir=Path(source['snapshot']);pdf=next(snapdir.glob('1-*.pdf'));cache=next(snapdir.glob('3-*.json'))
 rec={'fonte':r['fonte'],'data_circulacao':r['data_publicacao'],'sha256_pdf':r['fonte_sha256'],'extrator':'geometria-colunas-v2','sha256_extrator':r['pipeline_original']['extrair_diario_municipal.py'],'sha256_classificador':r['pipeline_original']['baixar_municipal.py'],'pdf':str(pdf),'cache_metadados':str(cache),'manifesto':str(p),'sha256_manifesto':sha(p.read_bytes()),'destinos':[{'acao':'novo' if r['acao']=='A' else 'modificado','acao_publica':'novo','arquivo':r['destino'],'codigo':r['codigo'],'sha256':decision['sha256_depois'],'sha256_bloco':r['prova_bloco_original']['sha256_bloco'],'cobertura':None}],'snapshots':([{'arquivo_anterior':r['destino'],'snapshot':decision['snapshot_anterior_worktree'],'sha256':decision['sha256_antes_worktree']}] if decision['sha256_antes_worktree'] else []),'referencias_parciais':[],'revisao':{'arquivo':str(B/'revisao.json'),'sha256':sha((B/'revisao.json').read_bytes())},'correcoes_manuais':{'proposta':str(p),'sha256':sha(p.read_bytes()),'descricao':'Datas próprias e pontuação/cabeçalho conferidos nos três renders; newline final única. Não atribuir overlays ao extrator.'},'aplicado_em':datetime.datetime.now().isoformat()};rec['id']=sha(json.dumps(rec,sort_keys=True).encode());assert not any(x.get('id')==rec['id'] for x in ledger['reconciliacoes']);ledger['reconciliacoes'].append(rec)
# Every precondition validated; preserve and apply atomically per file.
(S/'ledger-antes.json.gz').write_bytes(gzip.compress(oldledger,mtime=0))
for dest,final,old,actual in writes:
 if old:old.write_bytes(gzip.compress(actual,mtime=0))
 dest.parent.mkdir(parents=True,exist_ok=True);tmp=dest.with_name(dest.name+'.root.tmp');tmp.write_bytes(final);tmp.replace(dest)
with ledgerp.with_suffix('.json.lock').open('a') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX);assert ledgerp.read_bytes()==oldledger;tmp=ledgerp.with_name(ledgerp.name+'.root.tmp');tmp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n');tmp.replace(ledgerp)
report={'estado':'aplicado_raiz_aguarda_commit','delta_worktree':{'A':1,'M':1,'D':0},'delta_publico':{'A':2,'M':0,'D':0},'documentos':rows,'verificacao':'Root releu três renders integrais, artigos1–4AM/1–9RJ, cifras/fechos/assinaturas/fronteiras e posição dos44travessões. Deltas reversíveis e hashes completos conferidos.','limites':['Não corrige extrator; causa yMin/dashes emdossiê; outros141MDs precisam auditoria própria.','Não inclui edital associativo AAM emManaus.','Não altera fila ou fingerprints dos scripts.','Única normalização adicional é remover linhas vazias extras noEOF doscanônicos; snapshots originais intactos.']}
(S/'aplicacao-raiz.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
paths=[str(x) for x in B.rglob('*') if x.is_file()]+[str(x) for x in S.rglob('*') if x.is_file()]+[r['destino'] for r in j['documentos']]+[str(ledgerp),'WORKLOG.md'];Path('/tmp/municipais2-publicacao-paths.txt').write_text('\n'.join(paths)+'\n');print('AplicadosA1/M1local;A2público,D0;arquivos',len(paths),'semstage/commit.')
