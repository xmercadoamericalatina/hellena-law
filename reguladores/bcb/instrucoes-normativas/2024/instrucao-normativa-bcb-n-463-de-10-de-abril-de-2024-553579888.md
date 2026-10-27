---
titulo: "INSTRUÇÃO NORMATIVA BCB Nº 463, DE 10 DE ABRIL DE 2024"
orgao: "Banco Central do Brasil/Àrea de Regulação/Departamento de Regulação do Sistema Financeiro"
tipo: "Instrução Normativa"
numero: "463"
data: 2024-04-10
revogada: null
versao_texto: "publicação original"
publicacao: "DOU de 11/04/2024, seção 1, p. 223"
data_publicacao: 2024-04-11
edicao: "70"
fonte: "https://www.in.gov.br/web/dou/-/instrucao-normativa-bcb-n-463-de-10-de-abril-de-2024-553579888"
sha256_html_fonte: 185b4ec7c510a16bd80c6ccebe51cc68d1af430cef0ad521df1cdbde269ca7ed
baixado_em: 2026-10-16
---
# INSTRUÇÃO NORMATIVA BCB Nº 463, DE 10 DE ABRIL DE 2024

INSTRUÇÃO NORMATIVA BCB Nº 463, DE 10 DE ABRIL DE 2024

Divulga a versão 6.0 do Manual de Experiência do Cliente no Open Finance.

Os Chefes do Departamento de Regulação do Sistema Financeiro (Denor) e do Departamento de Tecnologia da Informação (Deinf), no uso das atribuições que lhes conferem os arts. 23, inciso I, alínea "a", do Regimento Interno do Banco Central do Brasil, anexo à Resolução BCB nº 340, de 21 de setembro de 2023, com base no art. 3º, inciso V, da Resolução BCB nº 32, de 29 de outubro de 2020, resolvem:

**Art. 1º** Esta Instrução Normativa divulga a versão 6.0 do Manual de Experiência do Cliente no Open Finance, de observância obrigatória por parte das instituições participantes, conforme Anexo.

**Parágrafo único.** O manual de que trata o caput, em sua versão mais recente, estará acessível na página do Open Finance no sítio eletrônico do Banco Central do Brasil na internet e no Portal do Open Finance no Brasil, mantido pela Estrutura Responsável pela Governança do Open Finance de que trata o art. 44, § 1º, da Resolução Conjunta nº 1, de 4 de maio de 2020.

**Art. 2º** Fica revogada a Instrução Normativa BCB nº 409, de 29 de agosto de 2023.

**Art. 3º** Esta Instrução Normativa entra em vigor na data de sua publicação.

GILNEU FRANCISCO ASTOLFI VIVAN

Chefe do Departamento de Regulação do Sistema Financeiro

HAROLDO JAYME MARTINS FROES CRUZ

Chefe do Departamento de Tecnologia da Informação

## ANEXO

Manual de Experiência do Cliente no Open Finance Versão 6.0

Sumário de alterações

<table>    <tbody>     <tr></tr>     <tr>      <td rowspan="1" colspan="1"><p>Data</p></td>      <td rowspan="1" colspan="1"><p>Versão</p></td>      <td rowspan="1" colspan="1"><p>Descrição das alterações</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>10/4/2024</p></td>      <td rowspan="1" colspan="1"><p>6.0</p></td>      <td rowspan="1" colspan="1"><p>Alterações na subseção 4.1.1 referentes ao comportamento na instituição transmissora quando do compartilhamento de agrupamento de dados e às instituições que devem implementar o redirecionamento sem a passagem por navegadores.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p>Alterações na subseção 4.1.2 referentes à inclusão de disposições sobre pagamentos sucessivos e às instituições que devem implementar o redirecionamento sem a passagem por navegadores.</p></td>     </tr>    </tbody>   </table>

Termos de Uso

Este manual define os princípios básicos da experiência do cliente no Open Finance, complementando a regulamentação vigente sobre o tema.

O manual será revisto e atualizado periodicamente a fim de preservar a compatibilidade com a regulamentação, bem como incorporar os aprimoramentos decorrentes da evolução do Open Finance.

