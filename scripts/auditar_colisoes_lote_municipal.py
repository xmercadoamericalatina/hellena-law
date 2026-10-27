"""Compara lote municipal com baseline congelado e entregas finais explícitas."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_municipal import metadados
from auditar_epigrafes_literais_sapl import normal, numero


def sha(b):
    return hashlib.sha256(b).hexdigest()


def paths(p):
    return p.read_text().replace('\0', '\n').splitlines()


def keys(text, path):
    m = metadados(text)
    result = []
    for field in ('fonte', 'fonte_texto'):
        if m.get(field):
            result.append(('url', m[field].split('#', 1)[0].rstrip('/')))
    kind = normal(str(m.get('tipo', '')))
    if kind in {'LEI', 'LEI ORDINARIA'}:
        kind = 'LEI ORDINARIA'
    parts = Path(path).parts
    city = str(m.get('codigo_ibge') or '/'.join(parts[1:3]))
    if kind and m.get('data'):
        result.append(('identidade', city, kind, numero(str(m.get('numero', ''))), str(m['data'])[:4]))
        # Acervo anterior pode não ter codigo_ibge; a rota municipal canônica
        # também permite confrontá-lo com o lote novo que já traz esse código.
        result.append(('identidade_rota', '/'.join(parts[1:3]), kind, numero(str(m.get('numero', ''))), str(m['data'])[:4]))
    return list(dict.fromkeys(result))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--baseline', type=Path, required=True)
    ap.add_argument('--adicional', action='append', type=Path, default=[])
    ap.add_argument('--lista', type=Path, required=True)
    ap.add_argument('--saida', type=Path, required=True)
    a = ap.parse_args()
    index = collections.defaultdict(set)
    baseline = set(p for f in [a.baseline]+a.adicional for p in paths(f)
                   if p.startswith('municipais/') and p.endswith('.md') and not any(x.startswith('_') for x in Path(p).parts))
    for p in sorted(baseline):
        for k in keys(Path(p).read_text(), p):
            index[k].add(p)
    collisions = []
    candidates = paths(a.lista)
    for p in candidates:
        for k in keys(Path(p).read_text(), p):
            if index.get(k):
                collisions.append(dict(path=p, chave=k, existentes=sorted(index[k])))
            index[k].add(p)
    result = dict(comparados=len(baseline), candidatos=len(candidates), colisoes=collisions,
                  fontes=[dict(arquivo=str(p), sha256=sha(p.read_bytes())) for p in [a.baseline]+a.adicional],
                  criterio='URL oficial da norma e do texto articulado; IBGE/tipo/número/ano, mantendo sufixos alfanuméricos. Também compara candidatos internamente. Lê o baseline e as listas finais explicitamente informadas, sem consultar Git nem promover versões antigas.',
                  codigo_sha256=sha(Path(__file__).read_bytes()))
    with a.saida.open('x') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps(dict(comparados=len(baseline), candidatos=len(candidates), colisoes=len(collisions))))
    return int(bool(collisions))


if __name__ == '__main__':
    raise SystemExit(main())
