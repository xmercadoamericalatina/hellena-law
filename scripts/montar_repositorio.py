"""Monta um repositório git em que cada commit é uma norma.

O autor do commit é quem assinou a norma (lido do bloco de assinatura, ver `scripts/signatarios.py`)
e a data do commit é a data em que a norma foi aprovada. A história fica em ordem cronológica, de
1821 até hoje — um `git log` do repositório é uma linha do tempo da legislação brasileira.

Quando o texto não revela o signatário (pouco mais de um terço dos casos: PDFs em que a assinatura
não está na camada de texto, ou OCR que a perdeu), o autor é a instituição — "Estado do Pará",
"República Federativa do Brasil". A mensagem do commit sempre diz de onde o autor saiu.

O e-mail é sintético: `nome-sobrenome-NNNNN@exemplo.com`, com cinco dígitos derivados do próprio
nome — assim cada pessoa tem sempre a mesma identidade no histórico.

Usa `git fast-import`: com 323 mil commits, um `git commit` por norma levaria dias.

O git conta a data em segundos desde 1970. Datas anteriores viram timestamp negativo, que o próprio
`git fsck` classifica como `badDate` — e o GitHub, que roda essa checagem ao receber, rejeita o
pacote inteiro. Como a maior parte do acervo é anterior a 1970, a data do commit dessas normas é
fixada no instante mais antigo representável (01-01-1970) e a data real vai no fim do título do
commit, depois de " | ", e repetida no corpo. A ordem cronológica se mantém pela sequência de
commits, que é linear.

    python3 -I scripts/montar_repositorio.py --saida /caminho/do/repo
"""
import argparse
import calendar
import hashlib
import os
import re
import subprocess
import sys
import time
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from signatarios import signatarios  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UFS = {
    "AC": "Estado do Acre", "AL": "Estado de Alagoas", "AM": "Estado do Amazonas",
    "AP": "Estado do Amapá", "BA": "Estado da Bahia", "CE": "Estado do Ceará",
    "DF": "Distrito Federal", "ES": "Estado do Espírito Santo", "GO": "Estado de Goiás",
    "MA": "Estado do Maranhão", "MG": "Estado de Minas Gerais", "MS": "Estado de Mato Grosso do Sul",
    "MT": "Estado de Mato Grosso", "PA": "Estado do Pará", "PB": "Estado da Paraíba",
    "PE": "Estado de Pernambuco", "PI": "Estado do Piauí", "PR": "Estado do Paraná",
    "RJ": "Estado do Rio de Janeiro", "RN": "Estado do Rio Grande do Norte",
    "RO": "Estado de Rondônia", "RR": "Estado de Roraima", "RS": "Estado do Rio Grande do Sul",
    "SC": "Estado de Santa Catarina", "SE": "Estado de Sergipe", "SP": "Estado de São Paulo",
    "TO": "Estado do Tocantins",
}
UNIAO = "República Federativa do Brasil"

# normas sem data em lugar algum: ordenadas no fim e datadas da importação
SEM_DATA = "9999-99-99"
AGORA = int(time.time())

IGNORAR = """# originais baixados (27 GB) e índices: reproduzíveis pelos scripts, não versionados
_fonte/
_indice/
_log*.txt
*.log
.DS_Store
scripts/bin/
"""


def email(nome):
    """nome-sobrenome-NNNNN@exemplo.com, estável para o mesmo nome."""
    sem_acento = "".join(
        c for c in unicodedata.normalize("NFD", nome) if unicodedata.category(c) != "Mn")
    partes = [p for p in re.split(r"[^A-Za-z]+", sem_acento) if p]
    base = "-".join(partes[:3]).lower() or "sem-nome"
    digitos = int(hashlib.sha256(nome.encode("utf-8")).hexdigest(), 16) % 100000
    return f"{base}-{digitos:05d}@exemplo.com"


def campos(cabecalho):
    d = {}
    for ln in cabecalho.split("\n"):
        m = re.match(r"^(\w+): ?(.*)$", ln)
        if m:
            d[m.group(1)] = m.group(2).strip().strip('"')
    return d


def normas():
    """Lista de (data, caminho_relativo, meta, corpo), sem ordenação."""
    saida = []
    for dp, dn, fn in os.walk(RAIZ):
        dn[:] = [d for d in dn if not d.startswith("_") and d not in ("scripts", "fonte", ".git")]
        for f in sorted(fn):
            if not f.endswith(".md") or f in ("README.md", "COBERTURA.md"):
                continue
            p = os.path.join(dp, f)
            with open(p, encoding="utf-8") as h:
                texto = h.read()
            rel = os.path.relpath(p, RAIZ)
            if not texto.startswith("---\n"):  # constituicao.md, sem cabeçalho
                saida.append(("1988-10-05", rel, {"titulo": "Constituição da República Federativa "
                                                            "do Brasil de 1988"}, texto))
                continue
            _, cab, corpo = texto.split("---\n", 2)
            meta = campos(cab)
            data = meta.get("data", "")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", data):
                ano = meta.get("ano", "")
                if re.fullmatch(r"\d{4}", ano):
                    data = f"{ano}-01-01"
                    meta["_data_aproximada"] = "só o ano é conhecido"
                else:
                    pasta = os.path.basename(dp)
                    if re.fullmatch(r"\d{4}", pasta):
                        data = f"{pasta}-01-01"
                        meta["_data_aproximada"] = "só o ano é conhecido"
                    else:
                        data = SEM_DATA  # vai para o fim da história
            saida.append((data, rel, meta, corpo))
    return saida


