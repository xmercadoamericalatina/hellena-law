---
titulo: "INSTRUÇÃO NORMATIVA BCB Nº 456, DE 29 DE FEVEREIRO DE 2024"
orgao: "Banco Central do Brasil/Àrea de Regulação/Departamento de Regulação do Sistema Financeiro"
tipo: "Instrução Normativa"
numero: "456"
data: 2024-02-29
revogada: null
versao_texto: "publicação original"
publicacao: "DOU de 01/03/2024, seção 1, p. 104"
data_publicacao: 2024-03-01
edicao: "42"
fonte: "https://www.in.gov.br/web/dou/-/instrucao-normativa-bcb-n-456-de-29-de-fevereiro-de-2024-546042588"
sha256_html_fonte: 4cd60e8fdbd23d58017e4d1745525055561af49080950fed26d6e36e1652f515
baixado_em: 2026-10-16
---
# INSTRUÇÃO NORMATIVA BCB Nº 456, DE 29 DE FEVEREIRO DE 2024

INSTRUÇÃO NORMATIVA BCB Nº 456, DE 29 DE FEVEREIRO DE 2024

Divulga a versão 5.0 do Manual de APIs do Open Finance.

Os Chefes do Departamento de Regulação do Sistema Financeiro (Denor) e do Departamento de Tecnologia da Informação (Deinf), no uso das atribuições que lhes conferem o art. 23, inciso I, alínea "a", do Regimento Interno do Banco Central do Brasil, anexo à Resolução BCB nº 340, de 21 de setembro de 2023, com base no art. 3º, inciso II, da Resolução BCB nº 32, de 29 de outubro de 2020, resolvem:

**Art. 1º** Esta Instrução Normativa divulga a versão 5.0 do Manual de APIs do Open Finance, de observância obrigatória por parte das instituições participantes, conforme Anexo.

**Parágrafo único.** O manual de que trata o caput, em sua versão mais recente, estará acessível na página do Open Finance no sítio eletrônico do Banco Central do Brasil na internet e no Portal do Open Finance no Brasil, mantido pela Estrutura Responsável pela Governança do Open Finance de que trata o art. 44, § 1º, da Resolução Conjunta nº 1, de 4 de maio de 2020.

**Art. 2º** Fica revogada a Instrução Normativa nº 306, de 19 de setembro de 2022.

**Art. 3º** Esta Instrução Normativa entra em vigor em 1º de março de 2024.

RENATO KIYOTAKA UEMA

Chefe do Departamento de Regulação do Sistema Financeiro

HAROLDO JAYME MARTINS FROES CRUZ

Chefe do Departamento de Tecnologia da Informação

## ANEXO

Manual de APIs do Open Finance Versão 5.0

Histórico de revisão

<table>    <tbody>     <tr></tr>     <tr>      <td rowspan="1" colspan="1"><p>Data</p></td>      <td rowspan="1" colspan="1"><p>Versão</p></td>      <td rowspan="1" colspan="1"><p>Descrição das alterações</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>29/2/2024</p></td>      <td rowspan="1" colspan="1"><p>5.0</p></td>      <td rowspan="1" colspan="1"><p>Simplificação da seção 2 "APIs do Open Finance".</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p>Atualização da seção 5 "Requisitos não funcionais", incluindo mais uma faixa de frequência a ser considerada, e detalhamento dos indicadores de desempenho e de disponibilidade das APIs.</p></td>     </tr>    </tbody>   </table>

Termos de Uso

Este manual detalha os requisitos técnicos para a implementação dos elementos necessários à operacionalização do Open Finance, complementando a regulamentação vigente sobre o tema.

O manual será revisto e atualizado periodicamente a fim de preservar a compatibilidade com a regulamentação, bem como para incorporar os aprimoramentos decorrentes da evolução do Open Finance e da tecnologia.

Informações mais detalhadas e exemplos da aplicação deste manual poderão ser encontrados nos guias e tutoriais disponíveis no Portal do Open Finance no Brasil, na Área do Desenvolvedor.

Sugestões, críticas ou pedidos de esclarecimento de dúvidas relativas ao conteúdo deste documento podem ser enviados ao Banco Central do Brasil por meio dos canais institucionais dessa autarquia.

Referências

As especificações baseiam-se, referenciam e complementam, quando aplicável, os seguintes documentos:

