"""Mede o acervo contra o plano e gera `progresso.svg` e `PROGRESSO.md`.

Conta os arquivos `.md` de cada item de `scripts/plano.py`, agrega por setor e por fase e desenha
uma barra para cada um. O SVG é escrito à mão, sem dependência: entra direto no README e funciona
no tema claro e no escuro porque o fundo é explícito.

    python3 -I scripts/progresso.py            # grava progresso.svg e PROGRESSO.md
    python3 -I scripts/progresso.py --conferir  # só imprime; não grava nada

Também audita o caminho inverso: pastas com `.md` no repositório que nenhum item do plano cobre.
Uma pasta órfã é sempre um dos dois: nome fora do padrão, ou tipo de norma que esquecemos de
planejar. As duas coisas precisam de correção humana, por isso aparecem no fim do relatório.
"""
import argparse
import collections
import datetime as dt
import fnmatch
import glob
import os
import sys
import subprocess
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plano import FASES, PLANO, por_setor  # noqa: E402
from pendencias_integralidade import carregar as carregar_pendencias

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def contar_md(caminho, pendentes=()):
    """Arquivos .md sob um caminho, ignorando as pastas de trabalho (`_fonte`, `_indice`)."""
    if caminho.endswith(".md"):
        return int(os.path.isfile(caminho) and os.path.relpath(caminho, RAIZ) not in pendentes)
    if not os.path.isdir(caminho):
        return 0
    n = 0
    for dirpath, dirs, arquivos in os.walk(caminho):
        dirs[:] = [d for d in dirs if not d.startswith("_")]
        n += sum(1 for a in arquivos if a.endswith(".md")
                 and os.path.relpath(os.path.join(dirpath, a), RAIZ) not in pendentes)
    return n


def expandir(caminho_do_item):
    """Resolve os caminhos de um item: vários separados por vírgula, cada um com `*` opcional."""
    for parte in caminho_do_item.split(","):
        parte = parte.strip()
        alvos = glob.glob(os.path.join(RAIZ, parte))
        # um caminho sem `*` que não existe ainda tem de ser reportado (conta zero), e não sumir
        yield from (alvos or ([os.path.join(RAIZ, parte)] if "*" not in parte else []))


def medir(pendentes=()):
    """[(item, atual)] na ordem do plano, mais o conjunto de pastas já cobertas."""
    medidas, cobertas = [], set()
    for item in PLANO:
        n = 0
        for alvo in expandir(item.caminho):
            n += contar_md(alvo, pendentes)
            cobertas.add(os.path.relpath(alvo, RAIZ))
        medidas.append((item, n))
    return medidas, cobertas


def medir_git(pendentes=()):
    """Conta o index que será publicado, sem incluir downloads ainda não adicionados."""
    saida = subprocess.check_output(["git", "ls-files", "--cached", "-z"], cwd=RAIZ)
    arquivos = {p for p in saida.decode().split("\0") if p.endswith(".md")
                and not any(c.startswith(("_", ".")) for c in p.split("/"))}
    arquivos.difference_update(pendentes)
    contagem = collections.Counter()
    for path in arquivos:
        partes = path.split("/")
        contagem[path] += 1
        for n in range(1, len(partes)):
            contagem["/".join(partes[:n])] += 1
    por_profundidade = collections.defaultdict(list)
    for path in contagem:
        por_profundidade[path.count("/")].append(path)
    medidas, cobertas = [], set()
    for item in PLANO:
        alvos = set()
        for padrao in item.caminho.split(","):
            padrao = padrao.strip()
            if "*" in padrao:
                alvos.update(p for p in por_profundidade[padrao.count("/")]
                             if fnmatch.fnmatchcase(p, padrao))
            elif padrao in contagem:
                alvos.add(padrao)
        medidas.append((item, sum(contagem[p] for p in alvos)))
        cobertas.update(alvos)
    achadas = collections.Counter()
    for path in arquivos:
        partes = path.split("/")
        if len(partes) == 1:
            continue
        if not any("/".join(partes[:n]) in cobertas for n in range(1, len(partes))):
            achadas["/".join(partes[:-1][:3])] += 1
    return medidas, achadas


def orfas(cobertas):
    """Pastas com .md que o plano não menciona — nome fora do padrão ou tipo não planejado."""
    achadas = collections.Counter()
    for dirpath, dirs, arquivos in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if not d.startswith(("_", "."))]
        if not any(a.endswith(".md") for a in arquivos):
            continue
        rel = os.path.relpath(dirpath, RAIZ)
        if rel == ".":
            continue
        # uma pasta está coberta se ela, ou qualquer ancestral dela, é alvo de um item
        partes = rel.split(os.sep)
        if any(os.sep.join(partes[:i]) in cobertas for i in range(1, len(partes) + 1)):
            continue
        achadas[os.sep.join(partes[:3])] += sum(1 for a in arquivos if a.endswith(".md"))
    return achadas


# ------------------------------------------------------------------------------------------ SVG

