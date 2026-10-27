"""Recupera retidos de PDF nativo sem imagens, conservando layout inteiro e backup.

Só opera depois dos controles integral e de imagens. Não promove OCR ou PDFs
mistos. Mantém fólio, cabeçalho, tabelas textuais e números isolados na transcrição.
"""
import argparse
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

sys.path.insert(0,str(Path(__file__).resolve().parent))
from auditar_imagens_pdf_sapl import auditar as auditar_imagens, CACHE as CACHE_IMAGENS
from auditar_municipal import metadados
from baixar_organicas_sapl import corpo_integral_reconhecivel
from granularidade_sapl import alertas_multiplos_atos

RAIZ=Path(__file__).resolve().parent.parent


def sha(b):return hashlib.sha256(b).hexdigest()


def reconstruir_md(texto,layout):
    cab,resto=texto.split('\n---\n',1);titulo=resto.lstrip('\n').split('\n\n',1)[0]
    if '```' in layout:raise ValueError('marcador de bloco no PDF requer revisão de formatação')
    corpo='```text\n'+layout.replace('\f','\n\n').rstrip('\n')+'\n```'
    transcrito=corpo[len('```text\n'):-len('\n```')]
    if re.findall(r'\w+',layout)!=re.findall(r'\w+',transcrito):raise ValueError('transcrição integral diverge')
    meta=metadados(texto)
    versao=str(meta.get('versao_texto',''))+'; transcrição integral preformatada de PDF nativo sem imagens, cabeçalhos/fólios/valores numéricos preservados; fidelidade à camada textual, sem certificar vigência jurídica'
    for campo,valor in [('sha256_texto',sha(corpo.encode())),('versao_texto',versao),('revisado_em',dt.date.today().isoformat())]:
        linha=campo+': '+json.dumps(valor,ensure_ascii=False)
        if re.search('^'+campo+r':.*$',cab,re.M):cab=re.sub('^'+campo+r':.*$',lambda _:linha,cab,flags=re.M)
        else:cab+='\n'+linha
    return cab+'\n---\n\n'+titulo+'\n\n'+corpo+'\n',corpo


