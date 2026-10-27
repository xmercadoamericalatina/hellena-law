import hashlib,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from conferir_tabelas_nativas_ta import conferir
from verificar_entrega_ta_sem_promocoes_v2 import verificar

class TestVerificadorTabelas(unittest.TestCase):
 def fixture(self,root,span='2',proof=True):
  original='<table><tr><th colspan="2">Órgão</th></tr><tr><td>0</td><td>R$ -1,50</td></tr></table>';body=original.replace('colspan="2"','colspan="'+span+'"');html='<div class="dptt" id="1">'+original+'</div>';source=root/'fonte.html';source.write_text(html);md=root/'norma.md';md.write_text('---\nsha256_texto: '+json.dumps(hashlib.sha256(body.encode()).hexdigest())+'\n---\n\n# Lei\n\n'+body+'\n');row=dict(path=str(md),sha256=hashlib.sha256(md.read_bytes()).hexdigest(),fonte=dict(arquivo=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
  if proof:row['prova_tabelas']=conferir(html,original)
  mapping=root/'mapa.json';mapping.write_text(json.dumps([row]));lst=root/'lista.txt';lst.write_text(str(md)+'\n');manifest=root/'manifesto.json';manifest.write_text(json.dumps(dict(normas=1,mapeamento_fontes=str(mapping),lista_normas=str(lst),arquivos=[dict(arquivo=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in [md,source,mapping,lst]])));return manifest
 def test_tabela_e_zero_preservados(self):
  with tempfile.TemporaryDirectory() as temp:self.assertTrue(verificar(self.fixture(Path(temp)),True)['apto_para_publicacao'])
 def test_mesmos_caracteres_mas_mesclagem_errada(self):
  with tempfile.TemporaryDirectory() as temp:
   result=verificar(self.fixture(Path(temp),span='1'),True);self.assertFalse(result['apto_para_publicacao']);self.assertIn('mesclagens',str(result['detalhes']))
 def test_prova_ausente_retida(self):
  with tempfile.TemporaryDirectory() as temp:
   result=verificar(self.fixture(Path(temp),proof=False),True);self.assertFalse(result['apto_para_publicacao']);self.assertIn('sem prova estrutural',str(result['detalhes']))
if __name__=='__main__':unittest.main()
