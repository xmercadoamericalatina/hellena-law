"""Gera COBERTURA.md: quantas normas foram convertidas por esfera/tipo e o que ficou de fora (e por quê)."""
import collections
import json
import os
import re

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
UFS = "AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO".split()


def contar(base):
    por_tipo, ocr = collections.Counter(), 0
    for dirpath, dirs, arquivos in os.walk(base):
        dirs[:] = [d for d in dirs if not d.startswith("_")]
        for a in arquivos:
            if a.endswith(".md"):
                por_tipo[os.path.relpath(dirpath, base).split(os.sep)[0]] += 1
                with open(os.path.join(dirpath, a), encoding="utf-8") as f:
                    ocr += "Texto obtido por OCR" in f.read(4000)
    return por_tipo, ocr


def falhas(base):
    """Motivos das normas sem texto, considerando só a rodada mais recente de cada item."""
    c = collections.Counter()
    caminho = os.path.join(base, "_falhas.jsonl")
    if not os.path.exists(caminho):
        return c
    for linha in open(caminho, encoding="utf-8"):
        d = json.loads(linha)
        if d.get("status") in ("sem_texto", "erro", "indice"):
            motivo = d.get("motivo") or (f"HTTP {d['http']}" if d.get("http") else d.get("status"))
            c[re.sub(r"\s+", " ", str(motivo))[:70]] += 1
    return c


def main():
    linhas = ["# Cobertura", "", "Gerado por `scripts/relatorio.py`. Números de arquivos `.md` convertidos.", ""]
    # a Constituição Federal fica na raiz, fora de federal/ e de estaduais/
    total = 1 if os.path.exists(os.path.join(RAIZ, "constituicao.md")) else 0
    linhas += ["## Constituição Federal", "",
               "A `constituicao.md` na raiz: texto vigente, do Planalto.", ""]
    tipos, ocr = contar(os.path.join(RAIZ, "federal"))
    total += sum(tipos.values())
    linhas += ["## Federal", "", "| Tipo | Normas |", "| --- | ---: |"]
    linhas += [f"| {t} | {n:,} |".replace(",", ".") for t, n in sorted(tipos.items())]
    linhas += ["", "## Estados e Distrito Federal", "",
               "| UF | Normas | Constituição | Leis ord. | Leis compl. | Emendas | Outras | Via OCR | Sem texto (principais motivos) |",
               "| --- | ---: | :---: | ---: | ---: | ---: | ---: | ---: | --- |"]
    for uf in UFS:
        base = os.path.join(RAIZ, "estaduais", uf)
        if not os.path.isdir(base):
            linhas.append(f"| {uf} | 0 | | | | | | | não coletado |")
            continue
        tipos, ocr = contar(base)
        n = sum(tipos.values())
        total += n
        # as pastas são canônicas (ver scripts/normalizar.py), então os grupos são conjuntos exatos
        CONST = {"constituicao", "constituicoes-historicas", "lei-organica"}
        ORD = {"leis-ordinarias", "leis-promulgadas"}
        COMPL = {"leis-complementares"}
        EMENDAS = {"emendas-constitucionais", "emendas-lei-organica"}
        n_const = sum(v for k, v in tipos.items() if k in CONST)
        const = "sim" if n_const else "não"
        lo = sum(v for k, v in tipos.items() if k in ORD)
        lc = sum(v for k, v in tipos.items() if k in COMPL)
        ec = sum(v for k, v in tipos.items() if k in EMENDAS)
        outras = n - lo - lc - ec - n_const
        motivos = "; ".join(f"{m}: {q}" for m, q in falhas(base).most_common(3))
        linhas.append(f"| {uf} | {n} | {const} | {lo} | {lc} | {ec} | {outras} | {ocr} | {motivos} |")
    linhas += ["", f"**Total: {total:,} normas em Markdown.**".replace(",", "."), ""]
    with open(os.path.join(RAIZ, "COBERTURA.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print("\n".join(linhas))


if __name__ == "__main__":
    main()
