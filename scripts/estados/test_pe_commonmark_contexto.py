from pathlib import Path
import unittest
try:
 from auditar_pe_commonmark_contexto import parser,Counters,texto_visivel_html as visible
except ImportError:
 parser=None;Counters=None;visible=None
def render(text):
 tokens=parser.parse(text);lists=[dict(start=t.attrGet('start') or 1,markup=t.markup,linhas=t.map) for t in tokens if t.type=='ordered_list_open'];c=Counters(lists);c.feed(parser.render(text));return visible(''.join(c.out)),c.proofs
@unittest.skipIf(parser is None, 'QA opcional requer markdown-it-py==4.0.0')
class Tests(unittest.TestCase):
 def test_inicio_explicito(self):self.assertEqual(render('4) A\n5) B\n')[0],'4) A 5) B')
 def test_salto_nao_inventado(self):self.assertEqual(render('1) A\n3) B\n')[0],'1) A 2) B')
 def test_inicio_padrao_estrutural(self):self.assertEqual(render('1. A\n2. B\n')[1][0]['inicio_efetivo'],1)
 def test_aninhadas(self):self.assertEqual(render('1. A\n   7) X\n   8) Y\n2. B\n')[0],'1. A 7) X 8) Y 2. B')
 def test_decimal_sinal_percentual(self):self.assertIn('-100,50; 0,5%',render('1) Valor -100,50; 0,5%\n')[0])
if __name__=='__main__':unittest.main()
