"""Encrypts stored CPF values and adds a keyed lookup fingerprint."""
import re

import sqlalchemy as sa
from alembic import op

from dados_sensiveis import (
    criptografar_cpf,
    indice_cpf,
)


revision = "proteger_cpf"
down_revision = "normalizar_schema"
branch_labels = None
depends_on = None


def _coluna_existe(nome: str) -> bool:
    return any(
        column["name"] == nome
        for column in sa.inspect(op.get_bind()).get_columns("usuarios")
    )


def _preparar_cpf_legado(valor: str, usuario_id: int) -> str:
    cpf = re.sub(r"\D", "", valor)
    if len(cpf) != 11:
        raise RuntimeError(
            "Migração interrompida: CPF inválido no usuário "
            f"id={usuario_id}; corrija o registro sem expor o CPF."
        )
    return cpf


def upgrade() -> None:
    bind = op.get_bind()
    if not _coluna_existe("cpf_indice"):
        op.add_column(
            "usuarios",
            sa.Column("cpf_indice", sa.String(length=64), nullable=True),
        )

    with op.batch_alter_table("usuarios") as batch:
        batch.alter_column(
            "cpf",
            existing_type=sa.String(length=11),
            type_=sa.String(length=255),
            existing_nullable=False,
        )

    registros = bind.execute(
        sa.text(
            "SELECT id, cpf FROM usuarios "
            "WHERE cpf_indice IS NULL ORDER BY id"
        )
    ).all()
    fingerprints: dict[str, int] = {
        fingerprint: usuario_id
        for usuario_id, fingerprint in bind.execute(
            sa.text(
                "SELECT id, cpf_indice FROM usuarios "
                "WHERE cpf_indice IS NOT NULL"
            )
        ).all()
    }
    atualizacoes: list[dict[str, str | int]] = []
    for usuario_id, cpf_legado in registros:
        cpf = _preparar_cpf_legado(cpf_legado, usuario_id)
        fingerprint = indice_cpf(cpf)
        usuario_anterior = fingerprints.get(fingerprint)
        if usuario_anterior is not None:
            raise RuntimeError(
                "Migração interrompida: CPFs duplicados após normalização "
                f"nos usuários id={usuario_anterior} e id={usuario_id}."
            )
        fingerprints[fingerprint] = usuario_id
        atualizacoes.append(
            {
                "id": usuario_id,
                "cpf": criptografar_cpf(cpf),
                "cpf_indice": fingerprint,
            }
        )

    for atualizacao in atualizacoes:
        bind.execute(
            sa.text(
                "UPDATE usuarios SET cpf = :cpf, cpf_indice = :cpf_indice "
                "WHERE id = :id"
            ),
            atualizacao,
        )

    with op.batch_alter_table("usuarios") as batch:
        batch.alter_column(
            "cpf_indice",
            existing_type=sa.String(length=64),
            nullable=False,
        )
        constraints = sa.inspect(bind).get_unique_constraints("usuarios")
        if not any(
            item["name"] == "uq_usuarios_cpf_indice"
            for item in constraints
        ):
            batch.create_unique_constraint(
                "uq_usuarios_cpf_indice",
                ["cpf_indice"],
            )


def downgrade() -> None:
    raise RuntimeError(
        "Downgrade bloqueado para evitar regravar CPFs em texto puro. "
        "Para voltar a uma revisão anterior, restaure um backup protegido."
    )
