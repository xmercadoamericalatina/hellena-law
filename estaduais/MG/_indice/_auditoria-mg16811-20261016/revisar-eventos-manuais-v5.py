import json,hashlib,re
from pathlib import Path
B=Path('estaduais/MG/_indice/_auditoria-mg16811-20261016');sha=lambda b:hashlib.sha256(b).hexdigest();inputfile=B/'revisao-unificada-contexto-v5.jsonl'
# Lista explícita dos primeiros eventos relidos em contexto, não aceite global por regex.
nums="35773 35852 36068 36293 36299 36470 36736 36895 37180 37567 37844 37898 37899 38052 38218 38398 38538 39603 39620 39665 39813 39814 40056 40190 40342 40375 40401 40537 40862 40945 41030 41129 41413 41535 41610 41646 41669 41688 41741 41863 42004 42127 42358 42681 42831 42846 43163 43195 43272 43324 43390 43493 43554 43605 43616 43618 43665 43705 43738 43743 43759 43785 43831 43835 43843 43854 43858 43864 43906 43920 43928 43941 43944 43950 43954 43995 43997 44015 44018 44023 44044 44056 44057 44082 44085 44087 44092 44093 44105 44119 44125 44131 44158 44162 44178 44179 44186 44188 44207 44239 44246 44256 44282 44286 44287 44288 44289 44301 44311 44320 44332 44350 44357 44366 44375 44381 44386 44389 44406 44420 44421 44449 44455 44462 44464 44468 44470 44497 44509 44521 44541 44553 44573 44580 44594 44595 44600 44605 44609 44624 44643 44664 44677 44678 44686 44706 44717 44733 44753 44754 44765 44792 44809 44822 44823 44840 44845 44856 44859 44867 44876 44878 44879 44894 44921 44926 44930 44931 44944 44965 44970 44981 44995 45008 45025 45047 45057 45058 45066 45068 45073 45074 45076 45081 45105 45110 45124 45126 45127 45129 45136 45150 45152 45154 45157 45163 45174 45182 45188 45190 45199 45210".split()
selected={'dec-'+n for n in nums}|{'dlb-'+n for n in '1260 1351 1465 1576 1807 1849 2379'.split()}|{'ral-'+n for n in '5183 5204 5212 5245'.split()}
out=[]
for r in map(json.loads,inputfile.read_text().splitlines()):
 stem=Path(r['path']).stem.rsplit('-',1)[0]
 if stem not in selected:continue
 events=[(j,e) for j,e in enumerate(r['reticencias']) if e['decisao'].startswith('incerto')]
 if not events:continue
 j,e=events[0];text=Path(r['path']).read_text();start=max(0,e['inicio']-2500);end=min(len(text),e['fim']+900);ctx=text[start:end]
 out.append(dict(path=r['path'],md_sha256=r['md_sha256'],fonte_sha256=r['fonte_sha256'],cache=r['cache'],inventario_v5_sha256=sha(inputfile.read_bytes()),evento_indice=j,literal_sha256=e['literal_sha256'],inicio=e['inicio'],fim=e['fim'],decisao='reticencia_de_porcoes_inalteradas_em_alteracao_expressa',fundamento='Evento relido no comando próprio de alteração/acréscimo/retificação de norma identificada e na respectiva redação parcial reproduzida. Reticência não substitui dado novo neste evento; conserva extensão não modificada. Decisão não se estende aos outros eventos do documento nem atesta integralidade global.',contexto_inicio=start,contexto_fim=end,contexto=ctx,contexto_sha256=sha(ctx.encode()),aprovacao_integralidade=False))
f=B/'revisao-individual-primeiros-eventos-v5.jsonl';f.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in out));print(len(out),sha(f.read_bytes()))
