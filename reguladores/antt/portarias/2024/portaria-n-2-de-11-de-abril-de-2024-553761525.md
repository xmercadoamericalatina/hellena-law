---
titulo: "PORTARIA Nº 2, DE 11 DE ABRIL DE 2024"
orgao: "Ministério dos Transportes/Agência Nacional de Transportes Terrestres/Superintendência de Serviços de Transporte Rodoviário de Passageiros"
tipo: "Portaria"
numero: "2"
data: 2024-04-11
revogada: null
versao_texto: "publicação original"
publicacao: "DOU de 12/04/2024, seção 1, p. 128"
data_publicacao: 2024-04-12
edicao: "71"
fonte: "https://www.in.gov.br/web/dou/-/portaria-n-2-de-11-de-abril-de-2024-553761525"
sha256_html_fonte: b5638a9c82d7f037e14ddf514e08d1e472fe0a93fee4bdbf5dc13f6c98f328b0
baixado_em: 2026-10-16
---
# PORTARIA Nº 2, DE 11 DE ABRIL DE 2024

PORTARIA Nº 2, DE 11 DE ABRIL DE 2024

O Superintendente de Serviços de Transporte Rodoviário de Passageiros da Agência Nacional de Transportes Terrestres, no uso de suas atribuições e em conformidade com o art. 25-A da Resolução ANTT nº 4.499, de 28 de novembro de 2014, resolve:

**Art. 1º** Aprovar o Documento de Interface de Software - Versão 3.0, que define as especificações de estrutura de dados dos registros do Sistema de Monitoramento do Transporte Rodoviário Coletivo Interestadual e Internacional de Passageiros a serem transmitidos à ANTT pelas empresas dos serviços rodoviário regular, rodoviário fretado e semiurbano regular.

**Parágrafo único.** O documento de que trata o caput será disponibilizado no sítio eletrônico da ANTT - https://www.gov.br/antt/pt-br

**Art. 2º** Os dados primários correspondem aos registros (logs) a serem gerados pelos Subsistemas Não Embarcado e Embarcado. Um Log de dados corresponde a um conjunto de dados bem definidos e estruturados, segundo uma sequência específica.

**Art. 3º** O Subsistema Não Embarcado é composto pelos seguintes logs:

<table>    <tbody>     <tr></tr>     <tr>      <td rowspan="1" colspan="1"><p>LogVendaPassagem</p></td>      <td rowspan="1" colspan="1"><p>Rodoviário Regular</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>LogRegistroOcorrenciaRodoviario</p></td>      <td rowspan="1" colspan="1"><p>Rodoviário Regular</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>LogCancelarPassagem</p></td>      <td rowspan="1" colspan="1"><p>Rodoviário Regular</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>LogCartaoEmitidoRecargaEfetuada</p></td>      <td rowspan="1" colspan="1"><p>Semiurbano Regular</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>LogRegistroOcorrenciaSemiUrbano</p></td>      <td rowspan="1" colspan="1"><p>Semiurbano Regular</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>LogReembolsocartao</p></td>      <td rowspan="1" colspan="1"><p>Semiurbano Regular</p></td>     </tr>    </tbody>   </table>

**Art. 4º** O Subsistema Embarcado é composto pelos seguintes logs:

<table>    <tbody>     <tr></tr>     <tr>      <td rowspan="1" colspan="1"><p>LogVelocidadeTempoLocalizacao</p></td>      <td rowspan="1" colspan="1"><p>Rodoviário Regular, Semiurbano Regular, Rodoviário Fretado</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>LogJornadaTrabalhoMotorista</p></td>      <td rowspan="1" colspan="1"><p>Rodoviário Regular, Semiurbano Regular, Rodoviário Fretado</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>LogDetectorParada</p></td>      <td rowspan="1" colspan="1"><p>Rodoviário Regular, Semiurbano Regular, Rodoviário Fretado</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>LogInicioFimViagemRegular</p></td>      <td rowspan="1" colspan="1"><p>Rodoviário Regular, Semiurbano Regular</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>LogInicioFimViagemFretado</p></td>      <td rowspan="1" colspan="1"><p>Rodoviário Fretado</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>LogBilheteEmbarque</p></td>      <td rowspan="1" colspan="1"><p>Rodoviário Regular</p></td>     </tr>     <tr>      <td rowspan="1" colspan="1"><p>LogLeitorCartaoRFID</p></td>      <td rowspan="1" colspan="1"><p>Semiurbano Regular</p></td>     </tr>    </tbody>   </table>

**Art. 5º** Todos os dados deverão ser enviados por meio de Webservice disponibilizado pela ANTT, em arquivo no formato XML, de acordo com padrão definido em arquivo XSD, ou através de formato binário compacto, que utilizará o protocolo UDP.

**§ 1º** A empresa operadora deve disponibilizar os dados, por meio de um ponto de disponibilização, através de conexão segura protegida por certificado digital padrão ICP-Brasil, ao Webservice da ANTT, contendo todos os dados especificados no Documento de Interface de Software.

**§ 2º** Todos os arquivos deverão ser assinados digitalmente, carimbados com carimbador de tempo, todos com certificado digital padrão ICP-Brasil e criptografados com criptografia de chave pública RSA de 2048 bits.

**Art. 6º** Todos os dados deverão ser enviados, conforme os protocolos de transmissão e de segurança especificados pela área de tecnologia da ANTT.

**Art. 7º** Os registros (logs) recebidos serão validados em função da compatibilidade entre as informações transmitidas e as cadastradas na ANTT.

**§ 1º** Os registros (logs) transmitidos fora dos prazos estabelecidos ou transmitidos em inconformidade com as especificações não serão considerados válidos.

**§ 2º** Somente o recebimento do registro (log) pela ANTT não garante a sua validação.

**Art. 8º** A ANTT disponibilizará à Empresa de transporte um recibo eletrônico assinado digitalmente com certificado padrão ICP-Brasil, contendo informações de envio e recebimento.

**§ 1º** Os recibos eletrônicos serão disponibilizados pela ANTT no formato padrão aberto Portable Document Format (PDF), assinados digitalmente com certificados padrão ICP-Brasil.

**§ 2º** O recibo eletrônico será emitido e disponibilizado pela ANTT no ato do envio após a verificação de integridade do arquivo disponibilizado pela Empresa de transporte.

**§ 3º** Solicitações de nova disponibilização dos dados devido a erros de transmissão ou inconsistência dos dados podem ser realizadas pela ANTT a qualquer tempo.

**§ 4º** O recibo eletrônico é a garantia para a Empresa de transporte do correto recebimento dos dados exigidos pela ANTT e deve ser armazenado por no mínimo 05 (cinco) anos.

**Art. 9º** Será de responsabilidade das empresas a aquisição, a implantação e a manutenção dos equipamentos e dos sistemas necessários para o atendimento a esta Portaria.

**Art. 10** As alterações promovidas pelo Documento de Interface de Software - Versão 3.0 deverão ser implementadas em até 90 (noventa) dias a partir da vigência desta Portaria.

Parágrafo Único. Fica revogado o Documento de Interface de Software - Versão 2.1, de 15 de março de 2019, findo o prazo estabelecido no caput.

**Art. 11** Esta Portaria entra em vigor na data de sua publicação.

JULIANO DE BARROS SAMÔR
