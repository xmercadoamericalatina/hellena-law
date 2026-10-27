import io
import unittest
import zipfile
from auditar_docx_sapl import extrair_simples
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
def docx(body,extras=None):
 out=io.BytesIO()
 with zipfile.ZipFile(out,'w') as z:
  z.writestr('word/document.xml',f'<w:document xmlns:w="{W}"><w:body>{body}</w:body></w:document>')
  for name,content in (extras or {}).items():z.writestr(name,content)
 return out.getvalue()
class DocxTest(unittest.TestCase):
 def test_paragrafos_explicitos_integrais(self):
  text,parts=extrair_simples(docx('<w:p><w:r><w:t>Art.1º Texto</w:t></w:r></w:p><w:p><w:r><w:t>0</w:t></w:r></w:p>'))
  self.assertEqual(text,'Art.1º Texto\n\n0');self.assertEqual(len(parts),1)
 def test_numero_gerado_imagem_tabela_ou_revisao_exigem_reter(self):
  for body,extras in [('<w:p><w:pPr><w:numPr/></w:pPr><w:r><w:t>Item</w:t></w:r></w:p>',{}),('<w:tbl/>',{}),('<w:p><w:del/></w:p>',{}),('<w:p/>',{'word/media/logo.png':b'png'})]:
   with self.assertRaises(ValueError):extrair_simples(docx(body,extras))
 def test_anexo_hiperlink_e_texto_adicional_nao_podem_ser_ignorados(self):
  for extras in [{'word/_rels/document.xml.rels':'<Relationships><Relationship TargetMode="External" Target="https://oficial/anexo.pdf"/></Relationships>'},{'word/footer1.xml':f'<w:ftr xmlns:w="{W}"><w:p><w:r><w:t>Conteúdo adicional</w:t></w:r></w:p></w:ftr>'},{'word/styles.xml':f'<w:styles xmlns:w="{W}"><w:vanish/></w:styles>'}]:
   with self.assertRaises(ValueError):extrair_simples(docx('<w:p/>',extras))
 def test_numeracao_herdada_e_fonte_de_simbolo_exigem_revisao(self):
  body='<w:p><w:pPr><w:pStyle w:val="Norma"/></w:pPr><w:r><w:t>Texto</w:t></w:r></w:p>'
  styles=f'<w:styles xmlns:w="{W}"><w:style w:styleId="Norma"><w:basedOn w:val="Auto"/></w:style><w:style w:styleId="Auto"><w:pPr><w:numPr/></w:pPr></w:style></w:styles>'
  with self.assertRaisesRegex(ValueError,'numeração herdada'):extrair_simples(docx(body,{'word/styles.xml':styles}))
  symbol=f'<w:p><w:r><w:rPr><w:rFonts w:ascii="Wingdings"/></w:rPr><w:t>a</w:t></w:r></w:p>'
  with self.assertRaisesRegex(ValueError,'fonte simbólica'):extrair_simples(docx(symbol))
if __name__=='__main__':unittest.main()
