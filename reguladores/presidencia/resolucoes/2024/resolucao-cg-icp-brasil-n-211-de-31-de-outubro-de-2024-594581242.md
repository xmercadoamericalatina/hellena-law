---
titulo: "RESOLUÇÃO CG ICP-BRASIL Nº 211, DE 31 DE OUTUBRO DE 2024"
orgao: "Presidência da República/Casa Civil/Comitê Gestor da Infraestrutura de Chaves Públicas"
tipo: "Resolução"
numero: "211"
data: 2024-10-31
revogada: null
versao_texto: "publicação original"
publicacao: "DOU de 07/11/2024, seção 1, p. 3"
data_publicacao: 2024-11-07
edicao: "216"
fonte: "https://www.in.gov.br/web/dou/-/resolucao-cg-icp-brasil-n-211-de-31-de-outubro-de-2024-594581242"
sha256_html_fonte: dc8f5719400b5728693ba496c83b6711311fa269ea9ce56a71037f6afe830016
baixado_em: 2026-10-16
---
# RESOLUÇÃO CG ICP-BRASIL Nº 211, DE 31 DE OUTUBRO DE 2024

RESOLUÇÃO CG ICP-BRASIL Nº 211, DE 31 DE OUTUBRO DE 2024

Dispõe sobre os tipos de certificados digitais emitidos no âmbito da Infraestrutura de Chaves Públicas Brasileira - ICP-Brasil.

**O COORDENADOR DO COMITÊ GESTOR DA INFRAESTRUTURA DE CHAVES PÚBLICAS BRASILEIRA,**no uso das atribuições que lhe confere o art. 6º, §1º, inc. IV, da Resolução CG ICP-Brasil nº 190, de 18 de maio de 2021 (Regimento Interno), torna público que o COMITÊ GESTOR DA INFRAESTRUTURA DE CHAVES PÚBLICAS BRASILEIRA, no exercício das competências previstas no art. 4º da Medida Provisória nº 2.200-2, de 24 de agosto de 2001, em reunião ordinária, realizada em sessão presencial em 31 de outubro de 2024, resolveu:

**Art. 1º** Esta Resolução dispõe sobre os tipos de certificados digitais emitidos no âmbito da Infraestrutura de Chaves Públicas Brasileira - ICP-Brasil.

**Art. 2º** Ficam criados os seguintes tipos de certificado digital no âmbito da ICP-Brasil:

I - certificado digital de selo eletrônico em software - SE-S;

II - certificado digital de selo eletrônico em hardware - SE-H;

III - certificado digital de aplicações específicas em software - AE-S; e

IV - certificado digital de aplicações específicas em hardware - AE-H.

**Art. 3º** Ficam extintos os seguintes tipos de certificado digital no âmbito da ICP-Brasil:

I - certificado de assinatura dos tipos A1 e A2; e

II - certificado de sigilo dos tipos S1, S2, S3 e S4.

**Art. 4º** Fica vedado o uso de certificado digital de selo eletrônico com propósito de assinatura como manifestação de vontade de pessoa jurídica.

**Art. 5º** Fica vedada a emissão de certificados digitais destinados à assinatura de código (*Code siging*) na Infraestrutura de Chaves Públicas Brasileira - ICP-Brasil.

**Parágrafo único.** Certificados para assinatura de código emitidos até a data de publicação desta Resolução permanecem vigentes até a data de expiração.

**Art. 6º** Fica dispensada a aderência aos requisitos de princípios e critérios*Webtrust Baseline - Code Signing*e SSL/TLS, para suas respectivas cadeias de certificação.

**Art. 7º** Ficam extintos os seguintes OIDs (*Object Identifier*) da extensão "*Subject Alternative Name*" do certificado digital:

I -**OID = 2.16.76.1.3.5 e conteúdo**= nas primeiras 12 (doze) posições, o número de inscrição do Título de Eleitor; nas 3 (três) posições subsequentes, a Zona Eleitoral; nas 4 (quatro) posições seguintes, a Seção; nas 22 (vinte e duas) posições subsequentes, o município e a UF do Título de Eleitor.

II -**OID = 2.16.76.1.3.9 e conteúdo**= nas primeiras 11 (onze) posições, o número de Registro de Identidade Civil.

III -**OID = 2.16.76.1.3.11 e conteúdo**= nas primeiras 10 (dez) posições, o cadastro único do servidor público da ativa e militares da União constante no Sistema de Gestão de Pessoal (SIGEPE) mantido pelo Ministério do Planejamento ou nos sistemas correlatos, no âmbito da esfera estadual e do Distrito Federal, e nos Sistemas de Gestão de Pessoal das Forças Armadas.

