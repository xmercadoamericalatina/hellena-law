---
titulo: "PORTARIA Nº 626, DE 4 DE AGOSTO DE 2026"
orgao: "Ministério dos Transportes/Gabinete do Ministro"
tipo: "Portaria"
numero: "626"
data: 2026-08-04
revogada: false
versao_texto: "publicação original"
publicacao: "DOU de 14/08/2026, seção 1, p. 128"
data_publicacao: 2026-08-14
edicao: "153"
fonte: "https://www.in.gov.br/web/dou/-/portaria-n-626-de-4-de-agosto-de-2026-725482065"
baixado_em: 2026-10-15
---
# PORTARIA Nº 626, DE 4 DE AGOSTO DE 2026

PORTARIA Nº 626, DE 4 DE AGOSTO DE 2026

Estabelece diretrizes e procedimentos operacionais para a gestão de backup e restauração de dados digitais no âmbito do Ministério dos Transportes.

O MINISTRO DE ESTADO DOS TRANSPORTES, no uso das atribuições que lhe confere o art. 87, parágrafo único, inciso II, da Constituição, e tendo em vista o disposto na Lei nº 12.527, de 18 de novembro de 2011 (Lei de Acesso à Informação), na Lei nº 13.709, de 14 de agosto de 2018 (Lei Geral de Proteção de Dados Pessoais - LGPD), e considerando as diretrizes estabelecidas pela Política de Segurança da Informação - POSIN, aprovada pela Portaria MT nº 287, de 4 de abril de 2025, e com base no constante dos autos do processo nº 50000.029522/2025-28, bem como a necessidade de padronizar os procedimentos técnicos e operacionais relacionados à proteção de ativos digitais, resolve:

#### CAPÍTULO I — DAS DISPOSIÇÕES PRELIMINARES E FUNDAMENTOS

##### Seção I — Do Objeto e da Finalidade

**Art. 1º** Esta Portaria institui a Norma de Backup e Restauração de Dados Digitais e disciplina, no âmbito do Ministério dos Transportes, as diretrizes para a execução de backup e de procedimentos de restauração de dados digitais, com o objetivo de promover a salvaguarda e a recuperação da informação institucional crítica, assegurando sua proteção contra falhas, perdas acidentais, eventos adversos, incidentes cibernéticos ou desastres.

**Parágrafo único.** A observância e o cumprimento desta Norma são elementos essenciais para a concretização dos pilares da segurança da informação - confidencialidade, integridade e disponibilidade - relativamente aos dados digitais corporativos mantidos sob a custódia do Ministério dos Transportes.

**Art. 2º** A Norma instituída por esta Portaria estabelece procedimentos técnicos e operacionais uniformes destinados à execução de backups de dados institucionais, englobando expressamente aqueles custodiados em ambientes internos (on-premises) e serviços de computação em nuvem (cloud computing) contratados pelo Ministério dos Transportes, de modo a garantir a plena continuidade das operações administrativas e finalísticas da Pasta.

**Art. 3º** A gestão integrada dos dados armazenados em todos os ambientes tecnológicos de responsabilidade do Ministério dos Transportes deverá incorporar mecanismos robustos que garantam a continuidade operacional e a proteção eficaz das informações, devendo o Plano de Contingência estar incorporado ao Plano de Backup e Restauração de Dados Digitais, contemplando:

I - a restauração de dados em casos de falhas, perdas acidentais, eventos adversos, incidentes cibernéticos ou desastres; e

II - armazenamento estruturado, rotinas de verificação, testes periódicos de restauração e descarte seguro, quando necessário.

**Art. 4º** Compete à Subsecretaria de Gestão Estratégica, Tecnologia e Inovação (SGETI) definir, coordenar, supervisionar, operacionalizar e padronizar os procedimentos técnicos indispensáveis à aplicação desta Norma, promovendo sua execução por intermédio da unidade técnica responsável pela infraestrutura de TIC do Ministério dos Transportes, atualmente a Coordenação de Infraestrutura de Tecnologias (COINT), ou outra que venha a substituí-la, conforme a organização administrativa vigente, observadas as atribuições previstas no respectivo regimento interno e os demais atos normativos setoriais aplicáveis.

##### Seção II — Das Definições Técnicas

**Art. 5º** Para os efeitos de aplicação e interpretação desta Norma, quando indispensável à adequada compreensão de seus dispositivos, adotam-se as seguintes definições conceituais, de natureza técnica, fundamentais para a uniformidade técnica e operacional:

I - Administrador de Backup: Agente público ou equipe formalmente designada, responsável pela totalidade dos procedimentos de configuração, agendamento, execução, monitoramento contínuo, elaboração de padrões técnicos, atendimentos de segundo e terceiro níveis (avançados), resolução de incidentes complexos e realização dos testes documentados relativos aos processos de backup e restauração de dados digitais;

II - Ativo de Informação: Meios de armazenamento, transmissão e processamento da informação, equipamentos necessários a isso, sistemas utilizados para tal, locais onde se encontram esses meios, recursos humanos que a eles têm acesso e conhecimento ou dado que tem valor para um indivíduo ou organização;

III - Banco de Dados: Coleção de dados inter-relacionados, representando informações sobre um domínio específico. São coleções organizadas de dados que se relacionam, a fim de criar algum sentido (informação) e de dar mais eficiência durante uma consulta ou a geração de informações ou conhecimento;

IV - Backup: Conjunto de procedimentos que permitem salvaguardar os dados de um sistema computacional, garantindo guarda, proteção e recuperação. Tem a fidelidade ao original assegurada. Esse termo também é utilizado para identificar a mídia em que a cópia é realizada;

