---
titulo: "Ato Declaratório Executivo Cofis nº 35, de 8 de novembro de 2024"
orgao: "Coordenação-Geral de Fiscalização"
tipo: "Ato Declaratório Executivo"
numero: "35"
data: "2024-11-08"
revogada: false
evidencia_revogacao: "vigente:true"
vigente_fonte: true
versao_texto: "publicação original — visão original da fonte"
publicacao: "Publicado(a) no DOU de 14/11/2024, seção 1, página 69"
data_publicacao: "2024-11-14"
fonte: "https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/141589/visao/original"
fonte_api: "https://normasinternet2.receita.fazenda.gov.br/api/consulta-externa/ato/141589/visao/original"
fonte_indice: "https://normas.receita.fazenda.gov.br/api/indexacao/ato/pesquisar"
id_rfb: "141589"
sha256_texto: "20df99ba174be5d2ec44b998ec7bdf26df0475b5525d6ede5d537c7d9409bbba"
baixado_em: "2026-10-16"
---
# Ato Declaratório Executivo Cofis nº 35, de 8 de novembro de 2024

Dispõe sobre o leiaute do Programa Gerador da Declaração do Imposto sobre a Renda Retido na Fonte (PGD Dirf 2025).

O COORDENADOR-GERAL DE FISCALIZAÇÃO, no uso das atribuições que lhe conferem os incisos I e II do art. 121 e inciso II do art. 358 do Regimento Interno da Secretaria Especial da Receita Federal do Brasil, aprovado pela Portaria ME nº 284, de 27 de julho de 2020, e tendo em vista o disposto na Instrução Normativa RFB nº 1.990, de 18 de novembro de 2020, declara:

**Art.1º** Fica aprovado o leiaute aplicável aos campos, registros e arquivos da Declaração do Imposto sobre a Renda Retido na Fonte (Dirf 2025) para apresentação das informações relativas ao ano calendário de 2024.

**Art.2º** A importação de dados pelo PGD Dirf 2025 deve ser efetuada em observância ao leiaute do arquivo constante do Anexo Único deste Ato Declaratório.

**Art.3º** Este Ato Declaratório Executivo entra em vigor na data de sua publicação no Diário Oficial da União.

RICARDO DE SOUZA MOREIRA

Anexo Único



ANEXO ÚNICO LEIAUTE DO ARQUIVO Declaração do Imposto sobre a Renda Retido na Fonte – Dirf 1. Regras gerais

Estas regras devem ser respeitadas em todos os arquivos gerados, quando não excepcionadas por regra específica referente a um dado registro e explicitada em suas observações.

Nº Regra de Descrição preenchimento

ALFANUMÉRICO (C): representados por “C” - todos os caracteres, excetuados o caractere “|” (pipe ou barra vertical). 1 Formato dos campos NUMÉRICO (N): representados por “N” – pode conter apenas os valores de zero a nove.

Campos numéricos (D) Devem ser informados conforme o padrão ano, mês e dia (AAAAMMDD), 2 cujo conteúdo excluindo-se quaisquer caracteres de separação (tais como “.”, “/”, “-”, etc.); representa data

Os campos numéricos com número de inscrição (CNPJ e CPF) ou códigos de Campos numéricos com receita deverão ser informados com todos os dígitos, inclusive os zeros à 3 número de inscrição ou esquerda; códigos de receita As máscaras (caracteres especiais de formatação, tais como “.”, “/”, “-”, etc.) não devem ser informadas.

Devem ser informados com até 13 posições, representando 11 posições inteiras e 2 decimais; Campos numéricos Os zeros não significativos não devem ser informados;

referentes a valores Os caracteres “.” (ponto) e “,” (vírgula) não devem ser informados;

Todos os valores monetários devem estar expressos em reais.

Os campos com conteúdo alfanumérico nos quais se faz necessário registrar números ou códigos de identificação (Exemplo: Número de Identificação Fiscal Campos alfanuméricos – NIF) deverão seguir a regra de formação e tamanho definidos pelo 5 com números ou respectivo órgão regulador; códigos de identificação As máscaras (caracteres especiais de formatação, tais como “.”, “/”, “-”, etc.) não devem ser informadas.

Ao final de cada campo (inclusive o último de cada registro) deve ser inserido 6 Formação dos campos o caractere delimitador “|” (pipe ou barra vertical: caractere 124 da Tabela ASCII);

O caractere delimitador “|” (barra vertical) não deve ser incluído como parte integrante do conteúdo de quaisquer campos numéricos, datas ou alfanuméricos;

Na ausência de informação, o campo vazio (campo sem conteúdo, nulo e com valor zero) deverá ser iniciado com o caractere “|” (barra vertical) e imediatamente encerrado com o mesmo caractere “|” (barra vertical) delimitador de campo.

7 Formação dos registros Cada registro deve necessariamente ocupar apenas uma linha no arquivo.

Preenchimento fixo: o campo deve ser preenchido com o tamanho exato. Preenchimento dos 8 Preenchimento variável: o campo pode ter variação de tamanho de campos preenchimento.

Deve ser informado com até 4 posições, representando 3 posições inteiras e 1 Campo numérico decimal; 9 referente a quantidade Os zeros não significativos não devem ser informados; de meses Os caracteres “.” (ponto) e “,” (vírgula) não devem ser informados.

2. Estrutura de arquivo

2.1 Estrutura completa de uma declaração de Pessoa Física

Dirf – Declaração do imposto sobre a renda retido na fonte

RESPO – Responsável pelo preenchimento

DECPF – Declarante pessoa física IDREC – Identificação do código de receita

BPFDEC – Beneficiário pessoa física do declarante

RTRT – Rendimentos tributáveis – Rendimento tributável

RTPO – Rendimentos tributáveis – Dedução – Previdência oficial

RTDP – Rendimentos tributáveis – Dedução – Dependentes

RTDS – Rendimentos tributáveis – Dedução – Desconto simplificado mensal

RTIRF – Rendimentos tributáveis – imposto sobre a renda retido na fonte

CJAC – Compensação de imposto por decisão judicial – Ano-calendário CJAA – Compensação de imposto por decisão judicial – Anos anteriores

ESRT – Tributação com exigibilidade suspensa – Rendimento tributável

ESPO – Tributação com exigibilidade suspensa – Dedução – Previdência oficial

ESDP – Tributação com exigibilidade suspensa – Dedução – Dependentes

ESDS – Tributação com exigibilidade suspensa – Dedução – Desconto simplificado mensal

ESIR – Tributação com exigibilidade suspensa – Imposto sobre a renda na fonte

ESDJ – Tributação com exigibilidade suspensa – Depósito judicial

INFPC – Informações de previdência complementar

RTPP – Rendimentos tributáveis – Dedução – Previdência privada

RTFA – Rendimentos tributáveis – Dedução – FAPI

ESPP – Tributação com exigibilidade suspensa – Dedução – Previdência privada