Informações mais detalhadas e exemplos da aplicação deste manual poderão ser encontradas no Portal do Open Finance no Brasil (https://openfinancebrasil.org.br/), mantido pela Estrutura de Governança Responsável pela Governança do Open Finance de que trata o art. 44, § 1º, da Resolução Conjunta nº 1, de 2020.

Sugestões, críticas ou pedidos de esclarecimento de dúvidas relativas ao conteúdo deste documento podem ser enviados ao Banco Central do Brasil por meio dos canais institucionais dessa autarquia.

Referências

As especificações constantes neste manual baseiam-se, referenciam e complementam, quando aplicável, os seguintes documentos:

I - Resolução Conjunta nº 1, de 4 de maio de 2020;

II - Circular nº 4.015, de 4 de maio de 2020;

III - Resolução BCB nº 32, de 29 de outubro de 2020; e

IV - Lei nº 13.709, de 14 de agosto de 2018 (Lei Geral de Proteção de Dados Pessoais - LGPD).

Os atos normativos de competência do Conselho Monetário Nacional ou do Banco Central do Brasil podem ser acessados no sítio eletrônico do Banco Central do Brasil na internet (www.bcb.gov.br), por meio da opção de "Busca de normas".

1\. Introdução

Este manual visa a garantir que a experiência do cliente ao compartilhar dados e serviços entre as instituições participantes do Open Finance seja segura, ágil, precisa e conveniente. Os consumidores de produtos e serviços financeiros somente terão confiança para autorizar o compartilhamento de dados e serviços se a sua experiência for condizente com suas expectativas e se as informações a respeito do processo lhes forem apresentadas de maneira clara e intuitiva, permitindo que seu consentimento para compartilhamento de dados e serviços seja inequívoco e bem-informado. Para que isso aconteça, é essencial que a jornada de compartilhamento ocorra em um ambiente seguro, com o mínimo de fricções possíveis.

Ao longo deste manual, algumas expressões serão frequentemente utilizadas, entre as quais:

I - jornada simples de compartilhamento de dados e serviços: sequência de etapas do compartilhamento de dados ou serviços realizada por um único cliente, pessoa natural ou jurídica;

II - jornada múltipla de compartilhamento de dados e serviços: sequência de etapas do compartilhamento de dados ou serviços quando é necessária a autorização de mais de um cliente, a exemplo de contas de pessoas jurídicas, em que o cliente solicitante inicia o compartilhamento de dados ou serviços e clientes aprovadores (representantes ou procuradores da pessoa jurídica) precisam autorizá-lo; e

III - ambiente de gestão de consentimentos: ambiente disponibilizado pelas instituições participantes em seus canais eletrônicos para que o cliente consulte e gerencie os consentimentos já efetivados ou pendentes, inclusive para fins de sua revogação.

As expressões mencionadas são utilizadas com objetivo de facilitar a compreensão deste manual e não precisam ser, necessariamente, empregadas durante as etapas da solicitação de compartilhamento.

2\. Disposições gerais sobre a experiência do cliente no Open Finance

É vedado às instituições participantes criar obstáculos ou adotar mecanismos que, de alguma maneira, prejudiquem a fluidez da jornada do cliente ou o incentivem, de forma voluntária ou involuntária, a desistir do compartilhamento de dados ou de serviços no âmbito do Open Finance. Tais obstáculos ou mecanismos incluem, por exemplo, a oferta de produtos e serviços ao cliente no decorrer de quaisquer jornadas do Open Finance, a inserção de telas, etapas ou informações desnecessárias, duplicadas ou redundantes, ou o uso de linguagem que possa gerar incerteza ou que afete negativamente, de forma direta ou indireta, a percepção do cliente quanto à credibilidade e à segurança do Open Finance ou das demais instituições participantes.

A vedação se aplica a todas as etapas da jornada do cliente no Open Finance referentes aos dados e serviços já tipificados ou que venham a sê-lo no âmbito do ecossistema, bem como às informações referentes à jornada de compartilhamento divulgadas nos diferentes canais de comunicação das instituições participantes com seus clientes.

As instituições participantes devem garantir que seus clientes vivenciem a melhor experiência nas jornadas do Open Finance. Com vistas a atingir esse objetivo, as instituições participantes que oferecem acesso aos seus produtos e serviços também por meio de aplicativo devem ofertar as jornadas do Open Finance também nesse canal.

As disposições ora estabelecidas devem constar de forma expressa no Guia de Experiência do Cliente, objeto da seção 4 deste manual.

3\. Princípios da experiência do cliente no Open Finance

Tendo por base as disposições da Resolução Conjunta nº 1, de 2020, consideram-se princípios da experiência do cliente no Open Finance:

I - a segurança e a privacidade;

II - a agilidade;

III - a conveniência e o controle; e

IV - a transparência.

3.1 Segurança e privacidade

O compartilhamento de dados e serviços no Open Finance deve ser realizado em um ambiente seguro, que garanta a privacidade dos dados pessoais do cliente, com observância da legislação e da regulamentação vigentes, especialmente dos atos normativos que tratam de segurança e privacidade de dados pessoais.

Durante a jornada do compartilhamento, o cliente deve ser adequadamente informado sobre a segurança do processo, objetivando o consentimento para o compartilhamento de seus dados cadastrais e transacionais, bem como do serviço de iniciação de transação de pagamento.

3.2 Agilidade

O processo de compartilhamento de dados e serviços no Open Finance deve ter duração compatível com os seus objetivos e o nível de complexidade, assegurando as condições necessárias para a livre escolha e a tomada de decisão por parte do cliente. Um processo desnecessariamente longo pode provocar a desistência do cliente, enquanto eventual precariedade na prestação de informações não permite uma tomada de decisão adequada.

O processo de compartilhamento de dados e serviços deve ocorrer de forma sucessiva e ininterrupta. Sendo assim, as etapas da solicitação de compartilhamento não devem ser interrompidas até a sua conclusão nem devem exigir ações desnecessárias por parte do cliente.

Nos casos de jornada múltipla de compartilhamento de dados e serviços, a confirmação do compartilhamento somente ocorrerá após a finalização do processo por todos os clientes envolvidos no compartilhamento, que não precisarão fazê-lo de forma simultânea ou imediata, observada a garantia da segurança e da transparência do processo, inclusive no que diz respeito aos prazos necessários para a sua conclusão.

3.3 Conveniência e controle

O compartilhamento de dados e serviços no Open Finance deve ser realizado para finalidades específicas e de forma conveniente e acessível ao cliente, inclusive no que diz respeito aos canais de acesso das instituições participantes. Deverão ser asseguradas ao cliente as condições necessárias para o exercício do controle dos seus dados pessoais compartilhados no Open Finance. Nesse sentido, a jornada de compartilhamento deve ser centrada no cliente, tendo em vista o seu perfil, as suas necessidades, os seus objetivos e as suas expectativas, com a disponibilização de informações e ambientes de gestão de consentimentos, inclusive para a revogação do consentimento quando entender oportuno e apropriado, respeitados os prazos definidos na regulamentação vigente.

As instituições participantes do Open Finance não podem criar etapas adicionais ou utilizar métodos de autenticação e confirmação mais rigorosos para confirmação do compartilhamento de dados e serviços no âmbito do Open Finance.

Em jornadas de múltipla alçada de pessoas jurídicas, os poderes e alçadas já constituídos e definidos para movimentação de contas nas suas políticas internas, tais como estatutos, contratos sociais ou outros documentos correlatos, devem ser utilizados para fins de compartilhamento de dados e serviços, de modo que é vedado às instituições transmissoras de dados e detentoras de conta exigirem a constituição de poderes e alçadas específicos para fins de compartilhamentos de dados e serviços no âmbito do Open Finance.

Adicionalmente, as instituições transmissoras de dados e detentoras de conta que disponibilizam, em seus canais, mecanismos para que representantes legais devidamente constituídos perante as próprias instituições possam autorizar ou delegar poderes para outras pessoas, devem contemplar, nesses mecanismos, a possibilidade de autorização ou delegação de poderes para compartilhamento de dados e serviços no âmbito do Open Finance.

3.4 Transparência

O cliente deve receber informações claras, objetivas e adequadas durante o processo de compartilhamento de dados e serviços. A instituição receptora de dados deve informar ao cliente com clareza e de forma tempestiva sobre quais dados serão compartilhados, inclusive referentes a produtos ou serviços que poderão vir a ser contratados pelo cliente ou comercializados pela instituição transmissora de dados no futuro, e os motivos pelos quais esses dados serão necessários para as finalidades em questão, além de outras informações obrigatórias previstas na regulamentação vigente. No caso de compartilhamento de serviços, deve sempre ficar transparente para o cliente durante a jornada qual é a instituição participante responsável pela prestação desse serviço, bem como as condições do serviço que está sendo prestado.

Informações desnecessárias ou excessivamente complexas podem gerar dúvidas e inseguranças ao cliente, que poderá desistir do compartilhamento por falta de compreensão do processo. Assim, as informações fornecidas ao cliente devem ser suficientes e precisas para que sua tomada de decisão seja inequívoca e bem-informada. A linguagem utilizada deve ser simples e compreensível, independentemente do nível de conhecimento prévio do cliente sobre produtos e serviços financeiros.

4\. Guia de Experiência do Cliente

Conforme a Resolução BCB nº 32, de 2020, a Estrutura Responsável pela Governança do Open Finance deverá disponibilizar às instituições participantes do Open Finance e ao público em geral o Guia de Experiência do Cliente, que congregará procedimentos operacionais e requisitos que deverão ser observados por todas as instituições participantes na interação com seus clientes durante a jornada do compartilhamento, observado o disposto neste manual e na regulamentação vigente sobre o Open Finance. A disponibilização desse documento, em sua versão mais atual, deverá ser realizada por meio do Portal do Open Finance no Brasil.

O Guia deverá ser revisado e atualizado periodicamente pela Estrutura Responsável pela Governança do Open Finance, que deverá manter controle transparente das versões publicadas. A publicação de novas versões do documento deverá ser acompanhada de testes de usabilidade com clientes representativos do público-alvo do Open Finance, bem como comunicada de forma tempestiva às instituições participantes e ao Banco Central do Brasil, que poderá determinar ajustes e correções.

Admite-se que o Guia estabeleça princípios e requisitos adicionais aos constantes neste manual. No entanto, o seu conteúdo deve estar em conformidade com o disposto na legislação e na regulamentação vigentes.

4.1 Conteúdo do Guia de Experiência do Cliente

O Guia de Experiência do Cliente deverá dispor sobre, no mínimo:

4.1.1 Jornada simples de compartilhamento de dados

O fluxo e o conteúdo das etapas dessa jornada devem abranger, no mínimo:

I - A identificação do cliente

Nessa etapa, a instituição receptora de dados deve identificar o cliente, conforme exigido pela regulamentação vigente.

II - As finalidades determinadas do consentimento

Nessa etapa, a instituição receptora de dados deve prestar informações ao cliente acerca da(s) finalidade(s) e do(s) serviço(s) associados ao processo de compartilhamento de dados.

III - A seleção dos dados objeto de compartilhamento na instituição receptora de dados

Nessa etapa, o cliente deve poder selecionar os dados que deseja compartilhar, observando os agrupamentos de dados definidos com base no art. 11 da Resolução Conjunta nº 1, de 2020.

O cliente deve ser informado sobre quais dados são necessários para a finalidade do compartilhamento e, conforme o caso, quais seriam opcionais. Os dados opcionais devem corresponder a uma finalidade determinada, mesmo que secundária em relação à finalidade principal. O cliente deve ser informado ainda sobre os motivos pelos quais esses dados são necessários para a(s) finalidade(s) em questão.

É facultada nessa etapa a apresentação de recurso de "Termos e Condições", ou similar, desde que não seja exigida ação adicional do cliente para o aceite dos termos.

IV - A seleção do prazo de compartilhamento de dados

Nessa etapa, o cliente deve poder selecionar o prazo pelo qual deseja compartilhar os dados selecionados, observada a finalidade e outros aspectos estabelecidos na regulamentação específica do Open Finance.

V - A seleção da instituição transmissora de dados

Nessa etapa, o cliente deve poder selecionar a instituição transmissora dos dados. Deve ser disponibilizado mecanismo de busca que propicie uma seleção ágil e clara da instituição desejada. Devem estar listadas todas as instituições participantes para fins de compartilhamento de dados no Open Finance devidamente registradas no Diretório de Participantes mantido pela Estrutura Responsável pela Governança do Open Finance.

VI - O redirecionamento para o ambiente da instituição transmissora de dados

Nessa etapa, o cliente deve ser informado que está sendo redirecionado de forma segura para o ambiente da instituição transmissora de dados selecionada. Deve ficar claro para o cliente que o compartilhamento ainda não está concluído e que etapas adicionais são necessárias para a sua efetivação.

O redirecionamento não pode envolver qualquer ação do cliente, tendo caráter apenas informativo, e deve contemplar o que segue:

a) jornadas iniciadas na instituição receptora de dados em dispositivo desktop: o redirecionamento pode ocorrer para o mesmo dispositivo ou para o dispositivo móvel; e

