"""Gera `estatisticas.html`: uma página com gráficos sobre o acervo.

Percorre os .md uma vez, calcula os números e escreve uma página única, sem dependência externa
nem servidor — os dados vão embutidos como JSON e os gráficos são SVG desenhado na própria página.
Abrir o arquivo no navegador basta (um `fetch` de JSON local seria bloqueado por CORS em `file://`).

    python3 -I scripts/estatisticas.py
"""
import collections
import json
import os
import re
import subprocess
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "estatisticas.html")

UF_NOME = {
    "AC": "Acre", "AL": "Alagoas", "AM": "Amazonas", "AP": "Amapá", "BA": "Bahia",
    "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo", "GO": "Goiás",
    "MA": "Maranhão", "MG": "Minas Gerais", "MS": "Mato Grosso do Sul", "MT": "Mato Grosso",
    "PA": "Pará", "PB": "Paraíba", "PE": "Pernambuco", "PI": "Piauí", "PR": "Paraná",
    "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte", "RO": "Rondônia", "RR": "Roraima",
    "RS": "Rio Grande do Sul", "SC": "Santa Catarina", "SE": "Sergipe", "SP": "São Paulo",
    "TO": "Tocantins",
}

# Categoria pela ementa. A ordem importa: vale a primeira que casar, das mais específicas
# ("utilidade pública") para as mais genéricas ("dispõe sobre"). Medido sobre as 301.350
# ementas do acervo: 13,8% não casam com nenhuma e caem em "Outros".
REGRAS = [
    ("Utilidade pública", r"utilidade publica"),
    ("Título de cidadão e honrarias",
     r"titulo de cidad|cidadao (honorario|benemerito)|cidada (honoraria|benemerita)|comenda|"
     r"medalha|honraria"),
    ("Datas e calendário oficial",
     r"calendario oficial|institui o dia|institui a semana|institui o mes|dia estadual|"
     r"semana estadual|mes estadual|feriado|data comemorativa"),
    ("Denominação de bem público", r"denomina|passa a denominar|da o nome|designa com o nome"),
    ("Auxílios e subvenções",
     r"concede auxilio|auxilio (especial|financeiro)|subvenc|destina recursos|concede subsidio|"
     r"repassa recursos|concede donativo"),
    ("Orçamento e crédito",
     r"credito (adicional|especial|suplementar|extraordinario)|orcament|plano plurianual|"
     r"diretrizes orcamentarias|estima a receita|fixa a despesa|abre credito"),
    ("Tributos e isenções",
     r"\bicms\b|\bipva\b|\bitcd\b|tribut|isenc|aliquota|imposto|\btaxa\b|incentivo fiscal|anistia"),
    ("Pessoal e cargos",
     r"\bcargos?\b|carreira|vencimento|quadro de pessoal|servidor|remunerac|subsidio|gratificac|"
     r"aposentad|plano de cargos|reajust"),
    ("Terras e imóveis", r"desapropri|imovel|terras devolutas|permuta|concede o uso|dominio"),
    ("Convênios e contratos", r"convenio|consorcio|acordo de|contrato de|protocolo de intencoes"),
    ("Transporte, obras e saneamento",
     r"rodovia|estrada|transporte|\bobras?\b|\bponte\b|saneament|energia eletrica|habitac"),
    ("Direitos e assistência social",
     r"assistencia social|crianca|adolescente|idoso|mulher|deficien|indigena|quilombola|"
     r"direitos humanos|violencia|familia"),
    ("Cultura, esporte e turismo",
     r"cultur|esporte|turismo|patrimonio (historico|cultural)|museu|biblioteca|teatro|festa"),
    ("Saúde", r"saude|hospital|\bsus\b|medicament|vacina|sanitari|enfermag"),
    ("Educação", r"educac|escola|ensino|universidade|professor|merenda|bolsa de estudo|creche"),
    ("Meio ambiente",
     r"ambient|residuo|\bagua\b|floresta|poluic|animal|animais|recurso hidrico|agropecuar|"
     r"agricultura"),
    ("Segurança pública", r"policia|seguranca publica|bombeir|penitenciari|presidio|militar"),
    ("Criação de órgão ou entidade",
     r"cria (a|o) (secretaria|fundacao|autarquia|conselho|fundo|empresa|instituto|agencia|"
     r"universidade)|institui o fundo|transforma a|extingue"),
    ("Alteração de outra norma",
     r"\baltera\b|nova redacao|acrescenta|modifica|revoga|introduz|inclui|prorroga"),
    ("Organização administrativa",
     r"dispoe sobre a (organizacao|estrutura)|reorganiza|estrutura administrativa|competencia|"
     r"dispoe sobre"),
]
RX = [(n, re.compile(p)) for n, p in REGRAS]

