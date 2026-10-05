from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Investimento
from esquema import InvestimentoCreate, InvestimentoResponse


router = APIRouter(
    prefix="/investimentos",
    tags=["Investimentos"]
)


# =========================================================
# CREATE
# =========================================================

@router.post(
    "/",
    response_model=InvestimentoResponse
)
def criar_investimento(
    investimento: InvestimentoCreate,
    db: Session = Depends(get_db)
):
    novo_investimento = Investimento(
        nome=investimento.nome,
        tipo=investimento.tipo,
        valor=investimento.valor,
        data_investimento=investimento.data_investimento,
        descricao=investimento.descricao,
        status=investimento.status
    )

    db.add(novo_investimento)
    db.commit()
    db.refresh(novo_investimento)

    return novo_investimento


# =========================================================
# READ - Listar
# =========================================================

@router.get(
    "/",
    response_model=list[InvestimentoResponse]
)
def listar_investimentos(
    db: Session = Depends(get_db)
):
    return db.query(Investimento).all()


# =========================================================
# READ - Buscar por ID
# =========================================================

@router.get(
    "/{investimento_id}",
    response_model=InvestimentoResponse
)
def buscar_investimento(
    investimento_id: int,
    db: Session = Depends(get_db)
):
    investimento = (
        db.query(Investimento)
        .filter(Investimento.id == investimento_id)
        .first()
    )

    if not investimento:
        raise HTTPException(
            status_code=404,
            detail="Investimento não encontrado"
        )

    return investimento


# =========================================================
# UPDATE
# =========================================================

@router.put(
    "/{investimento_id}",
    response_model=InvestimentoResponse
)
def atualizar_investimento(
    investimento_id: int,
    investimento_atualizado: InvestimentoCreate,
    db: Session = Depends(get_db)
):
    investimento = (
        db.query(Investimento)
        .filter(Investimento.id == investimento_id)
        .first()
    )

    if not investimento:
        raise HTTPException(
            status_code=404,
            detail="Investimento não encontrado"
        )

    investimento.nome = investimento_atualizado.nome
    investimento.tipo = investimento_atualizado.tipo
    investimento.valor = investimento_atualizado.valor
    investimento.data_investimento = investimento_atualizado.data_investimento
    investimento.descricao = investimento_atualizado.descricao
    investimento.status = investimento_atualizado.status

    db.commit()
    db.refresh(investimento)

    return investimento


# =========================================================
# DELETE
# =========================================================

@router.delete("/{investimento_id}")
def excluir_investimento(
    investimento_id: int,
    db: Session = Depends(get_db)
):
    investimento = (
        db.query(Investimento)
        .filter(Investimento.id == investimento_id)
        .first()
    )

    if not investimento:
        raise HTTPException(
            status_code=404,
            detail="Investimento não encontrado"
        )

    db.delete(investimento)
    db.commit()

    return {
        "mensagem": "Investimento excluído com sucesso"
    }