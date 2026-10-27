"""Confere números literais de epígrafes anteriores ao artigo inicial.

Sufixos alfabéticos são parte da identidade. Uma API com 1B e PDF com 01
permanece pendente. Ausência de epígrafe clara não confirma o número nem a data.
"""
import argparse
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_municipal import metadados
ROOT = Path(__file__).resolve().parent.parent
MESES = {m: i for i, m in enumerate('JANEIRO FEVEREIRO MARCO ABRIL MAIO JUNHO JULHO AGOSTO SETEMBRO OUTUBRO NOVEMBRO DEZEMBRO'.split(), 1)}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def normal(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.upper()) if unicodedata.category(c) != 'Mn')


def numero(s):
    value = re.sub(r'[^A-Z0-9]', '', normal(str(s)))
    return value.lstrip('0') or '0'


def analisar(meta, layout):
    article = re.search(r'\bART(?:IGO)?\.?\s*1[º°o.\s]', layout, re.I)
    header = normal(layout[:min(article.start() if article else 4000, 4000)])
    pattern = r'^\s*(LEI(?:\s+(?:COMPLEMENTAR|ORDINARIA|MUNICIPAL|DELEGADA)){0,2}|RESOLUCAO(?:\s+(?:ADMINISTRATIVA|LEGISLATIVA))?|DECRETO(?:\s+(?:LEGISLATIVO|MUNICIPAL|NORMATIVO))?)\s+(?:N[º°O.\s]*\s*)?(\d[\d.]*[A-Z]?)\s*(?=[/,]|$|\bDE\b)'
    own = normal(meta['tipo'])
    own = 'RESOLUCAO' if own.startswith('RESOLU') else 'DECRETO' if own.startswith('DECRETO') else 'LEI'
    found = []
    for m in re.finditer(pattern, header, re.M):
        if not m[1].startswith(own):
            continue
        # Exige data ou ano em sequência para distinguir título e remissão.
        tail = header[m.end():m.end() + 100]
        if not re.match(r'\s*(?:/\s*\d{4}|[,.-]?\s*(?:DE\s+)?\d{1,2}[º°]?\s+(?:DE\s+)?\w+\s+DE\s+\d{4})', tail):
            continue
        row = {'tipo': m[1], 'numero': m[2], 'numero_normalizado': numero(m[2]), 'trecho': header[m.start():m.end() + 120]}
        date = re.match(r'\s*[,.-]?\s*(?:DE\s+)?(\d{1,2})[º°]?\s+(?:DE\s+)?(\w+)\s+DE\s+(\d{4})', tail)
        if date and date[2] in MESES:
            try:
                row['data_literal'] = dt.date(int(date[3]), MESES[date[2]], int(date[1])).isoformat()
            except ValueError:
                row['data_literal'] = 'data inválida'
        found.append(row)
    mismatch = [r for r in found if r['numero_normalizado'] != numero(meta['numero'])]
    date_mismatch = [r for r in found if r.get('data_literal') and meta.get('data') and r['data_literal'] != meta['data']]
    return {'epigrafes': found, 'numero_metadado': meta['numero'], 'numero_literal_confirmado': bool(found) and not mismatch,
            'data_literal_confirmada': bool(found) and all(r.get('data_literal') == meta.get('data') for r in found) and bool(meta.get('data')),
            'divergencias': mismatch + date_mismatch, 'limite': 'Tipo completo continua sujeito aos demais controles; ausência de epígrafe ou data não confirma identidade.'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lista', type=Path, required=True)
    ap.add_argument('--evidencias', type=Path, required=True)
    ap.add_argument('--saida', type=Path, required=True)
    a = ap.parse_args()
    source = [json.loads(line) for line in a.evidencias.read_text().splitlines()]
    evidence = {r['path']: r['evidencia_extracao'] for r in source if r.get('evidencia_extracao')}
    rows = []
    a.saida.mkdir(exist_ok=False)
    for rel in a.lista.read_text().splitlines():
        b = (ROOT / rel).read_bytes()
        row = {'path': rel, 'sha256': sha(b)}
        try:
            e = evidence[rel]
            raw = (ROOT / e['path']).read_bytes()
            if sha(raw) != e['sha256']:
                raise ValueError('Extração mudou')
            row.update(analisar(metadados(b.decode()), json.loads(gzip.decompress(raw))['layout']))
            row['evidencia'] = e
        except Exception as err:
            row['pendencia'] = str(err)
        rows.append(row)
    (a.saida / 'controle.json').write_text(json.dumps({'criterio': __doc__, 'script_sha256': sha(Path(__file__).read_bytes()), 'resultados': rows}, ensure_ascii=False, indent=2))
    (a.saida / 'sem-divergencia.paths.txt').write_text(''.join(r['path'] + '\n' for r in rows if not r.get('pendencia') and not r['divergencias']))
    print(json.dumps({'documentos': len(rows), 'divergentes': sum(bool(r.get('divergencias') or r.get('pendencia')) for r in rows), 'numeros_confirmados_literalmente': sum(bool(r.get('numero_literal_confirmado')) for r in rows)}))


if __name__ == '__main__':
    main()
