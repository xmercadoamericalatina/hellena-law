import unittest
from integridade_por_tipo import verificar_dispositivo_por_tipo


class DispositivoPorTipo(unittest.TestCase):
    def test_portaria_com_itens_sem_artigos(self):
        corpo = 'PORTARIA N° 028/93\n\nO SECRETÁRIO DE SAÚDE DO DISTRITO FEDERAL, no uso de suas atribuições regimentais, RESOLVE:\n\n1\\. Fica prorrogado o prazo.\n\n2\\. Esta Portaria entra em vigor.'
        self.assertIsNone(verificar_dispositivo_por_tipo(corpo, 'Portaria', '28')[0])

    def test_decreto_historico_resolve_criar(self):
        corpo = 'O Governador do Estado de Minas Gerais, usando de suas atribuições, resolve criar um Jardim de Infância na cidade de Itaúna.\n\nPalácio da Liberdade, 10 de janeiro de 1956.\nCLOVIS SALGADO GAMA'
        self.assertIsNone(verificar_dispositivo_por_tipo(corpo, 'Decreto', '4890')[0])

    def test_portaria_com_itens_romanos_ou_traco(self):
        for item in ['1 –', 'I -', '1)']:
            corpo = 'O SECRETÁRIO DE CULTURA, no uso de suas atribuições, resolve:\n\n' + item + ' Aprovar a programação e realização do programa.'
            self.assertIsNone(verificar_dispositivo_por_tipo(corpo, 'Portaria', '1')[0])

    def test_promulgacao_propria_nao_corrige_rotulo_da_fonte(self):
        corpo = 'Faço saber que a Assembléia aprovou e eu promulgo a seguinte Resolução:\n\nArt. 19 – Ficam aprovados os convênios.\nArt. 2º – Esta Resolução entra em vigor.'
        motivo, prova = verificar_dispositivo_por_tipo(corpo, 'Resolução', '2842')
        self.assertIsNone(motivo)
        self.assertIn('Art. 19', prova)
        self.assertNotIn('Art. 1º', prova)

    def test_autoridade_citada_em_errata_nao_basta(self):
        corpo = 'RETIFICAÇÃO\nOnde se lê:\nO SECRETÁRIO DE SAÚDE, no uso de suas atribuições, RESOLVE: 1. Aprovar a tabela.'
        self.assertIsNotNone(verificar_dispositivo_por_tipo(corpo, 'Portaria', '28')[0])

    def test_sumula_enunciado_e_tese_com_numero_exato(self):
        corpo = 'SÚMULAS DE JURISPRUDÊNCIA - ENUNCIADO 43\n\nO princípio da legalidade que restringe a ação do Administrador Público aos limites expressamente autorizados por lei abrange a Administração Direta, Indireta e Fundacional.\n\nConstituição Federal, art. 32.\n\nEste texto não substitui o publicado no DODF nº 228.'
        self.assertIsNone(verificar_dispositivo_por_tipo(corpo, 'Súmula', '43')[0])
        self.assertIsNotNone(verificar_dispositivo_por_tipo(corpo, 'Súmula', '44')[0])

    def test_sumula_so_referencias_nao_basta(self):
        corpo = 'SÚMULAS DE JURISPRUDÊNCIA - ENUNCIADO 43\n\nReferências:\n\nConstituição Federal, artigo 32, cujo texto tem muitas palavras, sem representar tese própria alguma.\n\nEste texto não substitui o publicado no DODF nº 228.'
        self.assertIsNotNone(verificar_dispositivo_por_tipo(corpo, 'Súmula', '43')[0])


if __name__ == '__main__':
    unittest.main()
