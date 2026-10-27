import unittest
import hashlib
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from pdf_texto_fiel import formatar_camada_textual, validar_inventario_imagens, conferir_visuais_pdf


class CamadaTextualFiel(unittest.TestCase):
    def test_preserva_valores_e_repeticoes(self):
        original = 'Art. 1º Tabela\n  Índice  Valor\n  0       001\n0\n123\nCabeçalho repetido\n\fCabeçalho repetido\n0\n'
        corpo = formatar_camada_textual(original)
        self.assertIn('  0       001\n0\n123\n', corpo)
        self.assertEqual(corpo.count('Cabeçalho repetido'), 2)
        self.assertIn('Página 2 da camada textual', corpo)

    def test_recurso_visual_exige_comprovacao(self):
        registro = 'cabeçalho\n---\n 1 0 image 46 64 index 1 4 image no [inline] 71 71 572B 39%\n'
        with self.assertRaises(ValueError):
            validar_inventario_imagens(registro)
        validar_inventario_imagens(registro, {(46, 64)})
        with self.assertRaises(ValueError):
            validar_inventario_imagens(registro.replace('46 64', '80 90'), {(46, 64)})

    def test_mesmas_dimensoes_hash_desconhecido_retido(self):
        imagem = b'imagem normativa diferente do brasao'
        inventario = b'header\n---\n1 0 image 46 64 index 1 4 image no 1 0 71 71 572B 39%\n'

        def executar(argumentos, **kwargs):
            if argumentos[1] == '-png':
                Path(argumentos[-1] + '-000.png').write_bytes(imagem)
            return SimpleNamespace(returncode=0, stdout=inventario, stderr=b'')

        with patch('pdf_texto_fiel.subprocess.run', side_effect=executar):
            with self.assertRaisesRegex(ValueError, 'hash visual'):
                conferir_visuais_pdf(b'%PDF', {(46, 64)}, {'hash-do-brasao'})
            conferir_visuais_pdf(b'%PDF', {(46, 64)}, {hashlib.sha256(imagem).hexdigest()})

    def test_cerca_nao_interrompe_fonte(self):
        self.assertIn('````text\n```\n', formatar_camada_textual('```\n'))


if __name__ == '__main__':
    unittest.main()
