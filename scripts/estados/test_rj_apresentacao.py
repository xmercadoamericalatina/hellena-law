import unittest
try:
    from normalizar_rj_apresentacao import normalizar
except ModuleNotFoundError as e:
    if e.name != 'markdown_it': raise
    normalizar = None


@unittest.skipIf(normalizar is None, 'requer markdown-it-py==4.0.0')
class ApresentacaoTests(unittest.TestCase):
    def test_hardbreak_tem_mesmo_dom(self):
        self.assertEqual(normalizar('A  \nB\n'), 'A<br>\nB\n')

    def test_fim_de_paragrafo_nao_ganha_break(self):
        self.assertEqual(normalizar('A  \n\nB\n'), 'A\n\nB\n')

    def test_preformatado_nao_perde_espacos(self):
        for source in ('```\n0  \n1\n```\n', '<pre>0  \n1</pre>', '<div style="white-space:pre">0  \n1</div>'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                normalizar(source)

    def test_sinais_numericos_literais_preservados(self):
        self.assertEqual(normalizar('-100,50  \n0,5%\n'), '-100,50<br>\n0,5%\n')


if __name__ == '__main__': unittest.main()
