import json,hashlib
from pathlib import Path
B=Path('federal/_fonte/auditorias/dpl13-quadros-visuais-20261016')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
limites={
'2168':'Após o fecho de 2167; até Nilo Peçanha e Leopoldo de Bulhões no fim da página.',
'3497':'Início da página 164; tabelas C/D e nota (1) próprias; termina Antonio Francisco de Azeredo antes de 3498.',
'3681':'Começa após 3680 na página 192; tabela e Art.2 na 193; termina Delfim Moreira/Urbano Santos antes de 3682.',
'5018':'Após 5017 na página 45; listas de 24 e 3 entradas nas páginas 46/47; termina Arthur Bernardes/Affonso Penna Junior antes de 5019.',
'5099':'Ato superior da página 124; termina Washington Luis/Arnaldo Siqueira Pinto da Luz antes de 5100.',
'5116':'Início da página 152; quadro continua na 153; termina Washington Luis/Augusto de Vianna antes de 5117.',
'5173':'Após 5172 na página 118; quadro e parágrafo único na 119; termina Washington Luis/Geminiano Lyra Castro antes de 5174.',
'5368':'Após fecho de 5367; termina Washington Luis/Arnaldo Siqueira/Getulio Vargas no fim da página 249.',
'5585':'Após 5584 na página 233; três blocos anuais e totais na 234; termina Art.4 e Washington Luis/Augusto de Vianna na 235 antes de 5586.',
'5597':'Após 5596 na página 243; inclui tabela anexa I e parágrafo II na página 244 após o fecho; não encerrar na assinatura.',
'5633':'Ato integral da página PDF20, primeira página de Atos; Arts.1–2, tabela ouro/papel e fecho Washington Luis/F.C.de Oliveira Botelho.',
'5636':'Após 5635 na página 22; nove credores em duas páginas; termina Art.3 e Washington Luis/F.C.de Oliveira Botelho antes de 5637.',
'5745':'Após correção/fecho Gavotti na página 108; inclui quadros e subtotais nas 109–111; termina Art.5 e três assinaturas na 112 antes de 5746.'}
achados={
'5173':['Parágrafo próprio ausente no HTML: Paragrapho unico. Estes funccionarios gosarão, quanto aos vencimentos, os mesmos favores que os actuaes.'],
'5099':['Quadro impresso com colunas Ord./Grat./Total; encarregado de diligencia não tem valor numérico em Ord.; não preencher zero.'],
'5116':['30:588$351 e 52:447$208 pertencem a posições distintas no quadro; HTML concatena valores.'],
'5368':['Cinco dotações e total em linhas separadas no impresso.'],
'5585':['Blocos anuais têm coluna própria de subtotal; leitura do total impresso requer ampliação antes de transcrição. Nenhum valor corrigido por soma.'],
'5597':['Tabela anexa e parágrafo II pertencem ao ato; regras horizontais não autorizam semântica de inserção.'],
'5018':['Divergência ementa 54:764$750 / Art.2 54:761$750 já existe no impresso; não corrigir por cálculo.'],
'5636':['Grafias de nomes no impresso divergem do HTML; cotejo literal integral ainda necessário.'],
'5745':['Quadros nas páginas 109–111 distinguem valores unitários, adicionais e subtotais por posição e regras horizontais.']}
records=[json.loads(x) for x in Path('federal/_fonte/auditorias/dpl-auditoria-20261016/inventario5409-revisado.jsonl').read_text().splitlines()]
out=[]
for page in json.loads((B/'inventario13-paginas-inicial.json').read_text()):
 n=page['numero'];year=page['ano'];matches=[r for r in records if str(r['metadados'].get('numero'))==n and str(r['metadados'].get('data','')).startswith(str(year))];assert len(matches)==1,(n,len(matches));r=matches[0]
 source=B/f'fonte{year}.json' if year!=1928 else Path('federal/_fonte/auditorias/dpl-ilegiveis-pesquisa-20261016/fonte1928.json')
 provenance=json.loads(source.read_text()); files=[(page['fonte_pdf'],page['fonte_pdf_sha256']),(page['PDF_derivado'],page['PDF_derivado_sha256'])]
 for p in page['paginas']:files.extend([(p['PDF_path'],p['PDF_sha256']),(p['PNG_path'],p['PNG_sha256'])])
 for p,s in files:assert sha(p)==s,p
 current=Path(r['path']).read_bytes();assert hashlib.sha256(current.split(b'---',2)[2]).hexdigest()==r['sha256_corpo'],n
 backup=B/'atos'/n/'HTML-alternativa-md-baseline.json';put(backup,{'path':r['path'],'sha256_md_atual':sha(r['path']),'sha256_corpo':r['sha256_corpo'],'texto':current.decode()})
 out.append({**page,'path_canonico':r['path'],'urn_primario':r['urn'],'data_primaria':r['metadados']['data'],'fonte_HTML_alternativa':r['metadados']['fonte'],'proveniencia_coletanea':provenance,'prova_proveniencia_path':str(source),'prova_proveniencia_sha256':sha(source),'limites_proprios':limites[n],'identidade_data_fecho_conferidos_visualmente':True,'paginas_visualmente_inspecionadas':[p['pagina_PDF'] for p in page['paginas']],'cotejo_literal_integral_HTML_coletanea':False,'achados':achados.get(n,['Fonte visual integral localizada; diferenças de formatação e texto aguardam cotejo integral.']),'backup_md_path':str(backup),'backup_md_sha256':sha(backup),'publicavel':False,'estado':'retido_aguarda_cotejo_literal_e_representacao_fiel'})
put(B/'inventario13-fontes-visuais.json',out)
proof={'atos':len(out),'paginas':sum(len(r['paginas']) for r in out),'fontes_pdf_unicas':len({r['fonte_pdf_sha256'] for r in out}),'todos_hashes_conferidos':True,'corpos_canonicos_inalterados':True,'candidatos_gravados':0,'publicaveis':0,'limite':'Inspeção visual de identidade, limites e estrutura; não substitui cotejo literal integral. Coletânea oficial, não fac-símile DOU.'}
put(B/'validacao-inventario13.json',proof)
helper=B/('inventariar13-'+sha(__file__)+'.py');helper.write_bytes(Path(__file__).read_bytes())
manifest={'estado':'inventario_congelado_sem_aplicacao','escopo':proof,'inventario':{'path':str(B/'inventario13-fontes-visuais.json'),'sha256':sha(B/'inventario13-fontes-visuais.json')},'validacao':{'path':str(B/'validacao-inventario13.json'),'sha256':sha(B/'validacao-inventario13.json')},'helper':{'path':str(helper),'sha256':sha(helper)}}
put('federal/_inventario_dpl13_fontes_visuais_20261016.json',manifest)
print(json.dumps(proof,ensure_ascii=False));print(sha('federal/_inventario_dpl13_fontes_visuais_20261016.json'))
