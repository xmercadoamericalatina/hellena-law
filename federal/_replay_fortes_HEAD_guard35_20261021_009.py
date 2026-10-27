"""Replay offline e somente leitura do predicado e dos 5.178 blobs propostos.

Executar na raiz: python3 -B federal/_replay_fortes_HEAD_guard35_20261021_009.py
Não faz HTTP, Git, alterações de MD ou gravações de relatórios.
"""
import collections
import gzip
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
assert Path.cwd().resolve() == ROOT, 'Executar na raiz do repositório.'
proof = ROOT / 'federal/_prova_predicado_guard35_head_20261021_008'
# Confronta dependências vivas com os módulos exatos arquivados. Não aceita
# silenciosamente um guard ou parser modificado depois da entrega.
for snapshot, live in [
    ('03-guard35.py.txt', 'scripts/integridade_anexos_decreto.py'),
    ('04-fields.py.txt', 'scripts/preparar_lote_decretos_cache.py'),
    ('05-contagens.py.txt', 'scripts/integridade_html_federal.py'),
]:
    assert (proof / snapshot).read_bytes() == (ROOT / live).read_bytes(), live

# As duas partes originais são executadas somente até o fim dos laços puros,
# antes das instruções de escrita. Assim o replay usa o predicado exato,
# preservando a distinção entre risco de citação/lista e o estrato forte.
code1 = (proof / '01-estratificar.py.txt').read_text().split('\nmanifest=')[0]
g = {'__name__': 'replay_estratos_somente_leitura'}
exec(compile(code1, '01-estratificar.py.txt', 'exec'), g)
old = g['rows']
assert len(old) == 6700
sys.path.insert(0, str(ROOT / 'scripts'))
from integridade_anexos_decreto import _rotulo_vazio

code2 = (proof / '02-predicado-forte.py.txt').read_text()
pure_functions_and_loop = code2[code2.index('def label('):code2.index('\nassert len(rows)==6700;')]
stored = [json.loads(line) for line in gzip.open(
    ROOT / 'federal/_receipts_estratos_delta_guard35_20261021_007.jsonl.gz', 'rt')]
g.update(old={'registros': old}, rows=[], counts=collections.Counter(),
         samplepaths={r['path'] for r in stored if r['conferencia_contextual_na_amostra']},
         _rotulo_vazio=_rotulo_vazio)
exec(compile(pure_functions_and_loop, '02-predicado-forte.py.txt', 'exec'), g)
recomputed = {r['path']: r for r in g['rows']}
for record in stored:
    actual = recomputed[record['path']]
    for key in ('sha256_md', 'sha256_fonte_html', 'verificacoes', 'estrato',
                'indicador_automatico_forte', 'rotulos_finais_vazios',
                'prefixo_assinaturas_estrutural'):
        assert actual[key] == record[key], (record['path'], key)

# Aplica o filtro exato do snapshot HEAD/máscaras/literais/API. O corte ocorre
# antes da criação da pasta de código, das provas gzip e de qualquer write.
code3 = (proof / '06-selecao-HEAD.py.txt').read_text().split('\ncode=B/')[0]
h = {'__name__': 'replay_filtro_HEAD_somente_leitura'}
exec(compile(code3, '06-selecao-HEAD.py.txt', 'exec'), h)
proposed = [json.loads(line) for line in gzip.open(
    ROOT / 'federal/_proposta_fortes_HEAD_guard35_20261021_008.jsonl.gz', 'rt')]
assert len(h['rows']) == len(proposed) == 5178
assert {r['path']: r for r in h['rows']} == {r['path']: r for r in proposed}
assert len(h['strong']) == 5262
assert len(h['masked']) == 2145
print(json.dumps({
    'head': h['snap']['head'], 'delta_recalculado': len(old),
    'estrato_forte_recalculado': len(h['strong']),
    'propostas_HEAD_reproduzidas_integralmente': len(proposed),
    'exclusoes': dict(h['excluded']),
    'sha256_propostas': hashlib.sha256((ROOT / 'federal/_proposta_fortes_HEAD_guard35_20261021_008.jsonl.gz').read_bytes()).hexdigest(),
    'mutacoes': 0,
}, ensure_ascii=False, indent=2))
