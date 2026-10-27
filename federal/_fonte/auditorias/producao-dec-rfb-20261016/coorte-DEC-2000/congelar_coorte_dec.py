import collections,datetime,gzip,hashlib,json,re,sys,unicodedata,base64,subprocess,ast,shutil
from pathlib import Path
from html.parser import HTMLParser
D=Path('federal/_fonte/auditorias/producao-dec-rfb-20261016')
C=D/'coorte-DEC-2000'
LIMIT=2000
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.lower())if not unicodedata.combining(c))
class Plain(HTMLParser):
    def __init__(self,s):super().__init__(convert_charrefs=True);self.skip=0;self.parts=[];self.feed(s)
    def handle_starttag(self,t,a):
        if t in ('head','style','script'):self.skip+=1
        if not self.skip and t in ('p','div','br','li','tr','h1','h2','h3'):self.parts.append('\n')
    def handle_endtag(self,t):
        if t in ('head','style','script'):self.skip=max(0,self.skip-1)
        if not self.skip and t in ('p','div','li','tr','h1','h2','h3'):self.parts.append('\n')
    def handle_data(self,s):
        if not self.skip:self.parts.append(s)
    def lines(self):return [re.sub(r'\s+',' ',x).strip()for x in ''.join(self.parts).splitlines()if x.strip()]
def readjsonl(path):
    result=[]
    for line in path.open():
        try:result.append(json.loads(line))
        except json.JSONDecodeError:continue
    return result
inventory={d['path']:d for d in readjsonl(D/'inventario-DEC.jsonl')}
gfm=readjsonl(D/'gates-GFM-DEC.jsonl')
head={}
for l in (D/'HEAD-urns-escopo-amplo.txt').read_text().splitlines():
    m=re.match(r'HEAD:(.*?):\d+:urn:\s*(.*)',l)
    if m:
        try:u=json.loads(m[2])
        except ValueError:u=m[2]
        head.setdefault(u,[]).append(m[1])
