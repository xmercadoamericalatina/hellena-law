"""Inventário offline de retenções SIJUT por corpo divergente; nunca promove."""
import argparse,collections,datetime,gzip,hashlib,json,sys
from pathlib import Path
from zoneinfo import ZoneInfo
sys.path.insert(0,str(Path(__file__).resolve().parent))
import baixar_rfb as rfb
from sijut_paragrafos_literais_proposta import extrair_literal
ROOT=Path(__file__).resolve().parent.parent

def sha(raw):return hashlib.sha256(raw).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--saida',type=Path,required=True);a=ap.parse_args();a.saida.mkdir(exist_ok=False);origins=[];pool={};accepted=set()
    for p in sorted((ROOT/'scripts/dados').glob('rfb-cache*.json')):
        raw=p.read_bytes();doc=json.loads(raw);origins.append(dict(arquivo=str(p.relative_to(ROOT)),sha256=sha(raw),bytes=len(raw)));(a.saida/'recibos').mkdir(exist_ok=True);(a.saida/'recibos'/p.name).write_bytes(raw)
        accepted.update(r['path'] for r in doc.get('documentos',[]) if r.get('path'))
        for row in doc.get('retidos',[]):
            if row.get('motivo')=='corpo difere da reextração integral da API':pool.setdefault(row['path'],[]).append(str(p.relative_to(ROOT)))
    rows=[];counts=collections.Counter();excluded=collections.Counter();start=datetime.datetime.now(ZoneInfo('America/Recife')).isoformat()
    for n,(path,receipts) in enumerate(sorted(pool.items()),1):
        r=dict(path=path,recibos_origem=receipts,aceito_em_algum_recibo_rfb=path in accepted,elegivel_extrair_literal=False)
        try:
            pre=(ROOT/path).read_bytes();r.update(sha256_preimagem=sha(pre),bytes_preimagem=len(pre));meta,_=rfb.metadados_md(pre.decode());ident=int(meta['id_rfb']);r['id_rfb']=ident;r['identidade_preimagem']={k:meta.get(k) for k in ['titulo','tipo','numero','data','orgao','baixado_em']};url=rfb.CORPO+str(ident)+'/visao/original';cache=rfb.RAIZ/'_fonte/sijut'/(sha(url.encode())+'.json.gz');compressed=cache.read_bytes();raw=gzip.decompress(compressed);doc=json.loads(raw);r.update(cache=str(cache.relative_to(ROOT)),sha256_cache_gzip=sha(compressed),sha256_fonte=sha(raw),bytes_fonte=len(raw),identidade_fonte=rfb.identidade(doc),epigrafe_completa_fonte=doc.get('epigrafeCompleta'),fonte_api=url)
            if doc.get('idAto')!=ident:raise ValueError('ID da fonte diverge da preimagem')
            extraido=extrair_literal(doc);r.update(elegivel_extrair_literal=True,sha256_representacao_proposta=sha(extraido.encode()),bytes_representacao_proposta=len(extraido.encode()),segmentos_ativos=sum(not s.get('omitir') and bool(s.get('original')) for s in doc.get('ementas',[])+doc.get('outrosSegmentos',[])))
        except Exception as exc:r['motivo_exclusao']=type(exc).__name__+': '+str(exc);excluded[r['motivo_exclusao']]+=1
        counts['elegivel' if r['elegivel_extrair_literal'] else 'excluido']+=1
        if r['aceito_em_algum_recibo_rfb']:counts['tambem_aceito_em_recibo_rfb']+=1
        rows.append(r)
        if n%1000==0:print(n,dict(counts),flush=True)
    (a.saida/'resultados.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows));(a.saida/'elegiveis.paths.txt').write_text(''.join(r['path']+'\n' for r in rows if r['elegivel_extrair_literal']));(a.saida/'excluidos.paths.txt').write_text(''.join(r['path']+'\n' for r in rows if not r['elegivel_extrair_literal']));(a.saida/'controle.json').write_text(json.dumps(dict(inicio=start,fim=datetime.datetime.now(ZoneInfo('America/Recife')).isoformat(),retencoes_unicas=len(rows),contagens=counts,motivos_exclusao=excluded,recibos=origins,limite='Elegibilidade da representação literal, não aprovação ou confirmação de publicação. União histórica de retenções deduplicada por path/ID; SHA atuais da preimagem e do cache. Nenhuma rede, norma ou auditor alterado; sem afirmar conformidade de catálogo/duplicação/vigência/íntegra jurídica.',codigo_sha256=sha(Path(__file__).read_bytes())),ensure_ascii=False,indent=2)+'\n');print('FIM',len(rows),dict(counts),dict(excluded),flush=True)

if __name__=='__main__':main()
