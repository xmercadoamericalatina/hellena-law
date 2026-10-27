import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from marcar_tachados_sapl_revisados import marcar, mapa_normalizado


class TestMarcar(unittest.TestCase):
    def test_formato_preservado_e_nota_fora_do_tachado(self):
        body = '**Art. 1º** Texto antigo.\n(Revogado com efeitos condicionados.)\nTexto sucessor.\n'
        needle = mapa_normalizado('Art. 1º Texto antigo.')[0]
        out, spans = marcar(body, [{'texto_normalizado': needle, 'pagina': 3, 'grupo': 1}])
        self.assertIn('FIM DO TRECHO TACHADO NA FONTE⟧\n(Revogado com efeitos condicionados.)', out)
        self.assertIn('Texto sucessor.', out)
        self.assertEqual(len(spans), 1)

    def test_nao_escolhe_entre_ocorrencias_repetidas(self):
        with self.assertRaises(ValueError):
            marcar('Texto. Texto.', [{'texto_normalizado': 'Texto.', 'pagina': 1, 'grupo': 1}])

    def test_sobreposicao_retida(self):
        with self.assertRaises(ValueError):
            marcar('Texto anterior.', [{'texto_normalizado': 'Textoanterior.', 'pagina': 1, 'grupo': 1},
                                      {'texto_normalizado': 'anterior.', 'pagina': 1, 'grupo': 2}])


if __name__ == '__main__':
    unittest.main()
