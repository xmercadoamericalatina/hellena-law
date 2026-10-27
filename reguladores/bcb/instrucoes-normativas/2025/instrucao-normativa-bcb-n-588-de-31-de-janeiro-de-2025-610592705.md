---
titulo: "INSTRUÇÃO NORMATIVA BCB Nº 588, DE 31 DE JANEIRO DE 2025"
orgao: "Banco Central do Brasil/Àrea de Regulação/Departamento de Regulação do Sistema Financeiro"
tipo: "Instrução Normativa"
numero: "588"
data: 2025-01-31
revogada: false
versao_texto: "publicação original"
publicacao: "DOU de 04/02/2025, seção 1, p. 80"
data_publicacao: 2025-02-04
edicao: "24"
fonte: "https://www.in.gov.br/web/dou/-/instrucao-normativa-bcb-n-588-de-31-de-janeiro-de-2025-610592705"
baixado_em: 2026-10-15
---
# INSTRUÇÃO NORMATIVA BCB Nº 588, DE 31 DE JANEIRO DE 2025

INSTRUÇÃO NORMATIVA BCB Nº 588, DE 31 DE JANEIRO DE 2025

Divulga a versão 4.0 do Manual de Serviços Prestados pela Estrutura de Governança do Open Finance.

Os Chefes do Departamento de Regulação do Sistema Financeiro (Denor), do Departamento de Supervisão de Cooperativas e de Instituições Não Bancárias (Desuc), do Departamento de Supervisão Bancária (Desup) e do Departamento de Tecnologia da Informação (Deinf), no uso da atribuição que lhes confere o art. 23, inciso I, alínea "a", do Regimento Interno do Banco Central do Brasil, anexo à Resolução BCB nº 340, de 21 de setembro de 2023, com base no art. 3º, inciso III, da Resolução BCB nº 32, de 29 de outubro de 2020, resolvem:

**Art. 1º** Esta Instrução Normativa divulga a versão 4.0 do Manual de Serviços Prestados pela Estrutura de Governança do Open Finance, de observância obrigatória por parte das instituições participantes, conforme Anexo.

**Parágrafo único.** O manual de que trata o caput, em sua versão mais recente, estará acessível na página do Open Finance no sítio eletrônico do Banco Central do Brasil na internet e no Portal do Open Finance no Brasil, mantido pela Estrutura de Governança do Open Finance de que trata o art. 44, § 1º, da Resolução Conjunta nº 1, de 4 de maio de 2020.

**Art. 2º** Fica revogada a Instrução Normativa BCB nº 359, de 3 de março de 2023, publicada no Diário Oficial da União de 7 de março de 2023.

**Art. 3º** Esta Instrução Normativa entra em vigor na data de sua publicação.

RENATO KIYOTAKA UEMA

Chefe do Departamento de Regulação do Sistema FinanceiroSubstituto

ADALBERTO FELINTO DA CRUZ JUNIOR

Chefe do Departamento de Supervisão de Cooperativas e de Instituições Não Bancárias

BELLINE SANTANA

Chefe do Departamento de Supervisão Bancária

CAIO MOREIRA FERNANDES

Chefe do Departamento de Tecnologia da Informação

## ANEXO

Manual de Serviços Prestados pela Estrutura de Governança do Open Finance Versão 4.0

Sumário das alterações

| Data | Versão | Descrição das alterações |
| --- | --- | --- |
| 31/1/2025 | 4.0 | Seção 2: atualização da subseção referente ao gerenciamento de identidades e acessos. |
|  |  | Seção 3: reorganização e maior detalhamento dado para a seção relativa ao*Service Desk*. |
|  |  | Seção 5: atualização das subseções referentes à área do desenvolvedor e à área do participante. |
|  |  | Seção 8: simplificação do texto, considerando a edição do Manual de Monitoramento do*Open Finance*. |

Termos de Uso

Este manual detalha os requisitos técnicos para a implementação dos elementos necessários à operacionalização do Open Finance, complementando a regulamentação vigente sobre o tema.

O manual será revisto e atualizado periodicamente a fim de preservar a compatibilidade com a regulamentação, bem como para incorporar os aprimoramentos decorrentes da evolução do Open Finance e da tecnologia.

Informações mais detalhadas e exemplos da aplicação deste manual poderão ser encontrados nos guias e tutoriais disponíveis no Portal do Open Finance no Brasil, na Área do Desenvolvedor.

Sugestões, críticas ou pedidos de esclarecimento de dúvidas relativas ao conteúdo deste documento podem ser enviados ao Banco Central do Brasil por meio dos canais institucionais dessa autarquia.

Referências

Estas especificações baseiam-se, referenciam e complementam, quando aplicável, os seguintes documentos:

| Referência | Origem |
| --- | --- |
| Resolução Conjunta nº 1, de 2020 | https://www.bcb.gov.br/estabilidadefinanceira/ exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20 Conjunta&numero=1 |
| Resolução BCB nº 32, de 2020 | https://www.bcb.gov.br/estabilidadefinanceira/ exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20 BCB&numero=32 |

1\. Introdução

O funcionamento do Open Finance pressupõe o provimento de alguns serviços fundamentais. No modelo adotado no País, definido pela Resolução Conjunta nº 1, de 4 de maio de 2020, do Conselho Monetário Nacional e do Banco Central do Brasil, e pela Resolução BCB nº 32, de 29 de outubro de 2020, essa incumbência ficou a cargo da Estrutura de Governança do Open Finance.