<table>    <tbody>     <tr></tr>     <tr>      <td rowspan="1" colspan="1"><p>Referência</p></td>      <td rowspan="1" colspan="1"><p>Origem</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>Resolução Conjunta nº 1, de 2020</p></td>      <td rowspan="1" colspan="1"><p>https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20Conjunta&amp;numero=1</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>Resolução BCB nº 32, de 2020</p></td>      <td rowspan="1" colspan="1"><p>https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20BC B&amp;numero=32</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>Hypertext Transfer Protocol - HTTP/1.1</p></td>      <td rowspan="1" colspan="1"><p>https://tools.ietf.org/html/rfc2616</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>ISO 20022</p></td>      <td rowspan="1" colspan="1"><p>https://www.iso20022.org/</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>OpenAPI Specification</p></td>      <td rowspan="1" colspan="1"><p>https://github.com/OAI/OpenAPI-Specification/blob/3.0.0/versions/3.0.0.md</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>Representational State Transfer</p></td>      <td rowspan="1" colspan="1"><p>https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm</p></td>     </tr>    </tbody>   </table>

1\. Introdução

O Open Finance está intrinsecamente ligado às APIs, interfaces por meio das quais será possível interligar os diferentes sistemas das instituições. Ao serem disponibilizadas pelos participantes, as APIs devem satisfazer condições tais como padronização, robustez e segurança, a fim de que o objetivo de compartilhamento de dados e serviços seja atendido a contento.

Nesse sentido, este manual visa a definir os principais aspectos relativos às especificações e implementações das APIs que integram o Open Finance no País, observando as disposições da Resolução Conjunta nº 1, de 4 de maio de 2020, e da Resolução BCB nº 32, de 29 de outubro de 2020.

São tratados neste manual aspectos como: formato para a troca de dados, desenho da interface, protocolo para transmissão de dados, versionamento, modelo de APIs e endpoints. Desse modo, o manual estabelece as diretrizes gerais sem esgotar todos os aspectos necessários à implementação das APIs para o Open Finance. As demais definições a cargo das instituições participantes, por meio da Estrutura Responsável pela Governança do Open Finance, nos termos da Circular nº 4.032, de 23 de junho de 2020, estarão disponíveis no Portal do Open Finance no Brasil, no qual poderão ser encontrados guias, tutoriais e outras informações operacionais sobre as APIs.

Ao longo deste manual, será constante o uso de siglas e terminologia específica para designar algumas expressões cotidianas dos profissionais da área de tecnologia. Alguns exemplos das mais frequentemente utilizadas, com as correspondentes definições, são as seguintes:

I - API (Application Programming Interface): um conjunto de definições sobre como um sistema pode acessar dados ou funcionalidades providos por um outro sistema;

II - REST (Representational State Transfer): estilo arquitetural de software;

III - API RESTful: API que adere às restrições do estilo arquitetural REST;

IV - OpenAPI: linguagem de especificação de APIs RESTful;

V - endpoint: elemento de uma especificação OpenAPI sobre o qual podem ser executadas operações para acessar dados ou funcionalidades;

VI - HTTP (Hypertext Transfer Protocol): protocolo para sistemas hipermídia, distribuídos e colaborativos;

VII - operação: elemento de uma especificação OpenAPI que declara uma maneira válida de se acessar um endpoint, informando, por exemplo, qual método HTTP (GET, POST etc.) utilizar, nomes e tipos de parâmetros, etc;

VIII - provedor da API: instituição que disponibiliza uma API para ser consumida por outras instituições. Nas APIs de "Serviços de Iniciação de Pagamentos", é a instituição detentora de contas; no caso de APIs de "Dados Cadastrais e Transacionais", é a instituição transmissora de dados;

IX - consumidor da API: instituição que consome uma API provida por outras instituições. Nas APIs de "Serviços de Iniciação de Pagamentos", é a instituição iniciadora de pagamentos; no caso de APIs de "Dados Cadastrais e Transacionais", é a instituição receptora de dados; e

X - gateway de API: é um serviço, dispositivo ou proxy que atua como intermediário, aceitando, transformando, encaminhando e gerenciando o tráfego de APIs para serviços de back-end. Ele permite a comunicação e a transferência de dados entre endpoints e pode ser útil quando há várias plataformas que precisam interagir umas com as outras sem conceder acesso direto às APIs umas das outras. Além disso, um gateway de API pode lidar com tarefas como autenticação, limitação de taxas, armazenamento em cache e transformação de solicitação/resposta, reduzindo a carga sobre o aplicativo e melhorando a segurança geral e o desempenho do sistema.

2\. APIs do Open Finance

As APIs a serem providas pelas instituições no âmbito do Open Finance devem ser categorizadas em um dos seguintes tipos:

I - Dados Abertos;

II - Dados Cadastrais e Transacionais;

III - Serviços; e

IV - Relatórios e Métricas.

3\. Princípios