IV -**OID = 2.16.76.1.3.4 e conteúdo**= nas primeiras 8 (oito) posições, a data de nascimento do responsável pelo certificado, no formato ddmmaaaa; nas 11 (onze) posições subsequentes, o Cadastro de Pessoa Física (CPF) do responsável; nas 11 (onze) posições subsequentes, o número de Identificação Social - NIS (PIS, PASEP ou CI); nas 15 (quinze) posições subsequentes, o número do RG do responsável; nas 10 (dez) posições subsequentes, as siglas do órgão expedidor do RG e respectiva UF;

V -**OID = 2.16.76.1.3.2 e conteúdo**= nome do responsável pelo certificado;

**Art. 8º** Fica implementado o campo*serialNumber*(OID 2.5.4.5) no*Distinguished Name*do titular do certificado digital de pessoa física, contendo o CPF, e de selo eletrônico, contendo CNPJ, a fim de garantir a unicidade de nome.

**Art. 9º** O anexo daResolução CG ICP-Brasil nº 178, de 20 de outubro de 2020, DOC-ICP-03, passa a vigorar com as seguintes alterações:

"2.2.2.1.2 a solicitação de credenciamento deve estar separada por propósito de uso de chave, quais sejam:

i. autenticação de aplicações específicas;

ii. assinatura de documentos e proteção de e-mail (S/MIME) e garantia de origem e integridade; e

iii. assinatura de carimbo do tempo (*TimeStamping*)." (NR)

**Art. 10.** O anexo daResolução CG ICP-Brasil nº 179, de 20 de outubro de 2020, DOC-ICP-04, passa a vigorar com as seguintes alterações:

"1.1.5 São 10 (dez) os tipos de certificados digitais para usuários finais da ICP-Brasil:

A3

A4

SE-S

SE-H

T3

T4

AE-S

AE-H

A CF-e-SAT

OM-BR

1.1.6 Certificados do tipo A3 e A4 são certificados de assinatura e devem ser emitidos exclusivamente para pessoas físicas.

1.1.7 Certificados do tipo SE-S e SE-H são certificados de selo eletrônico, respectivamente em software e em hardware, e devem ser emitidos apenas para pessoas jurídicas.

1.1.8 Certificados do tipo T3 e T4 somente devem ser emitidos para equipamentos das Autoridades de Carimbo do Tempo - ACTs credenciadas na ICP-Brasil. Os certificados do tipo T3 e T4 estão associados aos mesmos requisitos de segurança, exceto pelo tamanho das chaves criptográficas utilizadas.

1.1.9 Certificados do tipo AE-S e AE-H são certificados de aplicações específicas, respectivamente em software e em hardware, e devem ser emitidos pelas ACs para equipamentos, servidores, aplicações e dispositivos IOT.

1.1.10 Certificados do tipo A CF-e-SAT devem ser emitidos apenas para equipamentos integrantes do Sistema de Autenticação e Transmissão do Cupom Fiscal Eletrônico - SAT-CF-e, seguindo a regulamentação do CONFAZ.

1.1.11 Certificados do tipo Objeto Metrológico - OM-BR devem ser emitidos apenas para equipamentos metrológicos regulados pelo Inmetro.

1.1.12 Outros tipos de certificado, além dos anteriormente relacionados, podem ser propostos para a apreciação do Comitê Gestor da ICP-Brasil - CG ICP-Brasil. As propostas serão analisadas quanto à conformidade com as normas específicas da ICP-Brasil e, quando aprovadas, serão acrescidas aos tipos de certificados aceitos pela ICP-Brasil.

1.2 Nome do documento e identificação

1.2.1 Neste item deve ser identificada a PC e indicado, no mínimo, o tipo de certificado a que está associada. Exemplo: "Política de Certificado de Assinatura Digital, tipo A3, do(a) &lt;nome da instituição>". O OID (*Object Identifier*) da PC deve também ser incluído neste item.

1.2.2 No âmbito da ICP-Brasil, os OIDs das PCs serão atribuídos na conclusão do processo de credenciamento da AC, conforme a Tabela 3 a seguir:

Tabela 3 - OID de PC na ICP-Brasil

