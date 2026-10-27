---
titulo: "Portaria MF nº 501, de 30 de setembro de 2010"
orgao: "Ministério da Fazenda"
tipo: "Portaria"
numero: "501"
data: "2010-09-30"
revogada: false
evidencia_revogacao: "vigente:true"
vigente_fonte: true
versao_texto: "publicação original — visão original da fonte"
publicacao: "Publicado(a) no DOU de 01/10/2010, página 15"
data_publicacao: "2010-10-01"
fonte: "https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/28326/visao/original"
fonte_api: "https://normasinternet2.receita.fazenda.gov.br/api/consulta-externa/ato/28326/visao/original"
fonte_indice: "https://normas.receita.fazenda.gov.br/api/indexacao/ato/pesquisar"
id_rfb: "28326"
sha256_texto: "b0a1cb8283724d92d7f9d364a42d7dd1ea39d0869130993ef899efe27f141db2"
baixado_em: "2026-10-21"
---
# Portaria MF nº 501, de 30 de setembro de 2010

"Dispõe sobre o fornecimento, pelos Estados e o Distrito Federal, das informações relativas aos estabelecimentos de contribuintes do ICMS que realizam operações e prestações que destinem ao exterior mercadorias ou serviços, bem como operações equiparadas."

O MINISTRO DE ESTADO DA FAZENDA, no uso da atribuição que lhe confere o inciso II do parágrafo único do art. 87 da Constituição, e tendo em vista o disposto no art. 6º da Medida Provisória nº 501, de 8 de setembro de 2010, resolve:

**Art. 1º** Os Estados e o Distrito Federal deverão prestar as informações a seguir discriminadas, por mês de competência, relativas aos estabelecimentos de contribuintes do imposto sobre operações relativas à circulação de mercadorias e sobre prestações de serviços de transporte interestadual e intermunicipal e de comunicação (ICMS) que realizam operações e prestações que destinem ao exterior mercadorias ou serviços, bem como operações equiparadas, nos termos do art. 3º, II, e parágrafo único, da Lei Complementar nº 87, de 13 de setembro de 1996:

I - valor das operações e prestações que destinem ao exterior mercadorias ou serviços, bem como operações equiparadas, nos termos do art. 3º, II e parágrafo único, da Lei Complementar nº 87, de 1996;

II - valor do total das operações e prestações;

III - valor dos créditos de ICMS;

IV - o valor das transferências de saldo credor;

V - saldo credor acumulado registrado no final do mês de competência;

**§ 1º** As informações deverão ser encaminhadas à Secretaria da Receita Federal do Brasil em arquivo magnético para o endereço eletrônico dadosexportacao@receita.fazenda.gov.br, devendo ser requerida a opção de confirmação automática de entrega da mensagem.

**§ 2º** O arquivo magnético deverá observar o seguinte formato:

I - o nome do arquivo magnético deverá ser composto pela sigla da Unidade da Federação seguida de hífen e de quatro dígitos indicativos do ano e dois dígitos indicativos do mês de competência a que se referem as informações (UF-AAAAMM).

II - o arquivo deverá ser composto pelos seguintes conjuntos de registros, classificados na ordem abaixo:

Tipos de Registros Observações 01 1º registro 02 demais registros: informações de cada estabelecimento exportador

<table>   <tbody><tr>    <td>    <p>Tipos de Registros</p>      </td>    <td>    <p>Observações</p>      </td>     </tr>   <tr>    <td>    <p>01 </p>      </td>    <td>    <p>1<del>º</del> registro </p>       </td>    </tr>   <tr>    <td>    <p>02 </p>      </td>    <td>    <p>demais registros:    informações de cada estabelecimento exportador </p>       </td>    </tr>  </tbody></table>

III - o tamanho de cada registro será de 190 bytes, acrescidos de quebra de linha - CR/LF (carriage return/line feed) - ao final de cada registro, observando organização seqüencial e codificação ASCII;

IV - o Registro Tipo 01 - Totalizador da Unidade Federada - será assim composto:

Nº Denominação do Campo Conteúdo Tamanho Posição Formato 01 Tipo do registro "01" 02 1 2 N 02 UF Sigla da Unidade da Federação de localização do estabelecimento exportador 02 3 4 X 03 Ano/mês Ano e mês de competência ao qual se referem as informações 06 5 10 N 04 Total das exportações Valor total das operações e prestações de exportação dos estabelecimentos exportadores 13 11 23 N 05 Total das operações e prestações Valor total das operações e prestações dos estabelecimentos exportadores 13 24 36 N 06 Total dos créditos de ICMS Valor total dos créditos de ICMS dos estabelecimentos exportadores 13 37 49 N 07 Total dos saldos credores do ICMS Valor total dos saldos credores dos estabelecimentos exportadores 13 50 62 N 08 Transferências de saldo credor Valor total dos créditos acumulados que os estabelecimentos exportadores transferiram no mês de competência 13 63 75 N 09 Quantidade de registros tipo 02 Quantidade de registros tipo 02 referentes ao mês de competência 4 76 79 N 10 Observações Informações complementares 109 80 190 X

<table>   <tbody><tr>    <td>    <p>N<del>º</del></p>      </td>    <td>    <p>Denominação do Campo</p>       </td>    <td>    <p>Conteúdo</p>      </td>    <td>    <p>Tamanho</p>      </td>    <td colspan="2">     <p>Posição</p>      </td>    <td>    <p>Formato</p>      </td>    </tr>   <tr>    <td>     <p>01 </p>      </td>    <td>    <p>Tipo do    registro </p>      </td>    <td>    <p>"01"    </p>       </td>    <td>    <p>02</p>      </td>    <td>    <p>1</p>      </td>    <td>     <p>2</p>      </td>    <td>    <p>N</p>      </td>    </tr>   <tr>    <td>     <p>02 </p>      </td>    <td>    <p>UF </p>      </td>    <td>    <p>Sigla da    Unidade da Federação de localização do estabelecimento exportador </p>       </td>    <td>    <p>02</p>      </td>    <td>    <p>3</p>      </td>    <td>     <p>4</p>      </td>    <td>    <p>X</p>      </td>    </tr>   <tr>    <td>     <p>03 </p>      </td>    <td>    <p>Ano/mês </p>      </td>    <td>    <p>Ano e mês    de competência ao qual se referem as informações </p>       </td>    <td>    <p>06</p>      </td>    <td>    <p>5</p>      </td>    <td>     <p>10</p>      </td>    <td>    <p>N</p>      </td>    </tr>   <tr>    <td>     <p>04 </p>      </td>    <td>    <p>Total das    exportações </p>      </td>    <td>    <p>Valor    total das operações e prestações de exportação dos estabelecimentos    exportadores </p>       </td>    <td>    <p>13</p>      </td>    <td>    <p>11</p>      </td>    <td>     <p>23</p>      </td>    <td>    <p>N</p>      </td>    </tr>   <tr>    <td>     <p>05 </p>      </td>    <td>    <p>Total das    operações e prestações </p>      </td>    <td>    <p>Valor    total das operações e prestações dos estabelecimentos exportadores </p>       </td>    <td>    <p>13</p>      </td>    <td>    <p>24</p>      </td>    <td>     <p>36</p>      </td>    <td>    <p>N</p>      </td>    </tr>   <tr>    <td>     <p>06 </p>      </td>    <td>    <p>Total dos créditos    de ICMS </p>      </td>    <td>    <p>Valor    total dos créditos de ICMS dos estabelecimentos exportadores </p>       </td>    <td>    <p>13</p>      </td>    <td>    <p>37</p>      </td>    <td>     <p>49</p>      </td>    <td>    <p>N</p>      </td>    </tr>   <tr>    <td>     <p>07 </p>      </td>    <td>    <p>Total dos    saldos credores do ICMS </p>      </td>    <td>    <p>Valor    total dos saldos credores dos estabelecimentos exportadores </p>       </td>    <td>    <p>13</p>      </td>    <td>    <p>50</p>      </td>    <td>     <p>62</p>      </td>    <td>    <p>N</p>      </td>    </tr>   <tr>    <td>     <p>08 </p>      </td>    <td>    <p>Transferências    de saldo credor </p>      </td>    <td>    <p>Valor    total dos créditos acumulados que os estabelecimentos exportadores    transferiram no mês de competência </p>       </td>    <td>    <p>13</p>      </td>    <td>    <p>63</p>      </td>    <td>     <p>75</p>      </td>    <td>    <p>N</p>      </td>    </tr>   <tr>    <td>     <p>09 </p>      </td>    <td>    <p>Quantidade    de registros tipo 02 </p>      </td>    <td>    <p>Quantidade    de registros tipo 02 referentes ao mês de competência </p>       </td>    <td>    <p>4</p>      </td>    <td>    <p>76</p>      </td>    <td>     <p>79</p>      </td>    <td>    <p>N</p>      </td>    </tr>   <tr>    <td>     <p>10 </p>      </td>    <td>    <p>Observações    </p>      </td>    <td>    <p>Informações    complementares </p>       </td>    <td>    <p>109</p>      </td>    <td>    <p>80</p>      </td>    <td>     <p>190</p>      </td>    <td>    <p>X</p>      </td>    </tr>  </tbody></table>

