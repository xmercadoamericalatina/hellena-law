---
titulo: "Portaria ALF/PGA nº 31, de 26 de junho de 2012"
orgao: "Alfândega da Receita Federal do Brasil no Porto de Paranaguá"
tipo: "Portaria"
numero: "31"
data: "2012-06-26"
revogada: false
evidencia_revogacao: "vigente:true"
vigente_fonte: true
versao_texto: "publicação original — visão original da fonte"
publicacao: "Publicado(a) no DOU de 28/06/2012, seção 1, página 171"
data_publicacao: "2012-06-28"
fonte: "https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/144264/visao/original"
fonte_api: "https://normasinternet2.receita.fazenda.gov.br/api/consulta-externa/ato/144264/visao/original"
fonte_indice: "https://normas.receita.fazenda.gov.br/api/indexacao/ato/pesquisar"
id_rfb: "144264"
sha256_texto: "7ead90bee0e3732250647ae671c8240a6652b55852e2511a7b53d5cb4a845ab3"
baixado_em: "2026-10-21"
---
# Portaria ALF/PGA nº 31, de 26 de junho de 2012

Disciplina a utilização de meio físico para controle de entrada e saída de pessoas em recinto sob controle aduaneiro, na jurisdição da ALF/PGA, e dá outras providências.

O INSPETOR-CHEFE DA ALFÂNDEGA DA RECEITA FEDERAL DO BRASIL DO PORTO DE PARANAGUÁ, no uso da atribuição do inciso VI do art. 314 do Regimento Interno da Secretaria da Receita Federal do Brasil, aprovado pela Portaria MF n.º 203, de 14 de maio de 2012, resolve:

**Art. 1°** O meio físico de controle de entrada e saída de pessoas em recinto sob controle aduaneiro, na jurisdição da desta Alfândega, obedecerá ao disposto neste ato.

**Art. 2º** O recinto deverá manter os controles de acesso, inclusive solicitando os documentos e dados necessários ao credenciamento de pessoas que pleiteiam o acesso, sendo facultada a adoção de outras providências de controle de acesso que considere pertinentes às normas de segurança.

**Art. 3º** O recinto deverá, após atendidas as normas de segurança e controle, efetuar o credenciamento do meio físico nos sistemas de controle de acesso do mesmo, nos termos do previsto nos anexos I e II da presente Portaria.

**Art. 4º** Caso a pessoa que pleiteia o credenciamento esteja munida de meio físico (crachá) já fornecido por outro recinto da jurisdição nos moldes previstos nesta Portaria, e sendo passível a autorização nos mesmos códigos de acesso constantes do crachá, o recinto deverá vincular este ao credenciamento da pessoa, permitindo que o mesmo acesse o recinto utilizando o meio físico que já possui.

**Parágrafo único.** Caso os códigos de acesso do meio físico fornecido por outro recinto sejam distintos dos permitidos no recinto em que a pessoa está pleiteando o acesso, o recinto deverá fornecer outro meio físico em que constem apenas os códigos de acesso possíveis.

Art 5º O sistema de controle de acesso deverá detectar entradas ou saídas em duplicidade e impedir o acesso até que seja registrada justificativa detalhada do motivo da falha.

**Art. 6º** Esta Portaria entra em vigor na data de sua publicação.

JACKSON ALUIR CORBARI

## Anexo I

1\. Os cartões deverão obedecer ao previsto na norma ISO 14443A. Cada cartão deverá armazenar, pelo menos, 6144 bits de dados, divididos em 16 setores (numerados de 0 a 15), cada setor dividido em 3 blocos (numerados de 0 a 2), cada bloco composto por 16 bytes (numerados de 0 a 15) e cada byte composto por 8 bits.

2\. O setor inicial (de número 0) não será utilizado;

3\. O segundo setor (de número 1) conterá os dados básicos de identificação do cartão:

3.1. Identificador do cartão: um número de 40 bits localizado nos 5 primeiros bytes (números 0 até 4) do bloco 0, contendo o CPF (somente números) do proprietário do cartão;

3.2. Data de emissão: (o total de dias transcorridos desde 01/01/2000) em 16 bits localizado nos 2 próximos bytes (números 5 e 6) do bloco 0;

3.3. Validade: (número de dias - DDDD) em 16 bits localizados nos 2 próximos bytes (números 7 e 8) do bloco 0;

3.4. Versão: 8 bits localizados no próximo byte (número 9) do bloco 0;

3.5. Recinto Emissor: 32 bits localizados nos 4 próximos bytes (10, 11, 12 e 13) do bloco 0, contendo o código do recinto no Siscomex;

4\. O terceiro setor (de número 2) conterá os mesmos dados do segundo setor (de número 1), atualizados simultaneamente a título de backup;

5\. Cada setor deverá apresentar nos últimos dois bytes (nros 14 e 15) do terceiro bloco (nro 2) CRC (16 bits) de todo o setor;

6\. No fornecimento do cartão o campo Validade deverá conter o valor 9999

7\. A cada entrada do usuário em um recinto o sistema deve verificar em seu sistema se o crachá apresentado está com status “cancelado”:

7.1. Caso esteja, NÃO PERMITIR o acesso;

7.2. Caso não esteja, verificar se a data de emissão mais o conteúdo do campo validade resultam em data MAIOR que a data atual:

7.2.1. Caso afirmativo, PERMITIR o acesso;

7.2.2. Caso contrário, NÃO PERMITIR o acesso;

8\. Os bytes devem ser gravados no sistema Little Endian.

## Anexo II

<table>   <tr>    <td>    <p>St.</p>    </td>    <td>    <p>Bl.</p>    </td>    <td>    <p>0</p>    </td>    <td>    <p>1</p>    </td>    <td>    <p>2</p>    </td>    <td>    <p>3</p>    </td>    <td>    <p>4</p>    </td>    <td>    <p>5</p>    </td>    <td>    <p>6</p>    </td>    <td>    <p>7</p>    </td>    <td>    <p>8</p>    </td>    <td>    <p>9</p>    </td>    <td>    <p>10</p>    </td>    <td>    <p>11</p>    </td>    <td>    <p>12</p>    </td>    <td>    <p>13</p>    </td>    <td>    <p>14</p>    </td>    <td>    <p>15</p>    </td>   </tr>   <tr>    <td rowspan="3">    <p>0</p>    </td>    <td>    <p>0</p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>   </tr>   <tr>    <td>    <p>1</p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>   </tr>   <tr>    <td>    <p>2</p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>   </tr>   <tr>    <td rowspan="3">    <p>1</p>    </td>    <td>    <p>0</p>    </td>    <td colspan="5">    <p>CPF</p>    </td>    <td colspan="2">    <p>Emissão</p>    </td>    <td colspan="2">    <p>Validade</p>    </td>    <td>    <p>Versão</p>    </td>    <td colspan="4">    <p>Recinto    Emissor</p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>   </tr>   <tr>    <td>    <p>1</p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>   </tr>   <tr>    <td>    <p>2</p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td>    <p> </p>    </td>    <td colspan="2">    <p>CRC</p>    </td>   </tr>   <tr>    <td rowspan="3">    <p>2</p>    </td>    <td>    <p>0</p>    </td>    <td colspan="16" rowspan="3">    <p>BACKUP    SETOR 1</p>    </td>   </tr>   <tr>    <td>    <p>1</p>    </td>   </tr>   <tr>    <td>    <p>2</p>    </td>   </tr>  </table>
