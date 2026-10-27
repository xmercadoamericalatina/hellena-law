from pathlib import Path
import json,re,gzip,hashlib,html,subprocess,collections
import html5lib
from cmarkgfm import github_flavored_markdown_to_html as render
from cmarkgfm.cmark import Options
B=Path('estaduais/_indice/_recuperacao-v2-20261016');sha=lambda b:hashlib.sha256(b).hexdigest();VOID={'br','hr','img','meta','link','input','wbr','col','embed','source'}
def tag(e):return e.tag.split('}')[-1] if isinstance(e.tag,str) else ''
def style(e,prior):
 weight,italic=prior;t=tag(e)
 if t in ('b','strong'):weight=700
 if t in ('i','em'):italic=True
 declarations={k.strip().lower():v.strip().lower().replace('!important','').strip() for k,v in (x.split(':',1) for x in e.attrib.get('style','').split(';') if ':' in x)}
 w=declarations.get('font-weight')
 if w:
  if w in ('normal','initial','revert'):weight=400
  elif w=='bold':weight=700
  elif w=='bolder':weight=400 if weight<350 else 700 if weight<550 else 900
  elif w=='lighter':weight=100 if weight<550 else 400 if weight<750 else 700
  elif w.isdigit():weight=int(w)
  elif w not in ('inherit','unset'):raise ValueError('font-weight não mapeado: '+w)
 i=declarations.get('font-style')
 if i:
  if i in ('normal','initial','revert'):italic=False
  elif i=='italic' or i.startswith('oblique'):italic=True
  elif i not in ('inherit','unset'):raise ValueError('font-style não mapeado: '+i)
 return weight,italic
def glyphs(root):
 out=[]
 def visit(e,prior):
  if tag(e) in ('head','script','style','title') or not tag(e):return
  state=style(e,prior);flag=(state[0]>=600,state[1])
  if e.text:out.extend((c,flag) for c in e.text)
  for child in e:
   visit(child,state)
   if child.tail:out.extend((c,flag) for c in child.tail)
 visit(root,(400,False));return out
def relevant(gs):
 text=''.join(c for c,f in gs);m=re.search(r'DECRETO\s+LEGISLATIVO',text);assert m;return gs[m.start():]
def nonwhite(gs):return [(c,f) for c,f in gs if not c.isspace() and c!='\ufeff']
def paragraph_tokens(e):
 out=[]
 def visit(n):
  if n.text:out.append(('text',n.text))
  for c in n:
   if tag(c)=='br':out.append(('br',''))
   else:visit(c)
   if c.tail:out.append(('text',c.tail))
 visit(e)
 merged=[]
 for kind,value in out:
  if kind=='text' and merged and merged[-1][0]=='text':merged[-1]=('text',merged[-1][1]+value)
  else:merged.append((kind,value))
 return merged
def inline_runs(tokens,source,cursor):
 out=[];opened=(False,False);last=(False,False)
 def switch(flags):
  nonlocal opened
  if flags==opened:return
  if opened[1]:out.append('</em>')
  if opened[0]:out.append('</strong>')
  if flags[0]:out.append('<strong>')
  if flags[1]:out.append('<em>')
  opened=flags
 for typ,s in tokens:
  if typ=='br':out.append('<br>');continue
  for c in s:
   if c.isspace() or c=='\ufeff':flags=last
   else:
    assert cursor<len(source),(cursor,len(source));sc,flags=source[cursor];assert sc==c,(cursor,sc,c);cursor+=1;last=flags
   switch(flags);out.append(html.escape(c,quote=False))
 switch((False,False));return ''.join(out),cursor
