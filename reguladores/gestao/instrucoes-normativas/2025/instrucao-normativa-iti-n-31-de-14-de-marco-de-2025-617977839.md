---
titulo: "INSTRUÇÃO NORMATIVA ITI Nº 31, DE 14 DE MARÇO DE 2025"
orgao: "Ministério da Gestão e da Inovação em Serviços Públicos/Instituto Nacional de Tecnologia da Informação"
tipo: "Instrução Normativa"
numero: "31"
data: 2025-03-14
revogada: false
versao_texto: "publicação original"
publicacao: "DOU de 17/03/2025, seção 1, p. 33"
data_publicacao: 2025-03-17
edicao: "51"
fonte: "https://www.in.gov.br/web/dou/-/instrucao-normativa-iti-n-31-de-14-de-marco-de-2025-617977839"
baixado_em: 2026-10-15
---
# INSTRUÇÃO NORMATIVA ITI Nº 31, DE 14 DE MARÇO DE 2025

INSTRUÇÃO NORMATIVA ITI Nº 31, DE 14 DE MARÇO DE 2025

Aprova o regulamento de envio de informações e arquivos ao Instituto Nacional de Tecnologia da Informação - ITI.

O DIRETOR-PRESIDENTE DO INSTITUTO NACIONAL DE TECNOLOGIA DA INFORMAÇÃO, no uso das atribuições que lhe foram conferidas pelo inciso VI do art. 13 do Anexo I do Decreto nº 12.103, de 8 de julho de 2024, pelo art. 1º da Resolução nº 33 do Comitê Gestor da ICP-Brasil, de 21 de outubro de 2004, e pelo art. 2º da Resolução nº 163 do Comitê Gestor da ICP-Brasil, de 17 de abril de 2020, resolve:

**Art. 1º** Esta Instrução Normativa regulamenta o envio de informações e arquivos ao Instituto Nacional de Tecnologia da Informação - ITI.

**Parágrafo único.** O disposto nesta Instrução Normativa não se aplica ao Cadastro de Agentes de Registros - CAR, que possui regulamentação própria.

**Art. 2º** Todas as Autoridades Certificadoras - ACs que emitem certificados digitais para usuário final deverão enviar diariamente, incluindo finais de semana e feriados, ao Instituto Nacional de Tecnologia da Informação - ITI os certificados emitidos, as biometrias atreladas a cada certificado e informações sobre suas emissões.

**§ 1º** Os arquivos dos certificados deverão ser identificados e encaminhados individualmente, utilizando a codificação DER (\*.cer).

**§ 2º** Os arquivos biométricos da face e das impressões digitais deverão ter os formatos e a indicação do dedo, se for o caso, conforme disposto no DOC-ICP-05.02, Anexo da Instrução Normativa ITI nº 05, de 22 de fevereiro de 2021, e no DOC-ICP-05.03, Anexo da Instrução Normativa ITI nº 09, de 22 de outubro de 2020, seguindo as definições dispostas no ADE-ICP-05.C.

**§ 3º** As informações, os arquivos dos certificados e os arquivos biométricos deverão ser encaminhados ao ITI em um arquivo compactado (.zip), por meio do carregamento do arquivo (upload) dentro da respectiva área de transferência de arquivos da AC (FTP).

**§ 4º** O nome do arquivo compactado e o procedimento de envio deverão seguir as orientações dispostas no ADE-ICP-05.C, disponível no site do ITI.

**Art. 3º** As informações referentes às emissões deverão ser encaminhadas em um arquivo CSV, identificado com nome "Anexo1.csv", contendo, para cada certificado emitido, o hash SHA1 do arquivo do certificado, associado às informações relacionadas com a emissão do certificado.

**§ 1º** O arquivo CSV deverá conter todos os campos estabelecidos no "Modelo Informacional de Dados dos Certificados Emitidos" do ADE-ICP-05.C, os quais deverão ser preenchidos obedecendo aos critérios de obrigatoriedade indicados na coluna "Presença de conteúdo".

**§ 2º** A primeira linha do arquivo CSV deverá conter o nome das colunas, sendo obrigatório uso das denominações e sequência estabelecidas no "Modelo Informacional de Dados dos Certificados Emitidos" do ADE-ICP-05.C.

**§ 3º** Para os certificados emitidos na modalidade "certificado digital", os seguintes campos do arquivo CSV deverão ser preenchidos com o termo "VAZIO": CPF\_AGR\_i, CPF\_AGR\_v, Data\_i, Data\_v, Data\_PSBIO, TCN, IDN, CPF\_RESP\_SELO, CNPJ\_Titular, Resposta\_DATAVALID, Resposta\_PSBIO, Forma\_pagto e ID\_MAQ\_AGR.

**§ 4º** Cada emissão registrada no arquivo CSV deve corresponder a um certificado enviado no arquivo compactado e todo certificado do arquivo compactado deve ter suas informações registradas no arquivo CSV.

**§ 5º** No dia em que não houver emissão de certificado digital, a AC deverá encaminhar o arquivo "Anexo1.csv" contendo apenas a primeira linha com os nomes das colunas.

**Art. 4º** Anualmente, até o dia 15 de dezembro, em conformidade com o DOC-ICP-08, as Autoridades Certificadoras - ACs, Autoridades de Carimbo do Tempo - ACTs, Prestadores de Serviços Biométricos - PSBios e Prestadores de Serviços de Confiança - PSCs deverão encaminhar ao ITI o Plano Anual de Auditoria Operacional - PLAAO.

