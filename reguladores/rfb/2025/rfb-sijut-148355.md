---
titulo: "Ato Declaratório Executivo Cofis nº 27, de 15 de dezembro de 2025"
orgao: "Coordenação-Geral de Fiscalização"
tipo: "Ato Declaratório Executivo"
numero: "27"
data: "2025-12-15"
revogada: false
evidencia_revogacao: "vigente:true"
vigente_fonte: true
versao_texto: "publicação original — visão original da fonte"
publicacao: "Publicado(a) no DOU de 16/12/2025, seção 1, página 102"
data_publicacao: "2025-12-16"
fonte: "https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/148355/visao/original"
fonte_api: "https://normasinternet2.receita.fazenda.gov.br/api/consulta-externa/ato/148355/visao/original"
fonte_indice: "https://normas.receita.fazenda.gov.br/api/indexacao/ato/pesquisar"
id_rfb: "148355"
sha256_texto: "8664f02f7d875e3feeb12d24c9f34954e150d0187ee0bec6c448fe15a776c869"
baixado_em: "2026-10-15"
---
# Ato Declaratório Executivo Cofis nº 27, de 15 de dezembro de 2025

Dispõe sobre o leiaute do Programa Gerador da Declaração de Serviços Médicos e de Saúde (PGD Dmed 2026).

A COORDENADORA-GERAL DE FISCALIZAÇÃO, no uso das atribuições que lhe conferem os incisos I e II do art. 121 do Regimento Interno da Secretaria Especial da Receita Federal do Brasil, aprovado pela Portaria ME nº 284, de 27 de julho de 2020, e tendo em vista o disposto no art. 125 da referida Portaria, DECLARA:

**Art. 1º** Fica aprovado o leiaute aplicável aos campos, registros e arquivos da Declaração de Serviços Médicos e de Saúde (Dmed) para apresentação das informações relativas aos anos-calendário de 2020 a 2025, situação normal, e de 2020 a 2026, nos casos de situação especial.

**Art. 2º** Para a elaboração ou importação de dados pelo PGD Dmed 2026 deverá ser observado o leiaute do arquivo constante do Anexo Único deste Ato Declaratório.

**Art. 3º** Este Ato Declaratório Executivo entra em vigor na data de sua publicação no Diário Oficial da União.

VANDREIA MOTA ROCHA

ANEXO ÚNICO  
LEIAUTE DO ARQUIVO DA DECLARAÇÃO  
Declaração de Serviços Médicos e Saúde - Dmed



ANEXO ÚNICO

LEIAUTE DO ARQUIVO DA DECLARAÇÃO Declaração de Serviços Médicos e Saúde – Dmed

1. Regras Gerais 2. Estrutura de Arquivo 2.1. Exemplo de estrutura de declarante Pessoa Jurídica 3. Leiaute 3.1. Registro de informação da declaração (identificador Dmed) 3.2. Registro do responsável pelo preenchimento (identificador RESPO) 3.3. Registro de informação do declarante pessoa jurídica (identificador DECPJ) 3.4. Registro de informação da operadora de plano de assistência à saúde (identificador OPPAS) 3.5. Registro de informação do titular do plano (identificador TOP) 3.6. Registro de informação de reembolso do titular do plano (identificador RTOP) 3.7. Registro de informação de dependente do titular (identificador DTOP) 3.8. Registro de informação de reembolso do dependente (identificador RDTOP) 3.9. Registro de informação do prestador de serviço de saúde (identificador PSS) 3.10. Registro de informação do responsável pelo pagamento ao prestador do serviço de saúde (identificador RPPSS) 3.11. Registro de informação de beneficiário do serviço pago (identificador BRPPSS) 3.12. Registro identificador do término da declaração (identificador FIMDmed) 4. Tabela de relação de dependência