b) jornadas iniciadas na instituição receptora de dados em dispositivo móvel:

1\. no caso das instituições transmissoras de dados pertencentes aos conglomerados sujeitos ao monitoramento de jornada do cliente, conforme Manual de Monitoramento do Open Finance, o redirecionamento deve ocorrer diretamente para o aplicativo da instituição transmissora sem a passagem por navegadores; e

2\. as demais instituições transmissoras de dados não abrangidas pelo monitoramento de jornada do cliente, conforme Manual de Monitoramento do Open Finance, devem observar, preferencialmente, o redirecionamento para seus aplicativos.

Os conglomerados enquadrados no item 1 podem apresentar ao Banco Central do Brasil pedidos fundamentados para a dispensa de instituições ou marcas específicas em que o redirecionamento obrigatório para o aplicativo possa prejudicar a jornada dos seus clientes.

Excepcionalmente, caso o cliente não possua o aplicativo da instituição transmissora instalado no dispositivo móvel, o redirecionamento deve ser feito para o ambiente da instituição no navegador ou para a loja de aplicativos, sempre no mesmo dispositivo.

VII - A autenticação do cliente na instituição transmissora de dados

Nessa etapa, o cliente deve se autenticar na instituição transmissora de dados. O cliente deve poder reconhecer que está no ambiente da instituição com a qual já mantém relacionamento e que as credenciais utilizadas para autenticação não estão visíveis e não serão compartilhadas com a instituição receptora dos dados.

