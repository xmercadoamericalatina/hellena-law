"""Atualizar a descoberta não deve apagar capturas nem regravar texto idêntico."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import baixar_jurisprudencia as coletor


class SemEspera:
    def esperar(self):
        pass


class AtualizacaoBNPTest(unittest.TestCase):
    def test_nova_versao_preserva_antiga_e_consulta_identica_nao_regrava(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(coletor, 'RAIZ', tmp):
            cache = Path(tmp) / '_fonte/bnp/tnu-uniformizacao-todos/pagina-1.json'
            cache.parent.mkdir(parents=True)
            anterior = {'id': 'tnu-1', 'orgao': 'TNU', 'tipo': 'PUIL', 'nr': 1, 'tese': 'Tese original', 'situacao': 'Ativo'}
            cache.write_text(json.dumps({'resultados': [anterior], 'total': 1}))
            bruto_antigo = cache.read_bytes()
            self.assertEqual(coletor.bnp_stf(SemEspera(), tribunal='TNU')['ok'], 1)
            path = Path(tmp) / 'tnu/uniformizacao/puil-1.md'
            novo = {**anterior, 'tese': 'Tese atualizada'}
            resposta = json.dumps({'resultados': [novo], 'total': 1}).encode()
            with patch.object(coletor.urllib.request, 'urlopen', return_value=io.BytesIO(resposta)):
                self.assertEqual(coletor.bnp_stf(SemEspera(), tribunal='TNU', atualizar_indice=True)['ok'], 1)
            corpo = path.read_bytes()
            self.assertIn(b'Tese original', corpo)
            self.assertIn(b'Tese atualizada', corpo)
            snapshots = [p.read_bytes() for p in (Path(tmp) / '_fonte/bnp-capturas').glob('*.json')]
            self.assertIn(bruto_antigo, snapshots)
            self.assertIn(resposta, snapshots)
            with patch.object(coletor.urllib.request, 'urlopen', return_value=io.BytesIO(resposta)):
                resultado = coletor.bnp_stf(SemEspera(), tribunal='TNU', atualizar_indice=True)
            self.assertEqual(resultado, {'ok': 0, 'pulado': 1})
            self.assertEqual(corpo, path.read_bytes())


if __name__ == '__main__':
    unittest.main()
