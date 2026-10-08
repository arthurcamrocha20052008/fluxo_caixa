# 💰 Fluxo de Caixa

API em Python para controle financeiro pessoal e empresarial, desenvolvida com FastAPI, SQLAlchemy e MySQL.

O projeto foi estruturado para gerenciar usuários, contas bancárias, movimentações financeiras, cálculos por período e metas financeiras, oferecendo uma base sólida para acompanhamento do fluxo de caixa.

---

## 📌 Visão geral

Este sistema permite:

- cadastrar usuários;
- criar e acompanhar contas bancárias;
- registrar entradas, saídas, transferências e investimentos;
- corrigir saldos por meio de ajustes assinados;
- calcular saldos por período;
- gerar resumos financeiros;
- manter metas financeiras por usuário;
- manter a API organizada em módulos funcionais.

---

## 🚀 Stack tecnológica

| Tecnologia | Uso |
|---|---|
| Python | Linguagem principal |
| FastAPI | Framework da API REST |
| MySQL | Banco de dados relacional |
| SQLAlchemy | ORM e acesso ao banco |
| Pydantic | Validação de dados |
| Uvicorn | Servidor ASGI |
| python-dotenv | Variáveis de ambiente |
| pwdlib | Hash seguro de senhas |
| PyJWT | Tokens de acesso |
| Alembic | Migrações versionadas |
| pytest | Testes automatizados |
| Swagger / OpenAPI | Documentação interativa |

---

## 🏗️ Arquitetura da aplicação

```text
Cliente / Swagger
       │
       ▼
   FastAPI
       │
       ▼
  Rotas + regras de negócio
       │
       ▼
  SQLAlchemy / ORM
       │
       ▼
      MySQL
```

A aplicação está organizada em camadas:

- `backend/api.py` — inicialização da aplicação e registro das rotas
- `backend/rotasdeapi/` — endpoints por recurso
- `backend/financeiro.py` — regras de negócio e cálculos financeiros
- `backend/seguranca/` — geração e validação de hashes de senha
- `backend/autenticacao.py` — autenticação e tokens JWT
- `backend/migrations/` — histórico de migrações Alembic
- `backend/models.py` — modelos do banco
- `backend/esquema.py` — schemas e validações
- `backend/database.py` — conexão com o banco

---

## 📁 Estrutura do projeto

```text
fluxo_caixas/
├── .env
├── .gitignore
├── pytest.ini
├── explicaçao.txt
├── README.md
├── backend/
│   ├── api.py
│   ├── autenticacao.py
│   ├── database.py
│   ├── financeiro.py
│   ├── esquema.py
│   ├── models.py
│   ├── readme.md
│   ├── alembic.ini
│   ├── migrations/
│   │   ├── README.md
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   ├── versions/
│   │       ├── README.md
│   │       ├── adicionar_ajustes_e_resumos.py
│   │       ├── adicionar_tranferencia.py
│   │       ├── criar_categorias_movimentacao.py
│   │       ├── adicionar_ajustes_e_resumos.py
│   │       └── limitar_tentativas_login.py
│   ├── tests/
│   │   ├── README.md
│   │   ├── conftest.py
│   │   └── test_financeiro.py
│   ├── seguranca/
│   │   ├── __init__.py
│   │   ├── seguranca.py
│   │   └── readme.md
│   ├── rotasdeapi/
│       ├── __init__.py
│       ├── usuario.py
│       ├── conta_bancaria.py
│       ├── fluxo_dinheiro.py
│       ├── calculo_financeiro.py
│       ├── meta_financeira.py
│       └── readme.md
├── banco de dados/
│   ├── fluxo_caixa_usuarios.sql
│   ├── fluxo_caixa_contas_bancarias.sql
│   ├── fluxo_caixa_fluxo_dinheiro.sql
│   ├── fluxo_caixa_calculos_financeiros.sql
│   ├── fluxo_caixa_metas_financeiras.sql
│   └── readme.md
├── requirements.txt
└── .venv/  (ambiente local, não versionado)
```

---

## ✅ Funcionalidades implementadas

