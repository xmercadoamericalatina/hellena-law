"""Revisão com fecho não pode validar citação, anexo ou data contraditória."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from identidade_decreto_revisao import verificar_epigrafe_e_fecho as verificar


def texto(epigrafe, fecho='Brasília, 8 de novembro de 1999.'):
    return epigrafe + '\n\nO PRESIDENTE DA REPÚBLICA decreta:\n\nArt. 1º Fica aprovado o regulamento.\n\n' + fecho + '\n\nFERNANDO HENRIQUE CARDOSO'


class RevisaoIdentidade(unittest.TestCase):
    def test_mes_defeituoso_com_fecho_proprio(self):
        result = verificar(texto('DECRETO Nº 3.234, DE 8 DE NOBEMBRO DE 1999.'), '3234', '1999-11-08')
        self.assertEqual(result['metodo'], 'numero_proprio_e_data_do_fecho_proprio')
        self.assertEqual(result['epigrafe']['mes_literal'], 'NOBEMBRO')

    def test_epigrafe_apenas_numero_ano(self):
        self.assertIsNotNone(verificar(texto('DECRETO Nº 3.234/1999'), '3234', '1999-11-08'))

    def test_numero_ou_data_clara_divergentes_nao_sao_sobrescritos(self):
        for epigrafe in ['DECRETO Nº 3.235, DE 8 DE NOBEMBRO DE 1999.',
                         'DECRETO Nº 3.234, DE 9 DE NOBEMBRO DE 1999.',
                         'DECRETO Nº 3.234, DE 8 DE DEZEMBRO DE 1999.',
                         'DECRETO Nº 3.234, DE 8 DE NOBEMBRO DE 1998.']:
            with self.subTest(epigrafe=epigrafe):
                self.assertIsNone(verificar(texto(epigrafe), '3234', '1999-11-08'))

    def test_datas_numericas_e_mes_incompativel_nao_sao_sobrescritos(self):
        for epigrafe in ['DECRETO Nº 3.234, DE 08/12/1999',
                         'DECRETO Nº 3.234, DE 08/12/99',
                         'DECRETO Nº 3.234, DE 8 DE 12 DE 1999',
                         'DECRETO Nº 3.234, DE 8 12 1999',
                         'DECRETO Nº 3.234, DE 8 DE NOVEMBRO DE 98',
                         'DECRETO Nº 3.234, DE 9. DE NOVEMBRO DE 1999',
                         'DECRETO Nº 3.234, DE 8 DE MAJO DE 1999']:
            with self.subTest(epigrafe=epigrafe):
                self.assertIsNone(verificar(texto(epigrafe), '3234', '1999-11-08'))

    def test_anexo_e_citacao_nao_sao_identidade(self):
        self.assertIsNone(verificar(texto('O texto cita o DECRETO Nº 3.234/1999'), '3234', '1999-11-08'))
        self.assertIsNone(verificar(texto('Art. 1º Cita-se:\n\nDECRETO Nº 3.234/1999'), '3234', '1999-11-08'))
        body = texto('DECRETO Nº 3.234/1999', 'ANEXO I\n\nBrasília, 8 de novembro de 1999.')
        self.assertIsNone(verificar(body, '3234', '1999-11-08'))

    def test_h1_gerado_e_fecho_tardio_nao_confirmam(self):
        self.assertIsNone(verificar(texto('# Decreto nº 3.234/1999'), '3234', '1999-11-08'))
        body = texto('DECRETO Nº 3.234/1999', 'Brasília, 7 de novembro de 1999.\n\nBrasília, 8 de novembro de 1999.')
        self.assertIsNone(verificar(body, '3234', '1999-11-08'))


if __name__ == '__main__':
    unittest.main()
