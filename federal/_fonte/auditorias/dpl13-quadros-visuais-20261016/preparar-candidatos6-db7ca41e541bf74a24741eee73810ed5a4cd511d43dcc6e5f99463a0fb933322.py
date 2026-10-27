import json,hashlib,re,difflib,sys
from pathlib import Path
B=Path('federal/_fonte/auditorias/dpl13-quadros-visuais-20261016')
I=json.loads((B/'inventario13-fontes-visuais.json').read_text())
def sha(x):return hashlib.sha256(x).hexdigest()
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
tables={
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
 src=r['proveniencia_coletanea'];header=re.sub(r'(?m)^fonte:.*$', 'fonte: '+json.dumps(src['arquivo_vinculado']),header);header=re.sub(r'(?m)^versao_texto:.*$','versao_texto: "coletanea_oficial_transcricao_cotejada"',header);header=re.sub(r'(?m)^revogada:.*$','revogada: null',header)
 header+='fonte_alternativa_HTML: '+json.dumps(r['fonte_HTML_alternativa'])+'\nfonte_coletanea: '+json.dumps(src['item_oficial'])+'\nfonte_pdf_sha256: '+json.dumps(r['fonte_pdf_sha256'])+'\npaginas_PDF: '+json.dumps([p['pagina_PDF'] for p in r['paginas']])+'\npaginas_impressas: '+json.dumps([p['pagina_impressa'] for p in r['paginas']])+'\n'
 note='> Transcrição cotejada com a coletânea oficial digitalizada pela Câmara, indicada nos metadados; não é fac-símile do DOU. O HTML anterior permanece preservado como fonte alternativa. A tabela explicita as posições de colunas do impresso; o PDF e a imagem integrais preservam também os pontilhados e regras gráficas.\n\n'
 pos=body.index('\n\n',body.index('# '))+2;body=body[:pos]+note+body[pos:]
 new='---'+header+'---'+body;dest=B/'atos'/n/'candidato-coletanea-v1.md';dest.write_text(new)
 d={'numero':n,'path_canonico':r['path_canonico'],'candidato':str(dest),'sha256_candidato':sha(new.encode()),'sha256_corpo':sha(body.encode()),'backup':r['backup_md_path'],'backup_sha256':r['backup_md_sha256'],'fonte_visual':r['PDF_derivado'],'fonte_visual_sha256':r['PDF_derivado_sha256'],'fonte_original_sha256':r['fonte_pdf_sha256'],'limites':r['limites_proprios'],'cotejo_literal_integral':True,'estado':'candidato_isolado_aguarda_revisao_independente','diff_unificado':list(difflib.unified_diff(old.splitlines(),new.splitlines(),fromfile='HTML/MD anterior',tofile='coletanea cotejada',lineterm=''))}
 put(B/'atos'/n/'cotejo-v1.json',d);out.append(d)
put(B/('checkpoint-candidatos'+str(len(out))+'-v1.json'),out)
print([(r['numero'],r['sha256_candidato']) for r in out])
