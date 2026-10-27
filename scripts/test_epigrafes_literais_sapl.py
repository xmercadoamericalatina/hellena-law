from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_epigrafes_literais_sapl import analisar, numero


class TestEpigrafes(unittest.TestCase):
    def test_sufixo_nao_desaparece(self):
        self.assertNotEqual(numero('1B'), numero('001'))
        self.assertEqual(numero('01.234-A'), numero('1234A'))

    def test_caso_real_sabugi_api_sufixo_pdf_sem_sufixo(self):
        for value, printed, date in [('1B', '01', '20 de dezembro de 2006'), ('8B', '008', '18 de junho de 2024')]:
            r = analisar({'tipo': 'Resolução', 'numero': value}, 'Resolução nº ' + printed + ', de ' + date + '\nArt. 1º Texto.')
            self.assertTrue(r['divergencias'])
            self.assertFalse(r['numero_literal_confirmado'])

    def test_caso_valido_e_sem_epigrafe(self):
        r = analisar({'tipo': 'Lei Complementar', 'numero': '1234A'}, 'LEI COMPLEMENTAR N.º 1.234A, DE 2 DE MARÇO DE 2026\nArt. 1º Texto.')
        self.assertTrue(r['numero_literal_confirmado'])
        r = analisar({'tipo': 'Lei', 'numero': '1'}, 'Ementa somente.\nArt. 1º Texto.')
        self.assertFalse(r['numero_literal_confirmado'])
        self.assertFalse(r['divergencias'])

    def test_data_real_sem_preposicao_e_discrepancia(self):
        source = 'Lei Complementar Municipal nº 592,\n de 16 abril de 2021\nArt. 1º Texto.'
        r = analisar({'tipo': 'Lei Complementar', 'numero': '592', 'data': '2021-04-16'}, source)
        self.assertTrue(r['data_literal_confirmada'])
        r = analisar({'tipo': 'Lei Complementar', 'numero': '592', 'data': '2021-04-15'}, source)
        self.assertTrue(r['divergencias'])
        self.assertFalse(r['data_literal_confirmada'])


if __name__ == '__main__':
    unittest.main()