Os princípios abaixo norteiam as especificações e implementações das APIs do Open Finance.

3.1 Experiência do usuário

As especificações e implementações das APIs devem oferecer uma boa experiência para os usuários, sejam eles implementadores ou consumidores das APIs.

3.2 Independência de tecnologia

As especificações das APIs devem ser independentes de tecnologia, podendo ser implementadas e consumidas em diferentes linguagens, tais como Java, JavaScript e Python; ou plataformas, tais como Windows, Linux, Android e iOS.

3.3 Segurança

Procedimentos e controles (assinaturas digitais, criptografia, protocolos de autenticação e autorização, entre outros) devem ser adotados de forma a proteger os participantes do Open Finance, seus clientes, os consumidores das APIs e demais participantes do ecossistema, observada a compatibilidade com a política de segurança cibernética da instituição.

3.4 Extensibilidade

No futuro, as APIs poderão ser evoluídas para atender a novos casos de uso e, portanto, devem ser especificadas e implementadas de forma a permitir e facilitar extensões como, por exemplo, novos endpoints, operações, parâmetros e propriedades.

3.5 Padrões abertos

Padrões abertos devem ser adotados sempre que possível.

3.6 APIs RESTful

As especificações das APIs devem atender às restrições do estilo arquitetural REST sempre que possível.

3.7 ISO 20022

