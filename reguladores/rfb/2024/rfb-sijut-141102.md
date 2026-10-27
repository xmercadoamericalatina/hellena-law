---
titulo: "Instrução Normativa RFB nº 2229, de 15 de outubro de 2024"
orgao: "Secretaria Especial da Receita Federal do Brasil"
tipo: "Instrução Normativa"
numero: "2229"
data: "2024-10-15"
revogada: false
evidencia_revogacao: "vigente:true"
vigente_fonte: true
versao_texto: "publicação original — visão original da fonte"
publicacao: "Publicado(a) no DOU de 16/10/2024, seção 1, página 84"
data_publicacao: "2024-10-16"
fonte: "https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/141102/visao/original"
fonte_api: "https://normasinternet2.receita.fazenda.gov.br/api/consulta-externa/ato/141102/visao/original"
fonte_indice: "https://normas.receita.fazenda.gov.br/api/indexacao/ato/pesquisar"
id_rfb: "141102"
sha256_texto: "7a83110f056e6e92eb790121c4f766b8816b8a421f22376d03ccaed9d16a1fb1"
baixado_em: "2026-10-16"
---
# Instrução Normativa RFB nº 2229, de 15 de outubro de 2024

Altera a Instrução Normativa RFB nº 2.119, de 6 de dezembro de 2022, para estabelecer o formato alfanumérico para o número identificador do Cadastro Nacional da Pessoa Jurídica no âmbito da Secretaria Especial da Receita Federal do Brasil.

O SECRETÁRIO ESPECIAL DA RECEITA FEDERAL DO BRASIL, no uso da atribuição que lhe confere o art. 350, caput, inciso III, do Regimento Interno da Secretaria Especial da Receita Federal do Brasil, aprovado pela Portaria ME nº 284, de 27 de julho de 2020, resolve:

**Art. 1º** A Instrução Normativa RFB nº 2.119, de 6 de dezembro de 2022, passa a vigorar com as seguintes alterações:

"Art. 2º ....................................................................................................

**Parágrafo único.** O CNPJ adotará o formato alfanumérico composto por quatorze posições, conforme disposto no Anexo XV, com previsão de implementação a partir de julho de 2026." (NR)

"Art. 37 ...................................................................................................

**§ 8º** A entidade ou estabelecimento filial será imediatamente declarada Suspensa, a partir da ciência do termo de retenção, caso seja constatada a realização de atividades de comercialização, exposição, armazenamento, guarda ou transporte de produtos proibidos, que representem potencial risco à saúde pública, ao meio ambiente ou à segurança, tais como cigarros eletrônicos, vapes, fumígenos, entre outros, especialmente durante operações de combate ao contrabando, descaminho, tráfico internacional de drogas e lavagem de dinheiro, sem prejuízo das demais sanções cabíveis."

(NR)

**Art. 2º** A Instrução Normativa RFB nº 2.119, de 6 de dezembro de 2022, passa a vigorar acrescida do Anexo XV, nos termos do Anexo Único desta Instrução Normativa.

**Art. 3º** Esta Instrução Normativa entrará em vigor 10 (dez) dias após sua publicação no Diário Oficial da União.

ROBINSON SAKIYAMA BARREIRINHAS

ANEXO ÚNICO



ANEXO ÚNICO (Anexo XV da Instrução Normativa RFB nº 2.119, de 6 de dezembro de 2022)

1. Informações Básicas: CNPJ Numérico x CNPJ Alfanumérico Informações Básicas CNPJ numérico CNPJ alfanumérico Os números existentes serão mantidos. Será destinado a novas inscrições. Tamanho: 14 posições Tamanho: 14 posições 1ª a 8ª posições: numéricas, compondo a raiz do 1ª a 8 ª posições: alfanuméricas, compondo a raiz do CNPJ. CNPJ. 9ª a 12ª posições: numéricas, identificando a 9ª a 12ª posições: alfanuméricas, identificando a ordem do ordem do estabelecimento. estabelecimento. 13ª e 14ª posições: numéricas, identificando os 13ª e 14ª posições: numéricas, identificando os dígitos dígitos verificadores. verificadores.

