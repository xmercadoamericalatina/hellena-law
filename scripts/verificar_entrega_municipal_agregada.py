"""Hashes e replays independentes de seleção TA e LO Aracaju explícitas; só leitura."""
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
    ap.add_argument('--manifesto',type=Path,required=True)
    ap.add_argument('--saida',type=Path,required=True)
    ap.add_argument('--replay',action='store_true')
    a = ap.parse_args()
    manifest = json.loads(a.manifesto.read_text())
    errors = []
    for row in manifest['arquivos']:
        p = Path(row['arquivo'])
        if not p.is_file() or sha(p.read_bytes()) != row['sha256'] or p.stat().st_size != row['bytes']:
            errors.append(dict(arquivo=str(p),erro='Hash, tamanho ou presença diverge'))
    mapping = json.loads(Path(manifest['mapeamento_ta']).read_text())
    norms = Path(manifest['lista_normas']).read_text().splitlines()
    ta_paths = [r['path'] for r in mapping]
    pdf_path = 'municipais/SE/aracaju/lei-organica/1990/lei-organica-aracaju-1990.md'
    if len(ta_paths) != manifest['normas_ta'] or len(set(ta_paths)) != len(ta_paths) or len(norms) != manifest['normas'] or set(norms) != set(ta_paths) | {pdf_path}:
        errors.append(dict(erro='Seleção, mapeamento e cardinalidade não conferem'))
    html_results = []
    pdf_result = None
    if a.replay:
        from auditar_commonmark_ta_v2 import comparar
        from auditar_municipal import metadados
        from verificar_replay_organica_aracaju import verificar
        for row in mapping:
            result = dict(path=row['path'],aprovado=False)
            try:
                raw = Path(row['path']).read_bytes()
                source = Path(row['fonte']['arquivo']).read_bytes()
                if sha(raw) != row['sha256'] or sha(source) != row['fonte']['sha256']:
                    raise ValueError('Norma ou fonte diverge')
                text = raw.decode()
                body = text.split('\n---\n',1)[1].lstrip('\n').split('\n\n',1)[1][:-1]
                if sha(body.encode()) != metadados(text)['sha256_texto']:
                    raise ValueError('Hash do corpo diverge')
                result.update(comparar(source.decode(),body))
            except Exception as e:
                result['erro'] = type(e).__name__+': '+str(e)
            html_results.append(result)
            if not result['aprovado']:
                errors.append(dict(arquivo=row['path'],erro='Replay TA diverge',detalhe=result))
        try:
            pdf_result = verificar()
        except Exception as e:
            pdf_result = dict(aprovado=False,erro=type(e).__name__+': '+str(e))
            errors.append(dict(arquivo='LO Aracaju',erro='Replay PDF diverge',detalhe=pdf_result))
    result = dict(arquivos_verificados=len(manifest['arquivos']),normas=manifest['normas'],
                  replay_ta=len(html_results),replay_ta_aprovados=sum(r['aprovado'] for r in html_results),
                  replay_aracaju=pdf_result,problemas=len(errors),detalhes=errors,resultados_ta=html_results,
                  apto_para_publicacao=not errors and a.replay and len(html_results)==manifest['normas_ta'] and bool(pdf_result and pdf_result['aprovado']))
    with a.saida.open('x') as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({k:result[k] for k in ('arquivos_verificados','normas','replay_ta','replay_ta_aprovados','problemas','apto_para_publicacao')}))
    return int(bool(errors))


if __name__=='__main__':
    raise SystemExit(main())
