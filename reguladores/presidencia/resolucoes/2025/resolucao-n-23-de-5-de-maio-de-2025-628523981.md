---
titulo: "RESOLUÇÃO Nº 23, de 5 de MAIO de 2025"
orgao: "Presidência da República/Casa Civil/Câmara-Executiva Federal de Identificação do Cidadão"
tipo: "Resolução"
numero: "23"
data: 2025-05-05
revogada: false
versao_texto: "publicação original"
publicacao: "DOU de 09/05/2025, seção 1, p. 3"
data_publicacao: 2025-05-09
edicao: "86"
fonte: "https://www.in.gov.br/web/dou/-/resolucao-n-23-de-5-de-maio-de-2025-628523981"
baixado_em: 2026-10-15
---
# RESOLUÇÃO Nº 23, de 5 de MAIO de 2025

RESOLUÇÃO Nº 23, de 5 de MAIO de 2025

Altera a Resolução nº 20, de 9 de setembro de 2024, da Câmara Executiva Federal de Identificação do Cidadão - CEFIC, que institui o Modelo Informacional da Carteira de Identidade Nacional, no âmbito dos órgãos de identificação civil dos Estados e do Distrito Federal e dos órgãos federais executores do Serviço de Identificação do Cidadão, e dá outras providências.

O COORDENADOR DA CÂMARA-EXECUTIVA FEDERAL DE IDENTIFICAÇÃO DO CIDADÃO - CEFIC, no uso das atribuições que lhe confere o art. 6º, §1º, inc. IV, do Regimento Interno da CEFIC, aprovado pela Resolução nº 10, de 6 de abril de 2023, da CEFIC, torna público que a CÂMARA-EXECUTIVA FEDERAL DE IDENTIFICAÇÃO DO CIDADÃO, no exercício da competência de que trata o art. 10, do Decreto nº 11.797, de 27 de novembro de 2023, em reunião ordinária realizada em 22 de abril de 2025, resolve:

**Art. 1º** A Resolução nº 20, de 9 de setembro de 2024, da Câmara Executiva Federal de Identificação do Cidadão - CEFIC, passa a vigorar com as seguintes alterações:

"Art. 1º .................................................................................................................................................................................................................................................................

**§ 1º** O conteúdo e as estruturas das informações que compõem o referido modelo de informação estão descritos no anexo a esta Resolução" (NR).

"Art. 3º Os órgãos executores do SIC deverão apresentar, no prazo de 30 dias após a publicação desta Resolução, cronograma de implementação integrado para adoção do Modelo Informacional da CIN no âmbito do Grupo de Trabalho Técnico.

........................................................................................................................................................................................................................................................................................

**§ 2º** O cronograma de implementação deverá ser executado em até 180 dias, para o cumprimento do disposto no art. 2º.

............................................................................................................................................................................................................................................................................" (NR).

**Art. 2º** Fica revogado o art. 2º da Resolução nº 9, de 7 de novembro de 2022, da CEFIC.

**Art. 3º** O Anexo I da Resolução nº 20, de 9 de setembro de 2024, da CEFIC, fica substituído pelo Anexo constante nesta Resolução.

**Art. 4º** Esta publicação entra em vigor na data da sua publicação.

PEDRO HELENA PONTUAL MACHADO

## ANEXO

## ANEXO

Tabela I - Modelo Informacional da Carteira de Identidade Nacional

| Nível | Ocorrência | Seção/Item | Tipo de Dado | Conceito/Observações/Regrasde negócio | CIN física - papele cartão | CIN digital - Carteira de documentos digitais do aplicativo Gov.br | Bases Legais |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [1..1] | Identificação do órgão expedidor | Seção |  |  |  |  |
| 2 | [1..1] | Órgão Expedidor / Card Issuer | Texto Codificado | Indica o nome do órgão que expede a CIN, conforme padrão da coluna "Representação na CIN" da Tabela II. | Texto variável, 37 caracteres por linha, máximo 2 linhas; Fonte: Tahoma Bold | Texto variável, 37 caracteres por linha, máximo 2 linhas; Fonte: Tahoma Bold | Art. 3º, c, da Lei nº 7.116/83;Art. 11, III, do Decreto nº |
|  |  |  |  |  | 5pt; Cor Preta. | 4.8pt; Cor Preta. | 10.977/2022;Art. 8°, III, da Lei Complementar nº 123/2006. |
| 2 | [0..1] | Cargo do(a) dirigente do órgão expedidor | Caracteres alfanuméricos | Nome do cargo do(a) dirigente do órgão expedidor. | Texto variável, máximo 18 caracteres; Fonte: Arial Regular 5pt; Cor Preta. | Texto variável, máximo 18 caracteres; Fonte: Arial Regular 3.5pt; Cor Preta. |  |
| 2 | [1..1] | Assinatura do Expedidor / Card Issuer Signature | Imagem | Imagem da assinatura do(a) dirigente responsável pelo órgão expedidor (Tabela II). | Imagem base64; Cor Preta. | 500.000 caracteres (png em base64). | Art. 3º, g, da Lei nº 7.116/83;Art. 11, VIII, do Decreto nº 10.977/22; |
|  |  |  |  |  |  |  | Art. 3º-A, § 1º, IV, da Lei nº 13.977/2020. |
| 1 | [1..1] | Caracterização da expedição | Seção |  |  |  |  |
| 2 | [1..1] | Ente federativo | Texto codificado | Indica o ente federativo que expediu a CIN, conforme padrão da coluna | Texto variável, máximo 29 caracteres; Fonte: | Texto variável, máximo 29 caracteres; Fonte: | Art. 3º, b, da Lei nº 7.116/83;Art. 11, II, do Decreto nº |
|  |  |  |  | "Representação na CIN" da Tabela III. | Arial Bold 6pt, Cor Preta. | Arial Bold 6pt, Cor Preta. | 10.977/2022;Art. 3º-A, § 1º, IV, da Lei nº 13.977/2020. |
| 2 | [1..1] | Data de Emissão / | Data | Data de emissão/expedição da CIN, no formato AAAA/MM/DD, conforme | Texto variável, máximo 10 caracteres; Fonte: | Texto variável, máximo 10 caracteres; Fonte: | Art. 3º, d, da Lei nº 7.116/83; Art. 11, X, do |
|  |  | Issue Date |  | ISO 8601. | Tahoma Bold 5.5pt (papel); 5pt (cartão); Cor Preta. | Tahoma Bold 5pt; Cor Preta. | Decreto nº 10.977/2022. |
| 2 | [1..1] | Local / Place of Issue | Texto codificado | Código de 7 dígitos do município de expedição, conforme IBGE. | Sem representação. | Sem representação. | Art 3º, d, da Lei nº 7.116/1983;Art. 11, X do Decreto nº 10.977/2022. |
| 3 | [1..1] | Nome do município | Texto codificado | Nome do município de expedição sem | Texto variável, máximo 36 caracteres, em até 2 | Texto variável, máximo 36 caracteres, em até 2 | Art 3º, d, da Lei nº 7.116/1983;Art. 11, X, do |
|  |  | de expedição |  | referência à UF, conforme descrição | linhas; Fonte: Tahoma Bold; Tamanho da Fonte: 5pt; Cor Preta. | linhas; Fonte: Tahoma Bold 5pt; Cor Preta. | Decreto nº 10.977/2022. |
|  |  |  |  | do código na Tabela do IBGE. | Para municípios com mais de 36 caracteres, o elemento deve ser abreviado. |  |  |
| 2 | [0..1] | Data de Validade / | Data | Data de validade do documento, no formato AAAA/MM/DD, conforme ISO 8601. | Texto variável, máximo 14 caracteres; Fonte: Tahoma Bold; | Texto variável, máximo 14 caracteres; Fonte: Tahoma Bold 5pt; | Art. 3º, d, da Lei nº 7.116/1983;Art. 11, X, do Decreto nº |
|  |  | Date of Expiry |  | Regra Negocial: A data de validade deve ser verificada com a data de nascimento. Para titulares maiores de 60 (sessenta) anos, indicar validade como "Indeterminada". | Tamanho da Fonte: 5pt; Cor Preta. | Cor Preta. | 10.977/2022. |
| 3 | [0..1] | Validade Indeterminada | Booleano | Indica a validade indeterminada para o(a) titular maior de 60 (sessenta) anos. | Texto variável, máximo 14 caracteres; Fonte: Tahoma Bold 5pt; Cor Preta. | Texto variável, máximo 14 caracteres; Fonte: Tahoma Bold 5pt; Cor Preta. | Art. 3º, d, da Lei nº 7.116/1983;Art. 11, X, do Decreto nº 10.977/2022. |
| 2 | [1..1] | Identificador do | Caracteres numéricos | Identificador da CIN impressa, por um | Texto variável, máximo 12 | Sem representação. | Manual da Carteira de Identidade Nacional - Projeto Gráfico e |
|  |  | Espelho |  | sequencial alfanumérico de controle. | caracteres; Fonte: Arial Bold 5pt; Cor Preta. |  | Elementos de Segurança - Ministério da Justiça e Segurança Pública. |
| 1 | [1..1] | Identificador nacional | Seção |  |  |  |  |
| 2 | [1..1] | Registro Geral-CPF / | Caracteres numéricos | O identificador do cidadão é o número de inscrição do(a) titular no CPF. Regra Negocial: Caso o cidadão não | Texto variável, máximo 14 caracteres; Fonte: Tahoma Bold 7.5pt; Cor Preta. | Texto variável, máximo 14 caracteres, Fonte: Tahoma Bold 7.5pt; Cor Preta. | Art.3º, h e seu § 1º, da Lei nº 7.116/83;Art. 3º do Decreto nº 10.977/2022;Art.5° do Decreto |
|  |  | Personal Number |  | tenha CPF, ou necessita atualizar seus dados biográficos, os órgãos de identificação civil devem inscrever ou alterar CPF no Cadastro. | CPF - Dígitos com mascaramento: xxx.xxx.xxx-xx | CPF - Dígitos com mascaramento: xxx.xxx.xxx-xx | nº 11.797/2023. |
| 1 | [1..1] | Informações biográficas do(a) titular | Seção |  |  |  |  |
| 2 | [1..1] | Prenome / Given names | Caracteres alfanuméricos, alfabeto latino, padrão HTML UTF-8 (Capital Letter), conformeTabela IV | Indica o "nome individual" do(a) titular. Regras Negociais: - O conjunto de caracteres válidos para nome consta na Tabela IV; | Representação do nome completo. | Representação do nome completo. | ICAO 9303-4;Art. 11, XII, do Decreto nº 10.977/2022;Art. 148 da Lei nº 6.015/1973; |
|  |  |  |  | - Os nomes que contêm caracteres não incluídos naTabela IV deverão sofrer transliteração; - Em caso de algarismos arábicos no nome, registrar por extenso ou romano. |  |  | ISO 9:1995. |
| 2 | [0..1] | Sobrenome / Surname | Caracteres alfanuméricos, alfabeto latino, padrão HTML UTF-8 (Capital Letter), conformeTabela IV | Indica o sobrenome. Mesmas regras negociais do Prenome. | Representação do nome completo. | Representação do nome completo. | ICAO 9303-4;Art. 11, XII, do Decreto nº 10.977/2022;Lei nº 10.406/2002 (Código Civil). |
| 2 | [1..1] | Nome completo | Caracteres alfanuméricos, alfabeto latino, padrão HTML UTF-8 (Capital Letter), conformeTabela IV | Indica o prenome, sobrenome e agnome, se houver, do(a) titular. Mesmas regras negociais do Prenome. | Representação do nome completo (prenome + sobrenome). | Representação do nome completo (prenome + sobrenome). | Lei nº 7.116/1983;Decreto nº 10.977/2022. |
|  |  |  |  |  | Texto variável, 37 caracteres por linha, máximo 2 linhas; Fonte: Tahoma Bold 5pt; Cor Preta. | Sequência de caracteres alfanuméricos, com limite de 74, máximo 2 linhas; Fonte: Tahoma Bold 4.8 pt. |  |
|  |  |  |  |  | Para emissão da CIN física e digital, caso ultrapasse o limite de caracteres determinado, seguir | Para emissão da CIN física e digital, caso ultrapasse o limite de caracteres |  |
|  |  |  |  |  | regras de abreviação da Resolução CEFIC nº 15, 01/11/2023. | determinado, seguir regras de abreviação da Resolução CEFIC nº 15, 01/11/2023. |  |

