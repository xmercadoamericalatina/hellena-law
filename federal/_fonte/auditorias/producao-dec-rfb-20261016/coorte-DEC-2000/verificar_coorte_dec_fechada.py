import ast,base64,datetime,gzip,hashlib,json,re,sys
from pathlib import Path
from html.parser import HTMLParser
from cmarkgfm import github_flavored_markdown_to_html
from cmarkgfm.cmark import Options
sys.path.insert(0,'scripts')
import auditar
import baixar_federal as federal
C=Path('federal/_fonte/auditorias/producao-dec-rfb-20261016/coorte-DEC-2000')
def sha(b):return hashlib.sha256(b).hexdigest()
manifest=json.loads((C/'manifesto.json').read_text())
for p in manifest['arquivos']:assert sha(Path(p['path']).read_bytes())==p['sha256'],p['path']
rows=[json.loads(l)for l in (C/'coorte2000.jsonl').open()]
assert len(rows)==2000 and len({d['inventario']['urn']for d in rows})==2000
module=ast.parse((C/'verificar_dec_gfm.py').read_text())
cls=next(n for n in module.body if isinstance(n,ast.ClassDef)and n.name=='Forma')
exec(compile(ast.Module(body=[cls],type_ignores=[]),'parser-congelado-Forma','exec'))
with gzip.open(C/'backup-MDs.jsonl.gz','rt')as mdpack,gzip.open(C/'backup-fontes.jsonl.gz','rt')as sources:
    count=0
    for row,ml,sl in zip(rows,mdpack,sources):
        count+=1
        d=row['inventario'];m=json.loads(ml);s=json.loads(sl);raw=Path(d['path']).read_bytes()
        assert raw==m['MD'].encode()and sha(raw)==d['sha256_MD']and sha(raw.split(b'---',2)[2])==d['sha256_corpo']
        gz=base64.b64decode(s['fonte_gzip_base64'],validate=True);mgz=base64.b64decode(s['metadata_gzip_base64'],validate=True)
        assert sha(gz)==d['sha256_fonte_gzip']and sha(mgz)==d['sha256_metadados_gzip']
        source=gzip.decompress(gz);metadata=gzip.decompress(mgz)
        assert sha(source)==d['sha256_fonte']and sha(metadata)==d['meta']['sha256_metadados_fonte']
        meta=json.loads(metadata);assert meta['legislationIdentifier']==d['urn']and meta['legislationDate']==d['meta']['data']
        force=federal.como_lista(meta.get('legislationLegalForce'));assert force==json.loads(d['meta']['forca_legal_fonte'])
        assert d['meta']['revogada']==(False if force==['InForce']else None)
        assert federal.escolher_texto(meta)==d['encoding_escolhido']
        body=raw.split(b'---',2)[2].decode().lstrip('\n');prefix='# '+d['meta']['titulo']+'\n\n';assert body.startswith(prefix);body=body[len(prefix):]
        assert body==federal.convert(source.decode())
        er,wa=auditar.validar(raw.decode(),d['path'],datetime.date(2026,10,16));assert not er and not wa,(d['path'],er,wa)
        a=Forma(re.sub(r'###[A-Z0-9-]*@@@','',source.decode()));render=github_flavored_markdown_to_html(body,options=Options.CMARK_OPT_UNSAFE);b=Forma(render)
        assert a.text()==b.text()and sha(render.encode())==row['gate_GFM']['sha256_render_GFM']
        assert ''.join(x[0]for x in a.chars)==''.join(x[0]for x in b.chars)
        for x,y in zip(a.chars,b.chars):
            assert all((flag in x[1])==(flag in y[1])for flag in ('i','s','sup','sub'))
            assert 'b'not in x[1]or'b'in y[1]
        assert {f['data']for f in row['fechos_proprios']}=={d['meta']['data']}and row['assinaturas_proprias']
    assert count==2000 and not mdpack.readline()and not sources.readline()
print('COORTE2000: hashes,backups,fontes,metadados,status,versao,replay,formato eGFM completos sem erros')
