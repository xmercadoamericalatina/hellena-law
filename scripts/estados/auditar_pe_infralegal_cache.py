"""QA de capturas PE infralegais por índice e respostas oficiais congeladas.

Somente leitura; documento capturado não é publicável por contagem. Rejeita
imagens, tachados/ocultação, anexos/objetos não comprovados e divergências de
identidade ou de CommonMark. CSS externo ausente da captura não é certificado.
"""
import argparse
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from markdown_it import MarkdownIt
from coletar_pe_infralegal import identidade_primaria
from pe import limites_texto_html, TIPOS
from comum import decodificar, html_para_md
from auditar_pe_recuperacao_utf8 import metadados, matrizes
from pe_fidelidade_visivel import texto_visivel_html, _heading_comprovado, assinatura_numerica
from auditar_pe_commonmark_contexto import Counters
from auditar_pe_cache import APP, FOREIGN
from integridade_texto import verificar_integridade_texto
from avisos_fonte import avisos_de_omissao
from anexos_fonte import remissoes_sem_representacao

SHA = lambda b: hashlib.sha256(b).hexdigest()
PARSER = MarkdownIt('commonmark', {'html': True}).enable('table')
RISCO = re.compile(r'<(?:img|svg|canvas|object|embed|iframe|script|s|strike|del|math|v:\w+|m:oMath)\b|\bon\w+\s*=|javascript\s*:|line-through|display\s*:\s*none|visibility\s*:\s*(?:hidden|collapse)|mso-hide\s*:\s*all|opacity\s*:\s*0(?:\.0*)?\s*(?:!important\s*)?(?:[;}\s"\x27]|$)|font-size\s*:\s*0(?:\.0*)?(?:[a-z%]+)?\s*(?:!important\s*)?(?:[;}\s"\x27]|$)|color\s*:\s*transparent|\bhidden(?:\s|=|>)|aria-hidden\s*=\s*["\x27]?true|Wingdings|Webdings|(?:font-family\s*:\s*|face\s*=\s*)["\x27]?\s*Symbol\b|class\s*=\s*["\x27][^"\x27]*(?:tachad|revogad|riscad|desativad|deleted)', re.I)
OWN = re.compile(r'\banex[oa]s?\s+(?:[úu]nic[oa]s?\s+|[IVXLC0-9]+\s+)?(?:desta|deste|a\s+esta|a\s+este|[àa]\s+presente)\b', re.I)


