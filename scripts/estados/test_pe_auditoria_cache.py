import unittest
from auditar_pe_cache import limpar_residuo_limite, documento_da_lista


class LimitePernambucoTest(unittest.TestCase):
    def test_remove_apenas_residuo_com_restante_igual_fonte(self):
        self.assertEqual(limpar_residuo_limite('Art. 1º Valor 99.\n\n&lt;div', '**Art. 1º** Valor 99.'), ('Art. 1º Valor 99.', '\n\n&lt;div'))

    def test_divergencia_normativa_impede_remocao(self):
        old='Art. 1º Valor 99.\n\n&lt;div'
        self.assertEqual(limpar_residuo_limite(old,'Art. 1º Valor 88.'),(old,None))

    def test_literal_div_normativo_nao_e_residuo(self):
        old='Art. 1º Código informado:\n\n&lt;div'
        self.assertEqual(limpar_residuo_limite(old,old),(old,None))

    def test_div_interno_nao_e_removido(self):
        old='Art. 1º &lt;div designa elemento.\nArt. 2º Fim.'
        self.assertEqual(limpar_residuo_limite(old,old),(old,None))

    def test_copia_auxiliar_e_traversal_sao_recusados(self):
        for p in ['estaduais/PE/_indice/candidatos/decreto.md','estaduais/PE/decretos/../arquivo.md','estaduais/PE/decretos/2026/_backup.md']:
            with self.subTest(p=p),self.assertRaises(ValueError):documento_da_lista(p)


if __name__=='__main__':unittest.main()
