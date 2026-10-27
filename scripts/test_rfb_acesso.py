"""Não continua a fila SIJUT após recusa HTTP ou limite de taxa."""
import unittest
from urllib.error import HTTPError

from baixar_rfb import acesso_recusado


class RecusaRFB(unittest.TestCase):
    def test_status_de_recusa_interrompem(self):
        for status in (401, 403, 429):
            with self.subTest(status=status):
                self.assertTrue(acesso_recusado(HTTPError('https://example.invalid', status, 'recusa', {}, None)))
                self.assertTrue(acesso_recusado(RuntimeError('HTTP ' + str(status) + ': fonte')))

    def test_numero_no_id_nao_e_status_http(self):
        self.assertFalse(acesso_recusado(ValueError('ato 429: fonte não declara texto íntegro e público')))

    def test_falha_transitoria_nao_e_recusa(self):
        self.assertFalse(acesso_recusado(RuntimeError('HTTP 502: gateway')))


if __name__ == '__main__':
    unittest.main()