def auditar(raw, source, item, ctype='text/html; charset=utf-8'):
    text = raw.decode('utf-8'); meta = metadados(text); pagina = decodificar(source, ctype)
    numero, data, ep = identidade_primaria(item, pagina)
    if re.sub(r'[.\s]', '', meta['numero']).upper().lstrip('0') != numero.lstrip('0'):
        raise ValueError('número do MD diverge de índice/epígrafe')
    if meta['tipo'] != TIPOS[item['tipo']][1] or meta['data'] != data or meta['ano'] != data[:4]:
        raise ValueError('tipo/data/ano do MD divergem da epígrafe própria')
    modo = 'TEXTOATUALIZADO' if 'TEXTOATUALIZADO' in item['textos'] else 'TEXTOORIGINAL'
    url = 'https://legis.alepe.pe.gov.br/texto.aspx?id='+item['id']+'&tipo='+modo
    if meta['fonte'] != url or meta['versao_texto'] != ('atualizada' if modo == 'TEXTOATUALIZADO' else 'original'):
        raise ValueError('fonte/versão diverge do índice oficial')
    if meta.get('revogada') is not None:
        raise ValueError('revogada não pode ser inferida sem prova literal de situação')
    if meta.get('publicacao') != item['publicacao'] or meta.get('ementa') != item['ementa']:
        raise ValueError('publicação/ementa divergem do índice')
    a, b = limites_texto_html(pagina); field = pagina[a:b]
    if RISCO.search(field):
        raise ValueError('visual/ativo/tachado/ocultação/fonte de símbolos exige contexto')
    if re.search(r'<(?:ol|ul)\b', field, re.I):
        raise ValueError('lista HTML nativa exige associação contextual')
    body = text.split('\n---\n', 1)[1]; body = re.sub(r'^\s*# [^\n]*\n', '', body, count=1).strip()
    converted = html_para_md(field); issue, dispositivo = verificar_integridade_texto(converted)
    if issue:
        raise ValueError(issue)
    if avisos_de_omissao(converted) or remissoes_sem_representacao(converted):
        raise ValueError('aviso/remissão sem representação comprovada')
    source_visible = texto_visivel_html(field); own = OWN.search(source_visible); app = APP.search(source_visible)
    if own and not re.search(r'(?im)^\s*[#*\s]*ANEXO\b', body):
        raise ValueError('remissão própria ou citada a anexo exige contexto; tabela genérica não comprova')
    if app and not re.search(r'(?im)^\s*[#*\s]*(?:ANEXO|REGULAMENTO|REGIMENTO|ESTATUTO|PLANO|MANUAL)\b', body):
        raise ValueError('objeto aprovado sem título representado exige contexto')
    if any(re.sub(r'\D', '', m[2]) != re.sub(r'\D', '', numero) for m in FOREIGN.finditer(converted.replace('*', ''))):
        raise ValueError('outra epígrafe completa exige revisão de granularidade')
    tokens = PARSER.parse(body); lists = [dict(start=t.attrGet('start') or 1, markup=t.markup, linhas=t.map) for t in tokens if t.type == 'ordered_list_open']
    rendered = PARSER.render(body); counters = Counters(lists); counters.feed(rendered)
    visible, heading_proof = _heading_comprovado(texto_visivel_html(''.join(counters.out)), body, source_visible)
    if visible != source_visible or assinatura_numerica(visible) != assinatura_numerica(source_visible):
        raise ValueError('CommonMark integral/sinais/pontuação divergem da fonte')
    tables = matrizes(field)
    if tables != matrizes(rendered):
        raise ValueError('matrizes de tabela multilinha divergem')
    return dict(epigrafe_literal=ep, data=data, numero=numero, tipo=meta['tipo'], versao=modo,
                sha256_fonte=SHA(source), sha256_campo=SHA(field.encode()), limites_campo=[a,b],
                dispositivo_proprio=dispositivo, igualdade_visivel_CommonMark=True,
                assinatura_numerica_sinais=True, tabelas_multilinhas=len(tables), listas=counters.proofs,
                normalizacoes_heading=heading_proof)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--capturas', required=True); ap.add_argument('--saida', required=True)
    args = ap.parse_args(); log = Path(args.capturas).read_bytes()
    log = log[:log.rfind(b'\n')+1]  # coletor pode continuar; nunca ler uma linha parcial
    rows = [json.loads(l) for l in log.splitlines()]; rows = [r for r in rows if r['status'] == 'ok']
    with Path(args.saida).open('x') as out:
        for i, r in enumerate(rows, 1):
            result = dict(path=r['path'], id_oficial=r['id_oficial'], item_indice=r['item_indice'], cache=r['cache'], captura=r['captura'], aceito=False,
                          auditado_em=dt.datetime.now(ZoneInfo('America/Recife')).isoformat(), bytes_prefixo_log=len(log), sha256_prefixo_log=SHA(log), sha256_codigo_auditor=SHA(Path(__file__).read_bytes()))
            try:
                raw = Path(r['path']).read_bytes(); assert SHA(raw) == r['sha256_md'], 'MD mudou desde captura'
                z = Path(r['cache']).read_bytes(); source = gzip.decompress(z)
                assert SHA(source) == r['sha256_resposta']
                assert gzip.decompress(Path(r['captura']).read_bytes()) == source
                proof = auditar(raw, source, r['item_indice'], r['content_type'])
                result.update(aceito=True, sha256_md=SHA(raw), sha256_cache=SHA(z), QA=proof)
            except Exception as e:
                result['motivo'] = type(e).__name__+': '+str(e)
            out.write(json.dumps(result, ensure_ascii=False)+'\n'); out.flush()
            if i % 100 == 0:
                print('PROGRESSO', i, flush=True)
