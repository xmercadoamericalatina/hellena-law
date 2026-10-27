"""Prepara recortes de contexto para revisão visual dos grupos geométricos; não edita normas."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unicodedata
sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image, ImageDraw
from pypdf import PdfReader


def norm(t):
    return ''.join(unicodedata.normalize('NFKC', c).replace('°', 'o')
                   for c in t if not c.isspace() and c not in '*#`')


def grupos(page):
    unique = {}
    for h in page['suspeitas']:
        key = (round(h['y']), norm(h.get('texto', '')))
        if any(abs(y - h['y']) < 2 and n == key[1] for y, n in unique):
            continue
        unique[key] = h
    hits = sorted(unique.values(), key=lambda h: (h['y'], h['x0']))
    result = []
    for h in hits:
        if result and h['y'] - result[-1][-1]['y'] <= 21:
            result[-1].append(h)
        else:
            result.append([h])
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--controle', type=Path, required=True)
    ap.add_argument('--municipio', action='append', required=True)
    ap.add_argument('--saida', type=Path, required=True)
    a = ap.parse_args()
    a.saida.mkdir(parents=True, exist_ok=False)
    rows = [json.loads(l) for l in a.controle.read_text().splitlines()]
    records = []
    for r in rows:
        city = r['documento'].split('/')[2]
        if city not in a.municipio:
            continue
        reader = PdfReader(r['pdf'])
        for page in r['paginas_suspeitas']:
            i = page['pagina']
            stem = a.saida / (city + '-' + str(i))
            subprocess.run(['/opt/homebrew/bin/pdftoppm', '-f', str(i), '-l', str(i), '-scale-to', '1300', '-png', '-singlefile', r['pdf'], str(stem)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            full = Image.open(stem.with_suffix('.png')).convert('RGB')
            scale = full.height / float(reader.pages[i - 1].mediabox.height)
            for j, group in enumerate(grupos(page), 1):
                top = max(0, int((min(h['y'] for h in group) - 45) * scale))
                bottom = min(full.height, int((max(h['y'] for h in group) + 70) * scale))
                crop = full.crop((0, top, full.width, bottom))
                path = a.saida / (city + '-' + str(i) + '-grupo-' + str(j) + '.png')
                crop.save(path)
                records.append({'documento': r['documento'], 'pagina': i, 'grupo': j, 'imagem': str(path),
                                'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                                'texto_normalizado': norm(''.join(h['texto'] for h in group))})
    for k in range(0, len(records), 5):
        selected = records[k:k + 5]
        ims = [Image.open(r['imagem']).convert('RGB') for r in selected]
        width = max(im.width for im in ims)
        sheet = Image.new('RGB', (width, sum(im.height + 36 for im in ims)), 'white')
        draw = ImageDraw.Draw(sheet)
        y = 0
        for r, im in zip(selected, ims):
            draw.text((10, y + 8), r['documento'].split('/')[2] + ' | pagina ' + str(r['pagina']) + ' | grupo ' + str(r['grupo']), fill='black')
            sheet.paste(im, (0, y + 30))
            y += im.height + 36
        sheet.save(a.saida / ('contato-' + str(k // 5 + 1).zfill(3) + '.png'))
    (a.saida / 'grupos.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
    print(json.dumps({'grupos': len(records), 'contatos': (len(records) + 4) // 5}))


if __name__ == '__main__':
    main()