Conforme estabelece a Resolução Conjunta nº 1, de 2020, os procedimentos e controles para autenticação do cliente devem ser compatíveis com os aplicáveis ao acesso aos canais de atendimento eletrônicos já disponibilizados pela instituição transmissora. Essa compatibilidade abrange, entre outros, os fatores de autenticação, a quantidade de etapas e a duração do procedimento.

VIII - A confirmação de compartilhamento pelo cliente na instituição transmissora de dados

Nessa etapa, o cliente deve confirmar o compartilhamento na instituição transmissora de dados. Deve ser apresentado ao cliente para conferência, no mínimo, a identificação da instituição receptora de dados, o período de validade do consentimento e os dados que serão objeto de compartilhamento.

Todas as origens ou agrupamentos de dados apresentados ao cliente devem estar pré-selecionados, de modo que somente seja requerida ação do cliente caso ele deseje excluir um ou mais itens do escopo a ser compartilhado (opt-out).

A seleção dos agrupamentos de dados para compartilhamento não pode ser alterada no ambiente da instituição transmissora. Seleções no ambiente da instituição transmissora devem se restringir à origem dos dados.

Excepcionalmente no caso de operações de crédito, de investimento e de câmbio, os dados devem ser apresentados em agrupamentos únicos que englobem todas as diferentes modalidades de produtos ou serviços existentes, inclusive as modalidades não contratadas pelo cliente ou que ainda não são comercializadas pela instituição, sendo vedada a possibilidade de seleção pelo cliente da origem dos dados (modalidades, submodalidades, ou contratos específicos) para o compartilhamento.

