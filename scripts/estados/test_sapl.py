"""Regressões de identidade SAPL; não acessam a rede nem o acervo real."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import sapl


class IdentidadeSAPL(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        self.patch = patch.object(sapl, 'RAIZ_ESTADUAIS', str(self.raiz))
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.n = {'id': 42, 'numero': '39', 'ano': 2014, 'data': '2014-02-04',
                  'tipo': 6, 'texto_integral': 'https://example.test/oficial.pdf',
                  '__str__': 'Emenda 39'}
        self.tipos = {'6': 'EMENDA À CONSTITUIÇÃO'}
        self.pasta = self.raiz / 'AL/emendas-constitucionais/2014'
        self.pasta.mkdir(parents=True)
        self.antigo = self.pasta / 'emenda-constituicao-39-2014-id42.md'
        self.alias = self.pasta / 'emenda-a-constituicao-39-2014-id42.md'

    def gravar(self, caminho, meta=None, corpo='Art. 1º Texto'):
        meta = meta or sapl.identidade('AL', self.n, 'Emenda Constitucional')
        caminho.write_text('---\n' + '\n'.join(
            f'{k}: {json.dumps(v)}' for k, v in meta.items()) + '\n---\n# Emenda\n\n' + corpo)

    def test_slug_distinto_mesmo_id_pula_sem_rede(self):
        self.gravar(self.antigo)
        with patch.object(sapl.rede, 'get', side_effect=AssertionError('rede inesperada')):
            self.assertEqual(sapl.processar_factory('AL', self.tipos)(self.n), ('pulado', None))

    def test_id_diferente_nao_e_equivalente(self):
        self.gravar(self.pasta / 'emenda-constituicao-39-2014-id420.md')
        self.assertEqual(sapl.existentes('AL', 'emendas-constitucionais', self.n,
                                        'Emenda Constitucional'), [])

    def test_divergencias_registradas_sem_duplicar(self):
        for campo in ('fonte', 'uf', 'tipo', 'numero', 'data', 'arquivo'):
            with self.subTest(campo=campo):
                meta = sapl.identidade('AL', self.n, 'Emenda Constitucional')
                meta[campo] = 'divergente'
                self.gravar(self.antigo, meta)
                with patch.object(sapl.rede, 'get', side_effect=AssertionError('rede inesperada')):
                    status, erro = sapl.processar_factory('AL', self.tipos)(self.n)
                self.assertEqual(status, 'sem_texto')
                self.assertIn('identidade divergente', erro['motivo'])
                self.assertFalse(self.alias.exists())

    def reconciliar(self):
        with patch.object(sapl, 'indice', return_value={'tipos': self.tipos, 'normas': [self.n]}), contextlib.redirect_stdout(io.StringIO()):
            return sapl.reconciliar('AL', aplicar=True)

    def test_reconciliacao_preserva_limpeza_e_e_idempotente(self):
        self.gravar(self.antigo, corpo=r'Art. 1º Texto \_\_\_\_\_ PRESIDENTE')
        self.gravar(self.alias, corpo='Art. 1º Texto PRESIDENTE')
        self.assertEqual(len(self.reconciliar()), 1)
        self.assertFalse(self.alias.exists())
        self.assertIn('Texto PRESIDENTE', self.antigo.read_text())
        self.assertEqual(self.reconciliar(), [])
        self.assertEqual(len(list((self.raiz / 'AL/_fonte/auditorias').glob('*.json'))), 1)

    def test_corpo_divergente_nao_remove_nem_reescreve(self):
        self.gravar(self.antigo)
        original = self.antigo.read_bytes()
        self.gravar(self.alias, corpo='Art. 1º Outro texto')
        with self.assertRaisesRegex(ValueError, 'corpos divergentes'):
            self.reconciliar()
        self.assertEqual(self.antigo.read_bytes(), original)
        self.assertTrue(self.alias.exists())


if __name__ == '__main__':
    unittest.main()
