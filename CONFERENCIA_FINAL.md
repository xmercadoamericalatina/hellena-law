# Conferência da transferência — 27/10/2026

A execução [40496970572](https://github.com/xmercadoamericalatina/hellena-law/actions/runs/40496970572) concluiu com sucesso: 1.213.027 arquivos transferíveis do snapshot `30ca553382452a83c7d4643248ed9fecc90c0844` conferidos por modo e SHA Git; zero divergências. Testes do atualizador e auditoria da coleção passaram.

## Atualização posterior na origem

A origem avançou para `195e11025a11adb451e2971b735500b2253eacb1` durante a migração. A coleção `lei-seca` desse ponto foi preservada integralmente em `arquivo-origem/195e11025a11adb451e2971b735500b2253eacb1/lei-seca`. Sua árvore Git é exatamente `f001cc1a7f3af1af14e4e62172ec093f657bb06f`, idêntica à origem, incluindo o estado da fila. Os demais diretórios de acervo mantêm os mesmos SHAs de árvore na origem e no destino.

Um documento (`senado-33429875`) havia sido obtido na origem e sofrido erro transitório de leitura no destino. Seus quatro arquivos (texto, original, metadados e versão) foram recuperados com os mesmos SHAs, e a fila, o índice, a cobertura e as pendências foram reconciliados sem substituir o avanço da nova coleta. A coleção curada passa a 284 textos publicados.

## Atualizador independente

O workflow `lei-seca.yml` usa o próprio repositório e fontes oficiais; não lê o repositório antigo. A primeira execução [40499547392](https://github.com/xmercadoamericalatina/hellena-law/actions/runs/40499547392) passou nos testes, na auditoria e na gravação de novo commit, publicando 149 documentos. A conclusão global ficou vermelha para sinalizar nove fontes com pendências e uma leitura incompleta, não por falha ao gravar no repositório. A leitura incompleta foi suprida pela recuperação descrita acima; as pendências de fontes continuam registradas para correção posterior.

Não se declara que todas as fontes estão funcionando nem que a base jurídica está completa ou vigente. O código de transferência mantém referência à origem apenas para a migração e não é necessário ao atualizador recorrente. Licença preexistente preservada em `LICENSE-TERCEIROS`.

Nenhum repositório foi excluído por esta conferência.
