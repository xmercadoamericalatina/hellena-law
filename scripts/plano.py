"""O plano do acervo: todo tipo de norma brasileira que deve estar aqui, onde fica e de onde vem.

Este arquivo é a única fonte de verdade sobre o escopo. `scripts/progresso.py` o lê, conta o que
já existe em disco e gera `progresso.svg` e `PROGRESSO.md`. Um tipo de norma que não está nesta
lista não é medido; um que está e tem zero arquivos aparece como lacuna aberta.

`meta=None` indica universo ainda desconhecido e fica fora dos percentuais.
O campo `meta` numérico passa por três estados, nesta ordem. Começa como **estimativa** do tamanho do
universo de cada tipo, montada a partir da numeração mais recente da série e da ordem de grandeza
que a fonte declara — serve para dimensionar a barra, não para afirmar um número oficial. Quando o
índice da fonte é baixado, vira o **tamanho real do índice**: é o caso das séries federais, todas
contadas em `federal/_indice/`. O fim de uma execução não reduz a meta ao volume coletado:
falhas e itens sem texto continuam sendo lacunas. Alterar a meta exige evidência do índice
oficial, com duplicatas e recortes identificados.

`caminho` é relativo à raiz do repositório, aceita `*` (um nível) para varrer as 27 unidades
federativas ou os municípios, e aceita vários caminhos separados por vírgula quando um mesmo item
reúne pastas que as fontes distinguem (lei promulgada e lei constitucional, por exemplo).
"""
import collections

Item = collections.namedtuple("Item", "setor nome caminho meta fase fonte")

# As fases organizam a coleta por escopo e fontes disponíveis.
FASES = {
    1: ("Fase 1 — legislação federal e leis estaduais", "Planalto, Senado, Câmara e assembleias"),
    2: ("Fase 2 — infralegal e jurisprudência", "diários oficiais e portais de órgãos e tribunais"),
    3: ("Fase 3 — direito municipal", "5.571 municípios no cadastro do IBGE, sem índice legislativo central"),
}

