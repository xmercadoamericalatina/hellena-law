import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fila_textos_articulados_sapl import candidatos, validar_casa


class FilaTA(unittest.TestCase):
    def setUp(self):
        self.item = dict(url='https://sapl.erechim.rs.leg.br/', municipio='Erechim', uf='RS', codigo_ibge='4307005')

    def test_nao_repete_portal_ja_iniciado(self):
        self.assertEqual(candidatos([self.item], {'sapl.erechim.rs.leg.br'}), [])

    def test_deduplica_mesma_identidade_e_retém_vinculos_conflitantes(self):
        self.assertEqual(len(candidatos([self.item, dict(self.item)], set())), 1)
        self.assertEqual(candidatos([self.item, dict(self.item, codigo_ibge='1')], set()), [])

    def test_rota_ou_dominio_nao_autorizado_nao_entra(self):
        self.assertEqual(candidatos([dict(self.item, url='https://sapl.erechim.rs.leg.br/subrota'), dict(self.item, url='https://exemplo.com')], set()), [])

    def test_casa_de_outro_municipio_rejeitada_antes_dos_corpos(self):
        with self.assertRaisesRegex(ValueError, 'não corresponde'):
            validar_casa(dict(results=[dict(municipio='Rio Branco', uf='AC')]), self.item)
        with self.assertRaisesRegex(ValueError, 'ambígua'):
            validar_casa(dict(results=[]), self.item)

    def test_ibge_oficial_e_casa_compativeis(self):
        self.assertEqual(validar_casa(dict(results=[dict(municipio='Erechim', uf='RS')]), self.item)['municipio'], 'Erechim')
        with self.assertRaisesRegex(ValueError, 'IBGE divergente'):
            validar_casa(dict(results=[dict(municipio='Erechim', uf='RS')]), dict(self.item, codigo_ibge='4307006'))


if __name__ == '__main__':
    unittest.main()
