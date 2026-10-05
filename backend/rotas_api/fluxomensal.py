from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import FluxoMensal
from esquema import FluxoMensalCreate, FluxoMensalResponse


router = APIRouter(
    prefix="/fluxo-mensal",
    tags=["Fluxo Mensal"]
)


# =========================================================
# CREATE
# =========================================================

@router.post(
    "/",
    response_model=FluxoMensalResponse
)
def criar_fluxo_mensal(
    fluxo: FluxoMensalCreate,
    db: Session = Depends(get_db)
):
    novo_fluxo = FluxoMensal(
        mes=fluxo.mes,
        ano=fluxo.ano,
        valor_original=fluxo.valor_original,
        total_entradas=fluxo.total_entradas,
        total_contas_fixas=fluxo.total_contas_fixas,
        total_contas_variaveis=fluxo.total_contas_variaveis,
        total_investimentos=fluxo.total_investimentos,
        valor_final=fluxo.valor_final
    )

    db.add(novo_fluxo)
    db.commit()
    db.refresh(novo_fluxo)

    return novo_fluxo


# =========================================================
# READ - Listar
# =========================================================

@router.get(
    "/",
    response_model=list[FluxoMensalResponse]
)
def listar_fluxos_mensais(
    db: Session = Depends(get_db)
):
    return db.query(FluxoMensal).all()


# =========================================================
# READ - Buscar por ID
# =========================================================

@router.get(
    "/{fluxo_id}",
    response_model=FluxoMensalResponse
)
def buscar_fluxo_mensal(
    fluxo_id: int,
    db: Session = Depends(get_db)
):
    fluxo = (
        db.query(FluxoMensal)
        .filter(FluxoMensal.id == fluxo_id)
        .first()
    )

    if not fluxo:
        raise HTTPException(
            status_code=404,
            detail="Fluxo mensal não encontrado"
        )

    return fluxo


# =========================================================
# UPDATE
# =========================================================

@router.put(
    "/{fluxo_id}",
    response_model=FluxoMensalResponse
)
def atualizar_fluxo_mensal(
    fluxo_id: int,
    fluxo_atualizado: FluxoMensalCreate,
    db: Session = Depends(get_db)
):
    fluxo = (
        db.query(FluxoMensal)
        .filter(FluxoMensal.id == fluxo_id)
        .first()
    )

    if not fluxo:
        raise HTTPException(
            status_code=404,
            detail="Fluxo mensal não encontrado"
        )

    fluxo.mes = fluxo_atualizado.mes
    fluxo.ano = fluxo_atualizado.ano
    fluxo.valor_original = fluxo_atualizado.valor_original
    fluxo.total_entradas = fluxo_atualizado.total_entradas
    fluxo.total_contas_fixas = fluxo_atualizado.total_contas_fixas
    fluxo.total_contas_variaveis = fluxo_atualizado.total_contas_variaveis
    fluxo.total_investimentos = fluxo_atualizado.total_investimentos
    fluxo.valor_final = fluxo_atualizado.valor_final

    db.commit()
    db.refresh(fluxo)

    return fluxo


# =========================================================
# DELETE
# =========================================================

@router.delete("/{fluxo_id}")
def excluir_fluxo_mensal(
    fluxo_id: int,
    db: Session = Depends(get_db)
):
    fluxo = (
        db.query(FluxoMensal)
        .filter(FluxoMensal.id == fluxo_id)
        .first()
    )

    if not fluxo:
        raise HTTPException(
            status_code=404,
            detail="Fluxo mensal não encontrado"
        )

    db.delete(fluxo)
    db.commit()

    return {
        "mensagem": "Fluxo mensal excluído com sucesso"
    }