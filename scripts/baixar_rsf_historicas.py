"""Reproduz transcrições visuais históricas vinculadas ao PDF oficial preservado."""
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
AVISO = "> Transcrição visual conferida do Diário do Congresso Nacional: a extração automática apresenta erros. O PDF oficial e a página integral permanecem preservados; quebras e separadores tipográficos foram normalizados.\n\n"


def sha(bruto):
    return hashlib.sha256(bruto).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--auditar", action="store_true")
    args = ap.parse_args()
    primario = {montar(d)["urn"]: d for d in carregar_indice({"RSF"})}
    registros = json.loads((RAIZ / "federal/_transcricoes_rsf_historicas.json").read_text())
    for r in registros:
        d = primario[r["urn"]]
        info = montar(d)
        assert numero_oficial(d) == r["numero"] and info["data"] == r["data"]
        for campo, digest, comprimido in [("cache_pdf", "sha256_pdf", True), ("cache_layout", "sha256_layout", True), ("render", "sha256_render", False)]:
            bruto = (RAIZ / r[campo]).read_bytes()
            assert sha(gzip.decompress(bruto) if comprimido else bruto) == r[digest], r[campo]
        texto = r["texto_verificado"]
        assert texto.startswith(f'RESOLUÇÃO Nº {r["numero"]}, DE 1982\n')
        dia = "16 de agosto" if r["data"] == "1982-08-16" else "30 de setembro"
        assert f"Sala das Comissões, {dia} de 1982." in texto
        assert "Artigo único." in texto and "O Senado Federal resolve:" in texto
        corpo = AVISO + texto
        path = Path(info["md"])
        if args.auditar:
            atual = path.read_text().split("---\n", 2)[2].strip().split("\n\n", 1)[1]
            assert atual == corpo, path
            print("auditado", path, sha(corpo.encode()))
            continue
        if path.exists():
            raise ValueError(f"destino já existe; use --auditar: {path}")
        meta = {"titulo": d["normaNome"], "tipo": info["nome"], "numero": numero_oficial(d), "data": info["data"], "ementa": d.get("ementa", ""), "urn": info["urn"], "revogada": None, "versao_texto": "publicação original no Diário do Congresso Nacional (Seção II)", "metodo_extracao": "transcrição visual conferida", "fonte": r["fonte"], "id_senado": d["id"], "pagina_impressa": str(r["pagina_impressa"]), "sha256_pdf_fonte": r["sha256_pdf"], "sha256_texto": sha(corpo.encode()), "sha256_texto_normativo": sha(texto.encode()), "baixado_em": dt.date.today().isoformat()}
        cab = "---\n" + "".join(k + ": " + ("null" if v is None else yaml_str(str(v))) + "\n" for k, v in meta.items()) + "---\n"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(cab + "# " + d["normaNome"] + "\n\n" + corpo + "\n")
        with (RAIZ / "federal/_recuperacoes_rsf_historicas.jsonl").open("a") as f:
            f.write(json.dumps({"path": str(path.relative_to(RAIZ)), **meta}, ensure_ascii=False) + "\n")
        print("ok", path)


if __name__ == "__main__":
    main()
