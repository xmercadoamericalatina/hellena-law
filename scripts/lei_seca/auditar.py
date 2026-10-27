"""Verifica escopo, originais, hashes, índice e correspondência dos textos publicados."""
import argparse
import gzip
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import MAX_BYTES, allowed_kind, digest, read_json, validate_url


def audit(root):
    errors = []
    index_path = root / 'indice.json'
    index = read_json(index_path, [])
    ids = set()
    for row in index:
        ident = row['id']
        try:
            if not re.fullmatch(r'[a-zA-Z0-9_-]+', ident) or ident in ids:
                raise ValueError('ID inseguro ou duplicado')
            ids.add(ident)
            m = read_json(root / 'metadados' / (ident + '.json'))
            if not m or not allowed_kind(m['tipo']) or m.get('politica') != 'lei-seca-v1':
                raise ValueError('Metadados fora da política')
            validate_url(m['url_texto'])
            expected = 'originais/' + m['sha256_original'][:2] + '/' + m['sha256_original'] + '.gz'
            if m['original'] != expected:
                raise ValueError('Caminho do original divergente')
            with gzip.open(root / expected, 'rb') as f:
                data = f.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES or digest(data) != m['sha256_original']:
                raise ValueError('Hash do original divergente')
            document = (root / 'textos' / (ident + '.md')).read_text(encoding='utf-8')
            fence = re.search(r'^(`{3,})text\n', document, re.M)
            if not fence:
                raise ValueError('Texto sem bloco literal')
            text = document[fence.end():]
            suffix = fence.group(1) + '\n'
            if not text.endswith(suffix):
                raise ValueError('Bloco literal truncado')
            text = text[:-len(suffix)]
            if digest(text.encode()) != m['sha256_texto'] or row['sha256_texto'] != m['sha256_texto']:
                raise ValueError('Hash do texto divergente')
        except Exception as exc:
            errors.append(ident + ': ' + str(exc))
    actual = {p.stem for p in (root / 'metadados').glob('*.json')}
    if actual != ids:
        errors.append('Índice e metadados não correspondem')
    return errors


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pasta', type=Path)
    a = ap.parse_args()
    problems = audit(a.pasta)
    print(json.dumps({'erros': problems}, ensure_ascii=False, indent=2))
    sys.exit(bool(problems))
