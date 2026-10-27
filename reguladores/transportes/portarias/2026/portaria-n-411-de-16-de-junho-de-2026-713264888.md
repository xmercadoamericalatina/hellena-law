---
titulo: "PORTARIA Nº 411, DE 16 DE JUNHO DE 2026"
orgao: "Ministério dos Transportes/Gabinete do Ministro"
tipo: "Portaria"
numero: "411"
data: 2026-06-16
revogada: false
versao_texto: "publicação original"
publicacao: "DOU de 18/06/2026, seção 1, p. 208"
data_publicacao: 2026-06-18
edicao: "112"
fonte: "https://www.in.gov.br/web/dou/-/portaria-n-411-de-16-de-junho-de-2026-713264888"
baixado_em: 2026-10-15
---
# PORTARIA Nº 411, DE 16 DE JUNHO DE 2026

PORTARIA Nº 411, DE 16 DE JUNHO DE 2026

Institui a Norma de Gestão de Controle de Acesso no âmbito do Ministério dos Transportes.

O MINISTRO DE ESTADO DOS TRANSPORTES, no uso das atribuições que lhe confere o art. 87, parágrafo único, incisos I e II da Constituição, o Decreto nº 11.360, de 1º de janeiro de 2023, o art. 2º do Decreto nº 12.198, de 24 de setembro de 2024, e considerando o disposto no art. 3º, caput, inciso III do Decreto nº 7.579, de 11 de outubro de 2011, na Instrução Normativa GSI/PR nº 1, de 27 de maio de 2020, e no processo nº 50000.022596/2025-33, resolve:

#### CAPÍTULO I — DAS DISPOSIÇÕES PRELIMINARES

##### Seção I — Dos Objetivos

**Art. 1º** Fica aprovada, no âmbito do Ministério dos Transportes, a Norma de Gestão de Controle de Acesso, que estabelece princípios, diretrizes e responsabilidades para a proteção da confidencialidade, integridade e disponibilidade das informações e dos recursos institucionais, em complemento à Política de Segurança da Informação - POSIN do Ministério dos Transportes - MT.

**Art. 2º** A presente Norma tem por objetivo estabelecer controles de identificação, autenticação e autorização para salvaguardar as informações e ativos do Ministério dos Transportes - MT, estejam em meio digital ou físico, a fim de prevenir acessos não autorizados que possam ocasionar destruição, alteração, perda, roubo ou divulgação indevida.

**Art. 3º** São objetivos específicos desta Norma:

I - assegurar que todos os acessos sejam concedidos conforme necessidade de uso e função;

II - adotar o princípio do menor privilégio em todas as concessões de acesso;

III - garantir a confidencialidade, integridade e disponibilidade das informações sob custódia do MT;

IV - definir procedimentos para concessão, manutenção, revisão e revogação de credenciais; e

V - disciplinar o uso de acessos especiais ou privilegiados, prevenindo riscos de abuso, fraude ou erro não detectado.

##### Seção II — Das Definições

**Art. 4º** Para fins desta Norma, adotam-se as definições constantes:

I - do Glossário de Segurança da Informação do Gabinete de Segurança Institucional da Presidência da República, aprovado pela Portaria GSI/PR nº 93, de 18 de outubro de 2021;

II - da Política de Segurança da Informação do Ministério dos Transportes (POSIN), instituída pela Portaria MT nº 287, de 4 de abril de 2025; e

III - dos conceitos específicos de Controle de Acesso previstos no Modelo de Política de Gestão de Controle de Acesso da Secretaria de Governo Digital.

**Art. 5º** Para os fins desta Portaria, consideram-se:

I - Acesso - ato de ingressar, transitar, conhecer ou consultar informação, bem como usar ativos de informação, observadas as restrições aplicáveis;

II - Conta de Serviço - credencial destinada a procedimentos automáticos (aplicações, scripts, rotinas), sem intervenção humana direta;

III - Controle de Acesso - conjunto de procedimentos, recursos e meios empregados para conceder, restringir ou bloquear o uso de ativos físicos ou computacionais; e

IV - Multifactor Authentication - MFA - autenticação multifatores, baseada em dois ou mais elementos distintos (algo que o usuário sabe, possui ou é).

#### CAPÍTULO II — ACESSO LÓGICO

**Art. 6º** O acesso lógico aos recursos do Ministério dos Transportes será realizado por meio de sistema centralizado de controle de acesso, administrado pela área de Tecnologia da Informação - TI, com base nas responsabilidades e tarefas atribuídas a cada usuário.

