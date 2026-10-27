import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from retomar_fila_ta_sigi import selecionar
class TestRetomada(unittest.TestCase):
 def test_so_interrupcao_sem_erro(self):
  state={'sapl.a.leg.br':dict(estado='iniciado; não repetir automaticamente',vinculo_sigi={'host':'sapl.a.leg.br'})};self.assertEqual(len(selecionar(state,['sapl.a.leg.br'])),1)
  for key,value in [('fim','2026-10-21'),('erro','HTTP 429')]:
   state['sapl.a.leg.br'][key]=value
   with self.assertRaises(ValueError):selecionar(state,['sapl.a.leg.br'])
   del state['sapl.a.leg.br'][key]
 def test_host_vinculo_e_repeticao(self):
  state={'sapl.a.leg.br':dict(estado='iniciado; não repetir automaticamente',vinculo_sigi={'host':'sapl.b.leg.br'})}
  with self.assertRaises(ValueError):selecionar(state,['sapl.a.leg.br'])
  with self.assertRaises(ValueError):selecionar(state,['sapl.a.leg.br']*2)
if __name__=='__main__':unittest.main()
