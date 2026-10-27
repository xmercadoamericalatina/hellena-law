"""Regenera o corpo dos .md a partir do HTML bruto guardado em _fonte, com a versão atual do conversor.

Mantém o front matter e o título; PDFs e textos obtidos por OCR não são tocados (o caminho do PDF não mudou).
Uso: python3 -I scripts/reconverter.py [federal|UF ...]   (sem argumentos: tudo)
"""
import gzip
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import AVISO_OCR, RAIZ_ESTADUAIS, decodificar, html_para_md  # noqa: E402
from html2md import convert  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
# cabeçalhos institucionais removidos por estado (os mesmos dos raspadores)
REMOVER = {
    "SP": {"Assembleia Legislativa do Estado de São Paulo", "Ficha informativa",
    "Assembleia Legislativa do Estado de São Paulo Ficha informativa"},
    "DF": {"Texto Compilado", "Texto Original"},
    "MS": {"Sair", "Editar", "Excluir", "Novo Anexo", "Sair | Editar | Excluir | Novo Anexo"},
    "RS": {"Assembleia Legislativa do Estado do Rio Grande do Sul", "Sistema LEGIS - Texto da Norma",
           "Carregando a página. Aguarde...", "Carregando a página. Aguarde ..."},
    "CE": {"O texto desta Lei não substitui o publicado no Diário Oficial",
           "O texto desta Lei não substitui o publicado no Diário Oficial."},
}


def preprocessar(uf, html):
    if uf == "SC":  # a ALESC usa <s> para o "º/°" sobrescrito
        html = re.sub(r"<s>\s*(&deg;|&ordm;|&ordf;|°|º|ª|o|a)\s*</s>", r"\1", html)
    return html


def reconverter_arquivo(md_path, fonte_path, uf):
    bruto = gzip.open(fonte_path).read()
    if bruto[:4] == b"%PDF" or bruto[:2] == b"PK" or bruto[:5] == b"{\\rtf":
        return False
    texto = open(md_path, encoding="utf-8").read()
    if AVISO_OCR.strip() in texto:
        return False
    partes = texto.split("\n---\n", 1)
    if len(partes) != 2:
        return False
    cabecalho, corpo_antigo = partes
    titulo = corpo_antigo.lstrip("\n").split("\n", 1)[0] if corpo_antigo.lstrip("\n").startswith("# ") else None
    html = preprocessar(uf, decodificar(bruto))
    corpo = convert(html) if uf == "federal" else html_para_md(html, REMOVER.get(uf, ()))
    novo = cabecalho + "\n---\n" + (f"{titulo}\n\n" if titulo else "") + corpo
    if novo != texto:
        tmp = md_path + ".tmp"
        open(tmp, "w", encoding="utf-8").write(novo)
        os.replace(tmp, md_path)
        return True
    return False


def bases(alvos):
    if not alvos or "federal" in alvos:
        yield "federal", os.path.join(RAIZ, "federal")
    for uf in sorted(os.listdir(RAIZ_ESTADUAIS)):
        if (not alvos or uf in alvos) and os.path.isdir(os.path.join(RAIZ_ESTADUAIS, uf, "_fonte")):
            yield uf, os.path.join(RAIZ_ESTADUAIS, uf)


def main():
    alvos = {a.upper() if len(a) == 2 else a for a in sys.argv[1:]}
    for uf, base in bases(alvos):
        fonte_raiz = os.path.join(base, "_fonte")
        mudados = vistos = 0
        for dirpath, _, arquivos in os.walk(fonte_raiz):
            for arq in arquivos:
                if not arq.endswith(".html.gz"):
                    continue
                fonte = os.path.join(dirpath, arq)
                md = os.path.join(base, os.path.relpath(dirpath, fonte_raiz), arq[: -len(".html.gz")] + ".md")
                if not os.path.exists(md):
                    continue
                vistos += 1
                try:
                    mudados += reconverter_arquivo(md, fonte, uf)
                except Exception as e:
                    print(f"[{uf}] erro em {md}: {e}", flush=True)
        print(f"[{uf}] {vistos} arquivos verificados, {mudados} atualizados", flush=True)


if __name__ == "__main__":
    main()
