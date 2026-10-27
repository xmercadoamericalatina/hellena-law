"""Prova independente de tabelas HTML ativas, célula por célula e com mesclagens.

Triagem somente: não aprova identidade, anexos, vigência ou integralidade do ato.
Recusa mídia, tabelas aninhadas e apresentação contextual dentro da tabela.
"""
from html.parser import HTMLParser
import re
import hashlib
from pathlib import Path
import sys
sys.path.insert(0,'/tmp/constituicao-markdown-qa-20261020')
from markdown_it import MarkdownIt
STRUCT={'table','thead','tbody','tfoot','tr','td','th','caption','colgroup','col'}
ALLOWED=STRUCT|{'p','div','span','strong','b','em','i','u','br','a'}
VOID={'br','col','img','meta','link','input','hr','wbr','source','area','embed','param'}

class Tabelas(HTMLParser):
    def __init__(self,source=False):
        super().__init__(convert_charrefs=True);self.source=source;self.stack=[];self.tables=[];self.current=None
    def emit(self,event):
        if event[0]=='text' and self.current and self.current[-1][0]=='text':self.current[-1]=('text',self.current[-1][1]+event[1])
        else:self.current.append(event)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);parent=self.stack[-1] if self.stack else dict(active=not self.source,hidden=False,struck=False);state=dict(parent,tag=tag)
        if 'dptt' in a.get('class','').split():state.update(hidden=parent['hidden'] or 'desativado' in a.get('class','').split());state['active']=not state['hidden']
        state['struck']=parent['struck'] or tag in {'s','del','strike'} or bool(re.search('line-through',a.get('style',''),re.I))
        if tag=='table' and state['active']:
            if self.current is not None:raise ValueError('Tabela aninhada exige prova própria')
            if state['struck']:raise ValueError('Tabela tachada exige prova contextual')
            self.current=[];self.tables.append(self.current)
        if self.current is not None:
            if tag not in ALLOWED or state['struck']:raise ValueError('Mídia, tag ou tachado dentro da tabela exige revisão')
            classes=a.get('class','').split()
            if classes and not (tag=='table' and classes==['mat']):raise ValueError('Classe contextual na tabela exige revisão')
            if any(k in a for k in ('color','bgcolor')) or any(k.startswith('on') for k in a):raise ValueError('Cor ou comportamento na tabela exige revisão')
            if 'hidden' in a or a.get('aria-hidden')=='true' or a.get('dir') or re.search(r'color|display|visibility|position|text-decoration|content|direction|transform',a.get('style',''),re.I):raise ValueError('Apresentação contextual na tabela exige revisão')
            if tag in STRUCT:
                semantic={k:a[k] for k in ('rowspan','colspan','scope','headers','abbr','span') if k in a}
                for k in ('rowspan','colspan','span'):
                    if k in semantic and (not re.fullmatch('[1-9][0-9]*',semantic[k]) or int(semantic[k])>1000):raise ValueError('Mesclagem inválida ou não suportada')
                self.emit(('open',tag,tuple(sorted(semantic.items()))))
            if tag=='a':self.emit(('link',a.get('href','')))
        if tag not in VOID:self.stack.append(state)
    def handle_endtag(self,tag):
        if self.current is not None:
            if tag in STRUCT:self.emit(('close',tag))
            if tag=='table':self.current=None
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i]['tag']==tag:del self.stack[i:];break
    def handle_data(self,text):
        if self.current is not None:
            compact=''.join(text.split())
            if compact:self.emit(('text',compact))
    def handle_startendtag(self,tag,attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID:self.handle_endtag(tag)


def conferir(source,body):
    original=Tabelas(True);original.feed(source);original.close()
    if original.current is not None:raise ValueError('Tabela original não encerrada')
    rendered=MarkdownIt('commonmark',{'html':True}).enable('table').enable('strikethrough').render(body);replay=Tabelas();replay.feed(rendered);replay.close()
    if replay.current is not None:raise ValueError('Tabela renderizada não encerrada')
    if not original.tables:raise ValueError('Nenhuma tabela ativa na fonte')
    if original.tables!=replay.tables:raise ValueError('Estrutura/células/mesclagens/links da tabela divergem')
    return dict(tabelas=len(original.tables),eventos=sum(map(len,original.tables)),assinaturas=original.tables,codigo_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
