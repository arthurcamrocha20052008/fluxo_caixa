# 💰 Sistema de Fluxo de Caixa

API para controle de finanças domésticas desenvolvida em Python utilizando FastAPI, SQLAlchemy e MySQL.

O projeto tem como objetivo criar um sistema capaz de cadastrar contas bancárias e registrar movimentações financeiras, servindo como base para um sistema completo de fluxo de caixa.

---

## 📌 Sobre o projeto

O Sistema de Fluxo de Caixa foi desenvolvido como um projeto prático para aplicar conceitos de:

- Desenvolvimento de APIs
- Python
- Banco de dados
- Programação orientada a objetos
- ORM
- Validação de dados
- Versionamento com Git e GitHub

Atualmente, o projeto já possui integração entre a API desenvolvida em Python e um banco de dados MySQL.

---

## 🚀 Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| 🐍 Python | Linguagem principal |
| ⚡ FastAPI | Framework para desenvolvimento da API |
| 🗄️ MySQL | Banco de dados |
| 🔗 SQLAlchemy | ORM e comunicação com o banco |
| ✅ Pydantic | Validação dos dados |
| 🚀 Uvicorn | Servidor da aplicação |
| 🔐 python-dotenv | Gerenciamento de variáveis de ambiente |
| 📚 Swagger/OpenAPI | Documentação e testes da API |
| 🔧 Git | Controle de versão |
| ☁️ GitHub | Hospedagem do código |

---

## 🏗️ Arquitetura

O projeto atualmente segue o seguinte fluxo:

```text
                USUÁRIO
                   │
                   ▼
              Swagger/API
                   │
                   ▼
               FastAPI
                   │
                   ▼
              Pydantic
                   │
                   ▼
              SQLAlchemy
                   │
                   ▼
                MySQL
