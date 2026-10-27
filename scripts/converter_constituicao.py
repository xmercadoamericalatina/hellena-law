"""Reproduz constituicao.md a partir do snapshot oficial compilado do Planalto.

Uso: python3 scripts/converter_constituicao.py [--check]
O HTML histórico continua em fonte/constituicao.htm. A seleção de redações é a
da fonte compilada: não se infere vigência pela posição, ano ou palavra revogado.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from html2md import LABEL, Parser, heading_level, looks_like_name, render_runs

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / "fonte/constituicao-compilado.htm"
META = FONTE.with_suffix(".json")
DESTINO = RAIZ / "constituicao.md"
ROTULO = re.compile(r"^((?:Art\.|Artigo)\s*\d+[º°.]?(?:-[A-Z]+)?\.?|§§?\s*\d+[º°.]?(?:-[A-Z]+)?\.?|Parágrafo único\.|[IVXLCDM]+\s*-|[a-z]\))\s")


class ConstituicaoParser(Parser):
    def __init__(self):
        super().__init__(exclude_struck=True)

    def flush(self):
        # A formatação da publicação não define a hierarquia do Markdown.
        plain = lambda runs: render_runs([(t, False, False, False) for t, _, _, _ in runs])
        original = plain(self.runs)
        content = plain([run for run in self.runs if not run[3]])
        self.runs = []
        # O Planalto às vezes tacha inclusive o número do dispositivo revogado.
        # Recupera só esse identificador, nunca sua antiga regra material.
        if re.match(r"^[.\s]*(?:\(Revogad[oa]s?\b)", content, re.I):
            content = content.lstrip(". ")
            label = ROTULO.match(original)
            if label and not ROTULO.match(content):
                content = label.group(1) + " " + content
        if content and re.search(r"\w", content):
            self.emitir((self.block_tag or "p", content, self.block_center))


def converter(html_text):
    # Exclui apenas a navegação institucional anterior ao preâmbulo, incluindo
    # sua tabela com brasão. Falha fechado se a identidade da página não confere.
    if "CONSTITUIÇÃO DA REPÚBLICA FEDERATIVA DO BRASIL" not in html_text.upper():
        raise ValueError("fonte não identifica a Constituição Federal")
    preambulo = re.search(r"PREÂMBULO", html_text, re.I)
    if not preambulo:
        raise ValueError("preâmbulo ausente na fonte")
    start = html_text.lower().rfind("<p", 0, preambulo.start())
    if start < 0:
        raise ValueError("parágrafo do preâmbulo ausente")
    p = ConstituicaoParser()
    p.feed(html_text[start:])
    p.close()
    p.flush()
    if p.table_depth:
        raise ValueError("tabela HTML sem fechamento")
    blocks = p.blocks
    out = []
    i = 0
    while i < len(blocks):
        kind, content, _ = blocks[i]
        if kind == "html_table":
            # A fonte tem uma tabela vazia no rodapé.
            if re.search(r"\w", re.sub(r"<[^>]*>", "", content)):
                out.append(content)
            i += 1
            continue
        lvl = heading_level(content)
        if content == "PREÂMBULO":
            out.append("## PREÂMBULO")
        elif content == "ATO DAS DISPOSIÇÕES CONSTITUCIONAIS TRANSITÓRIAS":
            out.append("# " + content)
        elif lvl and len(content) < 250:
            title = re.sub(r"\s*\n\s*", " — ", content)
            if re.fullmatch(r"\S+ [IVXLC]+(?:-[A-Z])?", title, re.I) and i + 1 < len(blocks):
                nk, nc, _ = blocks[i + 1]
                if nk != "html_table" and looks_like_name(nc):
                    title += " — " + nc
                    i += 1
            out.append("#" * max(2, lvl - 1) + " " + title)
        else:
            label = LABEL.match(content)
            if label:
                end = label.end(1)
                content = "**" + content[:end] + "**" + content[end:]
            out.append(content)
        i += 1
    body = "\n\n".join(out).strip() + "\n"
    if not re.search(r"\*\*Art\. 1º\*\*", body) or "**Art. 138." not in body:
        raise ValueError("corpo constitucional incompleto: início ou fim do ADCT ausente")
    return body


def documento(html_bytes, meta):
    if hashlib.sha256(html_bytes).hexdigest() != meta["sha256"]:
        raise ValueError("SHA-256 da fonte diverge do registro de obtenção")
    source = html_bytes.decode(meta["encoding"])
    note = (
        f'> Fonte: [texto compilado do Planalto]({meta["url"]}), obtido em {meta["obtido_em"]}. '
        "Redações tachadas foram omitidas; indicações de revogação, vigência e decisões judiciais foram preservadas. "
        "A compilação não dispensa a consulta às regras de transição e de produção de efeitos das emendas.\n\n"
        "> No art. 7º, a EC 141/2026 prevê implementação gradual da jornada semanal (art. 6º) "
        "e vigência diferida da alteração do inciso XV (art. 10, I). "
        "Consulte as [regras e prazos da emenda](https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc141.htm); "
        "a redação de 40 horas no inciso XIII não significa aplicação imediata desse limite a todos os contratos.\n"
    )
    return "# Constituição da República Federativa do Brasil de 1988\n\n" + note + "\n" + converter(source)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="confere reprodução sem escrever")
    args = ap.parse_args()
    result = documento(FONTE.read_bytes(), json.loads(META.read_text(encoding="utf-8")))
    if args.check:
        if DESTINO.read_text(encoding="utf-8") != result:
            raise SystemExit("constituicao.md diverge do snapshot e conversor")
        print("constituicao.md reproduzido integralmente do snapshot registrado")
    else:
        DESTINO.write_text(result, encoding="utf-8")


if __name__ == "__main__":
    main()
