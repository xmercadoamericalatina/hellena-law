"""Refaz o OCR dos .md que vieram de PDF escaneado, com a versão atual do `scripts/bin/ocr`.

Existe por causa de uma correção específica: o OCR passou a respeitar a ordem de leitura em
páginas de duas colunas (ver `scripts/ocr.swift`). Os arquivos gravados antes dessa correção têm o
texto das colunas intercalado linha a linha. O `reconverter.py` não serve aqui — ele regenera o
corpo a partir do HTML e **pula** de propósito o que veio de OCR, porque reprocessar um PDF custa
uma ordem de grandeza mais.

O que faz, por arquivo: localiza o original em `_fonte`, refaz o OCR, remonta o corpo pelo mesmo
caminho que os raspadores usam (`comum.documento_para_md`), reaplica a correção de ordinais do
`corrigir_ocr.py` — que já tinha sido aplicada ao texto gravado — e só reescreve se o resultado
diferir. Assim a comparação é entre iguais e um arquivo que não mudou não é tocado.

Idempotente e em simulação por padrão, como os demais scripts de manutenção: só grava com
`--aplicar`. Rodar de novo, depois de aplicado, relata zero mudanças.

    python3 -I scripts/reocr.py                  # simula sobre o acervo inteiro
    python3 -I scripts/reocr.py PB PI --aplicar  # grava, só nessas UFs
    python3 -I scripts/reocr.py --limite 50      # amostra, para estimar quanto vai mudar

Refazer o OCR é caro: alguns segundos por página. Conte horas para o acervo inteiro.
"""
import argparse
import gzip
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import AVISO_OCR, documento_para_md  # noqa: E402
from corrigir_ocr import corrigir, numeros, quantos_converter  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def mapa_de_fontes(bases):
    """(unidade, nome do arquivo) -> original; nomes coincidem entre esferas e UFs."""
    mapa = {}
    for base in bases:
        for dirpath, dirs, arquivos in os.walk(base):
            if os.sep + "_fonte" not in dirpath + os.sep:
                continue
            for a in arquivos:
                if a.endswith(".html.gz"):
                    unidade = dirpath.split(os.sep + "_fonte", 1)[0]
                    nome = a[: -len(".html.gz")]
                    mapa[(os.path.abspath(unidade), nome)] = os.path.join(dirpath, a)
    return mapa


def arquivos_com_ocr(bases):
    for base in bases:
        for dirpath, dirs, arquivos in os.walk(base):
            dirs[:] = [d for d in dirs if not d.startswith("_")]
            for a in arquivos:
                if not a.endswith(".md"):
                    continue
                caminho = os.path.join(dirpath, a)
                with open(caminho, encoding="utf-8") as f:
                    cabeca = f.read(4000)
                if "Texto obtido por OCR" in cabeca:
                    yield caminho


def partes(texto):
    """(front matter + título, corpo) de um .md do acervo."""
    if not texto.startswith("---\n"):
        return None, texto
    _, cab, resto = texto.split("---\n", 2)
    # o corpo começa depois do "# título" e da linha em branco que o segue
    linhas = resto.split("\n")
    i = next((n for n, ln in enumerate(linhas) if ln.startswith("# ")), None)
    if i is None:
        return "---\n" + cab + "---\n", resto
    return "---\n" + cab + "---\n" + "\n".join(linhas[: i + 2]) + "\n", "\n".join(linhas[i + 2:])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("alvos", nargs="*", help="federal ou siglas de UF; vazio = tudo")
    ap.add_argument("--aplicar", action="store_true", help="grava; sem isso, só relata")
    ap.add_argument("--limite", type=int, default=0, help="processa só os N primeiros (amostra)")
    a = ap.parse_args()

    if a.alvos:
        bases = [os.path.join(RAIZ, "federal") if t == "federal"
                 else os.path.join(RAIZ, "estaduais", t.upper()) for t in a.alvos]
    else:
        bases = [os.path.join(RAIZ, "federal"), os.path.join(RAIZ, "estaduais")]
    bases = [b for b in bases if os.path.isdir(b)]

    fontes = mapa_de_fontes(bases)
    print(f"{len(fontes)} originais indexados em _fonte", flush=True)

    alvos = list(arquivos_com_ocr(bases))
    if a.limite:
        alvos = alvos[: a.limite]
    print(f"{len(alvos)} arquivos vieram de OCR", flush=True)

    cont = {"mudou": 0, "igual": 0, "sem_fonte": 0, "erro": 0}
    for n, md in enumerate(alvos, 1):
        nome = os.path.basename(md)[:-3]
        partes_md = os.path.relpath(md, RAIZ).split(os.sep)
        unidade = os.path.join(RAIZ, *partes_md[:2]) if partes_md[0] == "estaduais" else os.path.join(RAIZ, partes_md[0])
        src = fontes.get((unidade, nome))
        if not src:
            cont["sem_fonte"] += 1
            continue
        try:
            bruto = gzip.open(src, "rb").read()
            if not bruto.startswith(b"%PDF"):
                cont["sem_fonte"] += 1
                continue
            corpo, motivo = documento_para_md(bruto, src)
            if corpo is None:
                cont["erro"] += 1
                continue
            # o texto gravado já passou por corrigir_ocr.py; aplica a mesma regra ao novo, com o
            # mesmo critério de quantas ocorrências converter, para que a comparação seja entre iguais
            nums = numeros(corpo)
            limite = quantos_converter(nums) if nums else 0
            if limite:
                corpo = corrigir(corpo, limite)
            texto = open(md, encoding="utf-8").read()
            cabeca, antigo = partes(texto)
            novo = (AVISO_OCR + corpo) if not corpo.startswith(AVISO_OCR.strip()[:20]) else corpo
            if novo.strip() == antigo.strip():
                cont["igual"] += 1
            else:
                cont["mudou"] += 1
                print(f"  muda: {os.path.relpath(md, RAIZ)}", flush=True)
                if a.aplicar:
                    tmp = md + ".tmp"
                    with open(tmp, "w", encoding="utf-8") as f:
                        f.write(cabeca + novo.lstrip("\n"))
                    os.replace(tmp, md)
        except Exception as e:
            cont["erro"] += 1
            print(f"  erro: {os.path.relpath(md, RAIZ)}: {str(e)[:120]}", flush=True)
        if n % 100 == 0:
            print(f"{n}/{len(alvos)} {cont}", flush=True)

    print(("APLICADO " if a.aplicar else "SIMULAÇÃO ") + str(cont), flush=True)
    if not a.aplicar and cont["mudou"]:
        print("nada foi gravado; repita com --aplicar", flush=True)


if __name__ == "__main__":
    main()
