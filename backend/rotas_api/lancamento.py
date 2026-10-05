from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Lancamento
from esquema import LancamentoCreate, LancamentoResponse


router = APIRouter(
    prefix="/lancamentos",
    tags=["Lançamentos"]
)


# =========================================================
# CREATE
# =========================================================

@router.post(
    "/",
    response_model=LancamentoResponse
)
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


# =========================================================
# READ - Listar
# =========================================================

@router.get(
    "/",
    response_model=list[LancamentoResponse]
)
def listar_lancamentos(
    db: Session = Depends(get_db)
):
    return db.query(Lancamento).all()


# =========================================================
# READ - Buscar por ID
# =========================================================

@router.get(
    "/{lancamento_id}",
    response_model=LancamentoResponse
)
def buscar_lancamento(
    lancamento_id: int,
    db: Session = Depends(get_db)
):
    lancamento = (
        db.query(Lancamento)
        .filter(Lancamento.id == lancamento_id)
        .first()
    )

    if not lancamento:
        raise HTTPException(
            status_code=404,
            detail="Lançamento não encontrado"
        )

    return lancamento


# =========================================================
# UPDATE
# =========================================================

@router.put(
    "/{lancamento_id}",
    response_model=LancamentoResponse
)
def atualizar_lancamento(
    lancamento_id: int,
    lancamento_atualizado: LancamentoCreate,
    db: Session = Depends(get_db)
):
    lancamento = (
        db.query(Lancamento)
        .filter(Lancamento.id == lancamento_id)
        .first()
    )

    if not lancamento:
        raise HTTPException(
            status_code=404,
            detail="Lançamento não encontrado"
        )

    lancamento.descricao = lancamento_atualizado.descricao
    lancamento.tipo = lancamento_atualizado.tipo
    lancamento.categoria = lancamento_atualizado.categoria
    lancamento.valor = lancamento_atualizado.valor
    lancamento.data = lancamento_atualizado.data

    db.commit()
    db.refresh(lancamento)

    return lancamento


# =========================================================
# DELETE
# =========================================================

@router.delete("/{lancamento_id}")
def excluir_lancamento(
    lancamento_id: int,
    db: Session = Depends(get_db)
):
    lancamento = (
        db.query(Lancamento)
        .filter(Lancamento.id == lancamento_id)
        .first()
    )

    if not lancamento:
        raise HTTPException(
            status_code=404,
            detail="Lançamento não encontrado"
        )

    db.delete(lancamento)
    db.commit()

    return {
        "mensagem": "Lançamento excluído com sucesso"
    }