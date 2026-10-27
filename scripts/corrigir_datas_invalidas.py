"""Corrige datas impossíveis vindas de erro de digitação na fonte.

Algumas normas vinham com data que não existe no calendário: ano fora de 1800–2026
("0002-12-16", "3023-03-24"), mês 13, dia 39 ou 31 de junho. São erros das próprias fontes,
não da conversão. A data correta é buscada, nesta ordem:

1. a epígrafe do texto (`scripts/datas.py`);
2. a data que já está no campo `titulo`, que vem do índice e não do texto;
3. o ano da pasta — que vem do campo `ano` do índice, independente da data quebrada — combinado
   com o dia e mês da data original;
4. a tabela MANUAL, para os casos em que nada disso serve.

O arquivo é movido para a pasta do ano correto. Uso:

    python3 -I scripts/corrigir_datas_invalidas.py            # simulação
    python3 -I scripts/corrigir_datas_invalidas.py --aplicar
"""
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datas import data_do_texto  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho relativo -> (data, justificativa). Só para o que as regras automáticas não resolvem.
# SEM_DIA significa: a data da fonte é impossível e o dia não é recuperável. O campo `data` fica
# vazio e só o `ano` é afirmado — melhor do que inventar um dia que a fonte não diz.
SEM_DIA = "SEM_DIA"
MANUAL = {
    "estaduais/AP/leis-ordinarias/2027/lei-2180-2027-p41432.md": (
        "2017-05-16",
        "a fonte traz o ano com dois dígitos ('16/05/27'); as leis 2.177, 2.178 e 2.179, vizinhas "
        "na numeração, são todas de 16/05/2017",
    ),
    "estaduais/CE/leis-ordinarias/2006/lei-13852-2006-id5102.md": (
        "2006-12-21",
        "a epígrafe traz o mês 13 ('DE 21.13.06'), que não existe; o Diário Oficial de 28.12.06, "
        "citado na própria epígrafe, situa a lei em dezembro",
    ),
    "estaduais/SC/leis-ordinarias/1956/lei-1496-1956-id1770.md": (
        SEM_DIA, "a fonte diz '31 de junho de 1956', dia que não existe"),
    "estaduais/MA/leis-ordinarias/1997/lei-6990-1997.md": (
        SEM_DIA, "a fonte não informa o dia ('de 00/10/1997', 'DE OUTUBRO DE 1997')"),
    "estaduais/AP/leis-ordinarias/2015/lei-1920-2015-p31352.md": (
        SEM_DIA, "a fonte diz '31/06/15', dia que não existe em junho"),
    "estaduais/AP/leis-ordinarias/2015/lei-1972-2015-p37045.md": (
        SEM_DIA, "a fonte diz '39/12/15', dia inexistente"),
    "estaduais/AP/leis-ordinarias/2000/lei-1136-2000-p11135.md": (
        SEM_DIA, "a fonte não informa data alguma ('00/00/00')"),
    "estaduais/CE/leis-ordinarias/2007/lei-13894-2007-id4806.md": (
        SEM_DIA, "a fonte diz '31.06.07', dia que não existe em junho"),
    "estaduais/RN/leis-ordinarias/2026/lei-12626-2026-12-31-lpn5p43zo2.md": (
        "2025-12-31",
        "o índice da Assembleia diz 31.12.2026, data futura; a epígrafe do texto diz '31 de "
        "dezembro de 2025' e as leis 12.624, 12.625 e 12.627 são todas de 31/12/2025",
    ),
}


def ano_ok(texto):
    if not re.fullmatch(r"\d{4}", texto or ""):
        return False
    # 1821 é o ano da norma mais antiga do acervo; nada anterior é data de lei brasileira
    return 1821 <= int(texto) <= datetime.date.today().year


def plausivel(data):
    """A data existe no calendário e está no intervalo em que há legislação brasileira."""
    if not data or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", data):
        return False
    ano, mes, dia = (int(x) for x in data.split("-"))
    if not ano_ok(str(ano)):
        return False
    try:
        d = datetime.date(ano, mes, dia)
    except ValueError:
        return False
    # lei promulgada não tem data no futuro; quando tem, é erro de digitação da fonte
    return d <= datetime.date.today()


def data_do_titulo(titulo):
    m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", titulo)
    if m:
        d = f"{int(m.group(3)):04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"
        return d if plausivel(d) else None
    return data_do_texto(titulo) or None


