from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import date, datetime
from typing import Optional


# =========================================================
# 1. USUÁRIOS
# =========================================================
# Schema utilizado para receber os dados de um novo usuário.
#
# Não colocamos "id" nem "criado_em" aqui porque esses campos
# são gerados automaticamente pelo banco de dados.
# =========================================================

class UsuarioCreate(BaseModel):

    nome: str

    email: str

    senha: str


# Schema utilizado para devolver um usuário pela API.
# A senha NÃO é devolvida na resposta.

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
# Exemplo:
#
# {
#     "nome": "Salário",
#     "tipo": "entrada"
# }
#
# O tipo pode ser:
# entrada
# saida
# =========================================================

class CategoriaCreate(BaseModel):

    nome: str

    tipo: str


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
# Representa o resumo financeiro de um determinado mês.
#
# Exemplo:
#
# mês: 10
# ano: 2026
# valor_original: 5000
# total_entradas: 3000
# total_contas_fixas: 1000
# total_contas_variaveis: 500
# total_investimentos: 500
# valor_final: 6000
# =========================================================

class FluxoMensalCreate(BaseModel):

    mes: int

    ano: int

    valor_original: Decimal = Decimal("0.00")

    total_entradas: Decimal = Decimal("0.00")

    total_contas_fixas: Decimal = Decimal("0.00")

    total_contas_variaveis: Decimal = Decimal("0.00")

    total_investimentos: Decimal = Decimal("0.00")

    valor_final: Decimal = Decimal("0.00")


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
# Exemplos:
#
# Aluguel
# Internet
# Energia
# Mensalidade
#
# status:
# pendente
# paga
# atrasada
# =========================================================

class ContaFixaCreate(BaseModel):

    nome: str

    valor: Decimal

    dia_vencimento: int

    categoria_id: Optional[int] = None

    status: str = "pendente"

    observacao: Optional[str] = None


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
# Exemplos:
#
# Mercado
# Restaurante
# Transporte
# Compras
# =========================================================

class ContaVariavelCreate(BaseModel):

    nome: str

    valor: Decimal

    data_conta: date

    categoria_id: Optional[int] = None

    observacao: Optional[str] = None


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
# Exemplos:
#
# CDB
# Tesouro Direto
# Ações
# Fundos
#
# status:
# planejado
# realizado
# =========================================================

class InvestimentoCreate(BaseModel):

    nome: str

    tipo: str

    valor: Decimal

    data_investimento: date

    descricao: Optional[str] = None

    status: str = "realizado"


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
# Representa uma movimentação financeira relacionada a uma
# categoria e, opcionalmente, a uma conta bancária.
#
# Exemplo:
#
# {
#     "descricao": "Salário",
#     "valor": 3000,
#     "tipo": "entrada",
#     "data_movimentacao": "2026-10-05",
#     "categoria_id": 1,
#     "observacao": "Salário mensal",
#     "conta_bancaria_id": 1
# }
# =========================================================

class MovimentacaoCreate(BaseModel):

    descricao: str

    valor: Decimal

    tipo: str

    data_movimentacao: date

    categoria_id: Optional[int] = None

    observacao: Optional[str] = None

    conta_bancaria_id: Optional[int] = None


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
# Exemplos:
#
# Renda Fixa
# Ações
# Fundos
# Criptomoedas
# =========================================================

class CategoriaInvestimentoCreate(BaseModel):

    nome: str

    descricao: Optional[str] = None


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
# Exemplos:
#
# Nubank
# Itaú
# Banco do Brasil
# Caixa
#
# tipo_conta:
# corrente
# poupanca
# investimento
# =========================================================

class ContaBancariaCreate(BaseModel):

    nome_banco: str

    nome_conta: str

    tipo_conta: str

    saldo_atual: Decimal = Decimal("0.00")

    ativa: bool = True


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
# Mantemos esta tabela separada de "movimentacoes" porque
# as duas existem no seu banco de dados.
#
# Campos da tabela lancamentos:
#
# descricao
# tipo
# categoria
# valor
# data
# =========================================================

class LancamentoCreate(BaseModel):

    descricao: str

    tipo: str

    categoria: str

    valor: Decimal

    data: date


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