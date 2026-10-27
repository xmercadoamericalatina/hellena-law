import json,hashlib,gzip,shutil,collections,concurrent.futures,os,tempfile
from pathlib import Path
base=Path('estaduais/MG/_indice/_auditoria-mg16811-20261016');sha=lambda b:hashlib.sha256(b).hexdigest();profile={r['path']:r for r in map(json.loads,(base/'perfil-documentos.jsonl').read_text().splitlines())};gates=[json.loads(x) for x in (base/'gates-contexto-documentos.jsonl').read_text().splitlines()];over={r['path']:r for r in map(json.loads,(base/'oracle-literal-prefixo421-overlay.jsonl').read_text().splitlines())};context={r['path']:r for r in map(json.loads,(base/'revisao-contextual-3565-sem-artigo-v2.jsonl').read_text().splitlines())};individual={r['path']:r for r in json.load(open(base/'revisao-individual-15-sem-comando.json'))['documentos']};refs={r['path']:r for r in json.load(open(base/'revisao-independente-8-remissoes.json'))['documentos']};records=[]
for row in gates:
 r=over.get(row['path'],row);r['oracle_fonte']='raw_literal_decodificado' if profile[r['path']]['formato']=='outrotextoUTF8' else 'HTMLParserindependente';r['classificacao_dispositivo_heuristica_ampla_original']=r.pop('classificacao_dispositivo')
 if r['path'] in context:r['revisao_contextual_sem_artigo']=context[r['path']]
 if r['path'] in individual:
  man=individual[r['path']];r['revisao_individual_sem_comando']=man
  if man['decisao'].startswith('reter'):r['retencoes'].append(man['decisao'])
  else:r['retencoes']=[x for x in r['retencoes'] if x!='dispositivo_nao_reconhecido_exige_contexto']
 if r['path'] in refs:
  r['revisao_remissao']=refs[r['path']]
  if refs[r['path']]['decisao'].startswith('reter'):r['retencoes'].append(refs[r['path']]['decisao'])
 r['retencoes']=sorted(set(r['retencoes']));records.append(r)
assert len(records)==16811 and len({r['path'] for r in records})==16811
final=base/'gates-finais-consolidados.jsonl';final.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records));ready=[r for r in records if not r['retencoes']];held=[r for r in records if r['retencoes']];(base/'retidos-prova-contextual.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in held))
def salvar(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.NamedTemporaryFile(dir=p.parent,delete=False) as f:f.write(b);tmp=f.name
 os.replace(tmp,p)
 assert sha(p.read_bytes())==sha(b)
for p,expected in json.load(open(base/'perfil-resumo.json'))['csv_sha256'].items():
 raw=Path(p).read_bytes();assert sha(raw)==expected;salvar(base/'snapshots-indice'/Path(p).name,raw)
def prepare(r):
 p=profile[r['path']];md=Path(r['path']).read_bytes();rawgz=Path(p['cache']).read_bytes();xml=Path(p['xml']['path']).read_bytes();assert sha(md)==r['md_sha256'];assert sha(rawgz)==r['source_gzip_sha256'];assert sha(gzip.decompress(xml))==p['xml']['sha256'];snapshot=base/'coorte'/ 'snapshots'/r['path'];font=base/'coorte'/'fontes'/p['cache'];xs=base/'coorte'/'xml'/Path(p['xml']['path']).name
 salvar(snapshot,md);salvar(font,rawgz);salvar(xs,xml)
 return dict(path=r['path'],estado='candidato_sem_mudanca_em_revisao',md_sha256=sha(md),header_sha256=p['header_sha256'],body_sha256=p['body_sha256'],snapshot=str(snapshot),candidato=str(snapshot),candidato_sha256=sha(md),fonte=p['fonte'],source_sha256=r['source_sha256'],source_gzip_sha256=r['source_gzip_sha256'],snapshot_fonte=str(font),XML=dict(path=p['xml']['path'],snapshot=str(xs),gzip_sha256=sha(xml),source_sha256=p['xml']['sha256'],identidade=p['xml']['matching_conteudo']),CSV=dict(path=p['indice_csv'],registro=p['indice_registro']),prova=r)
out=base/'coorte-preparada.jsonl';count=0
with out.open('w') as log,concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for count,r in enumerate(pool.map(prepare,ready),1):
  log.write(json.dumps(r,ensure_ascii=False)+'\n')
  if count%1000==0:log.flush();print('COORTEMG',count,'/',len(ready),flush=True)
summary=dict(estado='proposta offline sem aplicação/Git/HTTP; revisão raiz pendente',total_alvo=16811,coorte_sem_alertas=len(ready),retidos_pendentes=len(held),candidatos_modificados=0,coorte_path=str(out),coorte_sha256=sha(out.read_bytes()),gates_path=str(final),gates_sha256=sha(final.read_bytes()),retidos_path=str(base/'retidos-prova-contextual.jsonl'),retidos_sha256=sha((base/'retidos-prova-contextual.jsonl').read_bytes()),retencoes=dict(collections.Counter(x for r in held for x in r['retencoes'])),fontes_sem_tabelas_imagens_tachado=16811,oracle_texto_puro_literal=2292,oracle_HTML_independente=14519,sem_artigo_original=3565,contexto3565=json.load(open(base/'revisao-contextual-3565-resumo-v2.json')),remissoes8=dict(retencoes_reais=4,falsos_positivos=4),scripts=dict(core=sha(Path('scripts/html2md.py').read_bytes()),baseline95=sha(Path('/tmp/html2md-antes-tachado.py').read_bytes())),limites=['Esta coorte confere captura textual/identidade/datas daAPI e conservação de caracteres/tachado emGFM; não certifica diagramação original ou anexos externos.','A API pode fornecer quadros linearizados sem<table>; não inventamos células/associações ausentes dafonte textual.0tabelasHTML não significa inexistência dequadros na publicação original.','417gates deomissão/materialexterno incluem declarações anexo não digitado;884diferençasGFM incluem separadores/heading eprecisam contextopróprio, não são todas perdas normativas.','172datas/697fechos são gates heurísticos conservadores, não correções automáticas.','Meta16811preservada; pendências seguem como objetivo, não exclusão definitiva.'])
(base/'manifesto-coorte-proposta.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));(base/'coorte-paths.txt').write_text('\n'.join(r['path'] for r in ready)+'\n');print('FINALCOORTE',summary['coorte_sem_alertas'],summary['retidos_pendentes'],sha((base/'manifesto-coorte-proposta.json').read_bytes()))
