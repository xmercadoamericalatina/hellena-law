"""Reproduz publicação oficial com data divergente do índice, sem escolher uma delas."""
import argparse
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from baixar_federal import carregar_indice, montar, numero_oficial
from comum import yaml_str

RAIZ = Path(__file__).resolve().parent.parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--auditar", action="store_true")
    args = ap.parse_args()
    primario = {montar(d)["urn"]: d for d in carregar_indice({"RSF"})}
    for r in json.loads((RAIZ / "federal/_transcricoes_rsf_data_incerta.json").read_text()):
        d = primario[r["urn"]]
        info = montar(d)
        assert numero_oficial(d) == r["numero"] and info["data"] == r["data_indice"]
        assert r["data_indice"] != r["data_fecho_fonte"]
        for campo, digest, comprimido in [("cache_pdf", "sha256_pdf", True), ("cache_metadados", "sha256_json_metadados", True), ("render", "sha256_render", False)]:
            b = (RAIZ / r[campo]).read_bytes()
            assert sha(gzip.decompress(b) if comprimido else b) == r[digest], r[campo]
        texto = r["texto_verificado"]
        assert f'RESOLUÇÃO Nº {r["numero"]}, DE {r["ano"]}' in texto
        assert "Senado Federal, 2 de junho de 1967." in texto
        titulo = f'Resolução do Senado Federal nº {r["numero"]}, de {r["ano"]} (data divergente)'
        aviso = "> Data incerta: o índice oficial registra 1º de junho de 1967; o fecho do original registra 2 de junho de 1967. A edição original é de 3 de junho, enquanto a referência do índice informa 7 de junho. As divergências foram preservadas, sem escolher uma data. O URN e o caminho conservam a identificação do índice.\n\n> Transcrição visual conferida do original; grafias dos nomes preservadas. A coletânea também registra o fecho de 2 de junho, mas possui diferenças de grafia.\n\n"
        corpo = aviso + texto
        path = Path(info["md"])
        if args.auditar:
            atual = path.read_text().split("---\n", 2)[2].strip().split("\n\n", 1)[1]
            assert atual == corpo, path
            print("auditado", path, sha(corpo.encode()))
            continue
        if path.exists():
            raise ValueError(f"destino existente; use --auditar: {path}")
        meta = {"titulo": titulo, "titulo_indice": d["normaNome"], "tipo": info["nome"], "numero": numero_oficial(d), "data": "", "data_indice": r["data_indice"], "data_fecho_fonte": r["data_fecho_fonte"], "data_publicacao": r["data_publicacao_fonte"], "data_publicacao_indice": r["data_publicacao_indice"], "estado_data": "divergência entre índice oficial e fecho original", "ementa": d.get("ementa", ""), "urn": info["urn"], "revogada": None, "versao_texto": "publicação original no Diário do Congresso Nacional (Seção II)", "metodo_extracao": "transcrição visual conferida", "fonte": r["fonte"], "id_senado": d["id"], "sha256_pdf_fonte": r["sha256_pdf"], "sha256_metadados_fonte": r["sha256_json_metadados"], "sha256_texto": sha(corpo.encode()), "sha256_texto_normativo": sha(texto.encode()), "baixado_em": dt.date.today().isoformat()}
        cab = "---\n" + "".join(k + ": " + ("null" if v is None else yaml_str(str(v))) + "\n" for k, v in meta.items()) + "---\n"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(cab + "# " + titulo + "\n\n" + corpo + "\n")
        with (RAIZ / "federal/_recuperacoes_rsf_data_incerta.jsonl").open("a") as f:
            f.write(json.dumps({"path": str(path.relative_to(RAIZ)), **meta}, ensure_ascii=False) + "\n")
        print("ok", path)


if __name__ == "__main__":
    main()