V - Backup Completo (Full Backup): Modalidade de backup que implica na cópia integral de todos os dados abrangidos pelo escopo de salvaguarda para uma unidade de armazenamento designada, independentemente de terem sido alterados ou movidos desde o último backup realizado;

VI - Backup Diferencial (Differential Backup): Modalidade de backup na qual são salvaguardados exclusivamente os dados que foram novos ou modificados desde a execução do último Backup Completo (Full Backup) efetuado;

VII - Backup Incremental (Incremental Backup): Modalidade de backup que abrange somente os arquivos que foram criados ou modificados a partir da execução do backup imediatamente anterior, seja este um Backup Completo, Diferencial ou Incremental;

VIII - Backup Offline: Modalidade de armazenamento em que, após sua conclusão, o backup não permanece acessível por meio da rede de dados do Ministério, sendo armazenado em mídias físicas, logicamente ou fisicamente removíveis;

IX - Backup Offsite: Modalidade de armazenamento em que, após sua conclusão, o backup é transferido e armazenado em um local geograficamente distinto, como um segundo centro de dados (data center) ou em um serviço de backup em nuvem (modalidade remota), garantindo a proteção contra sinistros locais;

X - Backup Online: Modalidade de armazenamento em que o backup, uma vez realizado, permanece acessível dentro da rede de dados do Ministério dos Transportes, facilitando a restauração e o acesso imediato dos sistemas;

XI - Código-Fonte: O conjunto legível de palavras ou símbolos ordenados, contendo instruções escritas em uma linguagem de programação específica, de maneira lógica e sequencial, que constitui o programa de computador;

XII - Criticidade: O grau inerente de importância e essencialidade da informação para a continuidade ininterrupta das atividades, serviços e processos finalísticos e subsidiários do Ministério dos Transportes;

XIII - Custodiante da Informação: Qualquer indivíduo, setor ou estrutura orgânica que possua a responsabilidade formal de proteger a informação e de aplicar os níveis de controles de segurança em estrita conformidade com as exigências de Segurança da Informação previamente comunicadas pelo proprietário da informação;

XIV - Descarte: A ação formal e segura de eliminação de informações institucionais, documentos, mídias ou acervos digitais armazenados;

XV - Escopo: Identificação e delimitação claras dos dados digitais, sistemas ou repositórios que serão submetidos às rotinas regulares de backup;

XVI - Frequência: A periodicidade regular estabelecida para a execução de backups, podendo ser diária, semanal, mensal ou anual, conforme a criticidade e a volatilidade dos dados;

XVII - Gestor da Informação: Agente público formalmente designado e responsável primário pela administração funcional do serviço, sistema ou conjunto de dados e informações produzidos no âmbito de seu processo de trabalho, caracterizando-se como o gestor da área de negócio ou da missão institucional correspondente;

XVIII - Janela de Backup: O período de tempo específico, disponível ou planejado, reservado para a execução das rotinas de backup, de forma a minimizar ou evitar qualquer tipo de interferência adversa no desempenho e na disponibilidade da rede de dados e dos serviços de TIC do Ministério dos Transportes;

XIX - Mídia: Os mecanismos físicos ou lógicos em que dados podem ser armazenados e conservados, incluindo, mas não se limitando a discos ópticos, magnéticos, fitas, discos rígidos (storage) e soluções de arquivo em nuvem;

XX - Operador de Backup: Pessoa responsável pela execução dos procedimentos operacionais de atendimento de primeiro nível, englobando o acompanhamento detalhado da execução de rotinas de backup, a realização de restaurações de arquivos específicas solicitadas por usuários, a execução de testes de restauração de dados e outras atividades operacionais diárias relacionadas ao processo de backup e restauração de dados digitais;

XXI - Plano de Backup e Restauração de Dados Digitais: Documento formalizado que estabelece o conjunto detalhado de diretrizes, procedimentos técnicos e controles que orientam a criação, o armazenamento, a verificação da integridade, os procedimentos de restauração e o descarte seguro de cópias de dados;

XXII - Plano de Contingência: Instrumento normativo e operacional que estabelece as diretrizes, os procedimentos de restauração de backups e as responsabilidades previamente definidas, destinado a assegurar a rápida restauração e a preservação dos dados e ativos de informação em situações de falhas críticas, perdas acidentais de grande escala, eventos adversos, incidentes cibernéticos ou desastres;

XXIII - Recovery Point Objective - RPO: O ponto no tempo máximo aceitável em que os dados de um determinado serviço de TIC devem ser recuperados após uma situação de interrupção ou perda;

XXIV - Recovery Time Objective - RTO: O tempo estimado e máximo para que os dados sejam restaurados e o serviço de TIC correspondente volte a se encontrar em pleno funcionamento;

XXV - Repositório de Arquivo: Um conjunto organizado de documentos digitais ou um local lógico onde os documentos são guardados, gerenciados e preservados;

XXVI - Retenção: O período temporal estabelecido e formal de armazenamento e conservação das cópias de segurança para fins de auditoria, históricos e legais;

XXVII - Rotina de Backup: O fluxo procedimental automatizado ou manual de realização de backups; e

XXVIII - Serviços de TIC: Conjunto estruturado e organizado de recursos tecnológicos, processos operacionais e atividades de suporte essenciais para fornecer serviços de coleta, processamento, armazenamento, transmissão e proteção de informações digitais no Ministério dos Transportes.

**§ 1º** Além das definições contidas neste artigo, a interpretação e a aplicação desta Norma deverão considerar e respeitar os conceitos dispostos na Lei nº 12.527, de 2011 (Lei de Acesso à Informação - LAI), na Lei nº 13.709, de 2018 (Lei Geral de Proteção de Dados Pessoais - LGPD), no Glossário de Segurança da Informação (Portaria GSI/PR nº 93, de 18 de outubro de 2021) e na Política de Segurança da Informação em vigor no Ministério - POSIN (Portaria MT nº 287, de 4 de abril de 2025).

