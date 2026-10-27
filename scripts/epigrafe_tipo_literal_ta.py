"""Identidade literal TA: aceita também o nome completo cadastrado como tipo.

Complementa o parser anterior sem descartar divergências já encontradas. Não
normaliza sufixos institucionais desconhecidos nem altera o título da fonte.
"""
import datetime as dt
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_epigrafes_literais_sapl import analisar as anterior, normal, numero, MESES


def analisar(meta, title):
    legacy = anterior(meta, title)
    article = re.search(r'\bART(?:IGO)?\.?\s*1[º°o.\s]', title, re.I)
    header = normal(title[:min(article.start() if article else 4000, 4000)])
    kind = normal(meta['tipo']).strip()
    found = list(legacy['epigrafes'])
    if kind:
        pattern = r'^\s*' + re.escape(kind) + r'\s+(?:N[º°O.\s]*\s*)?(\d[\d.]*[A-Z]?)\s*(?=[/,]|$|\bDE\b)'
        for m in re.finditer(pattern, header, re.M):
            tail = header[m.end():m.end()+100]
            date = re.match(r'\s*[,.-]?\s*(?:DE\s+)?(\d{1,2})[º°]?\s+(?:DE\s+)?(\w+)\s+DE\s+(\d{4})', tail)
            if not date and not re.match(r'\s*/\s*\d{4}', tail):
                continue
            row = dict(tipo=kind, numero=m[1], numero_normalizado=numero(m[1]), trecho=header[m.start():m.end()+120], tipo_completo_literal=True)
            if date and date[2] in MESES:
                try:
                    row['data_literal'] = dt.date(int(date[3]), MESES[date[2]], int(date[1])).isoformat()
                except ValueError:
                    row['data_literal'] = 'data inválida'
            if not any(r['tipo']==row['tipo'] and r['numero']==row['numero'] and r.get('data_literal')==row.get('data_literal') for r in found):
                found.append(row)
    mismatch = [r for r in found if r['numero_normalizado'] != numero(meta['numero'])]
    date_mismatch = [r for r in found if r.get('data_literal') and meta.get('data') and r['data_literal'] != meta['data']]
    return dict(epigrafes=found, numero_metadado=meta['numero'],
        numero_literal_confirmado=bool(found) and not mismatch,
        data_literal_confirmada=bool(found) and bool(meta.get('data')) and all(r.get('data_literal')==meta['data'] for r in found),
        divergencias=mismatch+date_mismatch,
        limite='Tipo completo aceito somente quando literal e igual ao cadastro oficial; todos os números e datas encontrados devem concordar. Divergências do parser anterior são preservadas. Jurisdição, fonte, anexos, contexto e vigência continuam sujeitos aos demais gates.')
