import argparse,gzip,hashlib,json,os,subprocess
from pathlib import Path

ROOT=Path('/Volumes/ExternalSSD/GitHub/constituicao')
PROOF=ROOT/'estaduais/RS/_referencias/reparos-visuais-20261016'
ASSETS=ROOT/'estaduais/RS/_ativos_visuais'
CONFIG=[('dec-53969-2018-id64510.md',range(3,18)),('dec-53894-2018-id64432.md',range(2,5)),('dec-54083-2018-id64692.md',range(10,19))]
sha=lambda b:hashlib.sha256(b).hexdigest()
NOTE='(*) Existem expressões de valores ocultas nas unidades inferiores a R$ 1.000'
def prepare():
    source=json.loads((ROOT/'estaduais/_fonte/auditorias/integralidade-snapshot-20261016.json').read_text())
    PROOF.mkdir(parents=True,exist_ok=True);ASSETS.mkdir(exist_ok=True);records=[]
    for filename,pages in CONFIG:
        r=next(x for x in source['documentos'] if x['path'].endswith(filename));old=(ROOT/r['path']).read_bytes();assert sha(old)==r['md_sha256']
        folder=PROOF/Path(filename).stem;folder.mkdir(exist_ok=True)
        for dst,data in [(folder/'antes.md',old),(folder/'fonte.pdf',gzip.decompress((ROOT/r['cache']).read_bytes()))]:
            if dst.exists():assert dst.read_bytes()==data
            else:dst.write_bytes(data)
        pdf=folder/'fonte.pdf';assert sha(pdf.read_bytes())==r['fonte_sha256']
        text=old.decode();edits=[]
        if filename.startswith('dec-53894'):
            heads=[x for x in text.splitlines() if x.startswith('ANEXO')];assert len(heads)==3
            for head in heads:
                before=head+'\n\n';after=before+'Em R$ milhares*\n\n';assert text.count(before)==1;text=text.replace(before,after);edits.append({'antes':before,'depois':after,'prova_paginas':[heads.index(head)+2]})
            before='Principais critérios utilizados:';assert text.count(before)==2
            text=text.replace(before,NOTE+'\n\n'+before);edits.append({'antes':before,'depois':NOTE+'\n\n'+before,'ocorrencias':2,'prova_paginas':[2,3]})
            before='Resultados bimestrais decorrentes';assert text.count(before)==1;text=text.replace(before,NOTE+'\n\n¹ '+before);edits.append({'antes':before,'depois':NOTE+'\n\n¹ '+before,'prova_paginas':[4]})
            before='Desdobramentos bimestrais da meta anual';assert text.count(before)==1;text=text.replace(before,'² '+before);edits.append({'antes':before,'depois':'² '+before,'prova_paginas':[4]})
        visual='\n\n## Anexos em reprodução da publicação original\n\n[PDF da fonte oficial preservado](../../_referencias/reparos-visuais-20261016/'+Path(filename).stem+'/fonte.pdf)\n'
        assets=[]
        for n in pages:
            dst=folder/f'pagina-{n:02d}';png=dst.with_suffix('.png')
            cmd=['rtk','proxy','pdftoppm','-f',str(n),'-l',str(n),'-scale-to','2600','-png','-singlefile',str(pdf),str(dst)]
            if not png.exists():subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            b=png.read_bytes();h=sha(b);asset=ASSETS/(h+'.png')
            if asset.exists():assert asset.read_bytes()==b
            else:asset.write_bytes(b)
            visual+='\n![Anexo da publicação original, página '+str(n)+'](../../_ativos_visuais/'+h+'.png)\n'
            assets.append({'pagina_pdf':n,'path':str(asset.relative_to(ROOT)),'sha256':h,'render_prova':str(png.relative_to(ROOT)),'pagina_inteira_sem_recorte':True,'comando':cmd})
        new=(text.rstrip()+visual+'\n').encode();assert old.split(b'---\n',2)[1]==new.split(b'---\n',2)[1]
        check=text
        for e in reversed(edits):check=check.replace(e['depois'],e['antes'])
        assert check.encode()==old
        candidate=folder/'candidato.md';candidate.write_bytes(new)
        records.append({'path':r['path'],'cache':r['cache'],'sha256_fonte':r['fonte_sha256'],'sha256_antes':sha(old),'sha256_depois':sha(new),'snapshot':str((folder/'antes.md').relative_to(ROOT)),'candidato':str(candidate.relative_to(ROOT)),'pdf_preservado':str(pdf.relative_to(ROOT)),'assets':assets,'edicoes_literais':edits,'sha256_bloco_visual':sha(visual.encode()),'metadados_inalterados':True,'corpo_anterior_preservado_exceto_edicoes_literais':True})
    ledger={'estado':'preparado, não aplicado','documentos':records,'limites':['Restauração visual por páginas inteiras renderizadas do PDF oficial; não redesenho ou OCR de cifras.','O texto preexistente é mantido; não se certifica a transcrição literal de todas as palavras/células já presentes.','Somente trechos de unidade monetária/notas de53894 foram acrescidos literalmente após confronto visual das páginas2–4.'],'script_sha256':sha(Path(__file__).read_bytes())}
    (PROOF/'ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n');print('preparados',len(records),'assets',sum(len(x['assets']) for x in records),flush=True)
def apply():
    ledger=json.loads((PROOF/'ledger.json').read_text());assert ledger['estado']=='preparado, não aplicado'
    for r in ledger['documentos']:
        assert sha((ROOT/r['path']).read_bytes())==r['sha256_antes'];assert sha((ROOT/r['snapshot']).read_bytes())==r['sha256_antes'];assert sha((ROOT/r['candidato']).read_bytes())==r['sha256_depois'];assert sha((ROOT/r['pdf_preservado']).read_bytes())==r['sha256_fonte']
        for x in r['assets']:assert sha((ROOT/x['path']).read_bytes())==x['sha256']
    for r in ledger['documentos']:
        path=ROOT/r['path'];tmp=path.with_suffix('.md.visual-tmp');tmp.write_bytes((ROOT/r['candidato']).read_bytes());os.replace(tmp,path)
    ledger['estado']='aplicado reversivelmente; aguarda revisão/publicação';(PROOF/'ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n');print('aplicados',len(ledger['documentos']))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--aplicar',action='store_true');args=ap.parse_args();apply() if args.aplicar else prepare()
