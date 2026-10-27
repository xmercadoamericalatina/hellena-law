from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from converter_organica_curitiba import converter


class TestCuritiba(unittest.TestCase):
    def test_bloco_exclui_navegacao_e_historico_mantem_revogado(self):
        html = '<nav>Menu</nav><div id="alterado_conteudo"><p><s>Texto antigo.</s></p><p>Art.1º Texto atual.</p><p>Art.2º Revogado.</p></div><div id="original">Histórico original.</div>'
        md, _, old = converter(html)
        self.assertNotIn('Menu', md)
        self.assertNotIn('Histórico', md)
        self.assertNotIn('Texto antigo', md)
        self.assertIn('Revogado.', md)
        self.assertEqual(old, ['Texto antigo.'])

    def test_bloco_incompleto_ou_duplicado_retido(self):
        for html in ['<div id="alterado_conteudo">Texto', '<div id="alterado_conteudo">A</div><div id="alterado_conteudo">B</div>']:
            with self.assertRaises(ValueError):
                converter(html)


if __name__ == '__main__':
    unittest.main()
