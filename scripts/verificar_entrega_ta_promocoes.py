"""Confere artefatos, preimagens e replays TA; nunca promove candidatos."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def verificar(manifest, replay=False, exigir_promocao=False):
    errors = []
    for r in manifest['arquivos']:
        p = Path(r['arquivo'])
        if not p.is_file() or sha(p.read_bytes()) != r['sha256'] or p.stat().st_size != r['bytes']:
            errors.append(dict(arquivo=str(p),erro='Presença, hash ou bytes divergem'))
    mappings = json.loads(Path(manifest['mapeamento_fontes']).read_text())
    norms = Path(manifest['normas_apos_promocao']).read_text().splitlines()
    if len(norms) != manifest['normas'] or len(set(norms)) != len(norms) or len(mappings) != len(norms) or {r['destino'] for r in mappings} != set(norms):
        errors.append(dict(erro='Lista, mapeamento ou cardinalidade divergente'))
    results = []
    promoted = pending = 0
    if replay:
        from auditar_commonmark_ta_v2 import comparar
        from auditar_municipal import metadados
    for r in mappings:
        item = dict(destino=r['destino'],aprovado=False)
        try:
            target = Path(r['destino'])
            current = sha(target.read_bytes())
            if r.get('candidato'):
                if current == r['sha256']:
                    selected = target
                    promoted += 1
                    item['promocao'] = 'promovido'
                elif current == r['sha256_anterior']:
                    selected = Path(r['candidato'])
                    pending += 1
                    item['promocao'] = 'pendente; usar candidato privado somente para revisão'
                    if exigir_promocao:
                        raise ValueError('Promoção ainda pendente')
                else:
                    raise ValueError('Destino não corresponde à preimagem ou ao candidato aprovado')
            else:
                selected = target
                item['promocao'] = 'norma direta'
            raw = selected.read_bytes()
            if sha(raw) != r['sha256']:
                raise ValueError('SHA do texto selecionado diverge')
            if replay:
                source = Path(r['fonte']['arquivo']).read_bytes()
                if sha(source) != r['fonte']['sha256']:
                    raise ValueError('SHA da fonte diverge')
                text = raw.decode()
                body = text.split('\n---\n',1)[1].lstrip('\n').split('\n\n',1)[1]
                if not body.endswith('\n'):
                    raise ValueError('EOF não corresponde à transcrição entregue')
                body = body[:-1]
                if sha(body.encode()) != metadados(text)['sha256_texto']:
                    raise ValueError('SHA do corpo diverge')
                item.update(comparar(source.decode(),body))
                if not item['aprovado']:
                    raise ValueError('Replay independente não confere')
        except Exception as e:
            item['erro'] = type(e).__name__+': '+str(e)
            errors.append(dict(destino=r['destino'],erro=item['erro']))
        results.append(item)
    ready = not errors and replay and len(results)==manifest['normas'] and all(r['aprovado'] for r in results)
    return dict(arquivos_verificados=len(manifest['arquivos']),normas=manifest['normas'],
        replays_aprovados=sum(r['aprovado'] for r in results),promocoes_concluidas=promoted,promocoes_pendentes=pending,
        problemas=len(errors),detalhes=errors,resultados=results,preparacao_aprovada=ready,
        apto_para_publicacao=ready and pending==0)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--manifesto',type=Path,required=True)
    ap.add_argument('--saida',type=Path,required=True)
    ap.add_argument('--replay',action='store_true')
    ap.add_argument('--exigir-promocao',action='store_true')
    a=ap.parse_args()
    result=verificar(json.loads(a.manifesto.read_text()),a.replay,a.exigir_promocao)
    with a.saida.open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({k:result[k] for k in ('arquivos_verificados','normas','replays_aprovados','promocoes_concluidas','promocoes_pendentes','problemas','preparacao_aprovada','apto_para_publicacao')}))
    return int(bool(result['problemas']))


if __name__=='__main__':raise SystemExit(main())