| 3 | [0..1] | Nome Social / Social Name | Caracteres alfanuméricos, alfabeto latino, padrão HTML UTF-8 (Capital Letter), conforme Tabela IV | Nome designado pela pessoa travesti ou transexual que se identifica e é socialmente reconhecida.Mesmas regras negociais do Prenome. | Texto variável, 37 caracteres por linha, máximo 2 linhas.Fonte: Tahoma Bold; Tamanho da Fonte: 5pt; Cor Preta. | Sequência de caracteres alfanuméricos, com limite de 37 caracteres por linha, máximo 2 linhas. | Art. 13 do Decreto nº 10.977/2022; Decreto nº 8.727/2016; Art. 2° da Resolução CEFIC nº 15, 01/11/2023. |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | Para emissão da CIN | Fonte: Tahoma Bold; Tamanho da Fonte: 4.8 pt.Para emissão da CIN física e digital, caso |  |
|  |  |  |  |  |  | ultrapasse o limite de caracteres determinado, seguir regras de abreviação da Resolução CEFIC nº 15, 01/11/2023. |  |
|  |  |  |  |  | física e digital, caso ultrapasse o limite de caracteres determinado, seguir regras de abreviação |  |  |
|  |  |  |  |  | da Resolução CEFIC nº 15, 01/11/2023. |  |  |
| 2 | [0..N] | Filiação / Filiation | Caracteres alfanuméricos, | Indica o nome completo da filiação | Texto variável, para 4 filiações, uma filiação por linha até o limite de 37 | Sequência de caracteres alfanuméricos, com limite de 37 | Art. 13 do Decreto nº 10.977/2022; Decreto nº 8.727/2016; |
|  |  |  |  |  | caracteres por linha;Para menos de 4 filiações: em caso de filiação ter menos de 37 caracteres, utilizar | caracteres por linha, máximo 4 linhas; Fonte: Tahoma Bold 4.8pt. | Art. 2° da Resolução CEFIC nº 15, de 01/11/2023. |
|  |  |  |  |  | uma por linha, se houver mais de 37 caracteres, pode ser | Para emissão da CIN física e digital, caso ultrapasse o limite |  |
|  |  |  |  |  | usada mais de uma linha, até o limite de 4 linhas;Fonte: Tahoma Bold 5pt; Cor Preta. | de caracteres determinado, seguir regras de abreviação da Resolução CEFIC nº 15, 01/11/2023. |  |
|  |  |  |  |  | Para emissão da CIN física e digital, caso ultrapasse o limite de caracteres determinado, seguir |  |  |
|  |  |  |  |  | regras de abreviação da Resolução CEFIC nº 15, 01/11/2023. |  |  |
|  |  |  | alfabeto latino, padrão HTML UTF-8 (Capital Letter), conforme Tabela IV | do(a) titular.Mesmas regras negociais do campo Prenome. |  |  |  |
| 3 | [0..N] | CPF da Filiação | Caracteres numéricos | Identificador da filiação da criança e do adolescente, menor de 16 anos, para gestão da CIN digital na Carteira de documentos digitais do aplicativo Gov.br. | Texto variável, máximo 14 caracteres; Fonte: Tahoma Bold 7.5pt; Cor Preta. | Texto variável, máximo 14 caracteres; Fonte: Tahoma Bold 7.5pt; Cor Preta. |  |
| 2 | [1..1] | Sexo / Sex | Texto codificado ICAO | Indica o sexo do(a) titular, conforme padronização da ICAO, 1 caractere, M, F ou X (Masculino; Feminino; Indeterminado / Não especificado). | Texto variável, máximo 1 caracter; Fonte: Tahoma Bold 5.5pt; Cor Preta. | Texto variável, máximo 1 caracter;Fonte: Tahoma Bold 5.5pt; Cor Preta. | Art. 5º da Lei nº 7.116/1983;Art. 11, V, do Decreto nº 10.977/22;ICAO 9303-4. |
| 2 | [1..1] | Nacionalidade / | Texto codificado IBGE | Indica a nacionalidade do(a) titular, brasileiro(a) nato(a), brasileiro(a) | Texto variável, | Texto variável, | Art. 5º da Lei nº 7.116/1983; Art. 11, V, do Decreto nº |