FUNDO, CARTAO, TRILHA = "#0d1117", "#161b22", "#21262d"
TEXTO, FRACO, BORDA = "#e6edf3", "#8b949e", "#30363d"
CHEIO, PARCIAL, VAZIO = "#3fb950", "#58a6ff", "#484f58"

LARG = 1180
X_ROTULO, X_BARRA, LARG_BARRA = 24, 430, 470
X_NUM, X_PCT = X_BARRA + LARG_BARRA + 16, LARG - 24


def mil(n):
    return f"{n:,}".replace(",", ".")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cor(atual, meta):
    if meta is None:
        return FRACO
    if atual == 0:
        return VAZIO
    return CHEIO if atual >= meta else PARCIAL


def barra(y, atual, meta, altura=9):
    frac = min(atual / meta, 1.0) if meta else 0.0
    larg = max(round(LARG_BARRA * frac), 2 if atual else 0) if meta is not None else 0
    r = altura / 2
    partes = [f'<rect x="{X_BARRA}" y="{y}" width="{LARG_BARRA}" height="{altura}" rx="{r}" fill="{TRILHA}"/>']
    if larg:
        partes.append(f'<rect x="{X_BARRA}" y="{y}" width="{larg}" height="{altura}" rx="{r}" '
                      f'fill="{cor(atual, meta)}"/>')
    return "".join(partes)


def linha(y, rotulo, atual, meta, destaque=False):
    peso, tam, cl = ("600", 13, TEXTO) if destaque else ("400", 12, FRACO)
    pct = percentual(atual, meta)
    numeros = f"{mil(atual)} / {mil(meta)}" if meta is not None else "sem meta"
    return (
        f'<text x="{X_ROTULO}" y="{y + 9}" font-size="{tam}" font-weight="{peso}" fill="{cl}">'
        f'{esc(rotulo)}</text>'
        + barra(y, atual, meta)
        + f'<text x="{X_NUM}" y="{y + 9}" font-size="11" fill="{FRACO}" font-family="ui-monospace,monospace">'
          f'{numeros}</text>'
        + f'<text x="{X_PCT}" y="{y + 9}" font-size="11.5" text-anchor="end" font-weight="600" '
          f'fill="{cor(atual, meta)}" font-family="ui-monospace,monospace">{pct}</text>'
    )


def totais(medidas):
    """Total, numerador limitado à meta de cada série, metas e documentos sem meta."""
    return (sum(n for _, n in medidas),
            sum(min(n, i.meta) for i, n in medidas if i.meta is not None),
            sum(i.meta for i, _ in medidas if i.meta is not None),
            sum(n for i, n in medidas if i.meta is None))


def percentual(atual, meta):
    if not meta:
        return "—"
    valor = 100 * atual / meta
    return f"{min(valor, 99.9) if atual < meta else valor:.1f}%"


def resumo(medidas):
    total, conhecido, meta, desconhecido = totais(medidas)
    if not meta:
        return f"{mil(total)} documentos · universo desconhecido"
    if not any(i.meta is None for i, _ in medidas) and total == conhecido:
        return f"{mil(total)} / ~{mil(meta)} documentos ({percentual(conhecido, meta)})"
    return (f"{mil(total)} documentos · {mil(conhecido)} / ~{mil(meta)} nas séries com meta "
            f"({percentual(conhecido, meta)}) · {mil(desconhecido)} sem meta")


def desenhar(medidas):
    atual_item = {id(i): n for i, n in medidas}
    total, conhecido, meta, desconhecido = totais(medidas)
    corpo, y = [], 174
    for fase in sorted(FASES):
        itens = [(i, n) for i, n in medidas if i.fase == fase]
        _, fa, fm, fu = totais(itens)
        titulo, nota = FASES[fase]
        corpo.append(f'<rect x="0" y="{y - 22}" width="{LARG}" height="1" fill="{BORDA}"/>')
        corpo.append(f'<text x="{X_ROTULO}" y="{y}" font-size="12.5" font-weight="700" fill="{TEXTO}">{esc(titulo.upper())}</text>')
        corpo.append(f'<text x="{X_BARRA}" y="{y}" font-size="11" fill="{FRACO}">{esc(nota)}</text>')
        corpo.append(f'<text x="{X_PCT}" y="{y}" font-size="12.5" text-anchor="end" fill="{PARCIAL}">{percentual(fa, fm)}</text>')
        y += 20
        for setor, itens_setor in por_setor().items():
            pares = [(i, atual_item[id(i)]) for i in itens_setor if i.fase == fase]
            if not pares:
                continue
            _, a, m, u = totais(pares)
            corpo.append(linha(y, setor, a, m if any(i.meta is not None for i, _ in pares) else None, destaque=True))
            y += 22
            if any(i.meta is None for i, _ in pares):
                corpo.append(f'<text x="{X_BARRA}" y="{y}" font-size="11" fill="{FRACO}">{mil(u)} documentos em séries sem meta</text>')
                y += 16
        y += 24
    altura = y + 34
    frac = min(conhecido / meta, 1) if meta else 0
    base_percentual = f"Percentuais: somente séries com meta · {mil(conhecido)} / ~{mil(meta)}" if meta else "Percentual indisponível: universo desconhecido"
    cab = [f'<rect width="{LARG}" height="{altura}" fill="{FUNDO}"/>',
           f'<text x="{X_ROTULO}" y="40" font-size="21" font-weight="700" fill="{TEXTO}">Acervo da legislação brasileira</text>',
           f'<text x="{X_ROTULO}" y="62" font-size="12.5" fill="{TEXTO}">{mil(total)} documentos em Markdown · {mil(desconhecido)} em séries sem meta</text>',
           f'<text x="{X_ROTULO}" y="82" font-size="12" fill="{FRACO}">{base_percentual}</text>',
           f'<text x="{X_PCT}" y="82" font-size="13" text-anchor="end" fill="{PARCIAL}">{percentual(conhecido, meta)}</text>',
           f'<rect x="{X_ROTULO}" y="98" width="{LARG - 48}" height="16" rx="8" fill="{TRILHA}"/>']
    if frac:
        cab.append(f'<rect x="{X_ROTULO}" y="98" width="{round((LARG - 48) * frac)}" height="16" rx="8" fill="{PARCIAL}"/>')
    pe = f'<text x="{X_ROTULO}" y="{altura - 14}" font-size="10.5" fill="{FRACO}">Atualizado em {dt.date.today():%d/%m/%Y} · metas estimadas ou contadas nos índices oficiais</text>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{LARG}" height="{altura}" viewBox="0 0 {LARG} {altura}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">'
            + "".join(cab + corpo) + pe + "</svg>\n")


