import sys, json, hashlib, datetime, re, urllib.parse, gzip
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'scripts'))
import baixar_camara as cam
from comum import Rede
P=Path(__file__).resolve().parent
class R(Rede):
    def get(self,url,**kw):
        st,b,ct=super().get(url,**kw)
        h=hashlib.sha256(b).hexdigest()
        (P/(h+'.bin')).write_bytes(b)
        (P/(h+'.json')).write_text(json.dumps(dict(url=url,status=st,content_type=ct,SHA=h,bytes=len(b),observado=datetime.datetime.now(datetime.timezone.utc).isoformat()),ensure_ascii=False,indent=2))
        return st,b,ct
r=R(rps=1)
out=[]
for n,ano in [('77544','1976'),('77620','1976'),('78587','1976')]:
    total,docs=cam.pagina(r,1,'dpl',{'tipo':'Decreto','numero':n,'ano':ano})
    item={'numero':n,'total_busca':total,'resultados':[]}
    for d in docs:
        if not re.search(r'/decreto-'+n+'-',d['url']):continue
        s=cam.obter(r,d['url'])
        h=hashlib.sha256(s.encode()).hexdigest(); (P/(h+'.html')).write_text(s)
        links=[]
        for u,t in re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',s,re.S|re.I):
            url=urllib.parse.urljoin(d['url'],__import__('html').unescape(u))
            if '/legin/' in url and ('.pdf' in url.lower() or 'publicacaooriginal' in url.lower()):
                links.append({'url':url,'rotulo':cam.texto(t)})
        item['resultados'].append(dict(d,metadata_SHA=h,links=links))
    out.append(item)
    (P/'busca-metadados-links.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
    print(json.dumps(item,ensure_ascii=False),flush=True)

for item in out:
    for d in item["resultados"]:
        for l in d["links"]:
            s=cam.obter(r,l["url"]);h=hashlib.sha256(s.encode()).hexdigest();(P/(h+".html")).write_text(s);(P/(item["numero"]+"-texto-camara.txt")).write_text(cam.texto(cam.corpo_norma(s)))