1 – Regras gerais: Esta seção apresenta as regras que devem ser respeitadas em todos os arquivos gerados, quando não excepcionadas por regra específica referente a um dado registro e explicitada em suas observações. Regra de Nº Descrição preenchimento Alfanumérico (C): representados por “C” - todos os caracteres, excetuados o Formato dos 1 caractere “|” (pipe ou barra vertical, caractere 124 da Tabela ASCII); campos Numérico (N): representados por “N” - pode conter apenas os valores de “0” a “9”. Campos numéricos Devem ser informados conforme o padrão ano, mês, dia (AAAAMMDD), excluindo- 2 (D) cujo conteúdo se quaisquer caracteres de separação, tais como: “.” (ponto), “/” (barra inclinada), representa data “-” (hífen), etc. Campos numéricos 3 (N) cujo conteúdo Devem ser informados conforme o padrão “ano” (AAAA). representa ano Os campos numéricos com número de inscrição (CNPJ, CPF, CNES e ANS) Campos numéricos deverão ser informados com todos os dígitos, inclusive os zeros (0) à esquerda; 4 com número de As máscaras (caracteres especiais de formatação, tais como “.” (ponto), “/” (barra inscrição inclinada), “-“ (hífen), etc.) não devem ser informadas. Devem ser informados com até 9 posições, representando 7 posições inteiras e 2 Campos numéricos decimais; 5 referentes a valores Os zeros não significativos não devem ser informados; monetários Os caracteres “.” (ponto) e “,” (vírgula) não devem ser informados. 6 Campos Os campos com conteúdo alfanumérico nos quais se faz necessário registrar alfanuméricos com números ou códigos de identificação (Ex.: Cadastro Nacional de Estabelecimentos números ou

códigos de de Saúde – CNES) deverão seguir a regra de formação e tamanho definidos pelo identificação respectivo órgão regulador; As máscaras (caracteres especiais de formatação, tais como: “.” (ponto), “/” (barra inclinada), “-” (hífen), etc.) não devem ser informadas. 7 Formação dos Ao final de cada campo (incluído o último de cada registro) deve ser inserido o campos caractere delimitador “|” (pipe ou barra vertical: caractere 124 da Tabela ASCII); O caractere delimitador “|” (pipe) não deve ser incluído como parte integrante do conteúdo de quaisquer campos numéricos, datas ou alfanuméricos; Na ausência de informação, o campo vazio (campo sem conteúdo; nulo e com valor zero) deverá ser iniciado com caractere “|” e imediatamente encerrado com o mesmo caractere “|” delimitador de campo. 8 Formação dos Cada registro deve necessariamente ocupar apenas uma linha no arquivo. registros Preenchimento dos Preenchimento fixo: o campo deve ser preenchido com o tamanho exato;

campos Preenchimento variável: o campo pode ter variação de tamanho de preenchimento.

2 – Estrutura de arquivo 2.1 – Exemplo de estrutura de declarante Pessoa Jurídica

Dmed – Declaração de serviços médicos e de saúde RESPO – Responsável pelo preenchimento DECPJ – Declarante pessoa jurídica OPPAS – Operadora de plano de assistência à saúde TOP – Titular do plano RTOP – Reembolso do titular do plano DTOP – Dependente do titular RDTOP – Reembolso do dependente PSS – Prestador de serviço de saúde RPPSS – Responsável pelo pagamento ao prestador do serviço de saúde BRPPSS – Beneficiário do serviço pago FIMDmed – Término da declaração

3 – Leiaute do arquivo 3.1 – Registro de informação da declaração (identificador Dmed)

- Registro obrigatório no arquivo; - Deve ser o 1º (primeiro) registro no arquivo;

1 Identificador de registro C Fixo 4 Dmed Sim 2 Ano referência N Fixo 4 2026 Sim 3 Ano-calendário N Fixo 4 2020 a 2026 Sim Indicador de retificadora S – Retificadora 4 C Fixo 1 Sim N – Original 5 Número do recibo N Fixo 12 - Não Identificador de estrutura do 6 C Fixo 6 - Não leiaute

5 Número do recibo Se a declaração for original, não preencher; Se a declaração for retificadora, deverá ser preenchido com o número do recibo da última declaração entregue, se o declarante não transmitir a declaração com assinatura digital.

3.2 – Registro do Responsável pelo preenchimento (identificador RESPO)

- Registro obrigatório no arquivo; - Deve ser o 2º (segundo) registro no arquivo;

1 Identificador de registro C Fixo 5 RESPO Sim 2 CPF N Fixo 11 - Sim 3 Nome C Variável 60 - Sim 4 DDD N Fixo 2 - Sim 5 Telefone N Fixo 9 - Sim 6 Ramal N Variável 6 - Não 7 Fax N Fixo 9 - Não 8 Correio eletrônico C Variável 50 - Não

