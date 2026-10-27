"""Materializa apenas TAs aprovados com prova API original e sem norma existente.

Mantém HTML integral e histórico na fonte; não substitui versões no acervo.
Todo caminho criado e sua dependência ficam enumerados no recibo do lote.
Versão 3: identidade literal com rótulo institucional da fonte; dia derivado da captura original, com conversão America/Recife para
timestamps com offset e preservação literal dos timestamps sem fuso informado.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_textos_articulados_sapl_v3 import conferir
from auditar_epigrafes_literais_sapl import numero, normal
from auditar_municipal import metadados
from comum import normalizar_chave, slugify, yaml_str
import datetime as dt
from zoneinfo import ZoneInfo
ROOT = Path(__file__).resolve().parent.parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def dia_captura(timestamp):
    original = dt.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    if original.tzinfo is None:
        return original.date().isoformat(), 'não informado no timestamp original; dia literal preservado'
    return original.astimezone(ZoneInfo('America/Recife')).date().isoformat(), 'America/Recife'


def capture_proof(path, url=None):
    b = path.read_bytes()
    meta = path.with_suffix('.meta.json')
    info = json.loads(meta.read_text())
    if sha(b) != info['sha256'] or info['status'] != 200 or (url and info['url'] != url):
        raise ValueError('Prova de captura divergente')
    return json.loads(b), {'arquivo': str(path.relative_to(ROOT)), 'sha256': sha(b), 'metadata': str(meta.relative_to(ROOT)), 'sha256_metadata': sha(meta.read_bytes()), 'url': info['url']}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--gates', type=Path, required=True)
    ap.add_argument('--saida', type=Path, required=True)
    ap.add_argument('--referencia', type=dt.date.fromisoformat, default=dt.date.today())
    a = ap.parse_args()
    a.saida = a.saida.resolve()
    a.saida.mkdir(exist_ok=False)
    gate_manifest = json.loads((a.gates / 'manifesto.json').read_text())
    for proof in gate_manifest['fontes']:
        if sha((ROOT / proof['arquivo']).read_bytes()) != proof['sha256']:
            raise ValueError('Snapshot dos gates mudou')
    candidates = [r for r in map(json.loads, (a.gates / 'resultados.jsonl').read_text().splitlines()) if r['aprovado_nestes_gates']]
    ibge_path = ROOT / 'municipais/_indice/ibge-municipios.json'
    ibge = {str(r['id']): r for r in json.loads(ibge_path.read_text())}
    hosts = sorted({r['host'] for r in candidates})
    ta_index = {}
    houses = {}
    kinds = {}
    annex = {}
    evidence = []
    existing = {}
    existing_bodies = {}
    for host in hosts:
        cache = ROOT / 'municipais/_fonte/texto-articulado-sapl' / host
        ta_index[host] = {}
        for meta in cache.glob('*.meta.json'):
            info = json.loads(meta.read_text())
            if '/api/compilacao/textoarticulado/?' not in info['url']:
                continue
            rawpath = meta.with_name(meta.name.replace('.meta.json', '.json'))
            data, proof = capture_proof(rawpath)
            for record in data['results']:
                ta_index[host][record['id']] = record, proof
        url = f'https://{host}/api/base/casalegislativa/'
        data, proof = capture_proof(cache / (sha(url.encode()) + '.json'), url)
        if len(data['results']) != 1:
            raise ValueError('Casa legislativa ambígua')
        houses[host] = data['results'][0], proof
        kinds[host] = {r['id']: r for r in json.loads((a.gates / (host + '.tipos.json')).read_text())['results']}
        annex[host] = json.loads((a.gates / (host + '.anexos.json')).read_text())
        actual = []
        for item in annex[host]['evidencias']:
            b = (ROOT / item['arquivo']).read_bytes()
            if sha(b) != item['sha256'] or item['status'] != 200:
                raise ValueError('Prova da relação de anexos mudou')
            actual.extend(json.loads(b)['results'])
        if actual != annex[host]['anexos'] or len(actual) != annex[host]['total']:
            raise ValueError('Relação de anexos difere das páginas originais')
        house = houses[host][0]
        cityrows = [c for c in ibge.values() if normalizar_chave(c['nome']) == normalizar_chave(house['municipio']) and c['regiao-imediata']['regiao-intermediaria']['UF']['sigla'] == house['uf']]
        if len(cityrows) != 1:
            raise ValueError('Identidade IBGE ambígua')
        city = cityrows[0]
        municipal_folder = ROOT / 'municipais' / house['uf'] / slugify(normalizar_chave(city['nome']))[:60]
        for p in municipal_folder.glob('**/*.md'):
            text = p.read_text()
            m = metadados(text)
            rel = str(p.relative_to(ROOT))
            key = (str(city['id']), normal(m.get('tipo', '')), numero(m.get('numero', '')), m.get('data', '')[:4])
            existing.setdefault(('identidade', key), []).append(rel)
            existing.setdefault(('fonte', m.get('fonte', '').rstrip('/')), []).append(rel)
            if '\n---\n' in text:
                body = text.split('\n---\n', 1)[1].lstrip('\n').split('\n\n', 1)[-1]
                existing_bodies.setdefault((host, sha(' '.join(re.findall(r'\w+', body)).encode())), []).append(rel)
    rows = []
    for candidate in candidates:
        row = {'host': candidate['host'], 'norma_id': candidate['norma_id'], 'ta_id': candidate['ta_id'], 'aprovado': False}
        try:
            host = candidate['host']
            record, proof = ta_index[host][candidate['ta_id']]
            if record != candidate['metadado_ta'] or record['privacidade'] not in {0, 69}:
                raise ValueError('Registro TA público diverge da página original da API')
            details = conferir(candidate, kinds[host], annex[host], a.referencia)
            norm = candidate['metadado_norma']
            city = ibge[candidate['codigo_ibge']]
            house, houseproof = houses[host]
            uf = city['regiao-imediata']['regiao-intermediaria']['UF']['sigla']
            if normalizar_chave(city['nome']) != normalizar_chave(house['municipio']) or uf != house['uf']:
                raise ValueError('Casa e IBGE divergem')
            url = f'https://{host}/norma/{norm["id"]}'
            key = (str(city['id']), normal(details['tipo_canonico']), numero(norm['numero']), norm['data'][:4])
            body = (ROOT / candidate['transcricao']).read_text()
            bodykey = (host, sha(' '.join(re.findall(r'\w+', body)).encode()))
            collisions = existing.get(('identidade', key), []) + existing.get(('fonte', url), []) + existing_bodies.get(bodykey, [])
            if collisions:
                row['colisoes'] = sorted(set(collisions))
                raise ValueError('Norma ou corpo já existente; conciliar versões antes de substituir')
            name = details['categoria'] + '-' + slugify(norm['numero']) + '-' + str(norm['ano']) + '-sapl-' + str(norm['id']) + '.md'
            target = ROOT / 'municipais' / uf / slugify(normalizar_chave(city['nome']))[:60] / details['categoria'] / str(norm['ano']) / name
            if target.exists():
                raise ValueError('Destino já existe')
            cuts = ', '.join(details['cortes_de_vigencia_declarados']) or 'corte de atualização não declarado'
            captured = candidate['prova_frontend']['capturado_em']
            capture_day, capture_zone = dia_captura(captured)
            version = ('versão padrão pública do texto articulado oficial, capturada em ' + dt.date.fromisoformat(capture_day).strftime('%d/%m/%Y') + '; ' + cuts + '; dispositivos desativados excluídos, marcadores de revogação e notas preservados; HTML integral com histórico mantido; sem certificação de vigência integral')
            meta = {'titulo': details['titulo_literal'], 'tipo': details['tipo_canonico'], 'tipo_na_fonte': details['tipo_oficial'], 'numero': str(norm['numero']), 'data': norm['data'], 'municipio': city['nome'], 'uf': uf, 'codigo_ibge': str(city['id']), 'origem_data': 'número e data confirmados na epígrafe literal do HTML oficial e nas APIs de norma e texto articulado', 'versao_texto': version, 'fonte': url, 'fonte_texto': candidate['prova_frontend']['url_final'], 'sha256_fonte': candidate['prova_frontend']['sha256'], 'sha256_texto': sha(body.encode()), 'capturado_em_fonte': captured, 'fuso_dia_captura': capture_zone, 'baixado_em': capture_day}
            result = '\n'.join(['---'] + [k + ': ' + yaml_str(v) for k, v in meta.items()] + ['revogada: null', '---', '', '# ' + meta['titulo'], '', body, ''])
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('x') as f:
                f.write(result)
            rel = str(target.relative_to(ROOT))
            row.update({'aprovado': True, 'path': rel, 'sha256': sha(target.read_bytes()), 'bytes': target.stat().st_size, 'gates': details, 'prova_ta': proof, 'prova_casa': houseproof, 'prova_norma': candidate['prova_norma'], 'prova_frontend': candidate['prova_frontend'], 'transcricao': candidate['transcricao']})
            existing.setdefault(('identidade', key), []).append(rel)
            existing.setdefault(('fonte', url), []).append(rel)
            existing_bodies.setdefault(bodykey, []).append(rel)
        except Exception as err:
            row['pendencia'] = str(err)
        rows.append(row)
    (a.saida / 'resultados.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
    (a.saida / 'normas.paths.txt').write_text(''.join(r['path'] + '\n' for r in rows if r['aprovado']))
    receipt = {'criterio': __doc__, 'candidatos': len(rows), 'normas': sum(r['aprovado'] for r in rows), 'retidos': sum(not r['aprovado'] for r in rows), 'script_sha256': sha(Path(__file__).read_bytes()), 'ibge_sha256': sha(ibge_path.read_bytes()), 'gates_sha256': sha((a.gates / 'manifesto.json').read_bytes()), 'colisoes': 'Compara URL oficial, IBGE/tipo/número/ano com sufixos e corpo textual contra todos os documentos locais dos dois municípios e contra os candidatos anteriores deste lote. Qualquer versão existente exige conciliação, sem substituição automática.'}
    (a.saida / 'manifesto.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == '__main__':
    main()
