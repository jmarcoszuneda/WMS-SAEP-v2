# ADR-0004 — Arquitetura em camadas dos apps de domínio

## Status

Aceita

## Contexto

Os apps de domínio (`accounts`, `estoque`, `requisicoes`) concentram regras sensíveis: máquina de estados, autorização contextual, mutação transacional de estoque. Sem uma divisão de responsabilidades explícita, regra de domínio vaza para views e models de forma inconsistente, e cada novo agente ou desenvolvedor inventa a própria organização.

ADR-0001 já posiciona policies no app dono do caso de uso. ADR-0002 e ADR-0003 pressupõem services transacionais. `docs/estado-transicoes-requisicao.md` exige transições declarativas aplicadas por uma função única.

## Decisão

Cada app de domínio adota um layout interno padrão:

- `models.py` — schema, constraints, choices e properties simples. Não orquestra casos de uso.
- `transitions.py` (em `requisicoes`) — tabela declarativa da máquina de estados.
- `services.py` — comandos de domínio. Único ponto de mutação de domínio. Abrem `transaction.atomic` quando aplicável, chamam policies, aplicam transições, registram timeline e disparam notificações apenas via `transaction.on_commit`.
- `policies.py` — autorização contextual. Chamadas tanto por views quanto por services.
- `selectors.py` — leituras não triviais, filas e escopos de visibilidade.
- `forms.py` — validação de input.
- `views.py` — finas; sem regra de domínio; orquestram input → policy → service/selector → render.
- `urls.py`, `admin.py`, `tests/`.

`services.py`, `policies.py` e `selectors.py` começam como arquivo único por app; são promovidos a pacote apenas quando o volume justificar.

Notificações nunca são pré-condição de uma transição de domínio e são disparadas só após o commit.

## Consequências

View nunca contém regra de domínio nem decisão de autorização própria.

Toda mutação de estado de domínio passa por um service.

A mesma policy é chamada por view e por service (PER-08); checagem de view não substitui policy.

Leitura com escopo de visibilidade vai para selector, não se espalha em views.

Models não importam services nem disparam casos de uso em `save()`.

Notificação que falhe não desfaz a transição.

A regra operacional detalhada para agentes fica em `docs/CONVENTIONS.md`.

## Trade-off

Mais arquivos e indireção por app do que um Django de "views gordas + models". Aceita-se em troca de fronteiras testáveis, autorização única e um codebase navegável por agentes de IA.
