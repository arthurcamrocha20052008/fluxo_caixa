# 📜 Histórico de Desenvolvimento (Changelog)

Todas as mudanças notáveis, migrações de banco de dados, alterações arquiteturais e deploys deste projeto são documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/) e adere ao Versionamento Semântico.

---

## [Em Andamento] - Novembro 2026

### 🚀 Adicionado
* **Skill Global de Desenvolvimento (`dev-standards`):** Padronização de governança para microcopy de UI, documentação obrigatória no `HISTORICO.md` e alinhamento de READMEs modulares.
* **Links de Rastreabilidade nos READMEs:** Referência cruzada direta entre o [README Principal](./README.md), [Backend README](./backend/README.md) e [Frontend README](./frontend/README.md).
* **Diretrizes Globais do Antigravity:** Integração de regras globais em `~/.gemini/config/rules/global_dev_rules.md` para novos projetos herdarem o padrão.

### 🎨 Corrigido & Polimento de Interface (Microcopy)
* **Revisão de Microcopy na Interface:** Substituição de textos genéricos por ações claras e intuitivas ("Salvar Transação", "Gerar Relatório"), mensagens de erro humanizadas e placeholders com exemplos realistas (`Ex: Mercado - R$ 150,00`).
* **Micro-interações e Acessibilidade:** Validação de feedback de estados nos botões de formulário e travamento de rolagem (*scroll lock*) durante modais e popovers.

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