**§ 2º** Em caso de divergência ou omissão de conceitos técnicos, prevalecerão as definições estabelecidas na Política de Segurança da Informação do Ministério e nas normas de segurança cibernética emitidas pelo Gabinete de Segurança Institucional da Presidência da República - GSI/PR.

##### Seção III — Do Âmbito de Aplicação

**Art. 6º** A presente Norma se aplica a todos os dados digitais institucionais produzidos ou custodiados pelo Ministério dos Transportes, inclusive os armazenados em serviços de computação em nuvem formalmente contratados pela Pasta.

**Parágrafo único.** A obrigatoriedade de salvaguarda dos dados digitais pertencentes aos serviços de TIC do Ministério dos Transportes, mas que estejam sob a custódia, interna ou externa, de outras entidades, públicas ou privadas, como ocorre nos casos de ambientes e serviços em nuvem (cloud computing), deverá estar explicitamente garantida e detalhada nos acordos, termos de referência e instrumentos contratuais que formalizam a relação de fornecimento e responsabilidade entre as partes envolvidas, assegurada a retenção da propriedade e do controle dos dados pelo Ministério.

**Art. 7º** As diretrizes estabelecidas nesta Norma aplicam-se a todos os agentes que interagem com o ambiente de Tecnologias da Informação e Comunicação do Ministério dos Transportes, compreendendo:

I - os servidores efetivos, os empregados públicos, os estagiários e quaisquer colaboradores terceirizados que, em razão de sua função ou acesso autorizado, criem, manipulem ou acessem dados pertencentes formalmente ao acervo informacional do Ministério; e

II - os prestadores de serviço, as empresas contratadas e quaisquer terceiros que utilizem, ainda que de forma temporária ou eventual, os serviços de TIC sob a responsabilidade do Ministério dos Transportes, inclusive no âmbito de suas unidades descentralizadas ou de entidades a ele vinculadas que utilizem a infraestrutura central de TIC.

**Art. 8º** Em virtude da distribuição de competências e da necessidade de delimitar o escopo de atuação direta da área de Tecnologia da Informação do Ministério, não se submetem às rotinas padronizadas de backup e restauração de dados digitais previstas nesta Norma:

I - os dados armazenados localmente em estações de trabalho pessoais, computadores portáteis (notebooks), dispositivos de armazenamento externos, mídias removíveis ou quaisquer outros equipamentos de TI que não sejam gerenciados, monitorados e controlados diretamente pela área de Infraestrutura de Tecnologias da Informação do Ministério dos Transportes; e

II - os dados produzidos e armazenados por órgãos ou entidades federais que, embora mantenham vínculo formal ou institucional com o Ministério dos Transportes, detenham autonomia administrativa, orçamentária e tecnológica para gerir sua própria infraestrutura e política de backup.

#### CAPÍTULO II — DOS PRINCÍPIOS GERAIS DE BACKUP E CONTINUIDADE

**Art. 9º** Esta Norma regulamenta as ações relacionadas ao backup e à restauração de dados digitais no âmbito do Ministério dos Transportes, devendo observar as diretrizes e os requisitos estabelecidos na Política de Segurança da Informação - POSIN.

**Art. 10.** A Norma de Backup e Restauração de Dados Digitais deverá manter alinhamento à gestão de continuidade de negócios do Ministério dos Transportes.

**Art. 11.** O Plano de Backup e Restauração de Dados Digitais deverá estar integrado ao Plano de Resposta a Incidentes de Segurança da Informação, à Política de Segurança da Informação - POSIN e ao processo institucional de gestão de riscos de segurança da informação do Ministério dos Transportes.

**Parágrafo único.** As falhas relevantes na execução das rotinas de backup, bem como os resultados dos testes de restauração que indiquem vulnerabilidades, indisponibilidades ou inconsistências relevantes, deverão ser registrados e tratados como eventos de segurança da informação, constituindo insumo para o processo institucional de gestão de riscos e para o aprimoramento contínuo dos controles de segurança da informação, devendo tais ocorrências ser comunicadas à unidade responsável pela gestão de incidentes de segurança da informação no âmbito do Ministério dos Transportes.

**Art. 12.** As rotinas de backup devem ser projetadas, configuradas e executadas com o propósito de viabilizar a restauração integral dos dados dentro do Recovery Time Objective (RTO) estabelecido no Plano de Backup e Restauração de Dados Digitais, especialmente em situações de indisponibilidade, falha crítica dos serviços de TIC, incidentes cibernéticos ou desastres.

**Art. 13.** As rotinas de backup devem utilizar soluções tecnológicas próprias e especializadas, concebidas especificamente para este fim, devendo ser implementada, sempre que tecnicamente viável, a automação das rotinas de backup.

**Art. 14.** Deverão ser estabelecidos requisitos mínimos diferenciados de periodicidade, frequência e retenção das rotinas de backup, definidos de acordo com a classificação de criticidade do serviço de TIC, da base de dados ou do tipo de dado salvaguardado, concedendo-se prioridade máxima de planejamento e execução aos serviços de TIC formalmente classificados como críticos para o funcionamento do Ministério dos Transportes.

**Art. 15.** O armazenamento dos backups deverá ser realizado, sempre que tecnicamente factível e economicamente viável, em local distinto da infraestrutura de produção.

**Art. 16.** A infraestrutura de rede utilizada nos processos de backup deverá ser segregada dos sistemas de produção e das redes que suportam serviços críticos, ao menos de forma lógica e, quando tecnicamente viável, também de forma física, de modo a prevenir a propagação de incidentes cibernéticos entre os ambientes de produção e de backup.