VAZIAS = set("""a as o os um uma uns umas de do da dos das em no na nos nas por para pelo pela
pelos pelas com sem sobre sob ante apos ate entre contra desde e ou mas que se como quando onde
qual quais cujo cuja ao aos à às e/ou nao sim ja mais menos muito pouco outro outra outros outras
mesmo mesma este esta esse essa aquele aquela isto isso aquilo seu sua seus suas lhe lhes ele ela
eles elas eu tu nos vos me te si tambem ser sendo foi sao era eram tem ter tinha havia haver
dar da-se fica ficam fique forma termos nos-termos art artigo lei leis estado estadual numero
providencias outras-providencias especifica qual-se referido referida citado citada presente
anexo anexos inciso alinea paragrafo caput""".split())


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def categoria(ementa):
    e = sem_acento(ementa).lower()
    for nome, rx in RX:
        if rx.search(e):
            return nome
    return "Outros"


def coletar():
    por_uf = collections.Counter()
    por_tipo = collections.Counter()
    por_ano = collections.Counter()
    por_cat = collections.Counter()
    palavras = collections.Counter()
    cat_por_uf = collections.defaultdict(collections.Counter)
    ocr = total = com_ementa = 0
    tamanho = 0

    for dp, dn, fn in os.walk(RAIZ):
        dn[:] = [d for d in dn if not d.startswith("_") and d not in ("scripts", "fonte", ".git")]
        for f in fn:
            if not f.endswith(".md") or f in ("README.md", "COBERTURA.md"):
                continue
            p = os.path.join(dp, f)
            with open(p, encoding="utf-8", errors="replace") as h:
                texto = h.read()
            total += 1
            tamanho += len(texto)
            if "obtido por OCR" in texto:
                ocr += 1
            partes = os.path.relpath(p, RAIZ).split(os.sep)
            esfera = "FED" if partes[0] == "federal" else (
                partes[1] if partes[0] == "estaduais" else "FED")
            por_uf[esfera] += 1
            if not texto.startswith("---\n"):
                continue
            cab = texto.split("---\n", 2)[1]

            m = re.search(r'^tipo: "(.*)"$', cab, re.M)
            if m:
                por_tipo[m.group(1)] += 1
            m = re.search(r'^data: ?"?(\d{4})-\d{2}-\d{2}"?$', cab, re.M)
            ano = m.group(1) if m else None
            if not ano:
                m = re.search(r'^ano: "?(\d{4})"?$', cab, re.M)
                ano = m.group(1) if m else None
            if ano:
                por_ano[int(ano)] += 1
            m = re.search(r'^ementa: "(.*)"$', cab, re.M)
            if m and m.group(1).strip():
                com_ementa += 1
                c = categoria(m.group(1))
                por_cat[c] += 1
                cat_por_uf[esfera][c] += 1
                for w in re.findall(r"[a-zà-ÿ]{4,}", m.group(1).lower()):
                    if sem_acento(w) not in VAZIAS:
                        palavras[w] += 1
    return dict(por_uf=por_uf, por_tipo=por_tipo, por_ano=por_ano, por_cat=por_cat,
                palavras=palavras, cat_por_uf=cat_por_uf, ocr=ocr, total=total,
                com_ementa=com_ementa, tamanho=tamanho)