O eventual detalhamento dos dados objeto do compartilhamento deve ser ocultado por padrão. Deve ser disponibilizado recurso (botão, link, entre outros) para que o cliente, caso deseje, possa acessar o detalhamento dos dados que serão compartilhados.

A jornada de compartilhamento de dados no ambiente da instituição transmissora de dados não deve conter recurso de "Termos e Condições", ou similar. O referido recurso pode, a critério da instituição, constar no ambiente de Gestão de Consentimentos da transmissora, de que trata a subseção 4.1.4 deste manual.

IX - O redirecionamento para o ambiente da instituição receptora de dados

Nessa etapa, o cliente deve ser informado que está sendo redirecionado de forma segura para o ambiente da instituição receptora de dados e que essa etapa é necessária para conclusão do compartilhamento. O redirecionamento não pode envolver qualquer ação do cliente, tendo caráter apenas informativo, e deve ocorrer para o mesmo canal eletrônico da instituição receptora de dados utilizado pelo cliente na etapa inicial da jornada.

As instituições sujeitas à obrigação de redirecionamento para o aplicativo sem a passagem por navegadores, conforme disposto no inciso VI desta subseção, quando estiverem atuando como receptoras de dados, devem implementar o redirecionamento previsto nesta etapa também sem a passagem por navegadores.

X - A efetivação da solicitação de compartilhamento de dados

