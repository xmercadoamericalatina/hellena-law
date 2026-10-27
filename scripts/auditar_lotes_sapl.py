"""Audita documentos SAPL locais e entrega lotes imutáveis, sem rede nem Git.

Cada lote registra hashes dos arquivos, corpos, fontes e evidência IBGE/SAPL.
O confronto com o binário verifica proveniência por hash; não certifica OCR.
"""
import argparse
import collections
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar import validar
from auditar_municipal import metadados, chave
from baixar_organicas_sapl import categoria_norma
from comum import normalizar_chave, slugify
from granularidade_sapl import alertas_multiplos_atos, alertas_outras_publicacoes

RAIZ = Path(__file__).resolve().parent.parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def evidencia_json(path, bruto):
    digest = sha(bruto)
    destino = RAIZ / "municipais/_fonte/auditorias/lotes-sapl/evidencias" / (digest + ".json")
    destino.parent.mkdir(parents=True, exist_ok=True)
    if not destino.exists():
        with destino.open("xb") as f:
            f.write(bruto)
    if sha(destino.read_bytes()) != digest:
        raise ValueError("snapshot de evidência corrompido")
    return {"cache_original": str(path.relative_to(RAIZ)), "path": str(destino.relative_to(RAIZ)), "sha256": digest}


