import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_tachados_pdf_municipal import analisar_pagina


class Pagina:
    def __init__(self, y, annotation=False):
        self.edges = [{'orientation': 'h', 'linewidth': .5, 'x0': 0,
                       'x1': 40, 'top': y}]
        self.chars = [{'text': c, 'x0': i * 8, 'x1': i * 8 + 7,
                       'top': 10, 'bottom': 20, 'fontname': 'Teste'}
                      for i, c in enumerate('texto')]
        self.annots = [{'data': {'Subtype': '/StrikeOut'}}] if annotation else []


class TestTachados(unittest.TestCase):
    def test_linha_no_meio_dos_glifos(self):
        self.assertEqual(analisar_pagina(Pagina(15))[0]['texto'], 'texto')

    def test_sublinhado_e_borda_nao_sao_tachado(self):
        self.assertEqual(analisar_pagina(Pagina(21)), [])
        self.assertEqual(analisar_pagina(Pagina(10)), [])

    def test_anotacao_explicita(self):
        self.assertEqual(analisar_pagina(Pagina(25, True))[0]['tipo'],
                         'anotacao_StrikeOut')

    def test_borda_duplicada_e_deduplicada(self):
        p = Pagina(15)
        p.edges += p.edges[:]
        self.assertEqual(len(analisar_pagina(p)), 1)


if __name__ == '__main__':
    unittest.main()
