# Atualizador de lei seca

Implementação independente dos coletores herdados, Python 3.12, somente biblioteca padrão.
Nenhum modelo de IA, chave de API paga ou serviço de interpretação jurídica é utilizado.

## Política

Entram Constituição, emendas, leis, decretos-leis, medidas provisórias, decretos e atos normativos expressamente admitidos em `core.py`. Ficam fora jurisprudência, acórdãos, sentenças, súmulas, orientações jurisprudenciais, pareceres, soluções de consulta, notícias, doutrina e proposições ainda em tramitação. Ser publicado por órgão público, por si só, não torna um documento lei seca.

A transcrição conserva a redação e notas da própria fonte, inclusive tachados e referências judiciais inseridas pelo editor oficial. Não apaga uma disposição porque ela menciona um julgamento. Não inclui o texto do julgamento nem produz interpretação, resumo ou consolidação própria. O campo de vigência não é inferido de uma consulta HTTP bem-sucedida. Texto compilado pode conter dispositivos com efeitos futuros.

A pasta `lei-seca/` e seu `indice.json` são a coleção mantida por este atualizador. O material herdado nas demais pastas não recebe certificação automática. O histórico original está preservado na branch `arquivo/acervo-original-2026-10-26`. Exclusões de categorias interpretativas identificadas estão documentadas em `ESCOPO_LEI_SECA.md`.

## Script por script

| Arquivo | Responsabilidade |
| --- | --- |
| `fontes.json` | Prioridades, índices oficiais, APIs SAPL habilitadas e lacunas conhecidas. |
| `core.py` | HTTPS oficial, limites de tamanho e requisições, bloqueio de IP privado, extração literal, SHA-256 e versões. |
| `coletar.py` | Descoberta por tipo/ano no Senado, resolução de textos, SAPL paginado e links legislativos do portal da reforma tributária. |
| `atualizar.py` | Fila retomável, reconsulta de normas existentes, checkpoints, índice, cobertura e pendências. |
| `auditar.py` | Confere escopo, correspondência do índice, originais comprimidos e hashes dos textos. |
| `sanear_legado.py` | Examina tipos dos documentos herdados. Simula por padrão; `--aplicar` remove somente categorias interpretativas explícitas. Tipos desconhecidos ficam para revisão. |
| `test_lei_seca.py` | Testes sem rede, com fontes simuladas e alteração de textos já publicados. |
| `.github/workflows/lei-seca.yml` | Testes, coleta agendada, auditoria e commit no GitHub. |

## Executar

Na raiz do repositório:

```sh
python3 -I -m unittest discover -s scripts/lei_seca -p 'test_*.py' -v
python3 -I scripts/lei_seca/atualizar.py --mode prioridades
python3 -I scripts/lei_seca/atualizar.py --mode completo --limit 150 --indices 8 --historic 2
python3 -I scripts/lei_seca/auditar.py lei-seca
```

Não rode duas instâncias locais gravando na mesma pasta. No GitHub, `concurrency` serializa as execuções. Use `--output /outro/diretorio` para um ensaio independente. `--force` ignora o intervalo de rechecagem; não ignora validação de conteúdo ou restrições de acesso.

## Rotina automática

O workflow na branch padrão agenda quatro execuções diárias: 03h17, 09h17, 15h17 e 21h17, horário de Belém. São horários solicitados ao GitHub; a execução pode atrasar. Também roda quando este pacote é alterado na `main` ou mediante **Actions → Atualizar lei seca → Run workflow**.

A conexão que grava o workflow precisa ter permissão `workflows`. O `GITHUB_TOKEN` precisa permitir escrita de conteúdo na branch e as Actions precisam estar habilitadas. O workflow usa `contents: write`, não solicita segredos nem chaves externas e nunca usa force push. Se proteção da branch impedir o commit, a execução falha de forma visível. Forks podem ter agendamentos desabilitados ou suspensos pelo GitHub; confira a primeira execução em Actions.

A coleta salva checkpoints e pendências mesmo quando uma fonte falha. Uma execução com erros fica vermelha após salvar o resultado, em vez de declarar sucesso parcial como atualização completa. Confira `ultima_execucao.json`, `pendencias.json` e `cobertura.json`.

## Prioridades e atualização histórica

A configuração inicial reconsulta diariamente a Constituição, EC 132/2023, LC 214/2025, LC 227/2026, CTN, Simples Nacional, CLT, Lei 13.467/2017 e outras leis trabalhistas/previdenciárias. O índice oficial da Receita é usado para descobrir links de novas normas; o conteúdo explicativo da página não é incorporado.

A legislação federal é descoberta em 14 séries da API do Senado, com ciclos separados para o ano atual/anterior e para a carga histórica desde o início de cada série. Os demais documentos são reconsultados a cada 30 dias quando alcançam a frente da fila. Os intervalos são mínimos, não um SLA: volume, limites de execução e indisponibilidade de fontes podem alongá-los. Não há promessa de atualização em tempo real.

O job padrão consulta oito fatias recentes e duas históricas por execução e processa até 150 documentos. Esses valores limitam custo, uso do runner e carga nos portais. A primeira carga pode levar muito tempo; aumente os limites em infraestrutura própria se necessário, respeitando a taxa de requisições. Versões históricas ficam preservadas mesmo quando a norma é revogada.

## Abrangência real e expansão

Há conectores habilitados para a base federal do Senado, prioridades do Planalto e SAPL das assembleias AC, AL, AM, PB, PI, RO, RR e TO. Os URLs SAPL foram identificados no coletor preexistente; disponibilidade e esquema de cada API precisam ser confirmados em execução real.

Para um município que utiliza SAPL, cadastre uma fonte com `id` único, `url` HTTPS oficial, `esfera: "municipal"`, `uf`, `municipio` e `habilitado: true`. O conector lê os tipos da própria API, percorre páginas e admite apenas categorias normativas. Isso não descobre automaticamente todos os portais brasileiros.

Fontes estaduais com outros sistemas, os demais municípios e o acervo infralegal integral de RFB/MTE exigem adaptadores específicos. Não há pretensão de coletor universal pronto para todos os portais. As lacunas são publicadas em `cobertura.json`; números de documentos não certificam completude nacional.

PDFs são preservados, porém não publicados como texto validado: não se presume que `pdftotext` ou OCR recuperou anexos, tabelas e imagens. HTML pode conter elementos visuais e notas: `integralidade: nao_certificada` é explícito. O original comprimido, seu SHA-256 e a fonte ficam disponíveis para conferência. Não abra originais como código nem os trate como uma certificação antivírus.

## Dados

- `textos/`: transcrição literal em blocos de texto, sem executar HTML/JavaScript recebido.
- `metadados/`: fonte, tipo normativo, hash, conferência e qualidade.
- `originais/`: resposta original comprimida, endereçada por SHA-256.
- `versoes/`: metadados das versões observadas; originais correspondentes preservados.
- `estado.json`: fila e cursores; não apagar para continuar a carga.
- `indice.json`: documentos publicados; marca a última tentativa pendente quando há falha posterior.
- `pendencias.json`: documentos que aguardam coleta ou validação.
- `cobertura.json`: fontes cobertas e lacunas.

Testes locais validam o funcionamento com respostas simuladas. Falha de DNS impediu a coleta direta do Planalto no ambiente de desenvolvimento; a primeira execução real no GitHub é necessária para confirmar acesso aos portais e possíveis mudanças de layout. Não se declara o acervo atualizado antes dessa verificação.