<table>    <tbody>     <tr></tr>     <tr>      <td rowspan="1" colspan="1"><p>Tipo de Certificado</p></td>      <td rowspan="1" colspan="1"><p>OID</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>A3</p></td>      <td rowspan="1" colspan="1"><p>2.16.76.1.2.3.<em>n</em></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>A4</p></td>      <td rowspan="1" colspan="1"><p>2.16.76.1.2.4.n</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>SE-S</p></td>      <td rowspan="1" colspan="1"><p>2.16.76.1.2.201.n</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>SE-H</p></td>      <td rowspan="1" colspan="1"><p>2.16.76.1.2.202.n</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>T3</p></td>      <td rowspan="1" colspan="1"><p>2.16.76.1.2.303.n</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>T4</p></td>      <td rowspan="1" colspan="1"><p>2.16.76.1.2.304.n</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>AE-S</p></td>      <td rowspan="1" colspan="1"><p>2.16.76.1.2.401.n</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>AE-H</p></td>      <td rowspan="1" colspan="1"><p>2.16.76.1.2.402.n</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>A CF-e-SAT</p></td>      <td rowspan="1" colspan="1"><p>2.16.76.1.2.500.n</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>OM-BR</p></td>      <td rowspan="1" colspan="1"><p>2.16.76.1.2.550.n</p></td>     </tr>    </tbody>   </table>

1.3 Participantes da ICP-Brasil

.......................................................................................................................................

1.4 Usabilidade do Certificado

1.4.1 ....................................................................................................................

........................................................................................................................................

1.4.1.4 Certificados do tipo A3 e A4 serão utilizados em aplicações como confirmação de identidade e assinatura de documentos eletrônicos com verificação da integridade de suas informações.

1.4.1.5 Certificados do tipo SE-S e SE-H serão utilizados para garantir origem e integridade de um documento eletrônico, servindo de prova da emissão do documento por uma pessoa jurídica.

1.4.1.6 Certificados do tipo T3 e T4 serão utilizados em aplicações mantidas por Autoridades de Carimbo do Tempo credenciadas na ICP-Brasil para assinatura de carimbos do tempo.

.........................................................................................................................................

1.4.1.9 Certificados do tipo AE-S e AE-H serão utilizados em equipamentos, servidores, aplicações e dispositivos IOT, entre entidades dentro de um ecossistema fechado, onde as autenticações são mútuas e limitadas aos intervenientes conhecidos.

1.4.2 ......................................................................................................................

1.4.2.1 É proibido o uso do certificado de aplicações específicas com a finalidade de autenticação de servidor (SSL/TLS) destinado ao reconhecimento confiável pelos navegadores de internet (browsers).

1.4.2.2 É proibido o uso do certificado de selo eletrônico para assinatura digital com o propósito de manifestação de vontade.

1.4.2.3. Neste item devem ser relacionadas, quando cabível, outras aplicações para as quais existem restrições ou proibições para o uso desses certificados.

1.5 Política de Administração

.......................................................................................................................................

6.1.1.8 .................................................................................................................

Tabela 4 - Mídias Armazenadoras de Chaves Criptográficas

<table>    <tbody>     <tr></tr>     <tr>      <td rowspan="1" colspan="1"><p>Tipo de Certificado</p></td>      <td rowspan="1" colspan="1"><p>Mídia Armazenadora de Chave Criptográfica (Requisitos Mínimos)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>SE-S e AE-S</p></td>      <td rowspan="1" colspan="1"><p>Repositório protegido por senha e/ou identificação biométrica, cifrado por software na forma definida acima.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>A3, A4, SE-H, T3, T4, AE-H e OM-BR</p></td>      <td rowspan="1" colspan="1"><p>Hardwarecriptográfico, homologado junto à ICP-Brasil ou com certificação INMETRO.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>A CF-e-SAT</p></td>      <td rowspan="1" colspan="1"><p>Hardware criptográfico.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>OM-BR</p></td>      <td rowspan="1" colspan="1"><p>Hardware criptográfico, homologado junto à ICP-Brasil ou com certificação INMETRO.</p></td>     </tr>    </tbody>   </table>

........................................................................................................................................

6.3.2.3...................................................................................................................

Tabela 6 - Períodos de Validade dos Certificados

