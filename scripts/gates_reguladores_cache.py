"""Gates suplementares de lotes DOU/SIJUT já auditados, sem rede ou reescrita.

Não certifica vigência. Retém dúvidas de identidade, remissões e objetos para
revisão contextual; uma retenção não afirma ausência definitiva na publicação.
"""
import argparse
from collections import defaultdict
import gzip
import hashlib
import html
import json
from pathlib import Path
import re

from auditar_cache_dou import meta_corpo
from auditar_cache_rfb import pendencia_visual
from comum import normalizar_chave
from metadados_lotes import carregar

ROOT = Path(__file__).resolve().parent.parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def chave(meta, path):
    data = str(meta.get('data', ''))
    numero = re.sub(r'[.\s]', '', str(meta.get('numero', '')).lower()).lstrip('0')
    if data:
        numero = re.sub('/' + re.escape(data[:4]) + '$', '', numero)
    return (path.split('/')[1], normalizar_chave(str(meta.get('tipo', ''))), numero, data)


def origem(registro):
    # O DOU também publica atos da Receita em reguladores/rfb/. A pasta do
    # órgão não identifica o formato da fonte nem autoriza json.loads(HTML).
    if registro.get('fonte_api') and registro['cache'].endswith('.json.gz'):
        return 'rfb'
    if registro.get('sha256_html') and registro['cache'].endswith('.html.gz'):
        return 'dou'
    raise ValueError('origem/formato do registro não comprovado')


def motivos_identidade(meta, path, keys, urls, tracked):
    k = chave(meta, path)
    if not all(k):
        return [{'motivo': 'identidade numérica incompleta exige qualificação pela epígrafe'}]
    if path in tracked or meta['fonte'] in urls or keys.get(k):
        return [{'motivo': 'identidade/URL/path coincidente; revisar subunidades', 'coincidencias': keys.get(k, [])}]
    return []


def motivos_conteudo(body):
    n = normalizar_chave(body)
    reasons = []
    for match in re.finditer(r'anex\w*|manual\w*|monografia\w*|tabela\w*|leiaute\w*|plano\w*', n):
        ctx = n[max(0, match.start() - 180):match.end() + 240]
        if re.search(r'disponibil|sitio|portal|endereco eletronico|publicad\w* no boletim|nao transcrit|nao reproduz|constam no|consta no', ctx):
            reasons.append({'motivo': 'remissão externa exige contexto', 'trecho': ctx})
    for pat in [r'nao (?:transcrit\w*|reproduzid\w*)', r'anex\w* const\w* (?:no|do) (?:dodf|diario|boletim)',
                r'omitid\w* por impossibilidade', r'publicad\w* na integra (?:no|em)']:
        m = re.search(pat, n)
        if m:
            reasons.append({'motivo': 'aviso literal exige contexto', 'trecho': n[max(0, m.start() - 180):m.end() + 240]})
    own = re.search(r'anex\w* (?:a est[ae]|dest[ae]|que (?:integra|acompanha))|(?:na forma|nos termos|conforme) d[oa] anex\w*|aprov\w*.{0,100}anex\w*', n)
    headings = list(re.finditer(r'(?im)^\s*(?:#{1,6}\s*)?(?:\*\*)?anex(?:o|os)\b[^\n]{0,160}$', body))
    if own and not headings:
        reasons.append({'motivo': 'remissão potencialmente própria sem título de anexo', 'trecho': n[max(0, own.start() - 150):own.end() + 200]})
    if headings and len(body[headings[-1].end():].strip()) < 80:
        reasons.append({'motivo': 'último título de anexo sem conteúdo substancial'})
    text = html.unescape(re.sub('<[^>]+>', ' ', body))
    start = re.search(r'\bArt(?:igo)?\.?\s*\*{0,2}\s*1[ºo°.]?\b|\bI\s*[-–.]', text, re.I)
    if start:
        window = text[start.start():start.start() + 2500]
        end = re.search(r'\bArt(?:igo)?\.?\s*\*{0,2}\s*2[ºo°.]?\b', window, re.I)
        if end:
            window = window[:end.start()]
        approval = re.search(r'\baprova(?:r|m|d[oa]s?)?\b[\s\S]{0,190}?\b(documento|manual|plano|programa|regulamento|regimento|estatuto|projeto|quadro|tabela|c[oó]digo|conv[eê]nio|acordo|termo)\b', window, re.I)
        if approval:
            reasons.append({'motivo': 'objeto aprovado no dispositivo inicial exige contexto', 'trecho': window[:2000]})
    decoded = body
    for _ in range(3):
        decoded = html.unescape(decoded)
    placeholder = re.search(r'(?im)^\s*(?:#{1,6}\s*)?(?:(?:<|\[){1,3}\s*(?:anex[oa]s?|tabela|quadro|modelo|planilha)\b[^\n]{0,180}(?:>|\])|(?:anexo|tabela|quadro|modelo|planilha)[^\n]{0,100}(?:omitid|n[aã]o\s+(?:transcrit|reproduz)|vide\s+(?:publica|original)))', decoded)
    if placeholder:
        reasons.append({'motivo': 'placeholder de suplemento exige contexto', 'trecho': placeholder[0]})
    return reasons


