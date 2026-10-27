import json, hashlib, gzip, subprocess, pathlib, tempfile
B=pathlib.Path('/Volumes/ExternalSSD/GitHub/constituicao')
A=B/'federal/_fonte/auditorias/dpl13-quadros-visuais-20261016'
out=A/'revisao-raiz13'
sha=lambda b:hashlib.sha256(b).hexdigest()
m=json.loads((A/'manifesto-final13-v2.json').read_text())
checks=[]
for r in m['arquivos']:
 p=B/r['path']; b=p.read_bytes(); h=sha(b); mode='bytes_arquivo'
 if h!=r['sha256'] and p.suffix=='.gz':
  h=sha(gzip.decompress(b));mode='conteudo_descomprimido'
 assert h==r['sha256'],str(p)
 checks.append({'path':r['path'],'sha256_fisico':sha(b),'sha256_manifesto':h,'dominio_hash_manifesto':mode})
renders=[]
with tempfile.TemporaryDirectory(prefix='dpl13-raiz-') as td:
 for p in sorted((A/'atos').glob('*/paginas.json')):
  d=json.loads(p.read_text()); src=B/d['fonte_pdf']; assert sha(src.read_bytes())==d['fonte_pdf_sha256']
  for r in d['paginas']:
   page=r['pagina_PDF']; target=pathlib.Path(td)/f'{d["numero"]}-{page}'
   subprocess.run(['rtk','proxy','pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','2200','-png',str(src),str(target)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
   image=pathlib.Path(str(target)+'.png'); actual=sha(image.read_bytes()); expected=sha((B/r['PNG_path']).read_bytes())
   assert actual==expected,(d['numero'],page,actual,expected)
   renders.append({'numero':d['numero'],'pagina_PDF':page,'sha256_PNG':actual,'original_pdf_sha256':d['fonte_pdf_sha256']})
result={'estado':'fontes_e_renders_reproduzidos_nao_aprovacao_editorial','arquivos_manifesto':len(checks),'arquivos':checks,'paginas_originais_reproduzidas':len(renders),'renders':renders}
(out/'verificacao-fontes-renders-raiz.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'arquivos':len(checks),'paginas':len(renders),'resultado':'todos exatos'}))
