import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import pe
from coletar_pe_infralegal import identidade_primaria


class PEInfralegalTests(unittest.TestCase):
    def test_ano_so_da_epigrafe_propria_incluindo_sufixo(self):
        item = dict(tipo='8', nome='Portaria Administrativa n° 321-C', publicacao='01/01/2026')
        pagina = '<div id="divTexto"><p>PORTARIA ADMINISTRATIVA Nº 321-C, DE 2 DE JANEIRO DE 2000.</p><p>Art. 1º Institui procedimento.</p></div>'
        self.assertEqual(identidade_primaria(item, pagina)[:2], ('321-C', '2000-01-02'))
        for errado in [pagina.replace('321-C,', '322-C,'),
                       pagina.replace('PORTARIA ADMINISTRATIVA', 'RESOLUÇÃO'),
                       '<div id="divTexto"><p>Art. 1º Altera a Portaria nº 321-C, de 2 de janeiro de 2000.</p></div>',
                       pagina.replace('2 DE JANEIRO DE 2000', '2 DE JANEIRO DE 2099')]:
            with self.subTest(errado=errado), self.assertRaises(ValueError):
                identidade_primaria(item, errado)

    def test_tipos_oficiais_roteiam_metadados_data_e_nao_repetem_fetch(self):
        casos = [
            ("4", "Resolução", "resolucoes", "Resolução", "res", "321"),
            ("5", "Decreto Legislativo", "decretos-legislativos", "Decreto Legislativo", "dl", "321"),
            ("8", "Portaria Administrativa", "portarias", "Portaria", "port", "321"),
            ("8", "Portaria Administrativa", "portarias", "Portaria", "port", "321-C"),
        ]
        for codigo, epigrafe, pasta, tipo, prefixo, numero in casos:
            with self.subTest(codigo=codigo), tempfile.TemporaryDirectory() as temp:
                raiz = Path(temp)
                html = ('<html><div id="divTexto"><p>' + epigrafe +
                        ' Nº ' + numero + ', DE 2 DE JANEIRO DE 2000.</p><p>Art. 1º Fica '
                        'instituído o procedimento descrito nesta norma.</p>'
                        '<p>Art. 2º Esta norma entra em vigor na publicação.</p></div></html>')

                def caminhos(uf, folder, ano, slug):
                    return (str(raiz / uf / folder / ano / (slug + '.md')),
                            str(raiz / uf / '_fonte' / folder / ano / (slug + '.html.gz')))

                item = dict(id='987654', tipo=codigo, nome=epigrafe + ' n° ' + numero,
                            ano='2000', publicacao='Publicada no DOE 03/01/2000',
                            textos=['TEXTOORIGINAL'], ementa='Institui procedimento.')
                with patch.object(pe, 'RAIZ_ESTADUAIS', str(raiz)), \
                        patch.object(pe, 'caminhos', caminhos), \
                        patch.object(pe.rede, 'get', return_value=(200, html.encode(), 'text/html; charset=utf-8')) as get:
                    self.assertEqual(pe.processar(item), ('ok', None))
                    self.assertEqual(pe.processar(item), ('pulado', None))
                    self.assertEqual(get.call_count, 1)
                md = raiz / 'PE' / pasta / '2000' / (prefixo + '-' + numero + '-2000-id987654.md')
                texto = md.read_text()
                self.assertIn('tipo: ' + json.dumps(tipo, ensure_ascii=False), texto)
                self.assertIn('numero: ' + json.dumps(numero), texto)
                self.assertIn('data: 2000-01-02', texto)
                self.assertIn('revogada: null', texto)
                self.assertIn('tipo=TEXTOORIGINAL', texto)
                self.assertIn('Art. 1º', texto)


if __name__ == '__main__':
    unittest.main()
