# ⚙️ Backend — Fluxo de Caixa

Este backend foi desenvolvido para gerenciar o sistema financeiro do projeto com uma API REST em FastAPI. Ele conecta ao banco de dados MySQL por meio do SQLAlchemy, valida dados com Pydantic e organiza a lógica em módulos específicos para usuários, contas, movimentações, cálculos e segurança.

As rotas financeiras exigem autenticação JWT e limitam os dados acessíveis ao usuário autenticado.

---

## 🎯 Objetivo

O backend tem como objetivo centralizar a regra de negócio do sistema financeiro, com foco em:

- cadastro e consulta de usuários;
- controle de contas bancárias;
- registro de movimentações financeiras;
- cálculo de saldos e resumos por período;
- gestão de metas financeiras;
- segurança na persistência de senhas.

---

## 🧰 Stack

- Python
- FastAPI
- SQLAlchemy
- MySQL
- Pydantic
- Uvicorn
- pwdlib
- PyJWT
- Alembic

---

## 📁 Estrutura atual

```text
backend/
├── api.py
├── autenticacao.py
├── database.py
├── financeiro.py
├── esquema.py
├── models.py
├── readme.md
├── alembic.ini
├── migrations/
│   ├── env.py
│   └── versions/
├── tests/
│   ├── conftest.py
│   └── test_financeiro.py
├── seguranca/
│   ├── __init__.py
│   ├── seguranca.py
│   └── readme.md
└── rotasdeapi/
    ├── __init__.py
    ├── usuario.py
    ├── conta_bancaria.py
    ├── fluxo_dinheiro.py
    ├── calculo_financeiro.py
    ├── meta_financeira.py
    └── readme.md
```

---

## 🧩 Componentes principais

### `api.py`
Inicializa a aplicação FastAPI e registra todos os routers da API.

### `database.py`
Responsável pela configuração da engine, sessão do banco e conexão com o MySQL. A aplicação informa claramente se `DATABASE_URL` estiver ausente.

### `autenticacao.py`
Emite e valida JWT assinados com a variável de ambiente `JWT_SECRET_KEY`.

### `financeiro.py`
Calcula totais por meio de agregações SQL e reconstrói os saldos, incluindo as duas pontas das transferências.

### `models.py`
Define os modelos ORM das entidades do sistema: usuários, contas, categorias, fluxo, cálculos e metas.

### `esquema.py`
Contém os schemas de entrada e saída usados pela API com validação do Pydantic.

### `rotasdeapi/`
Agrupa os endpoints organizados por recurso:

- `usuario.py`
- `conta_bancaria.py`
- `fluxo_dinheiro.py`
- `calculo_financeiro.py`
- `meta_financeira.py`

### `seguranca/`
Módulo dedicado ao hash e verificação de senha.

---

## 🔄 Fluxo da aplicação

```text
Requisição HTTP
      │
      ▼
  Router da API
      │
      ▼
  Regras de negócio (`financeiro.py`)
      │
      ▼
  SQLAlchemy ORM
      │
      ▼
     MySQL
```

---

## ▶️ Como executar

```bash
python -m uvicorn api:app --app-dir backend --reload --host 0.0.0.0 --port 8000
```

Configure `DATABASE_URL` e `JWT_SECRET_KEY` no `.env` da raiz. A chave JWT precisa ter pelo menos 32 caracteres. O login está disponível em `POST /login`; nas demais rotas, envie o token no cabeçalho `Authorization: Bearer <access_token>`. `ACCESS_TOKEN_EXPIRE_MINUTES` configura a validade do token (padrão: 60 minutos).

Para criar ou atualizar o esquema:

```bash
python -m alembic -c backend/alembic.ini upgrade head
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

Documentação Swagger/OpenAPI:

```text
http://127.0.0.1:8000/docs
```

---

## 🧠 Módulos do sistema

### Usuários
- cadastro;
- listagem;
- consulta por ID;
- exclusão;
- validação de dados, como CPF e e-mail.

### Contas bancárias
- criação e atualização;
- associação ao usuário;
- controle de saldo atual;
- ativação/desativação.

### Fluxo de dinheiro
- entradas;
- saídas;
- transferências;
- ajustes de saldo assinados;
- investimentos;
- registros com data, categoria e observação.

### Cálculos financeiros
- saldo inicial;
- total de entradas;
- total de saídas;
- total de investimentos;
- totais separados de transferências recebidas/enviadas e ajustes;
- saldo final.

### Metas financeiras
- criação de metas;
- acompanhamento de progresso;
- atualização e exclusão.

---

## 🔐 Segurança

O módulo `seguranca` protege as senhas antes do armazenamento. O login emite JWT; as respostas de usuário omitem o CPF; e as rotas filtram as consultas pelo usuário autenticado. O CPF ainda é armazenado sem criptografia no banco; implemente proteção para esse dado pessoal antes de usar dados reais em produção.

## 💳 Regras de saldo e transferências

- O saldo não pode ser editado pelo endpoint de atualização da conta; ajustes devem ser lançados como movimentações.
- Ajustes de saldo são lançamentos do tipo `ajuste`; use valor positivo para aumentar e negativo para reduzir. Eles aparecem em `total_ajustes`, não como renda ou gasto.
- Contas correntes podem ter saldo negativo. Contas poupança e investimento não podem.
- Uma transferência entre contas do mesmo usuário cria lançamentos vinculados para origem e destino.
- Os resumos exibem transferências recebidas/enviadas separadamente, sem classificá-las como renda/gasto; o saldo final considera esses valores.
- As categorias de movimentação são uma lista fixa em português sem acentos: `alimentacao`, `ajuste`, `compras`, `contas`, `educacao`, `freelance`, `impostos`, `investimento`, `lazer`, `moradia`, `outros`, `salario`, `saude`, `transporte`, `transferencia` e `vendas`. `ajuste` e `transferencia` são reservadas a seus respectivos tipos.
- Uma meta cancelada permanece cancelada mesmo que o valor atual alcance o objetivo.
- Transferências são excluídas como um par. Uma conta com transferências precisa ter os lançamentos removidos antes de ser excluída.
- Após cinco falhas de login do mesmo endereço IP em 15 minutos, novas tentativas desse IP recebem HTTP 429 durante a janela de bloqueio. O banco guarda um hash do endereço, não o IP em texto.

## 🧪 Testes e migrações

Execute os testes com `python -m pytest -q`. `pytest.ini` configura os imports do backend e os testes usam SQLite temporário. `backend/tests/conftest.py` compartilha as fixtures de banco e cliente HTTP.

O Alembic mantém o esquema versionado em `migrations/`. Os dumps SQL em `banco de dados/` são legados e contêm `DROP TABLE`; não os execute em bancos com dados.

---

## ✅ Status atual

Os testes das regras financeiras e a cadeia Alembic foram validados com SQLite temporário. A atualização do MySQL existente ainda deve ser executada após backup e verificação do esquema.

---

## 🚀 Próximas etapas

- [ ] ampliar testes de integração com MySQL e cenários de borda
- [ ] configurar CORS ao conectar um frontend
- [ ] preparação para produção