<table>    <tbody>     <tr></tr>     <tr>      <td rowspan="1" colspan="1"><p>Tipo de Certificado</p></td>      <td rowspan="1" colspan="1"><p>Período Máximo de Validade do Certificado(em anos)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>SE-S e AE-S</p></td>      <td rowspan="1" colspan="1"><p>1</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>A3, SE-H, AE-H e T3</p></td>      <td rowspan="1" colspan="1"><p>5</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>A4 e T4</p></td>      <td rowspan="1" colspan="1"><p>11 (para cadeias hierárquicas completas em Curvas Elípticas)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p>6 (para as demais hierarquias)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>A CF-e-SAT</p></td>      <td rowspan="1" colspan="1"><p>5</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>OM-BR</p></td>      <td rowspan="1" colspan="1"><p>10</p></td>     </tr>    </tbody>   </table>

6.4 Dados de Ativação

.........................................................................................................................................

7.1.2 Extensões de certificado

7.1.2.1 Neste item, a PC deve descrever todas as extensões de certificado utilizadas e sua criticalidade, conforme especificado na Tabela de Perfis de Certificado e LCR, Anexo I deste documento.

7.1.2.2 Os campos*otherName*devem estar de acordo com as seguintes especificações:

a) o conjunto de informações definido em cada campo*otherName*deve ser armazenado como uma cadeia de caracteres do tipo ASN.1 OCTET STRING ou PRINTABLE STRING;

b) quando os números de CPF, NIS (PIS, PASEP ou CI), RG, CNPJ, CNO ou CAEPF não estiverem disponíveis, os campos correspondentes devem ser integralmente preenchidos com caracteres "zero";

c) se o número do RG não estiver disponível, não se deve preencher o campo de órgão emissor e UF;

d) quando a identificação profissional não estiver disponível, não deverá ser inserido o campo (OID) correspondente, exceto nos casos de certificado digital cuja titularidade foi validada pela AR de conselho de classe profissional;

e) todas as informações de tamanho variável referentes a números, tais como RG, devem ser preenchidas com caracteres "zero" a sua esquerda para que seja completado seu máximo tamanho possível;

f) as 10 (dez) posições das informações sobre órgão emissor do RG e UF referem-se ao tamanho máximo, devendo ser utilizadas apenas as posições necessárias ao seu armazenamento, da esquerda para a direita;

g) apenas os caracteres de A a Z, de 0 a 9, observado o disposto no item 7.1.5.2, poderão ser utilizados, não sendo permitidos os demais caracteres especiais;

h) quando o número da inscrição estadual e o número da inscrição municipal da pessoa jurídica emissora do CF-e-SAT não estiverem disponíveis não precisam ser preenchidos.

7.1.2.3 Campos*otherName*adicionais, contendo informações específicas e forma de preenchimento e armazenamento definidas pela AC, poderão ser utilizados com OID atribuídos ou aprovados pela AC Raiz.

7.1.2.4 Os outros campos que compõem a extensão "*Subject Alternative Name*" poderão ser utilizados, na forma e com os propósitos definidos na RFC 5280.

7.1.2.5 Todas as informações utilizadas para preenchimento dos campos do certificado devem ser verificadas.

7.1.3.....................................................................................................................

.......................................................................................................................................

7.1.4 Formatos de nome

7.1.4.1 O nome do titular do certificado, constante do campo "*Subject*", deverá adotar o "*Distinguished Name*" (DN) do padrão ITU X.500/ISO 9594, conforme especificado na Tabela de Perfis de Certificado e LCR, Anexo I deste documento.

7.1.4.2 Será escrito o nome até o limite do tamanho do campo disponível, vedada a abreviatura.

7.1.5 Restrições de nome

......................................................................................................................................

7.2 Perfil de LCR

.......................................................................................................................................

7.2.2 Extensões de LCR e de suas entradas

7.2.2.1 Neste item, a PC deve descrever todas as extensões de LCR utilizadas e sua criticalidade, conforme especificado na Tabela de Perfis de Certificado e LCR, Anexo I deste documento.

7.3 Perfil de OCSP

.......................................................................................................................................

.......................................................................................................................................

## Anexo I — Tabela de Perfis de Certificado e LCR (NR)

(Anexo disponível em www.gov.br/iti/pt-br/assuntos/legislacao/resolucoes)

**Art. 11.** O anexo da Resolução CG ICP-Brasil nº 177, de 20 de outubro de 2020, DOC-ICP-05, passa a vigorar com as seguintes alterações:

"1.1.2 ...................................................................................................................

1.1.3 A estrutura desta DPC está baseada na RFC 3647.

1.1.4 A AC responsável deverá manter todas as informações da sua DPC sempre atualizadas.

