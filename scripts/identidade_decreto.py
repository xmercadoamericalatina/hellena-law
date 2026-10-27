"""Confronto conservador da epígrafe própria de decretos federais numerados.

Não usa citações no articulado, ementas ou fechos como identidade substituta.
Ausência de epígrafe inequívoca retorna None, nunca confirmação de identidade.
"""
import datetime as dt
import re
import unicodedata

MESES = {nome: n for n, nome in enumerate(
    ("JANEIRO", "FEVEREIRO", "MARCO", "ABRIL", "MAIO", "JUNHO", "JULHO",
     "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"), 1)}
EPIGRAFE = re.compile(
    r"^DECRETO\s+(?:N(?:UMERO)?[.º°O\s]*)?"
    r"(?P<numero>\d[\d.,]*(?:\s*[-–]\s*[A-Z])?)"
    r"\s*[,;:.–—-]*\s*(?:DE\s*)?"
    r"(?P<dia>\d{1,2})[º°]?\s*(?:DE\s*)?(?P<mes>JANEIRO|FEVEREIRO|MARCO|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)\s*[,;]?\s*(?:DE\s*)?"
    r"(?P<ano>[12]\.?\d{3})(?!\d)"
)


def numero_normalizado(numero):
    return re.sub(r"[.,\s]", "", str(numero)).replace("–", "-").upper()


def extrair_epigrafe_decreto(corpo):
    # Só os primeiros blocos de abertura. Uma citação posterior não é epígrafe.
    for bloco in corpo.split("\n\n")[:8]:
        limpo = re.sub(r"[*_`\\]", "", bloco).lstrip("# \t\n")
        limpo = re.sub(r"\s+", " ", limpo).strip()
        if re.match(r"^(?:Art\.?|Artigo)\s*(?:\d|[úu]nico)", limpo, re.I):
            break
        normal = "".join(c for c in unicodedata.normalize("NFD", limpo.upper())
                         if not unicodedata.combining(c))
        match = EPIGRAFE.match(normal)
        if not match or match["mes"] not in MESES:
            continue
        try:
            data = dt.date(int(match["ano"].replace(".", "")), MESES[match["mes"]], int(match["dia"]))
        except ValueError:
            continue
        return {"numero": numero_normalizado(match["numero"]), "data": data.isoformat(),
                "epigrafe": limpo}
    return None


def divergencia_epigrafe_decreto(tipo, numero, data, corpo):
    if tipo != "DEC-n":
        return None
    encontrada = extrair_epigrafe_decreto(corpo)
    if encontrada is None:
        return None  # inconclusivo; não equivale a epígrafe validada
    esperada = {"numero": numero_normalizado(numero), "data": data}
    if all(encontrada[k] == esperada[k] for k in esperada):
        return None
    return {"motivo": "Epígrafe própria diverge do número/data do índice e URN; revisão necessária; fonte preservada",
            "identidade_esperada": esperada, "epigrafe_encontrada": encontrada}
