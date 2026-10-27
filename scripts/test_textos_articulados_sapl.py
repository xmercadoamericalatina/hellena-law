import datetime as dt
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from baixar_textos_articulados_sapl import elegibilidade, comparar_norma


class TestArticulados(unittest.TestCase):
    def setUp(self):
        self.ta = {'id': 1, 'privacidade': 0, 'tipo_ta': 3, 'content_type': 68,
                   'object_id': 10, 'data': '2026-01-01', 'ano': 2026, 'numero': '1'}
        self.kinds = {3: {'descricao': 'Norma Jurídica', 'content_type': 68}}
        self.reference = dt.date(2026, 10, 20)

    def test_so_status_explicitamente_publicos(self):
        for status in [0, 69]:
            self.assertIsNone(elegibilidade({**self.ta, 'privacidade': status}, self.kinds, self.reference))
        for status in [None, 79, 89, 99]:
            self.assertIn('não público', elegibilidade({**self.ta, 'privacidade': status}, self.kinds, self.reference))

    def test_futuro_ano_e_modelo_divergentes_retidos(self):
        self.assertIn('futura', elegibilidade({**self.ta, 'data': '2026-12-16'}, self.kinds, self.reference))
        self.assertIn('ano divergente', elegibilidade({**self.ta, 'ano': 2013}, self.kinds, self.reference))
        self.assertIn('vínculo', elegibilidade({**self.ta, 'content_type': 48}, self.kinds, self.reference))
        self.assertIn('modelo', elegibilidade(self.ta, {3: {'descricao': 'Matéria Legislativa'}}, self.reference))

    def test_identidade_e_conflito_judicial(self):
        norma = {'id': 10, 'data': '2026-01-01', 'ano': 2026, 'numero': '001', 'observacao': ''}
        self.assertIsNone(comparar_norma(self.ta, norma))
        self.assertIn('divergentes', comparar_norma(self.ta, {**norma, 'data': '2026-01-02'}))
        self.assertIn('judicial', comparar_norma(self.ta, {**norma, 'observacao': 'ADI0802792declarouartigo237inconstitucional'}))


if __name__ == '__main__':
    unittest.main()