fixtures=[('<p style="font-weight:bold">A<span style="font-weight:normal">B<i>C</i></span>D</p>',[('A',(True,False)),('B',(False,False)),('C',(False,True)),('D',(True,False))]),('<em>A<strong style="font-weight:normal;font-style:normal">B</strong>C</em>',[('A',(False,True)),('B',(False,False)),('C',(False,True))]),('<b><span style="font-weight:400">A</span>B</b>',[('A',(False,False)),('B',(True,False))]),('<strong>Artigo 1.</strong>°',[(c,(c!='°',False)) for c in 'Artigo1.°'])]
for snippet,expected in fixtures:assert nonwhite(glyphs(html5lib.parseFragment(snippet,namespaceHTMLElements=False)))==expected
profile=B/'sp-dlg71-perfil.json';prior=B/'manifesto-sp-dlg70-versao-capturada.json';ctx=B/'overlay-contextos-sp-dlg71-correcao716-742.json';rows=json.loads(profile.read_text())['documentos'];contexts={r['numero']:r['contexto_revisto'] for r in json.loads(ctx.read_text())['documentos']};proofs=[];files={};outdir=B/'sp-dlg71-css';prior_manifest=json.loads(prior.read_text());prior_rows={r['path_canonico']:r for r in prior_manifest['documentos']}
def fp(p,role):
 p=Path(p);return {'path':str(p),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size,'papel':role}
for r in rows:
 p=Path(r['path']);old=p.read_bytes();assert sha(old)==r['md_sha256_atual'];cache=Path(r['cache_original']);gz=cache.read_bytes();raw=gzip.decompress(gz);assert sha(raw)==r['fonte_sha256'];source=html5lib.parse(raw.decode(r['encoding_real']),namespaceHTMLElements=False).find('body');assert source is not None;sg=nonwhite(relevant(glyphs(source)));assert not any(tag(e) in ('s','strike','del','table') for e in source.iter());head,oldbody=old.decode().split('\n---\n',1);h1,body=oldbody.split('\n',1);oldhtml=render(body,options=Options.CMARK_OPT_UNSAFE);dom=html5lib.parseFragment(oldhtml,namespaceHTMLElements=False);paragraphs=list(dom);assert all(tag(e)=='p' for e in paragraphs),[tag(e) for e in paragraphs];number=json.loads(r['metadata']['numero']);cursor=0;blocks=[];baseline_paragraphs=[];asterisks=0
 for e in paragraphs:
  tokens=paragraph_tokens(e)
  if number=='705':
   nt=[]
   for kind,s in tokens:
    ns,n=re.subn(r'^\*\*(Artigo [12]\.)\*\*(°)',r'\1\2',s);asterisks+=n;nt.append((kind,ns))
   tokens=nt
  baseline_paragraphs.append(tokens);content,cursor=inline_runs(tokens,sg,cursor);blocks.append('<p>'+content+'</p>')
 assert cursor==len(sg);assert asterisks==(2 if number=='705' else 0);newbody='\n\n'.join(blocks)+'\n';newdom=html5lib.parseFragment(render(newbody,options=Options.CMARK_OPT_UNSAFE),namespaceHTMLElements=False);ng=nonwhite(relevant(glyphs(newdom)));assert sg==ng,number;assert len(list(newdom))==len(paragraphs);newparagraphs=[paragraph_tokens(e) for e in newdom];assert baseline_paragraphs==newparagraphs,number
 if number=='705':assert '<strong>Artigo 1.</strong>°' in newbody and '<strong>Artigo 2.</strong>°' in newbody
 bg=nonwhite(relevant(glyphs(dom)));before_char_exact=[c for c,f in bg]==[c for c,f in sg];before_flags_equal=before_char_exact and bg==sg;nh=head.replace('versao_texto: "original"','versao_texto: "fonte capturada"');assert nh!=head
 if before_flags_equal:
  new=(nh+'\n---\n'+oldbody).encode();candidate=Path(prior_rows[str(p)]['candidato']);assert candidate.read_bytes()==new;snapshot=Path(prior_rows[str(p)]['snapshot_anterior']);assert snapshot.read_bytes()==old
 else:
  new=(nh+'\n---\n'+h1+'\n\n'+newbody).encode();candidate=outdir/'candidatos'/p.relative_to('estaduais/SP');candidate.parent.mkdir(parents=True,exist_ok=True);assert not candidate.exists();candidate.write_bytes(new)
  if str(p) in prior_rows:snapshot=Path(prior_rows[str(p)]['snapshot_anterior']);assert snapshot.read_bytes()==old
  else:
   snapshot=outdir/'snapshots'/p.relative_to('estaduais/SP');snapshot.parent.mkdir(parents=True,exist_ok=True);assert not snapshot.exists();snapshot.write_bytes(old)
 srcflags=collections.Counter(str(f) for c,f in sg);oldflags=collections.Counter(str(f) for c,f in bg);newflags=collections.Counter(str(f) for c,f in ng)
 proofs.append({'path':str(p),'candidato':str(candidate),'snapshot':str(snapshot),'old_sha256':sha(old),'new_sha256':sha(new),'fonte_sha256':sha(raw),'fonte_gzip_sha256':sha(gz),'cabecalho_old_sha256':sha(head.encode()),'cabecalho_new_sha256':sha(nh.encode()),'header_alteracao_unica':'versao_texto: original → fonte capturada','H1_inalterado':h1,'paragrafos_before_after':[len(paragraphs),len(list(newdom))],'tokens_texto_br_por_paragrafo_iguais':True,'bold_italic_source_before_after':[dict(srcflags),dict(oldflags),dict(newflags)],'source_new_chars_flags_sha256':sha(json.dumps(sg,ensure_ascii=False,separators=(',',':')).encode()),'before_chars_exact':before_char_exact,'before_flags_equal':before_flags_equal,'after_chars_flags_exact':True,'corpo_alterado':not before_flags_equal,'asteriscos_espurios705_removidos':asterisks,'contexto_revisto':contexts[number],'source_H1_H2_H3_tags':dict(collections.Counter(tag(e) for e in source.iter() if tag(e) in ('h1','h2','h3'))),'limites':['Máscaras por glifo não branco: tagsb/strong/i/em e CSS inline herdado/reset. Não infere defaultsUA de headings nem CSS externo não cacheado.','Espaços ebr/parágrafos seguem GFMbaseline; flags de espaços não são certificadas.','Logos institucionais anteriores à epígrafe não foram copiados ao corpo. Fontes originais preservadas.']})
 for q,role in [(candidate,'candidato_isolado'),(snapshot,'snapshot_integral'),(cache,'fonte_original_gzip')]:files[str(q)]=fp(q,role)
