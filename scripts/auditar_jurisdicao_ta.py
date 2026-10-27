"""Triagem de esfera oficial e cabeçalhos municipais nos corpos TA completos."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_municipal import metadados
from auditar_emissores_sapl import analisar
ROOT = Path(__file__).resolve().parent.parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lista', type=Path, required=True)
    ap.add_argument('--materializados', type=Path, required=True)
    ap.add_argument('--saida', type=Path, required=True)
    a = ap.parse_args()
    a.saida.mkdir(exist_ok=False)
    records = {r.get('path'): r for r in map(json.loads, (a.materializados / 'resultados.jsonl').read_text().splitlines()) if r['aprovado']}
    ibge = ROOT / 'municipais/_indice/ibge-municipios.json'
    names = [r['nome'] for r in json.loads(ibge.read_text())]
    rows = []
    for rel in a.lista.read_text().splitlines():
        b = (ROOT / rel).read_bytes()
        m = metadados(b.decode())
        r = records[rel]
        if sha(b) != r['sha256']:
            raise ValueError('Norma mudou')
        raw = (ROOT / r['prova_norma']['arquivo']).read_bytes()
        if sha(raw) != r['prova_norma']['sha256']:
            raise ValueError('API mudou')
        api = json.loads(raw)
        body = b.decode().split('\n---\n', 1)[1].lstrip('\n').split('\n\n', 1)[1]
        alerts = analisar(body, m['municipio'], names)
        if api.get('esfera_federacao') != 'M':
            alerts.append({'regra': 'esfera_oficial_nao_municipal', 'valor': api.get('esfera_federacao')})
        if re.search(r'\b(?:federal|estadual|distrital)\b', m.get('tipo_na_fonte', ''), re.I):
            alerts.append({'regra': 'tipo_oficial_de_outra_esfera', 'valor': m['tipo_na_fonte']})
        rows.append({'path': rel, 'sha256': sha(b), 'esfera_federacao_api': api.get('esfera_federacao'), 'alertas': alerts})
    (a.saida / 'controle.json').write_text(json.dumps({'criterio': __doc__, 'cadastro_ibge_sha256': sha(ibge.read_bytes()), 'script_sha256': sha(Path(__file__).read_bytes()), 'emissores_script_sha256': sha((ROOT / 'scripts/auditar_emissores_sapl.py').read_bytes()), 'resultados': rows}, ensure_ascii=False, indent=2))
    (a.saida / 'aprovados.paths.txt').write_text(''.join(r['path'] + '\n' for r in rows if not r['alertas']))
    print(json.dumps({'arquivos': len(rows), 'suspeitos': sum(bool(r['alertas']) for r in rows)}))


if __name__ == '__main__':
    main()