O Diretório de Participantes é o primeiro elemento essencial para a infraestrutura do Open Finance. Ele congrega uma série de funcionalidades críticas, como o gerenciamento de credenciais dos participantes.

A Estrutura de Governança deve acompanhar os níveis de serviço de tecnologia dos participantes e da infraestrutura compartilhada definidos em regulação.

Os canais de suporte aos serviços providos pela Estrutura de Governança do Open Finance e de encaminhamento de demandas às instituições participantes também são importantes para o atendimento das necessidades de apoio técnico na operacionalização do Open Finance. Eles constituem pontos focais para recepção e encaminhamento das demandas aos participantes, com o acompanhamento das demandas até a sua resolução.

Outro elemento importante para o funcionamento do Open Finance é a plataforma de resolução de disputas. Tal plataforma integra o mecanismo para resolução de disputas de que trata o art. 44, inciso IV, da Resolução Conjunta nº 1, de 2020. O acesso das instituições participantes aos recursos da referida plataforma deve observar a confidencialidade, a integridade, a disponibilidade dos dados e sistemas de informação utilizados, bem como a legislação e a regulamentação vigentes.

Com o propósito de promover a comunicação não somente entre os participantes do Open Finance, mas com o público em geral, a Estrutura de Governança do Open Finance deve disponibilizar o Portal do Open Finance no Brasil. Nesse portal, o cidadão poderá esclarecer suas dúvidas em relação aos serviços e à tecnologia; o desenvolvedor conseguirá informações de cunho técnico-operacional e as instituições participantes poderão obter informações sobre o ambiente.

A Estrutura de Governança do Open Finance deve, ainda, disponibilizar ambiente de teste (Sandbox) de application programming interfaces (APIs), com o objetivo de proporcionar estrutura de apoio ao desenvolvimento e testes por parte das instituições participantes, e um serviço de validação em produção com vistas a checar a conformidade e o registro de APIs das instituições participantes e garantir que os ambientes produtivos das instituições participantes estejam aderentes às suas respectivas certificações.

Convém ressaltar que diversos dos serviços supramencionados, tais como o Diretório de Participantes, ambientes de teste de APIs e de monitoramento de serviços de tecnologia, e ferramentas de validação em produção, constituem-se em elementos do papel de monitoramento dos participantes atribuído à Estrutura de Governança do Open Finance, conforme o art. 44, inciso VIII, da Resolução Conjunta nº 1, de 2020. Cumpre mencionar que, no entanto, tal papel não se limita aos serviços descritos neste manual.

Nesse sentido, esses são apenas alguns dos serviços prestados pela Estrutura de Governança do Open Finance com o objetivo de viabilizar o Open Finance no País. Naturalmente, haverá uma evolução das necessidades inerentes a essa iniciativa. Assim, a finalidade deste manual é estabelecer parte dos requisitos mínimos dos serviços essenciais sem a pretensão de ser exaustivo, deixando uma margem para decisão e atuação das instituições nos pontos não cobertos pelo documento, mas necessários para o sucesso da implementação do Open Finance.

2\. Diretório de Participantes

O Diretório de Participantes é o ambiente no qual uma instituição autorizada a funcionar pelo Banco Central do Brasil registra e formaliza sua participação no ambiente do Open Finance, realizando sua integração para dar início ao compartilhamento de dados ou serviços com as demais instituições participantes, por meio de APIs.

O Diretório de Participantes deve conter as seguintes funcionalidades:

I - gerenciamento de identidades e acessos: a emissão e o gerenciamento de registros de identidade para organizações e pessoas naturais que interagem com o Diretório;

II - gerenciamento de identidade e autorização de aplicações: identificação e autorização das aplicações das instituições participantes; e

III - gerenciamento de informações do Diretório: a capacidade de atualizar e encontrar as informações mantidas no Diretório, por meio de APIs, arquivos e/ou de uma interface de usuário web.

2.1 Gerenciamento de Identidades e Acessos

A funcionalidade "Gerenciamento de Identidades e Acessos" abrange todos os processos de negócio executados desde o primeiro contato do representante da instituição com a página inicial do Open Finance até o final de sua inscrição como participante do Diretório de Participantes.

O Diretório de Participantes deve coletar as informações necessárias para que as instituições sejam cadastradas como participantes no Open Finance e permitir que os representantes dessas instituições atualizem as informações necessárias à sua participação plena, de acordo com as respectivas modalidades de participação.

O Diretório de Participantes deve também dispor de funcionalidade para a revogação de certificado de participante, conforme a regulamentação vigente.

O processo de cadastramento deve estar detalhado no Portal do Open Finance no Brasil mantido pela Estrutura de Governança do Open Finance.

2.2 Gerenciamento de Identidade e Autorização de Aplicações

A funcionalidade "Gerenciamento de Identidade e Autorização de Aplicações" abrange os processos de negócio envolvidos com a identificação e autorização de participação de aplicações no Open Finance, permitindo um consumo seguro de informações.

Esse processo deve estar detalhado no Portal do Open Finance no Brasil mantido pela Estrutura de Governança do Open Finance.

2.3 Gerenciamento de Informações do Diretório

O Diretório de Participantes deve dispor de funcionalidades que possibilitem a listagem dos participantes, a consulta e alteração dos seus dados, de seus representantes e de seus contatos, bem como o histórico das modificações realizadas. Essas alterações devem ser passíveis de notificação aos participantes.