ESFA – Tributação com exigibilidade suspensa – Dedução – FAPI

INFPA – Informações do beneficiário da pensão alimentícia

RTPA – Rendimentos tributáveis – Dedução – Pensão alimentícia

ESPA – Tributação com exigibilidade suspensa – Dedução – Pensão alimentícia

RIDAC – Rendimentos isentos – Diária e Ajuda de custo

RIIRP – Rendimentos isentos – Indenizações por rescisão de contrato de trabalho, inclusive a título de PDV

RIAP – Rendimentos isentos – Abono pecuniário

RIP65 – Rendimentos isentos – Parcela isenta de aposentadoria (65 anos ou mais)

RIJMRE – Rendimentos isentos – Juros de mora recebidos, devidos pelo atraso no pagamento de remuneração por exercício de emprego, cargo ou função

RIO – Rendimentos isentos anuais – Outros

BPJDEC – Beneficiário pessoa jurídica do declarante

RTRT – Rendimentos tributáveis – Rendimento tributável

RTIRF – Rendimentos tributáveis – Imposto sobre a renda retido na fonte

RRA – Rendimentos recebidos acumuladamente

IDREC – Identificação do código de receita

BPFRRA – Beneficiário pessoa física do rendimento recebido acumuladamente

RTRT – Rendimentos tributáveis – Rendimento tributável

RTPO – Rendimentos tributáveis – Dedução – Previdência oficial

RTIRF – Rendimentos tributáveis – Imposto sobre a renda retido na fonte

DAJUD – Despesa com ação judicial QTMESES – Quantidade de meses

RIJMRE – Rendimentos isentos – Juros de mora recebidos, devidos pelo atraso no pagamento de remuneração por exercício de emprego, cargo ou função

INFPA – Informações do beneficiário da pensão alimentícia

RTPA – Rendimentos tributáveis – Dedução – Pensão alimentícia

SCP – Informações da sociedade em conta de participação

BPFSCP – Beneficiário pessoa física da sociedade em conta de participação

RISCP – Lucros e dividendos pagos ao sócio da sociedade em conta de participação

BPJSCP – Beneficiário pessoa jurídica da sociedade em conta de participação

RISCP – Lucros e dividendos pagos ao sócio da sociedade em conta de participação

PSE – Plano privado de assistência à saúde – coletivo empresarial

OPSE – Operadora de plano privado de assistência à saúde – coletivo empresarial

TPSE – Titular de plano privado de assistência à saúde – coletivo empresarial

RTPSE – Reembolso do titular do plano de assistência à saúde – coletivo empresarial

DTPSE – Dependente do titular de plano privado de assistência à saúde – coletivo empresarial

RDTPSE – Reembolso do dependente do titular do plano de assistência à saúde – coletivo empresarial

RPDE – Rendimentos pagos a residentes ou domiciliados no exterior

BRPDE – Beneficiário dos rendimentos pagos a residentes ou domiciliados no exterior

VRPDE – Valores de rendimentos pagos a residentes ou domiciliados no exterior

INF – Informações complementares para o comprovante de rendimentos

FIMDirf – Término da declaração

2.2 Estrutura completa de uma declaração de Pessoa Jurídica

Dirf – Declaração do imposto sobre a renda retido na fonte

RESPO – Responsável pelo preenchimento

DECPJ – Declarante pessoa jurídica

IDREC – Identificação do código de receita

BPFDEC – Beneficiário pessoa física do declarante

RTRT – Rendimentos tributáveis – Rendimento tributável

RTPO – Rendimentos tributáveis – Dedução – Previdência oficial

RTDP – Rendimentos tributáveis – Dedução – Dependentes

RTDS – Rendimentos tributáveis – Dedução – Desconto simplificado mensal

RTIRF – Rendimentos tributáveis – Imposto sobre a renda retido na fonte

CJAC – Compensação de imposto por decisão judicial – Ano-calendário

CJAA – Compensação de imposto por decisão judicial – Anos anteriores

ESRT – Tributação com exigibilidade suspensa – Rendimento tributável

ESPO – Tributação com exigibilidade suspensa – Dedução – Previdência oficial

ESDP – Tributação com exigibilidade suspensa – Dedução – Dependentes

ESDS – Tributação com exigibilidade suspensa – Dedução – Desconto simplificado mensal

ESIR – Tributação com exigibilidade suspensa – Imposto sobre a renda na fonte

ESDJ – Tributação com exigibilidade suspensa – Depósito judicial

INFPC – Informações de previdência complementar

RTPP – Rendimentos tributáveis – Dedução – Previdência privada

RTFA – Rendimentos tributáveis – Dedução – FAPI

RTSP – Rendimentos tributáveis – Dedução – Fundo de previdência do servidor público

RTEP – Rendimentos tributáveis – Dedução – Contribuição do ente público patrocinador

ESPP – Tributação com exigibilidade suspensa – Dedução – Previdência privada

ESFA – Tributação com exigibilidade suspensa – Dedução – FAPI

ESSP – Tributação com exigibilidade suspensa – Dedução – Fundo de previdência do servidor público

ESEP – Tributação com exigibilidade suspensa – Dedução – Contribuição do ente público patrocinador

INFPA – Informações do beneficiário da pensão alimentícia

RTPA – Rendimentos tributáveis – Dedução – Pensão alimentícia

ESPA – Tributação com exigibilidade suspensa – Dedução – Pensão alimentícia

RIDAC – Rendimentos isentos – Diária e Ajuda de custo

RIIRP – Rendimentos isentos – Indenizações por rescisão de contrato de trabalho, inclusive a título de PDV

RIAP – Rendimentos isentos – Abono pecuniário

RIMOG – Rendimentos isentos – Pensão, aposentadoria ou reforma por moléstia grave

RIP65 – Rendimentos isentos – Parcela isenta de aposentadoria (65 anos ou mais)

RIBMR – Rendimentos isentos – Bolsa de estudo recebida por médico-residente

RICAP – Rendimentos isentos – Complementação de aposentadoria de previdência complementar correspondente às contribuições efetuadas no período de 1º de janeiro de 1989 a 31 de dezembro de 1995

RIRPC – Rendimentos isentos – Resgate de previdência complementar por portador de moléstia grave

RIL96 – Rendimentos isentos anuais – Lucros e dividendos pagos a partir de 1996

RIPTS – Rendimentos isentos anuais – Valores pagos a titular ou sócio ou empresa de pequeno porte, exceto pró-labore e aluguéis

RIJMRE – Rendimentos isentos – Juros de mora recebidos, devidos pelo atraso no pagamento de remuneração por exercício de emprego, cargo ou função

RIO – Rendimentos isentos anuais – Outros

BPJDEC – Beneficiário pessoa jurídica do declarante

RTRT – Rendimentos tributáveis – Rendimento tributável

RTIRF – Rendimentos tributáveis – Imposto sobre a renda retido na fonte

VPEIM – Valores pagos às entidades imunes ou isentas – IN RFB 1.234/2012

