"""Recupera RSFs de páginas dos Diários disponibilizadas pela interface pública oficial."""
import argparse
import datetime as dt
import gzip
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import urllib.parse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from baixar_federal import carregar_indice, montar, numero_oficial
from baixar_rsf_coletaneas import blocos, markdown
from comum import Rede, yaml_str

RAIZ = Path(__file__).resolve().parent.parent / "federal"
CACHE = RAIZ / "_fonte/senado-anais"
TRANSCRICOES = RAIZ / "_transcricoes_rsf_diarios.json"
AVISO = "> Transcrição visual conferida do PDF oficial: a extração automática não reconheceu corretamente campos manuscritos e assinatura. O original permanece disponível na fonte indicada.\n\n"


def obter(rede, url, cache, somente_cache=False):
    if cache.exists():
        return gzip.decompress(cache.read_bytes())
    if somente_cache:
        raise ValueError(f"cache ausente em auditoria offline: {cache}")
    status, bruto, _ = rede.get(url, timeout=60, tentativas=1)
    if status != 200:
        raise ValueError(f"HTTP {status}: {url}")
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(gzip.compress(bruto))
    return bruto


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("urn")
    ap.add_argument("diario", type=int)
    ap.add_argument("pagina", type=int)
    ap.add_argument("--pagina-final", type=int)
    ap.add_argument("--parcial", action="store_true")
    ap.add_argument("--auditar", action="store_true")
    args = ap.parse_args()
    final = args.pagina if args.pagina_final is None else args.pagina_final
    if args.diario < 1 or args.pagina < 1 or not args.pagina <= final < args.pagina + 20:
        ap.error("diário e página devem ser positivos")
    candidatos = [d for d in carregar_indice({"RSF"}) if montar(d)["urn"] == args.urn]
    if len(candidatos) != 1:
        ap.error("identidade não é única no índice primário")
    d = candidatos[0]
    info = montar(d)
    path = Path(info["md"])
    if path.exists() and not args.auditar:
        print("pulado", path)
        return
    rede = Rede(1)
    pagina_url = f"https://legis.senado.leg.br/diarios/ver/{args.diario}"
    pagina = obter(rede, pagina_url, CACHE / f"diario{args.diario}.html.gz", args.auditar).decode()
    links = [urllib.parse.urljoin(pagina_url, html.unescape(u))
             for u in re.findall(r'href=["\']([^"\']+)["\']', pagina)]
    links = [u for u in links if urllib.parse.urlparse(u).hostname == "legis.senado.leg.br"
             and urllib.parse.urlparse(u).path == "/diarios/BuscaPaginasDiario"
             and urllib.parse.parse_qs(urllib.parse.urlparse(u).query) == {"codDiario": [str(args.diario)], "download": ["true"]}]
    if len(set(links)) != 1:
        raise ValueError("link público próprio do PDF não identificado")
    url = links[0]
    intervalo = str(args.pagina) if final == args.pagina else f"{args.pagina}-{final}"
    cache_pdf = CACHE / f"diario{args.diario}.pdf.gz"
    primeira_pdf, ultima_pdf = args.pagina, final
    if args.parcial:
        form = re.search(r'<form[^>]*id="frmDownloadPaginas"[\s\S]*?</form>', pagina)
        if not form or not re.search(r'name="codDiario"\s+value="' + str(args.diario) + r'"', form[0]):
            raise ValueError("formulário público de intervalo não comprovado para este diário")
        if any(f'name="{nome}"' not in form[0] for nome in ("paginaInicial", "paginaFinal")):
            raise ValueError("parâmetros de páginas não declarados pelo formulário")
        action = re.search(r'action="([^"]+)"', form[0])
        if not action or urllib.parse.urljoin(pagina_url, action[1]) != "https://legis.senado.leg.br/diarios/BuscaPaginasDiario":
            raise ValueError("destino do formulário não é o serviço público esperado")
        url = urllib.parse.urljoin(pagina_url, action[1]) + "?" + urllib.parse.urlencode({"codDiario": args.diario, "paginaInicial": args.pagina, "paginaFinal": final})
        cache_pdf = CACHE / f"diario{args.diario}-pp{intervalo}.pdf.gz"
        primeira_pdf, ultima_pdf = 1, final - args.pagina + 1
    bruto = obter(rede, url, cache_pdf, args.auditar)
    if not bruto.startswith(b"%PDF"):
        raise ValueError("resposta não é PDF; fonte preservada, sem contornar bloqueios")
    sha_pdf = hashlib.sha256(bruto).hexdigest()
    with tempfile.TemporaryDirectory() as tmp:
        pdf = Path(tmp) / "diario.pdf"
        pdf.write_bytes(bruto)
        texto = subprocess.check_output(["rtk", "proxy", "pdftotext", "-f", str(primeira_pdf), "-l", str(ultima_pdf), "-raw", str(pdf), "-"], timeout=60).decode()
    raw_sha = hashlib.sha256(texto.encode()).hexdigest()
    raw_cache = CACHE / f"diario{args.diario}-{'pp' if args.parcial else 'page'}{intervalo}-{raw_sha}.raw.txt.gz"
    if not args.auditar and not raw_cache.exists():
        raw_cache.write_bytes(gzip.compress(texto.encode()))
    transcricoes = json.loads(TRANSCRICOES.read_text()) if TRANSCRICOES.exists() else {}
    manual = transcricoes.get(f"{args.diario}:{args.pagina}")
    if manual:
        if final != manual.get("pagina_final", args.pagina) or manual["urn"] != args.urn or manual["sha256_pdf"] != sha_pdf or manual["sha256_extracao_original"] != raw_sha:
            raise ValueError("transcrição visual não corresponde à fonte exata")
        texto = manual["texto_verificado"]
    texto = re.sub(r"R[ \t]+E[ \t]+S[ \t]+O[ \t]+L[ \t]+U[ \t]+Ç[ \t]+Ã[ \t]+O", "RESOLUÇÃO", texto)
    texto = re.sub(r"RESOLUÇÃO\s+N[ºo.°]*\s*(\d+)\s*,?\s*DE\s*(\d{4})", r"RESOLUÇÃO Nº \1 – DE \2", texto)
    opcoes = blocos(texto).get((numero_oficial(d).lower(), int(info["data"][:4])), [])
    validos = [b for b in opcoes if b["datas"] == [info["data"]]]
    if len(validos) != 1:
        raise ValueError("epígrafe e fecho próprios não comprovam norma única")
    original = validos[0]["corpo"]
    fim = re.search(r"Senado Federal,?\s*(?:em\s*)?\d{1,2}\s+de\s+\w+\s+de\s+\d{4}\.[\s\S]{0,300}?Presidente do Senado Federal\.?", original)
    if not fim:
        raise ValueError("fim próprio da resolução não identificado")
    normativo = markdown(original[:fim.end()]).strip()
    corpo = (AVISO if manual else "") + normativo
    if args.auditar:
        existente = path.read_text().split("---\n", 2)[2].strip().split("\n\n", 1)[1]
        if existente != corpo:
            raise ValueError("corpo armazenado diverge da fonte conferida")
        print("auditado", path, hashlib.sha256(corpo.encode()).hexdigest())
        return
    meta = {"titulo": d["normaNome"], "tipo": info["nome"], "numero": numero_oficial(d), "data": info["data"],
            "ementa": d.get("ementa", ""), "urn": info["urn"], "revogada": None,
            "versao_texto": "publicação original no Diário do Senado Federal",
            "metodo_extracao": "transcrição visual conferida" if manual else "texto digital do PDF oficial",
            "paginas_fonte": intervalo,
            "fonte": url + f"#page={primeira_pdf}", "url_metadados": pagina_url, "id_senado": d["id"],
            "sha256_pdf_fonte": sha_pdf, "sha256_extracao_original": raw_sha,
            "sha256_texto": hashlib.sha256(corpo.encode()).hexdigest(),
            "sha256_texto_normativo": hashlib.sha256(normativo.encode()).hexdigest(), "baixado_em": dt.date.today().isoformat()}
    cab = "---\n" + "".join(k + ": " + ("null" if v is None else yaml_str(str(v))) + "\n" for k, v in meta.items()) + "---\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(cab + "# " + d["normaNome"] + "\n\n" + corpo + "\n")
    with (RAIZ / "_recuperacoes_rsf_diarios.jsonl").open("a") as f:
        f.write(json.dumps({"path": str(path.relative_to(RAIZ.parent)), **meta}, ensure_ascii=False) + "\n")
    print("ok", path, len(corpo))


if __name__ == "__main__":
    main()
