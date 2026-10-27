import unittest
from recuperar_integralidade_pdf_sapl import reconstruir_md
from auditar_municipal import metadados
import hashlib

class RecuperacaoPDFTest(unittest.TestCase):
    def test_reconstroi_valores_isolados_sem_renumerar_ou_remover_cabecalho(self):
        old='---\ntitulo: "Lei1"\nversao_texto: "original"\nsha256_texto: "antigo"\n---\n\n# Lei1\n\nArt.1 Texto truncado\n'
        raw='1\nCÂMARA MUNICIPAL\nArt. 1º Valores\n26\n0\n\f2\nContinuação\n137\n'
        new,corpo=reconstruir_md(old,raw)
        self.assertIn('\n26\n0\n',corpo);self.assertIn('137',corpo);self.assertIn('CÂMARA MUNICIPAL',corpo)
        self.assertEqual(metadados(new)['sha256_texto'],hashlib.sha256(corpo.encode()).hexdigest())
        self.assertEqual(new.split('\n---\n')[1].lstrip('\n').split('\n\n',1)[1].rstrip('\n'),corpo)
    def test_marcador_inesperado_na_fonte_requer_revisao(self):
        with self.assertRaises(ValueError):reconstruir_md('---\n---\n\n# X\n\nY','texto ``` conteúdo')

if __name__=='__main__':unittest.main()
