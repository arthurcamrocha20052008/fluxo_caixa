from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ContaBancaria
from esquema import (
    ContaBancariaCreate,
    ContaBancariaResponse
)


router = APIRouter(
    prefix="/contas-bancarias",
    tags=["Contas Bancárias"]
)


# =========================================================
# CREATE
# =========================================================

@router.post(
    "/",
    response_model=ContaBancariaResponse
)
def criar_conta_bancaria(
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


# =========================================================
# READ - Listar
# =========================================================

@router.get(
    "/",
    response_model=list[ContaBancariaResponse]
)
def listar_contas_bancarias(
    db: Session = Depends(get_db)
):
    return db.query(ContaBancaria).all()


# =========================================================
# READ - Buscar por ID
# =========================================================

@router.get(
    "/{conta_id}",
    response_model=ContaBancariaResponse
)
def buscar_conta_bancaria(
    conta_id: int,
    db: Session = Depends(get_db)
):
    conta = (
        db.query(ContaBancaria)
        .filter(ContaBancaria.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta bancária não encontrada"
        )

    return conta


# =========================================================
# UPDATE
# =========================================================

@router.put(
    "/{conta_id}",
    response_model=ContaBancariaResponse
)
def atualizar_conta_bancaria(
    conta_id: int,
    conta_atualizada: ContaBancariaCreate,
    db: Session = Depends(get_db)
):
    conta = (
        db.query(ContaBancaria)
        .filter(ContaBancaria.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta bancária não encontrada"
        )

    conta.nome_banco = conta_atualizada.nome_banco
    conta.nome_conta = conta_atualizada.nome_conta
    conta.tipo_conta = conta_atualizada.tipo_conta
    conta.saldo_atual = conta_atualizada.saldo_atual
    conta.ativa = conta_atualizada.ativa

    db.commit()
    db.refresh(conta)

    return conta


# =========================================================
# DELETE
# =========================================================

@router.delete("/{conta_id}")
def excluir_conta_bancaria(
    conta_id: int,
    db: Session = Depends(get_db)
):
    conta = (
        db.query(ContaBancaria)
        .filter(ContaBancaria.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta bancária não encontrada"
        )

    db.delete(conta)
    db.commit()

    return {
        "mensagem": "Conta bancária excluída com sucesso"
    }