|  |  |  |  | naturalizado(a) ou português(a) | máximo 3 caracteres; | máximo 3 caracteres; | 10.977/2022;Art. 12 da Constituição Federal de 1988; |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | Nationality | Países (ISO 3166-1) e padrão ISO ALPHA-3 | equiparado(a), sendo permitido somente as opções BRA ou PRT | Fonte: Tahoma Bold | Fonte: Tahoma Bold | Art. 75 da Lei nº 13.445/2017;Art. 248 a 253 do Decreto nº 9.199/2017; |
|  |  |  |  | (brasileira; português equiparado). | 5.5pt; Cor Preta. | 5.5pt; Cor Preta. | Portaria Interministerial nº 11, de 03/05/2018. |
| 2 | [0..1] | Naturalidade / Place | Subseção | Indica o local de nascimento do(a) | Texto variável, 19 | Texto variável, 19 | Art. 3º, alínea 'e', da Lei nº 7.116/83;Art. 11, V, do |
|  |  |  |  |  |  |  | Decreto nº 10.977/2022; Resolução CCGD/ME nº 6, |
|  |  | of Birth |  | titular. | caracteres por linha, | caracteres por linha, | 25/08/2021.Art. 12 da Constituição Federal de 1988; |
|  |  |  |  |  |  |  | Art. 75 da Lei nº 13.445/2017; Art. 248 a 253 do |
|  |  |  |  |  | máximo 2 linhas; Fonte: Tahoma Bold | máximo 2 linhas; Fonte: Tahoma Bold | Decreto nº 9.199/2017;Portaria Interministerial nº 11, de 03/05/2018;Convenção para a |
|  |  |  |  |  | 5,5pt; Cor Preta. | 5pt; Cor Preta. | Redução dos Casos de Apatridia, promulgada pelo Decreto nº 8.501/2015. |
| 3 | [0..1] | Código Município | Texto codificado | Código do município do(a) titular, de 7 dígitos, conforme IBGE.Regras Negociais:- Para nome de local de nascimento | Sem representação. | Sem representação. |  |
|  |  |  |  | que não exista na tabela de municípios do IBGE, realizar dois registros: 1) indicar código IBGE atual do município que corresponde ao |  |  |  |
|  |  | Naturalidade |  | local de nascimento no campo atual; e 2) indicar, em texto livre, no campo "Naturalidade conforme Certidão" o local conforme consta na Certidão de Nascimento/Casamento; |  |  |  |
|  |  |  |  | - Nos casos de naturalidade em branco na Certidão de Nascimento/Casamento, esse campo deverá ficar em branco e o campo "Inexistência de Naturalidade na Certidão" deverá ser marcado. |  |  |  |
| 3 | [0..1] | UF Naturalidade | Texto codificado | Código da Unidade da Federação, de 2 dígitos, conforme IBGE.Regras Negociais:- Nos casos de naturalidade em | Sem representação. | Sem representação. |  |
|  |  |  |  | branco na Certidão de Nascimento/Casamento, esse campo deverá ficar em branco e o campo "Inexistência de Naturalidade na Certidão" deverá ser marcado. |  |  |  |
| 3 | [0..1] |  | Caracteres alfanuméricos | Nome do município (cidade), conforme código do IBGE.Regras Negociais:- Nos casos de naturalidade em | Sem representação. | 50 caracteres. |  |
|  |  | Município Naturalidade |  | branco na Certidão de Nascimento/Casamento, esse campo deverá ficar em branco e o campo "Inexistência de Naturalidade na Certidão" deverá ser marcado. |  |  |  |
| 3 | [0..1] | País de Naturalidade | Texto codificado | Indica o país de nascimento do(a) titular, conforme IBGE Países.Regras Negociais: |  | 3 caracteres. |  |
|  |  |  |  | - Nos casos de titular nascido(a) fora do território nacional (estrangeiro(a) naturalizado(a), brasileiro(a) nascido(a) fora do território nacional, ou português(a) equiparado(a)), obrigatoriamente, deve ser indicado o |  |  |  |
|  |  |  |  | país de nascimento pela tabela atualizada de Países IBGE. |  |  |  |

