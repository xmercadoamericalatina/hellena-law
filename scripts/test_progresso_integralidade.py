import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from pendencias_integralidade import REGISTRO, carregar
from plano import Item
import progresso


class ProgressoTest(unittest.TestCase):
    def test_excesso_de_uma_serie_nao_preenche_lacuna_de_outra(self):
        a = Item('setor', 'a', 'federal/a', 2, 1, 'fonte')
        b = Item('setor', 'b', 'federal/b', 2, 1, 'fonte')
        desconhecida = Item('setor', 'c', 'federal/c', None, 1, 'fonte')
        self.assertEqual(progresso.totais([(a, 10), (b, 0), (desconhecida, 3)]), (13, 2, 4, 3))

    def test_pendente_preservado_fora_da_contagem_e_download_fora_do_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            subprocess.run(['git', 'init', '-q', tmp], check=True)
            pasta = raiz / 'federal/decretos'
            pasta.mkdir(parents=True)
            for nome in ('apto.md', 'pendente.md'):
                (pasta / nome).write_text('# Ato\n')
            registro = raiz / REGISTRO
            registro.parent.mkdir(parents=True)
            registro.write_text(json.dumps({'pendentes': [{'path': 'federal/decretos/pendente.md',
                'sha256_md': 'a' * 64, 'motivo': 'anexo pendente', 'evidencia': 'fonte oficial'}]}))
            subprocess.run(['git', 'add', '.'], cwd=raiz, check=True)
            (pasta / 'nao-publicado.md').write_text('# Outro\n')
            pendentes = carregar(raiz, True)
            item = Item('setor', 'decretos', 'federal/decretos', 10, 1, 'fonte')
            with patch.object(progresso, 'RAIZ', tmp), patch.object(progresso, 'PLANO', [item]):
                index, _ = progresso.medir_git(pendentes)
                worktree, _ = progresso.medir(pendentes)
            self.assertEqual(index[0][1], 1)
            self.assertEqual(worktree[0][1], 2)
            self.assertTrue((pasta / 'pendente.md').exists())


if __name__ == '__main__':
    unittest.main()
