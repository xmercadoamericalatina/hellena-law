from pathlib import Path
import json,hashlib,datetime
B=Path('/Volumes/ExternalSSD/GitHub/constituicao')
D=B/'federal/_fonte/auditorias/producao-dec-rfb-20261016'
O=D/'revisao-raiz-DEC1951'
sha=lambda b:hashlib.sha256(b).hexdigest()
expected=set((D/'overlay-contextual-DEC2000/paths-sem-alerta-adicional.txt').read_text().splitlines())
assert len(expected)==1951
merged={};inputs=[];rounds=[]
for folder in ('','rechecagem633/','rechecagem21-unico/','rechecagem1-apenso-v2/'):
 p=O/folder/'documentos-raiz.jsonl'
 rows=[json.loads(l) for l in p.read_text().splitlines()]
 inputs.append({'path':str(p.relative_to(B)),'sha256':sha(p.read_bytes())})
 rounds.append({'rodada':folder or 'V1','verificados':len(rows),'sem_erros':sum(not r['erros'] for r in rows)})
 for r in rows:
  assert r['path'] in expected
  if not r['erros']:
   assert r['path'] not in merged
   merged[r['path']]=r
assert set(merged)==expected
for p,r in merged.items():assert sha((B/p).read_bytes())==r['sha256_MD']
github=O/'GitHub/resumo-GitHub1951-raiz.json'
g=json.loads(github.read_text());assert g['documentos']==1951
rendered={}
for batch in g['lotes']:
 assert batch['estrutura_GFM_GitHub_igual'] and batch['sem_efeitos_entre_documentos']
 assert len(batch['MD_SHA256'])==batch['documentos']
 for p,h in batch['MD_SHA256'].items():
  assert p not in rendered and merged[p]['sha256_MD']==h
  rendered[p]=h
assert set(rendered)==expected
inputs.append({'path':str(github.relative_to(B)),'sha256':sha(github.read_bytes())})
context={
 '75871':('resolvido','Artigos8/9/75 pertencem a redacao citada do Decreto71848/1973. Artigos proprios1/2 completos.'),
 '75906':('retido','FonteHTML rotula como paragrafo4 o que outra numeracao poderia sugerir Art4. Preservar literal; candidato de fonte integral alternativa em recuperacao.'),
 '76923':('resolvido','Artigo15 integral presente com virgula no rotulo. Sem lacuna de artigo; literal mantido.'),
 '77443':('retido','Cotejo integral Camara identificou Paragrafo unico e todo GrupoSetorialVI ausentes no HTMLNormas. DuplicidadeArt4 adicional. Requer outra fonte integral, sem enxerto.'),
 '77544':('retido','Art. inicial sem numeral na fonteNormas; Camara possui1. Preparar versao integral alternativa, sem completar numeral por inferencia.'),
 '77620':('retido','Art. inicial sem numeral na fonteNormas; Camara possui1. Preparar versao integral alternativa, sem completar numeral por inferencia.'),
 '77978':('resolvido','Artigos1/2 internos entre aspas sao nova redacao do Decreto77318/1976. Artigos proprios1/2 completos.'),
 '78010':('resolvido','Artigos1/2 internos entre aspas sao nova redacao da concessao Decreto74203/1974. Artigos proprios1/2/3 completos.'),
 '78273':('resolvido','SegundoArt1 e redacao substitutiva explicitamente introduzida pelo primeiroArt1 sobre Decreto76206/1975; artigos proprios1/2.'),
 '78373':('resolvido','SegundoArt1 e redacao substitutiva explicitamente introduzida pelo primeiroArt1 sobre Decreto72174/1973; artigos proprios1/2.'),
 '78587':('retido','Art.- inicial sem numeral; Camara possui1. Frase repetida tambem na Camara nao corrigida. Fonte integral alternativa em recuperacao.'),
 '79192':('resolvido','Artigos14/45 internos entre aspas sao nova redacao do regulamento da ESG; artigos proprios1/2/3 completos.')}
alerts=json.loads((O/'artigos-alertas-contexto-raiz.json').read_text())
alerts=alerts['alertas'] if isinstance(alerts,dict) else alerts
assert len(alerts)==12
decisions=[]
for a in alerts:
 n=Path(a['path']).name.split('-')[1];state,reason=context[n]
 assert merged[a['path']]['sha256_fonte']==a['sha256_fonte']
 decisions.append({'path':a['path'],'sha256_fonte':a['sha256_fonte'],'estado':state,'decisao_leitura_integral_raiz':reason})
spatial=json.loads((O/'espacos5-contextos-e-76583-raiz.json').read_text())
spans=[s for r in spatial for s in r['spans']]
assert len(spans)==5 and sum(bool(r['spans']) for r in spatial)==4
assert all(s['literal']=='\xa0' for s in spans)
out=O/'documentos1951-consolidados-raiz.jsonl'
out.write_text(''.join(json.dumps(merged[p],ensure_ascii=False)+'\n' for p in sorted(merged)))
result={'estado':'validacao_fonte_render_concluida; dedup e aprovacao final pendentes','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'documentos':1951,'rodadas':rounds,'inputs':inputs,'consolidacao':{'path':str(out.relative_to(B)),'sha256':sha(out.read_bytes())},'contextos12':decisions,'referencia_apenso76583':'Processo apenso690-68DFZ02, nao anexo integrante do decreto. Excecao restrita ao literal completo normalizado; fonte e texto imutaveis. V1falhou por literal de excecao nao normalizado, V2passou.','spans_NBSP':{'documentos':4,'spans':5,'ocorrencias_propriedades_V1':10,'contexto':'4assinaturas e1epigrafe; nao colunas de dados'},'candidatos_sem_pendencia_contextual':1946,'retidos_contextuais':5,'aprovacao_publicacao':False,'limites':['Sem leitura humana integral1951 ou comprovacao de facsimiles. Contextos alertados12 foram lidos integralmente.','Original refere-se a metadado encodingOriginal do portal; API indica UnofficialLegalValue, nao certificacao de exemplar impresso.','Texto e B/I/del/U/sup/sub cotejados; B extra somente rotulos normativos. Nao alega pixels/CSStexttransform/posicionamento identicos.','Correcao de reconhecedorArtigoUnico e excecao processoapenso nao modificam corpus.','Dedup HEAD em execucao; nenhuma aprovacao/publicacao neste relatorio.']}
(O/'consolidacao-1951-raiz.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'documentos':1951,'rodadas':rounds,'retidos_contextuais':5,'SHA_consolidacao':sha(out.read_bytes())},ensure_ascii=False))
