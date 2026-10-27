"""Leitura de texto, tabelas e conteúdo visual em HTML normativo federal."""
import re
from html.parser import HTMLParser

class Visivel(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.data = []
        self.structure = []
        self.visual = []

    def handle_starttag(self, tag, attrs):
        if tag in {'head', 'style', 'script', 'title', 'xml'}:
            self.skip += 1
        if not self.skip:
            if tag in {'table', 'tr', 'td', 'th'}:
                self.structure.append((tag, tuple(sorted((k, v) for k, v in attrs if k in {'rowspan', 'colspan'}))))
            if tag in {'img', 'svg', 'object', 'embed', 'iframe', 'canvas', 'math'} or tag.startswith('v:') or tag.startswith('m:'):
                self.visual.append(tag)

    def handle_comment(self, data):
        # Office conditional comments may contain normative image fallbacks.
        if not self.skip and re.search(r'\[if\b', data, re.I):
            tags = re.findall(r'<((?:[a-z]+:)?(?:img|svg|object|embed|iframe|canvas|math)|v:[a-z]+|m:[a-z]+)\b', data, re.I)
            self.visual.extend('condicional:' + tag.lower() for tag in tags)

    def handle_endtag(self, tag):
        if tag in {'head', 'style', 'script', 'title', 'xml'}:
            self.skip = max(0, self.skip - 1)

    def handle_data(self, data):
        if not self.skip:
            self.data.append(data)
