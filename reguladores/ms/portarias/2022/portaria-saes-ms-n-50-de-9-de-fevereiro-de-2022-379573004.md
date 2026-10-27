---
titulo: "PORTARIA SAES/MS Nº 50, DE 9 DE FEVEREIRO DE 2022"
orgao: "Ministério da Saúde/Secretaria de Atenção Especializada à Saúde"
tipo: "Portaria"
numero: "50"
data: 2022-02-09
revogada: null
versao_texto: "publicação original"
publicacao: "DOU de 11/02/2022, seção 1, p. 165"
data_publicacao: 2022-02-11
edicao: "30"
fonte: "https://www.in.gov.br/web/dou/-/portaria-saes/ms-n-50-de-9-de-fevereiro-de-2022-379573004"
sha256_html_fonte: adf8527d4e5a26a2f59ceb9ca28b28ef7127f4679e07e0fc48b6d1324e51c800
baixado_em: 2026-10-20
---
# PORTARIA SAES/MS Nº 50, DE 9 DE FEVEREIRO DE 2022

PORTARIA SAES/MS Nº 50, DE 9 DE FEVEREIRO DE 2022

Institui os Modelos de Informação Registro de Prescrição de Medicamentos e Registro de Dispensação de Medicamentos.

O Secretário de Atenção Especializada à Saúde, no uso de suas atribuições,

Considerando a Lei nº 8.080, de 19 de setembro de 1990, que dispõe sobre as condições para a promoção, proteção e recuperação da saúde, a organização e o funcionamento dos serviços correspondentes e dá outras providências;

Considerando o Decreto nº 10.046, de 9 de outubro de 2019, que dispõe sobre a governança no compartilhamento de dados no âmbito da administração pública federal e institui o Cadastro Base do Cidadão e o Comitê Central de Governança de Dados;

Considerando a Portaria GM/MS nº 3.632, de 21 de dezembro de 2020, que altera a Portaria de Consolidação GM/MS nº 1, de 28 de setembro de 2017, para instituir a Estratégia de Saúde Digital para o Brasil 2020-2028 (ESD28);

Considerando a Portaria GM/MS nº 1.434, de 28 de maio de 2020, que institui o Programa Conecte SUS e altera a Portaria de Consolidação GM/MS nº 1, de 28 de setembro de 2017, para instituir a Rede Nacional de Dados em Saúde e dispor sobre a adoção de padrões de interoperabilidade em saúde;

Considerando a Portaria GM/MS nº 1.768, de 30 de julho de 2021, que altera o Anexo XLII da Portaria de Consolidação GM/MS nº 2, de 28 de setembro de 2017, para dispor sobre a Política Nacional de Informação e Informática em Saúde (PNIIS);

Considerando a Portaria GM/MS nº 535, de 25 de março de 2021, que altera a Portaria de Consolidação GM/MS nº 1, de 28 de setembro de 2017, para instituir o Comitê Gestor de Saúde Digital (CGSD);

Considerando a necessidade de garantir a troca da informação assistencial entre os diversos pontos de atenção à saúde, por meio de modelos clínicos capazes de garantir a continuidade do cuidado durante toda a vida do cidadão, apoiar os profissionais de saúde para uma assistência mais resolutiva e segura, disponibilizar ao paciente informações sobre seu estado de saúde enquanto protagonista do seu cuidado, e garantir informações de qualidade para a tomada de decisão em saúde;

Considerando a aprovação dos Modelos de Informação de Registro de Prescrição de Medicamentos e Registro de Dispensação de Medicamentos na 4ª Reunião Extraordinária do Comitê Gestor da Saúde Digital, realizada no dia 19 de novembro de 2021; e

Considerando que compete ao Departamento de Regulação, Avaliação e Controle (DRAC/SAES/MS) gerir o conteúdo e a estrutura dos modelos de informação, as regras de negócio e as terminologias administrativas e clínicas da atenção à saúde relacionadas com ações, serviços de saúde e estabelecimentos de saúde, de atendimentos assistenciais e correlatos, de acordo com o art. 24 do Decreto nº 9.795, de 17 de maio de 2019, constante do NUP/SEI 25000.175382/2021-98, resolve:

**Art. 1º** Ficam instituídos os seguintes documentos clínicos: Registro de Prescrição de Medicamentos (RPM) e Registro de Dispensação de Medicamentos (RDM). Os conteúdos e as estruturas das informações que compõem os referidos documentos clínicos estão descritos nos modelos de informação constantes nos anexos a esta Portaria.

**§ 1º** RPM é o registro clínico objetivo sobre os medicamentos prescritos por profissional de saúde habilitado, compreendendo a prescrição em âmbito de atendimento ambulatorial e de medicamentos não sujeitos a controle especial - Anexo A.

**§ 2º** RDM é o registro de dados de um atendimento de dispensação de medicamentos não sujeitos a controle especial, dispensados em âmbito de atendimento ambulatorial por unidades públicas de saúde, unidades privadas financiadas pelo SUS ou pelo Programa Farmácia Popular do Brasil - Anexo B.

**Art. 2º** A criação dos modelos computacionais do RPM e RDM e sua implantação técnica na Rede Nacional de Dados Saúde (RNDS) fica a cargo do Departamento de Informática do SUS (DATASUS/SE/MS), conforme competência definida na legislação em vigor.

**Art. 3º** Ao final da execução de piloto do Projeto Prescrição Eletrônica e Controle de Dispensação de Medicamentos. Foco: Farmácia Popular, os modelos RPM e RDM serão de adoção obrigatória em todo o sistema de saúde do País, abrangendo as pessoas físicas ou jurídicas que realizem atenção à saúde nas esferas pública, suplementar e privada.