V - o Registro Tipo 02 - Informações dos Estabelecimentos Exportadores - será assim composto:

Nº Denominação do Campo Conteúdo Tamanho Posição Formato 01 Tipo do registro "02" 02 1 2 N 02 UF Sigla da Unidade da Federação de localização do estabelecimento exportador 02 3 4 X 03 Ano/mês Ano e mês de competência ao qual se referem as informações 06 5 10 N 04 CNPJ CNPJ do estabelecimento exportador 14 11 24 N 05 Inscrição Estadual Inscrição Estadual do estabelecimento exportador 14 25 38 X 06 Exportações Valor das operações e prestações de exportação do estabelecimento exportador 13 39 51 N 07 Operações e Prestações Valor total das operações e prestações do estabelecimento exportador 13 52 64 N 08 Créditos de ICMS Valor total dos créditos dos ICMS do estabelecimento exportador 13 65 77 N 09 Saldo credor do ICMS Valor do saldo credor total apurado pelo estabelecimento exportador no mês de competência 13 78 90 N 10 Transferências de saldo credor Valor de créditos acumulados que o estabelecimento exportador transferiu no mês de competência 13 91 103 N 11 Observações Informações complementares 87 104 190 X

<table>   <tbody><tr>    <td>    <p>N<del>º</del></p>      </td>    <td>     <p>Denominação    do Campo</p>      </td>    <td>    <p>Conteúdo</p>      </td>    <td>    <p>Tamanho</p>       </td>    <td colspan="2">    <p>Posição</p>      </td>    <td>    <p>Formato</p>      </td>    </tr>    <tr>    <td>    <p>01</p>      </td>    <td>    <p>Tipo do    registro</p>      </td>    <td>     <p>"02"</p>      </td>    <td>    <p>02</p>      </td>    <td>    <p>1</p>       </td>    <td>    <p>2</p>      </td>    <td>    <p>N</p>      </td>    </tr>    <tr>    <td>    <p>02</p>      </td>    <td>    <p>UF</p>      </td>    <td>     <p>Sigla da    Unidade da Federação de localização do estabelecimento exportador</p>      </td>    <td>    <p>02</p>      </td>    <td>    <p>3</p>       </td>    <td>    <p>4</p>      </td>    <td>    <p>X</p>      </td>    </tr>    <tr>    <td>    <p>03</p>      </td>    <td>    <p>Ano/mês</p>      </td>    <td>     <p>Ano e mês    de competência ao qual se referem as informações</p>      </td>    <td>    <p>06</p>      </td>    <td>    <p>5</p>       </td>    <td>    <p>10</p>      </td>    <td>    <p>N</p>      </td>    </tr>    <tr>    <td>    <p>04</p>      </td>    <td>    <p>CNPJ</p>      </td>    <td>     <p>CNPJ do    estabelecimento exportador</p>      </td>    <td>    <p>14</p>      </td>    <td>    <p>11</p>       </td>    <td>    <p>24</p>      </td>    <td>    <p>N</p>      </td>    </tr>    <tr>    <td>    <p>05</p>      </td>    <td>    <p>Inscrição    Estadual</p>      </td>    <td>     <p>Inscrição    Estadual do estabelecimento exportador</p>      </td>    <td>    <p>14</p>      </td>    <td>    <p>25</p>       </td>    <td>    <p>38</p>      </td>    <td>    <p>X</p>      </td>    </tr>    <tr>    <td>    <p>06</p>      </td>    <td>    <p>Exportações</p>      </td>    <td>     <p>Valor das    operações e prestações de exportação do estabelecimento exportador</p>      </td>    <td>    <p>13</p>      </td>    <td>    <p>39</p>       </td>    <td>    <p>51</p>      </td>    <td>    <p>N</p>      </td>    </tr>    <tr>    <td>    <p>07</p>      </td>    <td>    <p>Operações    e Prestações</p>      </td>    <td>     <p>Valor    total das operações e prestações do estabelecimento exportador</p>      </td>    <td>    <p>13</p>      </td>    <td>    <p>52</p>       </td>    <td>    <p>64</p>      </td>    <td>    <p>N</p>      </td>    </tr>    <tr>    <td>    <p>08</p>      </td>    <td>    <p>Créditos    de ICMS</p>      </td>    <td>     <p>Valor    total dos créditos dos ICMS do estabelecimento exportador</p>      </td>    <td>    <p>13</p>      </td>    <td>    <p>65</p>       </td>    <td>    <p>77</p>      </td>    <td>    <p>N</p>      </td>    </tr>    <tr>    <td>    <p>09</p>      </td>    <td>    <p>Saldo    credor do ICMS</p>      </td>    <td>     <p>Valor do    saldo credor total apurado pelo estabelecimento exportador no mês de    competência</p>      </td>    <td>    <p>13</p>      </td>    <td>    <p>78</p>       </td>    <td>    <p>90</p>      </td>    <td>    <p>N</p>      </td>    </tr>    <tr>    <td>    <p>10</p>      </td>    <td>    <p>Transferências    de saldo credor</p>      </td>    <td>     <p>Valor de    créditos acumulados que o estabelecimento exportador transferiu no mês de    competência</p>      </td>    <td>    <p>13</p>      </td>    <td>    <p>91</p>       </td>    <td>    <p>103</p>      </td>    <td>    <p>N</p>      </td>    </tr>    <tr>    <td>    <p>11</p>      </td>    <td>    <p>Observações</p>      </td>    <td>     <p>Informações    complementares</p>      </td>    <td>    <p>87</p>      </td>    <td>    <p>104</p>       </td>    <td>    <p>190</p>      </td>    <td>    <p>X</p>      </td>    </tr>   </tbody></table>

