# ADR-0002 — Auditoria por models de domínio, sem snapshots automáticos

## Status

Aceita

## Contexto

O sistema precisa de rastreabilidade do ciclo de vida das requisições e das mutações de estoque.

Uma opção seria adotar `django-simple-history`, que gera snapshots `Historical*` a cada `save()`. Essa abordagem registra alterações técnicas de linhas e campos.

Os documentos de domínio, porém, já especificam um histórico de negócio curado para requisições, por meio de timeline de eventos. Também tratam movimentações, reservas, baixas, devoluções e estornos de estoque como conceitos de domínio.

Timeline de requisição, movimentação de estoque e reserva de estoque não são snapshots técnicos. São fatos de negócio.

## Decisão

Não adotar `django-simple-history` nesta fase — nem globalmente, nem para estoque.

O histórico de negócio da requisição será modelado explicitamente em `requisicoes` como `TimelineRequisicao`.

`TimelineRequisicao` é obrigatória, visível ao usuário e registra eventos de domínio curados, como criação, envio para autorização, autorização, recusa, atendimento, devolução e estorno, com ator, timestamp, transição/estado e justificativa quando aplicável.

As mutações de estoque serão auditadas por models de domínio, como `MovimentacaoEstoque` e `ReservaEstoque`, não por snapshots automáticos de `save()`.

Snapshots técnicos de linha não são fonte de verdade para o ciclo de vida da requisição nem para saldo, reserva ou movimentação de estoque.

## Consequências

A fonte de verdade de auditoria operacional será sempre um model de domínio explícito.

Não adicionar `django-simple-history` ao projeto nesta fase.

Não envolver models atuais em `HistoricalRecords`.

Não criar tabelas `Historical*` nesta fase.

Não substituir `TimelineRequisicao` por signals genéricos de `save()`.

Não usar snapshots técnicos como histórico visível ao usuário.

Todo evento auditável relevante deve ter representação de domínio: campo, model, registro de timeline, reserva ou movimentação.

`simple-history` pode ser reavaliado no futuro apenas se houver requisito explícito de auditoria técnica de models cadastrais, como `User`, `Setor` ou `Material`.

Se adotado no futuro, o uso deve ser restrito, não global, e registrado em ADR própria.

## Trade-off

Auditar por models de domínio exige modelar explicitamente cada evento, transição e movimentação, em vez de obter auditoria técnica de campo automaticamente.

Aceitamos esse custo em troca de histórico curado, com significado de negócio, justificativas e uma fonte de verdade adequada para operação, tela de usuário e rastreabilidade do domínio.
