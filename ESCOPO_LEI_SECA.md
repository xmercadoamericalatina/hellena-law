# Escopo: somente lei seca

A partir desta atualização, novas coletas usam `scripts/lei_seca/` e publicam a coleção em `lei-seca/`. Não coletam doutrina, jurisprudência, julgados, acórdãos, súmulas, pareceres ou soluções de consulta.

O estado anterior está preservado na branch [`arquivo/acervo-original-2026-10-26`](https://github.com/xmercadoamericalatina/leis/tree/arquivo/acervo-original-2026-10-26), no commit `15eb09b618ff08a38c4dfee06a91bd139d093f5d`. Nada foi apagado do histórico.

## Exclusões de categorias identificadas

As seguintes pastas de conteúdo interpretativo foram retiradas da branch principal. A seleção verifica categorias/pastas, não altera o texto de leis que mencionem decisões:

- `jurisprudencia` (árvore original `26be4c0442c63dcb0f352bacf31f65c65fc071fe`)
- `reguladores/agu/pareceres-normativos` (árvore original `12fe6eec78b034bb5f821b1e3a7a88b08e7fc33f`)
- `reguladores/agu/sumulas` (árvore original `e1bc7454b5d9f00986d7837515b54753b4284cf0`)
- `reguladores/anatel/sumulas` (árvore original `4f385ac4471407c64651a1679951ca44a9d48234`)
- `reguladores/anm/sumulas` (árvore original `e6c10ab1b0bf5c7af4bac0061b23a7d8c8ce904a`)
- `reguladores/anp/sumulas` (árvore original `68e7c9de6cc3ef55d5d0badad6d30cef0ca4d4a0`)
- `reguladores/ans/sumulas` (árvore original `36c74da3c2644087452a637c87486a3fc20a3396`)
- `reguladores/antt/sumulas` (árvore original `488042564ef1aad6c32136aa56ab42215b51780f`)
- `reguladores/anvisa/solucoes-de-consulta` (árvore original `caad0eea460bffd5ac5d2f771d5cae219380110f`)
- `reguladores/cne/sumulas` (árvore original `4693c8992cf1d9b1b323805dde765b68c113f7a8`)
- `reguladores/cvm/pareceres-normativos` (árvore original `a0acb305851cfd29097ceb135609a0896d1a17ac`)
- `reguladores/defesa/pareceres-normativos` (árvore original `74f3e8524ad8c9f47dc69ba9c60df4d2ab37d424`)
- `reguladores/fazenda/solucoes-de-consulta` (árvore original `66f3589c371cc1da55657470930f30b774d7bc44`)
- `reguladores/mapa/sumulas` (árvore original `a7a42a74e8f5992c2c4076cd9269638cdc9c8c44`)
- `reguladores/mdic/pareceres-normativos` (árvore original `148f9b021aef91025d8574fc416b7fed467d05a3`)
- `reguladores/mec/pareceres-normativos` (árvore original `8da5c5c6d1597f5400d7120a8fee28dfb05778db`)
- `reguladores/poder-judiciario/sumulas` (árvore original `3726b776d2b44b2f224e85d988c9b893526d1f89`)
- `reguladores/presidencia/solucoes-de-consulta` (árvore original `eeb8d1ff8a6ede8f3d23ecef050344c9ad6b3db9`)
- `reguladores/rfb/solucoes-de-consulta` (árvore original `adeaa8f15f24146e96662f645434ce8507f6e8e6`)
- `estaduais/DF/pareceres-normativos` (árvore original `b269d8bdda9a823ef23465601ee87fefb2d7f0dc`)
- `estaduais/DF/sumulas` (árvore original `3ed347347e837940f3a00e077858f83008b8573a`)

## Limites da revisão

A classificação por diretório não audita individualmente todos os documentos herdados. A Receita Federal também possui documentos em pastas por ano, que podem misturar tipos. O script `sanear_legado.py` permite localizar categorias interpretativas pelos metadados e registra tipos desconhecidos para revisão; não se afirma que todo o legado foi saneado.

`COBERTURA.md`, `PROGRESSO.md` e `WORKLOG.md` são relatórios históricos do projeto de origem e podem incluir contagens de conteúdo retirado. O indicador de cobertura do atualizador é `lei-seca/cobertura.json`, gerado após execução. A coleção ainda não é uma base nacional completa. Fontes não integradas e documentos sem validação permanecem explicitamente pendentes.
