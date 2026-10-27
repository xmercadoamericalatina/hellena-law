import unittest
import df  # sets the repository scripts import path
from sinj_tachados import converter_html_sinj, explicitar_css_tachado

CSS = '<style>div.strike { text-decoration: line-through; }</style>'


class SINJTachadosTest(unittest.TestCase):
    def test_compilado_exclui_herdado_preserva_redacao_atual(self):
        source = CSS + '<div class="strike"><p>Art. 1º Redação antiga.</p></div><p>Art. 1º Redação atual.</p>'
        body, edition, proof = converter_html_sinj(source, compilado=True, situacao='Sem Revogação Expressa')
        self.assertNotIn('antiga', body)
        self.assertIn('atual', body)
        self.assertIn('excluídas', edition)
        self.assertTrue(proof['vigencia_nao_inferida'])

    def test_totalmente_revogada_preserva_historico(self):
        source = CSS + '<div class="strike"><p>Art. 1º Histórico.</p></div>'
        body, edition, proof = converter_html_sinj(source, compilado=True, situacao='Revogada')
        self.assertIn('~~', body)
        self.assertIn('Histórico', body)
        self.assertIn('histórica', edition)
        self.assertEqual(proof['situacao_literal'], 'Revogada')

    def test_sem_dispositivo_nao_fabrica_compilacao_vazia(self):
        source = CSS + '<div class="strike"><p>Art. 1º Texto antigo.</p></div><p>(Revogado por outra norma.)</p>'
        body, edition, proof = converter_html_sinj(source, compilado=True, situacao='Sem Revogação Expressa')
        self.assertIn('~~', body)
        self.assertIn('histórica', edition)
        self.assertFalse(proof.get('redacoes_tachadas_excluidas', False))

    def test_original_preserva_historico_e_tabela(self):
        source = CSS + '<div class="strike"><table><tr><td>0</td><td>12</td></tr></table></div><p>Art. 2º Atual.</p>'
        body, edition, _ = converter_html_sinj(source, compilado=False, situacao='')
        self.assertIn('<del>0</del>', body)
        self.assertIn('12', body)
        self.assertIn('histórica', edition)

    def test_sem_css_comprovado_nao_infere_classe(self):
        with self.assertRaises(ValueError):
            explicitar_css_tachado('<div class="strike"><p>Art. 1º Texto.</p></div>')

    def test_sem_tachado_edicao_inalterada(self):
        source = CSS + '<p>Art. 1º Texto atual.</p>'
        body, edition, _ = converter_html_sinj(source, compilado=True, situacao='Sem Revogação Expressa')
        self.assertIn('atual', body)
        self.assertEqual(edition, 'compilada (SINJ-DF)')

    def test_inline_explicito_nao_tachado_sobrepoe_classe(self):
        source = CSS + '<div class="strike" style="text-decoration:none"><p>Art. 1º Texto atual.</p></div>'
        body, edition, _ = converter_html_sinj(source, compilado=True, situacao='')
        self.assertIn('Texto atual', body)
        self.assertNotIn('~~', body)

    def test_artigo_um_revogado_nao_apaga_artigo_dois_atual(self):
        source = CSS + '<div class="strike"><p>Art. 1º Antigo.</p></div><p>Art. 2º Atual.</p>'
        body, edition, _ = converter_html_sinj(source, compilado=True, situacao='')
        self.assertNotIn('Antigo', body)
        self.assertIn('Atual', body)
        self.assertIn('compilada', edition)

    def test_seletor_descendente_nao_prova_classe_no_proprio_div(self):
        with self.assertRaises(ValueError):
            explicitar_css_tachado('<style>div .strike {text-decoration:line-through}</style><div class="strike">Texto</div>')

    def test_coletor_preserva_rejeicao_de_html_vazio(self):
        from unittest.mock import patch
        import tempfile
        from pathlib import Path
        sample = {'_ch_tipo': 'Portaria', 'dt_assinatura': '01/01/2020',
                  'nr_norma': '1', 'ch_norma': 'teste',
                  'ar_atualizado': {'filename': 'a.html'}}
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(df, 'caminhos', return_value=(str(Path(tmp) / 'a.md'), str(Path(tmp) / 'a.gz'))), patch.object(df.rede, 'get', return_value=(200, b'<p>curto</p>', 'text/html')), patch.object(df, 'gravar') as write:
                status, diagnostic = df.processar(sample)
        self.assertEqual(status, 'sem_texto')
        self.assertEqual(diagnostic['motivo'], 'documento vazio')
        write.assert_not_called()
