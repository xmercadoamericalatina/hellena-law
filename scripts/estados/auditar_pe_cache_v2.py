"""Revisão v2 do auditor PE: pontuação visível e assinatura numérica da fonte.

Mantém o auditor v1 intacto. Não altera corpos: divergências são retidas, com
contexto literal para revisão, inclusive nos lotes que passaram pelo gate v1.
"""
from pathlib import Path
import argparse
import concurrent.futures
import collections
import gzip
import hashlib
import json
import re
import signal
import time

from auditar_pe_cache import R, one, documento_da_lista, timeout_handler
from pe import limites_texto_html
from comum import html_para_md
from pe_fidelidade_visivel import comparar_fidelidade, assinatura_numerica


def _primeira_diferenca(a,b):
    for i,(x,y) in enumerate(zip(a,b)):
        if x!=y:break
    else:i=min(len(a),len(b))
    return {'posicao':i,'fonte':a[max(0,i-100):i+200],'md':b[max(0,i-100):i+200]}


def auditar_v2(document):
    result=one(document)
    signal.signal(signal.SIGALRM,timeout_handler);signal.alarm(20)
    try:
        source=gzip.decompress((R/result['cache']).read_bytes()).decode()
        a,b=limites_texto_html(source,fragmento='id="divTexto"' not in source)
        field=source[a:b];expected=html_para_md(field)
        body=(R/document['path']).read_text().split('\n---\n',1)[1].split('\n',1)[1]
        body=re.sub(r'^# [^\n]*\n','',body,count=1).strip()
        proof=comparar_fidelidade(field,expected,body)
        checks={k:v for k,v in proof.items() if isinstance(v,bool)}
        detail={'comparacoes':checks,'normalizacoes_de_apresentacao':proof['normalizacoes_de_apresentacao'],'normalizacao_permitida':'whitespace e BOM invisível; marcadores de apresentação Markdown conhecidos; tags de apresentação HTML. Preserva caixa, acentos, pontuação, moedas, percentuais, decimais e sinais.','sha256_visivel_fonte':hashlib.sha256(proof['visivel_fonte'].encode()).hexdigest(),'sha256_visivel_md':hashlib.sha256(proof['visivel_md'].encode()).hexdigest(),'sha256_visivel_reconversao':hashlib.sha256(proof['visivel_reconversao'].encode()).hexdigest()}
        if (not checks['texto_visivel_md_igual_reconversao']
                and not checks['texto_visivel_md_igual_fonte_apos_formato_heading_comprovado']):
            result['problemas'].append('v2: texto visível diverge da reconversão, preservando pontuação')
            detail['divergencia_md_reconversao']=_primeira_diferenca(proof['visivel_reconversao'],proof['visivel_md'])
        if not checks['texto_visivel_md_igual_fonte_apos_formato_heading_comprovado']:
            result['problemas'].append('v2: texto visível diverge diretamente do HTML oficial, preservando pontuação')
            detail['divergencia_md_fonte']=_primeira_diferenca(proof['visivel_fonte'],proof['visivel_md_apos_heading_comprovado'])
        if not checks['numeros_sinais_moedas_percentuais_iguais_fonte']:
            result['problemas'].append('v2: números, sinais, moedas ou percentuais divergem do HTML oficial')
            detail['divergencia_numerica']=_primeira_diferenca(assinatura_numerica(proof['visivel_fonte']),assinatura_numerica(proof['visivel_md']))
        detail['fonte_primaria_prevalece_sobre_artefato_da_reconversao']=(not checks['texto_visivel_md_igual_reconversao'] and checks['texto_visivel_md_igual_fonte_apos_formato_heading_comprovado'] and checks['numeros_sinais_moedas_percentuais_iguais_fonte'])
        result['fidelidade_visivel_v2']=detail
    except Exception as e:
        result['problemas'].append('v2: erro de validação: '+type(e).__name__+': '+str(e)[:250])
    signal.alarm(0)
    result['publicavel']=not result['problemas']
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lista',required=True)
    parser.add_argument('--saida',required=True)
    parser.add_argument('--workers',type=int,default=4)
    args=parser.parse_args();paths=Path(args.lista).read_text().splitlines()
    if len(paths)!=len(set(paths)):raise ValueError('lista com caminhos repetidos')
    documents=[documento_da_lista(p) for p in paths if p]
    counts=collections.Counter();start=time.monotonic()
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as executor,Path(args.saida).open('x') as output:
        for n,result in enumerate(executor.map(auditar_v2,documents,chunksize=25),1):
            output.write(json.dumps(result,ensure_ascii=False)+'\n');output.flush()
            counts['publicavel' if result['publicavel'] else 'retido']+=1
            if n%250==0:print(n,dict(counts),'seg',round(time.monotonic()-start),flush=True)
    print('FINAL',len(documents),dict(counts),flush=True)


if __name__=='__main__':main()