1.1.5 Este documento compõe o conjunto normativo da ICP-Brasil e nele são referenciados outros regulamentos dispostos nas demais normas da ICP-Brasil, conforme especificado no item 10.

1.2 ......................................................................................................................

......................................................................................................................................

1.2.2 As ACs emissoras de certificados para usuários finais devem ser exclusivas e separadas de acordo com os seguintes propósitos de uso de chaves:

a) autenticação de aplicações específicas;

b) assinatura de documento e proteção de e-mail (S/MIME) e garantia de origem e integridade; e

c) assinatura de carimbo do tempo (*TimeStamping*).

1.3 .......................................................................................................................

......................................................................................................................................

3.1.1.1 Neste item devem ser definidos os tipos de nomes admitidos para os titulares de certificados emitidos pela AC responsável pela DPC. Entre os tipos de nomes considerados, poderão estar o "*Distinguished Name*" do padrão ITU X.500.

.....................................................................................................................................

3.2.2.2 Documentos para efeitos de identificação de uma organização

a).........................................................................................................................

b) .......................................................................................................................

i. .........................................................................................................................

ii. prova de inscrição no Cadastro Nacional de Obras - CNO.

Nota 1: As confirmações de que trata o item 3.2.2.2 poderão ser feitas de forma eletrônica, desde que em barramentos ou aplicações oficiais de órgão competente. É obrigatório que essas validações constem no dossiê eletrônico do titular do certificado.

3.2.2.3 Responsabilidade decorrente do uso do certificado de uma organização

Os atos praticados com o certificado digital de titularidade de uma organização estão sujeitos ao regime de responsabilidade definido em lei.

3.2.3 ....................................................................................................................

.......................................................................................................................................

3.2.3.1.8.1 No caso de AR ELETRÔNICA, a base oficial nacional, a ser definida por Instrução Normativa da AC Raiz, deverá ter como requisito técnico a garantia de individualização unívoca dos cidadãos, biométrica e biográfica, a nível nacional.

3.2.4 Informações não verificadas do titular do certificado

......................................................................................................................................

3.2.7.1.5 Fica dispensada a observância do item 3.2.2.1.3, alíneas "b" e "c", para certificados cujo titular seja pessoa jurídica quando a solicitação for assinada com o certificado digital ICP-Brasil válido, do tipo A3 ou superior, cuja titularidade é da mesma pessoa física responsável legal da organização e a verificação dos documentos elencados no item 3.2.2.2 possa ser realizada eletronicamente por meio de barramento ou aplicação oficial.

3.2.7.2 Procedimentos para efeitos de identificação de um equipamento ou aplicação

3.2.7.2.1 Para certificados de aplicações específicas que utilizem URL na identificação do titular, deve ser verificado se o solicitante do certificado detém o registro do nome de domínio junto ao órgão competente, ou se possui autorização do titular do domínio para usar aquele endereço. Nesse caso, deve ser apresentada documentação comprobatória (termo de autorização de uso de domínio ou similar) devidamente assinado pelo titular do domínio.

3.2.7.2.2 Para emissão de certificados do tipo T3 ou T4, para equipamentos de ACT credenciadas na ICP-Brasil, a solicitação deve conter o nome de servidor e o número de série do equipamento. Esses dados devem ser validados comparando-os com aqueles publicados pelo ITI no Diário Oficial da União, quando do deferimento do credenciamento da ACT.

3.2.7.3 Autenticação de identificação de equipamento para certificado CF-e-SAT

3.2.7.3.1 Disposições gerais

3.2.7.3.1.1 Em se tratando de certificado emitido para equipamento SAT, o titular será representado pelo contribuinte identificado no certificado digital ICP-Brasil de pessoa jurídica que assina a solicitação, associada ao número de série do equipamento detentor da chave privada.

3.2.7.3.1.2 Para certificados do tipo A CF-e-SAT, a confirmação da identidade da organização e das pessoas físicas se dará conforme disposto no item 3.2.2 e com a assinatura do TERMO DE TITULARIDADE [4] específico de que trata o item 4.1.

3.2.7.3.1.3 Para certificados do tipo A CF-e-SAT, por se tratar de certificado para equipamento fiscal específico para contribuinte já identificado quando da emissão do certificado digital ICP-Brasil de pessoa jurídica válido que assina a requisição do certificado A CF-e-SAT, a confirmação da identidade se dará exclusivamente na forma do disposto no item 3.2.3 e com a assinatura do TERMO DE TITULARIDADE [4] específico de que trata o item 4.1.

