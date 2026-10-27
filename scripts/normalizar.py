"""Normaliza nomes de pasta, valores de `tipo` e a ordem dos campos do cabeçalho.

Cada fonte foi raspada por um script próprio e cada uma nomeava as coisas à sua maneira: oito
Assembleias com SAPL gravavam `lei-ordinaria` onde as outras gravavam `leis-ordinarias`, e o mesmo
instrumento aparecia como "Lei", "Lei Ordinária", "Lei ordinária" e "LEI ORDINARIA". Este script
converge tudo para um vocabulário fechado.

Regras:

- pastas vão para a forma plural canônica (`lei-ordinaria` -> `leis-ordinarias`);
- `tipo` vira um dos valores de TIPOS_CANONICOS;
- `data` passa a existir sempre; quando a fonte não a informa, é lida da epígrafe do texto
  (ver `scripts/datas.py`) e fica vazia só se nem lá estiver;
- `ano` só fica quando é um ano de verdade — `"sem-ano"` era o nome da pasta vazando para o campo;
- os campos são gravados na ordem de ORDEM_CAMPOS.

Instrumentos distintos não são fundidos: `constituicoes-historicas` (BA), `leis-constitucionais`
(MG), `decretos-lei-complementares` (SP), `lei-organica`/`emendas-lei-organica` (DF) e
`leis-promulgadas` continuam separados, porque a fonte os distingue.

Uso:

    python3 -I scripts/normalizar.py            # simulação: só relata
    python3 -I scripts/normalizar.py --aplicar  # grava
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datas import data_do_texto  # noqa: E402
from comum import CANONICO, normalizar_chave  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PASTAS = {
    "constituicao-estadual": "constituicao",
    "constituicao-do-estado": "constituicao",
    "emenda-constitucional": "emendas-constitucionais",
    "emenda-constituicao": "emendas-constitucionais",
    "emenda-a-ce": "emendas-constitucionais",
    "lei-ordinaria": "leis-ordinarias",
    "lei": "leis-ordinarias",
    "lei-complementar": "leis-complementares",
    "lei-complementar-consolidada": "leis-complementares",
    "lei-delegada": "leis-delegadas",
    "decreto-lei": "decretos-lei",
    "lei-promulgada": "leis-promulgadas",
    "lei-ordinaria-promulgada": "leis-promulgadas",
}

TIPOS = {
    "Lei": "Lei Ordinária",
    "Lei ordinária": "Lei Ordinária",
    "LEI ORDINARIA": "Lei Ordinária",
    "Lei (não numerada)": "Lei Ordinária",
    "LEI COMPLEMENTAR": "Lei Complementar",
    "Lei Complementar Consolidada": "Lei Complementar",
    "LEI DELEGADA": "Lei Delegada",
    "Emenda à Constituição": "Emenda Constitucional",
    "Emenda a CE": "Emenda Constitucional",
    "EMENDA À CONSTITUIÇÃO": "Emenda Constitucional",
    "Emenda à Constituição Estadual": "Emenda Constitucional",
    "Constituição do Estado": "Constituição Estadual",
    "CONSTITUIÇÃO ESTADUAL": "Constituição Estadual",
    "Decreto Lei": "Decreto-Lei",
    "Lei Ordinária Promulgada": "Lei Promulgada",
}

# as constituições históricas da Bahia traziam o ano no tipo ("Constituição Estadual (1891)");
# o ano já está na pasta, no título e em `data`.
ANO_NO_TIPO = re.compile(r"^(Constituição Estadual) \(\d{4}\)$")

TIPOS_CANONICOS = {
    "Constituição Estadual", "Emenda Constitucional", "Lei Ordinária", "Lei Complementar",
    "Lei Delegada", "Lei Constitucional", "Lei Promulgada", "Decreto-Lei",
    "Decreto-Lei Complementar", "Lei Orgânica", "Emenda à Lei Orgânica",
}
TIPOS_CANONICOS.update(tipo for _, tipo in CANONICO.values())

ORDEM_CAMPOS = [
    "titulo", "uf", "tipo", "numero", "data", "ano", "ementa", "situacao", "revogada",
    "versao_texto", "publicacao", "data_publicacao", "urn", "fonte", "arquivo", "baixado_em",
]

CAMPO = re.compile(r"^(\w+):(.*)$")


def renomear_pastas(aplicar, cont):
    base = os.path.join(RAIZ, "estaduais")
    for uf in sorted(os.listdir(base)):
        d = os.path.join(base, uf)
        if not os.path.isdir(d):
            continue
        for sub in sorted(os.listdir(d)):
            novo = PASTAS.get(sub) or CANONICO.get(normalizar_chave(sub), (None, None))[0]
            if not novo or novo == sub or not os.path.isdir(os.path.join(d, sub)):
                continue
            origem, destino = os.path.join(d, sub), os.path.join(d, novo)
            if os.path.exists(destino):
                # funde: move os arquivos ano a ano, abortando se houver colisão de nome
                for ano in sorted(os.listdir(origem)):
                    po, pd = os.path.join(origem, ano), os.path.join(destino, ano)
                    for f in os.listdir(po):
                        if os.path.exists(os.path.join(pd, f)):
                            print(f"  COLISÃO, não movido: {uf}/{sub}/{ano}/{f}")
                            cont["colisao"] += 1
                            continue
                        if aplicar:
                            os.makedirs(pd, exist_ok=True)
                            os.rename(os.path.join(po, f), os.path.join(pd, f))
                        cont["movidos"] += 1
                if aplicar:
                    for raiz, _, arqs in os.walk(origem, topdown=False):
                        if not arqs:
                            os.rmdir(raiz)
            else:
                if aplicar:
                    os.rename(origem, destino)
                cont["pastas"] += 1
            print(f"  {uf}/{sub} -> {uf}/{novo}")


def normalizar_cabecalho(texto):
    """Devolve o texto com tipo canônico e campos na ordem padrão, ou None se não se aplica."""
    if not texto.startswith("---\n"):
        return None
    try:
        _, fm, corpo = texto.split("---\n", 2)
    except ValueError:
        return None
    campos = []
    for ln in fm.rstrip("\n").split("\n"):
        m = CAMPO.match(ln)
        if not m:
            return None  # cabeçalho fora do formato: não arrisca
        campos.append([m.group(1), m.group(2)])

    d = dict(campos)
    # o corpo abre com o título em H1. Os raspadores estaduais já faziam isso; o federal, não.
    titulo = d.get("titulo", "").strip().strip('"')
    if titulo and corpo.strip() and not corpo.lstrip("\n").startswith("# "):
        corpo = f"# {titulo}\n\n" + corpo.lstrip("\n")
    if "tipo" in d:
        bruto = d["tipo"].strip().strip('"')
        bruto = ANO_NO_TIPO.sub(r"\1", bruto)
        tipo = CANONICO.get(normalizar_chave(bruto), (None, TIPOS.get(bruto, bruto)))[1]
        d["tipo"] = ' "%s"' % tipo
    if d.get("ano", "").strip().strip('"') in ("sem-ano", ""):
        d.pop("ano", None)
    if "data" not in d:
        d["data"] = ' ""'
    # fonte sem data (ou só com o ano): tenta a epígrafe do texto
    if not re.fullmatch(r'\s*"?\d{4}-\d{2}-\d{2}"?', d["data"]):
        achada = data_do_texto(corpo, d.get("numero", "").strip().strip('"'))
        if achada:
            d["data"] = f" {achada}"

    vistos = []
    for k in ORDEM_CAMPOS:
        if k in d:
            vistos.append(f"{k}:{d[k]}")
    for k in d:  # campos não previstos: preservados no fim
        if k not in ORDEM_CAMPOS:
            vistos.append(f"{k}:{d[k]}")
    novo = "---\n" + "\n".join(vistos) + "\n---\n" + corpo
    return novo if novo != texto else None


def main(aplicar):
    cont = collections.Counter()
    print("pastas:")
    renomear_pastas(aplicar, cont)
    print("\ncabeçalhos:")
    tipos = collections.Counter()
    for dp, dn, fn in os.walk(RAIZ):
        dn[:] = [x for x in dn if not x.startswith("_") and x not in ("scripts", "fonte", ".git")]
        for f in fn:
            if not f.endswith(".md") or f in ("README.md", "COBERTURA.md"):
                continue
            p = os.path.join(dp, f)
            with open(p, encoding="utf-8") as h:
                texto = h.read()
            cont["arquivos"] += 1
            novo = normalizar_cabecalho(texto)
            if novo is None:
                if not texto.startswith("---\n"):
                    cont["sem_front_matter"] += 1
                continue
            cont["cabecalhos"] += 1
            if aplicar:
                with open(p, "w", encoding="utf-8") as h:
                    h.write(novo)
            m = re.search(r'^tipo: "(.*)"$', novo, re.M)
            if m:
                tipos[m.group(1)] += 1
    print(f"  arquivos: {cont['arquivos']}; cabeçalhos ajustados: {cont['cabecalhos']}; "
          f"sem front matter: {cont['sem_front_matter']}")
    print(f"  pastas renomeadas: {cont['pastas']}; arquivos movidos em fusão: {cont['movidos']}; "
          f"colisões: {cont['colisao']}")
    fora = {t: n for t, n in tipos.items() if t not in TIPOS_CANONICOS}
    if fora:
        print("  AVISO, tipo fora do vocabulário:", fora)
    if not aplicar:
        print("\nsimulação — use --aplicar para gravar")


if __name__ == "__main__":
    main("--aplicar" in sys.argv)
