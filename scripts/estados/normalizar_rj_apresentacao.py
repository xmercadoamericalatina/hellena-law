"""Normaliza somente hardbreaks RJ com prova de DOM CommonMark idêntico."""
from html.parser import HTMLParser
import re

from markdown_it import MarkdownIt

PARSER = MarkdownIt('commonmark', {'html': True}).enable('table')


class DOM(HTMLParser):
    VOID = {'br', 'hr', 'img', 'meta', 'link', 'input', 'wbr', 'col'}

    def __init__(self):
        super().__init__(convert_charrefs=True); self.tokens = []; self.stack = []

    def handle_starttag(self, tag, attrs):
        self.tokens.append(('start', tag, tuple(sorted(attrs))))
        if tag not in self.VOID:
            sensitive = tag in {'pre', 'code'} or any(k == 'style' and re.search(r'white-space\s*:\s*(?:pre|break-spaces)', v or '', re.I) for k,v in attrs)
            self.stack.append((tag, sensitive))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        self.tokens.append(('end', tag))
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]; break

    def handle_data(self, text):
        if not any(sensitive for _,sensitive in self.stack):
            text = ' '.join(text.split())
        if text:
            self.tokens.append(('data', text))


def dom(html):
    p = DOM(); p.feed(html); p.close(); return p.tokens


def normalizar(body):
    lines = body.split('\n')
    normalized = '\n'.join(re.sub(r'[ \t]+$', '', line) if not line.strip() or i+1 == len(lines) or not lines[i+1].strip() else re.sub(r' {2,}$', '<br>', line) for i,line in enumerate(lines))
    before = PARSER.render(body); after = PARSER.render(normalized)
    if dom(before) != dom(after):
        raise ValueError('normalização mudaria DOM/whitespace preformatado; reter original')
    if any(line.endswith((' ', '\t')) for line in normalized.splitlines()):
        raise ValueError('whitespace residual exige contexto')
    return normalized
