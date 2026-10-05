# 💰 Fluxo de Caixa

> Sistema de gerenciamento de finanças domésticas desenvolvido com Python, FastAPI, SQLAlchemy e MySQL.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql)](https://www.mysql.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00)](https://www.sqlalchemy.org/)
[![Git](https://img.shields.io/badge/Git-Version_Control-F05032?logo=git)](https://git-scm.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/)

---

# 📌 Sobre o projeto

O **Fluxo de Caixa** é um sistema para gerenciamento de finanças domésticas.

O projeto tem como objetivo permitir o controle e a organização das informações financeiras de uma pessoa ou família, centralizando dados como:

- Usuários;
- Categorias;
- Contas bancárias;
- Contas fixas;
- Contas variáveis;
- Lançamentos;
- Movimentações;
- Investimentos;
- Categorias de investimentos;
- Fluxo financeiro mensal.

O projeto está sendo desenvolvido de forma incremental, utilizando uma arquitetura organizada em diferentes áreas:

- 🗄️ Banco de Dados
- ⚙️ Backend
- 🔐 Segurança
- 🎨 Frontend

---

# 🎯 Objetivos

Os principais objetivos do projeto são:

- Desenvolver uma API REST utilizando Python;
- Aprender e aplicar o FastAPI;
- Criar uma conexão entre Python e MySQL;
- Utilizar SQLAlchemy como ORM;
- Trabalhar com Pydantic para validação de dados;
- Implementar operações CRUD;
- Criar documentação automática utilizando Swagger/OpenAPI;
- Organizar o backend em módulos e rotas;
- Separar as responsabilidades do projeto;
- Aplicar conceitos de segurança;
- Utilizar variáveis de ambiente;
- Utilizar Git para controle de versão;
- Hospedar o projeto no GitHub;
- Desenvolver posteriormente uma interface frontend.

---

# 🛠️ Tecnologias

| Tecnologia | Utilização |
|---|---|
| 🐍 Python | Linguagem principal |
| ⚡ FastAPI | Desenvolvimento da API REST |
| 🗄️ MySQL | Banco de dados |
| 🔗 SQLAlchemy | ORM e comunicação com o banco |
| 📋 Pydantic | Validação e schemas da API |
| 📖 Swagger / OpenAPI | Documentação e testes da API |
| 🔐 python-dotenv | Gerenciamento de variáveis de ambiente |
| 🌱 Git | Controle de versão |
| 🐙 GitHub | Hospedagem do código |
| 💻 VS Code | Ambiente de desenvolvimento |

---

# 🏗️ Estrutura do projeto

O projeto foi organizado para separar as diferentes responsabilidades do sistema.

```text
fluxo_caixas/
│
├── backend/
│   │
│   ├── rotas_api/
│   │   ├── usuario.py
│   │   ├── categoria.py
│   │   ├── fluxo_mensal.py
│   │   ├── conta_fixa.py
│   │   ├── conta_variavel.py
│   │   ├── investimento.py
│   │   ├── movimentacao.py
│   │   ├── categoria_investimento.py
│   │   ├── conta_bancaria.py
│   │   └── lancamento.py
│   │
│   ├── api.py
│   ├── database.py
│   ├── esquema.py
│   ├── models.py
│   ├── requirements.txt
│   └── README.md
│
├── banco de dados/
│   ├── bd.sql
│   └── README.md
│
├── segurança/
│   ├── seguranca.py
│   └── README.md
│
├── .gitignore
├── README.md
└── venv/
