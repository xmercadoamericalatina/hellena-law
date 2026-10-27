import unittest
from unittest.mock import patch

import html2md


class PosicoesTest(unittest.TestCase):
    FONTE = ('Árvore\r\n<p>Art.1º — início</p>\n'
             '<table><tr><td rowspan="2">0</td><td><s>Histórico</s></td></tr>\r\n'
             '<tr><td><table><tr><td>Índice 26</td></tr></table></td></tr></table>\n'
             '<p>Fim</p>\n<table><tr><td>137</td><td>95</td></tr></table>')

    def test_equivalencia_da_saida_com_calculo_anterior(self):
        class Referencia(html2md.Parser):
            def source_offset(self):
                linha, coluna = self.getpos()
                return sum(len(s) + 1 for s in self.source.split('\n')[:linha - 1]) + coluna
        for excluir in (False, True):
            atual = html2md.convert(self.FONTE, exclude_struck=excluir)
            with patch.object(html2md, 'Parser', Referencia):
                anterior = html2md.convert(self.FONTE, exclude_struck=excluir)
            self.assertEqual(atual, anterior)
            self.assertIn('rowspan="2"', atual)
            self.assertIn('Índice 26', atual)

    def test_posicoes_unicode_crlf_e_tags_divididas_entre_chunks(self):
        class Conferido(html2md.Parser):
            def source_offset(parser):
                linha, coluna = parser.getpos()
                esperado = sum(len(s) + 1 for s in parser.source.split('\n')[:linha - 1]) + coluna
                obtido = super().source_offset()
                self.assertEqual(obtido, esperado)
                return obtido
        inteiro = html2md.Parser()
        inteiro.feed(self.FONTE)
        inteiro.close()
        inteiro.flush()
        for largura in (1, 7, 29):
            parser = Conferido()
            for inicio in range(0, len(self.FONTE), largura):
                parser.feed(self.FONTE[inicio:inicio + largura])
            parser.close()
            parser.flush()
            self.assertEqual(parser.blocks, inteiro.blocks)


if __name__ == '__main__':
    unittest.main()
