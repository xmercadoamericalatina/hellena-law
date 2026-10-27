"""Confere hashes e replay de seleção TA agregada, sem promover nem editar normas."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--manifesto', type=Path, required=True)
    ap.add_argument('--saida', type=Path, required=True)
    ap.add_argument('--replay', action='store_true')
    ap.add_argument('--exigir-promocao', action='store_true')
    a = ap.parse_args()
    manifest = json.loads(a.manifesto.read_text())
    errors = []
    for row in manifest['arquivos']:
        p = Path(row['arquivo'])
        if not p.is_file():
            errors.append(dict(arquivo=str(p), erro='Arquivo ausente'))
        elif sha(p.read_bytes()) != row['sha256'] or p.stat().st_size != row['bytes']:
            errors.append(dict(arquivo=str(p), erro='Hash ou tamanho diverge'))
    promotion = json.loads(Path(manifest['promocao']).read_text())
    current = sha(Path(promotion['destino']).read_bytes())
    state = ('promovido' if current == promotion['sha256_candidato'] else
             'aguarda_promocao_explicita' if current == promotion['sha256_preimagem'] else 'preimagem_divergente')
    if state == 'preimagem_divergente' or (a.exigir_promocao and state != 'promovido'):
        errors.append(dict(arquivo=promotion['destino'], erro=state))
    replay = []
    if a.replay:
        from auditar_commonmark_ta_v2 import comparar
        from auditar_municipal import metadados
        for row in json.loads(Path(manifest['mapeamento_fontes']).read_text()):
            raw = Path(row['arquivo_leitura']).read_bytes()
            source = Path(row['fonte']['arquivo']).read_bytes()
            result = dict(path=row['destino'], aprovado=False)
            try:
                if sha(raw) != row['sha256'] or sha(source) != row['fonte']['sha256']:
                    raise ValueError('Corpo ou fonte diverge')
                text = raw.decode()
                body = text.split('\n---\n', 1)[1].lstrip('\n').split('\n\n', 1)[1][:-1]
                if sha(body.encode()) != metadados(text)['sha256_texto']:
                    raise ValueError('Hash do corpo diverge do metadado')
                result.update(comparar(source.decode(), body))
            except Exception as e:
                result['erro'] = type(e).__name__ + ': ' + str(e)
            if not result['aprovado']:
                errors.append(dict(arquivo=row['destino'], erro='Replay diverge', detalhe=result))
            replay.append(result)
    result = dict(arquivos_verificados=len(manifest['arquivos']), normas_previstas=771,
                  promocao=state, replay=len(replay), replay_aprovados=sum(r['aprovado'] for r in replay),
                  problemas=len(errors), detalhes=errors, resultados_replay=replay,
                  apto_para_publicacao=not errors and state == 'promovido')
    with a.saida.open('x') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps({k: result[k] for k in ('arquivos_verificados', 'promocao', 'replay', 'replay_aprovados', 'problemas', 'apto_para_publicacao')}))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
