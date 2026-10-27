"""As chaves de proveniência com dígitos precisam participar da auditoria."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from auditar_municipal import metadados

SCRIPT = Path(__file__).resolve().parent / "auditar_municipal.py"


class HashesMunicipaisTest(unittest.TestCase):
    def test_parser_preserva_chaves_sha256(self):
        d = metadados('---\nsha256_texto: "abc"\nsha256_fonte: "def"\ncodigo_ibge: "123"\n---\n')
        self.assertEqual(d["sha256_texto"], "abc")
        self.assertEqual(d["sha256_fonte"], "def")

    def test_corpo_adulterado_e_retido_pela_cli_sem_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            original = "Art. 1º Texto original."
            meta = {"municipio": "Cidade", "uf": "SP", "codigo_ibge": "123",
                    "fonte": "https://sapl.cidade.sp.leg.br/norma/1", "sha256_texto": hashlib.sha256(original.encode()).hexdigest()}
            p = raiz / "municipais/SP/cidade/leis-ordinarias/2000/lei-sapl-1.md"
            p.parent.mkdir(parents=True)
            cab = '---\n' + '\n'.join(k + ': ' + json.dumps(v) for k, v in meta.items()) + '\n---\n\n# Lei\n\n'
            p.write_text(cab + original + '\n')
            ibge = raiz / "ibge.json"
            ibge.write_text(json.dumps([{"id": 123, "nome": "Cidade", "regiao-imediata": {"regiao-intermediaria": {"UF": {"sigla": "SP"}}}}]))
            lista = raiz / "lista.txt"
            lista.write_text(str(p.relative_to(raiz)) + '\n')
            saida = raiz / "auditoria.json"
            cmd = [sys.executable, '-I', str(SCRIPT), '--raiz', str(raiz), '--lista', str(lista), '--ibge', str(ibge), '--saida', str(saida)]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            p.write_text(cab + "Art. 1º Texto adulterado.\n")
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 1)
            self.assertIn('hash do corpo diverge', saida.read_text())


if __name__ == '__main__':
    unittest.main()
