"""Súmulas do catálogo oficial TRF4, inclusive canceladas, com precedentes referenciados."""
import argparse
import datetime as dt
import hashlib
import html
import json
from pathlib import Path
import re
import sys
from urllib.parse import urljoin
sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import Rede, yaml_str

RAIZ = Path(__file__).resolve().parent.parent / "jurisprudencia"
URL = "https://www.trf4.jus.br/trf4/controlador.php?acao=sumulas_trf4"


def escrever(p, texto):
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(texto, encoding="utf-8")
    tmp.replace(p)


def analisar(bruto):
    texto = bruto.decode("cp1252")
    marcadores = list(re.finditer(r"<strong>\s*SÚMULA\s+(\d+)\s*</strong>", texto))
    numeros = [int(m[1]) for m in marcadores]
    if not numeros or sorted(numeros) != list(range(1, max(numeros) + 1)):
        raise RuntimeError("catálogo não contém sequência única completa iniciada em1")
    itens = []
    for i, m in enumerate(marcadores):
        fim = marcadores[i + 1].start() if i + 1 < len(marcadores) else texto.index("</div>", m.end())
        bloco = texto[m.end():fim]
        principal = bloco.split("Precedentes:", 1)[0]
        principal = re.sub(r"<br\s*/?>|<hr\s*/?>", "\n", principal, flags=re.I)
        principal = html.unescape(re.sub(r"<[^>]+>", "", principal))
        linhas = [re.sub(r"\s+", " ", ln).strip() for ln in principal.splitlines() if ln.strip()]
        if len(linhas) < 2 or len(linhas[0]) < 30:
            raise RuntimeError(f"súmula {m[1]} sem enunciado/publicação reconhecível")
        links = [(urljoin(URL, href), html.unescape(re.sub(r"<[^>]+>", "", label)).strip())
                 for href, label in re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', bloco, re.S)
                 if href.lower().endswith(".pdf")]
        itens.append({"numero": m[1], "linhas": linhas, "precedentes": links,
                      "cancelada": any(re.search(r"\b[Cc]ancelad[ao]\b", ln) for ln in linhas[1:])})
    return itens


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rps", type=float, default=1)
    ap.add_argument("--refazer", action="store_true")
    a = ap.parse_args()
    if not 0 < a.rps <= 4:
        ap.error("rps deve ser maior que zero e no máximo4")
    cache = RAIZ / "_fonte/trf4/sumulas.html"
    try:
        if not cache.exists():
            st, b, _ = Rede(rps=a.rps).get(URL, tentativas=1)
            if st != 200:
                raise RuntimeError(f"HTTP {st}")
            analisar(b)
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.with_suffix(".tmp").write_bytes(b)
            cache.with_suffix(".tmp").replace(cache)
        bruto = cache.read_bytes()
        itens = analisar(bruto)
        escrever(RAIZ / "_indice/trf4/sumulas.json", json.dumps({"fonte": URL,
            "sha256": hashlib.sha256(bruto).hexdigest(), "total": len(itens),
            "processado_em": dt.date.today().isoformat(), "sumulas": itens}, ensure_ascii=False))
        ok = pulado = 0
        for n in itens:
            p = RAIZ / "trf4/sumulas" / f"sumula-{n['numero']}.md"
            if p.exists() and not a.refazer:
                pulado += 1
                continue
            titulo = f"Súmula nº {n['numero']} do TRF4"
            meta = {"titulo": titulo, "tribunal": "TRF4", "tipo": "Súmula", "numero": n["numero"],
                    "data": "", "versao_texto": "catálogo oficial do TRF4",
                    "fonte": URL, "baixado_em": dt.date.today().isoformat()}
            publicacao = re.search(r"\b(\d{2})[/-](\d{2})[/-](\d{4})\b", n["linhas"][1])
            if publicacao:
                dia, mes, ano = publicacao.groups()
                meta["data_publicacao"] = dt.date(int(ano), int(mes), int(dia)).isoformat()
            corpo = "\n\n".join(n["linhas"])
            if n["precedentes"]:
                corpo += "\n\n## Precedentes\n\n" + "\n".join(f"- [{label}]({url})" for url, label in n["precedentes"])
            cab = ["---"] + [f"{k}: {yaml_str(v)}" for k,v in meta.items()]
            if n["cancelada"]:
                cab.append("revogada: true")
            escrever(p, "\n".join(cab + ["---", "", f"# {titulo}", "", corpo, ""]))
            ok += 1
        print(json.dumps({"novos": ok, "existentes": pulado, "total_catalogo": len(itens),
                          "canceladas": sum(n["cancelada"] for n in itens)}, ensure_ascii=False))
    except Exception as e:
        pasta = RAIZ / "_indice/trf4"
        pasta.mkdir(parents=True, exist_ok=True)
        with (pasta / "falhas.jsonl").open("a") as f:
            f.write(json.dumps({"fonte": URL, "erro": str(e), "quando": dt.datetime.now().isoformat()}) + "\n")
        print("FIM PARCIAL:", e)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
