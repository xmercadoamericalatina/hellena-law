from pathlib import Path
import json,gzip,re,hashlib,argparse,html5lib,sys
ROOT=Path.cwd();OUT=ROOT/'federal/_fonte/auditorias/dpl-tabelas114-revisao-final-20261016';sys.path.insert(0,str(ROOT/'scripts'));import baixar_camara as cam
sha=lambda b:hashlib.sha256(b).hexdigest()
def signature(s,compact=False):
 root=html5lib.parseFragment(s,namespaceHTMLElements=False);result=[]
 for e in root.iter():
  if e.tag in ('table','thead','tbody','tfoot','tr','td','th'):
   text=''.join(e.itertext()) if e.tag in ('td','th') else None
   if text is not None:text=re.sub(r'\s+' ,'' if compact else ' ',text).strip()
   result.append({'tag':e.tag,'spans':{k:e.attrib[k] for k in ('rowspan','colspan') if k in e.attrib},'texto':text})
 return result
ap=argparse.ArgumentParser();ap.add_argument('--auditar',action='store_true');args=ap.parse_args();result=[]
for r in map(json.loads,(OUT/'revisao114.jsonl').read_text().splitlines()):
 packed=(ROOT/r['fonte']['snapshot']).read_bytes();assert sha(packed)==r['fonte']['sha256_arquivo'];frag=cam.corpo_norma(gzip.decompress(packed).decode());raw=(ROOT/r['candidato']).read_bytes();assert sha(raw)==r['sha256_candidato'];body=raw.decode().split('---',2)[2].lstrip().split('\n\n',1)[1];a=signature(frag);b=signature(body);aa=signature(frag,True);bb=signature(body,True)
 if not r['retencoes']:assert a==b,r['path']
 result.append({'path':r['path'],'fonte_SHA':r['fonte']['sha256_fonte'],'candidato_SHA':sha(raw),'DOM_HTML5_estrutura_spans_texto':a==b,'DOM_HTML5_estrutura_spans_texto_sem_espacos':aa==bb,'sha256_DOM_fonte':sha(json.dumps(a,ensure_ascii=False).encode()),'sha256_DOM_candidato':sha(json.dumps(b,ensure_ascii=False).encode()),'retido':bool(r['retencoes']),'diagnostico_quatro':None if r['tabelas_celulas_spans_identicos'] else ('diferença de segmentação de nós/whitespace inline; células, spans e todos caracteres não brancos preservados' if aa==bb else 'diferença estrutural real'),'anexo_ausente':'dpl-4555-' in r['path']})
data=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode();p=OUT/'diagnostico-HTML5-114-final.json'
if args.auditar or p.exists():assert p.read_bytes()==data
else:p.write_bytes(data)
print(json.dumps({'documentos':114,'DOM_estrito':sum(x['DOM_HTML5_estrutura_spans_texto'] for x in result),'DOM_sem_whitespace':sum(x['DOM_HTML5_estrutura_spans_texto_sem_espacos'] for x in result),'retencoes_preservadas':sum(x['retido'] for x in result),'SHA':sha(data)}))