Em relação às APIs de dados acessíveis ao público relativos aos canais de atendimento e aos produtos e serviços disponíveis para contratação na instituição participante, ora definidos pelo Manual de Escopo de Dados, o Diretório de Participantes deve prover consultas, por meio de API ou arquivos, que permitam identificar os participantes que implementam uma determinada API ou endpoint, bem como listar as APIs e endpoints implementados por um participante. Em relação às demais APIs daquele manual, deve ser provida API que implemente consultas análogas, nesse caso restritas às instituições participantes do Open Finance.

Os processos envolvidos nessas funcionalidades devem estar detalhados no Portal do Open Finance no Brasil.

2.4 Testes de Conformidade e Registro de APIs

A Estrutura de Governança do Open Finance é responsável pelo processo de validação de conformidade de APIs dos participantes. O escopo mínimo dos testes deve abranger aspectos funcionais e não funcionais; os primeiros visam a avaliar se as implementações estão aderentes às especificações das APIs; os últimos objetivam avaliar se os requisitos não funcionais das APIs, em particular, segurança, estão sendo atendidos por suas implementações.

A execução dos testes de conformidade é realizada em ambiente disponibilizado pela Estrutura de Governança do Open Finance, que também se encarrega da certificação dos resultados.

Uma implementação de versão de API do Open Finance só poderá ser registrada no ambiente produtivo do Diretório de Participantes caso tenha sido certificada nos testes de conformidade.

A Estrutura de Governança do Open Finance deve estabelecer uma política de recertificações a ser seguida pelas instituições participantes.

Deverão ser disponibilizados em área pública do Portal do Open Finance no Brasil os resultados dos testes de conformidade de APIs já realizados.

2.5 Acordos de Nível de Serviço (SLAs) do Diretório de Participantes

O Diretório de Participantes deverá observar o seguinte nível mínimo de serviço:

Disponibilidade:

I - 24 horas por dia, 7 dias por semana;

II - 95% a cada 24 horas; e

III - 99,5% a cada 3 meses.

Desempenho das APIs:

Tempo de resposta de percentil 95 em, no máximo, 1.500ms.

3\. Service Desk

O Service Desk é o ambiente do Open Finance no qual são requisitados e mantidos, de forma centralizada, os tickets de suporte técnico relacionados ao Diretório de Participantes, às suas APIs e aos dados e serviços compartilhados entre os participantes.

Nesse ambiente, devem ser disponibilizadas quatro funcionalidades básicas:

I - solução de dúvidas gerais;

II - suporte na emissão de tickets;

III - suporte a notificações; e

IV - suporte aos serviços prestados pela Estrutura de Governança do Open Finance.

3.1 Solução de dúvidas gerais

Devem ser providas duas áreas para solução de dúvidas técnicas relacionadas ao Open Finance, a saber: perguntas frequentes sobre assuntos técnicos (FAQ) e um canal de atendimento, que poderá ser implementado com atendimento de forma automatizada, sem intervenção humana.

3.1.1 Perguntas frequentes

Nesta área, deverão ser encontradas as respostas para os questionamentos mais frequentes relacionados ao suporte técnico, ao Diretório de Participantes, às APIs, aos dados e serviços compartilhados entre as instituições participantes e aos processos deste compartilhamento, de modo que algumas dúvidas possam ser sanadas de maneira rápida e independente.

O conteúdo desta seção deverá ser reavaliado ao menos a cada lançamento de versão major das APIs, de forma a atender seu objetivo de esclarecer dúvidas frequentes do público.

3.1.2 Canal de atendimento

Deve ser disponibilizado canal de atendimento para suporte técnico, que pode ser implementado com atendimento de forma automatizada, sem intervenção humana. Nesse canal, poderão ser obtidas respostas para dúvidas de menor complexidade.

As respostas devem ser classificadas conforme o grau de sensibilidade, devendo ser fornecidas com observância do perfil do demandante.

Caso não seja possível atender às necessidades do demandante por meio do canal automatizado, deverá ser oferecida a possibilidade de abertura de ticket.

3.2 Suporte na abertura de tickets

3.2.1 Abertura de tickets

O Service Desk deve permitir, via canal de atendimento, a abertura de tickets:

I - pela Estrutura de Governança do Open Finance;

II - por instituições participantes;

III - por desenvolvedores; e

IV - por cidadãos.

Para o atendimento a dúvidas e a requisições de cidadãos, o Service Desk deve prover um ambiente com interface amigável e intuitiva e adaptado ao público em geral, de forma que as pessoas interessadas possam endereçar suas demandas à Estrutura de Governança do Open Finance sem a necessidade de conhecimento técnico específico.

No caso de recepção de demandas de cidadãos que envolvam reclamações contra instituições participantes, o demandante deve ser orientado a procurar primeiramente a instituição envolvida e, caso não consiga resolver o problema, registrar a reclamação no Banco Central do Brasil.

Adicionalmente, no caso de uma instituição participante, deve ser possível a abertura de tickets por meio de API específica.

Na abertura de um ticket, deve ser gerado um número de protocolo, que deve ser informado ao demandante. Nesse momento, começará a contar prazo para atendimento da demanda.

3.2.2 Tipos de tickets

O Service Desk deve suportar pelo menos três tipos de tickets:

I - requisição: solicitação de informações, solicitação de serviços ou sugestão de melhorias;

II - incidente: comunicação de falhas ou degradação de qualidade em serviços; e

