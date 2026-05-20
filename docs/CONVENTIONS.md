# Convenções de implementação — WMS-SAEP

Regras operacionais para implementar features nos apps de domínio. Decisão de
fundo: [ADR-0004](adr/0004-arquitetura-em-camadas.md). ADRs relacionados:
[0001](adr/0001-papeis-de-dominio-derivados.md) (papéis derivados),
[0002](adr/0002-auditoria-por-models-de-dominio.md) (auditoria),
[0003](adr/0003-numero-publico-contador-anual.md) (número público).

## Layout de um app de domínio

```
apps/<app>/
  models.py        schema, constraints, choices, properties simples
  transitions.py   (só requisicoes) tabela declarativa da máquina de estados
  services.py      comandos de domínio; único ponto de mutação
  policies.py      autorização contextual
  selectors.py     leituras não triviais, filas, escopos de visibilidade
  forms.py         validação de input
  views.py         views finas
  urls.py
  admin.py
  tests/
```

`services.py`, `policies.py`, `selectors.py` começam como arquivo único.
Promover a pacote (`services/` com um módulo por caso de uso) só quando o
volume justificar. Arquivos nascem com conteúdo — não criar stubs vazios.

## Onde colocar cada coisa

| Preciso de... | Camada |
|---|---|
| Novo campo, constraint, choice, property trivial | `models.py` |
| Mutar estado de domínio (criar, transicionar, baixar saldo) | `services.py` |
| Decidir se um ator pode fazer algo | `policies.py` |
| Listar/filtrar com escopo de visibilidade ou fila | `selectors.py` |
| Validar dados de um formulário | `forms.py` |
| Receber request e devolver response | `views.py` |
| Regra de transição estado→estado | `transitions.py` |

## Regras

**Views são finas.** Fluxo: ler input → chamar policy → chamar service ou
selector → renderizar. Nenhuma regra de domínio, nenhuma query de escopo,
nenhuma decisão de autorização própria na view.

**Services são o único ponto de mutação de domínio.** Um service:
- abre `transaction.atomic` quando há escrita de domínio;
- chama a policy aplicável antes de mutar;
- aplica transições via `transitions.py` (em `requisicoes`);
- registra os eventos de `TimelineRequisicao`;
- dispara notificações apenas via `transaction.on_commit`.

**Policies são autorização contextual compartilhada.** A mesma policy é
chamada pela view e pelo service (PER-08). Checagem na view não substitui a
policy no service. Policy decide a partir de ator + objeto/contexto; o papel
efetivo é derivado (ADR-0001), nunca lido de um campo no usuário.

**Selectors concentram leitura não trivial.** Filas de autorização e
atendimento, escopo de visibilidade por papel e listagens filtradas. Leitura
trivial pode usar o ORM direto na view.

**Models não orquestram.** Guardam schema, constraints, choices e properties
simples (ex.: `saldo_disponivel`). Não importam services, não disparam casos
de uso em `save()`, não geram timeline por signals.

**Auditoria é por model de domínio** (ADR-0002): `TimelineRequisicao`,
`MovimentacaoEstoque`, `ReservaEstoque`. Sem `django-simple-history`.

**Estoque** (ADR-0004 + EST-06): toda mutação de saldo passa por
`estoque.services`, sob `transaction.atomic` + `select_for_update` sobre
`SaldoEstoque`, em ordem determinística. Nenhum outro app escreve saldo.

## Checklist ao adicionar uma feature

- O caso de uso vive em `services.py`? A view ficou fina?
- A policy é chamada por view e por service?
- Mutação de domínio está dentro de `transaction.atomic`?
- Transições de requisição passam por `transitions.py`?
- O evento foi registrado em `TimelineRequisicao`?
- Notificações só em `transaction.on_commit`?
- Há teste de caminho feliz, permissão negada e violação de domínio
  (ver `docs/matriz-invariantes.md`)?
