"""Replay independente CommonMark/GFM contra a área ativa oficial do SAPL.

Não importa html2md nem o conversor de dispositivos. Conserva todos os caracteres
não brancos, inclusive pontuação e sinais. Exclusões: dispositivos desativados e
tachados explícitos; a nota editorial conhecida é retirada apenas se o HTML tem
tachado. Listas Markdown usam o contador efetivo de ol/start, não o número digitado.
"""
import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, '/tmp/constituicao-markdown-qa-20261020')
sys.path.insert(0, str(Path(__file__).resolve().parent / 'estados'))
from markdown_it import MarkdownIt
from pe_fidelidade_visivel import texto_visivel_html, assinatura_numerica, _heading_comprovado

ROOT = Path(__file__).resolve().parent.parent
NOTE = '_Nota editorial: a fonte contém redação tachada neste dispositivo; esse texto histórico foi omitido desta transcrição e permanece no HTML original._'
VOID = {'br', 'hr', 'img', 'meta', 'link', 'input', 'wbr', 'col', 'area', 'source', 'embed', 'param'}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def compact(s):
    return ''.join(s.split())


class AtivosIndependentes(HTMLParser):
    """Seleção por estado em pilha, independente do agrupador do materializador."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.out = []
        self.ativos = []
        self.historicos = []
        self.tachados = 0
        self.listas_nativas = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get('class', '').split()
        inherited = self.stack[-1] if self.stack else {'active': False, 'hidden': False, 'struck': False}
        current = dict(inherited, tag=tag)
        if 'dptt' in classes:
            if inherited['active']:
                raise ValueError('Dispositivo aninhado requer revisão')
            current['hidden'] = inherited['hidden'] or 'desativado' in classes
            current['active'] = not current['hidden']
            (self.ativos if current['active'] else self.historicos).append(attrs.get('id'))
        struck = tag in {'s', 'del', 'strike'} or 'line-through' in attrs.get('style', '').lower()
        if current['active'] and struck and not inherited['struck']:
            self.tachados += 1
        current['struck'] = inherited['struck'] or struck
        if current['active'] and not current['struck']:
            if tag in {'ol', 'ul'}:
                self.listas_nativas += 1
            if tag in {'p', 'div', 'br', 'li', 'td', 'th', 'tr', 'table'}:
                self.out.append(' ')
        if tag not in VOID:
            self.stack.append(current)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1]['active'] and not self.stack[-1]['struck']:
            self.out.append(' ')
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i]['tag'] == tag:
                del self.stack[i:]
                break

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_data(self, s):
        if self.stack and self.stack[-1]['active'] and not self.stack[-1]['struck']:
            self.out.append(s)


class Counters(HTMLParser):
    """Materializa o número que o navegador exibe em cada item Markdown."""
    def __init__(self, lists):
        super().__init__(convert_charrefs=False)
        self.lists = iter(lists)
        self.stack = []
        self.out = []
        self.proofs = []

    def handle_starttag(self, tag, attrs):
        self.out.append(self.get_starttag_text())
        d = dict(attrs)
        if tag == 'ol':
            ast = next(self.lists)
            start = int(d.get('start', '1'))
            if start != ast['start']:
                raise ValueError('Início da lista diverge da AST')
            proof = dict(ast=ast, inicio_efetivo=start, contadores=[])
            self.proofs.append(proof)
            self.stack.append(dict(n=start, ast=ast, proof=proof))
        elif tag == 'ul':
            self.stack.append(None)
        elif tag == 'li' and self.stack and self.stack[-1] is not None:
            ctx = self.stack[-1]
            n = int(d.get('value', ctx['n']))
            ctx['n'] = n + 1
            self.out.append(html.escape(str(n) + ctx['ast']['markup'] + ' '))
            ctx['proof']['contadores'].append(n)

    def handle_endtag(self, tag):
        self.out.append('</' + tag + '>')
        if tag in {'ol', 'ul'}:
            self.stack.pop()

    def handle_data(self, s):
        self.out.append(s)

    def handle_entityref(self, s):
        self.out.append('&' + s + ';')

    def handle_charref(self, s):
        self.out.append('&#' + s + ';')


def comparar(source, body):
    p = AtivosIndependentes()
    p.feed(source)
    p.close()
    if not p.ativos or p.listas_nativas:
        raise ValueError('Área ativa ausente ou lista HTML nativa exige associação contextual própria')
    notes = body.count(NOTE)
    if notes and not p.tachados:
        raise ValueError('Nota editorial sem tachado explícito na fonte')
    body = body.replace(NOTE, '')
    source_visible = ' '.join(''.join(p.out).split())
    engine = MarkdownIt('commonmark', {'html': True}).enable('table').enable('strikethrough')
    tokens = engine.parse(body)
    lists = [dict(start=t.attrGet('start') or 1, markup=t.markup, linhas=t.map)
             for t in tokens if t.type == 'ordered_list_open']
    rendered = engine.render(body)
    counters = Counters(lists)
    counters.feed(rendered)
    visible = texto_visivel_html(''.join(counters.out))
    normalized, headings = _heading_comprovado(visible, body, source_visible)
    a, b = compact(source_visible), compact(normalized)
    i = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    return dict(aprovado=a == b, igualdade_caracteres_nao_brancos=a == b,
                assinatura_numerica_confere=assinatura_numerica(a) == assinatura_numerica(b),
                ativos=p.ativos, historicos_excluidos=p.historicos,
                tachados_explicitos_excluidos=p.tachados, notas_editoriais_excluidas=notes,
                normalizacoes_heading=headings, listas=counters.proofs,
                sha256_visivel_fonte=sha(a.encode()), sha256_visivel_renderizado=sha(b.encode()),
                sha256_html_renderizado=sha(rendered.encode()),
                contexto=None if a == b else dict(indice=i, fonte=a[max(0,i-90):i+190],
                                                  renderizado=b[max(0,i-90):i+190]))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lista', type=Path, required=True)
    ap.add_argument('--materializados', type=Path, required=True)
    ap.add_argument('--saida', type=Path, required=True)
    args = ap.parse_args()
    rows = {r.get('path'): r for r in map(json.loads, (args.materializados/'resultados.jsonl').read_text().splitlines()) if r.get('aprovado')}
    result = []
    for rel in args.lista.read_text().splitlines():
        b = (ROOT/rel).read_bytes()
        row = dict(path=rel, sha256=sha(b), aprovado=False)
        try:
            r = rows[rel]
            source_b = (ROOT/r['prova_frontend']['arquivo']).read_bytes()
            if sha(b) != r['sha256'] or sha(source_b) != r['prova_frontend']['sha256']:
                raise ValueError('Preimagem ou fonte mudou')
            body = b.decode().split('\n---\n', 1)[1].lstrip('\n').split('\n\n', 1)[1]
            row.update(comparar(source_b.decode(), body))
            row['fonte'] = r['prova_frontend']
        except Exception as e:
            row['erro'] = type(e).__name__ + ': ' + str(e)
        result.append(row)
    args.saida.mkdir(parents=True, exist_ok=False)
    for name, selected in [('aprovados', True), ('retidos', False)]:
        (args.saida/(name+'.paths.txt')).write_text(''.join(r['path']+'\n' for r in result if r['aprovado'] == selected))
    control = dict(motor='markdown-it-py 4.0.0 CommonMark + table + strikethrough',
                   criterio='Comparação sequencial de todos os caracteres não brancos do HTML oficial ativo com o HTML renderizado; nenhuma pontuação, sinal ou número é descartado. Contadores reais de listas são materializados.',
                   arquivos=len(result), aprovados=sum(r['aprovado'] for r in result),
                   retidos=sum(not r['aprovado'] for r in result), resultados=result,
                   codigo_sha256=sha(Path(__file__).read_bytes()))
    (args.saida/'controle.json').write_text(json.dumps(control, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: control[k] for k in ('arquivos', 'aprovados', 'retidos')}))


if __name__ == '__main__':
    main()
