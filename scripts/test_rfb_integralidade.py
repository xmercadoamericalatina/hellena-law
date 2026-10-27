"""Uma errata isolada não pode virar a íntegra da norma identificada na API."""
import unittest

from baixar_rfb import extrair


def documento(texto):
    return {"integro": True, "publicado": True, "internet": True, "ementas": [],
            "outrosSegmentos": [{"ordemSegmentoAto": 1, "original": True,
                                  "omitir": False, "textoIntegra": texto}]}


class IntegralidadeRFB(unittest.TestCase):
    def test_retificacao_isolada_rejeitada_mesmo_declarada_integra(self):
        for titulo in ("Retificação", "RETIFICAÇÃO", "RETIFICAÇÕES", "Errata", "Onde se lê"):
            with self.subTest(titulo=titulo):
                s = f"<p>{titulo}</p><p>No ato anterior, onde se lê artigo primeiro, leia-se artigo segundo. Texto de errata suficientemente longo para ultrapassar a validação mínima de tamanho.</p>"
                with self.assertRaisesRegex(ValueError, "somente retificação"):
                    extrair(documento(s))

    def test_norma_que_retifica_outro_ato_e_preservada(self):
        s = "<p>ATO DECLARATÓRIO Nº 1</p><p>Art. 1º Fica retificado o ato anterior conforme o texto deste artigo normativo próprio.</p><p>Art. 2º Este ato entra em vigor na data de sua publicação.</p>"
        self.assertIn("Art. 1º", extrair(documento(s)))

    def test_fonte_sem_declaracao_de_integra_nao_e_aceita(self):
        doc = documento("<p>Art. 1º Texto normativo.</p>")
        doc["integro"] = False
        with self.assertRaisesRegex(ValueError, "íntegro e público"):
            extrair(doc)


if __name__ == "__main__":
    unittest.main()
