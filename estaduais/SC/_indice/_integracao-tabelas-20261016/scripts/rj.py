"""Rio de Janeiro — wrapper público oficial da ALERJ, com cache e lotes por página.

Segue os links reais de paginação Lotus Notes. Cada página é coletada antes da próxima;
assim, uma interrupção não exige reconstruir o índice inteiro para salvar os textos.
"""
import base64
import datetime as dt
import fcntl
import gzip
import hashlib
import html as htmllib
import json
import os
import re
import sys
import threading
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from comum import RAIZ_ESTADUAIS, Rede, caminhos, decodificar, executar, gravar, html_para_md
from datas import data_do_texto

UF = "RJ"
BASE = "https://www3.alerj.rj.gov.br/lotus_notes/default.asp"
FORMS = {
    "LeiOrdInt": (53, "leis-ordinarias", "Lei Ordinária", "lei"),
    "LeiCompInt": (52, "leis-complementares", "Lei Complementar", "lc"),
    "EmendaInt": (51, "emendas-constitucionais", "Emenda Constitucional", "ec"),
}
CACHE = Path(RAIZ_ESTADUAIS) / UF / "_indice" / "paginas-wrapper"
rede = Rede(rps=3)
bloqueado = threading.Event()


def limpar(s):
    return " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def url_publica(form, route):
    codigo = FORMS[form][0]
    return f"{BASE}?id={codigo}&url=" + urllib.parse.quote(base64.b64encode(route.encode()).decode(), safe="")


def obter(form, route):
    cache = CACHE / form / (hashlib.sha256(route.encode()).hexdigest() + ".html.gz")
    if cache.exists():
        return gzip.decompress(cache.read_bytes())
    if bloqueado.is_set():
        raise RuntimeError("ALERJ bloqueou o acesso; retomar somente após verificar disponibilidade")
    st, raw, ct = rede.get(url_publica(form, route), tentativas=2, timeout=180)
    if st in (401, 403, 429):
        bloqueado.set()
    if st != 200 or not raw:
        raise RuntimeError(f"ALERJ HTTP {st}: {route}")
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(gzip.compress(raw))
    return raw


def corpo_normativo(pagina):
    # O HTML legado contém divs desbalanceadas; os marcadores Notes delimitam o texto.
    inicio = re.search(r'<a\s+name\s*=\s*["\']TOPO["\']', pagina, re.I)
    if not inicio:
        return ""
    trecho = pagina[inicio.start():]
    fim = re.search(r'<a\s+name=["\']_Section2["\']|<a[^>]+id="A2"', trecho, re.I)
    if fim:
        trecho = trecho[:fim.start()]
    def remover_interface(m):
        class Imagem(HTMLParser):
            def handle_starttag(self, tag, attrs):
                self.attrs = dict(attrs)
        parser = Imagem()
        parser.feed(m[0])
        attrs = parser.attrs
        # Ícones Notes comprovados no fragmento oficial; outras imagens permanecem.
        if attrs == {"width": attrs.get("width"), "height": "1",
                     "src": "http://alerjln1.alerj.rj.gov.br/icons/ecblank.gif",
                     "border": "0", "alt": ""} and attrs["width"] in {"1", "76", "113", "151"}:
            return ""
        if attrs == {"width": "16", "height": "16", "border": "0",
                     "src": "http://alerjln1.alerj.rj.gov.br/icons/collapse.gif",
                     "alt": "Hide details for Texto da Lei   [ Em Vigor ]"}:
            return ""
        return m[0]
    trecho = re.sub(r"<img\b[^>]*>", remover_interface, trecho, flags=re.I)
    return html_para_md(trecho)


