import unittest
from ba import conferir_numero_epigrafe


class NumeroEpigrafeTest(unittest.TestCase):
    def test_sufixo_literal_preservado(self):
        self.assertEqual(conferir_numero_epigrafe('DECRETO Nº 181 - A DE 09 DE JULHO DE 1991', '181'), '181-A')
        self.assertEqual(conferir_numero_epigrafe('DECRETO Nº 34.321-A DE 15 DE JANEIRO DE 1987', '34321'), '34321-A')

    def test_formatacao_numero_sem_sufixo_inalterada(self):
        self.assertEqual(conferir_numero_epigrafe('DECRETO Nº 23.600 DE 16 DE ABRIL DE 2025', '23600'), '23600')
        self.assertEqual(conferir_numero_epigrafe('DECRETO Nº 181-A DE 09 DE JULHO DE 1991', '181-A'), '181-A')

    def test_conflito_nao_inferido(self):
        with self.assertRaisesRegex(ValueError, 'diverge'):
            conferir_numero_epigrafe('DECRETO Nº 372 DE 12 DE MAIO DE 1987', '272')
        with self.assertRaises(ValueError):
            conferir_numero_epigrafe('DECRETO Nº 181 DE 09 DE JULHO DE 1991', '181-A')
