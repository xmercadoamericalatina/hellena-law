from pathlib import Path
import json,hashlib,re,sys,datetime,subprocess,html
import html5lib
from cmarkgfm import github_flavored_markdown_to_html as render
sys.path.insert(0,str(Path('scripts').resolve()))
import auditar,baixar_camara as cam
B=Path('federal/_fonte/auditorias/dpl3-coletaneas-integra-20261016');O=B/'revisao-raiz';sha=lambda b:hashlib.sha256(b).hexdigest()
def meta(raw):
    d={}
    for line in raw.decode().split('---',2)[1].strip().splitlines():
        k,v=line.split(':',1);v=v.strip()
        try:d[k]=json.loads(v)
        except ValueError:d[k]=v
    return d
primary={}
for r in json.loads(Path('federal/_fonte/auditorias/dpl-auditoria-20261016/primario5831.json').read_text()):
    date=datetime.datetime.strptime(r['dataassinatura'],'%d/%m/%Y').date().isoformat();num=str(r['numero']).replace('.','').lower()+('-'+r['complemento'].lower() if r.get('complemento') else '');primary['urn:lex:br:federal:decreto.legislativo:'+date+';'+num]=r
queries={r['urn']:r for r in json.loads(Path('federal/_indice/camara-dpl-pendencias/indice.json').read_text())['consultas']}
report=json.loads((O/'verificacao-raiz3.json').read_text());head=subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'],text=True).strip()
for row in report['atos']:
    p=Path(row['candidato']);raw=p.read_bytes();assert sha(raw)==row['sha256'];old=Path(row['canonico']).read_bytes();om=meta(old);nm=meta(raw)
    changed={'revogada','fonte','versao_texto','fonte_alternativa_HTML','fonte_coletanea','paginas_fonte_PDF','paginas_fonte_impressas'}
    assert {k:v for k,v in om.items() if k not in changed}=={k:v for k,v in nm.items() if k not in changed}
    assert nm['revogada'] is None and nm['fonte_alternativa_HTML']==om['fonte'];assert nm['urn'] in primary
    doc=next(d for d in queries[nm['urn']]['documentos'] if d['url']==nm['url_metadados']);info=cam.identificar(doc,'dpl');assert info['urn']==nm['urn'] and info['data']==nm['data'] and info['numero']==nm['numero'] and doc['titulo']==nm['titulo'] and doc['situacao']==nm['situacao']
    assert nm['versao_texto']=='coletanea_oficial_transcricao_cotejada'
    body=raw.decode().split('---',2)[2].lstrip();rendered=render(body);dom=html5lib.parseFragment(rendered,namespaceHTMLElements=False)
    assert not list(dom.iter('ol')) and not list(dom.iter('table')) and not list(dom.iter('img'))
    expected=re.sub(r'(?m)^# ','',body);expected=re.sub(r'(?m)^> ','',expected);expected=expected.replace('**','').replace('*','').replace('\\.','.')
    plain=''.join(dom.itertext());norm=lambda s:''.join(c for c in s if not c.isspace() and c!='\ufeff')
    assert norm(plain)==norm(expected),(row['numero'],'GFM chars')
    legal=body.split('\n\n',2)[2];cam.conferir_data_propria({'numero':nm['numero'],'data':nm['data'],'urn':nm['urn']},legal,nm['titulo'],'dpl');assert cam.tipo_legislativo_comprovado(legal)
    errors,warnings=auditar.validar(raw.decode(),row['canonico'],datetime.date(2026,10,16));assert not errors and not warnings,(errors,warnings)
    r=subprocess.run(['rtk','proxy','git','cat-file','-e',head+':'+row['canonico']],stdout=subprocess.PIPE,stderr=subprocess.PIPE);assert r.returncode!=0
    (O/(row['numero']+'-render.html')).write_text(rendered)
    row.update({'sha256_antes':sha(old),'formato_erros':errors,'formato_avisos':warnings,'GFM_caracteres_pontuacao_iguais':True,'identidade_indice_metadados_data_fecho_tipo':True,'ausente_HEAD':head,'status':'aprovado_raiz_aguarda_aplicacao_commit_push'})
report['estado']='aprovado_raiz_3atos_18paginas_com_dois_deltas_adicionais';report['HEAD']=head
(O/'aprovacao-raiz3-final.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('3 APROVADOS;18páginas/2correções adicionais;formato/GFM/identidade confirmados;semapply.',sha((O/'aprovacao-raiz3-final.json').read_bytes()))
