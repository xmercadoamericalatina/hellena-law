"""Candidato privado: corrige só o delimitador forte do TA 9633 / norma 29531.

O arquivo normativo e os pacotes anteriores ficam intactos. O candidato precisa
substituir a preimagem por operação de publicação separada após revisão.
"""
import hashlib
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_commonmark_ta import comparar
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
TARGET = 'municipais/RO/porto-velho/decretos/2026/decretos-22256-2026-sapl-29531.md'
PREIMAGE = 'af15d78bb335acb0d119e2e81d037e7296dc20f02d232907e9d4487557155d09'
OLD = '**Sônia Maria dos Santos Pereira -**Suplente'
NEW = '**Sônia Maria dos Santos Pereira** -Suplente'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    original = (ROOT / TARGET).read_bytes()
    if sha(original) != PREIMAGE:
        raise ValueError('Preimagem mudou')
    text = original.decode()
    if text.count(OLD) != 1:
        raise ValueError('Delimitador esperado não é único')
    body = text.split('\n---\n', 1)[1].lstrip('\n').split('\n\n', 1)[1][:-1]
    before = sha(body.encode())
    candidate_body = body.replace(OLD, NEW, 1)
    after = sha(candidate_body.encode())
    candidate = text.replace(OLD, NEW, 1).replace('sha256_texto: "'+before+'"', 'sha256_texto: "'+after+'"', 1)
    if candidate.replace(NEW, OLD, 1).replace('sha256_texto: "'+after+'"', 'sha256_texto: "'+before+'"', 1) != text:
        raise ValueError('Reversão integral não confere')
    records = list(map(json.loads, (ROOT/'municipais/_lotes/20261020-textos-articulados-materializados-0002/resultados.jsonl').read_text().splitlines()))
    row = next(r for r in records if r.get('path') == TARGET)
    source = (ROOT/row['prova_frontend']['arquivo']).read_bytes()
    if sha(source) != row['prova_frontend']['sha256']:
        raise ValueError('Fonte mudou')
    proof = comparar(source.decode(), candidate_body)
    if not proof['aprovado']:
        raise ValueError('Replay independente ainda diverge')
    if comparar(source.decode(), body)['aprovado']:
        raise ValueError('Preimagem não reproduziu o defeito')
    out = ROOT/'municipais/_lotes/20261020-reparo-commonmark-ta29531'
    out.mkdir(exist_ok=False)
    (out/'preimagem.md').write_bytes(original)
    (out/'candidato.md').write_text(candidate)
    (out/'replay.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2)+'\n')
    rendered = MarkdownIt('commonmark', {'html': True}).enable('table').enable('strikethrough').render(candidate_body)
    (out/'renderizacao.html').write_text(rendered)
    manifest = dict(destino=TARGET, sha256_preimagem=PREIMAGE, sha256_candidato=sha(candidate.encode()),
                    fonte=row['prova_frontend'], alteracao=dict(antes=OLD, depois=NEW,
                    sha256_texto_antes=before, sha256_texto_depois=after),
                    validacao='Preimagem reproduz os asteriscos literais. Candidato passa em comparação sequencial de todos os caracteres não brancos contra o HTML ativo oficial após replay CommonMark/GFM independente. Reversão do delimitador e do hash recompõe a preimagem byte a byte.',
                    limite='Candidato privado; a norma no destino e os pacotes 107/145 e overlay 251 não foram alterados.',
                    codigo_sha256=sha(Path(__file__).read_bytes()))
    (out/'manifesto.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == '__main__':
    main()
