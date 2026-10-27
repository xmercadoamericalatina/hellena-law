"""Índice auxiliar reproduzível de cabeçalhos de um baseline Git congelado.

Evita reler dezenas de milhares de documentos a cada lote. Apenas os cinco
campos de identidade/proveniência são armazenados; o cache nunca publica texto.
"""
import gzip
import hashlib
import json
from pathlib import Path
import tempfile


def carregar(raiz, baseline):
    sha = hashlib.sha256(baseline).hexdigest()
    cache = raiz / "reguladores/_indice/auditoria-headers" / (sha + ".json.gz")
    if cache.exists():
        estado = json.loads(gzip.decompress(cache.read_bytes()))
        if estado["baseline_sha256"] != sha:
            raise ValueError("cache de cabeçalhos não corresponde ao baseline")
        return estado["documentos"]
    documentos = []
    for nome in baseline.decode().split("\0"):
        if not nome.startswith("reguladores/") or not nome.endswith(".md"):
            continue
        try:
            with (raiz / nome).open(encoding="utf-8") as f:
                cab = f.read(16384)
            if not cab.startswith("---\n") or "\n---\n" not in cab[4:]:
                continue
            meta = {}
            for linha in cab[4:].split("\n---\n", 1)[0].splitlines():
                k, v = linha.split(":", 1)
                if k not in {"orgao", "tipo", "numero", "data", "fonte"}:
                    continue
                v = v.strip()
                meta[k] = json.loads(v) if v.startswith('"') else v
            documentos.append({"path": nome, "meta": meta})
        except (OSError, ValueError):
            continue
    cache.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=cache.parent, suffix=".tmp", delete=False) as f:
        tmp = Path(f.name)
        f.write(gzip.compress(json.dumps({"baseline_sha256": sha, "documentos": documentos}, ensure_ascii=False).encode()))
    tmp.replace(cache)
    return documentos