def markdown(medidas, achadas, pendentes=()):
    L = ["# Progresso", "", f"Gerado em {dt.datetime.now(ZoneInfo('America/Recife')):%d/%m/%Y %H:%M:%S} (America/Recife). Escopo: `scripts/plano.py`.", "",
         "Percentuais usam somente documentos e metas das séries com universo estimado ou contado. "
         "Séries sem meta ficam fora do cálculo. Cada série contribui até sua própria meta. "
         "Volume não comprova integralidade das fontes ou qualidade das conversões.", "",
         f"**{resumo(medidas)}**", "", "![progresso](progresso.svg)", ""]
    if pendentes:
        L += [f"Há {mil(len(pendentes))} pendências de integralidade registradas em "
              "[registro auditável](scripts/dados/pendencias-integralidade-publicadas.json). "
              "Esses documentos ficam fora da contagem até validação; seus textos e histórico são preservados.", ""]
    atual_item = {id(i): n for i, n in medidas}
    for fase in sorted(FASES):
        itens = [(i, n) for i, n in medidas if i.fase == fase]
        titulo, nota = FASES[fase]
        L += [f"## {titulo}", "", nota[0].upper() + nota[1:] + ".", "", resumo(itens), ""]
        for setor, itens_setor in por_setor().items():
            pares = [(i, atual_item[id(i)]) for i in itens_setor if i.fase == fase]
            if not pares:
                continue
            L += [f"### {setor}", "", resumo(pares), "",
                  "| | Tipo de norma | Tem | Meta | Pasta | Fonte |", "| :-: | --- | ---: | ---: | --- | --- |"]
            for i, n in pares:
                marca = "—" if i.meta is None else ("✅" if n >= i.meta else ("🟦" if n else "⬜️"))
                pasta = ", ".join(f"`{p.strip()}`" for p in i.caminho.split(","))
                meta = "desconhecida" if i.meta is None else mil(i.meta)
                L.append(f"| {marca} | {i.nome} | {mil(n)} | {meta} | {pasta} | {i.fonte} |")
            L.append("")
    L += ["---", "", "## Pastas fora do plano", ""]
    if achadas:
        L += ["| Pasta | Arquivos |", "| --- | ---: |"]
        L += [f"| `{p}` | {mil(n)} |" for p, n in achadas.most_common()]
    else:
        L.append("Nenhuma: todo arquivo do repositório está sob um item do plano.")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--conferir", action="store_true", help="só imprime o resumo, não grava arquivos")
    ap.add_argument("--git-index", action="store_true", help="mede somente arquivos adicionados ao próximo commit")
    args = ap.parse_args()

    pendentes = carregar_pendencias(RAIZ, args.git_index)
    if args.git_index:
        medidas, achadas = medir_git(pendentes)
    else:
        medidas, cobertas = medir(pendentes)
        achadas = orfas(cobertas)
    for setor, itens in por_setor().items():
        print(setor + ": " + resumo([(i, n) for i, n in medidas if i in itens]))
    print("\nTOTAL: " + resumo(medidas))
    for pasta, n in achadas.most_common():
        print(f"fora do plano: {pasta} ({mil(n)} arquivos)")

    if args.conferir:
        return
    with open(os.path.join(RAIZ, "progresso.svg"), "w", encoding="utf-8") as f:
        f.write(desenhar(medidas))
    with open(os.path.join(RAIZ, "PROGRESSO.md"), "w", encoding="utf-8") as f:
        f.write(markdown(medidas, achadas, pendentes))
    print("\ngravados: progresso.svg, PROGRESSO.md")


if __name__ == "__main__":
    main()
