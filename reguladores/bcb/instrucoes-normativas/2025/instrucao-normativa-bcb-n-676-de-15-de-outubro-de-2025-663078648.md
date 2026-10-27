---
titulo: "INSTRUÇÃO NORMATIVA BCB Nº 676, DE 15 DE OUTUBRO DE 2025"
orgao: "Banco Central do Brasil/Área de Regulação/Departamento de Regulação, Supervisão e Controle das Operações do Crédito Rurais e do Proagro"
tipo: "Instrução Normativa"
numero: "676"
data: 2025-10-15
revogada: null
versao_texto: "publicação original"
publicacao: "DOU de 16/10/2025, seção 1, p. 443"
data_publicacao: 2025-10-16
edicao: "198"
fonte: "https://www.in.gov.br/web/dou/-/instrucao-normativa-bcb-n-676-de-15-de-outubro-de-2025-663078648"
baixado_em: 2026-10-16
sha256_html_fonte: 079b4f60e01be8c96a12c618aec4e64da4cce58b3ac8d57796fa7e6690459161
---
# INSTRUÇÃO NORMATIVA BCB Nº 676, DE 15 DE OUTUBRO DE 2025

INSTRUÇÃO NORMATIVA BCB Nº 676, DE 15 DE OUTUBRO DE 2025

Estabelece procedimentos operacionais aplicáveis à liquidação ou amortização de dívidas de produtores rurais cujas atividades foram prejudicadas por eventos adversos, de que tratam a Medida Provisória nº 1314, de 5 de setembro de 2025, e a Resolução CMN nº 5.247, de 19 de setembro de 2025.

O Chefe do Departamento de Regulação, Supervisão e Controle das Operações do Crédito Rural e do Proagro (Derop), no uso das atribuições que lhe confere o art. 23, inciso I, alínea "a", do Regimento Interno do Banco Central do Brasil, anexo à Resolução BCB nº 340, de 21 de setembro de 2023, e com base na disposição da alínea "b" do item 3 da Seção 6 (Contabilização e Controle) do Capítulo 3 (Operações) do Manual de Crédito Rural (MCR), resolve:

**Art. 1º** As operações de crédito rural e demais dívidas liquidadas ou amortizadas sob amparo da Medida Provisória nº 1.314, de 5 de setembro de 2025, e da Resolução CMN nº 5.247, de 19 de setembro de 2025, devem receber o status SOR05 ou SOR06 no Sistema de Operações do Crédito Rural e do Proagro - Sicor, observadas as instruções do MCR - Documento 1 (Requisitos e Instruções de Preenchimento do Sistema de Operações do Crédito Rural).

**§ 1º** Quando se tratar de liquidação de dívidas, as operações liquidadas devem receber o status SOR06;

**§ 2º** Quando se tratar de amortização de dívidas, as operações criadas para receber a parte do saldo renegociada devem receber o status SOR05.

**Art. 2º** Os seguintes campos do Sicor, referentes a operações de crédito rural enquadradas nas condições de que trata o art. 1º da Resolução CMN nº 5.247, de 2025, deverão ser registrados conforme segue:

I - Fonte de recursos: código "0100" (TESOURO NACIONAL);

II - Beneficiário:

a) produtor rural (pessoa física ou jurídica): tipo de beneficiário código "001";

b) cooperativa de produção agropecuária, na condição de sociedade prestadora de serviços de natureza agropecuária a seus cooperados: tipo de beneficiário código "002", observada a necessidade de envio da lista de cooperados (CPF e valor individual), via COR0001;

c) cooperativa de produção agropecuária, na condição de produtor rural: tipo de beneficiário código "003";

d) associação de produtores e condomínios rurais: tipo de beneficiário código "004", observada a necessidade de envio da lista de associados/condôminos (CPF e valor individual), via COR0001;

III - Programa: informar o código do programa ao qual o mutuário está vinculado, conforme segue:

a) "0001", caso se trate do Programa Nacional de Fortalecimento da Agricultura Familiar (Pronaf);

b) "0050", caso se trate do Programa Nacional de Apoio ao Médio Produtor Rural (Pronamp); e

c) "0999", caso se trate de mutuário sem vínculo a programa específico;

IV - Preenchimento do Grupo\_COR0001\_Renegc:

a) NumRefBCCORRenegc: preencher Refbacen da operação de crédito rural liquidada ou amortizada; e

b) CodBaseLegalRenegc: preencher com "Res. CMN 5.247/2025 - Art. 1º".

