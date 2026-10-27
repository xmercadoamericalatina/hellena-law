"""Sinaliza atos alheios/identidade divergente em qualquer coluna do PDF nativo.

Só produz suspeitos. Uma captura fiel de página inteira não prova granularidade.
Epígrafes/avisos/datas ambíguos exigem revisão; ausência não certifica vigência.
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
sys.path.insert(0,str(Path(__file__).resolve().parent))
from auditar_municipal import metadados
RAIZ=Path(__file__).resolve().parent.parent
EPIGRAFE=re.compile(r'(?:^|\s{2,})(?P<tipo>PORTARIA(?:\s+MUNICIPAL)?|RESOLU[ÇC][ÃA]O(?:\s+(?:ADMINISTRATIVA|LEGISLATIVA))?|DECRETO(?:\s+(?:LEGISLATIVO|MUNICIPAL|NORMATIVO))?|LEI(?:\s+(?:COMPLEMENTAR|ORDIN[ÁA]RIA|MUNICIPAL|DELEGADA)){0,2}|EMENDA(?:\s+[ÀA]\s+LEI\s+ORG[ÂA]NICA)?|ATO(?:\s+DA\s+MESA)?|DELIBERA[ÇC][ÃA]O|INSTRU[ÇC][ÃA]O\s+NORMATIVA|COMUNICADO|EDITAL)\s+(?:N[º°oO.\s]*\s*)?(?P<numero>\d[\d.]*)\s*(?=[/,]|$|\bDE\b)',re.M)
AVISO=re.compile(r'(?:^|\s{2,})(?:EXTRATO\s+(?:DE|DO|DA)\s+(?:CONTRATO|TERMO|DISPENSA|INEXIGIBILIDADE|ATA|ADITIVO)|AVISO\s+(?:DE|DO)\s+(?:LICITA[ÇC][ÃA]O|CONTRATA[ÇC][ÃA]O|DISPENSA|PREG[ÃA]O|TOMADA|CHAMADA)|EDITAL\s+(?:DE\s+)?(?:COMUNICA[ÇC][ÃA]O|LICITA[ÇC][ÃA]O|PREG[ÃA]O|CHAMAMENTO|CONVOCA[ÇC][ÃA]O)|PREG[ÃA]O\s+(?:ELETR[ÔO]NICO|PRESENCIAL)\s+N[º°.\s]*\d)',re.M)
PROJETO=re.compile(r'(?:^|\s{2,})(?:PROJETO\s+DE\s+(?:LEI|RESOLU[ÇC][ÃA]O|DECRETO)|MINUTA\b|ANTEPROJETO\b)',re.M)
MESES={'janeiro':1,'fevereiro':2,'marco':3,'abril':4,'maio':5,'junho':6,'julho':7,'agosto':8,'setembro':9,'outubro':10,'novembro':11,'dezembro':12}

def sha(b):return hashlib.sha256(b).hexdigest()
def normal(s):return ''.join(c for c in unicodedata.normalize('NFD',str(s)).lower() if unicodedata.category(c)!='Mn')
def numero(s):return re.sub(r'\D','',str(s)).lstrip('0')

def analisar(meta,layout):
    own=numero(meta.get('numero',''));tipo=normal(meta.get('tipo',''));tipo='EMENDA' if 'emenda' in tipo else 'DECRETO' if 'decreto' in tipo else 'RESOLU' if 'resolu' in tipo else 'LEI';out=[];date_checked=False
    def add(regra,a):out.append({'regra':regra,'offset':a.start(),'trecho':layout[max(0,a.start()-120):a.end()+270]})
    for a in EPIGRAFE.finditer(layout):
        if numero(a['numero'])!=own or not a['tipo'].startswith(tipo):add('epigrafe_divergente_possivel',a)
        if date_checked or a.start()>=5000 or numero(a['numero'])!=own:continue
        dm=re.match(r'\s*(?:/\s*\d{2,4})?\s*[,.-]?\s*(?:DE\s+)?(\d{1,2})[º°]?\s+DE\s+(\w+)\s+DE\s+(\d{4})',layout[a.end():a.end()+190],re.I)
        if not dm or normal(dm[2]) not in MESES:continue
        date_checked=True
        try:d=dt.date(int(dm[3]),MESES[normal(dm[2])],int(dm[1])).isoformat()
        except ValueError:d='data_inválida'
        if d!=meta.get('data'):add('data_epigrafe_divergente',a);out[-1].update({'data_metadado':meta.get('data'),'data_epigrafe':d})
    for a in AVISO.finditer(layout):add('aviso_contratacao_ou_publicacao_possivelmente_alheia',a)
    for a in PROJETO.finditer(layout[:2500]):add('arquivo_com_cabecalho_de_projeto',a)
    # Alguns SAPLs cadastram emendas como Lei Orgânica. A epígrafe pode incluir
    # o nome completo da cidade entre ORGÂNICA e Nº, fora do padrão curto acima.
    # Só examina o cabeçalho anterior ao primeiro artigo, nunca notas no corpo.
    article = re.search(r'\bart(?:igo)?\.?\s*1[º°o.\s]', layout, re.I)
    header = layout[:min(article.start() if article else 4000, 4000)]
    if 'organica' in normal(meta.get('tipo','')) and tipo != 'EMENDA':
        for a in re.finditer(r'^[\s*#]*EMENDA\s+[ÀA]\s+LEI\s+ORG[ÂA]NICA\b', header, re.M | re.I):
            add('epigrafe_de_emenda_em_cadastro_de_lei_organica', a)
    codigos=set(re.findall(r'[Cc][óo]digo\s+[Ii]dentificador\s*[:.\-]?\s*([A-Za-z0-9]{6,})',layout))
    if len(codigos)>1:out.append({'regra':'multiplos_codigos_identificadores','codigos':sorted(codigos)})
    if tipo=='EMENDA' and re.match(r'\s*REGIMENTO\s+INTERNO',layout,re.I):out.append({'regra':'objeto_regimento_em_cadastro_de_emenda','trecho':layout[:700]})
    return {'alertas':out,'data_epigrafe_clara_conferida':date_checked}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--lista',type=Path,action='append',required=True);ap.add_argument('--evidencias',type=Path,required=True);ap.add_argument('--saida',type=Path,required=True);a=ap.parse_args();a.saida.mkdir(exist_ok=False,parents=True)
    txt=a.evidencias.read_text();data=json.loads(txt) if a.evidencias.suffix=='.json' else [json.loads(l) for l in txt.splitlines()];data=data['registros'] if isinstance(data,dict) else data;evid={r['path']:r['evidencia_extracao'] for r in data if r.get('evidencia_extracao')};results=[]
    for rel in dict.fromkeys(s for p in a.lista for s in p.read_text().splitlines()):
        md=(RAIZ/rel).read_bytes();r={'path':rel,'sha256':sha(md)}
        try:
            e=evid[rel];b=(RAIZ/e['path']).read_bytes()
            if sha(b)!=e['sha256']:raise ValueError('extração mudou')
            d=json.loads(gzip.decompress(b));r.update(analisar(metadados(md.decode()),d['layout']));r['evidencia']=e
        except Exception as err:r['pendencia']=str(err)
        results.append(r)
    result={'criterio':__doc__,'script_sha256':sha(Path(__file__).read_bytes()),'listas':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in a.lista],'resultados':results};(a.saida/'controle.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({'documentos':len(results),'suspeitos':sum(bool(r.get('alertas') or r.get('pendencia')) for r in results)}))

if __name__=='__main__':main()
