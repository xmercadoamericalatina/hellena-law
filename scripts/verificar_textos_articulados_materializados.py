"""Verifica sem escrever normas: corpo integral, fonte e contexto do TA materializado."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_municipal import metadados
from auditar_contexto_completo_ta import ContextoCompleto
from converter_organica_fortaleza import converter
ROOT = Path(__file__).resolve().parent.parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lista', type=Path, required=True)
    ap.add_argument('--materializados', type=Path, required=True)
    ap.add_argument('--saida', type=Path, required=True)
    a = ap.parse_args()
    records = {r.get('path'): r for r in map(json.loads, (a.materializados / 'resultados.jsonl').read_text().splitlines()) if r['aprovado']}
    rows = []
    for rel in a.lista.read_text().splitlines():
        b = (ROOT / rel).read_bytes()
        row = {'path': rel, 'sha256': sha(b), 'aprovado': False}
        try:
            r = records[rel]
            if sha(b) != r['sha256']:
                raise ValueError('Norma mudou')
            source = (ROOT / r['prova_frontend']['arquivo']).read_bytes()
            if sha(source) != r['prova_frontend']['sha256']:
                raise ValueError('Fonte mudou')
            body = b.decode().split('\n---\n', 1)[1].lstrip('\n').split('\n\n', 1)[1][:-1]
            expected, parsed = converter(source.decode())
            if body != expected or sha(body.encode()) != metadados(b.decode())['sha256_texto']:
                raise ValueError('Corpo ou hash diverge da seleção oficial de dispositivos')
            context = ContextoCompleto()
            context.feed(source.decode())
            if context.fora or context.media or context.cp_encontrados != 1 or context.dispositivos_fora_da_area or context.ativos_em_ancestral_historico:
                raise ValueError('Contexto fora dos dispositivos ainda pendente')
            row.update({'aprovado': True, 'dispositivos_ativos': len(parsed.ativos), 'historicos': len(parsed.historicos), 'sha256_fonte': sha(source)})
        except Exception as err:
            row['erro'] = str(err)
        rows.append(row)
    result = {'arquivos': len(rows), 'aprovados': sum(r['aprovado'] for r in rows), 'problemas': sum(not r['aprovado'] for r in rows), 'script_sha256': sha(Path(__file__).read_bytes()), 'resultados': rows}
    with a.saida.open('x') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps({'arquivos': result['arquivos'], 'aprovados': result['aprovados'], 'problemas': result['problemas']}))
    if result['problemas']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
