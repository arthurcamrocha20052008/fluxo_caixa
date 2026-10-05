from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Enum,
    UniqueConstraint,
    text,
)

from database import Base


# =========================================================
# 1. USUÁRIOS
# =========================================================
# Tabela: usuarios
#
# Guarda os usuários que utilizarão o sistema.
#
# Exemplo:
# nome  -> Arthur
# email -> arthur@email.com
# senha -> senha do usuário
# =========================================================

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )
    senha_hash = Column(
        String(255), 
        nullable=False)

    
    criado_em = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )


# =========================================================
# 2. CATEGORIAS
# =========================================================
# Tabela: categorias
#
# Organiza as entradas e saídas financeiras.
#
# Exemplos:
# Salário      -> entrada
# Alimentação  -> saida
# Transporte   -> saida
# =========================================================

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(100),
        nullable=False
    )

    tipo = Column(
        Enum(
            "entrada",
            "saida"
        ),
        nullable=False
    )


# =========================================================
# 3. FLUXO MENSAL
# =========================================================
# Tabela: fluxo_mensal
#
# Guarda o resumo financeiro de cada mês.
#
# Exemplo:
#
# Valor original       = dinheiro no início do mês
# Total entradas       = dinheiro que entrou
# Contas fixas         = gastos fixos
# Contas variáveis     = gastos variáveis
# Investimentos        = dinheiro investido
# Valor final          = saldo final
# =========================================================

class FluxoMensal(Base):
    __tablename__ = "fluxo_mensal"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    mes = Column(
        Integer,
        nullable=False
    )

    ano = Column(
        Integer,
        nullable=False
    )

    valor_original = Column(
        Numeric(12, 2),
        nullable=False,
        default=0.00
    )

    total_entradas = Column(
        Numeric(12, 2),
        nullable=False,
        default=0.00
    )

    total_contas_fixas = Column(
        Numeric(12, 2),
        nullable=False,
        default=0.00
    )

    total_contas_variaveis = Column(
        Numeric(12, 2),
        nullable=False,
        default=0.00
    )

    total_investimentos = Column(
        Numeric(12, 2),
        nullable=False,
        default=0.00
    )

    valor_final = Column(
        Numeric(12, 2),
        nullable=False,
        default=0.00
    )

    # Impede dois registros para o mesmo mês e ano.
    __table_args__ = (
        UniqueConstraint(
            "mes",
            "ano",
            name="uq_fluxo_mensal_mes_ano"
        ),
    )


# =========================================================
# 4. CONTAS FIXAS
# =========================================================
# Tabela: contas_fixas
#
# Representa despesas que normalmente se repetem.
#
# Exemplos:
# - Aluguel
# - Internet
# - Energia
# - Mensalidade
# =========================================================

class ContaFixa(Base):
    __tablename__ = "contas_fixas"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(150),
        nullable=False
    )

    valor = Column(
        Numeric(12, 2),
        nullable=False
    )

    dia_vencimento = Column(
        Integer,
        nullable=False
    )

    categoria_id = Column(
        Integer,
        ForeignKey("categorias.id")
    )

    status = Column(
        Enum(
            "pendente",
            "paga",
            "atrasada"
        ),
        default="pendente"
    )

    observacao = Column(
        String(255)
    )


# =========================================================
# 5. CONTAS VARIÁVEIS
# =========================================================
# Tabela: contas_variaveis
#
# Representa despesas que podem variar.
#
# Exemplos:
# - Mercado
# - Restaurante
# - Transporte
# - Compras
# =========================================================

class ContaVariavel(Base):
    __tablename__ = "contas_variaveis"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(150),
        nullable=False
    )

    valor = Column(
        Numeric(12, 2),
        nullable=False
    )

    data_conta = Column(
        Date,
        nullable=False
    )

    categoria_id = Column(
        Integer,
        ForeignKey("categorias.id")
    )

    observacao = Column(
        String(255)
    )


# =========================================================
# 6. INVESTIMENTOS
# =========================================================
# Tabela: investimentos
#
# Guarda os investimentos realizados ou planejados.
#
# Exemplos:
# - CDB
# - Tesouro Direto
# - Ações
# - Fundos
# =========================================================

class Investimento(Base):
    __tablename__ = "investimentos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(100),
        nullable=False
    )

    tipo = Column(
        String(50),
        nullable=False
    )

    valor = Column(
        Numeric(12, 2),
        nullable=False
    )

    data_investimento = Column(
        Date,
        nullable=False
    )

    descricao = Column(
        String(255)
    )

    status = Column(
        Enum(
            "planejado",
            "realizado"
        ),
        default="realizado"
    )


# =========================================================
# 7. MOVIMENTAÇÕES
# =========================================================
# Tabela: movimentacoes
#
# Registra movimentações financeiras vinculadas a:
# - categorias
# - contas bancárias
#
# Exemplos:
# Salário recebido
# Compra no mercado
# Pagamento de uma conta
# =========================================================

class Movimentacao(Base):
    __tablename__ = "movimentacoes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    descricao = Column(
        String(200),
        nullable=False
    )

    valor = Column(
        Numeric(12, 2),
        nullable=False
    )

    tipo = Column(
        Enum(
            "entrada",
            "saida"
        ),
        nullable=False
    )

    data_movimentacao = Column(
        Date,
        nullable=False
    )

    categoria_id = Column(
        Integer,
        ForeignKey("categorias.id")
    )

    observacao = Column(
        String(255)
    )

    # Identifica em qual conta bancária
    # ocorreu a movimentação.
    conta_bancaria_id = Column(
        Integer,
        ForeignKey("contas_bancarias.id")
    )


# =========================================================
# 8. CATEGORIAS DE INVESTIMENTO
# =========================================================
# Tabela: categorias_investimento
#
# Organiza os tipos de investimentos.
#
# Exemplos:
# - Renda Fixa
# - Ações
# - Fundos
# =========================================================

class CategoriaInvestimento(Base):
    __tablename__ = "categorias_investimento"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(
        String(100),
        unique=True,
        nullable=False
    )

    descricao = Column(
        String(255)
    )


# =========================================================
# 9. CONTAS BANCÁRIAS
# =========================================================
# Tabela: contas_bancarias
#
# Guarda as contas bancárias utilizadas pelo usuário.
#
# Exemplos:
# - Nubank
# - Itaú
# - Banco do Brasil
# - Caixa
# =========================================================

class ContaBancaria(Base):
    __tablename__ = "contas_bancarias"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome_banco = Column(
        String(100),
        nullable=False
    )

    nome_conta = Column(
        String(100),
        nullable=False
    )

    tipo_conta = Column(
        Enum(
            "corrente",
            "poupanca",
            "investimento"
        ),
        nullable=False
    )

    saldo_atual = Column(
        Numeric(12, 2),
        nullable=False,
        default=0.00
    )

    ativa = Column(
        Boolean,
        default=True
    )


# =========================================================
# 10. LANÇAMENTOS
# =========================================================
# Tabela: lancamentos
#
# Esta tabela é diferente de "movimentacoes".
#
# Como ela existe no seu banco, vamos mantê-la no projeto.
#
# Campos:
# - descricao
# - tipo
# - categoria
# - valor
# - data
# =========================================================

class Lancamento(Base):
    __tablename__ = "lancamentos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    descricao = Column(
        String(200),
        nullable=False
    )

    tipo = Column(
        String(20),
        nullable=False
    )

    categoria = Column(
        String(100),
        nullable=False
    )

    valor = Column(
        Numeric(12, 2),
        nullable=False
    )

    data = Column(
        Date,
        nullable=False
    )