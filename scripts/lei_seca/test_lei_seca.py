"""Testes de escopo, integridade e atualização usando fontes simuladas."""
import argparse
import gzip
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import LegalHTML, allowed_kind, extract, publish, read_json, validate_url, write_json
from coletar import discover_portal, discover_sapl, discover_senate, senate_docs, senate_entry
from atualizar import enqueue, run
from auditar import audit

HTML = '''<html><head><title>Lei 123</title><script>roubar()</script></head><body>
<p>LEI Nº 123, DE 1 DE JANEIRO DE 2026</p>
<p>Dispõe sobre as relações de trabalho e outras providências normativas.</p>
<p>Art. 1º O empregado poderá requerer o benefício previsto nesta Lei.</p>
<p><s>Redação anterior.</s> Redação atual, com efeitos na data da publicação.</p>
<table><tr><td>Faixa A</td><td>10%</td></tr><tr><td>Faixa B</td><td>20%</td></tr></table>
<p>Art. 2º Esta Lei entra em vigor na data de sua publicação.</p></body></html>'''.encode()
ENTRY = dict(id='teste-123', tipo='Lei', titulo='Lei nº 123/2026', numero='123',
             conector='direto', url='https://www.planalto.gov.br/lei123.htm', prioridade=True)


class FakeNet:
    def __init__(self, data=HTML):
        self.data = data
        self.calls = []

    def get(self, url):
        self.calls.append(url)
        return self.data, 'text/html; charset=utf-8', url