RIMUN – Rendimentos imunes – art. 4º, inciso III

RISEN – Rendimentos isentos – art. 4º, inciso IV

FCI – Fundo ou clube de investimento

IDREC – Identificação do código de receita

BPFFCI – Beneficiário pessoa física do fundo ou clube de investimento

RTRT – Rendimentos tributáveis – Rendimento tributável

RTIRF – Rendimentos tributáveis – Imposto sobre a renda retido na fonte

CJAC – Compensação de imposto por decisão judicial – Ano-calendário

CJAA – Compensação de imposto por decisão judicial – Anos Anteriores

ESRT – Tributação com exigibilidade suspensa – Rendimento tributável

ESIR – Tributação com exigibilidade suspensa – Imposto sobre a renda na fonte

ESDJ – Tributação com exigibilidade suspensa – Depósito judicial

RIP65 – Rendimentos isentos – Parcela isenta de aposentadoria (65 anos ou mais)

RIMOG – Rendimentos isentos – Pensão, aposentadoria ou reforma por moléstia grave

RICAP – Rendimentos isentos – Complementação de aposentadoria de previdência complementar correspondente às contribuições efetuadas no período de 1º de janeiro de 1989 a 31 de dezembro de 1995

RIO – Rendimentos isentos anuais – Outros

BPJFCI – Beneficiário pessoa jurídica do fundo ou clube de investimento

RTRT – Rendimentos tributáveis – Rendimento tributável

RTIRF – Rendimentos tributáveis – Imposto sobre a renda retido na fonte

PROC – Processo da justiça do trabalho/federal/estadual/Distrito Federal

IDREC – Identificação do código de receita

BPFPROC – Beneficiário pessoa física do processo da justiça do trabalho/federal/estadual/Distrito Federal

RTRT – Rendimentos tributáveis – Rendimento tributável

RTPO – Rendimentos tributáveis – Dedução – Previdência oficial

RTDP – Rendimentos tributáveis – Dedução – Dependentes

RTDS – Rendimentos tributáveis – Dedução – Desconto simplificado mensal

RTIRF – Rendimentos tributáveis – Imposto sobre a renda retido na fonte

CJAC – Compensação de imposto por decisão judicial – Ano-calendário

CJAA – Compensação de imposto por decisão judicial – Anos Anteriores

ESRT – Tributação com exigibilidade suspensa – Rendimento tributável

ESPO – Tributação com exigibilidade suspensa – Dedução – Previdência oficial

ESDP – Tributação com exigibilidade suspensa – Dedução – Dependentes

ESDS – Tributação com exigibilidade suspensa – Dedução – Desconto simplificado mensal

ESIR – Tributação com exigibilidade suspensa – Imposto sobre a renda na fonte

ESDJ – Tributação com exigibilidade suspensa – Depósito judicial

RTPP – Rendimentos tributáveis – Dedução – Previdência privada

RTFA – Rendimentos tributáveis – Dedução – FAPI

RTSP – Rendimentos tributáveis – Dedução – Fundo de previdência do servidor público

ESPP – Tributação com exigibilidade suspensa – Dedução – Previdência privada

ESFA – Tributação com exigibilidade suspensa – Dedução – FAPI

ESSP – Tributação com exigibilidade suspensa – Dedução – Fundo de previdência do servidor público

RTPA – Rendimentos tributáveis – Dedução – Pensão alimentícia

ESPA – Tributação com exigibilidade suspensa – Dedução – Pensão alimentícia

RIMOG – Rendimentos isentos – Pensão, aposentadoria ou reforma por moléstia grave

RIJMRE – Rendimentos isentos – Juros de mora recebidos, devidos pelo atraso no pagamento de remuneração por exercício de emprego, cargo ou função

RIRSR – Rendimentos pagos sem retenção do IR na fonte – Lei nº 10.833/2003

BPJPROC – Beneficiário pessoa jurídica do processo da justiça do trabalho/federal/estadual/Distrito Federal

RTRT – Rendimentos tributáveis – Rendimento tributável

RTIRF – Rendimentos tributáveis – Imposto sobre a renda retido na fonte

RIRSR – Rendimentos pagos sem retenção do IR na fonte – Lei nº 10.833/2003

RRA – Rendimentos recebidos acumuladamente

IDREC – Identificação do código de receita

BPFRRA – Beneficiário pessoa física do rendimento recebido acumuladamente

RTRT – Rendimentos tributáveis – Rendimento tributável

RTPO – Rendimentos tributáveis – Dedução – Previdência oficial

INFPA – Informações do beneficiário da pensão alimentícia

RTPA – Rendimentos tributáveis – Dedução – Pensão alimentícia

RTIRF – Rendimentos tributáveis – Imposto sobre a renda retido na fonte

RIMOG – Rendimentos isentos – Pensão, aposentadoria ou reforma por moléstia grave

RIP65 – Rendimentos isentos – Parcela isenta de aposentadoria (65 anos ou mais)

RIJMRE – Rendimentos isentos – Juros de mora recebidos, devidos pelo atraso no

pagamento de remuneração por exercício de emprego, cargo ou função

DAJUD – Despesa com ação judicial

QTMESES – Quantidade de meses

SCP – Informações da sociedade em conta de participação

BPFSCP – Beneficiário pessoa física da sociedade em conta de participação

RISCP – Lucros e dividendos pagos ao sócio da sociedade em conta de participação

BPJSCP – Beneficiário pessoa jurídica da sociedade em conta de participação

RISCP – Lucros e dividendos pagos ao sócio da sociedade em conta de participação

PSE – Plano privado de assistência à saúde – coletivo empresarial

OPSE – Operadora de plano privado de assistência à saúde – coletivo empresarial

TPSE – Titular de plano privado de assistência à saúde – coletivo empresarial

RTPSE – Reembolso do titular do plano de assistência à saúde – coletivo empresarial

DTPSE – Dependente do titular de plano privado de assistência à saúde – coletivo empresarial

RDTPSE – Reembolso do dependente do titular do plano de assistência à saúde – coletivo empresarial

RPDE – Rendimentos pagos a residentes ou domiciliados no exterior

BRPDE – Beneficiário dos rendimentos pagos a residentes ou domiciliados no exterior

VRPDE – Valores de rendimentos pagos a residentes ou domiciliados no exterior

INF – Informações complementares para o comprovante de rendimentos

FIMDirf – Término da declaração

3. Leiaute do arquivo

3.1 Registro de identificação da declaração (identificador Dirf)

- Registro obrigatório no arquivo;

- Deve ser o primeiro registro no arquivo;

- Ocorre somente uma vez no arquivo.

1 Identificador de registro C Fixo 4 Dirf Sim

2 Ano referência N Fixo 4 2025 Sim

3 Ano-calendário N Fixo 4 2024 Sim

S – Retificadora 4 Indicador de retificadora C Fixo 1 Sim N – Original

5 Número do recibo N Fixo 12 - Não