def pagina_indice(form, route):
    raw = obter(form, route)
    pagina = decodificar(raw, "text/html; charset=utf-8")
    itens = {}
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", pagina, re.S | re.I):
        m = re.search(r'data-role="(/contlei\.nsf/[0-9a-f]+/[0-9a-f]+\?OpenDocument)"[^>]*>(.*?)</a>', tr, re.S | re.I)
        if not m:
            continue
        cols = [limpar(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S | re.I)]
        if len(cols) < 5 or not re.fullmatch(r"\d{4}", cols[1]):
            raise RuntimeError(f"linha de índice desconhecida: {form} {route}")
        href = htmllib.unescape(m[1])
        itens[href] = {"form": form, "href": href, "numero": limpar(m[2]),
                       "ano": cols[1], "situacao": cols[3], "ementa": cols[4]}
    links = [htmllib.unescape(x) for x in re.findall(r'data-role="([^"]+)"[^>]*shape=', pagina)]
    atuais = re.search(r"[?&]Start=(\d+)", route)
    inicio = int(atuais[1]) if atuais else 1
    proximos = [(int(m[1]), x) for x in links
                if (m := re.search(r"[?&]Start=(\d+)", x)) and int(m[1]) > inicio]
    proximo = min(proximos)[1] if proximos else None
    registro = {"rota": route, "itens": list(itens.values()), "proximo": proximo}
    destino = CACHE / form / (hashlib.sha256(route.encode()).hexdigest() + ".json")
    destino.write_text(json.dumps(registro, ensure_ascii=False))
    return registro


def processar(it):
    _, pasta, nome, prefixo = FORMS[it["form"]]
    numero = re.sub(r"\D", "", it["numero"])
    uid = it["href"].split("/")[-1].split("?")[0]
    md, fonte = caminhos(UF, pasta, it["ano"], f"{prefixo}-{numero}-{it['ano']}-{uid[:10]}")
    if os.path.exists(md):
        return "pulado", None
    if bloqueado.is_set():
        return "fonte_bloqueada", None
    raw = obter(it["form"], it["href"])
    pagina = decodificar(raw, "text/html; charset=utf-8")
    corpo = corpo_normativo(pagina)
    plano = re.sub(r"[*\\#]", "", limpar(corpo))
    num_rx = r"\b" + r"\.?".join(numero) + r"\b"
    if (len(re.sub(r"\W", "", corpo)) < 80
            or not re.search(num_rx, plano[:1000])
            or not re.search(r"\bArt(?:\.|igo)\s*\d", plano, re.I)):
        return "sem_texto", {"url": url_publica(it["form"], it["href"]), "motivo": "texto normativo não reconhecido"}
    m = re.search(r"Data da (?:Lei|Emenda(?: Constitucional)?)\s*(\d{2})/(\d{2})/(\d{4})", plano)
    data = ""
    raw_data = ""
    if m:
        raw_data = "/".join(m.groups())
        try:
            d = dt.date(int(m[3]), int(m[2]), int(m[1]))
            data = d.isoformat() if d <= dt.date.today() else ""
        except ValueError:
            pass
    else:
        data = data_do_texto(corpo, numero) or ""
    titulo = f"{nome} nº {it['numero']}/{it['ano']}"
    meta = [("titulo", titulo), ("uf", UF), ("tipo", nome), ("numero", it["numero"]),
            ("data", data), ("ementa", it["ementa"]), ("situacao", it["situacao"]),
            ("revogada", {"revogada": True, "revogado": True, "vigente": False, "em vigor": False}.get(it["situacao"].strip().lower())),
            ("versao_texto", "texto da base de legislação da ALERJ"),
            ("fonte", url_publica(it["form"], it["href"])),
            ("fonte_original", "http://alerjln1.alerj.rj.gov.br" + it["href"])]
    if raw_data and not data:
        meta.append(("data_na_fonte", raw_data))
    gravar(md, fonte, raw, meta, f"# {titulo}\n\n{corpo}")
    return "ok", None


def main():
    limite = int(sys.argv[1]) if len(sys.argv) > 1 else None
    for form in FORMS:
        route = f"/contlei.nsf/{form}?OpenForm"
        vistos, documentos = set(), set()
        while route and route not in vistos:
            vistos.add(route)
            pagina = pagina_indice(form, route)
            itens = [it for it in pagina["itens"] if it["href"] not in documentos]
            documentos.update(it["href"] for it in itens)
            if not pagina["itens"]:
                raise RuntimeError(f"índice sem normas: {form} {route}")
            if limite is not None:
                itens = itens[:limite]
                limite -= len(itens)
            print(f"[RJ] {form}: página {len(vistos)}, {len(documentos)} atos indexados", flush=True)
            executar(UF, itens, processar, workers=3)
            if bloqueado.is_set() or limite == 0:
                return
            route = pagina["proximo"]


if __name__ == "__main__":
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    trava = (CACHE.parent / "rj-coleta.lock").open("w")
    fcntl.flock(trava, fcntl.LOCK_EX | fcntl.LOCK_NB)
    main()
