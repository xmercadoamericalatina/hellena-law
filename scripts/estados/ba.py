"""Bahia — Portal de Legislação do Estado da Bahia (Casa Civil, legislabahia.ba.gov.br).

Índice: listagem /documentos?categoria[]=N&page=P (Drupal, 20 por página).
Texto: campo body da página de cada documento.
"""
import gzip
import hashlib
import html as htmllib
import json
import os
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, decodificar, executar, gravar, html_para_md  # noqa: E402

UF = "BA"
BASE = "https://www.legislabahia.ba.gov.br"
CATEGORIAS = {
    "11": ("constituicao", "Constituição Estadual (1989)"),
    "33": ("constituicoes-historicas", "Constituição Estadual (1967)"),
    "32": ("constituicoes-historicas", "Constituição Estadual (1947)"),
    "31": ("constituicoes-historicas", "Constituição Estadual (1935)"),
    "30": ("constituicoes-historicas", "Constituição Estadual (1891)"),
    "4": ("emendas-constitucionais", "Emenda Constitucional"),
    "5": ("leis-complementares", "Lei Complementar"),
    "7": ("leis-ordinarias", "Lei Ordinária"),
    "6": ("leis-delegadas", "Lei Delegada"),
    # o filtro do portal oferece também o infralegal da Casa Civil, que ficava inteiro de fora
    "2": ("decretos", "Decreto"),
    "1": ("decretos", "Decreto"),
    "3": ("decretos", "Decreto"),
    "19": ("portarias", "Portaria"),
    "20": ("portarias", "Portaria"),
    "26": ("portarias", "Portaria"),
    "92": ("instrucoes-normativas", "Instrução Normativa"),
}
rede = Rede(rps=3)


def indice(refazer=False):
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice")
    arq = os.path.join(pasta, "documentos.json")
    if os.path.exists(arq) and not refazer:
        return json.load(open(arq, encoding="utf-8"))
    itens, vistos = [], set()

    def pagina(cat, pag):
        for _ in range(5):
            st, dados, _ = rede.get(f"{BASE}/documentos?categoria%5B%5D={cat}&page={pag}")
            if st == 200 and dados:
                return decodificar(dados)
        raise RuntimeError(f"página {pag} da categoria {cat} indisponível")

    for cat in CATEGORIAS:
        html = pagina(cat, 0)
        # o paginador do Drupal traz o link da última página
        ultima = max([int(p) for p in re.findall(r"page=(\d+)", html)] or [0])
        for pag in range(ultima + 1):
            if pag:
                html = pagina(cat, pag)
            for ln in dict.fromkeys(re.findall(r'href="(/documentos/[^"?#]+)"', html)):
                if ln not in vistos:
                    vistos.add(ln)
                    itens.append({"path": ln, "categoria": cat})
        print(f"[{UF}] índice categoria {cat}: {len(itens)} acumulado ({ultima + 1} páginas)", flush=True)
    os.makedirs(pasta, exist_ok=True)
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(itens, f, ensure_ascii=False)
    return itens


def campo(html, nome):
    m = re.search(rf'field--name-{nome}\b.*?field--item">(.*?)</div>', html, re.S)
    return htmllib.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).strip() if m else ""


class _LimiteCorpo(HTMLParser):
    def __init__(self, html, fragmento):
        super().__init__(convert_charrefs=False)
        self.inicio = 0 if fragmento else None
        self.fim = None
        self.profundidade = 1 if fragmento else 0
        self.linhas = [0] + [m.end() for m in re.finditer("\n", html)]

    def posicao(self):
        linha, coluna = self.getpos()
        return self.linhas[linha - 1] + coluna

    def handle_starttag(self, tag, attrs):
        if self.fim is not None or tag != "div":
            return
        if self.inicio is None:
            classes = dict(attrs).get("class", "").split()
            if "field--name-body" in classes:
                self.inicio = self.posicao() + len(self.get_starttag_text())
                self.profundidade = 1
        else:
            self.profundidade += 1

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if self.inicio is None or self.fim is not None or tag != "div":
            return
        self.profundidade -= 1
        if self.profundidade == 0:
            self.fim = self.posicao()


def limites_corpo_html(html, fragmento=False):
    """Fragmentos antigos perderam só a abertura do div do campo Drupal."""
    limite = _LimiteCorpo(html, fragmento)
    limite.feed(html)
    if limite.inicio is None:
        return None
    if limite.fim is None:
        raise ValueError("campo body sem fechamento comprovado; extração recusada")
    return limite.inicio, limite.fim


