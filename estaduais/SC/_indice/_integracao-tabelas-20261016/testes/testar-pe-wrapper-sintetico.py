import sys,json,gzip,re,importlib.util,tempfile,types,hashlib,base64,urllib.parse,urllib.request
from pathlib import Path
sys.path.insert(0,str(Path('scripts').resolve()));import comum
urllib.request.urlopen=lambda *a,**k:(_ for _ in ()).throw(AssertionError('HTTP proibido no teste'))
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
old=load('/tmp/html2md-5f175-congelado.py','old');new=load('scripts/html2md.py','new');rj=load('scripts/estados/rj.py','rj_test');sc=load('scripts/estados/sc.py','sc_test');pe=load('scripts/estados/pe.py','pe_test')
sha=lambda b:hashlib.sha256(b).hexdigest()
def meta(path):
 s=Path(path).read_text().split('\n---\n',1)[0];out={}
 for ln in s.splitlines()[1:]:
  k,v=ln.split(':',1);v=v.strip()
  try:out[k]=json.loads(v)
  except:out[k]=v
 return out

rows=json.load(open('estaduais/_snapshot_coletas_20261016_visual_v2.json'))['publicaveis'];items={str(x['id']):x for x in json.load(open('estaduais/PE/_indice/lista.json'))};out=[]
with tempfile.TemporaryDirectory() as tmp:
 pe.RAIZ_ESTADUAIS=tmp
 for row in [x for x in rows if x['uf']=='PE']:
  original=gzip.decompress(Path(row['cache_original']).read_bytes())
  if b'<table' not in original.lower():continue
  ident=re.search(r'id(\d+)\.md$',row['path'])[1];it=items[ident];fragmento=original.decode('utf8');wrapper=('<html><body><div id="divTexto">'+fragmento+'</div></body></html>').encode('cp1252',errors='xmlcharrefreplace');pair=[]
  for conv in (old,new):
   comum.convert=conv.convert;cap={};pe.caminhos=lambda *a:(str(Path(tmp)/'nunca.md'),str(Path(tmp)/'fonte.gz'));pe.gravar=lambda md,fonte,raw,m,body:cap.update(meta=dict(m),raw_sha256=sha(raw),body_sha256=sha(body.encode()));pe.rede=types.SimpleNamespace(get=lambda *a,**k:(200,wrapper,'text/html; charset=windows-1252'));status=pe.processar(it);assert status[0]=='ok';assert cap['meta']['numero']==meta(row['path'])['numero'];assert cap['meta']['data']==pe.data_do_texto(old.convert(fragmento),numero=cap['meta']['numero']);pair.append(dict(status=status,captura=cap))
  assert pair[0]['captura']['meta']==pair[1]['captura']['meta'];out.append(dict(path=row['path'],natureza='fixture wrapper sintético divTexto válido; fragmento Word de cache oficial real; não é resposta HTTP real',fragmento_fonte_sha256=sha(original),wrapper_cp1252_sha256=sha(wrapper),antes=pair[0],depois=pair[1]))
  if len(out)==3:break
Path('/tmp/pe-processar-wrapper-sintetico.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print('PE fixture cp1252',len(out),'ok')
