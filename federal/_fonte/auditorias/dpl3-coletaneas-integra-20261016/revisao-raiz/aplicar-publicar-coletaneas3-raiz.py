from pathlib import Path
import hashlib,json,subprocess,os,shutil
P=Path;B=P('federal/_fonte/auditorias/dpl3-coletaneas-integra-20261016');O=B/'revisao-raiz';sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args,input=None):return subprocess.run(['rtk','proxy','git',*args],input=input,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout
assert not git('diff','--cached','--name-only').strip()
proof=O/'aprovacao-raiz3-final.json';assert sha(proof.read_bytes())=='e0555938b0da8b019d3fd8925453703836abb7ab7e9bdede07c0b3eba23cb002'
doc=json.loads(proof.read_text());m=P('federal/_preparacao_dpl3_coletaneas_20261016.json');assert sha(m.read_bytes())=='816a05568d9763753ae250f102cc036d7cbe312d229c8ded4fa67de8b8292486'
for f in json.loads(m.read_text())['arquivos']:assert sha(P(f['path']).read_bytes())==f['sha256']
for row in doc['atos']:
    assert sha(P(row['canonico']).read_bytes())==row['sha256_antes'];assert sha(P(row['candidato']).read_bytes())==row['sha256']
for row in doc['atos']:
    p=P(row['canonico']);tmp=p.with_suffix('.md.raiz-tmp');tmp.write_bytes(P(row['candidato']).read_bytes());os.replace(tmp,p)
for name in ['verificar-coletaneas3-raiz.py','verificar-coletaneas3-gfm-raiz.py','aplicar-publicar-coletaneas3-raiz.py']:
    shutil.copyfile(P('/tmp')/name,O/name)
shutil.copyfile('/tmp/leis-5515-raiz176-art13.png',O/'5515-art13-ponto-recorte.png')
publication=P('federal/_publicacao_coletaneas3_raiz_20261016.json')
publication.write_text(json.dumps({'estado':'aplicado_raiz_aguarda_commit_push','incremento_documentos':3,'prova':str(proof),'sha256_prova':sha(proof.read_bytes()),'documentos':doc['atos'],'v1_v2_preservados_nao_canonicos':True,'fontes':'coletaneas oficiais Imprensa Nacional digitalizadas pela Camara; nao identificado como fac-simile DOU','originais_PDF_incluidos':True},ensure_ascii=False,indent=2)+'\n')
paths={str(p) for p in B.rglob('*') if p.is_file()}
paths.update([str(m),str(publication),'WORKLOG.md']);paths.update(r['canonico'] for r in doc['atos'])
for num in ['4743','5488','5515']:
    pg=json.loads((B/num/'paginas.json').read_text());paths.add(pg['source_PDF'])
    year='1923' if num=='4743' else '1928';paths.add('federal/_fonte/auditorias/dpl-ilegiveis-pesquisa-20261016/fonte'+year+'.json')
wl=P('WORKLOG.md');s=wl.read_text();entry='## Coletaneas3 aplicadas pela raiz — 16/10/2026\n\n- Raiz aprovou3atos/18páginas lidas e re-renderizadas doPDForiginal e derivado comPNG byteidêntico;2deltasadicionais(4743Art24§3de;5515Art13ponto) emV3. Prova e0555938…cb002. Identidade própria/índice/data/fecho/tipo/formato/GFMcaracteres/pontuação conferidos3,0erros/avisos.\n- OriginaisHTML/MD/v1/v2 preservados;5488usav2inalterado;5515/4743v3. Fontetextualagora coletâneaoficial declarada, mantendoHTMLalternativo, páginas eproveniência. Originais2PDFs29MB incluídos. Nãoéfac-símileDOU/certificaçãojurídica.\n- Aplicados3canônicos novos,aguardaformatoíndice/commit/push,PROGRESSOviahook. Lista/tmp/coletaneas3-publicacao-paths.txt.\n\n';wl.write_text(s.replace('# Continuação da coleta\n\n','# Continuação da coleta\n\n'+entry,1))
paths=sorted(paths)
for path in paths:
    p=P(path);assert p.is_file() and not p.is_symlink() and '\n' not in path and p.stat().st_size<100000000,path
P('/tmp/coletaneas3-publicacao-paths.txt').write_text('\n'.join(paths)+'\n')
oids=git('hash-object','-w','--stdin-paths',input=('\n'.join(paths)+'\n').encode()).decode().splitlines();assert len(oids)==len(paths)
git('update-index','--add','-z','--index-info',input=b''.join(('100644 '+oid+'\t'+path+'\0').encode() for path,oid in zip(paths,oids)))
for row in doc['atos']:assert sha(git('show',':'+row['canonico']))==row['sha256']
print('APLICADOS/STAGED3',len(paths),'arquivos;3SHAindice exatos',flush=True)
