import sys
from pathlib import Path
import unittest
import json
sys.path.insert(0, str(Path(__file__).resolve().parent))
from preparar_reparos_commonmark_ta6 import CASES, ROOT, preparar, reparar, sha
from auditar_municipal import metadados


class ReparosPrivados(unittest.TestCase):
    def test_seis_casos_reais_replay_integral_e_canonico_intacto(self):
        for case in CASES:
            with self.subTest(destino=case[1]):
                before = (ROOT/case[1]).read_bytes()
                archived = json.loads((ROOT/'municipais/_lotes/20261021-reparos-commonmark-ta6/promocoes.json').read_text())
                evidence = next(r for r in archived if r['destino'] == case[1])
                preimage = (ROOT/evidence['backup']).read_bytes()
                old, new, result = preparar(case, preimage=preimage)
                self.assertEqual(sha(old), evidence['sha256_anterior'])
                self.assertEqual(sha(new), evidence['sha256_novo'])
                self.assertEqual((ROOT/case[1]).read_bytes(), before)
                self.assertFalse(result['replay_anterior']['aprovado'])
                self.assertTrue(result['replay']['aprovado'])
                self.assertTrue(result['replay']['assinatura_numerica_confere'])
                self.assertNotEqual(sha(old), sha(new))
                a, b = metadados(old.decode()), metadados(new.decode())
                a.pop('sha256_texto'); b.pop('sha256_texto')
                self.assertEqual(a, b)

    def test_hifen_numerico_nao_e_consumido(self):
        text = '- Item 0;\nValor: -5,00;\n-50 não é lista.\n'
        fixed, n = reparar(text, 'hífens')
        self.assertEqual(n, 1)
        self.assertEqual(fixed, '\\- Item 0;\nValor: -5,00;\n-50 não é lista.\n')

    def test_negrito_move_somente_delimitador_e_preserva_espacos(self):
        fixed, n = reparar('**Pessoa –**cargo; **Nome-**suplente.', 'negrito_travessão')
        self.assertEqual(n, 2)
        self.assertEqual(fixed, '**Pessoa** –cargo; **Nome**-suplente.')
        with self.assertRaisesRegex(ValueError, 'vazio'):
            reparar('**Pessoa** – cargo.', 'negrito_travessão')


if __name__ == '__main__':
    unittest.main()
