from pathlib import Path
import json,hashlib,shutil,subprocess
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');A=B/'estaduais/_indice/_recuperacao-v2-20261016';O=A/'revisao-raiz-sp-res24';O.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
head=subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'],text=True).strip();assert head=='fb687f302f8454a449c2cf8f4aa7f28d8e2a12ce'
assert not subprocess.check_output(['rtk','proxy','git','diff','--cached','--name-only']).strip()
expected={'manifesto-sp-res20.json':'a7491f3c43768ee76f7d1d4884e2a7ed96525a97d65c907f32b88a0d752a9f99','manifesto-sp-res5-tachado.json':'6ecd6ca04382743fdccda8515fc9a5e522478e3388976394fa85f93a2be8631f','sp-res5-overlay-correcao-coverage-navegacao-u.json':'badd52bb917482ac74c3816067f978072b3c665537ce3f99c6e331b8d140b6ff'}
for f,h in expected.items():assert sha((A/f).read_bytes())==h,f
m20=json.loads((A/'manifesto-sp-res20.json').read_text());m5=json.loads((A/'manifesto-sp-res5-tachado.json').read_text())
frozen={}
def rel(p):
    p=Path(p);return str(p.relative_to(B)) if p.is_absolute() else str(p)
for m in (m20,m5):
    for row in m['lista_publicacao_provas']:
        p=rel(row['path']);actual=(B/p).read_bytes();assert sha(actual)==row['sha256'],p
        if p in frozen:assert frozen[p]['sha256']==row['sha256']
        frozen[p]={'path':p,'sha256':row['sha256'],'bytes':len(actual)}
configs={};evidence=[]
for count,folder in ((20,'revisao-raiz-sp-res20'),(4,'revisao-raiz-sp-res4')):
    d=A/folder;cfg=json.loads((d/f'config{count}-raiz.json').read_text());assert len(cfg)==count;configs.update(cfg)
    masks=json.loads((d/'perfil-flags-CSS-raiz-final.json').read_text());assert masks['total']==count
    for r in masks['documentos']:
        assert r['flags_fonte_ausentes']==0 and not r['flags_adicionais_inesperados']
        if r['chars_flags_divergentes']:assert count==20 and '/res-alesp-807-' in r['path'] and r['chars_flags_divergentes']==3 and [x['texto'] for x in r['Bextra_rotulos_permitidos']]==['§2º']
        assert sha((B/cfg[r['path']]).read_bytes())==r['sha256_candidato']
    gh=json.loads((d/f'verificacao-GFM-GitHub{count}-raiz.json').read_text());assert gh['quantidade']==count
    for r in gh['atos']:assert sha((B/cfg[r['path']]).read_bytes())==r['sha256_candidato'] and not r['formato_erros'] and not r['formato_avisos']
    for name in ('perfil-flags-CSS-raiz-final.json',f'verificacao-GFM-GitHub{count}-raiz.json','censo-HTML-estilos-raiz.json'):evidence.append({'path':str((d/name).relative_to(B)),'sha256':sha((d/name).read_bytes())})
for count in (20,5):
    p=A/f'revisao-raiz-sp-res{count}'/f'verificacao-primarios{count}-raiz.json';d=json.loads(p.read_text());assert d['quantidade']==count and d['HEAD']==head and all(not a['HEAD_duplicatas'] for a in d['atos']);evidence.append({'path':str(p.relative_to(B)),'sha256':sha(p.read_bytes())})
overlay=json.loads((A/'revisao-raiz-sp-res4/overlay-candidatos4-raiz.json').read_text())
assert len(overlay['atos'])==4
for r in overlay['atos']:
    prev=(B/r['candidato_previo']).read_bytes();new=(B/r['candidato_final']).read_bytes();assert sha(new)==r['sha256_final'] and sha(prev)==r['sha256_previo'];assert prev.split(b'\n---\n',1)[0]==new.split(b'\n---\n',1)[0]
assert len(configs)==24 and not any('/res-alesp-821-' in p for p in configs)
docs=[]
for r in m20['documentos']+m5['documentos']:
    path=r['path']
    if path not in configs:continue
    current=(B/path).read_bytes();assert sha(current)==r['old_sha256'],path
    snapshot= r.get('snapshot') or str(A.relative_to(B)/'sp-res20/snapshots'/Path(path).relative_to('estaduais/SP'))
    assert (B/snapshot).read_bytes()==current,path
    candidate=(B/configs[path]).read_bytes()
    if r in m20['documentos']:assert sha(candidate)==r['new_sha256'] and candidate.split(b'\n---\n',1)[1]==current.split(b'\n---\n',1)[1]
    docs.append({'path':path,'candidato':configs[path],'old_sha256':r['old_sha256'],'new_sha256':sha(candidate),'snapshot':snapshot})
