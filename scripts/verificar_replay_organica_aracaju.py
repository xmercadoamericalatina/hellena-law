"""Replay independente do MD de Aracaju contra extração nativa integral fresca.

Somente leitura: não chama o conversor de Markdown nem altera a norma. Remove
da comparação apenas os rótulos editoriais explícitos, cuja quantidade e posição
também são conferidas contra a prova congelada e o plano visual.
"""
import argparse
import gzip
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
sys.path.insert(0, '/tmp/constituicao-markdown-qa-20261020')
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
RECEIPT = Path('municipais/_lotes/20261021-aracaju-lo/entrega-final.json')
RECEIPT_SHA = 'dcd131a8f376f923bfe7d67fabe3d49b99d523026e7ea5696d0d6fea6d8bfe8d'
LABEL = r'⟦(?:INÍCIO DO TRECHO TACHADO NA FONTE, página \d+, grupo \d+|FIM DO TRECHO TACHADO NA FONTE)⟧'


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Code(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pre = False
        self.current = None
        self.blocks = []

    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.pre = True
        if tag == 'code' and self.pre:
            self.current = []

    def handle_endtag(self, tag):
        if tag == 'code' and self.current is not None:
            self.blocks.append(''.join(self.current))
            self.current = None
        if tag == 'pre':
            self.pre = False

    def handle_data(self, data):
        if self.current is not None:
            self.current.append(data)


def verificar():
    receipt_raw = (ROOT/RECEIPT).read_bytes()
    if sha(receipt_raw) != RECEIPT_SHA:
        raise ValueError('Recibo original mudou')
    receipt = json.loads(receipt_raw)
    inventory = {r['arquivo']: r for r in receipt['arquivos']}
    def read(rel):
        raw = (ROOT/rel).read_bytes()
        record = inventory[rel]
        if sha(raw) != record['sha256'] or len(raw) != record['bytes']:
            raise ValueError('Hash ou tamanho diverge: '+rel)
        return raw
    raw = read(receipt['documento'])
    pdf = 'municipais/_fonte/capitais/aracaju/lei-organica-atualizada.pdf'
    read(pdf)
    native = subprocess.check_output(['/opt/homebrew/bin/pdftotext','-layout','-enc','UTF-8',str(ROOT/pdf),'-']).decode()
    archived = json.loads(gzip.decompress(read('municipais/_lotes/20261021-aracaju-lo/extracao-integral.json.gz')))
    if native != archived['layout_original']:
        raise ValueError('Extração fresca difere da nativa congelada; revisar versão/ordem')
    text = raw.decode()
    body = text.split('\n---\n',1)[1].lstrip('\n').split('\n\n',1)[1][:-1]
    stored = re.search(r'^sha256_texto: "([0-9a-f]{64})"$',text,re.M)
    if not stored or sha(body.encode()) != stored[1]:
        raise ValueError('Hash do corpo diverge')
    engine = MarkdownIt('commonmark',{'html':True}).enable('table').enable('strikethrough')
    if sum(t.type == 'fence' for t in engine.parse(body)) != 1:
        raise ValueError('Corpo normativo não está em bloco preformatado único')
    rendered = engine.render(body)
    code = Code()
    code.feed(rendered)
    if len(code.blocks) != 1:
        raise ValueError('HTML renderizado não tem bloco normativo único')
    content = code.blocks[0]
    expected = archived['layout_com_rotulos'].replace('\f','\n\n').rstrip('\n')+'\n'
    if content != expected:
        raise ValueError('Rótulos/posição ou conteúdo renderizado divergem da prova congelada')
    opens = re.findall(r'⟦INÍCIO DO TRECHO TACHADO NA FONTE, página (\d+), grupo (\d+)⟧',content)
    plan = json.loads(read('municipais/_lotes/20261021-aracaju-inspecao-tachados/plano-contextual.json'))
    if sorted((int(p),int(g)) for p,g in opens) != sorted((g['pagina'],g['grupo']) for g in plan['grupos']) or content.count('⟦FIM DO TRECHO TACHADO NA FONTE⟧') != 73:
        raise ValueError('Plano de distinção histórica não preservado')
    visible = re.sub(LABEL,'',content)
    a, b = ''.join(native.split()), ''.join(visible.split())
    if a != b:
        raise ValueError('Fonte/renderização divergem em caracteres oficiais, pontuação ou sinais')
    return dict(aprovado=True,documento=receipt['documento'],sha256_md=sha(raw),fonte=pdf,
                sha256_pdf=inventory[pdf]['sha256'],motor='markdown-it-py 4.0.0 CommonMark + table + strikethrough',
                extracao_nativa_fresca_igual_congelada=True,replay_caracteres_nao_brancos=True,
                pontuacao_sinais_alineas_folios_preservados=True,passagens_tachadas_identificadas=73,
                sha256_visivel_fonte=sha(a.encode()),sha256_visivel_renderizado=sha(b.encode()),
                sha256_html_renderizado=sha(rendered.encode()),limite='Notas editoriais fora do bloco são identificadas como tais; nenhum texto oficial é removido da comparação, somente os rótulos acrescentados.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--saida',type=Path,required=True)
    args = ap.parse_args()
    result = verificar()
    with args.saida.open('x') as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps(result,ensure_ascii=False))
