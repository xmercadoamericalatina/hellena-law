"""Corrige ordinais mal reconhecidos pelo OCR: "Art. 19" onde o original traz "Art. 1º".

O Vision lê o "º" como "9", então Art. 1º/2º/3º viram Art. 19/29/39. A correção só é aplicada
quando a hipótese se sustenta no documento inteiro: substituindo todo "Art. d9" por "Art. dº",
a sequência de artigos tem de ficar não decrescente e começar em 1. Assim um "Art. 19" legítimo
(num texto que já tem os artigos 1 a 18) nunca é alterado.

Mexe apenas em arquivos marcados como OCR. Uso:

    python3 -I scripts/corrigir_ocr.py            # simulação: só relata
    python3 -I scripts/corrigir_ocr.py --aplicar  # grava
"""
import collections
import os
import re
import sys

RAIZ = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "estaduais")
MARCA = "obtido por OCR"
# "Art. 19", "**Art. 19**", "Art. 19 -", mas não "Art. 19.407" nem "Art. 19º"
ARTIGO = re.compile(r"(Art\.? ?)(\d+)(?![\dº°o./-])")


def numeros(texto):
    return [int(m.group(2)) for m in ARTIGO.finditer(texto)]


def quantos_converter(nums):
    """Tamanho da sequência inicial 19, 29, 39... na ordem — as únicas ocorrências convertidas.

    Só a corrida que começa em 19 e avança de dez em dez é tratada como ordinal. Um "Art. 99"
    solto costuma ser citação de outra lei ("o artigo 99 da Lei Complementar nº 28") e fica
    como está. Exige ao menos dois termos: um "Art. 19" isolado não é evidência suficiente.
    """
    esperado = 19
    n = 0
    convertidos = []
    for num in nums:
        if num == esperado:
            convertidos.append(esperado // 10)
            esperado += 10
            n += 1
        else:
            convertidos.append(num)
    if n < 2:
        return 0
    # a conversão tem de deixar a numeração coerente: começando em 1 e não decrescente.
    # Numa lei de verdade com os artigos 1 a 29, converter o 19 em 1º quebraria a ordem.
    if convertidos[0] != 1 or any(b < a for a, b in zip(convertidos, convertidos[1:])):
        return 0
    return n


def corrigir(texto, limite):
    """Converte as `limite` primeiras ocorrências da corrida 19, 29, 39... em 1º, 2º, 3º..."""
    estado = {"esperado": 19, "feitos": 0}

    def troca(m):
        if estado["feitos"] >= limite:
            return m.group(0)
        if int(m.group(2)) == estado["esperado"]:
            d = estado["esperado"] // 10
            estado["esperado"] += 10
            estado["feitos"] += 1
            return f"{m.group(1)}{d}º"
        return m.group(0)

    return ARTIGO.sub(troca, texto)


def main(aplicar):
    cont = collections.Counter()
    por_uf = collections.Counter()
    exemplos = []
    for dp, dn, fn in os.walk(RAIZ):
        dn[:] = [d for d in dn if not d.startswith("_")]
        for f in sorted(fn):
            if not f.endswith(".md"):
                continue
            p = os.path.join(dp, f)
            with open(p, encoding="utf-8", errors="replace") as h:
                texto = h.read()
            # o aviso vem depois do cabeçalho e do título; em ementa longa passa de 600
            # caracteres, então a busca é no arquivo inteiro
            if MARCA not in texto:
                continue
            cont["ocr"] += 1
            nums = numeros(texto)
            limite = quantos_converter(nums) if nums else 0
            if not limite:
                continue
            novo = corrigir(texto, limite)
            if novo == texto:
                continue
            cont["corrigidos"] += 1
            por_uf[os.path.relpath(p, RAIZ).split(os.sep)[0]] += 1
            if len(exemplos) < 5:
                exemplos.append((p, nums[:6]))
            if aplicar:
                with open(p, "w", encoding="utf-8") as h:
                    h.write(novo)
    print(f"arquivos de OCR: {cont['ocr']}; com ordinal corrigido: {cont['corrigidos']}")
    print("por UF:", dict(por_uf.most_common()))
    for p, n in exemplos:
        print("  ex:", os.path.relpath(p, RAIZ), n)
    if not aplicar:
        print("simulação — use --aplicar para gravar")


if __name__ == "__main__":
    main("--aplicar" in sys.argv)