III - monitoramento: notificação ou demanda de ajustes em decorrência do processo de monitoramento.

O canal de atendimento do Service Desk deve ser utilizado como forma de comunicação preferencial para os tickets de requisição e obrigatória para tickets de incidente e de monitoramento.

3.2.2.1 Requisição

3.2.2.1.1 Solicitação de informações ou de serviços

A Estrutura de Governança do Open Finance pode solicitar informações das instituições participantes, com vistas a subsidiar o cumprimento de suas atribuições no âmbito do Open Finance.

As instituições participantes, os desenvolvedores e os cidadãos podem solicitar informações à Estrutura de Governança do Open Finance.

As instituições participantes e os desenvolvedores podem solicitar a prestação de serviços pela Estrutura de Governança do Open Finance.

3.2.2.1.2 Sugestão de melhorias

As instituições participantes e os desenvolvedores podem sugerir melhorias à Estrutura de Governança do Open Finance.

3.2.2.2 Incidentes

As instituições participantes, a Estrutura de Governança do Open Finance e os desenvolvedores podem abrir tickets de incidentes.

Os tickets abertos por desenvolvedores se restringem às APIs de canais de atendimento e de produtos e serviços das instituições participantes.

No caso de tickets abertos pela Estrutura de Governança do Open Finance que estejam inseridos no processo de monitoramento, eles também devem seguir o disposto na subseção 3.2.2.3.

Após o encerramento do ticket, a instituição participante responsável pelo atendimento deve analisar a necessidade de ajustes adicionais em sua implementação, com vistas a corrigir a causa raiz do objeto do ticket, ou em seus controles internos para mitigar novas ocorrências análogas. Esse procedimento deve ser documentado em relatório, atualizado no momento de conclusão dos referidos ajustes, e mantido à disposição do Banco Central do Brasil.

3.2.2.2.1 Incidentes sem indisponibilidade

Com a exceção dos casos enquadrados na categoria "Degradação de qualidade de serviço", devem ser abertos tickets, inicialmente, na categoria "Erro de desconformidade".

Caso a instituição participante responsável pelo atendimento entenda que o caso específico esteja enquadrado em categoria distinta da que melhor define o caso concreto, é possível solicitar a reclassificação do ticket.

3.2.2.2.1.1 Degradação de qualidade de serviço

Esse incidente se caracteriza por uma diminuição do desempenho ou da capacidade de resposta dos recursos da instituição participante.

Esse tipo de ticket pode ser aberto pelas instituições participantes ou pela Estrutura de Governança do Open Finance contra instituições participantes ou contra a Estrutura de Governança do Open Finance. Quando o ticket for aberto por uma instituição participante, a degradação pode ser caracterizada considerando apenas as chamadas entre as duas instituições participantes envolvidas, não sendo necessário caracterizar uma degradação generalizada da instituição participante responsável pelo atendimento.

3.2.2.2.1.2 Erro de desconformidade

Esse incidente se caracteriza por erros na jornada do cliente ou em APIs e artefatos associados.

Esse tipo de ticket pode ser aberto pelas instituições participantes, desenvolvedores ou pela Estrutura de Governança do Open Finance contra instituições participantes ou contra a Estrutura de Governança do Open Finance.

3.2.2.2.1.3 Demais erros

Esse incidente se caracteriza por erros relacionados a eventuais ambiguidades ou casos não previstos nas especificações ou nas documentações técnicas.

Esse tipo de ticket se aplica apenas por reclassificação, sendo necessária adequada fundamentação.

3.2.2.2.2 Incidentes com indisponibilidade

Esses incidentes se referem a qualquer erro que cause indisponibilidade no ambiente de Open Finance, incluindo o ambiente das APIs e artefatos associados, das instituições participantes.

Esse tipo de ticket pode ser aberto pelas instituições participantes ou pela Estrutura de Governança do Open Finance contra instituições participantes ou contra a Estrutura de Governança do Open Finance.

3.2.2.3 Monitoramento

A Estrutura de Governança do Open Finance pode notificar as instituições participantes, demandar ajustes para regularizar situações de desconformidade e demandar ações relativas a diferentes aspectos do processo de monitoramento.

3.2.2.3.1 Indícios de desconformidade - notificação

A Estrutura de Governança do Open Finance pode abrir esse ticket para notificar uma instituição participante a respeito de indício de desconformidade em relação a um dos itens monitorados, conforme Manual de Monitoramento do Open Finance. Na abertura do ticket, devem ser apresentadas as evidências do indício de desconformidade ou o local em que tais evidências estão disponíveis para consulta.

A instituição participante deve avaliar a situação e, caso entenda não haver desconformidade, apresentar argumentação fundamentada à Estrutura de Governança do Open Finance.

3.2.2.3.2 Indícios de desconformidade - demanda de ação

A Estrutura de Governança do Open Finance pode abrir esse ticket para demandar que uma instituição participante realize ajustes para regularizar situações de desconformidade em relação a um dos itens monitorados, conforme Manual de Monitoramento do Open Finance.

A instituição participante deve avaliar a situação e, caso entenda não haver desconformidade, apresentar argumentação fundamentada à Estrutura de Governança do Open Finance.

Caso os ajustes sejam realizados dentro da meta de atendimento do ticket, esse indício de desconformidade não será considerado para fins de aplicação das medidas de que trata o Manual de Monitoramento do Open Finance, salvo em situações específicas estabelecidas em ato normativo.

