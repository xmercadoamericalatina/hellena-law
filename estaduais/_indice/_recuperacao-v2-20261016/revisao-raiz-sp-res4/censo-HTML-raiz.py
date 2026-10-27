from pathlib import Path
import json,gzip,html5lib,collections
O=Path('estaduais/_indice/_recuperacao-v2-20261016/revisao-raiz-sp-res4')
p=json.loads((O/'perfil4-selecionado.json').read_text());out=[];tags=collections.Counter();styles=set();classes=set()
for r in p['documentos']:
    raw=gzip.decompress(Path(r['cache_original']).read_bytes());d=html5lib.parse(raw.decode(r['encoding_real']),namespaceHTMLElements=False);body=d.find('body');special=[]
    for e in body.iter():
        tags[e.tag]+=1
        if e.get('style'):styles.add(e.get('style'))
        if e.get('class'):classes.add(e.get('class'))
        if e.tag in ('table','img','svg','ol','ul','hr','iframe','object','script','form','input','canvas'):special.append([e.tag,dict(e.attrib)])
    out.append({'path':r['path'],'especial':special,'style_head':[x.text for x in d.find('head').iter('style')]})
assert not any(r['especial'] or r['style_head'] for r in out),out
proof={'documentos':out,'tags':dict(tags),'inline_styles':sorted(styles),'classes':sorted(classes),'limite':'Folha externa compartilhada nao carregada; HTML fonte e estilos inline inspecionados. Tachados semanticos/inline incluidos em prova separada.'}
(O/'censo-HTML-estilos-raiz.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in proof.items() if k!='documentos'},ensure_ascii=False))
