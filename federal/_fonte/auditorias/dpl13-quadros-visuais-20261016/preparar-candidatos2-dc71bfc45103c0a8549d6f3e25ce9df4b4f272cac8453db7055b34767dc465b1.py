import json,hashlib,re,difflib,sys
from pathlib import Path
B=Path('federal/_fonte/auditorias/dpl13-quadros-visuais-20261016')
I=json.loads((B/'inventario13-fontes-visuais.json').read_text())
def sha(x):return hashlib.sha256(x).hexdigest()
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
tables={
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
 else:
  start=body.index('Addidos navaes');end=body.index('\n\n**Art. 2º**',start);body=body[:start]+table+body[end:]
  body=body.replace('Brasil: Faço saber','Brasil:\n\nFaço saber')
  body=body.replace('5156,','5.156,')
  body=body.replace('Altera o art. 4º da lei n. 5.156, de 12 de janeiro de 1927, verba "30", do orçamento da Marinha\n','*Altera o art. 4º da lei n. 5.156, de 12 de janeiro de 1927, verba “30”, do orçamento da Marinha*\n')
  body=body.replace('verba "30" do orçamento','verba “30” do orçamento')
  body=body.replace('Arnaldo Siqueira Pinto da Luz.  \nGetulio Vargas.','*Arnaldo Siqueira Pinto da Luz.*  \n*Getulio Vargas.*')
 src=r['proveniencia_coletanea'];header=re.sub(r'(?m)^fonte:.*$', 'fonte: '+json.dumps(src['arquivo_vinculado']),header);header=re.sub(r'(?m)^versao_texto:.*$','versao_texto: "coletanea_oficial_transcricao_cotejada"',header)
 header+='fonte_alternativa_HTML: '+json.dumps(r['fonte_HTML_alternativa'])+'\nfonte_coletanea: '+json.dumps(src['item_oficial'])+'\nfonte_pdf_sha256: '+json.dumps(r['fonte_pdf_sha256'])+'\npaginas_PDF: '+json.dumps([p['pagina_PDF'] for p in r['paginas']])+'\npaginas_impressas: '+json.dumps([p['pagina_impressa'] for p in r['paginas']])+'\n'
 note='> Transcrição cotejada com a coletânea oficial digitalizada pela Câmara, indicada nos metadados; não é fac-símile do DOU. O HTML anterior permanece preservado como fonte alternativa. A tabela explicita as posições de colunas do impresso; o PDF e a imagem integrais preservam também os pontilhados e regras gráficas.\n\n'
 pos=body.index('\n\n',body.index('# '))+2;body=body[:pos]+note+body[pos:]
 new='---'+header+'---'+body;dest=B/'atos'/n/'candidato-coletanea-v1.md';dest.write_text(new)
 d={'numero':n,'path_canonico':r['path_canonico'],'candidato':str(dest),'sha256_candidato':sha(new.encode()),'sha256_corpo':sha(body.encode()),'backup':r['backup_md_path'],'backup_sha256':r['backup_md_sha256'],'fonte_visual':r['PDF_derivado'],'fonte_visual_sha256':r['PDF_derivado_sha256'],'fonte_original_sha256':r['fonte_pdf_sha256'],'limites':r['limites_proprios'],'cotejo_literal_integral':True,'estado':'candidato_isolado_aguarda_revisao_independente','diff_unificado':list(difflib.unified_diff(old.splitlines(),new.splitlines(),fromfile='HTML/MD anterior',tofile='coletanea cotejada',lineterm=''))}
 put(B/'atos'/n/'cotejo-v1.json',d);out.append(d)
put(B/'checkpoint-candidatos2-v1.json',out)
print([(r['numero'],r['sha256_candidato']) for r in out])
