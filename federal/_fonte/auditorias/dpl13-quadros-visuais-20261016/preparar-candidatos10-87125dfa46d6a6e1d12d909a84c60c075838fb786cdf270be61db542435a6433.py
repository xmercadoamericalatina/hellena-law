import json,hashlib,re,difflib,sys
from pathlib import Path
B=Path('federal/_fonte/auditorias/dpl13-quadros-visuais-20261016')
I=json.loads((B/'inventario13-fontes-visuais.json').read_text())
def sha(x):return hashlib.sha256(x).hexdigest()
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
tables={
'5018':'',
'3497':'''<table>
<thead><tr><th rowspan="2">Categorias</th><th colspan="2">Vencimentos</th></tr><tr><th>Mensaes</th><th>Annuaes</th></tr></thead>
<tbody>
<tr><td>1 primeiro chimico civil (1)</td><td>1:000$000</td><td>12:000$000</td></tr>
<tr><td>1 segundo chimico militar</td><td>200$000</td><td>2:400$000</td></tr>
<tr><td>3 segundos chimicos civis</td><td>500$000</td><td>18:000$000</td></tr>
<tr><td>1 preparador de laboratorio</td><td>250$000</td><td>3:000$000</td></tr>
<tr><td>1 encarregado geral de electricidade</td><td>450$000</td><td>5:400$000</td></tr>
<tr><td>1 encarregado geral de machinas</td><td>450$000</td><td>5:400$000</td></tr>
<tr><td>1 almoxarife</td><td>400$000</td><td>4:800$000</td></tr>
<tr><td>1 escrivão</td><td>450$000</td><td>5:400$000</td></tr>
<tr><td>1 apontador geral</td><td>250$000</td><td>3:000$000</td></tr>
<tr><td>3 amanuenses de 1ª classe</td><td>350$000</td><td>12:600$000</td></tr>
<tr><td>3 amanuenses de 2ª classe</td><td>300$000</td><td>10:800$000</td></tr>
<tr><td>1 fiel almoxarife</td><td>200$000</td><td>2:400$000</td></tr>
<tr><td>1 feitor das matas</td><td>250$000</td><td>3:000$000</td></tr>
<tr><td>1 guarda geral</td><td>250$000</td><td>3:000$000</td></tr>
<tr><td>1 enfermeiro</td><td>120$000</td><td>1:440$000</td></tr>
<tr><td>1 pratico de pharmacia</td><td>120$000</td><td>1:440$000</td></tr>
<tr><td></td><td></td><td>93:880$000</td></tr>
</tbody></table>

(1) O primeiro chimico, sendo militar, além de seus vencimentos militares, terá a gratificação de 500$000 mensaes.

TABELLA D

<table>
<thead><tr><th colspan="2">Categorias</th><th>Diarias</th><th>Vencimento annual</th></tr></thead>
<tbody>
<tr><td>3</td><td>mestres de 1ª classe</td><td>372$000</td><td>13:392$000</td></tr>
<tr><td>10</td><td>mestres de 2ª classe</td><td>360$000</td><td>43:200$000</td></tr>
<tr><td>13</td><td></td><td></td><td>56:592$000</td></tr>
<tr><td colspan="4">Em um anno de 365 dias:</td></tr>
<tr><td>7</td><td>operarios de 1ª classe</td><td>9$000</td><td>22:995$000</td></tr>
<tr><td>10</td><td>operarios de 2ª classe</td><td>8$000</td><td>29:200$000</td></tr>
<tr><td>23</td><td>operarios de 3ª classe</td><td>7$000</td><td>58:765$000</td></tr>
<tr><td>19</td><td>operarios de 4ª classe</td><td>6$000</td><td>41:610$000</td></tr>
<tr><td>14</td><td>operarios de 5ª classe</td><td>5$000</td><td>25:550$000</td></tr>
<tr><td>8</td><td>aprendizes de 1ª classe</td><td>2$000</td><td>5:840$000</td></tr>
<tr><td>22</td><td>aprendizes de 2ª classe</td><td>1$500</td><td>12:045$000</td></tr>
<tr><td>43</td><td>serventes de 1ª classe</td><td>3$000</td><td>47:085$000</td></tr>
<tr><td>23</td><td>serventes de 2ª classe</td><td>2$500</td><td>20:987$500</td></tr>
<tr><td>169</td><td></td><td></td><td>264:077$500</td></tr>
</tbody></table>''',
'5597':'''|  | Ord. | Grat. | Total |
| --- | --- | --- | --- |
| 1 director (em commissão) | 14:400$000 | 7:200$000 | 21:600$000 |
| 1 secretario | 10:000$000 | 5:000$000 | 15:000$000 |
| 1 encarregado dos mostruarios | 10:000$000 | 5:000$000 | 15:000$000 |
| 1 encarregado do serviço de informações | 10:000$000 | 5:000$000 | 15:000$000 |
| 1 archivista-bibliothecario | 10:000$000 | 5:000$000 | 15:000$000 |
| 5 auxiliares | 4:800$000 | 2:400$000 | 36:000$000 |
| 2 dactylographos | 4:800$000 | 2:400$000 | 14:400$000 |
|  |  |  | 132:000$000 |''',
'5636':'''|  |  |
| --- | --- |
| Winckler Fallart & Comp. | 408:252$400 |
| S. A. Casa Arens | 808:330$260 |
| David Accarino | 26:600$000 |
| Oscar Flues & Comp. | 1.370:009$540 |
| Companhia Marcenaria Auler | 289:016$000 |
| Companhia Brasileira de Electricidade Siemens Schuckert | 4.532:569$409 |
| Carlos Oswaldo e Eugenio Latour | 23:200$000 |
| Carlos Laubisch & Hirth | 108:000$000 |
| E. Coulit & Comp. | 4:223$500 |
|  | 7.570:201$109 |''',
'3681':'''| Cargos | Ordenado | Gratificação | Vencimentos | Total |
| --- | --- | --- | --- | --- |
| 1 secretario | 9:600$ | 4:800$ | 14:400$ | 14:400$000 |
| 1 sub-secretario | 8:000$ | 4:000$ | 12:000$ | 12:000$000 |
| 4 officiaes | 7:200$ | 3:600$ | 10:800$ | 43:200$000 |
| 1 official archivista | 7:200$ | 3:600$ | 10:800$ | 10:800$000 |
| 8 escripturarios | 5:600$ | 2:800$ | 8:400$ | 67:200$000 |
| 12 amanuenses | 4:000$ | 2:000$ | 6:000$ | 72:000$000 |
| 1 thesoureiro | 7:200$ | 3:600$ | 10:800$ | 10:800$000 |
| 1 fiel de thesoureiro | 3:600$ | 1:800$ | 5:400$ | 5:400$000 |
| 4 telephonistas | 2:400$ | 1:200$ | 3:600$ | 14:400$000 |
| 1 porteiro | 3:200$ | 1:600$ | 4:800$ | 4:800$000 |
| 8 continuos | 2:000$ | 1:000$ | 3:000$ | 24:000$000 |
| 12 serventes | 1:200$ | 600$ | 1:800$ | 21:600$000 |
|  | 61:200$ | 30:600$ | 91:800$ | 300:600$000 |''',
'5173':'''|  |  |
| --- | --- |
| Director geral | 18:000$000 |
| Assistente | 12:000$000 |
| Botanico | 12:000$000 |
| Inspector geral | 10:800$000 |
| Secretario | 8:400$000 |
| Escripturario | 6:000$000 |
| Dactylographo (dous) | 7:200$000 |
| Conservador do museu | 4:800$000 |
| Porteiro-continuo | 3:600$000 |
| Servente | 2:400$000 |
| Director do Horto (nos Estados) | 10:800$000 |
| Ajudante-agronomo (nos Estados) | 9:600$000 |''',
'2168':'''|  | Ouro | Papel |
| --- | --- | --- |
| Justiça e Negocios Interiores | $ | 410:211$299 |
| Marinha | $ | 16:543$821 |
| Guerra | $ | 158:271$336 |
| Industria e Viação | $ | 27:559$873 |
| Fazenda | 72:506$903 | 92:713$920 |
|  | 72:506$903 | 705:300$249 |''',
'5633':'''|  |  |  |
| --- | --- | --- |
| Pelo Ministerio da Justiça e Negocios Interiores | — | 15:200$000 |
| Pelo Ministerio do Exterior | 110:000$000 | 180:000$000 |
| Pelo Ministerio da Marinha | — | 5.840:167$086 |
| Pelo Ministerio da Guerra | 300:000$000 | 10.496:523$215 |
| Pelo Ministerio da Fazenda | — | 1.791:255$115 |
| Total | 410:000$000 | 18.323:145$416 |''',
'5099':'''|  | Ord. | Grat. | Total |
| --- | --- | --- | --- |
| 1 secretario civil | 2:000$ | 1:000$ | 3:000$000 |
| 1 encarregado de diligencia | ...... | 1:756$ | 1:756$000 |
| 1 auxiliar de escripta | 1:000$ | 500$ | 1:500$000 |
| 1 motorista | 1:200$ | 600$ | 1:800$000 |
| 1 patrão | 450$ | 225$ | 675$000 |
| 6 remadores | 400$ | 200$ | 3:600$000 |''',
'5368':'''|  |  |
| --- | --- |
| Addidos navaes, vencimento e gratificações | 250:000$000 |
| Commissões no estrangeiro para aperfeiçoamento de estudo | 200:000$000 |
| Passagens, ajuda de custo, correspondencia postal e telegraphica, objectos de expediente e passagens ás familias | 230:000$000 |
| Missão naval — vencimentos, passagens, frétes, transporte de bagagens, etc., e vencimentos a profissionaes technicos contractados para a Marinha | 420:000$000 |
| Vencimentos do pessoal em commissão no estrangeiro, acquisição de material no estrangeiro, etc. | 300:000$000 |
| Total | 1.400:000$000 |'''}
out=[]
for n,table in tables.items():
 r=next(x for x in I if x['numero']==n);old=json.loads(Path(r['backup_md_path']).read_text())['texto'];header,body=old.split('---',2)[1:]
 if n=='5099':
  start=body.index('Ord. Grat. Total');end=body.index('\n\n**Art. 3º**',start);body=body[:start]+table+body[end:]
  body=body.replace('Crêa uma capitania de 3ª classe no Estado de Minas Geraes\n','*Crêa uma capitania de 3ª classe no Estado de Minas Geraes.*\n')
  body=body.replace('WASHINGTON LUIS P. DE SOUZA  \nArnaldo Siqueira Pinto da Luz','WASHINGTON LUIS P. DE SOUZA.  \n*Arnaldo Siqueira Pinto da Luz.*')
 elif n=='5368':
  start=body.index('Addidos navaes');end=body.index('\n\n**Art. 2º**',start);body=body[:start]+table+body[end:]
  body=body.replace('Brasil: Faço saber','Brasil:\n\nFaço saber')
  body=body.replace('5156,','5.156,')
  body=body.replace('Altera o art. 4º da lei n. 5.156, de 12 de janeiro de 1927, verba "30", do orçamento da Marinha\n','*Altera o art. 4º da lei n. 5.156, de 12 de janeiro de 1927, verba “30”, do orçamento da Marinha*\n')
  body=body.replace('verba "30" do orçamento','verba “30” do orçamento')
  body=body.replace('Arnaldo Siqueira Pinto da Luz.  \nGetulio Vargas.','*Arnaldo Siqueira Pinto da Luz.*  \n*Getulio Vargas.*')
 elif n=='2168':
  start=body.index('|  | Ouro');end=body.index('\n\nRio de Janeiro',start);body=body[:start]+table+body[end:]
  body=body.replace('NILO PEÇANHA  \nLeopoldo de Bulhões','NILO PEÇANHA.  \n*Leopoldo de Bulhões.*')
 elif n=='5633':
  start=body.index('| Pelo Ministerio');end=body.index('\n\n**Art. 2º**',start);body=body[:start]+table+body[end:]
  body=body.replace('mensagem de 21 novembro','mensagem de 21 de novembro')
  body=body.replace('Autoriza a abrir creditos especiaes até os limites de 410:000$000, ouro, e 18.323:145$416, papel, para fazer face a despezas effectuadas em 1928\n','*Autoriza a abrir creditos especiaes até os limites de 410:000$000, ouro, e 18.323:145$416, papel, para fazer face a despezas effectuadas em 1928*\n')
  body=body.replace('WASHINGTON LUIS P. DE SOUSA  \nF. C. de Oliveira Botelho','WASHINGTON LUIS P. DE SOUSA.  \n*F. C. de Oliveira Botelho.*')
 elif n=='5173':
  start=body.index('Director geral');end=body.index('\n\n**Art. 3º**',start);body=body[:start]+table+'\n\nParagrapho unico. Estes funccionarios gosarão, quanto aos vencimentos, os mesmos favores que os actuaes.'+body[end:]
  e='Autoriza o Poder Executivo a despender a verba necessaria á installação e organização do Serviço Florestal do Brasil e altera a tabella de vencimentos dos seus funccionarios';body=body.replace(e+'\n','*'+e+'*\n')
  body=body.replace('WASHINGTON LUIS P. DE SOUSA  \nGeminiano Lyra Castro','WASHINGTON LUIS P. DE SOUSA.  \n*Geminiano Lyra Castro.*')
 elif n=='3681':
  start=body.index('| Cargos');end=body.index('\n\n**Art. 2º**',start);body=body[:start]+table+body[end:]
  e='Substitue a tabella de vencimentos annexa ao decreto n. 6.439, de 30 de março de 1907';body=body.replace(e+'\n','**'+e+'**\n')
  body=body.replace('DELFIM MOREIRA DA COSTA RIBEIRO  \nUrbano Santos da Costa Araujo','DELFIM MOREIRA DA COSTA RIBEIRO.  \n*Urbano Santos da Costa Araujo.*')
 elif n=='5636':
  start=body.index('Winckler Fallart & Comp.');end=body.index('\n\n**Art. 2º**',start);body=body[:start]+table+body[end:]
  e=body[body.index('\n\n',body.index('# '))+2:body.index('\n\nO Presidente')];new_e='Autoriza a abrir, ao Ministerio da Fazenda, o credito especial de 7.570:201$109, para saldar os compromissos contractuaes assumidos pela “Revista do Supremo Tribunal”, e dá outras providencias';body=body.replace(e,'*'+new_e+'*',1)
  for a,z in [('da República dos','da Republica dos'),('decretou e ou sanciono','decretou e eu sancciono'),('Winckler Fallart ,','Winckler Fallart,'),('Carlos Laubisch Hirth Comp.','Carlos Laubisch, Hirth Comp.'),('da entrada completa','da entrega completa'),('Anno "E"','Anno “E”'),('da" Revista do Supremo Tribunal"','da “Revista do Supremo Tribunal”'),('Sociedade Anonyma "Revista do Supremo Tribunal"','Sociedade Anonyma “Revista do Supremo Tribunal”'),('fornecimentos ,fixados','fornecimentos, fixados'),('Rio de janeiro,','Rio de Janeiro,'),('WASHINGTON LUIS P. DE SOUSA  \nF. C. de Oliveira Botelho','WASHINGTON LUIS P. DE SOUSA.  \n*F. C. de Oliveira Botelho.*')]:body=body.replace(a,z)
 elif n=='5597':
  start=body.index('|  | Ord');end=body.index('\n\nII -',start);body=body[:start]+table+body[end:]
  body=body.replace('Crêa o Instituto de Expansão Commercial\n','*Crêa o Instituto de Expansão Commercial*\n')
  for a,z in [('seguinte: 1 director;','seguinte:\n\n1 director;'),('; 1 secretario;',';  \n1 secretario;'),('; 1 encarregado',';  \n1 encarregado'),('; 2 auxiliares',';  \n2 auxiliares'),('; 3 auxiliares',';  \n3 auxiliares'),('; 1 archivista',';  \n1 archivista'),('; 2 escreventes',';  \n2 escreventes'),('dactylographos. Esses','dactylographos.\n\nEsses'),('annexa. Paragrapbo unico.','annexa.\n\nParagrapho unico.'),('mosturadios','mostruadios'),('**§ 1** º','**§ 1º**'),('Museu Argicola','Museu Agricola'),('Geminiano Lyro Castro.','*Geminiano Lyra Castro.*'),('I - Pessoal permanente','*I — Pessoal permanente*'),('II - Pessoal variavel e contractado','*II — Pessoal variavel e contractado*')]:body=body.replace(a,z)
 elif n=='3497':
  start=body.index('| Categorias');end=body.index('\n\n**Art. 4º**',start);body=body[:start]+table+body[end:]
  body=body.replace('O número e os vencimentos','O numero e os vencimentos')
  body=body.replace('Vice-Presidente do Senado,  \nFaço saber','Vice-Presidente do Senado, faço saber')
  body=body.replace('ANTONIO FRANCISCO DE AZEREDO\n','ANTONIO FRANCISCO DE AZEREDO.\n')
 elif n=='5018':
  def tabela_bloco(bloco):
   linhas=[]
   for linha in bloco.strip().split('\n\n'):
    linha=linha.replace('\\.','.');m=re.search(r'([\d.:]+\$\d*)\s*$',linha);assert m,linha
    desc=linha[:m.start()].rstrip(' .');desc=re.sub(r'\s+\.\s*$','',desc).rstrip(' .');linhas.append('| '+desc+' | '+m.group(1)+' |')
   return '|  |  |\n| --- | --- |\n'+'\n'.join(linhas)
  start=body.index('Ao interprete');end=body.index('\n\n**Art. 2º**',start);body=body[:start]+tabela_bloco(body[start:end])+body[end:]
  start=body.index('1\\. Director');end=body.index('\n\ng) ',start);body=body[:start]+tabela_bloco(body[start:end])+body[end:]
  start=body.index('1\\. Redactor');end=body.index('\n\nII. ',start);body=body[:start]+tabela_bloco(body[start:end])+body[end:]
  for a,z in [('Adolpho B, Nogueira','Adolpho B. Nogueira'),('22.$500','22$500'),('pagamenmto','pagamento'),('1925, A razão','1925, á razão'),('12.2 Dactylographo','12. 2 Dactylographo'),('Affonso Penna Junior.','*Affonso Penna Junior.*')]:body=body.replace(a,z)
  for al in 'abcdef':body=body.replace('*'+al+')*\n\n','*'+al+')* ')
  e=body[body.index('\n\n',body.index('# '))+2:body.index('\n\nO Presidente')];body=body.replace(e,'*'+e+'*',1)
 if n=='5636':header=re.sub(r'(?m)^ementa:.*$',lambda m:'ementa: '+json.dumps(new_e,ensure_ascii=False),header)
 src=r['proveniencia_coletanea'];header=re.sub(r'(?m)^fonte:.*$', 'fonte: '+json.dumps(src['arquivo_vinculado']),header);header=re.sub(r'(?m)^versao_texto:.*$','versao_texto: "coletanea_oficial_transcricao_cotejada"',header);header=re.sub(r'(?m)^revogada:.*$','revogada: null',header)
 header+='fonte_alternativa_HTML: '+json.dumps(r['fonte_HTML_alternativa'])+'\nfonte_coletanea: '+json.dumps(src['item_oficial'])+'\nfonte_pdf_sha256: '+json.dumps(r['fonte_pdf_sha256'])+'\npaginas_PDF: '+json.dumps([p['pagina_PDF'] for p in r['paginas']])+'\npaginas_impressas: '+json.dumps([p['pagina_impressa'] for p in r['paginas']])+'\n'
 note='> Transcrição cotejada com a coletânea oficial digitalizada pela Câmara, indicada nos metadados; não é fac-símile do DOU. O HTML anterior permanece preservado como fonte alternativa. A tabela explicita as posições de colunas do impresso; o PDF e a imagem integrais preservam também os pontilhados e regras gráficas.\n\n'
 pos=body.index('\n\n',body.index('# '))+2;body=body[:pos]+note+body[pos:]
 new='---'+header+'---'+body;dest=B/'atos'/n/'candidato-coletanea-v1.md';dest.write_text(new)
 d={'numero':n,'path_canonico':r['path_canonico'],'candidato':str(dest),'sha256_candidato':sha(new.encode()),'sha256_corpo':sha(body.encode()),'backup':r['backup_md_path'],'backup_sha256':r['backup_md_sha256'],'fonte_visual':r['PDF_derivado'],'fonte_visual_sha256':r['PDF_derivado_sha256'],'fonte_original_sha256':r['fonte_pdf_sha256'],'limites':r['limites_proprios'],'cotejo_literal_integral':True,'estado':'candidato_isolado_aguarda_revisao_independente','diff_unificado':list(difflib.unified_diff(old.splitlines(),new.splitlines(),fromfile='HTML/MD anterior',tofile='coletanea cotejada',lineterm=''))}
 put(B/'atos'/n/'cotejo-v1.json',d);out.append(d)
put(B/('checkpoint-candidatos'+str(len(out))+'-v1.json'),out)
print([(r['numero'],r['sha256_candidato']) for r in out])