Identificador de 6 C Fixo 7 R6GP3ZA Sim estrutura do leiaute

Observações:

Ordem Campo Descrição

O preenchimento será obrigatório se o campo de ordem 4 igual a 5 Número do recibo “S” e declaração transmitida sem o uso de certificação digital.

3.2 Registro do Responsável pelo preenchimento da declaração (identificador RESPO)

- Registro obrigatório no arquivo;

- Deve ser o segundo registro no arquivo;

- Ocorre somente uma vez no arquivo.

1 Identificador de registro C Fixo 5 RESPO Sim

2 CPF N Fixo 11 - Sim

3 Nome C Variável 60 - Sim

4 DDD N Fixo 2 - Sim

5 Telefone N Variável 9 - Sim

6 Ramal N Variável 6 - Não

7 Fax N Variável 9 - Não

8 Correio eletrônico C Variável 50 - Não

Observações:

Ordem Campo Descrição

4 DDD O primeiro algarismo deve ser diferente de zero.

5 Telefone Deve ser preenchido com oito ou nove algarismos.

7 Fax Deve ser preenchido com oito ou nove algarismos.

3.3 Registro de identificação do declarante pessoa física (identificador DECPF)

- Registro obrigatório no arquivo para declarante pessoa física;

- Deve ser o terceiro registro no arquivo;

- Ocorre somente uma vez no arquivo;

- Não pode ser informado se existir o registro tipo DECPJ.

1 Identificador de registro C Fixo 5 DECPF Sim

2 CPF N Fixo 11 - Sim

3 Nome C Variável 60 - Sim

S – Pagou Indicador de declarante rendimentos a de rendimentos pagos a 4 C Fixo 1 residentes ou Sim residentes ou domiciliados no domiciliados no exterior exterior

N – Não pagou rendimentos a residentes ou domiciliados no exterior

S – Titular de serviços notariais e de Indicador de Titular de registros 5 Serviços Notariais e de C Fixo 1 Sim Registros N – Não é titular de serviços notariais e de registros

Indicador de plano S – Existe pagamento privado de assistência à de valor pelo 6 C Fixo 1 Sim saúde – coletivo titular/dependente do empresarial plano de saúde

N – Não existe pagamento de valor pelo titular/dependente do plano de saúde

Indicador de sócio S – Sócio ostensivo ostensivo responsável 7 C Fixo 1 N – Não é sócio Sim por sociedade em conta de participação – SCP ostensivo

S – Encerramento de espólio/saída definitiva do país Indicador de situação 8 C Fixo 1 N – Não é Sim especial da declaração encerramento de espólio/saída definitiva do país

9 Data do Evento D Fixo 8 - Não

1 – Encerramento de espólio 10 Tipo de Evento N Fixo 1 Não 2 – Saída definitiva do Brasil

S – Declarante Indicador de declarante falecido 11 C Fixo 1 Sim falecido N – Declarante não falecido

12 Data do óbito D Fixo 8 - Não

0 – Sem espólio 13 Situação do espólio N Fixo 1 1 – Espólio não Não encerrado

14 CPF do inventariante N Fixo 11 - Não

15 Nome do inventariante C Variável 60 - Não

Observações:

Ordem Campo Descrição

9 Data do Evento O preenchimento será obrigatório se o campo de ordem 8 igual a “S”.

10 Tipo de Evento O preenchimento será obrigatório se o campo de ordem 8 igual a “S”.

11 Indicador de declarante falecido Deve ser preenchido com “S” se o campo de ordem 8 igual a “S” e campo de ordem 10 igual a 1

13 Situação do espólio Permitido somente para as declarações normais

Para o encerramento de espólio a declaração será sempre de situação especial;

Declarante falecido – indicador igual a SIM

Situação 1 – sem espólio

- Apresentar declaração normal do ano-calendário;

- Informar data do óbito e situação do espólio igual a 0;

Observação: não serão aceitas declarações para anos posteriores ao ano da data do óbito sem espólio;

Situação 2 – com espólio não encerrado

- Apresentar declaração normal do ano-calendário;

- Informar data do óbito e situação do espólio igual a 1;

Observação: serão aceitas declarações para anos posteriores ao ano da data do óbito até que seja apresentada uma declaração de situação especial – encerramento de espólio;

Situação 3 – encerramento de espólio

- Apresentar declaração de situação especial do ano-calendário; Observação: os campos 12 a 15 não serão preenchidos;

3.4 Registro de identificação do declarante pessoa jurídica (identificador DECPJ)

- Registro obrigatório no arquivo para declarante pessoa jurídica;

- Deve ser o terceiro registro no arquivo;

- Ocorre somente uma vez no arquivo;

- Não pode ser informado se existir o registro tipo DECPF.

1 Identificador de registro C Fixo 5 DECPJ Sim

2 CNPJ N Fixo 14 - Sim

3 Nome empresarial C Variável 150 - Sim

0 – Pessoa jurídica 4 Natureza do declarante N Fixo 1 Sim de direito privado

1 – Órgãos, autarquias e fundações da administração pública federal

2 – Órgãos, autarquias e fundações da administração pública estadual, municipal ou do Distrito Federal 3 – Empresa pública ou sociedade de economia mista federal

4 – Empresa pública ou sociedade de economia mista estadual, municipal ou do Distrito Federal

8 – Entidade com alteração de natureza jurídica (uso restrito)

CPF responsável 5 N Fixo 11 - Sim perante o CNPJ

Indicador de sócio S – Sócio ostensivo ostensivo responsável 6 C Fixo 1 N – Não é sócio Sim por sociedade em conta de participação – SCP ostensivo

S – Depositário de Indicador de declarante crédito decorrente de depositário de crédito decisão judicial 7 C Fixo 1 Sim decorrente de decisão N – Não é depositário judicial de crédito decorrente de decisão judicial

Indicador de declarante S – Instituição de instituição administradora ou administradora ou 8 C Fixo 1 intermediadora de Sim intermediadora de fundo fundo ou clube de ou clube de investimento investimento

N – Não é instituição administradora ou intermediadora de fundo ou clube de investimento

S – Pagou Indicador de declarante rendimentos a de rendimentos pagos a 9 C Fixo 1 residentes ou Sim residentes ou domiciliados no domiciliados no exterior exterior

N – Não pagou rendimentos a residentes ou domiciliados no exterior

S – Existe Indicador de plano pagamento de valor privado de assistência à 10 C Fixo 1 pelo Sim saúde – coletivo titular/dependente do empresarial plano de saúde

N – Não existe pagamento de valor pelo titular/dependente do plano de saúde

Indicador de entidade S – Existe em que a União detém pagamento de 11 maioria do capital social C Fixo 1 valores a entidades Sim sujeito a voto, recebe imunes/isentas recursos do Tesouro

Nacional e está N – Não existe obrigada a registrar a pagamento de execução orçamentária valores a entidades no Siafi (IN 1.234/2012, imunes/isentas

art. 4º, incisos III e IV)

