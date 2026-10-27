import unittest
from auditar_imagens_pdf_sapl import imagens

class ImagensPDFTest(unittest.TestCase):
    def test_tabela_embutida_na_camada_textual_e_listada(self):
        s='page num type width height color comp bpc enc interp object ID x-ppi y-ppi size ratio\n 142 1 image 399 758 rgb 3 8 jpeg yes 284 0 135 143 60.0K 6.8%\n'
        r=imagens(s)
        self.assertEqual(r[0]['pagina'],142);self.assertEqual(r[0]['largura_px'],399)
    def test_pdf_sem_imagens_e_formato_invalido(self):
        self.assertEqual(imagens('page num type width height\n-----------------\n'),[])
        with self.assertRaises(ValueError):imagens('142 1 image 399')

if __name__=='__main__':unittest.main()
