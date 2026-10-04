from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date
from database import Base


class ContaBancaria(Base):
    __tablename__ = "contas_bancarias"

    id = Column(Integer, primary_key=True, index=True)
    nome_banco = Column(String(100), nullable=False)
    nome_conta = Column(String(100), nullable=False)
    tipo_conta = Column(String(20), nullable=False)
    saldo_atual = Column(Numeric(12, 2), default=0.00)
    ativa = Column(Boolean, default=True)


class Lancamento(Base):
    __tablename__ = "lancamentos"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(200), nullable=False)
    tipo = Column(String(20), nullable=False)
    categoria = Column(String(100), nullable=False)
    valor = Column(Numeric(12, 2), nullable=False)
    data = Column(Date, nullable=False)