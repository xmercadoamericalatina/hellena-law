---
titulo: "RESOLUÇÃO CCGD Nº 10, DE 23 DE JUNHO DE 2022"
orgao: "Ministério da Economia/Secretaria Especial de Desburocratização, Gestão e Governo Digital/Comitê Central de Governança de Dados"
tipo: "Resolução"
numero: "10"
data: 2022-06-23
revogada: null
versao_texto: "publicação original"
publicacao: "DOU de 27/06/2022, seção 1, p. 60"
data_publicacao: 2022-06-27
edicao: "119"
fonte: "https://www.in.gov.br/web/dou/-/resolucao-ccgd-n-10-de-23-de-junho-de-2022-410364821"
sha256_html_fonte: c01a98ec77e419586872d6ac5f1d684a0c255ed4ed3036b5bf9498386ff4835b
baixado_em: 2026-10-20
---
# RESOLUÇÃO CCGD Nº 10, DE 23 DE JUNHO DE 2022

RESOLUÇÃO CCGD Nº 10, DE 23 DE JUNHO DE 2022

Institui o Registro de Referência da Pessoa com Deficiência.

O COMITÊ CENTRAL DE GOVERNANÇA DE DADOS, no uso das atribuições que lhe conferem o art. 21, inciso XI, do Decreto nº 10.046, de 9 de outubro de 2019, e tendo em vista o disposto no Objetivo 6 do Anexo ao Decreto nº 10.332, de 26 de abril de 2020, no Capítulo IV da Lei nº 13.709, de 14 de agosto de 2018, e nos arts. 38, 39 e 40 da Lei nº 14.129, de 29 de março de 2021, resolve:

**Art. 1º** Fica instituído o Registro de Referência da Pessoa com Deficiência, de uso obrigatório pelos órgãos e entidades da administração pública federal direta, autárquica e fundacional.

**Parágrafo único.** O disposto nesta Resolução não se aplica ao compartilhamento de dados com os conselhos de fiscalização de profissões regulamentadas.

**Art. 2º** Os Registros de Referência têm a finalidade de:

I - promover a interoperabilidade do conjunto de dados entre os órgãos e entidades de que trata o art. 1º;

II - auxiliar a formulação, a implementação, a avaliação, o monitoramento e a gestão de políticas públicas;

III - fomentar a qualidade e a fidedignidade dos dados custodiados pelos órgãos gestores de dados;

IV - aumentar a eficiência e reduzir custos das operações internas dos sistemas de informação dos órgãos gestores e consumidores de dados;

V - orientar o acesso aos órgãos e entidades de que trata o art. 1º ao conjunto de dados relacionado à Application Programming Interface - API da Pessoa com Deficiência, que tem como finalidade identificar de forma automática se determinado cidadão pesquisado é uma pessoa com deficiência, segundo a legislação vigente, a partir dos dados disponíveis:

a) no Cadastro Nacional de Informações Sociais (CNIS);

b) no Cadastro-Inclusão;

c) na Base de Dados do Benefício de Prestação Continuada (BPC);

d) na Base de Dados da Aposentadoria da Pessoa com Deficiência; e

e) na Base de Dados da Avaliação Biopsicossocial.

**Art. 3º** O Registro de Referência da Pessoa com Deficiência é o conjunto de dados para identificação do cidadão como pessoa com deficiência, conforme a legislação, constituído pelas bases de dados de que trata o art. 2º, IV, e composto, em sua primeira versão, pelos seguintes atributos:

I - CPF - Número do CPF a ser consultado, sem máscara.

II - Nome completo do cidadão pesquisado;

III - CPF, com máscara, do cidadão pesquisado;

IV - Possui Deficiência - Retorna verdadeiro true se o CPF for encontrado em uma das bases pesquisadas e falso false se a pesquisa não encontrar um registro.

**§1º** O Registro de Referência da Pessoa com Deficiência utilizará o CPF como chave de pesquisa no conjunto de dados da API da Pessoa com Deficiência.

**§2º** Os campos descritos nos incisos II ao IV do caput são respostas da pesquisa efetivada com o campo do inciso I.

**§3º** Em caso positivo, presume-se que o cidadão pesquisado é uma pessoa com deficiência, nos termos da legislação vigente, ressalvada possibilidade de averiguação da correção da informação no caso concreto.

**§4º** Em caso de retorno negativo, o cidadão não está cadastrado como pessoa com deficiência.

**Art. 4º** Compete à Coordenação-Geral de Dados e Informação da Pessoa com Deficiência do Ministério da Mulher, da Família e dos Direitos Humanos, na condição de Órgão Gestor de Dados da base de dados do Sistema de Benefício Assistencial à Pessoa com Deficiência (BPC/LOAS):

I - comunicar, com antecedência mínima de cinco dias, ao órgão de que trata o art. 5º eventuais atualizações na estrutura ou no próprio conjunto de dados do Registro de Referência;

II - comunicar ao órgão de que trata o art. 5º qualquer indisponibilidade que afete a oferta dos conjuntos de dados em até 24 horas; e

III - manter as boas práticas de governança, integração e qualidade de dados, a fim de garantir níveis adequados de interoperabilidade entre órgãos e entidades de que trata o art. 1º.

**Parágrafo único** É de responsabilidade do órgão de que trata o caput zelar, de maneira recorrente, pelo aperfeiçoamento do conjunto de dados dos Registros de Referência, no que diz respeito às recomendações de seu uso e ao surgimento de novas necessidades de interoperabilidade e transformação digital para a eficiência de políticas públicas de Estado.

**Art. 5º** Compete à Secretaria de Governo Digital da Secretaria Especial de Desburocratização, Gestão e Governo Digital do Ministério da Economia, na condição de Órgão Gestor do Registro de Referência da Pessoa com Deficiência:

I - estabelecer as medidas necessárias para promover a utilização do Registro de Referência da Pessoa com Deficiência pelos órgãos consumidores de dados;

II - adotar os procedimentos necessários para viabilizar a implantação, a operação e o monitoramento do Registro de Referência da Pessoa com Deficiência por meio da Plataforma de Interoperabilidade do Governo Federal Conecta Gov.br;

III - orientar os órgãos e entidades de que trata o art. 1º para uma melhor interoperabilidade entre os sistemas de informação; e

IV - propor ao Comitê Central de Governança de Dados a atualização, a ampliação e a otimização do Registro de Referência da Pessoa com Deficiência para uma melhor adequação às necessidades dos órgãos recebedores de dados.

**Art. 6º** Os órgãos recebedores de dados têm o prazo de noventa dias, contados da data de vigência desta Resolução, para elaborar um plano de adequação de seus sistemas de informação com a indicação dos critérios de priorização, sendo que os ajustes deverão ser implementados até 31 de dezembro de 2023.

**Parágrafo único.** É responsabilidade dos órgãos de que trata o caput arcar com os custos de adaptação de seus próprios sistemas de informação para viabilizar a interoperabilidade com o Registro de Referência da Pessoa com Deficiência.

**Art. 7º** Fica proibida a instituição de novas bases de dados que tratem do tema conjunto de dados da Pessoa com Deficiência no âmbito do Poder Executivo federal, exceto quando autorizado pelo órgão de que trata o art. 5º.

**Art. 8º** Esta Resolução entra em vigor no dia 1º de julho de 2022.

EMMANUELLE REGIANE CUNHA DE OLIVEIRA

Presidente do Comitê
