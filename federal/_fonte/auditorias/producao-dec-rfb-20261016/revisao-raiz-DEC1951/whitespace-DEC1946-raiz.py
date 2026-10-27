from pathlib import Path
import subprocess,json,hashlib,gzip,shutil
B=Path('/Volumes/ExternalSSD/GitHub/constituicao');O=B/'federal/_fonte/auditorias/producao-dec-rfb-20261016/revisao-raiz-DEC1951'
command=['rtk','proxy','git','diff','--cached','--check','--','federal/decretos']
r=subprocess.run(command,cwd=B,stdout=subprocess.PIPE,stderr=subprocess.PIPE);assert r.returncode in (0,2),r.stderr
lines=r.stdout.decode().splitlines();count=0;eof=0;i=0
while i<len(lines):
 line=lines[i]
 if not line:i+=1;continue
 if line.endswith('trailing whitespace.'):
  i+=1;assert i<len(lines) and lines[i].startswith('+')
  text=lines[i][1:];assert text.endswith('  ') and not text.endswith('   ') and not text.endswith('\t  '),line
  count+=1
 elif line.endswith('new blank line at EOF.'):eof+=1
 else:raise AssertionError(line)
 i+=1
(O/'whitespace-canonicos-Gitdiff-raiz.txt.gz').write_bytes(gzip.compress(r.stdout))
result={'canonicos_escopo':'federal/decretos staged1946','comando':command,'exit':r.returncode,'hardbreaks_duas_spaces':count,'EOFs':eof,'sem_outros_alertas':True,'raw_stdout_SHA256':hashlib.sha256(r.stdout).hexdigest(),'fontes_e_provas':'Arquivos primarios congelados preservados byteaByte, sem reformatacao por whitespace; gate integral de indexSHA separado.'}
(O/'whitespace-canonicos-raiz.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');shutil.copyfile('/tmp/whitespace-DEC1946-raiz.py',O/'whitespace-DEC1946-raiz.py');print(json.dumps(result,ensure_ascii=False))