**Art. 7º** Terão direito de acesso lógico os servidores efetivos, ocupantes de cargo em comissão, empregados públicos, estagiários, terceirizados e demais colaboradores temporários em atividade no MT; e

**Art. 8º** O acesso remoto será realizado por meio de rede privada virtual - VPN ou tecnologia equivalente, com uso obrigatório de MFA.

**Art. 9º** A área de TI deverá manter inventário atualizado de todas as contas (usuários, administrativas, de teste e de serviço).

**§ 1º** Para as contas de serviço, o inventário deverá registrar, no mínimo:

I - unidade proprietária;

II - responsável pela autorização do acesso;

III - data de criação ou última renovação de autorização; e

IV - ativo ou sistema vinculado.

**§ 2º** Todas as contas deverão ser validadas, no mínimo, a cada 90 (noventa) dias pela área de TI.

**Art. 10.** A gestão de contas será centralizada por meio de serviço de diretório e/ou identidade, integrando autenticação, autorização e auditoria (AAA) dos ativos de informação.

**Art. 11.** A área de TI manterá inventário dos sistemas de autenticação e autorização da organização, com revisão periódica para assegurar conformidade e atualização.

**Art. 12.** O controle de acesso será baseado em funções - Role Based Access Control - RBAC, garantindo que os privilégios concedidos sejam compatíveis com as atividades de cada função.

**§ 1º** A área de TI realizará análises periódicas de aderência dos acessos concedidos, sempre que houver criação ou alteração de funções e ativos relevantes.

**§ 2º** O acesso deverá obedecer ao Princípio do Menor Privilégio, concedendo-se apenas as permissões estritamente necessárias.

**Art. 13.** É vedado conceder permissões conflitantes a um mesmo usuário.

**§ 1º** A área de TI deverá implementar controles de Segregação de Funções - Segregation of Duties - SoD, de modo a evitar conflitos de interesse, ações fraudulentas ou erros não detectados.

**§ 2º** Exceções deverão ser formalmente justificadas, registradas e acompanhadas por controles compensatórios.

#### CAPÍTULO III — CONTA DE ACESSO LÓGICO E SENHA

**Art. 14.** A criação de conta de acesso (login único) será provida pela área de TI, mediante solicitação formal da unidade do requisitante.

**§ 1º** Os privilégios de acesso serão definidos pela unidade de lotação do usuário, limitando-se às atividades estritamente necessárias.

**§ 2º** Solicitações de perfis diferenciados deverão ser formalizadas pela chefia imediata e serão avaliadas pela TI, que poderá negá-las se entender não justificadas.

**Art. 15.** O login e a senha são de uso pessoal e intransferível, sendo vedada sua divulgação. O descumprimento ensejará o bloqueio imediato da conta, devendo a unidade requisitante formalizar nova solicitação para restabelecimento.

**Art. 16.** A liberação do login ficará condicionada à assinatura, pelo usuário, do Termo de Responsabilidade, a ser juntado eletronicamente ao processo de criação da conta, com assinatura digital que assegure fé pública, nos termos da legislação vigente.

**Art. 17.** O padrão de criação do login adotará o formato primeiro nome + ponto + último nome (ex.: joao.silva), garantindo a utilização do nome social quando aplicável.

**Parágrafo único.** Havendo duplicidade, a TI adotará outra combinação com base no nome completo/social.

**Art. 18.** As senhas de acesso deverão observar os seguintes requisitos mínimos:

I - comprimento mínimo de 8 caracteres para contas com MFA habilitado e 14 caracteres para contas sem MFA;

II - uso de letras maiúsculas, minúsculas, números e caracteres especiais;

III - proibição de sequências óbvias (numéricas, alfabéticas), nomes próprios, datas, apelidos ou termos de fácil dedução;

IV - proibição de termos comuns como "Brasil", "senha", "usuario", "password" ou equivalentes;

V - não reutilização das últimas 3 (três) senhas; e

VI - fornecimento, pela TI, de senha inicial temporária, que deverá ser obrigatoriamente alterada pelo usuário no primeiro acesso.

**Art. 19.** As senhas deverão ser renovadas a cada 90 (noventa) dias, sendo o usuário notificado previamente.

**Parágrafo único.** O não cumprimento do prazo acarretará bloqueio automático da conta até a definição de nova senha.

