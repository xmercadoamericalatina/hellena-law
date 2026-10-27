"""Copia snapshot rastreado, preserva identidade do destino e verifica objetos Git."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

PROTECTED = {'README.md', 'AGENTS.md', 'USO_E_CREDITOS.md', 'TRANSFERENCIA.md', 'TRANSFERENCIA.json', 'scripts/transferir_acervo.py'}


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)


def inventory(root):
    result = {}
    for record in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not record:
            continue
        header, name = record.split(b'\t', 1)
        mode, sha, stage = header.decode().split()
        if stage != '0':
            raise RuntimeError('Índice com conflito')
        result[os.fsdecode(name)] = (mode, sha)
    return result


def mapping(name):
    if name in PROTECTED or name.startswith('.github/'):
        return None
    return 'LICENSE-TERCEIROS' if name == 'LICENSE' else name


def transfer(src, dest, push=True):
    src, dest = src.resolve(), dest.resolve()
    if src == dest:
        raise ValueError('Origem e destino devem ser distintos')
    if push:
        git(dest, 'pull', '--rebase', 'origin', 'main')
    source_sha = git(src, 'rev-parse', 'HEAD').decode().strip()
    original, present = inventory(src), inventory(dest)
    expected = {}
    skipped = []
    for name, meta in original.items():
        target = mapping(name)
        if target is None:
            skipped.append(name)
            continue
        if meta[0] not in ('100644', '100755'):
            raise RuntimeError('Modo de arquivo exige revisão: ' + name)
        expected[target] = meta
    batch, size, batches = [], 0, 0

    def save():
        nonlocal batch, size, batches
        if not batch:
            return
        for offset in range(0, len(batch), 150):
            git(dest, 'add', '-f', '--', *batch[offset:offset + 150])
        rc = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=dest).returncode
        if rc not in (0, 1):
            raise RuntimeError('Falha ao conferir índice')
        if rc == 1:
            batches += 1
            git(dest, 'commit', '-m', 'Transfere acervo — lote ' + str(batches))
            if push:
                git(dest, 'pull', '--rebase', 'origin', 'main')
                git(dest, 'push', 'origin', 'HEAD:main')
            print('Lote salvo:', batches, 'arquivos:', len(batch), flush=True)
        batch, size = [], 0

    reused, copied = 0, 0
    for name, meta in original.items():
        target_name = mapping(name)
        if target_name is None:
            continue
        if present.get(target_name) == meta:
            reused += 1
            continue
        source, target = src / name, dest / target_name
        if source.is_symlink() or not source.is_file():
            raise RuntimeError('Arquivo irregular: ' + name)
        target.parent.mkdir(parents=True, exist_ok=True)
        # Mesmo runner: mover evita duplicar em disco o acervo de mais de um milhão de arquivos.
        length = source.stat().st_size
        shutil.move(str(source), str(target))
        batch.append(target_name)
        size += length
        copied += 1
        if size >= 150 * 1024 * 1024 or len(batch) >= 25000:
            save()
    save()
    actual = inventory(dest)
    mismatches = [name for name, meta in expected.items() if actual.get(name) != meta]
    if mismatches:
        raise RuntimeError('Arquivos divergentes ou ausentes: ' + repr(mismatches[:20]))
    required = ['lei-seca/estado.json', 'scripts/lei_seca/atualizar.py', 'LICENSE-TERCEIROS']
    for path in required:
        if path not in actual:
            raise RuntimeError('Arquivo obrigatório ausente: ' + path)
    workflow = dest / '.github/workflows/lei-seca.yml'
    if not workflow.exists():
        raise RuntimeError('Atualizador não instalado separadamente no destino')
    report = {'snapshot_origem': source_sha, 'arquivos_origem': len(original),
              'arquivos_transferiveis': len(expected), 'objetos_git_conferidos': len(expected),
              'copiados_nesta_execucao': copied, 'identicos_ja_presentes': reused,
              'divergencias': 0, 'excecoes_intencionais': skipped,
              'licenca_original': 'LICENSE-TERCEIROS',
              'workflow': 'instalado separadamente; não copiado pelo token da transferência',
              'validacao': 'modo e SHA de todos os arquivos transferíveis conferidos no índice Git',
              'observacao': 'Não certifica qualidade jurídica, vigência ou integralidade das normas; preserva o snapshot recebido.'}
    (dest / 'TRANSFERENCIA.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (dest / 'TRANSFERENCIA.md').write_text('# Transferência verificada\n\nSnapshot de origem: `' + source_sha + '`.\n\n' + str(len(expected)) + ' arquivos transferíveis conferidos por modo e SHA Git; zero divergências. Estado das coletas e licença original preservados. Exceções intencionais em [TRANSFERENCIA.json](TRANSFERENCIA.json). Atualizador instalado separadamente.\n\nA confirmação não certifica o conteúdo jurídico herdado nem significa que a primeira coleta no destino já tenha concluído.\n', encoding='utf-8')
    batch.extend(['TRANSFERENCIA.md', 'TRANSFERENCIA.json'])
    save()
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('origem', type=Path)
    p.add_argument('--destino', type=Path, default=Path.cwd())
    p.add_argument('--sem-push', action='store_true', help='Somente ensaio local')
    a = p.parse_args()
    transfer(a.origem, a.destino, not a.sem_push)
