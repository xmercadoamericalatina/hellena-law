"""Revisão documental de epígrafe incompleta com número próprio e fecho próprio.

Recebe texto convertido diretamente do HTML, sem o H1 gerado dos metadados.
Nunca substitui uma data completa divergente nem usa data de citação/anexo.
O guard normal permanece conservador; este método complementar fica explícito
no manifesto de revisão e preserva a redação defeituosa da fonte.
"""
import datetime as dt
import re
import unicodedata
from identidade_decreto import MESES, extrair_epigrafe_decreto, numero_normalizado

MESES_RE = '|'.join(MESES)
ABERTURA = re.compile(r'^DECRETO\s+(?:N(?:UMERO)?[.º°O\s]*)?(?P<numero>\d[\d.,]*(?:\s*[-–]\s*[A-Z])?)')
ARTIGO = re.compile(r'^\s*(?:ARTIGO|ART\.?)\s*[.º°O]*\s*(?:\d|UNICO)')
FECHO = re.compile(r'^(?:RIO DE JANEIRO|BRASILIA)[,.;\s]*(?:EM\s*)?(?:DE\s*)?'
                   r'(?P<dia>\d{1,2})[º°]?\s*(?:DE\s*)?'
                   rf'(?P<mes>{MESES_RE})\s*[,;]?\s*(?:DE\s*)?(?P<ano>[12]\.?\d{{3}})(?!\d)')


def normal(text):
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'[*_`\\]', '', text)
    return re.sub(r'\s+', ' ', ''.join(c for c in unicodedata.normalize('NFD', text.upper())
                                     if not unicodedata.combining(c))).strip()


def mes_defeituoso_compativel(literal, esperado):
    if literal == esperado or (len(literal) >= 3 and literal in esperado):
        return True
    if len(literal) == len(esperado):
        positions = [i for i, (a, b) in enumerate(zip(literal, esperado)) if a != b]
        return len(positions) <= 1 or (len(positions) == 2 and positions[1] == positions[0] + 1
                                     and literal[positions[0]] == esperado[positions[1]]
                                     and literal[positions[1]] == esperado[positions[0]])
    if abs(len(literal) - len(esperado)) == 1:
        short, long = sorted((literal, esperado), key=len)
        return any(long[:i] + long[i+1:] == short for i in range(len(long)))
    return False


def verificar_epigrafe_e_fecho(corpo_html_convertido, numero, data):
    esperada = dt.date.fromisoformat(data)
    blocks = corpo_html_convertido.split('\n\n')
    # H1 de metadados não pode virar evidência de identidade da fonte.
    source = '\n\n'.join(b for b in blocks if not b.lstrip().startswith('# '))
    completa = extrair_epigrafe_decreto(source)
    if completa:
        if completa['numero'] == numero_normalizado(numero) and completa['data'] == data:
            return {'metodo': 'epigrafe_completa', 'epigrafe': completa}
        return None
    abertura = None
    for block in blocks[:8]:
        if block.lstrip().startswith('# '):
            continue
        n = normal(block)
        if ARTIGO.match(n):
            break
        match = ABERTURA.match(n)
        if match:
            if numero_normalizado(match['numero']) != numero_normalizado(numero):
                return None
            tail = n[match.end():]
            year = re.search(r'(?<!\d)([12]\.?\d{3})(?!\d)', tail)
            if year and int(year[1].replace('.', '')) != esperada.year:
                return None
            before_year = tail[:year.start()] if year else tail
            day = re.match(r'^[\s,;:.–—/-]*(?:DE\s*)?(\d{1,2})(?!\d)', before_year)
            if day and int(day[1]) != esperada.day:
                return None
            numeric = re.match(r'^[\s,;:.–—/-]*(?:DE\s*)?(\d{1,2})\s*(?:[/.-]|DE\s*|\s)\s*(\d{1,2})\s*(?:[/.-]|DE\s*|\s)\s*(\d{2,4})(?!\d)', tail)
            if numeric and (int(numeric[1]) != esperada.day or int(numeric[2]) != esperada.month
                            or int(numeric[3]) not in {esperada.year, esperada.year % 100}):
                return None
            short_year = re.search(r'[A-Z]+\s+DE\s+(\d{2})(?!\d)', tail)
            if short_year and int(short_year[1]) != esperada.year % 100:
                return None
            known_months = re.findall(MESES_RE, before_year)
            if any(MESES[m] != esperada.month for m in known_months):
                return None
            parcial = re.match(r'^[\s,;:.–—/-]*(?:DE\s*)?(\d{1,2})[º°]?\s*(?:DE\s*)?([A-Z]+)', tail)
            literal_mes = parcial[2] if parcial else None
            if literal_mes and literal_mes.endswith('DE'):
                literal_mes = literal_mes[:-2]
            if literal_mes and not known_months:
                expected = next(name for name, value in MESES.items() if value == esperada.month)
                if not mes_defeituoso_compativel(literal_mes, expected):
                    return None
            abertura = {'numero': numero_normalizado(match['numero']), 'texto': block.strip(), 'mes_literal': literal_mes}
            break
    if not abertura:
        return None
    artigo_visto = False
    for block in blocks:
        n = normal(block)
        artigo_visto |= bool(ARTIGO.match(n))
        if not artigo_visto:
            continue
        if re.match(r'^(?:ANEXO\b|REGULAMENTO\b|CONVENCAO\b|ACORDO\b)', n):
            return None  # data de anexo não substitui fecho do decreto
        match = FECHO.match(n)
        if not match:
            continue
        try:
            encontrada = dt.date(int(match['ano'].replace('.', '')), MESES[match['mes']], int(match['dia']))
        except ValueError:
            return None
        if encontrada != esperada:
            return None
        return {'metodo': 'numero_proprio_e_data_do_fecho_proprio', 'epigrafe': abertura,
                'fecho': {'texto': block.strip(), 'data': encontrada.isoformat()},
                'ressalva': 'Epígrafe incompleta/defeituosa preservada; data completa corroborada no fecho do próprio decreto.'}
    return None
