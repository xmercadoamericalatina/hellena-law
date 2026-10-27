from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_contexto_completo_ta import ContextoCompleto


class TestContextoCompleto(unittest.TestCase):
    def parse(self, fragment):
        p = ContextoCompleto()
        p.feed('<div class="cp">' + fragment + '</div>')
        return p

    def test_nota_e_imagem_irmas_nao_podem_ser_omitidas(self):
        p = self.parse('<div class="dptt">Art. 1º Texto.</div><div class="dn">Nota própria.</div><div class="dpt-img"><img src="anexo.png"></div>')
        self.assertEqual(p.fora[0]['texto'], 'Nota própria.')
        self.assertEqual(len(p.media), 1)

    def test_historico_explicito_e_controles_da_interface(self):
        p = self.parse('<div class="desativado"><div class="dn">Nota histórica</div><img src="antiga.png"></div><div class="tipo-vigencias">TVL TVT</div><div class="dptt revogado">Art. 2º Revogado.</div>')
        self.assertFalse(p.fora)
        self.assertFalse(p.media)

    def test_nota_dentro_do_dispositivo_ja_contabilizada(self):
        p = self.parse('<div class="dptt">Art. 1º Texto.<a class="nota-alteracao">Redação dada pela Lei 2.</a></div>')
        self.assertFalse(p.fora)

    def test_ancestral_historico_e_dispositivo_fora_da_area(self):
        p = self.parse('<div class="desativado"><div class="dptt">Texto antigo sem classe própria.</div></div>')
        self.assertEqual(p.ativos_em_ancestral_historico, 1)
        self.assertEqual(p.cp_encontrados, 1)
        p.feed('<div class="dptt">Texto fora da área.</div>')
        self.assertEqual(p.dispositivos_fora_da_area, 1)


if __name__ == '__main__':
    unittest.main()
