"""Regressões das identidades divergentes encontradas nos lotes DEC de 1945."""
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import unittest
from unittest.mock import patch

import baixar_federal as coletor
from html2md import convert
from identidade_decreto import divergencia_epigrafe_decreto, extrair_epigrafe_decreto

RAIZ = Path(__file__).resolve().parent.parent
CASOS_REAIS = [
    ("17453", "1945-12-28", "DECRETO N. 17.453 – DE 28 DE DEZEMBRO DE 1944", "17453", "1944-12-28"),
    ("17424", "1945-12-26", "DECRETO N. 17.424 – DE 26 DE DEZEMBRO DE 1944", "17424", "1944-12-26"),
    ("20215", "1945-12-17", "DECRETO Nº 20.251, DE 17 DE DEZEMBRO DE 1945.", "20251", "1945-12-17"),
]


class IdentidadeDecretoTest(unittest.TestCase):
    def test_discrepancias_reais(self):
        for numero, data, epigrafe, encontrado, data_encontrada in CASOS_REAIS:
            with self.subTest(numero=numero):
                erro = divergencia_epigrafe_decreto("DEC-n", numero, data, epigrafe)
                self.assertEqual(erro["identidade_esperada"], {"numero": numero, "data": data})
                self.assertEqual(erro["epigrafe_encontrada"]["numero"], encontrado)
                self.assertEqual(erro["epigrafe_encontrada"]["data"], data_encontrada)

    def test_pontuacao_mes_ordinal_e_complemento(self):
        for epigrafe, numero, data in [
            ("**DECRETO N.º 20.289, DE 31 DE DEZEMBRO DE 1945.**", "20289", "1945-12-31"),
            ("Decreto n° 1.234-A — de 1º de março de 1.945", "1234-A", "1945-03-01"),
            ("DECRETO N. 19.533-A – DE 30 DE AGÔSTO DE 1945", "19533-A", "1945-08-30"),
            ("DECRETO 123, DE 2 DE janeiro DE 2000", "123", "2000-01-02"),
            ("DECRETO Nº 3.413, DE 14 ABRIL DE 2000.", "3413", "2000-04-14"),
            ("DECRETO Nº20,194, DE13DEDEZEMBRODE1945", "20194", "1945-12-13"),
            ("DECRETO Nº 20.110, DE 4DE DEZEMBRO DE 1945", "20110", "1945-12-04"),
        ]:
            with self.subTest(epigrafe=epigrafe):
                extraida = extrair_epigrafe_decreto(epigrafe)
                self.assertIsNotNone(extraida)
                self.assertEqual((extraida["numero"], extraida["data"]), (numero, data))
                self.assertIsNone(divergencia_epigrafe_decreto("DEC-n", numero, data, epigrafe))

    def test_inconclusivo_nao_confirma_por_citacao_ou_dado_parcial(self):
        for texto in [
            "O Presidente cita o DECRETO Nº 123, DE 2 DE JANEIRO DE 2000.",
            "**Art. 1º** Fica alterado o seguinte:\n\nDECRETO Nº 123, DE 2 DE JANEIRO DE 2000.",
            "DECRETO Nº 123, DE JANEIRO DE 2000.",
            "DECRETO Nº 123, DE 31 DE FEVEREIRO DE 2000.",
            "DECRETO-LEI Nº 123, DE 2 DE JANEIRO DE 2000.",
            "DECRETO LEGISLATIVO Nº 123, DE 2 DE JANEIRO DE 2000.",
        ]:
            with self.subTest(texto=texto):
                self.assertIsNone(extrair_epigrafe_decreto(texto))
        self.assertIsNone(divergencia_epigrafe_decreto("LEI-n", "99", "1900-01-01", CASOS_REAIS[0][2]))
        self.assertIsNone(divergencia_epigrafe_decreto("DEC-sn", "99", "1900-01-01", CASOS_REAIS[0][2]))

    def test_processar_retem_markdown_preserva_cache_e_retorna_pendencia(self):
        for numero, data, epigrafe, _, _ in CASOS_REAIS:
            with self.subTest(numero=numero), tempfile.TemporaryDirectory() as tmp:
                bruto = ("<p>" + epigrafe + "</p><p>Art. 1º Regra.</p>").encode()
                d = {"tipo": "DEC-n", "numero": numero, "dataassinatura": "/".join(reversed(data.split("-"))),
                     "id": "teste", "norma": "DEC-" + numero, "normaNome": "Decreto " + numero}
                meta = {"encoding": {"contentUrl": "https://example.invalid/api/binario/teste", "version": "Original"}}
                with patch.object(coletor, "RAIZ", tmp), patch.object(coletor, "obter_metadados", return_value=(coletor.montar(d)["urn"], meta)), patch.object(coletor, "http_get", return_value=(200, bruto)):
                    info = coletor.montar(d)
                    status, slug, extra = coletor.processar(d)
                self.assertEqual(status, "sem_texto")
                self.assertEqual(slug, info["slug"])
                self.assertIn("Epígrafe própria diverge", extra["motivo"])
                self.assertFalse(Path(info["md"]).exists())
                self.assertEqual(bruto, gzip.decompress(Path(info["fonte"]).read_bytes()))

    def test_processar_identidade_valida_grava_normalmente(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(coletor, "RAIZ", tmp):
            bruto = b'<p>DECRETO N. 20.289 - DE 31 DE DEZEMBRO DE 1945.</p><p>Art. 1 Regra.</p>'
            d = {"tipo": "DEC-n", "numero": "20289", "dataassinatura": "31/12/1945", "id": "teste",
                 "norma": "DEC-20289-1945-12-31", "normaNome": "Decreto 20289"}
            meta = coletor.MetadadosFonte(encoding={"contentUrl": "https://example.invalid/api/binario/teste", "version": "Original"})
            path = Path(tmp) / "metadata.json.gz"
            path.write_bytes(gzip.compress(b'{}'))
            meta.captura = {"path": str(path), "sha256": hashlib.sha256(b'{}').hexdigest()}
            info = coletor.montar(d)
            with patch.object(coletor, "obter_metadados", return_value=(info["urn"], meta)), patch.object(coletor, "http_get", return_value=(200, bruto)):
                self.assertEqual("ok", coletor.processar(d)[0])
            self.assertIn("DECRETO N. 20.289", Path(info["md"]).read_text())

    def test_caches_reais_e_manifesto_quando_disponiveis(self):
        manifesto = RAIZ / "federal/_lote_dec1945_20261020.json"
        caches = [RAIZ / f"federal/_fonte/decretos/1945/dec-{n}-{data}.html.gz"
                  for n, data, *_ in CASOS_REAIS]
        if not manifesto.exists() or not all(p.exists() for p in caches):
            self.skipTest("capturas locais de auditoria não distribuídas no acervo Git")
        retidos = json.loads(manifesto.read_text())["retidos"]
        for caso, cache in zip(CASOS_REAIS, caches):
            numero, data, epigrafe, _, _ = caso
            corpo = convert(gzip.decompress(cache.read_bytes()).decode("utf-8", "replace"))
            erro = divergencia_epigrafe_decreto("DEC-n", numero, data, corpo)
            self.assertEqual(erro["epigrafe_encontrada"]["epigrafe"], epigrafe)
            if numero in {"17453", "17424"}:
                registro = next(r for r in retidos if r["urn"].endswith(";" + numero))
                self.assertEqual(registro["epigrafe"], epigrafe)
                self.assertEqual(registro["fonte_html_sha256"], hashlib.sha256(gzip.decompress(cache.read_bytes())).hexdigest())


if __name__ == "__main__":
    unittest.main()
