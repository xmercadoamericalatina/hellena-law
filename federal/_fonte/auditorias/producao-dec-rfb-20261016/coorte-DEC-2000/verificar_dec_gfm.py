import gzip,hashlib,json,re,sys
from pathlib import Path
from html.parser import HTMLParser
from cmarkgfm import github_flavored_markdown_to_html
from cmarkgfm.cmark import Options
D=Path('federal/_fonte/auditorias/producao-dec-rfb-20261016')
def sha(b):return hashlib.sha256(b).hexdigest()
class Forma(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=True);self.stack=[];self.parts=[];self.chars=[];self.feed(s)
    def handle_starttag(self,t,attrs):
        a=dict(attrs);parent=self.stack[-1][1]if self.stack else set();flags=set(parent);style=a.get('style','').lower()
        for flag,tags,css in [('i',('i','em'),r'font-style\s*:\s*(?:italic|oblique)'),('b',('b','strong'),r'font-weight\s*:\s*(?:bold|[7-9]00)'),('s',('s','strike','del'),r'text-decoration[^;]*line-through'),('sup',('sup',),r'vertical-align\s*:\s*super'),('sub',('sub',),r'vertical-align\s*:\s*sub')]:
            if t in tags or re.search(css,style):flags.add(flag)
        if re.search(r'font-style\s*:\s*normal',style):flags.discard('i')
        if re.search(r'font-weight\s*:\s*(?:normal|400)',style):flags.discard('b')
        if t in ('head','script','style'):flags.add('skip')
        if t in ('p','div','br','li','tr','h1','h2','h3','h4','h5','h6'):self.parts.append('\n')
        if t not in ('br','img','meta','link','hr','input','wbr'):self.stack.append((t,flags))
    def handle_endtag(self,t):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==t:self.stack=self.stack[:i];break
        if t in ('p','div','li','tr','h1','h2','h3','h4','h5','h6'):self.parts.append('\n')
    def handle_data(self,s):
        flags=self.stack[-1][1]if self.stack else set()
        if 'skip'in flags:return
        s=s.replace('\ufeff','');self.parts.append(s);self.chars.extend((c,tuple(sorted(flags)))for c in s if not c.isspace())
    def text(self):return re.sub(r'\s+',' ',''.join(self.parts)).strip()
count=0;approved=0
with (D/'gates-GFM-DEC.jsonl').open('w')as out:
    for line in (D/'inventario-DEC.jsonl').open():
        d=json.loads(line)
        if d['retencoes']:continue
        result={'path':d['path'],'urn':d['urn'],'sha256_MD':d['sha256_MD'],'retencoes':[]}
        try:
            raw=Path(d['path']).read_bytes();assert sha(raw)==d['sha256_MD']
            prefix='# '+d['meta']['titulo']+'\n\n';body=raw.split(b'---',2)[2].decode().lstrip('\n');assert body.startswith(prefix);body=body[len(prefix):]
            source=gzip.decompress(Path(d['fonte_cache']).read_bytes()).decode('utf-8');assert sha(source.encode())==d['sha256_fonte']
            if any(re.search(r'font-(?:style|weight)|text-decoration|vertical-align',x,re.I)for x in re.findall(r'<style\b[^>]*>(.*?)</style>',source,re.S|re.I)):result['retencoes'].append('CSS_global_formato_sem_resolucao')
            source=re.sub(r'###[A-Z0-9-]*@@@','',source)
            a=Forma(source);rendered=github_flavored_markdown_to_html(body,options=Options.CMARK_OPT_UNSAFE);b=Forma(rendered)
            result.update({'sha256_texto_DOM_normalizado':sha(a.text().encode()),'sha256_texto_GFM_normalizado':sha(b.text().encode()),'sha256_render_GFM':sha(rendered.encode()),'caracteres_fonte_sem_espacos':len(a.chars),'caracteres_GFM_sem_espacos':len(b.chars)})
            if a.text()!=b.text():result['retencoes'].append('texto_DOM_GFM_divergente')
            if ''.join(x[0]for x in a.chars)==''.join(x[0]for x in b.chars):
                changes={flag:sum((flag in x[1])!=(flag in y[1])for x,y in zip(a.chars,b.chars))for flag in ('i','s','sup','sub')}
                changes['negrito_fonte_perdido']=sum('b'in x[1]and'b'not in y[1]for x,y in zip(a.chars,b.chars))
                result['deltas_mascaras_formato']=changes
                if any(changes.values()):result['retencoes'].append('formato_inline_divergente')
            else:result['retencoes'].append('sequencia_literal_diverge')
        except Exception as e:result['retencoes'].append('erro_verificacao');result['erro']=repr(e)
        result['condicionalmente_publicavel']=not result['retencoes'];out.write(json.dumps(result,ensure_ascii=False)+'\n');count+=1;approved+=result['condicionalmente_publicavel']
        if count%1000==0:print(count,'condicionais',approved,flush=True)
print('FIM GFM',count,approved,flush=True)
