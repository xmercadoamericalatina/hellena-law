"""Confronta DOCX simples com Markdown sem depender do conversor textutil.

Sem publicação automática: somente OOXML sem imagens, tabelas, campos, listas
implícitas, revisões ou partes textuais adicionais pode passar pelo confronto.
Toda estrutura não suportada permanece retida, incluindo links externos.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parent))
from auditar_municipal import metadados
from auditar_colunas_sapl import analisar as colunas
RAIZ=Path(__file__).resolve().parent.parent
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PROIBIDOS={'drawing','pict','object','tbl','numPr','fldSimple','fldChar','instrText','altChunk','del','ins','moveFrom','moveTo','vanish','strike','dstrike','sym','tab','sdt','oMath','oMathPara','footnoteReference','endnoteReference'}

def sha(b):return hashlib.sha256(b).hexdigest()
def extrair_simples(bruto):
    with zipfile.ZipFile(io.BytesIO(bruto)) as z:
        names=z.namelist()
        if 'word/document.xml' not in names:raise ValueError('não é DOCX WordprocessingML')
        if any(s.startswith(('word/media/','word/embeddings/','word/charts/','word/diagrams/')) or s.endswith('.bin') for s in names):raise ValueError('ativo gráfico, objeto ou diagrama requer revisão')
        parts=[];main=None
        for name in names:
            if name.endswith('.rels'):
                tree=ET.fromstring(z.read(name))
                if any(x.attrib.get('TargetMode')=='External' for x in tree):raise ValueError('relacionamento externo requer revisão')
            if not name.startswith('word/') or not name.endswith('.xml'):continue
            tree=ET.fromstring(z.read(name));tags={x.tag.rsplit('}',1)[-1] for x in tree.iter()}
            if name=='word/document.xml':
                unsupported=tags&PROIBIDOS
                if unsupported:raise ValueError('estrutura não suportada: '+','.join(sorted(unsupported)))
                main=tree
            elif name not in ('word/styles.xml','word/stylesWithEffects.xml','word/numbering.xml','word/settings.xml','word/fontTable.xml','word/webSettings.xml'):
                if tags&{'drawing','pict','object','fldSimple','fldChar','instrText','altChunk','oMath','oMathPara'}:raise ValueError('estrutura não suportada em parte adicional: '+name)
                texts=[''.join(x.itertext()) for x in tree.iter(W+'t')]
                if any(t.strip() for t in texts):raise ValueError('texto em parte adicional: '+name)
            if name in ('word/styles.xml','word/stylesWithEffects.xml') and tags&{'vanish','strike','dstrike'}:raise ValueError('estilo de ocultação/tachado requer revisão')
            parts.append({'path_ooxml':name,'sha256':sha(z.read(name))})
        body=main.find(W+'body')
        if body is None:raise ValueError('sem corpo OOXML')
        # Numeração e fontes de símbolos podem ser herdadas, sem numPr no corpo.
        usados={x.attrib.get(W+'val') for x in main.iter() if x.tag in (W+'pStyle',W+'rStyle')}
        estilos={}
        for stylepart in ('word/styles.xml','word/stylesWithEffects.xml'):
            if stylepart not in names:continue
            st=ET.fromstring(z.read(stylepart))
            for x in st.iter(W+'style'):
                sid=x.attrib.get(W+'styleId');estilos[sid]=x
                if x.attrib.get(W+'default') in ('1','true'):usados.add(sid)
        pendentes=list(usados)
        while pendentes:
            sid=pendentes.pop();st=estilos.get(sid)
            if st is None:continue
            if any(x.tag==W+'numPr' for x in st.iter()):raise ValueError('numeração herdada de estilo: '+str(sid))
            for parent in st.iter(W+'basedOn'):
                pid=parent.attrib.get(W+'val')
                if pid not in usados:usados.add(pid);pendentes.append(pid)
        if 'word/numbering.xml' in names:
            numbering=ET.fromstring(z.read('word/numbering.xml'))
            if any(x.attrib.get(W+'val') in usados for x in numbering.iter(W+'pStyle')):raise ValueError('estilo usado vinculado a numeração implícita')
        for tree in [main]+[estilos[x] for x in usados if x in estilos]:
            if any(re.search(r'(wingdings|webdings|symbol|dingbat)',v,re.I) for x in tree.iter(W+'rFonts') for v in x.attrib.values()):raise ValueError('fonte simbólica requer revisão visual')
        paragraphs=[''.join(''.join(x.itertext()) for x in p.iter(W+'t')) for p in body.iter(W+'p')]
        return '\n\n'.join(paragraphs),parts

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--lista',type=Path,required=True);ap.add_argument('--saida',type=Path,required=True);a=ap.parse_args();a.saida.mkdir(parents=True,exist_ok=False);rows=[]
    for rel in a.lista.read_text().splitlines():
        p=RAIZ/rel;b=p.read_bytes();m=metadados(b.decode());u=urlsplit(m['fonte']);raw=RAIZ/'municipais/_fonte/organicas-sapl'/u.hostname/(u.path.strip('/').split('/')[-1]+'.bin');record={'path':rel,'sha256':sha(b),'aprovado':False}
        try:
            binary=raw.read_bytes()
            if sha(binary)!=m['sha256_fonte']:raise ValueError('fonte mudou')
            native,parts=extrair_simples(binary);body=b.decode().split('\n---\n',1)[1].lstrip('\n').split('\n\n',1)[1]
            if re.findall(r'\w+',native)!=re.findall(r'\w+',body):raise ValueError('tokens do texto nativo completo divergem do Markdown')
            guard=colunas(m,native)
            if guard['alertas']:raise ValueError('identidade/objeto requer revisão: '+json.dumps(guard['alertas'],ensure_ascii=False))
            record.update({'aprovado':True,'fonte':m['fonte'],'fonte_texto':m['fonte_texto'],'fonte_binaria':{'path':str(raw.relative_to(RAIZ)),'sha256':sha(binary)},'partes_ooxml':parts,'texto_nativo':native,'tokens':len(re.findall(r'\w+',native)),'data_epigrafe_clara_conferida':guard['data_epigrafe_clara_conferida']})
        except Exception as err:record['retencao']=str(err)
        rows.append(record)
    (a.saida/'controle.json').write_text(json.dumps({'criterio':__doc__,'resultados':rows,'script_sha256':sha(Path(__file__).read_bytes())},ensure_ascii=False,indent=2));(a.saida/'candidatos.paths.txt').write_text(''.join(r['path']+'\n' for r in rows if r['aprovado']));print(json.dumps({'examinados':len(rows),'candidatos_simples':sum(r['aprovado'] for r in rows)}))
if __name__=='__main__':main()
