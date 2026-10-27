---
titulo: "INSTRUÇÃO NORMATIVA BCB Nº 777, DE 18 DE SETEMBRO DE 2026"
orgao: "Banco Central do Brasil/Área de Organização do Sistema Financeiro e de Resolução/Departamento de Competição e de Estrutura do Mercado Financeiro"
tipo: "Instrução Normativa"
numero: "777"
data: 2026-09-18
revogada: false
versao_texto: "publicação original"
publicacao: "DOU de 21/09/2026, seção 1, p. 196"
data_publicacao: 2026-09-21
edicao: "178"
fonte: "https://www.in.gov.br/web/dou/-/instrucao-normativa-bcb-n-777-de-18-de-setembro-de-2026-732957511"
baixado_em: 2026-10-15
---
# INSTRUÇÃO NORMATIVA BCB Nº 777, DE 18 DE SETEMBRO DE 2026

INSTRUÇÃO NORMATIVA BCB Nº 777, DE 18 DE SETEMBRO DE 2026

Divulga a versão 2.2 do Manual de Fluxos do Processo de Efetivação do Pix, que compõe o Regulamento do Pix.

O Chefe do Departamento de Competição e de Estrutura do Mercado Financeiro (Decem), no uso das atribuições que lhe conferem os arts. 23, caput, inciso I, alínea "a", e 94, caput, inciso IX, do Regimento Interno do Banco Central do Brasil, anexo à Resolução BCB nº 340, de 21 de setembro de 2023, e tendo em vista o disposto no art. 2º, caput, inciso III, do Regulamento anexo à Resolução BCB nº 1, de 12 de agosto de 2020, resolve:

**Art. 1º** Esta Instrução Normativa divulga a versão 2.2 do Manual de Fluxos do Processo de Efetivação do Pix, que compõe o Regulamento do Pix, conforme art. 2º do Regulamento anexo à Resolução BCB nº 1, de 12 de agosto de 2020.

**Parágrafo único.** O Manual de Fluxos do Processo de Efetivação do Pix está disponível no endereço eletrônico do Banco Central do Brasil na internet, na página destinada aos manuais que compõem o Regulamento do Pix: https://www.bcb.gov.br/content/estabilidadefinanceira/pix/Regulamento\_Pix/III\_Manualde FluxosdoProcessodeEfetivacaodoPix.pdf.

**Art. 2º** Fica revogada a Instrução Normativa BCB nº 631, de 5 de junho de 2025.

**Art. 3º** Esta Instrução Normativa entra em vigor em 1 de fevereiro de 2027.

Ricardo Teixeira Leite Mourão

## ANEXO

Manual de Fluxos do Processo de Efetivação do Pix Versão 2.2

Histórico de revisão

Data

Versão

Descrição das alterações

11/8/2020

1.0

Versão inicial.

10/9/2020

1.1

Ajuste no fluxo 2.3, sobre a geração da ordem de pagamento por QR Code dinâmico. Fluxo é exatamente igual ao fluxo de geração da ordem de pagamento por QR Code estático. Após o usuário pagador ler o QR Code dinâmico, PSP do pagador envia a chave contida no payload do QR para o DICT. Após retorno do DICT, PSP do pagador apresenta as informações do payload e as informações do usuário recebedor para o usuário pagador, solicitando confirmação do pagamento.

22/7/2021

1.2

Estrutura: inserção da subseção 2.1.3 "Prestador de serviço de iniciação de transação de pagamento, com acesso direto ao DICT".

Estrutura: inserção da subseção 2.4 "Geração da ordem de pagamento pelo serviço de iniciação de transação de pagamento, nos casos em que o participante possui todas as informações do usuário recebedor".

Seção 2.3: detalhamento da tabela de passo a passo, para explicitar melhor o processo de geração da ordem por QR Code dinâmico.

29/9/2021

1.3

Ajuste no fluxo 2.2 "Geração da ordem de pagamento por QR Code estático" e na tabela.

Estrutura: inserção da subseção 2.3.1 "Pix Cobrança para pagamento imediato".