Indicador de fundação S – Fundação pública pública de direito de direito privado privado instituída pela 12 C Fixo 1 N – Não é fundação Sim União, Estados, Municípios ou Distrito pública de direito Federal privado

S – Declaração de Indicador de situação situação especial 13 C Fixo 1 Sim especial da declaração N – Não é declaração de situação especial

14 Data do evento D Fixo 8 - Não

Observações:

Ordem Campo Descrição

Relativamente à natureza do declarante 8 – Entidade com alteração 4 Natureza do declarante de natureza jurídica (uso restrito), esclarecemos:

1. Para declarante que alterou sua natureza jurídica em relação ao ano-calendário e que implique em mudança da natureza do declarante na ficha Informações da Dirf;

2. Para declarante que mudou sua natureza jurídica de órgão público para privado, ou vice-versa. Aplica-se ainda para mudanças entre as esferas governamentais da federação. Por exemplo: órgão público ou pessoa jurídica de direito privado estadual ou municipal que passou a ser federal, ou vice-versa;

3. A declaração deverá ser entregue na RFB.

Indicador de entidade em que a Indicador com a opção “Sim” permitido somente se campo de ordem União detém maioria do capital 4 – Natureza do declarante, igual a “0”, “1”, “3” ou “8”

social sujeito a voto, recebe recursos do Tesouro

Nacional e está obrigada a registrar a execução orçamentária no Siafi (IN 1.234/2012, art. 4º, incisos III e IV)

Indicador de fundação pública Indicador com a opção “S” permitido somente se campo de ordem 4 de direito privado instituída pela – Natureza do declarante, igual a “1”, “2” ou “8”

União, Estados, Municípios ou Distrito Federal Para as demais naturezas do declarante deve ser igual a “N”

O preenchimento será obrigatório se o campo de ordem 13 igual a 14 Data do evento “S”.

3.5 Registro de identificação do código de receita (identificador IDREC)

- Deve ser apresentado com os códigos de receita em ordem crescente;

- Deve estar associado aos registros do tipo DECPF, DECPJ, FCI, PROC ou RRA.

1 Identificador de registro C Fixo 5 IDREC Sim De acordo com a tabela de códigos de 2 Código de receita N Fixo 4 receitas constante Sim na IN que dispõe sobre a Dirf

3.6 Registro de beneficiário pessoa física do declarante (identificador BPFDEC)

- Serão apresentados todos os CPF em ordem crescente;

- Devem ser apresentados antes dos registros com identificador BPJDEC, caso exista o registro;

- Deve estar associado a um registro do tipo IDREC.

1 Identificador de registro C Fixo 6 BPFDEC Sim

2 CPF N Fixo 11 - Sim

3 Nome C Variável 60 - Sim

Data atribuída pelo laudo Não 4 D Fixo 8 - da moléstia grave

S – Existem Sim Indicador de informações 5 identificação do C Fixo 1 detalhadas do alimentando alimentando

N – Não existem informações detalhadas do alimentando

S – Existem Sim Indicador de informações identificação da 6 C Fixo 1 detalhadas da previdência previdência complementar complementar

N – Não existem informações detalhadas da

previdência complementar

Observações: Ordem Campo Descrição

Indicador de identificação do Se campo igual a “S” – deverá constar o registro INFPA seguido do

alimentando registro de valor (RTPA e/ou ESPA) para cada alimentando.

Se campo igual a “N” – não apresentar o registro INFPA; deverão constar os registros de valores (RTPA e/ou ESPA) com o valor total de pensão alimentícia pago a todos os alimentandos do beneficiário.

– As informações detalhadas a que se refere o campo são: CPF, data de nascimento, nome e relação de dependência do alimentando (registro INFPA).

Se campo igual a “S” – deverá constar o registro INFPC seguido do Indicador de identificação da 6 registro de valor (RTPP, RTFA, RTSP e/ou ESPP, ESFA, ESSP) previdência complementar para cada entidade de previdência complementar do beneficiário. Se campo igual a “N” – não apresentar o registro INFPC; deverão constar apenas os registros de valores mensais (RTPP, RTFA, RTSP e/ou ESPP, ESFA, ESSP) com o total dos valores de previdência complementar pagos pelo beneficiário.

– As informações detalhadas a que se refere o campo são: CNPJ e Nome empresarial da entidade de previdência complementar (registro INFPC).

3.7 Registro de beneficiário pessoa jurídica do declarante (identificador BPJDEC)

- Serão apresentados todos os CNPJ em ordem crescente;

- Devem ser apresentados depois dos registros com identificador BPFDEC, caso exista o registro;

- Deve estar associado a um registro do tipo IDREC.

1 Identificador de registro C Fixo 6 BPJDEC Sim

2 CNPJ N Fixo 14 - Sim

3 Nome empresarial C Variável 150 - Sim

3.8 Registro de valores pagos às entidades imunes e isentas (identificador VPEIM)

- Serão apresentados todos os CNPJ em ordem crescente;

- Registro permitido somente para declarante pessoa jurídica; e se campo 12 do registro DECPJ igual a “S”;

1 Identificador de registro C Fixo 5 VPEIM Sim

2 CNPJ N Fixo 14 - Sim

3 Nome empresarial C Variável 150 - Sim

3.9 Registro de identificação do fundo ou clube de investimento (identificador FCI)

- Serão apresentados todos os CNPJ em ordem crescente;

- Deve estar associado ao registro do tipo DECPJ.

1 Identificador de registro C Fixo 3 FCI Sim

2 CNPJ N Fixo 14 - Sim

3 Nome empresarial C Variável 150 - Sim

3.10 Registro do beneficiário pessoa física do fundo ou clube de investimento (identificador BPFFCI)

- Serão apresentados todos os CPF em ordem crescente;

- Devem ser apresentados antes dos registros com identificador BPJFCI, caso exista o registro;

- Deve estar associado a um registro do tipo IDREC.

1 Identificador de registro C Fixo 6 BPFFCI Sim

2 CPF N Fixo 11 - Sim

3 Nome C Variável 60 - Sim

4 Data atribuída pelo laudo D Fixo 8 - Não da moléstia grave

3.11 Registro do beneficiário pessoa jurídica do fundo ou clube de investimento (identificador BPJFCI)

- Serão apresentados todos os CNPJ em ordem crescente;

- Devem ser apresentados depois dos registros com identificador BPFFCI, caso exista o registro;

- Deve estar associado a um registro do tipo IDREC.

1 Identificador de registro C Fixo 6 BPJFCI Sim

2 CNPJ N Fixo 14 - Sim

3 Nome empresarial C Variável 150 - Sim

3.12 Registro de processo da justiça do trabalho/federal/estadual/Distrito Federal (identificador PROC)

- Deve estar classificado em ordem crescente por:

- Tipo de justiça;

- Número do processo;

- Deve estar associado ao registro do tipo DECPJ.

1 Identificador de registro C Fixo 4 PROC Sim