Nessa etapa, o cliente deve ser comunicado pela instituição receptora de dados sobre a efetivação da solicitação de compartilhamento de dados. A comunicação deve incluir, no mínimo, a(s) finalidade(s), o prazo e os dados do compartilhamento.

4.1.2 Jornada simples de compartilhamento de serviço de iniciação de transação de pagamento

O fluxo e o conteúdo das etapas dessa jornada devem abranger, no mínimo:

I - A identificação do cliente

Nessa etapa, a instituição iniciadora de transação de pagamento deve identificar o cliente, conforme exigido pela regulamentação vigente.

II - A seleção da instituição detentora de conta

Nessa etapa, o cliente deve poder selecionar a instituição na qual mantém a conta que será utilizada para o pagamento. Deve ser disponibilizado mecanismo de busca que propicie uma seleção ágil e clara da instituição desejada. Devem estar listadas todas as instituições participantes para fins de compartilhamento do serviço de iniciação de transação pagamento no Open Finance devidamente registradas como instituições detentoras de conta no Diretório de Participantes mantido pela Estrutura Responsável pela Governança do Open Finance.

III - As informações sobre a transação de pagamento ou a configuração de uma recorrência, no caso de pagamentos sucessivos

Nessa etapa, devem ser solicitadas ou apresentadas ao cliente, no mínimo, as informações abaixo:

a) no caso de pagamentos únicos:

1\. o valor do pagamento;

2\. a forma de pagamento, de acordo com os serviços de pagamento de que trata o art. 6º da Circular nº 4.015, de 4 de maio de 2020;

3\. os dados do recebedor do pagamento, de acordo com os parâmetros referentes à forma de pagamento;

4\. a data do pagamento; e

5\. o valor da tarifa cobrada pelo serviço de iniciação de transação de pagamento, quando houver; e

b) no caso de configuração de recorrência para pagamentos sucessivos:

1\. o valor do pagamento, quando aplicável, sendo facultativo nos casos de transações de pagamento sucessivas em que o valor pactuado seja variável;

2\. a forma de pagamento, de acordo com os serviços de pagamento de que trata o art. 6º da Circular nº 4.015, de 2020;

3\. as datas futuras dos pagamentos, quando aplicável;

4\. a periodicidade das transações ou as condições que as desencadeiem;

5\. o prazo do consentimento, quando aplicável;

6\. limites, quando aplicável;

7\. os dados do recebedor do pagamento, de acordo com os parâmetros referentes à forma de pagamento; e

8\. o valor da tarifa cobrada pelo serviço de iniciação de transação de pagamento, quando houver.

Além das informações mínimas para a iniciação de transação de pagamento dispostas acima, devem ser observados, de forma geral, os dados dispostos nos regulamentos ou instrumentos que disciplinem o funcionamento do arranjo de pagamento referente à respectiva transação de pagamento e demais dados estabelecidos nas especificações disponíveis no Portal do Open Finance no Brasil.

É facultada nessa etapa a apresentação de recurso de "Termos e Condições", ou similar, desde que não seja exigida ação adicional do cliente para o aceite dos termos.

IV - O redirecionamento para o ambiente da instituição detentora de conta

Nessa etapa, o cliente deve ser informado que está sendo redirecionado de forma segura para o ambiente da instituição detentora de conta selecionada. Deve ficar claro para o cliente que o pagamento ainda não está concluído e que etapas adicionais são necessárias para a sua efetivação. O cliente deve ser informado, ainda, sobre o tempo máximo que ele possui para confirmar a transação.

O redirecionamento não pode exigir qualquer ação do cliente, tendo caráter apenas informativo, e deve contemplar o que segue:

a) jornadas iniciadas na instituição iniciadora de transação de pagamentos em dispositivo desktop: o redirecionamento pode ocorrer para o mesmo dispositivo ou para o dispositivo móvel; e

b) jornadas iniciadas na instituição iniciadora de transação de pagamentos em dispositivo móvel:

1\. no caso das instituições detentoras de conta pertencentes aos conglomerados sujeitos ao monitoramento de jornada do cliente, conforme Manual de Monitoramento do Open Finance, o redirecionamento deve ocorrer diretamente para o aplicativo da instituição detentora sem a passagem por navegadores; e

2\. as demais instituições detentoras de conta não abrangidas pelo monitoramento de jornada do cliente, conforme Manual de Monitoramento do Open Finance, devem realizar, preferencialmente, o redirecionamento para seus aplicativos.