3.2.7.4 Procedimentos para efeitos de identificação de um equipamento SAT

3.2.7.4.1 Para certificados de equipamento SAT, deve ser verificado se o CNPJ do contribuinte que assina digitalmente a solicitação desse certificado está vinculado ao número de série do referido equipamento, o qual deve estar registrado e autorizado pela unidade fiscal federada. Essas informações devem ser obtidas e confirmadas pela AC emissora do certificado.

3.2.7.5 Autenticação de identificação de equipamentos para certificado OM-BR

3.2.7.5 1 Disposições gerais

3.2.7.5.1.1 Em se tratando de certificado emitido para equipamento OM-BR, o titular será representado pelo fabricante identificado no certificado digital ICP-Brasil de pessoa jurídica que assina a solicitação, associada ao número de identificação do equipamento detentor da chave privada.

3.2.7.5.1.2 Para certificados do tipo OM-BR, a confirmação da identidade do fabricante se dará conforme disposto no item 3.2.7.1 e com a assinatura do TERMO DE TITULARIDADE [4] específico de que trata o item 4.1.

3.2.7.5.1.3 Para certificados do tipo OM-BR, por se tratar de certificado para equipamento metrológico específico de fabricante autorizado já identificado quando da emissão do certificado digital ICP-Brasil de pessoa jurídica válido que assina a requisição do certificado OM-BR, a confirmação da identidade se dará exclusivamente na forma do disposto no item 3.2.7.1 e com a assinatura do TERMO DE TITULARIDADE [4] específico de que trata o item 4.1.

3.2.7.6 Procedimentos para efeitos de identificação de um equipamento metrológico

3.2.7.6.1 Para certificados de equipamento metrológico, deve ser verificado se o CNPJ do fabricante que assina digitalmente a solicitação desse certificado está vinculado aos controles regulatórios do referido equipamento, o qual deve estar registrado e autorizado pelo Inmetro. Essas informações devem ser obtidas e confirmadas pela AC emissora do certificado.

3.2.8 Procedimentos complementares

3.2.8.1 A AC mantém políticas e procedimentos internos que são revisados regularmente a fim de cumprir os requisitos dos vários programas de raiz dos quais a AC é membro, bem como os Princípios e Critérios*WebTrust*.

......................................................................................................................................

3.2.9.7 ................................................................................................................

a) o responsável pelo uso do certificado de selo eletrônico deverá ser autenticado através de batimento biométrico (1:1) em PSBio credenciado na ICP-Brasil, na base biométrica oficial do TSE ou em outra base biométrica oficial da União, dos Estados ou do Distrito Federal, com comprovação auditável desse processo de autenticação biométrica por parte da AC. Essa comprovação poderá ser pelo CPF ou outro indexador viável entre os sistemas;

.......................................................................................................................................

3.2.9.8 ................................................................................................................

a) a pessoa física titular do certificado deverá ter sido biometricamente identificada e individualizada na base biométrica do órgão responsável pela emissão da Carteira de Identidade (RG) ou da Carteira Nacional de Habilitação (CNH), conforme o caso, bem como ter dado consentimento expresso e específico para o compartilhamento com as entidades da ICP-Brasil dos dados biométricos e biográficos necessários para a identificação, cadastro e emissão do certificado digital. Essa individualização poderá ser pelo CPF ou outro indexador viável entre os sistemas;

.......................................................................................................................................

3.3.2 ....................................................................................................................

a)...........................................................................................................................

b) solicitação, por meio eletrônico, assinada digitalmente com o uso de certificado ICP-Brasil válido, do tipo A3 ou superior, cujo certificado requisitado seja do mesmo nível de segurança ou inferior; ou

c) por meio de videoconferência, conforme procedimentos e requisitos técnicos definidos em Instrução Normativa da AC Raiz, os quais deverão assegurar nível de segurança equivalente à forma presencial, garantindo a validação das mesmas informações de identificação e biométricas, mediante o emprego de tecnologias eletrônicas seguras de comunicação, interação, documentação e tratamento biométrico.

3.3.2.1 Para certificados de aplicações específicas que utilizem URL, a AC poderá implementar mecanismos automatizado de gerenciamento de certificado (ACME) de forma a preservar a posse ou propriedade da URL (domínio) e a identificação do solicitante, seja pessoa física ou jurídica. O processo automatizado implica as seguintes etapas:

a) .......................................................................................................................

