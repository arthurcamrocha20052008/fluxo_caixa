from datetime import date
from decimal import Decimal
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
from models import MetaFinanceira, Usuario
from esquema import (
    MetaFinanceiraCreate,
    MetaFinanceiraResponse
)
from autenticacao import obter_usuario_logado


router = APIRouter(
    prefix="/metas-financeiras",
    tags=["Metas Financeiras"]
)

StatusMeta = Literal["em_andamento", "concluida", "cancelada"]


def _determinar_status_meta(
    valor_atual: Decimal,
    valor_meta: Decimal,
    status_solicitado: StatusMeta,
) -> StatusMeta:
    if status_solicitado == "cancelada":
        return "cancelada"
    if valor_atual >= valor_meta:
        return "concluida"
    return "em_andamento"


# =========================================================
# CRIAR META
# =========================================================

@router.post(
    "/",
    response_model=MetaFinanceiraResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_meta(
    dados: MetaFinanceiraCreate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(obter_usuario_logado)
):

    status_meta = _determinar_status_meta(
        dados.valor_atual,
        dados.valor_meta,
        dados.status,
    )

    nova_meta = MetaFinanceira(
        usuario_id=usuario_logado.id,
        nome=dados.nome,
        valor_meta=dados.valor_meta,
        valor_atual=dados.valor_atual,
        data_inicio=dados.data_inicio,
        data_limite=dados.data_limite,
        status=status_meta,
        descricao=dados.descricao
    )

    db.add(nova_meta)
    db.commit()
    db.refresh(nova_meta)

    return nova_meta


# =========================================================
# LISTAR METAS DO USUÁRIO
# =========================================================

@router.get(
    "/",
    response_model=list[MetaFinanceiraResponse]
)
def listar_metas(
    status_meta: StatusMeta | None = Query(
        default=None,
        alias="status",
    ),
    data_inicio: date | None = None,
    data_limite: date | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(obter_usuario_logado)
):

    consulta = (
        db.query(MetaFinanceira)
        .filter(
            MetaFinanceira.usuario_id == usuario_logado.id
        )
    )
    if status_meta:
        consulta = consulta.filter(MetaFinanceira.status == status_meta)
    if data_inicio:
        consulta = consulta.filter(MetaFinanceira.data_inicio >= data_inicio)
    if data_limite:
        consulta = consulta.filter(
            MetaFinanceira.data_limite <= data_limite
        )
    return (
        consulta.order_by(MetaFinanceira.id)
        .offset(offset)
        .limit(limit)
        .all()
    )


# =========================================================
# BUSCAR META
# =========================================================

@router.get(
    "/{meta_id}",
    response_model=MetaFinanceiraResponse
)
def buscar_meta(
    meta_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(obter_usuario_logado)
):

    meta = (
        db.query(MetaFinanceira)
        .filter(
            MetaFinanceira.id == meta_id,
            MetaFinanceira.usuario_id == usuario_logado.id
        )
        .first()
    )

    if not meta:
        raise HTTPException(
            status_code=404,
            detail="Meta financeira não encontrada."
        )

    return meta


# =========================================================
# ATUALIZAR META
# =========================================================

@router.put(
    "/{meta_id}",
    response_model=MetaFinanceiraResponse
)
def atualizar_meta(
    meta_id: int,
    dados: MetaFinanceiraCreate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(obter_usuario_logado)
):

    meta = (
        db.query(MetaFinanceira)
        .filter(
            MetaFinanceira.id == meta_id,
            MetaFinanceira.usuario_id == usuario_logado.id
        )
        .first()
    )

    if not meta:
        raise HTTPException(
            status_code=404,
            detail="Meta financeira não encontrada."
        )

    meta.nome = dados.nome
    meta.valor_meta = dados.valor_meta
    meta.valor_atual = dados.valor_atual
    meta.data_inicio = dados.data_inicio
    meta.data_limite = dados.data_limite
    meta.status = _determinar_status_meta(
        dados.valor_atual,
        dados.valor_meta,
        dados.status,
    )
    meta.descricao = dados.descricao

    db.commit()
    db.refresh(meta)

    return meta


# =========================================================
# EXCLUIR META
# =========================================================

@router.delete(
    "/{meta_id}"
)
def excluir_meta(
    meta_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(obter_usuario_logado)
):

    meta = (
        db.query(MetaFinanceira)
        .filter(
            MetaFinanceira.id == meta_id,
            MetaFinanceira.usuario_id == usuario_logado.id
        )
        .first()
    )

    if not meta:
        raise HTTPException(
            status_code=404,
            detail="Meta financeira não encontrada."
        )

    db.delete(meta)
    db.commit()

    return {
        "mensagem": "Meta financeira excluída com sucesso."
    }