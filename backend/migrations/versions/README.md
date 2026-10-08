# Revisões Alembic

Os arquivos Python desta pasta descrevem, em ordem, as alterações versionadas no esquema do banco. Cada revisão declara uma função `upgrade()` e, quando possível, uma função `downgrade()`.

## Histórico atual

| Revisão | Descrição |
|---|---|
| `20261008_0001` | Cria o esquema inicial: usuários, contas bancárias, movimentações, cálculos financeiros e metas. |
| `20261008_0002` | Adiciona os campos que relacionam as duas pontas de uma transferência e a conta contraparte. |
| `20261008_0003` | Cria `categorias_movimentacao`, normaliza categorias existentes e adiciona a referência entre movimentações e categorias. |
| `ajustes_e_resumos` | Adiciona ajustes assinados, totais separados de transferências e normaliza categorias legadas para a lista fixa. |
| `limite_login` | Cria o armazenamento de tentativas de login para limitar falhas por endereço cliente. |

As dependências entre revisões são declaradas por `down_revision`. Os IDs das revisões antigas foram mantidos para preservar compatibilidade com bancos que já as aplicaram. Não renomeie ou remova revisões já aplicadas; crie uma nova revisão para mudanças futuras e revise o resultado antes de aplicá-la a dados existentes.

Os novos arquivos de revisão usam nomes descritivos em português. `alembic.ini` define `file_template = %%(slug)s`; para criar uma revisão com ID textual explícito, use por exemplo `alembic revision -m "limitar tentativas de login" --rev-id limite_login`. As operações de downgrade podem remover colunas ou tabelas, e a reversão do ajuste converte ajustes existentes em entradas/saídas. Faça backup e avalie os dados antes de reverter uma revisão.
