import unittest
from avisos_fonte import avisos_de_omissao


class AvisosFonte(unittest.TestCase):
    def test_retem_aviso_mesmo_com_titulo_anexo(self):
        self.assertTrue(avisos_de_omissao('ANEXO I\n\nOBSERVAÇÃO: A imagem do formulário não foi reproduzida por impossibilidade técnica.'))
        self.assertTrue(avisos_de_omissao('OBS: Os Anexos não foram\nimplantados por impossibilidade técnica.'))

    def test_remissao_editorial_dos_anexos_ao_dodf(self):
        self.assertTrue(avisos_de_omissao('Os anexos constam no DODF.'))
        self.assertFalse(avisos_de_omissao('Este texto não substitui o publicado no DODF nº 63.'))
        self.assertFalse(avisos_de_omissao('Art. 1º Altera o anexo do Decreto nº 10, publicado no DODF.'))

    def test_disposicao_normativa_nao_e_aviso_da_fonte(self):
        self.assertFalse(avisos_de_omissao('Art. 31 – Evitar iniciativas isoladas, não incluídas no planejamento global da Fundação.'))
        self.assertFalse(avisos_de_omissao('Parágrafo único – Quando ocorrer impossibilidade técnica para emissão da nota fiscal, poderá ser preenchida datilograficamente.'))

    def test_anexo_transcrito_sem_aviso(self):
        self.assertFalse(avisos_de_omissao('Art. 1º Aprova o anexo.\nANEXO\n1 0 001'))


if __name__ == '__main__':
    unittest.main()
