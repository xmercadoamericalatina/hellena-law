from pathlib import Path
import json,hashlib,subprocess,gzip,datetime,re
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');D=B/'estaduais/_indice/_recuperacao-v2-20261016';O=D/'revisao-raiz-df11'
sha=lambda b:hashlib.sha256(b).hexdigest()
git=lambda *a:subprocess.check_output(['rtk','proxy','git',*a],cwd=B)
small=D/'df-dlg11-indice-subconjunto.json';assert sha(small.read_bytes())=='373220baca3ea469ebc1aae39f410759446154f8778d21647962793dfd88fcfa'
selected=json.loads(small.read_text());want={r['ch_norma']:r for r in selected['registros']};assert len(want)==11
primary=B/selected['indice_path'];h=hashlib.sha256()
with primary.open('rb') as f:
 for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
assert h.hexdigest()==selected['indice_sha256']=='fd4d1652e2db6eb53fade3ebeb83d398fc0a3df9d563d748cdfd5533c52496c5'
dec=json.JSONDecoder();buf='';pos=0;first=True;found={};total=0;ended=False
with primary.open() as f:
 while not ended:
  buf=buf[pos:]+f.read(1024*1024);pos=0
  if first:assert buf.startswith('[');pos=1;first=False
  while True:
   while pos<len(buf) and buf[pos] in ' \r\n\t,':pos+=1
   if pos<len(buf) and buf[pos]==']':ended=True;break
   try:r,end=dec.raw_decode(buf,pos)
   except json.JSONDecodeError:break
   pos=end;total+=1;uid=r.get('ch_norma')
   if uid in want:assert uid not in found and r==want[uid];found[uid]=r
  assert len(buf)-pos<2*1024*1024
assert total==selected['total_indice']==106683 and set(found)==set(want)
wide=json.loads((D/'df-dlg925-indice-subconjunto.json').read_text());byuid={r['ch_norma']:r for r in wide['registros']};assert all(byuid[u]==r for u,r in want.items())
overlay=json.loads((D/'df11-overlay-indice-UID-selecao-v2.json').read_text());manifest=json.loads((D/'manifesto-df-dlg11.json').read_text());rows={r['path']:r for r in manifest['documentos']}
head=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD:estaduais/DF').decode().strip();assert tree==overlay['DF_tree_oid']=='5c8d81dbd24c14d50652b555663c6c84d57fb649'
mapfile=B/overlay['mapa'];assert sha(mapfile.read_bytes())==overlay['mapa_sha256'];mapping=json.loads(mapfile.read_text());assert mapping['DF_tree_oid']==tree
commands=['rtk','proxy','git','grep','-n','-e','^fonte:','HEAD','--',':(glob)estaduais/DF/**/*.md']
p=subprocess.Popen(commands,cwd=B,stdout=subprocess.PIPE,stderr=subprocess.PIPE);actual=[]
with gzip.open(O/'DF-HEAD-fontes-raiz.txt.gz','wb') as frozen:
 for line in p.stdout:
  frozen.write(line);m=re.match(r'HEAD:(.*?):(\d+):fonte:\s*(.*)',line.decode());assert m
  path,ln,value=m.groups()
  try:value=json.loads(value)
  except json.JSONDecodeError:value=value.strip()
  u=re.search(r'/sinj/Norma/([^/]+)',value,re.I)
  actual.append({'path':path,'linha':int(ln),'fonte':value,'UID':u[1] if u else None})
err=p.stderr.read();assert p.wait()==0,err
assert sorted(actual,key=lambda r:r['path'])==sorted(mapping['fontes'],key=lambda r:r['path'])
assert len(actual)==mapping['total']==65976 and not set(want).intersection(r['UID'] for r in actual)
results=[]
for ov in overlay['documentos']:
 d=rows[ov['path']];uid=ov['UID'];r=want[uid];candidate=(B/d['candidato']).read_bytes();assert sha(candidate)==d['new_sha256']
 fields={}
 for line in candidate.decode()[4:].split('\n---\n',1)[0].splitlines():
  k,v=line.split(':',1)
  try:fields[k]=json.loads(v)
  except json.JSONDecodeError:fields[k]=v.strip()
 chosen=(r.get('ar_atualizado') or {}).get('filename') or [x['ar_fonte']['filename'] for x in r['fontes'] if x.get('ar_fonte',{}).get('filename')][-1]
 assert chosen==ov['arquivo_selecionado_pelo_caller']
 assert fields['fonte']==f'https://www.sinj.df.gov.br/sinj/Norma/{uid}/{chosen}'
 assert fields['numero']==r['nr_norma'] and fields['data']==datetime.datetime.strptime(r['dt_assinatura'],'%d/%m/%Y').date().isoformat()
 assert r['nm_tipo_norma']=='Decreto Legislativo' and fields['tipo']=='Decreto Legislativo'
 assert fields['revogada'] is None and r['nm_situacao']=='Sem Revogação Expressa'
 assert fields['versao_texto']=='fonte capturada'
 assert sha((B/ov['cache_original']).read_bytes())==ov['cache_original_gzip_sha256']
 assert sha(gzip.decompress((B/ov['cache_original']).read_bytes()))==d['fonte_sha256']
 results.append({'path':d['path'],'UID':uid,'numero':fields['numero'],'data':fields['data'],'arquivo':chosen,'versao_texto':fields['versao_texto'],'revogada':None,'SHA_candidato':sha(candidate)})
result={'estado':'identidade_indice_selecao_HEAD_DF11_conferidos_sem_aplicacao','HEAD':head,'DF_tree_oid':tree,'indice_primario_total':total,'registros11_exatos_primario_e925':True,'fontes_HEAD_lidas':len(actual),'UIDs_ausentes_HEAD':True,'documentos':results,'limites':'Publicacao e categoria do cadastro; nao certifica originalidade/facsimile. Fonte capturada. SemRevogacaoExpressa nao implica vigencia positiva.'}
(O/'identidade-indice-HEAD11-raiz.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='documentos'},ensure_ascii=False))