**Art. 17.** A unidade técnica responsável pela infraestrutura de TIC do Ministério dos Transportes deverá manter reserva estratégica de recursos físicos e lógicos de infraestrutura, adequadamente segregados dos ambientes de produção, destinados à realização de testes periódicos e formais de restauração de backups, conforme previsto no Plano de Backup e Restauração de Dados Digitais, assegurando que tais testes não comprometam a disponibilidade dos ambientes produtivos.

**Art. 18.** O Gestor da Informação ou o responsável técnico formalmente designado pelo produto, sistema ou serviço de TIC deverá solicitar formalmente à unidade técnica responsável pela infraestrutura de TIC do Ministério dos Transportes a inclusão de seus dados no sistema regular de backup, em conformidade com o Plano de Backup e Restauração de Dados Digitais, previamente à entrada em operação efetiva da solução.

**Art. 19.** Em situações em que a confidencialidade da informação seja relevante, os backups deverão ser protegidos por meio de mecanismos de criptografia, sempre que tecnicamente e economicamente viável, observados o nível de criticidade da informação e os riscos associados.

#### CAPÍTULO III — DA FREQUÊNCIA E ESTRATÉGIA DE BACKUP

##### Seção I — Da Frequência e dos Métodos de Backup

**Art. 20.** Os backups dos serviços de TIC do Ministério dos Transportes deverão ser realizados observando, no mínimo, as seguintes frequências temporais:

I - diária;

II - semanal;

III - mensal; ou

IV - anual.

**Art. 21.** As especificidades operacionais dos serviços de TIC, sejam eles classificados como críticos ou não críticos, poderão demandar a adoção de frequência, método e tempo de retenção distintos das frequências mínimas estabelecidas nos incisos do art. 20, desde que tais exceções estejam devidamente justificadas e formalmente aprovadas no Plano de Backup e Restauração de Dados Digitais.

**Art. 22.** Todos os ativos de informação diretamente envolvidos no processo de backup são considerados, para fins desta Norma, ativos críticos e deverão receber tratamento e níveis de proteção compatíveis com essa classificação.

**Art. 23.** Os backups deverão ser armazenados em diferentes dispositivos e tecnologias, conforme a necessidade técnica e a disponibilidade de recursos previstas no Plano de Backup e Restauração de Dados Digitais, podendo ser utilizados, entre outros meios:

I - fitas magnéticas;

II - discos rígidos ou de estado sólido em sistemas de armazenamento dedicados; ou

III - serviços de armazenamento em nuvem formalmente contratados pelo Ministério dos Transportes e que atendam aos requisitos de segurança da informação.

**Art. 24.** A realização dos backups poderá utilizar os métodos Completo, Diferencial ou Incremental.

**Parágrafo único.** A utilização e a periodicidade dos métodos Diferencial e Incremental poderão ser ajustadas pelo Administrador de Backup, mediante justificativa técnica formal, em razão de limitações de espaço de armazenamento ou da necessidade de otimização do uso dos recursos computacionais.

**Art. 25.** Os backups deverão possuir, no mínimo, duas cópias armazenadas em meios distintos, sendo uma mantida em ambiente online e outra em ambiente offline ou offsite.

**Art. 26.** Os sistemas, bases de dados ou repositórios de arquivos classificados como críticos deverão contar com backups armazenados em dispositivos offline, preferencialmente em mídias físicas.

**Art. 27.** A restauração de dados limita-se ao último ponto de recuperação disponível, correspondente à última execução bem-sucedida do backup, não sendo tecnicamente possível recuperar dados criados ou modificados após esse ponto.

**Art. 28.** Nos casos em que os serviços de TIC forem contratados para operar em ambiente de nuvem (cloud computing), as soluções e rotinas de backup poderão estar integradas ao serviço contratado, desde que o instrumento contratual assegure, de forma expressa e inequívoca:

I - a integridade dos dados armazenados;

II - a possibilidade de pronta restauração;

III - o atendimento ao Recovery Point Objective (RPO) estabelecido pelo Ministério dos Transportes; e

IV - o atendimento ao Recovery Time Objective (RTO) estabelecido pelo Ministério dos Transportes.

##### Seção II — Da Estrutura e do Escopo do Plano de Backup e Restauração de Dados Digitais

**Art. 29.** O Plano de Backup e Restauração de Dados Digitais deverá constituir documento dinâmico e suficientemente abrangente, refletindo com precisão os requisitos de negócio do Ministério dos Transportes, bem como os requisitos de segurança da informação e de proteção de dados.

**§ 1º** O Plano de Backup e Restauração de Dados Digitais deverá explicitar, como requisitos técnicos mínimos obrigatórios, para cada sistema ou conjunto de dados, no mínimo:

I - o escopo detalhado dos dados digitais a serem salvaguardados;

II - o tipo de backup a ser utilizado;

III - a frequência de execução das rotinas de backup;

IV - o período de retenção dos dados armazenados;

V - o Recovery Point Objective (RPO); e

VI - o Recovery Time Objective (RTO).

**Art. 30.** Somente serão incluídos nas rotinas regulares de backup os ativos de informação formalmente armazenados em servidores e demais infraestruturas físicas ou lógicas, inclusive ambientes locais (on-premises) ou em serviços de computação em nuvem, desde que:

I - estejam sob gestão direta da Subsecretaria de Gestão Estratégica, Tecnologia e Inovação (SGETI); e

II - sejam necessários à continuidade do negócio do Ministério dos Transportes ou formalmente classificados como estratégicos ou imprescindíveis.

**§ 1º** As naturezas dos dados e ativos de informação passíveis de backup incluem, mas não se limitam, às seguintes categorias:

I - arquivos de sistemas corporativos;

II - arquivos de sistemas operacionais;

III - bases de dados;

IV - arquivos armazenados em servidores de arquivos ou em serviços corporativos de armazenamento em nuvem;

V - repositórios de código-fonte de aplicações institucionais e documentação técnica associada;

VI - serviços de correio eletrônico corporativo;

VII - máquinas virtuais e ambientes conteinerizados;

VIII - diretórios de autenticação e serviços de identidade;

IX - arquivos de configuração de sistemas e equipamentos de rede; e

X - arquivos de log e registros de auditoria.

**§ 2º** O rol previsto no § 1º poderá ser ampliado a qualquer tempo pela SGETI, em razão da adoção de novas tecnologias, dispositivos ou contextos operacionais que demandem salvaguarda.

**§ 3º** A classificação de dados e ativos de informação como estratégicos ou imprescindíveis será realizada formalmente pelo Comitê de Governança Digital e Segurança da Informação (CGDSI), que poderá consultar, quando julgar pertinente, as áreas de negócio envolvidas, órgãos setoriais do Ministério dos Transportes ou entidades externas.

**Art. 31.** Do escopo regular das rotinas de backup estarão excluídos os dados armazenados em estações individuais de trabalho, bem como os dados de natureza pessoal de agente público do Ministério inseridos diretamente na rede ministerial, ressalvadas as seguintes hipóteses em que a salvaguarda é permitida para fins de análise e preservação probatória:

I - identificação de um incidente cibernético confirmado em algum desses ativos individuais, sendo o backup realizado para fins de mitigação de danos e análise forense; ou

II - ocorrência comprovada de infração à legislação penal ou de processo administrativo disciplinar (PAD) envolvendo dispositivo que faça parte do patrimônio do Ministério dos Transportes, sendo o backup fundamental para a cadeia de custódia da prova.

**Parágrafo único.** É de responsabilidade inequívoca e exclusiva do usuário o gerenciamento e o armazenamento de seus dados de trabalho no Servidor de Arquivos Corporativo, no OneDrive institucional ou no SharePoint, ambientes para os quais o Ministério já possui rotinas regulares e adequadas de backup.

#### CAPÍTULO IV — DA RETENÇÃO, PRESERVAÇÃO E DISPONIBILIDADE

##### Seção I — Da Política Geral de Retenção, Preservação e Descarte de Dados Digitais

**Art. 32.** A determinação do período de retenção, entendido como o prazo de armazenamento e conservação dos backups, bem como a posterior eliminação de dados, deverá observar a criticidade da informação, o tipo de serviço de TIC, a frequência de atualização dos dados, as características específicas de cada sistema e, prioritariamente, a legislação e as normas vigentes que estabelecem os prazos mínimos e máximos de armazenamento de dados e documentos no âmbito da Administração Pública Federal.

**Art. 33.** Os prazos de retenção, preservação e descarte de dados digitais previstos nesta Norma deverão ser aplicados em conformidade com a legislação arquivística federal, com as normas de gestão documental da Administração Pública Federal e com as orientações expedidas pelo Arquivo Nacional e pelo órgão central do Sistema de Gestão de Documentos e Arquivos - SIGA.

**Parágrafo único.** Na hipótese de superveniência de norma arquivística específica que estabeleça prazo distinto para guarda ou eliminação de dados e documentos digitais, prevalecerá o disposto na norma arquivística.

**Art. 34.** Expirado o prazo de retenção dos dados armazenados, a mídia física ou lógica utilizada poderá ser formalmente reutilizada para novos backups ou, se necessário, descartada ou destruída, observados seu estado de uso, o número limite de ciclos de leitura e gravação recomendados pelo fabricante e os requisitos de segurança da informação aplicáveis.

**Parágrafo único.** Nenhuma mídia de backup física deverá permanecer armazenada por período superior a 30 (trinta) anos. Caso esse prazo limite seja atingido, e sem prejuízo dos prazos legais de retenção aplicáveis aos dados, as informações deverão ser obrigatoriamente transferidas para mídia de tecnologia mais recente, e a mídia original deverá ser destruída de forma segura, garantindo sua completa inutilização, e descartada em local apropriado, em conformidade com a legislação ambiental e de resíduos sólidos vigente.

**Art. 35.** No caso de desligamento formal do usuário (seja de forma permanente ou temporária, como licença de longa duração), o backup de seus arquivos de trabalho armazenados em serviços corporativos de nuvem deverá ser mantido por um período de, no mínimo, 30 (trinta) dias, para fins de transição e eventual resgate.

**§ 1º** Após o decurso do prazo mínimo de 30 (trinta) dias, os arquivos do usuário desligado poderão ser excluídos a qualquer tempo pelo Administrador de Backup, salvo nas hipóteses em que for formalmente necessária a preservação dos dados, como nos casos vinculados a sindicâncias em curso, auditorias, processos judiciais ou processos administrativos disciplinares.

**§ 2º** Os pedidos de preservação de dados deverão ser encaminhados formalmente à unidade técnica responsável pela infraestrutura de TIC do Ministério dos Transportes, devidamente instruídos com as justificativas detalhadas que demonstrem a imperiosa necessidade de preservação e o prazo estimado para tal manutenção.

##### Seção II — Da Retenção e Preservação de Dados do Programa de Gestão e Desempenho - PGD

**Art. 36.** Os sistemas informatizados de suporte ao Programa de Gestão e Desempenho (PGD) deverão seguir os requisitos específicos para retenção, backup e expurgo (eliminação) descritos e estabelecidos na Resolução CPGD/MGI nº 5, de 21 de agosto de 2025, ou norma que a suceda.

