import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import pe
from pe_identidade import identidade_do_texto


class RetomadaTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.raiz = Path(self.temp.name)
        self.item = dict(id='123', tipo='4', nome='Resolução n° 321', textos=['TEXTOORIGINAL'],
                         publicacao='DOE 03/01/2000', ementa='Institui procedimento.')
        self.html = ('<html><head><meta charset="windows-1252"></head><div id="divTexto">'
                     '<p>RESOLUÇÃO Nº 321, DE 2 DE JANEIRO DE 2000.</p>'
                     '<p>Art. 1º A execução da ação fica instituída.</p></div></html>').encode('utf8')
        def paths(uf, pasta, ano, slug):
            return str(self.raiz/uf/pasta/ano/(slug+'.md')), str(self.raiz/uf/'_fonte'/pasta/ano/(slug+'.html.gz'))
        self.patches = [patch.object(pe,'RAIZ_ESTADUAIS',str(self.raiz)),patch.object(pe,'caminhos',paths),
                        patch.object(pe.rede,'get',return_value=(200,self.html,'text/html; charset=utf-8'))]
        for p in self.patches:p.start()
        self.get = pe.rede.get

    def tearDown(self):
        for p in reversed(self.patches):p.stop()
        self.temp.cleanup()

    def md(self):return self.raiz/'PE/resolucoes/2000/res-321-2000-id123.md'

    def test_indice_sem_ano_usa_so_epigrafe_e_preserva_utf8_real(self):
        self.assertEqual(pe.processar(self.item),('ok',None));t=self.md().read_text()
        self.assertIn('ano: "2000"',t);self.assertIn('execução da ação',t)
        self.assertFalse((self.raiz/'PE/resolucoes/sem-ano').exists())
        self.assertEqual(pe.processar(self.item)[0],'pulado');self.assertEqual(self.get.call_count,1)

    def test_ano_da_publicacao_nao_vence_epigrafe(self):
        item=dict(self.item,ano='2001',publicacao='DOE 03/01/2001')
        self.assertEqual(pe.processar(item),('ok',None));t=self.md().read_text()
        self.assertIn('ano_indice: "2001"',t);self.assertIn('data: 2000-01-02',t)

    def test_slug_distinto_mesmo_id_nao_baixa_nem_duplica(self):
        pe.processar(self.item);alias=self.md().with_name('res-outro-slug-id123.md');self.md().rename(alias);pe._ID_RAIZ=None
        status,detail=pe.processar(self.item);self.assertEqual(status,'pulado');self.assertIn(str(alias),detail['paths'])
        self.assertEqual(self.get.call_count,1);self.assertFalse(self.md().exists())

    def test_fonte_divergente_e_tipo_divergente_retidos_sem_abortar(self):
        pe.processar(self.item);p=self.md();p.write_text(p.read_text().replace('id=123&','id=999&'));pe._ID_RAIZ=None
        status,detail=pe.processar(dict(self.item,tipo='8'));self.assertEqual(status,'pulado')
        self.assertTrue(any('fonte' in x for x in detail['divergencias']));self.assertTrue(any('tipo' in x for x in detail['divergencias']))
        self.assertEqual(self.get.call_count,1)

    def test_edicao_e_publicacao_mudadas_sao_diagnostico_sem_novo_download(self):
        pe.processar(self.item)
        status,detail=pe.processar(dict(self.item,textos=['TEXTOORIGINAL','TEXTOATUALIZADO'],publicacao='DOE 04/01/2000'))
        self.assertEqual(status,'pulado');self.assertEqual(self.get.call_count,1)
        self.assertTrue(any('edição' in x for x in detail['divergencias']))
        self.assertTrue(any('publicação' in x for x in detail['divergencias']))

    def test_outro_id_mesma_chave_nao_funde_nem_cria_segunda_norma(self):
        pe.processar(self.item);status,detail=pe.processar(dict(self.item,id='124'))
        self.assertEqual(status,'sem_texto');self.assertIn('ID diferente',detail['motivo']);self.assertEqual(self.get.call_count,2)
        self.assertFalse(self.md().with_name('res-321-2000-id124.md').exists())

    def test_outro_id_outro_numero_e_norma_distinta(self):
        pe.processar(self.item);self.get.return_value=(200,self.html.replace(b'321,',b'322,'),'text/html; charset=utf-8')
        self.assertEqual(pe.processar(dict(self.item,id='124',nome='Resolução n° 322')),('ok',None))
        self.assertEqual(self.get.call_count,2)

    def test_sem_epigrafe_propria_preserva_resposta_sem_md(self):
        self.get.return_value=(200,b'<div id="divTexto">Aviso de indisponibilidade do texto desta norma. Consulte o Diario Oficial.</div>','text/html; charset=utf-8')
        status,detail=pe.processar(self.item);self.assertEqual(status,'sem_texto');self.assertTrue(Path(detail['captura']).exists());self.assertFalse(self.md().exists())

    def test_tipo_citado_e_ano_futuro_nao_definem_identidade(self):
        for body in ['Art. 1º Altera a Resolução Nº321, de2 de janeiro de2000.', 'RESOLUÇÃO Nº321, DE2 DEJANEIRO DE2099.']:
            with self.subTest(body=body),self.assertRaises(ValueError):identidade_do_texto(self.item,body)
        self.assertEqual(identidade_do_texto(dict(self.item,nome='Resolução n° 00321'),'# RESOLUÇÃO Nº321, DE 2 DE JANEIRO DE 2000.')[1],'2000-01-02')


if __name__=='__main__':unittest.main()
