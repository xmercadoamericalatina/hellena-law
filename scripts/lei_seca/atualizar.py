#!/usr/bin/env python3
"""Orquestra atualizações verificáveis. Sem dependências ou execução de código baixado."""
import argparse
import datetime as dt
import json
from pathlib import Path
import sys
import time

# -I impede importação do diretório de trabalho/PYTHONPATH; só este pacote é incluído.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import Network, allowed_kind, archive, now, publish, read_json, write_json
from coletar import discover_portal, discover_sapl, discover_senate, resolve_direct, resolve_senate
from auditar import audit


def enqueue(state, entries):
    queue = state.setdefault('fila', {})
    for entry in entries:
        if not allowed_kind(entry['tipo']):
            raise ValueError('Tipo proibido: ' + entry['tipo'])
        previous = queue.get(entry['id'], {})
        queue[entry['id']] = {**previous, 'entrada': entry}


def run(args, net=None):
    root = args.output.resolve()
    config = read_json(args.config)
    state = read_json(root / 'estado.json', {'schema': 1, 'fila': {}})
    if state.get('schema') != 1:
        raise ValueError('Estado com schema incompatível')
    net = net or Network()
    events, started = [], time.monotonic()
    deadline = started + args.seconds
    enqueue(state, config['prioridades'])
    if args.mode == 'completo':
        entries, discovery_events = discover_senate(net, state, args.indices, args.historic)
        enqueue(state, entries)
        events.extend(discovery_events)
        for source in config['indices_oficiais']:
            if time.monotonic() >= deadline:
                break
            try:
                entries = discover_portal(net, source)
                if not entries:
                    raise ValueError('Índice sem links de normas reconhecidos; verificar mudança de layout')
                enqueue(state, entries)
                events.append({'fonte': source['url'], 'status': 'ok', 'encontrados': len(entries)})
            except Exception as exc:
                events.append({'fonte': source['url'], 'status': 'erro', 'erro': str(exc)})
        for source in config['sapl']:
            if not source.get('habilitado', True) or time.monotonic() >= deadline:
                continue
            try:
                entries = discover_sapl(net, source, state)
                enqueue(state, entries)
                events.append({'fonte': source['url'], 'status': 'ok', 'encontrados': len(entries)})
            except Exception as exc:
                events.append({'fonte': source['url'], 'status': 'erro', 'erro': str(exc)})
    write_json(root / 'estado.json', state)
    # Prioridades têm rechecagem diária; demais, 30 dias. Falhas têm retry em 24h.
    due = []
    current = dt.datetime.now(dt.timezone.utc)
    for ident, record in state['fila'].items():
        if args.mode == 'prioridades' and not record['entrada'].get('prioridade'):
            continue
        checked = record.get('tentado_em')
        age = (current - dt.datetime.fromisoformat(checked)).total_seconds() if checked else float('inf')
        interval = 86400 if record['entrada'].get('prioridade') or record.get('status') == 'pendente' else args.refresh_days * 86400
        if not args.force and age < interval:
            continue
        due.append((ident, record))
    due.sort(key=lambda item: (not item[1]['entrada'].get('prioridade', False),
                               item[1].get('tentado_em', ''), item[0]))
    done = 0
    for ident, record in due:
        if done >= args.limit or time.monotonic() >= deadline:
            break
        entry = record['entrada']
        if args.mode == 'prioridades' and not entry.get('prioridade'):
            continue
        record['tentado_em'] = now()
        try:
            resolver = resolve_senate if entry['conector'] == 'senado' else resolve_direct
            resolved, data, ct, url = resolver(net, entry)
            # Preservar originais inclusive quando a conversão é recusada.
            original, sha = archive(root, data)
            record.update({'original': original, 'sha256_original': sha})
            record.update(publish(root, resolved, data, ct, url))
            record.pop('erro', None)
            events.append({'id': ident, 'status': 'ok', 'alterado': record['alterado']})
        except Exception as exc:
            record.update({'status': 'pendente', 'erro': str(exc)})
            events.append({'id': ident, 'status': 'erro', 'erro': str(exc)})
        done += 1
        # Checkpoint após cada documento: interrupção não perde o avanço.
        write_json(root / 'estado.json', state)
    report = {'executado_em': now(), 'modo': args.mode, 'processados': done,
              'fila_total': len(state['fila']), 'eventos': events,
              'limite_atingido': done >= args.limit or time.monotonic() >= deadline,
              'aviso': 'Volume não comprova cobertura nacional nem vigência. Não contém jurisprudência.'}
    write_json(root / 'ultima_execucao.json', report)
    manifest = []
    for path in sorted((root / 'metadados').glob('*.json')):
        m = read_json(path)
        record = state['fila'].get(m['id'], {})
        manifest.append({'id': m['id'], 'tipo': m['tipo'], 'titulo': m['titulo'],
                         'fonte': m['url_texto'], 'conferido_em': m['conferido_em'],
                         'sha256_texto': m['sha256_texto'],
                         'integralidade': m['integralidade'],
                         'atualizacao': record.get('status', 'desconhecida'),
                         'erro_ultima_tentativa': record.get('erro'),
                         'texto': 'textos/' + m['id'] + '.md'})
    write_json(root / 'indice.json', manifest)
    pending = [{'id': ident, 'fonte': r['entrada'].get('fonte', r['entrada'].get('url')),
                'status': r.get('status', 'aguardando_coleta'), 'erro': r.get('erro')}
               for ident, r in sorted(state['fila'].items()) if r.get('status') != 'publicado']
    write_json(root / 'pendencias.json', pending)
    coverage = {'atualizado_em': now(), 'publicados': len(manifest), 'pendentes_ou_aguardando': len(pending),
                'universo_nacional': 'desconhecido; não se declara completo',
                'federal': 'Senado: séries legislativas desde 1808, com cursores por tipo/ano e revisita; universo limitado ao serviço oficial',
                'fontes_sapl': [{k: s[k] for k in ('id', 'url', 'esfera', 'uf')} for s in config['sapl'] if s.get('habilitado', True)],
                'lacunas': config['lacunas'], 'jurisprudencia': 'excluída',
                'integralidade_textual': 'não certificada; PDFs sem validação ficam pendentes'}
    write_json(root / 'cobertura.json', coverage)
    errors = audit(root)
    if errors:
        raise ValueError('Auditoria falhou: ' + '; '.join(errors[:10]))
    print(json.dumps({'processados': done, 'publicados': len(manifest), 'pendentes': len(pending),
                      'erros_execucao': sum(e['status'] == 'erro' for e in events)}, ensure_ascii=False))
    return int(any(e['status'] == 'erro' for e in events))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--config', type=Path, default=Path(__file__).with_name('fontes.json'))
    ap.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[2] / 'lei-seca')
    ap.add_argument('--mode', choices=['completo', 'prioridades'], default='completo')
    ap.add_argument('--limit', type=int, default=150)
    ap.add_argument('--indices', type=int, default=6)
    ap.add_argument('--historic', type=int, default=2)
    ap.add_argument('--seconds', type=int, default=2400)
    ap.add_argument('--refresh-days', type=int, default=30)
    ap.add_argument('--force', action='store_true')
    args = ap.parse_args()
    if min(args.limit, args.indices, args.seconds, args.refresh_days) <= 0 or args.historic < 0:
        ap.error('Limites devem ser positivos; histórico pode ser zero')
    return run(args)


if __name__ == '__main__':
    sys.exit(main())