Estrutura: inserção da subseção 2.3.2 "Pix Cobrança para pagamento com vencimento".

Estrutura: inserção da seção 2.4 "Geração da ordem de pagamento de um Pix Agendado por inserção manual de dados ou por meio de chave Pix".

Estrutura: ajustes de numeração na subseção subsequente 2.5. "Geração da ordem de pagamento pelo serviço de iniciação de transação de pagamento, nos

casos em que o participante possui todas as informações do usuário recebedor."

29/10/2023

1.4

Seção 3.1: ajuste no texto explicativo e no fluxo para definição das ordens de pagamento que devem ser enviadas para o canal primário de transmissão de mensagens do SPI e para o canal secundário de transmissão de mensagens do SPI.

Seção 3.2: ajuste no texto explicativo e no fluxo para definição das ordens de pagamento que devem ser enviadas para o canal primário de transmissão de mensagens do SPI e para o canal secundário de transmissão de mensagens do SPI.

Seção 3.3: ajuste no texto explicativo e no fluxo em razão da criação do canal secundário de transmissão de mensagens do SPI.

Seção 3.4: ajuste no texto explicativo e no fluxo em razão da criação do canal secundário de transmissão de mensagens do SPI.

30/08/2024

2.0

Seção 3: inclusão de fluxos com liquidação agendada da ordem de pagamento (Pix Agendado, Pix Agendado recorrente e Pix Cobrança com vencimento).

Estrutura: inserção da seção 5 - Fluxos do Pix Automático.

Estrutura: revisão geral dos fluxos e textos explicativos.

05/06/2025

2.1

Estrutura: inserção da subseção 2.6 "Geração da ordem de pagamento por aproximação (NFC)".

Seção 3.1: ajuste no texto explicativo para inclusão do Pix Automático entre as ordens de pagamento que devem ser enviadas para o canal secundário de transmissão de mensagens do SPI.

Seção 5: ajuste no texto explicativo para indicação dos fluxos do Pix Automático que ocorrem no canal primário de transmissão de mensagens do SPI e no canal secundário de transmissão de mensagens do SPI.

Seção 5.1.3.1: ajuste no texto explicativo para ressaltar que o PSP do Recebedor deve aguardar a conclusão do fluxo de liquidação do primeiro pagamento imediato antes de dar prosseguimento a etapa de atualização do status da recorrência.

Seção 5.1.5.1: ajuste no texto explicativo para pontuar que após o cancelamento da recorrência, caso existam agendamentos pendentes a serem cancelados, a responsabilidade pelo seu cancelamento é do PSP do usuário pagador.

Seção 5.1.5.2: ajuste no texto explicativo para pontuar que após o cancelamento da recorrência, caso existam agendamentos pendentes a serem cancelados, a

responsabilidade pelo seu cancelamento é do PSP do usuário pagador.

01/02/2027

2.2

Seções 2.4, 3.1, 3.1.2, 3.2.2, 3.3.2 e 3.4.2: ajuste nos textos explicativos para retirada das referências ao Pix Agendado recorrente.

Seção 3: inclusão de texto explicativo sobre o tratamento das cobranças híbridas.

NOTA

O Decreto nº 10.411, de 30 de junho de 2020, prevê a obrigatoriedade da realização de análise de impacto regulatório (AIR) para a edição de atos normativos de interesse geral produzidos pelos órgãos e entidades da administração pública federal direta e indireta.

Todavia, consoante se definiu no parágrafo 8 do Voto 280/2021-BCB, de 10 de novembro de 2021, o Regulamento do Pix, inclusive os demais documentos que o integram ou que o detalham e o complementam, não se caracterizam como ato regulatório de força cogente, ostentando, em verdade, natureza eminentemente contratual. Assim, modificações promovidas no referido regulamento e nos demais documentos que o integram ou que o detalham e o complementam não se sujeitam à produção prévia de AIR.

Dessa forma, fica a presente Instrução Normativa dispensada da prévia produção de AIR.

Ricardo Teixeira Leite Mourão
