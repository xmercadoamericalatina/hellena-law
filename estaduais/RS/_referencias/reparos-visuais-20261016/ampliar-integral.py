import hashlib,json,os,subprocess
from pathlib import Path
from pypdf import PdfReader
ROOT=Path('/Volumes/ExternalSSD/GitHub/constituicao');BASE=ROOT/'estaduais/RS/_referencias/reparos-visuais-20261016';ASSETS=ROOT/'estaduais/RS/_ativos_visuais'
sha=lambda b:hashlib.sha256(b).hexdigest()
oldledger=BASE/'ledger.json';oldsha=sha(oldledger.read_bytes());assert oldsha=='f7b28b7f41e533bd25a9c18531137fd702a635087606bcd667160d5bf748739d'
old=json.loads(oldledger.read_text());records=[];marker='\n\n## Anexos em reprodução da publicação original\n\n'
for rec in old['documentos']:
    path=ROOT/rec['path'];before=path.read_bytes();assert sha(before)==rec['sha256_depois'];folder=BASE/Path(path).stem;snapshot=folder/'antes-ampliacao-integral.md'
    if snapshot.exists():assert snapshot.read_bytes()==before
    else:snapshot.write_bytes(before)
    text=before.decode();assert text.count(marker)==1;start=text.index(marker);assert sha(text[start:-1].encode())==rec['sha256_bloco_visual'];prefix=text[:start]
    pdf=ROOT/rec['pdf_preservado'];assert sha(pdf.read_bytes())==rec['sha256_fonte'];reader=PdfReader(pdf)
    visual='\n\n## Fonte oficial em reprodução integral\n\n[PDF da fonte oficial preservado](../../_referencias/reparos-visuais-20261016/'+path.stem+'/fonte.pdf)\n';assets=[]
    for n,page in enumerate(reader.pages,1):
        proof=folder/f'pagina-{n:02d}.png';stem=proof.with_suffix('')
        cmd=['rtk','proxy','pdftoppm','-f',str(n),'-l',str(n),'-scale-to','2600','-png','-singlefile',str(pdf),str(stem)]
        if not proof.exists():subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        raw=proof.read_bytes();h=sha(raw);asset=ASSETS/(h+'.png')
        if asset.exists():assert asset.read_bytes()==raw
        else:asset.write_bytes(raw)
        visual+='\n![Fonte oficial, página '+str(n)+'](../../_ativos_visuais/'+h+'.png)\n'
        assets.append({'pagina_pdf':n,'asset':str(asset.relative_to(ROOT)),'sha256_png':h,'prova_render':str(proof.relative_to(ROOT)),'bbox_pagina':[float(x) for x in page.mediabox],'sem_recorte':True,'comando':cmd})
    new=(prefix+visual+'\n').encode();assert new.split(b'---\n',2)[1]==before.split(b'---\n',2)[1];candidate=folder/'candidato-integral.md';candidate.write_bytes(new)
    records.append({'path':rec['path'],'cache':rec['cache'],'fonte_sha256':rec['sha256_fonte'],'pdf_preservado':rec['pdf_preservado'],'snapshot_original':rec['snapshot'],'sha256_original':rec['sha256_antes'],'snapshot_antes_ampliacao':str(snapshot.relative_to(ROOT)),'sha256_antes_ampliacao':sha(before),'candidato':str(candidate.relative_to(ROOT)),'sha256_depois':sha(new),'paginas_total':len(reader.pages),'assets':assets,'prefixo_texto_inalterado_sha256':sha(prefix.encode()),'metadados_inalterados':True})
ledger={'estado':'preparado integral, não aplicado','ledger_anterior':str(oldledger.relative_to(ROOT)),'sha256_ledger_anterior':oldsha,'documentos':records,'script_sha256':sha(Path(__file__).read_bytes()),'limites':['Reprodução de todas40páginas dos3PDFs:18+4+18, incluindo articulado, quadros e anexos.','Preserva integralmente os pixels da renderização em página inteira e o PDF original porSHA; não redesenha nem reconstrói cifras ocultas.','Texto preexistente permanece igual ao reparo anterior; não se certifica literalmente cada palavra/célula da transcrição. Unidade/notas53894 restauradas na fase anterior ficam preservadas.','Nenhuma conclusão geral sobre outrosPDFs, vigência ou integralidade jurídica externa.']}
for rec in records:
    assert sha((ROOT/rec['path']).read_bytes())==rec['sha256_antes_ampliacao'];assert sha((ROOT/rec['snapshot_antes_ampliacao']).read_bytes())==rec['sha256_antes_ampliacao']
for rec in records:
    p=ROOT/rec['path'];tmp=p.with_suffix('.md.integral-tmp');tmp.write_bytes((ROOT/rec['candidato']).read_bytes());os.replace(tmp,p)
ledger['estado']='aplicado reversivelmente, aguarda revisão/publicação';(BASE/'ledger-integral.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n');print('aplicados',len(records),'paginas',sum(x['paginas_total'] for x in records),flush=True)
