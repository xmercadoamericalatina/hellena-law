"""Registro explícito de documentos preservados mas ainda sem íntegra validada."""
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

REGISTRO = 'scripts/dados/pendencias-integralidade-publicadas.json'


def carregar(raiz, git_index=False):
    if git_index:
        existe = subprocess.run(['git', 'ls-files', '--error-unmatch', '--', REGISTRO],
                                cwd=raiz, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if existe.returncode == 1:
            return {}
        existe.check_returncode()
        raw = subprocess.check_output(['git', 'show', ':' + REGISTRO], cwd=raiz)
    else:
        path = Path(raiz) / REGISTRO
        if not path.exists():
            return {}
        raw = path.read_bytes()
    dados = json.loads(raw)
    if not isinstance(dados.get('pendentes'), list):
        raise ValueError('registro de integralidade sem lista de pendentes')
    saida = {}
    for item in dados['pendentes']:
        nome = item['path']
        p = PurePosixPath(nome)
        if (p.is_absolute() or '..' in p.parts or p.suffix != '.md'
                or p.parts[0] not in {'federal', 'estaduais', 'reguladores', 'jurisprudencia', 'tratados', 'municipais'}
                or any(x.startswith(('_', '.')) for x in p.parts)):
            raise ValueError('caminho inválido no registro de integralidade: ' + nome)
        if nome in saida:
            raise ValueError('pendência duplicada: ' + nome)
        if not item.get('motivo') or not item.get('evidencia'):
            raise ValueError('pendência sem motivo ou evidência: ' + nome)
        if not re.fullmatch('[a-f0-9]{64}', item.get('sha256_md', '')):
            raise ValueError('pendência sem hash do documento auditado: ' + nome)
        saida[nome] = item
    return saida
