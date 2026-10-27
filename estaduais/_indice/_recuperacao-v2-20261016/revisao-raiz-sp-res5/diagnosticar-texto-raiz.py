from pathlib import Path
import difflib
script=Path('estaduais/_indice/_recuperacao-v2-20261016/revisao-raiz-sp-res5/verificar-flags-CSS-raiz.py').read_text()
exec(compile(script.split('rows=[]')[0],'<helper-flags>','exec'))
out=[]
for r in profile['documentos']:
    raw=gzip.decompress((B/r['cache_original']).read_bytes());dom=html5lib.parse(raw.decode(r['encoding_real']),namespaceHTMLElements=False).find('body');source=flags(dom)
    s=''.join(c for c,_ in source);start=s.index(re.sub(r'\s+','',r['source_text'])[:60]);source=source[start:];s=''.join(c for c,_ in source)
    md=(B/config[r['path']]).read_text();body=md.split('\n---\n',1)[1].lstrip().split('\n',1)[1];render=cmarkgfm.github_flavored_markdown_to_html(body,options=cmarkgfm.Options.CMARK_OPT_UNSAFE);dest=flags(html5lib.parseFragment(render,namespaceHTMLElements=False));t=''.join(c for c,_ in dest)
    diffs=[]
    for tag,a,b,c,d in difflib.SequenceMatcher(None,s,t,autojunk=False).get_opcodes():
        if tag!='equal':diffs.append({'op':tag,'source':s[max(0,a-45):min(len(s),b+45)],'md':t[max(0,c-45):min(len(t),d+45)],'source_range':[a,b],'md_range':[c,d]})
    under=[{'tag':e.tag,'text':''.join(e.itertext()),'attrs':e.attrib} for e in dom.iter('u')]
    out.append({'path':r['path'],'len_fonte':len(s),'len_MD':len(t),'diffs':diffs,'u':under})
(O/'diagnostico-texto-preliminar-raiz.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
