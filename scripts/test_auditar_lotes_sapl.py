"""Capturas paginadas oficiais podem comprovar um índice agregado interrompido."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import auditar_lotes_sapl as auditor


class CapturasSAPLTest(unittest.TestCase):
    def test_recupera_pagina_provada_e_rejeita_nome_sem_prova_de_consulta(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(auditor, 'RAIZ', Path(tmp)):
            raiz = Path(tmp)
            host = 'sapl.cidade.sp.leg.br'
            source = f'https://{host}/norma/1'
            attachment = f'https://{host}/media/norma.pdf'
            raw = raiz / 'municipais/_fonte/organicas-sapl' / host / '1.bin'
            raw.parent.mkdir(parents=True)
            raw.write_bytes(b'fonte oficial')
            corpo = 'Art. 1º Regra municipal.'
            m = {'titulo': 'Lei 1', 'tipo': 'Lei ordinária', 'numero': '1', 'data': '2000-01-01',
                 'municipio': 'Cidade', 'uf': 'SP', 'codigo_ibge': '123', 'fonte': source, 'fonte_texto': attachment,
                 'versao_texto': 'texto integral SAPL', 'baixado_em': dt.date.today().isoformat(),
                 'sha256_texto': hashlib.sha256(corpo.encode()).hexdigest(),
                 'sha256_fonte': hashlib.sha256(raw.read_bytes()).hexdigest()}
            path = raiz / 'municipais/SP/cidade/leis-ordinarias/2000/lei-1-sapl-1.md'
            path.parent.mkdir(parents=True)
            path.write_text('---\n' + '\n'.join(k + ': ' + json.dumps(v) for k,v in m.items()) + '\n---\n\n# Lei 1\n\n' + corpo + '\n')
            cache = raiz / 'municipais/_indice/organicas-sapl' / host
            cache.mkdir(parents=True)
            def capturar(route, dados):
                url = f'https://{host}/api/{route}'
                arq = cache / (hashlib.sha256(url.encode()).hexdigest() + '.json')
                arq.write_text(json.dumps(dados))
                return arq
            capturar('base/casalegislativa/', {'results': [{'municipio': 'Cidade', 'uf': 'SP'}]})
            capturar('norma/tiponormajuridica/?page_size=100&page=1',
                     {'results': [{'id': 1, 'descricao': 'Lei Ordinária'}], 'pagination': {'next_page': None}})
            pagina = capturar('norma/normajuridica/?tipo=1&page_size=100&page=1',
                              {'results': [{'id': 1, 'tipo': 1, 'numero': 1, 'ano': 2000, 'data': '2000-01-01',
                                            'texto_integral': attachment, 'ementa': 'Dispõe sobre regras'}],
                               'pagination': {'page': 1}})
            ibge = {'123': {'nome': 'Cidade', 'regiao-imediata': {'regiao-intermediaria': {'UF': {'sigla': 'SP'}}}}}
            result = auditor.auditar(path, ibge, {}, {}, {}, {})
            self.assertEqual(result['erros'], [])
            self.assertTrue(any(e.get('cache_original', '').endswith(pagina.name) for e in result['evidencias']))
            pagina.rename(cache / ('0' * 64 + '.json'))
            result = auditor.auditar(path, ibge, {}, {}, {}, {})
            self.assertIn('identificador não encontrado no índice oficial capturado', result['erros'])


if __name__ == '__main__':
    unittest.main()
