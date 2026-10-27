"""Regressão offline da proposta privada; nenhum canônico é alterado."""
import copy
import datetime
import gzip
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parent))
sys.path.insert(0,'/tmp/constituicao-markdown-qa-20261020')
from markdown_it import MarkdownIt
import baixar_rfb as rfb
import sijut_paragrafos_literais_proposta as p
BASE=Path(__file__).resolve().parent.parent/'municipais/_lotes/20261021-sijut-paragrafos-proposta'

class Paragraphs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.rows=[];self.current=None
    def handle_starttag(self,tag,attrs):
        if tag=='p':
            attrs=dict(attrs);self.current=[attrs,''];self.rows.append(self.current)
    def handle_data(self,data):
        if self.current is not None:self.current[1]+=data
    def handle_endtag(self,tag):
        if tag=='p':self.current=None

class TestProposta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=json.loads((BASE/'casos.json').read_text());cls.docs=[json.loads(gzip.decompress(Path(r['cache']).read_bytes())) for r in cls.rows]
        spec=importlib.util.spec_from_file_location('auditor_privado',BASE/'auditar_cache_rfb.candidato.py');cls.audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.audit);cls.audit.RAIZ=Path(__file__).resolve().parent.parent
    def test_tres_casos_dom_e_metadados(self):
        for row,doc in zip(self.rows,self.docs):
            md=Path(row['candidato']).read_text();meta,body=rfb.metadados_md(md);original=Path(row['candidato'].replace('.candidato.md','.preimagem.md')).read_text();old,_=rfb.metadados_md(original)
            self.assertEqual({k:v for k,v in meta.items() if k not in ('sha256_texto','representacao_texto')},{k:v for k,v in old.items() if k!='sha256_texto'})
            extracted=p.extrair_literal(doc);self.assertEqual(meta['sha256_texto'],hashlib.sha256(extracted.encode()).hexdigest())
            parser=Paragraphs();parser.feed(MarkdownIt('commonmark',{'html':True}).render(md.split('\n---\n',1)[1]));segments=sorted(doc['ementas']+doc['outrosSegmentos'],key=lambda s:s['ordemSegmentoAto'])
            self.assertEqual([text for attrs,text in parser.rows],[s['textoIntegra'] for s in segments]);self.assertEqual([a['data-segmento'] for a,t in parser.rows],[str(s['idSegmento']) for s in segments]);self.assertIn('-'*75,[t for a,t in parser.rows])
    def test_auditor_completo_e_tamper(self):
        for row,doc in zip(self.rows,self.docs):
            path=Path(row['candidato']).resolve();meta,_=rfb.metadados_md(path.read_text());indice={doc['idAto']:{'dataAto':meta['data'],'numeroAto':meta['numero']}}
            checked,_=self.audit.auditar(path,indice,set(),set(),datetime.date(2026,10,21));self.assertEqual(checked['id_rfb'],doc['idAto'])
            with self.assertRaisesRegex(ValueError,'identidade/URL'):self.audit.auditar(path,indice,{self.audit.chave(meta)},set(),datetime.date(2026,10,21))
            with self.assertRaisesRegex(ValueError,'identidade diverge'):self.audit.auditar(path,{doc['idAto']:{'numeroAto':'99999'}},set(),set(),datetime.date(2026,10,21))
    def test_flags_ordem_escape_e_espacos(self):
        d=copy.deepcopy(self.docs[0]);d['ementas']=[];template=d['outrosSegmentos'][0];items=[]
        for i,text in [(3,'# literal **forte** `x` < 5 & x\n  fim'),(1,'1. enumeração literal '+'x'*100),(2,'-'*75)]:
            s=copy.deepcopy(template);s.update(idSegmento=i,ordemSegmentoAto=i,textoIntegra=text);items.append(s)
        omitted=copy.deepcopy(items[0]);omitted.update(idSegmento=90,ordemSegmentoAto=90,omitir=True,arquivoBinario={'idTipoArquivo':6});items.append(omitted)
        nonoriginal=copy.deepcopy(omitted);nonoriginal.update(original=False,omitir=False);items.append(nonoriginal);d['outrosSegmentos']=items
        parsed=Paragraphs();parsed.feed(MarkdownIt('commonmark',{'html':True}).render(p.extrair_literal(d)));self.assertEqual([t for a,t in parsed.rows],[s['textoIntegra'] for s in sorted(items[:3],key=lambda s:s['ordemSegmentoAto'])]);self.assertIn('&lt; 5 &amp; x',p.extrair_literal(d))
    def test_apresentacao_anexo_ambiguidades_retidos(self):
        for changes in [dict(tachado=True),dict(estiloSegmento='color:red'),dict(agendado=True),dict(arquivoBinario={'idTipoArquivo':4}),dict(textoIntegra='<b>texto</b>'),dict(textoIntegra='&lt;'),dict(ancorasDestino=[1])]:
            d=copy.deepcopy(self.docs[0]);d['outrosSegmentos'][0].update(changes)
            with self.assertRaises(ValueError):p.extrair_literal(d)
        d=copy.deepcopy(self.docs[0]);d['outrosSegmentos'][0]['ordemSegmentoAto']=1
        with self.assertRaises(ValueError):p.extrair_literal(d)
    def test_modo_explicito_sem_relaxar_padrao(self):
        class Fake:
            def extrair(self,doc,offline):return 'legado'
        self.assertEqual(p.extrair_para_auditoria({}, {},Fake(),None),'legado')
        with self.assertRaisesRegex(ValueError,'desconhecida'):p.extrair_para_auditoria({}, {'representacao_texto':'outro'},Fake(),None)
        with self.assertRaises(ValueError):p.extrair_literal(dict(integro=False,publicado=True,internet=True))

if __name__=='__main__':unittest.main()