3.2.2.3.3 Consolidação de desconformidades

A Estrutura de Governança do Open Finance pode abrir esse ticket para consolidar desconformidades ocorridas no mês de referência.

3.2.2.3.4 Apresentação de relatório de situações de desconformidade

De acordo com o Manual de Monitoramento do Open Finance, no âmbito do fluxo de aplicação de medidas, a Estrutura de Governança do Open Finance deve demandar uma instituição participante que apresentou desconformidades a entregar relatório de situações de desconformidade.

3.2.2.3.5 Apresentação de plano de adequação

De acordo com o Manual de Monitoramento do Open Finance, no âmbito do fluxo de aplicação de medidas, a Estrutura de Governança do Open Finance deve demandar uma instituição participante que apresente plano de adequação para que as situações de desconformidade sejam solucionadas, bem como elementos mitigadores para a prevenção de novas ocorrências.

3.2.2.3.6 Apresentação de avaliação específica sobre taxa de conversão

De acordo com o Manual de Monitoramento do Open Finance, no âmbito do fluxo de aplicação de medidas, a Estrutura de Governança do Open Finance deve demandar que a instituição participante apresente avaliação específica com diagnóstico sobre sua taxa de conversão e, se necessário, diagnóstico mais completo sobre a taxa de conversão da instituição participante em desconformidade emitido por empresa especializada independente.

3.2.3 Gerenciamento de tickets

3.2.3.1 Princípios para o gerenciamento de tickets

Deve ser implementada sistemática que permita a definição dos estados de atendimento dos tickets, bem como as transições entre os estados, de forma a permitir a adoção de ações adequadas ao seu tratamento, a exemplo de: triagem, enfileiramento, atribuição, resposta, avaliação e devolução. Essa sistemática deve estar detalhada no Portal do Open Finance no Brasil mantido pela Estrutura de Governança do Open Finance.

3.2.3.2 Classificação do prazo máximo de resolução do ticket

O prazo máximo de resolução do ticket deve estar associado ao mesmo antes do direcionamento às instituições participantes. Esses prazos estão definidos no item 3.2.3.4.

3.2.3.3 Trilha de auditoria do ticket

Toda atualização que gerar uma mudança do estado de atendimento ou do conteúdo do ticket deve ser devidamente registrada e armazenada para acesso futuro e para fins de verificação ou auditoria, observados os prazos de armazenamento previstos na regulamentação vigente.

3.2.3.4 Metas de prazo máximo para atendimento dos tickets

3.2.3.4.1 Requisição

As metas de prazo máximo para atendimento dos tickets por categoria de requisição são:

I - solicitação de informações ou de serviços: até cinco dias úteis

O prazo se refere ao fornecimento das informações solicitadas, à prestação dos serviços ou à indicação do canal adequado para a obtenção das informações.

II - sugestão de melhorias: até dez dias úteis

O prazo se refere ao fornecimento de resultado de análise preliminar da proposta, também informando prazo estimado de implementação, caso aplicável.

3.2.3.4.2 Incidentes

3.2.3.4.2.1 Incidentes sem indisponibilidade

As metas de prazo máximo para atendimento dos tickets por categoria de incidentes que não causem indisponibilidade de serviços são:

I - degradação de qualidade de serviço: até dois dias úteis;

II - erro de desconformidade: até dez dias úteis; e

III - demais erros: até trinta dias úteis.

Os prazos de que trata esta subseção contemplam a análise e a implantação de correção definitiva ou de contorno para reparar as falhas a que se referem.

Todos os tickets relativos a incidentes devem ser analisados de forma contínua pela Estrutura de Governança do Open Finance, a fim de avaliar eventual ajuste nas especificações e documentação, bem como aprimoramento da cobertura ou validação dos testes de certificação.

O Banco Central do Brasil pode estabelecer prazos diferenciados para quaisquer casos específicos, em virtude de análise quanto ao esforço requerido e ao impacto para o cidadão.

3.2.3.4.2.2 Incidentes com indisponibilidade

As metas para atendimento dos tickets relacionados a incidentes que causem indisponibilidade de serviços são de até 2,5 horas (duas horas e meia) para reestabelecimento do serviço. Uma vez reestabelecido o serviço, o ticket relativo ao incidente deve ser fechado em até um dia útil.

3.2.3.4.3 Monitoramento

As metas de prazo máximo para atendimento dos tickets relacionados a monitoramento são:

I - indícios de desconformidade - notificação: não há meta de prazo máximo;

II - indícios de desconformidade - demanda de ação: de acordo com a subseção 3.2.3.4.2;

III - consolidação de desconformidades: até cinco dias úteis para análise e eventual contestação;

IV - apresentação de relatório de situações de desconformidade: até cinco dias úteis após fim da análise do inciso III;

V - apresentação de plano de adequação: até dez dias úteis;

VI - apresentação de avaliação específica sobre taxa de conversão: até dez dias úteis; e

VII - apresentação de avaliação específica sobre taxa de conversão por empresa especializada independente: até noventa dias corridos.

3.2.3.5 Contagem de prazo de tickets

Os prazos se referem ao tempo total de atendimento, desde a geração do protocolo até o encerramento do ticket, englobando o tempo dispendido no Service Desk e nos participantes demandados. Caso haja necessidade de complementação de informações em relação aos tickets, a contagem de prazo fica suspensa até que as referidas informações sejam prestadas.

