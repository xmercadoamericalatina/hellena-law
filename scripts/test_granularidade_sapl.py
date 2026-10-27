"""Granularidade: referências não equivalem a epígrafes de outros atos."""
from pathlib import Path
import unittest
from granularidade_sapl import alertas_multiplos_atos, alertas_outras_publicacoes


class GranularidadeSAPLTest(unittest.TestCase):
    def test_aviso_edital_caceres_nao_exige_epigrafe_de_lei(self):
        s='Art.111. Outorga de concessão. EDITAL DISPONÍVEL NO SITE DA CÂMARA MUNICIPAL.\nABERTURA DA SESSÃO: dia15.'
        self.assertEqual(len(alertas_outras_publicacoes(s)),2)
        self.assertEqual(alertas_multiplos_atos(s,'Emenda à Lei Orgânica','52'),[])

    def test_referencia_generica_a_edital_nao_e_aviso_especifico(self):
        self.assertEqual(alertas_outras_publicacoes('Art.1º O edital da licitação observará os requisitos legais.'),[])
    def test_propria_epigrafe_repetida_e_pontuacao(self):
        s = 'EMENDA À LOMAN N. 121, DE 13 DE AGOSTO DE 2025\n\nEMENDA À LOMAN Nº 121/2025\n'
        self.assertEqual(alertas_multiplos_atos(s, 'Emenda à Loman', '121'), [])

    def test_referencias_corridas_e_citacoes_nao_sao_epigrafes(self):
        s = 'Conforme a LEI N° 1.265/2008 e a Portaria nº 65/2025.\n\n“LEI Nº 1.265/2008”\n\nA Lei Complementar Nacional nº 101/2000 estabelece limites.'
        self.assertEqual(alertas_multiplos_atos(s, 'Emenda à Lei Orgânica', '121'), [])

    def test_epigrafes_alheias_retem_sem_cortar(self):
        s = 'PORTARIA N° 065/2025\nNomeia servidor.\n\nLEI N. 1.265, DE 10 DE NOVEMBRO DE 2008\nArt. 1º Texto.\n\nPORTARIA N° 065/2025'
        r = alertas_multiplos_atos(s, 'Emenda à Lei Orgânica', '121')
        self.assertEqual([tuple(x['epigrafe_diversa']) for x in r], [('PORTARIA', '65'), ('LEI', '1265')])
        self.assertEqual(s[r[0]['posicao_no_corpo']:][:8], 'PORTARIA')

    def test_epigrafe_sem_marcador_numero_e_municipal(self):
        s = 'LEI MUNICIPAL 1.265, DE 10 DE NOVEMBRO DE 2008\n\nDECRETO MUNICIPAL Nº 65/2025'
        r = alertas_multiplos_atos(s, 'Lei', '1265')
        self.assertEqual([tuple(x['epigrafe_diversa']) for x in r], [('DECRETO', '65')])

    def test_manaus_121_anexo_real_quando_presente(self):
        p = Path(__file__).resolve().parent.parent / 'municipais/AM/manaus/emendas-lei-organica/2025/emendas-lei-organica-121-2025-sapl-8035.md'
        if not p.exists():
            self.skipTest('captura oficial local não distribuída no Git')
        s = p.read_text().split('\n---\n', 1)[1].lstrip('\n').split('\n\n', 1)[1]
        r = alertas_multiplos_atos(s, 'Emenda à Loman', '121')
        self.assertTrue(any(x['epigrafe_diversa'] == ('PORTARIA', '65') for x in r), r)
        self.assertTrue(all(x['epigrafe_diversa'] != ('EMENDA', '121') for x in r))


if __name__ == '__main__':
    unittest.main()
