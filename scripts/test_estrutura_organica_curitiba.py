from pathlib import Path
import re
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from estruturar_organica_curitiba import estruturar, ROOT, SOURCE
from converter_organica_curitiba import converter


class TestEstruturaCuritiba(unittest.TestCase):
    def test_negrito_mal_fechado_nao_colapsa_quebras(self):
        html = '<div id="alterado_conteudo"><strong>Art. 1º Regra.<br/><br/>I - Item.<br/><br/><strong>Art. 2º Outra regra.</strong><br/><s>Texto antigo</s><p>Art. 3º Revogado.</p></div>'
        md, events = estruturar(html)
        self.assertIn('Art. 1º Regra.\n\nI - Item.\n\nArt. 2º Outra regra.', md)
        self.assertIn('Art. 3º Revogado.', md)
        self.assertNotIn('Texto antigo', md)
        self.assertTrue(events)

    def test_snapshot_real_preserva_palavras_e_limites(self):
        html = (ROOT / SOURCE).read_text()
        md, events = estruturar(html)
        anterior, _, _ = converter(html)
        self.assertEqual(re.findall(r'\w+', anterior), re.findall(r'\w+', md))
        self.assertEqual(len(re.findall(r'\w+', md)), 23748)
        self.assertEqual(len(md.strip().split('\n\n')), 983)
        self.assertIn('Art. 4ºConstituem objetivos fundamentais', md)
        self.assertRegex(md, r'Art\. 4ºConstituem[^\n]+\n\nI - a defesa do regime democrático;')
        self.assertIn('\n\nArt. 5ºSão assegurados pelo Município', md)
        self.assertGreater(len(events), 1900)


if __name__ == '__main__':
    unittest.main()
