"""Congela o próximo lote de candidatos TA, sem repetir identidades já examinadas.

Versão 2: exporta diários/anexos apenas de portais selecionados, evitando exigir
metadados de tipos de portais sem candidatos neste lote.

O limite é somente o tamanho do lote de trabalho. A coleta de portais continua;
reexecuções com as exclusões anteriores cobrem os candidatos seguintes.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import shutil


def sha(b):
    return hashlib.sha256(b).hexdigest()


def identidade(row):
    return row['host'], row['ta_id']


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--captura', type=Path, required=True)
    ap.add_argument('--excluir', type=Path, action='append', default=[])
    ap.add_argument('--saida', type=Path, required=True)
    ap.add_argument('--tamanho-lote', type=int, default=500)
    a = ap.parse_args()
    excluded = set()
    for path in a.excluir:
        excluded.update(identidade(r) for r in map(json.loads, path.read_text().splitlines()))
    hosts = {}
    sources = []
    for journal in sorted(a.captura.glob('*/resultados.jsonl')):
        raw = journal.read_bytes()
        complete = raw[:raw.rfind(b'\n') + 1]
        latest = {r['ta_id']: r for r in map(json.loads, complete.decode().splitlines())}
        hosts[journal.parent.name] = [r for r in latest.values() if r['estado'] == 'candidato_estruturado_para_auditoria' and identidade(r) not in excluded]
        sources.append({'path': str(journal), 'sha256_prefixo': sha(complete), 'bytes_prefixo': len(complete)})
    selected = []
    for group in itertools.zip_longest(*(hosts[h] for h in sorted(hosts))):
        for row in group:
            if row:
                selected.append(row)
            if len(selected) == a.tamanho_lote:
                break
        if len(selected) == a.tamanho_lote:
            break
    a.saida.mkdir(exist_ok=False)
    for host in hosts:
        if not any(r['host'] == host for r in selected):
            continue
        folder = a.saida / host
        folder.mkdir()
        (folder / 'resultados.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in selected if r['host'] == host))
        shutil.copyfile(a.captura / host / 'anexos-index.json', folder / 'anexos-index.json')
    result = {'criterio': __doc__, 'selecionados': len(selected), 'disponiveis_apos_exclusoes': sum(map(len, hosts.values())), 'exclusoes': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p in a.excluir], 'prefixos_origem': sources, 'script_sha256': sha(Path(__file__).read_bytes()), 'identidades': [{'host': r['host'], 'ta_id': r['ta_id'], 'norma_id': r['norma_id']} for r in selected]}
    (a.saida / 'snapshot.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps({'selecionados': len(selected), 'disponiveis': result['disponiveis_apos_exclusoes']}))


if __name__ == '__main__':
    main()