|  |  |  |  | - Para brasileiros(as) nascidos(as) fora do território nacional e em país não reconhecido pelo Brasil, deve-se |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  | registrar o país reconhecido pelo Brasil em que a cidade está contida. Exemplo: Pristina, Sérvia; Taipé, China. |  |  |  |
|  |  |  |  | - Nos casos de naturalidade em branco na Certidão de Nascimento/Casamento, esse campo |  |  |  |
|  |  |  |  | deverá ficar em branco e o campo "Inexistência de Naturalidade na Certidão" deverá ser marcado. |  |  |  |
|  |  |  |  | - Código identificador do país - Especificado pela norma IBGE Países, que define o identificador do país usando 3 letras. |  |  |  |
| 3 | [0..1] | Naturalidade | Caracteres alfanuméricos | Local de nascimento conforme consta na Certidão de Nascimento/Casamento quando o nome de local de nascimento não existir na tabela de Municípios do | Essa informação deve prevalecer na CIN física. | 50 caracteres. |  |
|  |  | conforme Certidão |  | IBGE; caso exista, esse campo não deve ser preenchido.Regras Negociais: |  |  |  |
|  |  |  |  | - Para nome de local de nascimento que não exista na tabela de Municípios do IBGE, realizar dois |  |  |  |
|  |  |  |  | registros: 1) indicar, em texto livre, neste campo o local conforme consta na Certidão de |  |  |  |
|  |  |  |  | Nascimento/Casamento; e 2) indicar o código IBGE atual do município que corresponde ao local de nascimento no campo Código Município Naturalidade.- Nos casos de naturalidade em |  |  |  |
|  |  |  |  | branco na Certidão de Nascimento/Casamento, esse campo deverá ficar em branco e o campo "Inexistência de Naturalidade na Certidão" deverá ser marcado. |  |  |  |
| 3 | [0..1] | Inexistência de Naturalidade na | Booleano | Indica a inexistência de naturalidade na Certidão de Nascimento/Casamento. Regra Negocial: | Deve ser representada a expressão: "não consta". | Deve ser representada a expressão: "não consta". |  |
|  |  | Certidão |  | Se não houver registro de naturalidade na Certidão, este campo deve ser marcado e todos os demais campos referentes à naturalidade devem ficar em branco. |  |  |  |
| 2 | [0..1] |  | Data | Identifica a data de nascimento do(a) titular, conforme apresentado pela certidão de nascimento ou de casamento em formato físico ou digital, conforme ISO 8601 (AAAA/MM/DD). |  |  |  |
|  |  | Data de Nascimento |  | Regras Negociais: - Não será permitida data anterior a 01/01/1901;- Será permita data incompleta, como |  |  |  |
|  |  |  |  | mês e ano (MM/AAAA) ou somente ano (AAAA);- Não será permitido dia e mês;- Caso conste data fora do padrão |  |  |  |
|  |  | / Date of Birth |  | ISO8601, esse campo não deve ser preenchido e o campo de inexistência deve ser marcado. Exemplo: DD/MM ou DD ou MM não são permitidos;- Nos casos de data de nascimento em |  |  |  |
|  |  |  |  | branco na Certidão de Nascimento/ Casamento, o campo "Inexistência de Data de Nascimento na Certidão" deve ser marcado e o campo atual deve ficar em branco. |  |  |  |
| 3 | [0..1] | Inexistência de Data | Booleano | Indica a inexistência da data de nascimento na Certidão de Nascimento/Casamento. | Deve ser representada a expressão: "não consta". | Deve ser representada a expressão: "não consta". |  |
|  |  | de Nascimento na |  | Regra Negocial: Se não houver registro de data de nascimento na Certidão, o campo |  |  |  |
|  |  | Certidão |  | atual deve ser marcado indicando a inexistência de data e o campo "data de nascimento" deve ficar em branco. |  |  |  |
| 3 | [1..1] | CPF do(a) | Caracteres alfanuméricos | Indica o CPF do(a) representante legal da criança e do adolescente, menor de 16 anos, ou incapaz, para inscrição e/ou alteração do CPF no processo de | Sem representação. | Sem representação. | Anexo IV e V da Instrução Normativa RFB nº 2.172, de |
|  |  | representante legal |  | emissão da CIN. Regras Negociais:Em se tratando de guardião institucional (art. 92, § 1º, do Estatuto |  |  | 09/01/2024, atualizada pela Portaria Cocad nº 67, 05/08/2024; |
|  |  |  |  | da Criança e do Adolescente), é necessária a apresentação de documentação que comprove o |  |  | Art. 3° da Lei nº 10.406/2002 (Código Civil); |
|  |  |  |  | acolhimento institucional da criança ou adolescente (ex. Guia de |  |  | Art. 14, §1°, da Lei nº 13.709/2018 (LGPD);Provimento nº 61/2017;Art. 92, § 1º, da Lei |
|  |  |  |  | Acolhimento Institucional - modelo do CNJ, Instrução Normativa CNJ nº |  |  | nº 8.069/1990 (Estatuto da Criança e do Adolescente);Instrução |
|  |  |  |  | 03/2009) e documento que comprove que o solicitante é dirigente da entidade de abrigo.Em se tratando de criança e adolescente em unidade socioeducativa de internação, deverá ser observado o fluxo de exceção |  |  |  |
|  |  |  |  | previsto no Anexo V da Instrução |  |  | Normativa CNJ n° |
|  |  |  |  | Normativa RFB nº 2.172/2024, atualizado pela Portaria Cocad nº 67/2024. |  |  | 03/2009. |
| 4 | [1..1] | Vínculo do(a) | Texto codificado:1 - uma das filiações;2 -tutor;3 -curador; | Indica o vínculo do(a) representante legal da criança e do adolescente, menor de 16 anos, ou incapaz, para | Sem representação. | Sem representação. | Anexo IV da Instrução Normativa RFB nº 2.172, de 09/01/2024;Art. 3° da Lei nº 10.406/2002 |
|  |  | representante legal | 4 -guardião;5-representante por decisão judicial. | inscrição e/ou alteração do CPF no processo de emissão da CIN. |  |  | (Código Civil);Art. 14, §1°, da Lei nº 13.709/2018 (LGPD);Provimento nº 61/2017. |
| 2 | [1..1] | Endereço do(a) | Subseção | Identifica o endereço de domicílio do(a) titular no Brasil ou no exterior | Sem representação. | Representação somente do endereço do(a) titular portador(a) de | Instrução Normativa RFB nº 2172/2024;Lei nº 13.977/2020. |
|  |  |  |  | para inscrição no CPF e se titular |  | Ciptea. Exemplo: Avenida Alameda das Travessas, nº 111, Edifício Bosque |  |
|  |  | titular |  | portador de Carteira de Identificação da Pessoa com Transtorno do |  | do Cerrado, 2222 - Bairro dos Barris.CEP: 40000-000. Salvador/BA. |  |
|  |  |  |  | Espectro Autista (Ciptea). |  | Texto variável, máximo 255 caracteres; Fonte: Tahoma 12pt. |  |
| 3 | [0..1] | CEP Residência | Caracteres numéricos | Código de endereçamento postal (08 dígitos). | Sem representação. | Texto variável, máximo 8 caracteres; Fonte: Tahoma 12pt. |  |
| 3 | [1..1] | Código Município Residência | Texto codificado | Código do município na base de dados de município do IBGE. | Sem representação. | Texto variável, máximo 7 caracteres; Fonte: Tahoma 12pt. |  |
| 3 | [1..1] | UF Residência | Texto codificado | Sigla da Unidade da Federação. | Sem representação. | Texto variável, máximo 2 caracteres; Fonte: Tahoma 12pt. |  |
| 3 | [1..1] | Município Residência | Caracteres alfanuméricos | Nome do município (cidade). | Sem representação. | Texto variável, máximo 50 caracteres; Fonte: Tahoma 12pt. |  |