2 Indicador de Justiça N Fixo 1 1 – Justiça federal Sim

2 – Justiça do trabalho

3 – Justiça estadual/Distrito Federal

3 Número do processo C Variável 20 - Sim

Indicador de tipo de 1 – Pessoa física 4 advogado/escritório de N Fixo 1 Não advocacia 2 – Pessoa jurídica

CPF do advogado/ CNPJ CPF com 11 dígitos 5 do escritório de N Variável 14 CNPJ com 14 Não advocacia dígitos

Nome da pessoa física até 60 Nome do advogado/ posições 6 Nome empresarial do C Variável 150 Não escritório de advocacia Nome empresarial da pessoa jurídica até 150 posições

Valor pago para o Valor pago para o 7 N Variável 13 Não advogado advogado

3.13 Registro de beneficiário pessoa física do processo da justiça do trabalho/federal/estadual/Distrito Federal (identificador BPFPROC)

- Serão apresentados todos os CPF em ordem crescente;

- Devem ser apresentados antes dos registros com identificador BPJPROC, caso exista o registro;

- Deve estar associado a um registro do tipo IDREC.

1 Identificador de registro C Fixo 7 BPFPROC Sim

2 CPF N Fixo 11 - Sim

3 Nome C Variável 60 - Sim

4 Data atribuída pelo laudo D Fixo 8 - Não da moléstia grave

3.14 Registro de beneficiário pessoa jurídica do processo da justiça do trabalho/federal/estadual/Distrito Federal (identificador

BPJPROC)

- Serão apresentados todos os CNPJ em ordem crescente;

- Devem ser apresentados depois dos registros com identificador BPFPROC, caso exista o registro;

- Deve estar associado a um registro do tipo IDREC.

1 Identificador de registro C Fixo 7 BPJPROC Sim

2 CNPJ N Fixo 14 - Sim

3 Nome empresarial C Variável 150 - Sim

3.15 Registro de rendimentos recebidos acumuladamente (identificador RRA)

- Deve estar classificado em ordem crescente por:

- Identificador de rendimento recebido acumuladamente;

- Número do processo/requerimento.

1 Identificador de registro C Fixo 3 RRA Sim

1 – Pago pelo Identificador de declarante 2 rendimento recebido N Fixo 1 Sim acumuladamente 2 – Pago pela justiça

Número do 3 C Variável 20 - Não processo/requerimento

Indicador de tipo de 1 – Pessoa física 4 advogado/escritório de N Fixo 1 Não advocacia 2 – Pessoa jurídica

CPF com 11 dígitos CPF do advogado/CNPJ 5 N Variável 14 CNPJ com 14 Não do escritório de advocacia dígitos

Nome da pessoa física com até 60 Nome do advogado/Nome posições 6 empresarial do escritório C Variável 150 Nome empresarial Não de advocacia da pessoa jurídica com até 150 posições

Valor pago para o Valor pago para o 7 N Variável 13 Não advogado advogado

Observações:

Ordem Campo Descrição

3 Número do O preenchimento será obrigatório se o campo de ordem 2 igual a 2. processo/requerimento

3.16 Registro de beneficiário pessoa física dos rendimentos recebidos acumuladamente (identificador BPFRRA)

- Deve estar classificado em ordem crescente por:

- CPF;

- Natureza do RRA;

- Deve estar associado ao registro do tipo IDREC.

1 Identificador de registro C Fixo 6 BPFRRA Sim

2 CPF N Fixo 11 - Sim

3 Nome C Variável 60 - Sim

4 Natureza do RRA C Variável 50 - Não

Data atribuída pelo laudo 5 D Fixo 8 - Não da moléstia grave

S – Existem Indicador de identificação informações 6 C Fixo 1 Sim do alimentando detalhadas do alimentando

N – Não existem informações detalhadas do alimentando

Observações:

Ordem Campo Descrição

Indicador de identificação do 1. O campo só poderá ser igual a “S” se o campo 2 do registro RRA

alimentando igual a “1” (Pago pelo declarante);

2. Se campo igual a “S” – deverá constar o registro INFPA e RTPA para cada alimentando;

3. Se campo igual a “N” – não apresentar o registro INFPA; deverá constar o registro RTPA com o valor de pensão alimentícia pago a todos os alimentandos do beneficiário;

4. As informações detalhadas a que se refere o campo são: CPF, Data de nascimento e Nome do alimentando (registro INFPA).

3.17 Registro de identificação de Previdência Complementar (identificador INFPC)

- Registro permitido somente se campo 6 do registro BPFDEC (Indicador de identificação da previdência complementar) igual a “S”;

- Serão apresentados todos os CNPJ em ordem crescente;

- Deve estar associado ao registro do tipo BPFDEC;

- Deve constar um registro INFPC para cada CNPJ de entidade de previdência complementar.

1 Identificador de registro C Fixo 5 INFPC Sim

2 CNPJ N Fixo 14 - Sim

3 Nome empresarial C Variável 150 - Sim

3.18 Registro de informações do beneficiário da pensão alimentícia (identificador INFPA)

- Registro permitido somente se Indicador de identificação do alimentando igual a “S” (BPFDEC, campo 5; e BPFRRA, campo 6);

- Registro INFPA associado ao BPFRRA será permitido somente quando o identificador de rendimento recebido acumuladamente igual a “1 – Pago pelo declarante” (campo 2 do registro RRA);

- Deve estar classificado em ordem crescente de CPF e data de nascimento;

- Deve estar associado ao registro do tipo BPFDEC, BPFRRA.

1 Identificador de registro C Fixo 5 INFPA Sim

2 CPF do alimentando N Fixo 11 - Não

3 Data de nascimento D Fixo 8 - Não

4 Nome C Variável 60 - Sim

5 Relação de dependência N Fixo 2 03 – Cônjuge/ Não Companheiro (a)

04 – Filho (a)

06 – Enteado (a)

08 – Pai/Mãe

10 – Agregado/Outros

Observações: Ordem Campo Descrição

Preenchimento obrigatório para maiores de 18 anos completos até 31 2 CPF do alimentando de dezembro do ano-calendário da declaração. Preenchimento obrigatório para menores de 18 anos completos até 3 Data de nascimento 31 de dezembro do ano-calendário da declaração, que não tenham informado o CPF.

3.19 Registro de valores mensais (identificadores RTRT, RTPO, RTPP, RTFA, RTSP, RTEP, RTDP, RTPA, RTDS, RTIRF, CJAA, CJAC, ESRT, ESPO, ESPP, ESFA, ESSP, ESEP, ESDP, ESPA, ESDS, ESIR, ESDJ, RIP65, RIDAC, RIIRP, RIAP, RIMOG, RIRPC, RIBMR, RICAP, RIJMRE, RISCP, RIMUN, RISEN e DAJUD)

- Deve ocorrer apenas se houver pelo menos um dos valores referentes aos meses ou 13º salário;

- Deve ocorrer apenas um registro de cada identificador para o mesmo beneficiário;

