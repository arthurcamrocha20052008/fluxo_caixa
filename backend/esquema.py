# =========================================================
# SCHEMAS DA API - SISTEMA DE FLUXO DE CAIXA
# =========================================================

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator
)

from decimal import Decimal
from datetime import date, datetime
from typing import Optional, Literal


# =========================================================
# 1. USUÁRIOS
# =========================================================
# Schema utilizado para criar um usuário.
#
# A senha será recebida pela API, mas NÃO deve ser salva
# diretamente no banco de dados.
#
# O arquivo usuario.py será responsável por transformar
# a senha em hash antes de salvar.
# =========================================================

class UsuarioCreate(BaseModel):

    nome: str = Field(
        min_length=3,
        max_length=100
    )

    email: EmailStr

    senha: str = Field(
        min_length=8,
        max_length=128
    )

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor):
        valor = valor.strip()

        if len(valor) < 3:
            raise ValueError(
                "O nome deve possuir pelo menos 3 caracteres"
            )

        return valor

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, valor):

        if not any(c.isupper() for c in valor):
            raise ValueError(
                "A senha deve possuir pelo menos uma letra maiúscula"
            )

        if not any(c.islower() for c in valor):
            raise ValueError(
                "A senha deve possuir pelo menos uma letra minúscula"
            )

        if not any(c.isdigit() for c in valor):
            raise ValueError(
                "A senha deve possuir pelo menos um número"
            )

        if not any(not c.isalnum() for c in valor):
            raise ValueError(
                "A senha deve possuir pelo menos um caractere especial"
            )

        return valor


# =========================================================
# RESPOSTA DO USUÁRIO
# =========================================================
# IMPORTANTE:
# A senha nunca aparece na resposta da API.
# =========================================================

class UsuarioResponse(BaseModel):

    id: int
    nome: str
    email: str
    criado_em: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# 2. CATEGORIAS
# =========================================================

class CategoriaCreate(BaseModel):

    nome: str = Field(
        min_length=2,
        max_length=100
    )

    tipo: Literal["entrada", "saida"]

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor):
        return valor.strip()


class CategoriaResponse(BaseModel):

    id: int
    nome: str
    tipo: str

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# 3. FLUXO MENSAL
# =========================================================

class FluxoMensalCreate(BaseModel):

    mes: int = Field(
        ge=1,
        le=12
    )

    ano: int = Field(
        ge=2000,
        le=2100
    )

    valor_original: Decimal = Field(
        default=Decimal("0.00"),
        ge=0
    )

    total_entradas: Decimal = Field(
        default=Decimal("0.00"),
        ge=0
    )

    total_contas_fixas: Decimal = Field(
        default=Decimal("0.00"),
        ge=0
    )

    total_contas_variaveis: Decimal = Field(
        default=Decimal("0.00"),
        ge=0
    )

    total_investimentos: Decimal = Field(
        default=Decimal("0.00"),
        ge=0
    )

    valor_final: Decimal = Field(
        default=Decimal("0.00")
    )


class FluxoMensalResponse(BaseModel):

    id: int
    mes: int
    ano: int
    valor_original: Decimal
    total_entradas: Decimal
    total_contas_fixas: Decimal
    total_contas_variaveis: Decimal
    total_investimentos: Decimal
    valor_final: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# 4. CONTAS FIXAS
# =========================================================

class ContaFixaCreate(BaseModel):

    nome: str = Field(
        min_length=2,
        max_length=100
    )

    valor: Decimal = Field(
        gt=0
    )

    dia_vencimento: int = Field(
        ge=1,
        le=31
    )

    categoria_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    status: Literal[
        "pendente",
        "paga",
        "atrasada"
    ] = "pendente"

    observacao: Optional[str] = Field(
        default=None,
        max_length=500
    )

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor):
        return valor.strip()


class ContaFixaResponse(BaseModel):

    id: int
    nome: str
    valor: Decimal
    dia_vencimento: int
    categoria_id: Optional[int] = None
    status: str
    observacao: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# 5. CONTAS VARIÁVEIS
