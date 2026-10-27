from pathlib import Path
import json
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from preservar_notas_fortaleza import reparar, ROOT, SOURCE


class TestNotasFortaleza(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / SOURCE).read_text()
        self.old = (ROOT / 'municipais/_lotes/20261020-fortaleza-notas-constitucionalidade/documento-anterior.md').read_text().split('\n---\n', 1)[1].lstrip('\n').split('\n\n', 1)[1]

    def test_tres_notas_literais_e_reversao_integral(self):
        new, notes = reparar(self.html, self.old)
        self.assertEqual([n['dispositivo'] for n in notes], ['art. 168, § 5º', 'art. 177, § 8º', 'art. 177, § 9º'])
        self.assertIn('0620174-36.2023.8.06.000.', notes[0]['texto_literal'])
        self.assertTrue(all('0010204-81.2011.8.06.0000.' in n['texto_literal'] for n in notes[1:]))
        for n in notes:
            new = new.replace('\n\n' + n['trecho_inserido'], '', 1)
        self.assertEqual(new, self.old)

    def test_preimagem_e_nota_ausente_nao_sao_aceitas(self):
        with self.assertRaises(ValueError):
            reparar(self.html, self.old + 'palavra adicional')
        with self.assertRaises(ValueError):
            reparar(self.html.replace('id="dn2710"', 'id="nota-ausente"'), self.old)


if __name__ == '__main__':
    unittest.main()