Excepcionalmente, caso o cliente não possua o aplicativo da instituição detentora de conta instalado em seu dispositivo móvel, o redirecionamento deve ser realizado para o ambiente da instituição no navegador ou para a loja de aplicativos, sempre no mesmo dispositivo.

Ressalta-se que não há obrigatoriedade de desenvolvimento de aplicativo para as instituições que não ofereçam esse canal aos seus clientes. Nesse último caso, pode ser utilizado o canal da instituição no navegador.

V - A autenticação do cliente na instituição detentora de conta

Nessa etapa, o cliente deve se autenticar na instituição detentora de conta. O cliente deve poder reconhecer que está no ambiente da instituição com a qual já mantém relacionamento e que as credenciais utilizadas para autenticação não estão visíveis e não serão compartilhadas com a instituição iniciadora de transação de pagamento.

Conforme estabelece a Resolução Conjunta nº 1, de 2020, os procedimentos e controles para autenticação do cliente devem ser compatíveis com os aplicáveis ao acesso aos canais de atendimento eletrônicos já disponibilizados pela instituição detentora de conta. Essa compatibilidade abrange, entre outros, os fatores de autenticação, a quantidade de etapas e a duração do procedimento.

VI - A confirmação de compartilhamento pelo cliente na instituição detentora de conta

Nessa etapa, o cliente deve confirmar o pagamento na instituição detentora de conta. Caso seja titular de mais de uma conta associada às credenciais com as quais se autenticou, o cliente deve poder selecionar a conta que deseja utilizar para a transação de pagamento.

Devem ser apresentadas ao cliente para confirmação, no mínimo, as informações listadas nos itens 1 a 4 da alínea "a" e 1 a 7 da alínea "b" do inciso III desta subseção, que tratam da etapa das informações sobre a transação de pagamento. Adicionalmente, deve ser apresentado ao cliente o valor da tarifa cobrada pela instituição detentora de conta na realização da transação de pagamento, quando houver.

A jornada de compartilhamento de serviço de iniciação de transação de pagamento no ambiente da instituição detentora de conta não deve conter recurso de "Termos e Condições", ou similar. O referido recurso pode, a critério da instituição, constar no ambiente de Gestão de Consentimentos da detentora de conta, de que trata a subseção 4.1.4 deste manual.

VII - O redirecionamento para o ambiente da instituição iniciadora de transação de pagamento

Nessa etapa, o cliente deve ser informado que está sendo redirecionado de forma segura para o ambiente da instituição iniciadora de transação de pagamento e que essa etapa é necessária para conclusão do compartilhamento. O redirecionamento não pode exigir qualquer ação do cliente, tendo caráter apenas informativo, e deve ocorrer para o mesmo canal eletrônico da instituição iniciadora de transação de pagamento utilizado pelo cliente na etapa inicial da jornada.

As instituições sujeitas à obrigação de redirecionamento para o aplicativo sem a passagem por navegadores, conforme disposto no inciso IV desta subseção, quando estiverem atuando como iniciadoras de transação de pagamento, devem implementar o redirecionamento previsto nesta etapa também sem a passagem por navegadores.

VIII - A efetivação da transação de pagamento

Nessa etapa, a instituição iniciadora de transação de pagamento deve apresentar o comprovante da efetivação da transação de pagamento, seja ele único ou sucessivo. Deve ser apresentado ao cliente comprovante com, no mínimo, as informações listadas no inciso III desta subseção, que trata da etapa das informações sobre a transação de pagamento.

4.1.3 O fluxo das etapas da jornada de múltipla alçada de compartilhamento de dados e serviços

O Guia deve estabelecer parâmetros para a experiência do cliente em jornada múltipla de compartilhamento de dados e serviços, quando for o caso.

Nesse caso, todos os clientes envolvidos no compartilhamento devem ser informados com clareza sobre os procedimentos e as etapas necessárias para a efetivação do compartilhamento. Adicionalmente, os clientes aprovadores devem ser notificados tempestivamente pela instituição transmissora de dados ou detentora de conta sobre a necessidade de ação para efetivação do compartilhamento de dados ou serviços iniciado pelo cliente solicitante.

