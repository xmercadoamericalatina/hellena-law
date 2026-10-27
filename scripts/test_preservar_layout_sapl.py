from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from preservar_layout_integral_sapl import confrontar


class TestLayoutIntegral(unittest.TestCase):
    def test_zero_celula_e_folio_preservados(self):
        bbox = '<doc><page><word>Item</word><word>Valor</word><word>A</word><word>0</word><word>1</word></page><page/></doc>'
        self.assertEqual(confrontar('Item   Valor\nA      0\n1\f\f', bbox), (2, 5))
        with self.assertRaisesRegex(ValueError, 'palavras'):
            confrontar('Item Valor\nA\n1\f\f', bbox)

    def test_folha_vazia_nao_pode_desaparecer(self):
        with self.assertRaisesRegex(ValueError, 'física'):
            confrontar('Texto\f', '<doc><page><word>Texto</word></page><page/></doc>')

    def test_camada_vazia_nao_confirma_ocr(self):
        with self.assertRaisesRegex(ValueError, 'OCR'):
            confrontar('\f', '<doc><page/></doc>')


if __name__ == '__main__':
    unittest.main()
