"""Revisa apenas metadados legados DOU; nunca altera o corpo normativo.

Exige reconversão idêntica, assinatura e metadados reproduzíveis na fonte.
Snapshots e backups ficam preservados. Por padrão apenas simula a revisão.
"""
import argparse
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import re
import signal
import sys
import tempfile
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_cache_dou import RAIZ, conferir, meta_corpo


def proposta(raw, sha):
    texto = raw.decode('utf-8')
    meta, corpo = meta_corpo(texto)
    if meta.get('revogada') not in (False, None):
        raise ValueError('evidência de revogação existente exige revisão própria')
    cab, original = texto[4:].split('\n---\n', 1)
    cab, n = re.subn(r'^revogada:.*$', 'revogada: null', cab, flags=re.M)
    if n != 1:
        raise ValueError('campo revogada ausente/duplicado')
    if 'sha256_html_fonte' not in meta:
        cab += '\nsha256_html_fonte: ' + sha
    elif meta['sha256_html_fonte'] != sha:
        raise ValueError('SHA já registrado diverge do cache legado')
    novo = ('---\n' + cab + '\n---\n' + original).encode()
    assert meta_corpo(novo.decode())[1] == corpo
    return novo


def revisar(path, backup_raiz, hoje, aplicar=False):
    nome = path.relative_to(RAIZ)
    atual = path.read_bytes()
    backup = backup_raiz / nome
    retomado = backup.exists()
    raw = gzip.decompress(backup.read_bytes()) if retomado else atual
    pasta = RAIZ / 'reguladores/_fonte' / nome.parts[1] / nome.parts[3]
    antigo = pasta / (path.stem + '.html.gz')
    fonte = gzip.decompress(antigo.read_bytes())
    sha = hashlib.sha256(fonte).hexdigest()
    snapshot = pasta / (path.stem + '-' + sha + '.html.gz')
    criado = not snapshot.exists()
    if not criado and gzip.decompress(snapshot.read_bytes()) != fonte:
        raise ValueError('snapshot preexistente diverge do SHA')
    novo = proposta(raw, sha)
    if atual not in (raw, novo):
        raise ValueError('arquivo diverge tanto do backup como da proposta; preservado')
    registro, _ = conferir(path, set(), set(), hoje, bruto_md=novo, fonte_bytes=fonte)
    if novo == raw:
        raise ValueError('nenhuma correção necessária')
    if aplicar:
        if criado:
            snapshot.write_bytes(gzip.compress(fonte, mtime=0))
        backup.parent.mkdir(parents=True, exist_ok=True)
        if backup.exists() and gzip.decompress(backup.read_bytes()) != raw:
            raise ValueError('backup preexistente diferente; arquivo preservado')
        if not backup.exists():
            backup.write_bytes(gzip.compress(raw, mtime=0))
        if path.read_bytes() != atual:
            raise ValueError('arquivo alterado durante a revisão')
        if atual != novo:
            with tempfile.NamedTemporaryFile(dir=path.parent, suffix='.tmp', delete=False) as f:
                tmp = Path(f.name)
                f.write(novo)
            tmp.replace(path)
    return {**registro, 'sha256_anterior': hashlib.sha256(raw).hexdigest(),
            'backup': str(backup.relative_to(RAIZ)), 'corpo_normativo_inalterado': True,
            'aplicado': aplicar, 'snapshot_criado': criado, 'retomado_backup': retomado}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--manifesto-origem', required=True)
    ap.add_argument('--manifesto', required=True)
    ap.add_argument('--backup', required=True)
    ap.add_argument('--aplicar', action='store_true')
    ap.add_argument('--tempo-por-arquivo', type=int, default=30)
    args = ap.parse_args()
    origem = Path(args.manifesto_origem).read_bytes()
    candidatos = [x['path'] for x in json.loads(origem)['retidos']
                  if x['motivo'].startswith(('vigência sem evidência', 'snapshot imutável sem SHA'))]
    hoje = dt.datetime.now(ZoneInfo('America/Recife')).date()
    ok, retidos = [], []
    if args.tempo_por_arquivo <= 0:
        ap.error('tempo por arquivo deve ser positivo')
    def limite(signum, frame):
        raise TimeoutError('revisão excedeu prazo por arquivo; original preservado')
    signal.signal(signal.SIGALRM, limite)
    for i, nome in enumerate(dict.fromkeys(candidatos)):
        try:
            signal.alarm(args.tempo_por_arquivo)
            ok.append(revisar(RAIZ / nome, RAIZ / args.backup, hoje, args.aplicar))
        except (ValueError, OSError, KeyError, EOFError) as exc:
            retidos.append({'path': nome, 'motivo': str(exc)})
        finally:
            signal.alarm(0)
        if (i + 1) % 500 == 0:
            print(i + 1, len(ok), 'aprovados', len(retidos), 'retidos', flush=True)
    Path(args.manifesto).write_text(json.dumps({'sha256_manifesto_origem': hashlib.sha256(origem).hexdigest(),
        'aplicado': args.aplicar, 'criterio': 'somente metadados; corpo byte a byte e demais gates DOU',
        'documentos': ok, 'retidos': retidos}, ensure_ascii=False, indent=2) + '\n')
    print('FIM', len(ok), 'aprovados', len(retidos), 'retidos', flush=True)


if __name__ == '__main__':
    main()
