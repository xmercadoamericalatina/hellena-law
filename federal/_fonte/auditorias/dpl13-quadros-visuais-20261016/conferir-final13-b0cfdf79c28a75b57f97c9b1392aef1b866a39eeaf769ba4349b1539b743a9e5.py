import ast,datetime,difflib,gzip,hashlib,json,re,shutil,sys
from pathlib import Path
import html5lib
from cmarkgfm import github_flavored_markdown_to_html as render
from cmarkgfm.cmark import Options
sys.path.insert(0,'scripts')
import auditar
B=Path('federal/_fonte/auditorias/dpl13-quadros-visuais-20261016')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
manual=Path('/tmp/valores_dpl13_papel.json');expected=json.loads(manual.read_text());dest=B/'valores-monetarios-transcricao-manual.json';shutil.copyfile(manual,dest)
notas={
'2168':'Ouro/Papel; quatro células Ouro contêm apenas $. Rótulos próprios sem prefixo Ministerio: Justiça e Negocios Interiores, Marinha, Guerra, Industria e Viação, Fazenda. Totais em linha própria; linhas gráficas no visual.',
'3497':'C: cabeçalho Vencimentos sobre Mensaes/Annuaes com colspan2. D: quantidade separada da categoria para preservar13/169 e subtotais. Valores372$000/360$000 sob Diarias são literais, sem inferência mensal. Matias→matas e20.987→20:987 conforme papel; nota(1) mantida.',
'3681':'Cargos/Ordenado/Gratificação/Vencimentos/Total;12 cargos+totais. Releitura4000px confirma10:800$ na linha4 officiaes (render menor parecia1:800$); nenhum valor alterado por cálculo.',
'5018':'Três quadros: cinco pagamentos;24 entradas numeradas+subtotal;três entradas+subtotal. Mantido12.2 como12. 2 impresso. Foguiste é lapso impresso;Adolpho B. e22$500 confirmados. Ementa ampliada54:761$750, não54:764. Versõesv1–v3 superadas porv4; pontilhados nunca parte do valor monetário.',
'5099':'Ord./Grat./Total: encarregado não tem número na célula Ord., só pontilhado; não inserir zero. Quantidade6 remadores pertence ao rótulo, valores400$/200$/3:600$000 não recalculados.',
'5116':'Nove dotações e total. Valores internos à descrição permanecem nela;30:588$351 e52:447$208 separados conforme posição real. Linha Colonia de Alienados atravessa páginas. Aspa final isolada em Escola de Enfermeiras preservada.',
'5173':'Doze cargos+vencimentos em duas páginas. Parágrafo único presente no papel e omitido no HTML recuperado integralmente. Nenhum total inventado.',
'5368':'Cinco dotações+total em linhas próprias;passagens/commissão/contractados cotejados com papel. Valores250/200/230/420/300 e1.400 contos preservados sem aritmética.',
'5585':'Três blocos anuais com duas posições monetárias: parcela e subtotal à direita da última linha. Totaes18:105$651 preservado emboraArt2diga18:150$561. Não corrigir pela soma. Art3PauloWatzl:papel julho,HTMLjunho;Geminiano não é assinatura deste ato. Nota de divergência exige revisão independente.',
'5597':'Seis artigos+parágrafo único+doisparágrafosArt4+anexoI/IIcompletos. Total132:000$000 em linha própria depois da linha14:400$000. Grafias mostruadios/trasentos impressas preservadas;assinaturaLyra, nãoLyro;Art5Agricola, nãoArgicola.',
'5633':'Sem cabeçalhos de moeda impressos no quadro; células de ausência são travessões e não zero. Ementa/Art1 dão ouro/papel, sem inserir cabeçalho inexistente. Marinha5.840:167$086;mensagem21de novembro;total e assinaturas conferidos.',
'5636':'Nove credores+total;EugenioLatour,CarlosLaubisch&Hirth,SiemensSchuckert conferidos nas duas páginas. Art2entrega completa, nãoentrada;AnnoE literal mantido. Ementa aoMinisterio/outras e fórmula eu sancciono preferem papel, HTML alternativo preservado.',
'5745':'Art1sete verbas+total;Art2nove destinatários+total;Art4c23 destinatários no papel. HTML contém adicionalmenteMiguelCazelli/JoséFerreiradeMesquita, ausentes nestas páginas da coletânea: divergência de versão mantida explícita, sem declarar identidade integral de textos. Art4d três posições com subtotais10:296/7:800/12:000/7:200;Art5vírgula final impressa preservada. Requer revisão especial de versão.'}
rows=json.loads((B/'checkpoint-candidatos13-v2.json').read_text());inventory={r['numero']:r for r in json.loads((B/'inventario13-fontes-visuais.json').read_text())};proof=[]
for r in rows:
 n=r['numero'];i=inventory[n];p=Path(r['candidato']);text=p.read_text();old=json.loads(Path(i['backup_md_path']).read_text())['texto'];assert sha(p)==r['sha256_candidato']
 for key in ('urn','numero','data','tipo','url_metadados'):
  a=re.search(r'(?m)^'+key+r':.*$',old);z=re.search(r'(?m)^'+key+r':.*$',text);assert a.group()==z.group(),(n,key)
 assert '\nrevogada: null\n' in text
 er,wa=auditar.validar(text,str(p),datetime.date(2026,10,16));assert not er and not wa,(n,er,wa)
 rendered=render(text.split('---',2)[2],options=Options.CMARK_OPT_UNSAFE);tree=html5lib.parse(rendered,namespaceHTMLElements=False);tables=[];amounts=[]
 for tab in tree.iter('table'):
  trs=[]
  for tr in tab.iter('tr'):
   cells=[]
   for c in tr:
    if c.tag not in ('td','th'):continue
    value=''.join(c.itertext()).strip();cells.append({'tag':c.tag,'texto':value,'rowspan':c.get('rowspan','1'),'colspan':c.get('colspan','1')})
    if c.tag=='td' and re.fullmatch(r'\d+(?:[.:]\d+)*\$\d*',value):amounts.append(value)
    assert not re.search(r'\d\.{2,}\d.*\$',value),(n,value)
   trs.append(cells)
  tables.append(trs)
 assert amounts==expected[n].split(),n
 assert '<u>' not in rendered and '<ins>' not in rendered,n
 renderpath=B/'atos'/n/(p.stem+'-GFM.html');renderpath.write_text(rendered)
 alts=[]
 for key in ('fonte','url_metadados'):
  url=re.search(r'(?m)^'+key+r': "(.*)"$',old).group(1);cache=Path('federal/_fonte/camara')/(hashlib.sha256(url.encode()).hexdigest()+'.html.gz');assert cache.exists(),cache
  original=cache.read_bytes();snapshot=B/'atos'/n/('alternativa-'+key+'-'+hashlib.sha256(original).hexdigest()+'.html.gz');snapshot.write_bytes(original);alts.append({'tipo':key,'URL':url,'snapshot':str(snapshot),'sha256_gzip':sha(snapshot),'sha256_HTML':hashlib.sha256(gzip.decompress(original)).hexdigest()})
 body=Path(i['path_canonico']).read_bytes().split(b'---',2)[2];backup=json.loads(Path(i['backup_md_path']).read_text())['texto'].encode().split(b'---',2)[2];assert body==backup,n
 proof.append({**r,'paginas':i['paginas'],'proveniencia':i['proveniencia_coletanea'],'alternativas_preservadas':alts,'releitura_interna':notas[n],'cotejo_esperado_numerico':'transcrição manual do papel, separada do parser preparador; não é soma','quantidade_celulas_monetarias_conferidas':len(amounts),'tabelas_GFM':tables,'render':str(renderpath),'render_sha256':sha(renderpath),'vigencia':'Não consta revogação expressa → desconhecida/null; não inferirvigência','normalizacoes_editoriais':['Artigos/ordinais em padrão existente; H1 primário preservado.','Quebras tipográficas de linha reunidas; pontilhados de alinhamento entre texto e valor substituídos pela posição de célula.','Regras horizontais dos subtotais/linhas não são marcação de inserção; visual integral preserva geometria gráfica.'],'alerta_revisao_especial':n in ('5585','5745'),'publicado':False})
