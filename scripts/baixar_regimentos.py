"""Regimentos consolidados nas publicações oficiais das três Casas, com fontes em cache."""
import datetime as dt
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from baixar_camara import corpo_norma, obter
from comum import Rede, texto_pdf_para_md, yaml_str
from html2md import convert

RAIZ = Path(__file__).resolve().parent.parent / "federal"
DOCUMENTOS = [
    ("senado", "Regimento Interno do Senado Federal", "93", "1970-11-27",
     "https://www25.senado.leg.br/documents/12427/45868/RISF+2018+Volume+1.pdf/cd5769c8-46c5-4c8a-9af7-99be436b89c4",
     "2025-07", "Art. 413"),
    ("congresso", "Regimento Comum do Congresso Nacional e normas conexas", "1", "1970-08-11",
     "https://www25.senado.leg.br/documents/59501/97171143/RCCN.pdf/933b504d-a653-4df5-9329-d4f38c42f64f",
     "2025-07", "Art. 153"),
    ("camara", "Regimento Interno da Câmara dos Deputados", "17", "1989-09-21",
     "https://www2.camara.leg.br/legin/fed/rescad/1989/resolucaodacamaradosdeputados-17-21-setembro-1989-320110-normaatualizada-pl.html",
     "", "Art. 280"),
]


def main():
    rede = Rede(1)
    cache = RAIZ / "_fonte" / "regimentos"
    cache.mkdir(parents=True, exist_ok=True)
    for slug, titulo, numero, data, url, atualizado, artigo_final in DOCUMENTOS:
        destino = RAIZ / "regimentos" / f"regimento-{slug}.md"
        if destino.exists():
            print("pulado", destino.name, flush=True)
            continue
        if slug == "camara":
            corpo = convert(corpo_norma(obter(rede, url)))
        else:
            pdf = cache / f"regimento-{slug}.pdf"
            if not pdf.exists():
                st, bruto, _ = rede.get(url, timeout=60)
                if st != 200 or not bruto.startswith(b"%PDF"):
                    raise ValueError(f"fonte não devolveu PDF válido: HTTP {st}: {url}")
                tmp = pdf.with_suffix(".tmp")
                tmp.write_bytes(bruto)
                tmp.replace(pdf)
            r = subprocess.run(["rtk", "proxy", "pdftotext", "-q", "-layout", "-enc", "UTF-8", str(pdf), "-"],
                               capture_output=True, check=True, timeout=60)
            corpo = texto_pdf_para_md(r.stdout.decode("utf-8"))
        if len(corpo) < 50000 or not re.search(re.escape(artigo_final).replace(r"\ ", r"\s+"), corpo):
            raise ValueError(f"extração incompleta: {slug}")
        valores = {"titulo": titulo, "tipo": "Regimento Interno", "numero": numero, "data": data,
                   "ementa": titulo, "revogada": False, "versao_texto": "compilada (edição da fonte)",
                   "fonte": url, "baixado_em": dt.date.today().isoformat()}
        if atualizado:
            valores["atualizado_ate"] = atualizado
        linhas = ["---"]
        for k, v in valores.items():
            linhas.append(f"{k}: {str(v).lower() if isinstance(v, bool) else v if k in ('data', 'baixado_em') else yaml_str(v)}")
        linhas += ["---", "", "# " + titulo, "", corpo]
        destino.parent.mkdir(parents=True, exist_ok=True)
        tmp = destino.with_suffix(".tmp")
        tmp.write_text("\n".join(linhas), encoding="utf-8")
        tmp.replace(destino)
        print("ok", destino.name, len(corpo), "caracteres", flush=True)


if __name__ == "__main__":
    main()
