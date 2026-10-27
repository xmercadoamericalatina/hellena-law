"""Confere versões BNP presentes nos MD contra capturas JSON oficiais imutáveis."""
import argparse
import collections
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar import validar
from auditar_municipal import metadados

RAIZ = Path(__file__).resolve().parent.parent


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lista', type=Path, required=True)
    ap.add_argument('--saida', type=Path, required=True)
    a = ap.parse_args()
    capturas = RAIZ / 'jurisprudencia/_fonte/bnp-capturas'
    por_identidade = collections.defaultdict(list)
    consultas = capturas / 'consultas.jsonl'
    for ln in consultas.read_text().splitlines():
        q = json.loads(ln)
        path = capturas / (q['sha256_resposta'] + '.json')
        if digest(path) != q['sha256_resposta']:
            raise ValueError('captura BNP mudou: ' + str(path))
        for r in json.loads(path.read_bytes())['resultados']:
            key = (r['orgao'], r['tipo'], str(r['nr']))
            por_identidade[key].append((r, {'path': str(path.relative_to(RAIZ)), 'sha256': q['sha256_resposta'],
                                          'fonte': q['fonte'], 'filtro': q['filtro']}))
    todas_versoes = {}
    for path in capturas.glob('*.json'):
        sha = digest(path)
        if path.stem != sha:
            raise ValueError('nome/hash da captura BNP divergem: ' + str(path))
        for registro in json.loads(path.read_bytes()).get('resultados', []):
            chave = json.dumps(registro, sort_keys=True, ensure_ascii=False)
            todas_versoes[chave] = {'path': str(path.relative_to(RAIZ)), 'sha256': sha,
                                   'fonte': 'https://pangeabnp.pdpj.jus.br/api/v1/precedentes'}
    tipos = {'Súmula vinculante': 'SV', 'Tema de repercussão geral': 'RG', 'PUIL': 'PUIL', 'Súmula': 'SUM'}
    rows = []
    for rel in a.lista.read_text().splitlines():
        p = RAIZ / rel
        b = p.read_bytes()
        texto = b.decode()
        m = metadados(texto)
        erros, avisos = validar(texto, rel, dt.date.today())
        records = [json.loads(t) for t in re.findall(r'```json\n(.*?)\n```', texto, re.S)]
        key = (m['tribunal'], tipos.get(m['tipo'], m['tipo']), str(m['numero']))
        if not records:
            erros.append('nenhum registro original BNP preservado')
        for r in records:
            if (r['orgao'], r['tipo'], str(r['nr'])) != key:
                erros.append('registro BNP fora da identidade tribunal/tipo/número do documento')
            if json.dumps(r, sort_keys=True, ensure_ascii=False) not in todas_versoes:
                erros.append('versão JSON sem correspondência integral em captura oficial preservada')
        correspondentes = [(r,e) for r,e in por_identidade[key] if r in records]
        if not correspondentes:
            erros.append('nenhuma versão coincide integralmente com captura oficial desta atualização')
        evidencias = list({e['sha256']: e for _,e in correspondentes}.values())
        for r in records:
            evidencia = todas_versoes.get(json.dumps(r, sort_keys=True, ensure_ascii=False))
            if evidencia and not any(e['sha256'] == evidencia['sha256'] for e in evidencias):
                evidencias.append(evidencia)
        rows.append({'path': rel, 'sha256': hashlib.sha256(b).hexdigest(), 'identidade': key,
                     'versoes_preservadas': len(records), 'evidencias': evidencias,
                     'checks': {'formato_identidade_captura_integral': not erros}, 'erros': erros, 'avisos': avisos})
    a.saida.parent.mkdir(parents=True, exist_ok=True)
    with a.saida.open('x') as f:
        json.dump({'auditado_em': dt.datetime.now().isoformat(), 'criterio': 'todas as versões JSON coincidem integralmente com capturas oficiais preservadas; identidade tribunal/tipo/número conferida; ao menos uma versão pertence às consultas de atualização registradas',
                   'lista': str(a.lista), 'sha256_lista': digest(a.lista), 'documentos': rows}, f, ensure_ascii=False, indent=2)
    problemas = sum(bool(r['erros']) for r in rows)
    print(json.dumps({'documentos': len(rows), 'problemas': problemas, 'saida': str(a.saida)}))
    return int(bool(problemas))


if __name__ == '__main__':
    raise SystemExit(main())
