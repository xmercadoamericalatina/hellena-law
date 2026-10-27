import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from epigrafe_tipo_literal_ta import analisar


class TipoLiteral(unittest.TestCase):
    def test_tipos_reais_com_sufixo_literal(self):
        for kind, number, date, title in [
            ('Lei Ordinária-MUN','1319','2023-11-22','Lei Ordinária-MUN nº 1.319, de 22 de novembro de 2023'),
            ('Decreto-SEMPOG','19415','2023-09-27','Decreto-SEMPOG nº 19.415, de 27 de setembro de 2023'),
            ('Decreto-GABPRES','11','2023-08-28','Decreto-GABPRES nº 11, de 28 de agosto de 2023'),
            ('Emenda à Lei Orgânica','82','2023-09-18','Emenda à Lei Orgânica nº 82, de 18 de setembro de 2023')]:
            with self.subTest(kind=kind):
                r=analisar(dict(tipo=kind,numero=number,data=date),title)
                self.assertTrue(r['numero_literal_confirmado'])
                self.assertTrue(r['data_literal_confirmada'])
                self.assertFalse(r['divergencias'])

    def test_nao_inventa_sufixo_ou_data(self):
        m=dict(tipo='Lei Ordinária-MUN',numero='1319A',data='2023-11-22')
        self.assertFalse(analisar(m,'Lei Ordinária-MUN nº 1.319, de 22 de novembro de 2023')['numero_literal_confirmado'])
        self.assertFalse(analisar(dict(m,numero='1319'),'Lei Ordinária-MUN nº 1.319/2023')['data_literal_confirmada'])
        self.assertFalse(analisar(dict(m,numero='1319'),'Lei Ordinária-OUTRO nº 1.319, de 22 de novembro de 2023')['numero_literal_confirmado'])

    def test_divergencia_legada_nao_e_descartada(self):
        r=analisar(dict(tipo='Lei Ordinária-MUN',numero='1319',data='2023-11-22'),
            'Lei nº 1.320, de 22 de novembro de 2023\nLei Ordinária-MUN nº 1.319, de 22 de novembro de 2023')
        self.assertFalse(r['numero_literal_confirmado'])
        self.assertTrue(r['divergencias'])

    def test_mes_acentuado_ordinais_e_zeros(self):
        r=analisar(dict(tipo='Resolução-MD',numero='3',data='2023-03-01'),'Resolução-MD nº 003, de 1º de março de 2023')
        self.assertTrue(r['numero_literal_confirmado']);self.assertTrue(r['data_literal_confirmada'])


if __name__=='__main__':unittest.main()
