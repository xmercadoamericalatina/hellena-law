"""A ausência de resposta ou paginação incompleta nunca prova ausência de anexos."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import auditar_anexos_sapl as a


class AnexosTest(unittest.TestCase):
    def consultar(self,pages):
        class Rede:
            def __init__(self,**kw): pass
            def get(self,url,**kw):
                n=int(url.rsplit('=',1)[1]);return 200,json.dumps(pages[n-1]).encode(),'application/json'
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(a,'RAIZ',Path(tmp)),patch.object(a,'CACHE',Path(tmp)/'cache'),patch.object(a,'Rede',Rede):return a.consultar_host('sapl.exemplo.leg.br')

    def test_anexo_relacionado_exige_paginacao_completa(self):
        row={'id':1,'norma':55,'anexo_arquivo':'https://sapl.exemplo.leg.br/anexo.pdf'}
        out=self.consultar([{'pagination':{'total_entries':1,'next_page':None},'results':[row]}])
        self.assertEqual(out['estado'],'indice_completo');self.assertEqual(out['anexos'],[row])
        for pages in [
          [{'pagination':{'total_entries':2,'next_page':None},'results':[row]}],
          [{'pagination':{'total_entries':2,'next_page':2},'results':[row]},{'pagination':{'total_entries':2,'next_page':None},'results':[row]}],
          [{'pagination':{'total_entries':1,'next_page':2},'results':[]},{'pagination':{'total_entries':0,'next_page':None},'results':[]}],
          [{'results':[]}]]:
            self.assertEqual(self.consultar(pages)['estado'],'pendente_api')

    def test_sessao_legislativa_nao_e_aviso_de_pregao(self):
        self.assertEqual(a.sinais('remeter plano por ocasião da abertura da sessão legislativa')[0],[])
        self.assertTrue(a.sinais('EDITAL DISPONÍVEL NO SITE DA CÂMARA. ABERTURA DA SESSÃO: dia15.')[0])

    def test_anexo_nao_reproduzido_ou_externo_requer_revisao(self):
        for s in ['Anexo não reproduzido nesta edição.','Anexo disponível em https://oficial.gov.br/tabela.pdf']:
            self.assertTrue(a.sinais(s)[0])
        self.assertTrue(a.sinais('É aprovado o Anexo Único integrante desta Lei.')[1])


if __name__=='__main__':unittest.main()
