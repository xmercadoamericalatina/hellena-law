from pathlib import Path
import json,hashlib,subprocess,shutil,datetime
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');D=B/'federal/_fonte/auditorias/producao-dec-rfb-20261016';O=D/'revisao-raiz-DEC1951'
sha=lambda b:hashlib.sha256(b).hexdigest()
git=lambda *a:subprocess.check_output(['rtk','proxy','git',*a],cwd=B).decode().strip()
head=git('rev-parse','HEAD');dedup=json.loads((O/'dedup-HEAD-raiz.json').read_text())
assert head==dedup['HEAD']=='f5b6edc42eddff0c0259f0caec8fdac2a566ce54'
assert dedup['canonicos_HEAD']==dedup['cabecalhos_extraidos']==156376 and not dedup['sem_cabecalho'] and not dedup['duplicatas']
assert not git('diff','--cached','--name-only')
qa=json.loads((O/'consolidacao-1951-raiz.json').read_text());assert qa['documentos']==1951
held={r['path'] for r in qa['contextos12'] if r['estado']=='retido'};assert len(held)==5
records={r['path']:r for r in map(json.loads,(O/'documentos1951-consolidados-raiz.jsonl').read_text().splitlines())}
inv={r['inventario']['path']:r['inventario'] for r in map(json.loads,(D/'coorte-DEC-2000/coorte2000.jsonl').read_text().splitlines())}
approved=set(records)-held;assert len(approved)==1946
envelope=json.loads((O/'envelope-coorte2000-v2-raiz.json').read_text());assert envelope['encoding_escolhido.legislationLegalValue']=={'"UnofficialLegalValue"':1951}
proofs={r['path'] for r in envelope['arquivos']}
proofs.update(str((D/n).relative_to(B)) for n in ('manifesto-final-DEC2000.json','overlay-contextual-DEC2000/manifesto-overlay.json','perfil-proveniencia-DEC2000.json'))
for name in ('ordinais1951-fontes','ordinais1951-fontes-segunda'):
 p=D/name/'manifesto.json';m=json.loads(p.read_text());proofs.add(str(p.relative_to(B)))
 for r in m['arquivos']:
  assert sha((B/r['path']).read_bytes())==r.get('SHA',r.get('sha256'));proofs.add(r['path'])
for name in ('consolidar-DEC1951-raiz.py','envelope-DEC2000-raiz.py','contexto-artigos-DEC1951-raiz.py','aprovar-DEC1946-raiz.py'):
 shutil.copyfile(Path('/tmp')/name,O/name)
payload=set(proofs);docs=[]
for p in sorted(approved):
 r=records[p];d=inv[p];assert not r['erros'] and r['sha256_MD']==d['sha256_MD']==sha((B/p).read_bytes())
 assert r['sha256_fonte']==d['sha256_fonte']
 for source,h in ((d['fonte_cache'],d['sha256_fonte_gzip']),(d['metadados_cache'],d['sha256_metadados_gzip'])):
  assert sha((B/source).read_bytes())==h;payload.add(source)
 payload.add(p);docs.append({'path':p,'sha256_MD':d['sha256_MD'],'sha256_corpo':d['sha256_corpo'],'sha256_fonte':d['sha256_fonte'],'fonte_cache':d['fonte_cache'],'metadados_cache':d['metadados_cache'],'URN':d['urn'],'numero':r['numero'],'data':r['data'],'revogada':r['revogada']})
approval={'estado':'APROVADO_RAIZ_PARA_PUBLICACAO_INCREMENTAL','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'HEAD_base':head,'novos_documentos':1946,'documentos':docs,'retidos5':sorted(held),'cobertura':'FonteHTML/metadata/indice oficial congelados, texto integral e seis mascaras de caracteres; GitHubGFM1951igual; dedup156376canonicosHEAD. Sete alertas resolvidos por leitura integral das citacoes/redacao, cinco recuperando fonte alternativa integral.','spans_NBSP':'5spans em4documentos,4assinaturas+1epigrafe. Semcolunas de dados.','versao':'Original pelo encodingAPI, legislationLegalValueUnofficialLegalValue. Nao certificado facsimile.','limites':qa['limites'],'recuperacao':'77443 retido por3perdas(Camara: membroBancoBrasil/Paragrafounico/GrupoVI).75906/77544/77620/78587 retidos por rotulos literais em recuperacao de outra fonte integral. Meta global100% inalterada.','provas_SHA256':{str(p.relative_to(B)):sha(p.read_bytes()) for p in (O/'consolidacao-1951-raiz.json',O/'dedup-HEAD-raiz.json',O/'envelope-coorte2000-v2-raiz.json',O/'GitHub/resumo-GitHub1951-raiz.json')}}
ap=O/'aprovacao-publicacao-DEC1946-raiz.json';ap.write_text(json.dumps(approval,ensure_ascii=False,indent=2)+'\n')
payload.update(str(p.relative_to(B)) for p in O.rglob('*') if p.is_file())
assert not held.intersection(payload)
canonical={p for p in payload if p.endswith('.md') and not any(part.startswith('_') for part in p.split('/'))};assert canonical==approved
ledger={'estado':'payload_conferido_disco_antes_stage','novos_documentos':1946,'HEAD_base':head,'arquivos':[{'path':p,'sha256':sha((B/p).read_bytes()),'bytes':(B/p).stat().st_size} for p in sorted(payload)]}
lp=O/'payload-publicacao-DEC1946-raiz.json';lp.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n');payload.add(str(lp.relative_to(B)));payload.add('WORKLOG.md')
Path('/tmp/DEC1946-publicacao-paths.txt').write_text('\n'.join(sorted(payload))+'\n')
Path('/tmp/DEC1946-commit.txt').write_text('Publica 1.946 decretos federais com fontes e revisão de integridade\n\nPreserva HTML e metadados originais; confere identidade, datas, formatação e duplicatas. Cinco casos seguem em recuperação de fonte integral.\n')
print(json.dumps({'aprovados':1946,'retidos':len(held),'payload_paths':len(payload),'bytes':sum(r['bytes'] for r in ledger['arquivos']),'aprovacao_SHA256':sha(ap.read_bytes())},ensure_ascii=False))
