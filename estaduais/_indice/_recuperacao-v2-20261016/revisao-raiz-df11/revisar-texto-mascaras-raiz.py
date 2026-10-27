from pathlib import Path
import json,gzip,hashlib,re
import html5lib,cmarkgfm
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');A=B/'estaduais/_indice/_recuperacao-v2-20261016';O=A/'revisao-raiz-df11';O.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
source=(A/'revisao-raiz-sp-res20/verificar-flags-CSS-raiz.py').read_text();fn=source[source.index('def flags(root):'):source.index('rows=[]')];exec(compile(fn,'<mascaras-raiz>','exec'))
m=json.loads((A/'manifesto-df-dlg11.json').read_text());ledger=json.loads((A/'df-dlg11/ledger.json').read_text());by={r['path']:r for r in ledger['documentos']};rows=[]
assert sha((A/'manifesto-df-dlg11.json').read_bytes())=='8096499071e6877e468dc6b544041fa7fef77571870d00ffa3658eb3a2e2cf0e'
for r in m['documentos']:
    l=by[r['path']];cache=B/'estaduais/DF/_fonte'/Path(r['path']).relative_to('estaduais/DF').with_suffix('.html.gz');packed=cache.read_bytes();raw=gzip.decompress(packed)
    assert sha(packed)==l['fonte_gzip_sha256'] and sha(raw)==r['fonte_sha256']
    d=html5lib.parse(raw.decode('utf-8'),namespaceHTMLElements=False);scopes=[e for e in d.iter() if e.get('id')=='div_texto'];assert len(scopes)==1,(r['path'],[(e.tag,e.get('id')) for e in d.iter() if e.get('id')]);scope=scopes[0]
    src=flags(scope);assert ''.join(c for c,_ in src)==re.sub(r'\s+','',l['texto_fonte'])
    candidate=(B/r['candidato']).read_bytes();assert sha(candidate)==r['new_sha256'];assert sha((B/r['snapshot']).read_bytes())==r['old_sha256'];assert sha((B/r['path']).read_bytes())==r['old_sha256']
    s=candidate.decode();body=s.split('\n---\n',1)[1].lstrip().split('\n',1)[1];dest=flags(html5lib.parseFragment(cmarkgfm.github_flavored_markdown_to_html(body,options=cmarkgfm.Options.CMARK_OPT_UNSAFE),namespaceHTMLElements=False));assert ''.join(c for c,_ in src)==''.join(c for c,_ in dest),r['path']
    missing=[i for i,(x,y) in enumerate(zip(src,dest)) if x[1]&~y[1]];assert not missing,(r['path'],missing)
    extra=[i for i,(x,y) in enumerate(zip(src,dest)) if x[1]!=y[1]];runs=[]
    for i in extra:
        if runs and runs[-1][1]==i:runs[-1][1]=i+1
        else:runs.append([i,i+1])
    labels=[]
    for a,b in runs:
        text=''.join(c for c,_ in src[a:b]);assert all(x[1]==0 and y[1]==1 for x,y in zip(src[a:b],dest[a:b])) and re.fullmatch(r'Art\.\d+[º°.]?',text),(r['path'],text)
        labels.append(text)
    forbidden=[e.tag for e in scope.iter() if e.tag in ('table','img','svg','ol','ul','iframe','object','script','form','input','canvas')];assert not forbidden,(r['path'],forbidden)
    rows.append({'path':r['path'],'candidato':r['candidato'],'SHA_candidato':sha(candidate),'fonte_cache':str(cache.relative_to(B)),'SHA_raw':sha(raw),'div_texto_unico':True,'texto_ledger_igual_HTML5':True,'texto_GFM_igual_HTML5':True,'mascaras_fonte_incluidas':True,'Bextra_rotulos':labels,'texto_fonte_lido_integralmente_raiz':l['texto_fonte'],'contexto_raiz':'Titulos honorificos56-60/62-65;61susta portaria externa,sem anexo proprio;66formula remuneratoria remete a base1995,sem tabela ausente.58-61nao possuem data de fecho propria,nao completar;epigrafe datada e assinatura presentes. Aviso editorial DCL preservado e normal.'})
out={'estado':'revisao_parcial_raiz_nao_aprovacao_publicacao','total':len(rows),'atos':rows,'pendencias':['Indice SINJ primario imutavel/UID e HEAD atual','Selecao de versao/Publicacao e status/metadados','Renderizacao GitHub e auditoria de formato','Decisao/aplicacao final'], 'limites':'Tags e CSS inline; nao certifica CSS externo ou pixels. Leitura11normas completas, nao todos925DF.'}
(O/'revisao-texto-mascaras11-raiz.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'atos':len(rows),'texto_mascaras':True,'aplicados':False}))
