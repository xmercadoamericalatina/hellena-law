import unittest
import datetime as dt
import gzip
import tempfile
from pathlib import Path
from unittest.mock import patch
import revisar_metadata_cache_dou as revisao
from revisar_metadata_cache_dou import proposta


class PropostaTest(unittest.TestCase):
    def test_altera_apenas_metadata_sem_tocar_tabelas_ou_tachados(self):
        corpo = '\n# Ato\n\n<table><tr><td rowspan="2">Texto</td></tr></table>\n<del>Histórico</del>\n'
        raw = ('---\ntitulo: "Ato"\nrevogada: false\n---\n' + corpo).encode()
        novo = proposta(raw, 'a' * 64)
        self.assertTrue(novo.endswith(corpo.encode()))
        self.assertIn(b'revogada: null', novo)
        self.assertIn(('sha256_html_fonte: ' + 'a' * 64).encode(), novo)

    def test_prova_anterior_nao_e_sobrescrita(self):
        for campo in ('revogada: true', 'revogada: null\nsha256_html_fonte: ' + 'b' * 64):
            with self.subTest(campo=campo), self.assertRaises(ValueError):
                proposta(('---\n' + campo + '\n---\n# Ato\n').encode(), 'a' * 64)

    def test_retomada_preserva_preimagem_e_recusa_alteracao_manual(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            p = raiz / 'reguladores/ans/portarias/2026/ato.md'
            p.parent.mkdir(parents=True)
            original = b'---\nrevogada: false\n---\n# Ato\n\nTexto integral\n'
            p.write_bytes(original)
            fonte = raiz / 'reguladores/_fonte/ans/2026/ato.html.gz'
            fonte.parent.mkdir(parents=True)
            fonte.write_bytes(gzip.compress(b'<p>Texto integral</p>'))
            backups = raiz / 'backups'
            with patch.object(revisao, 'RAIZ', raiz), patch.object(revisao, 'conferir', return_value=({}, {})):
                revisao.revisar(p, backups, dt.date(2026, 10, 20), aplicar=False)
                self.assertEqual(p.read_bytes(), original)
                self.assertFalse(backups.exists())
                revisao.revisar(p, backups, dt.date(2026, 10, 20), aplicar=True)
                modificado = p.stat().st_mtime_ns
                registro = revisao.revisar(p, backups, dt.date(2026, 10, 20), aplicar=True)
                self.assertTrue(registro['retomado_backup'])
                self.assertEqual(p.stat().st_mtime_ns, modificado)
                self.assertEqual(gzip.decompress((backups / p.relative_to(raiz)).read_bytes()), original)
                manual = p.read_bytes() + b'Alteracao manual\n'
                p.write_bytes(manual)
                with self.assertRaisesRegex(ValueError, 'preservado'):
                    revisao.revisar(p, backups, dt.date(2026, 10, 20), aplicar=True)
                self.assertEqual(p.read_bytes(), manual)


if __name__ == '__main__':
    unittest.main()