PLANO = [
    # ----------------------------------------------------------------- Constituição e leis federais
    Item("Constituição Federal", "Constituição de 1988 (texto vigente)", "constituicao.md", 1, 1,
         "https://www.planalto.gov.br"),
    Item("Constituição Federal", "Constituições históricas (1824, 1891, 1934, 1937, 1946, 1967, 1969)",
         "federal/constituicoes-historicas", 7, 1, "https://www.planalto.gov.br"),
    Item("Constituição Federal", "Emendas constitucionais e de revisão", "federal/emendas-constitucionais", 172, 1,
         "https://normas.leg.br"),

    Item("Leis federais", "Leis ordinárias, numeradas e não numeradas (1822–hoje)", "federal/leis-ordinarias", 16883, 1,
         "Senado (índice) + normas.leg.br (texto)"),
    Item("Leis federais", "Leis complementares", "federal/leis-complementares", 239, 1, "normas.leg.br"),
    Item("Leis federais", "Leis delegadas (série encerrada)", "federal/leis-delegadas", 13, 1, "normas.leg.br"),
    Item("Leis federais", "Leis constitucionais da Carta de 1937 (1938–1946)", "federal/leis-constitucionais", 21, 1,
         "https://www.planalto.gov.br/ccivil_03/LEIS/LCT/Quadro_Lct.htm"),
    Item("Leis federais", "Decretos-leis (série encerrada em 1988)", "federal/decretos-lei", 12378, 1,
         "normas.leg.br"),

    # ------------------------------------------------------------------------- Atos do Congresso
    Item("Atos do Congresso", "Decretos legislativos", "federal/decretos-legislativos", 21775, 1,
         "normas.leg.br"),
    Item("Atos do Congresso", "Medidas provisórias (originais e reedições)", "federal/medidas-provisorias", 7497, 1,
         "Planalto + normas.leg.br"),
    Item("Atos do Congresso", "Resoluções do Senado Federal", "federal/resolucoes-senado", 6578, 1,
         "normas.leg.br"),
    Item("Atos do Congresso", "Resoluções da Câmara dos Deputados", "federal/resolucoes-camara", 2300, 1,
         "camara.leg.br"),
    Item("Atos do Congresso", "Resoluções do Congresso Nacional e da Revisão Constitucional",
         "federal/resolucoes-congresso", 95, 1,
         "normas.leg.br"),
    Item("Atos do Congresso", "Regimentos internos (Senado, Câmara, Congresso)", "federal/regimentos", 3, 1,
         "senado.leg.br, camara.leg.br"),

    # ---------------------------------------------------------- Decretos do Executivo federal
    Item("Decretos do Executivo federal", "Decretos numerados (1889–hoje, as duas séries)",
         "federal/decretos", 139127, 1, "normas.leg.br + Planalto"),
    Item("Decretos do Executivo federal", "Decretos não numerados", "federal/decretos-nao-numerados", 14510, 1,
         "Planalto"),
    Item("Decretos do Executivo federal", "Regulamentos consolidados (RIR, RIPI, Aduaneiro, RPS, PAF)",
         "federal/regulamentos", 20, 1, "Planalto"),

    # ------------------------------------------------------------------ Tratados internacionais
    Item("Tratados internacionais", "Decretos de promulgação de tratados", "tratados/decretos", 4000, 1,
         "Concórdia/MRE + Planalto"),
    Item("Tratados internacionais", "Tratados de direitos humanos (status constitucional/supralegal)",
         "tratados/direitos-humanos", 40, 1, "MRE + Planalto"),
    Item("Tratados internacionais", "Convenções da OIT ratificadas", "tratados/oit", 100, 1, "ilo.org + MTE"),
    Item("Tratados internacionais", "Acordos de bitributação", "tratados/bitributacao", 40, 1, "RFB"),
    Item("Tratados internacionais", "Normas do Mercosul internalizadas", "tratados/mercosul", 1500, 1,
         "mercosur.int"),

    # ---------------------------------------------------------------------------- Tributário
    Item("Infralegal — tributário", "Receita Federal: instruções normativas, portarias, atos declaratórios, soluções de consulta e pareceres normativos",
         "reguladores/rfb", 115238, 2, "RFB — Sijut (23 espécies normativas) e Diário Oficial da União"),
    Item("Infralegal — tributário", "CONFAZ: convênios, protocolos e ajustes SINIEF",
         "reguladores/confaz", 12000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — tributário", "Tesouro Nacional: portarias e instruções",
         "reguladores/stn", 2000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — tributário", "Procuradoria-Geral da Fazenda Nacional",
         "reguladores/pgfn", 1500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — tributário", "CARF: súmulas e resoluções",
         "reguladores/carf", 300, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — tributário", "Ministério da Fazenda: demais atos normativos",
         "reguladores/fazenda", 3000, 2, "Diário Oficial da União (in.gov.br)"),

    # ---------------------------------------------------------------- Trânsito e transportes
    Item("Infralegal — trânsito e transportes", "CONTRAN: resoluções, deliberações e o Manual Brasileiro de Sinalização",
         "reguladores/contran", 1357, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trânsito e transportes", "SENATRAN/DENATRAN: portarias",
         "reguladores/senatran", 1500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trânsito e transportes", "ANTT: resoluções",
         "reguladores/antt", 6000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trânsito e transportes", "ANTAQ: resoluções",
         "reguladores/antaq", 500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trânsito e transportes", "ANAC: resoluções e RBAC",
         "reguladores/anac", 700, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trânsito e transportes", "Ministério dos Transportes: demais atos normativos",
         "reguladores/transportes", 2000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trânsito e transportes", "Ministério de Portos e Aeroportos",
         "reguladores/portos-aeroportos", 800, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trânsito e transportes", "Ministério da Infraestrutura (denominação histórica)",
         "reguladores/ministerio-da-infraestrutura", None, 2, "Diário Oficial da União (órgão literal da publicação)"),

    # --------------------------------------------------------------------------------- Saúde
    Item("Infralegal — saúde", "ANVISA: RDC, instruções normativas e portarias",
         "reguladores/anvisa", 3100, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — saúde", "Ministério da Saúde: portarias GM/MS e consolidadas",
         "reguladores/ms", 30000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — saúde", "Conselho Nacional de Saúde: resoluções",
         "reguladores/cns", 700, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — saúde", "ANS: resoluções normativas",
         "reguladores/ans", 600, 2, "Diário Oficial da União (in.gov.br)"),

    # ---------------------------------------------------------------- Trabalho e previdência
    Item("Infralegal — trabalho e previdência", "Ministério do Trabalho: normas regulamentadoras (NR-1 a NR-38) e portarias",
         "reguladores/mte", 3038, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trabalho e previdência", "INSS: instruções normativas",
         "reguladores/inss", 160, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trabalho e previdência", "Secretaria de Previdência: instruções normativas e portarias",
         "reguladores/sprev", 900, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — trabalho e previdência", "PREVIC: resoluções e instruções",
         "reguladores/previc", 400, 2, "Diário Oficial da União (in.gov.br)"),

    # ------------------------------------------------------------------------- Meio ambiente
    Item("Infralegal — meio ambiente", "CONAMA: resoluções",
         "reguladores/conama", 520, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — meio ambiente", "IBAMA: instruções normativas e portarias",
         "reguladores/ibama", 1500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — meio ambiente", "ICMBio: instruções normativas",
         "reguladores/icmbio", 400, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — meio ambiente", "ANA e CNRH: resoluções",
         "reguladores/ana", 3000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — meio ambiente", "Serviço Florestal Brasileiro: instruções normativas",
         "reguladores/sfb", 200, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — meio ambiente", "Ministério da Agricultura: instruções normativas",
         "reguladores/mapa", 3000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — meio ambiente", "Ministério do Meio Ambiente: demais atos normativos",
         "reguladores/mma", 1500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — meio ambiente", "Ministério da Pesca e Aquicultura",
         "reguladores/pesca", 600, 2, "Diário Oficial da União (in.gov.br)"),

    # ---------------------------------------------------------------------------- Financeiro
    Item("Infralegal — financeiro", "Banco Central e CMN: resoluções e circulares",
         "reguladores/bcb", 10200, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — financeiro", "CVM: instruções e resoluções",
         "reguladores/cvm", 500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — financeiro", "SUSEP e CNSP: circulares e resoluções",
         "reguladores/susep", 1200, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — financeiro", "CADE: resoluções",
         "reguladores/cade", 300, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — financeiro", "COAF: resoluções",
         "reguladores/coaf", 150, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — financeiro", "Conselho Federal de Contabilidade: resoluções",
         "reguladores/cfc", 1800, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — financeiro", "INMETRO: resoluções e instruções",
         "reguladores/inmetro", 2000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — financeiro", "Ministério do Desenvolvimento, Indústria, Comércio e Serviços",
         "reguladores/mdic", 3000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — financeiro", "Ministério do Empreendedorismo e da Microempresa",
         "reguladores/empreendedorismo", 400, 2, "Diário Oficial da União (in.gov.br)"),

    # -------------------------------------------------------------- Infraestrutura e energia
    Item("Infralegal — infraestrutura e energia", "ANEEL: resoluções normativas e homologatórias",
         "reguladores/aneel", 2000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — infraestrutura e energia", "ANP: resoluções",
         "reguladores/anp", 1000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — infraestrutura e energia", "ANATEL: resoluções e atos",
         "reguladores/anatel", 800, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — infraestrutura e energia", "ANM: resoluções (mineração)",
         "reguladores/anm", 300, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — infraestrutura e energia", "Ministério de Minas e Energia, CNPE e CMSE",
         "reguladores/mme", 1500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — infraestrutura e energia", "Ministério das Comunicações",
         "reguladores/comunicacoes", 800, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — infraestrutura e energia", "Ministério das Cidades",
         "reguladores/cidades", 800, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — infraestrutura e energia", "Ministério da Integração e do Desenvolvimento Regional",
         "reguladores/integracao", 800, 2, "Diário Oficial da União (in.gov.br)"),
    # Os universos históricos ainda não têm índice completo. Não preenchem
    # artificialmente as metas estimadas de ministérios atuais/sucessores.
    Item("Infralegal — infraestrutura e energia", "Ministério do Desenvolvimento Regional (denominação histórica)",
         "reguladores/ministerio-do-desenvolvimento-regional", None, 2, "Diário Oficial da União (órgão literal da publicação)"),

    # -------------------------------------------------------------------- Educação e cultura
    Item("Infralegal — educação e cultura", "Conselho Nacional de Educação: resoluções e pareceres",
         "reguladores/cne", 1500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — educação e cultura", "Ministério da Educação: portarias",
         "reguladores/mec", 4000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — educação e cultura", "INEP: portarias e instruções normativas",
         "reguladores/inep", 1200, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — educação e cultura", "CAPES: instruções normativas e portarias",
         "reguladores/capes", 1000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — educação e cultura", "ANCINE: instruções normativas",
         "reguladores/ancine", 500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — educação e cultura", "IPHAN: portarias e instruções normativas",
         "reguladores/iphan", 400, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — educação e cultura", "Ministério da Cultura",
         "reguladores/cultura", 1200, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — educação e cultura", "Ministério do Esporte",
         "reguladores/esporte", 400, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — educação e cultura", "Ministério do Turismo",
         "reguladores/turismo", 600, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — educação e cultura", "Ministério da Ciência, Tecnologia e Inovação",
         "reguladores/mcti", 1500, 2, "Diário Oficial da União (in.gov.br)"),

    # -------------------------------------------------------------------- Justiça e controle
    Item("Infralegal — justiça e controle", "Ministério da Justiça e Segurança Pública",
         "reguladores/mj", 3000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "Controladoria-Geral da União: instruções normativas e portarias",
         "reguladores/cgu", 1200, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "Advocacia-Geral da União: atos normativos",
         "reguladores/agu", 1500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "Ministério Público da União: resoluções e portarias",
         "reguladores/mpu", 1200, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "CNMP: resoluções e recomendações",
         "reguladores/cnmp", 400, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "Defensoria Pública da União",
         "reguladores/dpu", 400, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "Tribunal de Contas da União: instruções normativas e resoluções",
         "reguladores/tcu", 1500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "Conselhos federais de fiscalização profissional (CFM, COFEN, CONFEA/CREA e demais)",
         "reguladores/conselhos-profissionais", 7000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "Atos em rubricas gerais do DOU (órgão discriminado nos metadados)",
         "reguladores/editais-e-avisos,reguladores/entidades-de-fiscalizacao-dos-profission", None, 2,
         "Diário Oficial da União; rubrica e órgão preservados sem atribuir meta de outra série"),
    Item("Infralegal — justiça e controle", "Presidência da República: atos normativos",
         "reguladores/presidencia", 2000, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "Ministério da Gestão e da Inovação em Serviços Públicos",
         "reguladores/gestao", 2500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "Ministério do Planejamento e Orçamento",
         "reguladores/planejamento", 1200, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "Ministério da Defesa e comandos militares",
         "reguladores/defesa", 2500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "Ministério das Relações Exteriores",
         "reguladores/mre", 800, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "Atos administrativos normativos do Poder Judiciário publicados no DOU",
         "reguladores/poder-judiciario", 1500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "Atos administrativos normativos do Poder Legislativo publicados no DOU",
         "reguladores/poder-legislativo", 600, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — justiça e controle", "BNDES e demais estatais com poder normativo",
         "reguladores/bndes", 400, 2, "Diário Oficial da União (in.gov.br)"),

    # ----------------------------------------------------- Direitos e desenvolvimento social
    Item("Infralegal — direitos e desenvolvimento social", "Ministério do Desenvolvimento e Assistência Social",
         "reguladores/mds", 2500, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — direitos e desenvolvimento social", "Ministério dos Direitos Humanos e da Cidadania",
         "reguladores/mdh", 800, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — direitos e desenvolvimento social", "Ministério das Mulheres",
         "reguladores/mulheres", 300, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — direitos e desenvolvimento social", "Ministério da Mulher, da Família e dos Direitos Humanos (denominação histórica)",
         "reguladores/ministerio-da-mulher-da-familia-e-dos-di", None, 2, "Diário Oficial da União (órgão literal da publicação)"),
    Item("Infralegal — direitos e desenvolvimento social", "Ministério da Igualdade Racial",
         "reguladores/igualdade-racial", 300, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — direitos e desenvolvimento social", "Ministério dos Povos Indígenas",
         "reguladores/mpi", 300, 2, "Diário Oficial da União (in.gov.br)"),
    Item("Infralegal — direitos e desenvolvimento social", "Ministério do Desenvolvimento Agrário e Agricultura Familiar",
         "reguladores/mda", 1200, 2, "Diário Oficial da União (in.gov.br)"),
    # ----------------------------------------------------------------- Jurisprudência vinculante
    Item("Jurisprudência vinculante", "Súmulas vinculantes do STF", "jurisprudencia/stf/sumulas-vinculantes", 62, 2,
         "CNJ — Pangea/BNP (precedentes do STF)"),
    Item("Jurisprudência vinculante", "Súmulas do STF", "jurisprudencia/stf/sumulas", 736, 2, "stf.jus.br"),
    Item("Jurisprudência vinculante", "Temas de repercussão geral", "jurisprudencia/stf/repercussao-geral", 1489, 2,
         "CNJ — Pangea/BNP (precedentes do STF)"),
    Item("Jurisprudência vinculante", "Controle concentrado com eficácia erga omnes (ADI, ADC, ADPF, ADO)",
         "jurisprudencia/stf/controle-concentrado", 8000, 2, "stf.jus.br"),
    Item("Jurisprudência vinculante", "Súmulas do STJ", "jurisprudencia/stj/sumulas", 649, 2, "stj.jus.br"),
    Item("Jurisprudência vinculante", "Temas de recursos repetitivos (STJ)", "jurisprudencia/stj/repetitivos", 1474, 2,
         "STJ — dados abertos, Temas.csv (números únicos)"),
    Item("Jurisprudência vinculante", "Súmulas e orientações jurisprudenciais do TST", "jurisprudencia/tst", 1157, 2,
         "tst.jus.br"),
    Item("Jurisprudência vinculante", "Súmulas do TCU, TNU, STM e TSE", "jurisprudencia/outros-tribunais, jurisprudencia/tnu/sumulas", 700, 2,
         "tcu.gov.br, cjf.jus.br, stm.jus.br, tse.jus.br"),
    Item("Jurisprudência vinculante", "Regimentos internos dos tribunais superiores",
         "jurisprudencia/regimentos", 6, 2, "portais dos tribunais"),
    Item("Jurisprudência vinculante", "Temas de uniformização da TNU, incluindo cancelados",
         "jurisprudencia/tnu/uniformizacao", 394, 2, "CNJ — Pangea/BNP (precedentes da TNU)"),
    Item("Súmulas do TRF4", "Súmulas, incluindo canceladas", "jurisprudencia/trf4/sumulas", 136, 2,
         "https://www.trf4.jus.br/trf4/controlador.php?acao=sumulas_trf4"),

    # ----------------------------------------------------------- Estadual: leis (já coletado)
    Item("Leis estaduais e distritais", "Constituições estaduais e Lei Orgânica do DF", "estaduais/*/constituicao, estaduais/*/lei-organica", 27,
         1, "Assembleias e Casas Civis"),
    Item("Leis estaduais e distritais", "Constituições estaduais históricas", "estaduais/*/constituicoes-historicas",
         40, 1, "Assembleias"),
    Item("Leis estaduais e distritais", "Emendas constitucionais estaduais", "estaduais/*/emendas-constitucionais",
         2200, 1, "Assembleias"),
    Item("Leis estaduais e distritais", "Leis ordinárias estaduais", "estaduais/*/leis-ordinarias", 330000, 1,
         "19 scripts, uma fonte por UF"),
    Item("Leis estaduais e distritais", "Leis complementares estaduais", "estaduais/*/leis-complementares", 14000, 1,
         "19 scripts, uma fonte por UF"),
    Item("Leis estaduais e distritais", "Decretos-leis e leis delegadas estaduais",
         "estaduais/*/decretos-lei, estaduais/*/leis-delegadas, estaduais/*/decretos-lei-complementares", 600, 1,
         "Assembleias"),
    Item("Leis estaduais e distritais", "Leis promulgadas, constitucionais e emendas à Lei Orgânica",
         "estaduais/*/leis-promulgadas, estaduais/*/leis-constitucionais, estaduais/*/emendas-lei-organica",
         600, 1, "Assembleias"),

    # ----------------------------------------------------------- Estadual: infralegal (lacuna)
    Item("Infralegal estadual", "Decretos dos governadores (27 UF)", "estaduais/*/decretos, estaduais/*/decretos-nao-numerados", 400000, 2,
         "Casas Civis e diários oficiais estaduais"),
    Item("Infralegal estadual", "Regulamentos do ICMS (RICMS das 27 UF)", "estaduais/*/regulamentos", 27, 2,
         "Secretarias de Fazenda"),
    Item("Infralegal estadual", "Instruções normativas e portarias das SEFAZ", "estaduais/*/instrucoes-normativas",
         50000, 2, "Secretarias de Fazenda"),
    Item("Infralegal estadual", "Resoluções e decisões normativas dos TCE", "estaduais/*/resolucoes-tce", 10000, 2,
         "Tribunais de Contas estaduais"),
    Item("Infralegal estadual", "Resoluções e provimentos dos TJ e das Corregedorias",
         "estaduais/*/resolucoes-tj", 8000, 2, "Tribunais de Justiça"),
    Item("Infralegal estadual", "Regimentos internos das Assembleias", "estaduais/*/regimentos", 27, 2,
         "Assembleias"),
    Item("Infralegal estadual", "Decretos legislativos estaduais", "estaduais/*/decretos-legislativos", 20000, 2,
         "Assembleias (SAPL e sistemas próprios)"),
    Item("Infralegal estadual", "Resoluções das Assembleias", "estaduais/*/resolucoes", 25000, 2,
         "Assembleias (SAPL e sistemas próprios)"),
    Item("Infralegal estadual", "Portarias das administrações estaduais e distrital",
         "estaduais/*/portarias", 60000, 2, "SINJ-DF, Legisla Goiás e sistemas equivalentes"),
    Item("Infralegal estadual", "Deliberações, súmulas administrativas, provimentos e pareceres normativos",
         "estaduais/*/deliberacoes, estaduais/*/sumulas, estaduais/*/provimentos,"
         " estaduais/*/pareceres-normativos", 4000, 2,
         "SINJ-DF, Legisla Goiás e sistemas equivalentes"),

    # --------------------------------------------------------------------------- Municipal
    Item("Legislação municipal", "Leis orgânicas municipais e suas emendas",
         "municipais/*/*/lei-organica, municipais/*/*/emendas-lei-organica", 5571, 3,
         "diários das associações estaduais de municípios"),
    Item("Legislação municipal", "Planos diretores", "municipais/*/*/plano-diretor", 5571, 3, "portais municipais"),
    Item("Legislação municipal", "Códigos tributários municipais", "municipais/*/*/codigo-tributario", 5571, 3,
         "portais municipais"),
    Item("Legislação municipal", "Códigos de obras, posturas e zoneamento", "municipais/*/*/codigos", 16000, 3,
         "portais municipais"),
    Item("Legislação municipal", "Leis ordinárias e complementares municipais (27 capitais primeiro)",
         "municipais/*/*/leis-ordinarias, municipais/*/*/leis-complementares", 8300000, 3,
         "Câmaras municipais"),
    Item("Legislação municipal", "Decretos legislativos municipais", "municipais/*/*/decretos-legislativos", None, 3,
         "SAPL/Interlegis; universo nacional ainda desconhecido"),
    Item("Legislação municipal", "Resoluções municipais", "municipais/*/*/resolucoes", None, 3,
         "SAPL/Interlegis; universo nacional ainda desconhecido"),
    Item("Legislação municipal", "Decretos municipais", "municipais/*/*/decretos", 2000000, 3,
         "prefeituras e diários oficiais"),
]


def por_setor():
    """Agrupa o plano por setor, preservando a ordem em que os setores aparecem."""
    setores = collections.OrderedDict()
    for item in PLANO:
        setores.setdefault(item.setor, []).append(item)
    return setores