- Deve estar associado aos registros dos tipos BPFDEC, BPJDEC, BPFFCI, BPJFCI, BPFPROC, BPJPROC, BPFRRA, BPFSCP, BPJSCP, INFPC, INFPA, VPEIM.

RTRT

RTPO

1 Identificador de registro C Variável 5 RTPP Sim

RTFA RTSP

RTEP

RTDP

RTPA

RTDS

RTIRF

CJAC

CJAA

ESRT

ESPO

ESPP

ESFA

ESSP

ESEP

ESDP

ESPA

ESDS

ESIR

ESDJ

RIP65

RIDAC

RIIRP

RIAP

RIMOG

RIRPC

RIBMR

RICAP

RIJMRE

RISCP

RIMUN

RISEN DAJUD

2 Janeiro N Variável 13 - Não

3 Fevereiro N Variável 13 - Não

4 Março N Variável 13 - Não

5 Abril N Variável 13 - Não

6 Maio N Variável 13 - Não

7 Junho N Variável 13 - Não

8 Julho N Variável 13 - Não

9 Agosto N Variável 13 - Não

10 Setembro N Variável 13 - Não

11 Outubro N Variável 13 - Não

12 Novembro N Variável 13 - Não

13 Dezembro N Variável 13 - Não

14 Décimo Terceiro N Variável 13 - Não

3.20 Registro de valores anuais isentos/não tributáveis/sem retenção (identificadores RIL96, RIPTS e RIRSR)

- Deve ocorrer apenas um registro de cada identificador para o mesmo beneficiário; - Deve estar associado aos registros dos tipos BPFDEC (RIL96, RIPTS), BPFPROC/BPJPROC (RIRSR);

- Registro RIRSR permitido somente se “indicador de justiça” do registro PROC igual a 1 (Justiça Federal).

RIL96

1 Identificador de registro C Variável 6 RIPTS Sim

RIRSR

2 Valor pago no ano N Variável 13 - Sim

3.21 Registro de valores anuais de rendimentos isentos – outros (identificador RIO)

- Ocorrerá apenas um registro para cada beneficiário;

- Deve estar associado ao registro do tipo BPFDEC ou BPFFCI.

1 Identificador de registro C Fixo 3 RIO Sim

2 Valor pago no ano N Variável 13 - Sim

3 Descrição dos C Variável 60 - Sim rendimentos isentos – outros

3.22 Registro de quantidade de meses (identificador QTMESES)

- Deve ocorrer apenas um registro de cada identificador para o mesmo beneficiário;

- Deve estar associado ao registro do tipo BPFRRA.

1 Identificador de registro C Fixo 7 QTMESES Sim

2 Quantidade meses – N Variável 4 - Não janeiro

3 Quantidade meses – N Variável 4 - Não fevereiro

4 Quantidade meses – N Variável 4 - Não março

5 Quantidade meses – abril N Variável 4 - Não

6 Quantidade meses – N Variável 4 - Não maio

7 Quantidade meses – N Variável 4 - Não junho

8 Quantidade meses – N Variável 4 - Não julho

9 Quantidade meses – N Variável 4 - Não agosto

10 Quantidade meses – N Variável 4 - Não setembro

11 Quantidade meses – N Variável 4 - Não outubro

12 Quantidade meses – N Variável 4 - Não novembro

13 Quantidade meses – N Variável 4 - Não dezembro

3.23 Registro de informações da Sociedade em Conta de Participação (identificador SCP)

- Serão apresentados em ordem crescente de CNPJ.

- Deve constar um registro para cada CNPJ de Sociedade em conta de participação

1 Identificador de registro C Fixo 3 SCP Sim

2 CNPJ da Sociedade em N Fixo 14 - Sim Conta de Participação

3 Nome empresarial da C Variável 150 - Sim Sociedade em Conta de Participação

3.24 Registro de beneficiário pessoa física da sociedade em conta de participação (identificador BPFSCP)

- Serão apresentados todos os CPF em ordem crescente;

- Devem ser apresentados antes dos registros com identificador BPJSCP, caso exista o registro;

- Deve estar associado a um registro do tipo SCP.

1 Identificador de registro C Fixo 6 BPFSCP Sim

2 CPF N Fixo 11 - Sim

3 Nome C Variável 60 - Sim

4 Percentual de N Variável 4 - Não participação na SCP

3.25 Registro de beneficiário pessoa jurídica da sociedade em conta de participação (identificador BPJSCP)

- Serão apresentados todos os CNPJ em ordem crescente;

- Devem ser apresentados depois dos registros com identificador BPFSCP, caso exista o registro;

- Deve estar associado a um registro do tipo SCP.

1 Identificador de registro C Fixo 6 BPJSCP Sim

2 CNPJ N Fixo 14 - Sim

3 Nome empresarial C Variável 150 - Sim

4 Percentual de C Variável 4 - Não participação na SCP

3.26 Registro de pagamentos a plano privado de assistência à saúde – coletivo empresarial (identificador PSE)

- Ocorre somente uma vez no arquivo, caso exista informação de valores pagos pelo titular/dependente do plano de assistência à saúde.

1 Identificador de registro C Fixo 3 PSE Sim

3.27 Registro de operadora do plano privado de assistência à saúde – coletivo empresarial (identificador OPSE)

- Ocorre caso exista o registro PSE;

- Serão apresentados todos os CNPJ em ordem crescente.

1 Identificador de registro C Fixo 4 OPSE Sim

CNPJ da operadora de plano privado de 2 N Fixo 14 - Sim assistência à saúde – coletivo empresarial

3 Nome empresarial C Variável 150 - Sim

4 Registro ANS N Fixo 6 - Não

3.28 Registro de titular do plano privado de assistência à saúde – coletivo empresarial (identificador TPSE)

- Serão apresentados todos os CPF em ordem crescente.

- Deve estar associado ao registro do tipo OPSE.

1 Identificador de registro C Fixo 4 TPSE Sim

2 CPF do titular N Fixo 11 - Sim

3 Nome C Variável 60 - Sim

4 Valor pago no ano N Variável 9 - Sim

Observações: Ordem Campo Descrição

Preenchimento obrigatório se o titular não possuir dependente 4 Valor pago no ano cadastrado e nem reembolso informado.

3.29 Registro de informação de reembolso do titular do plano de saúde – coletivo empresarial (identificador RTPSE)

- Deve estar classificado em ordem crescente de CPF/CNPJ do prestador de serviço (primeiro os CPF e depois os CNPJ); - Deve estar associado ao registro do tipo TPSE;

- Só deverá constar o registro se houver valor de reembolso do ano-calendário ou de anos-calendário anteriores.

1 Identificador de registro C Fixo 5 RTPSE Sim

CPF/CNPJ do prestador CPF com 11 dígitos 2 N Variável 14 Sim de serviço CNPJ com 14 dígitos

Nome da pessoa Nome/Nome empresarial 3 C Variável 150 física até 60 Sim do prestador de serviço posições

