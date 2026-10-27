import unittest
from unittest.mock import patch
import sapl


class ConversaoSAPL(unittest.TestCase):
    def test_pdf_nao_passa_pelo_removedor_de_numeros(self):
        original = 'Art. 1º ' + 'Texto normativo com conteúdo suficiente. ' * 4 + '\n0\n001\n123\n'
        with patch.object(sapl, 'conferir_visuais_pdf'), patch.object(sapl, 'extrair_camada_textual', return_value=(original, original)), patch.object(sapl, 'documento_para_md', side_effect=AssertionError('conversor destrutivo')):
            corpo, erro = sapl.converter_anexo_sem_omissoes(b'%PDF', 'norma.pdf')
        self.assertIsNone(erro)
        self.assertIn('\n0\n001\n123\n', corpo)

    def test_imagem_fora_de_tabela_rejeitada(self):
        corpo, erro = sapl.converter_anexo_sem_omissoes(b'<p>Art. 1</p><img src="anexo.png">', 'norma.html')
        self.assertIsNone(corpo)
        self.assertIn('imagem normativa', erro)

    def test_timeout_do_extrator_registra_falha(self):
        import subprocess
        with patch.object(sapl, 'conferir_visuais_pdf', side_effect=subprocess.TimeoutExpired('pdfimages', 120)):
            corpo, erro = sapl.converter_anexo_sem_omissoes(b'%PDF', 'norma.pdf')
        self.assertIsNone(corpo)
        self.assertIn('timed out', erro)

    def test_pdf_com_imagem_desconhecida_rejeitado(self):
        with patch.object(sapl, 'conferir_visuais_pdf', side_effect=ValueError('imagem sem hash visual comprovado')):
            corpo, erro = sapl.converter_anexo_sem_omissoes(b'%PDF', 'norma.pdf')
        self.assertIsNone(corpo)
        self.assertIn('hash visual', erro)

    def test_anexo_declarado_nao_transcrito_rejeitado(self):
        html = '<p>Art. 1º '+ 'Norma com conteúdo suficiente. '*4 +'</p><p>ANEXO</p><p>OBS: O Anexo não foi transcrito por impossibilidade técnica.</p>'
        corpo, erro = sapl.converter_anexo_sem_omissoes(html.encode(), 'norma.html')
        self.assertIsNone(corpo)
        self.assertIn('não reproduzido', erro)


class CacheSAPL(unittest.TestCase):
    def test_cache_divergente_ou_corrompido_preserva_ambos_sem_md(self):
        import gzip
        import tempfile
        from pathlib import Path
        n = {'id': 42, 'numero': '39', 'ano': 2014, 'data': '2014-02-04',
             'tipo': 6, 'texto_integral': 'https://example.test/oficial.html',
             '__str__': 'Emenda 39'}
        for corrompido in [False, True]:
            with self.subTest(corrompido=corrompido), tempfile.TemporaryDirectory() as td:
                raiz = Path(td)
                fonte = raiz/'fonte.html.gz'
                antigo = b'cache ilegivel' if corrompido else gzip.compress(b'fonte anterior')
                fonte.write_bytes(antigo)
                md = raiz/'nao-criar.md'
                novo = b'<p>Art. 1 texto oficial novo.</p>'
                with patch.object(sapl, 'RAIZ_ESTADUAIS', td), patch.object(sapl, 'existentes', return_value=[]), patch.object(sapl, 'caminhos', return_value=(str(md),str(fonte))), patch.object(sapl.rede,'get',return_value=(200,novo,'text/html')):
                    status, erro = sapl.processar_factory('AL', {'6':'Emenda à Constituição'})(n)
                self.assertEqual(status,'sem_texto')
                self.assertFalse(md.exists())
                self.assertEqual(fonte.read_bytes(),antigo)
                self.assertEqual(gzip.decompress(Path(erro['nova_fonte']).read_bytes()),novo)


if __name__ == '__main__':
    unittest.main()
