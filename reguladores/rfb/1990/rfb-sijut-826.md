---
titulo: "Ato Declaratório Cief nº 11, de 10 de outubro de 1990"
orgao: "Coordenação de Informações Econômico-Fiscais"
tipo: "Ato Declaratório"
numero: "11"
data: "1990-10-10"
revogada: false
evidencia_revogacao: "vigente:true"
vigente_fonte: true
versao_texto: "publicação original — visão original da fonte"
publicacao: "Publicado(a) no DOU de 11/10/1990, seção 1, página 19293"
data_publicacao: "1990-10-11"
fonte: "https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/826/visao/original"
fonte_api: "https://normasinternet2.receita.fazenda.gov.br/api/consulta-externa/ato/826/visao/original"
fonte_indice: "https://normas.receita.fazenda.gov.br/api/indexacao/ato/pesquisar"
id_rfb: "826"
sha256_texto: "62a1f72ff49e975ecba5ebdbaa31383e06bcde3e2529cf0d93c976e1f518f817"
baixado_em: "2026-10-21"
---
# Ato Declaratório Cief nº 11, de 10 de outubro de 1990

Dispõe sobre a apresentação da Declaração de Imposto sobre Produtos Industrializados - DIPI, em arquivo magnético.

O COORDENADOR DO SISTEMA DE INFORMAÇÕES ECONÔMICO-FISCAIS, no uso de suas atribuições, e tendo em vista o disposto no item 5 do anexo II da Instrução Normativa do Diretor do Departamento da Receita Federal nº 113, de 26 de setembro de 1990, DECLARA:

1 A Declaração de Imposto sobre Produtos Industrializados que os contribuintes do IPI estão obrigados a apresentar, anualmente, ao Departamento da Receita Federal nos termos da IN/RF nó 113, poderá ser apresentada em arquivo magnético de acordo com o estabelecido neste ato.

2 O arquivo magnético contendo as informações que substituirá a DIPI completa deverá:

a) ser gerado segundo as normas estabelecidas pela IN/RF nº , para preenchimento da declaração em formulário plano, observadas as especificações técnicas descritas nos anexos I e II deste ato.

b) estar acompanhado de duas vias do Relatório de Acompanhamento, anexo III, deste Ato, uma das quais constituir-se-á em recibo provisório. Após a verificação pela Receita Federal de que foram observadas as especificações dos anexos I e II deste Ato, será emitido eletronicamente o Recibo Definitivo de Entrega, para envio ao estabelecimento declarante.

3 Os gabaritos dos registros descritos no Anexo II se encontrarão à disposição dos contribuintes nas Delegacias da Receita Federal.

4 O estabelecimento declarante deverá manter, por cinco anos, listagem com as informações contidas no arquivo magnético, segundo "lay out" do formulário plano.

PAULO JOBIM FILHO

## ANEXO I

ESPECIFICAÇÕES TÉCNICAS DO ARQUIVO MAGNÉTICO - IPIFITA 1 - O arquivo será gerado de acordo com os seguintes dados técnicos: a) Fita Magnética - Organização .................... seqüencial - Nº de trilhas .................. 9 trilhas - Densidade de gravação .......... 800 ou 1600 BPI - "BYTES" ........................ na configuração de 08 "bits" em EBCDIC - Tamanho do Registro............ 1.600 "bytes" (Posições) - Tamanho do bloco ............... 1.600 "bytes" - Fator de bloco ................. 10 (dez) - "Label" ........................ omitido, com um tape mark no início e outro no fi- nal do volume. - Características dos campos ..... zonado (z) caráter (c) b) Disquete 8" - Padrão ......................... IBM 3740 - "BYTES" por setor .............. 128 - Face ........................... simples - Densidade de gravação .......... simples - Tamanho do registro ............ 1.600 "bytes" (Posições) - Fator de bloco ................. 1 (um) - "Label" ........................ omitido - Características dos campos ..... zonado (z) - Multivolume .................... não permitido - Nome do arquivo ................ IPI c) Disquete 5 1/4" - Padrão de gravação lógica p/IBM/ PC ............................. DOS - Padrão de gravação para os dema- is ............................. CP/M - Padrão de gravação física ...... TRS 80, APPLE ou IBM/PC - Face ........................... simples - Densidade de gravação .......... simples ou dupla - Tamanho do registro ............ 1.600 "bytes" (Posições) - Fator de bloco ................. 1 (um) - "Label" ........................ omitido - Características dos campos ..... não compactado, Código AS- CII de "HEX 20" a "HEX 7E" - Multivolume .................... não permitido - Nome do arquivo ................ IPI - Formato de gravação ............ seqüencial. O arquivo físico deverá ser composto pelos "bytes" dos registros sem delimitadores, ou então, exclusivamente pelos delimitadores HEX ODOA entre os registros. Não serão aceitos arquivos com outros delimitadores. 2 - O arquivo IPIFITA conterá os seguintes tipos de registros: a) TIPO 0 - Registro mestre de arquivo. Será o primeiro registro do arquivo. b) TIPO 1 - Registro correspondente ao "Demonstrativo de Apuração Quinzenal do Saldo do IPI - Pág.. 1 do Formulário I. c) TIPO 2 - Registro correspondente a "Demonstração das Entradas de Mercadorias no Estabelecimento" - Pág.. 2 do Formulário I. d) TIPO 3 - Registro correspondente a "Demonstração das Saídas de Mercadorias do Estabelecimento" - Pág.: 3 do Formulário I. e) TIPO 4 - Registro correspondente ao "Demonstrativo de Créditos" - "Demonstrativo de Débitos" - "Dados sobre Pessoal Ocupado""Resumo das Entradas e Saídas de Mercadorias" - Pág.: 4 do Formulário I. f) TIPO 5 - Registro correspondente ao "Demonstrativo de Entradas e Saídas de Mercadorias" - Anexo 1. Poderão existir vários registros TIPO 5, g) TIPO 6 - Registro correspondente ao "Demonstrativo dos Estoques de Insumos" - Anexo 2. Poderão existir vários registros TIPO 6. h)TIPO 7. Registro correspondente ao "Demonstrativo dos Estoques de Produtos Acabados " - Anexo 2. Poderão existir vários registros TIPO 7. i) TIPO 8 - Registro correspondente ao "Demonstrativo dos Estoques de Mercadorias Adquiridas" - Anexo 2. Poderão existir vários registros TIPO 8. j) TIPO 9 - Registro totalizador de arquivo. Este registro é único e deve ser o último do arquivo. 3 - Os registros, no arquivo, terão a seguinte organização física: TIPO 0 - Mestre do estabelecimento. TIPO 1 - DEMONSTRATIVO - FORMULÁRIO I - Pág.. 1 TIPO 2 - DEMONSTRATIVO - FORMULÁRIO I - Pág.. 2 TIPO 3 - DEMONSTRATIVO - FORMULÁRIO I - Pág.. 3 TIPO 4 - DEMONSTRATIVO - FORMULÁRIO I - Pág. 4 TIPO 5 - DEMONSTRATIVO - ANEXO 1 " " " " " " TIPO 6 - DEMONSTRATIVO - ANEXO 2 - INSUMOS " " " " " " TIPO 7 - DEMONSTRATIVO - ANEXO 2 - PRODUTOS ACABADOS " " " " " " TIPO 8 - DEMONSTRATIVO - ANEXO 2 - MERCADORIAS ADQUIRIDAS " " " " " " TIPO 9 - REGISTRO TOTALIZADOR DO ARQUIVO 4 - As informações referentes a um estabelecimento deverão estar contidas em um único arquivo. 4.1 - Caso as informações utilizem mais de um volume, o registro TIPO 9 (REGISTRO TOTALIZADOR) deverá ser obrigatoriamente o último registro do último volume. 4.2 - Todos os dados numéricos serão zonados e completados com zeros à esquerda. 4.3 - Os campos que possuem dados monetários deverão ser informados sem centavos. 4.4 - Os campos de quantidade deverão ser informados sem decimais. 4.5 - Somente os campos que possuem dados monetários deverão ser sinalizados. 4.6 - Os campos numéricos com ausência de informações deverão ser preenchidos com zeros. 6 - O arquivo será entregue: a) juntamente com 2 (duas) vias do relatório de acompanhamento, ambas com o carimbo do C.G.C. aposto; e b) com etiqueta de identificação, contendo as informações conforme modelo abaixo: MODELO DA ETIQUETA - FITA MAGNÉTICA DECLARAÇÃO DE IMPOSTO SOBRE PRODUTOS INDUSTRIALIZADOS-IPI C.G.C. PERÍODO DE APURAÇÃO RAZÃO SOCIAL LABEL REGISTROxF.BLOCO DENSIDADE DE GRAVAÇÃO OMITIDO 1.600x10 1600 ( ) 800 ( ) Nº DE TRILHAS Nº DE VOLS. DATA DA GERAÇÃO: 9 A/B PARA USO DO SERPRO MODELO DA ETIQUETA - DISQUETE DECLARAÇÃO DE IMPOSTO SOBRE PRODUTOS INDUSTRIALIZADOS - IPI C.G.C PERÍODO DE APURAÇÃO RAZÃO SOCIAL DATA DA GERAÇÃO REGISTROxF.BLOCO EQUIPAMENTO/LINGUAGEM 5 1/4" ( )FACE: SIMPLES DENSIDADE: SIMPLES ( ) DUPLA ( ) 8" ( )FACE: SIMPLES DENSIDADE: SIMPLES PARA USO DO SERPRO: ESPECIFICAÇÕES TÉCNICAS DO ARQUIVO MAGNÉTICO - IPIFITA 1 - O arquivo será gerado de acordo com os seguintes dados técnicos: a) Fita Magnética - Organização .................... seqüencial - Nº de trilhas .................. 9 trilhas - Densidade de gravação .......... 800 ou 1600 BPI - "BYTES" ........................ na configuração de 08 "bits" em EBCDIC - Tamanho do Registro............ 1.600 "bytes" (Posições) - Tamanho do bloco ............... 1.600 "bytes" - Fator de bloco ................. 10 (dez) - "Label" ........................ omitido, com um tape mark no início e outro no fi- nal do volume. - Características dos campos ..... zonado (z) caráter (c) b) Disquete 8" - Padrão ......................... IBM 3740 - "BYTES" por setor .............. 128 - Face ........................... simples - Densidade de gravação .......... simples - Tamanho do registro ............ 1.600 "bytes" (Posições) - Fator de bloco ................. 1 (um) - "Label" ........................ omitido - Características dos campos ..... zonado (z) - Multivolume .................... não permitido - Nome do arquivo ................ IPI c) Disquete 5 1/4" - Padrão de gravação lógica p/IBM/ PC ............................. DOS - Padrão de gravação para os dema- is ............................. CP/M - Padrão de gravação física ...... TRS 80, APPLE ou IBM/PC - Face ........................... simples - Densidade de gravação .......... simples ou dupla - Tamanho do registro ............ 1.600 "bytes" (Posições) - Fator de bloco ................. 1 (um) - "Label" ........................ omitido - Características dos campos ..... não compactado, Código AS- CII de "HEX 20" a "HEX 7E" - Multivolume .................... não permitido - Nome do arquivo ................ IPI - Formato de gravação ............ seqüencial. O arquivo físico deverá ser composto pelos "bytes" dos registros sem delimitadores, ou então, exclusivamente pelos delimitadores HEX ODOA entre os registros. Não serão aceitos arquivos com outros delimitadores. 2 - O arquivo IPIFITA conterá os seguintes tipos de registros: a) TIPO 0 - Registro mestre de arquivo. Será o primeiro registro do arquivo. b) TIPO 1 - Registro correspondente ao "Demonstrativo de Apuração Quinzenal do Saldo do IPI - Pág.. 1 do Formulário I. c) TIPO 2 - Registro correspondente a "Demonstração das Entradas de Mercadorias no Estabelecimento" - Pág.. 2 do Formulário I. d) TIPO 3 - Registro correspondente a "Demonstração das Saídas de Mercadorias do Estabelecimento" - Pág.: 3 do Formulário I. e) TIPO 4 - Registro correspondente ao "Demonstrativo de Créditos" - "Demonstrativo de Débitos" - "Dados sobre Pessoal Ocupado""Resumo das Entradas e Saídas de Mercadorias" - Pág.: 4 do Formulário I. f) TIPO 5 - Registro correspondente ao "Demonstrativo de Entradas e Saídas de Mercadorias" - Anexo 1. Poderão existir vários registros TIPO 5, g) TIPO 6 - Registro correspondente ao "Demonstrativo dos Estoques de Insumos" - Anexo 2. Poderão existir vários registros TIPO 6. h)TIPO 7. Registro correspondente ao "Demonstrativo dos Estoques de Produtos Acabados " - Anexo 2. Poderão existir vários registros TIPO 7. i) TIPO 8 - Registro correspondente ao "Demonstrativo dos Estoques de Mercadorias Adquiridas" - Anexo 2. Poderão existir vários registros TIPO 8. j) TIPO 9 - Registro totalizador de arquivo. Este registro é único e deve ser o último do arquivo. 3 - Os registros, no arquivo, terão a seguinte organização física: TIPO 0 - Mestre do estabelecimento. TIPO 1 - DEMONSTRATIVO - FORMULÁRIO I - Pág.. 1 TIPO 2 - DEMONSTRATIVO - FORMULÁRIO I - Pág.. 2 TIPO 3 - DEMONSTRATIVO - FORMULÁRIO I - Pág.. 3 TIPO 4 - DEMONSTRATIVO - FORMULÁRIO I - Pág. 4 TIPO 5 - DEMONSTRATIVO - ANEXO 1 " " " " " " TIPO 6 - DEMONSTRATIVO - ANEXO 2 - INSUMOS " " " " " " TIPO 7 - DEMONSTRATIVO - ANEXO 2 - PRODUTOS ACABADOS " " " " " " TIPO 8 - DEMONSTRATIVO - ANEXO 2 - MERCADORIAS ADQUIRIDAS " " " " " " TIPO 9 - REGISTRO TOTALIZADOR DO ARQUIVO 4 - As informações referentes a um estabelecimento deverão estar contidas em um único arquivo. 4.1 - Caso as informações utilizem mais de um volume, o registro TIPO 9 (REGISTRO TOTALIZADOR) deverá ser obrigatoriamente o último registro do último volume. 4.2 - Todos os dados numéricos serão zonados e completados com zeros à esquerda. 4.3 - Os campos que possuem dados monetários deverão ser informados sem centavos. 4.4 - Os campos de quantidade deverão ser informados sem decimais. 4.5 - Somente os campos que possuem dados monetários deverão ser sinalizados. 4.6 - Os campos numéricos com ausência de informações deverão ser preenchidos com zeros. 6 - O arquivo será entregue: a) juntamente com 2 (duas) vias do relatório de acompanhamento, ambas com o carimbo do C.G.C. aposto; e b) com etiqueta de identificação, contendo as informações conforme modelo abaixo: MODELO DA ETIQUETA - FITA MAGNÉTICA DECLARAÇÃO DE IMPOSTO SOBRE PRODUTOS INDUSTRIALIZADOS-IPI C.G.C. PERÍODO DE APURAÇÃO RAZÃO SOCIAL LABEL REGISTROxF.BLOCO DENSIDADE DE GRAVAÇÃO OMITIDO 1.600x10 1600 ( ) 800 ( ) Nº DE TRILHAS Nº DE VOLS. DATA DA GERAÇÃO: 9 A/B PARA USO DO SERPRO MODELO DA ETIQUETA - DISQUETE DECLARAÇÃO DE IMPOSTO SOBRE PRODUTOS INDUSTRIALIZADOS - IPI C.G.C PERÍODO DE APURAÇÃO RAZÃO SOCIAL DATA DA GERAÇÃO REGISTROxF.BLOCO EQUIPAMENTO/LINGUAGEM 5 1/4" ( )FACE: SIMPLES DENSIDADE: SIMPLES ( ) DUPLA ( ) 8" ( )FACE: SIMPLES DENSIDADE: SIMPLES PARA USO DO SERPRO:

