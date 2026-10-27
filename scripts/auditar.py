"""Audita formato e proveniência dos Markdown; --staged lê exatamente o lote do Git.

    python3 -I scripts/auditar.py estaduais/MS
    python3 -I scripts/auditar.py --staged

Não certifica a completude jurídica nem a fidelidade da conversão à fonte.
"""
import argparse
import collections
import contextlib
import datetime as dt
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

RAIZ = Path(__file__).resolve().parent.parent
BASES = ("federal", "estaduais", "reguladores", "jurisprudencia", "tratados", "municipais")
CAMPOS = {"titulo", "tipo", "numero", "data", "versao_texto", "fonte", "baixado_em"}


def validar(texto, caminho, hoje):
    erros, avisos = [], []
    if not texto.startswith("---\n") or "\n---\n" not in texto[4:]:
        return ["cabeçalho ausente ou incompleto"], avisos
    cab, corpo = texto[4:].split("\n---\n", 1)
    campos = {}
    for linha in cab.splitlines():
        m = re.fullmatch(r"([\w]+):[ \t]*(.*)", linha)
        if not m:
            erros.append("linha de cabeçalho inválida")
            continue
        chave, valor = m.groups()
        if chave in campos:
            erros.append(f"campo duplicado: {chave}")
        try:
            campos[chave] = json.loads(valor) if valor.startswith('"') else valor
        except json.JSONDecodeError:
            erros.append(f"string inválida: {chave}")
    erros += [f"campo ausente: {c}" for c in sorted(CAMPOS - campos.keys())]
    for chave in ("titulo", "tipo", "versao_texto", "fonte", "baixado_em"):
        if chave in campos and not campos[chave]:
            erros.append(f"campo vazio: {chave}")
    for chave in ("data", "data_publicacao", "baixado_em"):
        if chave not in campos:
            continue
        valor = campos[chave]
        if not valor:
            avisos.append(f"{chave} não informada")
            continue
        try:
            data = dt.date.fromisoformat(valor)
            if data > hoje:
                erros.append(f"{chave} futura: {valor}")
        except (TypeError, ValueError):
            erros.append(f"{chave} inválida: {valor}")
    fonte = urlparse(str(campos.get("fonte", "")))
    if fonte.scheme not in ("http", "https") or not fonte.hostname:
        erros.append("fonte não é URL HTTP(S)")
    if caminho.startswith("estaduais/") and campos.get("uf") != caminho.split("/")[1]:
        erros.append("UF do cabeçalho difere da pasta")
    linhas = corpo.lstrip().splitlines()
    if not linhas or not linhas[0].startswith("# "):
        erros.append("título H1 ausente")
    elif not "\n".join(linhas[1:]).strip():
        erros.append("corpo vazio")
    if "\x00" in texto:
        erros.append("caractere NUL")
    return erros, avisos


def documentos(alvos, staged):
    if staged:
        nomes = subprocess.check_output(["git", "diff", "--cached",
                                         "--diff-filter=ACMR", "--name-only", "-z"], cwd=RAIZ)
        processo = subprocess.Popen(["git", "cat-file", "--batch"], cwd=RAIZ,
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            for nome in nomes.decode().split("\0"):
                if (not nome.endswith(".md") or nome.split("/")[0] not in BASES
                        or any(p.startswith(("_", ".")) for p in Path(nome).parts)):
                    continue
                processo.stdin.write((":" + nome + "\n").encode())
                processo.stdin.flush()
                cab = processo.stdout.readline().split()
                if len(cab) != 3 or cab[1] != b"blob":
                    raise RuntimeError(f"objeto Git indisponível: {nome}")
                bruto = processo.stdout.read(int(cab[2]))
                if processo.stdout.read(1) != b"\n":
                    raise RuntimeError("resposta cat-file incompleta")
                yield nome, bruto.decode("utf-8")
        finally:
            processo.stdin.close()
            processo.stdout.close()
            if processo.wait() != 0:
                raise RuntimeError("git cat-file falhou")
    else:
        import os
        for alvo in alvos or BASES:
            for raiz, dirs, arquivos in os.walk(RAIZ / alvo):
                dirs[:] = [d for d in dirs if not d.startswith(("_", "."))]
                for nome in arquivos:
                    if nome.endswith(".md"):
                        path = Path(raiz) / nome
                        yield str(path.relative_to(RAIZ)), path.read_text(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("alvos", nargs="*")
    ap.add_argument("--staged", action="store_true")
    ap.add_argument("--falhas", help="grava todos os caminhos com erro em JSONL")
    a = ap.parse_args()
    if a.staged and a.alvos:
        ap.error("use --staged ou caminhos, sem combinar os dois")
    hoje = dt.datetime.now(ZoneInfo("America/Recife")).date()
    cont, avisos, motivos, exemplos = collections.Counter(), collections.Counter(), collections.Counter(), []
    destino = open(a.falhas, "w", encoding="utf-8") if a.falhas else contextlib.nullcontext()
    with destino as registro:
        for nome, texto in documentos(a.alvos, a.staged):
            erros, alertas = validar(texto, nome, hoje)
            cont["arquivos"] += 1
            cont["com_erros"] += bool(erros)
            avisos.update(alertas)
            motivos.update(erros)
            if erros:
                caso = {"arquivo": nome, "erros": erros}
                if len(exemplos) < 25:
                    exemplos.append(caso)
                if registro:
                    registro.write(json.dumps(caso, ensure_ascii=False) + "\n")
                    registro.flush()
    print(json.dumps({"origem": "index Git" if a.staged else "disco", "contagens": cont,
                      "avisos": avisos, "erros": motivos, "exemplos": exemplos}, ensure_ascii=False))
    return 1 if cont["com_erros"] or not cont["arquivos"] else 0


if __name__ == "__main__":
    sys.exit(main())