**Art. 4º** Esta Portaria entra em vigor na data de sua publicação.

SERGIO YOSHIMASA OKANE

ANEXO A

Modelo de Informação

Registro de Prescrição de Medicamentos (RPM)

1\. Introdução

A prescrição de medicamentos é documento de valor legal, instrumento utilizado pelos profissionais da área da saúde habilitados para apontar um tratamento e instruir o paciente sobre sua condução. É composta pela indicação de medicamentos e sua orientação de uso, detalhando de forma clara e objetiva seu modo de utilização e período do tratamento.

O registro de prescrição de medicamentos, por se tratar de ato posterior ao diagnóstico clínico, compreende-se não somente como documento clínico de intervenção, mas aponta também para a decisão clínica tomada por meio do tratamento indicado. Tal é a importância da prescrição que essa, por si só, pode indicar a condição clínica do paciente, compondo importante registro de seu estado atual e seu histórico clínico.

1\. Objetivo

Estabelecer a estrutura do modelo de informação do RPM, no intuito de estabelecer consenso nacional sobre os dados indispensáveis à realização do registro de prescrição de medicamentos não sujeitos a controle especial.

2.1 Objetivos específicos

\- Garantir que um conjunto mínimo de informações clínicas padronizadas possa ser encaminhado e processado para múltiplos sistemas de informação em saúde, apoiando a comunicação entre os diversos níveis de atenção e subsidiando a continuidade do cuidado do indivíduo;

\- Melhorar a qualidade da atenção em saúde e a segurança do indivíduo;

\- Fortalecer a Rede Nacional de Dados em Saúde (RNDS) e a qualidade das informações prestadas;

\- Facilitar a coleta, agregação, tratamento e análise de dados para tomada de decisão e produção de conhecimento.

3\. Escopo

Este documento provê aos desenvolvedores a especificação do modelo de informação do Registro de Prescrição de Medicamentos e se aplica a todas as partes interessadas no processo de continuidade da assistência do indivíduo, incluindo:

\- Estabelecimentos de saúde em processo de planejamento, implementação ou atualização de sistemas de informação de saúde;

\- Desenvolvedores de sistemas de informação de saúde;

\- Gestores e realizadores de políticas públicas, especialistas clínicos, gerentes de informática em saúde e equipes de suporte, bem como integradores de sistemas;

\- Profissionais de saúde;

\- Profissionais de Tecnologia da Informação e Comunicação (TIC);

\- Usuários dos serviços de saúde e suas entidades representativas.

4.Termos, definições e abreviaturas

4.1. Termos e definições

Para os efeitos deste documento, aplicam-se os seguintes termos e definições.

Cadastro Nacional de Estabelecimentos de Saúde (CNES)

Sistema de informação oficial de cadastramento de informações de todos os estabelecimentos de saúde no País, independentemente de sua natureza jurídica ou de integrarem o Sistema Único de Saúde (SUS). Trata-se do cadastro oficial do Ministério da Saúde (MS) no tocante à realidade da capacidade instalada e mão-de-obra assistencial de saúde no Brasil em estabelecimentos de saúde públicos ou privados, com convênio SUS ou não.

Cartão Nacional de Saúde (CNS)

Número de identificação do usuário do SUS. Esse número é armazenado no Cadastro Nacional de Usuários do SUS (CADSUS) e permite a identificação em âmbito nacional.

Concentração do medicamento

Quantidade do princípio farmacologicamente ativo contida no medicamento por unidade de dosagem farmacêutica. Nas formas sólidas (comprimido, cápsulas, drágeas, óvulos, adesivos transdérmicos, pó liofilizado para injetável e supositórios), a concentração é expressa por unidade de peso (mg, g, etc.). Nas formas líquidas ou semissólidas, a concentração será expressa em mg/mL, mg/g ou percentual, entre outras.

Dose

Quantidade de medicamento utilizada a cada administração.

Estabelecimento de saúde

Espaço físico delimitado e permanente onde são realizados ações e serviços de saúde humana sob responsabilidade técnica.

Medicamento

Produto farmacêutico, tecnicamente obtido ou elaborado, com finalidade curativa, paliativa ou para fins de diagnóstico.

Posologia

Forma de utilização de um medicamento compreendendo a dose utilizada, via de administração, período de tratamento e frequência de administrações.

Profissional prescritor

Indivíduo com profissão de saúde habilitada para a realização de prescrição de medicamentos.

Terminologia

Sistematização e representação linguística de um conceito, ou seja, uma unidade de conhecimento criada por uma combinação única de características para fornecer um vocabulário sistematizado e controlado. No caso específico da saúde, trata de informações clinicamente relevantes que podem ser usadas durante a entrada de dados para maior precisão que o obtido por texto livre que não pode ser interpretado automaticamente por um sistema.

Unidade de medida da concentração

As unidades de medida das concentrações de medicamentos são expressas pelo menor volume ou peso e devem ser expressas seguindo a nomenclatura das unidades de medidas internacionais.

Via de administração

Modo pelo qual o medicamento entra em contato com o organismo.

4.2. Abreviaturas

