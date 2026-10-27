import sys,json,gzip,hashlib,tempfile,importlib.util,types
from pathlib import Path
sys.path.insert(0,str(Path('scripts').resolve()))
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
r=load('scripts/baixar_rfb.py','r');old=load('/tmp/html2md-5f175-congelado.py','old');import html2md

with tempfile.TemporaryDirectory() as tmp:
 r.RAIZ=Path(tmp);checks=[]
 for source in json.load(open('/tmp/consumidores-tabelas-rfb-binariohtml.json')):
  raw=gzip.decompress(Path(source['cache']).read_bytes());doc=json.loads(raw);r.convert=old.convert;body=r.extrair(doc);r.convert=html2md.convert;ident=r.identidade(doc);meta={k:v for k,v in ident.items() if k!='orgaos'};meta['orgao']='; '.join(ident['orgaos']);meta['revogada']=False;canonical=r.RAIZ/('canonico-'+str(doc['idAto'])+'.md');canonical.write_text('---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in meta.items())+'---\n# Ato\n\n'+body);checks.append((canonical,canonical.read_bytes()));url=r.CORPO+str(doc['idAto'])+'/visao/original';r.salvar(r.RAIZ/'_fonte/sijut'/(hashlib.sha256(url.encode()).hexdigest()+'.json.gz'),gzip.compress(raw));r.salvar(r.RAIZ/'_indice/sijut/equivalentes'/f"{doc['idAto']}.json",json.dumps(dict(id_rfb=doc['idAto'],fonte_api=url,arquivo=canonical.name)).encode())
 result=r.auditar_equivalencias();summary=json.loads((r.RAIZ/'_indice/sijut/auditoria-equivalencias.json').read_text());assert result==0 and summary['contagem']['pendentes_estrutura']==4 and summary['contagem']['confirmadas']==0;assert all(p.read_bytes()==b for p,b in checks);Path('/tmp/rfb-auditoria-guarda-estrutural-provas.json').write_text(json.dumps(dict(script_sha256=hashlib.sha256(Path('scripts/baixar_rfb.py').read_bytes()).hexdigest(),contagem=summary['contagem'],canonicos_preservados=4),ensure_ascii=False,indent=2))