class Tests(unittest.TestCase):
    def test_types(self):
        for kind in ['Lei', 'Lei Complementar', 'Decreto-Lei', 'Emenda Constitucional', 'Portaria Normativa', 'Instrução Normativa']:
            self.assertTrue(allowed_kind(kind), kind)
        for kind in ['Projeto de Lei', 'Súmula', 'Acórdão', 'Parecer Normativo', 'Solução de Consulta', 'Orientação Jurisprudencial', 'Lei comentada', 'Lei — doutrina']:
            self.assertFalse(allowed_kind(kind), kind)

    def test_urls(self):
        for url in ['https://www.planalto.gov.br/x', 'https://sapl.al.pb.leg.br/api/']:
            validate_url(url)
        for url in ['http://www.planalto.gov.br', 'https://planalto.gov.br.evil.com', 'https://127.0.0.1', 'https://evil@www.planalto.gov.br', 'https://www.planalto.gov.br:8000/x']:
            with self.assertRaises(ValueError):
                validate_url(url)

    def test_literal_preserves_strike_and_table(self):
        text, _ = extract(HTML, '', ENTRY['titulo'], '123')
        self.assertNotIn('roubar', text)
        self.assertIn('~~Redação anterior.~~', text)
        self.assertIn('Faixa A\t10%', text)
        self.assertIn('Faixa B\t20%', text)

    def test_wrong_identity_and_block_page(self):
        with self.assertRaises(ValueError):
            extract(HTML, '', 'Lei 999', '999')
        with self.assertRaises(ValueError):
            extract(b'<html><p>Verifique que voce e humano</p></html>', '', 'Lei', '')
        with self.assertRaises(ValueError):
            extract(b'%PDF-1.7 abc', '', 'Lei', '')

    def test_changed_law_and_tampering(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            a = publish(root, ENTRY, HTML, '', ENTRY['url'])
            b = publish(root, ENTRY, HTML, '', ENTRY['url'])
            self.assertTrue(a['alterado'])
            self.assertFalse(b['alterado'])
            c = publish(root, ENTRY, HTML.replace(b'10%', b'15%'), '', ENTRY['url'])
            self.assertTrue(c['alterado'])
            self.assertEqual(len(list((root / 'versoes' / ENTRY['id']).glob('*.json'))), 2)
            write_json(root / 'indice.json', [{'id': ENTRY['id'], 'sha256_texto': c['sha256_texto']}])
            self.assertEqual(audit(root), [])
            (root / 'textos' / (ENTRY['id'] + '.md')).write_text('corrompido')
            self.assertTrue(audit(root))

    def test_index_single_and_invalid(self):
        doc = {'id': 123, 'tipo': 'LEI-n', 'dataassinatura': '01/01/2026', 'numero': '123', 'normaNome': 'Lei 123'}
        self.assertEqual(senate_docs({'ListaDocumento': {'documentos': {'documento': doc}}}), [doc])
        self.assertEqual(senate_entry(doc)['urn'], 'urn:lex:br:federal:lei:2026-01-01;123')
        with self.assertRaises(ValueError):
            senate_docs({'error': 'rate limited'})

    def test_no_advance_on_source_failure(self):
        net = FakeNet()
        net.json = lambda url: {'error': 'unavailable'}
        state = {}
        docs, events = discover_senate(net, state, 1, 1)
        self.assertEqual(docs, [])
        self.assertEqual(state['indices'], {})
        self.assertTrue(all(x['status'] == 'erro' for x in events))

    def test_official_portal_does_not_publish_commentary(self):
        net = FakeNet(b'<html><a href="https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp227.htm">Lei Complementar 227</a><a href="https://blog.com/lei.htm">Comentada</a><p>Comentario sobre a reforma</p></html>')
        docs = discover_portal(net, {'url': 'https://www.gov.br/rfb', 'tema': 'tributario'})
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]['numero'], '227')

    def test_sapl_pagination_and_exclusion(self):
        class Net:
            def json(self, url):
                if 'tiponorma' in url:
                    return {'results': [{'id': 1, 'descricao': 'Lei'}, {'id': 2, 'descricao': 'Parecer'}], 'pagination': {'next_page': None}}
                return {'results': [{'id': 10, 'tipo': 1, 'numero': 123, 'ano': 2026, 'texto_integral': '/texto.htm'},
                                    {'id': 11, 'tipo': 2, 'texto_integral': '/parecer.htm'}], 'pagination': {'next_page': 2}}
        source = dict(id='pb', url='https://sapl.al.pb.leg.br', esfera='estadual', uf='PB')
        state = {}
        docs = discover_sapl(Net(), source, state)
        self.assertEqual([d['id'] for d in docs], ['pb-10'])
        self.assertEqual(state['sapl']['pb']['page'], 2)

    def test_queue_keeps_last_check(self):
        state = {'fila': {'teste-123': {'tentado_em': '2026-01-01', 'status': 'publicado'}}}
        enqueue(state, [ENTRY])
        self.assertEqual(state['fila']['teste-123']['tentado_em'], '2026-01-01')

    def test_end_to_end_and_no_skip_existing_law(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            cfg = root / 'config.json'
            write_json(cfg, {'prioridades': [ENTRY], 'sapl': [], 'indices_oficiais': [], 'lacunas': ['teste']})
            args = argparse.Namespace(output=root / 'out', config=cfg, seconds=30, mode='prioridades', limit=10,
                                      indices=1, historic=0, force=False, refresh_days=30)
            self.assertEqual(run(args, FakeNet()), 0)
            self.assertEqual(len(read_json(args.output / 'indice.json')), 1)
            args.force = True
            self.assertEqual(run(args, FakeNet(HTML.replace(b'10%', b'30%'))), 0)
            self.assertIn('30%', (args.output / 'textos' / 'teste-123.md').read_text())
            self.assertEqual(audit(args.output), [])

    def test_pending_pdf_keeps_original(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            cfg = root / 'config.json'
            write_json(cfg, {'prioridades': [ENTRY], 'sapl': [], 'indices_oficiais': [], 'lacunas': []})
            args = argparse.Namespace(output=root / 'out', config=cfg, seconds=30, mode='prioridades', limit=10,
                                      indices=1, historic=0, force=False, refresh_days=30)
            self.assertEqual(run(args, FakeNet(b'%PDF-1.7 incomplete')), 1)
            self.assertEqual(read_json(args.output / 'indice.json'), [])
            self.assertEqual(len(list((args.output / 'originais').glob('*/*.gz'))), 1)
            self.assertEqual(read_json(args.output / 'pendencias.json')[0]['status'], 'pendente')


if __name__ == '__main__':
    unittest.main()
