"""Marca trechos gráficos revisados, com ocorrência única e reversibilidade integral.

Exige plano vinculado a hashes de MD e de recortes vistos. Não decide revogação,
não exclui palavras nem altera datas e notas jurídicas da fonte.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parent.parent
NOTE = ('Nota de transcrição: esta edição oficial reúne trechos tachados e não tachados. '
        'Os trechos tachados foram preservados entre rótulos explícitos, com indicação da página da fonte; '
        'as notas de alteração, revogação e efeitos permanecem literais. A marcação reproduz a apresentação '
        'da fonte e não certifica vigência jurídica integral ou atualização posterior.\n\n')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def mapa_normalizado(text):
    chars = []
    positions = []
    for i, c in enumerate(text):
        if c.isspace() or c in '*#`':
            continue
        for ch in unicodedata.normalize('NFKC', c).replace('°', 'o'):
            chars.append(ch)
            positions.append(i)
    return ''.join(chars), positions


def marcar(body, groups):
    norm, mapping = mapa_normalizado(body)
    spans = []
    for group in groups:
        needle = group['texto_normalizado']
        if not needle or norm.count(needle) != 1:
            raise ValueError('Trecho sem ocorrência única: ' + needle[:90])
        i = norm.index(needle)
        spans.append((mapping[i], mapping[i + len(needle) - 1] + 1, group['pagina'], group['grupo']))
    spans.sort()
    if any(a[1] > b[0] for a, b in zip(spans, spans[1:])):
        raise ValueError('Trechos se sobrepõem')
    result = body
    labels = []
    for start, end, page, group in reversed(spans):
        opening = f'⟦INÍCIO DO TRECHO TACHADO NA FONTE, página {page}, grupo {group}⟧'
        closing = '⟦FIM DO TRECHO TACHADO NA FONTE⟧'
        labels.extend([opening, closing])
        result = result[:start] + opening + result[start:end] + closing + result[end:]
    restored = result
    for label in set(labels):
        restored = restored.replace(label, '')
    if restored != body:
        raise ValueError('Corpo anterior não foi recuperado byte a byte')
    return result, spans


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--plano', type=Path, required=True)
    ap.add_argument('--saida', type=Path, required=True)
    ap.add_argument('--aplicar', action='store_true')
    ap.add_argument('--anterior', type=Path, help='Recibo anterior, para revisão controlada a partir de seu backup')
    a = ap.parse_args()
    plan = json.loads(a.plano.read_text())
    previous = {r['documento']: r for r in json.loads(a.anterior.read_text())['documentos']} if a.anterior else {}
    prepared = []
    for row in plan['documentos']:
        path = ROOT / row['documento']
        raw = path.read_bytes()
        if row['documento'] in previous:
            earlier = previous[row['documento']]
            if sha(raw) != earlier['sha256_novo']:
                raise ValueError('Documento mudou após o recibo anterior')
            raw = Path(earlier['backup']).read_bytes()
        if sha(raw) != row['sha256']:
            raise ValueError('MD diverge: ' + str(path))
        for g in row['grupos']:
            if sha((ROOT / g['imagem']).read_bytes()) != g['sha256'] or not g['revisto_visualmente']:
                raise ValueError('Prova visual ausente/divergente')
        cab, rest = raw.decode().split('\n---\n', 1)
        title, body = rest.lstrip('\n').split('\n\n', 1)
        marked, spans = marcar(body, row['grupos'])
        newbody = NOTE + marked
        version = re.search(r'(?m)^versao_texto: (.*)$', cab)
        value = json.loads(version[1]) + '; trechos tachados identificados conforme a fonte, com texto e notas preservados'
        cab = re.sub(r'(?m)^versao_texto:.*$', lambda _: 'versao_texto: ' + json.dumps(value, ensure_ascii=False), cab)
        hashbody = newbody[:-1] if newbody.endswith('\n') else newbody
        cab = re.sub(r'(?m)^sha256_texto:.*$', 'sha256_texto: "' + sha(hashbody.encode()) + '"', cab)
        new = (cab + '\n---\n\n' + title + '\n\n' + newbody).encode()
        prepared.append((row, raw, new, spans))
    a.saida.mkdir(exist_ok=False, parents=True)
    records = []
    for row, raw, new, spans in prepared:
        backup = a.saida / 'backup' / (sha(raw) + '.md')
        backup.parent.mkdir(exist_ok=True)
        backup.write_bytes(raw)
        if a.aplicar:
            (ROOT / row['documento']).write_bytes(new)
        else:
            preview = a.saida / 'preview' / row['documento']
            preview.parent.mkdir(parents=True, exist_ok=True)
            preview.write_bytes(new)
        records.append({'documento': row['documento'], 'sha256_anterior': sha(raw), 'sha256_novo': sha(new),
                        'backup': str(backup), 'trechos': len(spans), 'corpo_anterior_recuperavel_exatamente': True})
    (a.saida / 'normas.paths.txt').write_text(''.join(r['documento'] + '\n' for r in records))
    manifest = {'aplicado': a.aplicar, 'plano': str(a.plano), 'plano_sha256': sha(a.plano.read_bytes()),
                'script_sha256': sha(Path(__file__).read_bytes()), 'documentos': records,
                'limite': 'Identifica somente a marca gráfica revisada; não infere revogação, efeitos ou vigência jurídica integral.'}
    (a.saida / 'manifesto.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(json.dumps({'documentos': len(records), 'trechos': sum(r['trechos'] for r in records), 'aplicado': a.aplicar}))


if __name__ == '__main__':
    main()
