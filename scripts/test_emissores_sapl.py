import unittest
from auditar_emissores_sapl import analisar
class EmissoresTest(unittest.TestCase):
 def test_erros_reais_de_outro_municipio(self):
  nomes=['Cambira','Cambará','Tomazina','Pinhalão','Ibaiti']
  for text,own,other in [('Câmara Municipal de Cambara compõe-se','Cambira','cambara'),('A Câmara Municipal de Pinhalão aprovou','Tomazina','pinhalao'),('documentação com a Câmara Municipal de Ibaiti.','Tomazina','ibaiti')]:
   self.assertEqual(analisar(text,own,nomes)[0]['municipio_no_cabecalho_normalizado'],other)
 def test_hifen_acentos_e_vereadores_do_proprio_municipio(self):
  self.assertEqual(analisar('PREFEITURA MUNICIPAL DE CERRO-CORÁ\nCâmara Municipal de Vereadores de Cerro Corá.','Cerro Corá',['Cerro Corá']),[])
 def test_projeto_generico_nao_e_nome_de_municipio(self):
  self.assertEqual(analisar('apresentação à Câmara Municipal de projeto de lei','Luz',['Luz','Alegre']),[])
if __name__=='__main__':unittest.main()
