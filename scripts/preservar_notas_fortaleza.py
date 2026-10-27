"""Acrescenta três notas literais da fonte SAPL de Fortaleza, sem mudar dispositivos.

As referências judiciais são atribuídas ao portal municipal; não se infere o
alcance das decisões nem se corrige a numeração de processo grafada na fonte.
"""
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from converter_organica_fortaleza import converter
from html2md import convert
ROOT = Path(__file__).resolve().parent.parent
DOC = Path('municipais/CE/fortaleza/lei-organica/2006/lei-organica-1-2006.md')
SOURCE = Path('municipais/_fonte/capitais/fortaleza/lei-organica-2006-sapl44.html')
OLD = '5383b555d6d642eb734c8fbd63444cd4ea789cb8221ccef7a0dcc5adb7f268ef'
SOURCE_SHA = 'a3770625ec2abf27f8fc85a7bf41c97865f7d1cca5f74a157df76b92eabb602d'
IDS = {'2710': 'art. 168, § 5º', '4773': 'art. 177, § 8º', '4774': 'art. 177, § 9º'}


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Notas(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.current = None
        self.depth = 0
        self.parts = []
        self.notes = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if not self.current and tag == 'div' and a.get('id') in {'dn' + n for n in IDS}:
            self.current = a['id'][2:]
            self.parts = []
            self.depth = 0
        if self.current:
            self.parts.append(self.get_starttag_text())
            self.depth += tag == 'div'

    def handle_endtag(self, tag):
        if self.current:
            self.parts.append('</' + tag + '>')
            self.depth -= tag == 'div'
            if self.depth == 0:
                if self.current in self.notes:
                    raise ValueError('Nota repetida')
                self.notes[self.current] = ''.join(self.parts)
                self.current = None

    def handle_data(self, text):
        if self.current:
            self.parts.append(text)

    def handle_entityref(self, text):
        self.handle_data('&' + text + ';')

    def handle_charref(self, text):
        self.handle_data('&#' + text + ';')


class TextoNota(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.links = []

    def handle_data(self, text):
        self.parts.append(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs)['href'])


def reparar(html, old_body):
    md, parsed = converter(html)
    if old_body.rstrip('\n') != md.rstrip('\n'):
        raise ValueError('Corpo anterior não corresponde ao snapshot')
    np = Notas()
    np.feed(html)
    if np.current or set(np.notes) != set(IDS):
        raise ValueError('Três notas esperadas ausentes ou incompletas')
    pieces = []
    additions = []
    notes = []
    for block in parsed.ativos:
        piece = convert(block['html'], exclude_struck=True)
        if block['tachado_interno_omitido']:
            piece += '\n\n_Nota editorial: a fonte contém redação tachada neste dispositivo; esse texto histórico foi omitido desta transcrição e permanece no HTML original._'
        ident = block['id'].removeprefix('dptt')
        if ident in IDS:
            text = TextoNota()
            text.feed(np.notes[ident])
            literal = ' '.join(' '.join(text.parts).split())
            if len(text.links) != 1 or not text.links[0].startswith('https://esaj.tjce.jus.br/'):
                raise ValueError('Referência judicial divergente')
            note = ('> Nota literal da fonte municipal, vinculada ao ' + IDS[ident] + ':\n>\n> ' + literal + '\n>\n> Referência informada pelo portal: [Diário da Justiça do TJCE](' + text.links[0] + ').')
            additions.append('\n\n' + note)
            piece += additions[-1]
            notes.append({'id_dispositivo': block['id'], 'id_nota': 'dn' + ident, 'dispositivo': IDS[ident], 'texto_literal': literal, 'link_informado': text.links[0], 'html': np.notes[ident], 'sha256_html': sha(np.notes[ident].encode()), 'trecho_inserido': note})
        if piece.strip():
            pieces.append(piece)
    new_md = '\n\n'.join(pieces)
    reconstructed = new_md
    for addition in additions:
        if reconstructed.count(addition) != 1:
            raise ValueError('Inserção não é única')
        reconstructed = reconstructed.replace(addition, '', 1)
    if reconstructed != md:
        raise ValueError('Houve alteração além das três notas')
    return new_md + old_body[len(md):], notes


def main():
    path = ROOT / DOC
    old = path.read_bytes()
    raw = (ROOT / SOURCE).read_bytes()
    if sha(old) != OLD or sha(raw) != SOURCE_SHA:
        raise ValueError('Preimagem ou fonte mudou')
    header, rest = old.decode().split('\n---\n', 1)
    title, body = rest.lstrip('\n').split('\n\n', 1)
    new_body, notes = reparar(raw.decode(), body)
    for key, value in [('sha256_texto', sha(new_body[:-1].encode())), ('versao_texto', 'compilação do SAPL marcada como atual, vigência a partir de 30/06/2025 dada pela Emenda 25/2025; dispositivos desativados excluídos, marcadores de revogação e três notas literais de inconstitucionalidade da fonte municipal preservados; referências atribuídas ao portal, sem inferir alcance judicial ou certificar vigência integral')]:
        header = re.sub(r'(?m)^' + key + r':.*$', lambda match: key + ': ' + json.dumps(value, ensure_ascii=False), header)
    new = header + '\n---\n\n' + title + '\n\n' + new_body
    out = ROOT / 'municipais/_lotes/20261020-fortaleza-notas-constitucionalidade'
    out.mkdir(exist_ok=False)
    (out / 'documento-anterior.md').write_bytes(old)
    for note in notes:
        (out / (note['id_nota'] + '.html')).write_text(note['html'])
    (out / 'notas-literais.json').write_text(json.dumps(notes, ensure_ascii=False, indent=2))
    path.write_text(new)
    (out / 'normas.paths.txt').write_text(str(DOC) + '\n')
    receipt = {'documento': str(DOC), 'sha256_head_preimagem': OLD, 'head_verificado': '8f6cef4dfd68542f03852ddb09492b08be7a458e', 'sha256': sha(path.read_bytes()), 'fonte': str(SOURCE), 'sha256_fonte': SOURCE_SHA, 'notas_inseridas': 3, 'prova': 'Remover exatamente as três inserções reconstrói todo o corpo anterior byte a byte. A preimagem integral corresponde ao arquivo no HEAD informado.', 'script_sha256': sha(Path(__file__).read_bytes()), 'limite': 'As três notas e os links são declarações literais da fonte municipal. O processo 0620174-36.2023.8.06.000 é preservado com a grafia da fonte. A consulta dos links do TJCE retornou página sem texto acessível; não foi inferido alcance judicial.'}
    (out / 'manifesto.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == '__main__':
    main()
