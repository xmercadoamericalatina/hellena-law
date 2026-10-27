"""Transcreve o PDF oficial de Aracaju, preservando passagens tachadas e notas.

Exige a revisão visual congelada de 73 passagens em 45 páginas. A marcação é
contextual, não decide revogação nem exclui caracteres. Preserva todas as páginas,
fólios, alíneas, valores e a grade de nomes/cargos da página final.
"""
import collections
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import yaml_str
from marcar_tachados_sapl_revisados import marcar

ROOT = Path(__file__).resolve().parent.parent
PDF = Path('municipais/_fonte/capitais/aracaju/lei-organica-atualizada.pdf')
PDF_SHA = '5126f91b91aa3d4d680d8282b2d4f51ebaf6a6abe11dfac79c9b3ba80e0dbc1e'
PLAN = Path('municipais/_lotes/20261021-aracaju-inspecao-tachados/plano-contextual.json')
PLAN_SHA = 'c7fb92f6177dfda2241524115543fe1aa3145b7457b448e604ffda274bf1d65b'
VISUAL = {70: '06eaf8c41d6abbb7c32582997471b5cad45bc24dc896d5c10594ed8a61e2e2fb',
          107: 'f22560297ddc7ffd389d6aaf39ebd5e35769984b730003de757f56ed95c77602'}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def preparar(layout, bbox, groups):
    chunks = layout.split('\f')
    pages = [p for p in ET.fromstring(bbox).iter() if p.tag.rsplit('}', 1)[-1] == 'page']
    if len(pages) != 107 or len(chunks) != 108 or chunks[-1].strip():
        raise ValueError('Contagem física difere')
    by_page = collections.defaultdict(list)
    for group in groups:
        by_page[group['pagina']].append(group)
    if len(groups) != 73 or len(by_page) != 45:
        raise ValueError('Plano visual incompleto')
    proof = []
    result = []
    for n, (chunk, page) in enumerate(zip(chunks[:-1], pages), 1):
        a = ''.join(chunk.split())
        b = ''.join(''.join(w.text or '' for w in page.iter() if w.tag.rsplit('}', 1)[-1] == 'word').split())
        if n in VISUAL and sha(a.encode()) != VISUAL[n]:
            raise ValueError('Ordem diferente da página visualmente revista: ' + str(n))
        if a != b and (n not in VISUAL or collections.Counter(a) != collections.Counter(b)):
            raise ValueError('Caracteres não conferidos na página ' + str(n))
        marked, spans = marcar(chunk, by_page.get(n, []))
        labels = re.findall(r'⟦(?:INÍCIO DO TRECHO TACHADO NA FONTE, página \d+, grupo \d+|FIM DO TRECHO TACHADO NA FONTE)⟧', marked)
        # Rótulos em linhas próprias conservam a indentação original da passagem.
        for label in set(labels):
            marked = marked.replace(label, '\n'+label+'\n')
        restored = marked
        for label in set(labels):
            restored = restored.replace('\n'+label+'\n', '')
        if restored != chunk:
            raise ValueError('Reversão integral diverge na página ' + str(n))
        result.append(marked)
        proof.append(dict(pagina=n, sequencia_layout_bbox=a == b,
                          multiconjunto_layout_bbox=collections.Counter(a) == collections.Counter(b),
                          fluxo_visual=n in VISUAL, grupos_marcados=len(spans),
                          reversao_byte_a_byte=True, sha256_layout=sha(chunk.encode())))
    return '\f'.join(result)+ '\f', proof


