---
titulo: "Ato Declaratório Executivo Cofis nº 34, de 7 de novembro de 2024"
orgao: "Coordenação-Geral de Fiscalização"
tipo: "Ato Declaratório Executivo"
numero: "34"
data: "2024-11-07"
revogada: false
evidencia_revogacao: "vigente:true"
vigente_fonte: true
versao_texto: "publicação original — visão original da fonte"
publicacao: "Publicado(a) no DOU de 11/11/2024, seção 1, página 39"
data_publicacao: "2024-11-11"
fonte: "https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/141485/visao/original"
fonte_api: "https://normasinternet2.receita.fazenda.gov.br/api/consulta-externa/ato/141485/visao/original"
fonte_indice: "https://normas.receita.fazenda.gov.br/api/indexacao/ato/pesquisar"
id_rfb: "141485"
sha256_texto: "ed60370fdbd0e55ab178edcfcdbc2f104c7854afe66ca77886c9944385dd67a8"
baixado_em: "2026-10-16"
---
# Ato Declaratório Executivo Cofis nº 34, de 7 de novembro de 2024

Dispõe sobre o leiaute do Programa Gerador da Declaração de Serviços Médicos e de Saúde (PGD Dmed 2025)

O COORDENADOR-GERAL DE FISCALIZAÇÃO, no uso das atribuições que lhe conferem os incisos I e II do art. 121 do Regimento Interno da Secretaria Especial da Receita Federal do Brasil, aprovado pela Portaria ME nº 284, de 27 de julho de 2020, e tendo em vista o disposto no art. 122 da referida Portaria, declara:

**Art. 1º** Fica aprovado o leiaute aplicável aos campos, registros e arquivos da Declaração de Serviços Médicos e de Saúde (Dmed) para apresentação das informações relativas aos anos-calendário de 2019 a 2024, situação normal, e de 2019 a 2025, nos casos de situação especial.

**Art. 2º** Para o preenchimento ou importação de dados pelo PGD Dmed 2025 deverá ser observado o leiaute do arquivo constante do Anexo Único deste Ato Declaratório.

**Art. 3º** Este Ato Declaratório Executivo entra em vigor na data de sua publicação no Diário Oficial da União.

RICARDO DE SOUZA MOREIRA

Anexo Único



ANEXO ÚNICO

LEIAUTE DO ARQUIVO DA DECLARAÇÃO Declaração de Serviços Médicos e Saúde – Dmed 1. Regras Gerais 2. Estrutura de Arquivo 2.1. Exemplo de estrutura de declarante Pessoa Jurídica 3. Leiaute 3.1. Registro de informação da declaração (identificador Dmed) 3.2. Registro do responsável pelo preenchimento (identificador RESPO) 3.3. Registro de informação do declarante pessoa jurídica (identificador DECPJ) 3.4. Registro de informação da operadora de plano de assistência à saúde (identificador OPPAS) 3.5. Registro de informação do titular do plano (identificador TOP) 3.6. Registro de informação de reembolso do titular do plano (identificador RTOP) 3.7. Registro de informação de dependente do titular (identificador DTOP) 3.8. Registro de informação de reembolso do dependente (identificador RDTOP) 3.9. Registro de informação do prestador de serviço de saúde (identificador PSS) 3.10. Registro de informação do responsável pelo pagamento ao prestador do serviço de saúde (identificador RPPSS) 3.11. Registro de informação de beneficiário do serviço pago (identificador BRPPSS) 3.12. Registro identificador do término da declaração (identificador FIMDmed) 4. Tabela de relação de dependência

1 Regras gerais: Esta seção apresenta as regras que devem ser respeitadas em todos os arquivos gerados, quando não excepcionadas por regra específica referente a um dado registro e explicitada em suas observações. Regra de Nº Descrição preenchimento Alfanumérico (C): representados por “C” - todos os caracteres, excetuados o caractere “|” (pipe ou barra vertical, caractere 124 da Formato dos 1 Tabela ASCII); campos Numérico (N): representados por “N” - pode conter apenas os valores de “0” a “9”. Campos Devem ser informados conforme o padrão ano, mês, dia numéricos (D) 2 (AAAAMMDD), excluindo-se quaisquer caracteres de separação, tais cujo conteúdo como: “.” (ponto), “/” (barra inclinada), “-” (hífen), etc. representa data Campos numéricos (N) 3 Devem ser informados conforme o padrão “ano” (AAAA). cujo conteúdo representa ano Os campos numéricos com número de inscrição (CNPJ, CPF, CNES Campos e ANS) deverão ser informados com todos os dígitos, inclusive os numéricos com zeros (0) à esquerda;

