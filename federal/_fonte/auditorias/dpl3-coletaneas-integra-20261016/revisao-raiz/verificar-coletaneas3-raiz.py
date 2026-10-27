import pathlib,json,hashlib,subprocess,tempfile,gzip,difflib
P=pathlib.Path;B=P('federal/_fonte/auditorias/dpl3-coletaneas-integra-20261016');O=B/'revisao-raiz';O.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=json.loads(P('federal/_preparacao_dpl3_coletaneas_20261016.json').read_text())
for row in manifest['arquivos']:
    assert sha(P(row['path']).read_bytes())==row['sha256'],row['path']
ledgers=[json.loads(x) for x in (B/'ledger3-cotejo-v2.jsonl').read_text().splitlines()]
results=[];seen=set()
with tempfile.TemporaryDirectory(prefix='leis-cotejo-raiz-') as tmp:
    for row in ledgers:
        assert sha(P(row['path']).read_bytes())==row['sha256_antes']
        assert gzip.decompress(P(row['backup_MD']).read_bytes())==P(row['path']).read_bytes()
        body=P(row['candidato']).read_bytes();assert sha(body)==row['sha256_depois']
        pages=json.loads(P(row['paginas_e_render_SHA']).read_text());src=P(pages['source_PDF'])
        assert sha(src.read_bytes())==pages['source_sha256']==row['fonte_coletanea']['sha256_pdf']
        output=[]
        for ix,page in enumerate(pages['paginas']):
            n=page['pagina_PDF_original'];prefix=str(P(tmp)/('p'+row['numero']+'-'+str(n)))
            subprocess.run(['rtk','proxy','pdftoppm','-f',str(n),'-l',str(n),'-scale-to','2200','-singlefile','-png',str(src),prefix],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            original=P(prefix+'.png').read_bytes();assert sha(original)==page['png_sha256']==sha(P(page['png_path']).read_bytes()),(row['numero'],n)
            # Also compare the selected pages in the full-act derivative, independent of extraction metadata.
            subprocess.run(['rtk','proxy','pdftoppm','-f',str(ix+1),'-l',str(ix+1),'-scale-to','2200','-singlefile','-png',pages['PDF_derivado'],prefix+'-deriv'],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            assert P(prefix+'-deriv.png').read_bytes()==original,(row['numero'],n,'derivative')
            output.append({'pagina_PDF':n,'pagina_impressa':page['pagina_impressa'],'PNG_sha256':sha(original),'render_original_derivado_identico':True,'leitura_visual_raiz_trecho_integral':True})
        text=body.decode();deltas=[]
        for num,before,after,pdfpage,printed in [('4743','com o prazo dez dias','com o prazo de dez dias',194,173),('5515','procedente o corpo de delicto, quando','procedente o corpo de delicto. quando',176,142)]:
            if row['numero']==num:
                assert text.count(before)==1
                text=text.replace(before,after)
                deltas.append({'antes_v2':before,'depois_impresso':after,'pagina_PDF':pdfpage,'pagina_impressa':printed,'criterio':'leitura visual independente raiz; preservar impresso'})
        target=P(row['candidato'])
        if deltas:
            target=B/'candidatos-v3'/row['path'];target.parent.mkdir(parents=True,exist_ok=True);new=text.encode()
            if target.exists():assert target.read_bytes()==new
            else:target.write_bytes(new)
            (O/(row['numero']+'-delta-v2-v3.diff')).write_text(''.join(difflib.unified_diff(body.decode().splitlines(True),text.splitlines(True),fromfile=row['candidato'],tofile=str(target))))
        results.append({'numero':row['numero'],'canonico':row['path'],'candidato':str(target),'sha256':sha(target.read_bytes()),'paginas':output,'correcoes_raiz':deltas,'original_HTML_preservado':True,'v2_preservado':True,'status':'aguarda_formato_GFM_identidade_e_aplicacao','normalizacoes_observadas':['ordinais tipograficos normalizados','hifenizacao final de linha unida','tracos longos impressos representados por hifen ASCII no Art1 de4743','titulos e Art/§ com negrito editorial; variacoes de tinta nao reproduzidas como peso de fonte'],'limites':'Leitura visual integral dos trechos dos 3atos nas18paginas; nao certificacao juridica nem fac-simile do DOU. Fontes sao coletaneas oficiais.'})
        print('CONFIRMADO',row['numero'],len(output),'paginas',len(deltas),'correcoes',flush=True)
(O/'verificacao-raiz3.json').write_text(json.dumps({'atos':results,'paginas':18,'correcoes_raiz':2,'canonicos_alterados':0,'HTTP':0},ensure_ascii=False,indent=2)+'\n')
print('PROVA',sha((O/'verificacao-raiz3.json').read_bytes()),flush=True)
