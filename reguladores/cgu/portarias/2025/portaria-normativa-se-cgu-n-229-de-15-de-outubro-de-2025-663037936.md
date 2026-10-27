---
titulo: "PORTARIA NORMATIVA SE/CGU Nº 229, DE 15 DE OUTUBRO DE 2025"
orgao: "Controladoria-Geral da União/Secretaria Executiva"
tipo: "Portaria"
numero: "229"
data: 2025-10-15
revogada: null
versao_texto: "publicação original"
publicacao: "DOU de 16/10/2025, seção 1, p. 443"
data_publicacao: 2025-10-16
edicao: "198"
fonte: "https://www.in.gov.br/web/dou/-/portaria-normativa-se/cgu-n-229-de-15-de-outubro-de-2025-663037936"
baixado_em: 2026-10-16
sha256_html_fonte: ce5586586b50cd42e52e434069238a1de52727dddd812f1f09810186a0b64d03
---
# PORTARIA NORMATIVA SE/CGU Nº 229, DE 15 DE OUTUBRO DE 2025

PORTARIA NORMATIVA SE/CGU Nº 229, DE 15 DE OUTUBRO DE 2025

Institui a Política de Gerenciamento de Configuração Segura de Dispositivos e Softwares Corporativos no âmbito da Controladoria-Geral da União.

A SECRETÁRIA-EXECUTIVA DA CONTROLADORIA-GERAL DA UNIÃO, no exercício das atribuições previstas no art. 35 do Anexo I do Decreto nº 11.330, de 1º de janeiro de 2023, e no art. 5º, caput, inciso II, da Portaria Normativa CGU nº 164, de 30 de agosto de 2024 , e tendo em vista o disposto no Decreto nº 12.572, de 4 de agosto de 2025, no Decreto nº 12.069, de 21 de junho de 2024 , na Portaria SE/CGU nº 587, de 10 de março de 2021 , e na Instrução Normativa GSI/PR nº 3, de 28 de maio de 2021, bem como o que consta no Processo Administrativo nº 00190.106635/2025-96, resolve:

#### CAPÍTULO I — DISPOSIÇÕES PRELIMINARES

**Art. 1º** Esta Portaria Normativa institui a Política de Gerenciamento de Configuração Segura de Dispositivos e Softwares Corporativos e estabelece princípios, diretrizes e responsabilidades relacionadas à configuração segura de dispositivos e softwares corporativos no âmbito da Controladoria-Geral da União.

**Art. 2º** Para os efeitos desta Portaria Normativa, considera-se:

I - dispositivos corporativos - dispositivos de usuário final, incluindo portáteis e móveis, dispositivos de rede, servidores e dispositivos não computacionais relativos à internet das coisas conectados ou integrados aos ambientes tecnológicos da Controladoria-Geral da União e que estejam sob gestão direta ou indireta da área de tecnologia da informação;

II - softwares corporativos - sistemas operacionais, aplicações, plataformas e serviços de nuvem; e

III - hardening - processo de mapeamento das ameaças, mitigação de riscos e execução de atividades corretivas, com foco em infraestrutura, com o objetivo principal de torná-la mais resiliente a tentativas de ataques cibernéticos;

**Parágrafo único.** Na aplicação desta Portaria Normativa, deverão ser observados, no que couber, os conceitos constantes do Glossário de Segurança da Informação aprovado pela Portaria GSI/PR nº 93, de 18 de outubro de 2021.

##### Seção I — Objetivo

**Art. 3º** O objetivo da Política de Gerenciamento de Configuração Segura de Dispositivos e Softwares Corporativos é instituir princípios e responsabilidades no gerenciamento de configuração segura de dispositivos e softwares corporativos para identificar, aplicar e manter configurações seguras durante toda a vida útil dos ativos e serviços da Controladoria-Geral da União.

##### Seção II — Abrangência

**Art. 4º** As disposições desta Portaria Normativa e da regulamentação correlata aplicam-se:

I - aos dispositivos e softwares corporativos da Controladoria-Geral da União; e

II - aos agentes públicos e terceiros responsáveis pelo planejamento, implementação, monitoramento ou modificação das configurações seguras dos dispositivos e softwares corporativos da Controladoria-Geral da União.