As respostas das APIs devem ter como base os elementos e componentes de mensagem ISO 20022 (https://www.iso20022.org/). Os casos particulares em que a adoção do padrão ISO não seja possível ou recomendada poderão sofrer adequações, desde que especificamente apontados para avaliação pelo Banco Central do Brasil.

3.8 Declaração de obrigatoriedade

Todos os elementos que compõem as especificações das APIs (endpoints, operações, parâmetros, propriedades de respostas etc.) devem ser explicitamente declarados como "Obrigatório", "Opcional" ou "Condicional", caso sejam obrigatórios apenas em certas condições.

Funcionalidades que sejam de implementação opcional pelo transmissor devem ficar explícitas na sua documentação, tanto para informar adequadamente ao público transmissor, que poderá ou não implementar a funcionalidade, quanto ao público consumidor, que pode não encontrar a funcionalidade disponível em alguns transmissores.

4\. Definições e recomendações

As definições e recomendações abaixo devem ser observadas pelas especificações e implementações das APIs do Open Finance.

4.1 Especificações

As APIs devem ser especificadas com a versão 3.0.0 ou superior da linguagem OpenAPI (https://github.com/OAI/OpenAPI-Specification/blob/3.0.0/versions/3.0.0.md).

As especificações das APIs devem ser analisadas com a versão 5.9.0 ou superior do software livre e de código aberto Spectral (https://github.com/stoplightio/spectral/tree/v5.9.0). A análise deve ser feita com o conjunto de regras (ruleset) padrão desta versão do Spectral. O resultado da análise não deve conter erros ou alertas.

É recomendado que a versão 3.0.25 ou superior do software livre e de código aberto Swagger Codegen (https://github.com/swagger-api/swagger-codegen/tree/v3.0.25) seja utilizada para gerar o código de clientes e também o código inicial de implementações das APIs a partir de suas especificações. Recomenda-se que o código gerado seja analisado com o intuito de identificar possíveis recursos da linguagem OpenAPI que foram utilizados nas especificações, mas que não são adequadamente suportados pelo Swagger Codegen e, possivelmente, por outros softwares que trabalham com especificações OpenAPI. Caso isso ocorra, deve-se avaliar se não é possível alterar as especificações para não mais fazer uso desses recursos.

Devem ser disponibilizadas implementações de exemplo das APIs. Os dados retornados por elas não precisam ser dados reais e nem volumosos, pois o objetivo da disponibilização é dar ao Banco Central do Brasil, aos implementadores e aos consumidores das APIs mais um recurso para dirimir eventuais dúvidas acerca de suas especificações e implementações. É recomendado que o código inicial de implementações das APIs mencionado anteriormente seja complementado de forma a constituir-se nas implementações de exemplo.

As informações disponibilizadas nos dicionários de dados devem ser consistentes com as especificações OpenAPI associadas.

Todos os endpoints das APIs implementados devem ser previamente registrados no diretório de participantes.

Todos os endpoints registrados que retornem listas, caso os parâmetros sejam válidos, devem retornar a lista associada, mesmo que seja lista vazia. Não é considerado um retorno válido o erro 404, neste cenário, quando não houver a informação associada.

4.2 Versionamento

As versões das especificações das APIs serão tipificadas como "major", "minor", "patch" e "release candidate" de acordo com os critérios a seguir:

I - major: inclui novas características da implementação, mudanças, correções a serem incorporadas e que podem ser incompatíveis com versões anteriores, por exemplo, v1.0.0 e v2.0.0;

II - minor: pequenas mudanças nos elementos já existentes, com manutenção da compatibilidade com as versões até a major imediatamente anterior, por exemplo, v1.1.0 e v1.2.0;

III - patch: esclarecimentos às especificações minor, não incluem alterações funcionais, por exemplo, v1.1.1, v1.1.2; e

IV - release candidate: versões de pré-lançamento de qualquer versão futura do tipo patch, minor ou major, por exemplo, v1.0.0-rc e v1.0.0-rc2.

A Estrutura Responsável pela Governança do Open Finance, de que trata o art. 44, § 1º, da Resolução Conjunta nº 1, de 2020, pode lançar novas versões das APIs.

O Banco Central do Brasil pode definir:

I - o cronograma de implantação das novas versões das especificações das APIs e de certificação das instituições participantes; e

II - a tipificação de determinadas alterações como "minor" ou "patch" independentemente dos critérios definidos nos incisos de I a IV desta subseção.

Alterações feitas na especificação de uma API devem sempre ser documentadas com um novo versionamento desta especificação.

Por fim, credenciais de acesso associadas às APIs devem ser agnósticas às suas versões.

4.3 Portal do Open Finance no Brasil

O sítio eletrônico de que trata o art. 15 da Resolução BCB nº 32, de 2020, deverá conter definições e recomendações acessórias não presentes neste manual, bem como outros artefatos necessários à especificação, implementação e consumo das APIs do Open Finance. Todas as definições e recomendações acessórias e artefatos publicados no portal deverão estar em concordância com este e com os demais manuais do Open Finance.

4.4 Cronograma

O Portal do Open Finance deverá listar as APIs em produção, suas versões atuais, datas em que entraram em produção, link para suas especificações e lista de mudanças desde a última publicação. Também deverá apresentar o cronograma de homologação das APIs, indicando versão, data de divulgação, data prevista de entrada em produção e outras informações relevantes.

4.5 Logs de mudanças

Todas as versões já publicadas das APIs devem ser listadas no Portal do Open Finance, juntamente com os respectivos logs de mudanças e períodos em que estiveram em produção.

4.6 Definições acessórias

A Estrutura Responsável pela Governança do Open Finance deverá estabelecer e publicar no Portal do Open Finance um guia de estilo de especificações de APIs contendo definições e recomendações para os seguintes elementos:

I - estrutura de URIs (Uniform Resource Identifiers);

II - cabeçalhos HTTP;

III - códigos de status HTTP;

IV - convenções de corpo de requisições e respostas;

V - convenções de nomenclatura;

VI - tipos de dados comuns;

VII - paginação; e

VIII - estabilidade de identificadores.

4.7 Processo de gerência de mudanças

A Estrutura Responsável pela Governança do Open Finance deve estabelecer e publicar no Portal do Open Finance o processo que ela adotará para gerenciar mudanças nas especificações das APIs.

4.8 Tutoriais

Todas as informações necessárias para o desenvolvimento, testes e entrada em produção de aplicações ou APIs no Open Finance devem estar disponíveis em tutoriais publicados na Área do Desenvolvedor no Portal do Open Finance. Cada tutorial deve conter todos os passos necessários para o completo desenvolvimento da atividade em questão, como desenvolvimento e uso de aplicações e APIs, autenticação e autorização, uso da Sandbox, aplicação de testes de conformidade e cadastramento no diretório. Quando pertinente, devem ser fornecidos exemplos de código fonte ou de capturas de telas, tornando o processo o mais claro possível para todos os participantes e interessados.

4.9 Extensibilidade

As especificações das APIs do Open Finance podem não dar acesso a todos os dados e funcionalidades que um ou mais participantes desejam expor para os consumidores das APIs. Isso pode ser necessário para melhor suportar casos de uso ou possibilitar inovações em produtos e serviços financeiros. Para atender estas e outras necessidades, é facultado aos participantes implementarem versões estendidas das APIs inteiramente compatíveis com as especificações padrões das APIs que são:

I - novos endpoints;

II - novas operações em endpoints pré-existentes;

III - novos parâmetros em operações pré-existentes, desde que opcionais; e

IV - novas propriedades em respostas pré-existentes.

A Estrutura Responsável pela Governança do Open Finance deverá publicar no Portal do Open Finance as definições e recomendações acessórias relacionadas às extensões das APIs.

Todas as extensões implementadas pelos participantes deverão estar listadas, com sua documentação referenciada, em seção específica no Portal do Open Finance e disponíveis para consumo, observadas as regras de ressarcimento de despesas previstas na regulamentação vigente.

5\. Requisitos não funcionais

Esta seção apresenta os requisitos não funcionais que as instituições participantes devem observar na implementação das APIs do Open Finance.

Para auxiliar na definição de alguns requisitos não funcionais, é necessário que cada endpoint seja classificado no Portal do Open Finance de acordo com a sua frequência de atualização dos dados, conforme as opções abaixo:

I - alta frequência;

II - média-alta frequência;

III - média frequência; e

IV - baixa frequência

Os Limites de tráfego por origem, limites operacionais e tempo de resposta (desempenho) serão definidos baseados nessa classificação.

Os endpoints das APIs do tipo "Serviços", das APIs de "Segurança" (Token - consumo OAuth 2.0 (FAPI), Token - DCR/DCM) e das APIs de "Recursos" e de "Consentimento" devem ser considerados como de alta frequência.

5.1 Limites de tráfego

5.1.1 Limites por origem

Cada endpoint implementado no Open Finance pode ter uma restrição quanto ao tráfego a partir de determinada origem. Em APIs do tipo "Dados Abertos" a origem é o IP de onde partiu a requisição, em APIs autenticadas é a organizationId da instituição que fez a requisição.

No caso de uma instituição implementar limites, eles devem respeitar os valores mínimos de Transações por Minuto (TPM). conforme definido abaixo:

I - 2.000 TPM, por endpoint e por origem, em endpoints classificados como de alta frequência;

II - 1.500 TPM, por endpoint e por origem, em endpoints classificados como de média-alta frequência;

III - 1.000 TPM, por endpoint e por origem, em endpoints classificados como de média frequência; e

IV - 500 TPM, por endpoint e por origem, em endpoints classificados como de baixa frequência.

Aplicabilidade: Alguns endpoints não podem ter limites de tráfego definidos por origem, como nas APIs do tipo "Serviços", nas APIs de "Segurança", e de "Recursos" e de "Consentimento". A informação se o limite por origem é "aplicável" ou "não aplicável" deve estar explícito por endpoint no Portal do Open Finance.

As requisições que excederem os limites implementados deverão ser respondidas com o código de status HTTP 429 (Too Many Requests).

Por fim, as requisições que ultrapassarem os limites deverão ser desprezadas no cálculo do tempo de resposta das implementações das APIs.

5.1.2 Limites globais

A infraestrutura das instituições provendo APIs no Open Finance deve ter a capacidade de, no mínimo, atender a 300 requisições simultâneas por segundo (TPS).

Caso uma instituição atinja o limite de 300 TPS, no contexto do Open Finance, a mesma deve ampliar sua capacidade de infraestrutura para possibilitar um acréscimo de 150 TPS ao limite anterior. Tal aumento deve ocorrer novamente a cada vez que o limite vigente naquela instituição for atingido. Cada instituição deve criar monitoramento preventivo, de acordo com critérios definidos; as evidências devem estar à disposição do Banco Central do Brasil por um período de doze meses.

As requisições que excederem os limites de TPS deverão ser respondidas com o código de status HTTP 529 (Site is overloaded).

O Portal do Open Finance deverá conter uma especificação detalhada de como TPS e gatilhos para aumento ou diminuição da capacidade serão calculados.

Endpoints criados dentro do conceito de extensibilidade, sejam dentro de novas APIs ou em APIs existentes, não podem ser considerados para controle do limite global de transações simultâneas.

5.2 Limites operacionais

É facultado às instituições participantes que implementem um limite de acesso mensal por endpoint e por cliente.

Em endpoints que acessem recursos ou produtos, os limites serão também considerados por recurso ou produto.

A contabilização dos acessos deve ser feita por:

I - mês;

II - endpoint;

III - objeto mais granular referenciado na chamada (consentimento/recurso/produto);

IV - cliente (CPF ou CNPJ); e

V - instituição consumidora da informação.

Por exemplo: uma instituição receptora "A" pode acessar um endpoint "B", acessando o recurso "C", de um cliente "D" da instituição transmissora "E", no mínimo "N" vezes (ou chamadas) com sucesso por mês.

Aplicabilidade dos limites operacionais: todos os endpoints das APIs do tipo Dados Cadastrais e Transacionais (conforme classificação por tipo), excetuando-se os endpoints das APIs de Consentimento (Consents) e Recursos (Resources). As APIs dos tipos Dados Abertos, de Serviços (como de Iniciação de Pagamento) e de Segurança não podem ter restrições de limites operacionais.

A implementação dos limites operacionais é opcional pelas instituições transmissoras, mas, uma vez que sejam implementados, devem garantir o consumo mínimo estabelecido no Portal do Open Finance. É facultada à instituição a possibilidade de ampliar estes limites, mas vedada a implementação de limites inferiores aos estabelecidos.

O Portal do Open Finance deve listar os valores mínimos de limites operacionais a serem considerados, por endpoint, que devem ser iguais ou maiores que os abaixo, de acordo com a classificação de frequência de utilização:

I - 4 chamadas ao mês, para endpoint classificado como de baixa frequência;

II - 30 chamadas ao mês, para endpoint classificados como de média frequência;

III - 120 chamadas ao mês, para endpoint classificados como de média-alta frequência;

IV - 240 chamadas ao mês, para endpoint classificado como de alta frequência; e

V - 420 chamadas ao mês, para os seguintes endpoints da API de Contas: "Saldos da conta" e "Limites da conta".

Só deverão ser contabilizadas nos limites operacionais as requisições respondidas com código de status HTTP 2XX (com sucesso), sendo que as requisições adicionais a um endpoint para fins de paginação não devem ser contabilizadas.

As requisições que excederem os limites operacionais deverão ser respondidas com o código de status HTTP 423.

Todas as requisições autenticadas em endpoints sujeitos ao limite operacional devem possuir o atributo x-fapi-interaction-id preenchido no seu header pela instituição receptora de dados, que deve ser copiado pela instituição transmissora de dados nos headers da resposta. Essa definição objetiva permitir um adequado rastreamento de divergências que podem ocorrer entre instituições transmissoras e receptoras de dados associadas ao limite operacional.

5.3 Desempenho

Deverá ser medido o tempo de resposta de cada requisição, ou seja, o tempo transcorrido entre o recebimento de uma requisição que não ultrapassa os limites de tráfego e o momento em que a requisição é completamente respondida. Adicionalmente, esta medição deverá ser feita de maneira que os tempos medidos sejam os mais próximos possíveis dos tempos de resposta experimentados por quem fez a requisição. A medição na instituição provedora da API deve iniciar quando a requisição é recebida pelo gateway e deve terminar após o último byte da resposta desta requisição ser enviado.

5.3.1 Cálculo do desempenho

Para fins do cálculo do desempenho, deve-se considerar o valor do percentil 95 e as requisições para medir o desempenho, que pretende minimizar impacto do aparecimento de valores extremos (outliers). O valor do percentil 95 pode ser obtido da seguinte maneira:

I - coleta dos dados: Seja R o conjunto de todos os tempos de resposta de um dia, onde r i é o tempo de resposta da i-ésima requisição. Ou seja, R={r 1 , r 2 , ..., r n };

II - cálculo do índice do percentil 95: o índice para o percentil 95, denotado por i 95 , é calculado pela fórmula i 95 = 0.95 \* n, arredondado para o número inteiro mais próximo, e onde n representa número de requisições;

III - ordenação dos dados: Ordene o conjunto R em ordem crescente para obter o conjunto ordenado R ord ={r(1), r(2), ..., r(n)}, onde r(1) é o menor tempo de resposta e r(n) é o maior; e

IV - obtenção do valor do percentil 95: o valor do percentil 95, denotado por P 95 , é o valor no índice i 95 no conjunto ordenado R ord . Ou seja, P 95 = r (i95) .

Considerando um exemplo em que um endpoint recebe 10.555 requisições em um dia (ou seja, n = 10.555). Nesse caso, o índice para o percentil 95 será 10.027 (i 95 = [0.95 \* n] = [10.027,25] = 10.027). Após ordenarmos as medições do tempo de resposta em ordem crescente (formando o conjunto R ord ), o valor do percentil 95 (P 95 ) para esse dia será igual ao tempo de resposta na posição 10.027 no conjunto ordenado R ord .

5.3.2 Service Level Agreement (SLA) do desempenho

Neste contexto, os endpoints das APIs deverão manter, diariamente, o percentil 95 do tempo de resposta em no máximo:

I - 1.500ms, em endpoints classificados como de alta e média-alta frequências;

II - 2.000ms, em endpoints classificados como de média frequência; e

III - 4.000ms, em endpoints classificados como de baixa frequência.

Por exemplo, em um dia que um endpoint de alta frequência receba 10.000 requisições, o tempo de resposta de pelo menos 9.500 requisições deve ser inferior a 1.500ms.

Informações adicionais:

I - as medições de tempo de resposta devem ser realizadas de maneira independente para cada versão major dos endpoints em produção;

II - devem ser consideradas as requisições com todos os códigos de retorno possíveis, com exceção dos associados a limites de tráfego e limites operacionais;

III - esta subseção não se aplica às APIs de "Webhook";

IV - as instituições provedoras devem gerar e acompanhar seus indicadores de desempenho, de maneira independente da Plataforma de Coleta de Métricas (PCM) provida pela Estrutura Responsável pela Governança do Open Finance;

V - as instituições consumidoras das APIs devem registrar os tempos de resposta das APIs que consomem para envio à PCM. Nelas a medição do tempo de resposta de cada requisição deve iniciar no momento antes da requisição ser feita e deve terminar após o último byte ser recebido, antes de qualquer processamento;

VI - o valor do tempo de resposta a ser considerado para uma requisição é o valor reportado pelo consumidor da API;

VII - na falta de informações dos consumidores, serão utilizadas as informações dos provedores para o cálculo do SLA de desempenho; e

VIII - a Estrutura Responsável pela Governança do Open Finance deverá disponibilizar indicadores adicionais para monitoramento e aprimoramento do ecossistema, que não terão, nesse momento, um SLA mínimo, tais como:

a) percentil 95 do tempo de resposta somente de requisições com status code 2XX;

b) percentil 95 do tempo de resposta - provedor - deve considerar todas as requisições fornecidas pelo provedor das APIs, mesmo quando houver diferença entre as informações entre provedor e consumidor;

c) percentil 95 do tempo de resposta - consumidor - deve considerar todas as requisições fornecidas pelos consumidores das APIs, mesmo quando houver diferença entre as informações entre provedor e consumidor;

d) índice de paridade - percentual do número de requisições no status "PAIRED" em relação ao total; e

