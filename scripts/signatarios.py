"""Extrai os signatários de uma norma a partir do bloco de assinatura no fim do texto.

As normas brasileiras terminam com quem as assinou: o chefe do Executivo em caixa alta e, abaixo,
os ministros ou secretários que referendaram. Leis promulgadas pelo Legislativo trazem
"a) Nome - Presidente". Isto é heurística sobre texto livre (parte dele vindo de OCR), então erra:
o `grau` devolvido diz o quanto confiar.

Uso como biblioteca: `signatarios(corpo)` -> (principal, [demais], grau).
"""
import re
import unicodedata

# linhas do bloco final que não são nome de pessoa
RUIDO = re.compile(
    r"LEI|DECRETO|EMENDA|CONSTITUI|ASSEMBLEIA|ASSEMBLÉIA|CONGRESSO|SENADO|CÂMARA|CAMARA|"
    r"PAL[ÁA]CIO|GOVERNO|ESTADO|UNI[ÃA]O|REP[ÚU]BLICA|SECRETARI|GABINETE|MINIST[ÉE]RIO|"
    r"PRESID[ÊE]NCIA|PUBLICAD|REGISTRAD|DI[ÁA]RIO|OFICIAL|BRAS[ÍI]LIA|ANEXO|TABELA|"
    r"PROJETO|AUTORIA|JUSTIFICATIVA|VETAD|SAN[ÇC]IONAD|PROMULGAD|ARTIGO|PAR[ÁA]GRAFO|"
    r"TOTAL|VALOR|R\$|CARGO|REFER[ÊE]NCIA|QUADRO|ÓRG[ÃA]O|ORG[ÃA]O|DEPARTAMENTO|"
    r"DIVIS[ÃA]O|SE[ÇC][ÃA]O|SUBSE[ÇC][ÃA]O|T[ÍI]TULO|CAP[ÍI]TULO|LIVRO|PARTE|VIGOR|"
    r"DISPOSI[ÇC]|CONTR[ÁA]RIO|REVOGA|FIM DO|DOCUMENTO|RELA[ÇC][ÃA]O|SERVIDOR|LISTA|"
    r"DENOMINA|S[ÍI]MBOLO|SIMBOLO|FUN[ÇC][ÃA]O|GRATIFICA|UTILIDADE|P[ÚU]BLICA|DECLARA|"
    r"INSTITUI|AUTORIZA|ALTERA|DISP[ÕO]E|CRIA|FICA|SUMÁRIO|SUMARIO|EMPRESA|MUNIC[ÍI]PIO"
)
# partículas que podem ficar minúsculas num nome em caixa alta
PARTICULAS = {"de", "da", "do", "das", "dos", "e", "a", "o", "em", "del", "di", "la", "y"}
CARGO = re.compile(
    r"^(?:Governador|Presidente|Vice|Deputad|Senador|Secret[áa]ri|Ministr|Chefe|Procurador|"
    r"1[º°]|2[º°]|Primeir|Segund)", re.I
)


def _sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


# topônimos que passam por nome de pessoa ("Rio Grande do Norte"). Comparados por igualdade, não
# por substring: "Paulo" e "Grande" são sobrenomes legítimos.
LUGARES = {
    "rio grande do norte", "rio grande do sul", "mato grosso", "mato grosso do sul",
    "rio de janeiro", "sao paulo", "minas gerais", "espirito santo", "santa catarina",
    "distrito federal", "rio branco", "belo horizonte", "porto alegre", "campo grande",
    "joao pessoa", "boa vista", "porto velho", "sao luis", "republica federativa do brasil",
}


def _nome_valido(s):
    s = s.strip(" .,;:-–—*_")
    if not (6 <= len(s) <= 60):
        return None
    if re.search(r"[\d@/\\|()\[\]]", s):
        return None
    palavras = s.split()
    if not (2 <= len(palavras) <= 7):
        return None
    if RUIDO.search(_sem_acento(s).upper()):
        return None
    if _sem_acento(s).lower() in LUGARES:
        return None
    # cada palavra é um nome próprio (ou partícula): só letras, sem siglas de uma letra
    for p in palavras:
        limpo = p.strip(".,")
        if limpo.lower() in PARTICULAS:
            continue
        # abreviatura ("Tec.", "Dr.", "Cel."): linha de cargo ou de tabela, não nome de pessoa
        if p.endswith(".") and len(limpo) <= 4:
            return None
        if not re.fullmatch(r"[A-Za-zÀ-ÿ'´`]{2,}", limpo):
            return None
    return " ".join(palavras)


def _titulo(s):
    """CAIXA ALTA -> Caixa Alta, preservando partículas minúsculas."""
    if not s.isupper():
        return s
    saida = []
    for i, p in enumerate(s.split()):
        baixo = p.lower()
        saida.append(baixo if i and baixo.strip(".,") in PARTICULAS else baixo.capitalize())
    return " ".join(saida)


def signatarios(corpo, cauda=28):
    """(principal, [demais], grau) a partir do fim do texto.

    grau: "caixa-alta" (bloco de assinatura do Executivo), "promulgacao" ("a) Nome - Cargo")
    ou None quando nada foi reconhecido.
    """
    linhas = [ln.strip().rstrip("\\") for ln in corpo.strip().split("\n")]
    linhas = [ln for ln in linhas if ln.strip()][-cauda:]

    # 1) "a) Samuel Moreira - Presidente": promulgação pelo Legislativo
    promulgados = []
    for ln in linhas:
        m = re.match(r"^a\)\s*(.+?)\s*[-–—]\s*(.+)$", ln)
        if m and _nome_valido(m.group(1)):
            promulgados.append(_nome_valido(m.group(1)))
    if promulgados:
        return promulgados[0], promulgados[1:], "promulgacao"

    # 2) bloco de assinatura: o chefe do Executivo assina primeiro.
    # Aceita só dois sinais fortes — a linha está em CAIXA ALTA, ou a linha seguinte é um cargo.
    # Sem isso, frases como "Declara de utilidade pública" passariam por nome de pessoa.
    limpas = [re.sub(r"\*+", "", ln).strip() for ln in linhas]
    nomes = []
    for i, texto in enumerate(limpas):
        if CARGO.match(texto):  # linha de cargo, não de nome
            continue
        n = _nome_valido(texto)
        if not n:
            continue
        seguinte = limpas[i + 1] if i + 1 < len(limpas) else ""
        if n.isupper() or CARGO.match(seguinte):
            nomes.append(_titulo(n))
    if nomes:
        # remove repetições preservando a ordem
        vistos, unicos = set(), []
        for n in nomes:
            if n.lower() not in vistos:
                vistos.add(n.lower())
                unicos.append(n)
        return unicos[0], unicos[1:], "caixa-alta"

    return None, [], None