**Art. 37.** Os dados classificados como de arquivo corrente, relativos ao PGD, deverão ser preservados em ambiente ativo com acesso direto por meio dos sistemas informatizados do Programa de Gestão, por um período mínimo de 5 (cinco) anos, período este contado a partir da data de seu arquivamento.

**§ 1º** Considera-se arquivamento, para os fins da Resolução CPGD/MGI nº 5, de 21 de agosto de 2025, o momento em que os dados deixam de ter uso corrente, em razão do encerramento de seu ciclo funcional ou processual.

**§ 2º** No caso dos planos de trabalho e de entregas do PGD, considera-se arquivamento o término da fase de avaliação, incluindo a análise de eventuais recursos, quando não houver mais necessidade operacional direta de acesso ou modificação dos dados.

**§ 3º** Os dados referentes a registros de auditoria (logs) ficam dispensados da retenção em ambiente ativo.

**Art. 38.** Após os prazos previstos no art. 37, os dados do PGD poderão ser removidos do ambiente ativo e preservados em ambiente de backup, desde que atendidos cumulativamente os seguintes requisitos:

I - inexistência de pendências legais ou administrativas associadas aos dados; e

II - envio completo das informações à Interface de Programação de Aplicação - API do PGD, nos termos do art. 29 da Instrução Normativa Conjunta SEGES-SGPRT/MGI nº 24, de 2023.

**Art. 39.** Os dados dos sistemas informatizados do PGD deverão ser preservados em ambiente de backup por 52 (cinquenta e dois) anos, contados a partir da data de sua transferência do ambiente ativo, assegurando-se, durante todo o período, sua integridade, rastreabilidade e disponibilidade mediante solicitação de autoridade competente.

**§ 1º** Os dados referentes a registros de auditoria (logs) dos sistemas informatizados do PGD deverão ser preservados em ambiente de backup por um período de 5 (cinco) anos.

**§ 2º** Sempre que solicitado por autoridade administrativa ou judicial competente, os dados preservados em ambiente de backup deverão ser disponibilizados no prazo determinado no pedido ou, na ausência de previsão específica, em até 30 (trinta) dias corridos.

**Art. 40.** Decorridos os prazos previstos no art. 39, os dados poderão ser definitivamente eliminados, desde que haja verificação formal da inexistência de pendências legais, administrativas ou de valor histórico associado às informações.

#### CAPÍTULO V — DOS REQUISITOS TÉCNICOS E OPERACIONAIS

##### Seção I — Da Gestão do Tráfego na Rede de Computadores

**Art. 41.** O Administrador de Backup deverá realizar o planejamento e o monitoramento contínuo dos processos de backup, de modo a mitigar os impactos de sua execução sobre o desempenho geral da rede de dados do Ministério dos Transportes, prevenindo indisponibilidades não planejadas e assegurando que o tráfego necessário às rotinas de backup não comprometa a continuidade dos demais serviços de TIC.

**Art. 42.** A execução do backup deve concentrar-se, preferencialmente, no período da Janela de Backup, de modo a não interferir no desempenho da rede de dados do Ministério dos Transportes.

**Art. 43.** O período da Janela de Backup e seus limites temporais devem ser determinados de forma articulada pelo Administrador de Backup em conjunto com a unidade técnica responsável pela infraestrutura de TIC do Ministério dos Transportes, com a anuência formal das áreas de negócio impactadas.

##### Seção II — Do Transporte e Acondicionamento das Mídias

**Art. 44.** A escolha das unidades de armazenamento e das tecnologias utilizadas na salvaguarda dos dados digitais deve ser precedida de análise formal que considere, no mínimo, as seguintes características técnicas e econômicas dos dados a serem resguardados:

I - a criticidade do dado salvaguardado;

II - o tempo de retenção do dado;

III - a probabilidade de necessidade de restauração;

IV - o tempo esperado para restauração;

V - o custo de aquisição da unidade de armazenamento de backup; e

VI - a vida útil da unidade de armazenamento de backup.

**Art. 45.** O Administrador de Backup tem a atribuição de identificar a viabilidade técnica e logística de utilização de diferentes tecnologias na realização de backups, propondo a solução mais apropriada e resiliente para cada caso.

**Art. 46.** Podem ser utilizadas técnicas de compressão de dados, contanto que o acréscimo no tempo de restauração dos dados seja considerado aceitável pelo Gestor da Informação.

**Art. 47.** A execução e o planejamento das rotinas de backup devem envolver a previsão contínua de ampliação e escalabilidade da capacidade dos dispositivos e sistemas de armazenamento envolvidos, em face do crescimento constante do volume de dados institucionais.

**Art. 48.** As unidades de armazenamento que contêm backups devem ser acondicionadas e mantidas em locais seguros e apropriados, que possuam controle de fatores ambientais sensíveis, tais como umidade, temperatura e poeira.

**§ 1º** O acesso físico aos locais de armazenamento deve ser restrito e controlado, permitindo o ingresso unicamente a pessoas previamente autorizadas pelo Administrador de Backup e pela unidade técnica responsável pela infraestrutura de TIC do Ministério dos Transportes.

**§ 2º** Os limites de temperatura, umidade e pressão nos locais de armazenamento de mídias físicas devem ser aqueles detalhados e exigidos pelo fabricante das respectivas unidades de armazenamento, garantindo a longevidade e a integridade dos backups.

#### CAPÍTULO VI — DOS TESTES DE RESTAURAÇÃO E VALIDAÇÃO

**Art. 49.** A efetividade e a integridade dos backups serão validadas por meio de procedimentos documentados, conforme os seguintes requisitos mínimos:

I - os registros de auditoria (logs) de execução do backup deverão ser revisados periodicamente em busca de erros, falhas de hardware e durações anormais de processamento, visando à identificação de oportunidades para aprimorar o desempenho e a estabilidade do processo de backup;

