from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import CategoriaInvestimento
from esquema import (
    CategoriaInvestimentoCreate,
    CategoriaInvestimentoResponse
)


router = APIRouter(
    prefix="/categorias-investimento",
    tags=["Categorias de Investimento"]
)


# =========================================================
# CREATE
# =========================================================

@router.post(
    "/",
    response_model=CategoriaInvestimentoResponse
)
def criar_categoria_investimento(
    categoria: CategoriaInvestimentoCreate,
    db: Session = Depends(get_db)
):
    nova_categoria = CategoriaInvestimento(
        nome=categoria.nome,
        descricao=categoria.descricao
    )

    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)

    return nova_categoria


# =========================================================
# READ - Listar
# =========================================================

@router.get(
    "/",
    response_model=list[CategoriaInvestimentoResponse]
)
def listar_categorias_investimento(
    db: Session = Depends(get_db)
):
    return db.query(CategoriaInvestimento).all()


# =========================================================
# READ - Buscar por ID
# =========================================================

@router.get(
    "/{categoria_id}",
    response_model=CategoriaInvestimentoResponse
)
def buscar_categoria_investimento(
    categoria_id: int,
    db: Session = Depends(get_db)
):
    categoria = (
        db.query(CategoriaInvestimento)
        .filter(CategoriaInvestimento.id == categoria_id)
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria de investimento não encontrada"
        )

    return categoria


# =========================================================
# UPDATE
# =========================================================

@router.put(
    "/{categoria_id}",
    response_model=CategoriaInvestimentoResponse
)
def atualizar_categoria_investimento(
    categoria_id: int,
    categoria_atualizada: CategoriaInvestimentoCreate,
    db: Session = Depends(get_db)
):
    categoria = (
        db.query(CategoriaInvestimento)
        .filter(CategoriaInvestimento.id == categoria_id)
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria de investimento não encontrada"
        )

    categoria.nome = categoria_atualizada.nome
    categoria.descricao = categoria_atualizada.descricao

    db.commit()
    db.refresh(categoria)

    return categoria


# =========================================================
# DELETE
# =========================================================

@router.delete("/{categoria_id}")
def excluir_categoria_investimento(
    categoria_id: int,
    db: Session = Depends(get_db)
):
    categoria = (
        db.query(CategoriaInvestimento)
        .filter(CategoriaInvestimento.id == categoria_id)
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria de investimento não encontrada"
        )

    db.delete(categoria)
    db.commit()

    return {
        "mensagem": "Categoria de investimento excluída com sucesso"
    }