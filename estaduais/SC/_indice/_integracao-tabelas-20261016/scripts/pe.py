"""Pernambuco — Alepe Legis (legis.alepe.pe.gov.br).

Índice: lista.aspx?tiponorma=N, um ano por vez (postback ASP.NET do seletor ddlAno).
Texto: texto.aspx?id=N&tipo=TEXTOATUALIZADO (quando existe) ou TEXTOORIGINAL; conteúdo em div#divTexto.
"""
import html as htmllib
import http.cookiejar
import datetime as dt
import gzip
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.parse
import urllib.request
from html.parser import HTMLParser

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, UA, Rede, caminhos, decodificar, executar, gravar, html_para_md  # noqa: E402
from datas import data_do_texto

UF = "PE"
BASE = "https://legis.alepe.pe.gov.br"
# tiponorma do Alepe Legis -> (pasta, tipo canônico, prefixo). O tipo 6 é "Decreto do Executivo",
# com acervo de 1996 a hoje, e ficava inteiro de fora. Os quatro primeiros prefixos já estão
# gravados e não mudam.
TIPOS = {
    "13": ("emendas-constitucionais", "Emenda Constitucional", "ec"),
    "2": ("leis-complementares", "Lei Complementar", "lc"),
    "1": ("leis-ordinarias", "Lei Ordinária", "lei"),
    "11": ("decretos-lei", "Decreto-Lei", "dl"),
    "6": ("decretos", "Decreto", "dec"),
}
rede = Rede(rps=2)
LINHA = re.compile(
    r"nome-norma\"><a href='texto\.aspx\?id=(\d+)[^>]*>([^<]+)</a></span>\s*<span class=\"publicacao\">([^<]*)</span>(.*?)</tr>",
    re.S,
)


def listar_ano(op, tipo, ano, campos):
    dados = dict(campos, __EVENTTARGET="ctl00$conteudo$ddlAno", __EVENTARGUMENT="")
    dados["ctl00$conteudo$ddlAno"] = ano
    url = f"{BASE}/lista.aspx?tiponorma={tipo}"
    rede.limite.esperar()
    req = urllib.request.Request(
        url, data=urllib.parse.urlencode(dados).encode(), headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded"}
    )
    return op.open(req, timeout=180).read().decode("utf-8", "replace")


def campos_ocultos(html):
    return {n: htmllib.unescape(v) for n, v in re.findall(r'<input type="hidden" name="([^"]+)" id="[^"]*" value="([^"]*)"', html)}


def linhas(html, tipo):
    for id_, nome, pub, resto in LINHA.findall(html):
        textos = re.findall(r"tipo=(TEXTO[A-Z]+)", resto)
        ementa = re.search(r'class="ementa-norma[^"]*">\s*<div class="fLeft">(.*?)</div>', resto, re.S)
        yield {
            "id": id_,
            "tipo": tipo,
            "nome": " ".join(htmllib.unescape(nome).split()),
            "publicacao": " ".join(htmllib.unescape(pub).split()),
            "textos": sorted(set(textos)),
            "ementa": " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", ementa.group(1))).split()) if ementa else "",
        }


def indice(refazer=False):
    pasta = os.path.join(RAIZ_ESTADUAIS, UF, "_indice")
    arq = os.path.join(pasta, "lista.json")
    if os.path.exists(arq) and not refazer:
        return json.load(open(arq, encoding="utf-8"))
    itens = {}
    for tipo in TIPOS:
        op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        rede.limite.esperar()
        pagina = op.open(urllib.request.Request(f"{BASE}/lista.aspx?tiponorma={tipo}", headers={"User-Agent": UA}), timeout=180)
        html = pagina.read().decode("utf-8", "replace")
        anos = re.findall(r'<option[^>]*value="(\d{4})"', html.split('id="ddlAno"', 1)[1].split("</select>", 1)[0]) if 'id="ddlAno"' in html else []
        if not anos:
            for it in linhas(html, tipo):
                itens[it["id"]] = it
        for ano in anos:
            h = listar_ano(op, tipo, ano, campos_ocultos(html))
            for it in linhas(h, tipo):
                it["ano"] = ano
                itens[it["id"]] = it
        print(f"[{UF}] índice tipo {tipo}: {sum(1 for i in itens.values() if i['tipo'] == tipo)}", flush=True)
    lista = list(itens.values())
    os.makedirs(pasta, exist_ok=True)
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False)
    return lista


