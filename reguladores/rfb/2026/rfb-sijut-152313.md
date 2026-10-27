---
titulo: "Ato Declaratório Executivo Corat nº 26, de 9 de julho de 2026"
orgao: "Coordenação-Geral de Administração do Crédito Tributário"
tipo: "Ato Declaratório Executivo"
numero: "26"
data: "2026-07-09"
revogada: false
versao_texto: "publicação original — visão original da fonte"
publicacao: "Publicado(a) no DOU de 10/07/2026, seção 1, página 109"
data_publicacao: "2026-07-10"
fonte: "https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/152313/visao/original"
fonte_api: "https://normasinternet2.receita.fazenda.gov.br/api/consulta-externa/ato/152313/visao/original"
fonte_indice: "https://normas.receita.fazenda.gov.br/api/indexacao/ato/pesquisar"
id_rfb: "152313"
sha256_texto: "a2538f4039f2b065441113f5a12f54bd648a9c6a7ef9d9e332cddfad180cccd6"
baixado_em: "2026-10-15"
vigente_fonte: true
evidencia_revogacao: "vigente:true"
---
# Ato Declaratório Executivo Corat nº 26, de 9 de julho de 2026

Aprova a versão 1.0 do leiaute do arquivo para importação de Declarações do Imposto sobre a Propriedade Territorial Rural - DITR a partir do exercício 2026.

O COORDENADOR-GERAL DE ADMINISTRAÇÃO DO CRÉDITO TRIBUTÁRIO, no uso das atribuições que lhe conferem o art. 66, caput, inciso II, e art. 358, caput, inciso II, do Regimento Interno da Secretaria Especial da Receita Federal do Brasil, aprovado pela Portaria ME nº 284, de 27 de julho de 2020, declara:

**Art. 1º** Fica aprovada a versão 1.0 do leiaute do arquivo para a importação de Declarações do Imposto sobre a Propriedade Territorial Rural - DITR a partir do exercício 2026, por meio da funcionalidade "Importar Declarações", serviço "Minhas Declarações do ITR", no Portal de Serviços da Receita Federal, observada a especificação técnica e estrutural constante do Anexo Único deste Ato Declaratório.

**Art. 2º** Este Ato Declaratório Executivo entra em vigor na data de sua publicação no Diário Oficial da União.

JORDÃO NÓBRIGA DA SILVA JUNIOR

ANEXO ÚNICO



ANEXO ÚNICO

Leiaute para Importação - “Minhas Declarações do ITR” Este documento apresenta a especificação técnica e estrutural completa para a geração do arquivo no formato CSV destinado à importação de declarações, em lote, no serviço digital “Minhas Declarações do ITR” para exercícios a partir de 2026. Estão disponíveis dois modelos de arquivos para importação: um modelo em branco e o outro pré-preenchido com os dados cadastrais recuperados da base da Receita Federal. Devem ser preenchidos apenas os campos que reflitam as particularidades de cada imóvel rural, observada a legislação aplicável. 1. Padrão de Formatação Para o processamento eletrônico correto do arquivo de importação, todas as linhas de registros devem seguir estritamente as convenções abaixo: - Separador de Campos: Deve ser utilizado o ponto e vírgula (;). - Separador Decimal: Obrigatoriamente a vírgula (,) para todos os campos indicados com notação decimal. - Separador de Milhar: Opcional. Se utilizado, deve ser o ponto (.). Exemplo válido: 1.250,50 ou 1250,50. - Tratamento de Strings (Texto): Valores com espaços ou caracteres especiais não devem conter aspas desnecessárias, respeitando o limite máximo de caracteres. - Formato de Datas: DD/MM/AAAA (Dia com 2 dígitos, mês com 2 e ano com 4). - Máscaras de Documentos: Campos como CIB, CPF, CEP e CAR devem ser informados sem pontos, traços ou barras, apenas os caracteres alfanuméricos puros. Importante: A primeira linha do arquivo (cabeçalho) deve conter exatamente os nomes dos campos conforme listados na coluna 'Campo no Modelo' deste documento. É obrigatório que a grafia seja idêntica (sem alterações ou traduções) e que a ordem das colunas siga a sequência estabelecida nos modelos disponibilizados, para que o sistema processe as informações corretamente.