número de As máscaras (caracteres especiais de formatação, tais como “.” inscrição (ponto), “/” (barra inclinada), “-“ (hífen), etc.) não devem ser informadas. Campos Devem ser informados com até 9 posições, representando 7 numéricos posições inteiras e 2 decimais; 5 referentes a Os zeros não significativos não devem ser informados; valores Os caracteres “.” (ponto) e “,” (vírgula) não devem ser informados. monetários 6 Campos Os campos com conteúdo alfanumérico nos quais se faz necessário alfanuméricos registrar números ou códigos de identificação (Ex.: Cadastro com números Nacional de Estabelecimentos de Saúde – CNES) deverão seguir a ou códigos de regra de formação e tamanho definidos pelo respectivo órgão identificação regulador;

As máscaras (caracteres especiais de formatação, tais como: “.” (ponto), “/” (barra inclinada), “-” (hífen), etc.) não devem ser informadas. 7 Formação dos Ao final de cada campo (incluído o último de cada registro) deve ser campos inserido o caractere delimitador “|” (pipe ou barra vertical: caractere 124 da Tabela ASCII); O caractere delimitador “|” (pipe) não deve ser incluído como parte integrante do conteúdo de quaisquer campos numéricos, datas ou alfanuméricos; Na ausência de informação, o campo vazio (campo sem conteúdo; nulo e com valor zero) deverá ser iniciado com caractere “|” e imediatamente encerrado com o mesmo caractere “|” delimitador de campo. 8 Formação dos Cada registro deve necessariamente ocupar apenas uma linha no registros arquivo. Preenchimento fixo: o campo deve ser preenchido com o tamanho Preenchimento exato;

dos campos Preenchimento variável: o campo pode ter variação de tamanho de preenchimento.

2 Estrutura de arquivo 2.1 Exemplo de estrutura de declarante Pessoa Jurídica

Dmed – Declaração de serviços médicos e de saúde RESPO – Responsável pelo preenchimento DECPJ – Declarante pessoa jurídica OPPAS – Operadora de plano de assistência à saúde TOP – Titular do plano RTOP – Reembolso do titular do plano DTOP – Dependente do titular RDTOP Reembolso do dependente PSS Prestador de serviço de saúde RPPSS Responsável pelo pagamento ao prestador do serviço de saúde BRPPSS Beneficiário do serviço pago FIMDmed Término da declaração

3 Leiaute do arquivo 3.1 Registro de informação da declaração (identificador Dmed)

Registro obrigatório no arquivo; Deve ser o 1º (primeiro) registro no arquivo;

Ordem Campo Formato Preenchimento Tamanho Valores Válidos Obrigatório

1 C Fixo 4 Dmed Sim

2 Ano referência N Fixo 4 2025 Sim 3 Ano-calendário N Fixo 4 2019 a 2025 Sim Indicador de S Retificadora 4 C Fixo 1 Sim retificadora N Original 5 Número do recibo N Fixo 12 - Não

6 C Fixo 6 - Não estrutura do leiaute

5 Número do recibo Se a declaração for original, não preencher;

Se a declaração for retificadora, deverá ser preenchido com o número do recibo da última declaração entregue, se o declarante não transmitir a declaração com assinatura digital.

3.2 Registro do Responsável pelo preenchimento (identificador RESPO)

Registro obrigatório no arquivo; Deve ser o 2º (segundo) registro no arquivo;

Ordem Campo Formato Preenchimento Tamanho Valores Válidos Obrigatório

1 C Fixo 5 RESPO Sim

2 CPF N Fixo 11 - Sim 3 Nome C Variável 60 - Sim 4 DDD N Fixo 2 - Sim 5 Telefone N Fixo 9 - Sim 6 Ramal N Variável 6 - Não 7 Fax N Fixo 9 - Não 8 Correio eletrônico C Variável 50 - Não

