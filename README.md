# 💰 Sistema de Fluxo de Caixa — Enterprise Edition

> 🌐 **Aplicação Web Online (Vercel):** [**https://fluxo-caixa-coral-two.vercel.app**](https://fluxo-caixa-coral-two.vercel.app)  
> ⚡ **API Backend em Produção (Render):** [**https://fluxo-caixa-cuq1.onrender.com**](https://fluxo-caixa-cuq1.onrender.com) | [**Swagger UI (`/docs`)**](https://fluxo-caixa-cuq1.onrender.com/docs) | [**Healthcheck (`/health`)**](https://fluxo-caixa-cuq1.onrender.com/health)  
> 📜 **Histórico de Atualizações:** [**HISTORICO.md**](./HISTORICO.md)

<div align="center">

[![Live Demo](https://img.shields.io/badge/Demo_Online-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://fluxo-caixa-coral-two.vercel.app)
[![API Status](https://img.shields.io/badge/API_Backend-Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://fluxo-caixa-cuq1.onrender.com/health)
[![Database](https://img.shields.io/badge/Database-Supabase_PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![Database](https://img.shields.io/badge/MySQL_Compatível-TiDB_Cloud-005571?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x_ORM-D71F00?logo=databricks&logoColor=white)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-16_Revisões-F59E0B?logo=alembic&logoColor=white)](https://alembic.sqlalchemy.org/)
[![Pytest](https://img.shields.io/badge/Pytest-Automated_Suite-brightgreen?logo=pytest&logoColor=white)](https://pytest.org/)
[![Security](https://img.shields.io/badge/Security-Zero_CPF_LGPD_Fernet_AES128_%2B_Argon2id_%2B_OAuth2-blueviolet)](https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd)
[![WCAG](https://img.shields.io/badge/Accessibility-WCAG_AA_Light_%26_Dark-10B981)](frontend/css/style.css)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

<br/>

**Plataforma Full-Stack de gestão patrimonial e fluxo de caixa corporativo/pessoal em nuvem. Construída com API REST assíncrona em FastAPI, banco de dados relacional (Supabase PostgreSQL / TiDB Cloud MySQL), precisão contábil exata (`Decimal 12,2`), arquitetura de privacidade Zero-CPF sob a LGPD (Fernet AES-128 + Argon2id), Login Social Google OAuth 2.0, verificação multi-canal 2FA/OTP (E-mail ou SMS), Design Engineering de alta precisão (`Emil Kowalski` + `Impeccable` + `Taste-Skill` + `Ponytail`) e Design System Dual-Theme WCAG AA.**

</div>

---

## 📑 Sumário

- [Acesso Rápido à Demo Online](#-acesso-rápido-à-demo-online)
- [Visão Geral & Proposta de Valor](#-visão-geral--proposta-de-valor)
- [Motores de Engenharia de Design & Qualidade](#-motores-de-engenharia-de-design--qualidade)
- [Arquitetura Full-Stack em Nuvem](#-arquitetura-full-stack-em-nuvem)
- [Principais Funcionalidades e Diferenciais](#-principais-funcionalidades-e-diferenciais)
- [Stack Tecnológica Completa](#-stack-tecnológica-completa)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Execução Local Passo a Passo](#-execução-local-passo-a-passo)
- [Deploy em Nuvem (Vercel + Render + Supabase)](#-deploy-em-nuvem-vercel--render--supabase)
- [Catálogo de Endpoints da API](#-catálogo-de-endpoints-da-api)
- [Segurança & Privacidade LGPD (Zero-CPF)](#-segurança--privacidade-lgpd-zero-cpf)
- [Qualidade & Testes Automatizados](#-qualidade--testes-automatizados)
- [Histórico de Desenvolvimento (Changelog)](HISTORICO.md)
- [Documentações Complementares](#-documentações-complementares)

---

## 🌍 Acesso Rápido à Demo Online

| Recurso / Serviço | Plataforma | URL Pública | Finalidade |
|---|---|---|---|
| **Landing Page Institucional** | Vercel Edge | [https://fluxo-caixa-coral-two.vercel.app](https://fluxo-caixa-coral-two.vercel.app) | Apresentação de recursos, privacidade Zero-CPF LGPD e CTAs (`/inicio.html`) |
| **Aplicação Web (SPA)** | Vercel Edge | [https://fluxo-caixa-coral-two.vercel.app/index.html](https://fluxo-caixa-coral-two.vercel.app/index.html) | Painel financeiro autenticado (Modo Claro e Escuro) |
| **Página de Login** | Vercel Edge | [https://fluxo-caixa-coral-two.vercel.app/login.html](https://fluxo-caixa-coral-two.vercel.app/login.html) | Acesso seguro com Google OAuth 2.0, E-mail + Senha, OTP (E-mail/SMS) e rate limiting |
| **Página de Cadastro** | Vercel Edge | [https://fluxo-caixa-coral-two.vercel.app/cadastro.html](https://fluxo-caixa-coral-two.vercel.app/cadastro.html) | Abertura de conta sem CPF (Nome, E-mail, Telefone DDD e Senha Forte) + 2FA OTP |
| **Termos & Privacidade LGPD** | Vercel Edge | [https://fluxo-caixa-coral-two.vercel.app/privacidade.html](https://fluxo-caixa-coral-two.vercel.app/privacidade.html) | Termos de Uso e Política de Privacidade em linguagem clara e humana (Lei nº 13.709/2018) |
| **API REST (Backend)** | Render Web Service | [https://fluxo-caixa-cuq1.onrender.com](https://fluxo-caixa-cuq1.onrender.com) | Núcleo de serviços e regras contábeis |
| **Documentação Interativa** | Swagger UI | [https://fluxo-caixa-cuq1.onrender.com/docs](https://fluxo-caixa-cuq1.onrender.com/docs) | Teste e inspeção direta de endpoints |
| **Healthcheck Operacional** | Render Monitor | [https://fluxo-caixa-cuq1.onrender.com/health](https://fluxo-caixa-cuq1.onrender.com/health) | Diagnóstico de integridade da API |

> [!NOTE]
> No plano gratuito do Render, caso a API permaneça inativa por alguns minutos, a primeira requisição (*cold start*) pode levar cerca de **30 a 50 segundos** para despertar o contêiner. Após a inicialização, todas as respostas são servidas em milissegundos.

---

## 🌟 Visão Geral & Proposta de Valor

O **Sistema de Fluxo de Caixa** substitui o uso frágil de planilhas manuais por uma arquitetura transacional, auditável e resiliente:
- **Precisão Financeira Estrita:** Todo cálculo opera com aritmética contábil `Decimal(12, 2)`, sem dízimas ou erros de ponto flutuante.
- **Privacidade por Padrão (Zero-CPF):** Seguindo o princípio de minimização de dados da LGPD (Art. 6º, III), não exigimos CPF para criar ou acessar sua conta — o cadastro utiliza exclusivamente **Nome, E-mail, Telefone Celular (DDD) e Senha** (ou **Google OAuth 2.0**).
- **Psicologia das Cores Financeiras:** Design corporativo sóbrio (`#0B0F19`, `#111827`, `#059669`, `#3B82F6`, `#BE123C`), sem emojis ou símbolos Unicode informais, utilizando exclusivamente ícones vetoriais SVG de alta definição.
- **Módulo Unificado de Investimentos:** Aporte direto em ativos de Renda Fixa e Renda Variável com débito automático da conta de origem e consolidação patrimonial em tempo real.
- **Classificação Transacional:** Subdivisão estruturada de receitas (**Ganhos Fixos** vs **Ganhos Variáveis**) e despesas (**Gastos Fixos** vs **Gastos Variáveis**).

---

## ⚡ Motores de Engenharia de Design & Qualidade

A interface e a arquitetura de código operam sob 4 pilares de engenharia integrados em [`.agents/rules/core-skills.md`](.agents/rules/core-skills.md):

1. **Emil Kowalski Design Engineering (Física & Micro-interações):**
   - Curvas de aceleração naturais (`cubic-bezier(0.22, 1, 0.36, 1)`) com duração calibrada entre `160ms` e `220ms`.
   - Feedback tátil imediato (`scale(0.97)`) em botões ativos, animações de entrada ancoradas (`transform-origin`) em modais e respeito rigoroso a `@media (prefers-reduced-motion: reduce)`.
2. **Impeccable UI System (Craft, Typeset & Harden):**
   - Alinhamento óptico de bordas e raios de curvatura proporcionais, estados visuais completos (`default`, `hover`, `focus-visible` com anel de foco, `active`, `disabled`).
   - Tipografia financeira com `font-variant-numeric: tabular-nums` em todos os saldos, KPIs e tabelas, `letter-spacing: -0.022em` em títulos e medida ideal de leitura (`66ch`) nos documentos legais.
3. **Taste-Skill Aesthetic Engine (Curadoria Estética & Anti-Tells):**
   - Superfícies em camadas de grafite/ardósia escuro (`#0B0F19` -> `#111827`) com bordas translúcidas de `1px` (`rgba(255, 255, 255, 0.08)`), livre de gradientes neon clichês ou símbolos Unicode improvisados.
   - Botão **Continuar com Google** (`#google-oauth-btn`) desenhado como elemento principal de conversão com ícone vetorial oficial em 4 cores.
4. **Ponytail Code Discipline (Zero Débito Técnico):**
   - Eliminação de código duplicado entre módulos JS, remoção de atributos `style="..."` inline nas páginas HTML e atualização unificada de cache-busting (`?v=19`).

---

## 🏛️ Arquitetura Full-Stack em Nuvem

A aplicação adota o princípio de **Separação de Responsabilidades (SoC)** com três camadas desacopladas em nuvem e suporte nativo a ambiente local:

```mermaid
flowchart TD
    subgraph PresentationLayer ["🌐 Camada de Apresentação (Vercel CDN / Edge)"]
        SPA["Frontend SPA (index.html, login.html, cadastro.html, inicio.html)"]
        DESIGN["Design System & Física de Movimento (style.css)"]
        HTTP_CLIENT["Cliente HTTP & Módulos (api.js, legal.js)"]
        SPA --- DESIGN
        SPA --> HTTP_CLIENT
    end

    subgraph ApplicationLayer ["⚡ Camada de Aplicação (Render / FastAPI)"]
        CORS_FILTER["Middleware CORS Estrito por Ambiente"]
        RATE_LIMIT["Rate Limiter Anti-Brute Force (IP + E-mail)"]
        SECURITY_MOD["OAuth2 JWT + Hashing Argon2id (pwdlib)"]
        ROUTERS["Controladores REST (/rotasdeapi)"]
        ENGINE["Motor Contábil & Regras de Domínio (financeiro.py)"]
        CRYPTO["Criptografia LGPD (Fernet AES-128 + Blind Index HMAC)"]
        OTP_SVC["Serviço Multi-Canal OTP E-mail & SMS (servicos/email.py)"]

        HTTP_CLIENT -- "HTTPS REST JSON (Bearer JWT)" --> CORS_FILTER
        CORS_FILTER --> RATE_LIMIT
        RATE_LIMIT --> SECURITY_MOD
        SECURITY_MOD --> ROUTERS
        ROUTERS --> ENGINE
        ROUTERS --> CRYPTO
        ROUTERS --> OTP_SVC
    end

    subgraph PersistenceLayer ["🗄️ Camada de Persistência (Supabase PostgreSQL / TiDB Cloud)"]
        ORM["SQLAlchemy 2.x Declarative Models"]
        POOL["Engine com SSL/TLS Nativo & Pool Pre-Ping"]
        ALEMBIC["Alembic Migrations (16 Revisões Versionadas)"]
        DATABASE[("Supabase PostgreSQL 15+ / TiDB MySQL Serverless")]

        ENGINE --> ORM
        CRYPTO --> ORM
        ORM --> POOL
        POOL -- "Conexão Segura Criptografada (Pooler 6543)" --> DATABASE
        ALEMBIC -. "Upgrade Automático no Deploy" .-> DATABASE
    end
```

---

## 🚀 Principais Funcionalidades e Diferenciais

### 💼 Motor Contábil & Investimentos
- **Gestão de Investimentos Integrada:** Registro de aportes com dedução instantânea da conta bancária de origem e integração direta com o resumo de patrimônio. Ativos suportados:
  - *Renda Fixa:* Poupança, CDB, LCI/LCA, Tesouro Direto, Fundos de Investimento.
  - *Renda Variável:* Ações, ETFs, FIIs e Subscrições.
- **Subdivisão de Entradas e Saídas:**
  - *Entradas:* Classificação explícita entre **Ganhos Fixos** (Salário, pró-labore) e **Ganhos Variáveis** (Pix, vendas de itens, freelas, rendimentos).
  - *Saídas:* Classificação entre **Gastos Fixos** (contas essenciais) e **Gastos Variáveis** (consumo pontual).
- **Transferências Atômicas Vinculadas:** Operações entre contas geram pares vinculados por `transferencia_id` (UUIDv4) com trava pessimista (`SELECT ... FOR UPDATE`), garantindo que a exclusão de qualquer ponta reverta os saldos das duas contas de forma indivisível.
- **Orçamentos Mensais & Alertas Proativos:** Estabeleça tetos de gastos por categoria no mês, com barras de progresso dinâmicas e avisos de saídas nos próximos 7 dias.

### 🔐 Autenticação Multi-Canal (Zero-CPF), 2FA/OTP & Google OAuth 2.0
- **Cadastro Simplificado (Sem CPF):** Abertura de conta rápida e transparente utilizando **Nome Completo, E-mail, Telefone com DDD e Senha Forte** (5 requisitos verificados em tempo real).
- **Login Social com Google (`#google-oauth-btn`):** Suporte ao `id_token` oficial (Google Identity Services) e ao `access_token` via popup OAuth 2.0. Quando o `GOOGLE_CLIENT_ID` não está configurado, o sistema aciona automaticamente o **Fluxo Google Assistido** (pedindo apenas Nome, E-mail e Telefone opcional).
- **Verificação 2FA/OTP via E-mail ou SMS:** O usuário escolhe receber o código numérico de 6 dígitos por **E-mail** ou **SMS** tanto no cadastro quanto na recuperação de senha, podendo alternar o canal com 1 clique.
- **Modo de Contingência Resiliente:** Caso o provedor SMTP/SMS não esteja configurado no ambiente, o código de 6 dígitos é exibido em banner informativo na própria interface (`modo_contingencia`) para impedir bloqueios de acesso.
- **Copywriting LGPD Claro e Humano:** Termos de Uso (`/termos.html`) e Política de Privacidade (`/privacidade.html`) escritos em linguagem direta, sem juridiquês, detalhando exatamente como protegemos seus dados.

---

## 🛠️ Stack Tecnológica Completa

| Camada | Tecnologia | Descrição & Papel |
|---|---|---|
| **Frontend Hosting** | Vercel Edge Network | Hospedagem estática global com HTTPS, cache otimizado e rewrites via `vercel.json` |
| **Frontend Core** | HTML5, CSS3, JavaScript (ES6+), Chart.js | SPA responsiva sem frameworks pesados, gráficos analíticos e exportação CSV |
| **Backend Hosting** | Render Web Service | Contêiner Python gerenciado com deploy contínuo integrado ao GitHub |
| **API Framework** | FastAPI + Uvicorn | Framework assíncrono moderno com validação via Pydantic v2 e OpenAPI 3.1 |
| **ORM & Migrações** | SQLAlchemy 2.x + Alembic | Mapeamento declarativo relacional, transações ACID e 16 revisões versionadas |
| **Banco em Nuvem** | Supabase PostgreSQL / TiDB Cloud | PostgreSQL 15+ com Pooler PgBouncer porta 6543 e MySQL 8 Serverless com TLS |
| **Segurança & Crypto** | Cryptography (Fernet) + pwdlib (Argon2id) + PyJWT | Cifragem de PII (telefone), hashing resistente a GPU e tokens JWT assinados |
| **Serviço OTP (E-mail/SMS)** | HTTP Email API / SMTP STARTTLS / Twilio SMS | Envio de códigos OTP de 6 dígitos por E-mail ou SMS com fallback resiliente |
| **Suíte de Testes** | Pytest + HTTPX TestClient | Suíte automatizada cobrindo fluxos E2E, integridade contábil, OAuth 2.0, OTP e LGPD |

---

## 📁 Estrutura do Projeto

```text
fluxo_caixas/
├── .agents/
│   ├── rules/core-skills.md            # Motores ativos: Emil Kowalski + Impeccable + Taste-Skill + Ponytail
│   └── skills/                         # Skills especializadas de design engineering, animação e UI polish
├── backend/                            # Núcleo da API REST e regras de negócio
│   ├── rotasdeapi/                     # Controladores REST modulares por domínio
│   │   ├── usuario.py                  # Cadastro Zero-CPF, Google OAuth 2.0, OTP E-mail/SMS, login e perfil
│   │   ├── conta_bancaria.py           # Gestão de contas correntes, poupanças e investimentos
│   │   ├── fluxo_dinheiro.py           # Lançamentos, transferências vinculadas e aportes de investimentos
│   │   ├── calculo_financeiro.py       # Relatórios e balanços consolidados periódicos
│   │   ├── meta_financeira.py          # Metas financeiras com acompanhamento de progresso
│   │   ├── orcamentos_alertas.py       # Tetos por categoria, acompanhamento e alertas de vencimento
│   │   └── readme.md                   # Catálogo técnico de rotas, contratos e payloads
│   ├── seguranca/                      # Segurança e criptografia
│   │   ├── seguranca.py                # Hashing e validação de senhas com Argon2id
│   │   └── readme.md                   # Diretrizes de proteção de senhas
│   ├── servicos/                       # Serviços utilitários
│   │   ├── email.py                    # Envio de códigos OTP de 6 dígitos via E-mail (HTTP/SMTP) e SMS
│   │   └── google_oauth.py             # Validação de ID Token Google OAuth 2.0 (iss, aud, exp, email_verified)
│   ├── tests/                          # Suíte de testes automatizados (Pytest)
│   ├── api.py                          # Configuração do FastAPI, CORS, tradução PT-BR e healthcheck
│   ├── autenticacao.py                 # Emissão e validação de tokens JWT
│   ├── configuracao.py                 # Carregamento seguro de configurações (.env)
│   ├── dados_sensiveis.py              # Cifragem Fernet AES-128 e Blind Index HMAC
│   ├── database.py                     # Conexão SQLAlchemy normalizada (PostgreSQL/Supabase/MySQL)
│   ├── esquema.py                      # Schemas Pydantic v2 (Zero-CPF por padrão, senha forte e LGPD)
│   ├── financeiro.py                   # Motor contábil e cálculos com precisão Decimal
│   ├── models.py                       # Entidades ORM (10 tabelas mapeadas)
│   └── readme.md                       # Documentação técnica do backend
│
├── banco de dados/                     # Esquema relacional e versionamento Alembic
│   ├── migrations/                     # 16 migrações incrementais do banco
│   ├── alembic.ini                     # Arquivo de configuração Alembic
│   └── readme.md                       # Diagrama ERD e dicionário de dados
│
├── frontend/                           # Aplicação Web SPA & Landing Page (Vercel)
│   ├── assets/logo.svg                 # Logotipo vetorial corporativo oficial em SVG
│   ├── css/style.css                   # Design system financeiro responsivo + física Emil Kowalski (?v=19)
│   ├── js/                             # Módulos JS (api.js, legal.js, dashboard.js, login.js, cadastro.js)
│   ├── inicio.html                     # Landing Page de alta conversão com CTAs estratégicos
│   ├── index.html                      # Painel financeiro principal autenticado (SPA 100% vetorial SVG)
│   ├── login.html                      # Tela de login com botão Google em destaque e recuperação via OTP
│   ├── cadastro.html                   # Cadastro Zero-CPF (Nome, E-mail, Telefone e Senha) + OTP E-mail/SMS
│   ├── termos.html                     # Página dedicada dos Termos de Uso em linguagem clara
│   ├── privacidade.html                # Página dedicada da Política de Privacidade e LGPD humana
│   └── README.md                       # Guia do frontend e publicação na Vercel
│
├── scripts/                            # Scripts utilitários administrativos
├── .env.example                        # Template seguro de variáveis de ambiente
├── .gitignore                          # Regras de exclusão do Git
├── .vercelignore                       # Exclusão de arquivos backend no deploy do frontend
├── ESTRUTURA.md                        # Mapa arquitetural detalhado do sistema
├── main.py                             # Ponto de entrada unificado para execução local
├── pytest.ini                          # Configuração do executor Pytest
├── requirements.txt                    # Dependências Python fixadas
└── vercel.json                         # Roteamento, rewrites e cabeçalhos de segurança da Vercel
```

---

## 💻 Execução Local Passo a Passo

### 1. Clonar o Repositório e Criar o Ambiente Virtual

```powershell
git clone https://github.com/arthurcamrocha20052008/fluxo_caixa.git
cd fluxo_caixas
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente (`.env`)

Crie seu arquivo local a partir do modelo `.env.example`:

```powershell
Copy-Item .env.example .env
```

Gere chaves criptográficas seguras:

```powershell
# Chave para assinatura JWT
python -c "import secrets; print(secrets.token_urlsafe(48))"

# Chave Fernet para PII (Telefone e identificadores criptográficos)
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Preencha no seu arquivo `.env`:
```ini
APP_ENV=development
DATABASE_URL=postgresql+psycopg2://usuario:senha@host:6543/postgres?sslmode=require
JWT_SECRET_KEY=sua_chave_gerada_acima
CPF_ENCRYPTION_KEY=sua_chave_fernet_gerada_acima
CORS_ORIGINS=http://127.0.0.1:5500,http://127.0.0.1:5173
```

### 3. Aplicar as Migrações do Banco de Dados

Execute o Alembic para criar ou atualizar todas as tabelas:

```powershell
python -m alembic -c "banco de dados/alembic.ini" upgrade head
```

### 4. Inicializar a API FastAPI

```powershell
python main.py
```

A API estará disponível em:
- **API Local:** `http://127.0.0.1:8000`
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **Healthcheck:** `http://127.0.0.1:8000/health`

### 5. Executar o Frontend Localmente

Inicie um servidor HTTP local a partir da pasta `frontend`:

```powershell
python -m http.server 5173 --bind 127.0.0.1 --directory frontend
```

Acesse em seu navegador: [**http://127.0.0.1:5173/login.html**](http://127.0.0.1:5173/login.html).

---

## ☁️ Deploy em Nuvem (Vercel + Render + Supabase)

O fluxo de CI/CD está configurado para publicação automática a partir de commits na branch `main`:

```mermaid
flowchart LR
    GIT["GitHub (branch main)"] -->|Deploy Automático| VERCEL["Frontend (Vercel)"]
    GIT -->|Deploy Automático| RENDER["Backend (Render)"]
    RENDER -->|Pooler AWS 6543| SUPABASE[("Banco de Dados (Supabase PostgreSQL)")]
```

1. **Banco de Dados (Supabase PostgreSQL):**
   - Criação das tabelas e índices via migrações Alembic ou script [`scripts/supabase_schema_completo.sql`](scripts/supabase_schema_completo.sql).
   - Conexão configurada pelo connection pooler PgBouncer na porta `6543` com SSL obrigatório.
2. **Backend (Render Web Service):**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python -m alembic -c "banco de dados/alembic.ini" upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:** `APP_ENV=production`, `CORS_ORIGINS=https://fluxo-caixa-coral-two.vercel.app`, `DATABASE_URL`, `JWT_SECRET_KEY`, `CPF_ENCRYPTION_KEY`.
   - **Opcionais (autenticação):** `GOOGLE_CLIENT_ID`, `EMAIL_API_KEY` / `EMAIL_FROM` (Resend ou Brevo), `SMTP_SERVER` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASSWORD`, `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN` / `TWILIO_FROM_NUMBER`, `SMS_PROVIDER_URL` / `SMS_API_KEY`. Veja o [`.env.example`](.env.example).
3. **Frontend (Vercel):**
   - Publicação configurada em [`vercel.json`](vercel.json) (`outputDirectory: "frontend"`), redirecionando a raiz `/` para a Landing Page `/inicio.html`, com rewrites amigáveis (`/inicio`, `/login`, `/cadastro`, `/dashboard`, `/termos`, `/privacidade`) e cabeçalhos HTTP de segurança.

---

## 📡 Catálogo de Endpoints da API

| Módulo | Método | Rota | Descrição | Autenticação |
|---|---|---|---|---|
| **Sistema** | `GET` | `/` | Confirmação de status da API | Pública |
| **Sistema** | `GET` | `/health` | Healthcheck operacional e ambiente ativo | Pública |
| **Usuários** | `POST` | `/usuarios/` | Cadastro Zero-CPF (Nome, E-mail, Telefone, Senha Forte e LGPD) + disparo de OTP (E-mail ou SMS) | Pública |
| **Usuários** | `POST` | `/usuarios/verificar-email` | Confirmação de conta via código OTP de 6 dígitos (uso único) + emissão imediata de JWT | Pública |
| **Usuários** | `POST` | `/usuarios/confirmar-email` | Rota compatível de confirmação de conta via código OTP de 6 dígitos | Pública |
| **Usuários** | `POST` | `/usuarios/reenviar-verificacao` | Reenvio de código OTP temporário de verificação de cadastro | Pública (Rate Limited) |
| **Usuários** | `POST` | `/usuarios/enviar-codigo` | Envio/reenvio de OTP de 6 dígitos com escolha/troca de canal (`email` ou `sms`) | Pública (Rate Limited) |
| **Usuários** | `GET` | `/usuarios/auth/google/config` | Consulta disponibilidade e `client_id` público do Google OAuth 2.0 | Pública |
| **Usuários** | `POST` | `/usuarios/auth/google` | Login Social Google OAuth 2.0 (cria/vincula conta e retorna JWT) | Pública (Rate Limited) |
| **Usuários** | `POST` | `/usuarios/auth/google/assistido` | Fluxo Google assistido (Zero-CPF) quando `GOOGLE_CLIENT_ID` não está ativo | Pública (Rate Limited) |
| **Usuários** | `PUT` | `/usuarios/me/completar-cadastro` | Atualização rápida opcional de telefone pós-OAuth | Bearer JWT |
| **Usuários** | `POST` | `/login` | Autenticação OAuth2 (`username` = e-mail, `password` = senha) | Pública (Rate Limited) |
| **Usuários** | `POST` | `/usuarios/esqueci-senha` | Disparo de código OTP de recuperação por E-mail ou SMS | Pública |
| **Usuários** | `POST` | `/usuarios/redefinir-senha` | Redefinição de senha validada exclusivamente por E-mail + código OTP de 6 dígitos | Pública |
| **Usuários** | `GET` | `/usuarios/me` | Retorna dados cadastrais do usuário autenticado | Bearer JWT |
| **Usuários** | `PUT` | `/usuarios/me` | Atualiza perfil cadastral (`nome_completo`, `telefone`) | Bearer JWT |
| **Usuários** | `DELETE`| `/usuarios/me` | Exclui permanentemente a conta do usuário logado e todos os dados vinculados | Bearer JWT |
| **Contas** | `GET` | `/contas-bancarias/` | Lista contas bancárias com saldos atualizados | Bearer JWT |
| **Contas** | `POST` | `/contas-bancarias/` | Cria nova conta (`corrente`, `poupanca`, `investimento`) | Bearer JWT |
| **Contas** | `PUT` | `/contas-bancarias/{id}` | Atualiza nome, tipo ou status da conta bancária | Bearer JWT |
| **Contas** | `DELETE`| `/contas-bancarias/{id}` | Exclui conta bancária sem vínculos pendentes | Bearer JWT |
| **Fluxo** | `GET` | `/fluxo-dinheiro/` | Extrato de movimentações com filtros combinados | Bearer JWT |
| **Fluxo** | `POST` | `/fluxo-dinheiro/` | Registra entrada, saída, investimento ou transferência | Bearer JWT |
| **Fluxo** | `PUT` | `/fluxo-dinheiro/{id}` | Atualiza movimentação e recalcula saldos vinculados | Bearer JWT |
| **Fluxo** | `DELETE`| `/fluxo-dinheiro/{id}` | Exclui movimentação (ou par atômico de transferência) | Bearer JWT |
| **Orçamentos**| `GET` | `/orcamentos` | Lista orçamentos mensais e percentual de consumo | Bearer JWT |
| **Orçamentos**| `POST` | `/orcamentos` | Define teto mensal de gastos por categoria | Bearer JWT |
| **Orçamentos**| `PUT` | `/orcamentos/{id}` | Altera o limite mensal de um orçamento existente | Bearer JWT |
| **Orçamentos**| `DELETE`| `/orcamentos/{id}` | Remove teto orçamentário | Bearer JWT |
| **Alertas** | `GET` | `/alertas` | Consulta alertas de orçamentos e saídas dos próximos 7 dias | Bearer JWT |
| **Alertas** | `PUT` | `/alertas/lido` | Marca alerta específico como lido | Bearer JWT |
| **Alertas** | `GET` | `/alertas/preferencias` | Consulta preferências de notificação do usuário | Bearer JWT |
| **Alertas** | `PUT` | `/alertas/preferencias` | Atualiza preferências de notificação | Bearer JWT |
| **Cálculos** | `POST` | `/calculos-financeiros/` | Consolida e grava balanço contábil por período | Bearer JWT |
| **Cálculos** | `GET` | `/calculos-financeiros/` | Histórico de consolidações contábeis | Bearer JWT |
| **Metas** | `GET` | `/metas-financeiras/` | Lista metas de economia e percentual concluído | Bearer JWT |
| **Metas** | `POST` | `/metas-financeiras/` | Cria nova meta financeira com alvo e data | Bearer JWT |
| **Metas** | `PUT` | `/metas-financeiras/{id}` | Atualiza aportes e conclui automaticamente ao atingir alvo | Bearer JWT |
| **Metas** | `DELETE`| `/metas-financeiras/{id}` | Remove meta financeira | Bearer JWT |

---

## 🔒 Segurança & Privacidade LGPD (Zero-CPF)

- **Minimização de Dados (Zero-CPF):** Nenhuma tela de cadastro, login ou recuperação solicita CPF. Identificadores internos são derivados criptograficamente do e-mail verificado (`Fernet AES-128` + `HMAC-SHA256`), mantendo compatibilidade total com o esquema relacional sem coletar documentos desnecessários.
- **Cifragem Simétrica Fernet:** O número de telefone celular reside em repouso sob cifra AES-128 em modo CBC com integridade verificada por HMAC-SHA256.
- **Hashing de Senha Resistente a GPU:** Implementação moderna via `pwdlib` utilizando **Argon2id** (vencedor da Password Hashing Competition) e fallback Bcrypt.
- **Defesa Anti-Enumeração:** A rota de login utiliza tempo simulado caso o e-mail não exista, prevenindo enumeração de contas por análise de latência (*timing attacks*).
- **Rate Limiting em Camada de Aplicação:** Bloqueio progressivo após 5 falhas consecutivas em janela de 15 minutos com status `HTTP 429`.

---

## 🧪 Qualidade & Testes Automatizados

A aplicação conta com suíte completa de testes automatizados executada via Pytest com banco de dados SQLite em memória totalmente isolado:

```powershell
python -m pytest -q
```

---

## 📚 Documentações Complementares

- 📜 [**Histórico de Desenvolvimento e Atualizações (HISTORICO.md)**](HISTORICO.md)
- 🏛️ [**Mapa Arquitetural Completo (ESTRUTURA.md)**](ESTRUTURA.md)
- ⚙️ [**Guia do Módulo Backend**](backend/readme.md)
- 🧭 [**Catálogo Técnico de Rotas da API**](backend/rotasdeapi/readme.md)
- 🔐 [**Arquitetura de Segurança e Criptografia LGPD**](backend/seguranca/readme.md)
- 🧪 [**Manual da Suíte de Testes Automatizados**](backend/tests/README.md)
- 🗄️ [**Modelagem e Dicionário de Dados**](banco%20de%20dados/readme.md)
- 🔄 [**Manual de Migrações Alembic**](banco%20de%20dados/migrations/README.md)
- 🖥️ [**Documentação do Frontend e SPA Vercel**](frontend/README.md)
- 🛠️ [**Guia de Scripts Administrativos**](scripts/README.md)

---

<div align="center">
Desenvolvido com excelência técnica, precisão contábil, privacidade Zero-CPF e engenharia de design moderna em nuvem.
</div>
