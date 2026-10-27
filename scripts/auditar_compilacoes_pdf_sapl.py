"""Overlay somente leitura de riscos vetoriais e cores das LOs de listas explícitas."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pdfplumber
from auditar_municipal import metadados
from auditar_tachados_pdf_municipal import analisar_pagina

ROOT = Path(__file__).resolve().parent.parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lista', type=Path, action='append', required=True)
    ap.add_argument('--saida', type=Path, required=True)
    a = ap.parse_args()
    a.saida.mkdir(parents=True, exist_ok=False)
    with (a.saida / 'resultados.jsonl').open('x') as log:
        for rel in dict.fromkeys(p for lista in a.lista for p in lista.read_text().splitlines()):
            raw = (ROOT / rel).read_bytes()
            m = metadados(raw.decode())
            if m.get('tipo') != 'Lei Orgânica':
                continue
            row = {'documento': rel, 'sha256': sha(raw)}
            try:
                u = urlsplit(m['fonte'])
                pdf = ROOT / 'municipais/_fonte/organicas-sapl' / u.hostname / (u.path.rstrip('/').split('/')[-1] + '.bin')
                source = pdf.read_bytes()
                if not source.startswith(b'%PDF'):
                    raise ValueError('Fonte não é PDF; controle específico necessário')
                if sha(source) != m['sha256_fonte']:
                    raise ValueError('SHA fonte diverge')
                row.update({'pdf': str(pdf.relative_to(ROOT)), 'sha256_fonte': sha(source), 'paginas_suspeitas': []})
                colors = Counter()
                colorpages = defaultdict(set)
                with pdfplumber.open(pdf) as doc:
                    row['total_paginas'] = len(doc.pages)
                    for i, page in enumerate(doc.pages, 1):
                        hits = analisar_pagina(page)
                        if hits:
                            row['paginas_suspeitas'].append({'pagina': i, 'suspeitas': hits})
                        for c in page.chars:
                            if c.get('text', '').strip():
                                k = json.dumps(c.get('non_stroking_color'))
                                colors[k] += 1
                                colorpages[k].add(i)
                        page.close()
                row['cores'] = [{'cor': json.loads(k), 'caracteres': n, 'paginas': sorted(colorpages[k])} for k, n in colors.most_common()]
            except Exception as err:
                row['pendencia'] = str(err)
            log.write(json.dumps(row, ensure_ascii=False) + '\n')
            log.flush()
            print(json.dumps({'documento': rel, 'paginas_suspeitas': len(row.get('paginas_suspeitas', [])), 'pendencia': row.get('pendencia')}, ensure_ascii=False), flush=True)
    receipt = {'criterio': __doc__, 'listas': [{'arquivo': str(p), 'sha256': sha(p.read_bytes())} for p in a.lista],
               'script_sha256': sha(Path(__file__).read_bytes()),
               'detector_sha256': sha((ROOT / 'scripts/auditar_tachados_pdf_municipal.py').read_bytes()),
               'resultado_sha256': sha((a.saida / 'resultados.jsonl').read_bytes()),
               'limite': 'Candidatos exigem inspeção visual; ausência de candidatos não certifica vigência integral.'}
    (a.saida / 'manifesto.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
