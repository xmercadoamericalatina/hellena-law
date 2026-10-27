"""Recupera RSFs faltantes das coletâneas públicas dos Anais do Senado."""
import argparse
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unicodedata
import urllib.parse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from baixar_federal import carregar_indice, montar, numero_oficial
from comum import Rede, texto_pdf_para_md, yaml_str

RAIZ = Path(__file__).resolve().parent.parent / "federal"
CATALOGO = "https://www.senado.leg.br/publicacoes/anais/asp/RE_Resolucoes.asp"
CACHE = RAIZ / "_fonte/senado-coletaneas"
MESES = {m: i for i, m in enumerate(("janeiro", "fevereiro", "marco", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"), 1)}


def obter(rede, url, path):
    if path.exists():
        return gzip.decompress(path.read_bytes())
    status, bruto, _ = rede.get(url, timeout=60, tentativas=1)
    if status != 200 or not bruto:
        raise ValueError(f"HTTP {status}: {url}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(bruto))
    return bruto


def extrair_pdf(rede, url):
    nome = urllib.parse.urlparse(url).path.rsplit("/", 1)[-1]
    bruto = obter(rede, url, CACHE / (nome + ".gz"))
    if not bruto.startswith(b"%PDF"):
        raise ValueError("fonte não é PDF: " + url)
    path = CACHE / (nome + ".txt.gz")
    if path.exists():
        return gzip.decompress(path.read_bytes()).decode(), hashlib.sha256(bruto).hexdigest()
    with tempfile.TemporaryDirectory() as pasta:
        pdf = Path(pasta) / "tomo.pdf"
        pdf.write_bytes(bruto)
        proc = subprocess.run(["rtk", "proxy", "pdftotext", "-q", "-layout", "-enc", "UTF-8", str(pdf), "-"], capture_output=True, timeout=120, check=True)
    texto = proc.stdout.decode("utf-8")
    path.write_bytes(gzip.compress(texto.encode()))
    return texto, hashlib.sha256(bruto).hexdigest()


def blocos(texto):
    rx = re.compile(r"(?m)^[ \t\f]*RESOLUÇÃO[ \t]+N[.ºo°]*[ \t]*([\d.]+(?:[-–][A-Z])?)[ \t]*[–,-]?[ \t]*DE[ \t]+([^\n]{0,80})")
    titulos = []
    for match in rx.finditer(texto):
        anos = re.findall(r"\b(?:19|20)\d{2}\b", match[2])
        if len(anos) == 1:
            pos = match.start() + len(match[0]) - len(match[0].lstrip())
            titulos.append((match, pos, match[1].replace(".", "").replace("–", "-").lower(), int(anos[0])))
    inicios = []
    for idx, (match, pos, _, _) in enumerate(titulos):
        limite = max(titulos[idx - 1][0].end() if idx else 0, pos - 1800)
        prefixo = texto[limite:pos]
        formulas = list(re.finditer(r"(?m)^[ \t\f]*(?:Faço saber|O Senado Federal (?:aprova|resolve)|O Presidente do Senado Federal)", prefixo, re.I))
        if formulas:
            formula = formulas[-1]
            trecho = prefixo[formula.start():]
            if not re.search(r"(?m)^\s*Art(?:igo)?\b|Publicad[ao]\s+no|(?:Senado Federal|Sala das Sessões),?\s*(?:em\s*)?\d", trecho, re.I):
                pos = limite + formula.start()
        inicios.append(pos)
    encontrados = {}
    for idx, (_, cabeca, numero, ano) in enumerate(titulos):
        fim = inicios[idx + 1] if idx + 1 < len(inicios) else len(texto)
        corpo = texto[inicios[idx]:fim].strip()
        if len(corpo) < 120 or "\x00" in corpo or not re.search(r"(?m)^\s*Art(?:igo)?\.?\s*(?:\d|[úu]nico)", corpo, re.I):
            continue
        normal = unicodedata.normalize("NFKD", corpo).encode("ascii", "ignore").decode().lower()
        datas = set()
        for dia, mes, ano_data in re.findall(r"(?:senado federal|sala das sessoes|brasilia|rio de janeiro),?\s*(?:em\s*)?(\d{1,2})(?:o)?\s+de\s+([a-z]+)\s+(?:de|da)\s*(\d{4})", normal):
            if mes in MESES:
                try:
                    datas.add(dt.date(int(ano_data), MESES[mes], int(dia)).isoformat())
                except ValueError:
                    datas.add("data inválida na fonte")
        encontrados.setdefault((numero, ano), []).append({"corpo": corpo, "datas": sorted(datas),
                    "pagina_inicio": texto[:cabeca].count("\f") + 1,
                    "pagina_fim": texto[:fim].count("\f") + 1})
    return encontrados


def markdown(texto):
    # Impede que o conversor elimine valores numéricos isolados de tabelas.
    texto = re.sub(r"(?m)^[ \t]*(\d{1,5})[ \t]*$", lambda m: "VALORORIGINAL" + m[1] + "PRESERVADO", texto.replace("\f", "\n\n"))
    corpo = texto_pdf_para_md(texto)
    return re.sub(r"VALORORIGINAL(\d+)PRESERVADO", r"\1", corpo)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rps", type=float, default=1)
    ap.add_argument("--limite-tomos", type=int, default=0)
    ap.add_argument("--somente-auditar", action="store_true")
    ap.add_argument("--revalidar", action="store_true", help="confere também MDs já extraídos desta coletânea")
    a = ap.parse_args()
    if not 0 < a.rps <= 4 or a.limite_tomos < 0:
        ap.error("rps ou limite inválido")
    rede = Rede(a.rps)
    html = obter(rede, CATALOGO, CACHE / "catalogo.html.gz").decode("latin1")
    alvos = []
    for d in carregar_indice({"RSF"}):
        info = montar(d)
        path = Path(info["md"])
        proprio = path.exists() and 'fonte_catalogo: "' + CATALOGO + '"' in path.read_text().split("---", 2)[1]
        if not path.exists() or (a.revalidar and proprio):
            alvos.append((d, info))
    anos = {int(i["data"][:4]) for _, i in alvos}
    tomos = []
    for href in re.findall(r'href=["\']([^"\']+)["\']', html, re.I):
        if "/Resolucoes/" not in href:
            continue
        url = urllib.parse.urljoin(CATALOGO, href)
        if urllib.parse.urlparse(url).hostname != "www.senado.leg.br":
            raise ValueError("host fora do catálogo oficial")
        limites = list(map(int, re.findall(r"\d{4}", url.rsplit("/", 1)[-1])))
        if limites and any(limites[0] <= ano <= limites[-1] for ano in anos):
            tomos.append((url, limites[0], limites[-1]))
    fora_catalogo = [i["urn"] for _, i in alvos if not any(inicio <= int(i["data"][:4]) <= fim for _, inicio, fim in tomos)]
    if a.limite_tomos:
        tomos = tomos[:a.limite_tomos]
    cont = {"ok": 0, "pendente": 0, "sem_tomo": len(fora_catalogo), "falhas_tomo": 0}
    registros = []
    for url, inicio, fim in tomos:
        try:
            texto, hash_pdf = extrair_pdf(rede, url)
            candidatos = blocos(texto)
        except Exception as exc:
            cont["falhas_tomo"] += 1
            erro = {"origem": "senado-coletaneas", "fonte": url, "erro": str(exc)}
            with (RAIZ / "_falhas_rsf_coletaneas.jsonl").open("a") as f:
                f.write(json.dumps(erro, ensure_ascii=False) + "\n")
            print(erro, flush=True)
            if any(c in str(exc) for c in ("HTTP 401", "HTTP 403", "HTTP 429")):
                break
            continue
        for d, info in alvos:
            if not inicio <= int(info["data"][:4]) <= fim:
                continue
            opcoes = candidatos.get((numero_oficial(d).lower(), int(info["data"][:4])), [])
            validos = [b for b in opcoes if b["datas"] == [info["data"]]]
            unicos = {hashlib.sha256(b["corpo"].encode()).hexdigest(): b for b in validos}
            registro = {"origem": "senado-coletaneas", "urn": info["urn"], "fonte": url, "candidatos": len(opcoes), "datas_encontradas": [b["datas"] for b in opcoes]}
            if len(unicos) != 1:
                cont["pendente"] += 1
                registro.update(resultado="pendente", motivo="texto completo com número/ano/data não identificado de forma única")
                path = Path(info["md"])
                if a.revalidar and not a.somente_auditar and path.exists():
                    antigo = path.read_bytes()
                    snapshot = CACHE / "revisoes" / (path.stem + "-" + hashlib.sha256(antigo).hexdigest()[:12] + ".md.gz")
                    snapshot.parent.mkdir(parents=True, exist_ok=True)
                    snapshot.write_bytes(gzip.compress(antigo))
                    path.unlink()
                    registro.update(versao_anterior=str(snapshot), retirado_por_revalidacao=True)
            else:
                bloco = next(iter(unicos.values()))
                corpo = markdown(bloco["corpo"])
                meta = {"titulo": d["normaNome"], "tipo": info["nome"], "numero": numero_oficial(d), "data": info["data"],
                        "ementa": d.get("ementa", ""), "urn": info["urn"], "revogada": None,
                        "versao_texto": "reprodução na coletânea histórica oficial do Senado",
                        "fonte": url + "#page=" + str(bloco["pagina_inicio"]), "fonte_catalogo": CATALOGO,
                        "paginas_fonte": str(bloco["pagina_inicio"]) + "-" + str(bloco["pagina_fim"]),
                        "id_senado": d["id"], "sha256_pdf_fonte": hash_pdf, "sha256_texto": hashlib.sha256(corpo.encode()).hexdigest(),
                        "baixado_em": dt.date.today().isoformat()}
                publicacoes = re.findall(r"Publicad[ao][^\n]*\bde\s+([^\n]+)", bloco["corpo"], re.I)
                if any((match := re.search(r"\d{1,2}(?:º|o)?[./-]\d{1,2}[./-](\d{2,4})", p)) and match[1][-2:] != info["data"][2:4] for p in publicacoes):
                    meta["observacao_fonte"] = "Anotação de publicação da coletânea diverge do ano do fecho; conteúdo original mantido."
                if not a.somente_auditar:
                    path = Path(info["md"])
                    path.parent.mkdir(parents=True, exist_ok=True)
                    cab = "---\n" + "".join(k + ": " + ("null" if v is None else yaml_str(str(v))) + "\n" for k, v in meta.items()) + "---\n"
                    novo = cab + "# " + d["normaNome"] + "\n\n" + corpo
                    if path.exists() and path.read_text() != novo:
                        antigo = path.read_bytes()
                        snapshot = CACHE / "revisoes" / (path.stem + "-" + hashlib.sha256(antigo).hexdigest()[:12] + ".md.gz")
                        snapshot.parent.mkdir(parents=True, exist_ok=True)
                        snapshot.write_bytes(gzip.compress(antigo))
                        registro["versao_anterior"] = str(snapshot)
                    tmp = path.with_suffix(".tmp")
                    tmp.write_text(novo)
                    tmp.replace(path)
                cont["ok"] += 1
                registro.update(resultado="validado" if a.somente_auditar else "ok", arquivo=info["md"], pagina=bloco["pagina_inicio"])
            registros.append(registro)
            if not a.somente_auditar:
                with (RAIZ / "_recuperacoes_rsf_coletaneas.jsonl").open("a") as f:
                    f.write(json.dumps(registro, ensure_ascii=False) + "\n")
                if registro["resultado"] == "pendente":
                    with (RAIZ / "_falhas_rsf_coletaneas.jsonl").open("a") as f:
                        f.write(json.dumps(registro, ensure_ascii=False) + "\n")
            print(registro, flush=True)
        pasta = RAIZ / "_indice/senado-coletaneas"
        pasta.mkdir(parents=True, exist_ok=True)
        (pasta / "recuperacao.json").write_text(json.dumps({"contagem": cont, "alvos_iniciais": len(alvos), "tomos_consultados": len(tomos), "sem_tomo": fora_catalogo, "registros": registros}, ensure_ascii=False, indent=2))
    print("FIM", cont, flush=True)
    return int(bool(cont["pendente"] or cont["sem_tomo"] or cont["falhas_tomo"]))


if __name__ == "__main__":
    sys.exit(main())
