"""Integra apenas anexos individuais revisados, vinculados por SHA e prova visual.

Não consulta rede. Plano explícito distingue material adicional de alternativa
assinada integral; não mistura compilações históricas com redações originais.
"""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from auditar_municipal import metadados
from granularidade_sapl import alertas_multiplos_atos, alertas_outras_publicacoes
RAIZ=Path(__file__).resolve().parent.parent
PDFTOTEXT='/opt/homebrew/bin/pdftotext'
PDFIMAGES='/opt/homebrew/bin/pdfimages'

def sha(b):return hashlib.sha256(b).hexdigest()

def bloco(layout):
    if '```' in layout:raise ValueError('marcador ambíguo no PDF')
    corpo='```text\n'+layout.replace('\f','\n\n').rstrip('\n')+'\n```'
    if re.findall(r'\w+',layout)!=re.findall(r'\w+',corpo[len('```text\n'):-len('\n```')]):raise ValueError('tokens alterados')
    return corpo

def preparar(r):
    p=RAIZ/r['path'];old=p.read_bytes()
    if sha(old)!=r['sha256_md_antes']:raise ValueError('MD mudou desde revisão')
    fonte=RAIZ/r['arquivo'];b=fonte.read_bytes()
    if sha(b)!=r['sha256_arquivo'] or not b.startswith(b'%PDF'):raise ValueError('fontePDF diverge')
    if r['modo'] not in ('acrescentar','alternativa_integral'):raise ValueError('modo não revisado')
    for v in r.get('evidencias_visuais',[]):
        if sha((RAIZ/v['path']).read_bytes())!=v['sha256']:raise ValueError('evidência visual mudou')
    imagens=subprocess.check_output([PDFIMAGES,'-list',str(fonte)],text=True)
    if sha(imagens.encode())!=r['sha256_pdfimages']:raise ValueError('objetos de imagem divergem')
    if re.search(r'^\s*\d+\s+\d+\s+',imagens,re.M) and not r.get('evidencias_visuais'):raise ValueError('imagem sem revisão')
    layout=subprocess.check_output([PDFTOTEXT,'-layout',str(fonte),'-'],text=True)
    if not all(re.search(r'\w',pg) for pg in layout.rstrip('\f').split('\f')):raise ValueError('página sem camada textual')
    if not re.search(r['identidade_regex'],layout,re.I):raise ValueError('identidade não confere no conteúdo')
    md=old.decode();cab,resto=md.split('\n---\n',1);titulo,corpo=resto.lstrip('\n').split('\n\n',1);m=metadados(md)
    if alertas_multiplos_atos('\n'.join(x.lstrip() for x in layout.splitlines()),m.get('tipo_na_fonte',m['tipo']),m['numero']):raise ValueError('epígrafe alheia detectada')
    if alertas_outras_publicacoes(layout):raise ValueError('outra publicação suspeita')
    secao='## '+r['titulo_secao']+'\n\nFonte oficial: '+r['url']+'\n\n'+r['nota_editorial']+'\n\n'+bloco(layout)
    if r['modo']=='acrescentar':corpo=corpo.rstrip()+'\n\n'+secao
    else:
        corpo=secao
        m['fonte_texto']=r['url'];m['sha256_fonte']=sha(b)
    m['versao_texto']=str(m.get('versao_texto',''))+'; '+r['descricao_revisao']+'; reprodução da fonte, sem certificar vigência integral'
    updates={k:m[k] for k in ['fonte_texto','sha256_fonte','versao_texto']};updates.update({'sha256_texto':sha(corpo.encode()),'revisado_em':dt.date.today().isoformat()})
    for k,v in updates.items():
        line=k+': '+json.dumps(v,ensure_ascii=False)
        if re.search('^'+k+':.*$',cab,re.M):cab=re.sub('^'+k+':.*$',lambda _:line,cab,flags=re.M)
        else:cab+='\n'+line
    new=(cab+'\n---\n\n'+titulo+'\n\n'+corpo+'\n').encode()
    return old,new,{'path':r['path'],'sha256':sha(new),'sha256_anterior':sha(old),'sha256_fonte_adicional':sha(b),'url_fonte_adicional':r['url'],'modo':r['modo'],'tokens_adicionais_ou_substitutos':len(re.findall(r'\w+',layout)),'sha256_layout':sha(layout.encode()),'imagens':imagens,'revisao':r}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--plano',type=Path,required=True);ap.add_argument('--saida',type=Path,required=True);ap.add_argument('--aplicar',action='store_true');a=ap.parse_args();a.saida.mkdir(exist_ok=False,parents=True);rows=[]
    for r in json.loads(a.plano.read_text())['revisados']:
        old,new,record=preparar(r)
        if a.aplicar:
            backup=RAIZ/'municipais/_fonte/auditorias/anexos-integrados'/(sha(old)+'.md');backup.parent.mkdir(parents=True,exist_ok=True)
            if backup.exists():assert backup.read_bytes()==old
            else:backup.write_bytes(old)
            (RAIZ/r['path']).write_bytes(new);record['backup']={'path':str(backup.relative_to(RAIZ)),'sha256':sha(old)}
        rows.append(record)
    (a.saida/'manifesto.json').write_text(json.dumps({'aplicado':a.aplicar,'plano':{'path':str(a.plano),'sha256':sha(a.plano.read_bytes())},'script_sha256':sha(Path(__file__).read_bytes()),'aprovados':rows},ensure_ascii=False,indent=2));(a.saida/'aprovados.paths.txt').write_text(''.join(r['path']+'\n' for r in rows))
    print(json.dumps({'documentos':len(rows),'aplicado':a.aplicar,'saida':str(a.saida)}))

if __name__=='__main__':main()