<table>    <tbody>     <tr>      <td rowspan="1" colspan="2"></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>ANVISA</p></td>      <td rowspan="1" colspan="1"><p>Agência Nacional de Vigilância Sanitária</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CADSUS</p></td>      <td rowspan="1" colspan="1"><p>Sistema de Cadastramento de usuários do SUS</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CATMAT</p></td>      <td rowspan="1" colspan="1"><p>Catálogo de Materiais do Governo Federal</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CBO</p></td>      <td rowspan="1" colspan="1"><p>Classificação Brasileira de Ocupações</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CNS</p></td>      <td rowspan="1" colspan="1"><p>Cartão Nacional de Saúde</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CNES</p></td>      <td rowspan="1" colspan="1"><p>Cadastro Nacional de Estabelecimentos de Saúde</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CNPJ</p></td>      <td rowspan="1" colspan="1"><p>Cadastro Nacional de Pessoas Jurídicas</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>COREN</p></td>      <td rowspan="1" colspan="1"><p>Conselho Regional de Enfermagem</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CPF</p></td>      <td rowspan="1" colspan="1"><p>Cadastro de Pessoa Física</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CRF</p></td>      <td rowspan="1" colspan="1"><p>Conselho Regional de Farmácia</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CRM</p></td>      <td rowspan="1" colspan="1"><p>Conselho Regional de Medicina</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CRN</p></td>      <td rowspan="1" colspan="1"><p>Conselho Regional de Nutrição</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CRO</p></td>      <td rowspan="1" colspan="1"><p>Conselho Regional de Odontologia</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>IBGE</p></td>      <td rowspan="1" colspan="1"><p>Instituto Brasileiro de Geografia e Estatística</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>ISO</p></td>      <td rowspan="1" colspan="1"><p><em>International Organization for Standardization</em>(Organização Internacional de Padronização)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>OBM</p></td>      <td rowspan="1" colspan="1"><p>Ontologia Brasileira de Medicamentos</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>RPM</p></td>      <td rowspan="1" colspan="1"><p>Registro de Prescrição de Medicamentos</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>SUS</p></td>      <td rowspan="1" colspan="1"><p>Sistema Único de Saúde</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>UF</p></td>      <td rowspan="1" colspan="1"><p>Unidade da Federação</p></td>     </tr>    </tbody>   </table>

5\. Usos

O Registro de Prescrição de Medicamentos é um documento essencial para:

Apoiar a comunicação das informações de registros de prescrições entre os diversos níveis de atenção de modo eficiente, efetivo e a tempo, contribuindo para uma atenção coordenada entre os cuidadores do indivíduo e apoiando a continuidade dos seus cuidados;

Melhorar a qualidade da atenção em saúde e a segurança para o indivíduo com informações qualificadas, completas e oportunas que contribuam para uma conduta mais adequada às necessidades individuais de cada indivíduo;

Garantir que um conjunto mínimo de informações clínicas padronizadas possa ser encaminhado e processado para múltiplos sistemas de informações em saúde, facilitando a agregação e análise desses dados para tomada de decisão e produção de conhecimento;

Reduzir o custo com entradas manuais, integrações, mapeamento de sistemas independentes e manutenção dos sistemas de informação em saúde;

Promover a simplificação e padronização das comunicações sobre os eventos de saúde entre os diversos envolvidos na atenção à saúde;

Alimentar o registro pessoal de saúde do indivíduo;

Dar subsídios ao uso secundário da informação.

6\. Modelo de informação

A Tabela 1 apresenta os elementos que são partes do modelo de informação do Registro de Prescrição de Medicamentos. O método que descreve o modelo é o seguinte:

\- Coluna 1 (Nível): indica a relação de dependência do elemento aos demais. Um número maior significa que aquele item depende ou está subordinado ao de número menor e anterior a ele no modelo. Assim, um elemento de nível 2 é subitem de um elemento de nível 1, um de nível 3 é subitem de um de nível 2 e assim sucessivamente.

\- Coluna 2 (Ocorrência): demonstra a obrigatoriedade e a quantidade de ocorrências do elemento.

\- [0..] - Indica que o elemento é opcional.

\- [1..] - Indica que o elemento é obrigatório.

\- [..1] - Indica que o elemento só pode ocorrer uma única vez.

\- [..N] - Indica que o elemento pode ocorrer várias vezes.

\- Coluna 3 (Seção/Item): descrição do elemento ou de um agrupador de elementos (seção).

\- Coluna 4 (Tipo de Dados): demonstra a forma de representar o elemento.

\- Coluna 5 (Conceito/Observações): conceitua ou esclarece a forma de utilizar o elemento.

Tabela 1 - Modelo de informação do Registro de Prescrição de Medicamentos

