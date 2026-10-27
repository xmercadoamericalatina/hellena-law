"""Audita identidade IBGE, rotas e duplicatas municipais sem consultar Git ou rede.

--lista aceita caminhos relativos separados por linha ou NUL; --raiz permite auditar
uma cópia exportada do snapshot. O cadastro IBGE é informado separadamente.
"""
import argparse
import collections
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import sys
import subprocess
sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import normalizar_chave, slugify

REPO = Path(__file__).resolve().parent.parent


def chave(nome):
    return normalizar_chave(nome.replace("'", "").replace("’", ""))


def metadados(texto):
    cab = texto.split("\n---", 1)[0]
    meta = {}
    for linha in cab.splitlines():
        m = re.match(r"^([a-z_][a-z0-9_]*):\s*(.*)$", linha)
        if m:
            try:
                meta[m[1]] = json.loads(m[2])
            except ValueError:
                meta[m[1]] = m[2].strip()
    return meta


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--staged", action="store_true", help="lê somente blobs municipais do índice, via git cat-file")
    ap.add_argument("--raiz", type=Path, default=REPO)
    ap.add_argument("--lista", type=Path)
    ap.add_argument("--ibge", type=Path, default=REPO / "municipais/_indice/ibge-municipios.json")
    ap.add_argument("--saida", type=Path, required=True)
    a = ap.parse_args()
    bruto = a.ibge.read_bytes()
    municipios = {}
    for x in json.loads(bruto):
        uf = x["regiao-imediata"]["regiao-intermediaria"]["UF"]["sigla"]
        municipios[(uf, chave(x["nome"]))] = x
    escopo = {"alterados_index": 0, "demais_index": 0}
    def documentos_auditar():
        if a.staged:
            if a.lista:
                ap.error("use --staged ou --lista")
            from auditar import documentos
            alterados = set()
            for nome, texto in documentos([], True):
                if nome.startswith("municipais/"):
                    alterados.add(nome)
                    escopo["alterados_index"] += 1
                    yield a.raiz / nome, texto
            # O índice completo inclui documentos anteriores inalterados, adições e
            # modificações, mas exclui remoções: detecta duplicatas entre lotes.
            dados = subprocess.check_output(["git", "ls-files", "--cached", "-z", "--", "municipais"], cwd=a.raiz)
            processo = subprocess.Popen(["git", "cat-file", "--batch"], cwd=a.raiz,
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            try:
                for nome in sorted(set(dados.decode().split("\0")) - alterados):
                    if not nome.endswith(".md") or any(c.startswith("_") for c in Path(nome).parts):
                        continue
                    processo.stdin.write((":" + nome + "\n").encode())
                    processo.stdin.flush()
                    cab = processo.stdout.readline().split()
                    if len(cab) != 3 or cab[1] != b"blob":
                        raise RuntimeError("blob indisponível no índice: " + nome)
                    bruto = processo.stdout.read(int(cab[2]))
                    if len(bruto) != int(cab[2]) or processo.stdout.read(1) != b"\n":
                        raise RuntimeError("git cat-file retornou blob incompleto")
                    escopo["demais_index"] += 1
                    yield a.raiz / nome, bruto.decode("utf-8")
            finally:
                processo.stdin.close()
                processo.stdout.close()
                if processo.wait() != 0:
                    raise RuntimeError("git cat-file terminou com erro")
        else:
            if a.lista:
                nomes = a.lista.read_text().replace("\0", "\n").splitlines()
                arquivos = [a.raiz / n for n in nomes if n.startswith("municipais/") and n.endswith(".md")
                            and not any(c.startswith("_") for c in Path(n).parts)]
            else:
                arquivos = sorted(p for p in (a.raiz / "municipais").glob("*/*/**/*.md")
                                  if not any(c.startswith("_") for c in p.relative_to(a.raiz).parts))
            for path in arquivos:
                yield path, None
    erros, avisos = [], []
    identidades = collections.defaultdict(list)
    codigos = collections.defaultdict(list)
    corpos = collections.defaultdict(list)
    sapl = 0
    total = 0
    for p, texto in documentos_auditar():
        total += 1
        rel = str(p.relative_to(a.raiz))
        def erro(motivo):
            erros.append({"arquivo": rel, "erro": motivo})
        if texto is None:
            if not p.is_file():
                erro("arquivo da lista não existe no snapshot")
                continue
            texto = p.read_text()
        meta = metadados(texto)
        partes = Path(rel).parts
        if len(partes) < 4:
            erro("caminho municipal incompleto")
            continue
        uf = partes[1]
        item = municipios.get((uf, chave(str(meta.get("municipio", "")))))
        if not item:
            erro("município/UF não corresponde ao cadastro IBGE")
            continue
        if meta.get("uf") != uf:
            erro("UF do metadado diverge do caminho")
        esperado = slugify(normalizar_chave(item["nome"]))[:60]
        if partes[2] != esperado:
            erro("rota divergente; esperado " + esperado)
        if meta.get("codigo_ibge") and str(item["id"]) != str(meta["codigo_ibge"]):
            erro("código IBGE divergente")
        for campo in ("data", "data_publicacao"):
            v = meta.get(campo)
            if v:
                try:
                    if dt.date.fromisoformat(str(v)) > dt.date.today():
                        erro(campo + " posterior à data atual")
                except ValueError:
                    erro(campo + " não é data ISO válida")
        fonte = str(meta.get("fonte", ""))
        codigo = meta.get("codigo_identificador")
        if codigo:
            identidades[("diario", fonte, codigo)].append(rel)
            codigos[codigo].append(rel)
        elif "/norma/" in fonte:
            sapl += 1
            identidades[("sapl", fonte)].append(rel)
            digest = meta.get("sha256_texto")
            if digest:
                try:
                    resto = texto.split("\n---\n", 1)[1].lstrip("\n")
                    corpo = resto.split("\n\n", 1)[1]
                    if corpo.endswith("\n"):
                        corpo = corpo[:-1]
                    if hashlib.sha256(corpo.encode()).hexdigest() != digest:
                        erro("hash do corpo diverge do metadado SAPL")
                except IndexError:
                    erro("corpo SAPL sem estrutura reconhecível")
                corpos[(item["id"], digest)].append(rel)
    for identidade, caminhos in identidades.items():
        if len(caminhos) > 1:
            erros.append({"erro": "identidade oficial repetida", "identidade": identidade, "arquivos": caminhos})
    for identidade, caminhos in corpos.items():
        if len(caminhos) > 1:
            erros.append({"erro": "corpo SAPL repetido no município", "identidade": identidade, "arquivos": caminhos})
    for codigo, caminhos in codigos.items():
        if len(caminhos) > 1:
            avisos.append({"aviso": "código reutilizado; comparar edição/fonte e corpo antes de deduplicar",
                           "codigo": codigo, "arquivos": caminhos})
    resultado = {"origem": "índice Git" if a.staged else "disco", "escopo_index": escopo, "raiz": str(a.raiz), "lista": str(a.lista) if a.lista else None,
                 "ibge": str(a.ibge), "ibge_sha256": hashlib.sha256(bruto).hexdigest(),
                 "fonte_ibge": "https://servicodados.ibge.gov.br/api/v1/localidades/municipios?orderBy=nome",
                 "regra_alias": "acentos e apóstrofos normalizados para identificar nomes; rota exige nome oficial IBGE",
                 "arquivos": total, "sapl": sapl, "problemas": len(erros), "detalhes": erros, "avisos": avisos}
    a.saida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2))
    print(json.dumps({"arquivos": total, "sapl": sapl, "problemas": len(erros),
                      "avisos": len(avisos), "saida": str(a.saida)}, ensure_ascii=False))
    return int(bool(erros))

if __name__ == "__main__":
    raise SystemExit(main())