| 3 | [1..1] | Bairro | Caracteres alfanuméricos | Comunidade ou região dentro de uma cidade ou município.Para os endereços localizados no Distrito Federal, utiliza-se o modelo de divisão territorial utilizado pelo IBGE, que estabelece Brasília como | Sem representação. | Texto variável, máximo 50 caracteres; Fonte: Tahoma 12pt. |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  | único município. Dessa forma, para as regiões administrativas (RA) não divididas em bairros, estes locais devem ser informados como bairro. No caso das RA subdividas em bairros, informar o bairro e a RA entre parênteses. Ex.: Veredas (Brazlândia). |  |  |  |
| 3 | [1..1] | Logradouro | Caracteres alfanuméricos | Logradouro (empregado para se referir a uma localidade, tal como rua, praça, avenida ou um espaço público que compõe uma cidade). | Sem representação. | Texto variável, máximo 100 caracteres; Fonte: Tahoma 12pt. |  |
| 3 | [0..1] | Número | Caracteres alfanuméricos | Número do Endereço. | Sem representação. | Texto variável, máximo 20 caracteres; Fonte: Tahoma 12pt. |  |
| 3 | [0..1] | Complemento | Caracteres alfanuméricos | Complemento do endereço. | Sem representação. | Texto variável, máximo 50 caracteres; Fonte: Tahoma 12pt. |  |
| 3 | [0..1] | País de residência no | Texto codificado | Indica país de residência do(a) titular se domicílio fora do Brasil, conforme IBGE Países alpha 3.Regra negocial:Realizar o registro do código do país no campo atual e o registro do | Sem representação. | Texto variável, máximo 3 caracteres; Fonte: Tahoma 12pt. |  |
|  |  | exterior |  | endereço completo em texto livre no campo "Endereço residência no exterior".Código identificador do país - Especificado pela norma IBGE Países, que define o identificador do país usando 3 letras. |  |  |  |
| 4 | [0..1] | Endereço de residência no exterior | Caracteres alfanuméricos | Descrição do endereço de residência quando no exterior. | Sem representação. | Texto variável, máximo 200 caracteres; Fonte: Tahoma 12pt. |  |
| 2 | [1..1] | Documento de | Caracteres alfanuméricos | Número da matrícula de 32 dígitos da Certidão de Nascimento ou da Certidão de Casamento válida (com Averbação, quando for o caso), ou do Certificado de Naturalização do(a) titular. | Sem representação. | Texto variável, máximo 120 caracteres | Art. 3º, e, da Lei nº 7.116/83;Art. 11, VI, do Decreto nº 10.977/2022;Provimento nº 63, |
|  |  | origem |  | Regra Negocial:- Se certidão de nascimento ou casamento não estiver em formato de |  |  | de 14/11/2017 (DJe de 17/11/2017). |
|  |  |  |  | matrícula indicar, excepcionalmente, em texto livre, comarca, cartório, livro, folha e número do registro. |  |  |  |
| 3 | [0..1] | Data de emissão do documento de | Data | Data de emissão do documento de origem do(a) titular. | Sem representação. | Sem representação. | Art. 3º, e, da Lei nº 7.116/83;Art. 11, VI, do Decreto nº |
|  |  | origem |  | Atenção: Esta informação se refere a data de emissão do documento e não a data de nascimento ou casamento. |  |  | 10.977/2022;Provimento nº 63, de 14/11/2017 (DJe de 17/11/2017). |
| 2 | [0..1] | Estado Civil | Texto codificado:1 - solteiro(a)2 - casado(a) | Indica o estado civil do(a) titular.Observação: união estável não se | Sem representação. | Sem representação. | Código Civil;Provimento CNJ 61 - praticar o ato;Art. 1.571 da Lei nº 10.406/2002 |
|  |  |  | 3 - divorciado(a)4 - separado(a)/ | configura como estado civil. Caso seja apresentada e escritura de união |  |  | (Código Civil);Art. 315 da Lei nº 3.071/1916 (Código |
|  |  |  | desquitado(a)5 - viúvo(a) | estável, o registro deve ser de solteiro(a). |  |  | Civil de 1916);Lei nº 6.515/1977 (Lei do Divórcio). |
| 2 | [0..N] | Documentos adicionais do(a) titular | Subseção | Informações de documentos adicionais do(a) titular. |  |  |  |
| 3 | [0..1] | PIS / PASEP | Caracteres alfanuméricos | Número de inscrição do(a) titular no Programa de Integração Social (PIS) e no Programa de Formação do | Sem representação. | Texto variável, máximo 14 caracteres; Fonte: | Art. 4º da Lei nº 7.116/83. |
|  |  |  |  | Patrimônio do Servidor Público (PASEP), de acordo com a documentação apresentada pelo(a) requerente. |  | Tahoma 12pt. |  |
| 3 | [0..1] | NIS | Caracteres alfanuméricos | Número de Identificação Social (NIS), de acordo com a documentação apresentada pelo(a) requerente. | Sem representação. | Texto variável, máximo 14 caracteres; Fonte: | Art. 14 do Decreto nº 10.977/2022;Art. 1º, item 1, da |
|  |  |  |  |  |  | Tahoma 12pt. | Lei nº 9.049/95;§1º, art. 4º, da Lei nº 7.116/83. |
| 3 | [0..1] | NIT | Caracteres numéricos | Número de Inscrição do Trabalhador (NIT), de acordo com a documentação | Sem representação. | Texto variável, máximo 14 | Art. 14 do Decreto nº 10.977/2022;Art. 1º, item 1, da |
|  |  |  |  | apresentada pelo(a) requerente. |  | caracteres; Fonte: Tahoma 12pt. | Lei nº 9.049/95;§1º, art. 4º, da Lei nº 7.116/83. |
| 3 | [0..1] | CTPS | Caracteres alfanuméricos | Número da Carteira de Trabalho e Previdência Social (CTPS), de acordo com a documentação apresentada pelo(a) requerente. | Sem representação. | Texto variável, máximo 22 caracteres; Fonte: Tahoma 12pt. | Art. 14 do Decreto nº 10.977/2022;Art. 1º, item 1, da Lei nº 9.049/95;§1º, art. 4º, da Lei nº 7.116/83. |
| 3 | [0..1] | Título de Eleitor | Caracteres alfanuméricos | Indica o número de inscrição eleitoral do(a) titular, de acordo com a | Sem representação. | Texto variável, máximo 14 | Art. 14 do Decreto nº 10.977/2022;Art. 1º, item 1, da Lei nº 9.049/95;§1º, art. 4º, da Lei |
|  |  |  |  | documentação apresentada pelo(a) requerente. |  | caracteres; Fonte: Tahoma 12pt. | 7.116/83.Resolução TSE nº 23.659, de 26/10/2021. |
| 3 | [0..1] | CNH | Caracteres numéricos | Número do Registro Nacional do condutor, de acordo com a Carteira | Sem representação. | Texto variável, máximo 18 | Art. 14 do Decreto nº 10.977/2022;Art. 1º, item 1, da Lei nº 9.049/95; |
|  |  |  |  | Nacional de Habilitação (CNH) apresentada pelo(a) requerente. |  | caracteres; Fonte: Tahoma 12pt. | §1º, art. 4º, da Lei nº 7.116/83.Resolução CONTRAN nº 886, de 13/12/2021. |
| 4 | [1..1] | Data de validade da | Data | Data de validade da Carteira Nacional de Habilitação, conforme ISO 8601.Regra Negocial: As informações da | Sem representação. | Texto variável, máximo 10 | Art. 14 do Decreto nº 10.977/2022;Art. 1º, item 1, da Lei nº 9.049/95; |
|  |  | CNH |  | CNH devem ser coletadas somente se a data estiver dentro do prazo de validade, no momento da solicitação do(a) titular. |  | caracteres; Fonte: Tahoma 12pt. | §1º, art. 4º, da Lei nº 7.116/83.Resolução CONTRAN nº 886, de 13/12/2021. |
| 5 | [1..1] | Categoria da CNH | Texto codificado: A, B, C, D, E, X, AB, AC, AD, AE, XB, | Indica letra(s) correspondente à(s) categoria(s) na(s) qual(is) o(a) condutor(a) for habilitado(a) na | Sem representação. | Texto variável, máximo 4 caracteres; | Art. 14 do Decreto nº 10.977/2022;Art. 1º, item 1, da Lei nº 9.049/95;§1º, art. 4º, da Lei |
|  |  |  | XC, XD, XE | Carteira Nacional de Habilitação (CNH), conforme Tabela V. |  | Fonte: Tahoma 12pt. | nº 7.116/83.Resolução CONTRAN nº 886, de 13/12/2021. |
| 3 | [0..N] | Identidade Funcional | Caracteres alfanuméricos | Número, Unidade Federativa e órgão emissor da Carteira de Identidade | Sem representação. | Texto variável, máximo 28 | Art. 14 do Decreto nº 10.977/2022;Art. 1º, item 1, da |
|  |  | ou Carteira Profissional |  | Profissional emitido/registrado nos sistemas próprios das categorias profissionais. |  | caracteres; Fonte: Tahoma 12pt. | Lei nº 9.049/95;§1º, art. 4º, da Lei 7.116/83. |
| 3 | [0..1] | Certificado Militar | Caracteres alfanuméricos | Certificado Militar do(a) titular que | Sem representação. | Texto variável, máximo 14 | Art. 14 do Decreto nº 10.977/2022;Art. 1º, item 1, da |
|  |  |  |  | comprove a quitação com o serviço militar obrigatório. |  | caracteres; Fonte: Tahoma 12pt. | Lei nº 9.049/95;§1º, art. 4º, da Lei nº 7.116/83. |
| 1 | [1..1] | Informações biométricas do(a) titular | Seção |  |  |  |  |
| 2 | [1..1] | Fotografia da face | Imagem facial | Apresenta a fotografia do(a) titular de acordo com os requisitos para captura | Resolução 300 dpi; tamanho máximo de 200 kb; Formato Mínimo de 640x480 | Resolução mínima: 250 x 250 pixels.Resolução desejável: 750 x 750 pixels. | Art. 3º, f, da Lei nº 7.116/83;Art. 11, VII, do Decreto nº |
|  |  |  |  | e codificação de imagens faciais, padrão ICAO, especificados na ISO/IEC 39794-5. | PNG OU JPEG; Papel: imagem colorida; Cartão: imagem em preto e branco. | Tamanho máximo do base64: 500.000 caracteres. Imagem colorida. | 10.977/2022;ICAO Doc 9303, Machine Readable Travel Documents. |
| 2 | [1..1] | Impressão digital | Booleano | Indica se o(a) titular possui impressão digital. | Sem representação. | Sem representação. | Art. 3º, f, da Lei nº 7.116/83;Art. 11, VII, do Decreto nº 10.977/2022. |
| 3 | [1..N] | Posição do dedo da impressão digital | Texto codificado: | "Indica a posição do dedo da impressão digital contida na ficha decadactilar, conforme especificação ISO/IEC 19794-2:2011. | Sem representação. | Sem representação. | Art. 3º, f, da Lei nº 7.116/83;Art. 11, VII, do Decreto nº 10.977/2022. |
|  |  |  | 0 - posição do dedo desconhecida; |  |  |  |  |
|  |  |  | 1 - polegar direito; |  |  |  |  |
|  |  |  | 2 - indicador direito; |  |  |  |  |
|  |  |  | 3 - médio direito; |  |  |  |  |
|  |  |  | 4 - anular direito; |  |  |  |  |
|  |  |  | 5 - mínimo direito; |  |  |  |  |
|  |  |  | 6 - polegar esquerdo; |  |  |  |  |
|  |  |  | 7 - indicador esquerdo; |  |  |  |  |
|  |  |  | 8 - médio esquerdo; |  |  |  |  |
|  |  |  | 9 - anular esquerdo; |  |  |  |  |

