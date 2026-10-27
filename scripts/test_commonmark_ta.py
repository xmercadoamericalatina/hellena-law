import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_commonmark_ta import comparar, NOTE


def source(text):
    return '<div class="cp"><div class="dptt" id="atual">'+text+'</div></div>'


class CommonMarkTA(unittest.TestCase):
    def test_pontuacao_e_sinais_nao_sao_descartados(self):
        self.assertTrue(comparar(source('Art. 1º R$ -0,50 (2%); `x`.'), 'Art. 1º R$ -0,50 (2%); \\`x\\`.')['aprovado'])
        self.assertFalse(comparar(source('Art. 1º R$ -0,50 (2%);'), 'Art. 1º R$ 0,50 (2%);')['aprovado'])

    def test_crase_consumida_pelo_motor_e_detectada(self):
        self.assertFalse(comparar(source('`nome`'), '`nome`')['aprovado'])

    def test_numeracao_efetiva_nao_copia_numero_digitado(self):
        result = comparar(source('3. Primeiro 9. Segundo'), '3. Primeiro\n9. Segundo')
        self.assertFalse(result['aprovado'])
        self.assertEqual(result['listas'][0]['contadores'], [3, 4])
        self.assertTrue(comparar(source('3. Primeiro 4. Segundo'), '3. Primeiro\n9. Segundo')['aprovado'])

    def test_historicos_tachados_e_nota_atribuida(self):
        original = '<div class="dptt desativado">Antiga</div>'+source('Art. 1º <s>velha</s> atual. (Revogado)')
        result = comparar(original, 'Art. 1º atual. (Revogado)\n\n'+NOTE)
        self.assertTrue(result['aprovado'])
        self.assertEqual(result['tachados_explicitos_excluidos'], 1)
        self.assertEqual(result['notas_editoriais_excluidas'], 1)
        with self.assertRaises(ValueError):
            comparar(source('atual'), 'atual\n\n'+NOTE)

    def test_lista_html_nativa_requer_associacao_propria(self):
        with self.assertRaises(ValueError):
            comparar(source('<ol><li>Primeiro</li></ol>'), '1. Primeiro')

    def test_caso_real_porto_velho_negrito_invalido(self):
        self.assertFalse(comparar(source('<b>Sônia Maria dos Santos Pereira - </b>Suplente'),
                                  '**Sônia Maria dos Santos Pereira - **Suplente')['aprovado'])
        self.assertTrue(comparar(source('<b>Sônia Maria dos Santos Pereira - </b>Suplente'),
                                 '**Sônia Maria dos Santos Pereira -** Suplente')['aprovado'])


if __name__ == '__main__':
    unittest.main()
