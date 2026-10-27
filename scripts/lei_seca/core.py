"""Rede restrita a fontes oficiais, preservação de evidências e publicação literal."""
import datetime as dt
import gzip
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

VERSION = 1
MAX_BYTES = 16 * 1024 * 1024
BLOCKED = re.compile(r'projeto|proposta|parecer|consulta|jurisprud|s[uú]mula|ac[oó]rd[aã]o|senten[çc]a|decis[aã]o|doutrina|orienta[çc][aã]o|not[ií]cia|mensagem|veto', re.I)
KINDS = re.compile(r'^(?:constitui[çc][aã]o(?: estadual| federal)?|lei(?: org[aâ]nica| ordin[aá]ria| complementar| delegada| constitucional| promulgada)?|emenda(?: constitucional| [àa] (?:constitui[çc][aã]o|lei org[aâ]nica))|decreto(?:[- ]lei| legislativo| executivo)?|medida provis[oó]ria|resolu[çc][aã]o(?: legislativa| do senado federal| do congresso nacional)?|portaria(?: normativa)?|instru[çc][aã]o normativa|regulamento|regimento interno)$', re.I)


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def read_json(path, default=None):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else default


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_bytes(data if isinstance(data, bytes) else data.encode('utf-8'))
    os.replace(tmp, path)


def write_json(path, data):
    atomic(path, canonical(data))


def allowed_kind(kind):
    return bool(KINDS.fullmatch(kind.strip())) and not BLOCKED.search(kind)


def validate_url(url):
    u = urllib.parse.urlsplit(url)
    h = (u.hostname or '').lower()
    if (u.scheme != 'https' or u.username or u.password or u.port not in (None, 443)
            or not (h.endswith('.gov.br') or h.endswith('.leg.br') or h == 'gov.br')):
        raise ValueError('URL fora da política de fontes oficiais HTTPS: ' + url)
    return url


class Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class Network:
    def __init__(self, seconds=1.1, timeout=30):
        self.seconds, self.timeout = seconds, timeout
        self.last = 0.0
        self.blocked = set()
        self.opener = urllib.request.build_opener(Redirect())

    def get(self, url):
        validate_url(url)
        host = urllib.parse.urlsplit(url).hostname
        if host in self.blocked:
            raise ValueError('Fonte bloqueada nesta execução: ' + host)
        # DNS não pode apontar a localhost, redes privadas ou metadata de nuvem.
        for item in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM):
            if not ipaddress.ip_address(item[4][0]).is_global:
                raise ValueError('Endereço não público para fonte oficial')
        for attempt in range(3):
            time.sleep(max(0, self.seconds - (time.monotonic() - self.last)))
            self.last = time.monotonic()
            try:
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'LeisSecasXMercado/1.0 (public legislative archive)',
                    'Accept-Encoding': 'identity', 'Accept': '*/*'})
                with self.opener.open(req, timeout=self.timeout) as response:
                    validate_url(response.url)
                    data = response.read(MAX_BYTES + 1)
                    if len(data) > MAX_BYTES:
                        raise ValueError('Documento acima do limite de 16 MiB')
                    return data, response.headers.get('Content-Type', ''), response.url
            except urllib.error.HTTPError as exc:
                if exc.code in (401, 403, 429):
                    self.blocked.add(host)
                    raise
                if exc.code < 500 or attempt == 2:
                    raise
            except (urllib.error.URLError, TimeoutError):
                if attempt == 2:
                    raise
            time.sleep(2 ** attempt)
        raise RuntimeError('Falha de rede')

    def json(self, url):
        data, _, _ = self.get(url)
        return json.loads(data)


def decode(data, content_type=''):
    m = re.search(r'charset=["\']?([\w-]+)', content_type, re.I)
    if not m:
        m = re.search(rb'charset=["\']?([\w-]+)', data[:4096], re.I)
    enc = m.group(1) if m else 'utf-8'
    if isinstance(enc, bytes):
        enc = enc.decode('ascii')
    for encoding in dict.fromkeys([enc, 'utf-8', 'cp1252']):
        try:
            return data.decode(encoding)
        except (UnicodeError, LookupError):
            pass
    raise ValueError('Codificação não reconhecida sem perda de caracteres')


