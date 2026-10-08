# Testes do backend

Esta pasta reúne testes automatizados das regras financeiras, validações e endpoints da API. `conftest.py` fornece as fixtures compartilhadas; `test_financeiro.py` contém os casos de teste.

## Cobertura existente

- agregações de entradas, saídas e investimentos e resumo do período;
- transferência entre contas, criação das duas movimentações e reversão ao excluir;
- bloqueio de saídas que deixariam saldo de poupança negativo;
- validação dos dígitos verificadores do CPF;
- correspondência entre o tipo de cálculo e o intervalo informado.
- precisão decimal e validação de categorias fixas/reservadas;
- normalização de e-mail e categorias;
- ajustes assinados fora dos totais comuns;
- login, expiração de JWT, bloqueio após falhas, isolamento entre usuários e atualização de movimentação pela API.

Os testes usam um banco SQLite temporário em memória, ativam as chaves estrangeiras e criam/removem o esquema para cada teste. Não dependem do banco MySQL de desenvolvimento.

## Executar

Na raiz do repositório:

```bash
python -m pytest -q
```

Os testes não dependem do MySQL de desenvolvimento. A validação funcional em SQLite não substitui teste de bloqueios concorrentes no MySQL: SQLite não implementa o mesmo comportamento de `SELECT ... FOR UPDATE`.