3.3 – Registro de informação do declarante pessoa jurídica (identificador DECPJ)

- Registro obrigatório no arquivo quando for declarante pessoa jurídica; - Deve ser o 3º (terceiro) registro no arquivo; - Ocorre somente uma vez no arquivo;

1 Identificador de C Fixo 5 DECPJ Sim registro 2 CNPJ N Fixo 14 - Sim 3 Nome empresarial C Variável 150 - Sim 4 Tipo do declarante N Fixo 1 1 – Prestador de Sim serviço de saúde; 2 – Operadora de plano de assistência à saúde; 3 – Prestador de serviço de saúde e Operadora de plano de assistência à saúde. 5 Registro ANS N Fixo 6 - Não 6 CNES N Fixo 7 - Não

7 CPF responsável N Fixo 11 - Sim perante o CNPJ

8 Indicador de situação C Fixo 1 S – Declaração de Sim da declaração situação especial; N – Não é declaração de situação especial. 9 Data do evento D Fixo 8 - Não 10 Indicador declarante C Fixo 1 S – Declarante Não possui registro ANS possui registro na ANS; N – Declarante não possui registro na ANS

5 Registro ANS Agência Nacional de Saúde Suplementar – ANS;

Preenchimento obrigatório se campo de ordem 4 – Tipo do declarante igual a “2” ou “3”; e campo de ordem 10 – Indicador declarante possui registro ANS igual a “S”. 6 CNES Cadastro Nacional de Estabelecimentos de Saúde – CNES. 9 Data do evento Preenchimento obrigatório se campo de ordem 8 – Indicador de situação da declaração igual a “S”. 10 Indicador declarante possui Preenchimento obrigatório se campo de ordem 4 – Tipo do registro ANS declarante igual a “2” ou “3”.

3.4 – Registro de informação da operadora de plano de assistência à saúde (identificador OPPAS)

- Ocorre caso o declarante seja operadora de plano de assistência à saúde.

1 Identificador de registro C Fixo 5 OPPAS Sim

Preenchimento obrigatório se o campo de ordem 4 – Tipo do Declarante, do registro DECPJ igual a “2”; 1 Identificador de registro Preenchimento opcional se o campo de ordem 4 – Tipo do Declarante, do registro DECPJ igual a “3”, e o declarante não exerceu atividades de Operadora de Plano de Assistência à Saúde no ano-calendário.

3.5 – Registro de informação do titular do plano (identificador TOP)

- Deve estar classificado em ordem crescente por CPF do titular; - Deve estar associado ao registro do tipo OPPAS.

1 Identificador de registro C Fixo 3 TOP Sim 2 CPF do titular N Fixo 11 - Sim

3 Nome C Variável 60 - Sim Valor pago no ano com o 4 N Variável 9 - Não titular

Valor pago no ano com o Preenchimento obrigatório se não existir registros RTOP e/ou DTOP 4 titular associados ao TOP.

3.6 – Registro de informação de reembolso do titular do plano (identificador RTOP)

- Deve estar classificado em ordem crescente por CPF/CNPJ do prestador de serviço (primeiro os CPF e depois os CNPJ); - Deve estar associado ao registro do tipo TOP; - Só deverá constar o registro se houver valor de reembolso do ano-calendário ou de anos-calendário anteriores.

1 Identificador de registro C Fixo 4 RTOP Sim 2 CPF/CNPJ do N Variável 14 CPF com 11 Sim prestador de serviço dígitos; CNPJ com 14 dígitos. 3 Nome/Nome C Variável 150 Nome da Sim empresarial do pessoa física prestador de serviço até 60 posições. Nome empresarial da pessoa jurídica até 150 posições. 4 Valor do reembolso do N Variável 9 - Não ano-calendário Valor do reembolso de - 5 N Variável 9 Não anos anteriores

Valor do reembolso do ano- Valores reembolsados no ano-calendário, referentes a

calendário pagamentos de serviços prestados no ano-calendário. Valor do reembolso de anos Valores reembolsados no ano-calendário referentes a

anteriores pagamentos de serviços prestados em anos anteriores.

3.7 – Registro de informação de dependente do titular (identificador DTOP)