class LegalHTML(HTMLParser):
    """Texto literal; não executa HTML. Mantém tachados, células e notas da fonte."""
    BLOCKS = {'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'tr', 'li', 'section', 'blockquote'}
    SKIP = {'script', 'style', 'head', 'nav', 'footer', 'noscript', 'iframe', 'object'}
    VOID = {'img', 'br', 'hr', 'meta', 'link', 'input', 'wbr', 'embed', 'source'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.links, self.stack, self.visual = [], [], [], []
        self.header = []
        self.in_title = False
        self.active_link = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        skip = (self.stack[-1][1] if self.stack else False) or tag in self.SKIP
        if tag == 'title':
            self.in_title = True
        if tag == 'a' and attrs.get('href'):
            self.links.append((attrs['href'], ''))
            self.active_link = len(self.links) - 1
        if not skip:
            if tag in self.BLOCKS or tag == 'br':
                self.parts.append('\n')
            if tag in {'td', 'th'}:
                self.parts.append('\t')
            if tag in {'img', 'svg', 'math', 'canvas', 'embed'}:
                self.visual.append(tag)
            if tag in {'strike', 's', 'del'} or 'line-through' in attrs.get('style', '').lower():
                self.parts.append('~~')
                attrs['_strike'] = True
        if tag not in self.VOID:
            self.stack.append((tag, skip, attrs))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == 'a':
            self.active_link = None
        if tag == 'title':
            self.in_title = False
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, skipped, attrs = self.stack[i]
                if not skipped:
                    if attrs.get('_strike'):
                        self.parts.append('~~')
                    if tag in self.BLOCKS:
                        self.parts.append('\n')
                del self.stack[i:]
                break

    def handle_data(self, value):
        if self.active_link is not None:
            href, label = self.links[self.active_link]
            self.links[self.active_link] = (href, label + value)
        if self.in_title:
            self.header.append(value)
        if not self.stack or not self.stack[-1][1]:
            self.parts.append(value.replace('\r', ' ').replace('\n', ' '))

    def text(self):
        lines = [re.sub(r'[ \xa0]+', ' ', x).strip() for x in ''.join(self.parts).split('\n')]
        return '\n\n'.join(x for x in lines if x).strip() + '\n'


def extract(data, content_type, title, number=''):
    if data.startswith(b'%PDF'):
        # Sem atestar OCR ou ignorar anexos/figuras: PDF fica pendente, sem texto publicado.
        raise ValueError('PDF exige validação de integralidade; original preservado')
    if b'\x00' in data[:4096]:
        raise ValueError('Conteúdo binário não autorizado')
    html = decode(data, content_type)
    if not re.search(r'<(?:html|body|p|div)\b', html, re.I):
        raise ValueError('Fonte não é HTML legislativo')
    parser = LegalHTML()
    parser.feed(html)
    text = parser.text()
    # Identidade no título/epígrafe, não em uma referência casual a outra lei no corpo.
    plain = unicodedata.normalize('NFKD', text)
    plain = ''.join(c for c in plain if not unicodedata.combining(c))
    head = plain[:3500]
    if len(text) < 150 or not re.search(r'\bArt(?:igo)?\.?\s*\d', plain, re.I):
        raise ValueError('Sem corpo articulado suficiente; possível índice/bloqueio')
    if number:
        n = re.escape(re.sub(r'\D', '', str(number)))
        compact = re.sub(r'[.,\sº°]', '', head)
        if not re.search(r'(?:LEICOMPLEMENTAR|LEIORDINARIA|DECRETO[-–]?LEI|DECRETOLEGISLATIVO|LEI|EMENDACONSTITUCIONAL|DECRETO|MEDIDAPROVISORIA|RESOLUCAO|PORTARIA|INSTRUCAONORMATIVA)(?:N[O°º]?)?' + n + r'(?!\d)', compact, re.I):
            raise ValueError('Número não confirmado na epígrafe; revisão necessária')
    # Imagens no cabeçalho podem ser brasões. Não atestamos integralidade de anexos gráficos.
    return text, {'elementos_visuais': sorted(set(parser.visual)),
                  'integralidade': 'nao_certificada',
                  'notas_da_fonte': 'Preservadas, sem interpretação ou consolidação própria.'}


def archive(root, data):
    sha = digest(data)
    path = root / 'originais' / sha[:2] / (sha + '.gz')
    if not path.exists():
        atomic(path, gzip.compress(data, mtime=0))
    return path.relative_to(root).as_posix(), sha


def publish(root, entry, data, content_type, url, previous=None):
    raw_path, raw_sha = archive(root, data)
    text, quality = extract(data, content_type, entry['titulo'], entry.get('numero', ''))
    ident = entry['id']
    if not re.fullmatch(r'[a-zA-Z0-9_-]+', ident):
        raise ValueError('Identificador inseguro')
    text_sha = digest(text.encode('utf-8'))
    metadata = {**entry, **quality, 'url_texto': url, 'sha256_original': raw_sha,
                'original': raw_path, 'sha256_texto': text_sha,
                'versao_texto': entry.get('versao_texto', 'versão disponibilizada pela fonte'),
                'vigencia': entry.get('vigencia', 'nao_inferida'),
                'conferido_em': now(), 'politica': 'lei-seca-v1'}
    # Rechecagens sem mudança não criam versões artificiais.
    old = read_json(root / 'metadados' / (ident + '.json'), {})
    changed = old.get('sha256_texto') != text_sha or old.get('sha256_original') != raw_sha
    fence = '`' * max(3, max((len(m.group()) + 1 for m in re.finditer(r'`+', text)), default=3))
    document = '# ' + entry['titulo'].replace('\n', ' ') + '\n\nFonte oficial: ' + url + '\n\n' + fence + 'text\n' + text + fence + '\n'
    if changed:
        atomic(root / 'textos' / (ident + '.md'), document)
        write_json(root / 'versoes' / ident / (raw_sha + '.json'), metadata)
    write_json(root / 'metadados' / (ident + '.json'), metadata)
    return {'sha256_original': raw_sha, 'sha256_texto': text_sha, 'conferido_em': now(),
            'alterado': changed, 'status': 'publicado', 'original': raw_path}
