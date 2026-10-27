import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from conferir_tabelas_nativas_ta import conferir
class TestTabelas(unittest.TestCase):
 def test_zero_sinais_mesclagem_e_ordem(self):
  table='<table><tbody><tr><th colspan="2">Órgão</th></tr><tr><td>0</td><td>R$ -1.234,50</td></tr></tbody></table>';source='<div class="dptt" id="1">'+table+'</div>';self.assertEqual(conferir(source,table)['tabelas'],1)
  for bad in [table.replace('>0<','><'),table.replace('-1.234,50','1.234,50'),table.replace('colspan="2"','colspan="1"'),table.replace('<td>0</td><td>R$ -1.234,50</td>','<td>R$ -1.234,50</td><td>0</td>')]:
   with self.assertRaises(ValueError):conferir(source,bad)
 def test_historico_e_apresentacao_retidos(self):
  table='<table><tr><td>Atual 0</td></tr></table>';source='<div class="dptt desativado">'+table.replace('Atual','Antigo')+'</div><div class="dptt">'+table+'</div>';self.assertEqual(conferir(source,table)['tabelas'],1)
  for bad in [table.replace('<td>','<td style="color:red">'),table.replace('<td>','<td bgcolor="red">'),table.replace('<td>','<td class="revogado">'),table.replace('Atual','<s>Atual</s>'),table.replace('Atual','<img src="x">Atual'),table.replace('Atual',table)]:
   with self.assertRaises(ValueError):conferir('<div class="dptt">'+bad+'</div>',bad)
if __name__=='__main__':unittest.main()
