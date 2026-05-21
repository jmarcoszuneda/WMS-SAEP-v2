# Manutenção de memórias Serena

- Ao iniciar trabalho neste projeto, confirme `Active project: WMS-SAEP-v2` com `get_current_config` e rode `check_onboarding_performed` antes de depender das memórias.
- Leia memórias relevantes antes de alterar código, docs ou backlog. Memórias base atuais esperadas: `project_overview`, `style_and_conventions`, `suggested_commands`, `task_completion` e esta `memory_maintenance`.
- Trate memórias como resumo operacional, não como fonte única. Quando houver divergência entre memória e árvore atual, prefira código/docs vivos e atualize a memória afetada.
- `project_overview` deve refletir a topologia real do repo. Estado atual conhecido: Django 6/Python 3.13, apps `accounts`, `core`, `estoque`, `requisicoes`, `notificacoes`, config em `config/settings/`, docs em `docs/`, templates/static em `apps/core` e `apps/accounts`.
- Atualize memórias no mesmo turno quando uma decisão durável mudar: arquitetura, workflow de testes, comandos, escopo de apps, invariantes de domínio, convenção de linguagem ou política de migrations efêmeras.
- Para mudanças de schema/modelos, mantenha memória alinhada com a regra do projeto: migrations locais são efêmeras; fonte de verdade é `models`, constraints, indexes, regras de domínio e testes; fluxo estrutural exige `make setup`.
- Para navegação fina, use Serena primeiro: `get_symbols_overview` para arquivos novos, `find_symbol` para classes/funções específicas, `find_referencing_symbols` antes de refatorar ou mudar contrato.
- Não registre detalhes transitórios: logs locais, saídas longas de teste, branches temporárias, WIP sem decisão, erros já resolvidos sem valor recorrente.
- Registre só conteúdo reutilizável por agentes futuros: decisões confirmadas, comandos canônicos, riscos recorrentes, invariantes, padrões de implementação e pontos de entrada do código.
- Ao atualizar memória existente, leia antes e depois da alteração para confirmar persistência. Use `write_memory` para nova memória e `edit_memory` para ajustes focados.
- Se uma memória estiver stale, corrija de forma explícita em vez de criar memória paralela contraditória.
