"""Replay privado de candidatos PE: fonte, preimagens, corpo e destinos.

Não promove arquivos, não toca canônicos e não usa a rede. Requer o mesmo
runtime markdown-it-py==4.0.0 do auditor. A versão atual do gate pode reter
candidatos de um snapshot anterior sem reescrever o manifesto anterior.
"""
import argparse
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
from zoneinfo import ZoneInfo

from auditar_pe_recuperacao_utf8 import candidato


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifesto', action='append', required=True)
    p.add_argument('--saida', required=True)
    args = p.parse_args(); rows = []; seen = set(); destinos = set()
    for m in args.manifesto:
        for r in json.loads(Path(m).read_text())['candidatos']:
            path = r['path']; dest = r.get('destino_canonico', path)
            assert path not in seen and dest not in destinos
            seen.add(path); destinos.add(dest)
            result = dict(path=path, destino_canonico=dest, manifesto=m, aceito=False)
            try:
                raw = Path(path).read_bytes(); assert sha(raw) == r['sha256_HEAD'], 'MD real/preimagem HEAD diverge'
                backupz = Path(r['backup']).read_bytes(); assert sha(backupz) == r['sha256_backup']
                assert gzip.decompress(backupz) == raw
                priorbody = gzip.decompress(Path(r['body_preimagem']).read_bytes())
                assert sha(priorbody) == r['sha256_body_preimagem']
                assert priorbody == raw.decode().split('\n---\n', 1)[1].encode()
                z = Path(r['cache']).read_bytes(); assert sha(z) == r['sha256_cache']
                source = gzip.decompress(z); assert sha(source) == r['sha256_fonte']
                new, proof = candidato(raw, source)
                candidatez = Path(r['candidato_privado']).read_bytes()
                assert sha(candidatez) == r['sha256_candidato_gz']
                assert gzip.decompress(candidatez) == new and sha(new) == r['sha256_candidato']
                if dest != path:
                    assert '/sem-ano/' in path and '/'+proof['data'][:4]+'/' in dest
                    assert not Path(dest).exists(), 'destino canônico já existe'
                result.update(aceito=True, sha256_candidato=sha(new), sha256_HEAD=sha(raw),
                              sha256_fonte=sha(source), QA=proof)
            except Exception as e:
                result['motivo'] = type(e).__name__+': '+str(e)
            rows.append(result)
            if len(rows) % 100 == 0:
                print('PROGRESSO', len(rows), 'falhas', sum(not r['aceito'] for r in rows), flush=True)
    obj = dict(auditado_em=dt.datetime.now(ZoneInfo('America/Recife')).isoformat(), total=len(rows),
               total_aceito=sum(r['aceito'] for r in rows), total_retido=sum(not r['aceito'] for r in rows),
               codigo_gate='scripts/estados/auditar_pe_recuperacao_utf8.py',
               sha256_codigo_gate=sha(Path('scripts/estados/auditar_pe_recuperacao_utf8.py').read_bytes()),
               manifestos={m: sha(Path(m).read_bytes()) for m in args.manifesto}, documentos=rows)
    with Path(args.saida).open('x') as out:
        out.write(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')
    print('FINAL', obj['total'], obj['total_aceito'], obj['total_retido'], flush=True)


if __name__ == '__main__':
    main()
