# Estrutura do projeto

Este guia explica onde encontrar cada parte do Fluxo de Caixa.

## Pastas principais

```text
fluxo_caixas/
├── backend/             API, regras, modelos e testes Python
├── banco de dados/      Alembic, revisões e dumps SQL legados
├── frontend/            Aplicação web (ainda não implementada)
├── README.md            Visão geral e instruções para executar o projeto
├── ESTRUTURA.md         Este guia
├── requirements.txt     Dependências Python do backend
└── pytest.ini           Configuração dos testes do backend
```

## Backend

- `api.py`: cria a aplicação FastAPI e registra os endpoints.
- `rotasdeapi/`: endpoints de usuários, contas, movimentações, relatórios e metas.
- `financeiro.py`: regras e cálculos financeiros.
- `models.py`: modelos ORM das tabelas.
- `esquema.py`: schemas e validações da API.
- `database.py`: conexão e sessões SQLAlchemy.
- `autenticacao.py`, `dados_sensiveis.py` e `seguranca/`: autenticação, proteção de CPF e senhas.
- `tests/`: testes automatizados; usam SQLite isolado.

## Banco de dados

- `alembic.ini` e `migrations/`: configuração e histórico oficial das migrações.
- `*.sql`: dumps antigos, mantidos apenas para referência. Podem conter comandos destrutivos; use Alembic para atualizar o esquema.

Execute os comandos Alembic a partir da raiz, por exemplo:

```bash
python -m alembic -c "banco de dados/alembic.ini" current
python -m alembic -c "banco de dados/alembic.ini" upgrade head
```

## Frontend

A pasta `frontend/` é reservada para a aplicação web e, por enquanto, contém apenas instruções. O código, as dependências e os testes específicos do frontend devem ficar nessa pasta.

## Arquivos da raiz

Configurações gerais do projeto, documentação e dependências do backend ficam na raiz. `.env` é somente uma configuração local ignorada pelo Git; no Windows, segredos locais são carregados de `%LOCALAPPDATA%\fluxo_caixa\secrets.env`.