**Parágrafo único.** Para fins de observância ao disposto na alínea "d" do inciso I do § 3º do art. 1º da Resolução CMN nº 5.247, de 2025, os valores indicados:

I - nas listas de cooperados ou de associados/condôminos sensibilizarão os limites individuais;

II - nas operações individuais sensibilizarão os limites disponíveis para cada produtor, quando integrarem listas de cooperados ou de associados/condôminos.

**Art. 3º** Os seguintes campos do Sicor, referentes a operações de crédito rural enquadradas nas condições de que trata o art. 2º da Resolução CMN nº 5.247, de 2025, deverão ser registrados conforme segue:

I - Fonte de recursos: código "0402" (RECURSOS LIVRES);

II - Beneficiário: seguir as instruções de que trata o inciso II do art. 2º, dispensado o envio de listas de que tratam as alíneas "b" e "d";

III - Preenchimento do Grupo\_COR0001\_Renegc:

a) NumRefBCCORRenegc: preencher Refbacen da operação de crédito rural liquidada ou amortizada; e

b) CodBaseLegalRenegc: preencher com "Res. CMN 5.247/2025 - Art. 2º".

**Art. 4º** Caso as dívidas liquidadas ou amortizadas correspondam a Cédulas de Produto Rural - CPR ou a empréstimos de que trata o inciso IV do art. 2º da Resolução CMN nº 5.247, de 2025, a instituição financeira deverá inserir código de onze dígitos no campo NumRefBCCORRenegc para fins de identificação da dívida liquidada ou amortizada, mediante utilização da seguinte regra de formação:

I - Primeiro e segundo dígitos: ano de emissão da CPR ou do empréstimo, no formato XX (por exemplo: CPR emitida em 2021, código "21");

II - Terceiro e quarto dígitos: mês de emissão da CPR ou do empréstimo;

III - Quinto dígito:

a) número 5 (cinco), caso se trate de CPR; e

b) número 6 (seis), caso se trate de empréstimo;

IV - últimos seis dígitos:

a) últimos seis dígitos do número de registro da CPR, quando for o caso; ou

b) últimos seis dígitos do número identificador padronizado da operação de crédito - IPOC no Sistema de Informações de Créditos - SCR, para os empréstimos de que trata o inciso IV do art. 2º da Resolução CMN nº 5.247, de 2025.

**Art. 5º** Todas as dívidas de um mesmo mutuário que venham a ser liquidadas ou amortizadas sob amparo da Medida Provisória nº 1.314, de 2025, e da Resolução CMN nº 5.247, de 2025, devem, preferencialmente, ser incluídas como destinações de uma única RefBacen.

**Parágrafo único.** Admite-se que a instituição financeira conceda mais de uma operação para efetuar as liquidações ou amortizações de um mesmo mutuário, nas seguintes hipóteses:

I - heterogeneidade das características das dívidas enquadradas;

II - mutuário já houver tomado créditos para a finalidade de que trata o caput em outra instituição financeira; e

III - inviabilidade operacional para a instituição financeira.

**Art. 6º** Para fins de preenchimento e envio dos dados das operações resultantes das renegociações no Documento 3040 do SCR, utilizar a submodalidade "Financiamentos rurais - investimento" (código 0802).

**Art. 7º** As operações de crédito rural destinadas à liquidação ou à amortização de dívidas de produtores rurais no âmbito da Medida Provisória nº 1.314, de 2025, e da Resolução CMN nº 5.247, de 2025, devem ser escrituradas nas seguintes rubricas contábeis do Padrão Contábil das Instituições Reguladas pelo Banco Central do Brasil (Cosif):

I - no caso das operações de que trata o art. 1º da Resolução CMN nº 5.247, de 2025:

a) 1.6.3.45.00.00-9 Financiamentos Rurais - Aplicações com Recursos de Fontes Públicas;

b) 3.8.1.20.60.10-1 Valor Contábil Bruto - Recursos Tesouro Nacional; e

c) 3.8.1.20.60.90-5 (-) Perdas Esperadas - Recursos Tesouro Nacional.

II - no caso das operações de que trata o art. 2º da Resolução CMN nº 5.247, de 2025:

a) 1.6.3.05.00.00-3 Financiamentos Rurais - Aplicações com Recursos Livres;

b) 3.8.1.20.60.15-6 Valor Contábil Bruto - Recursos Livres; e

c) 3.8.1.20.60.95-0 (-) Perdas Esperadas - Recursos Livres.

**Art. 8º** Esta Instrução Normativa BCB entra em vigor na data de sua publicação.

Claudio Filgueiras Pacheco Moreira