Nome empresarial da pessoa jurídica até 150 posições

Valor do reembolso do 4 N Variável 9 - Não ano-calendário

Valor do reembolso de 5 N Variável 9 - Não anos anteriores

Observações: Ordem Campo Descrição

Valor do reembolso do ano- Valores reembolsados no ano-calendário, referentes a pagamentos

calendário de serviços prestados no ano-calendário.

Valor do reembolso de anos Valores reembolsados no ano-calendário referentes a pagamentos de

anteriores serviços prestados em anos anteriores.

3.30 Registro de dependente do plano privado de assistência à saúde – coletivo empresarial (identificador DTPSE)

- Deve estar classificado em ordem crescente de CPF e data de nascimento;

- Deve estar associado ao registro do tipo TPSE.

Ordem Campo Formato Preenchimento Tamanho Valores válidos Obrigatório

1 Identificador de registro C Fixo 5 DTPSE Sim

2 CPF do dependente N Fixo 11 - Não

3 Data de nascimento D Fixo 8 - Não

4 Nome C Variável 60 - Sim

03 – Cônjuge/ Companheiro(a)

04 – Filho(a) Relação de 5 N Fixo 2 06 – Enteado(a) Não dependência 08 – Pai/Mãe

10 – Agregado/ Outros

6 Valor pago no ano N Variável 9 - Sim

Observações: Ordem Campo Descrição

CPF do dependente Preenchimento obrigatório para maiores de 18 anos completos até

31 de dezembro do ano-calendário da declaração. Data de nascimento Preenchimento obrigatório para menores de 18 anos completos até 3 31 de dezembro do ano-calendário da declaração, que não tenham informado o CPF.

Valor pago no ano Preenchimento obrigatório se o dependente não possuir reembolso

informado.

3.31 – Registro de informação de reembolso do dependente (identificador RDTPSE):

- Deve estar classificado em ordem crescente de CPF/CNPJ do prestador de serviço (primeiro os CPF e depois os CNPJ);

- Deve estar associado ao registro do tipo DTPSE;

- Só deverá constar o registro se houver valor de reembolso do ano-calendário ou de anos-calendário anteriores.

1 Identificador de registro C Fixo 6 RDTPSE Sim

CPF/CNPJ do prestador CPF com 11 dígitos 2 N Variável 14 Sim de serviço CNPJ com 14 dígitos

Nome da pessoa física até 60 posições 3 Nome/Nome Empresarial C Variável 150 Sim do prestador de serviço Nome empresarial da pessoa jurídica até 150 posições

Valor do reembolso do 4 N Variável 9 - Não ano-calendário

Valor do reembolso de 5 N Variável 9 - Não anos anteriores

Observações: Ordem Campo Descrição

Valor do reembolso do ano- Valores reembolsados no ano-calendário, referentes a pagamentos

calendário de serviços prestados no ano-calendário Valor do reembolso de anos Valores reembolsados no ano-calendário referentes a pagamentos

anteriores de serviços prestados em anos anteriores

3.32 Registro de rendimentos pagos a residentes ou domiciliados no exterior (identificador RPDE)

- Ocorre somente uma vez no arquivo, caso exista informação de rendimentos pagos a residentes ou domiciliados no exterior

1 Identificador de registro C Fixo 4 RPDE Sim

3.33 Registro de beneficiário dos rendimentos pagos a residentes ou domiciliados no exterior (identificador BRPDE)

- Deve estar classificado em ordem crescente por:

- Beneficiário;

- Código de país;

- Número de identificação fiscal – NIF;

- Deve estar associado ao registro do tipo RPDE.

1 Identificador de registro C Fixo 5 BRPDE Sim

1 – Pessoa física 2 Beneficiário N Fixo 1 Sim 2 – Pessoa jurídica

De acordo com a tabela de código dos 3 Código de país N Variável 3 países constante na Sim IN que dispõe sobre a Dirf

Número de identificação 4 C Variável 30 - Não fiscal – NIF

S – Dispensado do Número de identificação fiscal – Indicador de beneficiário NIF dispensado do Número 5 C Fixo 1 N – Não é Sim de Identificação Fiscal – NIF dispensado do Número de identificação fiscal – NIF

S – Dispensado do Número de identificação fiscal – Indicador de que o país NIF 6 não exige Número de C Fixo 1 N – Não é Sim Identificação Fiscal – NIF dispensado do Número de identificação fiscal – NIF

CPF com 11 dígitos 7 CPF/CNPJ N Variável 14 Não CNPJ com 14 dígitos

8 Nome/Nome empresarial C Variável 150 - Sim

De acordo com a tabela de Relação fonte pagadora informações sobre pessoa jurídica e 9 N Fixo 3 os beneficiários dos Não beneficiário pessoa rendimentos jurídica constante na IN que dispõe sobre a Dirf

10 Logradouro C Variável 60 - Não

11 Número C Variável 6 - Não

12 Complemento C Variável 25 - Não

13 Bairro/Distrito C Variável 20 - Não

14 Código postal N Variável 10 - Não

15 Cidade C Variável 40 - Não

16 Estado/Província C Variável 40 - Não

17 Telefone N Variável 15 - Não

Observações:

Ordem Campo Descrição

Relação fonte pagadora Preenchimento obrigatório se campo de ordem 2 (Beneficiário) igual 9 pessoa jurídica e beneficiário a 2. pessoa jurídica

3.34 Registro de valores de rendimentos pagos a residentes ou domiciliados no exterior (identificador VRPDE)

- Deve estar classificado em ordem crescente por:

- Data do pagamento;

- Código de receita;

- Deve estar associado ao registro do tipo BRPDE.

1 Identificador de registro C Fixo 5 VRPDE Sim

2 Data do pagamento D Fixo 8 - Sim

3 Código de receita N Fixo 4 - Sim

De acordo com a tabela de informações sobre os 4 Tipo de rendimento N Fixo 3 Sim rendimentos constante na IN que dispõe sobre a Dirf

5 Rendimento pago N Variável 13 - Sim

6 Imposto retido N Variável 13 - Não

De acordo com a tabela de informações sobre a 7 Forma de tributação N Fixo 2 Sim forma de tributação constante na IN que dispõe sobre a Dirf

3.35 Registro de informações complementares para o comprovante de rendimento (identificador INF)

- Serão apresentados todos os CPF em ordem crescente;

- Deve haver um registro BPFDEC, BPFPROC e/ou BPFRRA correspondente na declaração;

- Deve ocorrer apenas um registro para cada beneficiário.

1 Identificador de registro C Fixo 3 INF Sim

2 CPF N Fixo 11 - Sim

Informações 3 C Variável 500 - Sim complementares

3.36 Registro identificador do término da declaração (identificador FIMDirf)

- Registro obrigatório no arquivo; - Deve ser o último registro no arquivo;

- Ocorre somente uma vez no arquivo.

1 Identificador de registro C Fixo 7 FIMDirf Sim