II - ações corretivas deverão ser adotadas e registradas quando os problemas de backup forem identificados, a fim de reduzir os riscos associados a backups com falha;

III - a unidade técnica responsável pela infraestrutura de TIC do Ministério dos Transportes manterá registros históricos detalhados de todas as execuções de backups e dos respectivos testes de restauração, demonstrando a plena conformidade com as diretrizes e os requisitos técnicos desta Norma;

IV - os testes de restauração devem ser realizados com base em critérios de risco, considerando a criticidade do sistema de origem, a natureza dos dados e o tipo de backup, conforme definido no Plano de Backup e Restauração de Dados Digitais;

V - a periodicidade, a abrangência, os procedimentos e as rotinas inerentes aos testes de restauração dos backups deverão constar do Plano de Backup e Restauração de Dados Digitais; e

VI - os backups deverão ser validados quanto à integridade nos termos do Plano de Backup e Restauração de Dados Digitais.

**Art. 50.** Os testes de restauração dos backups devem ser realizados, sempre que tecnicamente viável e observados os recursos humanos e tecnológicos disponíveis, em equipamentos servidores diferentes daqueles que atendem aos ambientes de produção.

#### CAPÍTULO VII — DOS PROCEDIMENTOS DE RESTAURAÇÃO DE BACKUP

**Art. 51.** O atendimento de solicitações de restauração de arquivos, e-mails ou quaisquer outras formas de dados digitais deve obedecer às seguintes orientações procedimentais, visando à rastreabilidade e à segurança:

I - a solicitação de restauração de objetos de informação deverá sempre partir do Gestor da Informação, ou de seu preposto formalmente designado, mediante abertura de chamado técnico, utilizando a ferramenta de controle de atendimentos oficial disponibilizada pela área de TIC;

II - o chamado técnico de solicitação deverá conter, de forma obrigatória, no mínimo, o nome completo e o setor do usuário solicitante, a identificação precisa do(s) objeto(s) a ser(em) recuperado(s), a localização original em que o objeto se encontrava, a data exata da versão que se deseja recuperar, o local alternativo para armazenamento temporário do(s) objeto(s) restaurado(s) e, quando for o caso, a justificativa formal para a restauração do dado;

III - a restauração dos objetos de informação somente será técnica e legalmente possível quando a informação solicitada estiver contemplada e protegida pela estratégia de backup definida no Plano de Backup e Restauração de Dados Digitais; e

IV - o Administrador de Backup poderá submeter à unidade técnica responsável pela infraestrutura de TIC do Ministério dos Transportes as solicitações de restauração que apresentem indícios de desconformidade com a atividade institucional, com os requisitos de segurança da informação ou com as finalidades autorizadas, cabendo à unidade técnica emitir decisão fundamentada sobre o atendimento da solicitação.

**Art. 52.** Os arquivos e pastas que forem objeto de solicitações de restauração serão disponibilizados em mídia ou localização diversa daquela em que foram originalmente armazenados (ambiente de produção), com o objetivo de assegurar que, antes de seu uso ou de sua cópia de retorno para a mídia de origem, sua integralidade seja verificada e seja evitada a sobreposição indesejada ou acidental de dados.

**Art. 53.** Caberá ao Operador de Backup executar os testes de restauração de dados de backup, conforme a periodicidade, a abrangência e os procedimentos estabelecidos no Plano de Backup e Restauração de Dados Digitais, com apoio técnico do Administrador de Backup, de modo a averiguar de forma contínua a integridade dos arquivos copiados e a funcionalidade do processo de restauração.

**Parágrafo único.** Os testes de restauração previstos no caput deverão ser documentados formalmente por meio de relatório específico, contendo, no mínimo, a descrição dos dados envolvidos, a data de realização do teste, o tempo gasto na restauração, o resultado obtido e a confirmação da integridade e da completude dos dados restaurados.

**Art. 54.** As restaurações de imagens completas de servidores críticos e de bases de dados críticas (restauração de desastre) somente poderão ser demandadas e executadas com a expressa e formal autorização da unidade técnica responsável pela infraestrutura de TIC do Ministério dos Transportes, após avaliação da necessidade técnica, da oportunidade estratégica e da conveniência administrativa da ação de restauração.

#### CAPÍTULO VIII — DAS ATRIBUIÇÕES

**Art. 55.** A SGETI, por meio da unidade técnica responsável pela infraestrutura de TIC, é a unidade central responsável pela gestão da infraestrutura necessária às rotinas de backup e restauração, pela definição das diretrizes técnicas e de segurança envolvidas e pela fiscalização do cumprimento desta Norma.

**Art. 56.** O Administrador de Backup deverá possuir formação técnica ou capacitação profissional compatível com suas atribuições e deverá ser formalmente designado pela unidade técnica responsável pela infraestrutura de TIC do Ministério dos Transportes.

**Art. 57.** O Operador de Backup deverá ser designado pelo Administrador de Backup, mediante a aprovação formal da unidade técnica responsável pela infraestrutura de TIC do Ministério dos Transportes, devendo ser um agente com conhecimento técnico operacional adequado.

**Art. 58.** É dever da unidade técnica responsável pela infraestrutura de TIC do Ministério dos Transportes zelar para que o Administrador de Backup e o Operador de Backup estejam capacitados e mantenham conhecimento atualizado sobre as tecnologias, os procedimentos e as soluções utilizadas nas rotinas de armazenamento e backup.

**Art. 59.** Sem prejuízo de outras estabelecidas em regulamentos, são atribuições do Administrador de Backup:

I - consolidar, formalizar e manter atualizados, em conjunto com os Gestores da Informação, os Planos de Backup e Restauração de Dados Digitais;

