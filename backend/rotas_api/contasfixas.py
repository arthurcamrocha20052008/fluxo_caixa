from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ContaFixa
from esquema import ContaFixaCreate, ContaFixaResponse


router = APIRouter(
    prefix="/contas-fixas",
    tags=["Contas Fixas"]
)


# =========================================================
# CREATE
# =========================================================

@router.post(
    "/",
    response_model=ContaFixaResponse
)
def criar_conta_fixa(
    conta: ContaFixaCreate,
    db: Session = Depends(get_db)
):
    nova_conta = ContaFixa(
        nome=conta.nome,
        valor=conta.valor,
        dia_vencimento=conta.dia_vencimento,
        categoria_id=conta.categoria_id,
        status=conta.status,
        observacao=conta.observacao
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
    response_model=list[ContaFixaResponse]
)
def listar_contas_fixas(
    db: Session = Depends(get_db)
):
    return db.query(ContaFixa).all()


# =========================================================
# READ - Buscar por ID
# =========================================================

@router.get(
    "/{conta_id}",
    response_model=ContaFixaResponse
)
def buscar_conta_fixa(
    conta_id: int,
    db: Session = Depends(get_db)
):
    conta = (
        db.query(ContaFixa)
        .filter(ContaFixa.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta fixa não encontrada"
        )

    return conta


# =========================================================
# UPDATE
# =========================================================

@router.put(
    "/{conta_id}",
    response_model=ContaFixaResponse
)
def atualizar_conta_fixa(
    conta_id: int,
    conta_atualizada: ContaFixaCreate,
    db: Session = Depends(get_db)
):
    conta = (
        db.query(ContaFixa)
        .filter(ContaFixa.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta fixa não encontrada"
        )

    conta.nome = conta_atualizada.nome
    conta.valor = conta_atualizada.valor
    conta.dia_vencimento = conta_atualizada.dia_vencimento
    conta.categoria_id = conta_atualizada.categoria_id
    conta.status = conta_atualizada.status
    conta.observacao = conta_atualizada.observacao

    db.commit()
    db.refresh(conta)

    return conta


# =========================================================
# DELETE
# =========================================================

@router.delete("/{conta_id}")
def excluir_conta_fixa(
    conta_id: int,
    db: Session = Depends(get_db)
):
    conta = (
        db.query(ContaFixa)
        .filter(ContaFixa.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta fixa não encontrada"
        )

    db.delete(conta)
    db.commit()

    return {
        "mensagem": "Conta fixa excluída com sucesso"
    }