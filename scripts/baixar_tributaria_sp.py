"""Consolidação tributária paulistana: decreto e seu único anexo oficial, um documento.

Não transforma o índice do anexo em normas independentes. Preserva a identidade
formal do Decreto 65.599/2026 e o corte temporal da compilação aprovada.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re
import sys
import subprocess

sys.path.insert(0, str(Path(__file__).resolve().parent))
from comum import Rede, yaml_str
from html2md import convert

RAIZ = Path(__file__).resolve().parent.parent
URL = 'https://legislacao.prefeitura.sp.gov.br/decreto-65599-de-1-de-outubro-de-2026'


def transcricao_anexo(pdf, tabelas=None):
    """Conserva colunas/tabelas e números isolados; só retira fólio sequencial."""
    r = subprocess.run(['pdftotext', '-layout', '-enc', 'UTF-8', str(pdf), '-'],
                       capture_output=True, check=True, timeout=300)
    paginas = [p for p in r.stdout.decode().split('\f') if p.strip()]
    if len(paginas) != 232:
        raise ValueError('anexo mudou de extensão; revisão necessária')
    limpas = []
    for numero, pagina in enumerate(paginas, 1):
        linhas = pagina.splitlines()
        primeiro = next(i for i,x in enumerate(linhas) if x.strip())
        if linhas[primeiro].strip() != str(numero):
            raise ValueError('fólio sequencial não reconhecido; não retirar números por heurística')
        del linhas[primeiro]
        texto_pagina='\n'.join(linhas).strip('\n')
        tabela=(tabelas or {}).get(str(numero))
        if tabela:
            transcrita='\n'.join(' | '.join(row) for row in [tabela['cabecalho']]+tabela['linhas'])
            texto_pagina=(transcrita+'\n\n'+texto_pagina if tabela['posicao']=='antes_do_texto' else texto_pagina+'\n\n'+transcrita)
        limpas.append(texto_pagina)
    return '```text\n' + '\n\n'.join(limpas) + '\n```'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ibge = json.loads((RAIZ / 'municipais/_indice/ibge-municipios.json').read_text())
    cidade = next(x for x in ibge if str(x['id']) == '3550308')
    if cidade['nome'] != 'São Paulo' or cidade['regiao-imediata']['regiao-intermediaria']['UF']['sigla'] != 'SP':
        raise ValueError('identidade IBGE diverge do catálogo')
    pasta = RAIZ / 'municipais/_fonte/capitais/sao-paulo'
    pasta.mkdir(parents=True, exist_ok=True)
    destino = RAIZ / 'municipais/SP/sao-paulo/decretos/2026/decreto-65599-2026.md'
    if destino.exists():
        print('já existente', destino)
        return
    rede = Rede(rps=1)
    def capturar(url, nome):
        p = pasta / nome
        if not p.exists():
            st, b, _ = rede.get(url, tentativas=1, timeout=90)
            if st != 200:
                raise ValueError('fonte indisponível HTTP ' + str(st))
            with p.open('xb') as f:
                f.write(b)
        return p.read_bytes(), p
    html, origem = capturar(URL, 'decreto-65599-2026.html')
    texto = html.decode('utf-8')
    trecho = re.search(r'<div class="col s12 customStyle">\s*(.*?)<div class="bx-mensagem', texto, re.S)
    if not trecho:
        raise ValueError('seção individual da norma não reconhecida')
    corpo_decreto = convert(trecho[1])
    if not all(s in corpo_decreto for s in ('65.599', 'OUTUBRO', '2026', 'Art. 1º', 'Art. 2º', 'Consolidação das Leis Tributárias')):
        raise ValueError('identidade/data/conteúdo do decreto não comprovados')
    link = re.search(r'Anexo nº.*?href="([^"]+)"[^>]*>162347694</a>', texto, re.S)
    if not link:
        raise ValueError('anexo oficial esperado não identificado')
    url_anexo = link[1]
    bruto, anexo = capturar(url_anexo, 'decreto-65599-2026-anexo.pdf')
    if not bruto.startswith(b'%PDF'):
        raise ValueError('anexo não é PDF')
    tabela_path=RAIZ/'scripts/dados/sp-tributaria-65599-tabelas.json'
    tabelas=json.loads(tabela_path.read_text())
    if sha(bruto)!=tabelas['sha256_pdf']:
        raise ValueError('PDF diferente da fonte das tabelas manualmente conferidas')
    corpo_anexo = transcricao_anexo(anexo,tabelas['paginas'])
    if not all(s in corpo_anexo for s in ('Anexo Único', 'Art. 1', 'IPTU', 'ISS')):
        raise ValueError('conteúdo do anexo não reconhecido')
    corpo = corpo_decreto + '\n\n## Anexo Único — Consolidação das Leis Tributárias\n\n' + corpo_anexo
    titulo = 'Decreto nº 65.599, de 1º de outubro de 2026 — Consolidação das Leis Tributárias do Município de São Paulo'
    meta = {'titulo': titulo, 'tipo': 'Decreto', 'numero': '65599', 'data': '2026-10-01',
            'municipio': 'São Paulo', 'uf': 'SP', 'codigo_ibge': '3550308',
            'versao_texto': 'texto original do decreto e Anexo Único oficial que aprova a consolidação; corte da publicação de 01/10/2026, sem certificação de atualização posterior; anexo preformatado e três tabelas em imagem transcritas e conferidas visualmente',
            'fonte': URL, 'fonte_texto': URL, 'fonte_anexo': url_anexo,
            'sha256_fonte': sha(html), 'sha256_anexo': sha(bruto), 'sha256_texto': sha(corpo.encode()),
            'baixado_em': dt.date.today().isoformat()}
    saida = '\n'.join(['---'] + [k + ': ' + yaml_str(v) for k,v in meta.items()] + ['revogada: null', '---', '', '# ' + titulo, '', corpo, ''])
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open('x') as f:
        f.write(saida)
    manifesto = {'path': str(destino.relative_to(RAIZ)), 'sha256': sha(saida.encode()),
                  'fontes': [{'url': URL, 'path': str(origem.relative_to(RAIZ)), 'sha256': sha(html)},
                             {'url': url_anexo, 'path': str(anexo.relative_to(RAIZ)), 'sha256': sha(bruto)}],
                  'sha256_corpo_decreto': sha(corpo_decreto.encode()), 'sha256_corpo_anexo': sha(corpo_anexo.encode()),
                  'transcricao_tabelas': {'path':str(tabela_path.relative_to(RAIZ)),'sha256':sha(tabela_path.read_bytes()),'linhas':56,'paginas':[142,226]},
                  'criterio': 'Documento individual: decreto formal e seu anexo integrante; não contado como lei tributária original ou edição diária.',
                  'obtido_em': dt.datetime.now().isoformat()}
    with (pasta / 'decreto-65599-2026.manifesto.json').open('x') as f:
        json.dump(manifesto, f, ensure_ascii=False, indent=2)
    print(json.dumps(manifesto, ensure_ascii=False))


if __name__ == '__main__':
    main()