# =========================================================

class ContaVariavelCreate(BaseModel):

    nome: str = Field(
        min_length=2,
        max_length=100
    )

    valor: Decimal = Field(
        gt=0
    )

    data_conta: date

    categoria_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    observacao: Optional[str] = Field(
        default=None,
        max_length=500
    )

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor):
        return valor.strip()


class ContaVariavelResponse(BaseModel):

    id: int
    nome: str
    valor: Decimal
    data_conta: date
    categoria_id: Optional[int] = None
    observacao: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# 6. INVESTIMENTOS
# =========================================================

class InvestimentoCreate(BaseModel):

    nome: str = Field(
        min_length=2,
        max_length=100
    )

    tipo: str = Field(
        min_length=2,
        max_length=50
    )

    valor: Decimal = Field(
        gt=0
    )

    data_investimento: date

    descricao: Optional[str] = Field(
        default=None,
        max_length=500
    )

    status: Literal[
        "planejado",
        "realizado"
    ] = "realizado"

    @field_validator("nome", "tipo")
    @classmethod
    def limpar_texto(cls, valor):
        return valor.strip()


class InvestimentoResponse(BaseModel):

    id: int
    nome: str
    tipo: str
    valor: Decimal
    data_investimento: date
    descricao: Optional[str] = None
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# 7. MOVIMENTAÇÕES
# =========================================================

class MovimentacaoCreate(BaseModel):

    descricao: str = Field(
        min_length=2,
        max_length=200
    )

    valor: Decimal = Field(
        gt=0
    )

    tipo: Literal[
        "entrada",
        "saida"
    ]

    data_movimentacao: date

    categoria_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    observacao: Optional[str] = Field(
        default=None,
        max_length=500
    )

    conta_bancaria_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    @field_validator("descricao")
    @classmethod
    def validar_descricao(cls, valor):
        return valor.strip()


class MovimentacaoResponse(BaseModel):

    id: int
    descricao: str
    valor: Decimal
    tipo: str
    data_movimentacao: date
    categoria_id: Optional[int] = None
    observacao: Optional[str] = None
    conta_bancaria_id: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# 8. CATEGORIAS DE INVESTIMENTO
# =========================================================

class CategoriaInvestimentoCreate(BaseModel):

    nome: str = Field(
        min_length=2,
        max_length=100
    )

    descricao: Optional[str] = Field(
        default=None,
        max_length=500
    )

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor):
        return valor.strip()


class CategoriaInvestimentoResponse(BaseModel):

    id: int
    nome: str
    descricao: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# 9. CONTAS BANCÁRIAS
# =========================================================

class ContaBancariaCreate(BaseModel):

    nome_banco: str = Field(
        min_length=2,
        max_length=100
    )

    nome_conta: str = Field(
        min_length=2,
        max_length=100
    )

    tipo_conta: Literal[
        "corrente",
        "poupanca",
        "investimento"
    ]

    saldo_atual: Decimal = Decimal("0.00")

    ativa: bool = True

    @field_validator("nome_banco", "nome_conta")
    @classmethod
    def limpar_texto(cls, valor):
        return valor.strip()


class ContaBancariaResponse(BaseModel):

    id: int
    nome_banco: str
    nome_conta: str
    tipo_conta: str
    saldo_atual: Decimal
    ativa: bool

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# 10. LANÇAMENTOS
# =========================================================

class LancamentoCreate(BaseModel):

    descricao: str = Field(
        min_length=2,
        max_length=200
    )

    tipo: Literal[
        "entrada",
        "saida"
    ]

    categoria: str = Field(
        min_length=2,
        max_length=100
    )

    valor: Decimal = Field(
        gt=0
    )

    data: date

    @field_validator("descricao", "categoria")
    @classmethod
    def limpar_texto(cls, valor):
        return valor.strip()


class LancamentoResponse(BaseModel):

    id: int
    descricao: str
    tipo: str
    categoria: str
    valor: Decimal
    data: date

    model_config = ConfigDict(
        from_attributes=True
    )