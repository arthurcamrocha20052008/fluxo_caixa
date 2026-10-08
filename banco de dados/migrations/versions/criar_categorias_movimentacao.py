"""Cria categorias fixas e normaliza categorias das movimentações."""
import unicodedata

from alembic import op
import sqlalchemy as sa


revision = "categorias_movimentacao"
down_revision = "transferencias"
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
    nome = nome or ""
    decomposicao = unicodedata.normalize("NFKD", nome.strip().casefold())
    slug = "".join(
        caractere
        for caractere in decomposicao
        if not unicodedata.combining(caractere)
    )
    if slug == "investimentos":
        slug = "investimento"
    return slug if slug in CATEGORIAS_FIXAS else "outros"


def _popular_e_normalizar_categorias() -> None:
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
            .where(movimentos.c.id == registro["id"])
            .values(
                categoria=_normalizar_categoria(
                    registro["categoria"],
                    registro["tipo"],
                )
            )
        )


def upgrade() -> None:
    op.create_table(
        "categorias_movimentacao",
        sa.Column("nome", sa.String(length=100), primary_key=True),
    )
    _popular_e_normalizar_categorias()
    with op.batch_alter_table("fluxo_dinheiro") as batch_op:
        batch_op.create_foreign_key(
            "fk_fluxo_categoria",
            "categorias_movimentacao",
            ["categoria"],
            ["nome"],
            ondelete="RESTRICT",
            onupdate="CASCADE",
        )


def downgrade() -> None:
    with op.batch_alter_table("fluxo_dinheiro") as batch_op:
        batch_op.drop_constraint(
            "fk_fluxo_categoria",
            type_="foreignkey",
        )
    op.drop_table("categorias_movimentacao")