A N E X O II

DESCRIÇÃO DOS REGISTROS REGISTRO TIPO 0 REGISTRO MESTRE DO ARQUIVO NOME DO POSIÇÃO CAMPO INIC. FIM TAMAN. FORMATO CONTEÚDO TIPO 01 01 01 Z Será "0". Será o primeiro registro do arquivo. Posição 2 a 9 - Num Básico Posição 10 a 13- Num. Ordem C.G.C 02 15 14 Z Posição 14 a 15 - DV Deverá estar sempre comple- to com 14 dígitos Exercício de Apuração 16 17 02 Z Será o ano do exercício de apuração Será "0" para Situação Nor- mal Será "1" para Retificação de Declaração Situação 18 18 01 C Será "2" para Encerramento Especial de Atividades Será "3"para Retificação de Declaração e Encerramento de Atividades Optante Convênio 19 19 01 Z Será "1" para optante pelo ICMS Convênio ICMS Será "2" para não optante pelo Convênio ICMS Registro Especial de 20 37 Engarrafadores 20 31 12 Z Número da Ordem 32 37 6 Z Data da Emissão Razão Social 38 92 55 C Razão Social/Denominação Comercial do Estab. Endereço 93 222 93 96 04 C Tipo de Logradouro 97 119 23 C Logradouro 120 125 06 C Número 126 144 19 C Complemento 145 163 19 C Bairro 164 168 05 C CEP 169 198 30 C Município 199 200 02 C U.F 201 211 11 C Telex 212 222 11 C Telefone Tipo de Estabele 223 224 02 Z Será um dos códigos do tipo cimento constante do Manual de pre- enchimento do IPI Atividade Econômica 225 228 04 Z Código da Atividade Econô- mica Principal "Filler" 229 1600 1372 C B R A N C O S REGISTRO TIPO 1 DEMONSTRATIVO DE APURAÇÃO QUINZENAL DO SALDO DO IPI - FORMULÁRIO I NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 Z Será "1" 1ª 02 03 02 Z Será "01" Q U 04 04 01 Será "1" I 05 19 15 Z Débito J N 20 34 15 Z Crédito A Z. 35 49 15 Z Saldo credor no período N anterior E 50 64 15 Z Saldo apurado I R 2ª 65 65 01 Z Será "2" O Q 66 80 15 Z Débito U 81 95 15 Z Crédito I 96 110 15 Z Saldo credor no período N anterior Z. 111 125 15 Z Saldo apurado 1ª 126 127 02 Z Será "02" Q U 128 128 01 Z Será "1" I 129 143 15 Z Débito F N 144 158 15 Z Crédito E Z. 159 173 15 Z Saldo credor no período V anterior E 174 188 15 Z Saldo apurado R E 2ª 189 189 01 Z Será "2" I Q 190 204 15 Z Débito R U 205 219 15 Z Crédito O I 220 234 15 Z Saldo credor no período N anterior Z. 235 249 15 Z Saldo apurado 1ª 250 251 02 Z Será "03" Q U 252 252 01 Z Será "1" I 253 267 15 Z Débito M N 268 282 15 Z Crédito A Z. 283 297 15 Z Saldo credor no período R anterior Ç 298 312 15 Z Saldo apurado O 2ª 313 313 01 Z Será "2" Q 314 328 15 Z Débito U 329 343 15 Z Crédito I 344 358 15 Z Saldo credor no período N anterior Z. 359 373 15 Z Saldo apurado 1ª 374 375 02 Z Será "04" Q U 376 376 01 Z Será "1" I 377 391 15 Z Débito A N 392 406 15 Z Crédito B Z. 407 421 15 Z Saldo credor no período R anterior I 422 436 15 Z Saldo apurado L 2ª 437 437 01 Z Será "2" Q 438 452 15 Z Débito U 453 467 15 Z Crédito I 468 482 15 Z Saldo credor no período N anterior Z. 483 497 15 Z Saldo apurado 1ª 498 499 02 Z Será "05" Q U 500 500 01 Z Será "1" I 501 515 15 Z Débito M N 516 530 15 Z Crédito A Z. 531 545 15 Z Saldo credor no período I anterior O 546 560 15 Z Saldo apurado 2ª 561 561 01 Z Será "2" Q 562 576 15 Z Débito U 577 591 15 Z Crédito I 592 606 15 Z Saldo credor no período N anterior Z. 607 621 15 Z Saldo apurado 1ª 622 623 02 Z Será "06" Q U 624 624 01 Z Será "1" I 625 639 15 Z Débito J N 640 654 15 Z Crédito U Z. 655 669 15 Z Saldo credor no período N anterior H 670 684 15 Z Saldo apurado O 2ª 685 685 01 Z Será "2" Q 686 700 15 Z Débito U 701 715 15 Z Crédito I 716 730 15 Z Saldo credor no período N anterior Z. 731 745 15 Z Saldo apurado 1ª 746 747 02 Z Será "07" Q U 748 748 01 Z Será "1" I 749 763 15 Z Débito J N 764 778 15 Z Crédito U Z. 779 793 15 Z Saldo credor no período L anterior H 794 808 15 Z Saldo apurado O 2ª 809 809 01 Z Será "2" Q 810 824 15 Z Débito U 825 839 15 Z Crédito I 840 854 15 Z Saldo credor no período N anterior Z. 855 869 15 Z Saldo apurado 1ª 870 871 02 Z Será "08" Q U 872 872 01 Z Será "1" I 873 887 15 Z Débito A N 888 902 15 Z Crédito G Z. 903 917 15 Z Saldo credor no período O anterior S 918 932 15 Z Saldo apurado T O 2ª 933 933 01 Z Será "2" Q 934 948 15 Z Débito U 949 963 15 Z Crédito I 964 978 15 Z Saldo credor no período N anterior Z. 979 993 15 Z Saldo apurado 1ª 994 995 02 Z Será "09" Q U 996 996 01 Z Será "1" I 997 1011 15 Z Débito S N 1012 1026 15 Z Crédito E Z. 1027 1041 15 Z Saldo credor no período T anterior E 1042 1056 15 Z Saldo apurado M B 2ª 1057 1057 01 Z Será "2" R Q 1058 1072 15 Z Débito O U 1073 1087 15 Z Crédito I 1088 1102 15 Z Saldo credor no período N anterior Z. 1103 1117 15 Z Saldo apurado 1ª 1118 1119 02 Z Será "10" Q U 1120 1120 01 Z Será "1" I 1121 1135 15 Z Débito O N 1136 1150 15 Z Crédito U Z. 1151 1165 15 Z Saldo credor no período T anterior U 1166 1180 15 Z Saldo apurado B R 2ª 1181 1181 01 Z Será "2" O Q 1182 1196 15 Z Débito U 1197 1211 15 Z Crédito I 1212 1226 15 Z Saldo credor no período N anterior Z. 1227 1241 15 Z Saldo apurado 1ª 1242 1243 02 Z Será "11" Q U 1244 1244 01 Z Será "1" I 1245 1259 15 Z Débito N N 1260 1274 15 Z Crédito O Z. 1275 1289 15 Z Saldo credor no período V anterior E 1290 1304 15 Z Saldo apurado M B 2ª 1305 1305 01 Z Será "2" R Q 1306 1320 15 Z Débito O U 1321 1335 15 Z Crédito I 1336 1350 15 Z Saldo credor no período N anterior Z. 1351 1365 15 Z Saldo apurado 1ª 1366 1367 02 Z Será "12" Q U 1368 1368 01 Z Será "1" I 1369 1383 15 Z Débito D N 1384 1398 15 Z Crédito E Z. 1399 1413 15 Z Saldo credor no período Z anterior E 1414 1428 15 Z Saldo apurado M B 2ª 1429 1429 01 Z Será "2" R Q 1430 1444 15 Z Débito O U 1445 1459 15 Z Crédito I 1460 1474 15 Z Saldo credor no período N anterior Z. 1475 1489 15 Z Saldo apurado FILLER 1490 1600 111 C B R A N C O S - ESTE REGISTRO É ÚNICO E CORRESPONDE A PÁG.. 1 DO FORMULÁRIO I - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS. REGISTRO TIPO 2 DEMONSTRAÇÃO DAS ENTRADAS DE MERCADORIAS NO ESTABELECIMENTO - FORMULÁRIO I NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 Z Será "2". Código 02 04 03 Z Será "111" Fiscal 05 19 15 Z Base de Cálculo 111 20 34 15 Z Imposto creditado 35 49 15 Z Operações sem direito a crédito de Imposto Código 50 52 03 Z Será "111" Fiscal 53 67 15 Z Base de Cálculo 111 68 82 15 Z Imposto creditado 83 97 15 Z Operações sem direito a crédito de Imposto Código 98 100 03 Z Será "112" Fiscal 101 115 15 Z Base de Cálculo 112 116 130 15 Z Imposto creditado 131 145 15 Z Operações sem direito a crédito de Imposto Código 146 148 03 Z Será "113" Fiscal 149 163 15 Z Base de Cálculo 113 164 178 15 Z Imposto creditado 179 193 15 Z Operações sem direito a crédito de Imposto Código 194 196 03 Z Será "121" Fiscal 197 211 15 Z Base de Cálculo 121 212 226 15 Z Imposto creditado 227 241 15 Z Operações sem direito a crédito de Imposto Código 242 244 03 Z Será "121" Fiscal 245 259 15 Z Base de Cálculo 121 260 274 15 Z Imposto creditado 275 289 15 Z Operações sem direito a crédito de Imposto Código 290 292 03 Z Será "122" Fiscal 293 307 15 Z Base de Cálculo 122 308 322 15 Z Imposto creditado 323 337 15 Z Operações sem direito a crédito de Imposto Código 338 340 03 Z Será "131" Fiscal 341 355 15 Z Base de Cálculo 131 356 370 15 Z Imposto creditado 371 385 15 Z Operações sem direito a crédito de Imposto Código 386 388 03 Z Será "132" Fiscal 389 403 15 Z Base de Cálculo 132 404 418 15 Z Imposto creditado 419 433 15 Z Operações sem direito a crédito de Imposto Código 434 436 03 Z Será "193" Fiscal 437 451 15 Z Base de Cálculo 193 452 466 15 Z Imposto creditado 467 481 15 Z Operações sem direito a crédito de Imposto Código 482 484 03 Z Será "194" Fiscal 485 499 15 Z Base de Cálculo 194 500 514 15 Z Imposto creditado 515 529 15 Z Operações sem direito a crédito de Imposto Código 530 532 03 Z Será "199" Fiscal 533 547 15 Z Base de Cálculo 199 548 562 15 Z Imposto creditado 563 577 15 Z Operações sem direito a crédito de Imposto Código 578 580 03 Z Será "211" Fiscal 581 595 15 Z Base de Cálculo 211 596 610 15 Z Imposto creditado 611 625 15 Z Operações sem direito a crédito de Imposto Código 626 628 03 Z Será "211" Fiscal 629 643 15 Z Base de Cálculo 211 644 658 15 Z Imposto creditado 659 673 15 Z Operações sem direito a crédito de Imposto Código 674 676 03 Z Será "212" Fiscal 677 691 15 Z Base de Cálculo 212 692 706 15 Z Imposto creditado 707 721 15 Z Operações sem direito a crédito de Imposto Código 722 724 03 Z Será "213" Fiscal 725 739 15 Z Base de Cálculo 213 740 754 15 Z Imposto creditado 755 769 15 Z Operações sem direito a crédito de Imposto Código 770 772 03 Z Será "221" Fiscal 773 787 15 Z Base de Cálculo 221 788 802 15 Z Imposto creditado 803 817 15 Z Operações sem direito a crédito de Imposto Código 818 820 03 Z Será "221" Fiscal 821 835 15 Z Base de Cálculo 221 836 850 15 Z Imposto creditado 851 865 15 Z Operações sem direito a crédito de Imposto Código 866 868 03 Z Será "222" Fiscal 869 883 15 Z Base de Cálculo 222 884 898 15 Z Imposto creditado 899 913 15 Z Operações sem direito a crédito de Imposto Código 914 916 03 Z Será "231" Fiscal 917 931 15 Z Base de Cálculo 231 932 946 15 Z Imposto creditado 947 961 15 Z Operações sem direito a crédito de Imposto Código 962 964 03 Z Será "232" Fiscal 965 979 15 Z Base de Cálculo 232 980 994 15 Z Imposto creditado 995 1009 15 Z Operações sem direito a crédito de Imposto Código 1010 1012 03 Z Será "293" Fiscal 1013 1027 15 Z Base de Cálculo 293 1028 1042 15 Z Imposto creditado 1043 1057 15 Z Operações sem direito a crédito de Imposto Código 1058 1060 03 Z Será "294" Fiscal 1061 1075 15 Z Base de Cálculo 294 1076 1090 15 Z Imposto creditado 1091 1105 15 Z Operações sem direito a crédito de Imposto Código 1106 1108 03 Z Será "299" Fiscal 1109 1123 15 Z Base de Cálculo 299 1124 1138 15 Z Imposto creditado 1139 1153 15 Z Operações sem direito a crédito de Imposto Código 1154 1156 03 Z Será "311" Fiscal 1157 1171 15 Z Base de Cálculo 311 1172 1186 15 Z Imposto creditado 1187 1201 15 Z Operações sem direito a crédito de Imposto Código 1202 1204 03 Z Será "311" Fiscal 1205 1219 15 Z Base de Cálculo 311 1220 1234 15 Z Imposto creditado 1235 1249 15 Z Operações sem direito a crédito de Imposto Código 1250 1252 03 Z Será "312" Fiscal 1253 1267 15 Z Base de Cálculo 312 1268 1282 15 Z Imposto creditado 1283 1297 15 Z Operações sem direito a crédito de Imposto Código 1298 1300 03 Z Será "321" Fiscal 1301 1315 15 Z Base de Cálculo 321 1316 1330 15 Z Imposto creditado 1331 1345 15 Z Operações sem direito a crédito de Imposto Código 1298 1300 03 Z Será "321" Fiscal 1301 1315 15 Z Base de Cálculo 321 1316 1330 15 Z Imposto creditado 1331 1345 15 Z Operações sem direito a crédito de Imposto Código 1346 1348 03 Z Será "322" Fiscal 1349 1363 15 Z Base de Cálculo 322 1364 1378 15 Z Imposto creditado 1379 1393 15 Z Operações sem direito a crédito de Imposto Código 1394 1396 03 Z Será "394" Fiscal 1397 1411 15 Z Base de Cálculo 394 1412 1426 15 Z Imposto creditado 1427 1441 15 Z Operações sem direito a crédito de Imposto Código 1442 1444 03 Z Será "399" Fiscal 1445 1459 15 Z Base de Cálculo 399 1460 1474 15 Z Imposto creditado 1475 1489 15 Z Operações sem direito a crédito de Imposto FILLER 1490 1600 111 C B R A N C O S - ESTE REGISTRO SERÁ ÚNICO NO ARQUIVO E CORRESPONDE AO FORMULÁRIO I - PÁGINA 2 - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS. REGISTRO TIPO 3 DEMONSTRAÇÃO DAS SAÍDAS DE MERCADORIAS DO ESTABELECIMENTO - FORMULÁRIO I NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 Z Será "3". Código 02 04 03 Z Será "511" Fiscal 05 19 15 Z Base de Cálculo 511 20 34 15 Z Imposto Debitado 35 49 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 50 52 03 Z Será "512" Fiscal 53 67 15 Z Base de Cálculo 512 68 82 15 Z Imposto Debitado 83 97 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 98 100 03 Z Será "513" Fiscal 101 115 15 Z Base de Cálculo 513 116 130 15 Z Imposto Debitado 131 145 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 146 148 03 Z Será "521" Fiscal 149 163 15 Z Base de Cálculo 521 164 178 15 Z Imposto Debitado 179 193 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 194 196 03 Z Será "522" Fiscal 197 211 15 Z Base de Cálculo 522 212 226 15 Z Imposto Debitado 227 241 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 242 244 03 Z Será "531" Fiscal 245 259 15 Z Base de Cálculo 531 260 274 15 Z Imposto Debitado 275 289 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 290 292 03 Z Será "532" Fiscal 293 307 15 Z Base de Cálculo 532 308 322 15 Z Imposto Debitado 323 337 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 338 340 03 Z Será "593" Fiscal 341 355 15 Z Base de Cálculo 593 356 370 15 Z Imposto Debitado 371 385 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 386 388 03 Z Será "594" Fiscal 389 403 15 Z Base de Cálculo 594 404 418 15 Z Imposto Debitado 419 433 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 434 436 03 Z Será "599" Fiscal 437 451 15 Z Base de Cálculo 599 452 466 15 Z Imposto Debitado 467 481 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 482 484 03 Z Será "611" Fiscal 485 499 15 Z Base de Cálculo 611 500 514 15 Z Imposto Debitado 515 529 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 530 532 03 Z Será "612" Fiscal 533 547 15 Z Base de Cálculo 612 548 562 15 Z Imposto Debitado 563 577 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 578 580 03 Z Será "613" Fiscal 581 595 15 Z Base de Cálculo 613 596 610 15 Z Imposto Debitado 611 625 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 626 628 03 Z Será "621" Fiscal 629 643 15 Z Base de Cálculo 621 644 658 15 Z Imposto Debitado 659 673 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 674 676 03 Z Será "622" Fiscal 677 691 15 Z Base de Cálculo 622 692 706 15 Z Imposto Debitado 707 721 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 722 724 03 Z Será "631" Fiscal 725 739 15 Z Base de Cálculo 631 740 754 15 Z Imposto Debitado 755 769 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 770 772 03 Z Será "632" Fiscal 773 787 15 Z Base de Cálculo 632 788 802 15 Z Imposto Debitado 803 817 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 818 820 03 Z Será "693" Fiscal 821 835 15 Z Base de Cálculo 693 836 850 15 Z Imposto Debitado 851 865 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 866 868 03 Z Será "694" Fiscal 869 883 15 Z Base de Cálculo 694 884 898 15 Z Imposto Debitado 899 913 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 914 916 03 Z Será "699" Fiscal 917 931 15 Z Base de Cálculo 699 932 946 15 Z Imposto creditado 947 961 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 962 964 03 Z Será "611" Fiscal 965 979 15 Z Base de Cálculo 611 980 994 15 Z Imposto Debitado 995 1009 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1010 1012 03 Z Será "612" Fiscal 1013 1027 15 Z Base de Cálculo 612 1028 1042 15 Z Imposto Debitado 1043 1057 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1058 1060 03 Z Será "613" Fiscal 1061 1075 15 Z Base de Cálculo 613 1076 1090 15 Z Imposto Debitado 1091 1105 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1106 1108 03 Z Será "631" Fiscal 1109 1123 15 Z Base de Cálculo 631 1124 1138 15 Z Imposto Debitado 1139 1153 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1154 1156 03 Z Será "693" Fiscal 1157 1171 15 Z Base de Cálculo 693 1172 1186 15 Z Imposto creditado 1187 1201 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1202 1204 03 Z Será "694" Fiscal 1205 1219 15 Z Base de Cálculo 694 1220 1234 15 Z Imposto Debitado 1235 1249 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1250 1252 03 Z Será "699" Fiscal 1253 1267 15 Z Base de Cálculo 699 1268 1282 15 Z Imposto Debitado 1283 1297 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1298 1300 03 Z Será "711" Fiscal 1301 1315 15 Z Base de Cálculo 711 1316 1330 15 Z Imposto Debitado 1331 1345 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1346 1348 03 Z Será "712" Fiscal 1349 1363 15 Z Base de Cálculo 712 1364 1378 15 Z Imposto Debitado 1379 1393 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1394 1396 03 Z Será "731" Fiscal 1397 1411 15 Z Base de Cálculo 731 1412 1426 15 Z Imposto Debitado 1427 1441 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1442 1444 03 Z Será "732" Fiscal 1445 1459 15 Z Base de Cálculo 732 1460 1474 15 Z Imposto Debitado 1475 1489 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1490 1492 03 Z Será "799" Fiscal 1493 1507 15 Z Base de Cálculo 799 1508 1522 15 Z Imposto Debitado 1523 1537 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1538 1540 03 Z Será "799" Fiscal 1541 1555 15 Z Base de Cálculo 799 1556 1570 15 Z Imposto Debitado 1571 1585 15 Z Operações sem lançamento de débito e/ou com débito suspenso Filler 1586 1600 15 C B R A N C O S - ESTE REGISTRO SERÁ ÚNICO NO ARQUIVO E CORRESPONDE AO FORMULÁRIO I - PÁGINA 3 - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS. REGISTRO TIPO 4 DEMONSTRATIVO DE CRÉDITOS/DEMONSTRATIVO DE DÉBITOS/DADOS SOBRE PESSOAL OCUPADO/RESUMO DE ENTRADAS E SAÍDAS DE MERCADORIAS NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 Z Será "4" 02 16 15 Z Entradas de insumos do mercado nacional D E M 17 31 15 Z Entradas de insumos do O mercado externo N S 32 46 15 Z Outras entradas T R 47 61 15 Z Insumos utilizados na fa- A br de produtos exportados T I 62 76 15 Z Insumos utilizados no fabr. de produtos vendi- V dos a Empresa Comercial O Exportadora - DL 1248/72 D 77 91 15 Z Insumos utilizados no fa- E br máquinas e implementos agrícolas. C 92 106 15 Z Exportação de Prod. de R Fabr. Nac. nos termos do É DL. 1894/81 e LEI 7739/89 D I 107 121 15 Z Outros Créditos Incenti- vados T O 122 136 15 Z Outros Créditos S 137 151 15 Z Total de outros Créditos D D 152 166 15 Z Saídas para o Mercado Na- cional E E M 167 181 15 Z Estorno de Créditos Bási- cos O D N E 182 196 15 Z Inadimplemento do compro- S B misso de exportação s/re- T I gime "DRAW BACK" R T 197 211 15 Z Estorno de outros crédi- A O tos incentivados T S I 212 226 15 Z Ressarcimento de créditos V O 227 241 15 Z Outros Débitos D P O 242 256 15 Z Pessoal ocupado na produ- A E C ção (H/H) D S U 257 271 15 Z Pessoal ocupado fora da O S P produção (H/H) S O A A D 272 286 15 Z Consumo de energia elé- S L O trica no período - (TOTAL KWH) O B R E R D 287 301 15 Z Mercado Nacional - insumos E E com dito S U M 302 316 15 Z Mercado Nacional - insumos M E sem crédito O R C 317 331 15 Z Mercado Nacional - outras D A com crédito E D 332 346 15 Z Mercado Nacional - outras O sem crédito E R 347 361 15 Z Mercado Externo - insumos N I com crédito T A 362 376 15 Z Mercado Externo - insumos R S sem crédito A D A 392 406 15 Z Mercado Externo - outras S sem crédito R D 407 421 15 Z Mercado Nacional - Produção do Estabelecimento com dé- E E bito S U M 422 436 15 Z Mercado Nacional - Produção M E do Estabelecimento sem dé- O R bito C 437 451 15 Z Mercado Nacional - outras D A com Débito E D 452 466 15 Z Mercado Nacional - outras O sem Débito S R 467 481 15 Z Mercado Externo - Produção A I do Estabelecimento com débi I A to D S 482 496 15 Z Mercado Externo - Produção A do Estabelecimento sem débi to. 497 511 15 Z Mercado Externo - outras com débito 512 526 15 Z Mercado Externo - outras sem débito "FILLER" 527 1600 1073 Z B R A N C O S - ESTE REGISTRO É ÚNICO E CORRESPONDE A PÁGINA 4 DO FORMULÁRIO I - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS - SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO CONTER SINAL. REGISTRO TIPO 5 DEMONSTRATIVO DE ENTRADAS E SAÍDAS DE MERCADORIAS - ANEXO 1 NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 Z Será "5" Natureza da 02 04 03 Z Código de Natureza Operação da Operação 1ª OCORRÊNCIA 05 14 10 Z Código NBM/SH DO 15 27 13 Z Quantidade REGISTRO 28 40 13 Z Valor da Mercadoria 41 53 13 Z Imposto Lançado (débito/crédito) NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO 54 1523 1470 30 OCORRÊNCIAS NO MES- MO FORMATO DA 1º OCOR- RÊNCIA (PARA A MESMA NATUREZA DA OPERAÇÃO) "FILLER 1524 1600 77 C B R A N C O S - ESTE REGISTRO CORRESPONDE AO FORMULÁRIO ANEXO 2 (INSUMOS) - PODERÃO EXISTIR VÁRIOS REGISTROS TIPO "6" - AS OCORRÊNCIAS DO REGISTROS NÃO UTILIZADAS DEVERÃO SER PREENCHIDAS COM ZEROS - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS - OS CAMPOS DE QUANTIDADE DEVERÃO SER INFORMADOS SEM DECIMAIS, OU SEJA, OS DÍGITOS DECIMAIS DEVERÃO SER OMITIDOS - SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO CONTER SINAL REGISTRO TIPO 6 DEMONSTRATIVO DOS ESTOQUES DE INSUMOS - ANEXOS 2 NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 Z Será "6" 1ª 02 11 10 Z Código NBM\\SH OCORRÊNCIA 12 26 15 Z Quantidade Física no Início do Período do 27 41 15 Z Quantidade Física no Final do Período REGISTRO 42 56 15 Z Valor no Início do Pe- ríodo 57 71 15 Z Valor no final do Pe- ríodo 72 1541 1470 - 21 OCORRÊNCIAS NO MESMO FORMATO DA 1º OCORRÊNCIA "FILLER" 1542 1600 59 C B R A N C O S - ESTE REGISTRO CORRESPONDE AO FORMULÁRIO ANEXO 2 (INSUMOS) - PODERÃO EXISTIR VÁRIOS REGISTROS TIPO "6" - AS OCORRÊNCIAS DO REGISTRO NÃO UTILIZADAS DEVERÃO SER PREENCHIDAS COM ZEROS - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS - OS CAMPOS DE QUANTIDADE DEVERÃO SER INFORMADOS SEM DECIMAIS, OU SEJA, OS DÍGITOS DECIMAIS DEVERÃO SER OMITIDOS - SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO CONTER SINAL REGISTRO TIPO 7 DEMONSTRATIVO DOS ESTOQUES DE PRODUTOS ACABADOS - ANEXO 2 NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 Z Será "7" 1ª 02 11 10 Z Código NBM\\SH OCORRÊNCIA 12 26 15 Z Quantidade Física no Início do Período do 27 41 15 Z Quantidade Física no Final do Período REGISTRO 42 56 15 Z Valor no Início do Período 57 71 15 Z Valor no final do Pe- ríodo 72 1541 1470 - 21 OCORRÊNCIAS NO MESMO FORMATO DA 1º OCORRÊNCIA "FILLER" 1542 1600 59 C B R A N C O S - ESTE REGISTRO CORRESPONDE AO FORMULÁRIO ANEXO 2 (PRODUTOS ACABADOS) - PODERÃO EXISTIR VÁRIOS REGISTROS TIPO "7" - AS OCORRÊNCIAS DO REGISTRO NÃO UTILIZADAS DEVERÃO SER PREENCHIDAS COM ZEROS - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS - OS CAMPOS DE QUANTIDADE DEVERÃO SER INFORMADOS SEM DECIMAIS, OU SEJA, OS DÍGITOS DECIMAIS DEVERÃO SER OMITIDOS - SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO CONTER SINAL REGISTRO TIPO 8 DEMONSTRATIVO DOS ESTOQUES DE MERCADORIAS ADQUIRIDAS - ANEXO 2 TIPO 01 01 01 Z Será "8" 1ª 02 11 10 Z Código NBM\\SH OCORRÊNCIA 12 26 15 Z Quantidade Física no Início do Período do 27 41 15 Z Quantidade Física no Final do Período REGISTRO 42 56 15 Z Valor no Início do Pe- ríodo 57 71 15 Z Valor no final do Pe- ríodo 72 1541 1470 - 21 OCORRÊNCIAS NO MESMO FORMATO DA 1º OCORRÊNCIA "FILLER" 1542 1600 59 C B R A N C O S - ESTE REGISTRO CORRESPONDE AO FORMULÁRIOS ANEXO 2 (MERCADORIA ADQUIRIDAS - PODERÃO EXISTIR VÁRIOS REGISTROS TIPO "8" - AS OCORRÊNCIAS DOS REGISTO NÃO UTILIZADAS DEVERÃO SER PREENCHIDAS COM ZEROS - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS - OS CAMPOS DE QUANTIDADE DEVERÃO SER INFORMADOS SEM DECIMAIS, OU SEJA, OS DÍGITOS DECIMAIS DEVERÃO SER OMITIDOS - SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO CONTER SINAL. REGISTRO TIPO 9 REGISTRO TOTALIZADOR DO ARQUIVO NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 C Será "9" TOTAL DE 02 18 17 Z Total dos débitos do re- DÉBITO gistro do tipo 1 (soma- tório dos valores de dé- bito de janeiro a dezem- bro) TOTAL DE 19 35 17 Z Total dos créditos do CRÉDITOS registro do tipo 1 ( so- matório dos valores de débito de janeiro a de- zembro) TOTAL BASE DE CÁLCULO 36 52 17 Z Total da base de cálculo DAS do registro tipo 2 ( so- ENTRADAS matório dos valores de base de cálculo de todos os códigos fiscais das entradas) TOTAL 53 69 17 Z Total do imposto credi- IMPOSTO tado do registro tipo 2 CREDITADO (somatório dos valores de impostos creditados de todos os códigos fis- cais da entradas) TOTAL DE OPERAÇÕES 70 86 17 Z Total das operações sem S/DIREITO direito a crédito do im- A CRÉDITO posto do registro tipo 2 DO IMPOSTO (somatório dos valores das operações sem direi- to a crédito do imposto de todos os códigos fis- cais da entradas) TOTAL BASE DE 87 103 17 Z Total da base de cálculo CÁLCULOS do registro tipo 3 (so- DAS SAÍDAS matório dos valores da base cálculo de todos os códigos fiscais das saí- das) TOTAL IMPOSTO 104 120 17 Z Total do imposto debita- DEBITADO do do registro tipo 3 (somatório dos valores do imposto debitado de todos os códigos fiscais das saídas) TOTAL OPERAÇÕES Total das operações sem S/DIREITO direito de débito e/ou DE DÉBITO 121 137 17 Z com débito suspenso do E/OU COM registro tipo 3 (somató- DÉBITO rio dos valores das ope- SUSPENSO rações sem direito de débito e/ou com débito suspenso de todos códi- gos fiscais das saídas TOTAL Total dos valores de DEMONSTRA créditos Registro tipo 4 TIVOS DE 138 154 17 Z CRÉDITOS TOTAL DEMONSTRA TIVOS DE Total dos valores de dé- DÉBITOS 155 171 17 Z bitos do retro tipo 4 TOTAL RESUMO Total do resumo dos va- DAS 172 188 17 Z lores das entradas de ENTRADAS mercadorias com crédito DE MERC do registro tipo 4 (mer- ADORIAS cado nacional + externo) COM CRÉ DITO TOTAL RESUMO Total do resumo de valo- DAS ENTRA res das entradas de mer- DAS DE cadorias sem crédito do MERCA 189 205 17 Z registro tipo 4 (mercado DORIAS nacional + externo) SEM CRÉ DITO TOTAL RESUMO Total do resumo dos va- DAS SAÍ lores das saídas de mer- DAS DE 206 222 17 Z cadorias com débito do MERCA- registro 4 mercado na- DORIAS cional + mercado externo COM DÉ BITO TOTAL RESUMO Total do resumo dos va- DAS lores das saídas de mer- SAÍDAS cadorias sem débito do DE MERCA 223 239 17 Z registro tipo 4 (mercado DORIAS nacional + externo) SEM DÉBITO TOTAL 240 256 17 Z Total valor das mercado- NOP rias 50.7 257 273 17 Z Total imposto lançado TOTAL 274 290 17 Z Total valor das mercado- NOP rias 51.5 291 307 17 Z Total imposto lançado TOTAL 308 324 17 Z Total valor das mercado- NOP rias 52.3 325 341 17 Z Total imposto lançado TOTAL 342 358 17 Z Total valor das mercado NOP rias 53.1 359 375 17 Z Total imposto lançado TOTAL 376 392 17 Z Total valor das mercado- NOP rias 54.0 393 409 17 Z Total imposto lançado TOTAL 410 426 17 Z Total valor das mercado- NOP rias 55.8 427 443 17 Z Total imposto lançado TOTAL 444 460 17 Z Total valor das mercado- NOP rias 56.6 461 477 17 Z Total imposto lançado TOTAL 478 494 17 Z Total valor das mercado- NOP rias 57.4 495 511 17 Z Total imposto lançado TOTAL 512 528 17 Z Total valor das mercado- NOP rias 60.4 529 545 17 Z Total imposto lançado TOTAL 546 562 17 Z Total valor das mercado- NOP rias 61.2 563 579 17 Z Total imposto lançado TOTAL 580 596 17 Z Total valor das mercado- NOP rias 62.0 597 613 17 Z Total imposto lançado TOTAL 614 630 17 Z Total valor das mercado- NOP rias 63.9 631 647 17 Z Total imposto lançado TOTAL 648 664 17 Z Total valor das mercado- NOP rias 64.7 665 681 17 Z Total imposto lançado TOTAL 682 698 17 Z Total valor das mercado- NOP rias 70.1 699 715 17 Z Total imposto lançado TOTAL 716 732 17 Z Total valor das mercado- NOP rias 71.0 733 749 17 Z Total imposto lançado TOTAL 750 766 17 Z Total valor das mercado- NOP rias 72.8 767 783 17 Z Total imposto lançado TOTAL 784 800 17 Z Total valor das mercado- NOP rias 73.6 801 817 17 Z Total imposto lançado TOTAL 818 834 17 Z Total valor das mercado- NOP rias 77.2 835 851 17 Z Total imposto lançado TOTAL 852 868 17 Z Total valor das mercado- NOP rias 78.7 869 885 17 Z Total imposto lançado TOTAL 886 902 17 Z Total valor das mercado- NOP rias 80.9 903 919 17 Z Total imposto lançado TOTAL 920 936 17 Z Total valor das mercado- NOP rias 81.7 937 953 17 Z Total imposto lançado TOTAL 954 970 17 Z Total valor das mercado- NOP rias 84.1 971 987 17 Z Total imposto lançado TOTAL 988 1004 17 Z Total valor das mercado- NOP rias 85.0 1005 1021 17 Z Total imposto lançado TOTAL 1022 1038 17 Z Total valor das mercado- NOP rias 86.8 1039 1055 17 Z Total imposto lançado TOTAL 1056 1072 17 Z Total valor das mercado- NOP rias 90.6 1073 1089 17 Z Total imposto lançado TOTAL 1090 1106 17 Z Total valor das mercado- NOP rias 91.4 1107 1123 17 Z Total imposto lançado TOTAL 1124 1140 17 Z Total valor das mercado- NOP rias 92.2 1141 1157 17 Z Total imposto lançado 1158 1174 17 Z Total dos valores do iní- cio do período dos regis- TOTAL tros tipo 6 (somatório VALOR DE dos valores do início do INSUMOS período de insumos) Total dos valores do fi- nal do período dos regis- 1175 1191 17 Z tros tipo 6 (somatório dos valores do final do período de insumos). Total dos valores do iní- cio do período dos regis- TOTAL 1192 1208 17 Z tros tipo 7 (somatório dos valores do início do VALOR períodos de produtos aca- DE PRO bados) DUTOS Total dos valores do fi- ACABA nal do período dos regis- DOS 1209 1225 17 Z tros tipo 7 (somatório dos valores do final do período de produtos aca- bados) Total dos valores do iní- cio do período dos regis- TOTAL 1226 1242 17 Z tros tipo 8 (somatório VALOR dos valores do início do DE MER períodos de mercadorias CADORIAS adquirida ADQUIRI DAS Total dos valores do fi- nal do período dos regis- 1243 1259 17 Z tros tipo 8 (somatório dos valores do final de mercadorias adquiridas) TOTAL DE REGISTRO 1260 1264 05 Z Total dos registros tipo TIPO 5 5 gravados no arquivo. TOTAL DE REGISTRO 1265 1269 05 Z Total dos registros tipo TIPO 6 6 gravados no arquivo. TOTAL DE REGISTRO 1270 1274 05 Z Total dos registros tipo TIPO 7 7 gravados no arquivo. TOTAL DE REGISTRO 1275 1279 05 Z Total dos registros tipo TIPO 8 8 gravados no arquivo. QUANT IDADE TO 1280 1284 05 Z Quantidade total de todos TAL DE os tipos de registros gra- REGISTROS vados no arquivo (tipo 0 + tipo 1 + tipo 2 + tipo 3 + tipo 4 + tipo 5 + tipo 6 + tipo 7 + tipo 8 + tipo 9 ) "FILLER" 1285 1600 316 C B R A N C O S - ESTE REGISTRO É ÚNICO E DEVERÁ SER O ÚLTIMO REGISTRO DO ARQUIVO - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS - SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO CONTER SINAL. DESCRIÇÃO DOS REGISTROS REGISTRO TIPO 0 REGISTRO MESTRE DO ARQUIVO NOME DO POSIÇÃO CAMPO INIC. FIM TAMAN. FORMATO CONTEÚDO TIPO 01 01 01 Z Será "0". Será o primeiro registro do arquivo. Posição 2 a 9 - Num Básico Posição 10 a 13- Num. Ordem C.G.C 02 15 14 Z Posição 14 a 15 - DV Deverá estar sempre comple- to com 14 dígitos Exercício de Apuração 16 17 02 Z Será o ano do exercício de apuração Será "0" para Situação Nor- mal Será "1" para Retificação de Declaração Situação 18 18 01 C Será "2" para Encerramento Especial de Atividades Será "3"para Retificação de Declaração e Encerramento de Atividades Optante Convênio 19 19 01 Z Será "1" para optante pelo ICMS Convênio ICMS Será "2" para não optante pelo Convênio ICMS Registro Especial de 20 37 Engarrafadores 20 31 12 Z Número da Ordem 32 37 6 Z Data da Emissão Razão Social 38 92 55 C Razão Social/Denominação Comercial do Estab. Endereço 93 222 93 96 04 C Tipo de Logradouro 97 119 23 C Logradouro 120 125 06 C Número 126 144 19 C Complemento 145 163 19 C Bairro 164 168 05 C CEP 169 198 30 C Município 199 200 02 C U.F 201 211 11 C Telex 212 222 11 C Telefone Tipo de Estabele 223 224 02 Z Será um dos códigos do tipo cimento constante do Manual de pre- enchimento do IPI Atividade Econômica 225 228 04 Z Código da Atividade Econô- mica Principal "Filler" 229 1600 1372 C B R A N C O S REGISTRO TIPO 1 DEMONSTRATIVO DE APURAÇÃO QUINZENAL DO SALDO DO IPI - FORMULÁRIO I NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 Z Será "1" 1ª 02 03 02 Z Será "01" Q U 04 04 01 Será "1" I 05 19 15 Z Débito J N 20 34 15 Z Crédito A Z. 35 49 15 Z Saldo credor no período N anterior E 50 64 15 Z Saldo apurado I R 2ª 65 65 01 Z Será "2" O Q 66 80 15 Z Débito U 81 95 15 Z Crédito I 96 110 15 Z Saldo credor no período N anterior Z. 111 125 15 Z Saldo apurado 1ª 126 127 02 Z Será "02" Q U 128 128 01 Z Será "1" I 129 143 15 Z Débito F N 144 158 15 Z Crédito E Z. 159 173 15 Z Saldo credor no período V anterior E 174 188 15 Z Saldo apurado R E 2ª 189 189 01 Z Será "2" I Q 190 204 15 Z Débito R U 205 219 15 Z Crédito O I 220 234 15 Z Saldo credor no período N anterior Z. 235 249 15 Z Saldo apurado 1ª 250 251 02 Z Será "03" Q U 252 252 01 Z Será "1" I 253 267 15 Z Débito M N 268 282 15 Z Crédito A Z. 283 297 15 Z Saldo credor no período R anterior Ç 298 312 15 Z Saldo apurado O 2ª 313 313 01 Z Será "2" Q 314 328 15 Z Débito U 329 343 15 Z Crédito I 344 358 15 Z Saldo credor no período N anterior Z. 359 373 15 Z Saldo apurado 1ª 374 375 02 Z Será "04" Q U 376 376 01 Z Será "1" I 377 391 15 Z Débito A N 392 406 15 Z Crédito B Z. 407 421 15 Z Saldo credor no período R anterior I 422 436 15 Z Saldo apurado L 2ª 437 437 01 Z Será "2" Q 438 452 15 Z Débito U 453 467 15 Z Crédito I 468 482 15 Z Saldo credor no período N anterior Z. 483 497 15 Z Saldo apurado 1ª 498 499 02 Z Será "05" Q U 500 500 01 Z Será "1" I 501 515 15 Z Débito M N 516 530 15 Z Crédito A Z. 531 545 15 Z Saldo credor no período I anterior O 546 560 15 Z Saldo apurado 2ª 561 561 01 Z Será "2" Q 562 576 15 Z Débito U 577 591 15 Z Crédito I 592 606 15 Z Saldo credor no período N anterior Z. 607 621 15 Z Saldo apurado 1ª 622 623 02 Z Será "06" Q U 624 624 01 Z Será "1" I 625 639 15 Z Débito J N 640 654 15 Z Crédito U Z. 655 669 15 Z Saldo credor no período N anterior H 670 684 15 Z Saldo apurado O 2ª 685 685 01 Z Será "2" Q 686 700 15 Z Débito U 701 715 15 Z Crédito I 716 730 15 Z Saldo credor no período N anterior Z. 731 745 15 Z Saldo apurado 1ª 746 747 02 Z Será "07" Q U 748 748 01 Z Será "1" I 749 763 15 Z Débito J N 764 778 15 Z Crédito U Z. 779 793 15 Z Saldo credor no período L anterior H 794 808 15 Z Saldo apurado O 2ª 809 809 01 Z Será "2" Q 810 824 15 Z Débito U 825 839 15 Z Crédito I 840 854 15 Z Saldo credor no período N anterior Z. 855 869 15 Z Saldo apurado 1ª 870 871 02 Z Será "08" Q U 872 872 01 Z Será "1" I 873 887 15 Z Débito A N 888 902 15 Z Crédito G Z. 903 917 15 Z Saldo credor no período O anterior S 918 932 15 Z Saldo apurado T O 2ª 933 933 01 Z Será "2" Q 934 948 15 Z Débito U 949 963 15 Z Crédito I 964 978 15 Z Saldo credor no período N anterior Z. 979 993 15 Z Saldo apurado 1ª 994 995 02 Z Será "09" Q U 996 996 01 Z Será "1" I 997 1011 15 Z Débito S N 1012 1026 15 Z Crédito E Z. 1027 1041 15 Z Saldo credor no período T anterior E 1042 1056 15 Z Saldo apurado M B 2ª 1057 1057 01 Z Será "2" R Q 1058 1072 15 Z Débito O U 1073 1087 15 Z Crédito I 1088 1102 15 Z Saldo credor no período N anterior Z. 1103 1117 15 Z Saldo apurado 1ª 1118 1119 02 Z Será "10" Q U 1120 1120 01 Z Será "1" I 1121 1135 15 Z Débito O N 1136 1150 15 Z Crédito U Z. 1151 1165 15 Z Saldo credor no período T anterior U 1166 1180 15 Z Saldo apurado B R 2ª 1181 1181 01 Z Será "2" O Q 1182 1196 15 Z Débito U 1197 1211 15 Z Crédito I 1212 1226 15 Z Saldo credor no período N anterior Z. 1227 1241 15 Z Saldo apurado 1ª 1242 1243 02 Z Será "11" Q U 1244 1244 01 Z Será "1" I 1245 1259 15 Z Débito N N 1260 1274 15 Z Crédito O Z. 1275 1289 15 Z Saldo credor no período V anterior E 1290 1304 15 Z Saldo apurado M B 2ª 1305 1305 01 Z Será "2" R Q 1306 1320 15 Z Débito O U 1321 1335 15 Z Crédito I 1336 1350 15 Z Saldo credor no período N anterior Z. 1351 1365 15 Z Saldo apurado 1ª 1366 1367 02 Z Será "12" Q U 1368 1368 01 Z Será "1" I 1369 1383 15 Z Débito D N 1384 1398 15 Z Crédito E Z. 1399 1413 15 Z Saldo credor no período Z anterior E 1414 1428 15 Z Saldo apurado M B 2ª 1429 1429 01 Z Será "2" R Q 1430 1444 15 Z Débito O U 1445 1459 15 Z Crédito I 1460 1474 15 Z Saldo credor no período N anterior Z. 1475 1489 15 Z Saldo apurado FILLER 1490 1600 111 C B R A N C O S - ESTE REGISTRO É ÚNICO E CORRESPONDE A PÁG.. 1 DO FORMULÁRIO I - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS. REGISTRO TIPO 2 DEMONSTRAÇÃO DAS ENTRADAS DE MERCADORIAS NO ESTABELECIMENTO - FORMULÁRIO I NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 Z Será "2". Código 02 04 03 Z Será "111" Fiscal 05 19 15 Z Base de Cálculo 111 20 34 15 Z Imposto creditado 35 49 15 Z Operações sem direito a crédito de Imposto Código 50 52 03 Z Será "111" Fiscal 53 67 15 Z Base de Cálculo 111 68 82 15 Z Imposto creditado 83 97 15 Z Operações sem direito a crédito de Imposto Código 98 100 03 Z Será "112" Fiscal 101 115 15 Z Base de Cálculo 112 116 130 15 Z Imposto creditado 131 145 15 Z Operações sem direito a crédito de Imposto Código 146 148 03 Z Será "113" Fiscal 149 163 15 Z Base de Cálculo 113 164 178 15 Z Imposto creditado 179 193 15 Z Operações sem direito a crédito de Imposto Código 194 196 03 Z Será "121" Fiscal 197 211 15 Z Base de Cálculo 121 212 226 15 Z Imposto creditado 227 241 15 Z Operações sem direito a crédito de Imposto Código 242 244 03 Z Será "121" Fiscal 245 259 15 Z Base de Cálculo 121 260 274 15 Z Imposto creditado 275 289 15 Z Operações sem direito a crédito de Imposto Código 290 292 03 Z Será "122" Fiscal 293 307 15 Z Base de Cálculo 122 308 322 15 Z Imposto creditado 323 337 15 Z Operações sem direito a crédito de Imposto Código 338 340 03 Z Será "131" Fiscal 341 355 15 Z Base de Cálculo 131 356 370 15 Z Imposto creditado 371 385 15 Z Operações sem direito a crédito de Imposto Código 386 388 03 Z Será "132" Fiscal 389 403 15 Z Base de Cálculo 132 404 418 15 Z Imposto creditado 419 433 15 Z Operações sem direito a crédito de Imposto Código 434 436 03 Z Será "193" Fiscal 437 451 15 Z Base de Cálculo 193 452 466 15 Z Imposto creditado 467 481 15 Z Operações sem direito a crédito de Imposto Código 482 484 03 Z Será "194" Fiscal 485 499 15 Z Base de Cálculo 194 500 514 15 Z Imposto creditado 515 529 15 Z Operações sem direito a crédito de Imposto Código 530 532 03 Z Será "199" Fiscal 533 547 15 Z Base de Cálculo 199 548 562 15 Z Imposto creditado 563 577 15 Z Operações sem direito a crédito de Imposto Código 578 580 03 Z Será "211" Fiscal 581 595 15 Z Base de Cálculo 211 596 610 15 Z Imposto creditado 611 625 15 Z Operações sem direito a crédito de Imposto Código 626 628 03 Z Será "211" Fiscal 629 643 15 Z Base de Cálculo 211 644 658 15 Z Imposto creditado 659 673 15 Z Operações sem direito a crédito de Imposto Código 674 676 03 Z Será "212" Fiscal 677 691 15 Z Base de Cálculo 212 692 706 15 Z Imposto creditado 707 721 15 Z Operações sem direito a crédito de Imposto Código 722 724 03 Z Será "213" Fiscal 725 739 15 Z Base de Cálculo 213 740 754 15 Z Imposto creditado 755 769 15 Z Operações sem direito a crédito de Imposto Código 770 772 03 Z Será "221" Fiscal 773 787 15 Z Base de Cálculo 221 788 802 15 Z Imposto creditado 803 817 15 Z Operações sem direito a crédito de Imposto Código 818 820 03 Z Será "221" Fiscal 821 835 15 Z Base de Cálculo 221 836 850 15 Z Imposto creditado 851 865 15 Z Operações sem direito a crédito de Imposto Código 866 868 03 Z Será "222" Fiscal 869 883 15 Z Base de Cálculo 222 884 898 15 Z Imposto creditado 899 913 15 Z Operações sem direito a crédito de Imposto Código 914 916 03 Z Será "231" Fiscal 917 931 15 Z Base de Cálculo 231 932 946 15 Z Imposto creditado 947 961 15 Z Operações sem direito a crédito de Imposto Código 962 964 03 Z Será "232" Fiscal 965 979 15 Z Base de Cálculo 232 980 994 15 Z Imposto creditado 995 1009 15 Z Operações sem direito a crédito de Imposto Código 1010 1012 03 Z Será "293" Fiscal 1013 1027 15 Z Base de Cálculo 293 1028 1042 15 Z Imposto creditado 1043 1057 15 Z Operações sem direito a crédito de Imposto Código 1058 1060 03 Z Será "294" Fiscal 1061 1075 15 Z Base de Cálculo 294 1076 1090 15 Z Imposto creditado 1091 1105 15 Z Operações sem direito a crédito de Imposto Código 1106 1108 03 Z Será "299" Fiscal 1109 1123 15 Z Base de Cálculo 299 1124 1138 15 Z Imposto creditado 1139 1153 15 Z Operações sem direito a crédito de Imposto Código 1154 1156 03 Z Será "311" Fiscal 1157 1171 15 Z Base de Cálculo 311 1172 1186 15 Z Imposto creditado 1187 1201 15 Z Operações sem direito a crédito de Imposto Código 1202 1204 03 Z Será "311" Fiscal 1205 1219 15 Z Base de Cálculo 311 1220 1234 15 Z Imposto creditado 1235 1249 15 Z Operações sem direito a crédito de Imposto Código 1250 1252 03 Z Será "312" Fiscal 1253 1267 15 Z Base de Cálculo 312 1268 1282 15 Z Imposto creditado 1283 1297 15 Z Operações sem direito a crédito de Imposto Código 1298 1300 03 Z Será "321" Fiscal 1301 1315 15 Z Base de Cálculo 321 1316 1330 15 Z Imposto creditado 1331 1345 15 Z Operações sem direito a crédito de Imposto Código 1298 1300 03 Z Será "321" Fiscal 1301 1315 15 Z Base de Cálculo 321 1316 1330 15 Z Imposto creditado 1331 1345 15 Z Operações sem direito a crédito de Imposto Código 1346 1348 03 Z Será "322" Fiscal 1349 1363 15 Z Base de Cálculo 322 1364 1378 15 Z Imposto creditado 1379 1393 15 Z Operações sem direito a crédito de Imposto Código 1394 1396 03 Z Será "394" Fiscal 1397 1411 15 Z Base de Cálculo 394 1412 1426 15 Z Imposto creditado 1427 1441 15 Z Operações sem direito a crédito de Imposto Código 1442 1444 03 Z Será "399" Fiscal 1445 1459 15 Z Base de Cálculo 399 1460 1474 15 Z Imposto creditado 1475 1489 15 Z Operações sem direito a crédito de Imposto FILLER 1490 1600 111 C B R A N C O S - ESTE REGISTRO SERÁ ÚNICO NO ARQUIVO E CORRESPONDE AO FORMULÁRIO I - PÁGINA 2 - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS. REGISTRO TIPO 3 DEMONSTRAÇÃO DAS SAÍDAS DE MERCADORIAS DO ESTABELECIMENTO - FORMULÁRIO I NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 Z Será "3". Código 02 04 03 Z Será "511" Fiscal 05 19 15 Z Base de Cálculo 511 20 34 15 Z Imposto Debitado 35 49 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 50 52 03 Z Será "512" Fiscal 53 67 15 Z Base de Cálculo 512 68 82 15 Z Imposto Debitado 83 97 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 98 100 03 Z Será "513" Fiscal 101 115 15 Z Base de Cálculo 513 116 130 15 Z Imposto Debitado 131 145 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 146 148 03 Z Será "521" Fiscal 149 163 15 Z Base de Cálculo 521 164 178 15 Z Imposto Debitado 179 193 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 194 196 03 Z Será "522" Fiscal 197 211 15 Z Base de Cálculo 522 212 226 15 Z Imposto Debitado 227 241 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 242 244 03 Z Será "531" Fiscal 245 259 15 Z Base de Cálculo 531 260 274 15 Z Imposto Debitado 275 289 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 290 292 03 Z Será "532" Fiscal 293 307 15 Z Base de Cálculo 532 308 322 15 Z Imposto Debitado 323 337 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 338 340 03 Z Será "593" Fiscal 341 355 15 Z Base de Cálculo 593 356 370 15 Z Imposto Debitado 371 385 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 386 388 03 Z Será "594" Fiscal 389 403 15 Z Base de Cálculo 594 404 418 15 Z Imposto Debitado 419 433 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 434 436 03 Z Será "599" Fiscal 437 451 15 Z Base de Cálculo 599 452 466 15 Z Imposto Debitado 467 481 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 482 484 03 Z Será "611" Fiscal 485 499 15 Z Base de Cálculo 611 500 514 15 Z Imposto Debitado 515 529 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 530 532 03 Z Será "612" Fiscal 533 547 15 Z Base de Cálculo 612 548 562 15 Z Imposto Debitado 563 577 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 578 580 03 Z Será "613" Fiscal 581 595 15 Z Base de Cálculo 613 596 610 15 Z Imposto Debitado 611 625 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 626 628 03 Z Será "621" Fiscal 629 643 15 Z Base de Cálculo 621 644 658 15 Z Imposto Debitado 659 673 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 674 676 03 Z Será "622" Fiscal 677 691 15 Z Base de Cálculo 622 692 706 15 Z Imposto Debitado 707 721 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 722 724 03 Z Será "631" Fiscal 725 739 15 Z Base de Cálculo 631 740 754 15 Z Imposto Debitado 755 769 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 770 772 03 Z Será "632" Fiscal 773 787 15 Z Base de Cálculo 632 788 802 15 Z Imposto Debitado 803 817 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 818 820 03 Z Será "693" Fiscal 821 835 15 Z Base de Cálculo 693 836 850 15 Z Imposto Debitado 851 865 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 866 868 03 Z Será "694" Fiscal 869 883 15 Z Base de Cálculo 694 884 898 15 Z Imposto Debitado 899 913 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 914 916 03 Z Será "699" Fiscal 917 931 15 Z Base de Cálculo 699 932 946 15 Z Imposto creditado 947 961 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 962 964 03 Z Será "611" Fiscal 965 979 15 Z Base de Cálculo 611 980 994 15 Z Imposto Debitado 995 1009 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1010 1012 03 Z Será "612" Fiscal 1013 1027 15 Z Base de Cálculo 612 1028 1042 15 Z Imposto Debitado 1043 1057 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1058 1060 03 Z Será "613" Fiscal 1061 1075 15 Z Base de Cálculo 613 1076 1090 15 Z Imposto Debitado 1091 1105 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1106 1108 03 Z Será "631" Fiscal 1109 1123 15 Z Base de Cálculo 631 1124 1138 15 Z Imposto Debitado 1139 1153 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1154 1156 03 Z Será "693" Fiscal 1157 1171 15 Z Base de Cálculo 693 1172 1186 15 Z Imposto creditado 1187 1201 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1202 1204 03 Z Será "694" Fiscal 1205 1219 15 Z Base de Cálculo 694 1220 1234 15 Z Imposto Debitado 1235 1249 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1250 1252 03 Z Será "699" Fiscal 1253 1267 15 Z Base de Cálculo 699 1268 1282 15 Z Imposto Debitado 1283 1297 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1298 1300 03 Z Será "711" Fiscal 1301 1315 15 Z Base de Cálculo 711 1316 1330 15 Z Imposto Debitado 1331 1345 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1346 1348 03 Z Será "712" Fiscal 1349 1363 15 Z Base de Cálculo 712 1364 1378 15 Z Imposto Debitado 1379 1393 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1394 1396 03 Z Será "731" Fiscal 1397 1411 15 Z Base de Cálculo 731 1412 1426 15 Z Imposto Debitado 1427 1441 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1442 1444 03 Z Será "732" Fiscal 1445 1459 15 Z Base de Cálculo 732 1460 1474 15 Z Imposto Debitado 1475 1489 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1490 1492 03 Z Será "799" Fiscal 1493 1507 15 Z Base de Cálculo 799 1508 1522 15 Z Imposto Debitado 1523 1537 15 Z Operações sem lançamento de débito e/ou com débito suspenso Código 1538 1540 03 Z Será "799" Fiscal 1541 1555 15 Z Base de Cálculo 799 1556 1570 15 Z Imposto Debitado 1571 1585 15 Z Operações sem lançamento de débito e/ou com débito suspenso Filler 1586 1600 15 C B R A N C O S - ESTE REGISTRO SERÁ ÚNICO NO ARQUIVO E CORRESPONDE AO FORMULÁRIO I - PÁGINA 3 - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS. REGISTRO TIPO 4 DEMONSTRATIVO DE CRÉDITOS/DEMONSTRATIVO DE DÉBITOS/DADOS SOBRE PESSOAL OCUPADO/RESUMO DE ENTRADAS E SAÍDAS DE MERCADORIAS NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 Z Será "4" 02 16 15 Z Entradas de insumos do mercado nacional D E M 17 31 15 Z Entradas de insumos do O mercado externo N S 32 46 15 Z Outras entradas T R 47 61 15 Z Insumos utilizados na fa- A br de produtos exportados T I 62 76 15 Z Insumos utilizados no fabr. de produtos vendi- V dos a Empresa Comercial O Exportadora - DL 1248/72 D 77 91 15 Z Insumos utilizados no fa- E br máquinas e implementos agrícolas. C 92 106 15 Z Exportação de Prod. de R Fabr. Nac. nos termos do É DL. 1894/81 e LEI 7739/89 D I 107 121 15 Z Outros Créditos Incenti- vados T O 122 136 15 Z Outros Créditos S 137 151 15 Z Total de outros Créditos D D 152 166 15 Z Saídas para o Mercado Na- cional E E M 167 181 15 Z Estorno de Créditos Bási- cos O D N E 182 196 15 Z Inadimplemento do compro- S B misso de exportação s/re- T I gime "DRAW BACK" R T 197 211 15 Z Estorno de outros crédi- A O tos incentivados T S I 212 226 15 Z Ressarcimento de créditos V O 227 241 15 Z Outros Débitos D P O 242 256 15 Z Pessoal ocupado na produ- A E C ção (H/H) D S U 257 271 15 Z Pessoal ocupado fora da O S P produção (H/H) S O A A D 272 286 15 Z Consumo de energia elé- S L O trica no período - (TOTAL KWH) O B R E R D 287 301 15 Z Mercado Nacional - insumos E E com dito S U M 302 316 15 Z Mercado Nacional - insumos M E sem crédito O R C 317 331 15 Z Mercado Nacional - outras D A com crédito E D 332 346 15 Z Mercado Nacional - outras O sem crédito E R 347 361 15 Z Mercado Externo - insumos N I com crédito T A 362 376 15 Z Mercado Externo - insumos R S sem crédito A D A 392 406 15 Z Mercado Externo - outras S sem crédito R D 407 421 15 Z Mercado Nacional - Produção do Estabelecimento com dé- E E bito S U M 422 436 15 Z Mercado Nacional - Produção M E do Estabelecimento sem dé- O R bito C 437 451 15 Z Mercado Nacional - outras D A com Débito E D 452 466 15 Z Mercado Nacional - outras O sem Débito S R 467 481 15 Z Mercado Externo - Produção A I do Estabelecimento com débi I A to D S 482 496 15 Z Mercado Externo - Produção A do Estabelecimento sem débi to. 497 511 15 Z Mercado Externo - outras com débito 512 526 15 Z Mercado Externo - outras sem débito "FILLER" 527 1600 1073 Z B R A N C O S - ESTE REGISTRO É ÚNICO E CORRESPONDE A PÁGINA 4 DO FORMULÁRIO I - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS - SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO CONTER SINAL. REGISTRO TIPO 5 DEMONSTRATIVO DE ENTRADAS E SAÍDAS DE MERCADORIAS - ANEXO 1 NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 Z Será "5" Natureza da 02 04 03 Z Código de Natureza Operação da Operação 1ª OCORRÊNCIA 05 14 10 Z Código NBM/SH DO 15 27 13 Z Quantidade REGISTRO 28 40 13 Z Valor da Mercadoria 41 53 13 Z Imposto Lançado (débito/crédito) NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO 54 1523 1470 30 OCORRÊNCIAS NO MES- MO FORMATO DA 1º OCOR- RÊNCIA (PARA A MESMA NATUREZA DA OPERAÇÃO) "FILLER 1524 1600 77 C B R A N C O S - ESTE REGISTRO CORRESPONDE AO FORMULÁRIO ANEXO 2 (INSUMOS) - PODERÃO EXISTIR VÁRIOS REGISTROS TIPO "6" - AS OCORRÊNCIAS DO REGISTROS NÃO UTILIZADAS DEVERÃO SER PREENCHIDAS COM ZEROS - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS - OS CAMPOS DE QUANTIDADE DEVERÃO SER INFORMADOS SEM DECIMAIS, OU SEJA, OS DÍGITOS DECIMAIS DEVERÃO SER OMITIDOS - SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO CONTER SINAL REGISTRO TIPO 6 DEMONSTRATIVO DOS ESTOQUES DE INSUMOS - ANEXOS 2 NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 Z Será "6" 1ª 02 11 10 Z Código NBM\\SH OCORRÊNCIA 12 26 15 Z Quantidade Física no Início do Período do 27 41 15 Z Quantidade Física no Final do Período REGISTRO 42 56 15 Z Valor no Início do Pe- ríodo 57 71 15 Z Valor no final do Pe- ríodo 72 1541 1470 - 21 OCORRÊNCIAS NO MESMO FORMATO DA 1º OCORRÊNCIA "FILLER" 1542 1600 59 C B R A N C O S - ESTE REGISTRO CORRESPONDE AO FORMULÁRIO ANEXO 2 (INSUMOS) - PODERÃO EXISTIR VÁRIOS REGISTROS TIPO "6" - AS OCORRÊNCIAS DO REGISTRO NÃO UTILIZADAS DEVERÃO SER PREENCHIDAS COM ZEROS - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS - OS CAMPOS DE QUANTIDADE DEVERÃO SER INFORMADOS SEM DECIMAIS, OU SEJA, OS DÍGITOS DECIMAIS DEVERÃO SER OMITIDOS - SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO CONTER SINAL REGISTRO TIPO 7 DEMONSTRATIVO DOS ESTOQUES DE PRODUTOS ACABADOS - ANEXO 2 NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 Z Será "7" 1ª 02 11 10 Z Código NBM\\SH OCORRÊNCIA 12 26 15 Z Quantidade Física no Início do Período do 27 41 15 Z Quantidade Física no Final do Período REGISTRO 42 56 15 Z Valor no Início do Período 57 71 15 Z Valor no final do Pe- ríodo 72 1541 1470 - 21 OCORRÊNCIAS NO MESMO FORMATO DA 1º OCORRÊNCIA "FILLER" 1542 1600 59 C B R A N C O S - ESTE REGISTRO CORRESPONDE AO FORMULÁRIO ANEXO 2 (PRODUTOS ACABADOS) - PODERÃO EXISTIR VÁRIOS REGISTROS TIPO "7" - AS OCORRÊNCIAS DO REGISTRO NÃO UTILIZADAS DEVERÃO SER PREENCHIDAS COM ZEROS - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS - OS CAMPOS DE QUANTIDADE DEVERÃO SER INFORMADOS SEM DECIMAIS, OU SEJA, OS DÍGITOS DECIMAIS DEVERÃO SER OMITIDOS - SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO CONTER SINAL REGISTRO TIPO 8 DEMONSTRATIVO DOS ESTOQUES DE MERCADORIAS ADQUIRIDAS - ANEXO 2 TIPO 01 01 01 Z Será "8" 1ª 02 11 10 Z Código NBM\\SH OCORRÊNCIA 12 26 15 Z Quantidade Física no Início do Período do 27 41 15 Z Quantidade Física no Final do Período REGISTRO 42 56 15 Z Valor no Início do Pe- ríodo 57 71 15 Z Valor no final do Pe- ríodo 72 1541 1470 - 21 OCORRÊNCIAS NO MESMO FORMATO DA 1º OCORRÊNCIA "FILLER" 1542 1600 59 C B R A N C O S - ESTE REGISTRO CORRESPONDE AO FORMULÁRIOS ANEXO 2 (MERCADORIA ADQUIRIDAS - PODERÃO EXISTIR VÁRIOS REGISTROS TIPO "8" - AS OCORRÊNCIAS DOS REGISTO NÃO UTILIZADAS DEVERÃO SER PREENCHIDAS COM ZEROS - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS - OS CAMPOS DE QUANTIDADE DEVERÃO SER INFORMADOS SEM DECIMAIS, OU SEJA, OS DÍGITOS DECIMAIS DEVERÃO SER OMITIDOS - SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO CONTER SINAL. REGISTRO TIPO 9 REGISTRO TOTALIZADOR DO ARQUIVO NOME DO POSIÇÃO CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO TIPO 01 01 01 C Será "9" TOTAL DE 02 18 17 Z Total dos débitos do re- DÉBITO gistro do tipo 1 (soma- tório dos valores de dé- bito de janeiro a dezem- bro) TOTAL DE 19 35 17 Z Total dos créditos do CRÉDITOS registro do tipo 1 ( so- matório dos valores de débito de janeiro a de- zembro) TOTAL BASE DE CÁLCULO 36 52 17 Z Total da base de cálculo DAS do registro tipo 2 ( so- ENTRADAS matório dos valores de base de cálculo de todos os códigos fiscais das entradas) TOTAL 53 69 17 Z Total do imposto credi- IMPOSTO tado do registro tipo 2 CREDITADO (somatório dos valores de impostos creditados de todos os códigos fis- cais da entradas) TOTAL DE OPERAÇÕES 70 86 17 Z Total das operações sem S/DIREITO direito a crédito do im- A CRÉDITO posto do registro tipo 2 DO IMPOSTO (somatório dos valores das operações sem direi- to a crédito do imposto de todos os códigos fis- cais da entradas) TOTAL BASE DE 87 103 17 Z Total da base de cálculo CÁLCULOS do registro tipo 3 (so- DAS SAÍDAS matório dos valores da base cálculo de todos os códigos fiscais das saí- das) TOTAL IMPOSTO 104 120 17 Z Total do imposto debita- DEBITADO do do registro tipo 3 (somatório dos valores do imposto debitado de todos os códigos fiscais das saídas) TOTAL OPERAÇÕES Total das operações sem S/DIREITO direito de débito e/ou DE DÉBITO 121 137 17 Z com débito suspenso do E/OU COM registro tipo 3 (somató- DÉBITO rio dos valores das ope- SUSPENSO rações sem direito de débito e/ou com débito suspenso de todos códi- gos fiscais das saídas TOTAL Total dos valores de DEMONSTRA créditos Registro tipo 4 TIVOS DE 138 154 17 Z CRÉDITOS TOTAL DEMONSTRA TIVOS DE Total dos valores de dé- DÉBITOS 155 171 17 Z bitos do retro tipo 4 TOTAL RESUMO Total do resumo dos va- DAS 172 188 17 Z lores das entradas de ENTRADAS mercadorias com crédito DE MERC do registro tipo 4 (mer- ADORIAS cado nacional + externo) COM CRÉ DITO TOTAL RESUMO Total do resumo de valo- DAS ENTRA res das entradas de mer- DAS DE cadorias sem crédito do MERCA 189 205 17 Z registro tipo 4 (mercado DORIAS nacional + externo) SEM CRÉ DITO TOTAL RESUMO Total do resumo dos va- DAS SAÍ lores das saídas de mer- DAS DE 206 222 17 Z cadorias com débito do MERCA- registro 4 mercado na- DORIAS cional + mercado externo COM DÉ BITO TOTAL RESUMO Total do resumo dos va- DAS lores das saídas de mer- SAÍDAS cadorias sem débito do DE MERCA 223 239 17 Z registro tipo 4 (mercado DORIAS nacional + externo) SEM DÉBITO TOTAL 240 256 17 Z Total valor das mercado- NOP rias 50.7 257 273 17 Z Total imposto lançado TOTAL 274 290 17 Z Total valor das mercado- NOP rias 51.5 291 307 17 Z Total imposto lançado TOTAL 308 324 17 Z Total valor das mercado- NOP rias 52.3 325 341 17 Z Total imposto lançado TOTAL 342 358 17 Z Total valor das mercado NOP rias 53.1 359 375 17 Z Total imposto lançado TOTAL 376 392 17 Z Total valor das mercado- NOP rias 54.0 393 409 17 Z Total imposto lançado TOTAL 410 426 17 Z Total valor das mercado- NOP rias 55.8 427 443 17 Z Total imposto lançado TOTAL 444 460 17 Z Total valor das mercado- NOP rias 56.6 461 477 17 Z Total imposto lançado TOTAL 478 494 17 Z Total valor das mercado- NOP rias 57.4 495 511 17 Z Total imposto lançado TOTAL 512 528 17 Z Total valor das mercado- NOP rias 60.4 529 545 17 Z Total imposto lançado TOTAL 546 562 17 Z Total valor das mercado- NOP rias 61.2 563 579 17 Z Total imposto lançado TOTAL 580 596 17 Z Total valor das mercado- NOP rias 62.0 597 613 17 Z Total imposto lançado TOTAL 614 630 17 Z Total valor das mercado- NOP rias 63.9 631 647 17 Z Total imposto lançado TOTAL 648 664 17 Z Total valor das mercado- NOP rias 64.7 665 681 17 Z Total imposto lançado TOTAL 682 698 17 Z Total valor das mercado- NOP rias 70.1 699 715 17 Z Total imposto lançado TOTAL 716 732 17 Z Total valor das mercado- NOP rias 71.0 733 749 17 Z Total imposto lançado TOTAL 750 766 17 Z Total valor das mercado- NOP rias 72.8 767 783 17 Z Total imposto lançado TOTAL 784 800 17 Z Total valor das mercado- NOP rias 73.6 801 817 17 Z Total imposto lançado TOTAL 818 834 17 Z Total valor das mercado- NOP rias 77.2 835 851 17 Z Total imposto lançado TOTAL 852 868 17 Z Total valor das mercado- NOP rias 78.7 869 885 17 Z Total imposto lançado TOTAL 886 902 17 Z Total valor das mercado- NOP rias 80.9 903 919 17 Z Total imposto lançado TOTAL 920 936 17 Z Total valor das mercado- NOP rias 81.7 937 953 17 Z Total imposto lançado TOTAL 954 970 17 Z Total valor das mercado- NOP rias 84.1 971 987 17 Z Total imposto lançado TOTAL 988 1004 17 Z Total valor das mercado- NOP rias 85.0 1005 1021 17 Z Total imposto lançado TOTAL 1022 1038 17 Z Total valor das mercado- NOP rias 86.8 1039 1055 17 Z Total imposto lançado TOTAL 1056 1072 17 Z Total valor das mercado- NOP rias 90.6 1073 1089 17 Z Total imposto lançado TOTAL 1090 1106 17 Z Total valor das mercado- NOP rias 91.4 1107 1123 17 Z Total imposto lançado TOTAL 1124 1140 17 Z Total valor das mercado- NOP rias 92.2 1141 1157 17 Z Total imposto lançado 1158 1174 17 Z Total dos valores do iní- cio do período dos regis- TOTAL tros tipo 6 (somatório VALOR DE dos valores do início do INSUMOS período de insumos) Total dos valores do fi- nal do período dos regis- 1175 1191 17 Z tros tipo 6 (somatório dos valores do final do período de insumos). Total dos valores do iní- cio do período dos regis- TOTAL 1192 1208 17 Z tros tipo 7 (somatório dos valores do início do VALOR períodos de produtos aca- DE PRO bados) DUTOS Total dos valores do fi- ACABA nal do período dos regis- DOS 1209 1225 17 Z tros tipo 7 (somatório dos valores do final do período de produtos aca- bados) Total dos valores do iní- cio do período dos regis- TOTAL 1226 1242 17 Z tros tipo 8 (somatório VALOR dos valores do início do DE MER períodos de mercadorias CADORIAS adquirida ADQUIRI DAS Total dos valores do fi- nal do período dos regis- 1243 1259 17 Z tros tipo 8 (somatório dos valores do final de mercadorias adquiridas) TOTAL DE REGISTRO 1260 1264 05 Z Total dos registros tipo TIPO 5 5 gravados no arquivo. TOTAL DE REGISTRO 1265 1269 05 Z Total dos registros tipo TIPO 6 6 gravados no arquivo. TOTAL DE REGISTRO 1270 1274 05 Z Total dos registros tipo TIPO 7 7 gravados no arquivo. TOTAL DE REGISTRO 1275 1279 05 Z Total dos registros tipo TIPO 8 8 gravados no arquivo. QUANT IDADE TO 1280 1284 05 Z Quantidade total de todos TAL DE os tipos de registros gra- REGISTROS vados no arquivo (tipo 0 + tipo 1 + tipo 2 + tipo 3 + tipo 4 + tipo 5 + tipo 6 + tipo 7 + tipo 8 + tipo 9 ) "FILLER" 1285 1600 316 C B R A N C O S - ESTE REGISTRO É ÚNICO E DEVERÁ SER O ÚLTIMO REGISTRO DO ARQUIVO - OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS - SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO CONTER SINAL.

REGISTRO TIPO 0

REGISTRO MESTRE DO ARQUIVO

NOME DO POSIÇÃO

CAMPO INIC. FIM TAMAN. FORMATO CONTEÚDO

TIPO 01 01 01 Z Será "0". Será o primeiro

registro do arquivo.

Posição 2 a 9 - Num Básico

Posição 10 a 13- Num. Ordem

C.G.C 02 15 14 Z Posição 14 a 15 - DV

Deverá estar sempre comple-

to com 14 dígitos

Exercício

de Apuração 16 17 02 Z Será o ano do exercício de

apuração

Será "0" para Situação Nor-

mal

Será "1" para Retificação

de Declaração

Situação 18 18 01 C Será "2" para Encerramento

Especial de Atividades

Será "3"para Retificação de

Declaração e Encerramento

de Atividades

Optante

Convênio 19 19 01 Z Será "1" para optante pelo

ICMS Convênio ICMS Será "2" para

não optante pelo Convênio

ICMS

Registro

Especial de 20 37

Engarrafadores

20 31 12 Z Número da Ordem

32 37 6 Z Data da Emissão

Razão

Social 38 92 55 C Razão Social/Denominação

Comercial do Estab.

Endereço 93 222

E Z. 1027 1041 15 Z Saldo credor no período

T anterior

E 1042 1056 15 Z Saldo apurado

M

B 2ª 1057 1057 01 Z Será "2"

R Q 1058 1072 15 Z Débito

O U 1073 1087 15 Z Crédito

I 1088 1102 15 Z Saldo credor no período

N anterior

Z. 1103 1117 15 Z Saldo apurado

1ª 1118 1119 02 Z Será "10"

Q

U 1120 1120 01 Z Será "1"

I 1121 1135 15 Z Débito

O N 1136 1150 15 Z Crédito

U Z. 1151 1165 15 Z Saldo credor no período

T anterior

U 1166 1180 15 Z Saldo apurado

B

R 2ª 1181 1181 01 Z Será "2"

O Q 1182 1196 15 Z Débito

U 1197 1211 15 Z Crédito

I 1212 1226 15 Z Saldo credor no período

N anterior

Z. 1227 1241 15 Z Saldo apurado

1ª 1242 1243 02 Z Será "11"

Q

U 1244 1244 01 Z Será "1"

I 1245 1259 15 Z Débito

N N 1260 1274 15 Z Crédito

O Z. 1275 1289 15 Z Saldo credor no período

V anterior

E 1290 1304 15 Z Saldo apurado

M

B 2ª 1305 1305 01 Z Será "2"

R Q 1306 1320 15 Z Débito

O U 1321 1335 15 Z Crédito

I 1336 1350 15 Z Saldo credor no período

N anterior

Z. 1351 1365 15 Z Saldo apurado

1ª 1366 1367 02 Z Será "12"

Q

U 1368 1368 01 Z Será "1"

I 1369 1383 15 Z Débito

D N 1384 1398 15 Z Crédito

E Z. 1399 1413 15 Z Saldo credor no período

Z anterior

E 1414 1428 15 Z Saldo apurado

M

B 2ª 1429 1429 01 Z Será "2"

R Q 1430 1444 15 Z Débito

O U 1445 1459 15 Z Crédito

I 1460 1474 15 Z Saldo credor no período

N anterior

Z. 1475 1489 15 Z Saldo apurado

FILLER 1490 1600 111 C B R A N C O S

\- ESTE REGISTRO É ÚNICO E CORRESPONDE A PÁG.. 1 DO FORMULÁRIO I

\- OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM

CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS.

REGISTRO TIPO 2

DEMONSTRAÇÃO DAS ENTRADAS DE MERCADORIAS NO ESTABELECIMENTO -

FORMULÁRIO I

NOME DO POSIÇÃO

CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO

TIPO 01 01 01 Z Será "2".

Código 02 04 03 Z Será "111"

Fiscal 05 19 15 Z Base de Cálculo

111 20 34 15 Z Imposto creditado

35 49 15 Z Operações sem direito a

crédito de Imposto

Código 50 52 03 Z Será "111"

Fiscal 53 67 15 Z Base de Cálculo

111 68 82 15 Z Imposto creditado

83 97 15 Z Operações sem direito a

crédito de Imposto

Código 98 100 03 Z Será "112"

Fiscal 101 115 15 Z Base de Cálculo

112 116 130 15 Z Imposto creditado

131 145 15 Z Operações sem direito a

crédito de Imposto

Código 146 148 03 Z Será "113"

Fiscal 149 163 15 Z Base de Cálculo

113 164 178 15 Z Imposto creditado

179 193 15 Z Operações sem direito a

crédito de Imposto

Código 194 196 03 Z Será "121"

Fiscal 197 211 15 Z Base de Cálculo

121 212 226 15 Z Imposto creditado

227 241 15 Z Operações sem direito a

crédito de Imposto

Código 242 244 03 Z Será "121"

Fiscal 245 259 15 Z Base de Cálculo

121 260 274 15 Z Imposto creditado

275 289 15 Z Operações sem direito a

crédito de Imposto

Código 290 292 03 Z Será "122"

Fiscal 293 307 15 Z Base de Cálculo

122 308 322 15 Z Imposto creditado

323 337 15 Z Operações sem direito a

crédito de Imposto

Código 338 340 03 Z Será "131"

Fiscal 341 355 15 Z Base de Cálculo

131 356 370 15 Z Imposto creditado

371 385 15 Z Operações sem direito a

crédito de Imposto

Código 386 388 03 Z Será "132"

Fiscal 389 403 15 Z Base de Cálculo

132 404 418 15 Z Imposto creditado

419 433 15 Z Operações sem direito a

crédito de Imposto

Código 434 436 03 Z Será "193"

Fiscal 437 451 15 Z Base de Cálculo

193 452 466 15 Z Imposto creditado

467 481 15 Z Operações sem direito a

crédito de Imposto

Código 482 484 03 Z Será "194"

Fiscal 485 499 15 Z Base de Cálculo

194 500 514 15 Z Imposto creditado

515 529 15 Z Operações sem direito a

crédito de Imposto

Código 530 532 03 Z Será "199"

Fiscal 533 547 15 Z Base de Cálculo

199 548 562 15 Z Imposto creditado

563 577 15 Z Operações sem direito a

crédito de Imposto

Código 578 580 03 Z Será "211"

Fiscal 581 595 15 Z Base de Cálculo

211 596 610 15 Z Imposto creditado

611 625 15 Z Operações sem direito a

crédito de Imposto

Código 626 628 03 Z Será "211"

Fiscal 629 643 15 Z Base de Cálculo

211 644 658 15 Z Imposto creditado

659 673 15 Z Operações sem direito a

crédito de Imposto

Código 674 676 03 Z Será "212"

Fiscal 677 691 15 Z Base de Cálculo

212 692 706 15 Z Imposto creditado

707 721 15 Z Operações sem direito a

crédito de Imposto

Código 722 724 03 Z Será "213"

Fiscal 725 739 15 Z Base de Cálculo

213 740 754 15 Z Imposto creditado

755 769 15 Z Operações sem direito a

crédito de Imposto

Código 770 772 03 Z Será "221"

Fiscal 773 787 15 Z Base de Cálculo

221 788 802 15 Z Imposto creditado

803 817 15 Z Operações sem direito a

crédito de Imposto

Código 818 820 03 Z Será "221"

Fiscal 821 835 15 Z Base de Cálculo

221 836 850 15 Z Imposto creditado

851 865 15 Z Operações sem direito a

crédito de Imposto

Código 866 868 03 Z Será "222"

Fiscal 869 883 15 Z Base de Cálculo

222 884 898 15 Z Imposto creditado

899 913 15 Z Operações sem direito a

crédito de Imposto

Código 914 916 03 Z Será "231"

Fiscal 917 931 15 Z Base de Cálculo

231 932 946 15 Z Imposto creditado

947 961 15 Z Operações sem direito a

crédito de Imposto

Código 962 964 03 Z Será "232"

Fiscal 965 979 15 Z Base de Cálculo

232 980 994 15 Z Imposto creditado

995 1009 15 Z Operações sem direito a

crédito de Imposto

Código 1010 1012 03 Z Será "293"

Fiscal 1013 1027 15 Z Base de Cálculo

293 1028 1042 15 Z Imposto creditado

1043 1057 15 Z Operações sem direito a

crédito de Imposto

Código 1058 1060 03 Z Será "294"

Fiscal 1061 1075 15 Z Base de Cálculo

294 1076 1090 15 Z Imposto creditado

1091 1105 15 Z Operações sem direito a

crédito de Imposto

Código 1106 1108 03 Z Será "299"

Fiscal 1109 1123 15 Z Base de Cálculo

299 1124 1138 15 Z Imposto creditado

1139 1153 15 Z Operações sem direito a

crédito de Imposto

Código 1154 1156 03 Z Será "311"

Fiscal 1157 1171 15 Z Base de Cálculo

311 1172 1186 15 Z Imposto creditado

1187 1201 15 Z Operações sem direito a

crédito de Imposto

Código 1202 1204 03 Z Será "311"

Fiscal 1205 1219 15 Z Base de Cálculo

311 1220 1234 15 Z Imposto creditado

1235 1249 15 Z Operações sem direito a

crédito de Imposto

Código 1250 1252 03 Z Será "312"

Fiscal 1253 1267 15 Z Base de Cálculo

312 1268 1282 15 Z Imposto creditado

1283 1297 15 Z Operações sem direito a

crédito de Imposto

Código 1298 1300 03 Z Será "321"

Fiscal 1301 1315 15 Z Base de Cálculo

321 1316 1330 15 Z Imposto creditado

1331 1345 15 Z Operações sem direito a

crédito de Imposto

Código 1298 1300 03 Z Será "321"

Fiscal 1301 1315 15 Z Base de Cálculo

321 1316 1330 15 Z Imposto creditado

1331 1345 15 Z Operações sem direito a

crédito de Imposto

Código 1346 1348 03 Z Será "322"

Fiscal 1349 1363 15 Z Base de Cálculo

322 1364 1378 15 Z Imposto creditado

1379 1393 15 Z Operações sem direito a

crédito de Imposto

Código 1394 1396 03 Z Será "394"

Fiscal 1397 1411 15 Z Base de Cálculo

394 1412 1426 15 Z Imposto creditado

1427 1441 15 Z Operações sem direito a

crédito de Imposto

Código 1442 1444 03 Z Será "399"

Fiscal 1445 1459 15 Z Base de Cálculo

399 1460 1474 15 Z Imposto creditado

1475 1489 15 Z Operações sem direito a

crédito de Imposto

FILLER 1490 1600 111 C B R A N C O S

\- ESTE REGISTRO SERÁ ÚNICO NO ARQUIVO E CORRESPONDE AO FORMULÁRIO I

\- PÁGINA 2

\- OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM

CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS.

REGISTRO TIPO 3

DEMONSTRAÇÃO DAS SAÍDAS DE MERCADORIAS DO ESTABELECIMENTO -

FORMULÁRIO I

NOME DO POSIÇÃO

CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO

TIPO 01 01 01 Z Será "3".

Código 02 04 03 Z Será "511"

Fiscal 05 19 15 Z Base de Cálculo

511 20 34 15 Z Imposto Debitado

35 49 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 50 52 03 Z Será "512"

Fiscal 53 67 15 Z Base de Cálculo

512 68 82 15 Z Imposto Debitado

83 97 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 98 100 03 Z Será "513"

Fiscal 101 115 15 Z Base de Cálculo

513 116 130 15 Z Imposto Debitado

131 145 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 146 148 03 Z Será "521"

Fiscal 149 163 15 Z Base de Cálculo

521 164 178 15 Z Imposto Debitado

179 193 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 194 196 03 Z Será "522"

Fiscal 197 211 15 Z Base de Cálculo

522 212 226 15 Z Imposto Debitado

227 241 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 242 244 03 Z Será "531"

Fiscal 245 259 15 Z Base de Cálculo

531 260 274 15 Z Imposto Debitado

275 289 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 290 292 03 Z Será "532"

Fiscal 293 307 15 Z Base de Cálculo

532 308 322 15 Z Imposto Debitado

323 337 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 338 340 03 Z Será "593"

Fiscal 341 355 15 Z Base de Cálculo

593 356 370 15 Z Imposto Debitado

371 385 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 386 388 03 Z Será "594"

Fiscal 389 403 15 Z Base de Cálculo

594 404 418 15 Z Imposto Debitado

419 433 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 434 436 03 Z Será "599"

Fiscal 437 451 15 Z Base de Cálculo

599 452 466 15 Z Imposto Debitado

467 481 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 482 484 03 Z Será "611"

Fiscal 485 499 15 Z Base de Cálculo

611 500 514 15 Z Imposto Debitado

515 529 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 530 532 03 Z Será "612"

Fiscal 533 547 15 Z Base de Cálculo

612 548 562 15 Z Imposto Debitado

563 577 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 578 580 03 Z Será "613"

Fiscal 581 595 15 Z Base de Cálculo

613 596 610 15 Z Imposto Debitado

611 625 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 626 628 03 Z Será "621"

Fiscal 629 643 15 Z Base de Cálculo

621 644 658 15 Z Imposto Debitado

659 673 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 674 676 03 Z Será "622"

Fiscal 677 691 15 Z Base de Cálculo

622 692 706 15 Z Imposto Debitado

707 721 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 722 724 03 Z Será "631"

Fiscal 725 739 15 Z Base de Cálculo

631 740 754 15 Z Imposto Debitado

755 769 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 770 772 03 Z Será "632"

Fiscal 773 787 15 Z Base de Cálculo

632 788 802 15 Z Imposto Debitado

803 817 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 818 820 03 Z Será "693"

Fiscal 821 835 15 Z Base de Cálculo

693 836 850 15 Z Imposto Debitado

851 865 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 866 868 03 Z Será "694"

Fiscal 869 883 15 Z Base de Cálculo

694 884 898 15 Z Imposto Debitado

899 913 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 914 916 03 Z Será "699"

Fiscal 917 931 15 Z Base de Cálculo

699 932 946 15 Z Imposto creditado

947 961 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 962 964 03 Z Será "611"

Fiscal 965 979 15 Z Base de Cálculo

611 980 994 15 Z Imposto Debitado

995 1009 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 1010 1012 03 Z Será "612"

Fiscal 1013 1027 15 Z Base de Cálculo

612 1028 1042 15 Z Imposto Debitado

1043 1057 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 1058 1060 03 Z Será "613"

Fiscal 1061 1075 15 Z Base de Cálculo

613 1076 1090 15 Z Imposto Debitado

1091 1105 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 1106 1108 03 Z Será "631"

Fiscal 1109 1123 15 Z Base de Cálculo

631 1124 1138 15 Z Imposto Debitado

1139 1153 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 1154 1156 03 Z Será "693"

Fiscal 1157 1171 15 Z Base de Cálculo

693 1172 1186 15 Z Imposto creditado

1187 1201 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 1202 1204 03 Z Será "694"

Fiscal 1205 1219 15 Z Base de Cálculo

694 1220 1234 15 Z Imposto Debitado

1235 1249 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 1250 1252 03 Z Será "699"

Fiscal 1253 1267 15 Z Base de Cálculo

699 1268 1282 15 Z Imposto Debitado

1283 1297 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 1298 1300 03 Z Será "711"

Fiscal 1301 1315 15 Z Base de Cálculo

711 1316 1330 15 Z Imposto Debitado

1331 1345 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 1346 1348 03 Z Será "712"

Fiscal 1349 1363 15 Z Base de Cálculo

712 1364 1378 15 Z Imposto Debitado

1379 1393 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 1394 1396 03 Z Será "731"

Fiscal 1397 1411 15 Z Base de Cálculo

731 1412 1426 15 Z Imposto Debitado

1427 1441 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 1442 1444 03 Z Será "732"

Fiscal 1445 1459 15 Z Base de Cálculo

732 1460 1474 15 Z Imposto Debitado

1475 1489 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 1490 1492 03 Z Será "799"

Fiscal 1493 1507 15 Z Base de Cálculo

799 1508 1522 15 Z Imposto Debitado

1523 1537 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Código 1538 1540 03 Z Será "799"

Fiscal 1541 1555 15 Z Base de Cálculo

799 1556 1570 15 Z Imposto Debitado

1571 1585 15 Z Operações sem lançamento

de débito e/ou com débito

suspenso

Filler 1586 1600 15 C B R A N C O S

\- ESTE REGISTRO SERÁ ÚNICO NO ARQUIVO E CORRESPONDE AO FORMULÁRIO I

\- PÁGINA 3

\- OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM

CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS.

REGISTRO TIPO 4

DEMONSTRATIVO DE CRÉDITOS/DEMONSTRATIVO DE DÉBITOS/DADOS SOBRE

PESSOAL OCUPADO/RESUMO DE ENTRADAS E SAÍDAS DE MERCADORIAS

NOME DO POSIÇÃO

CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO

TIPO 01 01 01 Z Será "4"

02 16 15 Z Entradas de insumos do

mercado nacional

D

E

M 17 31 15 Z Entradas de insumos do

O mercado externo

N

S 32 46 15 Z Outras entradas

T

R 47 61 15 Z Insumos utilizados na fa-

A br de produtos exportados

T

I 62 76 15 Z Insumos utilizados no

fabr. de produtos vendi-

V dos a Empresa Comercial

O Exportadora - DL 1248/72

D 77 91 15 Z Insumos utilizados no fa-

E br máquinas e implementos

agrícolas.

C 92 106 15 Z Exportação de Prod. de

R Fabr. Nac. nos termos do

É DL. 1894/81 e LEI 7739/89

D

I 107 121 15 Z Outros Créditos Incenti-

vados

T

O 122 136 15 Z Outros Créditos

S

137 151 15 Z Total de outros Créditos

D D 152 166 15 Z Saídas para o Mercado Na-

cional

E E

M 167 181 15 Z Estorno de Créditos Bási-

cos

O D

N E 182 196 15 Z Inadimplemento do compro-

S B misso de exportação s/re-

T I gime "DRAW BACK"

R T 197 211 15 Z Estorno de outros crédi-

A O tos incentivados

T S

I 212 226 15 Z Ressarcimento de créditos

V

O 227 241 15 Z Outros Débitos

D P O 242 256 15 Z Pessoal ocupado na produ-

A E C ção (H/H)

D S U 257 271 15 Z Pessoal ocupado fora da

O S P produção (H/H)

S O A

A D 272 286 15 Z Consumo de energia elé-

S L O trica no período - (TOTAL

KWH)

O

B

R

E

R D 287 301 15 Z Mercado Nacional - insumos

E E com dito

S

U M 302 316 15 Z Mercado Nacional - insumos

M E sem crédito

O R

C 317 331 15 Z Mercado Nacional - outras

D A com crédito

E D 332 346 15 Z Mercado Nacional - outras

O sem crédito

E R 347 361 15 Z Mercado Externo - insumos

N I com crédito

T A 362 376 15 Z Mercado Externo - insumos

R S sem crédito

A

D

A 392 406 15 Z Mercado Externo - outras

S sem crédito

R D 407 421 15 Z Mercado Nacional - Produção

do Estabelecimento com dé-

E E bito

S

U M 422 436 15 Z Mercado Nacional - Produção

M E do Estabelecimento sem dé-

O R bito

C 437 451 15 Z Mercado Nacional - outras

D A com Débito

E D 452 466 15 Z Mercado Nacional - outras

O sem Débito

S R 467 481 15 Z Mercado Externo - Produção

A I do Estabelecimento com débi

I A to

D S 482 496 15 Z Mercado Externo - Produção

A do Estabelecimento sem débi

to.

497 511 15 Z Mercado Externo - outras

com débito

512 526 15 Z Mercado Externo - outras

sem débito

"FILLER" 527 1600 1073 Z B R A N C O S

\- ESTE REGISTRO É ÚNICO E CORRESPONDE A PÁGINA 4 DO FORMULÁRIO I

\- OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM

CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS

\- SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO CONTER

SINAL.

REGISTRO TIPO 5

DEMONSTRATIVO DE ENTRADAS E SAÍDAS DE MERCADORIAS - ANEXO 1

NOME DO POSIÇÃO

CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO

TIPO 01 01 01 Z Será "5"

Natureza

da 02 04 03 Z Código de Natureza

Operação da Operação

1ª

OCORRÊNCIA 05 14 10 Z Código NBM/SH

DO 15 27 13 Z Quantidade

REGISTRO 28 40 13 Z Valor da Mercadoria

41 53 13 Z Imposto Lançado

(débito/crédito)

NOME DO POSIÇÃO

CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO

NOME DO POSIÇÃO

CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO

54 1523 1470 30 OCORRÊNCIAS NO MES-

MO FORMATO DA 1º OCOR-

RÊNCIA (PARA A MESMA

NATUREZA DA OPERAÇÃO)

"FILLER 1524 1600 77 C B R A N C O S

\- ESTE REGISTRO CORRESPONDE AO FORMULÁRIO ANEXO 2 (INSUMOS)

\- PODERÃO EXISTIR VÁRIOS REGISTROS TIPO "6"

\- AS OCORRÊNCIAS DO REGISTROS NÃO UTILIZADAS DEVERÃO SER

PREENCHIDAS COM ZEROS

\- OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER INFORMADOS SEM

CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO SER OMITIDOS

\- OS CAMPOS DE QUANTIDADE DEVERÃO SER INFORMADOS SEM DECIMAIS, OU

SEJA, OS DÍGITOS DECIMAIS DEVERÃO SER OMITIDOS

\- SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO CONTER

SINAL

REGISTRO TIPO 6

DEMONSTRATIVO DOS ESTOQUES DE INSUMOS - ANEXOS 2

NOME DO POSIÇÃO

CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO

TIPO 01 01 01 Z Será "6"

1ª 02 11 10 Z Código NBM\\SH

OCORRÊNCIA 12 26 15 Z Quantidade Física no

Início do Período

do 27 41 15 Z Quantidade Física no

Final do Período

REGISTRO 42 56 15 Z Valor no Início do Pe-

ríodo

57 71 15 Z Valor no final do Pe-

ríodo

72 1541 1470 - 21 OCORRÊNCIAS NO MESMO

FORMATO DA 1º OCORRÊNCIA

"FILLER" 1542 1600 59 C B R A N C O S

\- ESTE REGISTRO CORRESPONDE AO FORMULÁRIO ANEXO 2

(INSUMOS)

\- PODERÃO EXISTIR VÁRIOS REGISTROS TIPO "6"

\- AS OCORRÊNCIAS DO REGISTRO NÃO UTILIZADAS DEVERÃO SER

PREENCHIDAS COM ZEROS

\- OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER

INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO

SER OMITIDOS

\- OS CAMPOS DE QUANTIDADE DEVERÃO SER INFORMADOS SEM

DECIMAIS, OU SEJA, OS DÍGITOS DECIMAIS DEVERÃO SER OMITIDOS

\- SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO

CONTER SINAL

REGISTRO TIPO 7

DEMONSTRATIVO DOS ESTOQUES DE PRODUTOS ACABADOS - ANEXO 2

NOME DO POSIÇÃO

CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO

TIPO 01 01 01 Z Será "7"

1ª 02 11 10 Z Código NBM\\SH

OCORRÊNCIA 12 26 15 Z Quantidade Física no

Início do Período

do 27 41 15 Z Quantidade Física no

Final do Período

REGISTRO 42 56 15 Z Valor no Início do

Período

57 71 15 Z Valor no final do Pe-

ríodo

72 1541 1470 - 21 OCORRÊNCIAS NO MESMO

FORMATO DA 1º OCORRÊNCIA

"FILLER" 1542 1600 59 C B R A N C O S

\- ESTE REGISTRO CORRESPONDE AO FORMULÁRIO ANEXO 2

(PRODUTOS ACABADOS)

\- PODERÃO EXISTIR VÁRIOS REGISTROS TIPO "7"

\- AS OCORRÊNCIAS DO REGISTRO NÃO UTILIZADAS DEVERÃO SER

PREENCHIDAS COM ZEROS

\- OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER

INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO

SER OMITIDOS

\- OS CAMPOS DE QUANTIDADE DEVERÃO SER INFORMADOS SEM

DECIMAIS, OU SEJA, OS DÍGITOS DECIMAIS DEVERÃO SER OMITIDOS

\- SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO

CONTER SINAL

REGISTRO TIPO 8

DEMONSTRATIVO DOS ESTOQUES DE MERCADORIAS ADQUIRIDAS - ANEXO 2

TIPO 01 01 01 Z Será "8"

1ª 02 11 10 Z Código NBM\\SH

OCORRÊNCIA 12 26 15 Z Quantidade Física no

Início do Período

do 27 41 15 Z Quantidade Física no

Final do Período

REGISTRO 42 56 15 Z Valor no Início do Pe-

ríodo

57 71 15 Z Valor no final do Pe-

ríodo

72 1541 1470 - 21 OCORRÊNCIAS NO MESMO

FORMATO DA 1º OCORRÊNCIA

"FILLER" 1542 1600 59 C B R A N C O S

\- ESTE REGISTRO CORRESPONDE AO FORMULÁRIOS ANEXO 2

(MERCADORIA ADQUIRIDAS

\- PODERÃO EXISTIR VÁRIOS REGISTROS TIPO "8"

\- AS OCORRÊNCIAS DOS REGISTO NÃO UTILIZADAS DEVERÃO SER

PREENCHIDAS COM ZEROS

\- OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO SER

INFORMADOS SEM CENTAVOS, OU SEJA, OS DÍGITOS DE CENTAVOS DEVERÃO

SER OMITIDOS

\- OS CAMPOS DE QUANTIDADE DEVERÃO SER INFORMADOS SEM

DECIMAIS, OU SEJA, OS DÍGITOS DECIMAIS DEVERÃO SER OMITIDOS

\- SOMENTE OS CAMPOS QUE POSSUEM DADOS MONETÁRIOS DEVERÃO

CONTER SINAL.

REGISTRO TIPO 9

REGISTRO TOTALIZADOR DO ARQUIVO

NOME DO POSIÇÃO

CAMPO INICIO FIM TAMANHO FORMATO CONTEÚDO

TIPO 01 01 01 C Será "9"

TOTAL DE 02 18 17 Z Total dos débitos do re-

DÉBITO gistro do tipo 1 (soma-

tório dos valores de dé-

bito de janeiro a dezem-

bro)

TOTAL DE 19 35 17 Z Total dos créditos do

CRÉDITOS registro do tipo 1 ( so-

matório dos valores de

débito de janeiro a de-

zembro)

TOTAL

BASE DE

CÁLCULO 36 52 17 Z Total da base de cálculo

DAS do registro tipo 2 ( so-

ENTRADAS matório dos valores de

base de cálculo de todos

os códigos fiscais das

entradas)

TOTAL 53 69 17 Z Total do imposto credi-

IMPOSTO tado do registro tipo 2

CREDITADO (somatório dos valores

de impostos creditados

de todos os códigos fis-

cais da entradas)

TOTAL DE

OPERAÇÕES 70 86 17 Z Total das operações sem

S/DIREITO direito a crédito do im-

A CRÉDITO posto do registro tipo 2

DO IMPOSTO (somatório dos valores

das operações sem direi-

to a crédito do imposto

de todos os códigos fis-

cais da entradas)

TOTAL

BASE DE 87 103 17 Z Total da base de cálculo

CÁLCULOS do registro tipo 3 (so-

DAS SAÍDAS matório dos valores da

base cálculo de todos os

códigos fiscais das saí-

das)

TOTAL

IMPOSTO 104 120 17 Z Total do imposto debita-

DEBITADO do do registro tipo 3

(somatório dos valores

do imposto debitado de

todos os códigos fiscais

das saídas)

TOTAL

OPERAÇÕES Total das operações sem

S/DIREITO direito de débito e/ou

DE DÉBITO 121 137 17 Z com débito suspenso do

E/OU COM registro tipo 3 (somató-

DÉBITO rio dos valores das ope-

SUSPENSO rações sem direito de

débito e/ou com débito

suspenso de todos códi-

gos fiscais das saídas

TOTAL Total dos valores de

DEMONSTRA créditos Registro tipo 4

TIVOS DE 138 154 17 Z

CRÉDITOS

TOTAL

DEMONSTRA

TIVOS DE Total dos valores de dé-

DÉBITOS 155 171 17 Z bitos do retro tipo 4

TOTAL

RESUMO Total do resumo dos va-

DAS 172 188 17 Z lores das entradas de

ENTRADAS mercadorias com crédito

DE MERC do registro tipo 4 (mer-

ADORIAS cado nacional + externo)

COM CRÉ

DITO

TOTAL

RESUMO Total do resumo de valo-

DAS ENTRA res das entradas de mer-

DAS DE cadorias sem crédito do

MERCA 189 205 17 Z registro tipo 4 (mercado

DORIAS nacional + externo)

SEM CRÉ

DITO

TOTAL

RESUMO Total do resumo dos va-

DAS SAÍ lores das saídas de mer-

DAS DE 206 222 17 Z cadorias com débito do

MERCA- registro 4 mercado na-

DORIAS cional + mercado externo

COM DÉ

BITO

TOTAL

RESUMO Total do resumo dos va-

DAS lores das saídas de mer-

SAÍDAS cadorias sem débito do

DE MERCA 223 239 17 Z registro tipo 4 (mercado

DORIAS nacional + externo)

SEM DÉBITO

TOTAL 240 256 17 Z Total valor das mercado-

NOP rias

50.7 257 273 17 Z Total imposto lançado

TOTAL 274 290 17 Z Total valor das mercado-

NOP rias

51.5 291 307 17 Z Total imposto lançado

TOTAL 308 324 17 Z Total valor das mercado-

NOP rias

52.3 325 341 17 Z Total imposto lançado

TOTAL 342 358 17 Z Total valor das mercado

NOP rias

53.1 359 375 17 Z Total imposto lançado

TOTAL 376 392 17 Z Total valor das mercado-

NOP rias

54.0 393 409 17 Z Total imposto lançado

TOTAL 410 426 17 Z Total valor das mercado-

NOP rias

55.8 427 443 17 Z Total imposto lançado

TOTAL 444 460 17 Z Total valor das mercado-

NOP rias

56.6 461 477 17 Z Total imposto lançado

TOTAL 478 494 17 Z Total valor das mercado-

NOP rias

57.4 495 511 17 Z Total imposto lançado

TOTAL 512 528 17 Z Total valor das mercado-

NOP rias

60.4 529 545 17 Z Total imposto lançado

TOTAL 546 562 17 Z Total valor das mercado-

NOP rias

61.2 563 579 17 Z Total imposto lançado

TOTAL 580 596 17 Z Total valor das mercado-

NOP rias

62.0 597 613 17 Z Total imposto lançado

TOTAL 614 630 17 Z Total valor das mercado-

NOP rias

63.9 631 647 17 Z Total imposto lançado
