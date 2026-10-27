import unittest

try:
    from auditar_rj_complementar import complementar, IMAGENS_INTERFACE
except ModuleNotFoundError as e:
    if e.name != 'markdown_it':
        raise
    complementar = None


@unittest.skipIf(complementar is None, 'requer markdown-it-py==4.0.0')
class RJComplementarTests(unittest.TestCase):
    def test_anexo_proprio_nao_e_comprovado_por_tabela_generica(self):
        field = '<p>Conforme Anexo Único desta Lei.</p><table><tr><td>Assunto</td></tr><tr><td>Valor</td></tr></table>'
        issues, _ = complementar(field, field, field, [])
        self.assertTrue(any('anexo' in s for s in issues))

    def test_objeto_aprovado_sem_nome_nao_e_comprovado_por_tabela(self):
        s = '<p>Fica aprovado o documento de referência.</p><table><tr><td>A</td></tr><tr><td>B</td></tr></table>'
        issues, _ = complementar(s, s, s, [])
        self.assertTrue(any('objeto aprovado' in s for s in issues))

    def test_tabela_preserva_decimal_negativo_percentual_e_ordem(self):
        s = '<table><tr><td>Valor</td><td>Taxa</td></tr><tr><td>-100,50</td><td>0,5%</td></tr></table>'
        self.assertFalse(complementar(s, s, s, [])[0])
        for errado in (s.replace('-100,50', '10050'), s.replace('0,5%', '05')):
            self.assertIn('matrizes multilinhas divergem', complementar(s, s, errado, [])[0])

    def test_identidade_de_imagem_exige_todos_os_atributos(self):
        self.assertFalse(complementar('<p>Texto</p>', '', 'Texto', [IMAGENS_INTERFACE[0]])[0])
        errada = dict(IMAGENS_INTERFACE[0], width='800')
        self.assertTrue(complementar('<p>Texto</p>', '', 'Texto', [errada])[0])

    def test_css_local_oculto_ou_tachado_exige_contexto(self):
        for regra in ('opacity:0.0', 'font-size:0px', 'display:none', 'text-decoration:line-through'):
            issues, _ = complementar('<p>Texto</p>', '<style>.classe {'+regra+'}</style>', 'Texto', [])
            self.assertTrue(any('CSS' in s for s in issues), regra)

    def test_anexo_de_outra_norma_na_citacao_nao_e_mascarado_automaticamente(self):
        # O helper conserva o sinal para revisão. A decisão humana contextual
        # documentada em overlay é que readmite citações, nunca uma máscara.
        s = '<p>O art. 22 da Lei nº 2.657 passa a vigorar: “Anexo Único desta Lei”.</p>'
        issues, _ = complementar(s, s, s, [])
        self.assertTrue(issues)


if __name__ == '__main__':
    unittest.main()