Ao solicitar complementação de informações, a instituição responsável pelo atendimento deve se certificar de que a informação é necessária e desconhecida para o cenário específico em análise. Se a informação for derivável de outras informações prestadas no ticket, não é classificável como desconhecida.

3.2.3.6 Atualização de tickets

A instituição participante responsável pelo atendimento deve atualizar tempestivamente a data prevista de implementação, mesmo que posterior à meta de atendimento estabelecida, em todos os tickets que demandem implementação.

Toda atualização no ticket (conteúdo e/ou estado de atendimento) deverá ser notificada ao demandante. Os participantes demandados também poderão receber notificações.

3.2.3.7 Encerramento de tickets

A instituição participante responsável pelo atendimento deve registrar a causa-raiz do objeto do ticket e descrever os ajustes realizados.

É vedado o encerramento de ticket referenciando evento no futuro, de modo que o referido encerramento deve ocorrer após a publicação de eventual ajuste na implementação.

Conforme os princípios para o gerenciamento de tickets, é necessário que haja uma avaliação da Estrutura de Governança do Open Finance, para que se assegure que a demanda que o ensejou tenha sido resolvida.

Para tickets associados ao processo de monitoramento, essa avaliação pode ser realizada antes do seu encerramento. Para os demais tickets, tal avaliação deve ser realizada após o seu encerramento e, caso a Estrutura de Governança do Open Finance entenda que é necessário aprofundamento da análise, deve ser aberto outro ticket solicitando providências, esclarecimentos ou evidências adicionais.

Caso se detecte que a demanda do ticket original não havia sido adequadamente resolvida quando do seu encerramento, tal ticket deve ser reaberto com recálculo de sua meta de prazo máximo para atendimento, independentemente do prazo decorrido.

Por exemplo, caso um ticket tenha sido encerrado dois dias úteis após sua meta e se detecte que a demanda não havia sido adequadamente resolvida, após recálculo, a nova meta de tal ticket deve ser dois dias úteis antes da data de reabertura.

3.2.3.8 Reabertura de tickets

O ticket pode ser reaberto pelo requerente caso a demanda não tenha sido adequadamente resolvida, de acordo com prazos definidos pela Estrutura de Governança do Open Finance.

A reabertura do ticket pode ser demandada a qualquer tempo pelo Banco Central do Brasil.

O recálculo da meta de prazo máximo para atendimento deve ser realizado de acordo com o definido no item 3.2.3.7.

3.3 Suporte a notificações

O Service Desk deve dispor de funcionalidade para notificação e divulgação de informações relevantes para as instituições participantes e demais interessados.

O processo envolve o reporte, a inserção em quadro de notícias ou o envio de informações às instituições participantes.

3.3.1 Tipos de notificações

As instituições participantes e a Estrutura de Governança do Open Finance devem reportar as seguintes informações:

I - atualizações tempestivas sobre indisponibilidade de APIs;

II - atualizações tempestivas sobre degradação de qualidade de serviços;

III - notificações sobre indisponibilidades programadas; e

IV - notificações sobre reestabelecimento de serviços.

A Estrutura de Governança do Open Finance pode utilizar a funcionalidade de que trata esta subseção para a realização de pesquisas e para a comunicação com instituições participantes.

A Estrutura de Governança do Open Finance deve detalhar as informações, as formas e o prazo das notificações, devendo esse detalhamento estar previsto no Portal do Open Finance no Brasil.

3.4 Suporte aos serviços prestados pela Estrutura de Governança do Open Finance

O Service Desk deve prover suporte aos seguintes tópicos relacionados aos serviços prestados pela Estrutura de Governança do Open Finance:

I - registro dos participantes no Diretório de Participantes;

II - acesso ao Diretório de Participantes;

III - atualizações do Diretório de Participantes; e

IV - consultas, reporte de problemas e reclamações quanto aos serviços prestados pela Estrutura de Governança do Open Finance.

3.5 SLAs do Service Desk

O Service Desk deve observar o seguinte nível mínimo de serviço:

Disponibilidade:

I - 24 horas por dia, 7 dias por semana;

II - 95% a cada 24 horas; e

III - 99,5% a cada 3 meses.

Desempenho das APIs:

Tempo de resposta de percentil 95 em, no máximo, 1500ms.

4\. Plataforma de Resolução de Disputas

A plataforma de resolução de disputas é ambiente que integra o mecanismo para resolução de disputas de que trata o art. 44, inciso IV, da Resolução Conjunta nº 1, de 2020. Complementarmente ao disposto neste manual, a plataforma de resolução de disputas deve ser desenvolvida de acordo com os padrões técnicos e outras questões operacionais definidas em documentos elaborados pela Estrutura de Governança do Open Finance.

4.1 SLAs da Plataforma de Resolução de Disputas

A Plataforma de Resolução de Disputas deverá observar o seguinte nível mínimo de serviço:

Disponibilidade:

I - 24 horas por dia, 7 dias por semana;

II - 95% a cada 24 horas; e

III - 99,5% a cada 3 meses.

5\. Portal do Open Finance no Brasil

5.1 Diretrizes do Portal do Open Finance no Brasil

5.1.1 Acessibilidade e diversidade

Todas as áreas a serem disponibilizadas no Portal do Open Finance no Brasil devem garantir acessibilidade e atender ao padrão Web Content Accessibility Guidelines (WCAG) e todo o conteúdo informativo deve levar em consideração a diversidade regional do país (rural/urbano, capital/interior), bem como a diversidade na população brasileira relativa a raça, gênero, faixa etária e deficiência.

