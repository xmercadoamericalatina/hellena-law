import sys,json,gzip,hashlib,tempfile,importlib.util,types
from pathlib import Path
sys.path.insert(0,str(Path('scripts').resolve()))
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
r=load('scripts/baixar_rfb.py','r');old=load('/tmp/html2md-5f175-congelado.py','old');import html2md
out=[]
with tempfile.TemporaryDirectory() as tmp:
 for source in json.load(open('/tmp/consumidores-tabelas-rfb-binariohtml.json')):
  raw=gzip.decompress(Path(source['cache']).read_bytes());doc=json.loads(raw);r.convert=old.convert;b0=r.extrair(doc);r.convert=html2md.convert;b1=r.extrair(doc)
  for mode in ('GFM_antigo','HTML_igual','HTML_celula_alterada'):
   r.RAIZ=Path(tmp)/str(doc['idAto'])/mode;canonical=r.RAIZ/'canonico.md';canonical.parent.mkdir(parents=True);body=b0 if mode=='GFM_antigo' else b1
   if mode=='HTML_celula_alterada':
    import re
    body=re.sub(r'<(td|th)(?=[ >])',r'<\1 rowspan="2"',body,count=1)
   canonical.write_text('# Ato\n\n'+body);original=canonical.read_bytes();ident=r.identidade(doc);r.METAS.clear();r.DOU.clear();r.EQUIVALENTES.clear();r.METAS[canonical]={**ident,'orgao':'; '.join(ident['orgaos'])};r.EQUIVALENTES[r.assinatura(body)]=[canonical];url=r.CORPO+str(doc['idAto'])+'/visao/original';cache=r.RAIZ/'_fonte/sijut'/(hashlib.sha256(url.encode()).hexdigest()+'.json.gz');r.salvar(cache,gzip.compress(raw));noHTTP=types.SimpleNamespace(get=lambda *a,**k:(_ for _ in ()).throw(AssertionError('HTTP proibido')));item=dict(idAto=doc['idAto'],dataAto=ident['data'],anoAto=ident['data'][:4]);status=r.processar(noHTTP,item);assert status==('equivalente' if mode=='HTML_igual' else 'pendente_estrutura'),(mode,status);assert canonical.read_bytes()==original;assert not (r.RAIZ/item['anoAto']/('rfb-sijut-'+str(doc['idAto'])+'.md')).exists()
   if status=='pendente_estrutura':
    p=r.RAIZ/'_indice/sijut/pendencias-estrutura'/f"{doc['idAto']}.json";record=json.loads(p.read_text());assert record['bodycandidate_sha256']==hashlib.sha256(b1.encode()).hexdigest();assert record['source_sha256']==hashlib.sha256(raw).hexdigest();assert record['snapshot_canonico'].encode()==original;assert r.processar(noHTTP,item)==status
   out.append(dict(id=doc['idAto'],modo=mode,resultado=status,canonico_preservado=True,fonte_sha256=hashlib.sha256(raw).hexdigest()))
Path('/tmp/rfb-guarda-estrutural-provas.json').write_text(json.dumps(dict(script_sha256=hashlib.sha256(Path('scripts/baixar_rfb.py').read_bytes()).hexdigest(),casos=out,limite='GFM retido conservadoramente; mapeamento estrutural GFM não certificado.'),ensure_ascii=False,indent=2));print(out)
