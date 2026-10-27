import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_commonmark_ta_v2 import comparar


def source(s):
    return '<div class="cp"><div class="dptt">'+s+'</div></div>'


class HeadingTA(unittest.TestCase):
    def test_heading_com_limites_html_sem_espaco_literal(self):
        result = comparar(source('<b>CAPÍTULO II</b><b>DA COMPOSIÇÃO</b>'), '### CAPÍTULO II — DA COMPOSIÇÃO')
        self.assertTrue(result['aprovado'])
        self.assertEqual(len(result['normalizacoes_heading']), 1)

    def test_travessao_literal_e_sinal_de_valor_nao_sao_removidos(self):
        self.assertTrue(comparar(source('CAPÍTULO II — DA COMPOSIÇÃO'), '### CAPÍTULO II — DA COMPOSIÇÃO')['aprovado'])
        self.assertFalse(comparar(source('CAPÍTULO II — DA COMPOSIÇÃO'), '### CAPÍTULO II DA COMPOSIÇÃO')['aprovado'])
        self.assertFalse(comparar(source('CAPÍTULO II DA COMPOSIÇÃO R$ −2,00'), '### CAPÍTULO II — DA COMPOSIÇÃO R$ 2,00')['aprovado'])


if __name__ == '__main__':
    unittest.main()