5.1.2 Linguagem e tempestividade

A linguagem utilizada nas diferentes áreas do Portal deve ser adequada aos perfis de público que as visitam. O conteúdo deve ser disponibilizado de forma clara, acessível, transparente e atualizado de maneira tempestiva, refletindo adequadamente o cenário do Open Finance naquele momento e provendo as informações necessárias para entendê-lo e utilizá-lo. Em especial na área do cidadão, deve haver ênfase na aplicação visual, com vídeos, imagens, gráficos e infográficos que facilitem a compreensão das pessoas.

5.1.3 Segurança, sigilo e proteção de dados

O Portal deve prover um ambiente seguro de navegação, livre de malwares ou de meios para instalação de vulnerabilidades que possibilitem obter vantagem ilícita. Deve ser assegurado que o tratamento de dados, inclusive eventuais requisições de dados às pessoas visitantes, esteja em conformidade com a legislação vigente, em particular com as disposições da Lei nº 13.709, de 14 de agosto de 2018 (Lei Geral de Proteção de Dados).

5.2 Área do Desenvolvedor

A Área do Desenvolvedor deve ser um ambiente aberto, que evolua ao longo do tempo, em linha com o desenvolvimento do Open Finance.

O conteúdo a seguir deve ser disponibilizado de forma obrigatória:

I - especificações de APIs;

II - especificações de registro;

III - perfil de segurança;

IV - especificações do ambiente de Sandbox, incluindo tutoriais relacionados;

V - especificações dos testes de conformidade e de validação do ambiente de produção;

VI - documentação de políticas;

VII - problemas conhecidos da especificação;

VIII - diretrizes operacionais;

IX - diretrizes de experiência do cliente;

X - diretrizes técnicas do Diretório de Participantes;

XI - calendário;

XII - guias de implementação dos participantes;

XIII - perguntas frequentes (FAQ);

XIV - histórico de especificações; e

XV - histórico de alterações.

Se algum item ainda estiver pendente de especificação, a informação "a ser publicada" deve ser prestada.

As especificações de APIs devem observar o cronograma de implementação do Open Finance estabelecido na regulamentação vigente e na documentação da Estrutura de Governança do Open Finance.

A Estrutura de Governança do Open Finance deve notificar as instituições participantes a respeito de alterações no conteúdo dos itens de que tratam os incisos I a XII desta subseção.

5.3 Área do Cidadão

A Área do Cidadão deve ser um ambiente aberto, com foco na experiência do cidadão, com uso de linguagem adequada ao tema e de fácil compreensão, que evolua ao longo do tempo, em consonância com o desenvolvimento do Open Finance.

O conteúdo a seguir deve ser disponibilizado de forma obrigatória:

I - o que é o Open Finance?: explicação sobre o ambiente do Open Finance, incluindo sua origem, benefícios e aplicações, além do seu modo de funcionamento;

II - Estrutura de Governança do Open Finance: explicação sobre a Estrutura de Governança, com esclarecimento sobre o processo de formação, suas diferentes instâncias (nível estratégico, técnico e administrativo), composição, papéis e responsabilidades, bem como sobre a função do Banco Central do Brasil nesses aspectos;

III - jornada do cliente: material em formato visual (infográfico ou, preferencialmente, vídeo) que esclareça as pessoas sobre todos os passos para compartilhamento de dados, incluindo as etapas de consentimento, autenticação e confirmação; para iniciação de pagamentos e para encaminhamento de proposta de operação de crédito. O conteúdo deve explicar os termos utilizados durante a jornada e os campos de preenchimento requeridos, bem como abordar a jornada relativa à pessoa natural e à pessoa jurídica;

IV - segurança: infraestrutura de segurança do Open Finance, incluindo as responsabilidades das instituições participantes, alertas de segurança, cuidados a serem tomados para prevenção de fraudes e orientações caso a pessoa seja vítima de alguma fraude;

V - perguntas frequentes do cidadão (FAQ): resposta às dúvidas recorrentes dos cidadãos, em especial quanto ao objeto do Open Finance, as instituições participantes, a jornada do cliente, os direitos dos usuários, a segurança das transações e os canais para apresentação de demandas;

VI - orientações para encaminhamento de demandas: além de constar na FAQ, devem ser disponibilizadas, em área visível no portal, orientações que esclareçam o cidadão a quem recorrer em casos de dúvidas sobre o Open Finance ou de reclamação sobre as instituições participantes. Essas orientações devem abranger, inclusive, os casos em que a demanda é referente às entidades envolvidas no compartilhamento;

VII - mecanismo de busca de instituições participantes do Open Finance, que atenda as seguintes condições:

a) o mecanismo de busca deve, obrigatoriamente, propiciar a pesquisa por, no mínimo, nome da instituição, tipo de instituição, marca e modalidade de participação no Open Finance; e

b) a lista de participantes deve ser extraída do Diretório de Participantes mantido pela Estrutura de Governança do Open Finance e ser mantida permanentemente atualizada;

VIII - notícias: informações de interesse do cidadão;

IX - eventos: lista informativa de eventos sobre Open Finance, a exemplo de fóruns, conferências, painéis de discussão e eventos de networking; e

X - glossário: principais termos utilizados no contexto do Open Finance, com vistas a facilitar o entendimento de consumidores.

