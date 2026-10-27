import unittest
from tabelas_estrutura import conferir_tabelas_complexas


class EstruturaTabelas(unittest.TestCase):
    def test_preserva_cabecalhos_e_dados_literalmente(self):
        html = '<table><tr><th colspan="2">Lados</th><th rowspan="2">Coordenada</th></tr><tr><td>1</td><td>2</td><td>8.802.537,291</td></tr></table>'
        self.assertEqual(len(conferir_tabelas_complexas(html, html)), 1)
        with self.assertRaises(ValueError):
            conferir_tabelas_complexas(html, html.replace('colspan="2"', 'colspan="3"'))
        with self.assertRaises(ValueError):
            conferir_tabelas_complexas(html, html.replace('8.802.537,291', '8.802.537,292'))

    def test_tabela_aninhada_preservada(self):
        html = '<table><tr><td>Antes<table><tr><td>Valor</td></tr></table>Depois</td></tr></table>'
        self.assertEqual(len(conferir_tabelas_complexas(html, html)), 1)

    def test_tabela_sem_fecho_rejeitada(self):
        with self.assertRaises(ValueError):
            conferir_tabelas_complexas('<table><tr><td colspan="2">Texto', '')


if __name__ == '__main__':
    unittest.main()
