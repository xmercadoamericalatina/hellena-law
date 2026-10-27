"""Coleta e valida lotes federais explícitos, preservando área de trabalho e originais."""
import sys,os,json,gzip,hashlib,threading,shutil,datetime,re,argparse,fcntl
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,str(Path(__file__).resolve().parent));import baixar_federal as f;import preparar_lote_decretos_cache as v;import auditar
from identidade_decreto import extrair_epigrafe_decreto,numero_normalizado
parser=argparse.ArgumentParser(description="Coleta lotes explícitos e retomáveis de decretos com área de validação e promoção controlada, sem Git.")
parser.add_argument('--entrada',required=True)
parser.add_argument('--lote',required=True)
parser.add_argument('--rps',type=float,default=4)
parser.add_argument('--workers',type=int,default=4)
parser.add_argument('--repetir-pendentes',action='store_true',help='Reconsulta pendentes de execução interrompida; resultados concluídos permanecem imutáveis')
args=parser.parse_args()
if not 0<args.rps<=4 or not 1<=args.workers<=8:parser.error('Taxa/concorrência fora dos limites')
if not re.fullmatch(r'[a-z0-9_]+',args.lote):parser.error('Identificador de lote inválido')
BASE=Path(f.RAIZ);ROOT=BASE.parent;LOTE=args.lote;CACHE=BASE/'_fonte/auditorias'/LOTE;CACHE.mkdir(parents=True,exist_ok=True)
_run_lock=(CACHE/'run.lock').open('a')
try:fcntl.flock(_run_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
except BlockingIOError:parser.error('Já existe processo vivo neste lote; não duplicar coleta')
def atomic_bytes(path,raw):
 tmp=Path(str(path)+'.tmp');tmp.write_bytes(raw);tmp.replace(path)
def atomic_json(path,value):atomic_bytes(path,json.dumps(value,ensure_ascii=False,indent=2).encode())
source=json.loads(Path(args.entrada).read_text());inputpath=CACHE/'candidatos.json'
if inputpath.exists():
 if json.loads(inputpath.read_text())!=source:parser.error('Entrada diverge do snapshot imutável deste lote')
else:atomic_json(inputpath,source)
manifest_final=BASE/('_'+LOTE+'.json')
if manifest_final.exists():
 finalized=json.loads(manifest_final.read_text());lista=Path('/tmp/'+LOTE+'-publicar-paths.txt')
 if not lista.exists():atomic_bytes(lista,('\n'.join(r['path'] for r in finalized['publicaveis'])+'\n'+str(manifest_final.relative_to(ROOT))+'\n').encode())
 print('LOTE JÁ FINALIZADO, sem novo HTTP:',manifest_final,flush=True);_run_lock.close();sys.exit(0)
previous_path=CACHE/'coleta.json';previous={r['path']:r for r in json.loads(previous_path.read_text()).get('registros',[])} if previous_path.exists() else {}
f.RAIZ=str(CACHE/'work');f.LIMITE=f.Limitador(args.rps);stop=threading.Event();original_get=f.http_get

def get(*a,**k):
 if stop.is_set():raise RuntimeError('Coleta suspensa por recusa da fonte; nenhum novo HTTP')
 try:return original_get(*a,**k)
 except Exception as e:
  if re.search(r'HTTP (?:401|403|429)',str(e)):stop.set()
  raise
f.http_get=get

def worker(r):
 prior=previous.get(r['path'])
 if prior and prior['status'] not in {'ok','pulado'} and not args.repetir_pendentes:return prior
 if stop.is_set():return {**r,'status':'nao_tentado_bloqueio'}
 try:
  status,slug,extra=f.processar(r['indice']);status='ok' if status=='pulado' else status;return {**r,'status':status,'detalhe':extra}
 except Exception as e:return {**r,'status':'erro','detalhe':str(e)}
records=[]
with ThreadPoolExecutor(args.workers) as ex:
 fs=[ex.submit(worker,r) for r in source]
 for fu in as_completed(fs):
  records.append(fu.result())
  if len(records)%20==0 or len(records)==len(source):
   atomic_json(CACHE/'coleta.json',{'rps':args.rps,'limite_snapshot':len(source),'registros':records});print('COLETA',len(records),'/',len(source),'ok',sum(r['status']=='ok' for r in records),'bloqueio',stop.is_set(),flush=True)
f.RAIZ=str(BASE);public=[];ret=[]
for r in records:
 if r['status']!='ok':ret.append(r);continue
 try:
  d=r['indice'];info=f.montar(d);staged=CACHE/'work'/Path(r['path']).relative_to('federal');raw=staged.read_bytes();field,cab,body=v.fields(raw.decode());corpo=body.split('\n',2)[2];ep=extrair_epigrafe_decreto(corpo)
  assert ep and ep['numero']==numero_normalizado(f.numero_oficial(d)) and ep['data']==info['data'],'Epígrafe inconclusiva/divergente'
  assert not f.motivo_texto_parcial_decreto('DEC-n',corpo)
  src=CACHE/'work/_fonte'/Path(r['path']).relative_to('federal');src=src.with_suffix('.html.gz');htmlraw=gzip.decompress(src.read_bytes());html=htmlraw.decode('utf8');sv,sp=v.visible(html);mv,mp=v.visible(corpo,True);assert sv==mv,'Texto visível difere';assert sp.structure==mp.structure,'Tabela difere';assert not sp.visual,'Conteúdo visual';errors,warnings=auditar.validar(raw.decode(),r['path'],datetime.date.today());assert not errors and not warnings,(errors,warnings)
  assert not v.anexo_proprio_ausente(corpo,sp),'Anexo próprio ausente do HTML'
  msha=field['sha256_metadados_fonte'];metap=CACHE/'work/_fonte/metadados-normas'/hashlib.sha256(info['urn'].encode()).hexdigest()/(msha+'.json.gz');metaraw=gzip.decompress(metap.read_bytes());meta=json.loads(metaraw);assert meta.get('legislationDate')==info['data'] and meta.get('legislationType') in {'Decreto Numerado','Decreto'},'Data/tipo dos metadados divergem do índice';assert hashlib.sha256(metaraw).hexdigest()==msha and meta['legislationIdentifier']==info['urn'];capture=f.registrar_metadados(info['urn'],metaraw)
  target=ROOT/r['path'];backup=CACHE/(staged.name+'.anterior.md.gz')
  old=gzip.decompress(backup.read_bytes()) if backup.exists() else target.read_bytes() if r.get('preexistente') and target.exists() else None
  if old is not None and not backup.exists():atomic_bytes(backup,gzip.compress(old))
  dstsource=Path(info['fonte'])
  sourcebackup=CACHE/(staged.name+'.anterior.html.gz')
  if dstsource.exists() and not sourcebackup.exists():atomic_bytes(sourcebackup,dstsource.read_bytes())
  dstsource.parent.mkdir(parents=True,exist_ok=True);atomic_bytes(dstsource,src.read_bytes());target.parent.mkdir(parents=True,exist_ok=True);atomic_bytes(target,raw)
  public.append({'path':r['path'],'preexistente':r.get('preexistente',False),'origem':'Recuperação nova pela API oficial; versão Current ou Original preferida, fonte anterior preservada.','urn':info['urn'],'fonte':field['fonte'],'url_texto':f.escolher_texto(meta)['contentUrl'],'sha256':hashlib.sha256(raw).hexdigest(),'sha256_anterior':hashlib.sha256(old).hexdigest() if old is not None else None,'sha256_fonte_html':hashlib.sha256(htmlraw).hexdigest(),'sha256_metadados':msha,'captura_metadados':str(Path(capture['path']).relative_to(ROOT)),'epigrafe':ep,'tabelas':sum(x[0]=='table' for x in sp.structure),'checks':{'artigos_proprios':True,'sem_retificacao_avulsa':True,'indice_urn_numero_data':True,'texto_visivel_integral':True,'estrutura_tabelas':True,'sem_imagens':True,'formato_datas':True}})
 except Exception as e:r['status']='retido_validacao';r['detalhe']=str(e);ret.append(r)
result={'lote':LOTE,'origem':'Lote explícito de índice oficial; consulta de metadados e íntegra em normas.leg.br, sem alias conhecido. Candidatos e resultados preservados.','publicaveis':public,'retidos':ret,'resumo':{'candidatos':len(source),'publicaveis':len(public),'retidos':len(ret),'bloqueio':stop.is_set()},'limite_integralidade':'Conteúdo integral disponível no HTML oficial; anexos citados mas ausentes da própria fonte exigem verificação específica.'}
assert len(public)+len(ret)==len(source);manifest=BASE/('_'+LOTE+'.json');atomic_json(manifest,result);Path('/tmp/'+LOTE+'-publicar-paths.txt').write_text('\n'.join(r['path'] for r in public)+'\n'+str(manifest.relative_to(ROOT))+'\n');print('FIM RECUPERACAO',result['resumo'],flush=True)

_run_lock.close()