cib Texto (8) Identificação do imóvel rural no Cadastro Imobiliário Brasileiro.

municipio Texto (40) Nome do município de localização do imóvel rural.

uf Texto (2) Sigla da Unidade da Federação de localização do imóvel rural. Ex: SP, MT, BA.

area Numérico (7,1) Área total do imóvel em hectares (ha). Máximo 9.999.999,9.

contribuinte\_cpf\_conjuge Texto (11) CPF do cônjuge do contribuinte, se aplicável. Apenas dígitos.

contribuinte\_endereco\_cep Texto (8) Código de Endereçamento Postal do endereço para entrega de correspondência. Sem hífen.

contribuinte\_endereco\_tipo\_logradouro Texto (17) Tipo de logradouro padrão dos Correios (exemplo: Rua, Avenida, Alameda).

contribuinte\_endereco\_logradouro Texto (56) Nome do logradouro para entrega de correspondência.

contribuinte\_endereco\_numero Texto (5) Número do endereço para entrega de correspondência. Informar 'S/N' se não houver.

contribuinte\_endereco\_complemento Texto (20) Dados adicionais do endereço para entrega de correspondência (ex: Bloco B, Apt 42, Km 12).

contribuinte\_endereco\_bairro Texto (40) Bairro ou distrito do endereço para entrega de correspondência.

contribuinte\_endereco\_telefone Texto (11) Telefone para contato com o contribuinte (DDD + Número), apenas dígitos.

contribuinte\_cpf\_inventariante Texto (11) CPF do inventariante. No caso de Espólio, se contribuinte pessoa física.

2. Campos do leiaute Abaixo encontra-se a listagem dos campos estruturados por seções funcionais, com suas respectivas tipagens na notação (I, D) — onde 'I' representa o número de dígitos inteiros e 'D' as casas decimais.

2.1 Identificação do Imóvel rural e Contribuinte 2.2 Distribuição da Área do Imóvel Rural

utilizacao\_imovel\_area\_preservacao\_permanente Numérico (7,1) Áreas de Preservação Permanente (APP) protegidas por sua função ambiental no imóvel rural, em hectares (ha). utilizacao\_imovel\_area\_reserva\_legal Numérico (7,1) Áreas de Reserva Legal (RL) com a função ambiental de assegurar o uso econômico de modo sustentável dos recursos naturais, em hectares (ha). utilizacao\_imovel\_area\_rppn Numérico (7,1) Áreas de Reserva Particular do Patrimônio Natural (RPPN) destinadas à conservação da diversidade biológica, em hectares (ha). utilizacao\_imovel\_area\_interesse\_ecologico Numérico (7,1) Áreas declaradas de relevante interesse ecológico por ato do Poder Público, em hectares (ha). utilizacao\_imovel\_area\_servidao\_ambiental Numérico (7,1) Áreas instituídas na forma de servidão florestal, em hectares (ha). utilizacao\_imovel\_area\_florestas\_nativas Numérico (7,1) Áreas cobertas por florestas nativas em estágio médio ou avançado de regeneração, em hectares (ha). utilizacao\_imovel\_area\_alagada Numérico (7,1) Áreas inundadas para constituição de reservatórios de usinas hidrelétricas autorizadas pelo poder público, em hectares (ha). utilizacao\_imovel\_area\_benfeitorias Numérico (7,1) Soma das áreas ocupadas por moradias, galpões, estradas internas e instalações, enquadradas como úteis às atividades rurais, em hectares (ha). 2.3 Área Utilizada na Atividade Rural

utilizacao\_imovel\_area\_produtos\_vegetais Numérico (7,1) Área plantada com culturas temporários e/ou permanentes, em hectares (ha).

utilizacao\_imovel\_area\_descanso Numérico (7,1) Área que tenha permanecido em descanso para a recuperação do solo mediante laudo técnico, em hectares (ha).

