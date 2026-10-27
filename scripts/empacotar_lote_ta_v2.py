"""Congela seleção final TA e provas explícitas sem promover retidos ou consultar rede/Git."""
import argparse
import hashlib
import json
from pathlib import Path


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def dump(p, x):
    with Path(p).open('x') as f:
        json.dump(x, f, ensure_ascii=False, indent=2)
        f.write('\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--prefixo', required=True, help='Ex.: 20261021-textos-articulados')
    ap.add_argument('--lote', required=True)
    ap.add_argument('--codigo-base', type=Path, required=True)
    ap.add_argument('--saida', type=Path, required=True)
    a = ap.parse_args()
    base = Path('municipais/_lotes')
    dirs = {k: base / (a.prefixo + '-' + k + '-' + a.lote) for k in
            ('selecao', 'gates', 'materializados', 'contexto', 'commonmark', 'jurisdicao')}
    norms = (dirs['jurisdicao'] / 'aprovados.paths.txt').read_text().splitlines()
    assert norms and len(norms) == len(set(norms))
    context = dirs['contexto']
    audit = json.loads((context / 'auditoria-municipal-final.json').read_text())
    assert audit['arquivos'] == len(norms) and not audit['problemas'] and not audit['avisos']
    assert not json.loads((context / 'formato.json').read_text())['problemas']
    collision = json.loads((context / 'colisoes-globais.json').read_text())
    assert collision['candidatos'] == len(norms) and not collision['colisoes']
    verification = json.loads((context / 'verificacao-integral.json').read_text())
    assert not verification['problemas']
    for kind in ('contexto', 'commonmark'):
        assert set(norms) <= set((dirs[kind] / 'aprovados.paths.txt').read_text().splitlines())
    jurisdiction = json.loads((dirs['jurisdicao'] / 'controle.json').read_text())
    by_path = {r['path']: r for r in jurisdiction['resultados']}
    for p in norms:
        r = by_path[p]
        assert not r['alertas'] and r['esfera_federacao_api'] == 'M' and sha(p) == r['sha256']
    rows = [json.loads(t) for t in (dirs['materializados'] / 'resultados.jsonl').read_text().splitlines()]
    selected = [r for r in rows if r.get('path') in set(norms)]
    assert len(selected) == len(norms)
    source_files = set()

    def proof(r):
        p = Path(r['arquivo'])
        assert p.is_file() and (not r.get('sha256') or sha(p) == r['sha256']), str(p)
        source_files.add(str(p))
        meta = Path(r.get('metadata') or p.with_suffix('.meta.json'))
        assert meta.is_file(), str(meta)
        assert not r.get('sha256_metadata') or sha(meta) == r['sha256_metadata']
        source_files.add(str(meta))

    for r in selected:
        assert sha(r['path']) == r['sha256'] and r['gates']['anexos_proprios'] == 0
        for k in ('prova_ta', 'prova_casa', 'prova_norma', 'prova_frontend'):
            proof(r[k])
        source_files.add(r['transcricao'])
    for p in dirs['gates'].glob('*.anexos.json'):
        for r in json.loads(p.read_text()).get('evidencias', []):
            proof(r)
    source_files.update(('municipais/_indice/ibge-municipios.json',
                         'municipais/_fonte/capitais/fortaleza/compilacao.0baf3580.css',
                         'municipais/_fonte/capitais/fortaleza/compilacao.148cb66b.js'))
    files = source_files | set(norms)
    for folder in dirs.values():
        files.update(str(p) for p in folder.iterdir() if p.is_file())
    code = a.codigo_base.read_text().splitlines()
    code.append(str(Path(__file__).relative_to(Path.cwd())))
    files.update(code)
    a.saida.mkdir(exist_ok=False)
    (a.saida / 'normas.paths.txt').write_text('\n'.join(norms) + '\n')
    (a.saida / 'codigo.paths.txt').write_text('\n'.join(sorted(set(code))) + '\n')
    dump(a.saida / 'mapeamento-fontes.json', selected)
    candidates = json.loads((dirs['selecao'] / 'snapshot.json').read_text())['selecionados']
    dump(a.saida / 'retencao.json', dict(candidatos=candidates, aprovados=len(norms),
        retidos=candidates-len(norms), jurisdicao=[r for r in jurisdiction['resultados'] if r['alertas']],
        replay_retidos=(dirs['commonmark'] / 'retidos.paths.txt').read_text().splitlines(),
        criterio='Retidos não integram a lista de normas. Controles conservam os motivos e identidades; não promovidos por contagem ou por comparação da mesma conversão.'))
    dump(a.saida / 'disjuncao.json', dict(comparados=collision['comparados'], candidatos=len(norms),
        colisoes=0, fontes=collision['fontes'], controle=str(context / 'colisoes-globais.json')))
    (a.saida / 'TESTAR.txt').write_text(
        'Replay independente (use diretório de saída novo):\n'
        '/Users/joaodavisn/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I scripts/auditar_commonmark_ta_v2.py'
        f' --lista {a.saida}/normas.paths.txt --materializados {dirs["materializados"]} --saida /tmp/ta{len(norms)}-replay-root\n'
        f'Esperado: {len(norms)} aprovados, 0 retidos.\n'
        'Verifique também todos os SHA/bytes de manifesto.json antes do staging. Não incorporar normas de listas intermediárias.\n')
    files.update(str(p) for p in a.saida.iterdir())
    pathlist = a.saida / 'artefatos.paths.txt'
    # O manifesto contém o SHA da própria lista; a lista não inclui a si mesma.
    pathlist.write_text('\n'.join(sorted(files)) + '\n')
    files.add(str(pathlist))
    records = [dict(arquivo=p, sha256=sha(p), bytes=Path(p).stat().st_size) for p in sorted(files)]
    manifest = dict(normas=len(norms), candidatos_auditados=candidates, retidos=candidates-len(norms),
        criterio='Fonte pública oficial, IBGE, esfera M, epígrafe literal, contexto integral, anexos próprios ausentes conforme índice completo e replay independente CommonMark/GFM preservando pontuação, sinais e numeração efetiva.',
        data_captura='Dia derivado da captura original, com America/Recife para timestamps com offset; ausência de offset declarada sem fingir recaptura.',
        vigencia='Cortes e situação atribuídos à fonte padrão pública. Não certifica atualização ou vigência jurídica integral.',
        validacao=dict(auditoria_municipal=0, replay_retidos=0, colisoes=0, comparados=collision['comparados']),
        arquivos=records, bytes=sum(r['bytes'] for r in records),
        listas=dict(normas=str(a.saida / 'normas.paths.txt'), artefatos=str(pathlist), codigo=str(a.saida / 'codigo.paths.txt')))
    dump(a.saida / 'manifesto.json', manifest)
    print(json.dumps(dict(normas=len(norms), arquivos=len(records), bytes=manifest['bytes'], manifesto=str(a.saida / 'manifesto.json'), sha256=sha(a.saida / 'manifesto.json'))))


if __name__ == '__main__':
    main()