2. Composição do CNPJ Numérico X Composição do CNPJ Alfanumérico Solução CNPJ Alfanumérico

CNPJ (14 posições) CNPJ alfanumérico (14 posições)

NN.NNN.NNN / NNNN - NN SS.SSS.SSS / SSSS - NN ↓ ↓ ↓ ↓ ↓ ↓ RAIZ ORDEM DV RAIZ ORDEM DV

N- Número N- Número S- Letra e Número

3. Forma de cálculo do Digito Verificador Cálculo do Dígito Verificador CNPJ CNPJ numérico CNPJ alfanumérico Cálculo pelo Módulo 11 Cálculo pelo Módulo 11

4. Detalhamento dos Cálculos dos Dígitos Verificadores do CNPJ Alfanumérico

5.1 Atribuição de valores aos números e às letras do CNPJ 5.1.1 Os valores decimais, contidos na Tabela Código ASCII, serão atribuídos aos valores numéricos e alfanuméricos do novo CNPJ. 5.1.2 Valores numéricos serão substituídos pelo valor decimal constante da tabela código ASCII e, para cada um deles, subtraído o valor 48. 5.1.3 Valores alfanuméricos serão substituídos pelos valores decimais relativos às letras maiúsculas da tabela código ASCII e, para cada um deles, subtraído o valor 48. 5.4 Dessa forma, obtêm-se os valores para cada atributo do novo CNPJ. 5.2 Atribuição de pesos aos valores obtidos após os procedimentos descritos

5.2.1 Os valores obtidos após os passos anteriores serão multiplicados por pesos, atribuídos da esquerda para direita, do valor 2 até o valor 9. 5.2.2 A partir do 8º caractere será reiniciada a atribuição dos pesos pelo valor 2. 5.3 Somatório 5.3.1 Realiza-se o somatório de todos os valores obtidos x pesos atribuídos. 5.3.2 Opera-se o módulo do somatório pelo valor 11 encontrando-se o valor do “resto”. 5.3.3 Se o “resto” da divisão for igual a zero ou 1, o dígito verificador será igual a zero. 5.4 Subtração 5.4.1 Será subtraído do valor 11 o valor do “resto”, encontrando-se, assim, o 1º DV. 5.4.2 O 2º DV será calculado da mesma maneira, incluindo-se o valor atribuído ao 1º dígito verificador nos procedimentos acima descritos.

EXEMPLOS DOS CÁLCULOS DOS DÍGITOS VERIFICADORES

5. Exemplo 1: Cálculo do 1º Dígito Verificador Cálculo do 1º Dígito Verificador do CNPJ Alfanumérico CNPJ alfanumérico 12.ABC.345/ 01DE

1 2. A B C. 3 4 5 /0 1 D E 1 2 17 18 19 3 4 5 / 0 1 20 21 Valores atribuídos (Valor ASCII - 48)

5 4 3 2 9 8 7 6/5 4 3 2 Pesos atribuídos

5 8 51 36 171 24 28 30 0 4 60 42 ∑= 459

MOD (459/11) = 8 MOD (∑ ÷ 11) = N° obtido

11-8 = 3 11- N° obtido = 1° DV

1º DV = 3

6. Exemplo 2: Cálculo do 2º Dígito verificador Cálculo do 2º Dígito Verificador do CNPJ Alfanumérico CNPJ alfanumérico 12.ABC.345/ 01DE - 3

1 2. A B C. 3 4 5 /0 1 D E - 3 1 2 17 18 19. 3 4 5 / 0 1 20 21 - 3 Valores atribuídos (Valor ASCII - 48)

6 5 4 3 2 9 8 7 6 5 4 3- 2 Pesos atribuídos

6 10 68 54 38 27 32 35 0 5 80 63 6 ∑= 424

MOD (424/11) = 6 MOD (∑ ÷ 11) = N° obtido

11-6=5 11- N° obtido = 2° DV

2º DV = 5

CNPJ alfanumérico = 12. ABC.345 /01DE–35

7. Tabela Código ASC II

