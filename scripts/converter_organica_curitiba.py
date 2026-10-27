"""LO deCuritiba: bloco oficial Texto alterado, preservando notas e marcadores.

Somente sete segmentos< s >do snapshot são históricos omitidos; o HTML integral
fica no acervo. A indicação EmVigor é atribuída ao portal, não certificação legal.
"""
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from html2md import convert
from comum import yaml_str

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path('municipais/_fonte/capitais/curitiba/captura-63d8488d93187c08dfca.bin')


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Bloco(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.depth = 0
        self.found = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if self.depth:
            self.parts.append(self.get_starttag_text())
            self.depth += tag == 'div'
        elif tag == 'div' and dict(attrs).get('id') == 'alterado_conteudo':
            self.found += 1
            self.depth = 1

    def handle_endtag(self, tag):
        if self.depth:
            self.depth -= tag == 'div'
            if self.depth:
                self.parts.append('</' + tag + '>')

    def handle_startendtag(self, tag, attrs):
        if self.depth:
            self.parts.append(self.get_starttag_text())

    def handle_data(self, text):
        if self.depth:
            self.parts.append(text)

    def handle_entityref(self, name):
        self.handle_data('&' + name + ';')

    def handle_charref(self, name):
        self.handle_data('&#' + name + ';')


class Texto(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []
        self.old = []

    def handle_starttag(self, tag, attrs):
        if tag == 's':
            self.skip += 1
            self.old.append('')

    def handle_endtag(self, tag):
        if tag == 's':
            self.skip -= 1

    def handle_data(self, text):
        if self.skip:
            self.old[-1] += text
        else:
            self.parts.append(text)


def converter(html):
    parser = Bloco()
    parser.feed(html)
    if parser.found != 1 or parser.depth:
        raise ValueError('Bloco alterado ausente, múltiplo ou incompleto')
    fragment = ''.join(parser.parts)
    text = Texto()
    text.feed(fragment)
    if text.skip:
        raise ValueError('Segmento histórico incompleto')
    md = convert(fragment, exclude_struck=True)
    if re.findall(r'\w+', ' '.join(text.parts)) != re.findall(r'\w+', md):
        raise ValueError('Confronto integral diverge')
    return md, fragment, text.old


def main():
    raw = (ROOT / SOURCE).read_bytes()
    if sha(raw) != '9a313009f55a332c50c24d22416328c6b10bc9d5475298d45adc41a5900fc0a5':
        raise ValueError('Snapshot diferente; revisar novamente')
    html = raw.decode()
    md, fragment, old = converter(html)
    if len(old) != 7 or re.search(r'<(?:img|table)\b', fragment, re.I):
        raise ValueError('Estrutura difere da revisão')
    if not all(mark in md for mark in ['Art. 1º', 'Art. 214', 'Art. 215', 'ATO DAS DISPOSIÇÕES TRANSITÓRIAS', 'Revogado.']):
        raise ValueError('Marcos normativos ausentes')
    ibge = json.loads((ROOT / 'municipais/_indice/ibge-municipios.json').read_text())
    city = next(r for r in ibge if str(r['id']) == '4106902')
    if city['nome'] != 'Curitiba' or city['regiao-imediata']['regiao-intermediaria']['UF']['sigla'] != 'PR':
        raise ValueError('Identidade IBGE diverge')
    target = ROOT / 'municipais/PR/curitiba/lei-organica/1990/lei-organica-curitiba-1990.md'
    if target.exists() or any(target.parent.parent.glob('**/*.md')):
        raise ValueError('LO existente requer conciliação de versões')
    note = ('Nota de transcrição: esta é a opção “Texto alterado” do portal oficial, que indica a situação “Em Vigor”. '
            'Sete segmentos tachados foram omitidos desta redação e permanecem identificados no HTML integral e no controle histórico. '
            'Os marcadores de revogação e as notas de emendas foram preservados; o portal não informa um corte expresso de atualização.\n\n')
    body = note + md
    title = 'Lei Orgânica do Município de Curitiba, de 5 de abril de 1990'
    meta = {'titulo': title, 'tipo': 'Lei Orgânica', 'numero': '', 'data': '1990-04-05',
            'data_publicacao_na_fonte': '1990-04-10', 'municipio': 'Curitiba', 'uf': 'PR', 'codigo_ibge': '4106902',
            'origem_data': 'campo Assinado em do portal oficial; publicação indicada em10/04/1990, DiárioOficial27',
            'versao_texto': 'Texto alterado do portal oficial capturado em20/10/2026; corte de atualização não declarado; sete segmentos tachados históricos omitidos, notas e Revogado preservados; sem certificação de vigência integral',
            'fonte': 'https://legisladocexterno.curitiba.pr.gov.br/VisualizarHTML.aspx?id=335597',
            'fonte_texto': 'https://legisladocexterno.curitiba.pr.gov.br/VisualizarHTML.aspx?id=335597',
            'sha256_fonte': sha(raw), 'sha256_texto': sha(body.encode()), 'baixado_em': '2026-10-20'}
    result = '\n'.join(['---'] + [k + ': ' + yaml_str(v) for k, v in meta.items()] + ['revogada: null', '---', '', '# ' + title, '', body, ''])
    out = ROOT / 'municipais/_lotes/20261020-curitiba-lo'
    out.mkdir(exist_ok=False)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(result)
    (out / 'historico-tachado.json').write_text(json.dumps({'fonte': str(SOURCE), 'sha256_fonte': sha(raw), 'segmentos_historicos': old}, ensure_ascii=False, indent=2))
    (out / 'bloco-alterado.html').write_text(fragment)
    receipt = {'documento': str(target.relative_to(ROOT)), 'sha256': sha(target.read_bytes()), 'fonte': str(SOURCE),
               'sha256_fonte': sha(raw), 'tokens_ativos_em_ordem': len(re.findall(r'\w+', md)),
               'historicos_omitidos': 7, 'marcadores_revogacao_preservados': md.lower().count('revogad'),
               'anexos_na_interface': 'sem anexos', 'imagens_ou_tabelas_no_bloco': 0,
               'verificacao': 'Todos os tokens ativos em ordem idênticos à leitura independente do HTML; navegação e painel do PDF original excluídos pelo ID do bloco.',
               'script_sha256': sha(Path(__file__).read_bytes()),
               'limite': 'Situação EmVigor é declaração do portal; corte de atualização não explicitado. Data vem do campo oficial, sem inventar número para epígrafe vazia.'}
    (out / 'manifesto.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
    (out / 'normas.paths.txt').write_text(str(target.relative_to(ROOT)) + '\n')
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == '__main__':
    main()