utilizacao\_imovel\_area\_reflorestamento Numérico (7,1) Área de reflorestamento de essências exóticas ou nativas, em hectares (ha).

utilizacao\_imovel\_area\_granjeira\_aquicola Numérico (7,1) Área para a exploração granjeira ou aquícola ocupada com benfeitorias, construções e instalações destinadas ou empregadas diretamente na criação, em hectares (ha). utilizacao\_imovel\_area\_frustracao\_safra Numérico (7,1) Área de frustação de safra ou destruição de pastagem em área de calamidade pública reconhecida pelo Governo Federal, em hectares (ha).

utilizacao\_imovel\_area\_pastagem Numérico (7,1) Área de pastagem total (deve corresponder à soma de nativa e plantada), em hectares (ha). ATENÇÃO: Não preencher se os campos referentes aos campos do modelo de "Atividade Pecuária" forem preenchidos. utilizacao\_imovel\_area\_exploracao\_extrativa Numérico (7,1) Área utilizada com atividade de extração e coleta de produtos vegetais nativos (não plantados), inclusive a exploração madeireira de florestas nativas, em hectares (ha). ATENÇÃO: Não preencher se os campos referentes aos campos do modelo de "Atividade Extrativa" forem preenchidos. utilizacao\_imovel\_numero\_car Texto (41) Número do recibo do Cadastro Ambiental Rural (CAR).

2.4 Atividade Pecuária

atividade\_pecuaria\_grande\_porte\_quantidade Numérico (7,0) Quantidade média de animais de grande porte (bovinos, bufalinos, equinos, asininos e muares) presentes na data de referência. Máximo 9.999.999.

atividade\_pecuaria\_medio\_porte\_quantidade Numérico (7,0) Quantidade média de animais de médio porte (dentre outros, ovinos e caprinos). Máximo 9.999.999.

atividade\_pecuaria\_area\_pastagem\_nativa Numérico (7,1) Área de pastagem nativa efetivamente utilizada para alimentação dos animais, em hectares (ha).

atividade\_pecuaria\_area\_pastagem\_plantada Numérico (7,1) Área de pastagem plantada efetivamente utilizada para alimentação dos animais, em hectares (ha).

atividade\_pecuaria\_area\_forrageira\_corte Numérico (7,1) Área ocupada por forrageira de corte efetivamente utilizada para alimentação dos animais, em hectares (ha).

atividade\_pecuaria\_area\_pastagem\_formacao Numérico (7,1) Área ocupada por pastagem ainda em formação, em hectares (ha).

atividade\_pecuaria\_area\_projeto\_tecnico Numérico (7,1) Área de pastagem efetivamente utilizada, objeto de projeto técnico, aprovado por órgão federal, em hectares (ha).

atividade\_pecuaria\_orgao\_projeto\_tecnico Texto (30) Nome da entidade ou órgão federal competente que aprovou o projeto técnico.

atividade\_pecuaria\_data\_projeto\_tecnico Data (10) Data da assinatura do projeto técnico. Formato: DD/MM/AAAA.

2.5 Atividade Extrativa (Por Produto)

atividade\_extrativa\_acacia\_negra\_area Numérico (7,1) Área de extração de acácia negra, em hectares (ha).

atividade\_extrativa\_acacia\_negra\_quantidade Numérico (8,2) Quantidade extraída de acácia negra, em toneladas (ton).

atividade\_extrativa\_babacu\_area Numérico (7,1) Área de extração de babaçu, em hectares (ha).

atividade\_extrativa\_babacu\_quantidade Numérico (6,2) Quantidade extraída de babaçu, em toneladas (ton).

atividade\_extrativa\_borracha\_area Numérico (7,1) Área de extração de borracha, em hectares (ha).

atividade\_extrativa\_borracha\_quantidade Numérico (8,2) Quantidade extraída de borracha, em quilogramas (kg).

atividade\_extrativa\_carnauba\_area Numérico (7,1) Área de extração de carnaúba, em hectares (ha).

atividade\_extrativa\_carnauba\_quantidade Numérico (6,2) Quantidade extraída de carnaúba, em toneladas (ton).

