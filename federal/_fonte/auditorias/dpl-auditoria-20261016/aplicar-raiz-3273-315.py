from pathlib import Path
import json,hashlib,subprocess,shutil,datetime
B=Path('federal/_fonte/auditorias/dpl-auditoria-20261016');T=Path('federal/_fonte/auditorias/dpl-triestado3270-20261016');H=Path('federal/_fonte/auditorias/dpl-triestado315-head-20261016');sha=lambda b:hashlib.sha256(b).hexdigest()
assert not subprocess.check_output(['rtk','proxy','git','diff','--cached','--name-only']).strip()
proof=B/'verificacao-raiz-identidade-3273.jsonl';assert sha(proof.read_bytes())=='b1efb56f687738e02325cefd7e70691caf3e10b76cbb162a9603a05bbb84c582'
proof315=H/'verificacao-raiz-315.json';assert sha(proof315.read_bytes())=='ab8b0c27f6c2ef8c5521ba7ecf972534e85ee22aa87bd370e293005aa2facf12'
passed={r['path']:r for r in map(json.loads,proof.open())};ledgers={r['path_canonico']:r for r in map(json.loads,(T/'ledger3270.jsonl').open())};oldheads={r['path_canonico']:r for r in map(json.loads,(H/'ledger315.jsonl').open())};assert len(passed)==3273 and len(oldheads)==315 and not set(passed)&set(oldheads)
held={'federal/decretos-legislativos/1928/dpl-5488-1928-07-09.md','federal/decretos-legislativos/1928/dpl-5515-1928-08-13.md'};assert not held&set(passed)
entries=[];writes=[]
for path,r in passed.items():
 actual=Path(path).read_bytes();assert sha(actual)==r['sha256_antes']
 if path in ledgers:
  l=ledgers[path];new=Path(l['path_candidato']).read_bytes();assert sha(new)==r['sha256_depois'];writes.append((Path(path),new))
 else:new=actual;assert sha(new)==r['sha256_depois']
 entries.append({'path':path,'acao_publica':'A','acao_local':'M' if path in ledgers else 'inalterado','sha256_antes':sha(actual),'sha256_depois':sha(new)})
for path,l in oldheads.items():
 actual=Path(path).read_bytes();new=Path(l['path_candidato']).read_bytes();assert sha(actual)==l['sha256_antes'] and sha(new)==l['sha256_depois'];writes.append((Path(path),new));entries.append({'path':path,'acao_publica':'M','acao_local':'M','sha256_antes':sha(actual),'sha256_depois':sha(new)})
assert len(writes)==3583 and len(entries)==3588
for p,new in writes:
 tmp=p.with_name(p.name+'.root.tmp');tmp.write_bytes(new);tmp.replace(p)
for r in entries:assert sha(Path(r['path']).read_bytes())==r['sha256_depois']
report={'estado':'aplicado_raiz_aguarda_formato_commit_push','aplicado_em':datetime.datetime.now().isoformat(),'novos_publicos':3273,'metadata_only_ja_publicados':315,'triestado_total':3583,'sem_alteracao_novos':5,'documentos':entries,'provas':{'identidade_final':{'path':str(proof),'sha256':sha(proof.read_bytes())},'315':{'path':str(proof315),'sha256':sha(proof315.read_bytes())}},'retidos_adicionais':sorted(held),'limites':['Corrige revogada:false para null apenasquando fonte própria nãoasseguravigência; situação literalpreservada.','Dois documentos com ilegível foram retidos; demais115retidos/467pendências mantidos.','315jápublicados tiveram apenas metadata corrigida, nãoaprovadosnovamenteporintegralidadedocorpo.','Sem alteração de metas, scripts coletores, dados fonte ou históriaGit.']}
out=Path('federal/_publicacao_dpl3273_triestado315_20261016.json');assert not out.exists();out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
shutil.copyfile('/tmp/verificar-dpl-identidade-final-raiz.py',B/'verificar-raiz-identidade-final.py');shutil.copyfile('/tmp/aplicar-dpl3273-315-raiz.py',B/'aplicar-raiz-3273-315.py')
paths=[str(x) for directory in (B,T,H) for x in directory.rglob('*') if x.is_file()]+[r['path'] for r in entries]+['federal/_preparacao_dpl_20261016.json','federal/_preparacao_dpl_triestado3270_20261016.json','federal/_preparacao_dpl_triestado315_head_20261016.json','federal/_overlay_dpl_triestado_retencoes_20261016.json',str(out),'WORKLOG.md']
Path('/tmp/dpl3273-315-publicacao-paths.txt').write_text('\n'.join(dict.fromkeys(paths))+'\n');print('APLICADOS',len(writes),'mudanças;novos3273,315metadata;lista preparada',len(set(paths)),flush=True)
