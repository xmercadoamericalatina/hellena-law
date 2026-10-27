"""Converte o HTML de normas (exportado do Word, como servido pelo normas.leg.br) em Markdown."""
import re
from html.parser import HTMLParser

BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "div", "blockquote"}
SKIP_TAGS = {"head", "style", "script", "title", "xml"}

LABEL = re.compile(
    r"^((?:Art\.|Artigo) ?\d+(?:\.\d+)*\.?[º°o]?(?:-[A-Z]+)?\.?|§ ?\d+\.?[º°]?(?:-[A-Z]+)?\.?|Parágrafo único\.?)(?=\s)"
)
HEADINGS = [
    (re.compile(r"^PARTE (GERAL|ESPECIAL|[IVXLC]+)\b", re.I), 2),
    (re.compile(r"^LIVRO [IVXLC]+(-[A-Z])?\b", re.I), 2),
    (re.compile(r"^LIVRO COMPLEMENTAR\b", re.I), 2),
    (re.compile(r"^TÍTULO [IVXLC]+(-[A-Z])?\b", re.I), 3),
    (re.compile(r"^CAPÍTULO [IVXLC]+(-[A-Z])?\b", re.I), 4),
    (re.compile(r"^SEÇÃO [IVXLC]+(-[A-Z])?\b", re.I), 5),
    (re.compile(r"^SUBSEÇÃO [IVXLC]+(-[A-Z])?\b", re.I), 6),
    (re.compile(r"^ANEXOS?\b(\s+[IVXLC\d]+)?$", re.I), 2),
]


def style_flags(attrs):
    style = (dict(attrs).get("style") or "").replace(" ", "").lower()
    return {
        "b": "font-weight:bold" in style or "font-weight:700" in style,
        "i": "font-style:italic" in style,
        "s": "line-through" in style,
        "center": "text-align:center" in style,
    }


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.fmt = []  # pilha de (tag, flags)
        self.runs = []  # [(texto, bold, italic)]
        self.block_center = False
        self.block_tag = None
        self.blocks = []  # (tipo, conteúdo, centralizado)
        self.tabelas = []  # pilha de tabelas abertas: {"linhas": [[célula, ...]], "celula": [parágrafos] | None}

    # --- formatação inline herdada ---
    def cur(self, key):
        return any(f.get(key) for _, f in self.fmt)

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip += 1
            return
        if tag in ("br",):
            self.runs.append(("\n", False, False))
            return
        if tag == "img":
            return
        flags = style_flags(attrs)
        if tag in ("b", "strong"):
            flags["b"] = True
        if tag in ("i", "em"):
            flags["i"] = True
        if tag in ("s", "strike", "del"):
            flags["s"] = True
        if tag == "table":
            self.flush()
            self.tabelas.append({"linhas": [], "celula": None})
            return
        if tag == "tr" and self.tabelas:
            self.tabelas[-1]["linhas"].append([])
            return
        if tag in ("td", "th") and self.tabelas:
            self.flush()
            self.tabelas[-1]["celula"] = []
            return
        if tag in BLOCK_TAGS:
            self.flush()
            self.block_tag = tag
            self.block_center = flags["center"] or (dict(attrs).get("align") or "").lower() == "center"
        self.fmt.append((tag, flags))

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            self.skip = max(0, self.skip - 1)
            return
        if tag == "table" and self.tabelas:
            self.flush()
            self.fechar_tabela(self.tabelas.pop())
            return
        if tag in ("td", "th") and self.tabelas and self.tabelas[-1]["celula"] is not None:
            self.flush()
            t = self.tabelas[-1]
            if not t["linhas"]:
                t["linhas"].append([])
            t["linhas"][-1].append(t["celula"])
            t["celula"] = None
            return
        # desempilha até a tag correspondente
        for k in range(len(self.fmt) - 1, -1, -1):
            if self.fmt[k][0] == tag:
                del self.fmt[k:]
                break
        if tag in BLOCK_TAGS:
            self.flush()

    def handle_data(self, data):
        if self.skip or self.cur("s"):
            return
        # quebra de linha no fonte HTML é só espaço; quebras reais vêm de <br>
        data = data.replace("\r", " ").replace("\n", " ")
        self.runs.append((data, self.cur("b"), self.cur("i")))

    def emitir(self, bloco):
        """Envia um bloco para a célula aberta da tabela externa, ou para o documento."""
        if self.tabelas and self.tabelas[-1]["celula"] is not None:
            self.tabelas[-1]["celula"].append(bloco)
        else:
            self.blocks.append(bloco)

    def flush(self):
        text = render_runs(self.runs)
        self.runs = []
        if text:
            self.emitir((self.block_tag or "p", text, self.block_center))

    def fechar_tabela(self, t):
        if t["celula"] is not None:  # </td> ausente
            t["linhas"].append([t["celula"]]) if not t["linhas"] else t["linhas"][-1].append(t["celula"])
        linhas = [ln for ln in t["linhas"] if any(c for c in ln)]
        if not linhas:
            return
        texto = lambda cel: " ".join(b[1] if b[0] != "table" else " ".join(" ".join(r) for r in b[1]) for b in cel)
        colunas = max(len(ln) for ln in linhas)
        # tabela de diagramação (comum em páginas antigas e no Lotus Notes): vira parágrafos
        diagramacao = colunas <= 1 or len(linhas) == 1 or any(
            len(texto(c)) > 300 or sum(1 for b in c if b[0] != "table") > 3 for ln in linhas for c in ln
        )
        if diagramacao:
            for ln in linhas:
                for c in ln:
                    for b in c:
                        self.emitir(b)
        else:
            self.emitir(("table", [[texto(c).replace("\n", " ").strip() for c in ln] for ln in linhas], False))


