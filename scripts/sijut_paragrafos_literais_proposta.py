"""Proposta offline: representação explícita de segmentos SIJUT estritamente literais.

Não coleta, não publica e não altera a extração padrão. HTML, anexos ou estilos
ativos exigem outra prova; não são achatados para caber neste modo.
"""
import html
import re

MODO = 'html-paragrafos-literais-sijut-v1'


def extrair_literal(doc):
    if not all(doc.get(k) is True for k in ('integro', 'publicado', 'internet')):
        raise ValueError('fonte não declara texto íntegro e público')
    if not doc.get('outrosSegmentos'):
        raise ValueError('texto integral insuficiente')
    segmentos = doc.get('ementas', []) + doc.get('outrosSegmentos', [])
    ativos = [s for s in segmentos if not s.get('omitir') and s.get('original')]
    ids, ordens, partes = set(), set(), []
    for s in ativos:
        ident, ordem = s.get('idSegmento'), s.get('ordemSegmentoAto')
        if type(ident) is not int or type(ordem) is not int or ident in ids or ordem in ordens:
            raise ValueError('ID/ordem de segmento ausente, ambíguo ou repetido')
        ids.add(ident); ordens.add(ordem)
        texto = s.get('textoIntegra', '')
        if not isinstance(texto, str) or '\x00' in texto:
            raise ValueError('texto de segmento inválido')
        if s.get('arquivoBinario'):
            raise ValueError('anexo exige representação e prova próprias')
        if s.get('tachado') or s.get('estiloSegmento') or s.get('agendado'):
            raise ValueError('tachado, estilo ou agendamento exige prova própria')
        if s.get('ancorasOrigem') or s.get('ancorasDestino'):
            raise ValueError('âncoras exigem prova contextual própria')
        if re.search(r'<\s*(?:[A-Za-z/!?])|&(?:#\d+|#x[0-9a-f]+|[A-Za-z][A-Za-z0-9]+);', texto, re.I):
            raise ValueError('HTML ou entidade exige interpretação própria')
        partes.append((ordem, ident, texto))
    partes.sort()
    abertura = next((t.lstrip() for _, _, t in partes if t.strip()), '')
    if re.match(r'^(?:Retifica(?:ção|ções|cao|coes)|Erratas?|Onde se l[êe])\b', abertura, re.I):
        raise ValueError('visão contém somente retificação; exige classificação própria')
    if sum(len(t) for _, _, t in partes) < 100:
        raise ValueError('texto integral insuficiente')
    return '\n\n'.join(
        '<p data-segmento="{}" data-ordem="{}" style="white-space: pre-wrap">{}</p>'.format(
            ident, ordem, html.escape(texto, quote=False)) for ordem, ident, texto in partes)


def extrair_para_auditoria(doc, meta, rfb, offline):
    modo = meta.get('representacao_texto')
    if modo is None:
        return rfb.extrair(doc, offline)
    if modo != MODO:
        raise ValueError('representação textual desconhecida')
    return extrair_literal(doc)