def autor(meta, corpo):
    """(nome, email, [co-autores], procedencia)."""
    principal, demais, grau = signatarios(corpo)
    if principal:
        origem = ("assinatura no texto" if grau == "caixa-alta"
                  else "promulgação pelo Legislativo")
        return principal, email(principal), demais, origem
    uf = meta.get("uf")
    inst = UFS.get(uf, UNIAO) if uf else UNIAO
    return inst, email(inst), [], "signatário não identificado no texto; autoria institucional"


def mensagem(meta, rel, co, origem, data, grampeada):
    titulo = meta.get("titulo") or os.path.basename(rel)
    # o sufixo só existe onde a data do commit não é a da norma: nos demais ela já está no commit
    if grampeada:
        ano, mes, dia = data.split("-")
        titulo = f"{titulo} | {dia}-{mes}-{ano}"
    elif not data:
        titulo = f"{titulo} | sem data na fonte"
    linhas = [titulo, ""]
    if meta.get("ementa"):
        linhas += [meta["ementa"], ""]
    if grampeada:
        linhas.append(f"Data da norma: {data}")
        linhas.append(
            "A data do commit está fixada em 01-01-1970: o git não representa data anterior a essa "
            "(vira timestamp negativo, que o GitHub rejeita). A data real da norma é a do título e "
            "a da linha acima.")
    elif not data:
        linhas.append(
            "A fonte não informa a data desta norma; a data do commit é a da importação.")
    if meta.get("_data_aproximada"):
        linhas.append(f"Precisão: {meta['_data_aproximada']}.")
    linhas.append(f"Autoria: {origem}.")
    if meta.get("fonte"):
        linhas.append(f"Fonte: {meta['fonte']}")
    linhas.append("")
    for c in co:
        linhas.append(f"Co-Authored-By: {c} <{email(c)}>")
    return "\n".join(linhas) + "\n"


def dados(s):
    b = s.encode("utf-8")
    return b"data %d\n" % len(b) + b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", required=True, help="pasta do repositório a criar")
    ap.add_argument("--limite", type=int, help="processa só as N primeiras normas (teste)")
    a = ap.parse_args()

    repo = os.path.abspath(a.saida)
    os.makedirs(repo, exist_ok=True)
    subprocess.run(["git", "init", "-q", "-b", "main", repo], check=True)

    itens = normas()
    itens.sort(key=lambda x: (x[0], x[1]))
    if a.limite:
        itens = itens[: a.limite]
    print(f"{len(itens)} normas; de {itens[0][0]} a {itens[-1][0]}", flush=True)

    fluxo = subprocess.Popen(
        ["git", "fast-import", "--quiet", "--date-format=raw"],
        cwd=repo, stdin=subprocess.PIPE)
    w = fluxo.stdin
    eu = "Joao Davi <joao@supersoniclabs.ai>"

    # commit inicial: ferramentas e documentação
    base = []
    for nome in ("README.md", "COBERTURA.md"):
        if os.path.exists(os.path.join(RAIZ, nome)):
            base.append(nome)
    for dp, dn, fn in os.walk(os.path.join(RAIZ, "scripts")):
        dn[:] = [d for d in dn if d not in ("bin", "__pycache__")]
        for f in sorted(fn):
            if f.endswith((".py", ".swift")):
                base.append(os.path.relpath(os.path.join(dp, f), RAIZ))
    w.write(b"commit refs/heads/main\n")
    w.write(("committer %s 0 +0000\n" % eu).encode())
    w.write(dados("Ferramentas e documentação do acervo\n\n"
                  "Os commits seguintes são as normas, em ordem cronológica, assinadas por quem as "
                  "aprovou.\n"))
    w.write(b"M 100644 inline .gitignore\n")
    w.write(dados(IGNORAR))
    for rel in base:
        with open(os.path.join(RAIZ, rel), encoding="utf-8") as h:
            w.write(("M 100644 inline %s\n" % rel).encode())
            w.write(dados(h.read()))

    for n, (data, rel, meta, corpo) in enumerate(itens, 1):
        nome, mail, co, origem = autor(meta, corpo)
        if data == SEM_DATA:
            data_real, quando, grampeada = "", AGORA, False
        else:
            ano, mes, dia = (int(x) for x in data.split("-"))
            bruto = calendar.timegm((ano, mes, dia, 12, 0, 0))
            data_real = data
            grampeada = bruto < 0
            quando = max(bruto, 0)
        ident = "%s <%s>" % (nome.replace("<", "").replace(">", ""), mail)
        w.write(b"commit refs/heads/main\n")
        w.write(("author %s %d +0000\n" % (ident, quando)).encode())
        w.write(("committer %s %d +0000\n" % (ident, quando)).encode())
        w.write(dados(mensagem(meta, rel, co, origem, data_real, grampeada)))
        caminho = os.path.join(RAIZ, rel)
        with open(caminho, "rb") as h:
            conteudo = h.read()
        w.write(("M 100644 inline %s\n" % rel).encode())
        w.write(b"data %d\n" % len(conteudo) + conteudo + b"\n")
        if n % 20000 == 0:
            print(f"  {n}/{len(itens)}", flush=True)

    w.write(b"done\n")
    w.close()
    if fluxo.wait() != 0:
        sys.exit("fast-import falhou")
    if os.path.abspath(repo) == RAIZ:
        # repositório montado sobre o próprio acervo: aponta HEAD e índice para a história
        # construída sem escrever nada na árvore de trabalho, que já tem esse conteúdo.
        subprocess.run(["git", "symbolic-ref", "HEAD", "refs/heads/main"], cwd=repo, check=True)
        subprocess.run(["git", "reset", "--mixed", "-q", "main"], cwd=repo, check=True)
    else:
        subprocess.run(["git", "checkout", "-q", "main"], cwd=repo, check=True)
    print("pronto:", repo, flush=True)


if __name__ == "__main__":
    main()