3.3 Registro de informação do declarante pessoa jurídica (identificador DECPJ)

Registro obrigatório no arquivo quando for declarante pessoa jurídica; Deve ser o 3º (terceiro) registro no arquivo; Ocorre somente uma vez no arquivo; Ordem Campo Formato Preenchimento Tamanho Valores Obrigatório

1 Identificador C Fixo 5 DECPJ Sim de registro 2 CNPJ N Fixo 14 - Sim 3 Nome C Variável 150 - Sim empresarial 4 Tipo do N Fixo 1 1 Prestador Sim declarante de serviço de saúde;

Operadora de plano de assistência à saúde; 3 Prestador de serviço de saúde e Operadora de plano de assistência à saúde. 5 Registro ANS N Fixo 6 - Não 6 CNES N Fixo 7 - Não 7 CPF N Fixo 11 - Sim responsável perante o CNPJ

8 Indicador de C Fixo 1 S– Sim situação da Declaração declaração de situação especial; N – Não é declaração de situação especial. 9 Data do evento D Fixo 8 - Não 10 Indicador C Fixo 1 S– Não declarante Declarante possui registro possui ANS registro na ANS; N– Declarante não possui registro na ANS

5 Registro ANS Agência Nacional de Saúde Suplementar – ANS; Preenchimento obrigatório se campo de ordem 4 – Tipo do declarante igual a “2” ou “3”; e campo de ordem 10 – Indicador declarante possui registro ANS igual a “S”. 6 CNES Cadastro Nacional de Estabelecimentos de Saúde – CNES. 9 Data do evento Preenchimento obrigatório se campo de ordem 8 – Indicador de situação da declaração igual a “S”. 10 Indicador declarante Preenchimento obrigatório se campo de ordem 4 – possui registro ANS Tipo do declarante igual a “2” ou “3”.

3.4 Registro de informação da operadora de plano de assistência à saúde (identificador OPPAS)

Ocorre caso o declarante seja operadora de plano de assistência à saúde.

1 C Fixo 5 OPPAS Sim

Preenchimento obrigatório se o campo de ordem 4 – Tipo do Declarante, do registro DECPJ igual a “2”; Identificador de Preenchimento opcional se o campo de ordem 4 – Tipo do

registro Declarante, do registro DECPJ igual a “3”, e o declarante não exerceu atividades de Operadora de Plano de Assistência à Saúde no ano-calendário.

3.5 Registro de informação do titular do plano (identificador TOP)

Deve estar classificado em ordem crescente por CPF do titular; Deve estar associado ao registro do tipo OPPAS.

1 C Fixo 3 TOP Sim

2 CPF do titular N Fixo 11 - Sim 3 Nome C Variável 60 - Sim Valor pago no ano 4 N Variável 9 - Não com o titular

Valor pago no ano Preenchimento obrigatório se não existir registros RTOP e/ou

com o titular DTOP associados ao TOP.

3.6 Registro de informação de reembolso do titular do plano (identificador RTOP)

Deve estar classificado em ordem crescente por CPF/CNPJ do prestador de serviço (primeiro os CPF e depois os CNPJ); Deve estar associado ao registro do tipo TOP; Só deverá constar o registro se houver valor de reembolso do ano-calendário ou de anos- calendário anteriores.

1 C Fixo 4 RTOP Sim

2 CPF/CNPJ do N Variável 14 CPF com 11 Sim prestador de dígitos; serviço CNPJ com 14 dígitos. 3 Nome/Nome C Variável 150 Nome da Sim empresarial do pessoa prestador de física até 60 serviço posições. Nome empresarial da pessoa jurídica até

posições. 4 Valor do N Variável 9 - Não reembolso do ano- calendário Valor do reembolso - 5 N Variável 9 Não de anos anteriores

Valor do reembolso do ano- Valores reembolsados no ano-calendário, referentes 4 calendário a pagamentos de serviços prestados no ano- calendário. Valor do reembolso de anos Valores reembolsados no ano-calendário referentes 5 anteriores a pagamentos de serviços prestados em anos anteriores.

