"""Prepara uma lista explícita de dados no index, preservando arquivos e refs.

Milhares de blobs são escritos num pack via fast-import, sem comandos de commit,
branch ou reset. update-index recebe somente os caminhos conferidos. O commit
normal e o hook de progresso continuam obrigatórios e ficam com o coordenador.
Por padrão apenas valida; --aplicar grava objetos/index. Filtros de checkout ou
arquivos executáveis/simbólicos exigem git add convencional, nunca são ignorados.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

RAIZ = Path(__file__).resolve().parent.parent


def preparar(raiz, caminhos, aplicar=False, hashes=None):
    caminhos = list(dict.fromkeys(caminhos))
    if not caminhos:
        raise ValueError("lista vazia")
    for nome in caminhos:
        p = Path(nome)
        if p.is_absolute() or '..' in p.parts or p.parts[0] == '.git' or p.suffix not in {'.md', '.json', '.txt'}:
            raise ValueError("caminho fora do recorte de dados: " + nome)
        path = raiz / p
        if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o111:
            raise ValueError("arquivo ausente, executável ou simbólico: " + nome)
        if not path.resolve().is_relative_to(raiz.resolve()):
            raise ValueError("caminho sai do repositório: " + nome)
    nomes_z = b'\0'.join(p.encode() for p in caminhos) + b'\0'
    attrs = subprocess.check_output(['git', 'check-attr', '-z', '--stdin', 'filter', 'text', 'eol', 'working-tree-encoding'], cwd=raiz, input=nomes_z)
    campos = attrs.decode().split('\0')
    for i in range(0, len(campos)-1, 3):
        if campos[i+2] != 'unspecified':
            raise ValueError("atributo exige git add convencional: " + ', '.join(campos[i:i+3]))
    formato = subprocess.check_output(['git', 'rev-parse', '--show-object-format'], cwd=raiz).decode().strip()
    if formato not in {'sha1', 'sha256'}:
        raise ValueError("formato de objetos desconhecido")
    processo = subprocess.Popen(['git', 'fast-import', '--quiet', '--done'], cwd=raiz, stdin=subprocess.PIPE) if aplicar else None
    entradas = []
    total = 0
    try:
        for nome in caminhos:
            raw = (raiz / nome).read_bytes()
            # Dados do acervo são UTF-8/LF; não ignorar conversões de linha.
            raw.decode('utf-8')
            if b'\r' in raw:
                raise ValueError("quebras de linha exigem git add convencional: " + nome)
            if hashes is not None:
                if nome not in hashes:
                    raise ValueError("hash auditado ausente: " + nome)
                if hashlib.sha256(raw).hexdigest() != hashes[nome]:
                    raise ValueError("hash difere do lote auditado: " + nome)
            oid = hashlib.new(formato, b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
            entradas.append(('100644 ' + oid + '\t' + nome + '\0').encode())
            total += len(raw)
            if processo:
                processo.stdin.write(b'blob\ndata ' + str(len(raw)).encode() + b'\n')
                processo.stdin.write(raw)
                processo.stdin.write(b'\n')
        if processo:
            processo.stdin.write(b'done\n')
            processo.stdin.close()
            if processo.wait() != 0:
                raise RuntimeError('fast-import não concluiu os blobs; index não alterado')
            subprocess.run(['git', 'update-index', '-z', '--index-info'], cwd=raiz, input=b''.join(entradas), check=True)
    except BaseException:
        if processo:
            if processo.poll() is None:
                processo.terminate()
            if not processo.stdin.closed:
                try:
                    processo.stdin.close()
                except BrokenPipeError:
                    pass
            processo.wait()
        raise
    return {'arquivos': len(caminhos), 'bytes': total, 'aplicado': aplicar,
            'refs': 'preservadas; nenhum commit ou reset executado', 'worktree': 'preservado'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lista', required=True)
    ap.add_argument('--hashes', help='JSON caminho → SHA-256 auditado')
    ap.add_argument('--aplicar', action='store_true')
    args = ap.parse_args()
    hashes = json.loads(Path(args.hashes).read_text()) if args.hashes else None
    print(json.dumps(preparar(RAIZ, Path(args.lista).read_text().splitlines(), args.aplicar, hashes), ensure_ascii=False))


if __name__ == '__main__':
    main()