counts=collections.Counter(d['urn']for d in inventory.values()if 'urn'in d)
alternatives=json.loads((D/'HEAD-decretos-alternativos-metadados.json').read_text())
alternate_identity={(str(d['meta'].get('numero','')).replace('.',''),d['meta'].get('data')):d['path']for d in alternatives}
months={'janeiro':1,'fevereiro':2,'marco':3,'abril':4,'maio':5,'junho':6,'julho':7,'agosto':8,'setembro':9,'outubro':10,'novembro':11,'dezembro':12}
selected=[];held=[]
for gate in gfm:
    if not gate['condicionalmente_publicavel']:continue
    d=inventory[gate['path']];reasons=[]
    assert not d['retencoes']
    raw=Path(d['path']).read_bytes();assert sha(raw)==d['sha256_MD']
    gz=Path(d['fonte_cache']).read_bytes();assert sha(gz)==d['sha256_fonte_gzip'];source=gzip.decompress(gz).decode();assert sha(source.encode())==d['sha256_fonte']
    mgz=Path(d['metadados_cache']).read_bytes();assert sha(mgz)==d['sha256_metadados_gzip'];mraw=gzip.decompress(mgz);meta=json.loads(mraw);assert sha(mraw)==d['meta']['sha256_metadados_fonte']
    if head.get(d['urn']):reasons.append('URN_ja_HEAD_escopo_amplo')
    if (str(d['meta']['numero']).replace('.',''),d['meta']['data'])in alternate_identity:reasons.append('identidade_ja_HEAD_regulamentos_ou_decretos_alternativos')
    if counts[d['urn']]!=1:reasons.append('URN_duplicada_snapshot')
    if not re.fullmatch(r'\d+',str(d['meta']['numero'])):reasons.append('complemento_requer_cotejo_proprio')
    if d['meta']['tipo']!='Decreto' or d['primario']['tipo']!='DEC-n' or norm(meta.get('legislationType',''))!='decreto numerado':reasons.append('tipo_nao_comprovado_em_todas_fontes')
    if d['encoding_escolhido'].get('version')not in ('Current','Original','Intermediate'):reasons.append('versao_desconhecida')
    for label,pat in [('geometria_bordas',r'border-(?:bottom|top)|column-count|text-align\s*:\s*(?:right|center).{0,100}[$]'),('fonte_simbolica',r'font-family\s*:[^;\">]*(?:Symbol|Wingdings|Webdings|Dingbats|Courier|monospace)|[\ue000-\uf8ff]'),('conteudo_oculto',r'display\s*:\s*none|visibility\s*:\s*hidden|mso-hide|opacity\s*:\s*0(?:[;"\s])'),('midia_nao_textual',r'<(?:math|iframe|video|audio|form|pre|code)\b')]:
        if re.search(pat,source,re.I):reasons.append(label)
    lines=Plain(source).lines();closures=[];signers=[]
    money=r'(?:R\s*\$\s*[\d.,]+|\d[\d.:,]*\$[\d.,]*)'
    if any(len(re.findall(money,line))>1 for line in lines):reasons.append('multiplos_valores_requerem_revisao_contextual')
    if any(re.search(r'\S\xa0{2,}\S|\S\t+\S',line)for line in lines):reasons.append('separadores_espaciais_requerem_revisao')
    for i,line in enumerate(lines):
        n=norm(line)
        if not re.match(r'^(?:brasilia|rio de janeiro|capital federal|palacio)\b',n):continue
        date=re.search(r'(\d{1,2})(?:[ºo°])?\s+de\s+(\w+)\s+de\s+(\d{4})',n)
        if not date:continue
        value=f"{date[3]}-{months.get(date[2],0):02d}-{int(date[1]):02d}"
        closures.append({'literal':line,'data':value})
        tail=lines[i+1:i+7]
        signers.extend(x for x in tail if re.fullmatch(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ .’'-]{5,120}",x)and len(x.split())>=2 and not re.match(r'^(este texto|publicad|republicad|retificad|diario|d\.?o\.?|bras[ií]lia)',norm(x)))
    if not closures or {x['data']for x in closures}!={d['meta']['data']}:reasons.append('fecho_proprio_integral_data_nao_comprovada')
    if not signers:reasons.append('assinatura_propria_nao_comprovada')
    epigraphs=[x for x in lines if re.match(r'^decreto\s+n[ºo° .]*\s*\d',norm(x))]
    if len(epigraphs)!=1:reasons.append('multiplicidade_epigrafes_requer_revisao')
    if reasons:held.append({'path':d['path'],'urn':d['urn'],'retencoes_adicionais':reasons});continue
    selected.append({'inventario':d,'gate_GFM':gate,'fechos_proprios':closures,'assinaturas_proprias':signers,'HEAD_URN_equivalente':[]})
    if len(selected)>=LIMIT:break
if len(selected)<LIMIT:
    print('AGUARDANDO',len(selected),'/',LIMIT,'gates disponiveis',len(gfm),'inventario',len(inventory),flush=True)
    sys.exit(2)
C.mkdir(exist_ok=True)
paths=[d['inventario']['path']for d in selected]
query=subprocess.run(['rtk','proxy','git','cat-file','--batch-check'],input=''.join('HEAD:'+p+'\n'for p in paths),text=True,capture_output=True,check=True)
assert len(query.stdout.splitlines())==LIMIT and all(l.endswith(' missing')for l in query.stdout.splitlines())
(C/'HEAD-paths.txt').write_text(query.stdout)
(C/'HEAD-congelamento.txt').write_text(subprocess.run(['rtk','proxy','git','rev-parse','HEAD'],text=True,capture_output=True,check=True).stdout)
with gzip.open(C/'backup-MDs.jsonl.gz','wt',encoding='utf-8')as mdpack,gzip.open(C/'backup-fontes.jsonl.gz','wt',encoding='utf-8')as sources:
    for i,d in enumerate(selected,1):
        r=d['inventario'];raw=Path(r['path']).read_bytes();assert sha(raw)==r['sha256_MD'];src=Path(r['fonte_cache']).read_bytes();assert sha(src)==r['sha256_fonte_gzip'];meta=Path(r['metadados_cache']).read_bytes();assert sha(meta)==r['sha256_metadados_gzip']
        mdpack.write(json.dumps({'linha':i,'path':r['path'],'sha256_MD':r['sha256_MD'],'MD':raw.decode()},ensure_ascii=False)+'\n')
        sources.write(json.dumps({'linha':i,'path':r['path'],'fonte_gzip_base64':base64.b64encode(src).decode(),'sha256_fonte_gzip':sha(src),'metadata_gzip_base64':base64.b64encode(meta).decode(),'sha256_metadata_gzip':sha(meta)})+'\n')
        d['linha_backups']=i
(C/'coorte2000.jsonl').write_text(''.join(json.dumps(d,ensure_ascii=False)+'\n'for d in selected))
(C/'retencoes-adicionais-ate-coorte.json').write_text(json.dumps(held,ensure_ascii=False,indent=2)+'\n')
(C/'paths2000.txt').write_text('\n'.join(paths)+'\n')
for name in ('inventariar_producao_dec.py','verificar_dec_gfm.py','congelar_coorte_dec.py','verificar_coorte_dec_fechada.py'):
    p=Path('/tmp')/name;ast.parse(p.read_text());shutil.copyfile(p,C/name)
files=[p for p in C.iterdir()if p.is_file()]
manifest={'estado':'2000 decretos novos condicionais para revisao da raiz, sem publicacao/aplicacao','documentos':LIMIT,'universo_primario_preservado':139127,'limite_da_coorte':'Subcoorte fechada da producao ja coletada; auditoria ampla e coletores continuam fora desta lista. Nao e alegacao de cobertura/completude do universo.','fontes':'HTMLpublico normas.leg.br e JSONoriginal imutavel porSHA; encoding/versao/forca legal/URN/data/numero conferidos; backups completos de todos2000MDs+fontes/metadados.','fidelidade':'Texto completo DOM/GFM normalizado identico; mascaras italico/strike/sup/sub identicas, negrito-fonte preservado; sem tabelas/imagens/U/anexos/OCR/omissoes/geometria/bordas/fontes simbolicas/ocultos. Data epigrafe e fecho proprios+assinaturas; casos que nao passam retidos. Nao afirma revisao visual de fac-simile.','status':'False apenas InForce explicito noJSON associado; demais null. NotInForce nao interpretado como revogacao.','dedup':'URN unica no snapshot e ausente emHEAD federal/reguladores;2000paths ausentes emHEAD no congelamento.','arquivos':[{'path':str(p),'sha256':sha(p.read_bytes())}for p in sorted(files)],'HTTP':False,'Git_mutacao':False,'canonicos_alterados':False,'frozen_11_e_8_intactos':True}
p=C/'manifesto.json';p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print('CONGELADO',LIMIT,str(p),sha(p.read_bytes()),flush=True)
