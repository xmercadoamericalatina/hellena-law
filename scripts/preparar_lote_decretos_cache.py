"""Audita e prepara lotes preexistentes de decretos, sem rede nem operações Git.

Preserva originais antes de reparar metadados/corpos. A lista de entrada é um
snapshot explícito de arquivos ainda não publicados, não um glob de staging.
"""
import argparse
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

sys.path.insert(0, str(Path(__file__).resolve().parent))
import auditar
from integridade_html_federal import Visivel
from integridade_anexos_decreto import anexo_proprio_ausente
import baixar_federal as f
from identidade_decreto import extrair_epigrafe_decreto, numero_normalizado

ROOT = Path(__file__).resolve().parent.parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()



def visible(text, markdown=False):
    if markdown:
        text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    p = Visivel()
    p.feed(text)
    content = re.sub(r'###.*?@@@', '', ''.join(p.data))
    return ''.join(c.lower() for c in content if c.isalnum()), p


def fields(text):
    cab, body = text[4:].split('\n---\n', 1)
    result = {}
    for line in cab.splitlines():
        key, val = line.split(':', 1)
        val = val.strip()
        result[key] = json.loads(val) if val.startswith('"') else val
    return result, cab, body


def preparar(candidates, lote, registro):
    cache = ROOT / 'federal/_fonte/auditorias' / lote
    cache.mkdir(parents=True, exist_ok=False)
    indexed = {str(Path(f.montar(d)['md']).relative_to(ROOT)): d for d in f.carregar_indice('DEC-n')}
    aliases = {(numero_normalizado(r['numero']), r['data']): r['path'] for r in registro}
    result = {'lote': lote, 'criado_em': dt.datetime.now().isoformat(), 'rede': False,
              'origem': 'Arquivos e HTML preexistentes em disco, autoria da coleta não presumida.',
              'publicaveis': [], 'retidos': [],
              'limites': 'Texto integral disponível no HTML cache; não prova anexos externos ausentes da fonte nem vigência atual. Epígrafe inconclusiva não é identidade validada.'}
    for i, path in enumerate(candidates, 1):
        r = {'path': path, 'preexistente': True}
        try:
            d = indexed[path]
            info = f.montar(d)
            sourcepath = Path(info['fonte'])
            raw = (ROOT / path).read_bytes()
            r['sha256_anterior'] = sha(raw)
            backup = cache / (Path(path).name + '.original.md.gz')
            backup.write_bytes(gzip.compress(raw))
            r['backup_original'] = str(backup.relative_to(ROOT))
            previous, cab, oldbody = fields(raw.decode())
            r['sha256_corpo_anterior'] = sha(oldbody.encode())
            alias = aliases.get((numero_normalizado(f.numero_oficial(d)), info['data']))
            if alias:
                raise ValueError('Identidade já publicada em caminho especializado: ' + alias)
            r['revogada_anterior'] = previous.get('revogada')
            if previous.get('versao_texto') not in {'original', 'compilada (texto vigente)'}:
                raise ValueError('Versão intermediária/republicação/retificação: exige obter a norma integral, não só o documento de alteração')
            source = gzip.decompress(sourcepath.read_bytes())
            if source.startswith(b'%PDF'):
                raise ValueError('PDF em cache; exige validação específica')
            html = source.decode('utf8')
            corpo = f.convert(html)
            parcial = f.motivo_texto_parcial_decreto('DEC-n', corpo)
            if parcial:
                raise ValueError(parcial)
            epigrafe = extrair_epigrafe_decreto(corpo)
            if not epigrafe:
                raise ValueError('Epígrafe própria inconclusiva; requer revisão/fonte alternativa')
            if epigrafe['numero'] != numero_normalizado(f.numero_oficial(d)) or epigrafe['data'] != info['data']:
                raise ValueError('Epígrafe própria diverge: ' + json.dumps(epigrafe, ensure_ascii=False))
            if previous.get('urn') != info['urn'] or previous.get('data') != info['data'] or previous.get('numero') != f.numero_oficial(d) or previous.get('tipo') != 'Decreto':
                raise ValueError('Cabeçalho/URN/número/data/tipo diverge do índice oficial')
            sourcevisible, parsedsource = visible(html)
            mdvisible, parsedmd = visible(corpo, markdown=True)
            if sourcevisible != mdvisible:
                raise ValueError('Sequência de todo o texto visível não preservada pela conversão')
            if parsedsource.visual:
                raise ValueError('Fonte contém conteúdo visual não validado: ' + str(parsedsource.visual))
            ausente = anexo_proprio_ausente(corpo, parsedsource)
            if ausente:
                raise ValueError('Anexo próprio ausente: ' + json.dumps(ausente, ensure_ascii=False))
            if parsedsource.structure != parsedmd.structure:
                raise ValueError('Estrutura de tabela não preservada')
            cab = re.sub(r'^revogada:.*$', 'revogada: null', cab, flags=re.M)
            newbody = '\n# ' + previous['titulo'] + '\n\n' + corpo
            text = '---\n' + cab + '\n---\n' + newbody
            errors, alerts = auditar.validar(text, path, dt.date.today())
            if errors or alerts:
                raise ValueError('Auditoria: ' + str((errors, alerts)))
            if text.encode() != raw:
                (ROOT / path).write_text(text)
            r.update({'urn': info['urn'], 'fonte': previous['fonte'], 'fonte_html_cache': str(sourcepath.relative_to(ROOT)),
                      'sha256_fonte_html': sha(source), 'sha256': sha(text.encode()),
                      'sha256_corpo': sha(newbody.encode()), 'epigrafe': epigrafe,
                      'revogada': None, 'fundamento_vigencia': 'Sem captura imutável de metadados associada à obtenção original; valor legado preservado no backup, sem inferir vigência.',
                      'corpo_reextraido': newbody != oldbody, 'checks': {'formato_datas': True, 'indice_urn_numero_data_tipo': True, 'epigrafe_numero_data': True,
                      'texto_visivel_integral': True, 'estrutura_tabelas': True, 'sem_conteudo_visual': True, 'sem_alias_publicado': True},
                      'tabelas': sum(t[0] == 'table' for t in parsedsource.structure)})
            result['publicaveis'].append(r)
        except Exception as e:
            r['motivo'] = str(e)
            result['retidos'].append(r)
        if i % 100 == 0:
            print(lote, i, 'publicaveis', len(result['publicaveis']), 'retidos', len(result['retidos']), flush=True)
            (cache / 'checkpoint.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    result['resumo'] = {'candidatos_preexistentes': len(candidates), 'publicaveis': len(result['publicaveis']), 'retidos': len(result['retidos']),
                        'novos_downloads': 0, 'tabelas_preservadas': sum(r['tabelas'] for r in result['publicaveis'])}
    result['equacao'] = f"{len(candidates)} candidatos = {len(result['publicaveis'])} publicáveis + {len(result['retidos'])} retidos"
    result['retidos_preservados'] = 'Não removidos nem reescritos; fora da lista de publicação. Backups imutáveis preservam todos os candidatos.'
    manifest = ROOT / 'federal' / ('_' + lote + '.json')
    manifest.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    lista = Path('/tmp') / (lote + '-publicar-paths.txt')
    lista.write_text('\n'.join(r['path'] for r in result['publicaveis']) + '\n' + str(manifest.relative_to(ROOT)) + '\n')
    (cache / 'resultado.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print('FIM', result['resumo'], 'manifesto', manifest, 'lista', lista, flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--entrada', required=True)
    ap.add_argument('--lote', required=True)
    ap.add_argument('--registro-identidades', required=True, help='JSON de identidades publicadas em caminhos especializados sem URN')
    ap.add_argument('--inicio', type=int, default=0)
    ap.add_argument('--limite', type=int, default=1000)
    args = ap.parse_args()
    paths = json.loads(Path(args.entrada).read_text())
    paths.sort(key=lambda p: (p.rsplit('-', 3)[-3:]), reverse=True)
    preparar(paths[args.inicio:args.inicio + args.limite], args.lote, json.loads(Path(args.registro_identidades).read_text()))


if __name__ == '__main__':
    main()
