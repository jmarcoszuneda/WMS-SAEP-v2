# ADR-0003 — Número público da requisição por contador anual transacional

## Status

Aceita

## Contexto

Toda requisição enviada para autorização recebe um número público no formato `REQ-AAAA-NNNNNN`, onde `AAAA` é o ano e `NNNNNN` uma sequência anual. O número nasce no primeiro envio, é imutável e deve ser único. Rascunhos nunca enviados não consomem número.

Três abordagens foram consideradas para gerar a sequência anual:

- `MAX(numero) + 1` sob lock de tabela.
- Sequence nativa do PostgreSQL, uma por ano.
- Model contador dedicado, com uma linha por ano.

`MAX + 1` implica varredura e maior contenção. Sequences do PostgreSQL pulam valores em rollback, gerando lacunas na numeração pública, e exigem criar e gerenciar um objeto de sequence por ano.

## Decisão

A numeração será gerada por um model contador, `SequenciaRequisicao`, com `ano` único e `ultimo_numero`.

O número público é emitido por `requisicoes.services` dentro de `transaction.atomic`. O service obtém a linha do ano corrente com `select_for_update`, incrementa `ultimo_numero`, persiste e formata `REQ-AAAA-NNNNNN`. A emissão ocorre apenas no primeiro envio para autorização e o número é imutável depois.

Não usar `MAX(numero) + 1`. Não usar sequence nativa do PostgreSQL anual nesta fase.

## Consequências

A numeração anual é gap-free: como o incremento ocorre dentro da mesma transação do envio, um rollback desfaz também o incremento.

`select_for_update` na linha do ano serializa emissões concorrentes do mesmo ano sem bloquear a tabela inteira.

A estratégia é portável — não depende de objetos específicos do PostgreSQL — e testável.

Cada ano novo exige a linha correspondente em `SequenciaRequisicao`; o service deve criá-la sob lock quando ausente, dentro do mesmo `atomic`.

A unicidade de `numero_publico` na `Requisicao` permanece como rede de segurança independente do contador.

## Trade-off

Um model contador adiciona uma linha "quente" por ano e exige disciplina: nenhuma emissão de número fora do service transacional. Aceita-se isso em troca de numeração anual sem lacunas, portável e sob controle explícito.
