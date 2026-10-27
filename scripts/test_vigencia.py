"""Regressões de seleção de redações, sem inferir vigência jurídica."""
import hashlib
import json
import re
import unittest

from converter_constituicao import ConstituicaoParser, FONTE, META, RAIZ, documento
from html2md import convert


def paragrafos(source):
    p = ConstituicaoParser()
    p.feed(source)
    p.close()
    p.flush()
    return "\n\n".join(b[1] for b in p.blocks)


class TachadosTest(unittest.TestCase):
    def test_tags_e_css_aninhados_omitidos_so_no_modo_explicito(self):
        source = ('<p>atual <strike>antiga <b>interna</b></strike> '
                  '<del>excluída</del> <s>anterior</s> '
                  '<span style="text-decoration: line-through">substituída</span> final</p>')
        historico = convert(source)
        vigente = convert(source, exclude_struck=True)
        for word in ("antiga", "interna", "excluída", "anterior", "substituída"):
            self.assertIn(word, historico)
            self.assertNotIn(word, vigente)
        self.assertIn("~~", historico)
        self.assertEqual("atual final\n", vigente)

    def test_tachado_em_tabela_e_herdado(self):
        source = ('<table><tr><td><strike>valor antigo</strike>valor atual</td>'
                  '<td style="text-decoration:line-through">célula antiga</td></tr></table>')
        vigente = convert(source, exclude_struck=True)
        self.assertIn("valor atual", vigente)
        self.assertNotIn("antigo", vigente)
        self.assertNotIn("célula antiga", vigente)
        self.assertIn("<del>valor antigo</del>", convert(source))
        self.assertNotIn("valor atual", convert('<strike>' + source + '</strike>', exclude_struck=True))

    def test_revogado_nao_exclui_norma_ou_nota_por_palavra(self):
        source = '<p>Art. 2º O regulamento anterior fica revogado.</p><p>Art. 3º (Revogado pela EC 1)</p>'
        result = convert(source, exclude_struck=True)
        self.assertIn("O regulamento anterior fica revogado.", result)
        self.assertIn("**Art. 3º** (Revogado pela EC 1)", result)

    def test_mantem_redacao_futura_nao_tachada_e_nota_de_vigencia(self):
        source = '<p>Art. 1º Regra atual.</p><p>Art. 1º Regra futura. (Vigência em 2030)</p>'
        result = convert(source, exclude_struck=True)
        self.assertIn("Regra atual.", result)
        self.assertIn("Regra futura. (Vigência em 2030)", result)


class ConstituicaoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = (RAIZ / "fonte/constituicao.htm").read_bytes().decode("cp1252")
        cls.meta = json.loads(META.read_text(encoding="utf-8"))
        cls.raw = FONTE.read_bytes()
        cls.md = documento(cls.raw, cls.meta)

    def trecho_antigo(self, needle):
        index = self.old.index(needle)
        start = self.old.lower().rfind("<p", 0, index)
        end = self.old.lower().index("</p>", index) + 4
        return self.old[start:end]

    def test_real_art117_recupera_so_rotulo_revogado(self):
        fragment = self.trecho_antigo("Art. 117. O mandato dos representantes")
        result = paragrafos(fragment)
        self.assertIn("Art. 117. (Revogado pela Emenda Constitucional nº 24, de 1999)", result)
        self.assertNotIn("três anos", result)

    def test_real_art82_nao_inventa_dispositivo_atual_a_partir_de_nota(self):
        fragment = self.trecho_antigo("Art. 82. O mandato do Presidente da República é de cinco anos")
        result = paragrafos(fragment)
        self.assertIn("Vide Emenda Constitucional de Revisão", result)
        self.assertNotIn("Art. 82", result)
        self.assertNotIn("cinco anos", result)

    def test_real_css_de_cabecalho_obsoleto(self):
        fragment = self.trecho_antigo("DOS SERVIDORES PÚBLICOS MILITARES")
        self.assertEqual("", paragrafos(fragment))

    def test_snapshot_integro_e_saida_reproduzivel(self):
        self.assertEqual(self.meta["sha256"], hashlib.sha256(self.raw).hexdigest())
        self.assertEqual(self.md, (RAIZ / "constituicao.md").read_text(encoding="utf-8"))
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            documento(self.raw + b' ', self.meta)
        for evidence in self.meta["fontes_complementares"]:
            self.assertEqual(evidence["sha256"], hashlib.sha256((RAIZ / evidence["arquivo"]).read_bytes()).hexdigest())

    def test_nao_reintroduz_redacoes_antigas_e_preserva_revogacoes(self):
        self.assertNotIn("~~", self.md)
        self.assertNotIn("é de cinco anos, vedada a", self.md)
        self.assertNotIn("com auto aplicabilidade para a União", self.md)
        self.assertIn("**Art. 171.** (Revogado pela Emenda Constitucional nº 6, de 1995)", self.md)
        before_adct = self.md.split("# ATO DAS DISPOSIÇÕES", 1)[0]
        self.assertEqual(1, len(re.findall(r"^\*\*Art\. 82\.\*\*", before_adct, re.M)))
        self.assertEqual(1, len(re.findall(r"^\*\*Art\. 239\.\*\*", before_adct, re.M)))

    def test_ec141_preserva_vacatio_e_aviso_sobre_implementacao_gradual(self):
        art7 = self.md.split("**Art. 7º**", 1)[1].split("**Art. 8º**", 1)[0]
        self.assertIn("40 (quarenta) horas semanais", art7)
        self.assertIn("XV - repouso semanal remunerado, preferencialmente aos domingos;", art7)
        self.assertIn("(Vide Emenda Constitucional nº 141, de 2026) (Vigência)", art7)
        self.assertNotIn("XV - repouso semanal remunerado de 2", art7)
        self.assertIn("implementação gradual", self.md)
        self.assertIn("art. 10, I", self.md)


if __name__ == "__main__":
    unittest.main()
