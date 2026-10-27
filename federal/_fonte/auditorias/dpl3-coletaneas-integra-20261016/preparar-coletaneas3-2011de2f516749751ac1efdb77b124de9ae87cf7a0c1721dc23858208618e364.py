"""Candidatos isolados cotejados com coletâneas oficiais, com diferenças explícitas."""
from pathlib import Path
import json,gzip,re,hashlib,argparse,sys,datetime,difflib
ROOT=Path.cwd();OUT=ROOT/'federal/_fonte/auditorias/dpl3-coletaneas-integra-20261016';SOURCES=ROOT/'federal/_fonte/auditorias/dpl-ilegiveis-pesquisa-20261016';B=ROOT/'federal/_fonte/auditorias/dpl-auditoria-20261016';sys.path.insert(0,str(ROOT/'scripts'));import auditar
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,b,a):
 if a or p.exists():assert p.read_bytes()==b,str(p)
 else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
PATCHES={
'5488':[(156,'a (ilegível) teem direito','a que teem direito')],
'5515':[
(175,'e a srazões de convição','e as razões de convicção'),
(175,'quem a petição fôr dirigida. Paragrapho unico.','quem a petição fôr dirigida.\n\nParagrapho unico.'),
(176,'proceder immeditamente a exaem','proceder immediatamente a exaem'),
(177,'podendo contestar-Ihes','podendo contestar-lhes'),
(178,'que sejam (Ilegível) em auto apartado','que sejam feitas em auto apartado'),
(178,'sem devolução do inquerito que servirá de base, á apresentação','sem devolução do inquerito, que servirá de base á apresentação'),
(178,'é permittida a inerveção, com assistente de terceiro','é permittida a inervenção, com assistente, de terceiro'),
(178,'provada no inquerido a autoria','provada no inquerito a autoria'),
(178,'fazedo lavrar','fazendo lavrar'),
(178,'propriedade das coisas apprehendidas','propriedade das cousas apprehendidas'),
(178,'ou imcoveniencia de linguagem','ou inconveniencia de linguagem'),
(178,'autoridades judiciarias. policiaes','autoridades judiciarias, policiaes'),
(178,'respectivamente censurados em oficio,','respectivamente censurados, em officio,'),
(178,'Côrte de Appelalção','Côrte de Appellação'),
(178,'póde ser inciada','póde ser iniciada'),
(178,'pelo inquerido policial ou administrativo','pelo inquerito policial ou administrativo'),
(178,'**Art. 33.** O nquerito','**Art. 33.** O inquerito'),
(178,'art. 19, paragrapho unico. acompanhará','art. 19, paragrapho unico, acompanhará'),
(179,'as atribuições conferidas aos outros delegados','as attribuições conferidas aos outros delegados'),
(179,'serão cobra-das executivamente','serão cobradas executivamente'),
(179,'de 1910, será, applicado','de 1910, será applicado'),
(180,'WASHINGTON LUIS P. DE SOUSA  \nAugusto de Vianna do Castello\n','WASHINGTON LUIS P. DE SOUSA.  \nAugusto de Vianna do Castello.\n')],
'4743':[
(189,'quando se, tratar de estrangeiros','quando se tratar de estrangeiros'),
(189,'do Codigo Penal. Tratando-se','do Codigo Penal.\n\nTratando-se'),
(189,'as reformas e previdencias convenientes','as reformas e providencias convenientes'),
(189,'ao interesse publico comtanto','ao interesse publico, comtanto'),
(189,'gravura dcsenho,','gravura desenho,'),
(189,'offensa a ali alguma nação','offensa a alguma nação'),
(190,'nacionalidade certa e determinado','nacionalidade certa e determinada'),
(190,'fim de escandalo e (ilegível).','fim de escandalo e aleivosia.'),
(190,'de qualquer natureza desde','de qualquer natureza, desde'),
(190,'dinheiro ou outtro proveito','dinheiro ou outro proveito'),
(190,'A pubIicação de articulados','A publicação de articulados'),
(191,'ou não as reunir:','ou não as reunir;'),
(191,'3º. o dono da officina','3º, o dono da officina'),
(191,'responsabilidade que se Ihe attribue','responsabilidade que se lhe attribue'),
(191,'jornal ou pariodico fôr impresso','jornal ou periodico fôr impresso'),
(191,'os dezeres dessa formalidade','os dizeres dessa formalidade'),
(192,'contados do recebimento a resposta','contados do recebimento, a resposta'),
(192,'*a)*\n\nquando','*a)* quando'),
(192,'*b)*\n\nquando','*b)* quando'),
(192,'*c)*\n\nquando','*c)* quando'),
(193,'a nacionaIidade e folha corrida','a nacionalidade e folha corrida'),
(194,'prescrevem em dous annos. Paragrapho unico.','prescrevem em dous annos.\n\nParagrapho unico.'),
(194,'e a exceptio veritatis,','e a *exceptio veritatis*,'),
(194,'curador á lide,','curador *á lide*,'),
(195,'o prazo de tres para examinar','o prazo de tres dias para examinar'),
(195,'dentro de dez dias sob pena de deserção','dentro de dez dias, sob pena de deserção'),
(195,'celebrada após a do julgamento','celebrada após á do julgamento'),
(195,'com provas literaes incontinenti.','com provas literaes *incontinenti*.'),
(196,'do Codigo PenaI;','do Codigo Penal;'),
(196,'até que a mesma seja apresentada. Si, porém','até que a mesma seja apresentada.\n\nSi, porém'),
(196,'arts. 2º, 3º,e 4º','arts. 2º, 3º e 4º'),
(197,'ARTHUR DA SILVA BERNARDES  \nJoão Luiz Alves\n','ARTHUR DA SILVA BERNARDES.  \nJoão Luiz Alves.\n')]}
# Grafias/lapsos impressos deliberadamente preservados, sem normalização.
PRESERVED={'5488':['teem direito','tem direito'],'5515':['exaem','aso peritos','Recebidas e distribuidas','dntro de 24 horas','No relatoria','incompmunicabilidade','inervenção','sete artigo','da-nutum'],'4743':['ou autores ou editores','sob pna de multa','o prazo dez dias']}
def run(audit=False):
 inv={r['metadados'].get('numero'):r for r in map(json.loads,(B/'inventario5409-revisado.jsonl').read_text().splitlines()) if r['metadados'].get('numero') in PATCHES};assert len(inv)==3;ledger=[]
 for n in ('5488','5515','4743'):
  r=inv[n];path=r['path'];old=(ROOT/path).read_bytes();assert sha(old)==r['sha256_md'];backup=OUT/n/'backup-MD-original.md.gz';write(backup,gzip.compress(old,mtime=0),audit);body=old.decode().split('---',2)[2];changes=[]
  for page,before,after in PATCHES[n]:
   assert body.count(before)==1,(n,before,body.count(before));offset=body.index(before);body=body[:offset]+after+body[offset+len(before):];changes.append({'pagina_PDF':page,'pagina_impressa':page-(21 if n=='4743' else 34),'antes_HTML':before,'depois_coletanea':after,'offset_no_passo':offset})
  # Marcadores romanos seguem a pontuação literal da coletânea.
  if n=='5515':
   for label in ('I','II','III'):
    before='\n'+label+' - ';count=body.count(before);assert count==2
    body=body.replace(before,'\n'+label+', ');changes.append({'pagina_PDF':175,'antes_HTML':label+' -','depois_coletanea':label+',','ocorrencias':count})
   for before,after,page in [('policiaes ex-officio','policiaes *ex-officio*',178),('denuncia ou ex-officio','denuncia ou *ex-officio*',178),('são demissiveis da-nutum','são demissiveis *da-nutum*',180)]:
    assert body.count(before)==1;body=body.replace(before,after);changes.append({'pagina_PDF':page,'antes_HTML':before,'depois_coletanea':after,'natureza':'itálico impresso'})
  for literal in PRESERVED[n]:assert literal in body,(n,literal)
  year=1923 if n=='4743' else 1928;info=json.loads((SOURCES/f'fonte{year}.json').read_text());pdfurl=info['arquivo_vinculado'];header=old.decode().split('---',2)[1];header=re.sub(r'(?m)^revogada: false$','revogada: null',header);header=re.sub(r'(?m)^versao_texto:.*$','versao_texto: "coletanea_oficial_transcricao_cotejada"',header);header=re.sub(r'(?m)^fonte:.*$','fonte: '+json.dumps(pdfurl),header);header += 'fonte_alternativa_HTML: '+json.dumps(r['metadados']['fonte'])+'\n';header += 'fonte_coletanea: '+json.dumps(info['item_oficial'])+'\n';pages=json.loads((OUT/n/'paginas.json').read_text());pg=pages['paginas'];header += 'paginas_fonte_PDF: '+json.dumps(str(pg[0]['pagina_PDF_original'])+'–'+str(pg[-1]['pagina_PDF_original']))+'\n';header += 'paginas_fonte_impressas: '+json.dumps(str(pg[0]['pagina_impressa'])+'–'+str(pg[-1]['pagina_impressa']))+'\n'
  # Nota documental separada: não apresentar coletânea como scan do DOU.
  lines=body.lstrip().split('\n',1);note='Texto cotejado com a coletânea oficial da Imprensa Nacional digitalizada pela Câmara, nas páginas indicadas nos metadados. O HTML Legin anterior, com lacuna e outras diferenças, foi preservado como fonte alternativa. Esta reprodução não é identificada como fac-símile do DOU.';body='\n\n'+lines[0]+'\n\n> '+note+'\n'+lines[1];new=('---'+header+'---'+body).encode();target=OUT/'candidatos-v2'/path;write(target,new,audit)
  assert sha((ROOT/pages['source_PDF']).read_bytes())==pages['source_sha256']==info['sha256_pdf']
  assert sha((ROOT/pages['PDF_derivado']).read_bytes())==pages['PDF_derivado_sha256']
  for pageproof in pg:
   assert sha((ROOT/pageproof['pdf_path']).read_bytes())==pageproof['pdf_sha256']
   assert sha((ROOT/pageproof['png_path']).read_bytes())==pageproof['png_sha256']
  packed=(ROOT/r['fonte_cache']['snapshot']).read_bytes();assert sha(packed)==r['fonte_cache']['sha256_arquivo'];assert sha(gzip.decompress(packed))==r['fonte_cache']['sha256_fonte']
  errors,warnings=auditar.validar(new.decode(),path,datetime.date(2026,10,16));assert not errors,(n,errors);assert '(ilegível)' not in new.decode().lower()
  diff=''.join(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile=path,tofile=str(target.relative_to(ROOT))));write(OUT/n/'delta-integral-v2.diff',diff.encode(),audit)
  ledger.append({'numero':n,'path':path,'candidato':str(target.relative_to(ROOT)),'sha256_antes':sha(old),'sha256_depois':sha(new),'sha256_corpo_antes':r['sha256_corpo'],'sha256_corpo_depois':sha(new.split(b'---',2)[2]),'fonte_HTML':r['fonte_cache'],'fonte_coletanea':info,'backup_MD':str(backup.relative_to(ROOT)),'paginas_e_render_SHA':str((OUT/n/'paginas.json').relative_to(ROOT)),'diferencas_textuais_formatacao':changes,'lapsos_impressos_preservados':PRESERVED[n],'revisao_visual_paginas':list(range(pg[0]['pagina_PDF_original'],pg[-1]['pagina_PDF_original']+1)),'limites_normalizacao':['Hifenização de fim de linha, cabeçalhos/pés e quebras de página não transcritos como corpo.','Ordinais tipográficos 1.º/1.° normalizados como1º; rótulos Art./§ em negrito editorial.','Candidatos isolados requerem revisão independente raiz; não aplicados.'],'formato_erros':errors,'formato_avisos':warnings,'aplicado':False})
 data=''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in ledger).encode();write(OUT/'ledger3-cotejo-v2.jsonl',data,audit);print(json.dumps({'candidatos':3,'diferencas_registradas':sum(len(r['diferencas_textuais_formatacao']) for r in ledger),'paginas_visuais':18,'ledger_sha256':sha(data),'HTTP':0,'canonicos_alterados':0}))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--auditar',action='store_true');run(ap.parse_args().auditar)
