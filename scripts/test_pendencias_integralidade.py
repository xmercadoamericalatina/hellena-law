import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from pendencias_integralidade import REGISTRO, carregar


class RegistroTest(unittest.TestCase):
    def test_index_nao_le_registro_ainda_nao_publicado(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            subprocess.run(['git', 'init', '-q', tmp], check=True)
            p = raiz / REGISTRO
            p.parent.mkdir(parents=True)
            item = {'path': 'federal/decretos/1945/ato.md', 'sha256_md': hashlib.sha256(b'ato').hexdigest(),
                    'motivo': 'anexo próprio ausente', 'evidencia': 'fonte oficial e trecho preservados'}
            p.write_text(json.dumps({'pendentes': [item]}))
            self.assertEqual(carregar(raiz, True), {})
            subprocess.run(['git', 'add', REGISTRO], cwd=raiz, check=True)
            p.write_text(json.dumps({'pendentes': []}))
            self.assertEqual(list(carregar(raiz, True)), [item['path']])
            self.assertEqual(carregar(raiz), {})

    def test_recusa_registro_ambiguo_ou_sem_evidencia(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / REGISTRO
            p.parent.mkdir(parents=True)
            item = {'path': '../fora.md', 'sha256_md': 'a' * 64, 'motivo': 'pendente', 'evidencia': 'fonte'}
            for entradas in ([item], [{**item, 'path': 'federal/a.md', 'evidencia': ''}],
                             [{**item, 'path': 'federal/a.md'}] * 2):
                p.write_text(json.dumps({'pendentes': entradas}))
                with self.subTest(entradas=entradas), self.assertRaises(ValueError):
                    carregar(Path(tmp))


if __name__ == '__main__':
    unittest.main()