class _LimiteTexto(HTMLParser):
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
        if tag != "div" or self.fim is not None:
            return
        if self.inicio is None:
            if dict(attrs).get("id") == "divTexto":
                self.inicio = self.posicao() + len(self.get_starttag_text())
                self.profundidade = 1
        else:
            self.profundidade += 1

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag == "div" and self.inicio is not None and self.fim is None:
            self.profundidade -= 1
            if self.profundidade == 0:
                self.fim = self.posicao()


def limites_texto_html(html, fragmento=False):
    limite = _LimiteTexto(html, fragmento)
    limite.feed(html)
    if limite.inicio is None:
        return None
    if limite.fim is None:
        raise ValueError("divTexto sem fechamento comprovado; extração recusada")
    return limite.inicio, limite.fim


def texto_html(html):
    limites = limites_texto_html(html)
    return html[limites[0]:limites[1]] if limites else ""


def processar(it):
    pasta, nome, prefixo = TIPOS[it["tipo"]]
    num = re.search(r"n[°º]\s*([\d.]+)", it["nome"])
    numero = num.group(1).replace(".", "") if num else "sn"
    ano = it.get("ano") or "sem-ano"
    slug = f"{prefixo}-{numero}-{ano}-id{it['id']}"
    md, fonte = caminhos(UF, pasta, ano, slug)
    if os.path.exists(md):
        return "pulado", None
    tipo_txt = "TEXTOATUALIZADO" if "TEXTOATUALIZADO" in it["textos"] else "TEXTOORIGINAL"
    url = f"{BASE}/texto.aspx?id={it['id']}&tipo={tipo_txt}"
    st, bruto, ctype = rede.get(url, timeout=180)
    if st != 200:
        return "sem_texto", {"id": it["id"], "http": st}
    captura = os.path.join(RAIZ_ESTADUAIS, UF, "_fonte", "respostas", str(it["id"]), tipo_txt, hashlib.sha256(bruto).hexdigest() + ".html.gz")
    os.makedirs(os.path.dirname(captura), exist_ok=True)
    try:
        with gzip.open(captura, "rb") as f:
            integra = hashlib.sha256(f.read()).digest() == hashlib.sha256(bruto).digest()
    except (OSError, EOFError):
        integra = False
    if not integra:
        with tempfile.NamedTemporaryFile(dir=os.path.dirname(captura), delete=False) as f:
            temporario = f.name
            f.write(gzip.compress(bruto))
        os.replace(temporario, captura)
    html = decodificar(bruto, ctype)
    trecho = texto_html(html)
    if not trecho:
        return "sem_texto", {"id": it["id"], "motivo": "sem divTexto"}
    corpo = html_para_md(trecho)
    if len(re.sub(r"\W", "", corpo)) < 40:
        return "sem_texto", {"id": it["id"], "motivo": "texto vazio"}
    data = re.search(r"(\d{2})/(\d{2})/(\d{4})", it["publicacao"])
    data_publicacao = ""
    if data:
        try:
            publicada = dt.date(int(data[3]), int(data[2]), int(data[1]))
            if publicada <= dt.date.today():
                data_publicacao = publicada.isoformat()
        except ValueError:
            pass
    titulo = it["nome"]
    data_norma = data_do_texto(corpo, numero=numero) or ""
    if data_norma:
        try:
            if dt.date.fromisoformat(data_norma) > dt.date.today():
                data_norma = ""
        except ValueError:
            data_norma = ""
    meta = [
        ("titulo", titulo),
        ("uf", UF),
        ("tipo", nome),
        ("numero", num.group(1) if num else ""),
        ("data", data_norma),
        ("ano", ano),
        ("ementa", it["ementa"]),
        ("publicacao", it["publicacao"]),
        ("data_publicacao", data_publicacao),
        ("revogada", None),
        ("versao_texto", "atualizada" if tipo_txt == "TEXTOATUALIZADO" else "original"),
        ("fonte", url),
    ]
    if data and not data_publicacao:
        meta.append(("data_publicacao_na_fonte", "/".join(data.groups())))
    gravar(md, fonte, bruto, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


if __name__ == "__main__":
    itens = indice(refazer="--refazer" in sys.argv)
    itens.sort(key=lambda i: (i.get("ano") or "", int(i["id"])), reverse=True)
    print(f"[{UF}] {len(itens)} normas no índice", flush=True)
    limite = [a for a in sys.argv[1:] if a.isdigit()]
    if limite:
        itens = itens[: int(limite[0])]
    executar(UF, itens, processar, workers=2)
