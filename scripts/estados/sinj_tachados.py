"""Edição do histórico SINJ: CSS div.strike comprovado convertido em marca semântica.

Não certifica vigência. A fonte original não é alterada; a transformação só torna
explícito ao conversor o estilo herdado que o SINJ declara na própria página.
"""
import html
from html.parser import HTMLParser
import re
from html2md import convert


class _TachadosSINJ(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.offsets = [0] + [m.end() for m in re.finditer('\n', source)]
        self.edits = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag != 'div' or 'strike' not in (values.get('class') or '').split():
            return
        style = values.get('style') or ''
        decorations = re.findall(r'(?:^|;)\s*text-decoration\s*:\s*([^;]*)', style, re.I)
        if decorations and 'line-through' not in decorations[-1].casefold():
            return  # an explicit inline declaration overrides this element's class rule
        values['style'] = style.rstrip(';') + ';text-decoration:line-through'
        opening = '<div' + ''.join(' ' + k + ('' if v is None else '="' + html.escape(v, quote=True) + '"') for k, v in values.items()) + '>'
        line, column = self.getpos()
        offset = self.offsets[line - 1] + column
        self.edits.append((offset, offset + len(self.get_starttag_text()), opening))


def explicitar_css_tachado(source):
    styles = '\n'.join(re.findall(r'<style\b[^>]*>(.*?)</style>', source, re.I | re.S))
    confirmed = bool(re.search(r'\bdiv\.strike\s*\{[^{}]*text-decoration\s*:[^;{}]*line-through', styles, re.I))
    parser = _TachadosSINJ(source)
    parser.feed(source)
    parser.close()
    if parser.edits and not confirmed:
        raise ValueError('classe SINJ div.strike ativa sem regra CSS line-through comprovada')
    result = source
    for begin, end, opening in reversed(parser.edits):
        result = result[:begin] + opening + result[end:]
    return result, len(parser.edits)


def _converter(source, exclude_struck):
    converted = convert(source, exclude_struck=exclude_struck)
    blocks = converted.split('\n\n')
    while blocks and re.sub(r'[*\\\s]+', ' ', blocks[0]).strip() in {'Texto Compilado', 'Texto Original'}:
        blocks.pop(0)
    return '\n\n'.join(blocks).strip()


def converter_html_sinj(source, *, compilado, situacao):
    mapped, css_blocks = explicitar_css_tachado(source)
    historical = _converter(mapped, False)
    has_struck = css_blocks or bool(re.search(r'<(?:s|strike|del)\b|style\s*=\s*[\"\'][^\"\']*line-through', source, re.I))
    if not has_struck:
        return historical, 'compilada (SINJ-DF)' if compilado else 'original', {'blocos_css_tachados': 0, 'edicao': 'sem tachado ativo'}
    literal = situacao.strip()
    revoked = literal.casefold() in {'revogada', 'revogado'}
    if not compilado or revoked:
        why = 'situação oficial: ' + literal if revoked else 'publicação original'
        return historical, 'histórica (SINJ-DF; marcações tachadas preservadas)', {'blocos_css_tachados': css_blocks, 'edicao': 'histórica', 'motivo': why, 'situacao_literal': literal, 'redacoes_historicas_preservadas': True}
    current = _converter(mapped, True)
    plain = current.replace('*', '').replace('#', '')
    has_provision = bool(re.search(r'(?im)^\s*(?:Art(?:igo)?\.?\s*(?:\d+[º°o.]?|[uú]nico)(?:\b|\s)|[IVXL]+\s*[-–.])', plain))
    if not has_provision:
        return historical, 'histórica (SINJ-DF; dispositivo atual não identificado)', {'blocos_css_tachados': css_blocks, 'edicao': 'histórica', 'motivo': 'exclusão dos tachados não deixou dispositivo atual identificável; não se inferiu revogação integral', 'situacao_literal': literal, 'redacoes_historicas_preservadas': True}
    return current, 'compilada (SINJ-DF; redações tachadas excluídas)', {'blocos_css_tachados': css_blocks, 'edicao': 'compilada filtrada', 'situacao_literal': literal, 'redacoes_tachadas_excluidas': True, 'vigencia_nao_inferida': True}
