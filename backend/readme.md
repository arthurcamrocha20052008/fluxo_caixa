# ⚙️ Backend — Sistema de Fluxo de Caixa

Este backend foi desenvolvido para gerenciar as operações financeiras do sistema com uma API REST em **FastAPI**. Ele conecta ao banco de dados MySQL via **SQLAlchemy** e valida os dados com **Pydantic**.

## Stack

- Python
- FastAPI
- SQLAlchemy
- MySQL
- Pydantic
- Uvicorn

## Estrutura

```text
back end/
├── api.py
├── database.py
├── models.py
├── esquema.py
├── requirements.txt
├── readme.md
└── rotas_api/
    ├── usuario.py
    ├── categoria.py
    ├── fluxomensal.py
    ├── contasfixas.py
    ├── contasvariaveis.py
    ├── investimento.py
    ├── movimentação.py
    ├── CategoriaInvestimento.py
    ├── ContaBancaria.py
    └── lancamento.py
```

## O que foi implementado

- Cadastro e gestão de usuários
- Categorias de movimentações
- Contas fixas e variáveis
- Fluxo mensal
- Investimentos
- Contas bancárias
- Movimentações financeiras
- Categorias de investimento
- Lançamentos gerais
- Separação das rotas por módulo
- Validação de dados da API

## Execução

```bash
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

A API fica disponível em:

```text
http://127.0.0.1:8000
```

Documentação interativa:

```text
http://127.0.0.1:8000/docs
```

## 🚧 Próximas etapas

- [ ] Finalizar e revisar todas as rotas CRUD
- [ ] Testar todas as rotas no Swagger
- [ ] Melhorar o tratamento de erros
- [ ] Padronizar respostas da API
- [ ] Validar melhor os dados recebidos
- [ ] Implementar autenticação de usuários
- [ ] Integrar o sistema de segurança
- [ ] Implementar login
- [ ] Implementar JWT
- [ ] Proteger as rotas
- [ ] Criar controle de acesso por usuário
- [ ] Criar documentação completa da API
- [ ] Preparar a API para integração com o Front-End
- [ ] Realizar testes da API
- [ ] Preparar o Back-End para produção