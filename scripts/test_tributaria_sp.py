"""Valores isolados de tabelas não são números de página."""
import subprocess
import unittest
from unittest.mock import patch
from baixar_tributaria_sp import transcricao_anexo


class TranscricaoTributariaTest(unittest.TestCase):
    def pdf_text(self, alterar_folio=False):
        paginas=[]
        for i in range(1,233):
            folio=999 if alterar_folio and i==7 else i
            paginas.append(str(folio)+'\nItem da Lista\n26\nValor\n0\n')
        return ('\f'.join(paginas)+'\f').encode()

    def test_preserva_valores_numericos_isolados_e_colunas(self):
        with patch('baixar_tributaria_sp.subprocess.run', return_value=subprocess.CompletedProcess([],0,self.pdf_text())):
            s=transcricao_anexo('nao-abre-pdf-no-teste')
        self.assertEqual(s.count('\n26\n'),232)
        self.assertEqual(s.count('\n0\n'),232)
        self.assertIn('```text',s)

    def test_folio_inesperado_requer_revisao(self):
        with patch('baixar_tributaria_sp.subprocess.run', return_value=subprocess.CompletedProcess([],0,self.pdf_text(True))):
            with self.assertRaisesRegex(ValueError,'fólio sequencial'):
                transcricao_anexo('nao-abre-pdf-no-teste')


if __name__=='__main__':
    unittest.main()
