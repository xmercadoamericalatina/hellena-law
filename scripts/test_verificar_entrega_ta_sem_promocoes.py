import hashlib,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from verificar_entrega_ta_sem_promocoes import verificar

class TestEntrega(unittest.TestCase):
    def fixture(self,root):
        body='Art. 1º. O valor é R$ 1.234,50; prazo: 2 dias.';md=root/'norma.md';md.write_text('---\nsha256_texto: '+json.dumps(hashlib.sha256(body.encode()).hexdigest())+'\n---\n\n# Lei\n\n'+body+'\n');source=root/'fonte.html';source.write_text('<div class="dptt" id="d1"><p>'+body+'</p></div>');mapping=root/'mapa.json';mapping.write_text(json.dumps([dict(path=str(md),sha256=hashlib.sha256(md.read_bytes()).hexdigest(),fonte=dict(arquivo=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest()))]));lst=root/'normas.txt';lst.write_text(str(md)+'\n');manifest=root/'manifesto.json';manifest.write_text(json.dumps(dict(normas=1,mapeamento_fontes=str(mapping),lista_normas=str(lst),arquivos=[dict(arquivo=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in [md,source,mapping,lst]])));return manifest,md
    def test_replay_exato_e_sem_replay_nao_apto(self):
        with tempfile.TemporaryDirectory() as temp:
            path,_=self.fixture(Path(temp));self.assertTrue(verificar(path,True)['apto_para_publicacao']);self.assertFalse(verificar(path)['apto_para_publicacao'])
    def test_tamper_numero_e_cardinalidade_retidos(self):
        with tempfile.TemporaryDirectory() as temp:
            path,md=self.fixture(Path(temp));md.write_text(md.read_text().replace('1.234,50','1.234,51'));result=verificar(path,True);self.assertFalse(result['apto_para_publicacao']);self.assertGreater(result['problemas'],0)
            d=json.loads(path.read_text());d['normas']=2;path.write_text(json.dumps(d));self.assertTrue(any('cardinalidade' in x['erro'] for x in verificar(path)['detalhes']))

if __name__=='__main__':unittest.main()