**Parágrafo único.** As disposições desta Portaria Normativa não se aplicam a softwares desenvolvidos internamente pela Controladoria-Geral da União.

##### Seção III — Regime de excepcionalidade

**Art. 5º** Os dispositivos e softwares corporativos da Controladoria-Geral da União que, por dificuldades técnicas ou obrigações contratuais e normativas, não estejam contemplados em algum requisito desta política serão tratados de forma excepcional.

**§1º** As excepcionalidades a esta política deverão ser aprovadas e registradas pela área de segurança cibernética da Diretoria de Tecnologia da Informação da Secretaria Executiva.

**§2º** No registro da excepcionalidade deve constar a justificativa da excepcionalidade, os riscos em não se aplicar a configuração de segurança, bem como mitigações específicas que possam ser implementadas.

#### CAPÍTULO II — DOS PRINCÍPIOS GERAIS

**Art. 6º** A Política de que trata esta Portaria Normativa observará os princípios e os objetivos da Política Nacional de Segurança da Informação, instituída pelo Decreto nº 12.572, de 4 de agosto de 2025, e estará alinhada à Política de Segurança da Informação da Controladoria-Geral da União, prevista na Portaria SE/CGU nº 587, de 10 de março de 2021, e aos preceitos da Lei nº 13.709, de 14 de agosto de 2018 (Lei Geral de Proteção de Dados Pessoais).

**Art. 7º** As diretrizes de configuração segura devem ser selecionadas com base nos requisitos de hardening fornecidos pelo fabricante ou nos padrões do setor.

**Parágrafo único.** Se as diretrizes de configuração não estiverem disponíveis para uma tecnologia específica, a Diretoria de Tecnologia da Informação deverá definir um modelo de configuração segura para essa tecnologia antes de usá-la.

**Art. 8º** Dispositivos e softwares corporativos da Controladoria-Geral da União devem ser configurados apropriadamente, atendendo aos requisitos de segurança para seu propósito organizacional, observado o seguinte:

I - as contas padrão fornecidas com dispositivos e softwares corporativos, como conta raiz, de administrador e outras contas de fornecedores pré-configuradas, devem ser apropriadamente reconfiguradas para prevenir acesso não autorizado;

II - as expirações automáticas de sessão por inatividade devem ser configuradas para dispositivos e softwares corporativos onde suportadas, adotando-se como referência o período de até quinze minutos para sistemas operacionais e de até dois minutos para dispositivos móveis de usuários finais, admitindo-se prazos distintos mediante justificativa técnica e análise de risco aprovada pela Diretoria de Tecnologia da Informação da Secretaria-Executiva; e

III - para dispositivos corporativos implantados na Controladoria-Geral da União devem ser observadas as seguintes configurações:

a) desabilitação de portas, protocolos e serviços não necessários para suportar as operações; e

b) utilização de apenas protocolos de rede atualizados.

**Art. 9º** Dispositivos e softwares corporativos configurados de forma segura devem ser monitorados para garantir que permaneçam em conformidade com as configurações aprovadas.

**Art. 10.** Protocolos e ferramentas utilizados para instalar, modificar ou gerenciar configurações de tecnologia devem ser aprovados pela Diretoria de Tecnologia da Informação da Secretaria-Executiva.

#### CAPÍTULO III — DAS RESPONSABILIDADES

**Art. 11.** A Diretoria de Tecnologia da Informação da Secretaria-Executiva é responsável por:

I - elaborar, manter e fazer cumprir a Política e o Processo de Gerenciamento de Configuração Segura de Dispositivos e Softwares Corporativos no âmbito da Controladoria-Geral da União; e

II - planejar, implementar, monitorar e modificar as configurações seguras nos dispositivos e softwares corporativos da Controladoria-Geral da União.

#### CAPÍTULO IV — DISPOSIÇÕES FINAIS

**Art. 12.** Os casos omissos serão resolvidos pela Diretoria de Tecnologia da Informação da Secretaria Executiva.

**Art. 13.** A revisão desta Portaria Normativa deve ser realizada a cada dois anos ou sempre que se fizer necessário.

**Art. 14.** Esta Portaria Normativa entra em vigor na data de sua publicação.

EVELINE MARTINS BRITO
