from pathlib import Path
from html.parser import HTMLParser
import gzip,re,json,hashlib,collections
ROOT=Path('/Volumes/ExternalSSD/GitHub/constituicao');BASE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
class Node:
    def __init__(self,tag='',attrs=(),parent=None):self.tag=tag;self.attrs=dict(attrs);self.parent=parent;self.children=[]
class DOM(HTMLParser):
    VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self,s):
        super().__init__(convert_charrefs=True);self.root=Node();self.stack=[self.root];self.nodes=[];self.feed(s);self.close()
    def handle_starttag(self,tag,attrs):
        n=Node(tag,attrs,self.stack[-1]);self.stack[-1].children.append(n);self.nodes.append(n)
        if tag not in self.VOID:self.stack.append(n)
    def handle_endtag(self,tag):
        for k in range(len(self.stack)-1,0,-1):
            if self.stack[k].tag==tag:self.stack=self.stack[:k];return
    def handle_data(self,s):self.stack[-1].children.append(s)
def ancestors(n):
    a=[]
    while n is not None:a.append(n);n=n.parent
    return a
def flags(n):
    a=ancestors(n);styles=';'.join((x.attrs.get('style') or '').lower() for x in a);styles=re.sub(r'\s+','',styles)
    return (any(x.tag in ('b','strong') for x in a) or bool(re.search(r'font-weight:(?:bold|700)',styles)),any(x.tag in ('i','em') for x in a) or 'font-style:italic' in styles,any(x.tag in ('s','strike','del') for x in a) or 'line-through' in styles,any(x.tag=='sup' for x in a),any(x.tag=='sub' for x in a))
def content(n):
    chunks=[]
    def walk(x):
        if isinstance(x,str):chunks.extend((c,flags(n)) for c in x);return
        if x.tag in ('script','style','head','xml'):return
        if x.tag=='br':chunks.append(('␤',(False,)*5))
        if x.tag in ('p','div','li','blockquote'):chunks.append(('␞',(False,)*5))
        for child in x.children:
            if isinstance(child,str):chunks.extend((c,flags(x)) for c in child)
            else:walk(child)
    walk(n);norm=[]
    for c,f in chunks:
        if c.isspace():
            if norm and norm[-1][0]!=' ':norm.append((' ',(False,)*5))
        else:norm.append((c,f))
    while norm and norm[0][0]==' ':norm.pop(0)
    while norm and norm[-1][0]==' ':norm.pop()
    return norm
def nearest(n,tag):return next((x for x in ancestors(n.parent) if x.tag==tag),None)
def table_signature(dom):
    tables=[n for n in dom.nodes if n.tag=='table'];result=[]
    for t in tables:
        rows=[x for x in dom.nodes if x.tag=='tr' and nearest(x,'table') is t];cells=[];matrix={};overlap=[]
        for ri,row in enumerate(rows):
            cols=[x for x in dom.nodes if x.tag in ('th','td') and nearest(x,'tr') is row and nearest(x,'table') is t];ci=0
            for cell in cols:
                while (ri,ci) in matrix:ci+=1
                rs=int(cell.attrs.get('rowspan','1'));cs=int(cell.attrs.get('colspan','1'));index=len(cells);chars=content(cell)
                for rr in range(ri,ri+rs):
                    for cc in range(ci,ci+cs):
                        if (rr,cc) in matrix:overlap.append([rr,cc])
                        matrix[(rr,cc)]=index
                cells.append({'tag':cell.tag,'r':ri,'c':ci,'rowspan':rs,'colspan':cs,'scope':cell.attrs.get('scope'),'id':cell.attrs.get('id'),'headers':cell.attrs.get('headers'),'text':' '.join(''.join(c for c,_ in chars).replace('␞',' ').replace('␤',' ').split()),'runs':chars,'paragraphs':sum(1 for c,_ in chars if c=='␞'),'breaks':sum(1 for c,_ in chars if c=='␤')});ci+=cs
        groups=[{'tag':x.tag,'attrs':{k:v for k,v in x.attrs.items() if k in ('span','scope','id','headers')},'parent':x.parent.tag} for x in dom.nodes if x.tag in ('thead','tbody','tfoot','colgroup','col') and nearest(x,'table') is t]
        result.append({'grupos_colunas':groups,'cells':cells,'matrix':sorted([r,c,v] for (r,c),v in matrix.items()),'overlap':overlap,'rows':len(rows)})
    return result
def main():
    manifest=json.loads((BASE/'manifesto-base.json').read_text());out=[]
    for r in manifest['documentos']:
        raw=gzip.decompress((ROOT/r['cache']).read_bytes());assert sha(raw)==r['fonte_sha256'];s=raw.decode('utf-8');s=re.sub(r'<s>\s*(&deg;|&ordm;|&ordf;|°|º|ª|o|a)\s*</s>',r'\1',s)
        md=(ROOT/r['snapshot']).read_text();assert sha(md.encode())==r['sha256_depois'];source=DOM(s);target=DOM(md);a=table_signature(source);b=table_signature(target);dif=[]
        for i,(x,y) in enumerate(zip(a,b)):
            if x!=y:
                if x['matrix']!=y['matrix']:dif.append({'table':i,'issue':'grade'})
                if x['grupos_colunas']!=y['grupos_colunas']:dif.append({'table':i,'issue':'grupos/colunas'})
                for j,(c,d) in enumerate(zip(x['cells'],y['cells'])):
                    if c!=d:dif.append({'table':i,'cell':j,'source':c,'target':d})
                if len(x['cells'])!=len(y['cells']):dif.append({'table':i,'issue':'cell count'})
        if len(a)!=len(b):dif.append({'issue':'table count'})
        graphics=[{'tag':n.tag,'attrs':n.attrs} for n in source.nodes if n.tag in ('img','svg','object','embed','canvas','math') or n.tag.startswith('v:')]
        row={'path':r['path'],'fonte_sha256':sha(raw),'md_sha256_revisado':sha(md.encode()),'tabelas_fonte':len(a),'tabelas_md':len(b),'celulas':sum(len(x['cells']) for x in a),'grade_arvore_runs_iguais':not dif,'diferencas':dif,'sha256_semantica_tabelas':sha(json.dumps(a,ensure_ascii=False,sort_keys=True).encode()),'spans':{'rowspan':sum(c['rowspan']!=1 for x in a for c in x['cells']),'colspan':sum(c['colspan']!=1 for x in a for c in x['cells'])},'celulas_com_tachado':sum(any(f[2] for _,f in c['runs']) for x in a for c in x['cells']),'elementos_visuais_fonte':graphics,'sobreposicoes_grade':[x['overlap'] for x in a if x['overlap']]}
        out.append(row);print(r['path'],row['tabelas_fonte'],row['celulas'],'diff',len(dif),flush=True)
    p=BASE/'comparacao-estrutural.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('report',sha(p.read_bytes()),flush=True)
if __name__=='__main__':main()
