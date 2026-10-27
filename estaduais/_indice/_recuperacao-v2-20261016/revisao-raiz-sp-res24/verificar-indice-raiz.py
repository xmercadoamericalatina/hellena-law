from pathlib import Path
import subprocess, json, hashlib, gzip

def git(*a):
    return subprocess.check_output(['rtk','proxy','git',*a])

base=Path('estaduais/_indice/_recuperacao-v2-20261016/revisao-raiz-sp-res24')
ap=json.loads((base/'aprovacao-publicacao24-raiz.json').read_text())
assert git('rev-parse','HEAD').decode().strip()==ap['HEAD_preaplicacao']
paths=Path('/tmp/SP24-publicacao-paths.txt').read_text().splitlines()
assert len(paths)==len(set(paths))
staged=set(git('diff','--cached','--name-only','-z').decode().strip('\0').split('\0'))
assert staged<=set(paths),(staged-set(paths))
p=subprocess.Popen(['rtk','proxy','git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
rows=[]
for name in paths:
    p.stdin.write((':'+name+'\n').encode());p.stdin.flush()
    header=p.stdout.readline().split();assert len(header)==3 and header[1]==b'blob',(name,header)
    data=p.stdout.read(int(header[2]));assert p.stdout.read(1)==b'\n'
    actual=Path(name).read_bytes();assert data==actual,name
    sha=hashlib.sha256(data).hexdigest()
    rows.append({'path':name,'sha256':sha,'bytes':len(data),'alterado':name in staged})
p.stdin.close();p.stdout.close();assert p.wait()==0
hashes={r['path']:r['sha256'] for r in rows}
for a in ap['atos']:
    assert hashes[a['path']]==a['new_sha256']
    assert a['path'] in staged
checks=subprocess.run(['rtk','proxy','git','diff','--cached','--check'],capture_output=True)
assert checks.returncode in (0,2),checks.stderr
gzip.open(base/'diffcheck-indice-raiz.txt.gz','wb').write(checks.stdout+checks.stderr)
canonical_issues=[]
for a in ap['atos']:
    for n,line in enumerate(Path(a['path']).read_text().splitlines(),1):
        if line.rstrip()!=line and not (line.endswith('  ') and line[:-2].rstrip()==line[:-2]):
            canonical_issues.append([a['path'],n,repr(line[-30:])])
assert not canonical_issues,canonical_issues
result={'estado':'indice_conferido','HEAD':ap['HEAD_preaplicacao'],'atos':24,'paths':len(paths),'paths_alterados':len(staged),'bytes':sum(r['bytes'] for r in rows),'todos_blobs_iguais_disco':True,'24_SHA256_iguais_aprovacao':True,'whitespace_canonicos':'somente hardbreaks de dois espacos ou EOF; fontes e provas congeladas preservadas byte a byte','diff_check_exit':checks.returncode,'blobs':rows}
(base/'verificacao-indice-raiz.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='blobs'},ensure_ascii=False))
