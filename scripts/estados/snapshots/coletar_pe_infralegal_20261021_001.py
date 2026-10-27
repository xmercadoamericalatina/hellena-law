"""Captura serial de um índice PE congelado; coleta não equivale a publicação.

Sem ano no índice, usa somente a data da própria epígrafe. A resposta HTTP é
preservada por SHA antes de qualquer extração; o processador reutiliza os bytes
capturados, sem fazer uma segunda requisição. Bloqueios interrompem o lote.
"""
import argparse
import collections
import datetime as dt
import fcntl
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.request
from unittest.mock import patch
from zoneinfo import ZoneInfo

import pe
from comum import UA, caminhos, decodificar, html_para_md
from datas import data_do_texto


def agora():
    return dt.datetime.now(ZoneInfo('America/Recife')).isoformat()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def numero_indice(item):
    m = re.search(r'n[°º]\s*([\d.]+(?:-[A-Za-z]+)?)\b', item['nome'], re.I)
    if not m:
        raise ValueError('número do índice não comprovado')
    return m[1].replace('.', '').upper()


def identidade_primaria(item, pagina):
    """Não usa data de publicação, ementa ou normas citadas para escolher ano."""
    numero = numero_indice(item)
    campo = pe.texto_html(pagina)
    texto = html_para_md(campo)
    linhas = [ln.strip() for ln in texto.splitlines() if ln.strip() and not ln.startswith(('#', '>'))][:6]
    tipos = {'4': r'RESOLU[ÇC][ÃA]O', '5': r'DECRETO\s+LEGISLATIVO',
             '8': r'PORTARIA(?:\s+ADMINISTRATIVA)?'}
    flex = r'0*' + r'\.?'.join(map(re.escape, numero))
    ep = re.compile(r'^\s*\*{0,2}\s*' + tipos[item['tipo']] + r'\s+N[º°o.\s]*' + flex + r'\b', re.I)
    proprias = [ln for ln in linhas if ep.search(ln)]
    data = data_do_texto('\n'.join(proprias), numero=numero)
    if not data or dt.date.fromisoformat(data) > dt.datetime.now(ZoneInfo('America/Recife')).date():
        raise ValueError('tipo/número/data da epígrafe própria não comprovados')
    return numero, data, proprias[0]


