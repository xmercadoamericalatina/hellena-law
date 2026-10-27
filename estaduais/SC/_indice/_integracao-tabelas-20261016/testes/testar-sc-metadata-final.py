import sys,json,gzip,re,tempfile,types,importlib.util,hashlib
from pathlib import Path
sys.path.insert(0,str(Path('scripts').resolve()));from estados import sc
rows=json.load(open('estaduais/SC/_indice/_reparos-tachado-20261016/manifesto-preparado.json'))['documentos'];out=[]
with tempfile.TemporaryDirectory() as tmp:
 sc.RAIZ_ESTADUAIS=tmp
 for ident in (11179,12738):
  row=next(z for z in rows if z['path'].endswith('id'+str(ident)+'.md'));raw=gzip.decompress(Path(row['cache']).read_bytes());cap={};sc.rede=types.SimpleNamespace(get=lambda *a,**k:(200,raw,'text/html'));sc.caminhos=lambda *a:(str(Path(tmp)/'never.md'),str(Path(tmp)/'fonte.gz')) if not cap.update(caminhos=a) else None;sc.gravar=lambda md,fonte,bruto,meta,corpo:cap.update(meta=dict(meta));status=sc.processar(ident);assert status[0]=='ok';assert (cap['meta']['data'],cap['caminhos'][2])==('1994-10-09','1994') if ident==11179 else cap['meta']['revogada'] is True;out.append(dict(id=ident,fonte_sha256=hashlib.sha256(raw).hexdigest(),status=status,metadata=cap['meta'],rota=cap['caminhos']))
fixtures=[('REVOGADA TOTALMENTE PELA LEI280/04\nFONTE',True),('REVOGADA PARCIALMENTE PELA LEI280/04\nFONTE',None),('RESTABELECIDA PELA LEI280/04\nREVOGADA TOTALMENTE PELA LEI200/03\nFONTE',None),('TÍTULO\nFONTE\nREVOGADA TOTALMENTE PELA LEI280/04',None),('CORPO SEM MARCADOR FONTE: REVOGADA TOTALMENTE',None)]
for text,expected in fixtures:assert sc.norma_revogada('',text) is expected
assert sc.data_do_texto('Lei sem epígrafe','<meta name="publication" content="2000/01/01">',titulo='')==''
assert sc.data_do_texto('LEI Nº 1, DE 2 DE JANEIRO DE 1995','',titulo='LEI Nº 1, DE 3 DE JANEIRO DE 1995')=='1995-01-02'
p=Path('/tmp/sc-metadata-fallback-revogacao-provas.json');p.write_text(json.dumps(dict(script_sha256=hashlib.sha256(Path('scripts/estados/sc.py').read_bytes()).hexdigest(),reais=out,fixtures_status=5,fixtures_data=2,limite='Nenhum MD alterado; LC128 migração1994 e lei11178revogada ficam pendentes de revisão do lote.'),ensure_ascii=False,indent=2));print(out)