- Deve estar classificado em ordem crescente por CPF e Data de nascimento do dependente; - Deve estar associado ao registro do tipo TOP.

1 Identificador de registro C Fixo 4 DTOP Sim

2 CPF do dependente N Fixo 11 - Não 3 Data de Nascimento D Fixo 8 - Não

4 Nome C Variável 60 Sim Relação de Dependência Conforme Tabela 5 N Fixo 2 de Relação de Não Dependência Valor pago no ano com o Não 6 N Variável 9 - dependente

CPF do Preenchimento obrigatório para maiores de 18 anos completos até 31 de dezembro

dependente do ano-calendário da declaração.

Data de Preenchimento obrigatório para menores de 18 anos completos até 31 de dezembro

nascimento do ano-calendário da declaração, que não tenham informado o CPF.

3.8. Registro de informação de reembolso do dependente (identificador RDTOP)

- Deve estar classificado em ordem crescente por CPF/CNPJ do prestador de serviço (primeiro os CPF e depois os CNPJ); - Deve estar associado ao registro do tipo DTOP; - Só deverá constar o registro se houver valor de reembolso do ano-calendário e de anos-calendário anteriores.

1 Identificador de registro C Fixo 5 RDTOP Sim 2 CPF/CNPJ do prestador de N Variável 14 CPF com 11 Sim serviço dígitos; CNPJ com 14 dígitos. 3 Nome/Nome Empresarial C Variável 150 Nome da Sim do prestador de serviço pessoa física até 60 posições; Nome empresarial da pessoa jurídica até 150 posições. 4 Valor do reembolso do N Variável 9 - Não ano-calendário Valor do reembolso de anos 5 N Variável 9 - Não anteriores

Valor do reembolso do ano- Valores reembolsados no ano-calendário, referentes a pagamentos de

calendário serviços prestados no ano-calendário. Valor do reembolso de anos Valores reembolsados no ano-calendário referentes a pagamentos de

anteriores serviços prestados em anos anteriores.

3.9 – Registro de informação do prestador de serviço de saúde (identificador PSS)

- Ocorre caso o declarante seja prestador de serviço de saúde.

1 Identificador de registro C Fixo 3 PSS Sim

Identificador de registro Preenchimento obrigatório se o campo de ordem 4 – Tipo do Declarante, do registro DECPJ igual a “1”;

1 Preenchimento opcional se o campo de ordem 4 – Tipo do Declarante, do registro DECPJ igual a “3”, e o declarante não exerceu atividades de Prestador de Serviços de Saúde no ano-calendário.

3.10 – Registro de informação do responsável pelo pagamento ao prestador do serviço de saúde (identificador RPPSS)

- Deve estar classificado em ordem crescente por CPF do responsável pelo pagamento; - Deve estar associado ao registro do tipo PSS.

1 Identificador de registro C Fixo 5 RPPSS Sim CPF do responsável pelo 2 N Fixo 11 - Sim pagamento 3 Nome C Variável 60 - Sim Valor pago no ano pelo 4 responsável em benefício N Variável 9 - Não próprio

Valor pago no ano pelo Preenchimento obrigatório se não existir registro BRPPSS associado ao 4 responsável em benefício RPPSS. próprio

3.11 – Registro de informação de beneficiário do serviço pago (identificador BRPPSS)

- Deve estar classificado em ordem crescente por CPF e Data de nascimento do beneficiário; - Deve estar associado ao registro do tipo RPPSS.

1 Identificador de registro C Fixo 6 BRPPSS Sim 2 CPF do beneficiário N Fixo 11 - Não

3 Data de nascimento D Fixo 8 - Não

4 Nome C Variável 60 - Sim Valor pago no ano com o Sim 5 N Variável 9 >0 beneficiário

Data de nascimento Preenchimento obrigatório para o beneficiário do serviço de saúde que

não informar o número do CPF quando da prestação do serviço.

3.12 – Registro identificador do término da declaração (identificador FIMDmed)

- Registro obrigatório no arquivo; - Deve ser o último registro no arquivo;

1 Identificador de registro C Fixo 7 FIMDmed Sim

4 – Tabela de relação de dependência Código Descrição 03 Cônjuge/companheiro 04 Filho/filha 06 Enteado/enteada 08 Pai/mãe 10 Agregado/outros

