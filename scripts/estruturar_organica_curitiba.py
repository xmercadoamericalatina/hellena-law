"""Reproduz parágrafos de Curitiba pelas quebras HTML, sem herdar negritos mal fechados."""
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from converter_organica_curitiba import Bloco, converter, SOURCE, ROOT


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Paragrafos(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []
        self.events = []

    def boundary(self, tag):
        if not self.skip:
            self.parts.append('\n')
            self.events.append({'tag': tag, 'posicao_html': self.getpos()})

    def handle_starttag(self, tag, attrs):
        if tag == 's':
            self.skip += 1
        elif tag in {'br', 'p', 'h1', 'h2', 'div'}:
            self.boundary(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag == 's':
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == 's':
            self.skip -= 1
        elif tag in {'p', 'h1', 'h2', 'div'}:
            self.boundary('/' + tag)

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(re.sub(r'\s+', ' ', data))

    def result(self):
        if self.skip:
            raise ValueError('Histórico incompleto')
        return '\n\n'.join(re.sub(r' +', ' ', line).strip() for line in ''.join(self.parts).split('\n') if line.strip()) + '\n'


def estruturar(html):
    b = Bloco()
    b.feed(html)
    if b.found != 1 or b.depth:
        raise ValueError('Bloco alterado inválido')
    fragment = ''.join(b.parts)
    p = Paragrafos()
    p.feed(fragment)
    result = p.result()
    previous, _, _ = converter(html)
    if re.findall(r'\w+', previous) != re.findall(r'\w+', result):
        raise ValueError('Sequência de palavras diverge da conversão anterior')
    return result, p.events


def main():
    target = ROOT / 'municipais/PR/curitiba/lei-organica/1990/lei-organica-curitiba-1990.md'
    old = target.read_bytes()
    if sha(old) != '5a69eec183c09c1752bbc3898b034dbc691954c35401111cfe8a61dccff246d1':
        raise ValueError('Documento anterior mudou')
    raw = (ROOT / SOURCE).read_bytes()
    if sha(raw) != '9a313009f55a332c50c24d22416328c6b10bc9d5475298d45adc41a5900fc0a5':
        raise ValueError('Fonte mudou')
    new_body, events = estruturar(raw.decode())
    text = old.decode()
    header, rest = text.split('\n---\n', 1)
    title, body = rest.lstrip('\n').split('\n\n', 1)
    note, previous_body = body.split('\n\n', 1)
    replacement = note + '\n\n' + new_body
    header = re.sub(r'(?m)^sha256_texto:.*$', 'sha256_texto: ' + sha(replacement.encode()), header)
    result = header + '\n---\n\n' + title + '\n\n' + replacement + '\n'
    if re.findall(r'\w+', previous_body) != re.findall(r'\w+', new_body):
        raise ValueError('Palavras ou notas mudaram')
    out = ROOT / 'municipais/_lotes/20261020-curitiba-estrutura-v2'
    out.mkdir(exist_ok=False)
    backup = out / 'documento-anterior.md'
    backup.write_bytes(old)
    target.write_text(result)
    proof = {'fonte': str(SOURCE), 'sha256_fonte': sha(raw), 'limites_html': events,
             'tokens_ativos_em_ordem': len(re.findall(r'\w+', new_body)),
             'paragrafos': len(new_body.strip().split('\n\n')),
             'criterio': 'Parágrafos separados somente em br, p, h1, h2 e div da fonte. Negritos mal fechados não são herdados. Palavras e notas permanecem na mesma sequência. Junções literais como Art. 4ºConstituem já estão no HTML e são preservadas, sem emenda editorial.'}
    (out / 'prova-estrutura.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2))
    receipt = {'documento': str(target.relative_to(ROOT)), 'sha256_anterior': sha(old), 'sha256': sha(target.read_bytes()),
               'backup': str(backup.relative_to(ROOT)), 'sha256_backup': sha(backup.read_bytes()),
               'prova': str((out / 'prova-estrutura.json').relative_to(ROOT)),
               'sha256_prova': sha((out / 'prova-estrutura.json').read_bytes()),
               'script_sha256': sha(Path(__file__).read_bytes()),
               'snapshot_anterior_preservado': 'municipais/_lotes/20261020-curitiba-lo',
               'tokens_ativos_em_ordem': proof['tokens_ativos_em_ordem'], 'paragrafos': proof['paragrafos']}
    (out / 'manifesto.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
    (out / 'normas.paths.txt').write_text(str(target.relative_to(ROOT)) + '\n')
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == '__main__':
    main()
