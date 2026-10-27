"""Verifica offline preservação e associação de respostas distintas da mesma URN."""
import ast
import gzip
import hashlib
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parent))
import baixar_federal as f


def main():
    ast.parse(Path(f.__file__).read_text())
    d={"tipo":"DEC-n","numero":"1","dataassinatura":"01/01/1900","anoassinatura":"1900","normaNome":"Decreto de teste offline","ementa":"Fixture temporária","id":"offline","norma":"DEC-1-1900-01-01"}
    with tempfile.TemporaryDirectory() as tmp,patch.object(f,"RAIZ",tmp):
        urn=f.montar(d)["urn"]
        raws=[json.dumps({"legislationIdentifier":urn,"legislationLegalForce":v,"encoding":{"contentUrl":"https://normas.leg.br/texto-offline","encodingFormat":"text/html","version":"Original"}},indent=3).encode() for v in [["InForce"],["NotInForce"]]]
        metas=[]
        for raw in raws:
            with patch.object(f,"http_get",return_value=(200,raw)):
                _,meta=f.obter_metadados(urn,"offline")
            assert gzip.decompress(Path(meta.captura["path"]).read_bytes())==raw
            assert meta.captura["sha256"]==hashlib.sha256(raw).hexdigest()
            assert json.loads(raw)==dict(meta)
            metas.append(meta)
        assert metas[0].captura["path"]!=metas[1].captura["path"]
        for raw,meta,want in zip(raws,metas,["false","null"]):
            with patch.object(f,"obter_metadados",return_value=(urn,meta)),patch.object(f,"http_get",return_value=(200,b"<p>Art. 1. Texto normativo de teste sem rede.</p>")):
                f.processar(d)
            path=Path(f.montar(d)["md"])
            texto=path.read_text()
            assert "\nrevogada: "+want+"\n" in texto
            assert hashlib.sha256(raw).hexdigest() in texto
            assert f.yaml_str(json.dumps(meta["legislationLegalForce"],ensure_ascii=False)) in texto
            path.unlink()
        assert all(gzip.decompress(Path(meta.captura["path"]).read_bytes())==raw for meta,raw in zip(metas,raws))
    print("OK: duas respostas imutáveis da mesma URN; força/hash associados à resposta correta; JSON original intacto; zero HTTP.")


if __name__=="__main__":
    main()
