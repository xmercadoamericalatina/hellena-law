import json
import sys
import unittest

try:
    from auditar_pe_recuperacao_utf8 import candidato
except ModuleNotFoundError as e:
    if e.name != 'markdown_it':
        raise
    candidato = None


@unittest.skipIf(candidato is None, 'requer markdown-it-py==4.0.0')
class RecuperacaoUTF8Tests(unittest.TestCase):
    def fixture(self, body=None):
        body = body or ('<p>LEI Nº 123, DE 2 DE JANEIRO DE 2000.</p>'
                        '<p>Art. 1º A execução da ação seguirá os valores:</p>'
                        '<table><tr><td>Variação</td><td>Taxa</td></tr>'
                        '<tr><td>-100,50</td><td>0,5%</td></tr></table>'
                        '<p>Art. 2º Esta Lei entra em vigor na publicação.</p><p>JOÃO DA SILVA</p>')
        source = ('<html><head><meta charset="windows-1252"></head><body><div>'+
                  body+'</div></body></html></div><div ').encode('utf-8')
        meta = dict(titulo='Lei Ordinária n° 123', tipo='Lei Ordinária', numero='123',
                    data='', ano='2000', fonte='https://legis.alepe.pe.gov.br/texto.aspx?id=12&tipo=TEXTOORIGINAL')
        raw = ('---\n'+'\n'.join(k+': '+json.dumps(v, ensure_ascii=False) for k,v in meta.items())+
               '\n---\n# Lei Ordinária n° 123\n\nLEI NÂº 123. A execuÃ§Ã£o da aÃ§Ã£o.\n').encode()
        return raw, source

    def test_cache_utf8_metadata_windows_preserva_nome_sinais_e_tabela(self):
        raw, source = self.fixture(); new, proof = candidato(raw, source)
        text = new.decode()
        for literal in ('execução', 'ação', 'JOÃO DA SILVA', '-100,50', '0,5%'):
            self.assertIn(literal, text)
        self.assertIn('data: "2000-01-02"', text)
        self.assertNotIn('&lt;div', text)
        self.assertTrue(proof['igualdade_visivel_CommonMark'])
        self.assertEqual(proof['tabelas_multilinhas'], 1)
        self.assertNotIn('revogada:', text)

    def test_identidade_diferente_e_fonte_sem_fechamento_falham(self):
        raw, source = self.fixture()
        for changed in (source.replace(b'123,', b'124,'), source.replace(b'</body>', b'')):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                candidato(raw, changed)

    def test_nao_adivinha_encoding_nem_substitui_nomes(self):
        raw, source = self.fixture()
        with self.assertRaises(UnicodeDecodeError):
            candidato(raw, source.decode().encode('cp1252'))
        with self.assertRaises(ValueError):
            candidato(raw, source.replace('JOÃO'.encode(), '\ufffd'.encode()))

    def test_anexo_ausente_imagem_tachado_e_css_oculto_retidos(self):
        raw, source = self.fixture()
        for extra in ('<p>Art. 3º Fica aprovado o anexo único desta Lei.</p>',
                      '<img src="tabela.png">', '<s>redação anterior</s>',
                      '<p style="display:none">texto</p>'):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                candidato(raw, source.replace(b'</body>', extra.encode()+b'</body>'))


if __name__ == '__main__':
    unittest.main()
