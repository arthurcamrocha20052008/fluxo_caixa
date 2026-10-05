# 🗄️ Banco de Dados — Fluxo de Caixa

Este diretório reúne o banco do sistema em **MySQL**. O objetivo é armazenar e relacionar dados financeiros do usuário, como contas, movimentações, investimentos e resumo mensal.

## Banco

```sql
financas_casa
```

## Tecnologias

- MySQL 8+
- SQL
- SQLAlchemy
- Python
- FastAPI

## Tabelas principais

| Tabela | Finalidade |
| --- | --- |
| `usuarios` | Usuários do sistema |
| `categorias` | Categorias de entrada/saída |
| `contas_bancarias` | Contas do usuário |
| `movimentacoes` | Receitas e despesas |
| `contas_fixas` | Despesas recorrentes |
| `contas_variaveis` | Despesas variáveis |
| `investimentos` | Investimentos realizados/planejados |
| `categorias_investimento` | Tipos de investimento |
| `fluxo_mensal` | Resumo mensal de caixa |
| `lancamentos` | Lançamentos gerais |

## Fluxo principal

```text
usuarios
  ↓
contas_bancarias
  ↓
movimentacoes
  ↓
categorias
  ↓
fluxo_mensal
```

Para investimentos:

```text
usuarios
  ↓
categorias_investimento
  ↓
investimentos
  ↓
fluxo_mensal
```

## Regras e segurança

- Senhas armazenadas com hash
- Campos obrigatórios e validações
- Chaves primárias e estrangeiras
- E-mail único
- Separação entre frontend, backend e banco

## Estrutura do diretório

```text
banco de dados/
├── README.md
└── banco.sql
```

## Objetivo

O banco permite registrar, consultar e controlar:

- usuários
- contas bancárias
- receitas e despesas
- despesas fixas e variáveis
- investimentos
- categorias
- fluxo financeiro mensal

Essa estrutura suporta relatórios e dashboards do sistema.

## 🚧 Próximas etapas

- [ ] Revisar e padronizar os relacionamentos entre as tabelas
- [ ] Criar/ajustar as chaves estrangeiras
- [ ] Criar índices necessários
- [ ] Definir regras de integridade dos dados
- [ ] Criar dados iniciais para testes
- [ ] Testar todas as tabelas através do Back-End
- [ ] Fazer backup e restauração do banco
- [ ] Documentar completamente o banco de dados
- [ ] Preparar o banco para produção