#### CAPÍTULO IV — BLOQUEIO, DESBLOQUEIO E CANCELAMENTO DA CONTA DE ACESSO

**Art. 20.** A conta de acesso será bloqueada nos seguintes casos:

I - após 5 (cinco) tentativas consecutivas de autenticação inválida;

II - por solicitação formal do superior imediato do usuário, devidamente justificada;

III - quando houver suspeita de mau uso, descumprimento da Política de Segurança da Informação - POSIN ou de normas correlatas em vigor; e

IV - após 45 (quarenta e cinco) dias consecutivos de inatividade.

**Art. 21.** O desbloqueio da conta somente será realizado mediante solicitação formal da chefia imediata à área de Tecnologia da Informação.

**Art. 22.** Nos casos de afastamento temporário (licença, cessão ou afastamento equivalente), a unidade de lotação deverá solicitar o bloqueio preventivo da conta do usuário.

**Art. 23.** As contas de acesso que permanecerem sem uso por 180 (cento e oitenta) dias serão canceladas, sem prejuízo da preservação de registros para auditoria.

**Art. 24.** A TI deverá configurar o bloqueio automático de sessão nos ativos do MT após período de inatividade previamente estabelecido, variável conforme o risco associado ao ativo.

**Art. 25.** O processo de revogação e desativação de contas deverá ser priorizado pela TI, garantindo a preservação de dados e registros de log para eventuais auditorias.

#### CAPÍTULO V — DOS CONTROLES DE ACESSOS FÍSICOS E DO AMBIENTE

**Art. 26.** O controle de acesso físico tem por objetivo assegurar a proteção de pessoas, informações e ativos do MT, permitindo acesso apenas a pessoas devidamente autorizadas.

**§ 1º** Devem ser definidos perímetros de segurança, de acordo com a criticidade das informações e ativos neles contidos.

**§ 2º** O acesso a áreas sensíveis será realizado por meio de mecanismos de autenticação (crachá, senha, PIN, biometria), complementados por barreiras físicas.

**§ 3º** Os mecanismos de controle de acesso devem ser monitorados por equipe ou sistema responsável, com registros de entrada e saída.

**§ 4º** O monitoramento deve ser contínuo por meio de sistemas de vigilância e alarmes, especialmente em áreas críticas como datacenters, salas técnicas e locais de armazenamento de documentos sigilosos.

**§ 5º** Visitantes e prestadores de serviço deverão ter acesso supervisionado durante todo o período de permanência.

**§ 6º** Os perímetros definidos deverão ser revistos periodicamente, com base em avaliação de risco.

**§ 7º** Quando implementada, a conta de acesso biométrico deverá estar vinculada a uma conta de acesso lógico, sendo ambas utilizadas de forma combinada, em atendimento ao conceito de autenticação multifator.

**§ 8º** Os dados biométricos deverão ser tratados como informações sigilosas, preferencialmente por meio de criptografia, em conformidade com a legislação vigente.

**Art. 27.** O acesso físico a ambientes críticos, como datacenters, salas técnicas ou arquivos que contenham informações classificadas, será restrito a pessoal autorizado, com base em gestão formal de permissões, que deve prever:

I - provisão, revisão, atualização e revogação periódica de acessos;

II - uso de crachá específico para áreas restritas; e

III - autorização especial para ingresso fora do expediente, mediante registro junto à segurança e confirmação da Administração.

**Art. 28.** O MT deverá implementar e manter registros de todos os acessos físicos a ambientes e ativos de informação, garantindo sua integridade e disponibilidade para fins de auditoria.

**§ 1º** As áreas e instalações que contenham documentos classificados em qualquer grau de sigilo, ou que demandem proteção em razão de sua utilização ou finalidade, terão acesso restrito a pessoas autorizadas e serão protegidas por sistemas de segurança.

**§ 2º** O ingresso em áreas de acesso restrito será permitido apenas a pessoas portadoras de crachá específico.

**§ 3º** O acesso extraordinário, realizado fora do horário de expediente, em sábados, domingos ou feriados, deverá ocorrer pela entrada principal do edifício, mediante identificação junto ao vigilante de plantão e confirmação da autorização pela Administração.

**Art. 29.** O acesso de fornecedores e prestadores de serviços a ambientes ou ativos críticos somente será permitido quando:

I - houver finalidade específica e autorizada;

II - houver autorização formal da área responsável pelo ativo; e

III - o acesso for acompanhado e monitorado por responsável autorizado.

