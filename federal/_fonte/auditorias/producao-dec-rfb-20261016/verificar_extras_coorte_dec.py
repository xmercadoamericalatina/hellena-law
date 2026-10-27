import base64,gzip,hashlib,json,re
from pathlib import Path
from html.parser import HTMLParser
D=Path('federal/_fonte/auditorias/producao-dec-rfb-20261016');C=D/'coorte-DEC-2000'
class Bruto(HTMLParser):
    def __init__(self,s):super().__init__(convert_charrefs=True);self.skip=0;self.parts=[];self.feed(s)
    def handle_starttag(self,t,a):
        if t in ('head','style','script'):self.skip+=1
    def handle_endtag(self,t):
        if t in ('head','style','script'):self.skip=max(0,self.skip-1)
    def handle_data(self,s):
        if not self.skip:self.parts.append(s)
rows=[json.loads(l)for l in(C/'coorte2000.jsonl').open()];out=[]
with gzip.open(C/'backup-fontes.jsonl.gz','rt')as f:
    for row,line in zip(rows,f):
        record=row['inventario'];d=json.loads(line);raw=gzip.decompress(base64.b64decode(d['fonte_gzip_base64']));assert hashlib.sha256(raw).hexdigest()==record['sha256_fonte'];source=raw.decode();flags=[]
        patterns=[('VML_Office_vector_ou_imagem',r'<(?:v:|w:drawing|w:pict|w:object|m:|o:OLEObject|picture\b)|background(?:-image)?\s*:[^;\">]*url\('),('script_ou_midias',r'<(?:script|iframe|canvas|math|video|audio|ruby|rt)\b'),('font_face_simbolica',r'face\s*=\s*["\x27][^"\x27]*(?:Symbol|Wingdings|Webdings|Dingbats|Courier)'),('arquivo_externo_linkado',r'href\s*=\s*["\x27][^"\x27]*\.(?:pdf|png|jpe?g|tif|docx?)(?:[?#"\x27])'),('geometria_horizontal_ou_boxdrawing',r'<hr\b|[\u2500-\u257f]'),('layout_CSS_espacial',r'float\s*:|display\s*:\s*(?:inline-block|table|flex|grid)|position\s*:\s*(?:absolute|fixed|relative)|font-size\s*:\s*0(?:[;"\s])'),('spans_posicionados',r'<span\b[^>]*style=["\x27][^"\x27]*(?:margin-left|padding-left|word-spacing|letter-spacing|width)\s*:')]
        for label,pattern in patterns:
            if re.search(pattern,source,re.I):flags.append(label)
        parser=Bruto(source)
        spatial=[s for s in parser.parts if re.search(r'\S(?:\xa0{2,}|\t+)\S',s)]
        if spatial:flags.append('tabs_ou_NBSP_espaciais_antes_normalizacao')
        out.append({'path':record['path'],'sha256_MD':record['sha256_MD'],'sha256_fonte':record['sha256_fonte'],'retencoes_extras':flags,'exemplos_separadores_brutos':spatial[:3]})
assert len(out)==2000
proof={'documentos':len(out),'retidos':sum(bool(x['retencoes_extras'])for x in out),'motivo_overlay':'O teste de tabs/NBSP no preparador usa linhas ja normalizadas e e ineficaz; este gate verifica handle_data bruto antes de qualquer normalizacao, sem modificar congelados. Acrescenta VML/fontes/layout/arquivos externos.','registros':out}
p=D/'gates-extras-midias-DEC2000-v2.json';text=json.dumps(proof,ensure_ascii=False,indent=2)+'\n'
if '--auditar' in __import__('sys').argv:assert p.read_text()==text
else:p.write_text(text)
print('GATES_EXTRAS2000',proof['retidos'],hashlib.sha256(p.read_bytes()).hexdigest())
