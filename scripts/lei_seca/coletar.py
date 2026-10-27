"""Descoberta federal contínua, SAPL e prioridades, sem jurisprudência."""
import datetime as dt
import re
import urllib.parse

from core import LegalHTML, allowed_kind, decode, digest, validate_url

# Prefixos da API oficial, sem jurisprudência, pareceres ou proposições.
TYPES = {
    'LEI': 1808, 'LCP': 1967, 'LDL': 1962, 'LCT': 1937, 'DEL': 1937,
    'EMC': 1969, 'EMR': 1994, 'DEC': 1889, 'DLG': 1891, 'DPL': 1889,
    'MPV': 1988, 'RSF': 1826, 'RCN': 1891, 'RRC': 1993,
}
URN = {
    'LEI': ('federal', 'lei', 'Lei'), 'LCP': ('federal', 'lei.complementar', 'Lei Complementar'),
    'LDL': ('federal', 'lei.delegada', 'Lei Delegada'),
    'LCT': ('federal', 'lei.constitucional', 'Lei Constitucional'),
    'DEL': ('federal', 'decreto.lei', 'Decreto-Lei'),
    'EMC': ('federal', 'emenda.constitucional', 'Emenda Constitucional'),
    'EMR': ('federal', 'emenda.constitucional.revisao', 'Emenda Constitucional'),
    'DEC': ('federal', 'decreto', 'Decreto'),
    'DLG': ('federal', 'decreto.legislativo', 'Decreto Legislativo'),
    'DPL': ('federal', 'decreto.legislativo', 'Decreto Legislativo'),
    'MPV': ('federal', 'medida.provisoria', 'Medida Provisória'),
    'RSF': ('senado.federal', 'resolucao', 'Resolução do Senado Federal'),
    'RCN': ('congresso.nacional', 'resolucao', 'Resolução do Congresso Nacional'),
    'RRC': ('congresso.nacional', 'resolucao', 'Resolução do Congresso Nacional'),
}


def many(value):
    return value if isinstance(value, list) else [value] if value is not None else []


def senate_docs(response):
    if not isinstance(response, dict) or 'ListaDocumento' not in response:
        raise ValueError('Resposta não contém ListaDocumento; não tratar erro como lista vazia')
    docs = response['ListaDocumento'].get('documentos') or {}
    return many(docs.get('documento'))


def senate_entry(doc):
    full_type = doc['tipo']
    prefix = full_type.split('-')[0]
    if prefix not in URN:
        raise ValueError('Tipo fora da lista legislativa: ' + full_type)
    authority, urn_type, kind = URN[prefix]
    date = dt.datetime.strptime(doc['dataassinatura'], '%d/%m/%Y').date().isoformat()
    number = str(doc.get('numero', ''))
    if doc.get('complemento'):
        number += '-' + str(doc['complemento']).upper()
    if doc.get('reedicao'):
        number += '-' + str(doc['reedicao'])
    urn_number = 'seq-sf-' + str(doc['sequencia']) if full_type.endswith('-sn') else number
    urn = f'urn:lex:br:{authority}:{urn_type}:{date};{urn_number.lower()}'
    return {'id': 'senado-' + str(int(doc['id'])), 'conector': 'senado', 'tipo': kind,
            'titulo': doc.get('normaNome', doc.get('norma', kind)).strip(),
            'numero': number if not full_type.endswith('-sn') else '', 'data': date,
            'urn': urn, 'id_senado': str(doc['id']), 'esfera': 'federal',
            'fonte': 'https://normas.leg.br/?urn=' + urn}


def discover_senate(net, state, budget=6, historic=2):
    year = dt.date.today().year
    # Recente e histórico têm cursores separados: novas normas não esperam a carga antiga.
    recent_jobs = [(kind, y) for y in (year, year - 1) for kind in TYPES]
    past_jobs = [(kind, y) for kind, start in TYPES.items() for y in range(year - 2, start - 1, -1)]
    found, events = [], []
    for label, jobs, limit in [('recente', recent_jobs, budget), ('historico', past_jobs, historic)]:
        cursor = state.setdefault('indices', {}).get(label, 0) % len(jobs)
        for _ in range(limit):
            kind, y = jobs[cursor]
            url = 'https://legis.senado.leg.br/dadosabertos/legislacao/lista.json?' + urllib.parse.urlencode({'tipo': kind, 'ano': y})
            try:
                docs = senate_docs(net.json(url))
                entries = [senate_entry(d) for d in docs]
                found.extend(entries)
                events.append({'fonte': url, 'status': 'ok', 'encontrados': len(entries)})
                cursor = (cursor + 1) % len(jobs)
                state['indices'][label] = cursor
            except Exception as exc:
                # Não avança sobre erro: próximo ciclo tentará a mesma fatia.
                events.append({'fonte': url, 'status': 'erro', 'erro': str(exc)})
                break
    return found, events


