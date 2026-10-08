# Migrações do banco

Esta pasta contém a configuração de execução das migrações Alembic do backend. As revisões versionadas ficam em `versions/`; elas são o histórico oficial de alterações no esquema do banco.

## Arquivos

- `env.py` carrega a URL de conexão configurada em `DATABASE_URL`, importa os modelos do projeto para obter os metadados SQLAlchemy e executa as revisões em modo online ou offline.
- `versions/` contém as revisões ordenadas por dependência: esquema inicial; transferências; categorias fixas/normalizadas; ajustes e totais separados nos resumos; e limite persistente de tentativas de login.

Os três primeiros arquivos usam nomes em inglês com numeração (`20261008_0001_initial_schema.py`, `20261008_0002_transfer_movements.py` e `20261008_0003_movement_categories.py`). Os IDs internos dessas revisões foram preservados para compatibilidade com bancos que possam já as ter aplicado. Novas revisões usam o slug em `file_template = %%(slug)s`; para solicitar também um ID descritivo, informe `--rev-id` ao comando Alembic.

## Comandos

Execute na raiz do repositório:

```bash
python -m alembic -c backend/alembic.ini upgrade head
```

Para consultar a revisão atualmente aplicada:

```bash
python -m alembic -c backend/alembic.ini current
```

`DATABASE_URL` deve estar configurada antes da execução. Em um banco existente, faça backup e compare o esquema com a revisão inicial antes de usar `stamp` ou aplicar atualizações. Não execute as migrações contra um banco com dados sem verificar previamente o destino e o esquema.
