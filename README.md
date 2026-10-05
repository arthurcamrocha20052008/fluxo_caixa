# 💰 Fluxo de Caixa

> API REST para gerenciamento de finanças domésticas, desenvolvida com Python, FastAPI, SQLAlchemy e MySQL.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00)
![Git](https://img.shields.io/badge/Git-Version_Control-F05032?logo=git)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)

---

## 📌 Sobre o projeto

O **Fluxo de Caixa** é um projeto de backend desenvolvido para praticar e aplicar conceitos de desenvolvimento de APIs, banco de dados, ORM, arquitetura backend e versionamento de código.

A aplicação tem como objetivo centralizar o controle financeiro doméstico, permitindo trabalhar com contas bancárias, lançamentos, movimentações, contas fixas, contas variáveis, investimentos, categorias e fluxo financeiro mensal.

O projeto está sendo desenvolvido de forma incremental, começando pela estrutura do banco de dados e avançando para a construção da API REST.

---

## 🎯 Objetivos

O projeto foi desenvolvido com os seguintes objetivos:

- Desenvolver uma API REST utilizando Python;
- Aprender e aplicar o FastAPI;
- Criar uma conexão entre Python e MySQL;
- Utilizar SQLAlchemy como ORM;
- Trabalhar com schemas e validação de dados;
- Implementar operações CRUD;
- Testar endpoints através do Swagger;
- Organizar um projeto backend;
- Utilizar variáveis de ambiente;
- Aplicar boas práticas de versionamento com Git;
- Publicar e manter o projeto no GitHub.

---

# 🛠️ Tecnologias

| Tecnologia | Utilização |
|---|---|
| 🐍 Python | Linguagem principal |
| ⚡ FastAPI | Desenvolvimento da API REST |
| 🗄️ MySQL | Banco de dados |
| 🔗 SQLAlchemy | ORM e comunicação com o banco |
| 📋 Pydantic | Validação e schemas |
| 📖 Swagger / OpenAPI | Documentação e testes da API |
| 🔐 python-dotenv | Gerenciamento de variáveis de ambiente |
| 🌱 Git | Controle de versão |
| 🐙 GitHub | Hospedagem do código |

---

# 🏗️ Arquitetura

O projeto utiliza uma estrutura simples de backend separando responsabilidades:

```text
                    CLIENTE
                       │
                       ▼
              ┌─────────────────┐
              │     Swagger     │
              │    /docs        │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │     FastAPI     │
              │     api.py      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Pydantic     │
              │   esquema.py    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   SQLAlchemy    │
              │    models.py    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │      MySQL      │
              │  fluxo_caixa    │
              └─────────────────┘