def resolve_senate(net, entry):
    def meta_for(urn):
        url = 'https://normas.leg.br/api/public/normas?' + urllib.parse.urlencode({'urn': urn, 'tipo_documento': 'maior-detalhe'})
        meta = net.json(url)
        if meta.get('legislationIdentifier') != urn:
            raise ValueError('URN oficial divergente')
        return meta
    try:
        meta = meta_for(entry['urn'])
    except (ValueError, KeyError):
        detail = net.json('https://legis.senado.leg.br/dadosabertos/legislacao/' + entry['id_senado'] + '.json')
        docs = many(detail['DetalheDocumento']['documentos']['documento'])
        link = docs[0]['identificacao'].get('urlDocumento', '')
        urn = urllib.parse.parse_qs(urllib.parse.urlsplit(link).query).get('urn', [None])[0]
        if not urn:
            raise ValueError('Detalhe sem URN oficial verificável')
        meta = meta_for(urn)
        entry = {**entry, 'urn': urn, 'fonte': 'https://normas.leg.br/?urn=' + urn}
    encodings = [e for e in many(meta.get('encoding')) if isinstance(e, dict) and e.get('contentUrl')]
    encodings.sort(key=lambda e: ({'Current': 0, 'Original': 1}.get(e.get('version'), 2),
                                  'html' not in (e.get('encodingFormat') or '').lower()))
    if not encodings:
        raise ValueError('Fonte sem texto integral')
    enc = encodings[0]
    url = validate_url(enc['contentUrl'].replace('/api/binario/', '/api/public/binario/'))
    data, ct, final_url = net.get(url)
    return {**entry, 'versao_texto': enc.get('version', 'nao_informada'),
            'forca_legal_fonte': meta.get('legislationLegalForce'),
            'sha256_metadados_fonte': digest(__import__('json').dumps(meta, sort_keys=True, ensure_ascii=False).encode('utf-8'))}, data, ct, final_url


def resolve_direct(net, entry):
    data, ct, url = net.get(entry['url'])
    if not data.startswith(b'%PDF'):
        parser = LegalHTML()
        parser.feed(decode(data, ct))
        # Segue apenas um link explicitamente identificado como compilação da mesma norma.
        for href, label in parser.links:
            if 'texto compilado' in label.lower() or 'texto consolidado' in label.lower():
                target = urllib.parse.urljoin(url, href)
                if urllib.parse.urlsplit(target).hostname == urllib.parse.urlsplit(url).hostname:
                    data, ct, url = net.get(target)
                    break
    return entry, data, ct, url


def discover_portal(net, page):
    data, ct, url = net.get(page['url'])
    parser = LegalHTML()
    parser.feed(decode(data, ct))
    found = []
    for href, label in parser.links:
        target = urllib.parse.urljoin(url, href)
        u = urllib.parse.urlsplit(target)
        # Página informativa é apenas índice: nunca vira texto normativo.
        if not (u.hostname or '').endswith('.planalto.gov.br'):
            continue
        path = u.path.lower()
        m = re.search(r'/(?:lcp|l|del|d|emc)(\d+)(?:compilad[ao])?\.htm$', path)
        if not m:
            continue
        if '/leis/lcp/' in path:
            kind = 'Lei Complementar'
        elif '/constituicao/emendas/' in path:
            kind = 'Emenda Constitucional'
        elif '/decreto-lei/' in path:
            kind = 'Decreto-Lei'
        elif '/decreto/' in path:
            kind = 'Decreto'
        elif '/lei/' in path or '/leis/' in path:
            kind = 'Lei'
        else:
            continue
        # ID canônico por caminho, compilado e original são a mesma norma.
        normalized = re.sub(r'compilad[ao](?=\.htm$)', '', path)
        found.append({'id': 'planalto-' + digest(normalized.encode())[:24], 'conector': 'direto',
                      'tipo': kind, 'numero': m.group(1), 'titulo': label.strip() or kind + ' nº ' + m.group(1),
                      'url': urllib.parse.urlunsplit((u.scheme, u.netloc, u.path, '', '')),
                      'fonte_indice': page['url'], 'esfera': 'federal', 'tema': page['tema']})
    return found


def sapl_next(response):
    pagination = response.get('pagination')
    if isinstance(pagination, dict):
        return bool(pagination.get('next_page'))
    return bool(response.get('next'))


def discover_sapl(net, source, state):
    sid, base = source['id'], source['url'].rstrip('/')
    cursor = state.setdefault('sapl', {}).setdefault(sid, {'page': 1})
    if not cursor.get('types'):
        kinds, page = {}, 1
        while True:
            result = net.json(base + '/api/norma/tiponormajuridica/?page_size=100&page=' + str(page))
            if not isinstance(result.get('results'), list):
                raise ValueError('API SAPL sem results')
            kinds.update({str(t['id']): t['descricao'] for t in result['results'] if allowed_kind(t['descricao'])})
            if not sapl_next(result):
                break
            page += 1
            if page > 20:
                raise ValueError('Paginação de tipos acima do limite')
        if not kinds:
            raise ValueError('Nenhum tipo normativo aprovado na fonte')
        cursor['types'] = kinds
    page = cursor['page']
    result = net.json(base + '/api/norma/normajuridica/?page_size=100&page=' + str(page))
    if not isinstance(result.get('results'), list):
        raise ValueError('API SAPL sem results')
    found = []
    for doc in result['results']:
        kind = cursor['types'].get(str(doc.get('tipo')))
        if not kind:
            continue
        target = doc.get('texto_integral')
        if not target:
            continue
        target = validate_url(urllib.parse.urljoin(base + '/', target))
        ident = sid + '-' + str(int(doc['id']))
        found.append({'id': ident, 'conector': 'direto', 'tipo': kind,
                      'titulo': f"{kind} nº {doc.get('numero', '')}/{doc.get('ano', '')}",
                      'numero': str(doc.get('numero', '')), 'data': doc.get('data', ''),
                      'url': target, 'fonte': base + '/norma/' + str(doc['id']),
                      'esfera': source['esfera'], 'uf': source['uf'], 'municipio': source.get('municipio')})
    cursor['page'] = page + 1 if sapl_next(result) else 1
    if cursor['page'] == 1:
        # Revalidar tipos no próximo censo, inclusive quando o portal cria nova categoria.
        cursor.pop('types', None)
    return found
