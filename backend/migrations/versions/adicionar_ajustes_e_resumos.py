"""Adiciona ajustes assinados e totais separados de transferências."""

import unicodedata

from alembic import op
import sqlalchemy as sa


revision = "ajustes_e_resumos"
down_revision = "categorias_movimentacao"
branch_labels = None
depends_on = None


CATEGORIAS_FIXAS = (
    "alimentacao",
    "ajuste",
    "compras",
    "contas",
    "educacao",
    "freelance",
    "impostos",
    "investimento",
    "lazer",
    "moradia",
    "outros",
    "salario",
    "saude",
    "transporte",
    "transferencia",
    "vendas",
)


def _normalizar_categoria(nome: str | None, tipo: str) -> str:
    if tipo == "transferencia":
        return "transferencia"

    if tipo == "ajuste":
        return "ajuste"

    decomposicao = unicodedata.normalize(
        "NFKD",
        (nome or "").strip().casefold(),
    )

    slug = "".join(
        caractere
        for caractere in decomposicao
        if not unicodedata.combining(caractere)
    )

    if slug == "investimentos":
        slug = "investimento"

    return slug if slug in CATEGORIAS_FIXAS else "outros"


def _normalizar_categorias_existentes() -> None:
    with op.batch_alter_table("fluxo_dinheiro") as batch_op:
        batch_op.drop_constraint(
            "fk_fluxo_categoria",
            type_="foreignkey",
        )

    connection = op.get_bind()

    categorias = sa.table(
        "categorias_movimentacao",
        sa.column("nome", sa.String(length=100)),
    )

    movimentos = sa.table(
        "fluxo_dinheiro",
        sa.column("id", sa.Integer()),
        sa.column("categoria", sa.String(length=100)),
        sa.column("tipo", sa.String(length=30)),
    )

    connection.execute(
        sa.delete(categorias)
    )

    op.bulk_insert(
        categorias,
        [{"nome": nome} for nome in CATEGORIAS_FIXAS],
    )

    registros = list(
        connection.execute(
            sa.select(
                movimentos.c.id,
                movimentos.c.categoria,
                movimentos.c.tipo,
            )
        ).mappings()
    )

    for registro in registros:
        connection.execute(
            sa.update(movimentos)
            .where(
                movimentos.c.id == registro["id"]
            )
            .values(
                categoria=_normalizar_categoria(
                    registro["categoria"],
                    registro["tipo"],
                )
            )
        )

    with op.batch_alter_table("fluxo_dinheiro") as batch_op:
        batch_op.create_foreign_key(
            "fk_fluxo_categoria",
            "categorias_movimentacao",
            ["categoria"],
            ["nome"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
        )


def upgrade() -> None:
    _normalizar_categorias_existentes()

    with op.batch_alter_table("fluxo_dinheiro") as batch_op:
        batch_op.alter_column(
            "tipo",
            existing_type=sa.Enum(
                "entrada",
                "saida",
                "transferencia",
            ),
            type_=sa.Enum(
                "entrada",
                "saida",
                "transferencia",
                "ajuste",
            ),
            existing_nullable=False,
        )

    for nome in (
        "total_transferencias_recebidas",
        "total_transferencias_enviadas",
        "total_ajustes",
    ):
        op.add_column(
            "calculos_financeiros",
            sa.Column(
                nome,
                sa.Numeric(12, 2),
                nullable=False,
                server_default="0.00",
            ),
        )


def downgrade() -> None:
    connection = op.get_bind()

    movimentos = sa.table(
        "fluxo_dinheiro",
        sa.column("tipo", sa.String(length=30)),
        sa.column("valor", sa.Numeric(12, 2)),
        sa.column("categoria", sa.String(length=100)),
    )

    connection.execute(
        sa.update(movimentos)
        .where(
            movimentos.c.tipo == "ajuste",
            movimentos.c.valor > 0,
        )
        .values(
            tipo="entrada",
            categoria="outros",
        )
    )

    connection.execute(
        sa.update(movimentos)
        .where(
            movimentos.c.tipo == "ajuste",
            movimentos.c.valor < 0,
        )
        .values(
            tipo="saida",
            valor=sa.func.abs(movimentos.c.valor),
            categoria="outros",
        )
    )

    for nome in (
        "total_ajustes",
        "total_transferencias_enviadas",
        "total_transferencias_recebidas",
    ):
        op.drop_column(
            "calculos_financeiros",
            nome,
        )

    with op.batch_alter_table("fluxo_dinheiro") as batch_op:
        batch_op.alter_column(
            "tipo",
            existing_type=sa.Enum(
                "entrada",
                "saida",
                "transferencia",
                "ajuste",
            ),
            type_=sa.Enum(
                "entrada",
                "saida",
                "transferencia",
            ),
            existing_nullable=False,
        )