import sys,json,hashlib
from pathlib import Path
import html5lib
sys.path.insert(0,str(Path('scripts').resolve()));import html2md
cases=['<table><thead><tr><th>Nome<tbody><tr><td>Valor</table>','<table><colgroup><col span="2"><tbody><tr><td>A<td>B</table>','<table><tbody><tr><td>A<tbody><tr><td>B</table>','<table><colgroup><col><tr><td>A</table>','<table><caption>Título<tbody><tr><td>A</table>','<table><thead><tr><th>N<tfoot><tr><td>F<tbody><tr><td>B</table>','<table><colgroup><col><colgroup span="2"><tbody><tr><td>A</table>','<table><tbody><tr><td>Outer<table><thead><tr><th>N<tbody><tr><td>Inner</table><tbody><tr><td>Fim</table>']
def tree(e):
 return (e.tag,tuple(sorted(e.attrib.items())),e.text or '',tuple((tree(c),c.tail or '') for c in e))
def tables(s):
 f=html5lib.parseFragment(s,namespaceHTMLElements=False);return [tree(e) for e in f if e.tag=='table']
rows=[]
for src in cases:
 out=html2md.convert(src);assert tables(src)==tables(out),(src,out,tables(src),tables(out));rows.append(dict(fonte=src,resultado=out,arvore_html5_igual=True))
p=Path('/tmp/html2md-grupos-opcionais-oracle.json');p.write_text(json.dumps(dict(conversor_sha256=hashlib.sha256(Path('scripts/html2md.py').read_bytes()).hexdigest(),oracle='html5lib1.1',fixtures=rows),ensure_ascii=False,indent=2));print(len(rows),'HTML5OK',hashlib.sha256(p.read_bytes()).hexdigest())
