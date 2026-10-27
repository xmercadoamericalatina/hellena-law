import copy
import gzip
import json
from pathlib import Path
import re
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from converter_organica_aracaju import preparar, ROOT, PLAN


class Aracaju(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = json.loads(gzip.decompress((ROOT/'municipais/_lotes/20261021-aracaju-lo/extracao-integral.json.gz').read_bytes()))
        cls.groups = json.loads((ROOT/PLAN).read_text())['grupos']

    def test_107_paginas_e_reversao_exata_dos_73_grupos(self):
        marked, proof = preparar(self.raw['layout_original'], self.raw['bbox'], self.groups)
        restored = re.sub(r'\n⟦(?:INÍCIO DO TRECHO TACHADO NA FONTE, página \d+, grupo \d+|FIM DO TRECHO TACHADO NA FONTE)⟧\n', '', marked)
        self.assertEqual(restored, self.raw['layout_original'])
        self.assertEqual(sum(p['grupos_marcados'] for p in proof), 73)
        self.assertEqual(sum(p['sequencia_layout_bbox'] for p in proof), 105)
        self.assertIn('Modificado pela Emenda à Lei Orgânica nº 72/2023', restored)

    def test_linha_numerica_removida_e_detectada(self):
        chunks = self.raw['layout_original'].split('\f')
        chunks[5] = chunks[5].replace('6\n', '\n', 1)
        self.assertNotEqual(chunks[5], self.raw['layout_original'].split('\f')[5])
        with self.assertRaises(ValueError):
            preparar('\f'.join(chunks), self.raw['bbox'], self.groups)

    def test_mesmo_multiconjunto_nao_autoriza_permutacao_visual(self):
        chunks = self.raw['layout_original'].split('\f')
        chunks[106] = chunks[106].replace('Davis', 'sDavi', 1)
        with self.assertRaisesRegex(ValueError, 'visualmente revista'):
            preparar('\f'.join(chunks), self.raw['bbox'], self.groups)

    def test_ocorrencia_ambigua_do_plano_fica_retida(self):
        groups = copy.deepcopy(self.groups)
        groups[0]['texto_normalizado'] = 'Art.'
        with self.assertRaisesRegex(ValueError, 'ocorrência única'):
            preparar(self.raw['layout_original'], self.raw['bbox'], groups)


if __name__ == '__main__':
    unittest.main()