**Art. 30.** Os ativos de informação do MT que se encontrem fora de suas dependências devem ser protegidos contra perda, roubo, dano e acesso não autorizado, observando-se as seguintes diretrizes:

I - não deixar o ativo sem vigilância em locais públicos ou inseguros;

II - adotar medidas contra exposição visual indevida de informações; e

III - habilitar funcionalidades de rastreamento e limpeza remota.

**Art. 31.** Documentos físicos contendo informações classificadas ou sensíveis, nos termos da Lei nº 12.527/2011 e do Decreto nº 7.724/2012, devem ser armazenados em armários ou cofres dotados de fechadura e localizados em ambientes com acesso restrito.

**Art. 32.** Reuniões que envolvam informações classificadas ou sensíveis deverão ocorrer em salas controladas, vedada a utilização de dispositivos de gravação ou comunicação sem autorização da autoridade competente.

**Art. 33.** O tratamento de dados biométricos, quando utilizado para controle de acesso, deverá atender às seguintes diretrizes:

I - a autenticação biométrica deverá estar vinculada à conta lógica do usuário, compondo MFA; e

II - os dados biométricos serão tratados como informações sigilosas, com armazenamento preferencial em formato criptografado, em conformidade com a legislação vigente.

**§ 1º** Toda informação produzida, manuseada, armazenada, transportada ou custodiada pelo órgão constitui bem institucional e será protegida e gerenciada de acordo com as normas vigentes.

**§ 2º** A informação classificada nos termos do art. 24 da Lei nº 12.527/2011, será tratada conforme regulamentação específica.

**§ 3º** A destinação final de informações institucionais observará as políticas, normas, procedimentos internos, classificação arquivística, classificação de sigilo e a temporalidade prevista na legislação aplicável.

**Art. 34.** O descarte de documentos físicos que contenham informações sensíveis ou sigilosas deve ser realizado de forma segura e irrecuperável, utilizando métodos como trituração, fragmentação ou incineração, sendo recomendável a rastreabilidade do processo por meio de registro documental.

**Art. 35.** A supervisão da gestão dos controles de acesso físico caberá à unidade responsável pela Segurança da Informação, que deverá realizar auditorias periódicas para verificar a conformidade com esta Norma.

#### CAPÍTULO VI — MOVIMENTAÇÃO INTERNA

**Art. 36.** Sempre que houver mudança de lotação ou de função do usuário, os acessos anteriormente concedidos deverão ser imediatamente revogados, mediante solicitação da chefia da unidade de origem ou da Coordenação-Geral de Gestão de Pessoas.

**Art. 37.** A nova chefia imediata ou a Coordenação-Geral de Gestão de Pessoas deverá formalizar a solicitação de novos acessos, compatíveis com as atribuições do cargo ou função assumida.

**Art. 38.** Não será permitido o acúmulo de acessos anteriores com os da nova função, devendo os direitos antigos ser cancelados antes da liberação dos novos.

#### CAPÍTULO VII — AUTENTICAÇÃO MULTIFATORES

**Art. 39.** Para autenticação no âmbito do Ministério dos Transportes, deverá ser adotada a Autenticação Multifatores - MFA, combinando ao menos dois elementos distintos dentre:

I - algo que o usuário sabe (senha ou frase de segurança);

II - algo que o usuário possui (certificado digital, token, código enviado por SMS, e-mail ou aplicativo específico);

III - algo que o usuário é (biometria); e

IV - local de acesso (rede interna do MT), como fator adicional de contexto.

**Parágrafo único.** Para acessos remotos, não poderá ser utilizado o fator "local de acesso" isoladamente.

**Art. 40.** O uso de MFA é obrigatório nos casos de:

I - acesso remoto à Rede Local do MT, em modelo de segurança baseado em Confiança Zero - Zero Trust;

II - acesso a todas as aplicações corporativas ou de terceiros hospedadas externamente; e

III - utilização de contas com privilégios de administrador.

**Art. 41.** A autenticação biométrica, quando utilizada, deverá ser vinculada a uma conta lógica, compondo o MFA, e os respectivos dados biométricos deverão ser tratados como informações sigilosas, preferencialmente armazenados de forma criptografada, em conformidade com a legislação vigente.

#### CAPÍTULO VIII — GESTÃO DE ACESSO PRIVILEGIADO

**Art. 42.** As contas com privilégios de administrador somente serão concedidas a técnicos da TI devidamente autorizados, e exclusivamente para a execução de tarefas específicas de administração de ativos de informação.