assert len(docs)==24
approval={'estado':'aprovado_raiz_24_para_publicacao','HEAD_preaplicacao':head,'quantidade':24,'atos':docs,'provas':evidence,'fontes_congeladas':list(frozen.values()),'leitura_contextual_raiz':'25fontes completas lidas;24aprovadas.807/811/812/813/826/827pontilhados sao citacoes parciais de alteracao,nao omissoes novas.806anexoIXdeoutra norma;demaisestatutos/relatorios/documentosfuturosobjetosexternos.811nota republicada preservada.808epigrafe18outubro/fecho03maio literal.','retido821':'Perda de sublinhado; nao publicado canonicamente. Overlay de retratacao do agente preservado.','politica':'20fonte capturada e4compilada(edição capturada);24revogada:null.3Bextras somente rotulo§2º807;4mascaras textuais exatas incluindo tachado. Fontes e candidatos anteriores preservados. CSS externo e pixels nao certificados.'}
ap=O/'aprovacao-publicacao24-raiz.json';ap.write_text(json.dumps(approval,ensure_ascii=False,indent=2)+'\n')
for r in docs:shutil.copyfile(B/r['candidato'],B/r['path']);assert sha((B/r['path']).read_bytes())==r['new_sha256']
pub=B/'estaduais/_publicacao_SP24_raiz_20261016.json';pub.write_text(json.dumps({'quantidade':24,'aprovacao':str(ap.relative_to(B)),'sha256_aprovacao':sha(ap.read_bytes()),'atos':docs,'retido821':approval['retido821']},ensure_ascii=False,indent=2)+'\n')
shutil.copyfile('/tmp/aplicar-SP24-raiz.py',O/'aplicar-SP24-raiz.py')
shutil.copyfile('/tmp/diagnosticar-sp5-raiz.py',A/'revisao-raiz-sp-res5/diagnosticar-texto-raiz.py')
paths=set(frozen)|set(configs)|{str(pub.relative_to(B)),'WORKLOG.md','estaduais/SP/_indice/legislacao_normas.zip'}
for name in ('manifesto-sp-res20.json','manifesto-sp-res5-tachado.json','sp-res20-verificacao-final.json','sp-res20-overlay-coverage-css.json','sp-res20-perfil-css-independente.json','sp-res5-tachado-verificacao-final.json','sp-res5-overlay-correcao-coverage-navegacao-u.json'):paths.add(str((A/name).relative_to(B)))
for folder in ('revisao-raiz-sp-res20','revisao-raiz-sp-res5','revisao-raiz-sp-res4','revisao-raiz-sp-res24'):
    paths.update(str(p.relative_to(B)) for p in (A/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
for p in paths:assert (B/p).is_file(),p
Path('/tmp/SP24-publicacao-paths.txt').write_text('\n'.join(sorted(paths))+'\n')
w=B/'WORKLOG.md';s=w.read_text();note='\n## SP24 aprovado e aplicado — 16/10/2026\n\n-24resoluções SP:20corposbyteiguais+4restaurados805/808/822/829.25fontes integralmente lidas;821retida por U real perdido, nenhum ins substituto. Fonte24texto/máscaraspreservados;3Bextra só§2º807;4restauradosmáscarasexatas. Fontes HTML semtabelas/imagens/controles;GitHub20+4DOMtexto/marcas iguais. XML44+10relações,identidade/datas/tipo19/HEADsemduplicatas.808epígrafedata18out/fecho03maio preservados;811nota republicação preservada.20fontecapturada+4compilada(ediçãocapturada),24null.\n-Navegação69glifos nos5candidatos agente diagnosticada e removida só nos4publicáveis;ementa822HTMLliteral corrigida com H3próprio;overlay agente badd52bb…b6ff retrata coberturaampla.821congelados/fontes/provas mantidos fora canônicos. Aprovação'+sha(ap.read_bytes())+';lista/tmp/SP24-publicacao-paths.txt. Índice/commit/push pendentes,PROGRESSO viahook.\n- Federal overlaycontextual2000 5955ace8…320f:1951semalertaadicional+49retençõesconservadoras(41variantesliterais,8instrumentos/pósassinatura),semaceitehumano/raiz. Nadafederalaplicado.\n';w.write_text(s.replace('# Continuação da coleta\n','# Continuação da coleta\n'+note,1))
print(json.dumps({'canonicos':24,'paths':len(paths),'sha256_aprovacao':sha(ap.read_bytes()),'bytes':sum((B/p).stat().st_size for p in paths)}))
