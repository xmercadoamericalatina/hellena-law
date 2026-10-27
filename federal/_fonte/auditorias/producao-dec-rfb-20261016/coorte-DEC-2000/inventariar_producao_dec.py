import concurrent.futures,datetime,gzip,hashlib,html,json,re,sys,unicodedata
from pathlib import Path
from html.parser import HTMLParser
sys.path.insert(0,'scripts')
import baixar_federal as federal
import auditar
D=Path('federal/_fonte/auditorias/producao-dec-rfb-20261016')
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.lower())if not unicodedata.combining(c))
def headers(raw):
    result={}
    for line in raw.split(b'---',2)[1].decode().splitlines():
        if ':' not in line:continue
        k,v=line.split(':',1);v=v.strip()
        try:result[k]=json.loads(v)
        except ValueError:result[k]=v
    return result
class Texto(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=True);self.skip=0;self.parts=[];self.feed(s)
    def handle_starttag(self,t,a):
        if t in ('head','style','script'):self.skip+=1
        if not self.skip and t in ('p','div','br','li','tr','h1','h2','h3'):self.parts.append('\n')
    def handle_endtag(self,t):
        if t in ('head','style','script'):self.skip=max(0,self.skip-1)
        if not self.skip and t in ('p','div','li','tr','h1','h2','h3'):self.parts.append('\n')
    def handle_data(self,s):
        if not self.skip:self.parts.append(s)
    def text(self):return re.sub(r'###[A-Z0-9-]*@@@','', ''.join(self.parts))
index=federal.carregar_indice({'DEC-n'})
prim={federal.montar(d)['urn']:d for d in index}
head={}
for l in (D/'HEAD-urns-decretos.txt').read_text().splitlines():
    m=re.match(r'HEAD:(.*?):\d+:urn:\s*(.*)',l)
    if m:
        try:u=json.loads(m[2])
        except ValueError:u=m[2]
        head.setdefault(u,[]).append(m[1])
