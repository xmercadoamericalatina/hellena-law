"""Revisa tipos do acervo herdado; remove só categorias interpretativas explícitas.

Uso: python3 -I scripts/lei_seca/sanear_legado.py [--aplicar]
Requer checkout dos diretórios de legislação. O relatório registra também tipos desconhecidos.
Não certifica a redação ou a vigência dos documentos herdados.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import BLOCKED, allowed_kind, digest, now, write_json


def field(header, key):
    match = re.search(r'^' + re.escape(key) + r':\s*(.+)$', header, re.M)
    if not match:
        return ''
    value = match.group(1).strip()
    try:
        return json.loads(value)
    except ValueError:
        return value.strip("'\"")


def scan(root, apply=False):
    removed, unknown, count = [], Counter(), 0
    for folder in ['federal', 'estaduais', 'municipais', 'reguladores', 'tratados', 'jurisprudencia']:
        for path in (root / folder).rglob('*.md'):
            relative = path.relative_to(root).as_posix()
            if any(part.startswith('_') for part in path.relative_to(root).parts):
                continue
            data = path.read_bytes()
            text = data.decode('utf-8', errors='strict')
            header = text.split('\n---', 1)[0] if text.startswith('---\n') else ''
            kind = str(field(header, 'tipo'))
            reason = 'jurisprudencia' if folder == 'jurisprudencia' else 'tipo_interpretativo' if BLOCKED.search(kind) else ''
            count += 1
            if reason:
                removed.append({'arquivo': relative, 'tipo': kind, 'motivo': reason, 'sha256': digest(data)})
                if apply:
                    path.unlink()
            elif not allowed_kind(kind):
                unknown[kind or '(sem tipo)'] += 1
    report = {'executado_em': now(), 'aplicado': apply, 'examinados': count,
              'excluidos' if apply else 'exclusoes_propostas': removed,
              'tipos_nao_classificados': dict(unknown),
              'aviso': 'Tipos desconhecidos são preservados para revisão; este relatório não certifica todo o legado.'}
    write_json(root / 'lei-seca' / 'saneamento-legado.json', report)
    print(json.dumps({'examinados': count, 'interpretativos': len(removed), 'tipos_desconhecidos': dict(unknown)}, ensure_ascii=False))
    return report


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument('--aplicar', action='store_true')
    a = ap.parse_args()
    scan(a.root, a.aplicar)
