import unittest
from pe_fidelidade_visivel import comparar_fidelidade, texto_visivel_markdown


class FidelidadeVisivelTest(unittest.TestCase):
    def conferir_divergencia(self,source,actual):
        r=comparar_fidelidade('<p>'+source+'</p>',source,actual)
        self.assertFalse(r['texto_visivel_md_igual_reconversao'])
        self.assertFalse(r['numeros_sinais_moedas_percentuais_iguais_fonte'])

    def test_decimal(self):self.conferir_divergencia('0,5','05')
    def test_negativo(self):self.conferir_divergencia('-100','100')
    def test_percentual(self):self.conferir_divergencia('5%','5')
    def test_moeda(self):self.conferir_divergencia('R$ 100,00','100,00')
    def test_parenteses_contabeis(self):self.conferir_divergencia('(100)','100')

    def test_formatacao_comprovada_preserva_texto(self):
        source='<p><b>Art. 1º</b> Valor <i>R$ -0,5 (5%)</i>.</p>'
        r=comparar_fidelidade(source,'**Art. 1º** Valor *R$ -0,5 (5%)*.','**Art. 1º** Valor *R$ -0,5 (5%)*.')
        self.assertTrue(all(v for v in r.values() if isinstance(v,bool)))

    def test_tabela_gfm_decimal_nao_e_digito_inteiro(self):
        source='<table><tr><td>Valor</td></tr><tr><td>-0,5%</td></tr></table>'
        md='| Valor |\n| --- |\n| -0,5% |'
        self.assertTrue(comparar_fidelidade(source,md,md)['texto_visivel_md_igual_html_fonte'])
        self.assertFalse(comparar_fidelidade(source,md,md.replace('-0,5%','05'))['numeros_sinais_moedas_percentuais_iguais_fonte'])

    def test_heading_editorial_provado_na_fonte(self):
        source='<p>CAPÍTULO I</p><p>DOS VALORES</p><p>Art. 1º -100.</p>'
        md='#### CAPÍTULO I — DOS VALORES\n\nArt. 1º -100.'
        r=comparar_fidelidade(source,md,md)
        self.assertFalse(r['texto_visivel_md_igual_html_fonte'])
        self.assertTrue(r['texto_visivel_md_igual_fonte_apos_formato_heading_comprovado'])
        self.assertEqual(len(r['normalizacoes_de_apresentacao']),1)
        self.assertFalse(comparar_fidelidade(source,md,md.replace('-100','100'))['numeros_sinais_moedas_percentuais_iguais_fonte'])

    def test_heading_mista_caixa_preserva_grafia_fonte(self):
        source='<p>Seção I</p><p>Da Fiscalização</p><p>Art. 1º −100.</p>'
        md='##### Seção I — Da Fiscalização\n\nArt. 1º −100.'
        self.assertTrue(comparar_fidelidade(source,md,md)['texto_visivel_md_igual_fonte_apos_formato_heading_comprovado'])

    def test_italico_mal_fechado_nao_some_como_formatacao(self):
        r=comparar_fidelidade('<p>no <i>caput</i>,</p>','no *caput *,','no *caput *,')
        self.assertFalse(r['texto_visivel_md_igual_fonte_apos_formato_heading_comprovado'])
        self.assertIn('*caput *',r['visivel_md'])

    def test_lacunas_de_formulario_nao_sao_italico(self):
        value='## MODELO Nº _____ DE __ DE _______'
        self.assertEqual(texto_visivel_markdown(value),'MODELO Nº _____ DE __ DE _______')

    def test_heading_romano_espacado_preservado(self):
        source='<p>CAPÍTULO V I</p><p>DA COMPETÊNCIA</p>'
        md='#### CAPÍTULO V I — DA COMPETÊNCIA'
        self.assertTrue(comparar_fidelidade(source,md,md)['texto_visivel_md_igual_fonte_apos_formato_heading_comprovado'])

    def test_heading_com_sufixo_literal_preservado(self):
        source='<p>Seção VIII-B</p><p>Da Nota Fiscal</p>'
        md='##### Seção VIII-B — Da Nota Fiscal'
        self.assertTrue(comparar_fidelidade(source,md,md)['texto_visivel_md_igual_fonte_apos_formato_heading_comprovado'])

    def test_travessao_literal_nao_e_removido(self):
        source='<p>CAPÍTULO I — DOS VALORES</p><p>Art. 1º −100.</p>'
        md='#### CAPÍTULO I — DOS VALORES\n\nArt. 1º −100.'
        r=comparar_fidelidade(source,md,md)
        self.assertTrue(r['texto_visivel_md_igual_html_fonte'])
        self.assertEqual(r['normalizacoes_de_apresentacao'],[])

    def test_asterisco_literal_html_e_escape_md(self):
        self.assertEqual(texto_visivel_markdown('<table><tr><td>3*5*2</td></tr></table>'),'3*5*2')
        self.assertEqual(texto_visivel_markdown(r'3\*5\*2'),'3*5*2')

    def test_fonte_primaria_supera_artefato_do_conversor(self):
        r=comparar_fidelidade('<p>no <i>caput</i>,</p>','no *caput *,','no *caput*,')
        self.assertFalse(r['texto_visivel_md_igual_reconversao'])
        self.assertTrue(r['texto_visivel_md_igual_fonte_apos_formato_heading_comprovado'])
        self.assertTrue(r['numeros_sinais_moedas_percentuais_iguais_fonte'])

    def test_nao_apaga_asterisco_literal_da_fonte(self):
        r=comparar_fidelidade('<p>Operador *caput* literal.</p>',r'Operador \*caput\* literal.','Operador *caput* literal.')
        self.assertFalse(r['texto_visivel_md_igual_fonte_apos_formato_heading_comprovado'])

    def test_crase_literal_escapada_e_preservada(self):
        self.assertEqual(texto_visivel_markdown(r'bomba d\`água e d\`água'),'bomba d`água e d`água')

    def test_crase_em_html_nativo_nao_e_codigo_md(self):
        self.assertEqual(texto_visivel_markdown('<table><tr><td>bomba d`água e d`água</td></tr></table>'),'bomba d`água e d`água')

    def test_barra_interna_de_codigo_e_literal(self):
        self.assertEqual(texto_visivel_markdown(r'`\*`'),r'\*')

    def test_codigo_separador_e_quebra_br(self):
        self.assertEqual(texto_visivel_markdown('`=======`\nA<br>B'),'======= A B')
        self.assertEqual(texto_visivel_markdown('<code>=======</code>\nA  \nB'),'======= A B')


if __name__=='__main__':unittest.main()
