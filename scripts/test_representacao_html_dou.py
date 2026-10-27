import unittest

from representacao_html_dou import MODO_HTML_NATIVO, representar_fragmento


class RepresentacaoHTMLDouTests(unittest.TestCase):
    def representar(self, corpo):
        return representar_fragmento(corpo, modo=MODO_HTML_NATIVO)

    def test_preserva_caracteres_atributos_valores_e_tabela(self):
        fonte = '<div class="texto-dou"><p style="font-weight:bold">*caput* -100,50; 0,5%; R$ 2,00</p><table><tr><td colspan="2">0</td></tr></table></div>'
        self.assertEqual(self.representar(fonte), fonte)

    def test_lf_sem_wrapper_nem_newline_adicional(self):
        fonte = '<div class="texto-dou">\r\n<p>A</p>\r<p>B</p>\r\n</div>'
        self.assertEqual(self.representar(fonte), fonte.replace('\r\n', '\n').replace('\r', '\n'))

    def test_espacos_finais_so_em_nos_textuais(self):
        fonte = '<div class="texto-dou"><p>A \t\nB</p></div>'
        self.assertEqual(self.representar(fonte), '<div class="texto-dou"><p>A&#32;&#9;\nB</p></div>')
        with self.assertRaises(ValueError):
            self.representar('<div class="texto-dou"><p title="A \nB">C</p></div>')

    def test_rejeita_modo_desconhecido(self):
        with self.assertRaises(ValueError):
            representar_fragmento('<div class="texto-dou">A</div>', modo='outro')

    def test_rejeita_campo_truncado_ou_texto_alheio(self):
        for fonte in ['<div class="texto-dou"><div>A</div>', '<div class="texto-dou">A</div>B', '<div>A</div>', '<div class="texto-dou">A</div><p>B</p>']:
            with self.subTest(fonte=fonte), self.assertRaises(ValueError):
                self.representar(fonte)

    def test_rejeita_ativos_visuais_e_eventos(self):
        for interno in ['<script>A</script>', '<img src="x">', '<svg></svg>', '<a onclick="x()">A</a>', '<a href="java&#x73;cript:alert(1)">A</a>', '<font face="Wingdings">A</font>']:
            with self.subTest(interno=interno), self.assertRaises(ValueError):
                self.representar('<div class="texto-dou">' + interno + '</div>')

    def test_rejeita_tachado_e_ocultacao_herdados(self):
        for atributo in ['style="text-decoration:line-through"', 'style="display:none"', 'style="visibility:hidden"', 'style="opacity:0"', 'style="font-size:0pt"', 'hidden', 'class="revogado"', 'style="dis/**/play:none"']:
            with self.subTest(atributo=atributo), self.assertRaises(ValueError):
                self.representar('<div class="texto-dou"><span ' + atributo + '><b>A</b></span></div>')
        for tag in ['s', 'strike', 'del']:
            with self.subTest(tag=tag), self.assertRaises(ValueError):
                self.representar('<div class="texto-dou"><' + tag + '>A</' + tag + '></div>')

    def test_representacao_idempotente(self):
        fonte = '<div class="texto-dou"><p>Literal *** ----  \r\n0</p></div>'
        resultado = self.representar(fonte)
        self.assertEqual(self.representar(resultado), resultado)

    def test_entidades_literais_e_limites(self):
        fonte = '<div class="texto-dou">A &amp; B &#60; 0</div>'
        self.assertEqual(self.representar(fonte), fonte)
        self.assertEqual(self.representar(fonte + '\n\n'), fonte + '\n\n')
        for externo in ['&amp;' + fonte, fonte + '&#65;', fonte + '</p>']:
            with self.subTest(externo=externo), self.assertRaises(ValueError):
                self.representar(externo)
        com_indentacao = self.representar(fonte + '\n  ')
        self.assertEqual(com_indentacao, fonte + '\n&#32;&#32;')
        self.assertEqual(self.representar(com_indentacao), com_indentacao)
        with self.assertRaises(ValueError):
            self.representar('<div class="texto-dou" class="outro">A</div>')


if __name__ == '__main__':
    unittest.main()
