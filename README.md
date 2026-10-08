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
- acompanhar o percentual atingido e o valor restante de cada meta;
- consultar relatórios diários, semanais, mensais e anuais por conta;
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
- `banco de dados/migrations/` — configuração e histórico de migrações Alembic
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
├── README.md
├── ESTRUTURA.md
├── requirements.txt
├── backend/
│   ├── api.py
│   ├── autenticacao.py
│   ├── configuracao.py
│   ├── dados_sensiveis.py
│   ├── database.py
│   ├── financeiro.py
│   ├── esquema.py
│   ├── models.py
│   ├── readme.md
│   ├── tests/
│   ├── seguranca/
│   ├── rotasdeapi/
├── frontend/
│   └── README.md
├── banco de dados/
│   ├── alembic.ini
│   ├── migrations/
│   ├── fluxo_caixa_usuarios.sql
│   ├── fluxo_caixa_contas_bancarias.sql
│   ├── fluxo_caixa_fluxo_dinheiro.sql
│   ├── fluxo_caixa_calculos_financeiros.sql
│   ├── fluxo_caixa_metas_financeiras.sql
│   └── readme.md
└── .venv/  (ambiente local, não versionado)
```

O backend concentra a API, as regras, os modelos e os testes. `banco de dados/`
concentra as migrações oficiais do Alembic e os dumps SQL antigos. A pasta
`frontend/` é o ponto de entrada da aplicação web; por enquanto contém apenas
instruções e ainda não tem uma aplicação implementada. Arquivos de configuração
do projeto e documentação geral permanecem na raiz.

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

O CPF é validado no cadastro, cifrado com Fernet antes de ser salvo e omitido das respostas. Uma impressão HMAC com chave derivada da chave CPF permite detectar duplicatas sem armazenar o CPF em texto puro. Configure uma `CPF_ENCRYPTION_KEY` Fernet separada da chave JWT. Guarde uma cópia segura dessa chave: perdê-la impede descriptografar CPFs existentes; não a troque sem um procedimento de recifragem. A migração `proteger_cpf` converte registros legados e seu downgrade é bloqueado para evitar voltar a armazenar CPFs em texto puro.

No Windows, as credenciais locais são carregadas primeiro de `%LOCALAPPDATA%\fluxo_caixa\secrets.env`, fora da pasta sincronizada do projeto. O arquivo `.env` da raiz continua sendo aceito como fallback; não guarde nele credenciais se o projeto estiver em uma pasta sincronizada, como OneDrive.

O CORS permite somente a origem local `http://fluxocaixa`, para a integração com o frontend. O nome `fluxocaixa` precisa apontar para `127.0.0.1` no arquivo `hosts` do Windows, e o frontend deve ser servido pela porta HTTP padrão 80 para que a URL não mostre uma porta. A API pode continuar em `http://fluxocaixa:8000`. Atualize a allowlist quando definir a origem de produção.

---

## ▶️ Como executar

1. Instale as dependências na raiz do projeto:

```bash
python -m pip install -r requirements.txt
```

2. Configure as variáveis de ambiente antes de iniciar a API:

```bash
DATABASE_URL=sqlite:///./fluxo_caixa.db
JWT_SECRET_KEY=sua_chave_segura_com_32_ou_mais_caracteres
CPF_ENCRYPTION_KEY=sua_chave_fernet_gerada_localmente
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

No Windows, o projeto também aceita um arquivo local em `%LOCALAPPDATA%\fluxo_caixa\secrets.env` para segredos fora da pasta sincronizada. `ACCESS_TOKEN_EXPIRE_MINUTES` é opcional (padrão: 60). Gere uma chave Fernet localmente com:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

3. Para um banco novo, aplique as migrações:

```bash
python -m alembic -c "banco de dados/alembic.ini" upgrade head
```

4. Inicie a API a partir da raiz do projeto:

```bash
python main.py
```

Ou, se preferir rodar diretamente com Uvicorn:

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
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

O projeto usa MySQL. A estrutura é mantida por migrações Alembic versionadas em `banco de dados/migrations/`.

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

As respostas de metas incluem `progresso_percentual` (com duas casas decimais) e `valor_restante` (nunca negativo). Metas atingidas são marcadas como concluídas, exceto quando foram explicitamente canceladas. Os relatórios são criados em `POST /calculos-financeiros/` para períodos diário, semanal, mensal ou anual e retornam saldos inicial/final, entradas, saídas e totais financeiros associados.

Os arquivos SQL em `banco de dados/` são dumps legados e incluem comandos destrutivos como `DROP TABLE`. Não os execute em bancos com dados; use Alembic para criar ou atualizar o esquema.

Para um banco legado já criado com o esquema original, faça backup e confira se as tabelas correspondem à revisão inicial antes de marcar essa revisão e aplicar as demais:

```bash
python -m alembic -c "banco de dados/alembic.ini" stamp esquema_inicial
python -m alembic -c "banco de dados/alembic.ini" upgrade head
```

Não marque a revisão inicial se o esquema existente não corresponder ao baseline.

---

## 📊 Status atual

Os cálculos financeiros, validações de entrada, regras de saldo, transferências e casos extremos de metas/relatórios possuem testes com SQLite. Testes HTTP cobrem cadastro/login/JWT, contas, movimentações, metas, relatórios, CORS, proteção dos dados sensíveis e isolamento entre usuários; os testes automatizados usam SQLite em memória e não alteram o MySQL configurado. A integração da API com o MySQL também foi validada separadamente. O MySQL está na revisão `proteger_cpf`; `alembic check` não detecta diferenças em relação aos modelos. Execute os comandos Alembic da raiz usando `python -m alembic -c "banco de dados/alembic.ini" ...`.

Para executar os testes:

```bash
python -m pytest -q
```

Os testes de integração HTTP usam um banco SQLite em memória isolado; o fluxo completo de autenticação, contas, movimentações, saldo, isolamento entre usuários e limpeza não altera o MySQL configurado em `.env`.

---

## 🚀 Próximos passos

- refinamento de mensagens e tratamento de erros;
- configurar CORS ao integrar um frontend, restringindo as origens permitidas;
- ampliar cenários de borda para metas e relatórios;
- proteger o CPF armazenado e preparar os controles operacionais para produção;
- preparação para ambiente de produção.

---

## 📘 Observação

Este README foi atualizado para refletir a estrutura real do projeto, os módulos implementados e o estado atual da aplicação após validação de conexão e funcionamento do backend.
