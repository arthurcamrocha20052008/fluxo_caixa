# 📜 Histórico de Desenvolvimento (Changelog)

Todas as mudanças notáveis, migrações de banco de dados, alterações arquiteturais e deploys deste projeto são documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/) e adere ao Versionamento Semântico.

---

## [Em Andamento] - Novembro 2026

### 🚀 Adicionado & Infraestrutura
* **Correção Definitiva de Boot no Railway (`502 Bad Gateway`):** Substituição do comando shell no `Procfile` por `web: python main.py`, adição de `railway.json` e `nixpacks.toml` explícitos com `healthcheckPath = "/health"`, variáveis seguras de fallback (`APP_ENV`, `CORS_ORIGINS`, `DATABASE_URL`, `CPF_ENCRYPTION_KEY`, `JWT_SECRET_KEY`), inicialização de esquema em background thread e escuta simultânea nas portas `{PORT, 8000, 8080}` em `0.0.0.0`.
* **Failover Inteligente na API Frontend (`api.js`):** Limpeza automática de URLs legadas no `localStorage`, conexão primária com `https://fluxocaixa-production-95d3afc7.up.railway.app` e fallback transparente de alta disponibilidade.
* **Correção de Esquema no Supabase PostgreSQL (`usuarios.cpf`) e Resiliência de Descriptografia:** Sincronização da coluna `cpf` na tabela `usuarios` do Supabase via `garantir_esquema_banco()`, tratamento tolerante de `telefone` cifrado com chaves anteriores em `UsuarioResponse` e adição de handler global de exceções HTTP 500 com preservação de cabeçalhos CORS em `backend/api.py`.
* **Página Dedicada "Continuar com o Google" (`google-auth.html`):** Ao clicar no botão do Google no Login ou Cadastro, o usuário é direcionado imediatamente para a página dedicada `google-auth.html` ("Fazer login com o Google / Escolha uma conta para prosseguir para Fluxo de Caixa") integrada à rota `POST /usuarios/auth/google/assistido` e `GET /usuarios/auth/google/url`.
* **Invalidação de Cache na Vercel (`?v=21` e `vercel.json`):** Atualização de versão de todos os assets CSS/JS para `?v=21` e ajuste de `Cache-Control` para `public, max-age=0, must-revalidate` para garantir entrega imediata das atualizações.
* **Skill Global de Desenvolvimento (`dev-standards`):** Padronização de governança para microcopy de UI, documentação obrigatória no `HISTORICO.md` e alinhamento de READMEs modulares.
* **Links de Rastreabilidade nos READMEs:** Referência cruzada direta entre o [README Principal](./README.md), [Backend README](./backend/readme.md) e [Frontend README](./frontend/readme.md).

### 🎨 Corrigido & Polimento Editorial de Interface
* **Remoção de Jargões Técnicos ("Segurança, OAuth2, Fernet"):** Substituição de explicações técnicas sobre como o site foi construído na Landing Page (`inicio.html`), Login (`login.html`), Cadastro (`cadastro.html`) e README principal por explicações claras sobre o que o sistema faz na prática (controle de contas, receitas/despesas, metas de gastos por categoria, investimentos, alertas de vencimento e relatórios CSV).
* **Microcopy de Ações Claras:** Refinamento dos botões de ação e filtros em todo o painel financeiro.

---

## [1.0.0] - Outubro 2026

### 🚀 Adicionado
* **Arquitetura Full-Stack Corporativa:** Backend construído com **FastAPI** e frontend rápido e sem frameworks pesados em **HTML5 Semântico, CSS3 Moderno, JavaScript Vanilla (ES6+)** e **Chart.js**.
* **Banco de Dados Relacional Híbrido:** Suporte nativo e testado para **Supabase (PostgreSQL 15+ com PgBouncer e SSL obrigatório)** e **TiDB Cloud Serverless (MySQL 8 com TLS nativo)**.
* **Migrações com Alembic:** 16 revisões versionadas e aplicáveis de forma reproduzível.
* **Segurança e Privacidade Zero-CPF (LGPD):** Cifragem simétrica com **Fernet (AES-128-CBC + HMAC-SHA256)** para dados sensíveis, blind index HMAC-SHA256 para unicidade e hashing de senhas moderno com **Argon2id** (`pwdlib`).
* **Autenticação Avançada & 2FA:** Suporte a Login Social via Google OAuth 2.0 e verificação multi-canal em dois fatores (OTP via E-mail com STARTTLS e SMS).
* **Motor Contábil de Alta Precisão:** Aritmética financeira exata via `Decimal(12, 2)`, conciliação bancária, débitos atômicos de investimentos e travas de concorrência (`SELECT ... FOR UPDATE`).
* **Deploys Contínuos em Nuvem:**
  * **Frontend:** Publicação na Vercel Edge Network com headers de segurança e roteamento otimizado (`vercel.json`).
  * **Backend:** Publicação no Render com automação via `render.yaml` e Uvicorn.
* **Suíte de Testes Automatizados:** 110 testes automatizados cobrindo autenticação, integridade contábil, segurança LGPD e tratamento de erros via **Pytest**.
