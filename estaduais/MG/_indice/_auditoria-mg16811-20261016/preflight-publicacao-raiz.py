from pathlib import Path
import json,hashlib,subprocess,collections
B=Path('estaduais/MG/_indice/_auditoria-mg16811-20261016');sha=lambda b:hashlib.sha256(b).hexdigest()
m=B/'manifesto-fechamento-publicacao-14691.json';assert sha(m.read_bytes())=='a9e3d13febc429cadecf6bf849a765256363637b6ef7c3f74603001de0aa2137'
manifest=json.loads(m.read_text())
for k in ['coorte_manifesto','lista','paths']:
    r=manifest[k];assert sha(Path(r['path']).read_bytes())==r['sha256']
final=json.loads(Path(manifest['coorte_manifesto']['path']).read_text())
for k in ['manifesto_anterior','coorte_anterior_ref','coorte_derivada_ref','paths_ref','retencoes_contextuais_ref']:
    r=final[k];assert sha(Path(r['path']).read_bytes())==r['sha256']
base={r['path']:r for r in map(json.loads,Path(final['coorte_anterior_ref']['path']).open())}
rows={r['path']:r for r in map(json.loads,Path(final['coorte_derivada_ref']['path']).open())}
held={r['path'] for r in json.loads(Path(final['retencoes_contextuais_ref']['path']).read_text())}
assert len(rows)==14691 and len(held)==32 and set(base)-set(rows)==held and not (set(rows)&held)
rootproof=B/'verificacao-raiz-14723.jsonl';assert sha(rootproof.read_bytes())=='a09fe6ad54b73550886a7470a34b6f4972547ef662ea3b40515b3645509631d8'
proof={r['path']:r for r in map(json.loads,rootproof.open())}
for path,r in rows.items():
    assert r==base[path];p=proof[path];assert p['confronto_independente'] and p['sha256_md']==r['md_sha256'] and p['fonte_sha256']==r['source_sha256'] and p['xml_sha256']==r['XML']['source_sha256']
payload=[json.loads(l) for l in Path(manifest['lista']['path']).open()];paths=[r['path'] for r in payload];assert len(paths)==len(set(paths))==58924
assert paths==Path(manifest['paths']['path']).read_text().splitlines()
canonical={r['path'] for r in payload if 'canonical_md' in r['roles']};assert canonical==set(rows)
assert not any(path in held for path in paths)
total=0
for n,r in enumerate(payload,1):
    p=Path(r['path']);assert p.is_file() and not p.is_symlink() and '\n' not in str(p) and '..' not in p.parts
    raw=p.read_bytes();assert len(raw)==r['bytes'] and len(raw)<100_000_000 and sha(raw)==r['sha256'],str(p);total+=len(raw)
    if n%10000==0:print('HASH',n,flush=True)
assert total==manifest['bytes_total']
head=subprocess.check_output(['rtk','proxy','git','rev-parse','HEAD'],text=True).strip()
checks=subprocess.check_output(['rtk','proxy','git','cat-file','--batch-check=%(objectname) %(objecttype) %(objectsize)'],input=''.join(head+':'+p+'\n' for p in rows).encode()).decode().splitlines();assert len(checks)==14691 and all(l.endswith(' missing') for l in checks)
output={'estado':'aprovado_raiz14691_sem_stage_commit','manifesto':str(m),'sha256_manifesto':sha(m.read_bytes()),'coorte':14691,'retidos_contextuais':32,'retidos_anteriores':2088,'payload':58924,'bytes':total,'HEAD_ausencia':head,'prova_raiz14723':str(rootproof),'sha256_prova_raiz14723':sha(rootproof.read_bytes()),'literais_preservados':True,'limites':['Contagem de documentos coletados; nao certificacao juridica/editorial.','Confronto completo fonte/MD/metadados anterior encadeado por SHA; revisao contextual com cobertura e limites por caso.','API fornece quadros lineares; geometria editorial original nao certificada.','2120pendencias mantidas fora;nenhuma reducao de meta.']}
out=B/'aprovacao-publicacao14691-raiz.json';out.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print('APROVADO',sha(out.read_bytes()),flush=True)