def preparar(r):
    p=RAIZ/r['path'];old=p.read_bytes()
    atual=old
    if sha(old)!=r['sha256']:
        backup=RAIZ/'municipais/_fonte/auditorias/recuperacao-pdf-sapl'/(r['sha256']+'.md')
        if not backup.exists() or sha(backup.read_bytes())!=r['sha256']:raise ValueError('documento mudou sem backup conferível')
        old=backup.read_bytes()
    m=metadados(old.decode());u=urlsplit(m['fonte']);rawpath=RAIZ/'municipais/_fonte/organicas-sapl'/u.hostname/(u.path.strip('/').split('/')[-1]+'.bin')
    raw=rawpath.read_bytes()
    if not raw.startswith(b'%PDF'):raise ValueError('recuperação exclusiva de PDF')
    if sha(raw)!=r['sha256_fonte']:raise ValueError('fonte diverge do confronto original')
    cap=RAIZ/'municipais/_fonte/auditorias/integralidade-pdf-sapl'/(sha(raw)+'.json.gz')
    with gzip.open(cap,'rt') as f:d=json.load(f)
    layout=d['layout']
    normalizado='\n'.join(x.lstrip() for x in layout.splitlines())
    if not corpo_integral_reconhecivel(normalizado,emenda='emenda' in str(m['tipo']).lower()):raise ValueError('texto normativo integral não reconhecido sem OCR')
    alertas=alertas_multiplos_atos(normalizado,m.get('tipo_na_fonte',m['tipo']),m['numero'])
    if alertas:raise ValueError('outra epígrafe no PDF bruto: '+json.dumps(alertas,ensure_ascii=False))
    saida,corpo=reconstruir_md(old.decode(),layout)
    if atual!=old and atual!=saida.encode():raise ValueError('documento mudou para estado diferente da recuperação determinística')
    imagecheck=auditar_imagens({**r,'sha256':sha(atual)})
    if not imagecheck['aprovado']:raise ValueError('PDF com imagem ou verificação indisponível; requer revisão visual/OCR: '+str(imagecheck.get('erro',imagecheck.get('criterio'))))
    return old,saida,{'path':r['path'],'sha256_anterior':sha(old),'sha256':sha(saida.encode()),'sha256_corpo':sha(corpo.encode()),'sha256_fonte':sha(raw),'fonte':m['fonte'],'fonte_texto':m['fonte_texto'],'codigo_ibge':m['codigo_ibge'], 'evidencia_extracao':{'path':str(cap.relative_to(RAIZ)),'sha256':sha(cap.read_bytes())},'controle_imagens':imagecheck, 'tokens_fonte':len(re.findall(r'\w+',layout)), 'checks':{'camada_textual_integral_em_ordem':True,'sem_imagens':True,'sem_epigrafe_alheia_detectada':True,'identidade_anterior_preservada':True}}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--controle-integral',type=Path,required=True);ap.add_argument('--controle-imagens',type=Path,required=True);ap.add_argument('--saida',type=Path,required=True);ap.add_argument('--aplicar',action='store_true');a=ap.parse_args()
    for ctrl in (a.controle_integral,a.controle_imagens):
        if not (ctrl/'entrega-final.json').exists():raise ValueError('controle ainda não encerrado: '+str(ctrl))
    a.saida.mkdir(parents=True,exist_ok=False);CACHE_IMAGENS.mkdir(parents=True,exist_ok=True)
    aptos_anteriores=set((a.controle_imagens/'aprovados.paths.txt').read_text().splitlines())
    originais=[json.loads(x) for x in (a.controle_integral/'resultados.jsonl').read_text().splitlines()]
    novos=[];retidos=0;lotes=[]
    def fechar_lote():
        nonlocal novos
        if not novos:return
        n=len(lotes)+1;prefix=a.saida/f'lote-{n:04d}';manifesto=prefix.with_suffix('.json');lista=prefix.with_suffix('.paths.txt')
        dados={'aplicado':a.aplicar,'criterio':__doc__,'aprovados':novos}
        with manifesto.open('x') as f:json.dump(dados,f,ensure_ascii=False,indent=2)
        with lista.open('x') as f:f.write(''.join(r['path']+'\n' for r in novos))
        lotes.append({'manifesto':str(manifesto),'sha256_manifesto':sha(manifesto.read_bytes()),'lista':str(lista),'sha256_lista':sha(lista.read_bytes()),'aprovados':len(novos)})
        print(json.dumps(lotes[-1],ensure_ascii=False),flush=True);novos=[]
    with (a.saida/'retidos.jsonl').open('x') as log,(a.saida/'aplicados.jsonl').open('x') as aplicados:
        for i,r in enumerate(originais,1):
            if r['path'] in aptos_anteriores:continue
            try:
                old,new,prova=preparar(r)
                if a.aplicar:
                    backup=RAIZ/'municipais/_fonte/auditorias/recuperacao-pdf-sapl'/(sha(old)+'.md');backup.parent.mkdir(parents=True,exist_ok=True)
                    if not backup.exists():
                        with backup.open('xb') as f:f.write(old)
                    if sha(backup.read_bytes())!=sha(old):raise ValueError('backup diverge')
                    p=RAIZ/r['path']
                    if p.read_bytes() not in (old,new.encode()):raise ValueError('arquivo mudou antes da gravação')
                    if p.read_bytes()!=new.encode():
                        temp=p.with_suffix('.recuperacao.tmp');temp.write_text(new);temp.replace(p)
                    prova['backup']={'path':str(backup.relative_to(RAIZ)),'sha256':sha(old)}
                else:
                    preview=a.saida/'candidatos'/r['path'];preview.parent.mkdir(parents=True,exist_ok=True);preview.write_text(new)
                novos.append(prova)
                aplicados.write(json.dumps(prova,ensure_ascii=False)+'\n');aplicados.flush()
                if len(novos)>=1000:fechar_lote()
            except Exception as e:
                retidos+=1;log.write(json.dumps({'path':r['path'],'sha256':r['sha256'],'motivo':str(e)},ensure_ascii=False)+'\n');log.flush()
            if i%100==0:print(json.dumps({'examinados':i,'recuperados':sum(l['aprovados'] for l in lotes)+len(novos),'retidos':retidos}),flush=True)
    fechar_lote()
    recibo={'aplicado':a.aplicar,'lotes':lotes,'recuperados':sum(l['aprovados'] for l in lotes),'retidos':retidos,'controles':[{'path':str(c/'entrega-final.json'),'sha256':sha((c/'entrega-final.json').read_bytes())} for c in (a.controle_integral,a.controle_imagens)],'script_sha256':sha(Path(__file__).read_bytes())}
    with (a.saida/'entrega-final.json').open('x') as f:json.dump(recibo,f,ensure_ascii=False,indent=2)
    print(json.dumps(recibo,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
