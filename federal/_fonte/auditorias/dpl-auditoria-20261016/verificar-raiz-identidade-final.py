from pathlib import Path
import json,gzip,hashlib,sys,re,datetime,html,subprocess
sys.path.insert(0,str(Path('scripts').resolve()));import baixar_camara as cam
B=Path('federal/_fonte/auditorias/dpl-auditoria-20261016');T=Path('federal/_fonte/auditorias/dpl-triestado3270-20261016');sha=lambda b:hashlib.sha256(b).hexdigest()
prior=[json.loads(x) for x in (B/'verificacao-raiz-3275.jsonl').open()];passed={r['path']:r for r in prior if not r['retencoes']};assert len(passed)==3273
primary={}
for r in json.loads((B/'primario5831.json').read_text()):
 date=datetime.datetime.strptime(r['dataassinatura'],'%d/%m/%Y').date().isoformat();num=str(r['numero']).replace('.','').lower()+('-'+r['complemento'].lower() if r.get('complemento') else '');primary['urn:lex:br:federal:decreto.legislativo:'+date+';'+num]=r
queries={q['urn']:q for q in json.loads(Path('federal/_indice/camara-dpl-pendencias/indice.json').read_text())['consultas']}
inventory={r['path']:r for r in map(json.loads,(B/'inventario5409-revisado.jsonl').open())};ledger={r['path_canonico']:r for r in map(json.loads,(T/'ledger3270.jsonl').open())}
rows=[];paths=list(passed)
head=subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'],text=True).strip();check=subprocess.check_output(['rtk','proxy','git','cat-file','--batch-check=%(objectname) %(objecttype) %(objectsize)'],input=''.join(head+':'+p+'\n' for p in paths),text=True).splitlines();assert len(check)==len(paths) and all(l.endswith(' missing') for l in check)
for n,path in enumerate(paths,1):
 r=inventory[path];md=r['metadados'];assert md['urn'] in primary;pr=primary[md['urn']];date=datetime.datetime.strptime(pr['dataassinatura'],'%d/%m/%Y').date().isoformat();assert date==md['data'] and (str(pr['numero']).replace('.','').lower()+('-'+pr['complemento'].lower() if pr.get('complemento') else ''))==md['numero'].lower()
 q=queries[md['urn']];ds=[d for d in q['documentos'] if d['url']==md['url_metadados']];assert len(ds)==1;d=ds[0];info=cam.identificar(d,'dpl');assert info['urn']==md['urn'] and d['titulo']==md['titulo'] and d['situacao']==md['situacao'] and info['numero']==md['numero'] and info['data']==md['data']
 old=Path(path).read_bytes();assert sha(old)==passed[path]['sha256_antes'];m=r['metadados_cache'];gz=Path(m['snapshot']).read_bytes();assert sha(gz)==m['sha256_arquivo'];raw=gzip.decompress(gz);assert sha(raw)==m['sha256_fonte_html'];s=raw.decode();links=[cam.urllib.parse.urljoin(m['url'],html.unescape(x)) for x in re.findall(r'href=["\']([^"\']+)["\']',s)]
 assert md['fonte'] in links and '-'+cam.id_camara(d)+'-' in md['fonte'];assert md['versao_texto']==('compilada' if '-normaatualizada-' in md['fonte'] else 'original')
 if path in ledger:
  l=ledger[path];new=Path(l['path_candidato']).read_bytes();assert sha(new)==passed[path]['sha256_depois'];literal='Não consta revogação expressa';assert md['situacao']==literal
  plain=html.unescape(re.sub('<[^>]+>',' ',s));pos=plain.find(literal)
  if pos<0:
   assert path=='federal/decretos-legislativos/1922/dpl-4492-1922-01-18.md';extra=json.loads((T/'evidencia-busca4492.json').read_text());data=gzip.decompress((T/'fonte-busca4492.html.gz').read_bytes());assert sha(data)==extra['sha256_fonte'];assert extra['documento_proprio_parser_real']['url']==m['url'] and extra['documento_proprio_parser_real']['situacao']==literal
  else:assert 'Situação:' in plain[max(0,pos-150):pos]
 else:new=old
 body=new.decode().split('\n---\n',1)[1].lstrip().split('\n\n',1)[1];cam.conferir_data_propria({'numero':md['numero'],'data':md['data'],'urn':md['urn']},body,md['titulo'],'dpl');assert cam.tipo_legislativo_comprovado(body)
 rows.append({'path':path,'sha256_antes':sha(old),'sha256_depois':sha(new),'urn':md['urn'],'numero':md['numero'],'data':md['data'],'versao_texto':md['versao_texto'],'fonte':md['fonte'],'metadata_url':m['url'],'metadata_sha256':sha(raw),'situacao_literal':md['situacao'],'identidade_indice_e_busca_proprios':True,'link_texto_proprio_e_versao':True,'tipo_legislativo_e_fecho_proprios':True,'ausente_HEAD':True})
 if n%500==0:print('IDENTIDADEDPL',n,flush=True)
out=B/'verificacao-raiz-identidade-3273.jsonl';out.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows));print('FINAL',len(rows),'HEAD',head,'SHA',sha(out.read_bytes()),flush=True)