e) média do tempo de resposta até P 95 - média do tempo de resposta de todas as requisições com tempo de resposta menores que o valor do P 95 .

5.3.3 Aferição do desempenho para fins do processo de monitoramento

Considerando que o Manual de Monitoramento do Open Finance estabelece que o período de apuração do desempenho é mensal, assim que o mês de referência se encerrar, a Estrutura Responsável pela Governança do Open Finance deve verificar se os endpoints das APIs das instituições participantes atenderam aos SLAs do desempenho definidos na seção anterior deste manual.

Para fins do processo de monitoramento, considera-se que um endpoint está em conformidade caso tenha respeitado o SLA do desempenho em pelo menos 90% dos dias do mês de referência, arredondando-se para o número inteiro mais próximo, desde que o valor do P 95 dos demais dias não tenha sido superior ao SLA do desempenho aumentado em 20%.

Por exemplo:

I - em um mês de 30 dias, em que um endpoint de alta frequência tenha apresentado valor de P 95 inferior a 1.500ms em 27 dias e, nos demais dias, tenha apresentado valor de P 95 entre 1.500ms e 1.800ms (1.500ms \* 1,2 = 1.800ms), o endpoint está em conformidade para fins do processo de monitoramento naquele mês; e

II - em um mês de 31 dias, em que um endpoint de alta frequência tenha apresentado valor de P 95 inferior a 1.500ms em 28 dias e, nos demais dias, tenha apresentado, em pelo menos um dos dias, valor de P 95 superior a 1.800ms (1.500ms \* 1,2 = 1.800ms), o endpoint não está em conformidade para fins do processo de monitoramento naquele mês.