b) a requisição deverá ser acompanhada do certificado da URL solicitada, ainda válido, e o conjunto (requisição + certificado da URL) deve ser assinado com certificado ICP-Brasil, no mínimo do tipo A3, do responsável pelo domínio;

......................................................................................................................................

4.1 ......................................................................................................................

......................................................................................................................................

c) um termo de titularidade assinado digitalmente pelo titular do certificado ou pelo responsável pelo certificado, no caso de certificado de pessoa jurídica, conforme o adendo referente ao TERMO DE TITULARIDADE [4] específico, e, ainda, quando emissão para servidor público da ativa e militar da União, Estados e Distrito Federal pela autoridade designada formalmente pelos órgãos competentes;

d) o disposto na alínea 'b' e a assinatura do termo de titularidade, no caso de AR ELETRÔNICA, por se tratar de procedimento automatizado, sem intervenção de agente de registro, serão regulamentados por Instrução Normativa da AC Raiz; e

e) que na impossibilidade técnica de assinatura digital do termo de titularidade (como certificados de equipamento, aplicação, carimbo de tempo e outros que façam uso de CSR) será aceita a assinatura manuscrita do termo ou assinatura digital do termo com o certificado ICP-Brasil do titular do certificado ou responsável pelo certificado, no caso de certificado de pessoa jurídica. No caso de assinatura manuscrita do termo será necessária a verificação da assinatura contra o documento de identificação.

4.1.1 ...................................................................................................................

......................................................................................................................................

4.9.1.4. A DPC deve observar que todo certificado deverá ter a sua validade verificada, na respectiva LCR ou OCSP, antes de ser utilizado.

4.9.1.5 ...............................................................................................................

.....................................................................................................................................

4.9.7.4 Caso sejam utilizadas frequências de emissão de LCR específicas para as PCs implementadas, as mesmas devem ser descritas nessas PCs, no item correspondente.

4.9.8 ...................................................................................................................

......................................................................................................................................

5.2.1.3 Todos os operadores do sistema de certificação da AC deverão receber treinamento específico antes de obter qualquer tipo de acesso. O tipo e o nível de acesso serão determinados, em documento formal, com base nas necessidades de cada perfil.

5.2.1.4................................................................................................................

.....................................................................................................................................

5.4.1.1 A AC responsável pela DPC deverá registrar em arquivos de auditoria todos os eventos relacionados à segurança do seu sistema de certificação. Entre outros, os seguintes eventos deverão obrigatoriamente estar incluídos em arquivos de auditoria:

.....................................................................................................................................

l) Operações de escrita nesse repositório, quando aplicável.

5.4.1.2.................................................................................................................

......................................................................................................................................

6.2.4.3 A AC não poderá manter cópia de segurança de chave privada de titular de certificado de assinatura digital por ela emitido.

6.2.5 Arquivamento de chave privada

6.2.5.1 Não devem ser arquivadas chaves privadas de assinatura digital.

......................................................................................................................................

6.3.2.1 ................................................................................................................

6.3.2.2 Cada PC implementada pela AC responsável deve definir o período máximo de validade do certificado que define, com base nos requisitos aplicáveis estabelecidos pelo documento REQUISITOS MÍNIMOS PARA AS POLÍTICAS DE CERTIFICADO NA ICP-BRASIL [7].

6.3.2.3 A validade admitida para certificados de AC é limitada à validade do certificado da AC que o emitiu, desde que mantido o mesmo padrão de algoritmo para a geração de chaves assimétricas implementado pela AC hierarquicamente superior.

.......................................................................................................................................

7.1 Perfil do certificado

Todos os certificados emitidos pela AC responsável deverão estar em conformidade com o formato definido pelo padrão ITU X.509 ou ISO/IEC 9594-8, de acordo com o perfil estabelecido na RFC 5280.

7.1.1 Número de versão

Todos os certificados emitidos pela AC responsável deverão implementar a versão 3 de certificado definida no padrão ITU X.509, de acordo com o perfil estabelecido na RFC 5280.

7.1.2 Extensões de certificado

A ICP-Brasil define como obrigatórias as extensões para certificados de AC conforme especificado na Tabela de Perfis de Certificado e LCR, Anexo I do DOC-ICP-04, aprovado pela Resolução CG ICP-Brasil nº 179, de 20 de outubro de 2020.

7.1.3....................................................................................................................

......................................................................................................................................

7.1.4 Formatos de nome

