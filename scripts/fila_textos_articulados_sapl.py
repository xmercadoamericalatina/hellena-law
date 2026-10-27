"""Fila de captura TA pública: uma passagem por portal SIGI, sem publicar normas.

Valida a Casa contra o vínculo SIGI antes de buscar corpos; reaproveita snapshots,
limita a 1 rps por host e registra indisponibilidades sem contornar bloqueios.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import datetime as dt
import fcntl
import hashlib
import json
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo
sys.path.insert(0, str(Path(__file__).resolve().parent))
import baixar_organicas_sapl as organicas
import baixar_textos_articulados_sapl_v2 as coletor
from comum import normalizar_chave
ROOT = Path(__file__).resolve().parent.parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def agora():
    return dt.datetime.now(ZoneInfo('America/Recife')).isoformat()


def candidatos(rows, iniciados):
    grouped = {}
    for r in rows:
        u = urlsplit(r['url'] if '://' in r['url'] else 'https://' + r['url'])
        host = u.hostname
        if not host or u.path.strip('/') or not re.fullmatch(r'[a-z0-9.-]+\.leg\.br', host):
            continue
        grouped.setdefault(host, []).append(r)
    result = []
    for host, rs in sorted(grouped.items()):
        identities = {(str(r.get('codigo_ibge')), normalizar_chave(r['municipio']), r['uf']) for r in rs}
        if host not in iniciados and len(identities) == 1:
            result.append(dict(rs[0], host=host))
    return result


def validar_casa(data, item):
    rows = data.get('results', [])
    if len(rows) != 1:
        raise ValueError('Casa oficial ausente ou ambígua')
    casa = rows[0]
    if normalizar_chave(casa.get('municipio', '')) != normalizar_chave(item['municipio']) or casa.get('uf') != item['uf']:
        raise ValueError('Casa não corresponde ao município/UF do vínculo SIGI')
    ibge = json.loads((ROOT / 'municipais/_indice/ibge-municipios.json').read_text())
    matches = [r for r in ibge if str(r['id']) == str(item['codigo_ibge'])]
    if len(matches) != 1 or normalizar_chave(matches[0]['nome']) != normalizar_chave(item['municipio']) or matches[0]['regiao-imediata']['regiao-intermediaria']['UF']['sigla'] != item['uf']:
        raise ValueError('Vínculo SIGI/IBGE divergente')
    return casa


def prevalidar(item):
    host = item['host']
    url = 'https://' + host + '/api/base/casalegislativa/'
    cache = ROOT / 'municipais/_fonte/texto-articulado-sapl' / host
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / (sha(url.encode()) + '.json')
    meta = path.with_suffix('.meta.json')
    rede = organicas.rede_host(host, 1)
    if path.exists() and meta.exists():
        b, info = path.read_bytes(), json.loads(meta.read_text())
        if sha(b) != info['sha256'] or info['url'] != url:
            raise ValueError('Preimagem de cache inválida')
    elif path.exists() or meta.exists():
        raise ValueError('Cache incompleto exige revisão; não sobrescrever')
    else:
        rede.limite.esperar()
        req = urllib.request.Request(url, headers={**rede.headers, 'Accept-Encoding': 'identity'})
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                b = response.read()
                info = dict(url=url, url_final=response.geturl(), status=response.status,
                            content_type=response.headers.get('Content-Type', ''))
        except urllib.error.HTTPError as e:
            b = b''
            info = dict(url=url, url_final=url, status=e.code, content_type='')
        info.update(sha256=sha(b), bytes=len(b), capturado_em=agora())
        path.write_bytes(b)
        meta.write_text(json.dumps(info, ensure_ascii=False, indent=2))
    if info['status'] != 200:
        raise ValueError('Casa indisponível HTTP ' + str(info['status']) + '; não repetir automaticamente')
    if urlsplit(info['url_final']).hostname != host:
        raise ValueError('Casa redireciona para outro host; exige vínculo oficial próprio')
    validar_casa(json.loads(b), item)
    return dict(arquivo=str(path.relative_to(ROOT)), sha256=sha(b), metadata=str(meta.relative_to(ROOT)), sha256_metadata=sha(meta.read_bytes()))


def executar(item, saida, reference, fingerprint):
    host = item['host']
    record = dict(host=host, vinculo_sigi=item, inicio=agora())
    try:
        if sha(Path(coletor.__file__).read_bytes()) != fingerprint:
            raise ValueError('Coletor congelado mudou durante a fila')
        record['prova_casa'] = prevalidar(item)
        coletor.executar(host, saida / host, reference)
        manifest = saida / host / 'manifesto.json'
        record.update(estado='captura concluída; candidatos ainda exigem todos os gates', manifesto=str(manifest.relative_to(ROOT)), sha256_manifesto=sha(manifest.read_bytes()))
    except Exception as e:
        record.update(estado='retido; execução parcial ou fonte indisponível', erro=type(e).__name__ + ': ' + str(e))
    finally:
        # A função original retém a trava até sair do processo. Nesta fila serial
        # por host, libere ao terminar para não bloquear a outra fila municipal.
        organicas.REDES_HOST.pop(host, None)
        lock = organicas.TRAVAS_HOST.pop(host, None)
        if lock:
            lock.close()
    record['fim'] = agora()
    return record


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--catalogo', type=Path, default=ROOT / 'municipais/_indice/organicas-sapl/sigi/catalogo.json')
    ap.add_argument('--saida', type=Path, required=True)
    ap.add_argument('--trabalhadores', type=int, choices=(1, 2), default=2)
    ap.add_argument('--referencia', type=dt.date.fromisoformat, default=dt.datetime.now(ZoneInfo('America/Recife')).date())
    a = ap.parse_args()
    a.saida = a.saida.resolve()
    a.saida.mkdir(parents=True, exist_ok=True)
    lock = (ROOT / 'municipais/_indice/organicas-sapl/fila-ta.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    checkpoint = a.saida / 'fila.json'
    state = json.loads(checkpoint.read_text()) if checkpoint.exists() else {}
    # Qualquer tentativa anterior é excluída, incluindo execuções parciais e
    # portais vivos em outras capturas. Revisão manual decide eventual retomada.
    iniciados = set(state) | {p.name for p in (ROOT / 'municipais/_fonte/texto-articulado-sapl').iterdir() if p.is_dir()}
    rows = candidatos(json.loads(a.catalogo.read_text())['candidatos_sapl'], iniciados)
    fingerprint = sha(Path(coletor.__file__).read_bytes())
    snapshot = a.saida / ('selecao-' + agora().replace(':', '-') + '.json')
    snapshot.write_text(json.dumps(dict(catalogo=str(a.catalogo.relative_to(ROOT)), sha256_catalogo=sha(a.catalogo.read_bytes()),
        codigo_sha256=sha(Path(__file__).read_bytes()), coletor_sha256=fingerprint, excluidos_iniciados=sorted(iniciados),
        candidatos=rows, criterio=__doc__), ensure_ascii=False, indent=2))

    def save():
        temp = checkpoint.with_suffix('.temporario')
        temp.write_text(json.dumps(state, ensure_ascii=False, indent=2))
        temp.replace(checkpoint)

    pending = iter(rows)
    with ThreadPoolExecutor(max_workers=a.trabalhadores) as pool:
        active = {}
        while True:
            while len(active) < a.trabalhadores:
                item = next(pending, None)
                if item is None:
                    break
                host = item['host']
                state[host] = dict(estado='iniciado; não repetir automaticamente', inicio=agora(), vinculo_sigi=item)
                save()
                active[pool.submit(executar, item, a.saida, a.referencia, fingerprint)] = host
            if not active:
                break
            done, _ = wait(active, timeout=30, return_when=FIRST_COMPLETED)
            for future in done:
                host = active.pop(future)
                state[host] = future.result()
                save()
                print(json.dumps(state[host], ensure_ascii=False), flush=True)
    print(json.dumps(dict(estado='fila de descoberta percorrida; não certifica cobertura ou publicação', portais_nesta_selecao=len(rows)), ensure_ascii=False))


if __name__ == '__main__':
    main()
