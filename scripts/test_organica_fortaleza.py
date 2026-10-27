"""Texto articulado: versões desativadas e tachados não aparecem como atuais."""
import unittest
from pathlib import Path
from converter_organica_fortaleza import converter


class TextoArticuladoTest(unittest.TestCase):
    def test_desativado_sai_revogado_permanece_e_nota_preservada(self):
        h='<div class="dptt desativado" id="a"><a>V</a><div class="dtxt">Regra anterior</div></div><div class="dptt" id="b"><a>V</a><div class="dtxt">Regra atual</div><a class="nota-alteracao">Alteração feita pela Emenda16.</a></div><div class="dptt revogado" id="c">Art.17. (Revogado)</div>'
        m,p=converter(h)
        self.assertNotIn('Regra anterior',m)
        self.assertIn('Regra atual',m)
        self.assertIn('Alteração feita pela Emenda16.',m)
        self.assertIn('(Revogado)',m)
        self.assertEqual(len(p.historicos),1)

    def test_tachado_interno_gera_nota_e_nao_redacao_atual(self):
        m,p=converter('<div class="dptt" id="a">§5º <span style="text-decoration: line-through">Regra histórica</span></div>')
        self.assertNotIn('Regra histórica',m)
        self.assertIn('Nota editorial',m)
        self.assertTrue(p.ativos[0]['tachado_interno_omitido'])

    def test_fortaleza_real_quando_cache_disponivel(self):
        p=Path(__file__).resolve().parent.parent/'municipais/_fonte/capitais/fortaleza/lei-organica-2006-sapl44.html'
        if not p.exists():self.skipTest('captura oficial não distribuída')
        m,parsed=converter(p.read_text())
        self.assertNotIn('de quinhentos habitantes por unidade',m)
        self.assertIn('trezentos e vinte e cinco habitantes por unidade',m)
        self.assertEqual(len(parsed.historicos),127)
        self.assertEqual(sum(x['tachado_interno_omitido'] for x in parsed.ativos),3)
        self.assertIn('(Revogado)',m)


if __name__=='__main__':unittest.main()
