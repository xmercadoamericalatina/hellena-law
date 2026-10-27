"""Sobrepõe retenções de granularidade a entregas anteriores sem modificá-las."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_municipal import metadados
from granularidade_sapl import alertas_multiplos_atos

RAIZ = Path(__file__).resolve().parent.parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def registros(path):
    d = json.loads(path.read_text())
    if 'aprovados' in d:
        for r in d['aprovados']:
            yield r, path
    else:
        for lote in d['lotes']:
            yield from registros(RAIZ / lote['manifesto'])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--entrega', type=Path, action='append', required=True)
    ap.add_argument('--saida', type=Path, required=True)
    a = ap.parse_args()
    a.saida.mkdir(parents=True, exist_ok=True)
    aprovados, retidos = [], []
    vistos = set()
    for entrega in a.entrega:
        for r, origem in registros(entrega):
            if r['path'] in vistos:
                continue
            vistos.add(r['path'])
            p = RAIZ / r['path']
            if not p.exists():
                retidos.append({'path': r['path'], 'erro': 'arquivo não existe no estado atual', 'manifesto_origem': str(origem)})
                continue
            b = p.read_bytes()
            m = metadados(b.decode())
            row = {'path': r['path'], 'sha256': sha(b), 'manifesto_origem': str(origem.relative_to(RAIZ)) if origem.is_absolute() else str(origem),
                   'sha256_manifesto_origem': sha(origem.read_bytes()), 'fonte': m.get('fonte'),
                   'fonte_texto': m.get('fonte_texto'), 'sha256_fonte': m.get('sha256_fonte')}
            if sha(b) != r['sha256']:
                row['erro'] = 'arquivo mudou desde entrega original; revisar novamente'
                retidos.append(row)
                continue
            corpo = b.decode().split('\n---\n', 1)[1].lstrip('\n').split('\n\n', 1)[1]
            alertas = alertas_multiplos_atos(corpo, m.get('tipo_na_fonte', m['tipo']), m['numero'])
            row['alertas_granularidade'] = alertas
            if alertas:
                retidos.append(row)
            else:
                row['checks'] = {'hash_entrega_original': True, 'sem_epigrafes_de_outras_identidades_detectadas': True}
                aprovados.append(row)
    geral = {'auditado_em': dt.datetime.now().isoformat(), 'entregas_substituidas_por_este_overlay': [str(x) for x in a.entrega],
             'criterio': 'Original intacto e hash conferido; retenção conservadora quando há epígrafe de outra identidade no corpo; não recorta automaticamente nem certifica ausência de toda ambiguidade OCR.',
             'aprovados': aprovados, 'retidos': retidos}
    with (a.saida / 'overlay.json').open('x') as f:
        json.dump(geral, f, ensure_ascii=False, indent=2)
    for numero, inicio in enumerate(range(0, len(aprovados), 1000), 1):
        rows = aprovados[inicio:inicio + 1000]
        lista = a.saida / f'lote-{numero:04d}.paths.txt'
        with lista.open('x') as f:
            f.write(''.join(r['path'] + '\n' for r in rows))
    with (a.saida / 'retidos.paths.txt').open('x') as f:
        f.write(''.join(r['path'] + '\n' for r in retidos))
    print(json.dumps({'aprovados': len(aprovados), 'retidos': len(retidos), 'overlay': str(a.saida / 'overlay.json')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
