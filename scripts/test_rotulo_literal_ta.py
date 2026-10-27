import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar_textos_articulados_sapl_v3 import identidade_titulo


class RotuloLiteral(unittest.TestCase):
    def test_qualificador_oficial_literal_confirma_numero_e_data(self):
        for kind,caption,n,date in [('Lei Ordinária','Lei Ordinária-MUN nº 1.319, de 22 de novembro de 2023','1319','2023-11-22'),('Decreto','Decreto-GABPRES nº 11, de 28 de agosto de 2023','11','2023-08-28')]:
            with self.subTest(caption=caption):
                r=identidade_titulo(dict(tipo=1,numero=n,data=date,__str__=caption),kind,caption)
                self.assertTrue(r['numero_literal_confirmado']);self.assertTrue(r['data_literal_confirmada']);self.assertFalse(r['divergencias'])
                self.assertEqual(r['rotulo_oficial_com_sufixo'],caption)

    def test_apenas_api_nao_confirma_titulo_literal(self):
        m=dict(numero='1319',data='2023-11-22',__str__='Lei Ordinária-MUN nº 1.319, de 22 de novembro de 2023')
        self.assertFalse(identidade_titulo(m,'Lei Ordinária','Título ausente')['numero_literal_confirmado'])
        self.assertFalse(identidade_titulo(m,'Lei Ordinária','Lei Ordinária-OUTRO nº 1.319, de 22 de novembro de 2023')['numero_literal_confirmado'])

    def test_numero_ou_data_da_api_divergente_permanece_retido(self):
        title='Lei Ordinária-MUN nº 1.319, de 22 de novembro de 2023'
        for number,date in [('1319A','2023-11-22'),('1319','2023-11-23')]:
            r=identidade_titulo(dict(numero=number,data=date,__str__=title),'Lei Ordinária',title)
            self.assertTrue(r['divergencias'])

    def test_divergencia_legada_nao_e_ocultada(self):
        cap='Lei Ordinária-MUN nº 1.319, de 22 de novembro de 2023'
        r=identidade_titulo(dict(numero='1319',data='2023-11-22',__str__=cap),'Lei Ordinária','Lei nº 1.320, de 22 de novembro de 2023\n'+cap)
        self.assertTrue(r['divergencias'])


if __name__=='__main__':unittest.main()