def main():
    source = (ROOT/PDF).read_bytes()
    plan_raw = (ROOT/PLAN).read_bytes()
    if sha(source) != PDF_SHA or sha(plan_raw) != PLAN_SHA:
        raise ValueError('Fonte ou plano visual mudou')
    plan = json.loads(plan_raw)
    review = ROOT/'municipais/_lotes/20261021-aracaju-inspecao-tachados/revisao-visual.json'
    if sha(review.read_bytes()) != plan['sha256_revisao_visual']:
        raise ValueError('Revisão visual mudou')
    layout = subprocess.check_output(['/opt/homebrew/bin/pdftotext', '-layout', '-enc', 'UTF-8', str(ROOT/PDF), '-']).decode()
    bbox = subprocess.check_output(['/opt/homebrew/bin/pdftotext', '-bbox-layout', '-enc', 'UTF-8', str(ROOT/PDF), '-'])
    marked, proof = preparar(layout, bbox, plan['grupos'])
    if '```' in marked or not re.search(r'Aracaju,\s*5 de abril de 1990\.', layout):
        raise ValueError('Delimitador ou data literal não conferida')
    ibge = next(c for c in json.loads((ROOT/'municipais/_indice/ibge-municipios.json').read_text()) if str(c['id']) == '2800308')
    if ibge['nome'] != 'Aracaju' or ibge['regiao-imediata']['regiao-intermediaria']['UF']['sigla'] != 'SE':
        raise ValueError('Identidade IBGE diverge')
    target = ROOT/'municipais/SE/aracaju/lei-organica/1990/lei-organica-aracaju-1990.md'
    if target.exists() or list(target.parent.parent.glob('**/*.md')):
        raise ValueError('Lei Orgânica existente exige conciliação; não substituir')
    title = 'Lei Orgânica do Município de Aracaju — compilação disponibilizada pela Câmara'
    note = ('Nota de transcrição: a edição oficial reúne redações tachadas e não tachadas. '
            'As 73 passagens com tachado confirmado visualmente estão delimitadas por rótulos explícitos com página e grupo; '
            'os rótulos são contextuais e podem incluir pontuação ou letras de alínea associadas, sem afirmar que todo glifo seja atravessado pelo risco. '
            'Todas as 107 páginas físicas, notas de alteração, revogação e efeitos, fólios, alíneas e valores foram mantidos. '
            'A nota da Emenda nº 72/2023 na página 77 também aparece tachada na fonte e conserva essa distinção. '
            'A grade de nomes e cargos da página 107 mantém seu alinhamento. '
            'O [mapa visual](../../../../_lotes/20261021-aracaju-inspecao-tachados/revisao-visual.json) documenta a apresentação. '
            'A marcação não decide vigência jurídica nem certifica atualização integral além do snapshot.\n\n')
    body = note+'```text\n'+marked.replace('\f', '\n\n').rstrip('\n')+'\n```'
    capture = json.loads((ROOT/'municipais/_fonte/capitais/aracaju/lei-organica-atualizada.fonte.json').read_text())
    metadata = dict(titulo=title, tipo='Lei Orgânica', numero='', data='1990-04-05', municipio='Aracaju', uf='SE', codigo_ibge='2800308',
                    origem_data='data literal de promulgação no fólio 106 do PDF oficial: Aracaju, 5 de abril de 1990',
                    versao_texto='compilação oficial disponível no portal da Câmara, sem rótulo global de data de edição; inclui notas até a Emenda 73/2026, sem certificar que todas as alterações até essa data estejam incorporadas; redações tachadas preservadas com rótulos contextuais',
                    fonte=capture['url'], sha256_fonte=PDF_SHA, sha256_texto=sha(body.encode()),
                    capturado_em_fonte=capture['capturado_em'], fuso_dia_captura='não informado no timestamp original; dia literal preservado', baixado_em=capture['capturado_em'][:10])
    output = '\n'.join(['---']+[k+': '+yaml_str(v) for k,v in metadata.items()]+['revogada: null','---','','# '+title,'',body,''])
    out = ROOT/'municipais/_lotes/20261021-aracaju-lo'
    out.mkdir(exist_ok=False)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x') as f:
        f.write(output)
    (out/'extracao-integral.json.gz').write_bytes(gzip.compress(json.dumps(dict(layout_original=layout,bbox=bbox.decode(),layout_com_rotulos=marked),ensure_ascii=False).encode(),mtime=0))
    (out/'prova-paginas.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
    (out/'normas.paths.txt').write_text(str(target.relative_to(ROOT))+'\n')
    manifest = dict(documento=str(target.relative_to(ROOT)), sha256=sha(target.read_bytes()), fonte=str(PDF), sha256_fonte=PDF_SHA,
                    paginas=107, sequencia_nativa_igual_em=105, fluxos_visuais=[70,107], grupos_tachados_preservados=73,
                    reversao='Remover apenas os rótulos inseridos recompõe cada página nativa byte a byte. Nenhuma linha numérica, margem, nota, pontuação, alínea ou palavra é removida.',
                    plano=str(PLAN), sha256_plano=PLAN_SHA, codigo_sha256=sha(Path(__file__).read_bytes()),
                    limite='Distinção gráfica atribuída ao PDF oficial, sem inferir efeito jurídico; data de captura original preservada. Exige gates finais de renderização, fonte e identidade antes de entrega.')
    (out/'manifesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(manifest,ensure_ascii=False))


if __name__ == '__main__':
    main()
