"""Não grava a norma de 1920 sob a data de 1919 indicada por um índice legado."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from baixar_dpl_planalto import conferir_epigrafe


class EpigrafeDpl(unittest.TestCase):
    corpo = ('DECRETO Nº 4.182, DE 13 DE NOVEMBRO DE 1920.\n'
             'Art. 1º Ao fundo de garantia serão incorporados os recursos.\n'
             'Rio de Janeiro, 13 de novembro de 1920.')

    def test_ano_errado_do_indice_nao_define_identidade(self):
        with self.assertRaisesRegex(ValueError, 'Epígrafe própria diverge'):
            conferir_epigrafe({'numero': '4182', 'data': '1919-11-13'}, self.corpo)

    def test_identidade_propria_concordante(self):
        conferir_epigrafe({'numero': '4182', 'data': '1920-11-13'}, self.corpo)

    def test_numero_diferente_tambem_recusado(self):
        with self.assertRaisesRegex(ValueError, 'Epígrafe própria diverge'):
            conferir_epigrafe({'numero': '4183', 'data': '1920-11-13'}, self.corpo)


if __name__ == '__main__':
    unittest.main()