Em particular, o Guia deve estabelecer, quando for o caso, os prazos máximos para ação dos clientes aprovadores, que deverão ser aplicados de maneira uniforme por todas as instituições participantes. Ademais, o Guia deve estabelecer parâmetros para os casos em que um ou mais clientes aprovadores não autorizem o compartilhamento abrangendo, no mínimo, a notificação aos demais clientes (solicitantes ou aprovadores) e a comunicação à instituição receptora de dados ou iniciadora de transação de pagamento.

Para fins de compartilhamento de dados relacionados a contas conjuntas de pessoas naturais, a instituição transmissora de dados deve garantir que a instituição receptora de dados tenha acesso a dados cadastrais apenas do titular da conta responsável pelo consentimento, não sendo admitido o compartilhamento dos dados cadastrais dos demais titulares da respectiva conta.

A instituição transmissora de dados deve exigir a confirmação de todos os titulares da conta para efetivar o compartilhamento somente se o acesso a informações transacionais da conta depender da autorização de todos os titulares.

4.1.4 Ambiente de gestão dos consentimentos

O Guia deve estabelecer requisitos para o ambiente de gestão de consentimentos das instituições participantes. No caso, as referidas instituições devem disponibilizar em seu canal eletrônico um ambiente específico para a gestão dos compartilhamentos em que estiveram envolvidas no âmbito do Open Finance.

Nesse ambiente, o cliente deve ter acesso de forma simples, ágil, precisa e conveniente a, no mínimo, informações sobre consentimentos vigentes ou que estejam pendentes de efetivação na jornada múltipla, com a possibilidade de pesquisa com base em critérios definidos para observância homogênea por todas as instituições participantes.

Adicionalmente, o cliente deve ter a faculdade de consultar e revogar os consentimentos, com observância do disposto no art. 15 da Resolução Conjunta nº 1, de 2020. A efetivação de revogação deve ser precedida de tela de confirmação com informações sobre as consequências da ação.

4.1.5 A terminologia utilizada pelas instituições participantes durante a jornada do compartilhamento

O Guia deve padronizar a terminologia utilizada pelas instituições participantes na comunicação com seus clientes durante a jornada de compartilhamento de dados e serviços.

Os termos e expressões utilizados neste manual e nos demais atos normativos editados pelo Banco Central do Brasil podem ser substituídos por outros considerados mais adequados para a compreensão de todos os clientes do Open Finance, desde que os seus significados sejam mantidos.

A terminologia contida no Guia deve ser adotada por todas as instituições participantes, inclusive em seus processos de comunicação ao público em geral associados ao Open Finance, garantida a uniformidade da experiência dos clientes e prevenindo o surgimento de dúvidas ou insegurança durante o compartilhamento de dados e serviços.

4.2 Estrutura do Guia de Experiência do Cliente

O Guia deve ser estruturado de modo claro e coeso, a fim de que seja interpretado adequadamente pelas partes interessadas. Adicionalmente, o Guia deve conter telas de exemplo que ilustrem as etapas das jornadas de compartilhamento de dados e serviços pelo cliente.

Por sua vez, os dispositivos do Guia devem ser classificados em, no mínimo:

I - requisitos: disposições que devem ser seguidas obrigatoriamente pelas instituições participantes; e

II - recomendações: disposições de observação não obrigatória pelas instituições participantes, mas cuja implementação é recomendável, considerando boas práticas para a experiência do cliente.

A esse respeito, o Guia deve conter requisitos e recomendações aplicáveis às diversas situações de compartilhamento de dados e serviços, abrangendo, no mínimo:

I - compartilhamento de dados e serviços por pessoas naturais;

II - compartilhamento de dados e serviços por pessoas jurídicas;

III - compartilhamento de dados e serviços por pessoas naturais titulares de contas conjuntas em que seja exigido o consentimento de mais de um titular da conta;

IV - compartilhamento de dados e serviços por pessoas jurídicas em que seja exigido o consentimento de mais de um representante ou procurador da empresa; e

V - ambiente de gestão de consentimentos concedidos por parte de pessoas naturais e jurídicas nas instituições participantes.

5\. Regras transitórias

As instituições receptoras de dados e as instituições iniciadoras de transação de pagamentos que passam a ser obrigadas a realizar o redirecionamento diretamente para o aplicativo da instituição transmissora de dados e da instituição detentora de conta, respectivamente, sem a passagem por navegadores, com base nas alterações promovidas nas subseções 4.1.1 e 4.1.2, devem concluir tal implementação até 30 de junho de 2024.
