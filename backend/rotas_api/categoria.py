# =========================================================
# ROTAS DE CATEGORIAS
# =========================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Categoria
from esquema import CategoriaCreate, CategoriaResponse


# =========================================================
# CONFIGURAÇÃO DO ROUTER
# =========================================================

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)


# =========================================================
# CREATE
# Criar categoria
# =========================================================

@router.post(
    "",
    response_model=CategoriaResponse,
    status_code=201
)
def criar_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Verifica se já existe uma categoria com o mesmo nome
    # e tipo
    # -----------------------------------------------------

    categoria_existente = (
        db.query(Categoria)
        .filter(
            Categoria.nome == categoria.nome,
            Categoria.tipo == categoria.tipo
        )
        .first()
    )

    if categoria_existente:
        raise HTTPException(
            status_code=409,
            detail="Essa categoria já existe"
        )

    # -----------------------------------------------------
    # Criar categoria
    # -----------------------------------------------------

    nova_categoria = Categoria(
        nome=categoria.nome,
        tipo=categoria.tipo
    )

    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)

    return nova_categoria


# =========================================================
# READ
# Listar todas as categorias
# =========================================================

@router.get(
    "",
    response_model=list[CategoriaResponse]
)
def listar_categorias(
    db: Session = Depends(get_db)
):

    categorias = (
        db.query(Categoria)
        .order_by(Categoria.id.asc())
        .all()
    )

    return categorias


# =========================================================
# READ
# Buscar categoria por ID
# =========================================================

@router.get(
    "/{categoria_id}",
    response_model=CategoriaResponse
)
def buscar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):

    categoria = (
        db.query(Categoria)
        .filter(
            Categoria.id == categoria_id
        )
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    return categoria


# =========================================================
# UPDATE
# Atualizar categoria
# =========================================================

@router.put(
    "/{categoria_id}",
    response_model=CategoriaResponse
)
def atualizar_categoria(
    categoria_id: int,
    categoria_atualizada: CategoriaCreate,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Procurar categoria
    # -----------------------------------------------------

    categoria = (
        db.query(Categoria)
        .filter(
            Categoria.id == categoria_id
        )
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    # -----------------------------------------------------
    # Verificar duplicidade
    # -----------------------------------------------------

    categoria_existente = (
        db.query(Categoria)
        .filter(
            Categoria.nome == categoria_atualizada.nome,
            Categoria.tipo == categoria_atualizada.tipo,
            Categoria.id != categoria_id
        )
        .first()
    )

    if categoria_existente:
        raise HTTPException(
            status_code=409,
            detail="Já existe outra categoria com esse nome e tipo"
        )

    # -----------------------------------------------------
    # Atualizar
    # -----------------------------------------------------

    categoria.nome = categoria_atualizada.nome
    categoria.tipo = categoria_atualizada.tipo

    db.commit()
    db.refresh(categoria)

    return categoria


# =========================================================
# DELETE
# Excluir categoria
# =========================================================

@router.delete(
    "/{categoria_id}"
)
def excluir_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # Procurar categoria
    # -----------------------------------------------------

    categoria = (
        db.query(Categoria)
        .filter(
            Categoria.id == categoria_id
        )
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    # -----------------------------------------------------
    # Excluir
    # -----------------------------------------------------

    db.delete(categoria)
    db.commit()

    return {
        "mensagem": "Categoria excluída com sucesso"
    }