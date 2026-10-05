Sim. Até agora, na parte de **Segurança**, fizemos somente o arquivo:

```text
seguranca/
└── seguranca.py
```

Então o `README.md` deve refletir **apenas o que realmente foi feito**, sem colocar arquivos que ainda não existem.

# 🔐 Segurança — Sistema de Fluxo de Caixa

Este diretório contém os recursos de segurança do **Sistema de Fluxo de Caixa**.

Atualmente, a estrutura de segurança possui o arquivo `seguranca.py`, responsável pelas funcionalidades de proteção utilizadas pelo sistema.

---

## 📁 Estrutura atual

```text
seguranca/
│
├── seguranca.py
│
└── README.md
```

---

## 🔐 `seguranca.py`

O arquivo `seguranca.py` concentra as funcionalidades relacionadas à segurança da aplicação.

Entre as responsabilidades planejadas e implementadas nessa etapa estão:

* 🔑 Tratamento seguro de senhas
* 🔒 Geração de hash para senhas
* 🛡️ Verificação de senhas
* ⚙️ Funções auxiliares relacionadas à segurança

A ideia é evitar que a senha original do usuário seja armazenada diretamente no banco de dados.

---

## 👤 Segurança dos usuários

O sistema possui uma tabela `usuarios` com o campo:

```python
senha_hash
```

Em vez de armazenar diretamente:

```text
senha = "MinhaSenha123"
```

o sistema trabalha com uma representação protegida da senha:

```text
senha → hash → senha_hash
```

Assim, a senha original não deve ser armazenada diretamente no banco.

---

## 🔒 Validação de senha

O cadastro de usuário possui validação através do Pydantic.

Atualmente, o schema define:

```python
senha: str = Field(
    min_length=8,
    max_length=128
)
```

Isso estabelece:

* mínimo de **8 caracteres**
* máximo de **128 caracteres**

---

## 🚫 Proteção da senha na API

O `UsuarioResponse` não possui o campo `senha` nem `senha_hash`.

Exemplo:

```python
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    criado_em: Optional[datetime] = None
```

Portanto, a senha não deve aparecer na resposta da API.

---

## 🏗️ Estrutura atual do projeto

A segurança faz parte da arquitetura geral:

```text
fluxo_caixas/
│
├── banco_de_dados/
│
├── back_end/
│
├── seguranca/
│   ├── seguranca.py
│   └── README.md
│
├── front_end/
│
└── README.md
```

---

## 🚧 Próximas etapas

A segurança ainda será expandida futuramente com recursos como:

```text
- [ ] Login
- [ ] JWT
- [ ] Autenticação
- [ ] Autorização
- [ ] Proteção das rotas
- [ ] Controle de acesso por usuário
- [ ] Finalizar o sistema de hash das senhas
- [ ] Implementar verificação de senha
- [ ] Criar sistema de login
- [ ] Implementar autenticação
- [ ] Implementar JWT
- [ ] Proteger as rotas da API
- [ ] Implementar autorização de usuários
- [ ] Controlar acesso aos dados de cada usuário
- [ ] Melhorar as validações de segurança
- [ ] Configurar CORS corretamente
- [ ] Criar tratamento seguro de erros
- [ ] Revisar variáveis de ambiente
- [ ] Preparar a segurança para produção