7.1.4.1 O nome da AC titular de certificado, constante do campo "*Subject*", deverá adotar o "*Distinguished Name*" (DN) do padrão ITU X.500/ISO 9594, conforme especificado na Tabela de Perfis de Certificado e LCR, Anexo I do DOC-ICP-04, aprovado pela Resolução CG ICP-Brasil nº 179, de 20 de outubro de 2020.

7.1.5 Restrições de nome

........................................................................................................................................

7.2.2 Extensões de LCR e de suas entradas

Neste item, a DPC deve descrever todas as extensões de LCR utilizadas pela AC responsável e sua criticalidade, conforme especificado na Tabela de Perfis de Certificado e LCR, Anexo I do DOC-ICP-04, aprovado pela Resolução CG ICP-Brasil nº 179, de 20 de outubro de 2020.

7.3 Perfil de OCSP

.......................................................................................................................................

9.3.3.3 A DPC deve informar que os titulares de certificados emitidos para pessoas físicas ou os responsáveis pelo uso de certificados emitidos para pessoas jurídicas, equipamentos ou aplicações, terão as atribuições de geração, manutenção e sigilo de suas respectivas chaves privadas. Além disso, responsabilizam-se pela divulgação ou utilização indevidas dessas mesmas chaves.

9.4 Privacidade da informação pessoal

........................................................................................................................................

9.6.1.6 Revogação

A AC irá revogar certificados da ICP-Brasil por qualquer razão especificada nas normas da ICP-Brasil e nos Princípios e Critérios*WebTrust*." (NR)

**Art. 12.** Ficam aprovadas:

I - a versão 7.2 do documento DOC-ICP-03 - Critérios e Procedimentos para Credenciamento das Entidades Integrantes da ICP-Brasil;

II - a versão 8.2 do documento DOC-ICP-04 - Requisitos Mínimos para as Políticas de Certificados na ICP-Brasil; e

III - a versão 6.5 do documento DOC-ICP-05 - Requisitos Mínimos para as Declarações de Práticas de Certificação das Autoridades Certificadoras da ICP-Brasil.

**Parágrafo único.** A identificação da versão deverá ser atualizada no preâmbulo e incluída no controle de versões do anexo das respectivas Resoluções.

Regras de transição

**Art. 13.** Os certificados digitais dos tipos A1, A2, A3, A4, S1, S2, S3, S4, T3 e T4, com seus perfis e propósitos de uso estabelecidos nos regulamentos da ICP-Brasil anteriores à data de publicação desta Resolução, poderão ser emitidos e utilizados na cadeia de certificação V5 durante toda a sua vigência, até 02 de março de 2029.

**Art. 14.** Poderão ser emitidos certificados digitais dos tipos A1 e A3 na cadeia V10 da AC Raiz da ICP-Brasil até 31 de dezembro de 2026 para uso restrito em aplicações específicas.

**Art. 15.** As entidades com pedido de credenciamento protocolado junto à ICP-Brasil antes da data de publicação deste regulamento deverão estar aderentes a esta Resolução e terão o prazo de até cento e oitenta dias da data de publicação deste regulamento para efetuar os ajustes necessários no pedido de credenciamento, bem como atender ao item 2.2.2.2.1 do Anexo I da Resolução CG ICP-Brasil nº 178, de 20 de outubro de 2020.

**Parágrafo único.** As entidades com pedido de credenciamento deferido pelo ITI e que não tenham consumado o credenciamento na ICP-Brasil poderão optar pela emissão de certificados na cadeia V5 da AC Raiz da ICP-Brasil no prazo de até cento e oitenta dias da data de publicação deste regulamento.

**Art. 16.** As entidades credenciadas na ICP-Brasil que já emitem certificados de equipamentos e aplicações na cadeia V10 terão até cento e oitenta dias, a partir da data de publicação deste regulamento, para incluir as novas políticas de aplicações específicas mediante a realização de credenciamento simplificado a ser definido por instrução normativa do ITI.

**§1º** As entidades credenciadas na ICP-Brasil que já emitem certificados de equipamentos e aplicações na cadeia V5 que migrarem para a cadeia V10 em até cento e oitenta dias da data de publicação deste regulamento realizarão credenciamento simplificado nessa cadeia.

**§2º** Após o período de cento e oitenta dias da data de publicação deste regulamento, a migração estará sujeita a um novo credenciamento.

**Art. 17.** Esta Resolução entra em vigor na data de sua publicação.

ENYLSON FLAVIO MARTINEZ CAMOLESI