<table>    <tbody>     <tr></tr>     <tr>      <td rowspan="1" colspan="1"><p>Nível</p></td>      <td rowspan="1" colspan="1"><p>Ocorrência</p></td>      <td rowspan="1" colspan="1"><p>Seção/Item</p></td>      <td rowspan="1" colspan="1"><p>Tipo de Dados</p></td>      <td rowspan="1" colspan="1"><p>Conceito/Observações (Regras de negócio)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>1</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Identificação do indivíduo</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p>RN01: O documento deve trazer um identificador nacional do indivíduo. Se não houver nenhum dos dois possíveis (CNS ou CPF), dever ser obrigatório o preenchimento do bloco Identificação por dados demográficos.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Identificador Nacional do Indivíduo</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Identificação unívoca dos usuários das ações e serviços de saúde, mediante número único válido em todo o território nacional, sendo:</p><p>- Cartão Nacional de Saúde (CNS);</p><p>- Cadastro de Pessoa Física (CPF).</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p>RN02: A validação do identificador nacional do indivíduo deve ser feita junto ao CADSUS.</p><p>RN03: Se o campo vier preenchido com CPF e o indivíduo não possuir CNS correspondente, necessita ser criado.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Identificação por dados demográficos</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p>RN04: Na hipótese de não ser possível a identificação por um dos identificadores nacionais acima, os campos do bloco de dados demográficos serão usados como parâmetros de pesquisa para a identificação do indivíduo e eventual atribuição de um CNS.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Nome completo</p></td>      <td rowspan="1" colspan="1"><p>Sequência de caracteres alfanuméricos</p></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Nome social</p></td>      <td rowspan="1" colspan="1"><p>Sequência de caracteres alfanuméricos</p></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Nome completo da mãe</p></td>      <td rowspan="1" colspan="1"><p>Sequência de caracteres alfanuméricos</p></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Data de nascimento</p></td>      <td rowspan="1" colspan="1"><p>Data</p></td>      <td rowspan="1" colspan="1"><p>Conforme ISO 8601.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Sexo</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado</p></td>      <td rowspan="1" colspan="1"><p>Masculino; Feminino; Ignorado</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>País de nascimento</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado por terminologia externa: IBGE</p></td>      <td rowspan="1" colspan="1"><p>RN05: Obrigatório se país estrangeiro.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Município de Nascimento</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado por terminologia externa: IBGE</p></td>      <td rowspan="1" colspan="1"><p>RN06: Preenchido somente se o país de nascimento for Brasil.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Endereço</p></td>      <td rowspan="1" colspan="1"><p>Sequência de caracteres alfanuméricos</p></td>      <td rowspan="1" colspan="1"><p>RN07: Preenchido somente se o país de nascimento for Brasil.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>1</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Caracterização do atendimento</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Identificador do Estabelecimento de saúde prescritor</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Identificação unívoca do estabelecimento prescritor, mediante número único válido em todo o território nacional, sendo:</p><p>- Cadastro Nacional de Estabelecimentos de Saúde (CNES);</p><p>- Cadastro Nacional de Pessoas Jurídicas (CNPJ).</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Endereço do estabelecimento ou do profissional prescritor</p></td>      <td rowspan="1" colspan="1"><p>Sequência de caracteres alfanuméricos</p></td>      <td rowspan="1" colspan="1"><p>RN08: Obrigatório se o campo Identificador do Estabelecimento de saúde prescritor não estiver preenchido.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Data e hora da prescrição</p></td>      <td rowspan="1" colspan="1"><p>Data</p></td>      <td rowspan="1" colspan="1"><p>Conforme ISO 8601.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Profissional prescritor</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Nome do profissional prescritor</p></td>      <td rowspan="1" colspan="1"><p>Sequência de caracteres alfanuméricos</p></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Conselho do profissional prescritor</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado</p></td>      <td rowspan="1" colspan="1"><p>Indica a entidade de conselho profissional do prescritor - CRM, CRF, CRO, CRN, COREN</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>UF do conselho do profissional prescritor</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado por terminologia externa: IBGE</p></td>      <td rowspan="1" colspan="1"><p>Indica a UF do conselho do profissional prescritor</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Número de conselho do profissional prescritor</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Número do conselho do profissional prescritor</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Identificador do profissional prescritor</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Identificação unívoca do profissional prescritor, mediante número único válido em todo o território nacional, sendo:</p><p>- Cartão Nacional de Saúde (CNS);</p><p>- Cadastro de Pessoa Física (CPF).</p><p>RN09: Validar junto ao CADSUS.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Ocupação do profissional prescritor</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado por terminologia externa: CBO MTE</p></td>      <td rowspan="1" colspan="1"><p>Atividade desempenhada pelo profissional que realizou a emissão da prescrição.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>1</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Prescrição no atendimento</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Medicamentos prescritos no atendimento (não estruturado)</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Descrição da prescrição</p></td>      <td rowspan="1" colspan="1"><p>Texto livre</p></td>      <td rowspan="1" colspan="1"><p>Descrição da prescrição de medicamentos de forma livre, em texto, podendo conter vários medicamentos. O profissional prescritor deverá descrever todos os campos necessários a uma prescrição, entre outros elementos relevantes.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Medicamentos prescritos no atendimento (estruturado)</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Nome e versão da terminologia de medicamentos</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado</p></td>      <td rowspan="1" colspan="1"><p>Lista de registro de medicamentos da ANVISA</p><p>Ontologia Brasileira de Medicamentos (OBM)</p><p>Catálogo de Materiais do Governo Federal (CATMAT)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>4</p></td>      <td rowspan="1" colspan="1"><p>[1..N]</p></td>      <td rowspan="1" colspan="1"><p>Medicamento</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado por terminologia externa</p></td>      <td rowspan="1" colspan="1"><p>Indica o nome do princípio ativo, concentração, unidade de medida e forma farmacêutica do medicamento prescrito.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>5</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Via de administração</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado por terminologia externa</p></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>5</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Posologia</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>6</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Posologia não estruturada</p></td>      <td rowspan="1" colspan="1"><p>Texto livre</p></td>      <td rowspan="1" colspan="1"><p>Descrição da posologia de medicamento de forma livre, em texto. O profissional prescritor deverá descrever todos os campos necessários a uma posologia, entre outros elementos relevantes.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>6</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Posologia estruturada</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>7</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Quantidade da Dose</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Quantidade da unidade de consumo do medicamento prescrito a cada dose.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>7</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Unidade de consumo da dose</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado por terminologia externa</p></td>      <td rowspan="1" colspan="1"><p>Unidade de consumo do medicamento prescrito (ex.: comprimido, cápsula, aplicação, mL, gota, copo dosador, infusão etc.).</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>7</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Frequência de uso do medicamento</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>8</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Dose única</p></td>      <td rowspan="1" colspan="1"><p>Booleano</p></td>      <td rowspan="1" colspan="1"><p>Sim; Não (verdadeiro/falso)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>8</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Uso contínuo</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p>RN10: preenchido obrigatoriamente se "Dose Única" = não/falso.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>9</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Uso se necessário</p></td>      <td rowspan="1" colspan="1"><p>Booleano</p></td>      <td rowspan="1" colspan="1"><p>Sim; Não (verdadeiro/falso)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>10</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Descrição da necessidade de uso do medicamento</p></td>      <td rowspan="1" colspan="1"><p>Texto livre</p></td>      <td rowspan="1" colspan="1"><p>Descrição de uso do medicamento indicado para o caso de uma necessidade específica (ex.: dor, febre, após tratamento etc.)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>9</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Intervalo em horas de cada dose do medicamento</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Intervalo, em horas, de cada uso do medicamento</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>9</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Frequência de doses do medicamento</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>10</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Repetições de dose para uma mesma unidade de tempo</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Número de doses a cada uso do medicamento (ex.: 1x, 2x, 3x 4x etc.)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>10</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Intervalo entre doses</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Descritor quantitativo da unidade de tempo entre doses</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>10</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Unidade de tempo entre doses</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado</p></td>      <td rowspan="1" colspan="1"><p>Unidade de tempo entre doses (ex.: hora, dia, semana, mês etc.).</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>9</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Turno</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>10</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Turno do dia</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado</p></td>      <td rowspan="1" colspan="1"><p>Manhã, tarde, noite.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>10</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Intervalo entre doses</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Descritor quantitativo da unidade de tempo entre doses</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>10</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Unidade de tempo entre doses</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado</p></td>      <td rowspan="1" colspan="1"><p>Unidade de tempo entre doses (ex.: hora, dia, semana, mês, ano).</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>7</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Quantidade de medicamento prescrito</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>8</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Quantidade a ser dispensada por atendimento</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>8</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Unidade de medida do medicamento</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado</p></td>      <td rowspan="1" colspan="1"><p>Unidade de medida do medicamento prescrito (ex.: comprimido, cápsula, frasco, caixa etc.).</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>7</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Duração de uso do medicamento</p></td>      <td rowspan="1" colspan="1"><p>Caracteres alfanuméricos</p></td>      <td rowspan="1" colspan="1"><p>Duração conforme ISO 8601</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>7</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Total do tratamento</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Quantidade total de medicamento prescrito.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>7</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Orientações sobre o uso do medicamento</p></td>      <td rowspan="1" colspan="1"><p>Texto livre</p></td>      <td rowspan="1" colspan="1"></td>     </tr>    </tbody>   </table>