| 4 | [1..N] | Fotografia da | Imagem | Apresenta até 10 (dez) fotografias, uma para cada dedo da impressão digital.Regras negociais:- Todas as dez impressões digitais devem ser coletadas, no entanto, se | Sem representação. | Formato: WSQ ou PNG; Resolução 500 DPI; Dimensão: 640 x 600 pixels (altura x largura); Tamanho máximo do base64: 500.000 caracteres. | Art. 3º, f, da Lei nº 7.116/83;Art. 11, VII, do Decreto nº 10.977/2022. |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | impressão digital |  | um ou mais dedos não estiverem disponíveis (por exemplo, devido a amputação), deverão ser coletados os dedos disponíveis. |  |  |  |
|  |  |  |  | - Quando menos de dez dedos forem coletados, será requerido o campo "indisponibilidade da impressão digital". |  |  |  |
| 5 | [0..N] | Indisponibilidade da | Texto codificado:XX: Leitura parcial ou | Indica os dedos que foram amputados ou dedos que não estavam disponíveis, no momento da captura, conforme padrão ANSI/NIST-ITL 1-2011. | Sem representação. | Sem representação. | Art. 3º, f, da Lei nº 7.116/83;Art. 11, VII, do Decreto nº 10.977/2022. |
|  |  |  | indisponível por | Regras negociais:- Campo obrigatório quando houver menos de 10 fotografias de impressão |  |  |  |
|  |  | impressão digital | amputação /*Amputated*;UP: Dedo temporariamente | digital;- O campo é composto pela junção de dois itens de informação: Posição do dedo + código de amputado ou de temporariamente indisponível. |  |  |  |
|  |  |  | indisponível/*Unable to Print* | Exemplo:Dedo médio direito amputado: 3XX; dedo mínimo esquerdo enfaixado por acidente: 10UP. |  |  |  |
| 2 | [0..1] | Assinatura do(a) titular / Cardholder's | Imagem | Indica a assinatura do(a) titular, representado por um gesto gráfico.Regras negociais:- Para casos de não alfabetizados ou impossibilitados de assinatura (por deficiência ou perda de função | Formato PNG ou JPEG; Resolução 300dpi; tamanho mínimo 300KB; tamanho máximo 1024KB. | 500.000 caracteres (png em base64).A assinatura precisa estar centralizada, ter o fundo transparente e tamanho 285x70 pixels. | Art. 3º, alínea 'f', da Lei nº 7.116/83;Art. 11, VII, do Decreto nº 10.977/2022. |
|  |  | Signature |  | momentânea), registrar a justificativa e apresentar na CIN a expressão "Não assinou nesse ato";- Caso o(a) titular possua nome social, a assinatura poderá ser do nome social. |  |  |  |
| 3 | [0..1] | Justificativa de ausência da assinatura | Texto codificado:1 - Não alfabetizado;2 - Impossibilitado. | Indica a justificativa do não envio da assinatura do(a) titular. | "Não assinou nesse ato". | "Não assinou nesse ato". |  |
| 1 | [0..1] | Informações de saúde do(a) titular | Seção |  |  |  |  |
| 2 | [0..1] | Observações de | Caracteres alfanuméricos | Informações sobre condições específicas de saúde cuja divulgação possa contribuir para preservar a saúde do(a) titular ou salvar a sua | Sem representação. | Texto variável 50 caracteres; Fonte: | Art. 14, § 2º, do Decreto nº 10.977/2022;Art. 2º da Lei nº |
|  |  |  |  | vida. Regra Negocial:Se solicitado pelo(a) titular, é possível |  | Tahoma 12 pt. | 9.049/95;§1º, art. 4º, da Lei nº 7.116/83;ABNT NBR |
|  |  | Saúde |  | incluir código e descrição da Classificação Estatística Internacional de Doenças e Problemas Relacionados com a Saúde (CID). Atenção à |  |  | 9050:2020. |
|  |  |  |  | descrição de doenças, pois trata-se de dado pessoal sensível e pode gerar algum tipo de discriminação.Exemplo: CID M79.7: Fibromialgia. |  |  |  |
| 2 | [0..1] | Tipo sanguíneo / | Texto codificado:A+; A-; B+; B-; AB+; AB-; | Tipo sanguíneo e fator RH positivo (+) ou negativo (-) do(a) titular.A+; A-; B+; B-; AB+; AB-; O+; O-, de | Sem representação. | Texto variável, máximo 3 caracteres; | Art. 14, § 2º, do Decreto nº 10.977/2022;Art. 2º da Lei nº |
|  |  | Fator RH | O+; O- | acordo com a documentação apresentada pelo requerente. |  | Fonte: Tahoma 12pt. | 9.049/95;§1º, art. 4º, da Lei nº 7.116/83. |
| 2 | [0..1] | Doador de Órgãos | Booleano | Disposição do(a) titular a doar órgãos | Sem representação. | Texto variável, máximo 3 caracteres; | Art. 14, § 2º, do Decreto nº 10.977/2022; |
|  |  |  |  | em caso de morte. |  | Fonte: Tahoma 12pt. | Art. 2º da Lei nº 9.049/95;§1º, art. 4º, da Lei nº 7.116/83. |
| 2 | [0..1] | Deficiência Física | Booleano | Identifica a pessoa com deficiência | Pictograma - Imagem | Imagem base64; Cor | Art. 14, § 2º, do Decreto nº 10.977/2022;Art. 2º da Lei nº |
|  |  |  |  | física a partir do Símbolo Internacional de Acesso (SIA). | base64; Cor Preta. | Preta. | 9.049/95;§1º, art. 4º, da Lei nº 7.116/83;ABNT NBR 9050:2020. |

| 2 | [0..1] | Deficiência Auditiva | Booleano | Identifica a pessoa com deficiência auditiva, a partir do símbolo | Pictograma - Imagem | Imagem base64; Cor | Art. 14, § 2º, do Decreto nº 10.977/2022; Art. 2º da Lei nº |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  | internacional de pessoas com deficiência auditiva. | base64; Cor Preta. | Preta. | 9.049/95;§1º, art. 4º, da Lei nº 7.116/83;ABNT NBR 9050:2020. |
| 2 | [0..1] | Deficiência | Booleano | Identifica a pessoa com deficiência | Pictograma - Imagem | Imagem base64; Cor | Art. 14, § 2º, do Decreto nº 10.977/2022; |
|  |  | Intelectual / Psicossocial |  | intelectual / psicossocial. | base64; Cor Preta. | Preta. | Art. 2º da Lei nº 9.049/95;§1º, art. 4º, da Lei nº 7.116/83. |
| 2 | [0..1] | Deficiência Visual | Booleano | Identifica a pessoa com deficiência visual, a partir do símbolo | Pictograma - Imagem | Imagem base64; Cor | Art. 14, § 2º, do Decreto nº 10.977/2022; Art. 2º da Lei nº |
|  |  |  |  | internacional de pessoas com deficiência visual. | base64; Cor Preta. | Preta. | 9.049/95;§1º, art. 4º, da Lei nº 7.116/83;ABNT NBR 9050:2020. |
| 2 | [0..1] | Autismo | Booleano | Identifica a pessoa com Transtorno do | Pictograma fita - | Imagem base64; Cor | Art. 14, III, do Decreto nº 10.977/2022; |
|  |  |  |  | Espectro Autista. | Imagem base64, Cor Preta. | Preta. | Art. 3º-A, § 1º, IV, da Lei nº 13.977/2020. |
| 3 | [0..1] | Ciptea | Booleano | Identifica a pessoa com Transtorno do Espectro Autista que possui a Carteira de Identificação da Pessoa com Transtorno do Espectro Autista (Ciptea). | Sem representação. | Sem representação. | Lei nº 13.977/2020. |
| 4 | [0..1] | Validade da Ciptea | Data | Data de emissão/expedição do documento, no formato AAAA/MM/DD, conforme ISO 8601. | Sem representação. | Texto variável, máximo 10 caracteres;Fonte: Tahoma 12pt. | Art. 3º-A, § 1º, III, da Lei nº 13.977/2020. |
| 4 | [0..N] | Código do diagnóstico | Texto codificado por terminologia externa: cid-9; cid-10; cid-11 | Código do diagnóstico relacionado à condição de saúde do(a) titular. | Sem representação. | 6 caracteres. | Art. 3º-A, § 1º, III, da Lei nº 13.977/2020. |
| 4 | [0..1] | Telefone do(a) titular com TEA | Caracteres alfanuméricos | Indica o telefone do(a) titular com TEA. | Sem representação. | Texto variável, máximo 14 caracteres;Fonte: Tahoma 12pt. | Art. 3º-A, § 1º, III, da Lei nº 13.977/2020. |
| 4 | [0..1] | CPF do(a) responsável | Caracteres numéricos | Identifica o(a) responsável legal ou cuidador(a) do(a) titular com Transtorno do Espectro Autista. | Sem representação. | Texto variável, máximo 11 caracteres; Fonte: Tahoma 12pt. | Art. 3º-A, § 1º, III, da Lei nº 13.977/2020. |
| 4 | [0..1] | Nome do(a) responsável | Caracteres alfanuméricos | Nome completo do(a) responsável legal ou cuidador. | Sem representação. | Sequência de caracteres alfanuméricos, com limite de 255 caracteres; Fonte: Tahoma 12pt. | Art. 3º-A, § 1º, III, da Lei nº 13.977/2020. |
| 4 | [0..1] | Endereço do(a) responsável | Caracteres alfanuméricos | Endereço residencial do(a) responsável legal ou cuidador, no mesmo padrão de endereço de domicílio do(a) titular no Brasil ou no exterior. | Sem representação. | Texto variável, máximo 255 caracteres; Fonte: Tahoma 12pt. | Art. 3º-A, § 1º, III, da Lei nº 13.977/2020. |
| 4 | [0..1] | E-mail do(a) responsável | Caracteres alfanuméricos | E-mail do(a) responsável legal ou cuidador(a). | Sem representação. | Texto variável, máximo 80 caracteres; Fonte: Tahoma 12pt. | Art. 3º-A, § 1º, III, da Lei nº 13.977/2020. |
| 4 | [0..1] | Telefone do(a) responsável | Caracteres alfanuméricos | Telefone do(a) responsável legal ou cuidador(a). | Sem representação. | Texto variável, máximo 14 caracteres; Fonte: Tahoma 12pt. | Art. 3º-A, § 1º, III, da Lei nº 13.977/2020. |

Tabela II - Órgãos de Identificação Civil no Brasil

| UF | Órgão de Identificação | Representação na CIN | CNPJ - Nome Fantasia | CNPJ - Nome Empresarial | CNPJ |
| --- | --- | --- | --- | --- | --- |
| AC | Instituto de Identificação Raimundo Hermínio de Melo | INSTITUTO DE IDENTIFICAÇÃO RAIMUNDO HERMÍNIO DE MELO - IIRHM | POLÍCIA CIVIL DO ESTADO DO ACRE - PCAC | POLÍCIA CIVIL DO ESTADO DO ACRE - PCAC | 10.584.440/0001-97 |
| AL | Instituto de Identificação de Alagoas | INSTITUTO DE IDENTIFICAÇÃO DEL. MÁRIO PEDRO DOS SANTOS | POLÍCIA CIENTIFICA DO ESTADO DE ALAGOAS | PERÍCIA OFICIAL DO ESTADO DE ALAGOAS | 13.898.581/0001-72 |
| AM | Instituto de Identificação Aderson Conceição de Melo | INSTITUTO DE IDENTIFICAÇÃO ADERSON CONCEIÇÃO DE MELO - IIACM | SSP | SECRETARIA DE ESTADO DE SEGURANCA PUBLICA | 01.804.019/0001-53 |
| AP | Departamento de Identificação Civil e Criminal | POLÍCIA CIENTÍFICA DO AMAPÁ | POLITEC | POLÍCIA TECNICO CIENTIFICA | 34.943.480/0001-46 |
| BA | Instituto de Identificação Pedro Mello | SSP/BA | BAHIA SSP GABINETE DO SECRETARIO | BAHIA SECRETARIA DA SEGURANCA PUBLICA | 13.937.149/0001-43 |
| CE | Coordenadoria de Identificação Humana e Perícia Biométrica | PERÍCIA FORENSE DO ESTADO DO CEARÁ COORDENADORIA DE IDENTIFICAÇÃO-CIHPB | PERÍCIA FORENSE DO ESTADO DO CEARA | PERÍCIA FORENSE DO ESTADO DO CEARA | 10.263.825/0001-52 |
| DF | Instituto de Identificação | INSTITUTO DE IDENTIFICAÇÃO PCDF | POLÍCIA CIVIL | POLÍCIA CIVIL DO DISTRITO FEDERAL | 37.115.482/0001-35 |
| ES | Instituto de Identificação da Polícia Científica | INSTITUTO DE IDENTIFICAÇÃO / PCIES | PCIES | POLÍCIA CIENTÍFICA DO ESTADO DO ESPÍRITO | 53.542.025/0001-83 |
| GO | Superintendência de Identificação Humana - Polícia Civil do Estado de Goiás | POLÍCIA CIVIL DE GOIÁS - SIH | POLÍCIA CIVIL DO ESTADO DE GOIAS | POLÍCIA CIVIL | 37.014.123/0001-91 |
| MA | Instituto de Identificação do Maranhão | INSTITUTO DE IDENTIFICAÇÃO DO MARANHÃO |  | ESTADO DO MARANHAO - SECRETARIA DE ESTADO DA SEGURANCA PUBLICA | 06.354.500/0001-08 |
| MG | Instituto de Identificação de Minas Gerais | POLÍCIA CIVIL DO ESTADO DE MINAS GERAIS | POLÍCIA CIVIL DO ESTADO DE MINAS GERAIS | POLÍCIA CIVIL DO ESTADO DE MINAS GERAIS | 18.715.532/0001-70 |
| MS | Instituto de Identificação Gonçalo Pereira | INSTITUTO DE IDENTIFICAÇÃO GONÇALO PEREIRA - IIGP | SEJUSP | SECRETARIA DE ESTADO DE JUSTICA E SEGURANCA PUBLICA - MS | 03.015.475/0001-40 |
| MT | Instituto de Identificação de Mato Grosso Aroldo Mendes de Paiva | INSTITUTO DE IDENTIFICAÇÃO/MT POLITEC | PERÍCIA OFICIAL E IDENTIFICACAO TECNICA - POLITEC | ESTADO DE MATO GROSSO | 03.507.415/0030-89 |
| PA | Identificação da Polícia Civil do Pará Enéas Martins | DIRETORIA DE IDENTIFICAÇÃO ENÉAS MARTINS | POLÍCIA CIVIL DO PARA | POLÍCIA CIVIL DO ESTADO DO PARA | 00.368.105/0001-06 |
| PB | Núcleo de Identificação Civil e Criminal/IPC/DG/SESDS | POLÍCIA CIVIL DO ESTADO DA PARAÍBA |  | POLÍCIA CIVIL DO ESTADO DA PARAIBA | 22.404.257/0001-41 |
| PE | Instituto de Identificação Tavares Buril | INSTITUTO DE IDENTIFICAÇÃO TAVARES BURIL | INSTITUTO DE IDENTIFICACAO TAVARES BURIL - IITB | POLÍCIA CIVIL DE PERNAMBUCO | 10.572.063/0261-32 |
| PI | Instituto de Identificação Digital Félix Pacheco | INSTITUTO DE IDENTIFICAÇÃO DIGITAL "FÉLIX PACHECO" - IIDFP | PI SEC GABINETE DO SECRETARIO | SECRETARIA DE SEGURANCA | 06.553.549/0001-90 |
| PR | Instituto de Identificação do Paraná | INSTITUTO DE IDENTIFICAÇÃO DO PARANÁ | PR SSP GABINETE DO SECRETARIO | SECRETARIA DE ESTADO DA SEGURANCA PUBLICA | 76.416.932/0001-81 |
| RJ | Diretoria de Identificação Civil DETRAN RJ | DETRAN RJ | DETRAN RJ | DEPARTAMENTO DE TRÂNSITO DO ESTADO DO RIO DE JANEIRO | 30.295.513/0001-38 |
| RN | Instituto Técnico-Científico de Perícia do Rio Grande do Norte | ITEP/RN | ITEP | INSTITUTO TECNICO- CIENTÍFICO DE PERÍCIA DO RIO GRANDE DO NORTE -ITEP/RN | 05.067.810/0001-89 |
| RO | Instituto de Identificação Civil e Criminal Engrácia da Costa Francisco | INSTITUTO DE IDENTIFICAÇÃO ENGRÁCIA DA COSTA FRANCISCO - IICCECF/PCRO | SESP | SECRETARIA DE ESTADO DA SEGURANA, DEFESA E CIDADANIA | 04.793.055/0001-57 |
| RR | Instituto de Identificação Odílio Cruz | INST. DE IDENTIFICAÇÃO ODÍLIO CRUZ SECRETARIA DE SEGURANÇA PÚBLICA DE RR | FUNDESPOL - RR | FUNDO DE MODERNIZACAO, MANUTENCAO E DESENVOLVIMENTO DA POLÍCIA CIVIL DO ESTADO DE RORAIMA - FUNDESPOL - RR | 29.827.234/0001-99 |
| RS | Departamento de Identificação do Instituto Geral de Perícias-RS | INSTITUTO-GERAL DE PERÍCIAS/RS | I G P | INSTITUTO GERAL DE PERÍCIAS | 02.626.165/0001-07 |
| SC | Polícia Científica do Estado de Santa Catarina | POLÍCIA CIENTÍFICA DE SANTA CATARINA (PCISC) | POLICIA CIENTIFICA DO ESTADO DE SANTA CATARINA (PCISC) | POLÍCIA CIENTIFICA DO ESTADO DE SANTA CATARINA | 36.127.642/0001-01 |
| SE | Instituto de Identificação de Sergipe | INSTITUTO DE IDENTIFICAÇÃO DE SERGIPE PAP. WENDEL DA SILVA GONZAGA - IIWSG | SECRETARIA DE ESTADO DA SEGURANCA PUBLICA | SECRETARIA DE ESTADO DA SEGURANCA PUBLICA | 34.841.214/0001-02 |
| SP | Instituto de Identificação Ricardo Glumbleton Daunt | INSTITUTO DE IDENTIFICAÇÃO RICARDO GUMBLETON DAUNT - IIRGD | INSTITUTO DE IDENTIFICACAO RICARDO GUMBLETON DAUNT | POLÍCIA CIVIL DO ESTADO DE SAO PAULO | 04.236.548/0008-62 |
| TO | Instituto de Identificação do Tocantins | INSTITUTO DE IDENTIFICAÇÃO SSPTO | SECRETARIA DA SEGURANCA PUBLICA - S.S.P. | SECRETARIA DA SEGURANCA PUBLICA - S.S.P. | 25.053.109/0001-18 |

Tabela III - Ente federativo que expediu a CIN, conforme código IBGE

| Código IBGE | Estado | Sigla | Representação na CIN |
| --- | --- | --- | --- |
| 12 | Acre | AC | Estado do Acre |
| 27 | Alagoas | AL | Estado de Alagoas |
| 13 | Amazonas | AM | Estado do Amazonas |
| 16 | Amapá | AP | Estado do Amapá |
| 29 | Bahia | BA | Estado da Bahia |
| 23 | Ceará | CE | Estado do Ceará |
| 53 | Distrito Federal | DF | Distrito Federal |
| 32 | Espírito Santo | ES | Estado do Espírito Santo |
| 52 | Goiás | GO | Estado de Goiás |
| 21 | Maranhão | MA | Estado do Maranhão |
| 31 | Minas Gerais | MG | Estado de Minas Gerais |
| 50 | Mato Grosso do Sul | MS | Estado do Mato Grosso do Sul |
| 51 | Mato Grosso | MT | Estado do Mato Grosso |
| 15 | Pará | PA | Estado do Pará |
| 25 | Paraíba | PB | Estado da Paraíba |
| 26 | Pernambuco | PE | Estado de Pernambuco |
| 22 | Piauí | PI | Estado do Piauí |
| 41 | Paraná | PR | Estado do Paraná |
| 33 | Rio de Janeiro | RJ | Estado do Rio de Janeiro |
| 24 | Rio Grande do Norte | RN | Estado do Rio Grande do Norte |
| 11 | Rondônia | RO | Estado de Rondônia |
| 14 | Roraima | RR | Estado de Roraima |
| 43 | Rio Grande do Sul | RS | Estado do Rio Grande do Sul |
| 42 | Santa Catarina | SC | Estado de Santa Catarina |
| 28 | Sergipe | SE | Estado de Sergipe |
| 35 | São Paulo | SP | Estado de São Paulo |
| 17 | Tocantins | TO | Estado do Tocantins |

Tabela V - Categorias da Carteira Nacional de Habilitação (CNH) conforme Manual do Registro Nacional de Condutores Habilitados (Renach)

Categoria

Descrição

A

Condutor de veículo motorizado de duas ou três rodas, com ou sem carro lateral.

B

Condutor de veículo motorizado, não abrangido pela categoria A, cujo peso bruto total não exceda a três mil e quinhentos quilogramas e cuja lotação não exceda a oito lugares, excluído o do motorista.

C

Condutor de veículo motorizado utilizado em transporte de carga, cujo peso bruto total exceda a três mil e quinhentos quilogramas.

D

Condutor de veículo motorizado utilizado no transporte de passageiros, cuja lotação exceda a oito lugares, excluído o do motorista.

E

Condutor de combinação de veículos em que a unidade tratora se enquadre nas categorias B, C ou D e cuja unidade acoplada, reboque, semirreboque ou articulada, tenha seis mil quilogramas ou mais de peso bruto total, ou cuja lotação exceda a oito lugares, ou, ainda, seja enquadrado na categoria trailer.

AB

Condutor de veículo motorizado de duas ou três rodas, com ou sem carro lateral; e condutor de veículo motorizado, não abrangido pela categoria A, cujo peso bruto não exceda a três mil e quinhentos quilogramas e cuja lotação não exceda a oito lugares, excluído o do motorista.

AC

Condutor de veículo motorizado de duas ou três rodas, com ou sem carro lateral; e condutor de veículo motorizado utilizado em transporte de carga, cujo peso bruto total exceda a três mil e quinhentos quilogramas.

AD

Condutor de veículo motorizado de duas ou três rodas, com ou sem carro lateral; e condutor de veículo motorizado utilizado no transporte de passageiros, cuja lotação exceda a oito lugares, excluído o do motorista.

AE

Condutor de veículo motorizado de duas ou três rodas, com ou sem carro lateral; e condutor de combinação de veículos em que a unidade tratora se enquadre nas categorias B, C ou D e cuja unidade acoplada, reboque, semirreboque ou articulada, tenha seis mil quilogramas ou mais de peso bruto total, ou cuja lotação exceda a oito lugares, ou, ainda, seja enquadrado na categoria trailer.

X

Autorização para condução de ciclomotor.

XB

Autorização para condução de ciclomotor; e condutor de veículo motorizado, não abrangido pela categoria A, cujo peso bruto não exceda a três mil e quinhentos quilogramas e cuja lotação não exceda a oito lugares, excluído o do motorista.

XC

Autorização para condução de ciclomotor; e condutor de veículo motorizado utilizado em transporte de carga, cujo peso bruto total exceda a três mil e quinhentos quilogramas.

XD

Autorização para condução de ciclomotor; e condutor de veículo motorizado utilizado no transporte de passageiros, cuja lotação exceda a oito lugares, excluído o do motorista.

XE

Autorização para condução de ciclomotor; e condutor de combinação de veículos em que a unidade tratora se enquadre nas categorias B, C ou D e cuja unidade acoplada, reboque, semirreboque ou articulada, tenha seis mil quilogramas ou mais de peso bruto total, ou cuja lotação exceda a oito lugares, ou, ainda, seja enquadrado na categoria trailer.
