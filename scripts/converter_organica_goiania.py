"""Transcreve a versão oficialmente denominada redação vigente da LOM de Goiânia."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from html2md import convert
from comum import yaml_str
from converter_organica_fortaleza import tokens
RAIZ=Path(__file__).resolve().parent.parent
URL='https://transparencia.camaragyn.go.gov.br/files/Legislacao-compilada/Lei-Organica-do-Municipio-de-Goiania.htm'


def sha(b):return hashlib.sha256(b).hexdigest()


def converter(html):
    if re.search(r'<(?:img|svg|object|embed|canvas)\b',html,re.I):raise ValueError('conteúdo visual requer revisão')
    match=re.search(r'<article>(.*?)</article>',html,re.S)
    if not match:raise ValueError('seção normativa não reconhecida')
    art=match[1]
    md=convert(art,exclude_struck=True)
    if tokens(art,True)!=tokens(md):raise ValueError('confronto integral de texto diverge')
    return md,len(tokens(art,True))


def main():
    pasta=RAIZ/'municipais/_fonte/capitais/goiania';source=pasta/'lei-organica.html';h=source.read_text()
    cidade=next(x for x in json.loads((RAIZ/'municipais/_indice/ibge-municipios.json').read_text()) if str(x['id'])=='5208707')
    if cidade['nome']!='Goiânia' or cidade['regiao-imediata']['regiao-intermediaria']['UF']['sigla']!='GO':raise ValueError('identidade IBGE divergente')
    if not all(s in h for s in ('redação vigente','Goi&acirc;nia, 05 de abril de 1990','Emenda à Lei Orgânica n&ordm; 88','DOM n&ordm; 8.693 de 05/01/2026')):raise ValueError('identidade/corte temporal não comprovados')
    corpo,n=converter(h)
    if '(Revogado' not in corpo or '(Suspenso' not in corpo:raise ValueError('marcadores de situação não reconhecidos')
    titulo='Lei Orgânica do Município de Goiânia, de 5 de abril de 1990'
    meta={'titulo':titulo,'tipo':'Lei Orgânica','numero':'','data':'1990-04-05','municipio':'Goiânia','uf':'GO','codigo_ibge':'5208707',
          'versao_texto':'redação vigente identificada no portal oficial, atualizada até a Emenda88 de16/12/2025, publicada noDOM8693 de05/01/2026; notas de revogação/suspensão preservadas; não certifica atualização além do snapshot',
          'fonte':URL,'fonte_texto':URL,'sha256_fonte':sha(source.read_bytes()),'sha256_texto':sha(corpo.encode()),'baixado_em':dt.date.today().isoformat()}
    destino=RAIZ/'municipais/GO/goiania/lei-organica/1990/lei-organica-goiania-1990.md'
    if list(destino.parent.parent.glob('**/*.md')):raise ValueError('categoria já tem documento; revisar antes de duplicar')
    saida='\n'.join(['---']+[k+': '+yaml_str(v) for k,v in meta.items()]+['revogada: null','---','','# '+titulo,'',corpo,''])
    destino.parent.mkdir(parents=True,exist_ok=True)
    with destino.open('x') as f:f.write(saida)
    manifesto={'path':str(destino.relative_to(RAIZ)),'sha256':sha(saida.encode()),'fonte':URL,'sha256_fonte':sha(source.read_bytes()),'tokens_conferidos_integralmente':n,'metodo':'Todos tokens da seçãoarticle em ordem idênticos aoMarkdown, com notas de alteração/revogação/suspensão. Nenhuma imagem normativa na seção. Página declara redaçãovigente e corteatéEmenda88/2025, cuja publicação declaradaé05/01/2026.','ibge_sha256':sha((RAIZ/'municipais/_indice/ibge-municipios.json').read_bytes())}
    with (pasta/'lei-organica-goiania-1990.manifesto.json').open('x') as f:json.dump(manifesto,f,ensure_ascii=False,indent=2)
    print(json.dumps(manifesto,ensure_ascii=False))


if __name__=='__main__':main()
