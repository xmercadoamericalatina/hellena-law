import unittest
from visuais_fonte import imagens_html, exigir_sem_imagem_omitida


class VisuaisFonte(unittest.TestCase):
    def test_anexo_fora_de_tabela_e_retido(self):
        with self.assertRaisesRegex(ValueError, 'anexo.jpg'):
            exigir_sem_imagem_omitida('<p>Art. 1º Anexo.</p><img src="anexo.jpg">')

    def test_imagem_dentro_de_tabela_e_retida(self):
        with self.assertRaises(ValueError):
            exigir_sem_imagem_omitida('<table><tr><td><img src="tabela.png"/></td></tr></table>')

    def test_texto_e_tabela_sem_imagem_passam(self):
        exigir_sem_imagem_omitida('<p>Art. 1º</p><table><tr><td>0</td></tr></table>')
        self.assertEqual(imagens_html('a &lt;img src="nao-tag"&gt;'), [])


if __name__ == '__main__':
    unittest.main()
