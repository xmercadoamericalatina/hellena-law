import base64,gzip,hashlib,html,json,re
from pathlib import Path
D=Path('federal/_fonte/auditorias/producao-dec-rfb-20261016');C=D/'coorte-DEC-2000'
FIXED={
'dec-75775-1975-05-26.md':('0019373a638141da0b64ccd08c08b56332da1e7ce45d5adc1856bc0f8f49fd45',['Ney Braga']),
'dec-75788-1975-05-28.md':('978d022c3171c1bf7de02095b6403631e34984b258935a47e5287ba88c358f42',['Shigeaki Ueki']),
'dec-78341-1976-08-31.md':('59a3633994b44414a517bde8ba5a2ca152de134893010419f12465de66437a45',['ERNESTO GEISEL','Ney Braga']),
'dec-79342-1977-03-07.md':('793282c48beb19e1cc191bb25d988536d2faffa30d633dca47fb5d67f1b0fcdd',['Decreto nº 79.342, de 7 de março de 1977'])}
proof=json.loads((D/'revisao4-espacos-posicionados-DEC2000.json').read_text());expected={r['path']:r for r in proof['documentos']};assert len(expected)==4
count=0;span_count=0
with gzip.open(C/'backup-fontes.jsonl.gz','rt')as f:
    for l in f:
        d=json.loads(l);name=Path(d['path']).name
        if name not in FIXED:continue
        raw=gzip.decompress(base64.b64decode(d['fonte_gzip_base64']));assert hashlib.sha256(raw).hexdigest()==FIXED[name][0];s=raw.decode();record=expected[d['path']];parents=[]
        for parent in re.findall(r'<p\b[^>]*>.*?</p>',s,re.S|re.I):
            spans=[]
            for literal in record['contextos']:
                for span in literal['spans']:
                    if span['HTML_literal']in parent and span['HTML_literal']not in spans:
                        assert html.unescape(re.sub('<[^>]*>','',span['HTML_literal']))=='\xa0'
                        assert hashlib.sha256(span['HTML_literal'].encode()).hexdigest()==span['sha256_HTML']
                        spans.append(span['HTML_literal']);span_count+=1;s=s.replace(span['HTML_literal'],'',1)
            if spans:
                text=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]*>','',parent))).strip();parents.append(text)
        assert parents==FIXED[name][1],(name,parents)
        assert not re.search(r'float\s*:|display\s*:\s*(?:inline-block|table|flex|grid)|position\s*:\s*(?:absolute|fixed|relative)|font-size\s*:\s*0(?:[;"\s])|<span\b[^>]*style=["\x27][^"\x27]*(?:margin-left|padding-left|word-spacing|letter-spacing|width)\s*:',s,re.I)
        count+=1
assert count==4 and span_count==5
print('4casos/5spans: somente1NBSP porrecuo deepigrafe/assinatura; demaisgeometrias ausentes; SHAfixo; semalteracao')
