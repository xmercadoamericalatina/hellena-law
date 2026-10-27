import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from materializar_textos_articulados_sapl_v2 import dia_captura


class DataCaptura(unittest.TestCase):
    def test_offset_utc_converte_dia_recife(self):
        self.assertEqual(dia_captura('2026-10-21T02:59:59+00:00'), ('2026-10-20', 'America/Recife'))
        self.assertEqual(dia_captura('2026-10-21T03:00:00Z'), ('2026-10-21', 'America/Recife'))

    def test_offset_local_e_timestamp_sem_offset(self):
        self.assertEqual(dia_captura('2026-10-20T23:59:59-03:00'), ('2026-10-20', 'America/Recife'))
        day, zone = dia_captura('2026-10-21T00:00:01.125')
        self.assertEqual(day, '2026-10-21')
        self.assertIn('não informado', zone)

    def test_timestamp_invalido_nao_adota_data_de_hoje(self):
        with self.assertRaises(ValueError):
            dia_captura('sem prova')


if __name__ == '__main__':
    unittest.main()
