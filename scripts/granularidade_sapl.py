"""Sinaliza outras epígrafes normativas em anexos atribuídos a uma norma SAPL.

Detector conservador: não recorta, não apaga texto e não trata referência corrida
ou citação entre aspas como nova norma. Alertas exigem revisão do PDF original.
"""
import re
import unicodedata

EPIGRAFE = re.compile(
    r"^(?:\s*[*#]+\s*)?"
    r"(?P<tipo>EMENDA(?:\s+[AÀ]\s+(?:LEI\s+ORG[ÂA]NICA|LOMAN))?|"
    r"LEI(?:\s+(?:COMPLEMENTAR|MUNICIPAL|PROMULGADA))?|DECRETO(?:\s+(?:LEGISLATIVO|MUNICIPAL))?|PORTARIA|RESOLU[ÇC][ÃA]O)"
    r"\s+(?:N(?:[.º°O\s])*\s*)?(?P<numero>\d[\d.]*(?:-[A-Z])?)"
    r"(?:\s*/\s*\d{2,4}\b|\s*[,–—-]?\s+DE\s+\d{1,2}(?:[º°])?(?:\s|/))",
    re.I | re.M)


def normal(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.upper()) if not unicodedata.combining(c))


def classe(tipo):
    t = normal(tipo)
    if 'EMENDA' in t:
        return 'EMENDA'
    if 'LEI COMPLEMENTAR' in t:
        return 'LEI COMPLEMENTAR'
    if 'DECRETO LEGISLATIVO' in t:
        return 'DECRETO LEGISLATIVO'
    if 'LEI ORGANICA' in t or t == 'LOMAN':
        return 'LEI ORGANICA'
    for nome in ('LEI', 'DECRETO', 'PORTARIA', 'RESOLUCAO'):
        if nome in t:
            return nome
    return t


def numero_base(numero):
    m = re.match(r'\s*(\d[\d.]*(?:-[A-Z])?)', str(numero), re.I)
    if not m:
        return None
    return m[1].replace('.', '').upper().lstrip('0') or '0'


def alertas_multiplos_atos(corpo, tipo, numero):
    esperada = (classe(tipo), numero_base(numero))
    alertas = []
    vistos = set()
    for m in EPIGRAFE.finditer(corpo):
        identidade = (classe(m['tipo']), numero_base(m['numero']))
        if identidade == esperada or identidade in vistos:
            continue
        vistos.add(identidade)
        fim = corpo.find('\n\n', m.start())
        fim = min(len(corpo), m.start() + 350) if fim < 0 else min(fim, m.start() + 350)
        alertas.append({'identidade_esperada': esperada, 'epigrafe_diversa': identidade,
                        'posicao_no_corpo': m.start(), 'trecho': corpo[m.start():fim].strip(),
                        'motivo': 'epígrafe de outra identidade no anexo; possível página/edição com múltiplos atos; revisar sem cortar automaticamente'})
    return alertas


def alertas_outras_publicacoes(corpo):
    """Avisos/extratos de outra coluna podem não conter epígrafe de lei/decreto."""
    padrao = re.compile(
        r'EDITAL\s+DISPON[IÍ]VEL|ABERTURA\s+DA\s+SESS[AÃ]O(?!\s+LEGISLATIVA)|RECEBIMENTO\s+DAS\s+PROPOSTAS|'
        r'PREG[AÃ]O\s+(?:ELETR[OÔ]NICO|PRESENCIAL)\s+N[.º°O\s]*\d|'
        r'EXTRATO\s+(?:DE|DO)\s+(?:CONTRATO|TERMO|DISPENSA|INEXIGIBILIDADE|ATA|ADITIVO)', re.I)
    return [{'offset':m.start(),'trecho':corpo[max(0,m.start()-150):m.end()+300],
             'motivo':'possível aviso/extrato de outra publicação; pode ser citação ou modelo, exige revisão contextual sem corte automático'}
            for m in padrao.finditer(corpo)]
