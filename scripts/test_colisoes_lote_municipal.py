import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_colisoes_lote_municipal import keys


def text(**meta):
    return '\n'.join(['---']+[k+': '+json.dumps(v) for k,v in meta.items()]+['---'])


class Colisoes(unittest.TestCase):
    def test_acervo_sem_ibge_ainda_colide_pela_rota(self):
        old = text(tipo='Lei', numero='1.234-A', data='2020-01-01')
        new = text(tipo='Lei ordinária', numero='1234A', data='2020-02-01', codigo_ibge='1100205')
        p = 'municipais/RO/porto-velho/leis-ordinarias/2020/a.md'
        self.assertTrue(set(keys(old,p)) & set(keys(new,p)))

    def test_sufixo_numerico_e_preservado(self):
        p = 'municipais/RO/porto-velho/leis-ordinarias/2020/a.md'
        self.assertFalse(set(keys(text(tipo='Lei',numero='1B',data='2020-01-01'),p)) &
                         set(keys(text(tipo='Lei',numero='1',data='2020-01-01'),p)))

    def test_url_igual_em_dois_campos_nao_autocolide(self):
        k = keys(text(fonte='https://example.gov.br/norma/1/',fonte_texto='https://example.gov.br/norma/1'), 'municipais/RO/porto-velho/a.md')
        self.assertEqual(len(k),1)


if __name__ == '__main__':
    unittest.main()