def render_runs(runs):
    # junta runs com mesma formatação e aplica ** / * com espaços por fora dos marcadores
    merged = []
    for text, b, i in runs:
        text = text.replace("﻿", "")
        text = re.sub(r"[ \t\r\f\v\xa0]+", " ", text.replace("\n", " \n "))
        if merged and merged[-1][1] == b and merged[-1][2] == i:
            merged[-1][0] += text
        else:
            merged.append([text, b, i])
    out = []
    for text, b, i in merged:
        core = text.strip(" ")
        if not re.search(r"\w", core):
            # só espaço/pontuação: formatação não acrescenta nada
            out.append(escape_inline(text))
            continue
        lead = " " if text.startswith(" ") else ""
        trail = " " if text.endswith(" ") else ""
        mark = ("**" if b else "") + ("*" if i else "")
        core = escape_inline(core)
        out.append(f"{lead}{mark}{core}{mark[::-1]}{trail}" if mark else f"{lead}{core}{trail}")
    s = "".join(out)
    s = re.sub(r" *\n *", "\n", s)
    s = re.sub(r" {2,}", " ", s).strip()
    s = re.sub(r"\*\*\s*\*\*", " ", s)  # negritos vazios / colados
    s = re.sub(r"###[A-Z0-9-]*@@@", "", s)
    s = s.replace("<<Anexo>>", "").replace("<<ANEXO>>", "").replace("<<ANEXOS>>", "")
    return s.strip()


def escape_inline(s):
    return s.replace("\\", "\\\\").replace("*", "\\*").replace("_", "\\_").replace("<", "&lt;")


def strip_md(s):
    return re.sub(r"[*\\]", "", s).strip()


def heading_level(plain):
    for rx, lvl in HEADINGS:
        if rx.match(plain):
            return lvl
    return None


def looks_like_name(plain):
    return (
        0 < len(plain) < 200
        and heading_level(plain) is None
        and not LABEL.match(plain)
        and not re.match(r"^[IVXLC]+ ?[-–—]", plain)
        and not re.match(r"^[a-z]\)", plain)
        and not plain.startswith("(")
        and not re.search(r"[.;:,]$", plain)
    )


def table_md(rows):
    width = max(len(r) for r in rows)
    rows = [[c.replace("|", "\\|").replace("\n", " ") for c in r] + [""] * (width - len(r)) for r in rows]
    lines = ["| " + " | ".join(rows[0]) + " |", "|" + " --- |" * width]
    lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    return "\n".join(lines)


def convert(html_text):
    p = Parser()
    p.feed(html_text)
    p.close()
    p.flush()
    blocks = p.blocks
    # parágrafos com vários dispositivos separados só por <br>: cada dispositivo vira um parágrafo
    inicio_dispositivo = re.compile(
        r"(?=^(?:\*\*)?(?:Art\.? ?\d|Artigo \d|§ ?\d|Parágrafo único|[IVXLC]+ ?[-–—]|[a-z]\) |"
        r"(?:TÍTULO|CAPÍTULO|SEÇÃO|SUBSEÇÃO|LIVRO) [IVXLC]))",
        re.M,
    )
    expandidos = []
    for b in blocks:
        if b[0] != "table" and "\n" in b[1]:
            partes = [p.strip() for p in inicio_dispositivo.split(b[1]) if p.strip()]
            expandidos += [(b[0], p, b[2]) for p in partes]
        else:
            expandidos.append(b)
    blocks = expandidos
    # cabeçalho institucional da compilação da Câmara
    while blocks and blocks[0][0] != "table" and strip_md(blocks[0][1]) in (
        "CÂMARA DOS DEPUTADOS",
        "Centro de Documentação e Informação",
    ):
        blocks = blocks[1:]

    out = []
    i = 0
    while i < len(blocks):
        kind, content, center = blocks[i]
        if kind == "table":
            out.append(table_md(content))
            i += 1
            continue
        plain = strip_md(content)
        lvl = heading_level(plain)
        if lvl and len(plain) < 250:
            # "CAPÍTULO I<br>DAS DISPOSIÇÕES" -> "CAPÍTULO I — DAS DISPOSIÇÕES"
            plain = re.sub(r"\s*\n\s*", " — ", plain)
            title = plain
            if re.fullmatch(r"\S+( \S+)? [IVXLC]+(-[A-Z])?|PARTE (GERAL|ESPECIAL)", plain, re.I) and i + 1 < len(blocks):
                nk, nc, _ = blocks[i + 1]
                if nk != "table" and looks_like_name(strip_md(nc)):
                    title = f"{plain} — {strip_md(nc)}"
                    i += 1
            out.append(f"{'#' * lvl} {title}")
        else:
            # "**Art.** 1.807." -> "**Art. 1.807.**"
            content = re.sub(
                r"^([“\"]?)\*\*(Art\.|§)\*\* ?(\d[\d.]*[º°o]?(?:-[A-Z]+)?\.?)(?=\s)", r"\1**\2 \3**", content
            )
            m = LABEL.match(plain)
            if m and not content.startswith("**"):
                # negrita o rótulo (Art. 1º, § 2º, Parágrafo único) quando ele vier sem formatação
                lab = m.group(1)
                if content.startswith(lab):
                    content = f"**{lab}**{content[len(lab):]}"
            if re.match(r"^\d+\. ", content):
                content = re.sub(r"^(\d+)\.", r"\1\\.", content)
            elif re.match(r"^[#>+\-] ", content):
                content = "\\" + content
            out.append(content.replace("\n", "  \n"))
        i += 1
    return "\n\n".join(out).strip() + "\n"


def convert_file(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return convert(f.read())


if __name__ == "__main__":
    import sys

    sys.stdout.write(convert_file(sys.argv[1]))
