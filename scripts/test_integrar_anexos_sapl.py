"""Anexos só podem alterar o acervo após revisão vinculada aos bytes originais."""
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import integrar_anexos_sapl_revisados as a
from auditar_municipal import metadados

class IntegracaoAnexoTest(unittest.TestCase):
    def test_fonte_ou_markdown_alterados_bloqueiam_antes_da_extracao(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'n.md').write_bytes(b'alterado')
            with patch.object(a,'RAIZ',root),patch.object(a.subprocess,'check_output') as call:
                with self.assertRaisesRegex(ValueError,'MD mudou'):a.preparar({'path':'n.md','sha256_md_antes':'0'*64})
                call.assert_not_called()

    def test_anexo_adicional_preserva_principal_e_numeros_de_celulas(self):
        old='---\ntipo: "Lei"\nnumero: "1"\nfonte_texto: "https://oficial/principal"\nsha256_fonte: "principal"\nversao_texto: "original"\n---\n\n# Lei1\n\nArt.1 Texto principal\n';raw=b'%PDF teste';images='page num type\n';layout='ANEXO I LEI1\nCARGO VAGAS\n1\n0\n137\n\f'
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'n.md').write_text(old);(root/'a.pdf').write_bytes(raw)
            r={'path':'n.md','sha256_md_antes':a.sha(old.encode()),'arquivo':'a.pdf','sha256_arquivo':a.sha(raw),'modo':'acrescentar','sha256_pdfimages':a.sha(images.encode()),'identidade_regex':'LEI1','titulo_secao':'AnexoI','url':'https://oficial/anexo','nota_editorial':'Fonte adicional','descricao_revisao':'anexo revisado'}
            with patch.object(a,'RAIZ',root),patch.object(a.subprocess,'check_output',side_effect=[images,layout]):before,after,rec=a.preparar(r)
            text=after.decode();self.assertEqual(before,old.encode());self.assertIn('Art.1 Texto principal',text);self.assertIn('\n1\n0\n137\n',text);self.assertEqual(metadados(text)['sha256_fonte'],'principal');self.assertEqual(rec['tokens_adicionais_ou_substitutos'],8)
            body=text.split('\n---\n',1)[1].lstrip('\n').split('\n\n',1)[1].rstrip('\n');self.assertEqual(metadados(text)['sha256_texto'],hashlib.sha256(body.encode()).hexdigest())

if __name__=='__main__':unittest.main()
