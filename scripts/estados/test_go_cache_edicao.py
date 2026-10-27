import unittest
from auditar_go_cache_edicao import Sinais, SP, POT

class EdicaoGO(unittest.TestCase):
    def test_status_conservador(self):
        from go import revogada_da_situacao
        self.assertIs(revogada_da_situacao("Revogada"),True)
        self.assertIs(revogada_da_situacao("Em Vigor"),False)
        for status in ("",None,"Revogada Parcialmente","Caducada","Declarada Inconstitucional","Sem Efeito","Vigente a partir de 26/10/2026"):
            with self.subTest(status=status):self.assertIsNone(revogada_da_situacao(status))
    def parse(self, s):
        p=Sinais();p.feed(s);p.close();return p
    def test_tachado_herdado_inline(self):
        p=self.parse('<p style="text-decoration: line-through"><b>Redação antiga</b></p><p>Atual</p>')
        self.assertIn('Redação antiga',SP(''.join(p.old)));self.assertEqual(SP(''.join(p.live)),'Atual')
    def test_repeticao_nao_e_exclusiva(self):
        p=self.parse('<s>Redação igual</s><p>Redação igual</p>');self.assertIn(SP(''.join(p.old)),SP(''.join(p.live)))
    def test_css_apenas_sinal_sem_atribuicao(self):
        p=self.parse('<head><style>.antiga{text-decoration:line-through}</style></head><p class="antiga">Texto</p>')
        self.assertEqual(SP(''.join(p.old)),'');self.assertTrue(POT.search(p.rules[0]));self.assertEqual(SP(''.join(p.live)),'Texto')
    def test_atributo_sem_valor(self):
        p=self.parse("<p style class>Texto íntegro</p>");self.assertEqual(SP("".join(p.live)),"Texto íntegro")
    def test_trecho_fragmentado_em_tags(self):
        text="Redação antiga com caracteres suficientes para comprovar a união dos nós textuais sem perder pontuação, 0,5% e -100."
        p=self.parse("<s><b>"+text[:30]+"</b>"+text[30:]+"</s>")
        self.assertEqual(p.blocks,[text])
    def test_sinais_decimais_preservados(self):
        p=self.parse('<p>-100; 0,5%; R$ 0,00</p>');self.assertEqual(SP(''.join(p.live)),'-100; 0,5%; R$ 0,00')

if __name__=='__main__':unittest.main()