def existentes(raiz):
    ids, chaves = {}, {}
    for base, dirs, files in os.walk(raiz / 'estaduais/PE'):
        dirs[:] = [d for d in dirs if not d.startswith('_')]
        for nome in files:
            m = re.search(r'-id(\d+)\.md$', nome)
            if not m:
                continue
            p = Path(base) / nome
            ids.setdefault(m[1], []).append(str(p.relative_to(raiz)))
            rel = p.relative_to(raiz).parts
            n = re.match(r'(?:res|dl|port)-(.+)-(\d{4})-id\d+\.md$', nome)
            if n:
                chaves.setdefault((rel[2], n[1].replace('.', '').upper(), n[2]), []).append(str(p.relative_to(raiz)))
    return ids, chaves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--indice', required=True)
    parser.add_argument('--lote', required=True)
    parser.add_argument('--limite', type=int, default=2000)
    parser.add_argument('--anterior', action='append', default=[])
    args = parser.parse_args()
    if not re.fullmatch(r'\d{8}-\d{3}', args.lote) or not 1 <= args.limite <= 2000:
        parser.error('lote AAAAMMDD-NNN; limite entre 1 e 2000')
    raiz = Path(__file__).resolve().parents[2]
    lock = (raiz / 'estaduais/PE/_indice/retomada-lacunas-20261020.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    ids, chaves = existentes(raiz)
    anteriores = set()
    for p in args.anterior:
        anteriores.update(r['id'] for r in json.loads(Path(p).read_text())['itens'])
    indice = Path(args.indice)
    itens = json.loads(indice.read_text())
    assert len({it['id'] for it in itens}) == len(itens)
    assert all(it['tipo'] in ('4', '5', '8') for it in itens)
    itens.sort(key=lambda it: ({'8': 0, '5': 1, '4': 2}[it['tipo']], -int(it['id'])))
    selecionados = [it for it in itens if it['id'] not in ids and it['id'] not in anteriores][:args.limite]
    nome = 'pe-infralegal-coleta-' + args.lote
    selecao = raiz / 'scripts/estados/manifestos' / (nome + '-selecao.json')
    log = raiz / 'estaduais/PE/_fonte/auditorias/infralegal' / (nome + '.jsonl')
    manifest = selecao.with_name(nome + '.json')
    if selecao.exists() or log.exists() or manifest.exists():
        raise FileExistsError('lote já existe; usar uma nova identificação')
    selecao.write_text(json.dumps(dict(selecionado_em=agora(),indice=str(indice),sha256_indice=sha(indice.read_bytes()),
                                      ids_preexistentes_disco=len(ids),ids_anteriores=len(anteriores),itens=selecionados), ensure_ascii=False, indent=2)+'\n')
    log.parent.mkdir(parents=True, exist_ok=True)
    inicio = agora(); ultimo = 0; falhas = 0; parada = False; contagens = collections.Counter()
    print('INICIO', len(selecionados), 'preexistentes', len(ids), flush=True)
    with log.open('x') as out:
        for i, it in enumerate(selecionados, 1):
            if parada:
                break
            r = dict(iniciado_em=agora(), item_indice=it, id_oficial=it['id'])
            modo = 'TEXTOATUALIZADO' if 'TEXTOATUALIZADO' in it['textos'] else 'TEXTOORIGINAL'
            url = f"{pe.BASE}/texto.aspx?id={it['id']}&tipo={modo}"
            r['url'] = url
            try:
                time.sleep(max(0, 1.1-(time.monotonic()-ultimo))); ultimo = time.monotonic()
                req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html'})
                with urllib.request.urlopen(req, timeout=40) as f:
                    bruto = f.read(); status = f.status; ctype = f.headers.get('Content-Type', '')
                    if f.headers.get('Content-Encoding') == 'gzip':
                        bruto = gzip.decompress(bruto)
                r.update(http=status, bytes=len(bruto), sha256_resposta=sha(bruto), content_type=ctype)
                captura = raiz / 'estaduais/PE/_fonte/respostas' / it['id'] / modo / (sha(bruto)+'.html.gz')
                captura.parent.mkdir(parents=True, exist_ok=True)
                if not captura.exists():
                    with captura.open('xb') as f:
                        f.write(gzip.compress(bruto))
                assert gzip.decompress(captura.read_bytes()) == bruto
                r['captura'] = str(captura.relative_to(raiz))
                falhas = 0
                numero, data, epigrafe = identidade_primaria(it, decodificar(bruto, ctype))
                r.update(numero=numero, data=data, epigrafe_literal=epigrafe)
                ano = data[:4]; folder, _, prefixo = pe.TIPOS[it['tipo']]; chave = (folder, numero, ano)
                if it['id'] in ids or chave in chaves:
                    r.update(status='colisao_retida', paths_existentes=ids.get(it['id'], [])+chaves.get(chave, []))
                else:
                    comano = dict(it, ano=ano)
                    with patch.object(pe.rede, 'get', return_value=(status, bruto, ctype)):
                        result, detalhe = pe.processar(comano)
                    r.update(status=result, detalhe=detalhe)
                    if result == 'ok':
                        md, cache = caminhos('PE', folder, ano, f"{prefixo}-{numero}-{ano}-id{it['id']}")
                        p = Path(md); r.update(path=str(p.relative_to(raiz)), sha256_md=sha(p.read_bytes()), cache=str(Path(cache).relative_to(raiz)))
                        ids[it['id']] = [r['path']]; chaves[chave] = [r['path']]
            except urllib.error.HTTPError as e:
                r.update(status='http_erro', http=e.code, erro=str(e)); falhas += 1
                parada = e.code in (401, 403, 429) or falhas >= 3
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                r.update(status='rede_erro', erro=type(e).__name__+': '+str(e)); falhas += 1
                parada = falhas >= 3
            except (ValueError, AssertionError) as e:
                r.update(status='identidade_ou_fonte_retida', erro=type(e).__name__+': '+str(e))
            r['finalizado_em'] = agora(); contagens[r['status']] += 1
            out.write(json.dumps(r, ensure_ascii=False)+'\n'); out.flush()
            if i % 25 == 0 or parada:
                print('PROGRESSO', i, dict(contagens), 'parada', parada, flush=True)
    manifest.write_text(json.dumps(dict(iniciado_em=inicio, finalizado_em=agora(), total_selecionado=len(selecionados),
                         contagens=dict(contagens), interrompido_para_diagnostico=parada, selecao=str(selecao.relative_to(raiz)),
                         resultado=str(log.relative_to(raiz)), sha256_resultado=sha(log.read_bytes()),
                         criterio='Captura serial com intervalo mínimo 1,1 s, 40 s de timeout, parada em 401/403/429 ou 3 falhas de rede consecutivas. Ano somente da epígrafe própria. IDs/chaves preexistentes e listas anteriores descontados. Captura não implica publicação: íntegra, visuais, tabelas, anexos, tachados, CommonMark e metadados exigem QA separado.'),ensure_ascii=False,indent=2)+'\n')
    print('FINAL', dict(contagens), 'parada', parada, flush=True)


if __name__ == '__main__':
    main()