ANEXO B

Modelo de Informação

Registro de Dispensação de Medicamentos (RDM)

1\. Introdução

A dispensação de medicamentos se caracteriza pelo ato de fornecimento ao consumidor de drogas, medicamentos, insumos farmacêuticos e correlatos, a título remunerado ou não, sendo privativa de farmácias, drogarias, postos de medicamentos, unidades volantes ou dispensário de medicamentos. A dispensação correta de um medicamento é essencial para a promoção da saúde do paciente e do uso racional de medicamentos, impedindo reações adversas evitáveis e reduzindo o risco de insucesso de um tratamento farmacológico.

O registro de dispensação de medicamentos em unidades públicas de saúde, em unidades privadas financiadas pelo SUS ou de produtos oferecidos pelo Programa Farmácia Popular do Brasil provê informações acerca do consumo de medicamentos no SUS, podendo auxiliar no controle de gastos do Sistema de Saúde, na continuidade do cuidado ao paciente e no fortalecimento do ciclo da Assistência Farmacêutica no País.

2\. Objetivo

Estabelecer a estrutura do modelo de informação do Registro de Dispensação de Medicamentos, no intuito de estabelecer consenso nacional sobre os dados indispensáveis à realização do registro de dispensação de medicamentos não sujeitos a controle especial, dispensados em âmbito de atendimento ambulatorial por unidades públicas de saúde, unidades privadas financiadas pelo SUS ou pelo Programa Farmácia Popular do Brasil.

2.1. Objetivos específicos

\- Garantir que um conjunto mínimo de informações clínicas padronizadas possa ser encaminhado e processado para múltiplos sistemas de informações em saúde apoiando a comunicação entre os diversos níveis de atenção e subsidiando a continuidade do cuidado do indivíduo;

\- Melhorar a qualidade da atenção em saúde e a segurança do indivíduo;

\- Fortalecer a Rede Nacional de Dados em Saúde (RNDS) e a qualidade das informações prestadas;

\- Facilitar a agregação e a análise de dados para tomada de decisão e produção de conhecimento;

\- Subsidiar o Ministério da Saúde com dados sobre o consumo de medicamentos e produtos para a saúde, fortalecendo o ciclo da Assistência Farmacêutica no SUS.

3\. Escopo

Este documento provê aos desenvolvedores a especificação do modelo de informação do Registro de Dispensação de Medicamentos e se aplica a todas as partes interessadas no processo de continuidade da assistência do indivíduo, incluindo:

\- Estabelecimentos de saúde em processo de planejamento, implementação ou atualização de sistemas de informação de saúde;

\- Desenvolvedores de sistemas de informação de saúde;

\- Gestores e realizadores de políticas públicas, especialistas clínicos, gerentes de informática em saúde e equipes de suporte, bem como integradores de sistemas;

\- Profissionais de saúde;

\- Profissionais de Tecnologia da Informação e Comunicação (TIC);

\- Usuários dos serviços de saúde e suas entidades representativas.

4.Termos, definições e abreviaturas

4.1. Termos e definições

Para os efeitos deste documento, aplicam-se os seguintes termos e definições.

Cadastro Nacional de Estabelecimentos de Saúde (CNES)

Sistema de informação oficial de cadastramento de informações de todos os estabelecimentos de saúde no País, independentemente de sua natureza jurídica ou de integrarem o Sistema Único de Saúde (SUS). Trata-se do cadastro oficial do Ministério da Saúde (MS) no tocante à realidade da capacidade instalada e mão-de-obra assistencial de saúde no Brasil em estabelecimentos de saúde públicos ou privados, com convênio SUS ou não.