Adicionalmente, deve ser previsto conteúdo específico para pessoas jurídicas, com esclarecimentos sobre como o Open Finance pode contribuir para as empresas, especialmente as de menor porte, incluindo possíveis casos de uso, bem como vídeos e infográficos explicativos.

5.4 Área do Participante

Deve ser disponibilizada Área do Participante com informações voltadas a tópicos de interesse das instituições que participam ou pretendam participar do Open Finance. À semelhança da Área do Cidadão, esse também deve ser um ambiente aberto, que evolua ao longo do tempo. Podem ser disponibilizadas áreas de acesso restrito aos participantes do Open Finance.

Para essa área, os tópicos a serem cobertos de forma obrigatória estão discriminados a seguir:

I - participação no Open Finance: esclarecimentos gerais sobre escopo de participação e quais são as instituições obrigatórias e voluntárias;

II - parcerias: explicação sobre as formas de participação de instituições não supervisionadas pelo Banco Central do Brasil e responsabilidades envolvidas;

III - implementação: cronograma futuro de implementações estabelecidas pelo Banco Central do Brasil;

IV - registro no Open Finance: esclarecimentos gerais e tutorial para registro no Diretório de Participantes, incluindo forma de acesso;

V - Service Desk: informações gerais, funcionamento, SLAs previstos, tipos de demandas recepcionadas, orientações para cadastro e forma de acesso;

VI - mecanismos de resolução de disputas: orientações sobre o processo de resolução de disputas envolvendo instituições participantes;

VII - custeio da Estrutura de Governança do Open Finance: explicações sobre base de cálculo, responsabilidades das partes envolvidas e como efetuar o pagamento;

VIII - regulamentação do Open Finance: informações sobre os atos normativos vigentes, bem como documentos associados, podendo haver link diretamente para a página do Banco Central do Brasil sobre o tema;

IX - escopo de dados: explicação sobre o escopo de dados a ser compartilhado pelas instituições participantes;

X - escopo de serviços: explicação sobre o escopo de serviços a ser compartilhado pelas instituições participantes; e

XI - perguntas frequentes das instituições participantes: esclarecimentos das principais dúvidas sobre participação no Open Finance.

5.5 SLAs do Portal do Open Finance

O Portal do Open Finance deve observar o seguinte nível mínimo de serviço:

Disponibilidade:

I - 24 horas por dia, 7 dias por semana;

II - 90% a cada 24 horas; e

III - 99,5% a cada 3 meses.

6\. Sandbox

A Estrutura de Governança do Open Finance deve disponibilizar uma estrutura, doravante denominada Sandbox, que permita aos participantes, no mínimo:

I - submeter, ainda em tempo de desenvolvimento, suas implementações das APIs do Open Finance a testes automatizados funcionais e não funcionais; e

II - acessar implementações de exemplo das APIs do Open Finance, inclusive ao menos uma que simule uma Instituição Participante de Referência, com implementação completa de cada API.

O Portal do Open Finance deve conter tutoriais apresentando de maneira completa, detalhada, passo a passo e, quando aplicável, por meio de trechos de código e/ou capturas de tela, como os participantes devem interagir com o Sandbox para, entre outras coisas, executar os testes automatizados e acessar as implementações de exemplo mencionadas anteriormente.

6.1 SLAs do Sandbox

O Sandbox deve observar o seguinte nível mínimo de serviço:

Disponibilidade:

I - 95%, das 8h às 20h em dias úteis, no fuso do Distrito Federal, conforme definido no art. 2º, alínea "b", do Decreto nº 2.784, de 18 de junho de 1913, com alterações posteriores; e

II - 80% nos demais horários.

7\. Validação do Ambiente de Produção

A Estrutura de Governança do Open Finance deve prover mecanismo de validação de forma a garantir que os ambientes de produção das instituições participantes estejam aderentes às suas respectivas certificações.

A política desse mecanismo de validação deve ser estabelecida pela Estrutura de Governança do Open Finance e ser seguida pelas instituições participantes.

8\. Monitoramento do Open Finance

A Estrutura de Governança do Open Finance deve realizar o monitoramento do ecossistema conforme o Manual de Monitoramento do Open Finance.

Esse processo inclui a disponibilização de informações para que as instituições participantes possam fazer a gestão das situações de desconformidade e a divulgação de dados estatísticos e indicadores sobre a atuação das instituições participantes no Open Finance.

9\. Regras transitórias

Considerando que a implementação de disponibilização de evidências em relação a alguns dos itens monitorados, conforme a versão 2.0 do Manual de Monitoramento do Open Finance, constante de anexo à Instrução Normativa BCB nº 575, de 20 de dezembro de 2024, somente ocorrerá a partir de 1º de julho de 2025, a obrigação de apresentação de evidências do indício de desconformidade ou do local em que tais evidências estão disponíveis para consulta, de que trata a subseção 3.2.2.3.1 Indícios de desconformidade - notificação, relativas a itens monitorados cuja implementação de disponibilização de evidências ocorrer apenas a partir de 1º de julho de 2025, entra em vigor também a partir dessa data.

Em decorrência da necessidade de aprimoramentos nas equipes da Estrutura de Governança do Open Finance responsáveis pelo monitoramento, as alterações relacionadas à avaliação a ser realizada pela Estrutura de Governança do Open Finance durante o processo de encerramento dos tickets, de que trata a subseção 3.2.3.7, entram em vigor a partir de 1º de julho de 2025.

Brasília, 31 de janeiro de 2025.
