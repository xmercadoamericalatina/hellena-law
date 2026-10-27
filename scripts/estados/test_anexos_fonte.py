import unittest
from anexos_fonte import remissoes_sem_representacao


class AnexosFonte(unittest.TestCase):
    def test_retem_remissao_propria_sem_tabela(self):
        self.assertTrue(remissoes_sem_representacao('Art. 1º Conforme a Tabela 2, deste decreto.'))
        self.assertTrue(remissoes_sem_representacao('Art. 1º No Anexo I a este Decreto.'))

    def test_anexo_de_outra_norma_nao_basta(self):
        self.assertFalse(remissoes_sem_representacao('Art. 1º Altera o Anexo I do Decreto nº 123, de 2000.'))
        self.assertFalse(remissoes_sem_representacao('Altera o anexo II do RICMS a que se refere o artigo 1º deste Decreto.'))

    def test_anexo_representado(self):
        self.assertFalse(remissoes_sem_representacao('Art. 1º Anexo I deste decreto.\n\n# ANEXO I\n0'))
        self.assertFalse(remissoes_sem_representacao('Tabela 1 em anexo.\n<table><tr><td>0</td></tr></table>'))


if __name__ == '__main__':
    unittest.main()
