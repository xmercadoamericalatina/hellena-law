"""Confronto independente conserva números de tabelas e exige margens comprovadas."""
import unittest
from auditar_integralidade_pdf_sapl import confrontar


def bbox(paginas):
    return '<html><doc>'+''.join('<page height="1000">'+''.join('<line yMin="%s" yMax="%s">%s</line>'%(y,y+10,''.join('<word>'+w+'</word>' for w in txt.split())) for y,txt in linhas)+'</page>' for linhas in paginas)+'</doc></html>'


class IntegralidadePDFTest(unittest.TestCase):
    def test_numero_interno_perdido_retem(self):
        layout='1\nArt. 1 Texto\n26\nValor 455,83\f'
        xml=bbox([[(20,'1'),(200,'Art. 1 Texto'),(450,'26'),(470,'Valor 455,83')]])
        d=confrontar(layout,xml,'Art. 1 Texto\nValor 455,83')
        self.assertFalse(d['tokens_em_ordem_identicos'])
        self.assertEqual(d['numeros_sem_prova_de_folio'][0]['linha'],'26')
        self.assertEqual([x['linha'] for x in d['margens_excluidas']],['1'])

    def test_cabecalho_repetido_e_folio_com_coordenadas(self):
        layout='1\nCAMARA MUNICIPAL\nArt. 1 Texto\f2\nCAMARA MUNICIPAL\nArt. 2 Texto\f'
        xml=bbox([[(20,'1'),(40,'CAMARA MUNICIPAL'),(200,'Art. 1 Texto')],[(20,'2'),(40,'CAMARA MUNICIPAL'),(200,'Art. 2 Texto')]])
        d=confrontar(layout,xml,'**Art. 1** Texto\n\n**Art. 2** Texto')
        self.assertTrue(d['tokens_em_ordem_identicos'])
        self.assertFalse(d['numeros_sem_prova_de_folio'])
        self.assertEqual(len(d['margens_excluidas']),4)

    def test_numero_sem_coordenadas_nao_e_confirmado(self):
        d=confrontar('1\nArt. 1 Texto\f',bbox([[(200,'Art. 1 Texto')]]),'Art. 1 Texto')
        self.assertEqual(d['numeros_sem_prova_de_folio'][0]['linha'],'1')


if __name__=='__main__':unittest.main()