Cartão Nacional de Saúde (CNS)

Número de identificação do usuário do SUS. Esse número é armazenado no Cadastro Nacional de Usuários do SUS e permite a identificação em âmbito nacional.

Código serial

Código individual contido no Identificador Único de Medicamento (IUM), composto de até 20 caracteres alfanuméricos gerado por algoritmo pseudorrandômico - parte do Sistema Nacional de Controle de Medicamentos (SNCM) da ANVISA.

Concentração do medicamento

Quantidade do princípio farmacologicamente ativo contida no medicamento por unidade de dosagem farmacêutica. Nas formas sólidas (comprimido, cápsulas, drágeas, óvulos, adesivos transdérmicos, pó liofilizado para injetável e supositórios) a concentração é expressa por unidade de peso (mg, g, etc.). Nas formas líquidas ou semissólidas, a concentração será expressa em mg/mL, mg/g ou percentual.

Estabelecimento de saúde

Espaço físico delimitado e permanente onde são realizados as ações e os serviços de saúde humana sob responsabilidade técnica.

Identificador Único de Medicamento (IUM)

Identificador composto de uma série de caracteres numéricos, alfanuméricos, criado através de padrões de identificação e codificação, que permita a identificação individualizada, exclusiva e inequívoca de cada embalagem comercial do medicamento - parte do Sistema Nacional de Controle de Medicamentos (SNCM) da ANVISA.

Medicamento

Produto farmacêutico, tecnicamente obtido ou elaborado, com finalidade curativa, paliativa ou para fins de diagnóstico.

Modalidade da dispensação

Indica a modalidade de estabelecimento ou financiamento na qual é realizada o registro de dispensação.

Profissional prescritor

Indivíduo com profissão de saúde habilidade para a realização de prescrição de medicamentos.

Profissional dispensador

Indivíduo que realiza o procedimento de dispensação de medicamentos.

Terminologia

Sistematização e representação linguística de um conceito, ou seja, uma unidade de conhecimento criada por uma combinação única de características para fornecer um vocabulário sistematizado e controlado. No caso específico da saúde, trata de informações clinicamente relevantes que podem ser usadas durante a entrada de dados para maior precisão que o obtido por texto livre que não pode ser interpretado automaticamente por um sistema.

Unidade de medida da concentração

As unidades de medida das concentrações de medicamentos são expressas pelo menor volume ou peso e devem ser expressas seguindo a nomenclatura das unidades de medidas internacionais.

4.2. Abreviaturas

<table>    <tbody>     <tr>      <td rowspan="1" colspan="2"></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>AMPP</p></td>      <td rowspan="1" colspan="1"><p><em>Actual Medicinal Product Pack</em>(Produto Medicinal Comercial com Apresentação)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>ANVISA</p></td>      <td rowspan="1" colspan="1"><p>Agência Nacional de Vigilância Sanitária</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CADSUS</p></td>      <td rowspan="1" colspan="1"><p>Sistema de Cadastramento de usuários do SUS</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CATMAT</p></td>      <td rowspan="1" colspan="1"><p>Catálogo de Materiais do Governo Federal</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CBO</p></td>      <td rowspan="1" colspan="1"><p>Classificação Brasileira de Ocupações</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CNS</p></td>      <td rowspan="1" colspan="1"><p>Cartão Nacional de Saúde</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CNES</p></td>      <td rowspan="1" colspan="1"><p>Cadastro Nacional de Estabelecimentos de Saúde</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CNPJ</p></td>      <td rowspan="1" colspan="1"><p>Cadastro Nacional de Pessoas Jurídicas</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>COREN</p></td>      <td rowspan="1" colspan="1"><p>Conselho Regional de Enfermagem</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CPF</p></td>      <td rowspan="1" colspan="1"><p>Cadastro de Pessoa Física</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CRF</p></td>      <td rowspan="1" colspan="1"><p>Conselho Regional de Farmácia</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CRM</p></td>      <td rowspan="1" colspan="1"><p>Conselho Regional de Medicina</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CRN</p></td>      <td rowspan="1" colspan="1"><p>Conselho Regional de Nutrição</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>CRO</p></td>      <td rowspan="1" colspan="1"><p>Conselho Regional de Odontologia</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>GTIN</p></td>      <td rowspan="1" colspan="1"><p><em>Global Trade Item Number</em>(Número Global de Item Comercial)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>IBGE</p></td>      <td rowspan="1" colspan="1"><p>Instituto Brasileiro de Geografia e Estatística</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>ISO</p></td>      <td rowspan="1" colspan="1"><p><em>International Organization for Standardization</em>(Organização Internacional de Padronização)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>IUM</p></td>      <td rowspan="1" colspan="1"><p>Identificador Único de Medicamento</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>OBM</p></td>      <td rowspan="1" colspan="1"><p>Ontologia Brasileira de Medicamentos</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>RDM</p></td>      <td rowspan="1" colspan="1"><p>Registro de Dispensação de Medicamentos</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>SNCM</p></td>      <td rowspan="1" colspan="1"><p>Sistema Nacional de Controle de Medicamentos</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>SUS</p></td>      <td rowspan="1" colspan="1"><p>Sistema Único de Saúde</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>UF</p></td>      <td rowspan="1" colspan="1"><p>Unidade da Federação</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>XML</p></td>      <td rowspan="1" colspan="1"><p>Extensible Markup Language</p></td>     </tr>    </tbody>   </table>

5.Usos

O Registro de Dispensação de Medicamentos é um documento essencial para:

Apoiar a comunicação das informações de registros de prescrições entre os diversos níveis de atenção de modo eficiente, efetivo e a tempo, contribuindo para uma atenção coordenada entre os cuidadores do indivíduo e apoiando a continuidade dos seus cuidados;

Melhorar a qualidade da atenção em saúde e a segurança para o indivíduo com informações qualificadas, completas e oportunas que contribuam para uma conduta mais adequada às necessidades individuais de cada indivíduo;

Garantir que um conjunto mínimo de informações clínicas padronizadas possa ser encaminhado e processado para múltiplos sistemas de informações em saúde, facilitando a agregação e análise desses dados para tomada de decisão e produção de conhecimento;

Reduzir o custo com entradas manuais, integrações, mapeamento de sistemas independentes e manutenção dos sistemas de informação em saúde;

Promover a simplificação e padronização das comunicações sobre os eventos de saúde entre os diversos envolvidos na atenção à saúde;

Alimentar o registro pessoal de saúde do indivíduo;

Dar subsídios ao uso secundário da informação.

6.Modelo de informação

A Tabela 1 apresenta os elementos que são partes do modelo de informação do Registro de Dispensação de Medicamentos. O método que descreve o modelo é o seguinte:

\- Coluna 1 (Nível): indica a relação de dependência do elemento aos demais. Um número maior significa que aquele item depende ou está subordinado ao de número menor e anterior a ele no modelo. Assim, um elemento de nível 2 é subitem de um elemento de nível 1, um de nível 3 é subitem de um de nível 2 e assim sucessivamente.

\- Coluna 2 (Ocorrência): demonstra a obrigatoriedade e a quantidade de ocorrências do elemento.

\- [0..] - Indica que o elemento é opcional.

\- [1..] - Indica que o elemento é obrigatório.

\- [..1] - Indica que o elemento só pode ocorrer uma única vez.

\- [..N] - Indica que o elemento pode ocorrer várias vezes.

\- Coluna 3 (Seção/Item): descrição do elemento ou de um agrupador de elementos (seção).

\- Coluna 4 (Tipo de Dados): demonstra a forma de representar o elemento.

\- Coluna 5 (Conceito/Observações): conceitua ou esclarece a forma de utilizar o elemento.

Tabela 1 - Modelo de informação do Registro de Dispensação de Medicamentos

