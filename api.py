from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import get_db, Base, engine
from models import ContaBancaria, Lancamento
from esquema import (
    ContaBancariaCreate,
    ContaBancariaResponse,
    LancamentoCreate,
    LancamentoResponse
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Fluxo de Caixa",
    description="API para controle de finanças domésticas",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "mensagem": "Sistema de Fluxo de Caixa funcionando!"
    }


@app.get("/teste")
def teste():
    return {
        "status": "OK",
        "projeto": "Fluxo de Caixa"
    }


@app.post("/contas-bancarias", response_model=ContaBancariaResponse)
def criar_conta(
    conta: ContaBancariaCreate,
    db: Session = Depends(get_db)
):
    nova_conta = ContaBancaria(
        nome_banco=conta.nome_banco,
        nome_conta=conta.nome_conta,
        tipo_conta=conta.tipo_conta,
        saldo_atual=conta.saldo_atual,
        ativa=conta.ativa
    )

    db.add(nova_conta)
    db.commit()
    db.refresh(nova_conta)

    return nova_conta

@app.post("/lancamentos", response_model=LancamentoResponse)
def criar_lancamento(
    lancamento: LancamentoCreate,
    db: Session = Depends(get_db)
):
    novo_lancamento = Lancamento(
        descricao=lancamento.descricao,
        tipo=lancamento.tipo,
        categoria=lancamento.categoria,
        valor=lancamento.valor,
        data=lancamento.data
    )

    db.add(novo_lancamento)
    db.commit()
    db.refresh(novo_lancamento)

    return novo_lancamento