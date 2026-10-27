import json,hashlib,re,difflib,sys
from pathlib import Path
B=Path('federal/_fonte/auditorias/dpl13-quadros-visuais-20261016')
I=json.loads((B/'inventario13-fontes-visuais.json').read_text())
AUDIT='--auditar' in sys.argv
def sha(x):return hashlib.sha256(x).hexdigest()
def put(p,v):
 text=json.dumps(v,ensure_ascii=False,indent=2)+'\n'
 if AUDIT:assert p.read_text()==text,str(p)
 else:p.write_text(text)
def tabela2(bloco):
 linhas=[]
 for linha in bloco.strip().split('\n\n'):
  linha=linha.replace('\\.','.');m=re.search(r'(\d+(?:[.:]\d+)*\$\d*)\s*$',linha);assert m,linha
  desc=linha[:m.start()].rstrip(' .');linhas.append('| '+desc+' | '+m.group(1)+' |')
 return '|  |  |\n| --- | --- |\n'+'\n'.join(linhas)
tables={
'5745':'',
'5585':'',
'5116':'''|  |  |
| --- | --- |
| Sub-consignação da verba 13ª — Objectos de expediente, 5:500$000; impressões, publicações e eventuaes, 2:500$000; conservação e limpeza do edificio, 2:500$000 | 10:500$000 |
| Sub-consignação da verba 13ª — Alimentação do Abrigo de Menores (inclusive de pessoal), 80:000$000; medicamentos, drogas, instrumentos dentarios e dietas, 8:000$000; roupa, calçado, concertos, lavagem e engommagem, 14:000$000 | 102:000$000 |
| Sub-consignação 33ª da verba 15ª — “Alimentação” (inclusive do pessoal) e dietas da Colonia Correccional de Dous Rios | 232:981$364 |
| Sub-consignações da verba 15ª — “Policia do Districto Federal”, combustivel e lubrificantes, material de lubrificação e limpeza das lanchas, 8:771$848; telephones, 11:329$109; aluguel de casa para delegacias, estações e postos policiaes, 1:788$; illuminação e força motriz, 30:588$351 | 52:447$208 |
| Sub-consignações da verba 17ª — “Casa de Detenção”, alimentação do pessoal, 68:435$616; alimentação, dietas e curativos dos detentos, 676:406$816; forragem e curativos de animaes, 15:726$400; cumbustivel, lubrificação e material de lubrificação, 18:944$000; custeio e conservação do material rodante, 8:188$800; asseio e desinfecção do estabelecimento e eventuaes, 9:173$333 | 799:874$965 |
| Sub-consignação da verba 21ª, n. 301, consignação “Material” — Escola de Enfermeiras” | 32:143$384 |
| Sub-consignações ns. 230 e 231, do n. 12, da verba 21ª, “Hospital Paula Candido”, “Dietas e alimentação do pessoal” | 62:910$210 |
| Sub-consignações ns. 28 e 45, da verba 20ª, consignação “Material”, “Alimentação e dietas para empregados e doentes, combustivel, lubrificantes e material de lubrificação da Colonia de Alienados” | 179:000$000 |
| Sub-consignação n. 4, consignação “Material”, da verba 27ª, “Alimentação e dietas do Instituto Nacional de Surdos Mudos” | 50:679$040 |
|  | 1.522:566$171 |''',
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
    linha=linha.replace('\\.','.');m=re.search(r'(\d+(?:[.:]\d+)*\$\d*)\s*$',linha);assert m,linha
    desc=linha[:m.start()].rstrip(' .');desc=re.sub(r'\s+\.\s*$','',desc).rstrip(' .');linhas.append('| '+desc+' | '+m.group(1)+' |')
   return '|  |  |\n| --- | --- |\n'+'\n'.join(linhas)
  start=body.index('Ao interprete');end=body.index('\n\n**Art. 2º**',start);body=body[:start]+tabela_bloco(body[start:end])+body[end:]
  start=body.index('1\\. Director');end=body.index('\n\ng) ',start);body=body[:start]+tabela_bloco(body[start:end])+body[end:]
  start=body.index('1\\. Redactor');end=body.index('\n\nII. ',start);body=body[:start]+tabela_bloco(body[start:end])+body[end:]
  for a,z in [('Adolpho B, Nogueira','Adolpho B. Nogueira'),('22.$500','22$500'),('pagamenmto','pagamento'),('1925, A razão','1925, á razão'),('12.2 Dactylographo','12. 2 Dactylographo'),('Affonso Penna Junior.','*Affonso Penna Junior.*')]:body=body.replace(a,z)
  body=body.replace('abrir, pelo Ministerio da Justiça e Negocios Interiores, os creditos especiaes de 200:000$000, 11:276$400, 54:764$750','abrir pelo Ministerio da Justiça e Negocios Interiores, os creditos especiaes de 200:000$000, 11:276$400, 54:761$750')
  header=header.replace('abrir, pelo Ministerio da Justiça e Negocios Interiores, os creditos especiaes de 200:000$000, 11:276$400, 54:764$750','abrir pelo Ministerio da Justiça e Negocios Interiores, os creditos especiaes de 200:000$000, 11:276$400, 54:761$750')
  for al in 'abcdef':body=body.replace('*'+al+')*\n\n','*'+al+')* ')
  e=body[body.index('\n\n',body.index('# '))+2:body.index('\n\nO Presidente')];body=body.replace(e,'*'+e+'*',1)
 elif n=='5116':
  start=body.index('Sub-consignação da verba');end=body.index('\n\n**Art. 2º**',start);body=body[:start]+table+body[end:]
  e=body[body.index('\n\n',body.index('# '))+2:body.index('\n\nO Presidente')];body=body.replace(e,'*'+e+'*',1)
  body=body.replace('31 de dezembro do 1925','31 de dezembro de 1925').replace('Augusto de Vianna do Castello.','*Augusto de Vianna do Castello.*')
 elif n=='5585':
  start=body.index('1926 - Outubro');end=body.index('\n\n**Art. 3.º**',start)
  blocos=[]
  for ano,periodo,meses,ajudante,continuos,demais,subtotal in [('1926','Outubro a dezembro','tres mezes','96$729','1:440$000','240$000','2:016$729'),('1927','Janeiro a dezembro','12 mezes','386$916','5:760$000','960$000','8:066$916'),('1928','Janeiro a dezembro','12 mezes','386$916','5:760$000','960$000','8:066$916')]:
   blocos.append(ano+' — '+periodo+':\n\n|  |  |  |\n| --- | --- | --- |\n| Ajudante de portaria, a 32$243, '+meses+' | '+ajudante+' |  |\n| 12 continuos a 40$, '+meses+' | '+continuos+' |  |\n| 2 motoristas a 40$, '+meses+' | '+demais+' |  |\n| 2 electricistas a 40$, '+meses+' | '+demais+' | '+subtotal+' |')
  blocos[-1]+='\n| Totaes |  | 18:105$651 |';body=body[:start]+'\n\n'.join(blocos)+body[end:]
  for ano,endmark in [('1927','\n\n1928:'),('1928','\n\n**Art. 4º**')]:
   start=body.index(ano+':',body.index('**Art. 3.º**'))+len(ano+':');end=body.index(endmark,start);bloco=body[start:end];rows=[]
   for linha in re.split(r'\s*\n\s*',bloco.strip()):
    if not linha.strip():continue
   bloco=bloco.replace('\n',' ');entries=re.split(r'(?=Ao (?:director|1º|2º|3º|continuo|guarda|redactor)|Para pagamento|5:644\$500\s*$)',bloco)
   for linha in entries:
    if not linha.strip():continue
    m=re.search(r'(\d+(?:[.:]\d+)*\$\d*)\s*$',linha.strip());assert m,linha;desc=linha.strip()[:m.start()].rstrip(' .');rows.append('| '+desc+' | '+m.group(1)+' |')
   body=body[:start]+'\n\n|  |  |\n| --- | --- |\n'+'\n'.join(rows)+body[end:]
  for a,z in [('aos continnos','aos continuos'),('da secretaria do Senado','da Secretaria do Senado'),('director de serviços Adolpho','director de Serviços Adolpho'),('nos mezes de junho a dezembro','nos mezes de julho a dezembro'),('Guimarães, diferença de gratificação','Guimarães, differença de gratificação'),('WASHINGTON LUIS P. DE SOUZA.','WASHINGTON LUIS P. DE SOUSA.'),('Augusto de Vianna do Castello.','*Augusto de Vianna do Castello.*')]:body=body.replace(a,z)
  e=body[body.index('\n\n',body.index('# '))+2:body.index('\n\nO Presidente')];body=body.replace(e,'*'+e+'*',1)
 elif n=='5745':
  body=body.replace('1.169.915$681','1.169:915$681')
  start=body.index("A' verba");end=body.index('\n\n**Art. 2º**',start);body=body[:start]+tabela2(body[start:end])+body[end:]
  start=body.index('Ao 1º official Sylvio');end=body.index('\n\n**Art. 3º**',start);body=body[:start]+tabela2(body[start:end])+body[end:]
  body=body.replace('Ao official, Victor Midosi Chermont, de 15 %,\n\nde 1','Ao official, Victor Midosi Chermont, de 15 %, de 1')
  start=body.index('Ao official, Victor');end=body.index('\n\nd) de 49:391',start);bloco=body[start:end];entries=[x for x in bloco.split('\n\n') if 'Miguel Cazelli' not in x and 'José Ferreira de Mesquita' not in x];body=body[:start]+tabela2('\n\n'.join(entries))+body[end:]
  start=body.index('Ao chefe da Secção');end=body.index('\n\n**Art. 5º**',start);rows=[]
  for linha in body[start:end].strip().split('\n\n'):
   if linha.endswith(':'):rows.append('| '+linha+' |  |  |');continue
   dupla=re.search(r'(\d+(?:[.:]\d+)*\$\d*)\s+(\d+(?:[.:]\d+)*\$\d*)\s*$',linha)
   simples=re.search(r'(\d+(?:[.:]\d+)*\$\d*)\s*$',linha);assert simples,linha
   match=dupla or simples;desc=linha[:match.start()].rstrip(' .');esquerda=dupla.group(1) if dupla else '';direita=dupla.group(2) if dupla else simples.group(1)
   if not dupla and desc in ('Diferença de vencimentos','Differença de vencimentos'):esquerda,direita=direita,''
   rows.append('| '+desc+' | '+esquerda+' | '+direita+' |')
  body=body[:start]+'|  |  |  |\n| --- | --- | --- |\n'+'\n'.join(rows)+body[end:]
  for a,z in [('autorizado a abril,','autorizado a abrir,'),('Tratado de Limites','Tratado de limites'),('efffectuar','effectuar'),('n. III;','n. III,'),('Secretaria do Senado Federal;\n\n|','Secretaria do Senado Federal:\n\n|'),('pagamento de diferença de vencimentos','pagamento de differença de vencimentos'),('da Biblioteca e do Archivo','da Bibliotheca e do Archivo'),('| Diferença de vencimentos','| Differença de vencimentos'),('de Annaes,','de *Annaes*,'),('Ao chauffeur,','Ao *chauffeur*,'),('classe jorge da Silva','classe jorge da Silva'),('Augusto de Vianna do Castello.','*Augusto de Vianna do Castello.*'),('F. C. da Oliveira Botelho.','*F. C. de Oliveira Botelho.*')]:body=body.replace(a,z)
  e=body[body.index('\n\n',body.index('# '))+2:body.index('\n\nO Presidente')];body=body.replace(e,'*'+e+'*',1)
  body=body.replace('**Art. 5º** Revogam-se as disposições em contrario.','**Art. 5º** Revogam-se as disposições em contrario,')
 if n=='5636':header=re.sub(r'(?m)^ementa:.*$',lambda m:'ementa: '+json.dumps(new_e,ensure_ascii=False),header)
 src=r['proveniencia_coletanea'];header=re.sub(r'(?m)^fonte:.*$', 'fonte: '+json.dumps(src['arquivo_vinculado']),header);header=re.sub(r'(?m)^versao_texto:.*$','versao_texto: "coletanea_oficial_transcricao_cotejada"',header);header=re.sub(r'(?m)^revogada:.*$','revogada: null',header)
 header+='fonte_alternativa_HTML: '+json.dumps(r['fonte_HTML_alternativa'])+'\nfonte_coletanea: '+json.dumps(src['item_oficial'])+'\nfonte_pdf_sha256: '+json.dumps(r['fonte_pdf_sha256'])+'\npaginas_PDF: '+json.dumps([p['pagina_PDF'] for p in r['paginas']])+'\npaginas_impressas: '+json.dumps([p['pagina_impressa'] for p in r['paginas']])+'\n'
 note='> Transcrição cotejada com a coletânea oficial digitalizada pela Câmara, indicada nos metadados; não é fac-símile do DOU. O HTML anterior permanece preservado como fonte alternativa. A tabela explicita as posições de colunas do impresso; o PDF e a imagem integrais preservam também os pontilhados e regras gráficas.\n\n'
 pos=body.index('\n\n',body.index('# '))+2;body=body[:pos]+note+body[pos:]
 new='---'+header+'---'+body;version='v4' if n=='5018' else ('v3' if n=='5745' else 'v1');dest=B/'atos'/n/('candidato-coletanea-'+version+'.md')
 if AUDIT:assert dest.read_text()==new,str(dest)
 else:dest.write_text(new)
 d={'numero':n,'path_canonico':r['path_canonico'],'candidato':str(dest),'sha256_candidato':sha(new.encode()),'sha256_corpo':sha(body.encode()),'backup':r['backup_md_path'],'backup_sha256':r['backup_md_sha256'],'fonte_visual':r['PDF_derivado'],'fonte_visual_sha256':r['PDF_derivado_sha256'],'fonte_original_sha256':r['fonte_pdf_sha256'],'limites':r['limites_proprios'],'cotejo_literal_integral':True,'estado':'candidato_isolado_aguarda_revisao_independente','diff_unificado':list(difflib.unified_diff(old.splitlines(),new.splitlines(),fromfile='HTML/MD anterior',tofile='coletanea cotejada',lineterm=''))}
 put(B/'atos'/n/('cotejo-'+version+'.json'),d);out.append(d)
put(B/('checkpoint-candidatos'+str(len(out))+'-v2.json'),out)
print([(r['numero'],r['sha256_candidato']) for r in out])