<table>    <tbody>     <tr></tr>     <tr>      <td rowspan="1" colspan="1"><p>Nível</p></td>      <td rowspan="1" colspan="1"><p>Ocorrência</p></td>      <td rowspan="1" colspan="1"><p>Seção/Item</p></td>      <td rowspan="1" colspan="1"><p>Tipo de Dados</p></td>      <td rowspan="1" colspan="1"><p>Conceito/Observações (Regras de negócio)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>1</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Identificação do registro de prescrição eletrônica</p></td>      <td rowspan="1" colspan="1"><p>Sequência de caracteres alfanuméricos</p></td>      <td rowspan="1" colspan="1"><p>RN01: A identificação do registro de prescrição eletrônica enviada para a RNDS - traz as informações de "Identificação do indivíduo", "Data da Prescrição", "Profissional Prescritor" e "Medicamento ou Produto".</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>1</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Identificação do indivíduo</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p>RN02: preenchimento obrigatório se a identificação do registro de prescrição eletrônica não for informada.</p><p>RN03: O documento deve trazer um identificador nacional do indivíduo. Se não houver nenhum dos dois possíveis (CNS ou CPF), dever ser obrigatório o preenchimento do bloco Identificação por dados demográficos.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Identificador Nacional do Indivíduo</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Identificação unívoca dos usuários das ações e serviços de saúde, mediante número único válido em todo o território nacional, sendo:</p><p>- Cartão Nacional de Saúde (CNS).</p><p>- Cadastro de Pessoa Física (CPF).</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p>RN04: A validação do identificador nacional do indivíduo deve ser feita junto ao CADSUS.</p><p>RN05: Se o campo vier preenchido com CPF e o indivíduo não possuir CNS correspondente, necessita ser criado.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Identificação por dados demográficos</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p>RN06: Na hipótese de não ser possível a identificação por um dos identificadores nacionais acima, os campos do bloco de dados demográficos serão usados como parâmetros de pesquisa para a identificação do indivíduo e eventual atribuição de um CNS.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Nome completo</p></td>      <td rowspan="1" colspan="1"><p>Sequência de caracteres alfanuméricos</p></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Nome social</p></td>      <td rowspan="1" colspan="1"><p>Sequência de caracteres alfanuméricos</p></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Nome completo da mãe</p></td>      <td rowspan="1" colspan="1"><p>Sequência de caracteres alfanuméricos</p></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Data de nascimento</p></td>      <td rowspan="1" colspan="1"><p>Data</p></td>      <td rowspan="1" colspan="1"><p>Conforme ISO 8601.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Sexo</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado</p></td>      <td rowspan="1" colspan="1"><p>Masculino; Feminino; Ignorado</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>País de nascimento</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado por terminologia externa: IBGE</p></td>      <td rowspan="1" colspan="1"><p>RN07: Obrigatório se país estrangeiro.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Município de Nascimento</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado por terminologia externa: IBGE</p></td>      <td rowspan="1" colspan="1"><p>RN08: Preenchido somente se o país de nascimento for Brasil.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>1</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Caracterização do atendimento</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Modalidade da dispensação</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado</p></td>      <td rowspan="1" colspan="1"><p>Representa em qual modalidade de estabelecimento ou financiamento a dispensação está sendo realizada:</p><p>-Unidade de saúde pública ou privada, com pagamento pelo SUS;</p><p>-Drogaria comercial, com pagamento (gratuidade de copagamento) pelo Programa Farmácia Popular do Brasil.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Identificador do Estabelecimento de Saúde Dispensador</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Identificação unívoca do estabelecimento, dispensador, mediante número único válido em todo o território nacional, sendo:</p><p>- Cadastro Nacional de Estabelecimentos de Saúde (CNES);</p><p>- Cadastro Nacional de Pessoas Jurídicas (CNPJ)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Data da prescrição</p></td>      <td rowspan="1" colspan="1"><p>Data</p></td>      <td rowspan="1" colspan="1"><p>Conforme ISO 8601:2004</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Data e hora da dispensação</p></td>      <td rowspan="1" colspan="1"><p>Data e hora</p></td>      <td rowspan="1" colspan="1"><p>Conforme ISO 8601:2004</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Profissional prescritor</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Conselho do profissional prescritor</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado</p></td>      <td rowspan="1" colspan="1"><p>Indica a entidade de conselho profissional do prescritor - CRM, CRF, CRO, CRN, COREN</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>UF do conselho do profissional prescritor</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado por terminologia externa: IBGE</p></td>      <td rowspan="1" colspan="1"><p>Indica a UF do conselho do profissional prescritor</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Número de conselho do profissional prescritor</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Número do conselho do profissional prescritor</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Identificador do profissional prescritor</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Identificação unívoca do profissional prescritor, mediante número único válido em todo o território nacional, sendo:</p><p>- Cartão Nacional de Saúde (CNS).</p><p>- Cadastro de Pessoa Física (CPF).</p><p>RN09: Validar junto ao CADSUS.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Ocupação do profissional prescritor</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado por terminologia externa: CBO/MTE</p></td>      <td rowspan="1" colspan="1"><p>Atividade desempenhada pelo profissional que realizou a emissão da prescrição.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Profissional dispensador</p></td>      <td rowspan="1" colspan="1"><p></p></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>CPF do profissional dispensador</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Identificação unívoca do profissional dispensador, mediante número único válido em todo o território nacional, sendo:</p><p>- Cadastro de Pessoa Física (CPF).</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>CRF do profissional dispensador</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Número do Conselho Regional de Farmácia do Profissional Dispensador.</p><p>RN10: Obrigatório para medicamentos que exijam a dispensação realizada por farmacêutico.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Identificação de quem retirou o medicamento</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Identificação unívoca de quem retira o medicamento, mediante número único válido em todo o território nacional, sendo:</p><p>- Cadastro de Pessoa Física (CPF).</p><p>RN11: Obrigatório para pessoa diferente do paciente da prescrição.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>1</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Dispensação no atendimento</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>2</p></td>      <td rowspan="1" colspan="1"><p>[1..N]</p></td>      <td rowspan="1" colspan="1"><p>Item dispensado</p></td>      <td rowspan="1" colspan="1"></td>      <td rowspan="1" colspan="1"><p></p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Nome e versão da terminologia de medicamentos</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado</p></td>      <td rowspan="1" colspan="1"><p>-Lista de registro de medicamentos da ANVISA</p><p>-Ontologia Brasileira de Medicamentos (OBM)</p><p>-Catálogo de Materiais do Governo Federal (CATMAT)</p><p>-Código de Barras (GTIN)</p><p>-IUM (Identificador Único de Medicamento)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Identificador do item dispensado</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado por terminologia externa</p></td>      <td rowspan="1" colspan="1"><p>CATMAT ou Código GTIN (código de barras) do produto dispensado.</p><p>RN12: validar junto à OBM (AMPP)</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Código serial da unidade de medicamento</p></td>      <td rowspan="1" colspan="1"><p>Texto livre</p></td>      <td rowspan="1" colspan="1"><p>RN13: Obrigatório em medicamentos serializados/Datamatrix - Elemento serl do XML para grupo IUM</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Lote</p></td>      <td rowspan="1" colspan="1"><p>Texto livre</p></td>      <td rowspan="1" colspan="1"><p>RN14: Se medicamento serializado/Datamatrix - Elemento lot do XML para grupo IUM</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Data de validade</p></td>      <td rowspan="1" colspan="1"><p>Data</p></td>      <td rowspan="1" colspan="1"><p>Conforme ISO 8601 (YYYY-MM)</p><p>RN15: Se medicamento serializado/Datamatrix - Elemento exp do XML para grupo IUM</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Unidade de medida do produto</p></td>      <td rowspan="1" colspan="1"><p>Texto codificado</p></td>      <td rowspan="1" colspan="1"><p>Unidade de medida do produto prescrito (ex.: comprimido, cápsula, frasco, caixa etc.).</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[1..1]</p></td>      <td rowspan="1" colspan="1"><p>Quantidade dispensada no atendimento</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Quantidade do produto dispensado (unidade).</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Quantidade de dias de fornecimento</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Quantidade de dias de fornecimento de produto dispensado.</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Valor do produto</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Valor em reais da apresentação dispensada</p><p>RN16: Obrigatório somente para atendimentos do Programa Farmácia Popular do Brasil</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Valor pago Ministério da Saúde</p></td>      <td rowspan="1" colspan="1"><p>Caracteres numéricos</p></td>      <td rowspan="1" colspan="1"><p>Valor em reais da apresentação dispensada</p><p>RN17: Obrigatório somente para atendimentos do Programa Farmácia Popular do Brasil</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>3</p></td>      <td rowspan="1" colspan="1"><p>[0..1]</p></td>      <td rowspan="1" colspan="1"><p>Orientação de uso do produto</p></td>      <td rowspan="1" colspan="1"><p>Texto livre</p></td>      <td rowspan="1" colspan="1"></td>     </tr>    </tbody>   </table>
