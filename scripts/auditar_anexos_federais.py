"""Reaudita manifests federais sem editar normas, fontes ou listas entregues.

Elementos visuais são examinados em toda a área normativa do HTML, inclusive
fora de tabelas. O gate de suplemento ausente é conservador e não comprova
que todas as possíveis remissões foram resolvidas.
"""
import argparse
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from preparar_lote_decretos_cache import Visivel, fields
from integridade_anexos_decreto import anexo_proprio_ausente

ROOT = Path(__file__).resolve().parent.parent


def auditar(manifestos):
    result = {'criado_em': dt.datetime.now(dt.timezone.utc).isoformat(), 'auditados': 0,
              'manifestos': [], 'elementos_visuais': [], 'anexos_pendentes': [], 'erros': []}
    digest = hashlib.sha256()
    seen = set()
    for manifest in manifestos:
        m = ROOT / manifest
        rawmanifest = m.read_bytes()
        result['manifestos'].append({'path': str(m.relative_to(ROOT)), 'sha256': hashlib.sha256(rawmanifest).hexdigest()})
        document = json.loads(rawmanifest)
        for row in document.get('publicaveis', document.get('registros', [])):
            p = row['path']
            if p in seen:
                continue
            seen.add(p)
            try:
                sourcepath = row.get('fonte_html_cache', p.replace('federal/decretos/', 'federal/_fonte/decretos/').replace('.md', '.html.gz'))
                raw = (ROOT / p).read_bytes()
                source = gzip.decompress((ROOT / sourcepath).read_bytes())
                mdsha = hashlib.sha256(raw).hexdigest()
                sourcesha = hashlib.sha256(source).hexdigest()
                expected = row.get('sha256', row.get('sha256_atual'))
                if expected and expected != mdsha:
                    raise ValueError('Hash do MD diverge do manifesto entregue')
                if row.get('sha256_fonte_html') != sourcesha:
                    raise ValueError('Hash da fonte diverge do manifesto entregue')
                parser = Visivel()
                parser.feed(source.decode('utf8'))
                meta, _, body = fields(raw.decode())
                record = {'path': p, 'urn': meta.get('urn'), 'fonte': meta.get('fonte'),
                          'sha256': mdsha, 'fonte_html_cache': sourcepath,
                          'sha256_fonte_html': sourcesha, 'manifesto': str(m.relative_to(ROOT))}
                if parser.visual:
                    result['elementos_visuais'].append(dict(record, elementos=parser.visual))
                evidence = anexo_proprio_ausente(body, parser)
                if evidence:
                    result['anexos_pendentes'].append(dict(record, evidencia=evidence))
                digest.update(json.dumps([p, mdsha, sourcesha], ensure_ascii=False).encode() + b'\n')
                result['auditados'] += 1
            except Exception as error:
                result['erros'].append({'path': p, 'erro': str(error)})
        print(manifest, result['auditados'], 'anexos pendentes', len(result['anexos_pendentes']), flush=True)
    result['sha256_sequencia_paths_md_html'] = digest.hexdigest()
    result['limite'] = 'Comprova revisão visual de todo HTML e registra casos conservadores de suplemento próprio ausente; não prova cobertura de toda remissão possível, vigência ou integralidade externa.'
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifestos', nargs='+', required=True)
    parser.add_argument('--saida', required=True)
    args = parser.parse_args()
    target = ROOT / args.saida
    if target.exists():
        parser.error('Saída já existe; auditorias entregues são imutáveis')
    result = auditar(args.manifestos)
    with target.open('x') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print('FIM', result['auditados'], 'erros', len(result['erros']), flush=True)