ledger=outdir/'ledger.json';assert not ledger.exists();ledger.write_text(json.dumps({'escopo':71,'correcao_coverage':'A prova anterior estilos-contexto varria somente line-through/hidden/underline; não cobria font-weight/font-style. Igualdade de caracteres não provava preservação dessas máscarasCSS. Coorte anterior70 fica substituída para revisão por estes71candidatos isolados, sem mutar seus manifestos.','fixtures_reset_heranca':len(fixtures),'documentos':proofs,'perfil':fp(profile,'perfil_anterior'),'contextos_corrigidos':fp(ctx,'overlay_contextual')},ensure_ascii=False,indent=2)+'\n')
for q in [profile,prior,ctx,ledger,Path(__file__)]:files[str(q)]=fp(q,'prova_reproducivel')
manifest=B/'manifesto-sp-dlg71-css.json';assert not manifest.exists();manifest.write_text(json.dumps({'estado':'proposta_isolada_revisao_raiz_pendente','total':71,'corpos_alterados':sum(r['corpo_alterado'] for r in proofs),'corpos_byteiguais':sum(not r['corpo_alterado'] for r in proofs),'ledger':fp(ledger,'ledger'),'documentos':[{'path':r['path'],'candidato':r['candidato'],'snapshot':r['snapshot'],'old_sha256':r['old_sha256'],'new_sha256':r['new_sha256'],'fonte_sha256':r['fonte_sha256']} for r in proofs],'lista_publicacao_provas':list(files.values()),'total_arquivos_lista':len(files),'total_bytes_lista':sum(r['bytes'] for r in files.values()),'limites':['Não altera canônicos/core/coletores/manifestos anteriores, semHTTP/Git de escrita.','71candidatos corrigem máscaras explícitas inline e705, aguardando revisão independente de CSS externo/headings/defaultsUA se exigida.','Statusnull, identidade/data/título/URI preservados; versãofontecapturada sem inferir atualização jurídica.']},ensure_ascii=False,indent=2)+'\n');print(manifest,sha(manifest.read_bytes()),len(files),sum(r['bytes'] for r in files.values()),flush=True)
