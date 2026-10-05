from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ContaVariavel
from esquema import ContaVariavelCreate, ContaVariavelResponse


router = APIRouter(
    prefix="/contas-variaveis",
    tags=["Contas Variáveis"]
)


# =========================================================
# CREATE
# =========================================================

@router.post(
    "/",
    response_model=ContaVariavelResponse
)
def criar_conta_variavel(
    conta: ContaVariavelCreate,
    db: Session = Depends(get_db)
):
    nova_conta = ContaVariavel(
        nome=conta.nome,
        valor=conta.valor,
        data_conta=conta.data_conta,
        categoria_id=conta.categoria_id,
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
    response_model=list[ContaVariavelResponse]
)
def listar_contas_variaveis(
    db: Session = Depends(get_db)
):
    return db.query(ContaVariavel).all()


# =========================================================
# READ - Buscar por ID
# =========================================================

@router.get(
    "/{conta_id}",
    response_model=ContaVariavelResponse
)
def buscar_conta_variavel(
    conta_id: int,
    db: Session = Depends(get_db)
):
    conta = (
        db.query(ContaVariavel)
        .filter(ContaVariavel.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta variável não encontrada"
        )

    return conta


# =========================================================
# UPDATE
# =========================================================

@router.put(
    "/{conta_id}",
    response_model=ContaVariavelResponse
)
def atualizar_conta_variavel(
    conta_id: int,
    conta_atualizada: ContaVariavelCreate,
    db: Session = Depends(get_db)
):
    conta = (
        db.query(ContaVariavel)
        .filter(ContaVariavel.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta variável não encontrada"
        )

    conta.nome = conta_atualizada.nome
    conta.valor = conta_atualizada.valor
    conta.data_conta = conta_atualizada.data_conta
    conta.categoria_id = conta_atualizada.categoria_id
    conta.observacao = conta_atualizada.observacao

    db.commit()
    db.refresh(conta)

    return conta


# =========================================================
# DELETE
# =========================================================

@router.delete("/{conta_id}")
def excluir_conta_variavel(
    conta_id: int,
    db: Session = Depends(get_db)
):
    conta = (
        db.query(ContaVariavel)
        .filter(ContaVariavel.id == conta_id)
        .first()
    )

    if not conta:
        raise HTTPException(
            status_code=404,
            detail="Conta variável não encontrada"
        )

    db.delete(conta)
    db.commit()

    return {
        "mensagem": "Conta variável excluída com sucesso"
    }