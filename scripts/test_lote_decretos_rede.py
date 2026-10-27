"""Retomada da área de validação reaproveita íntegra/metadados sem HTTP."""
import contextlib
import gc
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock
sys.path.insert(0, str(Path(__file__).resolve().parent))
import baixar_federal as f


class RetomadaLote(unittest.TestCase):
    def test_markdown_pendente_promocao_e_reusado_sem_http(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / 'federal'
            lote = 'teste_retomada_' + Path(tmp).name
            cache = base / '_fonte/auditorias' / lote
            work = cache / 'work'
            work.mkdir(parents=True)
            d = {'tipo': 'DEC-n', 'numero': '1', 'dataassinatura': '01/01/2000',
                 'normaNome': 'Decreto nº 1 de 01/01/2000', 'norma': 'DEC-1-2000-01-01', 'id': 'fixture'}
            source = [{'path': 'federal/decretos/2000/dec-1-2000-01-01.md', 'indice': d, 'preexistente': False}]
            entrada = Path(tmp) / 'entrada.json'
            entrada.write_text(json.dumps(source))
            with patch.object(f, 'RAIZ', str(work)):
                urn = f.montar(d)['urn']
                meta = json.dumps({'legislationIdentifier': urn, 'legislationDate': '2000-01-01',
                                   'legislationType': 'Decreto Numerado',
                                   'encoding': {'contentUrl': 'https://example.invalid/texto', 'version': 'Original'}}).encode()
                html = '<p>DECRETO Nº 1, DE 1 DE JANEIRO DE 2000.</p><p>Art. 1º Fica aprovado o regulamento.</p>'.encode()
                def resposta(url, *args, **kwargs):
                    return 200, meta if 'api/public/normas?' in url else html
                with patch.object(f, 'http_get', resposta):
                    self.assertEqual(f.processar(d)[0], 'ok')
            (cache / 'candidatos.json').write_text(json.dumps(source))
            (cache / 'coleta.json').write_text(json.dumps({'registros': [{**source[0], 'status': 'ok', 'detalhe': None}]}))
            argv = ['coletor', '--entrada', str(entrada), '--lote', lote, '--workers', '1']
            network = Mock(side_effect=AssertionError('Nenhum HTTP permitido ao retomar captura completa'))
            with patch.object(f, 'RAIZ', str(base)), patch.object(f, 'http_get', network), patch.object(sys, 'argv', argv), contextlib.redirect_stdout(io.StringIO()):
                runpy.run_path(str(Path(__file__).with_name('preparar_lote_decretos_rede.py')), run_name='__main__')
            gc.collect()
            self.assertEqual(network.call_count, 0)
            manifest = json.loads((base / ('_' + lote + '.json')).read_text())
            self.assertEqual(manifest['resumo']['publicaveis'], 1)
            self.assertEqual(manifest['resumo']['retidos'], 0)
            self.assertTrue((Path(tmp) / source[0]['path']).exists())
            Path('/tmp/' + lote + '-publicar-paths.txt').unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
