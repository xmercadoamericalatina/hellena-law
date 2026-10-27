"""Recupera integralmente o snapshot oficial da LO de João Pessoa, edição junho2026.

Não remove números, cabeçalhos, notas de emenda nem páginas textualmente vazias.
O brasão repetido foi revisto visualmente; o texto não contém tachado detectado.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_municipal import metadados

ROOT = Path(__file__).resolve().parent.parent
DOC = Path('municipais/PB/joao-pessoa/lei-organica/1990/lei-organica-1-1990-sapl-14101.md')
PDF = Path('municipais/_fonte/organicas-sapl/sapl.joaopessoa.pb.leg.br/14101.bin')
OLD = '7a49a93c53c2f24bb747d90a687854bf78f796863eb240c42d01aee686873e1b'
SOURCE = 'f859ade2226d6f03c01c2e2816990b68851354ed6d51d5ce54106bd0072ad825'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    out = ROOT / 'municipais/_lotes/20261020-joao-pessoa-integral'
    out.mkdir(exist_ok=False)
    path = ROOT / DOC
    raw = path.read_bytes()
    if sha(raw) != OLD or sha((ROOT / PDF).read_bytes()) != SOURCE:
        raise ValueError('Snapshot diverge')
    layout = subprocess.check_output(['/opt/homebrew/bin/pdftotext', '-layout', '-enc', 'UTF-8', str(ROOT / PDF), '-']).decode()
    bbox = subprocess.check_output(['/opt/homebrew/bin/pdftotext', '-bbox-layout', '-enc', 'UTF-8', str(ROOT / PDF), '-'])
    xml = ET.fromstring(bbox)
    pages = [e for e in xml.iter() if e.tag.rsplit('}', 1)[-1] == 'page']
    chunks = layout.split('\f')
    if chunks[-1].strip() or len(chunks) - 1 != len(pages) or len(pages) != 102:
        raise ValueError('Contagem física diverge')
    for i, (chunk, page) in enumerate(zip(chunks[:-1], pages), 1):
        source_tokens = re.findall(r'\w+', ' '.join(e.text or '' for e in page.iter() if e.tag.rsplit('}', 1)[-1] == 'word'))
        target_tokens = re.findall(r'\w+', chunk)
        # O título com sombra da capa é separado em letras pelo bbox; somente
        # nessa página, a sequência integral de caracteres deve ser idêntica.
        same_cover = i == 1 and ''.join(source_tokens) == ''.join(target_tokens)
        if source_tokens != target_tokens and not same_cover:
            raise ValueError('Layout e coordenadas divergem na página ' + str(i))
    text = raw.decode()
    cab, resto = text.split('\n---\n', 1)
    title = resto.strip().split('\n\n', 1)[0]
    body = '```text\n' + layout.replace('\f', '\n\n').rstrip('\n') + '\n```'
    if re.findall(r'\w+', body[8:-4]) != re.findall(r'\w+', layout):
        raise ValueError('Transcrição diverge')
    version = ('compilação oficial de junho de 2026, atualizada até a Emenda à Lei Orgânica nº44/2026; '
               'transcrição integral da camada nativa, com notas, cabeçalhos, fólios e valores preservados; '
               'brasão institucional repetido conferido visualmente; sem certificação de atualização posterior ou vigência integral')
    for key, value in [('versao_texto', version), ('sha256_texto', sha(body.encode()))]:
        cab = re.sub('(?m)^' + key + ':.*$', lambda m: key + ': ' + json.dumps(value, ensure_ascii=False), cab)
    new = cab + '\n---\n\n' + title + '\n\n' + body + '\n'
    (out / 'documento-anterior.md').write_bytes(raw)
    (out / 'fonte-layout.txt').write_text(layout)
    (out / 'fonte-bbox.xhtml').write_bytes(bbox)
    path.write_text(new)
    manifest = {'documento': str(DOC), 'sha256_anterior': OLD, 'sha256_novo': sha(path.read_bytes()),
                'pdf': str(PDF), 'sha256_fonte': SOURCE, 'paginas_fisicas': 102,
                'paginas_vazias': [i for i, c in enumerate(chunks[:-1], 1) if not c.strip()],
                'tokens_preservados': len(re.findall(r'\w+', layout)),
                'confronto': 'Todos os tokens em ordem por página: layout versus bbox, incluindo páginas vazias. Exceção restrita à capa: bbox separa título em letras; sequência integral de caracteres idêntica, título confirmado visualmente.',
                'api_anexos': 'municipais/_lotes/20261020-capitais-natal-joao-pessoa-anexos/overlay.json',
                'alerta_revisado': 'Extrato do contrato no incisoXXX do art70 é disposição própria; p41 conferida visualmente, não publicação de contrato alheio.',
                'script_sha256': sha(Path(__file__).read_bytes()),
                'artefatos': [{'arquivo': str(p.relative_to(ROOT)), 'sha256': sha(p.read_bytes())} for p in out.iterdir()]}
    (out / 'manifesto.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == '__main__':
    main()