5.4 Disponibilidade

5.4.1 Cálculo da disponibilidade

A disponibilidade dos endpoints das APIs do Open Finance será calculada empiricamente, baseada na monitoração de requisições válidas. Serão consideradas "requisições válidas" as requisições que retornam status code da faixa 2XX, 5XX, igual a 408 ou igual a 422. As requisições válidas podem ser divididas em "requisições válidas com sucesso" - com status code na faixa 2XX ou igual a 422 - e "requisições válidas com erro" - com status code na faixa 5XX ou igual a 408.

A disponibilidade pontual (t) será calculada como a fração do total de requisições válidas que cada endpoint recebe e as que ele processa com sucesso a cada intervalo de 1 minuto. Os intervalos de minuto deverão ser calculados do segundo zero (0s:000ms) até o segundo 59 (59s:999ms):

Disponibilidade pontual (t) = (Total de requisições válidas com sucesso)/(Total de requisições válidas com sucesso + Total de requisições válidas com erro).

Por exemplo, a disponibilidade pontual de um endpoint referente ao minuto 11:34, de um determinado dia, no qual houve um total de requisições válidas com sucesso de 255 e um total de requisições válidas com erro de 4, é calculada da seguinte forma:

Disponibilidade pontual (t = 11:34:00 - 11:34:59) = 255/(255 + 4) = 98,45%.