II - propor soluções de backup das informações digitais corporativas produzidas ou custodiadas pelo Ministério dos Transportes;

III - providenciar a criação, a manutenção e o monitoramento contínuo dos backups, garantindo sua fidelidade;

IV - configurar as soluções de backup;

V - manter as unidades de armazenamento de backups preservadas, funcionais e seguras;

VI - definir os procedimentos de restauração de backups;

VII - verificar os eventos gerados pela solução de backup, tomando as providências necessárias para remediação de eventuais falhas;

VIII - tomar medidas de natureza preventiva para evitar falhas sistêmicas ou operacionais nos processos de backup;

IX - reportar imediatamente à unidade técnica responsável pela infraestrutura de TIC do Ministério dos Transportes ou à autoridade hierárquica competente os incidentes ou erros que causem indisponibilidade ou impossibilitem a execução ou restauração eficaz das cópias de segurança;

X - gerenciar registros de auditoria (logs) e alertas técnicos gerados pela execução dos backups;

XI - disponibilizar informações e relatórios que subsidiem as decisões gerenciais referentes à gestão de capacidade de armazenamento relacionada aos backups;

XII - propor modificações visando ao aperfeiçoamento da Norma de Backup e Restauração de Dados Digitais; e

XIII - providenciar e acompanhar a execução dos testes de restauração.

**Art. 60.** Sem prejuízo de outras estabelecidas em regulamentos, são atribuições do Operador de Backup:

I - executar a restauração de dados a partir de backups em caso de necessidade, mediante solicitação formal aprovada nos termos do art. 51 desta Norma;

II - operar e manusear as unidades de armazenamento de backups;

III - informar prontamente ao Administrador de Backup sobre qualquer problema, falha ou anomalia que impossibilite a criação adequada ou a restauração integral de um backup; e

IV - executar e documentar os procedimentos de testes de restauração de backup conforme as diretrizes e a periodicidade estabelecida nos Planos de Backup e Restauração de Dados Digitais.

**Art. 61.** Sem prejuízo de outras estabelecidas em regulamentos, são atribuições da unidade técnica responsável pela infraestrutura de TIC do Ministério dos Transportes:

I - acompanhar a criação e a atualização dos Planos de Backup e Restauração de Dados Digitais;

II - gerenciar e acompanhar as solicitações de restaurações de dados, garantindo que haja a anuência prévia e formal do Gestor da Informação;

III - esclarecer dúvidas de natureza técnica do Administrador de Backup acerca da complexidade e dos requisitos tecnológicos das informações salvaguardadas; e

IV - validar tecnicamente o resultado das restaurações realizadas e a eficácia dos relatórios dos testes de restauração dos backups.

**Art. 62.** Sem prejuízo de outras estabelecidas em regulamentos, são atribuições inerentes aos Gestores da Informação:

I - contribuir para a definição do escopo, dos requisitos de negócio e da criticidade das informações e dados sob sua responsabilidade, para fins de elaboração dos Planos de Backup e Restauração de Dados Digitais;

II - solicitar, de modo formal e documentado, a salvaguarda das informações e dados geridos sob sua responsabilidade e conceder a anuência formal às solicitações de restauração de dados;

III - validar, sob o aspecto negocial e funcional, o resultado das restaurações solicitadas, atestando a integridade e a completude do dado restaurado; e

IV - validar, sob o aspecto negocial e funcional, o resultado dos testes periódicos de restauração dos backups, garantindo que o dado restaurado atenda aos requisitos de negócio.

#### CAPÍTULO IX — DAS DISPOSIÇÕES FINAIS E TRANSITÓRIAS

**Art. 63.** A lista dos sistemas de informação submetidos a backup e os respectivos Planos de Backup e Restauração de Dados Digitais deverão ser mantidos atualizados sempre que houver alteração de escopo, criticidade ou tecnologia, e formalmente revisados, no mínimo, a cada 12 (doze) meses.

**Art. 64.** Os Planos de Backup e Restauração de Dados Digitais dos novos sistemas deverão ser elaborados, implementados e validados previamente à entrada em produção, admitida, excepcionalmente, justificativa formal para adequação posterior em prazo definido pela SGETI.

**Parágrafo único.** Os sistemas legados que não possuam Plano de Backup e Restauração de Dados Digitais formalizados deverão ter seus planos elaborados no prazo máximo de 24 (vinte e quatro) meses, considerada a complexidade técnica, a criticidade operacional e a necessidade de continuidade dos serviços associados.

**Art. 65.** Esta Norma de Backup e Restauração de Dados Digitais deverá ser objeto de conscientização contínua no âmbito do Ministério dos Transportes, cabendo à Subsecretaria de Gestão Estratégica, Tecnologia e Inovação (SGETI) promover ações permanentes de divulgação e conscientização sobre as responsabilidades dos usuários quanto ao armazenamento adequado dos dados.

**Art. 66.** Esta Norma poderá ser revisada pela Subsecretaria de Gestão Estratégica, Tecnologia e Inovação (SGETI), a qualquer tempo, para fins de atualização, quando identificada a necessidade de alteração em qualquer de seus dispositivos.

**Art. 67.** Os casos omissos serão dirimidos pela Subsecretaria de Gestão Estratégica, Tecnologia e Inovação (SGETI), que poderá expedir normas complementares e disponibilizar informações adicionais em meio eletrônico, mediante aprovação do Comitê de Governança Digital e Segurança da Informação (CGDSI).

**Art. 68.** Fica revogada, no âmbito do Ministério dos Transportes, a Resolução SE/MINFRA nº 2.048, de 8 de março de 2022.

**Art. 69.** Esta Portaria entra em vigor na data de sua publicação.

GEORGE SANTORO