paths=[Path(p)for p in json.loads((D/'snapshot-paths.json').read_text())if p.startswith('federal/decretos/')]
months={'janeiro':1,'fevereiro':2,'marco':3,'abril':4,'maio':5,'junho':6,'julho':7,'agosto':8,'setembro':9,'outubro':10,'novembro':11,'dezembro':12}
def process(p):
    out={'path':str(p),'retencoes':[]}
    try:
        raw=p.read_bytes();meta=headers(raw);body=raw.split(b'---',2)[2];urn=meta['urn'];out.update({'urn':urn,'sha256_MD':sha(raw),'sha256_corpo':sha(body),'meta':meta,'HEAD_equivalente_URN':head.get(urn,[])})
        if head.get(urn):out['retencoes'].append('URN_ja_HEAD')
        if urn not in prim:out['retencoes'].append('fora_indice_primario')
        d=prim.get(urn);out['primario']=d
        source=Path('federal/_fonte/decretos')/p.parent.name/(p.stem+'.html.gz');cache=source.read_bytes();bruto=gzip.decompress(cache);out.update({'fonte_cache':str(source),'sha256_fonte_gzip':sha(cache),'sha256_fonte':sha(bruto)})
        if bruto.startswith(b'%PDF'):out['retencoes'].append('PDF_OCR_sem_revisao_visual');return out
        markup=bruto.decode('utf-8');text=Texto(markup).text();out['sha256_texto_DOM']=sha(text.encode())
        own=[re.sub(r'\s+',' ',x).strip().lstrip('\ufeff').strip()for x in text.splitlines()if x.strip().strip('\ufeff').strip()];out['epigrafe_propria']=own[0]if own else ''
        ep=norm(out['epigrafe_propria']);m=re.search(r'\bdecreto\s+(?:n[ºo° .]*\s*)?([\d.]+)',ep)
        if not m or re.sub(r'\D','',m[1])!=re.sub(r'\D','',str(meta['numero'])):out['retencoes'].append('numero_epigrafe_nao_comprovado')
        date=re.search(r'(\d{1,2})\s*(?:[ºo°])?\s+de\s+(\w+)\s+de\s+(\d{4})',ep)
        explicit=f"{date[3]}-{months.get(date[2],0):02d}-{int(date[1]):02d}"if date else None
        if explicit!=meta['data']:out['retencoes'].append('data_epigrafe_nao_comprovada')
        out['data_epigrafe']=explicit
        for label,pat in [('tabela',r'<table\b'),('imagem',r'<(?:img|svg|object|embed|canvas)\b'),('sublinhado',r'<u\b|text-decoration[^;"<>]*underline'),('lista_estrutura',r'<(?:ol|ul|dl)\b'),('geometria_CSS',r'position\s*:\s*(?:absolute|fixed)|white-space\s*:\s*pre|mso-tab|tab-stops')]:
            if re.search(pat,markup,re.I):out['retencoes'].append(label)
        flat=norm(text)
        for label,pat in [('anexo_requer_cotejo',r'\banex[oa]s?\b'),('marcador_omissao',r'ilegive[lí]|ileg[ií]vel|omitid|suprimid|\(\s*\.\s*\.\s*\.\s*\)|\.\s*\.\s*\.'),('integra_externa',r'integra.{0,80}(?:disponivel|site|endereco)|disponivel.{0,80}integra')]:
            if re.search(pat,flat,re.I):out['retencoes'].append(label)
        if '\x00'in text or '\ufffd'in text:out['retencoes'].append('caractere_perdido')
        if not re.search(r'\b(?:decreta|decretam)\s*:',flat):out['retencoes'].append('formula_decreto_ausente')
        if not re.search(r'\bart(?:igo)?[.\s]*[1-9u]',flat):out['retencoes'].append('articulado_nao_comprovado')
        if not re.search(r'(brasilia|rio de janeiro|palacio|capital federal).{0,120}\b\d{4}\b',flat):out['retencoes'].append('fecho_nao_comprovado')
        if not meta.get('sha256_metadados_fonte'):out['retencoes'].append('sem_rawmetadata_imutavel')
        else:
            mp=Path('federal/_fonte/metadados-normas')/sha(urn.encode())/(meta['sha256_metadados_fonte']+'.json.gz');mb=mp.read_bytes();mr=gzip.decompress(mb);md=json.loads(mr);out.update({'metadados_cache':str(mp),'sha256_metadados_gzip':sha(mb)})
            assert sha(mr)==meta['sha256_metadados_fonte'] and md['legislationIdentifier']==urn
            assert md['legislationDate']==meta['data']
            force=federal.como_lista(md.get('legislationLegalForce'));assert json.loads(meta['forca_legal_fonte'])==force
            assert meta['revogada']==(False if force==['InForce']else None)
            enc=federal.escolher_texto(md);out['encoding_escolhido']=enc
            assert enc and meta['versao_texto']=={'Current':'compilada (texto vigente)','Original':'original','Intermediate':'republicação/retificação'}.get(enc.get('version'),enc.get('version'))
        er,wa=auditar.validar(raw.decode(),str(p),datetime.date(2026,10,16));out['formato']={'erros':er,'avisos':wa}
        if er or wa:out['retencoes'].append('formato')
        if d:
            expected='# '+d['normaNome'].strip()+'\n\n'+federal.convert(markup)
            if body.decode().lstrip('\n')!=expected:out['retencoes'].append('replay_corpo_diverge')
    except Exception as e:out['retencoes'].append('erro_auditoria');out['erro']=repr(e)
    return out
from collections import Counter
counts=Counter();total=0;eligible=0
with (D/'inventario-DEC.jsonl').open('w')as f:
    with concurrent.futures.ThreadPoolExecutor(max_workers=8)as pool:
        for out in pool.map(process,paths):
            f.write(json.dumps(out,ensure_ascii=False)+'\n');total+=1;counts.update(out['retencoes']);eligible+=not out['retencoes']
            if total%2000==0:print(total,'pre_elegiveis',eligible,flush=True)
result={'snapshot':total,'pre_elegiveis_antes_GFM':eligible,'retencoes':dict(counts),'universo_indice_primario_DEC_n':len(prim),'coleta_completa':False,'revisao_GFM_pendente':True}
(D/'resumo-DEC-fase1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(result,flush=True)
