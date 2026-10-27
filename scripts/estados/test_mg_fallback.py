import gzip
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import mg


class RetomadaMG(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        self.md = self.raiz / 'decreto.md'
        self.original = '---\ntitulo: "Decreto 1"\n---\n# Decreto 1\n\n\n'
        self.md.write_text(self.original)
        self.r = {'Tipo': 'DEC', 'Numero': '1', 'Ano': '2026', 'Complemento': '', 'DataLegislacao': '01/01/2026', 'Ementa': 'Teste', 'Situacao': 'Vigente', 'LinkTextoAtualizado': '', 'LinkTextoOriginal': 'https://dadosabertos.almg.gov.br/api/v2/documento-original'}
        self.patches = [patch.object(mg, 'RAIZ_ESTADUAIS', str(self.raiz)), patch.object(mg, 'caminhos', return_value=(str(self.md), str(self.raiz / 'fonte.html.gz')))]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)
        mg.bloqueado.clear()

    def test_md_vazio_retoma_apos_paragrafo_xml_vazio(self):
        xml = b'<root><conteudo><![CDATA[<p></p>]]></conteudo></root>'
        pagina = b'<html><span class="textNorma"><p>O Governador decreta:</p><p>Art. 1 Fica criado o programa de teste.</p></span></html>'
        with patch.object(mg.rede, 'get', side_effect=[(200, xml, 'application/xml'), (200, pagina, 'text/html')]) as get, patch.object(mg, 'gravar') as gravar:
            self.assertEqual(mg.processar(self.r), ('ok', None))
        self.assertEqual(get.call_count, 2)
        self.assertIn('Art. 1', gravar.call_args.args[4])
        self.assertEqual(dict(gravar.call_args.args[3])['versao_texto'], 'original')
        backup = self.raiz / 'MG/_fonte/auditorias/reparos-vazios/dec-1-2026.md.gz'
        self.assertEqual(gzip.decompress(backup.read_bytes()).decode(), self.original)

    def test_texto_atualizado_nao_e_substituido_pelo_original(self):
        self.r['LinkTextoAtualizado'] = 'https://dadosabertos.almg.gov.br/api/v2/documento-atualizado'
        xml = b'<root><conteudo><![CDATA[<p></p>]]></conteudo></root>'
        with patch.object(mg.rede, 'get', return_value=(200, xml, 'application/xml')) as get, patch.object(mg, 'gravar') as gravar:
            status, _ = mg.processar(self.r)
        self.assertEqual(status, 'sem_texto')
        self.assertEqual(get.call_count, 1)
        gravar.assert_not_called()
        self.assertEqual(self.md.read_text(), self.original)

    def test_corpo_existente_integro_nao_e_sobrescrito(self):
        self.md.write_text(self.original + 'Art. 1 Texto já conferido.')
        with patch.object(mg.rede, 'get') as get:
            self.assertEqual(mg.processar(self.r), ('pulado', None))
        get.assert_not_called()


if __name__ == '__main__':
    unittest.main()