VI - o formato dos campos será:

a) numérico (N), sem sinal, não compactado, alinhado à direita, suprimidos a vírgula e os pontos decimais, com as posições não significativas zeradas.

b) alfanumérico (X) - alinhado à esquerda, com as posições não significativas em branco.

VII - preenchimento dos campos:

a) numérico - na ausência de informação, os campos deverão ser preenchidos com zeros, sendo que o campo ano/mês de competência deverá ser expresso no formato "AAAAMM".

b) alfanumérico - na ausência de informação, os campos deverão ser preenchidos com espaços em brancos.

**§ 3º** Preferencialmente, o arquivo magnético de que trata o § 2º deste artigo será do tipo Microsoft Excel, seguindo, nas colunas da planilha, o padrão estabelecido para cada campo dos respectivos registros, sendo que os campos relativos a valores deverão ter separador de centavos delimitado por vírgula, com duas casas decimais.

**§ 4º** Considera-se mês de competência, para efeito desta Portaria, o mês da ocorrência das respectivas operações e prestações.

**§ 5º** Em cada mês de competência, deverão ser incluídas as informações de todos os estabelecimentos que realizaram as operações ou prestações a que se refere o art. 1º no ano de 2009, mesmo que não as tenham realizado no mês de competência, incluindo-se aqueles que passem a realizar esse tipo de operações ou prestação no exercício de 2010.

**§ 6º** As informações prestadas deverão ser preferencialmente coletadas a partir das guias de informação dos contribuintes do ICMS.

**§ 7º** A Secretaria da Receita Federal do Brasil poderá editar instruções complementares quanto à forma de prestação das informações prevista nesta Portaria.

**Art. 2º** As informações relativas a cada mês de competência deverão ser prestadas pelas Unidades da Federação nos seguintes prazos:

I - até 15 de outubro de 2010, em relação aos meses de janeiro a agosto de 2010 e dos meses de 2009, em relação a Estados que não tenham efetuado a remessa de todas as informações requeridas na Portaria 363, de 2 julho de 2009 (DOU de 07/07/2009);

II - até o 5º dia útil do segundo mês subseqüente, em relação aos demais meses de 2010.

**Art. 3º** Esta Portaria entra em vigor na data de sua publicação.

GUIDO MANTEGA
