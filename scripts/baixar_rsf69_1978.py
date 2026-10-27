"""Reproduz offline a RSF69/1978 e seus documentos referidos, revistos página a página."""
import argparse
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from baixar_federal import carregar_indice, montar, numero_oficial
from comum import yaml_str

RAIZ = Path(__file__).resolve().parent.parent
URN = "urn:lex:br:senado.federal:resolucao:1978-09-19;69"
PDF_SHA = "601787e2b22bb0e036adbde1cecbfd603351ab86b604e1f7c7758cb76f29eb47"
NORMA_SHA = "7bc145332d7bb85da7a19221b52ffae5fd7afc9a8499952ecc317da0b3e8cfe1"
LEDGER_SHA = "ceb6a67848fffc72eb38034e74e85c93a9c47b63dac1ef022e9c1ac660b8fda1"
AVISO = "> Transcrição visual conferida do ato e dos documentos referidos, nas páginas impressas 4676–4684. O OCR foi revisto integralmente por confronto com o PDF oficial. Grafias e lapsos da impressão foram preservados; quebras de linha e separadores tipográficos foram normalizados.\n\n"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def corpo_revisado():
    r = json.loads((RAIZ / "federal/_transcricao_rsf69_1978.json").read_text())
    assert (r["urn"], r["numero"], r["data"], r["data_publicacao"]) == (URN, "69", "1978-09-19", "1978-09-22")
    assert r["sha256_pdf"] == PDF_SHA and r["sha256_texto_norma"] == NORMA_SHA
    assert sha(gzip.decompress((RAIZ / r["cache_pdf"]).read_bytes())) == r["sha256_pdf"]
    norma = r["texto_norma"]
    assert sha(norma.encode()) == r["sha256_texto_norma"]
    assert norma.startswith("RESOLUÇÃO Nº 69, DE 1978\n")
    assert "Sala das Sessões, 19 de setembro de 1978." in norma
    assert "nove membros" in norma and "noventa dias" in norma and "quinhentos mil cruzeiros" in norma
    ledger = (RAIZ / "federal/_revisao_rsf69_anexos.jsonl").read_bytes()
    assert sha(ledger) == LEDGER_SHA
    revisoes = [json.loads(l) for l in ledger.decode().splitlines()]
    assert [x["pagina_pdf"] for x in revisoes] == list(range(16, 25))
    partes = []
    for x in revisoes:
        assert x["conferencia_literal_extensao_inteira"] and not x["ambiguidades"]
        bruto = (RAIZ / x["ocr_original"]).read_bytes()
        assert sha(bruto) == x["sha256_ocr"]
        t = bruto.decode()[x["extracao_inicio"]:x["extracao_fim"]]
        t = re.sub(r"(?<=\w)-\n(?=\w)", "", t)
        for antigo, novo in x["correcoes"].items():
            assert antigo in t, (x["pagina_pdf"], antigo)
            t = t.replace(antigo, novo)
        t = re.sub(r"(?<!\n)\n(?!\n)", " ", t).strip() + "\n"
        if x["normalizar_hifen_remanescente_entre_linhas"]:
            t = re.sub(r"(?<=\w)-\n+(?=\w)", "", t)
        for antigo, novo in x["correcoes_pos_normalizacao"].items():
            assert antigo in t, (x["pagina_pdf"], antigo)
            t = t.replace(antigo, novo)
        assert sha(t.encode()) == x["sha256_revisado"]
        assert t == (RAIZ / x["revisado"]).read_text()
        assert sha((RAIZ / x["render"]).read_bytes()) == x["sha256_render"]
        partes.append(f'### Página {x["pagina_impressa"]} (PDF {x["pagina_pdf"]})\n\n' + t.strip())
    assert partes[-1].endswith("dores de poupança.")
    corpo = AVISO + norma + "\n\n## Documentos a que se refere a resolução\n\n" + "\n\n".join(partes)
    return r, corpo


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--auditar", action="store_true")
    args = ap.parse_args()
    r, corpo = corpo_revisado()
    candidatos = [d for d in carregar_indice({"RSF"}) if montar(d)["urn"] == r["urn"]]
    assert len(candidatos) == 1
    d = candidatos[0]
    info = montar(d)
    assert numero_oficial(d) == r["numero"] and info["data"] == r["data"]
    path = Path(info["md"])
    if args.auditar:
        atual = path.read_text().split("---\n", 2)[2].strip().split("\n\n", 1)[1]
        assert atual == corpo, path
        print("auditado", path, sha(corpo.encode()))
        return
    if path.exists():
        raise ValueError(f"destino existente; use --auditar: {path}")
    meta = {"titulo": d["normaNome"], "tipo": info["nome"], "numero": numero_oficial(d), "data": info["data"], "data_publicacao": r["data_publicacao"], "ementa": d.get("ementa", ""), "urn": info["urn"], "revogada": None, "versao_texto": "publicação original no Diário do Congresso Nacional (Seção II), com documentos referidos", "metodo_extracao": "transcrição visual do ato; OCR dos documentos referidos integralmente revisto por confronto visual", "fonte": r["fonte"], "id_senado": d["id"], "paginas_fonte": "PDF16–24; impressas4676–4684", "sha256_pdf_fonte": r["sha256_pdf"], "sha256_texto": sha(corpo.encode()), "sha256_texto_normativo": r["sha256_texto_norma"], "baixado_em": dt.date.today().isoformat()}
    cab = "---\n" + "".join(k + ": " + ("null" if v is None else yaml_str(str(v))) + "\n" for k, v in meta.items()) + "---\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(cab + "# " + d["normaNome"] + "\n\n" + corpo + "\n")
    print("ok", path, len(corpo))


if __name__ == "__main__":
    main()