3.7 Registro de informação de dependente do titular (identificador DTOP)

Deve estar classificado em ordem crescente por CPF e Data de nascimento do dependente; Deve estar associado ao registro do tipo TOP.

1 C Fixo 4 DTOP Sim

2 CPF do dependente N Fixo 11 - Não 3 Data de Nascimento D Fixo 8 - Não 4 Nome C Variável 60 Sim Relação de Conforme Dependência Tabela de 5 N Fixo 2 Não Relação de Dependência Valor pago no ano 6 N Variável 9 - Não com o dependente

CPF do Preenchimento obrigatório para maiores de 18 anos completos até 31

dependente de dezembro do ano-calendário da declaração. Data de Preenchimento obrigatório para menores de 18 anos completos até 31 3 nascimento de dezembro do ano-calendário da declaração, que não tenham informado o CPF.

3.8. Registro de informação de reembolso do dependente (identificador RDTOP)

Deve estar classificado em ordem crescente por CPF/CNPJ do prestador de serviço (primeiro os CPF e depois os CNPJ); Deve estar associado ao registro do tipo DTOP; Só deverá constar o registro se houver valor de reembolso do ano-calendário e de anos- calendário anteriores.

1 Identificador de registro C Fixo 5 RDTOP Sim 2 CPF/CNPJ do N Variável 14 CPF com 11 Sim prestador de serviço dígitos; CNPJ com 14 dígitos. 3 Nome/Nome C Variável 150 Nome da Sim Empresarial do pessoa prestador de serviço física até 60 posições; Nome empresarial da pessoa jurídica até

posições. 4 Valor do reembolso N Variável 9 - Não do ano-calendário Valor do reembolso de 5 N Variável 9 - Não anos anteriores

Valor do reembolso do Valores reembolsados no ano-calendário, referentes a

ano-calendário pagamentos de serviços prestados no ano-calendário. Valor do reembolso de Valores reembolsados no ano-calendário referentes a 5 anos anteriores pagamentos de serviços prestados em anos anteriores.

3.9 Registro de informação do prestador de serviço de saúde (identificador PSS)

Ocorre caso o declarante seja prestador de serviço de saúde.

1 C Fixo 3 PSS Sim

Identificador de Preenchimento obrigatório se o campo de ordem 4 Tipo do registro Declarante, do registro DECPJ igual a “1”; Preenchimento opcional se o campo de ordem 4 Tipo do

Declarante, do registro DECPJ igual a “3”, e o declarante não exerceu atividades de Prestador de Serviços de Saúde no ano-calendário.

3.10 Registro de informação do responsável pelo pagamento ao prestador do serviço de saúde (identificador RPPSS)

Deve estar classificado em ordem crescente por CPF do responsável pelo pagamento; Deve estar associado ao registro do tipo PSS.

1 C Fixo 5 RPPSS Sim

CPF do responsável 2 N Fixo 11 - Sim pelo pagamento 3 Nome C Variável 60 - Sim Valor pago no ano 4 pelo responsável em N Variável 9 - Não benefício próprio

Valor pago no ano Preenchimento obrigatório se não existir registro BRPPSS 4 pelo responsável em associado ao RPPSS. benefício próprio

3.11 Registro de informação de beneficiário do serviço pago (identificador BRPPSS)

Deve estar classificado em ordem crescente por CPF e Data de nascimento do beneficiário; Deve estar associado ao registro do tipo RPPSS.

1 C Fixo 6 BRPPSS Sim

2 CPF do beneficiário N Fixo 11 - Não 3 Data de nascimento D Fixo 8 - Não

4 Nome C Variável 60 - Sim Valor pago no ano 5 N Variável 9 >0 Sim com o beneficiário

Data de nascimento Preenchimento obrigatório para o beneficiário do serviço de 3 saúde que não informar o número do CPF quando da prestação do serviço.

3.12 Registro identificador do término da declaração (identificador FIMDmed)

Registro obrigatório no arquivo; Deve ser o último registro no arquivo;

1 C Fixo 7 FIMDmed Sim

4 Tabela de relação de dependência Código Descrição 03 Cônjuge/companheiro 04 Filho/filha 06 Enteado/enteada 08 Pai/mãe 10 Agregado/outros