**Art. 43.** O uso de login com privilégios de administrador deve ter prazo determinado e ser formalmente solicitado pela chefia imediata.

**Art. 44.** É vedada a utilização da conta de administrador para atividades gerais, como navegação na internet, e-mail ou uso de aplicativos de produtividade, devendo essas atividades ser realizadas a partir da conta primária não privilegiada do usuário.

**Art. 45.** Não será concedida, para um mesmo usuário, conta de administrador simultânea em mais de uma estação de trabalho, servidor ou dispositivo de rede, salvo em situações excepcionais devidamente justificadas.

**Art. 46.** Contas de administrador temporárias poderão ser concedidas a visitantes ou prestadores de serviço, mediante apreciação da área responsável pela gestão de acessos e sempre com prazo definido.

**Art. 47.** Constatada irregularidade no uso, o privilégio de administrador será imediatamente revogado, sem possibilidade de renovação automática.

**Art. 48.** A área de TI deverá implementar práticas de Gestão de Acesso Privilegiado - Privileged Access Management - PAM, incluindo, no mínimo:

I - concessão de privilégios temporários e granulares, conforme a necessidade da atividade;

II - restrição do número de usuários com contas privilegiadas;

III - auditoria e monitoramento contínuo das ações realizadas por contas administrativas;

IV - eliminação, sempre que possível, de privilégios permanentes; e

V - observância do princípio do menor privilégio também para contas administrativas.

#### CAPÍTULO IX — RESPONSABILIDADES

**Art. 49.** Cabe à chefia imediata do usuário comunicar formalmente à Coordenação-Geral de Gestão de Pessoas e à área de TI o desligamento, afastamento ou saída do colaborador, servidor ou estagiário, para que os acessos sejam bloqueados ou cancelados de forma imediata.

**Art. 50.** Compete à área de Tecnologia da Informação - TI:

I - monitorar o uso da Rede Local, dos serviços de internet e demais recursos tecnológicos;

II - investigar suspeitas de mau uso ou de incidentes de segurança, adotando medidas preventivas, inclusive bloqueio imediato de contas ou estações de trabalho até a elucidação do caso;

III - manter processos de auditoria periódica sobre concessão, manutenção e revogação de acessos; e

IV - preservar logs e registros relacionados ao uso de contas e acessos, observada a legislação vigente.

**Art. 51.** Compete aos usuários:

I - zelar pela confidencialidade de suas credenciais, sendo vedado o compartilhamento de senha;

II - responsabilizar-se por todos os acessos realizados com sua conta;

III - bloquear ou encerrar sessão sempre que se ausentar de sua estação de trabalho;

IV - não utilizar simultaneamente a mesma conta em mais de um dispositivo, salvo quando autorizado;

V - utilizar corretamente os equipamentos de informática, observando os cuidados preventivos definidos pelo MT;

VI - comunicar imediatamente à TI qualquer situação que configure violação de sigilo, uso indevido ou risco à segurança da informação; e

VII - assinar o Termo de Responsabilidade.

#### CAPÍTULO X — DAS DISPOSIÇÕES FINAIS

**Art. 52.** Todo incidente que comprometa ou possa comprometer a Segurança da Informação deverá ser imediatamente comunicado à Equipe de Tratamento e Resposta a Incidentes Cibernéticos - ETIR/MT, por meio do endereço eletrônico etir.mt@transportes.gov.br ou outro canal oficial disponibilizado.

**Art. 53.** Quando houver suspeita de quebra de segurança que exponha a risco os serviços ou ativos tecnológicos do MT, a Subsecretaria de Gestão Estratégica, Tecnologia e Inovação - SGETI poderá determinar a interrupção temporária do serviço afetado, sem necessidade de prévia autorização, para fins de investigação.

**§ 1º** Se o incidente envolver usuário do MT, a SGETI comunicará o fato à chefia imediata para adoção das medidas cabíveis.

**§ 2º** As violações a esta Norma e à POSIN sujeitam os infratores a responsabilidade civil, penal e administrativa, podendo ser instaurado processo administrativo disciplinar - PAD, quando aplicável.

**§ 3º** Casos omissos ou não previstos serão deliberados pelo Comitê de Governança Digital e Segurança da Informação do MT.

**Art. 54.** Esta Portaria entra em vigor na data de sua publicação.

GEORGE SANTORO
