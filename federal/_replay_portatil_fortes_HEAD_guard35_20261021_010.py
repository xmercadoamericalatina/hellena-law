"""Replay portátil, offline e somente leitura dos 5.178 casos do snapshot HEAD.

Na raiz: python3 -B federal/_replay_portatil_fortes_HEAD_guard35_20261021_010.py
Usa somente provas incluídas no manifesto de insumos e a biblioteca padrão.
Não usa Git, rede, caches normativos, módulos vivos do coletor ou arquivos /tmp.
"""
import ast
import collections
import gzip
import hashlib
import json
import sys
import types
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
assert Path.cwd().resolve() == ROOT, 'Execute na raiz do repositório.'
B = ROOT / 'federal/_prova_predicado_guard35_head_20261021_008'
manifest_path = ROOT / 'federal/_replay_portatil_fortes_HEAD_guard35_20261021_010_inputs.json'
inputs = json.loads(manifest_path.read_text())
for record in inputs['arquivos']:
    path = Path(record['path'])
    assert not path.is_absolute() and '..' not in path.parts
    assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256'], str(path)

# Carrega as dependências exatas arquivadas, sem importar os coletores vivos.
def frozen_module(name, filename):
    module = types.ModuleType(name)
    sys.modules[name] = module
    exec(compile((B / filename).read_text(), filename, 'exec'), module.__dict__)
    return module

guard = frozen_module('integridade_anexos_decreto', '03-guard35.py.txt')
visible = frozen_module('integridade_html_federal', '05-contagens.py.txt')
fields_ast = ast.parse((B / '04-fields.py.txt').read_text())
fields_node = next(node for node in fields_ast.body if isinstance(node, ast.FunctionDef) and node.name == 'fields')
fields_module = types.ModuleType('preparar_lote_decretos_cache')
fields_module.__dict__['json'] = json
exec(compile(ast.Module(body=[fields_node], type_ignores=[]), '04-fields.py.txt:fields', 'exec'), fields_module.__dict__)
sys.modules['preparar_lote_decretos_cache'] = fields_module

# Recalcula os 6.700 checks nas preimagens. Os cortes removem exclusivamente
# as instruções de geração dos artefatos, depois dos laços do predicado.
code1 = (B / '01-estratificar.py.txt').read_text().split('\nmanifest=')[0]
g = {'__name__': 'replay_portatil_estratos'}
exec(compile(code1, '01-estratificar.py.txt', 'exec'), g)
old_rows = g['rows']
assert len(old_rows) == 6700
code2 = (B / '02-predicado-forte.py.txt').read_text()
code2 = code2[code2.index('def label('):code2.index('\nassert len(rows)==6700;')]
stored = [json.loads(line) for line in gzip.open('federal/_receipts_estratos_delta_guard35_20261021_007.jsonl.gz', 'rt')]
g.update(old={'registros': old_rows}, rows=[], counts=collections.Counter(),
         samplepaths={r['path'] for r in stored if r['conferencia_contextual_na_amostra']},
         _rotulo_vazio=guard._rotulo_vazio)
exec(compile(code2, '02-predicado-forte.py.txt', 'exec'), g)
by_path = {r['path']: r for r in g['rows']}
for expected in stored:
    actual = by_path[expected['path']]
    for key in ('sha256_md', 'sha256_fonte_html', 'verificacoes', 'estrato',
                'indicador_automatico_forte', 'rotulos_finais_vazios',
                'prefixo_assinaturas_estrutural'):
        assert actual[key] == expected[key], (expected['path'], key)

# Mesmos bytes JSON da API, preservados nos backups dos 5.178. O único caso
# excluído depois de ler metadados é arquivado separadamente, sem corrigir
# seu teste estrito de caixa entre número MD e URN.
metadata_by_urn = {}
for line in gzip.open('federal/_receipts_fortes_HEAD_guard35_20261021_008.jsonl.gz', 'rt'):
    row = json.loads(line)
    raw = row['metadados_json_original'].encode()
    api = json.loads(raw)
    metadata_by_urn[api['legislationIdentifier']] = raw
extra = gzip.decompress((B / 'metadados-caso-excluido-99970-A.json.gz').read_bytes())
metadata_by_urn[json.loads(extra)['legislationIdentifier']] = extra
assert len(metadata_by_urn) == 5179

class MetadataArchive:
    """Substitui apenas exists/read_bytes do cache por bytes arquivados."""
    def __init__(self, urn, expected_sha):
        self.raw = metadata_by_urn.get(urn)
        if self.raw is not None:
            assert hashlib.sha256(self.raw).hexdigest() == expected_sha
    def exists(self):
        return self.raw is not None
    def read_bytes(self):
        assert self.raw is not None
        return gzip.compress(self.raw, mtime=0)

code3 = (B / '06-selecao-HEAD.py.txt').read_text().split('\ncode=B/')[0]
old_snapshot_literal = "'/tmp/federal-head-guard35-20261021.json'"
assert code3.count(old_snapshot_literal) == 1
code3 = code3.replace(old_snapshot_literal, repr(str(B / 'snapshot-HEAD.json')))
old_cache_expression = "B/'_fonte/metadados-normas'/sha(meta['urn'].encode())/(meta['sha256_metadados_fonte']+'.json.gz')"
assert code3.count(old_cache_expression) == 1
code3 = code3.replace(old_cache_expression, "MetadataArchive(meta['urn'],meta['sha256_metadados_fonte'])")
h = {'__name__': 'replay_portatil_HEAD', 'MetadataArchive': MetadataArchive}
exec(compile(code3, '06-selecao-HEAD.py.txt:IO-portatil', 'exec'), h)
proposed = [json.loads(line) for line in gzip.open('federal/_proposta_fortes_HEAD_guard35_20261021_008.jsonl.gz', 'rt')]
assert len(h['rows']) == len(proposed) == 5178
assert {r['path']: r for r in h['rows']} == {r['path']: r for r in proposed}
assert len(h['strong']) == 5262 and len(h['masked']) == 2145
print(json.dumps({
    'head': h['snap']['head'], 'delta_recalculado': len(old_rows),
    'estrato_forte_recalculado': len(h['strong']),
    'propostas_HEAD_reproduzidas_integralmente': len(proposed),
    'metadados_API_arquivados': len(metadata_by_urn),
    'exclusoes': dict(h['excluded']),
    'sha256_propostas': hashlib.sha256(Path('federal/_proposta_fortes_HEAD_guard35_20261021_008.jsonl.gz').read_bytes()).hexdigest(),
    'mutacoes': 0,
}, ensure_ascii=False, indent=2))
