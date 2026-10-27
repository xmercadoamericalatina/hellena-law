"""Recusa de acesso deve interromper a fonte, sem esgotar retries ou a fila."""
import unittest
from unittest.mock import Mock, patch
import urllib.error

import baixar_dou as dou


class RecusaDOU(unittest.TestCase):
    def tearDown(self):
        dou.ACESSO_RECUSADO.clear()

    def test_recusa_nao_repetida_nem_em_proximas_urls(self):
        for status in (401, 403, 429):
            with self.subTest(status=status):
                dou.ACESSO_RECUSADO.clear()
                erro = urllib.error.HTTPError('https://www.in.gov.br/teste', status, 'recusado', {}, None)
                with patch.object(dou.urllib.request, 'urlopen', side_effect=erro) as abrir:
                    with self.assertRaises(dou.AcessoHTTPRecusado):
                        dou.http('https://www.in.gov.br/teste', Mock())
                    with self.assertRaises(dou.AcessoHTTPRecusado):
                        dou.http('https://www.in.gov.br/outra', Mock())
                self.assertEqual(abrir.call_count, 1)


if __name__ == '__main__':
    unittest.main()
