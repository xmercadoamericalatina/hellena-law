"""Prepara seis candidatos privados com reparo só de delimitadores Markdown.

Nunca altera o destino municipal. Exige preimagem, fonte e replay independente;
promoção posterior deve conferir os hashes anterior e novo de cada candidato.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_commonmark_ta_v2 import comparar
from auditar_emissores_sapl import analisar, normal
from auditar_municipal import metadados
ROOT = Path(__file__).resolve().parent.parent
CASES = [
 ('0007','municipais/RR/boa-vista/leis-ordinarias/1974/leis-ordinarias-20-1974-sapl-807.md','negrito_itálico'),
 ('0007','municipais/RS/erechim/leis-ordinarias/2004/leis-ordinarias-3795-2004-sapl-3754.md','hífens'),
 ('0008','municipais/RS/erechim/leis-ordinarias/1997/leis-ordinarias-2995-1997-sapl-2957.md','hífens'),
 ('0008','municipais/RS/erechim/leis-ordinarias/1997/leis-ordinarias-2896-1997-sapl-2860.md','hífens'),
 ('0008','municipais/RO/porto-velho/decretos/2024/decretos-20.302-2024-sapl-26939.md','negrito_travessão'),
 ('0011','municipais/RO/porto-velho/decretos/2023/decretos-19.456-2023-sapl-25861.md','negrito_travessão'),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def reparar(body, mode):
    if mode == 'hífens':
        result, n = re.subn(r'(?m)^([ \t]*)([-+])(?=\s)', lambda m: m[1] + '\\' + m[2], body)
    elif mode == 'negrito_travessão':
        result, n = re.subn(r'\*\*([^*\n]+?)([ \t]*[–—-])\*\*', lambda m: '**' + m[1] + '**' + m[2], body)
    elif mode == 'negrito_itálico':
        old = next(l for l in body.splitlines() if l.startswith('***O SR. JÚLIO') and l.endswith('seguinte*'))
        if body.count(old) != 1:
            raise ValueError('Trecho ambíguo')
        result, n = body.replace(old, old + '**'), 1
    else:
        raise ValueError('Modo não autorizado')
    if not n or result == body:
        raise ValueError('Reparo vazio')
    return result, n


def preparar(case, preimage=None):
    batch, target, mode = case
    raw = (ROOT/target).read_bytes() if preimage is None else preimage
    meta = metadados(raw.decode())
    mat = ROOT/'municipais/_lotes'/('20261021-textos-articulados-materializados-' + batch)
    rows = [json.loads(l) for l in (mat/'resultados.jsonl').read_text().splitlines()]
    row = next(r for r in rows if r.get('path') == target and r.get('aprovado'))
    if sha(raw) != row['sha256']:
        raise ValueError('Preimagem mudou: ' + target)
    source = (ROOT/row['prova_frontend']['arquivo']).read_bytes()
    if sha(source) != row['prova_frontend']['sha256']:
        raise ValueError('Fonte mudou')
    prefix, rest = raw.decode().split('\n---\n', 1)
    title, body = rest.lstrip('\n').split('\n\n', 1)
    if body.endswith('\n'):
        body = body[:-1]
    if sha(body.encode()) != meta['sha256_texto']:
        raise ValueError('Hash anterior do corpo diverge')
    before = comparar(source.decode(), body)
    if before['aprovado']:
        raise ValueError('Caso já passa; reparo desnecessário')
    fixed, changes = reparar(body, mode)
    replay = comparar(source.decode(), fixed)
    if not replay['aprovado']:
        raise ValueError('Reparo não conserva a fonte: ' + str(replay.get('contexto')))
    for key in ('prova_norma', 'prova_casa', 'prova_ta'):
        if sha((ROOT/row[key]['arquivo']).read_bytes()) != row[key]['sha256']:
            raise ValueError('Prova API mudou: ' + key)
    norma = json.loads((ROOT/row['prova_norma']['arquivo']).read_text())
    if norma.get('esfera_federacao') != 'M' or norma.get('observacao'):
        raise ValueError('API não confirma esfera M/contexto vazio')
    ibge = json.loads((ROOT/'municipais/_indice/ibge-municipios.json').read_text())
    names = [r['nome'] for r in ibge]
    casa = json.loads((ROOT/row['prova_casa']['arquivo']).read_text())['results']
    if len(casa) != 1 or normal(casa[0]['municipio']) != normal(meta['municipio']) or casa[0]['uf'] != meta['uf']:
        raise ValueError('Casa municipal não corresponde ao destino')
    city = next(r for r in ibge if str(r['id']) == str(meta['codigo_ibge']))
    if normal(city['nome']) != normal(meta['municipio']) or city['regiao-imediata']['regiao-intermediaria']['UF']['sigla'] != meta['uf']:
        raise ValueError('IBGE diverge')
    if re.search(r'\b(?:federal|estadual|distrital)\b', meta.get('tipo_na_fonte', ''), re.I):
        raise ValueError('Tipo de outra esfera')
    alerts = analisar(fixed, meta['municipio'], names)
    if alerts:
        raise ValueError('Emissor exige revisão: ' + str(alerts))
    prefix, n = re.subn(r'(?m)^sha256_texto:.*$', 'sha256_texto: "' + sha(fixed.encode()) + '"', prefix)
    if n != 1:
        raise ValueError('Metadado de hash ambíguo')
    new = (prefix + '\n---\n\n' + title + '\n\n' + fixed + '\n').encode()
    return raw, new, dict(destino=target, sha256_anterior=sha(raw), sha256_novo=sha(new), modo=mode,
        delimitadores_reparados=changes, replay_anterior=before, replay=replay, origem_materializada=row,
        criterio='Somente escape de marcadores de lista, reposicionamento do fechamento de negrito antes do travessão ou fechamento de negrito/itálico. Palavras, pontuação, sinais, numeração e notas confrontados integralmente com a área ativa oficial. Destino municipal não alterado.')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--saida', type=Path, required=True)
    a = ap.parse_args()
    a.saida.mkdir(exist_ok=False)
    results = []
    for case in CASES:
        raw, new, record = preparar(case)
        stem = sha(case[1].encode())
        before = a.saida/(stem + '.anterior.md')
        candidate = a.saida/(stem + '.candidato.md')
        before.write_bytes(raw)
        candidate.write_bytes(new)
        record.update(backup=str(before), candidato=str(candidate))
        results.append(record)
    (a.saida/'promocoes.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(candidatos=len(results), canonicos_alterados=0)))


if __name__ == '__main__':
    main()
