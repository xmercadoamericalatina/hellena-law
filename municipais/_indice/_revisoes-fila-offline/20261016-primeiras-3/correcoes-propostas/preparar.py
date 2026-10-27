import datetime,hashlib,json,sys,difflib
from pathlib import Path

ROOT=Path('/Volumes/ExternalSSD/GitHub/constituicao')
BASE=ROOT/'municipais/_indice/_revisoes-fila-offline/20261016-primeiras-3'
OUT=BASE/'correcoes-propostas'
sha=lambda b:hashlib.sha256(b).hexdigest()
review=BASE/'revisao.json'
assert sha(review.read_bytes())=='e70732d9a413c3835eb3030784b4773aca7a080b3f0b2f7a9bbb55dc68b654a4'
data=json.loads(review.read_text());OUT.mkdir(exist_ok=True)
pipeline={n:sha((ROOT/'scripts'/n).read_bytes()) for n in data['pipeline_shas']}
assert pipeline==data['pipeline_shas']
records=[]
for item,date in zip(data['documentos'][1:],['2026-07-03','2026-01-05']):
    source=Path(item['candidato']);raw=source.read_bytes();assert sha(raw)==item['sha256_candidato']
    assert sha(Path(item['pdf']).read_bytes())==item['fonte_sha256']
    before=raw.decode();text=before;patches=[]
    def patch(old,new,count=1):
        global text
        assert text.count(old)==count,(item['codigo'],old,text.count(old))
        positions=[];start=0
        while (pos:=text.find(old,start))>=0:
            positions.append(pos);start=pos+len(old)
        text=text.replace(old,new)
        patches.append({'antes':old,'depois':new,'ocorrencias':count,'posicoes_antes':positions})
    patch('data: ""\n','data: "'+date+'"\n')
    if item['codigo']=='40E46327':
        patch('RESOLUÇÃO Nº 011/2026    CMAS/ITACOATIARA','RESOLUÇÃO Nº 011/2026 – CMAS/ITACOATIARA',3)
    else:
        patch('\n\f\nExtraordinária\n','\n')
    after=text.encode();check=text
    for p in reversed(patches):
        for i,pos in reversed(list(enumerate(p['posicoes_antes']))):
            pos+=i*(len(p['depois'])-len(p['antes']))
            assert check[pos:pos+len(p['depois'])]==p['depois']
            check=check[:pos]+p['antes']+check[pos+len(p['depois']):]
    assert check.encode()==raw
    snapshot=OUT/'snapshots'/item['codigo']/'antes.md';snapshot.parent.mkdir(parents=True,exist_ok=True)
    if snapshot.exists():assert snapshot.read_bytes()==raw
    else:snapshot.write_bytes(raw)
    dest=OUT/'candidatos'/item['destino'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(after)
    diff=''.join(difflib.unified_diff(before.splitlines(True),text.splitlines(True),fromfile=str(source),tofile=str(dest)))
    (snapshot.parent/'delta.diff').write_text(diff)
    original_dest=ROOT/item['destino'];oldcanonical=sha(original_dest.read_bytes()) if original_dest.exists() else None
    assert oldcanonical==item['sha256_destino_atual']
    records.append({'codigo':item['codigo'],'acao':item['delta'],'destino':item['destino'],'sha256_canonico_atual':oldcanonical,'candidato_original':str(source.relative_to(ROOT)),'sha256_candidato_original':sha(raw),'snapshot_antes':str(snapshot.relative_to(ROOT)),'candidato_corrigido':str(dest.relative_to(ROOT)),'sha256_corrigido':sha(after),'correcoes':patches,'fonte':item['fonte'],'pdf':str(Path(item['pdf']).relative_to(ROOT)),'fonte_sha256':item['fonte_sha256'],'uf':item['uf'],'municipio':item['municipio'],'ibge':item['ibge'],'data_propria':date,'data_publicacao':item['data_publicacao'],'prova_bloco_original':item['prova_bloco'],'pipeline_original':pipeline,'limite':'Derivado do pipeline original mais patches manuais documentados; não atribuir estas correções ao classificador original.'})
report={'estado':'proposta corrigida, não aplicada; aguarda revisão do root','revisao_anterior':str(review.relative_to(ROOT)),'sha256_revisao_anterior':sha(review.read_bytes()),'script_sha256':sha(Path(__file__).read_bytes()),'documentos':records,'deltas':{'A':sum(x['acao']=='A' for x in records),'M':sum(x['acao']=='M' for x in records),'D':0},'provas_compartilhadas':{p:sha((BASE/p).read_bytes()) for p in ['renders.json','provas-calendario.json','ibge-identidades.json','recursos-visuais.json','manifesto-provas.json']},'limites':['Fontes PDF completas e renders já lidos permanecem byte a byte iguais; confronto final limitado aos patches documentados, com igualdade reversa de todo o restante.','Datas próprias vêm dos fechos explícitos dos respectivos atos; não das normas citadas ou do calendário de circulação.','Nenhum canônico, candidato original, manifesto original, checkpoint, script do pipeline ou processo foi alterado; sem HTTP/Git.']}
(OUT/'proposta.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('preparados',len(records),report['deltas'],sha((OUT/'proposta.json').read_bytes()))