Dessa forma, obtém-se o indicador percentual para cada janela de tempo de 1 minuto. Cada período de 1 minuto será classificado como "disponível" ou "indisponível". Se a "disponibilidade pontual" da janela de tempo ficar abaixo de 95% isso indicará que ela será considerada como "indisponível", caso contrário será "disponível".

Períodos que não tenham requisições válidas são considerados "indefinidos" e são desconsiderados para cálculo da disponibilidade. Assim, considera-se, em relação à disponibilidade, que:

I - disponível, se disponibilidade pontual (t) ³ 95%;

II - indisponível, se disponibilidade pontual (t) &lt; 95%

III - indefinido, se disponibilidade pontual (t) = div/0.

A disponibilidade diária será calculada baseada nas informações das disponibilidades pontuais:

Disponibilidade diária = (Número de períodos disponíveis)/(Número de períodos disponíveis + Número de períodos indisponíveis).

Por exemplo, considerando um dia em que houve requisições válidas em 1.390 das 1.440 faixas de 1 minuto possíveis (1 dia = 24h \* 60min= 1.440 faixas de horário) para um endpoint específico "x" de versão 1, e dos quais 30 períodos tiveram a disponibilidade menor que o limite de disponibilidade definido (95%), a Disponibilidade Diária de "x" v1 será igual a:

Disponibilidade diária (2023-10-16) = 1360 / (1360 + 30) = 97,84%.

A disponibilidade longa deverá ser calculada diariamente como média móvel das disponibilidades dos últimos noventa dias corridos, considerando somente os dias em que a disponibilidade diária pode ser calculada (teve pelo menos uma disponibilidade pontual diferente de "indefinido"). Ou seja, caso nos últimos noventa dias tenhamos dois dias calculados como indefinidos, a média deve ser calculada considerando somente as 88 disponibilidades válidas.

A aferição mensal deve considerar a disponibilidade longa do último dia do mês de referência.

5.4.2 SLA da disponibilidade

Cada um dos endpoints das APIs categorizadas como "Dados Abertos", "Dados Cadastrais e Transacionais", "Relatórios e Métricas", por versão, e os endpoints das APIs de "Segurança" "/register" e "/token", deverão satisfazer os requisitos mínimos de disponibilidade abaixo:

I - disponibilidade diária (calendário): 95%; e

II - disponibilidade longa (média móvel de 90 dias), medida diariamente: 99,5%.

As APIs classificadas como "Serviços de Iniciação de Pagamentos" seguem o definido na regulamentação do Pix.

Informações adicionais:

I - as medições devem ser feitas todos os dias, em todas as faixas de 1 minuto disponíveis, iniciando na primeira faixa (00:00:00-00:00:59) e terminando na última faixa (23:59:00-23:59:59), considerando o horário de Brasília;

II - as medições de disponibilidade devem ser feitas para cada versão major dos endpoints em produção. Por exemplo, em períodos de convivência o endpoint de v1/resources poderia estar disponível no mesmo período em que o endpoint de v2/resources estaria também disponível. É importante que suas disponibilidades sejam calculadas de maneira independente;

III - as instituições provedoras devem gerar e acompanhar seus indicadores de disponibilidade, de maneira independente da Plataforma de Coleta de Métricas (PCM) provida pela Estrutura Responsável pela Governança do Open Finance;

IV - o status code a ser considerado para uma requisição é o valor reportado pelo consumidor da API;

V - na falta de informações dos consumidores, serão utilizadas as informações dos provedores para o cálculo do SLA de disponibilidade;

VI - a indisponibilidade programada não exime o cálculo da disponibilidade no período apurado;

VII esta subseção não se aplica às APIs de "Webhook";

VIII - a disponibilidade de endpoints que não tenham requisições válidas no período apurado será considerada "indefinida", não estando sujeita a um SLA; e

IX - a Estrutura Responsável pela Governança do Open Finance deverá disponibilizar indicadores adicionais para monitoramento e aprimoramento do ecossistema que não terão, nesse momento, um SLA mínimo, tais como:

a) Disponibilidade calculada do ponto de vista do provedor da API - deve considerar as informações fornecidas pelo provedor das APIs; e

b) Disponibilidade calculada do ponto de vista do consumidor da API - deve considerar as informações fornecidas somente pelos consumidores das APIs, classificadas no PCM como "PAIRED" ou "SINGLE".

5.5 Timeout

Padronização do timeout de tempo de resposta do provedor e do tempo de resposta do consumidor em quinze segundos.

As requisições que excederem o limite de timeout do provedor deverão ser respondidas com o código de status HTTP 504 (Gateway Timeout).

Brasília, 29 de fevereiro de 2024.
