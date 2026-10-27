import base64
import unittest
from auditar_cache_rfb import pendencia_visual


class ImagensTest(unittest.TestCase):
    def test_imagem_fora_de_tabela_nao_e_ignorada(self):
        for texto in ('<p>Art.1</p><img src="anexo.jpg">', '<svg><path/></svg>', '<math>x</math>', '<v:shape>tabela</v:shape>'):
            with self.subTest(texto=texto):
                self.assertIsNotNone(pendencia_visual({'outrosSegmentos': [{'original': True, 'textoIntegra': texto}]}))

    def test_pdf_exige_prova_de_numeros_e_paginacao(self):
        for tipo in (2, 6):
            self.assertIsNotNone(pendencia_visual({'ementas': [{'original': True, 'arquivoBinario': {'idTipoArquivo': tipo}}]}))

    def test_html_binario_tambem_tem_anexo_visual(self):
        anexo = {'idTipoArquivo': 4, 'arquivoBinario': base64.b64encode(b'<img src="tabela.jpg">').decode()}
        self.assertIsNotNone(pendencia_visual({'outrosSegmentos': [{'original': True, 'arquivoBinario': anexo}]}))

    def test_texto_historico_omitido_nao_contamina_original(self):
        self.assertIsNone(pendencia_visual({'outrosSegmentos': [
            {'original': False, 'textoIntegra': '<img src="historico.jpg">'},
            {'original': True, 'textoIntegra': '<table><tr><td>0</td></tr></table>'}]}))


if __name__ == '__main__':
    unittest.main()
