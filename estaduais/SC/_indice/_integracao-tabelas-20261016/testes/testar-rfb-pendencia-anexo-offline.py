import sys,json,gzip,hashlib,tempfile,types,importlib.util
from pathlib import Path
sys.path.insert(0,str(Path('scripts').resolve()));import baixar_rfb as r
source=json.load(open('/tmp/consumidores-tabelas-rfb-binariohtml.json'))[0];raw=gzip.decompress(Path(source['cache']).read_bytes());doc=json.loads(raw);doc['outrosSegmentos'].append(dict(original=True,omitir=False,ordemSegmentoAto=999,textoIntegra='',arquivoBinario=dict(idTipoArquivo=6,idArquivoBinario=99999999)));raw=json.dumps(doc).encode()
with tempfile.TemporaryDirectory() as tmp:
 r.RAIZ=Path(tmp);id=doc['idAto'];url=r.CORPO+str(id)+'/visao/original';cache=r.RAIZ/'_fonte/sijut'/(hashlib.sha256(url.encode()).hexdigest()+'.json.gz');r.salvar(cache,gzip.compress(raw));canon=r.RAIZ/'canon.md';canon.write_text('canônico preservado');pend=r.RAIZ/'_indice/sijut/pendencias-estrutura'/f'{id}.json';r.salvar(pend,json.dumps(dict(sourcecache=str(cache.relative_to(r.RAIZ)),arquivo=canon.name,sourcecache_gzip_sha256=hashlib.sha256(cache.read_bytes()).hexdigest(),canonico_sha256=hashlib.sha256(canon.read_bytes()).hexdigest(),corpo_candidato='anterior',bodycandidate_sha256=hashlib.sha256(b'anterior').hexdigest(),scripts_sha256={})).encode());before=pend.read_bytes();calls=[];fake=types.SimpleNamespace(get=lambda *a,**k:calls.append(a))
 try:r.processar(fake,dict(idAto=id,anoAto='2024'))
 except ValueError as e:assert 'anexo ausente no cache' in str(e) and 'HTTP recusado' in str(e);error=str(e)
 else:raise AssertionError('anexo ausente deveria falhar')
 assert not calls and pend.read_bytes()==before and canon.read_text()=='canônico preservado';result=dict(script_sha256=hashlib.sha256(Path('scripts/baixar_rfb.py').read_bytes()).hexdigest(),fixture='docpendente com segmentoPDFtipo6 semcache; JSONreal acrescido do segmento sintético',chamadas_HTTP=0,erro=error,canonico_ledger_preservados=True);Path('/tmp/rfb-pendencia-anexo-offline-prova.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(result)