def auditar(path, ibge, indices, casas, identidades, corpos):
    rel = str(path.relative_to(RAIZ))
    b = path.read_bytes()
    texto = b.decode("utf-8")
    meta = metadados(texto)
    erros, avisos = validar(texto, rel, dt.date.today())
    fonte = str(meta.get("fonte", ""))
    match = re.fullmatch(r"https://([a-z0-9.-]+\.(?:leg|gov)\.br)/norma/(\d+)/?", fonte)
    if not match:
        return None  # outra família de fonte requer seu próprio auditor
    host, identificador = match.groups()
    codigo = str(meta.get("codigo_ibge", ""))
    cidade = ibge.get(codigo)
    uf = cidade["regiao-imediata"]["regiao-intermediaria"]["UF"]["sigla"] if cidade else ""
    if not cidade or chave(meta.get("municipio", "")) != chave(cidade["nome"]) or meta.get("uf") != uf:
        erros.append("identidade municipal diverge do cadastro IBGE")
    if cidade and path.parts[-5:-3] != (uf, slugify(normalizar_chave(cidade["nome"]))[:60]):
        # A profundidade canônica é municipais/UF/município/categoria/ano/arquivo.
        erros.append("rota municipal diverge do cadastro IBGE")
    cache = RAIZ / "municipais/_indice/organicas-sapl" / host
    raw = RAIZ / "municipais/_fonte/organicas-sapl" / host / (identificador + ".bin")
    evidencias = []
    if raw.exists():
        digest = sha(raw.read_bytes())
        if digest != meta.get("sha256_fonte"):
            erros.append("hash da fonte bruta diverge")
        evidencias.append({"path": str(raw.relative_to(RAIZ)), "sha256": digest})
    else:
        erros.append("fonte bruta ausente")
    try:
        corpo = texto.split("\n---\n", 1)[1].lstrip("\n").split("\n\n", 1)[1]
        if corpo.endswith("\n"):
            corpo = corpo[:-1]
        digest_corpo = sha(corpo.encode())
        if digest_corpo != meta.get("sha256_texto"):
            erros.append("hash do corpo diverge do registro SAPL")
    except IndexError:
        corpo, digest_corpo = "", ""
        erros.append("corpo ausente")
    alertas_granularidade = alertas_multiplos_atos(corpo, meta.get("tipo_na_fonte", meta.get("tipo", "")), meta.get("numero", ""))
    if alertas_granularidade:
        erros.append("epígrafe de outra identidade no corpo; revisar granularidade do anexo")
    outras_publicacoes = alertas_outras_publicacoes(corpo)
    if outras_publicacoes:
        erros.append("possível aviso/extrato de outra publicação no corpo; revisar contexto")
    if host not in indices:
        normas, tipos, evids = {}, {}, []
        for nome in ("indice.json", "indice-legislacao.json"):
            arq = cache / nome
            if arq.exists():
                bruto = arq.read_bytes()
                dados = json.loads(bruto)
                evids.append(evidencia_json(arq, bruto))
                if str(dados.get("codigo_ibge")) != codigo:
                    erros.append("índice de fonte com código IBGE divergente")
                normas.update({str(n["id"]): n for n in dados["normas"]})
                tipos.update({t["id"]: t["descricao"] for t in dados.get("tipos_reais", dados["tipos"])})
        # Uma execução interrompida pode ter preservado as páginas oficiais e
        # seus documentos sem chegar a escrever o índice agregado final.
        pagina = 1
        while True:
            url = f"https://{host}/api/norma/tiponormajuridica/?page_size=100&page={pagina}"
            arq = cache / (sha(url.encode()) + ".json")
            if not arq.exists():
                break
            bruto = arq.read_bytes()
            dados = json.loads(bruto)
            tipos.update({t["id"]: t["descricao"] for t in dados["results"]})
            evids.append(evidencia_json(arq, bruto))
            if not dados["pagination"].get("next_page"):
                break
            pagina += 1
        for arq in cache.glob("*.json"):
            if not re.fullmatch(r"[0-9a-f]{64}\.json", arq.name):
                continue
            bruto = arq.read_bytes()
            dados = json.loads(bruto)
            resultados = dados.get("results") if isinstance(dados, dict) else None
            if not resultados or not isinstance(resultados[0], dict) or "texto_integral" not in resultados[0]:
                continue
            tipo = resultados[0]["tipo"]
            pagina = dados.get("pagination", {}).get("page")
            url = f"https://{host}/api/norma/normajuridica/?tipo={tipo}&page_size=100&page={pagina}"
            if arq.name != sha(url.encode()) + ".json" or any(n["tipo"] != tipo for n in resultados):
                continue
            evidencia = evidencia_json(arq, bruto)
            for n in resultados:
                normas.setdefault(str(n["id"]), {**n, "_evidencia_paginada": evidencia})
        indices[host] = normas, tipos, evids
    normas, tipos, evids = indices[host]
    evidencias.extend(evids)
    n = normas.get(identificador)
    if n is None:
        erros.append("identificador não encontrado no índice oficial capturado")
    else:
        if n.get("_evidencia_paginada"):
            evidencias.append(n["_evidencia_paginada"])
        categoria = categoria_norma(tipos.get(n["tipo"], ""), n)
        if categoria is None or categoria[0] != path.parts[-3]:
            erros.append("categoria diverge do tipo/ementa oficiais")
        if str(n["numero"]) != str(meta.get("numero")):
            erros.append("número diverge do índice")
        if str(n.get("data") or "") != str(meta.get("data_no_cadastro", meta.get("data", ""))):
            erros.append("data diverge do índice sem observação")
        u = urlsplit(n.get("texto_integral") or "")
        esperado = "https://" + (n["texto_integral"].split("://", 1)[1]) if u.hostname == host else n.get("texto_integral")
        if esperado != meta.get("fonte_texto"):
            erros.append("URL do texto diverge do índice")
    if host not in casas:
        url = f"https://{host}/api/base/casalegislativa/"
        arq = cache / (sha(url.encode()) + ".json")
        if arq.exists():
            bruto = arq.read_bytes()
            casas[host] = json.loads(bruto), evidencia_json(arq, bruto)
        else:
            casas[host] = None, None
    casa, evidencia_casa = casas[host]
    if not casa or not cidade or not any(chave(c.get("municipio", "")) == chave(cidade["nome"]) and c.get("uf") == uf for c in casa.get("results", [])):
        erros.append("identidade da casa SAPL não comprovada no cache oficial")
    if evidencia_casa:
        evidencias.append(evidencia_casa)
    for outros in (identidades.get(fonte, []), corpos.get((codigo, digest_corpo), [])):
        if any(p != rel for p in outros):
            erros.append("identidade ou corpo municipal duplicado no disco; revisar equivalência")
    return {"path": rel, "sha256": sha(b), "sha256_corpo": digest_corpo,
            "fonte": fonte, "fonte_texto": meta.get("fonte_texto"), "codigo_ibge": codigo,
            "evidencias": evidencias, "checks": {"formato": not validar(texto, rel, dt.date.today())[0],
                "origem_ibge_sapl_hashes_indice": not erros},
            "erros": erros, "avisos": avisos, "alertas_granularidade": alertas_granularidade,
            "alertas_outras_publicacoes": outras_publicacoes,
            "limite": "Hash do corpo e fonte verificados; não certifica fidelidade de OCR nem vigência jurídica."}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--baseline", type=Path, required=True)
    ap.add_argument("--candidatos", type=Path, required=True)
    ap.add_argument("--tamanho-lote", type=int, default=1000)
    ap.add_argument("--saida", type=Path, required=True)
    a = ap.parse_args()
    a.saida.mkdir(parents=True, exist_ok=True)
    baseline = set(a.baseline.read_text().split("\0"))
    ibge_path = RAIZ / "municipais/_indice/ibge-municipios.json"
    bruto_ibge = ibge_path.read_bytes()
    ibge = {str(x["id"]): x for x in json.loads(bruto_ibge)}
    entregues = set()
    for p in a.saida.glob("lote-*.json"):
        antigo = json.loads(p.read_text())
        entregues.update(r["path"] for r in antigo["aprovados"] + antigo["retidos"])
    candidatos = [p for p in a.candidatos.read_text().splitlines() if p not in baseline and p not in entregues and "sapl-" in p]
    prioridade = {"lei-organica": 0, "codigo-tributario": 1, "codigos": 1, "plano-diretor": 1, "emendas-lei-organica": 2}
    candidatos.sort(key=lambda p: (prioridade.get(Path(p).parts[3], 3), p))
    # Detecta duplicações também contra documentos anteriores do município.
    identidades, corpos = collections.defaultdict(list), collections.defaultdict(list)
    pastas = sorted({str(Path(p).parent.parent.parent) for p in candidatos})
    for pasta in pastas:
        for p in (RAIZ / pasta).glob("**/*sapl*.md"):
            m = metadados(p.read_text())
            identidades[str(m.get("fonte", ""))].append(str(p.relative_to(RAIZ)))
            corpos[(str(m.get("codigo_ibge", "")), str(m.get("sha256_texto", "")))].append(str(p.relative_to(RAIZ)))
    indices, casas = {}, {}
    aprovados, retidos = [], []
    seq = len(list(a.saida.glob("lote-*.json"))) + 1
    def entregar():
        nonlocal seq, aprovados, retidos
        if not aprovados and not retidos:
            return
        nome = a.saida / f"lote-{seq:04d}"
        dados = {"obtido_em": dt.datetime.now().isoformat(), "baseline": str(a.baseline),
                 "baseline_sha256": sha(a.baseline.read_bytes()), "ibge_sha256": sha(bruto_ibge),
                 "criterio": "auditoria local de fonte individual SAPL; sem rede, sem Git, sem edição dos documentos",
                 "aprovados": aprovados, "retidos": retidos}
        with nome.with_suffix(".json").open("x") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        lista = "".join(r["path"] + "\n" for r in aprovados)
        with nome.with_suffix(".paths.txt").open("x") as f:
            f.write(lista)
        print(json.dumps({"manifesto": str(nome.with_suffix('.json')), "lista": str(nome.with_suffix('.paths.txt')),
                          "aprovados": len(aprovados), "retidos": len(retidos), "sha256_lista": sha(lista.encode())}), flush=True)
        seq += 1
        aprovados, retidos = [], []
    for rel in candidatos:
        try:
            registro = auditar(RAIZ / rel, ibge, indices, casas, identidades, corpos)
        except Exception as e:
            registro = {"path": rel, "erros": [str(e)]}
        if registro is None:
            continue
        (retidos if registro["erros"] else aprovados).append(registro)
        if len(aprovados) >= a.tamanho_lote or len(retidos) >= 2000:
            entregar()
    entregar()


if __name__ == "__main__":
    main()