def corpo_html(html):
    limites = limites_corpo_html(html)
    return html[limites[0]:limites[1]] if limites else ""



def conferir_numero_epigrafe(texto, numero):
    """Conserva o sufixo literal da epígrafe quando o campo Drupal o omite."""
    epigrafe = htmllib.unescape(re.sub(r"<[^>]+>", " ", texto))
    m = re.search(
        r"\b(?:DECRETO(?:\s+FINANCEIRO)?|LEI(?:\s+COMPLEMENTAR)?|PORTARIA|"
        r"RESOLU[ÇC][ÃA]O|INSTRU[ÇC][ÃA]O\s+NORMATIVA)\s+N[.º°o\s]*"
        r"([0-9][0-9.]*)\s*(?:[-–]\s*([A-Za-z])\b)?", epigrafe[:1200], re.I)
    if not m:
        return numero
    literal = m.group(1) + ("-" + m.group(2).upper() if m.group(2) else "")
    def chave(valor):
        return re.sub(r"[^0-9a-z]", "", str(valor).casefold()).lstrip("0")
    if chave(numero) == chave(literal):
        return numero
    if m.group(2) and chave(numero) == chave(m.group(1)):
        return literal.replace(".", "")
    raise ValueError(f"número do campo Drupal {numero!r} diverge da epígrafe literal {literal!r}")

def processar(it):
    pasta, nome = CATEGORIAS[it["categoria"]]
    slug = it["path"].rsplit("/", 1)[-1][:120]
    m_ano = re.search(r"(1[89]\d\d|20\d\d)(?!.*(1[89]\d\d|20\d\d))", slug)
    ano = m_ano.group(1) if m_ano else "sem-ano"
    md, fonte = caminhos(UF, pasta, ano, slug)
    if os.path.exists(md):
        return "pulado", None
    url = BASE + it["path"]
    st, bruto, ctype = rede.get(url)
    if st != 200:
        return "sem_texto", {"url": url, "http": st}
    html = decodificar(bruto, ctype)
    corpo = corpo_html(html)
    texto = html_para_md(corpo) if corpo else ""
    if len(re.sub(r"\W", "", texto)) < 40:
        return "sem_texto", {"url": url, "motivo": "corpo vazio"}
    dm = re.search(r'field--name-field-data-doc.*?datetime="(\d{4})-(\d{2})-(\d{2})', html, re.S)
    data = f"{dm.group(1)}-{dm.group(2)}-{dm.group(3)}" if dm else ""
    try:
        numero = conferir_numero_epigrafe(texto, campo(html, "field-numero-doc"))
    except ValueError as exc:
        sha = hashlib.sha256(bruto).hexdigest()
        evidencia = fonte if not os.path.exists(fonte) else os.path.join(
            RAIZ_ESTADUAIS, UF, "_fonte", "auditorias", "numero-divergente", f"{slug}-{sha}.gz")
        os.makedirs(os.path.dirname(evidencia), exist_ok=True)
        if not os.path.exists(evidencia):
            with gzip.open(evidencia, "wb") as arq:
                arq.write(bruto)
        return "sem_texto", {"url": url, "motivo": str(exc), "cache": evidencia, "sha256_fonte": sha}
    if nome.startswith("Constituição"):
        titulo = f"Constituição do Estado da Bahia {nome[nome.find('('):]}"
    else:
        titulo = f"{nome} nº {numero or 's/n'}" + (f", de {dm.group(3)}/{dm.group(2)}/{dm.group(1)}" if dm else "")
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", numero),
        ("data", data),
        ("ementa", " ".join(campo(html, "field-ementa").split())),
        ("publicacao", ("DOE " + campo(html, "field-data-de-publicacao-no-doe")).strip() if campo(html, "field-data-de-publicacao-no-doe") else ""),
        ("revogada", None),
        ("versao_texto", "texto do Portal de Legislação da Bahia"),
        ("fonte", url),
    ]
    gravar(md, fonte, bruto, meta, f"# {titulo}\n\n{texto}")
    return "ok", None


if __name__ == "__main__":
    itens = indice(refazer="--refazer" in sys.argv)
    print(f"[{UF}] {len(itens)} normas no índice", flush=True)
    limite = [a for a in sys.argv[1:] if a.isdigit()]
    if limite:
        itens = itens[: int(limite[0])]
    executar(UF, itens, processar, workers=3)