put(B/'releitura-interna13-celulas-v2.json',proof)
helper=Path('/tmp/preparar_dpl13_candidatos.py');ast.parse(helper.read_bytes());hp=B/('preparar-candidatos13-'+sha(helper)+'.py');hp.write_bytes(helper.read_bytes())
validation={'formatos':13,'erros':0,'avisos':0,'valores_monetarios_transcritos_manualmente_conferidos':sum(r['quantidade_celulas_monetarias_conferidas'] for r in proof),'identidade_URN_numero_data_tipo_inalterados':True,'corpos_canonicos_inalterados':True,'tabelas_GFM_celulas_e_spans_registrados':True,'revisao_independente':'pendente','aprovacao_publicacao':False}
put(B/'validacao-final13-v2.json',validation)
shutil.copyfile('/tmp/dpl5585-total-alta.png',B/'atos/5585/pagina-234-4000.png');shutil.copyfile('/tmp/dpl2168-alta.png',B/'atos/2168/pagina-110-4000.png')
manifest={'estado':'candidatos_isolados_congelados_aguarda_revisao_independente','canonicos_alterados':0,'quantidade':13,'candidatos':[{'numero':r['numero'],'path':r['candidato'],'sha256':r['sha256_candidato'],'sha256_corpo':r['sha256_corpo']} for r in proof],'helper':{'path':str(hp),'sha256':sha(hp)},'releitura':{'path':str(B/'releitura-interna13-celulas-v2.json'),'sha256':sha(B/'releitura-interna13-celulas-v2.json')},'validacao':validation,'limite':'Cotejo interno de transcrição e estrutura; não aprovação independente. Coletânea não é fac-símile DOU. Nenhum ato promovido automaticamente. Revisão especial5585/5745.'}
manifest['arquivos']=[{'path':str(p),'sha256':sha(p)} for p in sorted(B.rglob('*')) if p.is_file() and p.name not in ('manifesto-final13-v2.json',)]
put(B/'manifesto-final13-v2.json',manifest);print(sha(B/'manifesto-final13-v2.json'));print(validation)
