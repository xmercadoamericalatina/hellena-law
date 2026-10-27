import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parent))
from verificar_entrega_ta_promocoes import verificar,sha


class Promocoes(unittest.TestCase):
    def fixture(self,folder):
        p=Path(folder);target=p/'destino.md';target.write_bytes(b'anterior');candidate=p/'candidato.md';candidate.write_bytes(b'novo')
        mapping=p/'mapa.json';mapping.write_text(json.dumps([dict(destino=str(target),sha256=sha(b'novo'),sha256_anterior=sha(b'anterior'),candidato=str(candidate))]))
        listing=p/'normas.txt';listing.write_text(str(target)+'\n')
        return dict(arquivos=[],mapeamento_fontes=str(mapping),normas_apos_promocao=str(listing),normas=1),target,candidate

    def test_pendente_nunca_e_publicavel_e_nao_altera_destino(self):
        with tempfile.TemporaryDirectory() as d:
            m,target,candidate=self.fixture(d);r=verificar(m)
            self.assertEqual(r['promocoes_pendentes'],1);self.assertEqual(r['problemas'],0)
            self.assertFalse(r['apto_para_publicacao']);self.assertEqual(target.read_bytes(),b'anterior')
            self.assertEqual(verificar(m,exigir_promocao=True)['problemas'],1)

    def test_preimagem_inesperada_e_rejeitada(self):
        with tempfile.TemporaryDirectory() as d:
            m,target,candidate=self.fixture(d);target.write_bytes(b'alheio');r=verificar(m)
            self.assertEqual(r['problemas'],1);self.assertEqual(target.read_bytes(),b'alheio')

    def test_promocao_ja_realizada_exige_sha_novo(self):
        with tempfile.TemporaryDirectory() as d:
            m,target,candidate=self.fixture(d);target.write_bytes(b'novo');r=verificar(m,exigir_promocao=True)
            self.assertEqual(r['promocoes_concluidas'],1);self.assertEqual(r['problemas'],0)
            self.assertFalse(r['apto_para_publicacao'])  # Hashes sem replay não certificam publicação.


if __name__=='__main__':unittest.main()
