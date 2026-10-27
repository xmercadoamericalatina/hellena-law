"""Triagem suplementar de tabelas, tachados e cores para listas SAPL integrais.

Somente leitura. Tabelas detectadas, cores não pretas e candidatos vetoriais
permanecem retidos para revisão contextual; ausência não certifica vigência.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pdfplumber
from auditar_municipal import metadados
from auditar_tachados_pdf_municipal import analisar_pagina

ROOT = Path(__file__).resolve().parent.parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def cor_preta(c):
    if c is None:
        return False
    if isinstance(c, (int, float)):
        return c == 0
    if isinstance(c, (list, tuple)):
        return tuple(c) in {(0,), (0, 0, 0), (0, 0, 0, 1)}
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lista', type=Path, required=True)
    ap.add_argument('--saida', type=Path, required=True)
    a = ap.parse_args()
    a.saida.mkdir(exist_ok=False)
    rows = []
    for rel in a.lista.read_text().splitlines():
        b = (ROOT / rel).read_bytes()
        m = metadados(b.decode())
        u = urlsplit(m['fonte'])
        pdf = ROOT / 'municipais/_fonte/organicas-sapl' / u.hostname / (u.path.rstrip('/').split('/')[-1] + '.bin')
        row = {'path': rel, 'sha256': sha(b), 'pdf': str(pdf.relative_to(ROOT)), 'sha256_fonte': sha(pdf.read_bytes()), 'paginas': []}
        try:
            if row['sha256_fonte'] != m['sha256_fonte']:
                raise ValueError('Fonte mudou')
            with pdfplumber.open(pdf) as doc:
                for i, page in enumerate(doc.pages, 1):
                    hits = analisar_pagina(page)
                    tables = page.find_tables()
                    chars = [c for c in page.chars if c.get('text', '').strip() and not cor_preta(c.get('non_stroking_color'))]
                    if hits or tables or chars:
                        row['paginas'].append({'pagina': i, 'tachados_candidatos': hits,
                            'tabelas': [{'bbox': list(t.bbox), 'linhas': len(t.rows), 'colunas': len(t.columns)} for t in tables],
                            'cores_nao_pretas': [{'texto': c['text'], 'cor': c.get('non_stroking_color')} for c in chars]})
                    page.close()
            row['sem_suspeitas_detectadas'] = not row['paginas']
        except Exception as e:
            row['pendencia'] = str(e)
            row['sem_suspeitas_detectadas'] = False
        rows.append(row)
        print(json.dumps({'path': rel, 'sem_suspeitas_detectadas': row['sem_suspeitas_detectadas']}), flush=True)
    for name, accepted in [('aprovados', True), ('retidos', False)]:
        (a.saida / (name + '.paths.txt')).write_text(''.join(r['path'] + '\n' for r in rows if r['sem_suspeitas_detectadas'] == accepted))
    (a.saida / 'controle.json').write_text(json.dumps({'criterio': __doc__, 'script_sha256': sha(Path(__file__).read_bytes()), 'lista_sha256': sha(a.lista.read_bytes()), 'resultados': rows}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
