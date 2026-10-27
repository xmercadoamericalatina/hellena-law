"""Replay somente leitura de fontes e corpos dos manifestos PE/RJ.

Usar markdown-it-py==4.0.0. O snapshot RJ conserva literalmente o auditor usado;
PE usa o helper contextual já entregue, inclusive para leis (sem a limitação
por pasta da antiga interface CLI). Não reconverte nem modifica os documentos.
"""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[1])]
from auditar_pe_commonmark_contexto import one as pe_one


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifesto', action='append', required=True)
    p.add_argument('--saida', required=True)
    args = p.parse_args()
    spec = importlib.util.spec_from_file_location('rj_snapshot', Path(__file__).resolve().parent / 'snapshots/auditar_rj_cache_20261021_001.py')
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    seen = set(); total = 0; falhas = 0
    with Path(args.saida).open('x') as out:
        for m in args.manifesto:
            for row in json.loads(Path(m).read_text())['documentos']:
                path = row['path']; assert path not in seen; seen.add(path)
                try:
                    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == row['sha256_md'], 'preimagem MD diverge'
                    cache = Path(row['cache']); z = cache.read_bytes()
                    assert hashlib.sha256(z).hexdigest() == row['sha256_cache'], 'cache comprimido diverge'
                    assert hashlib.sha256(gzip.decompress(z)).hexdigest() == row['sha256_fonte'], 'fonte descomprimida diverge'
                    if path.startswith('estaduais/PE/'):
                        r = pe_one(path)
                    elif path.startswith('estaduais/RJ/'):
                        r = mod.one(path); r['aceito'] = r['publicavel']
                    else:
                        raise ValueError('UF fora do escopo deste replay')
                    assert r['sha256_campo'] == row['sha256_campo'], 'limites/bytes do campo divergem'
                except Exception as e:
                    r = dict(path=path, aceito=False, erro=type(e).__name__+': '+str(e))
                total += 1; falhas += not r['aceito']
                out.write(json.dumps(r, ensure_ascii=False)+'\n'); out.flush()
                if total % 100 == 0:
                    print('PROGRESSO', total, 'falhas', falhas, flush=True)
    print('FINAL', total, 'falhas', falhas)
    if falhas:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