def signatarios_do_git():
    """Top signatários pelo histórico, separando pessoas de autorias institucionais."""
    try:
        saida = subprocess.run(["git", "-C", RAIZ, "log", "--format=%an"],
                               capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [], 0
    c = collections.Counter(saida.splitlines())
    inst = re.compile(r"^(Estado d|Distrito Federal|República Federativa|Joao Davi)")
    pessoas = [(n, v) for n, v in c.most_common() if not inst.match(n)]
    return pessoas[:15], len(c)


def main():
    d = coletar()
    pessoas, autores = signatarios_do_git()

    anos = sorted(a for a in d["por_ano"] if 1820 <= a <= 2026)
    serie_ano = [[a, d["por_ano"][a]] for a in anos]
    decadas = collections.Counter()
    for a in anos:
        decadas[(a // 10) * 10] += d["por_ano"][a]

    dados = {
        "total": d["total"],
        "ocr": d["ocr"],
        "com_ementa": d["com_ementa"],
        "autores": autores,
        "caracteres": d["tamanho"],
        "ufs": [[u, n, UF_NOME.get(u, "Federal")] for u, n in d["por_uf"].most_common()],
        "tipos": d["por_tipo"].most_common(),
        "categorias": d["por_cat"].most_common(),
        "ano": serie_ano,
        "decadas": sorted(decadas.items()),
        "palavras": d["palavras"].most_common(80),
        "pessoas": pessoas,
        "cat_uf": {u: c.most_common(6) for u, c in d["cat_por_uf"].items()},
    }
    with open(SAIDA, "w", encoding="utf-8") as h:
        h.write(PAGINA.replace("/*DADOS*/", json.dumps(dados, ensure_ascii=False)))
    print(f"{SAIDA} ({os.path.getsize(SAIDA)/1024:.0f} KB)")
    print(f"  {d['total']} normas, {len(dados['ufs'])} esferas, {autores} autores")


PAGINA = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Legislação brasileira em números</title>
<style>
  :root {
    color-scheme: light;
    --fundo: #fbfaf8; --cartao: #fff; --borda: #e7e3dc; --texto: #1c1a17;
    --suave: #6b655c; --realce: #9a3412; --realce2: #c2410c; --grade: #efece6;
    --serie: #9a3412;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      color-scheme: dark;
      --fundo: #14120f; --cartao: #1c1a17; --borda: #2e2a25; --texto: #f2efe9;
      --suave: #a39c91; --realce: #fb923c; --realce2: #fdba74; --grade: #272320;
      --serie: #fb923c;
    }
  }
  :root[data-theme="dark"] {
    color-scheme: dark;
    --fundo: #14120f; --cartao: #1c1a17; --borda: #2e2a25; --texto: #f2efe9;
    --suave: #a39c91; --realce: #fb923c; --realce2: #fdba74; --grade: #272320;
    --serie: #fb923c;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--fundo); color: var(--texto);
    font: 15px/1.6 ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    -webkit-text-size-adjust: 100%;
  }
  .env { max-width: 1120px; margin: 0 auto; padding: 48px 20px 80px; }
  header { border-bottom: 1px solid var(--borda); padding-bottom: 28px; margin-bottom: 36px; }
  h1 { font-size: clamp(26px, 5vw, 40px); line-height: 1.15; margin: 0 0 10px; letter-spacing: -.02em; }
  .sub { color: var(--suave); max-width: 62ch; margin: 0; }
  h2 {
    font-size: 13px; text-transform: uppercase; letter-spacing: .09em; color: var(--suave);
    margin: 52px 0 16px; font-weight: 600;
  }
  h2:first-of-type { margin-top: 36px; }
  .nota { color: var(--suave); font-size: 13px; margin: 10px 0 0; max-width: 70ch; }
  .numeros { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); }
  .num {
    background: var(--cartao); border: 1px solid var(--borda); border-radius: 12px; padding: 18px;
  }
  .num b { display: block; font-size: clamp(22px, 4vw, 30px); letter-spacing: -.02em; font-variant-numeric: tabular-nums; }
  .num span { color: var(--suave); font-size: 12.5px; }
  .cartao {
    background: var(--cartao); border: 1px solid var(--borda); border-radius: 14px;
    padding: 20px; overflow: hidden;
  }
  .duas { display: grid; gap: 16px; grid-template-columns: 1fr; }
  @media (min-width: 860px) { .duas { grid-template-columns: 1fr 1fr; } }
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  .barras td { padding: 5px 0; vertical-align: middle; }
  .barras td:first-child { white-space: nowrap; padding-right: 12px; color: var(--texto); }
  .barras td:last-child {
    text-align: right; font-variant-numeric: tabular-nums; color: var(--suave);
    padding-left: 12px; white-space: nowrap;
  }
  .trilha { background: var(--grade); border-radius: 4px; height: 20px; width: 100%; min-width: 60px; }
  .barra { background: var(--realce); height: 20px; border-radius: 4px; }
  .rotulo { font-variant-numeric: tabular-nums; }
  svg { display: block; width: 100%; height: auto; }
  .nuvem { line-height: 2.1; }
  .nuvem span { margin-right: 12px; color: var(--realce2); white-space: nowrap; }
  .nuvem span i { color: var(--suave); font-size: 11px; font-style: normal; }
  .rolar { overflow-x: auto; }
  footer { margin-top: 64px; padding-top: 24px; border-top: 1px solid var(--borda); color: var(--suave); font-size: 13px; }
  a { color: var(--realce2); }
  .aviso {
    background: var(--cartao); border: 1px solid var(--borda); border-left: 3px solid var(--realce);
    border-radius: 0 10px 10px 0; padding: 14px 18px; margin: 18px 0 0; font-size: 13.5px;
    color: var(--suave);
  }
</style>
</head>
<body>
<div class="env">
<header>
  <h1>Legislação brasileira em números</h1>
  <p class="sub">O que há no acervo: <span id="resumo"></span>. Tudo calculado a partir dos próprios
  arquivos, por <code>scripts/estatisticas.py</code>.</p>
</header>

<div class="numeros" id="cartoes"></div>

<h2>Normas por esfera</h2>
<div class="cartao"><table class="barras" id="t-ufs"></table></div>
<p class="nota">Paraná e Rio de Janeiro não aparecem: a fonte do PR bloqueia acesso automatizado e
o servidor da ALERJ não respondia. O Acre tem acervo só até 2009.</p>

<h2>Quando foram aprovadas</h2>
<div class="cartao"><div id="g-decadas"></div></div>
<p class="nota">Por década de aprovação. Normas sem data em nenhuma fonte ficam fora deste gráfico.</p>

<h2>Sobre o que as leis tratam</h2>
<div class="cartao"><table class="barras" id="t-cat"></table></div>
<div class="aviso">Categoria inferida da ementa por padrões de texto, não por classificação
oficial. Vale a primeira regra que casa, das mais específicas para as mais genéricas; 13,8% das
ementas não casam com nenhuma e caem em <b>Outros</b>. Serve para ter noção de proporção, não para
contagem exata.</div>

<div class="duas" style="margin-top:16px">
  <div>
    <h2 style="margin-top:36px">Tipo de instrumento</h2>
    <div class="cartao"><table class="barras" id="t-tipos"></table></div>
  </div>
  <div>
    <h2 style="margin-top:36px">Quem mais assinou</h2>
    <div class="cartao"><table class="barras" id="t-pessoas"></table></div>
  </div>
</div>
<p class="nota">O signatário sai do bloco de assinatura do próprio texto. Em cerca de 48% dos
arquivos a assinatura não está na camada de texto do PDF, ou o OCR a perdeu; esses ficam com
autoria institucional e não entram neste ranking.</p>

<h2>Palavras mais frequentes nas ementas</h2>
<div class="cartao nuvem" id="nuvem"></div>
<p class="nota">Palavras de quatro letras ou mais, sem as de função. O tamanho é proporcional à
frequência.</p>

<footer>
  Gerado de <b id="f-total"></b> arquivos Markdown convertidos de fontes oficiais.
  Os textos não substituem a publicação no Diário Oficial.
</footer>
</div>

<script>
const D = /*DADOS*/;
const fmt = n => n.toLocaleString('pt-BR');
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();

document.getElementById('resumo').textContent =
  `${fmt(D.total)} normas, de ${D.ano.length ? D.ano[0][0] : ''} a ${D.ano.length ? D.ano[D.ano.length-1][0] : ''}`;
document.getElementById('f-total').textContent = fmt(D.total);

const cartoes = [
  [fmt(D.total), 'normas em Markdown'],
  [fmt(D.ufs.length - 1) + ' + 1', 'estados e a União'],
  [fmt(D.autores), 'autores no histórico'],
  [(D.caracteres / 1e9).toFixed(2) + ' bi', 'caracteres de texto'],
  [fmt(D.ocr), 'vindas de OCR'],
];
document.getElementById('cartoes').innerHTML = cartoes
  .map(([a, b]) => `<div class="num"><b>${a}</b><span>${b}</span></div>`).join('');

function barras(alvo, dados, rotulo) {
  const max = Math.max(...dados.map(d => d[1]));
  document.getElementById(alvo).innerHTML = dados.map(d => `
    <tr>
      <td>${rotulo(d)}</td>
      <td style="width:100%"><div class="trilha"><div class="barra"
        style="width:${Math.max(2, 100 * d[1] / max)}%"></div></div></td>
      <td class="rotulo">${fmt(d[1])}</td>
    </tr>`).join('');
}

barras('t-ufs', D.ufs, d => d[0] === 'FED' ? 'União' : `${d[2]} <span style="color:var(--suave)">${d[0]}</span>`);
barras('t-cat', D.categorias, d => d[0]);
barras('t-tipos', D.tipos, d => d[0]);
barras('t-pessoas', D.pessoas, d => d[0]);

// --- série por década, em SVG ---
function decadas(alvo, dados) {
  const L = 44, R = 8, T = 10, B = 30, A = 260;
  const n = dados.length, max = Math.max(...dados.map(d => d[1]));
  const W = 900, larg = (W - L - R) / n;
  const y = v => T + (A - T - B) * (1 - v / max);
  const barras = dados.map(([dec, v], i) => {
    const x = L + i * larg;
    return `<rect x="${x + larg * 0.12}" y="${y(v)}" width="${larg * 0.76}"
      height="${A - B - y(v)}" rx="2" fill="var(--serie)">
      <title>${dec}s: ${fmt(v)} normas</title></rect>` +
      (dec % 20 === 0 ? `<text x="${x + larg / 2}" y="${A - 10}" text-anchor="middle"
        font-size="11" fill="var(--suave)">${dec}</text>` : '');
  }).join('');
  const linhas = [0, 0.5, 1].map(f => {
    const v = max * f;
    return `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="var(--grade)"/>
      <text x="${L - 6}" y="${y(v) + 4}" text-anchor="end" font-size="11"
        fill="var(--suave)">${v >= 1000 ? Math.round(v / 1000) + 'k' : Math.round(v)}</text>`;
  }).join('');
  document.getElementById(alvo).innerHTML =
    `<svg viewBox="0 0 ${W} ${A}" role="img" aria-label="normas por década">${linhas}${barras}</svg>`;
}
decadas('g-decadas', D.decadas);

// --- nuvem de palavras ---
const pmax = D.palavras[0][1], pmin = D.palavras[D.palavras.length - 1][1];
document.getElementById('nuvem').innerHTML = D.palavras.map(([p, c]) => {
  const t = 13 + 26 * Math.sqrt((c - pmin) / (pmax - pmin || 1));
  return `<span style="font-size:${t.toFixed(1)}px" title="${fmt(c)} ementas">${p} <i>${fmt(c)}</i></span>`;
}).join('');
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
