import datetime,hashlib,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from conferir_tabelas_nativas_ta import conferir
from auditar_textos_articulados_sapl_v3 import conferir as anterior
from auditar_textos_articulados_sapl_v4 import conferir as novo
BASE=Path(__file__).resolve().parent.parent
CASES=BASE/'municipais/_lotes/20261021-recuperacao-tabelas-ta-contexto-0001-v2/casos-reais.json'
class TestReais(unittest.TestCase):
 def test_tres_fontes_renderizadas_estruturalmente(self):
  for case in json.loads(CASES.read_text()):
   raw=(BASE/case['md']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),case['sha256_md']);body=raw.decode().split('\n---\n',1)[1].lstrip('\n').split('\n\n',1)[1][:-1];proof=case['row']['prova_frontend'];source=(BASE/proof['arquivo']).read_bytes();self.assertEqual(hashlib.sha256(source).hexdigest(),proof['sha256']);self.assertGreater(conferir(source.decode(),body)['tabelas'],0)
 def test_apenas_barreira_generica_tabela_mudou(self):
  for case in json.loads(CASES.read_text()):
   types={r['id']:r for r in json.loads((BASE/case['types']).read_text())['results']};annex=json.loads((BASE/case['annex']).read_text());reference=datetime.date(2026,10,21)
   with self.assertRaisesRegex(ValueError,'Mídia ou tabela ativa'):anterior(case['row'],types,annex,reference)
   self.assertGreater(novo(case['row'],types,annex,reference)['tabelas_nativas_prova']['tabelas'],0)
if __name__=='__main__':unittest.main()