- cadastro de usuários;
- gestão de contas bancárias;
- registro de movimentações financeiras;
- categorização de entradas, saídas e investimentos;
- cálculos automáticos por período;
- geração de saldo inicial e saldo final;
- acompanhamento de metas financeiras;
- validação de dados via Pydantic;
- hash seguro de senhas;
- login com token JWT e isolamento dos dados por usuário;
- transferência entre contas com movimentações de débito e crédito vinculadas;
- ajustes de saldo com valor assinado;
- proteção contra saldo negativo em contas que não sejam correntes;
- paginação e filtros nas listagens;
- categorias fixas normalizadas e referenciadas no banco;
- limite persistente de tentativas de login;
- organização modular da API.

---

## 🔐 Segurança

A aplicação utiliza hashing para evitar o armazenamento de senhas em texto puro. O login emite tokens JWT assinados com uma chave configurada fora do código.

A senha do usuário é transformada em hash antes de ser persistida. O endpoint `POST /login` verifica credenciais e emite JWT; a chave `JWT_SECRET_KEY` deve ter pelo menos 32 caracteres e nunca deve ser commitada. Após cinco falhas de login do mesmo IP em 15 minutos, o banco bloqueia novas tentativas temporariamente e guarda apenas o hash do IP. As rotas financeiras exigem autenticação e limitam consultas aos recursos do usuário autenticado.

O CPF é validado no cadastro e omitido das respostas, mas ainda é armazenado sem criptografia no banco. Antes de usar dados reais em produção, implemente proteção adequada para esse dado pessoal e defina controles de acesso, retenção e backup.

---

## ▶️ Como executar

1. Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

2. Configure um arquivo `.env` na raiz com `DATABASE_URL` e `JWT_SECRET_KEY`. `ACCESS_TOKEN_EXPIRE_MINUTES` é opcional (padrão: 60). Gere uma chave aleatória forte localmente; não reutilize a chave de exemplo nem a publique.
3. Para um banco novo, aplique as migrações:

```bash
python -m alembic -c backend/alembic.ini upgrade head
```

4. Inicie a API:

```bash
python -m uvicorn api:app --app-dir backend --reload --host 0.0.0.0 --port 8000
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

Documentação interativa:

```text
http://127.0.0.1:8000/docs
```

---

## 🗄️ Banco de dados

O projeto usa MySQL. A estrutura é mantida por migrações Alembic versionadas em `backend/migrations/`.

As tabelas principais são:

- `usuarios`
- `contas_bancarias`
- `fluxo_dinheiro`
- `categorias_movimentacao`
- `calculos_financeiros`
- `metas_financeiras`
- `tentativas_login`

As categorias aceitas são fixas: `alimentacao`, `ajuste`, `compras`, `contas`, `educacao`, `freelance`, `impostos`, `investimento`, `lazer`, `moradia`, `outros`, `salario`, `saude`, `transporte`, `transferencia` e `vendas`. `ajuste` e `transferencia` são reservadas.

Os resumos mostram transferências recebidas/enviadas e ajustes em campos próprios, sem classificá-los como entradas ou saídas comuns. O saldo final considera todos esses movimentos. Um ajuste usa valor positivo para aumentar o saldo e negativo para reduzi-lo.

Os arquivos SQL em `banco de dados/` são dumps legados e incluem comandos destrutivos como `DROP TABLE`. Não os execute em bancos com dados; use Alembic para criar ou atualizar o esquema.

Para um banco legado já criado com o esquema original, faça backup e confira se as tabelas correspondem à revisão inicial antes de marcar essa revisão e aplicar as demais:

```bash
python -m alembic -c backend/alembic.ini stamp 20261008_0001
python -m alembic -c backend/alembic.ini upgrade head
```

Não marque a revisão inicial se o esquema existente não corresponder ao baseline.

---

## 📊 Status atual

Os cálculos financeiros, validações de entrada, regras de saldo e transferências possuem testes com SQLite. A cadeia completa de migrações também foi executada em um banco SQLite temporário. A migração do banco MySQL existente deve ser aplicada separadamente após backup e verificação do esquema.

Para executar os testes:

```bash
python -m pytest -q
```

---

## 🚀 Próximos passos

- refinamento de mensagens e tratamento de erros;
- configurar CORS ao integrar um frontend, restringindo as origens permitidas;
- ampliar testes de integração com MySQL;
- proteger o CPF armazenado e preparar os controles operacionais para produção;
- preparação para ambiente de produção.

---

## 📘 Observação

Este README foi atualizado para refletir a estrutura real do projeto, os módulos implementados e o estado atual da aplicação após validação de conexão e funcionamento do backend.
