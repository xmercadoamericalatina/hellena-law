---
titulo: "Portaria SAES/MS Nº 4.177, DE 25 DE maio DE 2026"
orgao: "Ministério da Saúde/Secretaria de Atenção Especializada à Saúde"
tipo: "Portaria"
numero: "4177"
data: 2026-05-25
revogada: false
versao_texto: "publicação original"
publicacao: "DOU de 29/05/2026, seção 1, p. 105"
data_publicacao: 2026-05-29
edicao: "100"
fonte: "https://www.in.gov.br/web/dou/-/portaria-saes/ms-n-4.177-de-25-de-maio-de-2026-709145893"
baixado_em: 2026-10-15
---
# Portaria SAES/MS Nº 4.177, DE 25 DE maio DE 2026

Portaria SAES/MS Nº 4.177, DE 25 DE maio DE 2026

Altera a Portaria SAES/MS nº 37, de 18 de janeiro de 2021, para atualização de conceitos relacionados à identificação dos veículos de apoio das equipes da Atenção Primária à Saúde.

O SECRETÁRIO DE ATENÇÃO ESPECIALIZADA À SAÚDE substituto, no uso das atribuições que lhe confere o Decreto nº 11.798, de 28 de novembro de 2023, resolve:

**Art. 1º** O Anexo II da Portaria SAES/MS nº 37, de 18 de janeiro de 2022, passa a vigorar conforme o Anexo a esta Portaria.

**Art. 2º** Cabe à Coordenação-Geral de Gestão de Sistemas de Informação em Saúde do Departamento de Regulação Assistencial e Controle da Secretaria de Atenção Especializada à Saúde (CGSI/DRAC/SAES/MS) a adoção das providências necessárias no sentido de adequar o CNES para a implementação das alterações definidas por esta Portaria.

**Art. 3º** Esta Portaria entra em vigor na data de sua publicação, com efeitos operacionais a partir da competência seguinte à sua publicação.

CARLOS AMILCAR SALGADO

## ANEXO

MODELO DE INFORMAÇÃO DO CNES: MÓDULO EQUIPES

O modelo de informação do Módulo de Equipes foi elaborado utilizando a seguinte notação:

Coluna 1 (Nível): indica a relação de dependência do elemento aos demais. Um número maior significa que aquele item depende ou está subordinado ao de número menor e anterior à ele no modelo. Assim, um elemento de nível 2 é subitem de um elemento de nível 1, um de nível 3 é subitem de um de nível 2 e assim sucessivamente.

Coluna 2 (Ocorrência): demonstra a obrigatoriedade e a quantidade de ocorrências do elemento:

\- [0..] - indica que o elemento é opcional;

\- [1..] - indica que o elemento é obrigatório;

\- [..1] - indica que o elemento só pode ocorrer uma única vez;

\- [..N] - indica que o elemento pode ocorrer várias vezes.

Coluna 3 (Seção/Item): descrição do elemento ou de um agrupador de elementos (seção).

Coluna 4 (Tipo de Dados): demonstra a forma de representar o elemento.

Coluna 5 (Conceito): conceitua ou esclarece o elemento.

| NÍVEL | OCORRÊNCIA | SEÇÃO/ITEM | TIPO DE DADO | CONCEITO |
| --- | --- | --- | --- | --- |
| ... | .... | .... | ... | ... |
| 3 | [0..N] | Veículos de Apoio | Secção | Embarcações de pequeno porte ou veículo terrestre para o deslocamento dos profissionais da equipe identificadas conforme programação visual padronizada das unidades de saúde do SUS |
| 4 | [0..N] | Número do Veículo | Caracteres Alfanuméricos | Número do veículo identificado conforme programação visual padronizada das unidades de saúde do SUS |
| 4 | [0..N] | Nome do Veículo | Caracteres Alfanuméricos | Nome de referência do veículo conforme programação visual padronizada das unidades de saúde do SUS |
| 4 | [0..N] | Tipo de Veículo | Seleção | Identifica se é o veículo é uma Embarcação de pequeno porte ou veículo terrestre |
| 4 | [0..N] | Registro do Veículo | Caracteres Alfanuméricos | Nº identificador da embarcação na Marinha do Brasil ou Placa do veículo terrestre |
| ... | .... | .... | ... | ... |
