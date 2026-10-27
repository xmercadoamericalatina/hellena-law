"""Prova que estados sem situação conclusiva nunca recebem revogada:false por padrão."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import df
import mg
import sp


class VigenciaColetores(unittest.TestCase):
    CASOS = {
        'Revogada': True,
        'Revogado': True,
        'Vigente': False,
        'Em vigor': False,
        'Sem Revogação Expressa': None,
        'Alterado': None,
        'DECLARADA INCONSTITUCIONAL': None,
        'TORNADA SEM EFEITO': None,
        'Suspenso': None,
        '': None,
    }

    def executar(self, modulo, registro, situacao, pasta):
        destino = Path(pasta) / 'norma.md'
        html = b'<p>Art. 1 Texto normativo de teste.</p>'
        with patch.object(modulo, 'caminhos', return_value=(str(destino), str(destino) + '.gz')), patch.object(modulo, 'gravar') as gravar:
            if modulo is mg:
                xml = b'<root><conteudo><![CDATA[' + html + b']]></conteudo></root>'
                with patch.object(mg, 'RAIZ_ESTADUAIS', pasta), patch.object(mg.rede, 'get', return_value=(200, xml, 'application/xml')):
                    mg.bloqueado.clear()
                    status, _ = mg.processar(registro)
            elif modulo is df:
                with patch.object(df.rede, 'get', return_value=(200, html, 'text/html')), patch.object(df, 'documento_para_md', return_value=('Art. 1 Texto normativo de teste.', None)):
                    status, _ = df.processar(registro)
            else:
                info = {'dsSituacao': situacao, 'urlIntegraOriginal': 'https://www.al.sp.gov.br/norma-teste.html', 'nuNorma': '1'}
                responses = [(200, json.dumps(info).encode(), 'application/json'), (200, html, 'text/html')]
                with patch.object(sp.rede, 'get', side_effect=responses), patch.object(sp, 'documento_para_md', return_value=('Art. 1 Texto normativo de teste.', None)):
                    status, _ = sp.processar(registro)
            self.assertEqual(status, 'ok')
            return dict(gravar.call_args.args[3])

    def test_mg_preserva_situacao_sem_inferir_vigencia(self):
        for situacao, esperado in self.CASOS.items():
            with self.subTest(situacao=situacao), tempfile.TemporaryDirectory() as pasta:
                registro = {'Tipo': 'DEC', 'Numero': '1', 'Ano': '2026', 'Complemento': '', 'DataLegislacao': '01/01/2026', 'Ementa': 'Teste', 'Situacao': situacao, 'LinkTextoAtualizado': '', 'LinkTextoOriginal': 'https://dadosabertos.almg.gov.br/api/v2/norma-teste'}
                meta = self.executar(mg, registro, situacao, pasta)
                self.assertIs(meta['revogada'], esperado)
                self.assertEqual(meta['situacao'], situacao.capitalize())

    def test_df_preserva_situacao_sem_inferir_vigencia(self):
        for situacao, esperado in self.CASOS.items():
            with self.subTest(situacao=situacao), tempfile.TemporaryDirectory() as pasta:
                registro = {'_ch_tipo': 'Decreto', 'dt_assinatura': '01/01/2026', 'nr_norma': '1', 'ch_norma': 'teste', 'nm_situacao': situacao, 'ar_atualizado': {'filename': 'teste.html'}}
                meta = self.executar(df, registro, situacao, pasta)
                self.assertIs(meta['revogada'], esperado)
                self.assertEqual(meta['situacao'], situacao)

    def test_sp_preserva_situacao_sem_inferir_vigencia(self):
        for situacao, esperado in self.CASOS.items():
            with self.subTest(situacao=situacao), tempfile.TemporaryDirectory() as pasta:
                registro = {'IdTipo': '3', 'IdNorma': '1', 'Numero': '1', 'Data': '2026-01-01'}
                meta = self.executar(sp, registro, situacao, pasta)
                self.assertIs(meta['revogada'], esperado)
                self.assertEqual(meta['situacao'], situacao)


if __name__ == '__main__':
    unittest.main()
