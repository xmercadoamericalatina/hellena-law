import unittest
from integridade_texto import verificar_integridade_texto


class IntegraPropria(unittest.TestCase):
    def test_ordinal_ascii_e_artigo_proprio(self):
        motivo, prova = verificar_integridade_texto('Faço saber que promulgo a resolução:\n\n**Art. 1o** Fica aprovado o convênio.\nArt. 2º Vigência.')
        self.assertIsNone(motivo)
        self.assertIn('Art. 1o', prova)

    def test_promulgacao_inline(self):
        motivo, prova = verificar_integridade_texto('Faço saber que a Assembleia aprovou e eu promulgo a seguinte resolução: Art. 1º Fica aprovado o convênio. Art. 2º Vigência.')
        self.assertIsNone(motivo)
        self.assertIn('eu promulgo', prova)

    def test_aprovacao_inline(self):
        self.assertIsNone(verificar_integridade_texto('A Assembleia Legislativa de Minas Gerais aprova: Art. 1º Fica aprovado o convênio.')[0])

    def test_pontuacao_literal_artigo(self):
        self.assertIsNone(verificar_integridade_texto('Faço saber que promulgo a resolução:\nArt.- 1º Fica aprovado o convênio.')[0])

    def test_retificacao_com_artigo_citado_retem(self):
        motivo, _ = verificar_integridade_texto('RETIFICAÇÃO\nNo texto do decreto:\nArt. 1º Onde se lê valor X, leia-se valor Y.')
        self.assertIn('retificação', motivo)

    def test_retificacao_apos_norma_integral_nao_invalida(self):
        texto = 'O Governador decreta:\nArt. 1º Fica criado o programa.\nArt. 2º Vigência.\nPalácio da Liberdade.\nOBSERVAÇÃO:\nRetificação publicada em 1984.'
        self.assertIsNone(verificar_integridade_texto(texto)[0])

    def test_clausula_de_anexo_apos_artigo_nao_invalida(self):
        texto = 'Eu promulgo a resolução:\nArt. 1º Fica aprovado o termo aditivo.\nCLÁUSULA PRIMEIRA\nRetificação\nA cláusula do convênio passa a vigorar...'
        self.assertIsNone(verificar_integridade_texto(texto)[0])

    def test_artigo_apenas_citado_sem_dispositivo_retem(self):
        self.assertIsNotNone(verificar_integridade_texto('O sistema registra alteração do art. 1º do decreto citado.')[0])


if __name__ == '__main__':
    unittest.main()
