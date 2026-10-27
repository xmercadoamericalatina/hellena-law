import json
import unittest
try:
    from auditar_pe_infralegal_cache import auditar
    from comum import html_para_md
except ModuleNotFoundError as e:
    if e.name != 'markdown_it': raise
    auditar = None


@unittest.skipIf(auditar is None, 'requer markdown-it-py==4.0.0')
class PEInfralegalCacheTests(unittest.TestCase):
    def fixture(self, extra='', numero='321'):
        field = ('<p>RESOLUÇÃO Nº '+numero+', DE 2 DE JANEIRO DE 2000.</p>'
                 '<p>Art. 1º A execução seguirá os valores:</p>'
                 '<table><tr><td>Valor</td><td>Taxa</td></tr><tr><td>-100,50</td><td>0,5%</td></tr></table>'
                 '<p>Art. 2º Esta Resolução entra em vigor na publicação.</p>'+extra)
        source = ('<html><div id="divTexto">'+field+'</div></html>').encode()
        item = dict(id='123', tipo='4', nome='Resolução n° 321', publicacao='Publicada no DOE 03/01/2000',
                    textos=['TEXTOORIGINAL'], ementa='A execução seguirá valores.')
        meta = dict(titulo=item['nome'], tipo='Resolução', numero='321', data='2000-01-02', ano='2000',
                    revogada=None, versao_texto='original', publicacao=item['publicacao'], ementa=item['ementa'],
                    fonte='https://legis.alepe.pe.gov.br/texto.aspx?id=123&tipo=TEXTOORIGINAL')
        raw = ('---\n'+'\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in meta.items())+
               '\n---\n# '+item['nome']+'\n\n'+html_para_md(field)+'\n').encode()
        return raw, source, item

    def test_identidade_fonte_data_pontuacao_e_tabela_fieis(self):
        raw, source, item = self.fixture(); q = auditar(raw, source, item)
        self.assertEqual(q['data'], '2000-01-02')
        self.assertEqual(q['tabelas_multilinhas'], 1)
        self.assertTrue(q['assinatura_numerica_sinais'])

    def test_numero_diferente_falha(self):
        raw, source, item = self.fixture(numero='322')
        with self.assertRaises(ValueError): auditar(raw, source, item)

    def test_decimal_negativo_e_percentual_nao_se_confundem(self):
        raw, source, item = self.fixture()
        for changed in (raw.replace(b'-100,50', b'10050'), raw.replace(b'0,5%', b'05')):
            with self.subTest(changed=changed), self.assertRaises(ValueError): auditar(changed, source, item)

    def test_anexo_proprio_nao_e_satisfeito_por_tabela_generica(self):
        raw, source, item = self.fixture('<p>Art. 3º Fica aprovado o Anexo Único desta Resolução.</p>')
        with self.assertRaises(ValueError): auditar(raw, source, item)

    def test_visual_tachado_e_oculto_retidos(self):
        for extra in ('<img src="anexo.png">', '<s>Texto antigo.</s>', '<p style="opacity:0.0">Texto.</p>'):
            raw, source, item = self.fixture(extra)
            with self.subTest(extra=extra), self.assertRaises(ValueError): auditar(raw, source, item)

    def test_vigencia_nao_e_inferida_sem_situacao_oficial(self):
        raw, source, item = self.fixture(); raw = raw.replace(b'revogada: null', b'revogada: false')
        with self.assertRaises(ValueError): auditar(raw, source, item)


if __name__ == '__main__': unittest.main()
