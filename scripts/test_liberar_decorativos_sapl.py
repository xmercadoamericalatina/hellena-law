"""Uma imagem revista não libera outro objeto ou variante que não foi visto."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import liberar_decorativos_sapl as script


def sha(b):return hashlib.sha256(b).hexdigest()


class DecorativosTest(unittest.TestCase):
    def test_objeto_inline_nao_tem_identidade_reutilizavel(self):
        self.assertFalse(script.objetos_validos([{'object_id':['[inline]','-']}]))
        self.assertTrue(script.objetos_validos([{'object_id':['24','0']}]))

    def test_todos_objetos_e_hashes_devem_estar_cobertos(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cat=root/'catalogo';cat.mkdir();control=root/'controle';control.mkdir()
            norm='municipais/XX/exemplo/leis-ordinarias/2025/lei-1.md';p=root/norm;p.parent.mkdir(parents=True)
            p.write_text('---\nfonte: "https://sapl.exemplo.leg.br/norma/1"\ncodigo_ibge: "1"\n---\n\n# Lei1\n\nArt.1 Texto\n')
            raw=root/'municipais/_fonte/organicas-sapl/sapl.exemplo.leg.br/1.bin';raw.parent.mkdir(parents=True);raw.write_bytes(b'%PDF-fonte')
            g={'path':norm,'sha256':sha(p.read_bytes()),'aprovado':False,'imagens':[{'object_id':['1','0']},{'object_id':['2','0']}]}
            (control/'resultados.jsonl').write_text(json.dumps(g)+'\n');(control/'entrega-final.json').write_text('{}')
            (cat/'catalogo.json').write_text('{}');ims=[]
            for n in (1,2):
                image=root/f'imagem{n}.png';image.write_bytes(('pix'+str(n)).encode());ims.append({'object_id':[str(n),'0'],'sha256':sha(image.read_bytes()),'path':image.name,'pagina':1})
            d={'path':norm,'sha256_md_revisado':sha(p.read_bytes()),'sha256_fonte':sha(raw.read_bytes()),'imagens':ims}
            rev=root/'revisao.json'
            def run(seq,cobertura,aprovacoes):
                (cat/'documentos.jsonl').write_text(json.dumps({**d,'imagens':ims[:cobertura]})+'\n')
                rev.write_text(json.dumps({'catalogo_sha256':sha((cat/'catalogo.json').read_bytes()),'imagens':[{**x,'aprovado_como_decorativo':True,'tipo':'brasão'} for x in ims[:aprovacoes]]}))
                out=root/('out'+str(seq))
                with patch.object(script,'RAIZ',root),patch('sys.argv',['prog','--catalogo',str(cat),'--revisao',str(rev),'--controle-imagens',str(control),'--saida',str(out)]),contextlib.redirect_stdout(io.StringIO()):script.main()
                return json.loads((out/'entrega-final.json').read_text())['aprovados']
            self.assertEqual(run(1,1,2),0)  # segundo objeto não extraído
            self.assertEqual(run(2,2,1),0)  # extraído, mas não visto
            self.assertEqual(run(3,2,2),1)  # todos objetos extraídos e vistos


if __name__=='__main__':unittest.main()