**§ 1º** As informações deverão ser encaminhadas ao ITI em um arquivo no formato ZIP, contendo o arquivo PDF do ADE-ICP-08.C e as informações referentes ao PLAAO em arquivo CVS.

**§ 2º** O arquivo compactado deve ser identificado com nome "PLAAO\_ANO\_nome da entidade na ICP-Brasil.zip".

**§ 3º** O arquivo compactado deve ser encaminhado para o e-mail plaao@iti.gov.br.

**Art. 5º** As informações referentes ao PLAAO de AC deverão conter, para cada entidade vinculada, as seguintes informações:

I - nome da AC responsável pelo preenchimento das informações;

II - número do CNPJ da entidade vinculada à AC responsável pelo preenchimento;

III - nome da entidade vinculada à AC responsável pelo preenchimento;

IV - data prevista para o início da auditoria na respectiva instalação técnica;

V - data prevista para entrega do relatório de auditoria pela entidade responsável pela execução da auditoria;

VI - CNPJ da empresa que realizará a auditoria; e

VII - informações adicionais que a AC julgar conveniente apresentar.

**Parágrafo único.** O arquivo CSV deve ser identificado com nome "PLAAOANO\_nome da AC na ICP-Brasil.csv".

**Art. 6º** As informações referentes ao PLAAO de ACT, PSBio e PSC deverão conter, para cada entidade vinculada, as seguintes informações:

I - nome da ACT ou PSBio ou PSC responsável pelo preenchimento das informações;

II - data prevista para o início da auditoria nas respectivas entidades;

III - data prevista para entrega do relatório de auditoria pela entidade responsável pela execução da auditoria;

IV - CNPJ da empresa que realizará a auditoria; e

V - informações adicionais que a entidade julgar conveniente apresentar.

**Parágrafo único.** O arquivo CSV deve ser identificado com nome "PLAAO\_ANO\_nome da entidade na ICP-Brasil.csv".

**Art. 7º** As entidades de auditoria devem encaminhar ao ITI relatórios e informações de auditoria em até 15 dias após a data prevista no PLAAO para a entrega do relatório de auditoria, contendo, para cada entidade auditada, as seguintes informações:

I - para Relatório de AR:

a) CNPJ da entidade de auditoria responsável pelo preenchimento das informações;

b) nome na ICP-Brasil da entidade auditada, seguido de dois pontos ":" e número do CNPJ;

c) nome das ACs vinculada à AR auditada, separado por virgula, ex: AC xxxx rfb,AC XXXXX multipla;

d) ano da auditoria prevista no PLAAO;

e) data prevista para o início da auditoria na respectiva entidade;

f) data do relatório;

g) Conceito Geral atribuído à entidade auditada; e

h) relação das não conformidade identificadas.

II - para Relatório de AC e PSS:

a) CNPJ da entidade de auditoria responsável pelo preenchimento das informações;

b) nome na ICP-Brasil da entidade auditada, seguido de dois pontos ":" e número OID da DPC da AC auditada preenchido sem ponto, exemplo: AC TESTE:21676110;

c) nome da entidade superior vinculada à AC auditada, ex: AC RAIZ ou AC RFB;

d) ano da auditoria prevista no PLAAO;

e) data prevista para o início da auditoria na respectiva entidade;

f) data do relatório;

g) Conceito Geral atribuído à entidade auditada; e

h) relação das não conformidade identificadas.

III - para Relatório de ACT, PSC e PSBio:

a) CNPJ da entidade de auditoria responsável pelo preenchimento das informações, preenchido sem ponto ou barra ou hífen (ex: 99999999999999);

b) nome na ICP-Brasil da entidade auditada, seguido de dois pontos ":" e número do preenchido sem ponto ou barra ou hífen (ex: 99999999999999);

c) tipo de entidade auditada, ACT ou PSBio ou PSC;

d) ano da auditoria prevista no PLAAO;

e) data prevista para o início da auditoria na respectiva entidade;

f) data do relatório;

g) Conceito Geral atribuído a entidade auditada; e

h) relação das não conformidade identificadas.

**§ 1º** Os relatórios de auditoria devem ser no formato PDF, assinados digitalmente com certificado ICP-Brasil pelo responsável técnico da entidade de auditoria.

**§ 2º** As informações sobre o relatório de auditoria devem ser encaminhadas ao ITI em arquivo no formato CSV identificado com o nome "rel\_ano do relatório\_nome da entidade auditada.csv".

**§ 3º** O relatório (PDF) e as informações (CSV) devem ser incluídos em um único arquivo compactado (.zip) e encaminhados para o e-mail relatorio.auditoria@iti.gov.br.

**Art. 8º** Os arquivos CSV mencionados neste ato deverão seguir as "Definições do formato dos arquivos CSV" do ADE-ICP-05.C.

**Art. 9º** As Autoridades Certificadoras credenciadas que emitem certificados para usuário final terão os seguintes prazos para adequação:

I - até 30 (trinta) dias, contados da data de publicação deste regulamento, para implementação da regra de periodicidade de envio dos arquivos, conforme estabelecido no caput do art. 2º; e

II - até 90 (noventa) dias, contados da data de publicação deste regulamento, para adequação às regras previstas no art. 3º, relativas à inserção de novos campos no arquivo CSV que contém informações sobre emissões de certificados digitais.

**Art. 10.** Fica revogada a Instrução Normativa ITI nº 20, de 23 de novembro de 2021.

**Art. 11.** Esta Instrução Normativa entra em vigor na data de sua publicação.

ENYLSON FLÁVIO MARTINEZ CAMOLESI
