"""Complemento contextual para atos que legitimamente não se dividem em artigos.

Exige identidade/tipo e inteiro teor já confrontados pelo chamador com a fonte.
Não substitui os gates de anexos, imagens e avisos de material não reproduzido.
"""
import re
from integridade_texto import verificar_integridade_texto, heading, quoted

_AUTORIDADE = re.compile(
    r'(?im)^\s*(?:O|A|OS|AS)\s+(?:GOVERNAD[OA]R[A]?|SECRET[ÁA]RI[OA]|DIRET[OA]R[A]?|'
    r'PRESIDENTE|COMANDANTE|PROCURAD[OA]R[A]?|MESA(?:\s+DIRETORA)?)\b'
    r'[^\n]{0,1400}?\b(?:R\s*E\s*S\s*O\s*L\s*V\s*E(?:M)?|DELIBERA)\b\s*[:.]?\s*'
    r'(?=(?:(?:\d+|[IVXLC]+)\s*\\?[.)\-–—]|aprovar\b|revogar\b|designar\b|conceder\b|constituir\b|autorizar\b|'
    r'nomear\b|criar\b|alterar\b|prorrogar\b|determinar\b|instituir\b|reunir\b|reconhecer\b|'
    r'transformar\b|tornar\b|dispensar\b|estabelecer\b|conferir\b|transferir\b|adotar\b|'
    r'baixar\b|exonerar\b|retificar\b|suspender\b|declarar\b|excluir\b|incluir\b|publicar\b))',
    re.I,
)


def verificar_dispositivo_por_tipo(corpo, tipo, numero):
    motivo, prova = verificar_integridade_texto(corpo)
    if not motivo:
        return motivo, prova
    plano = corpo.replace('*', '').replace('#', '').replace('~~', '')
    comando = _AUTORIDADE.search(plano[:7000])
    if comando:
        anterior = plano[:comando.start()]
        if not heading.search(anterior) and not (quoted.search(anterior) and re.search(r'retific|errata', anterior, re.I)):
            return None, plano[comando.start():comando.end() + 280]
    promulgacao = re.search(r'(?im)^\s*Fa[çc]o saber[^\n]{0,800}?eu promulgo a seguinte (?:Resolu[çc][aã]o|Delibera[çc][aã]o|Lei|Emenda)[^\n]{0,100}:', plano[:7000])
    if promulgacao:
        anterior = plano[:promulgacao.start()]
        restante = plano[promulgacao.end():]
        if (not heading.search(anterior)
                and not (quoted.search(anterior) and re.search(r'retific|errata', anterior, re.I))
                and re.search(r'\bArt(?:igo)?\.?\s*\d', restante[:1800], re.I)):
            return None, plano[promulgacao.start():promulgacao.end() + 350]
    if tipo == 'Súmula':
        epigrafe = re.search(r'S[ÚU]MULAS?\s+DE\s+JURISPRUD[ÊE]NCIA\s*[-–—:]?\s*ENUNCIADO\s+(?:N[º°o.]?\s*)?(\d+)\b', plano[:1200], re.I)
        if epigrafe and str(numero).isdigit() and str(int(epigrafe[1])) == str(int(numero)) and not heading.search(plano[:epigrafe.start()]):
            restante = plano[epigrafe.end():]
            tese = []
            for paragrafo in re.split(r'\n\s*\n', restante):
                p = paragrafo.strip()
                if re.match(r'(?:Refer[êe]ncias|Constitui[çc][aã]o|Lei\b|Decreto\b|Decis[aã]o\b|Processo\b|Este texto n[aã]o substitui)', p, re.I):
                    continue
                if len(re.sub(r'\W', '', p)) >= 70:
                    tese.append(p)
            if tese and re.search(r'publicado no DODF', restante, re.I):
                return None, epigrafe[0] + '\n' + tese[0]
    return motivo, prova