atividade\_extrativa\_castanha\_do\_para\_area Numérico (7,1) Área de extração de castanha-do-pará, em hectares (ha).

atividade\_extrativa\_castanha\_do\_para\_quantidade Numérico (8,2) Quantidade extraída de castanha-do-pará, em quilogramas (kg).

atividade\_extrativa\_guarana\_area Numérico (7,1) Área de manejo extrativo de guaraná, em hectares (ha).

atividade\_extrativa\_guarana\_quantidade Numérico (6,2) Quantidade produzida de guaraná, em toneladas (ton).

atividade\_extrativa\_madeira\_area Numérico (7,1) Área do imóvel rural submetida ao corte ou manejo madeireiro, em hectares (ha).

atividade\_extrativa\_madeira\_quantidade Numérico (8,2) Quantidade de madeira extraída, em metros cúbicos (m³).

atividade\_extrativa\_plano\_manejo\_area Numérico (7,1) Área objeto de plano de manejo aprovado por órgão ambiental competente, em hectares (ha).

atividade\_extrativa\_data\_plano\_manejo Data (10) Data de aprovação, pelo órgão ambiental competente, do plano de manejo. Formato DD/MM/AAAA.

atividade\_extrativa\_outros\_area Numérico (7,1) Área de extração de demais produtos sem campos específicos, em hectares (ha).

2.6 Áreas Não Utilizadas

area\_nao\_utilizada\_area\_demais\_benfeitorias Numérico (7,1) Áreas ocupadas com instalações, construções e benfeitorias não enquadradas como úteis à atividade rural (ex: hotéis-fazenda, parques temáticos), em hectares (ha). area\_nao\_utilizada\_area\_mineracao Numérico (7,1) Áreas ocupadas por jazidas ou minas, exploradas ou não, em hectares (ha).

area\_nao\_utilizada\_area\_imprestavel Numérico (7,1) Áreas imprestáveis para a atividade rural, não declaradas de interesse ecológico por ato do órgão competente, tais como afloramentos rochosos, pedreiras, desertos, em hectares (ha). area\_nao\_utilizada\_area\_inexplorada Numérico (7,1) Áreas aproveitáveis que não tenham sido exploradas, em hectares (ha).

area\_nao\_utilizada\_outras\_areas Numérico (7,1) Demais áreas não utilizadas com atividade rural sem campos específicos, tais como camping, pesque-pague, em hectares (ha).

2.7 Apuração do Imposto

calculo\_imposto\_valor\_total\_imovel Numérico (10,2) Valor de mercado total do imóvel (Terra Nua + Benfeitorias + Culturas) na data de referência, em Reais (R$).

calculo\_imposto\_valor\_construcoes Numérico (10,2) Valor de mercado às construções, instalações e benfeitorias, em Reais (R$).

calculo\_imposto\_valor\_culturas Numérico (10,2) Valor das culturas permanentes e temporárias, em Reais (R$).

calculo\_imposto\_quantidade\_cotas Numérico (1,0) Número de quotas para pagamento do tributo (mínimo de R$ 50,00 por quota, máximo de 4 quotas conforme legislação).

3. Exemplo Estrutural de Registro CSV Reproduz-se abaixo um exemplo, com alguns campos preenchidos, de cabeçalho e linha de dados estruturados para exportação com base nas especificações técnicas apresentadas: cib;municipio;uf;area;contribuinte\_endereco\_cep;utilizacao\_imovel\_area\_preservacao\_permanente;utilizacao\_imovel\_numero\_car;calculo\_imposto\_val or\_total\_imovel;calculo\_imposto\_valor\_construcoes;calculo\_imposto\_quantidade\_cotas 12345678;Ribeirao Preto;SP;1500,5;14000000;45,2;SP354340201234567890123456789012345678901;5000000,00;450000,00;3 Verificação de Consistência: Observe que a “área” (1500,5) e a “area\_preservacao\_permanente” (45,2) usam a vírgula como separador interno de valores e o caractere ponto e vírgula delimita a passagem de campos, evitando erros de identificação das informações pelo serviço “Minhas Declarações do ITR”.