def conferir_fonte(registro, source):
    if origem(registro) == 'rfb':
        reason = pendencia_visual(json.loads(source))
        return [{'motivo': reason}] if reason else []
    text = source.decode('utf-8')
    m = re.search(r'<div[^>]+class="[^\"]*texto-dou[^\"]*".*?</div>\s*(?=<div|</section|</main)', text, re.S)
    if not m:
        return [{'motivo': 'campo texto-dou ausente'}]
    fragment = m[0]
    if len(re.findall(r'<div\b', fragment, re.I)) != len(re.findall(r'</div\s*>', fragment, re.I)):
        return [{'motivo': 'campo HTML desbalanceado'}]
    if re.search(r'<(?:img|svg|canvas|object|embed|iframe|math|v:\w+|m:oMath)\b', fragment, re.I):
        return [{'motivo': 'visual/fórmula exige revisão'}]
    return []


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--baseline', type=Path, required=True)
    ap.add_argument('--manifesto-origem', type=Path, action='append', required=True)
    ap.add_argument('--reservados', type=Path, action='append', default=[])
    ap.add_argument('--saida', type=Path, required=True)
    ap.add_argument('--lista', type=Path, required=True)
    a = ap.parse_args()
    if a.saida.exists() or a.lista.exists():
        raise ValueError('saída já existe; use nova versão para preservar snapshot')
    base = a.baseline.read_bytes()
    headers = carregar(ROOT, base)
    tracked = set(base.decode().split('\0'))
    reservations = {}
    for p in a.reservados:
        raw = p.read_bytes()
        reservations[str(p)] = sha(raw)
        for path in raw.decode().splitlines():
            if path.startswith('reguladores/') and path.endswith('.md'):
                meta, _ = meta_corpo((ROOT / path).read_text())
                headers.append({'path': path, 'meta': meta})
                tracked.add(path)
    keys, urls = defaultdict(list), set()
    for row in headers:
        k = chave(row['meta'], row['path'])
        if all(k):
            keys[k].append(row['path'])
        urls.add(row['meta'].get('fonte'))
    accepted, held, sources = [], [], {}
    for src in a.manifesto_origem:
        raw = src.read_bytes()
        sources[str(src)] = sha(raw)
        for row in json.loads(raw)['documentos']:
            path = row['path']
            md = (ROOT / path).read_bytes()
            if sha(md) != row['sha256_md']:
                raise ValueError('Markdown mudou: ' + path)
            source = gzip.decompress((ROOT / row['cache']).read_bytes())
            source_sha = row.get('sha256_html', row.get('sha256_fonte'))
            if sha(source) != source_sha:
                raise ValueError('fonte mudou: ' + path)
            meta, body = meta_corpo(md.decode())
            k = chave(meta, path)
            reasons = motivos_identidade(meta, path, keys, urls, tracked)
            reasons.extend(conferir_fonte(row, source))
            reasons.extend(motivos_conteudo(body))
            if reasons:
                held.append({'path': path, 'sha256_md': sha(md), 'motivos': reasons})
                continue
            accepted.append({'path': path, 'sha256_md': sha(md), 'fonte': meta['fonte'], 'cache': row['cache'],
                             'sha256_fonte': source_sha, 'manifesto_origem': str(src)})
            tracked.add(path)
            urls.add(meta['fonte'])
            if all(k):
                keys[k].append(path)
    out = {'criterio': __doc__, 'script_sha256': sha(Path(__file__).read_bytes()), 'baseline_sha256': sha(base),
           'manifestos_origem': sources, 'reservas_sha256': reservations,
           'total': len(accepted), 'documentos': accepted, 'retidos': held}
    a.saida.parent.mkdir(parents=True, exist_ok=True)
    a.saida.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    a.lista.write_text(''.join(r['path'] + '\n' for r in accepted) + str(a.saida) + '\n')
    print(json.dumps({'aptos': len(accepted), 'retidos': len(held)}))


if __name__ == '__main__':
    main()
