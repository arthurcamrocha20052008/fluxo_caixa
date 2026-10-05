from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Movimentacao
from esquema import MovimentacaoCreate, MovimentacaoResponse


router = APIRouter(
    prefix="/movimentacoes",
    tags=["Movimentações"]
)


# =========================================================
# CREATE
# =========================================================

@router.post(
    "/",
    response_model=MovimentacaoResponse
)
def criar_movimentacao(
    movimentacao: MovimentacaoCreate,
    db: Session = Depends(get_db)
):
    nova_movimentacao = Movimentacao(
        descricao=movimentacao.descricao,
        valor=movimentacao.valor,
        tipo=movimentacao.tipo,
        data_movimentacao=movimentacao.data_movimentacao,
        categoria_id=movimentacao.categoria_id,
        observacao=movimentacao.observacao,
        conta_bancaria_id=movimentacao.conta_bancaria_id
    )

    db.add(nova_movimentacao)
    db.commit()
    db.refresh(nova_movimentacao)

    return nova_movimentacao


# =========================================================
# READ - Listar
# =========================================================

@router.get(
    "/",
    response_model=list[MovimentacaoResponse]
)
def listar_movimentacoes(
    db: Session = Depends(get_db)
):
    return db.query(Movimentacao).all()


# =========================================================
# READ - Buscar por ID
# =========================================================

@router.get(
    "/{movimentacao_id}",
    response_model=MovimentacaoResponse
)
def buscar_movimentacao(
    movimentacao_id: int,
    db: Session = Depends(get_db)
):
    movimentacao = (
        db.query(Movimentacao)
        .filter(Movimentacao.id == movimentacao_id)
        .first()
    )

    if not movimentacao:
        raise HTTPException(
            status_code=404,
            detail="Movimentação não encontrada"
        )

    return movimentacao


# =========================================================
# UPDATE
# =========================================================

@router.put(
    "/{movimentacao_id}",
    response_model=MovimentacaoResponse
)
def atualizar_movimentacao(
    movimentacao_id: int,
    movimentacao_atualizada: MovimentacaoCreate,
    db: Session = Depends(get_db)
):
    movimentacao = (
        db.query(Movimentacao)
        .filter(Movimentacao.id == movimentacao_id)
        .first()
    )

    if not movimentacao:
        raise HTTPException(
            status_code=404,
            detail="Movimentação não encontrada"
        )

    movimentacao.descricao = movimentacao_atualizada.descricao
    movimentacao.valor = movimentacao_atualizada.valor
    movimentacao.tipo = movimentacao_atualizada.tipo
    movimentacao.data_movimentacao = movimentacao_atualizada.data_movimentacao
    movimentacao.categoria_id = movimentacao_atualizada.categoria_id
    movimentacao.observacao = movimentacao_atualizada.observacao
    movimentacao.conta_bancaria_id = movimentacao_atualizada.conta_bancaria_id

    db.commit()
    db.refresh(movimentacao)

    return movimentacao


# =========================================================
# DELETE
# =========================================================

@router.delete("/{movimentacao_id}")
def excluir_movimentacao(
    movimentacao_id: int,
    db: Session = Depends(get_db)
):
    movimentacao = (
        db.query(Movimentacao)
        .filter(Movimentacao.id == movimentacao_id)
        .first()
    )

    if not movimentacao:
        raise HTTPException(
            status_code=404,
            detail="Movimentação não encontrada"
        )

    db.delete(movimentacao)
    db.commit()

    return {
        "mensagem": "Movimentação excluída com sucesso"
    }