"""Lei Orgânica de Fortaleza no texto articulado oficial: só dispositivos ativos.

A interface oficial TVL oculta .dptt.desativado; conserva .revogado. O HTML,
CSS e JavaScript originais permanecem no cache para evidenciar esse critério.
"""
from html.parser import HTMLParser
from pathlib import Path
import datetime as dt
import hashlib
import json
import re
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from html2md import convert
from comum import yaml_str

RAIZ=Path(__file__).resolve().parent.parent


def sha(b):return hashlib.sha256(b).hexdigest()


class Dispositivos(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.ativos=[];self.historicos=[];self.atual=None;self.depth=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);classes=a.get('class','').split()
        if tag=='div' and 'dptt' in classes:
            if self.atual:raise ValueError('dptt aninhado requer revisão')
            self.atual={'id':a.get('id'),'historico':'desativado' in classes,'html':[]};self.depth=0
        if self.atual:
            self.atual['html'].append(self.get_starttag_text())
            if tag=='div':self.depth+=1
    def handle_endtag(self,tag):
        if self.atual:
            self.atual['html'].append('</'+tag+'>')
            if tag=='div':
                self.depth-=1
                if self.depth==0:
                    r=self.atual;r['html']=''.join(r['html'])
                    (self.historicos if r['historico'] else self.ativos).append(r);self.atual=None
    def handle_startendtag(self,tag,attrs):
        if self.atual:self.atual['html'].append(self.get_starttag_text())
    def handle_data(self,s):
        if self.atual:self.atual['html'].append(s)
    def handle_entityref(self,s):self.handle_data('&'+s+';')
    def handle_charref(self,s):self.handle_data('&#'+s+';')


class Texto(HTMLParser):
    def __init__(self,excluir_tachados=False):super().__init__();self.partes=[];self.stack=[];self.excluir_tachados=excluir_tachados
    def handle_data(self,s):
        if not any(x[1] for x in self.stack):self.partes.append(s)
    def handle_starttag(self,t,a):
        if t not in ('br','img','input','meta','link','hr','wbr','col'):
            style=dict(a).get('style','').lower()
            self.stack.append((t,self.excluir_tachados and (t in ('s','del','strike') or 'line-through' in style)))
        if t in ('div','p','br','td','th','tr','table','li'):self.partes.append('\n')
    def handle_endtag(self,t):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==t:
                del self.stack[i:];break
        if t in ('div','p','td','th','tr','table','li'):self.partes.append('\n')


def tokens(html,excluir_tachados=False):
    p=Texto(excluir_tachados);p.feed(html)
    return re.findall(r'\w+',''.join(p.partes).replace('\\_','_').replace('\\*','*'))


def converter(html):
    p=Dispositivos();p.feed(html);p.close()
    if p.atual:raise ValueError('dispositivo incompleto')
    partes=[]
    for bloco in p.ativos:
        trecho=convert(bloco['html'],exclude_struck=True)
        if tokens(bloco['html'],True)!=tokens(trecho):raise ValueError('confronto integral do dispositivo ativo diverge: '+str(bloco['id']))
        bloco['tachado_interno_omitido']=tokens(bloco['html'])!=tokens(bloco['html'],True)
        if bloco['tachado_interno_omitido']:
            trecho+='\n\n_Nota editorial: a fonte contém redação tachada neste dispositivo; esse texto histórico foi omitido desta transcrição e permanece no HTML original._'
        if trecho.strip():partes.append(trecho)
    md='\n\n'.join(partes)
    return md,p


def main():
    pasta=RAIZ/'municipais/_fonte/capitais/fortaleza'
    source=pasta/'lei-organica-2006-sapl44.html';html=source.read_text()
    if 'Vigência a partir de <b>30 de Junho de 2025</b>' not in html:raise ValueError('corte de vigência mudou')
    norma=json.loads((pasta/'norma-5257.json').read_text())
    casa=json.loads((pasta/'casa.json').read_text())['results'][0]
    if (norma['numero'],norma['data'],casa['municipio'],casa['uf'])!=('1','2006-12-15','Fortaleza','CE'):raise ValueError('identidade oficial divergente')
    ibge=next(x for x in json.loads((RAIZ/'municipais/_indice/ibge-municipios.json').read_text()) if str(x['id'])=='2304400')
    if ibge['nome']!='Fortaleza' or ibge['regiao-imediata']['regiao-intermediaria']['UF']['sigla']!='CE':raise ValueError('identidade IBGE divergente')
    corpo,p=converter(html)
    if not p.historicos or '(Revogado)' not in corpo:raise ValueError('estados histórico/revogado não reconhecidos')
    titulo='Lei Orgânica nº 1, de 15 de dezembro de 2006 — Município de Fortaleza'
    meta={'titulo':titulo,'tipo':'Lei Orgânica','numero':'1','data':'2006-12-15','municipio':'Fortaleza','uf':'CE','codigo_ibge':'2304400',
          'versao_texto':'compilação marcada no SAPL como atual, vigência a partir de 30/06/2025 dada pela Emenda25/2025; dispositivos desativados excluídos, marcadores de revogação preservados; não certifica atualização jurídica além do snapshot',
          'fonte':'https://sapl.fortaleza.ce.leg.br/norma/5257','fonte_texto':'https://sapl.fortaleza.ce.leg.br/ta/44/text',
          'sha256_fonte':sha(source.read_bytes()),'sha256_texto':sha(corpo.encode()),'baixado_em':dt.date.today().isoformat()}
    destino=RAIZ/'municipais/CE/fortaleza/lei-organica/2006/lei-organica-1-2006.md'
    if destino.exists():raise ValueError('documento já existe; não substituir sem revisão')
    if list(destino.parent.parent.glob('**/*.md')):raise ValueError('categoria já tem documento; revisar duplicata')
    saida='\n'.join(['---']+[k+': '+yaml_str(v) for k,v in meta.items()]+['revogada: null','---','','# '+titulo,'',corpo,''])
    destino.parent.mkdir(parents=True,exist_ok=True)
    with destino.open('x') as f:f.write(saida)
    manifesto={'path':str(destino.relative_to(RAIZ)),'sha256':sha(saida.encode()),'sha256_fonte':meta['sha256_fonte'],'tokens_ativos_conferidos':len(tokens(corpo)),
               'criterio':'Mesma seleção do controle oficial Texto Vigente COM Links: .dptt.desativado oculto, .dptt.revogado mantido; confronto integral de tokens da seleção ativa.',
               'evidencias':[{'path':str(x.relative_to(RAIZ)),'sha256':sha(x.read_bytes())} for x in sorted(pasta.iterdir()) if x.is_file()],
               'ativos':[{'id':x['id'],'sha256_html':sha(x['html'].encode()),'tachado_interno_omitido':x['tachado_interno_omitido']} for x in p.ativos],
               'historicos_retidos_apenas_no_html_fonte':[{'id':x['id'],'sha256_html':sha(x['html'].encode())} for x in p.historicos]}
    with (pasta/'lei-organica-1-2006.manifesto.json').open('x') as f:json.dump(manifesto,f,ensure_ascii=False,indent=2)
    print(json.dumps({'path':manifesto['path'],'ativos':len(p.ativos),'historicos':len(p.historicos),'tokens':len(tokens(corpo))},ensure_ascii=False))


if __name__=='__main__':main()
