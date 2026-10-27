import unittest

from gates_reguladores_cache import chave, conferir_fonte, motivos_conteudo, motivos_identidade, origem


class GatesTest(unittest.TestCase):
    def test_dou_receita_nao_e_json_por_pasta(self):
        row = {'path': 'reguladores/rfb/portarias/2022/x.md', 'cache': 'rfb/x.html.gz', 'sha256_html': 'a' * 64}
        self.assertEqual(origem(row), 'dou')
        self.assertEqual(conferir_fonte(row, b'<div class="texto-dou"><p>Art. 1 Texto.</p></div></main>'), [])

    def test_sijut_exige_prova_de_origem(self):
        row = {'cache': 'rfb/x.json.gz', 'fonte_api': 'https://normasinternet2.receita.fazenda.gov.br/api/x'}
        self.assertEqual(origem(row), 'rfb')
        with self.assertRaises(ValueError):
            origem({'cache': 'x.json.gz'})

    def test_dou_visual_e_campo_truncado_retidos(self):
        row = {'cache': 'x.html.gz', 'sha256_html': 'b' * 64}
        self.assertTrue(conferir_fonte(row, b'<div class="texto-dou"><img src="norma.png"></div></main>'))
        self.assertTrue(conferir_fonte(row, b'<div class="texto-dou"><div><p>x</p></div></main>'))

    def test_objeto_aprovado_e_remissao_externa(self):
        self.assertTrue(motivos_conteudo('Art. 1 Fica aprovado o regulamento.\nArt. 2 Vigora.'))
        self.assertTrue(motivos_conteudo('O manual encontra-se disponível no portal oficial.'))
        self.assertEqual(motivos_conteudo('Art. 1 Fica alterado o prazo para 30 dias.\nArt. 2 Vigora.'), [])

    def test_placeholder_escapado_e_anexo_vazio(self):
        self.assertTrue(motivos_conteudo('&amp;lt;&amp;lt;ANEXO&gt;&gt;'))
        self.assertTrue(motivos_conteudo('Art. 1 Conforme o anexo.\n\nANEXO\n'))

    def test_identidade_preserva_sufixo_e_normaliza_milhar(self):
        meta = {'tipo': 'Portaria', 'numero': '01.234/2026', 'data': '2026-01-02'}
        self.assertEqual(chave(meta, 'reguladores/rfb/x.md'), ('rfb', 'portaria', '1234', '2026-01-02'))
        meta['numero'] = '1234-A'
        self.assertEqual(chave(meta, 'reguladores/rfb/x.md')[2], '1234-a')

    def test_numero_ausente_nao_libera_colisao_silenciosamente(self):
        meta = {'tipo': 'Resolução', 'numero': '', 'data': '2024-09-09', 'fonte': 'https://www.in.gov.br/a'}
        self.assertTrue(motivos_identidade(meta, 'reguladores/cjf/x.md', {}, set(), set()))
        meta['numero'] = '910'
        self.assertEqual(motivos_identidade(meta, 'reguladores/cjf/x.md', {}, set(), set()), [])


if __name__ == '__main__':
    unittest.main()
