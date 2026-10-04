from pydantic import BaseModel
from decimal import Decimal
from datetime import date


# ==============================
# CONTA BANCÁRIA
# ==============================

class ContaBancariaCreate(BaseModel):
    nome_banco: str
    nome_conta: str
    tipo_conta: str
    saldo_atual: Decimal = 0
    ativa: bool = True


class ContaBancariaResponse(BaseModel):
    id: int
    nome_banco: str
    nome_conta: str
    tipo_conta: str
    saldo_atual: Decimal
    ativa: bool

    class Config:
        from_attributes = True


# ==============================
# LANÇAMENTO
# ==============================

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

    class Config:
        from_attributes = True