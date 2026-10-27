"""Inventário suplementar das cores de texto de PDFs, sem decidir vigência.

Preserva valores originais de cor, páginas e amostras. Cores podem indicar
notas, links, títulos ou redações históricas e exigem inspeção contextual.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import pdfplumber


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chave(c):
    return json.dumps(c, sort_keys=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pdf', type=Path, action='append', required=True)
    ap.add_argument('--saida', type=Path, required=True)
    a = ap.parse_args()
    a.saida.mkdir(parents=True, exist_ok=False)
    rows = []
    for path in a.pdf:
        counts = Counter()
        pages = defaultdict(set)
        samples = defaultdict(list)
        with pdfplumber.open(path) as doc:
            total = len(doc.pages)
            for i, page in enumerate(doc.pages, 1):
                groups = defaultdict(list)
                for c in page.chars:
                    if c.get('text', '').strip():
                        k = chave(c.get('non_stroking_color'))
                        counts[k] += 1
                        pages[k].add(i)
                        groups[k].append(c)
                for k, chars in groups.items():
                    if len(samples[k]) < 12:
                        samples[k].append({'pagina': i, 'texto': ''.join(c['text'] for c in chars)[:1200]})
                page.close()
                if i % 50 == 0:
                    print(json.dumps({'pdf': str(path), 'pagina': i}), flush=True)
        rows.append({'pdf': str(path), 'sha256_fonte': sha(path), 'total_paginas': total,
                     'cores': [{'cor_original': json.loads(k), 'caracteres': v,
                                'paginas': sorted(pages[k]), 'amostras': samples[k]}
                               for k, v in counts.most_common()]})
        print(json.dumps({'pdf': str(path), 'fim': True, 'cores': len(counts)}), flush=True)
    (a.saida / 'controle.json').write_text(json.dumps(
        {'criterio': __doc__, 'script_sha256': sha(Path(__file__)), 'documentos': rows},
        ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
