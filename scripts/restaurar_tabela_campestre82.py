"""Restaura sete colunas da tabela nativa da LC82/2026 deCampestre, vista na p1."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
DOC = Path('municipais/MG/campestre/leis-complementares/2026/leis-complementares-82-2026-sapl-1087.md')
SOURCE = Path('municipais/_fonte/organicas-sapl/sapl.campestre.mg.leg.br/1087.bin')
OLD = '2c19dc568c190a13b58e87ba82e209b52e21fde4f2c7a5fbf2b9a4281764f5f6'
HEADERS = ['Denominação dos cargos', 'Número de vagas criadas', 'Carga horária', 'Salário-base', 'Lotação', 'Escolaridade exigida', 'Atribuições']
CELLS = ['Salva-Vidas', '4', '12hx36h ou 40h semanais', 'R$ 3.800,00',
         'Secretaria Municipal de Esportes/ Complexo aquático Nacy Salomão',
         'Habilitação em curso de formação profissional específica, possuir aptidão física compatível com os esforços demandados para o cargo.',
         'Realizar práticas preventivas e de salvamento em ambientes aquáticos, manutenção de piscinas']


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    raw = (ROOT / DOC).read_bytes()
    if sha(raw) != OLD or sha((ROOT / SOURCE).read_bytes()) != '3d27fdea49a35f36e690887c058fc7e3a48868af5c6aa0fb6fbd511a776b7196':
        raise ValueError('Snapshot diverge')
    text = raw.decode()
    old = re.search(r'(?m)^Número Denominação.*cargo\.$', text)[0]
    table = '\n'.join(['| ' + ' | '.join(HEADERS) + ' |', '| ' + ' | '.join(['---'] * 7) + ' |', '| ' + ' | '.join(CELLS) + ' |'])
    if Counter(re.findall(r'\w+', old)) != Counter(re.findall(r'\w+', table)):
        raise ValueError('Tabela não preserva exatamente as palavras e números')
    text = text.replace(old, table, 1)
    # O restante do corpo, incluindo cláusulas e assinatura/data, é idêntico.
    if text.replace(table, old, 1) != raw.decode():
        raise ValueError('Mudança fora da tabela')
    oldversion = re.search(r'(?m)^versao_texto: (.*)$', text)
    version = json.loads(oldversion[1]) + '; tabela nativa da página1 recomposta em sete colunas, com células conferidas visualmente'
    text = re.sub(r'(?m)^versao_texto:.*$', lambda _: 'versao_texto: ' + json.dumps(version, ensure_ascii=False), text)
    rest = text.split('\n---\n', 1)[1].lstrip('\n').split('\n\n', 1)[1]
    hashbody = rest[:-1] if rest.endswith('\n') else rest
    text = re.sub(r'(?m)^sha256_texto:.*$', 'sha256_texto: "' + sha(hashbody.encode()) + '"', text)
    out = ROOT / 'municipais/_lotes/20261020-campestre82-tabela'
    out.mkdir(exist_ok=False)
    (out / 'documento-anterior.md').write_bytes(raw)
    (ROOT / DOC).write_text(text)
    evidence = Path('municipais/_referencias/auditorias/escala-sapl-0001-identidade/campestre-1087-1.png')
    result = {'documento': str(DOC), 'sha256_anterior': OLD, 'sha256_novo': sha((ROOT / DOC).read_bytes()),
              'fonte': str(SOURCE), 'sha256_fonte': sha((ROOT / SOURCE).read_bytes()),
              'pagina': 1, 'colunas': HEADERS, 'celulas': CELLS, 'linhas_dados': 1,
              'prova_visual': str(evidence), 'sha256_visual': sha((ROOT / evidence).read_bytes()),
              'verificacao': 'Todas as palavras/números da tabela anterior preservados exatamente; sete associações coluna/célula vistas no PDF. Restante do corpo idêntico.',
              'script_sha256': sha(Path(__file__).read_bytes())}
    (out / 'manifesto.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
