import unittest
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from auditar_colunas_sapl import analisar
class ColunasTest(unittest.TestCase):
 def test_portaria_e_lei_ordinaria_da_segunda_coluna(self):
  m={'tipo':'Emenda à Lei Orgânica','numero':'25','data':'2025-07-15'}
  for t in ['texto da emenda          PORTARIA Nº 745/2025\nNomeia servidora','Art.9º entra em vigor.         LEI ORDINÁRIA Nº 2.646, DE 31 DE DEZEMBRO DE 2025.']:
   self.assertIn('epigrafe_divergente_possivel',[a['regra'] for a in analisar(m,t)['alertas']])
 def test_data_clara_diverge_sem_alterar_meta(self):
  m={'tipo':'Emenda à Lei Orgânica','numero':'10','data':'2004-10-07'};r=analisar(m,'EMENDA N.º 10, DE 7 DE DEZEMBRO DE 2004\nÀ LEI ORGÂNICA')
  self.assertTrue(r['data_epigrafe_clara_conferida']);self.assertEqual(r['alertas'][0]['data_epigrafe'],'2004-12-07');self.assertEqual(m['data'],'2004-10-07')
 def test_arquivo_regimento_nao_e_emenda_individual(self):
  r=analisar({'tipo':'Emenda à Lei Orgânica','numero':'1'},'REGIMENTO INTERNO DA CÂMARA\nTexto revisado atéEmenda81/2022')
  self.assertEqual(r['alertas'][0]['regra'],'objeto_regimento_em_cadastro_de_emenda')
 def test_ausencia_de_data_nao_confirma_metadado(self):
  r=analisar({'tipo':'Lei','numero':'596','data':'2024-01-01'},'LEI Nº 596/2024\nArt.1º Texto')
  self.assertFalse(r['data_epigrafe_clara_conferida']);self.assertEqual(r['alertas'],[])
 def test_arapongas_epigrafe_longa_em_cadastro_de_lo(self):
  t='EMENDA À LEI ORGÂNICA DO MUNICÍPIO DE ARAPONGAS Nº. 01/2015\nDispõe sobre alteração do artigo36.\nArt.1º Oart.36passaavigorar.'
  r=analisar({'tipo':'Lei Orgânica','numero':'1','data':'2015-05-29'},t)
  self.assertIn('epigrafe_de_emenda_em_cadastro_de_lei_organica',[a['regra'] for a in r['alertas']])
 def test_nota_no_corpo_nao_reclassifica_lo(self):
  t='LEI ORGÂNICA DO MUNICÍPIO\nArt.1º Texto próprio.\nEMENDA À LEI ORGÂNICA Nº.1/2020'
  r=analisar({'tipo':'Lei Orgânica','numero':'1'},t)
  self.assertNotIn('epigrafe_de_emenda_em_cadastro_de_lei_organica',[a['regra'] for a in r['alertas']])
if __name__=='__main__':unittest.main()