def caminho_fonte(md):
    """estaduais/UF/pasta/ano/x.md -> estaduais/UF/_fonte/pasta/ano/x.* (o original guardado)."""
    partes = os.path.relpath(md, RAIZ).split(os.sep)
    if len(partes) < 5 or partes[0] != "estaduais":
        return None
    uf, resto = partes[1], partes[2:]
    base = os.path.join(RAIZ, "estaduais", uf, "_fonte", *resto)
    raiz_sem_ext = os.path.splitext(base)[0]
    for ext in (".html.gz", ".pdf.gz", ".gz"):
        if os.path.exists(raiz_sem_ext + ext):
            return raiz_sem_ext + ext
    pasta = os.path.dirname(base)
    alvo = os.path.splitext(os.path.basename(md))[0]
    if os.path.isdir(pasta):
        for f in os.listdir(pasta):
            if f.startswith(alvo):
                return os.path.join(pasta, f)
    return None


def mover_fonte(md_antigo, md_novo):
    """Move o original guardado junto com o .md, para o reconverter continuar achando."""
    origem = caminho_fonte(md_antigo)
    if not origem:
        return
    destino = caminho_fonte(md_novo) or os.path.join(
        os.path.dirname(origem).replace(
            os.sep + os.path.basename(os.path.dirname(origem)),
            os.sep + os.path.basename(os.path.dirname(md_novo))),
        os.path.basename(origem))
    if os.path.abspath(origem) == os.path.abspath(destino):
        return
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    os.rename(origem, destino)
    print(f"      _fonte movido: {os.path.relpath(destino, RAIZ)}")


def main(aplicar):
    achados = 0
    for dp, dn, fn in os.walk(RAIZ):
        dn[:] = [d for d in dn if not d.startswith("_") and d not in ("scripts", "fonte", ".git")]
        for f in sorted(fn):
            if not f.endswith(".md") or f in ("README.md", "COBERTURA.md"):
                continue
            p = os.path.join(dp, f)
            with open(p, encoding="utf-8") as h:
                texto = h.read()
            m = re.search(r'^data: ?"?(\d{4}-\d{2}-\d{2})"?$', texto, re.M)
            if not m or plausivel(m.group(1)):
                continue
            achados += 1
            rel = os.path.relpath(p, RAIZ)
            velha = m.group(1)
            cab, corpo = texto.split("---\n", 2)[1], texto.split("---\n", 2)[2]
            num = re.search(r'^numero: "(.*)"$', cab, re.M)
            tit = re.search(r'^titulo: "(.*)"$', cab, re.M)

            nova = razao = None
            achada = data_do_texto(corpo, num.group(1) if num else None)
            if plausivel(achada):
                nova, razao = achada, "epígrafe do texto"
            if not nova and tit:
                achada = data_do_titulo(tit.group(1))
                if plausivel(achada):
                    nova, razao = achada, "campo titulo"
            if not nova:
                pasta = os.path.basename(dp)
                if ano_ok(pasta) and plausivel(f"{pasta}-{velha[5:]}"):
                    nova = f"{pasta}-{velha[5:]}"
                    razao = "ano da pasta + dia/mês originais"
            if not nova and rel in MANUAL:
                nova, razao = MANUAL[rel][0], MANUAL[rel][1]
            if not nova:
                print(f"  NÃO RESOLVIDO  {velha}  {rel}")
                continue

            print(f"  {velha} -> {nova}  ({razao})\n      {rel}")
            if not aplicar:
                continue
            if nova == SEM_DIA:
                # dia irrecuperável: data vazia e o ano afirmado à parte
                ano = velha[:4]
                novo_texto = re.sub(r'^data: ?"?\d{4}-\d{2}-\d{2}"?$', 'data: ""', texto,
                                    count=1, flags=re.M)
                if re.search(r'^ano:', novo_texto, re.M):
                    novo_texto = re.sub(r'^ano: ?.*$', f'ano: "{ano}"', novo_texto, count=1,
                                        flags=re.M)
                else:
                    novo_texto = re.sub(r'^(data: "")$', f'\\1\nano: "{ano}"', novo_texto,
                                        count=1, flags=re.M)
            else:
                novo_texto = re.sub(r'^data: ?"?\d{4}-\d{2}-\d{2}"?$', f"data: {nova}", texto,
                                    count=1, flags=re.M)
                ano = nova[:4]
            destino = os.path.join(RAIZ, os.path.dirname(os.path.dirname(rel)), ano, f)
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            if os.path.exists(destino) and destino != p:
                print(f"      COLISÃO, só o campo foi corrigido: {destino}")
                destino = p
            with open(destino, "w", encoding="utf-8") as h:
                h.write(novo_texto)
            if destino != p:
                os.remove(p)
                mover_fonte(p, destino)
    print(f"\n{achados} datas impossíveis" + ("" if aplicar else " — simulação, use --aplicar"))


if __name__ == "__main__":
    main("--aplicar" in sys.argv)
