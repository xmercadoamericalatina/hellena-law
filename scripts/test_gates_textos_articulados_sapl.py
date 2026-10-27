import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import datetime as dt
sys.path.insert(0, str(Path(__file__).resolve().parent))
import auditar_textos_articulados_sapl as gate
from converter_organica_fortaleza import converter


class TestGatesTA(unittest.TestCase):
    def run_gate(self, extra='', body='<p>Art. 1º Regra atual.</p>', annexes=None, number='1'):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            html = '<h1 class="page-header">Lei Ordinária nº 1, de 2 de março de 2026</h1>' + extra + '<div class="dptt"><div class="dtxt">' + body + '</div></div>'
            (root / 'fonte.html').write_text(html)
            text, _ = converter(html)
            (root / 'candidato.txt').write_text(text)
            norma = {'id': 9, 'tipo': 1, 'numero': number, 'data': '2026-03-02', 'ementa': 'Regra'}
            (root / 'norma.json').write_text(json.dumps(norma))
            row = {'host': 'sapl.exemplo.leg.br', 'ta_id': 8, 'metadado_norma': norma, 'metadado_ta': {'numero': number},
                   'prova_norma': {'arquivo': 'norma.json', 'sha256': gate.sha((root / 'norma.json').read_bytes())},
                   'prova_frontend': {'arquivo': 'fonte.html', 'sha256': gate.sha((root / 'fonte.html').read_bytes()), 'url_final': 'https://sapl.exemplo.leg.br/ta/8/text', 'content_type': 'text/html; charset=utf-8'},
                   'transcricao': 'candidato.txt', 'sha256_transcricao': gate.sha(text.encode())}
            with patch.object(gate, 'ROOT', root):
                return gate.conferir(row, {1: {'descricao': 'Lei Ordinária'}}, {'estado': 'indice_completo', 'anexos': annexes or []}, dt.date(2026, 10, 20))

    def test_valido_sem_anexos(self):
        self.assertEqual(self.run_gate()['anexos_proprios'], 0)

    def test_versao_futura_retida(self):
        with self.assertRaisesRegex(ValueError, 'futura'):
            self.run_gate(extra='<p>Vigência a partir de <b>1 de Janeiro de 2027</b></p>')

    def test_nota_externa_e_anexo_nao_podem_sumir(self):
        with self.assertRaisesRegex(ValueError, 'Nota fora'):
            self.run_gate(extra='<div class="dn"><ul><li>Nota de emenda.</li></ul></div>')
        with self.assertRaisesRegex(ValueError, 'Anexo'):
            self.run_gate(annexes=[{'norma': 9, 'anexo_arquivo': 'anexo.pdf'}])

    def test_tabela_e_cor_exigem_contexto(self):
        for body in ['<p>Art. 1º Regra.</p><table><tr><td>0</td></tr></table>', '<p style="color: red">Art. 1º Regra.</p>']:
            with self.assertRaises(ValueError):
                self.run_gate(body=body)

    def test_sufixo_literal_nao_aceita_numero_diferente(self):
        with self.assertRaisesRegex(ValueError, 'Epígrafe'):
            self.run_gate(number='1B')


if __name__ == '__main__':
    unittest.main()
