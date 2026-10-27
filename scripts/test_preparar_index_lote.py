"""Empacotar dados pode alterar somente as entradas explicitamente auditadas."""
import hashlib
from pathlib import Path
import subprocess
import tempfile
import unittest

from preparar_index_lote import preparar


class IndexLote(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        subprocess.run(['git', 'init', '-q', self.tmp.name], check=True)
        (self.root / 'norma.md').write_text('---\ntexto de prova\n')
        (self.root / 'alheio.txt').write_text('alteração alheia preservada\n')
        subprocess.run(['git', 'add', 'alheio.txt'], cwd=self.root, check=True)

    def test_pack_sem_refs_e_sem_alterar_outros_arquivos_ou_index(self):
        raw = (self.root / 'norma.md').read_bytes()
        anterior = subprocess.check_output(['git', 'ls-files', '--stage', 'alheio.txt'], cwd=self.root)
        resultado = preparar(self.root, ['norma.md'], True, {'norma.md': hashlib.sha256(raw).hexdigest()})
        self.assertTrue(resultado['aplicado'])
        self.assertEqual(subprocess.check_output(['git', 'show', ':norma.md'], cwd=self.root), raw)
        self.assertEqual(subprocess.check_output(['git', 'ls-files', '--stage', 'alheio.txt'], cwd=self.root), anterior)
        self.assertEqual((self.root / 'norma.md').read_bytes(), raw)
        self.assertEqual(subprocess.run(['git', 'show-ref'], cwd=self.root, capture_output=True).returncode, 1)

    def test_simulacao_nao_altera_index(self):
        preparar(self.root, ['norma.md'])
        self.assertEqual(subprocess.check_output(['git', 'ls-files', '--', 'norma.md'], cwd=self.root), b'')

    def test_hash_alterado_nao_entra_no_index(self):
        with self.assertRaisesRegex(ValueError, 'hash difere'):
            preparar(self.root, ['norma.md'], True, {'norma.md': '0'*64})
        self.assertEqual(subprocess.check_output(['git', 'ls-files', '--', 'norma.md'], cwd=self.root), b'')

    def test_filtros_nao_sao_ignorados(self):
        (self.root / '.gitattributes').write_text('*.md text\n')
        with self.assertRaisesRegex(ValueError, 'git add convencional'):
            preparar(self.root, ['norma.md'], True)


if __name__ == '__main__':
    unittest.main()
