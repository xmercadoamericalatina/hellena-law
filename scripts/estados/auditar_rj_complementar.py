"""Complementa o snapshot RJ com gates de anexo, tabelas, imagens e CSS.

Somente leitura. CSS externo não capturado permanece um limite explícito.
A mera presença de tabela não prova a presença de anexo/objeto aprovado.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[1])]
from snapshots.auditar_rj_cache_20261021_001 import one as original, parser
from pe_fidelidade_visivel import texto_visivel_html
from tabelas_estrutura import _Tabelas
from auditar_pe_cache import APP

BASE_ICONE = 'http://alerjln1.alerj.rj.gov.br/icons/'
IMAGENS_INTERFACE = [dict(width=str(w), height='1', src=BASE_ICONE+'ecblank.gif', border='0', alt='') for w in (1, 76, 113, 151)] + [dict(width='16', height='16', src=BASE_ICONE+'collapse.gif', border='0', alt='Hide details for Texto da Lei   [ Em Vigor ]')]
CSS_POTENCIAL = re.compile(r'line-through|display\s*:\s*none|visibility\s*:\s*(?:hidden|collapse)|mso-hide\s*:\s*all|(?:^|[;{])\s*opacity\s*:\s*0(?:\.0*)?\s*(?:!important\s*)?(?:[;}]|$)|font-size\s*:\s*0(?:\.0*)?(?:[a-z%]+)?\s*(?:!important\s*)?(?:[;}]|$)', re.I)
OWN = re.compile(r'\banex[oa]s?\s+(?:[úu]nic[oa]s?\s+|[IVXLC0-9]+\s+)?(?:desta|deste|a\s+esta|a\s+este|[àa]\s+presente)\b', re.I)


def matrizes(html):
    p = _Tabelas(); p.feed(html); p.close()
    if p.pilha:
        raise ValueError('tabela sem fechamento')
    return [[dict(linha=c['linha'], rowspan=c['rowspan'], colspan=c['colspan'], texto=' '.join(''.join(c['texto']).split())) for c in t['celulas']] for t in p.tabelas if t['linha'] > 1]


def complementar(field, pagina, body, imagens):
    problemas = []; source = texto_visivel_html(field); own = OWN.search(source); app = APP.search(source)
    if own and not re.search(r'(?im)^\s*[#*\s]*ANEXO\b', body):
        problemas.append('anexo próprio ou citação contextual exige revisão; tabela genérica não comprova anexo')
    if app and not re.search(r'(?im)^\s*[#*\s]*(?:ANEXO|REGULAMENTO|REGIMENTO|ESTATUTO|PLANO|MANUAL)\b', body):
        problemas.append('objeto aprovado sem título representado exige revisão contextual')
    desconhecidas = [i for i in imagens if i not in IMAGENS_INTERFACE]
    if desconhecidas:
        problemas.append('imagem sem identidade exata de interface comprovada')
    source_tables = matrizes(field); rendered_tables = matrizes(parser.render(body))
    if source_tables != rendered_tables:
        problemas.append('matrizes multilinhas divergem')
    regras = [css for css in re.findall(r'<style\b[^>]*>(.*?)</style\s*>', pagina, re.I | re.S) if CSS_POTENCIAL.search(css)]
    if regras:
        problemas.append('regra CSS local potencialmente histórica/oculta exige contexto')
    if re.search(r'Wingdings|Webdings|face\s*=\s*["\']?Symbol\b', field, re.I):
        problemas.append('fonte de símbolos exige revisão visual')
    return problemas, dict(remissao_literal=own[0] if own else None, objeto_literal=app[0] if app else None,
                           imagens_nao_comprovadas=desconhecidas, total_tabelas_multilinhas=len(source_tables),
                           matrizes_conferem=source_tables == rendered_tables, regras_CSS_potenciais=regras)


def one(path):
    r = original(path)
    if not r.get('cache'):
        return r
    try:
        pagina = gzip.decompress(Path(r['cache']).read_bytes()).decode('utf-8')
        a, b = r['limite_campo']; field = pagina[a:b]
        body = Path(path).read_text().split('\n---\n', 1)[1].split('\n', 1)[1]
        body = re.sub(r'^# [^\n]*\n', '', body, count=1).strip()
        issues, proof = complementar(field, pagina, body, r['evidencias'].get('imagens', []))
        r['problemas'].extend(issues); r['QA_complementar'] = proof
    except Exception as e:
        r['problemas'].append(type(e).__name__+': '+str(e))
    r['publicavel'] = not r['problemas']
    return r


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lista', required=True); ap.add_argument('--saida', required=True)
    args = ap.parse_args()
    with Path(args.saida).open('x') as out:
        for i, p in enumerate(Path(args.lista).read_text().splitlines(), 1):
            if not p.startswith('estaduais/RJ/') or '..' in Path(p).parts:
                raise ValueError(p)
            r = one(p); out.write(json.dumps(r, ensure_ascii=False)+'\n'); out.flush()
            if i % 25 == 0:
                print('PROGRESSO', i, flush=True)
