"""Preserva toda a camada nativa por página, sem heurísticas de margem ou números.

Somente candidatos explícitos. Confere layout e palavras por coordenadas antes
de substituir o Markdown, mantendo backup e prova compacta de cada fonte.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_municipal import metadados
ROOT = Path(__file__).resolve().parent.parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def confrontar(layout, bbox):
    xml = ET.fromstring(bbox)
    pages = [p for p in xml.iter() if p.tag.rsplit('}', 1)[-1] == 'page']
    chunks = layout.split('\f')
    if chunks[-1].strip() or len(chunks) - 1 != len(pages):
        raise ValueError('Quantidade física de páginas diverge')
    if not any(c.strip() for c in chunks):
        raise ValueError('Camada nativa vazia não confirma OCR')
    for i, (chunk, page) in enumerate(zip(chunks[:-1], pages), 1):
        a = re.findall(r'\w+', chunk)
        b = re.findall(r'\w+', ' '.join(w.text or '' for w in page.iter() if w.tag.rsplit('}', 1)[-1] == 'word'))
        if a != b:
            raise ValueError('Ordem de palavras diverge na página ' + str(i))
    return len(pages), len(re.findall(r'\w+', layout))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lista', type=Path, required=True)
    ap.add_argument('--saida', type=Path, required=True)
    a = ap.parse_args()
    a.saida = a.saida.resolve()
    a.saida.mkdir(exist_ok=False)
    rows = []
    for rel in a.lista.read_text().splitlines():
        path = ROOT / rel
        old = path.read_bytes()
        row = {'path': rel, 'sha256_anterior': sha(old)}
        try:
            m = metadados(old.decode())
            u = urlsplit(m['fonte'])
            pdf = ROOT / 'municipais/_fonte/organicas-sapl' / u.hostname / (u.path.rstrip('/').split('/')[-1] + '.bin')
            source = pdf.read_bytes()
            if sha(source) != m['sha256_fonte']:
                raise ValueError('Fonte mudou')
            layout = subprocess.check_output(['/opt/homebrew/bin/pdftotext', '-layout', '-enc', 'UTF-8', str(pdf), '-']).decode()
            bbox = subprocess.check_output(['/opt/homebrew/bin/pdftotext', '-bbox-layout', '-enc', 'UTF-8', str(pdf), '-'])
            pages, tokens = confrontar(layout, bbox)
            header, rest = old.decode().split('\n---\n', 1)
            title, previous = rest.lstrip('\n').split('\n\n', 1)
            body = '```text\n' + layout.replace('\f', '\n\n').rstrip('\n') + '\n```'
            if re.findall(r'\w+', body[8:-4]) != re.findall(r'\w+', layout):
                raise ValueError('Transcrição diverge')
            version = (m.get('versao_texto', '').rstrip('; ') + '; camada nativa integral preservada em layout, incluindo cabeçalhos, notas, fólios, linhas numéricas e alinhamentos; snapshot da fonte capturado em 20/10/2026, sem certificação de vigência integral')
            for k, v in [('versao_texto', version), ('sha256_texto', sha(body.encode()))]:
                header = re.sub(r'(?m)^' + k + r':.*$', lambda match: k + ': ' + json.dumps(v, ensure_ascii=False), header)
            new = header + '\n---\n\n' + title + '\n\n' + body + '\n'
            stem = sha(rel.encode())
            backup = a.saida / (stem + '.anterior.md')
            backup.write_bytes(old)
            proof = a.saida / (stem + '.extracao.json.gz')
            with proof.open('xb') as f:
                f.write(gzip.compress(json.dumps({'layout': layout, 'bbox': bbox.decode(), 'pdf': str(pdf.relative_to(ROOT)), 'sha256_fonte': sha(source)}, ensure_ascii=False).encode(), mtime=0))
            row.update({'aprovado': True, 'sha256': sha(new.encode()), 'sha256_fonte': sha(source), 'pdf': str(pdf.relative_to(ROOT)), 'paginas': pages, 'tokens': tokens,
                'backup': str(backup.relative_to(ROOT)), 'sha256_backup': sha(old), 'prova': str(proof.relative_to(ROOT)), 'sha256_prova': sha(proof.read_bytes())})
            path.write_text(new)
        except Exception as err:
            row.update({'aprovado': False, 'pendencia': str(err)})
        rows.append(row)
    for name, accepted in [('aprovados', True), ('retidos', False)]:
        (a.saida / (name + '.paths.txt')).write_text(''.join(r['path'] + '\n' for r in rows if r['aprovado'] == accepted))
    result = {'criterio': __doc__, 'script_sha256': sha(Path(__file__).read_bytes()), 'lista_sha256': sha(a.lista.read_bytes()), 'resultados': rows}
    (a.saida / 'manifesto.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps({'aprovados': sum(r['aprovado'] for r in rows), 'retidos': sum(not r['aprovado'] for r in rows)}))


if __name__ == '__main__':
    main()
